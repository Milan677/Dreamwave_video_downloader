from django.urls import path 
from .views import *

urlpatterns = [
    path('video/extract-metadata/',video_meta_view, name = 'extract-meta-views'),
    # path('video/',download_video, name='download-video'),
    path('video/download/',download_merged_video, name = 'download-and-merge-video'),

    #instagram
    path('instagram-video/extract-metadata/',video_meta_view_instagram, name = 'extract-meta-views'),
    path('instagram-video/download/', download_merged_video_instagram, name ='download-instagram-reels'),
]