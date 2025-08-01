from django.db import models

# Create your models here.
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, default='')
    category = models.CharField(max_length=32, blank=True, default='')

    def __str__(self):
        return f"Image {self.id}"
