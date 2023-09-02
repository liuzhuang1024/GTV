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
from log import Log

opt = argparse.ArgumentParser()
opt.add_argument('--url', type=str, default='https://v.qq.com/x/cover/2iqrhqekbtgwp1s/p00347dsmqv.html')
args = opt.parse_args()

now = time.strftime("%Y_%m_%d", time.localtime())
print = Log(f"logs/SCAN_{now}.log").print

options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:\Users\Pencil\AppData\Local\Google\Chrome\User Data')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
browser = webdriver.Chrome(options=options)

url = urlparse(args.url)
url_base, cid, vid = url.path.strip('.html').rsplit('/', 2)
new_url = "https://" + url.netloc + url_base + '/' + cid + '.html'
print(new_url)
browser.get(new_url)   

vids = re.findall("data-vid=\"(.*?)\"", browser.page_source)
vids = list(set(vids))
print("All vids:", *vids, sep="\n")

for vid in vids[:]:
    new_url = "https://" + url.netloc + url_base + '/' + cid + '/' + vid + '.html'
    browser.get(new_url)
    print(browser.title, new_url)
    time.sleep(10)
browser.quit()