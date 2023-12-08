import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import sys
import json
import time
import requests
from moviepy.editor import *
url = "http://localhost:6975"
dlurl=input("YouTubeURL: ")
mp4flile=""
service = Service(executable_path="msedgedriver.exe")
driver = webdriver.Edge(service=service)
driver.get(f'{dlurl}')
f = open('myfile.html', 'w', encoding='utf-8')
print(driver.page_source)
f.write(driver.page_source)
f.close()
data = open('myfile.html', 'r', encoding='UTF-8').read()
if not data.rfind('"icon":"UNKNOWN"}'):
    print("Most played not found")
    sys.exit()
print(data[data.find('"markerType":"MARKER_TYPE_HEATMAP"')+35:data.rfind('"icon":"UNKNOWN"}')+19])
f = open('myfile.json', 'w', encoding='utf-8')
f.write("{"+data[data.find('"markerType":"MARKER_TYPE_HEATMAP"')+35:data.rfind('"icon":"UNKNOWN"}')+19]+"}")
f.close()
f= open("myfile.json", "r", encoding='utf-8')
jsonfile= json.load(f)
for i in jsonfile["markersDecoration"]["timedMarkerDecorations"]:
    print(i["decorationTimeMillis"])
#1s=1000ms
editime=jsonfile["markersDecoration"]["timedMarkerDecorations"][0]["decorationTimeMillis"]#msec
f.close()
editime/=1000#sec

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
    check()
    if check()[0]=="done":
        print(check())
        mp4flile=extracturl(check()[1])
        break
    time.sleep(2)
start = editime # 開始時刻
end = editime+60 # 終了時刻

video=VideoFileClip(mp4flile+".mp4")
print(video.end)
if end<=video.end:
    end=video.end
final_clip = video.subclip(start, end)
final_clip.write_videofile(f"{mp4flile}most.mp4",)
