import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import sys
import json
import time
import requests
from moviepy.editor import *
import moviepy.video.fx.crop as crop_vid
import moviepy.video.fx.resize as resize_vid
url = "http://localhost:6975"
dlurl=input("YouTubeURL: ")
mp4flile=""
service = Service(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service)
driver.get(f'{dlurl}')
f = open('myfile.html', 'w', encoding='utf-8')
print(driver.page_source)
f.write(driver.page_source)
driver.close()
f.close()
data = open('myfile.html', 'r', encoding='UTF-8').read()
print(data[data.find('"markerType":"MARKER_TYPE_HEATMAP"')+35:data.rfind('"icon":"UNKNOWN"}')+19])
f = open('myfile.json', 'w', encoding='utf-8')
f.write("{"+data[data.find('"markerType":"MARKER_TYPE_HEATMAP"')+35:data.rfind('"icon":"UNKNOWN"}')+19]+"}")
f.close()
f= open("myfile.json", "r", encoding='utf-8')
jsonfile= json.load(f)
try:
    for i in jsonfile["markersDecoration"]["timedMarkerDecorations"]:
        print(i["decorationTimeMillis"])
except:
    print("Most played not found")
    sys.exit()
#1s=1000ms
mosttime=jsonfile["markersDecoration"]["timedMarkerDecorations"]

payload = {"input": f"{dlurl}"}
headers = {"Content-Type": "application/json"}
response = requests.request("POST", url+"/download", json=payload, headers=headers)
print(response.json())

def check():
    response = requests.request("GET", url+"/items")
    #print(response.json())
    return response.json()["items"][0]["label_color"],response.json()["items"][0]["url"]

def extracturl(input_text):
    pattern = re.compile(r"https://www\.youtube\.com/watch\?v=(.*)")
    return pattern.match(input_text).group(1)

while True:
    if check()[0]=="done":
        print(check())
        mp4flile=extracturl(check()[1])
        break
    time.sleep(2)
video=VideoFileClip(mp4flile+".mp4")
count=0
for i in mosttime:
    i=i["decorationTimeMillis"]
    edittime=i/1000#sec
    start = edittime # 開始時刻
    end = edittime+59 # 終了時刻
    print(video.end)
    if end>=video.end:
        end=video.end
    final_clip = video.subclip(start, end)
    w, h = final_clip.size
    target_ratio = 1080 / 1920
    current_ratio = w / h
    if current_ratio > target_ratio:
        # The video is wider than the desired aspect ratio, crop the width
        new_width = int(h * target_ratio)
        x_center = w / 2
        y_center = h / 2
        final_clip = crop_vid.crop(final_clip, width=new_width, height=h, x_center=x_center, y_center=y_center)
    else:
        # The video is taller than the desired aspect ratio, crop the height
        new_height = int(w / target_ratio)
        x_center = w / 2
        y_center = h / 2
        final_clip = crop_vid.crop(final_clip, width=w, height=new_height, x_center=x_center, y_center=y_center)
    # Write the final video
    if mp4flile[0]=="-":
        mp4flile=mp4flile.replace(mp4flile[0], "(dash)", 1)
    final_clip=resize_vid.resize(final_clip, width=1080, height=1920)
    final_clip.write_videofile(f"{mp4flile}-most{count}.mp4")
    count=count+1
try:
    pass
except:
    pass
