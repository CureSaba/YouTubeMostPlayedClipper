import re
import socket
from urllib.request import Request, urlopen
import json

dlurl = input("YouTubeURL: ")
class (url):
    def __init__:
    def _execute_request(url, method=None, headers=None, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
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

    def list(self):
        data = get(dlurl)
        a = ("{" + data[data.find('"markerType":"MARKER_TYPE_HEATMAP"') + 35 : data.rfind('"icon":"UNKNOWN"}') + 19] + "}")
        a = json.loads(a)
        b = []
        try:
            for i in a["markersDecoration"]["timedMarkerDecorations"]:
                b.append(i["decorationTimeMillis"] / 1000)# 1s=1000ms
            return(b)
        except:
            raise NotFound("Most played not found")
        
