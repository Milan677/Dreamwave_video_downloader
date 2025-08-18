from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import get_client_ip

from .models import *
from .serializers import *

import yt_dlp
from urllib.parse import urlparse

import os
import re
import uuid
import tempfile
import subprocess
from django.http import FileResponse



# Create your views here.

# @api_view(['POST'])
# def video_meta_view(request):
#     url = request.data.get("url")
#     if not url:
#         return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         ydl_opts = {
#             'quiet': True,
#             'skip_download': True,
#             'nocheckcertificate': True  # <== This disables SSL verification
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=False)
#             print("====================")
#             print(info['formats'])
#             print("=====================")
#             formats = [
#                 {
#                     'format_id': fmt['format_id'],
#                     'resolution': fmt.get('format_note') or fmt.get('height'),
#                     'ext': fmt['ext'],
#                     'filesize': fmt.get('filesize')
#                 }
#                 for fmt in info['formats'] if fmt.get('height')
#             ]
#             return Response({
#                 'title': info['title'],
#                 'thumbnail': info.get('thumbnail'),
#                 'available_formats': formats
#             })
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def download_video(request):
#     url = request.data.get("url")
#     if not url:
#         return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

#     format_id = request.data.get('format_id')
#     platform = request.data.get('platform')

#     ip_address =   get_client_ip(request)

#     try:
#             ydl_opts = {
#                     'format': format_id,
#                     'outtmpl': f'downloads/%(title)s.%(ext)s',
#                     'nocheckcertificate': True  # <== This disables SSL verification
#                 }

#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(url, download=True)
#                 history = DownloadHistory.objects.create(
#                     video_url=url,
#                     platform=platform,
#                     resolution=format_id,
#                     ip_address=ip_address
#                 )
#             return Response({'message': 'Download started', 'title': info['title']})
#     except Exception as e:
#         return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)    





# @api_view(['POST'])
# def video_meta_view(request):
#     url = request.data.get("url")
#     if not url:
#         return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         ydl_opts = {
#             'quiet': True,
#             'skip_download': True,
#             'nocheckcertificate': True,
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=False)

#             best_audio = None
#             best_audio_bitrate = 0

#             # Find best audio-only stream
#             for fmt in info['formats']:
#                 if fmt.get('vcodec') == 'none' and fmt.get('acodec') != 'none':
#                     abr = fmt.get('abr') or 0
#                     if abr > best_audio_bitrate:
#                         best_audio = fmt
#                         best_audio_bitrate = abr

#             # Prepare video formats
#             video_formats = []
#             for fmt in info['formats']:
#                 if fmt.get('vcodec') != 'none':
#                     video_formats.append({
#                         'format_id': fmt['format_id'],
#                         'resolution': fmt.get('format_note') or f"{fmt.get('height')}p",
#                         'ext': fmt['ext'],
#                         'filesize': f"{(fmt.get('filesize') or 0)/1024/1024:.2f} MB" if fmt.get('filesize') else None,
#                         'audio_format_id': best_audio['format_id'] if best_audio else None,
#                         'combined_av': fmt.get('acodec') != 'none',
#                     })

#             return Response({
#                 'title': info.get('title'),
#                 'thumbnail': info.get('thumbnail'),
#                 'video_formats': video_formats,
#                 'best_audio_format_id': best_audio['format_id'] if best_audio else None
#             })

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# 2.

# @api_view(['POST'])
# def video_meta_view(request):
#     url = request.data.get("url")
#     if not url:
#         return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         ydl_opts = {
#             'quiet': True,
#             'skip_download': True,
#             'nocheckcertificate': True,
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=False)

#             # Separate formats
#             video_formats = []
#             audio_formats = []

#             for fmt in info['formats']:
#                 has_video = fmt.get('vcodec', 'none') != 'none'
#                 has_audio = fmt.get('acodec', 'none') != 'none'
#                 is_dash = fmt.get('format_id', '').startswith('dash')

