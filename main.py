import re
import http.client
import logging
import socket
from urllib.request import Request, urlopen
import sys
import json
import time
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid
import moviepy.video.fx.resize as resize_vid
import pytubefix
import os

dlurl = input("YouTubeURL: ")


def _execute_request(
    url, method=None, headers=None, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT
):
    base_headers = {"User-Agent": "Mozilla/5.0", "accept-language": "en-US,en"}
    if headers:
        base_headers.update(headers)
    if data:
        # encode data for request
        if not isinstance(data, bytes):
            data = bytes(json.dumps(data), encoding="utf-8")
    if url.lower().startswith("http"):
        request = Request(url, headers=base_headers, method=method, data=data)
    else:
        raise ValueError("Invalid URL")
    return urlopen(request, timeout=timeout)  # nosec


def get(url, extra_headers=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
    if extra_headers is None:
        extra_headers = {}
    response = _execute_request(url, headers=extra_headers, timeout=timeout)
    return response.read().decode("utf-8")


data = get(dlurl)
a = (
    "{"
    + data[
        data.find('"markerType":"MARKER_TYPE_HEATMAP"')
        + 35 : data.rfind('"icon":"UNKNOWN"}')
        + 19
    ]
    + "}"
)
a = json.loads(a)
# print(a)
print(a["markersDecoration"])
try:
    for i in a["markersDecoration"]["timedMarkerDecorations"]:
        print(i["decorationTimeMillis"])
except:
    print("Most played not found")
    sys.exit()
# 1s=1000ms
mosttime = a["markersDecoration"]["timedMarkerDecorations"]

youtube = pytubefix.YouTube(dlurl)
mp4flile = youtube.video_id
title = youtube.title
title = (
    title.replace("/", "")
    .replace('"', "")
    .replace("*", "")
    .replace(":", "")
    .replace("|", "")
)
youtube.streams.filter(only_video=True, mime_type="video/mp4").order_by(
    "resolution"
).last().download(filename=mp4flile + ".mp4")
youtube.streams.get_audio_only().download(filename=mp4flile + "-audio.mp3")
videoclip = VideoFileClip(mp4flile + ".mp4")
audioclip = AudioFileClip(mp4flile + "-audio.mp3")
video = videoclip.set_audio(audioclip)
count = 0
for i in mosttime:
    i = i["decorationTimeMillis"]
    edittime = i / 1000  # sec
    start = edittime  # 開始時刻
    end = edittime + 59  # 終了時刻
    print(video.end)
    if end >= video.end:
        end = video.end
    final_clip = video.subclip(start, end)
    w, h = final_clip.size
    target_ratio = 1080 / 1920
    current_ratio = w / h
    if current_ratio > target_ratio:
        # The video is wider than the desired aspect ratio, crop the width
        new_width = int(h * target_ratio)
        x_center = w / 2
        y_center = h / 2
        final_clip = crop_vid.crop(
            final_clip, width=new_width, height=h, x_center=x_center, y_center=y_center
        )
    else:
        # The video is taller than the desired aspect ratio, crop the height
        new_height = int(w / target_ratio)
        x_center = w / 2
        y_center = h / 2
        final_clip = crop_vid.crop(
            final_clip, width=w, height=new_height, x_center=x_center, y_center=y_center
        )
    # Write the final video
    if mp4flile[0] == "-":
        mp4flile = mp4flile.replace(mp4flile[0], "(dash)", 1)
    final_clip = resize_vid.resize(final_clip, width=1080, height=1920)
    final_clip.write_videofile(f"{title}-most{count}.mp4", fps=30, remove_temp=True)
    count = count + 1
os.remove(mp4flile + ".mp4")
os.remove(mp4flile + "-audio.mp3")
