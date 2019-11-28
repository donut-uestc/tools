#!/usr/bin/env python3

import sys

"""
{
	"bpId": 139,
	"sessionId": "xm_k3gkngg6o24hg4",
	"type": "slider",
	"captchaText": "286,-1",
	"startX": 782,
	"startY": 491,
	"startTime": 1574820247293
}
"""

import cv2

def FindPosition(target, template):
    """
    找出图像中最佳匹配位置
    :param target: 目标即背景图
    :param template: 模板即需要找到的图
    :return: 返回最佳匹配及其最差匹配和对应的坐标
    """
    target_rgb = cv2.imread(target)
    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
    template_rgb = cv2.imread(template, 0)
    res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
    value = cv2.minMaxLoc(res)
    print(value)
    return value

def FindPosition2(target):
    image = cv2.imread(target, 0)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    canny = cv2.Canny(blurred, 200, 400)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
    #cv2.imshow('xx', image)
    #cv2.waitKey(0)
    #return 0
    for i, contour in enumerate(contours):
        M = cv2.moments(contour)
        if M['m00'] == 0:
            cx = cy = 0
        else:
            cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
        #print(cv2.contourArea(contour), cv2.arcLength(contour, True))
        if 4000 < cv2.contourArea(contour) < 8000 and 300 < cv2.arcLength(contour, True) < 400:
            x, y, w, h = cv2.boundingRect(contour)  # 外接矩形
            #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            #cv2.imshow('image', image)
            #cv2.waitKey(0)
            return x + 32
    return 0

if __name__ == "__main__":
    #FindPosition('captcha_bg.png', 'captcha_fg.png')
    print(FindPosition2(sys.argv[1]))