#                 # Common metadata
#                 format_info = {
#                     'format_id': fmt['format_id'],
#                     'ext': fmt['ext'],
#                     'resolution': fmt.get('format_note') or f"{fmt.get('height', '')}p",
#                     'filesize_bytes': fmt.get('filesize'),
#                     'filesize': f"{(fmt.get('filesize') or 0)/1024/1024:.2f} MB" if fmt.get('filesize') else None,
#                     'video_codec': fmt.get('vcodec'),
#                     'audio_codec': fmt.get('acodec'),
#                 }

#                 if has_video and not has_audio:
#                     video_formats.append(format_info)
#                 elif has_audio and not has_video:
#                     audio_formats.append(format_info)
#                 elif has_video and has_audio:
#                     # Some formats contain both, keep them too
#                     format_info['combined_av'] = True
#                     video_formats.append(format_info)

#             return Response({
#                 'title': info.get('title'),
#                 'thumbnail': info.get('thumbnail'),
#                 'video_formats': video_formats,
#                 'audio_formats': audio_formats,
#                 'is_merge_required': True  # Let frontend know merging is needed
#             })

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def download_merged_video(request):
#     url = request.data.get("url")
#     video_format_id = request.data.get("video_format_id")
#     audio_format_id = request.data.get("audio_format_id")

#     if not url or not video_format_id or not audio_format_id:
#         return Response({'error': 'url, video_format_id, and audio_format_id are required'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         temp_dir = tempfile.mkdtemp()
#         video_file = os.path.join(temp_dir, f"video_{uuid.uuid4()}.mp4")
#         audio_file = os.path.join(temp_dir, f"audio_{uuid.uuid4()}.m4a")
#         output_file = os.path.join(temp_dir, f"merged_{uuid.uuid4()}.mp4")

#         # Download video
#         video_opts = {
#             'quiet': True,
#             'outtmpl': video_file,
#             'format': video_format_id,
#             'nocheckcertificate': True,
#         }
#         with yt_dlp.YoutubeDL(video_opts) as ydl:
#             # ydl.download([url])
#             info = ydl.extract_info(url, download=True)

#         # Download audio
#         audio_opts = {
#             'quiet': True,
#             'outtmpl': audio_file,
#             'format': audio_format_id,
#             'nocheckcertificate': True,
#         }
#         with yt_dlp.YoutubeDL(audio_opts) as ydl:
#             # ydl.download([url])
#             info = ydl.extract_info(url, download=True)

#         # Merge video and audio using ffmpeg
#         merge_cmd = [
#             'ffmpeg',
#             '-i', video_file,
#             '-i', audio_file,
#             '-c:v', 'copy',
#             '-c:a', 'aac',
#             '-strict', 'experimental',
#             '-y',  # Overwrite if exists
#             output_file
#         ]
#         subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

#         # Serve the merged file for download
#         filename = os.path.basename(output_file)
#         response = FileResponse(open(output_file, 'rb'), as_attachment=True, filename=filename)

#         return response

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 3.

