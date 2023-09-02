import re
import requests
import json
from mitmproxy import ctx, http
import uuid
import re
import os.path as path
from concurrent.futures import ThreadPoolExecutor
import threading
from traceback import print_exc
import os
import time
from log import Log
from urllib.parse import urlparse, unquote, parse_qs

pools = ThreadPoolExecutor(16)
lock = threading.Lock()
now = time.strftime("%Y_%m_%d", time.localtime())
print = Log(f"logs/DOWNLOAD_{now}.log").print

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi K30 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36"
}


def split_url(url: str):
    url = urlparse(url)
    return url.scheme + "://" + url.netloc + url.path.rsplit('/', 1)[0] + '/'
    
def download(base_urls: str, sub_list: list, name: str, vinfo: dict=None):
    for base_url in base_urls:
        f = open(f"videos/{name}", 'wb')
        for sub in sub_list:
            response = requests.get(base_url + sub, headers=headers)
            print(f"Donwloads {name}: Status: {response.status_code}, {base_url + sub}")
            if response.status_code != 200:
                f.close()
                os.remove(f"videos/{name}")
                print(f"Download failed: {name}!")
                print("Vinfo:")
                print(json.dumps(vinfo, ensure_ascii=False))
                break 
            f.write(response.content)
        else:
            f.close()
            return
    return

def response(flow: http.HTTPFlow):
    if 'proxyhttp' in flow.request.url:
        print("URL:", flow.request.url)
        data = json.loads(flow.response.content.decode())
        if 'vinfo' in data:
            try:
                vinfo = json.loads(data['vinfo'])
                url = vinfo['vl']['vi'][0]['ul']['ui'][0]['url']
                urls = [i['url'] for i in vinfo['vl']['vi'][0]['ul']['ui']]
                m3u8 = vinfo['vl']['vi'][0]['ul']['m3u8']
                sub_list = re.sub('#EX.*', '', m3u8).split()
                base_url = re.sub('gzc.*', '', url)
                base_urls = [split_url(i) for i in urls]
                print("Base urls:", *base_urls, sep="\n")
                # name = vinfo['vl']['vi'][0]['vid'] + '.ts'
                name = vinfo['vl']['vi'][0]['ti'] + '.ts'
            except :
                print("解析数据失败!")
                print("Vinfo:")
                print(data)
                print_exc()
                return
            
            if path.exists(f"videos/{name}"):
                print(f"Exist {name}!")
            else:
                pools.submit(download, base_urls, sub_list, name, vinfo)

def request(flow: http.HTTPFlow):
    if 'proxyhttp' in flow.request.url:
        flow.request.headers.pop('Accept-Encoding')
        
        
