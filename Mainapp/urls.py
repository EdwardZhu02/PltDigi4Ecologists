#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：pltdigi4ecologists 
@File    ：urls.py.py
@Author  ：Edward Zhu, zhuyzh37@mail2.sysu.edu.cn
@Date    ：2025/08/01 12:56 
@IDE     ：PyCharm 
-----------------------------
Description:
Input:
Output:

One-line usage note: python3 urls.py.py ,
- ARG1:

Environment requirement (if any): base
- Dependencies: None
-----------------------------
Notes:

-----------------------------
File Revisions:
    2025/08/01: Version 1 - Creation
"""
from django.urls import path
from Mainapp.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('upload', UploadImageView.as_view(), name='upload_image'),
    path('manage', ManageFiguresView.as_view(), name='manage_figures'),
    path('interactive/<int:image_id>', InteractiveView.as_view(), name='interactive_view'),
]
