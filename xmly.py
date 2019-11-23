#!/usr/bin/env python3

import sys
import os
import requests

HEADERS={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

album_id = int(sys.argv[1])

curpage = 1
while True:
    url = "https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=%d&pageNum=%d&sort=0"%(album_id, curpage)
    curpage = curpage + 1
    r = requests.get(url, headers=HEADERS).json()
    tracks = r['data']['tracks']
    if len(tracks) == 0 :
        break

    for track in tracks:
        title = track['title']
        track_id = track['trackId']
        print(title, track_id)

        url = "https://www.ximalaya.com/revision/play/v1/audio?id=%d&ptype=1"%track_id
        r = requests.get(url, headers=HEADERS).json()
        url = r['data']['src']
        os.system("wget -O %s.m4a \"%s\""%(title, url))
