#!/usr/bin/env python3

#wget https://audio.qingting.fm/audiostream/redirect/237072/8397875\?authuser\=\&device_id\=MOBILESITE\&qingting_id\=\&t\=1574391722266\&sign\=3bf54005527dcea897ee8a12187f80b8 -O xx

import sys
import os
from urllib.parse import quote
import hmac
import time
import requests

#channel = 237072
channel = int(sys.argv[1])

key = b'fpMn12&38f_2e'

url = "https://i.qingting.fm/capi/v3/channel/%d?user_id=null"%channel
r = requests.get(url)
version = r.json()['data']['v']

curpage = 1

while True:
    url = "https://i.qingting.fm/capi/channel/%d/programs/%s?curpage=%d&pagesize=30&order=asc"%(channel,version, curpage)
    r = requests.get(url).json()
    if 'data' not in r:
        break
    
    programs = r['data']['programs']
    curpage = curpage + 1
    #print(programs)

    for program in programs:
        program_id = program['id']
        program_name = program['title']
        #print(program_id, program_name)
        child_url="/audiostream/redirect/%d/%d?authuser=&device_id=MOBILESITE&qingting_id=&t=%d"%(channel, program_id, time.time())
        #print(child_url)
        h=hmac.new(key, digestmod='md5')
        h.update(child_url.encode('utf-8'))
        url= "https://audio.qingting.fm" + child_url + "&sign=%s"%h.hexdigest()
        os.system("wget -O %s.m4a \"%s\""%(program_name, url))
