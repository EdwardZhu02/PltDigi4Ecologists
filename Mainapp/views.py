from django.shortcuts import render, redirect
from .models import UploadedImage
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
import json
import os
from django.conf import settings

class HomeView(View):
    def get(self, request: HttpRequest):
        return render(request, 'home.html')

    def post(self, request: HttpRequest):
        # Handle any form submissions or data processing here
        return redirect('upload_image')

class UploadImageView(View):
    def get(self, request: HttpRequest):
        return render(request, 'upload_image.html')

    def post(self, request: HttpRequest):
        image_file = request.FILES.get('image')
        if image_file:
            fs = FileSystemStorage(location='uploaded_images/')
            filename = fs.save(image_file.name, image_file)
            uploaded_image = UploadedImage.objects.create(image=filename)
            # Jump to manage page after upload
            return redirect(reverse('manage_figures'))
        return render(request, 'upload_image.html')

class InteractiveView(View):
    def get(self, request: HttpRequest, image_id: int):
        try:
            uploaded_image = UploadedImage.objects.get(id=image_id)
            # load existing analysis JSON if present
            analysis_dir = os.path.join(settings.BASE_DIR, 'analysis_results')
            json_path = os.path.join(analysis_dir, f'figure_{image_id}.json')
            existing_analysis = {}
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    existing_analysis = json.load(f)
            # Load the appropriate template based on the category
            if uploaded_image.category == 'barplot':
                template_name = 'interactive_barplot.html'
            else:
                template_name = 'interactive_scatter.html'
            return render(request, template_name, {
                'uploaded_image': uploaded_image,
                'existing_analysis': existing_analysis
            })
        except UploadedImage.DoesNotExist:
            return redirect('upload_image')

    def post(self, request: HttpRequest, image_id: int):
        try:
            data = json.loads(request.body)
            # handle save results
            if data.get('saveResults'):
                analysis_dir = os.path.join(settings.BASE_DIR, 'analysis_results')
                os.makedirs(analysis_dir, exist_ok=True)
                json_path = os.path.join(analysis_dir, f'figure_{image_id}.json')
                with open(json_path, 'w') as f:
                    json.dump({'calibration': data.get('calibration', []), 'extractedData': data.get('extractedData', [])}, f)
                return JsonResponse({'status': 'success', 'message': 'Analysis saved'})
            # calibration and extracted handling unchanged
            if 'calibration' in data:
                # Handle calibration data
                calibration_data = data['calibration']
                print("Calibration data received:", calibration_data)
                return JsonResponse({'status': 'success', 'message': 'Calibration data processed'})

            if 'extractedData' in data:
                # Handle extracted data points
                extracted_data = data['extractedData']
                print("Extracted data received:", extracted_data)
                return JsonResponse({'status': 'success', 'message': 'Extracted data processed'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

class ManageFiguresView(View):
    def get(self, request: HttpRequest):
        figures = UploadedImage.objects.all()
        return render(request, 'manage_figures.html', {'figures': figures})

    def post(self, request: HttpRequest):
        data = json.loads(request.body)
        if data.get('delete_id'):
            fid = data['delete_id']
            try:
                figure = UploadedImage.objects.get(id=fid)
                # Delete the figure file
                if figure.image:
                    figure.image.delete(save=False)
                # Remove associated JSON file
                analysis_dir = os.path.join(settings.BASE_DIR, 'analysis_results')
                json_path = os.path.join(analysis_dir, f'figure_{fid}.json')
                if os.path.exists(json_path):
                    os.remove(json_path)
                # Delete the database record
                figure.delete()
                return JsonResponse({'status': 'success', 'message': 'Figure and its analysis deleted successfully'})
            except UploadedImage.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Figure not found'}, status=404)
        elif data.get('figure_id'):
            fid = data['figure_id']
            note = data.get('note', None)
            category = data.get('category', None)
            try:
                figure = UploadedImage.objects.get(id=fid)
                if note is not None:
                    figure.note = note
                if category is not None:
                    figure.category = category
                figure.save()
                return JsonResponse({'status': 'success', 'message': 'Note/Category updated'})
            except UploadedImage.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Figure not found'}, status=404)
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
