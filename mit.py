import re
import requests
import json
from mitmproxy import ctx, http
import uuid
import re
import os.path as path
from concurrent.futures import ThreadPoolExecutor
from traceback import print_exc
import os
import time

pools = ThreadPoolExecutor(16)

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi K30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36"
}

def download(base_url: str, sub_list: list, name: str):
    f = open(f"videos/{name}", 'wb')
    for sub in sub_list:
        response = requests.get(base_url + sub, headers=headers)
        print(f"Donwloads: {base_url + sub}, Status: {response.status_code}")
        if response.status_code != 200:
            f.close()
            os.remove(f"videos/{name}")
            print("Download failed!")
            return 
        f.write(response.content)
    f.close()
    
def response(flow: http.HTTPFlow):
    if 'proxyhttp' in flow.request.url:
        print("URL:", flow.request.url)
        data = json.loads(flow.response.content.decode())
        if 'vinfo' in data:
            try:
                vinfo = json.loads(data['vinfo'])
                url = vinfo['vl']['vi'][0]['ul']['ui'][0]['url']
                m3u8 = vinfo['vl']['vi'][0]['ul']['m3u8']
                sub_list = re.sub('#EX.*', '', m3u8).split()
                base_url = re.sub('gzc.*', '', url)
                # name = vinfo['vl']['vi'][0]['vid'] + '.ts'
                name = vinfo['vl']['vi'][0]['ti'] + '.ts'
            except :
                print_exc()
                return
            
            if path.exists(f"videos/{name}"):
                print(f"Exist {name}!")
            else:
                pools.submit(download, base_url, sub_list, name)

def request(flow: http.HTTPFlow):
    if 'proxyhttp' in flow.request.url:
        flow.request.headers.pop('Accept-Encoding')
        
        
