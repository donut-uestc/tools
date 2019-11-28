#!/usr/bin/env python3

import sys
import os
import requests
import time
import base64
import rsa

# coding=utf-8
import base64
import rsa
import hashlib

import cv2
import numpy

import captcha
import signature_vip

requests.packages.urllib3.disable_warnings()

__all__ = ['rsa_encrypt']

def baseN(num, b):
    return ((num == 0) and "0") or (baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

def _str2key(s):
    # 对字符串解码
    b_str = base64.b64decode(s)

    if len(b_str) < 162:
        return False

    hex_str = ''

    # 按位转换成16进制
    for x in b_str:
        h = hex(x)[2:]
        h = h.rjust(2, '0')
        hex_str += h

    # 找到模数和指数的开头结束位置
    m_start = 29 * 2
    e_start = 159 * 2
    m_len = 128 * 2
    e_len = 3 * 2

    modulus = hex_str[m_start:m_start + m_len]
    exponent = hex_str[e_start:e_start + e_len]

    return modulus, exponent


def rsa_encrypt(s, pubkey_str):
    '''
    rsa加密
    :param s:
    :param pubkey_str:公钥
    :return:
    '''
    key = _str2key(pubkey_str)
    modulus = int(key[0], 16)
    exponent = int(key[1], 16)
    pubkey = rsa.PublicKey(modulus, exponent)
    return base64.b64encode(rsa.encrypt(s.encode(), pubkey)).decode()

def check_path(seed, file_id):
    t = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\\:._-1234567890"
    s = ""
    l = len(t)
    for i in range(0, l):
        seed = int((211 * seed + 30031) % 65536)
        r = int((seed/65536) * len(t))
        s = s + t[r]
        t = "".join(t.split(t[r]))

    v = ""
    file_id = file_id.split('*') 
    for i in range(0, len(file_id) - 1):
        v = v + s[int(file_id[i])]

    return v


# return r.setPublicKey("MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVhaR3Or7suUlwHUl2Ly36uVmboZ3+HhovogDjLgRE9CbaUokS2eqGaVFfbxAUxFThNDuXq/fBD+SdUgppmcZrIw4HMMP4AtE2qJJQH/KxPWmbXH7Lv+9CisNtPYOlvWJ/GHRqf9x3TBKjjeJ2CjuVxlPBDX63+Ecil2JR9klVawIDAQAB"), r.encrypt(e)

HEADERS= {
#'Host': 'passport.ximalaya.com',
'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8' ,
#'Origin': 'https://www.ximalaya.com' ,
#'Accept': '*/*' ,
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15' ,
#'Referer': 'https://www.ximalaya.com/' ,
'Accept-Language': 'zh-cn' ,
}

HEADERS={   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Content-Type': 'application/json'}


session = requests.session()
session.headers.update(HEADERS)

bp_id = 139
cur_time = int(time.time()*1000)
session_id = 'xm_' + baseN(cur_time, 36) + '24hg4'

url = "https://mobile.ximalaya.com/captcha-web/check/slide/get?bpId=%d&sessionId=%s"%(bp_id, session_id)
r = session.get(url, verify=False).json()
#captcha_fg_url = r['data']['fgUrl']
captcha_bg_url = r['data']['bgUrl']


#with open('captcha_fg.png', 'wb') as f:
#    f.write(session.get(captcha_fg_url, verify=False).content)

with open('captcha_bg.jpg', 'wb') as f:
    f.write(session.get(captcha_bg_url, verify=False).content)

captchaText = captcha.FindPosition2('captcha_bg.jpg')
print(captchaText)

## 校验
url = "https://mobile.ximalaya.com/captcha-web/valid/slider"
captcha_data = {
    "bpId": bp_id,
    "sessionId": session_id,
    "type": "slider",
    "captchaText": "%d,0"%captchaText,
    "startX": 541,
    "startY": 396,
    "startTime": "%d"%(time.time())
}

r = session.post(url, verify=False, json=captcha_data).json()
print(r)

cookies={'fds_otp':r['token']}
print(cookies)

url = "https://passport.ximalaya.com/web/nonce/%d"%(time.time())
r = session.get(url, cookies=cookies, verify=False).json()

acount="18919633548"
nonce = r['nonce']
password = rsa_encrypt("55jiao893", "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVhaR3Or7suUlwHUl2Ly36uVmboZ3+HhovogDjLgRE9CbaUokS2eqGaVFfbxAUxFThNDuXq/fBD+SdUgppmcZrIw4HMMP4AtE2qJJQH/KxPWmbXH7Lv+9CisNtPYOlvWJ/GHRqf9x3TBKjjeJ2CjuVxlPBDX63+Ecil2JR9klVawIDAQAB")

#signature
#t: "account=18919633548&nonce=0-8BB39F891F014b399744055fd86563a06d607fe77e2406eac7683d83a8c88c&password=OCjJ5VhriZRAvU2Lq3ENTn4ZZVMVmbZ4kEYg3XlQ…"
#xx = "ACCOUNT=18919633548&NONCE=0-90D08073855FC5DAC7CC9F0EB45F964191FECAC8335F16D53FB4E7909ED31D&PASSWORD=O8xE5fw2ELqFp6JhelU+KBWv2IaeRu9Rbwt+Tw1dkdGTSLKB+V6E8ZuMqQoDyxjuTD8ypou+se2Pr4N7uwTcX73mhaX+TtZmELyfmyafyvpO52fYw93vEE8Jtw4eYvWEA5JNcB4B61SlHlgsGPuKgqYmDh87LZqMcqnm/Kym6Uk=&"

#print(xx.upper())


post_data = {
	"account": "18919633548",
	"nonce": nonce,
	"password": password,
        }

signature = ("account=%s&nonce=%s&password=%s&WEB-V1-PRODUCT-E7768904917C4154A925FBE1A3848BC3E84E2C7770744E56AFBC9600C267891F"%(post_data["account"], post_data["nonce"], post_data["password"])).upper()
print(signature)

#signature = "account=18919633548&nonce=0-814651796737165395f50f61a5cdcaf8bac8c6c6b1edcab1704f92cd8fc3b8&password=dPLX7tP0FVHvZQIRuzBwXYrDRDwDqt4ql8Sl9FGCLPbnDpydLlWIvpShpBRCZ8ZWxBzddXOn02V4IYfAdcfcFVnSBdjJ7m0iesk/LUqXQBPMZX8SRp78GxgJAS4rRY+6oX04dAplvnUB/TkqJuXOYlBrfl/JiG622TzmxZZ9fPQ=&WEB-V1-PRODUCT-E7768904917C4154A925FBE1A3848BC3E84E2C7770744E56AFBC9600C267891F"

signature = hashlib.sha1(signature.upper().encode('utf-8'))
signature = signature.hexdigest()
print(signature)

post_data["signature"] = signature
post_data["rememberMe"] = False

url = "https://passport.ximalaya.com/web/login/pwd/v1"

r = session.post(url, cookies=cookies, verify=False, json=post_data).json()
uid=r['uid']
token=r['token']
print(uid, token)
cookies['1&_token'] = "%d&%s"%(uid,token)

album_id = int(sys.argv[1])

curpage = 1
while True:
    url = "https://www.ximalaya.com/revision/album/v1/getTracksList?albumId=%d&pageNum=%d"%(album_id, curpage)
    curpage = curpage + 1
    r = session.get(url, cookies=cookies, headers=HEADERS, verify=False).json()
    tracks = r['data']['tracks']
    if len(tracks) == 0 :
        break

    for track in tracks:
        title = track['title']
        track_id = track['trackId']
        print(title, track_id)

        #url = "https://www.ximalaya.com/revision/play/v1/audio?id=%d&ptype=1"%track_id
        #r = requests.get(url, cookies=cookies, headers=HEADERS, verify=False).json()
        #print(r[''])

        """
        {'ret': 0, 'msg': '0', 'trackId': 75598151, 'uid': 96983437, 'albumId': 13507836, 'title': '明朝那些事儿 第01集', 'domain': 'http://audio.pay.xmcdn.com', 'totalLength': 11988139, 'sampleDuration': 0, 'sampleLength': 0, 'isAuthorized': True, 'apiVersion': '1.0.0', 'seed': 1833, 'fileId': '3*44*57*38*9*30*5*60*28*34*5*14*33*5*22*50*5*47*45*3*63*42*30*29*61*35*28*66*26*47*21*42*1*13*2*15*41*29*35*57*37*56*17*40*19*50*14*31*51*33*67*', 'buyKey': '332e3838353534363331373932373731382d302e35353833383433313631313434363935', 'duration': 1480, 'ep': '3kFqaox2Sn9SjagNPoocsQtdUx0ghCLPToYffF+1DX6qkbjZ3/uLz+4L0fqP36JhXu9013EGeqRi3PL+wAQW37wWOy5UE76uRomSuHBQqEXwpOdRmW1EMasodzqFUxPFcsHaF89KrGQ+4/j0sGJGf426FYAejo9BkQ==', 'highestQualityLevel': 1, 'downloadQualityLevel': 1, 'authorizedType': 1}
        """

        url = "https://mpay.ximalaya.com/mobile/track/pay/%d?device=pc&isBackend=true&_=%d"%(track_id, int(time.time()))
        r = session.get(url, cookies=cookies, headers=HEADERS, verify=False).json()
        
        sign, token, timestamp = signature_vip.create(r['ep'])
        
        url = "https://vod.xmcdn.com/download/%s/%s?sign=%s&buy_key=%s&token=%s&timestamp=%s&duration=%s"%(
                r['apiVersion'], 
                check_path(r['seed'], r['fileId']), 
                sign, r['buyKey'], token, timestamp, r['duration'])
        
        
        r = session.get(url, cookies=cookies, headers=HEADERS, verify=False)
        with open('x.m4a', 'wb') as f:
            f.write(r.content)
        print(url)
        break
    break

        #os.system("wget -O %s.m4a \"%s\""%(title, url))
        #print("wget -O %s.m4a \"%s\""%(title, url))