@api_view(['POST'])
def video_meta_view(request):
    url = request.data.get("url")
    if not url:
        return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if the URL belongs to YouTube
    parsed_url = urlparse(url)
    allowed_domains = ["youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com"]

    if parsed_url.netloc not in allowed_domains:
        return Response(
            {"error": "Only YouTube URLs are supported."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'nocheckcertificate': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            # Collect available resolutions from formats with video
            resolutions = set()
            for fmt in info['formats']:
                if fmt.get('vcodec', 'none') != 'none' and fmt.get('height'):
                    resolutions.add(f"{fmt['height']}p")

            return Response({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'available_resolutions': sorted(list(resolutions), reverse=True),
                'is_merge_required': False  # yt-dlp handles merging
            })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



def sanitize_filename(title):
    # Remove invalid characters for filenames
    return re.sub(r'[\\/*?:"<>|]', "_", title)


@api_view(['GET', 'POST'])
def download_merged_video(request):
    # url = request.data.get("url")
    # resolution = request.data.get("resolution")  # e.g. "720p"

    if request.method == 'GET':
        url = request.query_params.get("url")
        resolution = request.query_params.get("resolution")
    else:
        url = request.data.get("url")
        resolution = request.data.get("resolution")

    if not url or not resolution:
        return Response({'error': 'url and resolution are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        height = resolution.replace("p", "")
        format_string = f"bestvideo[height={height}]+bestaudio"

        temp_dir = tempfile.mkdtemp()

        # Extract video metadata
        info_opts = {
            'quiet': True,
            'skip_download': True,
            'nocheckcertificate': True,
        }

        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', f"video_{uuid.uuid4()}")
            safe_title = sanitize_filename(title)[:50]  # limit length

        # sanitized title in filename
        output_file = os.path.join(temp_dir, f"{safe_title}.mp4")

        ydl_opts = {
            'format': format_string,
            'outtmpl': output_file,
            'merge_output_format': 'mp4',
            'quiet': True,
            'nocheckcertificate': True,
            'prefer_ffmpeg': True,
            'postprocessors': [
                {
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4'
                }
            ]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        response = FileResponse(open(output_file, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_file)}"'
        return response

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# @api_view(['POST'])
# def download_merged_video(request):
#     url = request.data.get("url")
#     resolution = request.data.get("resolution")  # e.g. "720p"

#     if not url or not resolution:
#         return Response({'error': 'url and resolution are required'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # Remove "p" to get height (e.g., "720p" -> "720")
#         height = resolution.replace("p", "")
#         format_string = f"bestvideo[height={height}]+bestaudio"

#         temp_dir = tempfile.mkdtemp()
#         output_file = os.path.join(temp_dir, f"merged_{uuid.uuid4()}.mp4")

#         ydl_opts = {
#             'format': format_string,
#             'outtmpl': output_file,
#             'merge_output_format': 'mp4',
#             'quiet': True,
#             'nocheckcertificate': True,
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])

#         filename = os.path.basename(output_file)
#         response = FileResponse(open(output_file, 'rb'), as_attachment=True, filename=filename)
#         return response

#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#.......... instagram and facebook ............................

from urllib.parse import urlparse

@api_view(['POST'])
def video_meta_view_instagram(request):
    url = request.data.get("url")
    if not url:
        return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Basic platform detection
        hostname = urlparse(url).hostname or ""
        platform = "instagram" if "instagram" in hostname else "youtube"

        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'nocheckcertificate': True,
            'cookiefile': 'cookies.txt' if platform == "instagram" else None,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            resolutions = set()
            for fmt in info['formats']:
                if fmt.get('vcodec', 'none') != 'none' and fmt.get('height'):
                    resolutions.add(f"{fmt['height']}p")

            return Response({
                'platform': platform,
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'available_resolutions': sorted(list(resolutions), reverse=True),
                'is_merge_required': True  # Instagram formats may still need merging
            })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def download_merged_video_instagram(request):
    if request.method == 'GET':
        url = request.query_params.get("url")
        resolution = request.query_params.get("resolution")
    else:
        url = request.data.get("url")
        resolution = request.data.get("resolution")

    if not url or not resolution:
        return Response({'error': 'url and resolution are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        height = resolution.replace("p", "")
        # format_string = f"bestvideo[height={height}]+bestaudio"

        temp_dir = tempfile.mkdtemp()

        info_opts = {
            'quiet': True,
            'skip_download': True,
            'nocheckcertificate': True,
        }

        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', f"video_{uuid.uuid4()}")
            safe_title = sanitize_filename(title)[:50]

        output_file = os.path.join(temp_dir, f"{safe_title}.mp4")

        ydl_opts = {
            'format': 'best',
            'outtmpl': output_file,
            'merge_output_format': 'mp4',
            'quiet': True,
            'nocheckcertificate': True,
        }

        # Add cookies if Instagram
        if "instagram" in url:
            ydl_opts['cookiefile'] = 'cookies.txt'  # make sure this file exists!

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        response = FileResponse(open(output_file, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_file)}"'
        return response

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#...................... Instagram ...................................

