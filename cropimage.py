import cv2
import numpy as np
import imutils
# import pytesseract
from collections import Counter
from pandas import DataFrame as df
PATH_CROPPED = './cropped/'
PATH_OTHERS = 'D:/python/others/'
PATH = PATH_OTHERS
'''水平投影'''


def getHProjection(image):
    hProjection = np.zeros(image.shape, np.uint8)
    print('------1-------')
    # 图片高与宽
    (h, w) = image.shape
    print(h, w)
    # 长度与图像高度一致的数组
    h_ = [0] * h
    # 循环统计每一行白色像素的个数
    for y in range(h):
        for x in range(w):
            if image[y, x] == 255:
                h_[y] += 1

    # 绘制水平投影图像
    for y in range(h):
        for x in range(h_[y]):
            hProjection[y, x] = 255


    # cv2.imshow('hProjection2', hProjection)
    # cv2.waitKey(0)

    return h_


def getVProjection(image):
    vProjection = np.zeros(image.shape, np.uint8)
    (h, w) = image.shape

    w_ = [0] * w

    for x in range(w):
        for y in range(h):
            if image[y, x] == 255:
                w_[x] += 1

    for x in range(w):
        for y in range(h - w_[x], h):
            vProjection[y, x] = 255

    # cv2.imshow('vProjection', vProjection)
    cv2.waitKey(0)
    return w_


def fill_color(img, seedpoint):
    copyimg = img.copy()
    h, w = img.shape[:2]
    mask = np.zeros([h + 2, w + 2], np.uint8)
    mask[seedpoint[0]:seedpoint[2], seedpoint[1]:seedpoint[3]] = 0
    cv2.floodFill(copyimg, mask, (seedpoint[0] + 1, seedpoint[1] + 1), (0, 255, 255),
                  flags=cv2.FLOODFILL_MASK_ONLY)
    # cv2.imshow('fill_color',copyimg)


def modify_position(w, threshold=6):
    t = get_threshold(w, threshold)
    w_counter = Counter(w)
    weight = []
    for i in t:
    	weight.append(w_counter[i])

    m_mean = int(np.average(tuple(t), weights=weight))
    print(m_mean)
    # m_mean = sum(t)//len(t)
    m_max = max(t)
    w_ = []
    for item in w:
        if item < m_max and item > 0:
            w_.append(m_mean)
        # elif item < m_max:
        #     w_.append(m_mean)
        else:
        	w_.append(item)
    return w_, m_mean


def get_threshold(w, threshold=6):
	w_ = [0 if item < 2 else item for item in w]
	t = sorted(list(set(w_)))[1:threshold]
	return t


def main(file):
	origineImage = cv2.imread(file)
	print(file)
	# cv2.imshow('begin', origineImage)
	origineImage = imutils.resize(origineImage, width=1280)
	# 图片灰度化
	img = cv2.cvtColor(origineImage, cv2.COLOR_RGB2GRAY)
    # cv2.imshow('gray', img)
    # 二值化
	retval, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
	# cv2.imshow('binary', img)
	cv2.waitKey(0)
    # img = cv2.GaussianBlur(img,(3,3),0)
    # img = cv2.blur(img,(3,3))
    # img = cv2.medianBlur(img,5)
    # img = cv2.bilateralFilter(img,9,75,75)
    # cv2.imshow('Gauss',img)
    

    # contours, hierarchy = cv2.findContours(img,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    # cv2.imshow('contours',img)
    # kernel = np.ones((3, 3), np.uint8)
    # img = cv2.erode(img, kernel)
    # cv2.imshow('eroimg',img)
    # for i in range(len(contours)):
    # 	cv2.drawContours(img,contours,i,(0,255,255),3)
    # 	cv2.fillPoly(img,[contours[i]],(255,255,0))
    # cv2.imshow('fill',img)
    # print(type(contours),contours)
    # print(file)
	(h, w) = img.shape
	Position = []
    # 水平投影
	H = getHProjection(img)
	# print(H)
	start = 0
	H_Start = []
	H_End = []
    # 根据水平投影获取垂直分割位置
	for i in range(len(H)):
	    if H[i] > 0 and start == 0:
	        H_Start.append(i)
	        start = 1
	    if H[i] <= 0 and start == 1:
	        H_End.append(i)
	        start = 0
    # 分割行，分割之后再进行列分割列并保存分割位置
	# print(H_Start)
	# print(H_End)
	for i in range(len(H_Start)):
	    # 获取行图像
	    cropImg = img[H_Start[i]:H_End[i], 0:w]
	    # cv2.imshow('cropImg', cropImg)
	    # 对行图像进行垂直投影
	    W = getVProjection(cropImg)
	    # print(W)
	    threshold = 10
	    W, mean = modify_position(W, threshold)
	    # print(W)
	    WStart = 0
	    WEnd = 0
	    W_Start = 0
	    W_End = 0
	    for j in range(len(W)):
	        if W[j] > mean and WStart == 0:
	            W_Start = j
	            WStart = 1
	            WEnd = 0
	        if (j >= w-1 and WStart == 1) or (W[j] <=0  and WStart == 1):
	            W_End = j
	            WStart = 0
	            WEnd = 1
	        if WEnd == 1:
	            Position.append([W_Start, H_Start[i], W_End, H_End[i]])
	            WEnd = 0

	# new_Position = modify_position(Position)
	# print(Position)
	for m in range(len(Position)):
	    cv2.rectangle(origineImage, (Position[m][0], Position[m][1]),
	                  (Position[m][2], Position[m][3]), (0, 229, 238), 1)
	    # fill_color(origineImage,Position[m])

	cv2.imshow('image', origineImage)
	cv2.waitKey(0)
	return Position


if __name__ == '__main__':
	import os
	total_position = {}
	for i, file in enumerate(os.listdir(PATH)):
	    # print(file)
	    position = []
	    if file.split('.')[1] == 'png':
	        position = main(PATH+file)
	        total_position[file] = position
	    # if i > 25:
	    #     break
	import json
	with open('total_position.json', 'w') as f:
	    json.dump(total_position, f, ensure_ascii=False, indent=2)
	# main(PATH+'20200308120114_1.jpg')
