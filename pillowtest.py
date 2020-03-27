from PIL import Image, ImageFilter, ImageEnhance
import os
import numpy as np
import matplotlib.pyplot as plt

PATH_CROPPED = './cropped/'
PATH_BI = './cropped_bi/'
PATH_L = './cropped_L/'
PATH_NAME = './cropped_name/'
PATH_TEMP = './temp/'

# 、CONTOUR,DETAIL,EDGE_ENHANCE,EDGE_ENHANCE_MORE,EMBOSS,FIND_EDGES,SMOOTH,SMOOTH_MORE,SHARPEN]
FILTER = [ImageFilter.DETAIL]


def open_image_file(dir_path):
    for file in os.listdir(dir_path):
        img = open_img(dir_path+file)
        yield img, file
        # break


def open_img(img_file):
    img = Image.open(img_file)
    return img


def convert_img(img):
    return img.convert('L')


def show_img_hist(pixel_counts):
    plt.xlabel('Image_pixels')
    plt.ylabel('Counts')
    plt.title('OTSU')

    X = np.linspace(0, 255, 256)
    plt.bar(X, pixel_counts, color='g')
    plt.show()


def get_pixelcounts(img):
    pixeldata = img.load()
    width, height = img.size
    pixel_counts = np.zeros(256)
    print(width, height)
    for x in range(width):
        for y in range(height):
            pixel_counts[pixeldata[x, y]] += 1
    show_img_hist(pixel_counts)

    return pixel_counts, width*height


def OTSU(img):
    pixel_counts, total_pixel = get_pixelcounts(img)

    max_g = 0.0
    best_threshold = 0.0
    for threshold in range(256):
        n0 = pixel_counts[:threshold].sum()  # 阈值以下像素总数（前景）
        n1 = pixel_counts[threshold:].sum()  # 阈值以上像素总数（背景）
        # print(n0,n1)

        w0 = n0/total_pixel
        w1 = n1/total_pixel

        # 阈值以下平均灰度
        u0 = 0.0
        for i in range(threshold):
            u0 += i*pixel_counts[i]

        # 阈值以上平均灰度
        u1 = 0.0
        for i in range(threshold, 256):
            u1 += i*pixel_counts[i]

        u = u0*w0 + u1*w1

        g = w0*np.power((u-u0), 2) + w1*np.power((u-u1), 2)

        if g > max_g:
            best_threshold = threshold
            max_g = g
    return best_threshold


def get_bin_table(threshold=165):
    '''
    获取灰度转二值的映射table
    0表示黑色,1表示白色
    '''
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


def enhance_img(img):
    new_img = convert_img(img)
    threshold = OTSU(new_img)
    # print(threshold)
    table = get_bin_table(threshold)
    new_img = new_img.point(table, '1')
    new_img = new_img.filter(ImageFilter.SMOOTH_MORE)
    new_img = resize_img(new_img)
    return new_img


def enhance_all_img(dir_path):
    for img, file in open_image_file(dir_path):
        en_img = enhance_img(img)
        en_img.save(PATH_TEMP+file)

def resize_img(img):
	new_img = img.resize((img.size[0]*2,img.size[1]*2))
	return new_img
	

if __name__ == '__main__':
    # enhance_all_img(PATH_CROPPED)
    # OTSU(r'E:\文档\pythonStudy\图像识别\temp\20200308120126_3.jpg'))
    img = open_img(PATH_CROPPED + '20200308115339_5.jpg')
    en_img = enhance_img(img)
