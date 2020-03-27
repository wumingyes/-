import pytesseract
import os
from PIL import Image

PATH_CROPPED = './cropped/'
PATH_BI = './cropped_bi/'
PATH_L = './cropped_L/'
PATH_NAME = './cropped_name/'
PATH_TEMP = './temp/'
users_temp = ['揽清幽', '网卡', 'zh_ch', 'iamok', '干里马', '熊立伟']

# PATH = PATH_TEMP
PATH = 'D:/个人资料/论文投稿/论文截图/'



def open_file():
    for file in os.listdir(PATH):
        img = Image.open(PATH + file)
        yield img, file

def parse_image(LANG, img):
    text = pytesseract.image_to_string(img, lang=LANG, config=r'--psm 6')
    return text


def recognition_image():
    num = 1
    for img, file in open_file():
        # file_name_list = file.split('.')[0].split('_')
        # file_name = file_name_list[0]
        # last_ch = int(file_name_list[1])
        # LANG = 'chi_sim' if last_ch < 3 else 'mydit_bi'
        LANG = 'chi_sim+eng'
        text = parse_image(LANG, img)
        print(num,text,file)
        num += 1
        # if text not in users_temp:
        #     print(num,text,file)
        #     num += 1


if __name__ == '__main__':
    recognition_image()
