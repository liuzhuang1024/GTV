import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import re
import requests
import json
import argparse
import shutil
import os
from urllib.parse import urlparse, unquote, parse_qs
from traceback import print_exc

opt = argparse.ArgumentParser()
opt.add_argument('--url', type=str, default='https://v.qq.com/x/cover/mzc00200n53vkqc/s0047v8o3mf.html')
args = opt.parse_args()

options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:\Users\Pencil\AppData\Local\Google\Chrome\User Data')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome(options=options)

url = urlparse(args.url)
url_base, cid, vid = url.path.strip('.html').rsplit('/', 2)
new_url = "https://" + url.netloc + url_base + '/' + cid + '/' + vid + '.html'
browser.get(new_url)   

vids = re.findall("data-vid=\"(.*?)\"", browser.page_source)
vids = list(set(vids))
print("All vids:\n", vids)

for vid in vids[:]:
    new_url = "https://" + url.netloc + url_base + '/' + cid + '/' + vid + '.html'
    browser.get(new_url)
    time.sleep(10)
    try:
        src = f'videos/{cid}-{vid}.ts'
        tgt = f'videos/{browser.title}.ts'
        print(new_url, src, tgt)
        if os.path.exists(tgt): os.remove(tgt)
        if not os.path.exists(src): continue
        os.link(os.path.abspath(src), os.path.abspath(tgt))
    except :
        print_exc()
            
browser.quit()