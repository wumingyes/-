import json
import os
import time
from functools import reduce

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# APP_ID = '18639131'
# API_KEY = 'vaD8H6fcPyqa85kviyDG4kXT'
# SECRET_KEY = 'S49RB7BEhM65g39qH7yUplBpESS45AYC'
# client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
# options["language_type"] = "CHN_ENG"
# options["detect_direction"] = "true"
# options["detect_language"] = "true"
# options["probability"] = "true"
PATH_IMAGE = './images/'
PATH_CROPPED = './cropped/'
PATH_BI = './cropped_bi/'
PATH_L = './cropped_L/'
PATH_JSON = './'
PATH_TEMP = './temp/'
PATH_OTHERS = 'D:/python/others/'
options = {}
PATH = PATH_L

p_lu = (210, 110, 310, 150)
p_cu = (680, 110, 780, 150)
p_ru = (1140, 110, 1250, 150)
p_ld = (190, 500, 340, 580)
p_cd = (640, 500, 800, 580)
p_rd = (1110, 500, 1270, 580)
# p_t = (940,680,1170,720)
points = [p_lu, p_cu, p_ru, p_ld, p_cd, p_rd]
time_users_scores_dict = {}
users = []
scores = []
users_temp = ['揽清幽', '网卡', 'zh_ch', 'iamok', '干里马', '熊立伟']
error_num = 0
total_num = 0
error_files = []


def open_file_of_image(path):
    for file in os.listdir(path):
        # print(path + file)
        yield path + file


def load_from_file(PATH):
    with open(PATH_JSON + 'statistics.json', 'r', encoding='utf-8') as f:
        content = f.read()
        # print(content)
        time_users_scores_dict = json.loads(content, strict=False)
        # print(time_users_scores_dict)
    return time_users_scores_dict


def write_to_file(time_users_scores_dict):
    with open(PATH_JSON + 'statistics.json', 'w', encoding='utf-8') as f:
        json.dump(time_users_scores_dict, f, ensure_ascii=False, indent=2)


def crop_all_image(path):
    for file_full_path in open_file_of_image(path):
        file_name = os.path.basename(file_full_path).split('.')[0]
        if file_name not in list(time_users_scores_dict.keys()):
            print(file_name)
            crop_one_image(file_full_path)


def crop_one_image(file_full_path):
    img = Image.open(file_full_path)
    new_img = img.resize((1440, 720), Image.ANTIALIAS)
    path_name = PATH_CROPPED
    for i, p in enumerate(points):
        cropped = new_img.crop(p)
        cropped.save(
            path_name + os.path.basename(file_full_path).split('.')[0] + '_%s' % i + ".jpg")


def parse_all_image(PATH):
    for img_file in os.listdir(PATH):
        file_name = img_file.split('_')[0]
        if file_name not in list(time_users_scores_dict.keys()):
            parse_one_image(PATH + img_file)


def parse_image(LANG, img):
    text = pytesseract.image_to_string(
        img, lang=LANG, config='--psm 7 --oem 3')
    # print(LANG)
    return text


def open_one_img(img_file_full_path):
    img = Image.open(img_file_full_path)
    return img


def parse_one_image(img_file_full_path, enhance=0):
    global total_num
    img = open_one_img(img_file_full_path)
    img_file_name = os.path.basename(img_file_full_path)
    file_name_list = img_file_name.split('.')[0].split('_')
    file_name = file_name_list[0]
    last_ch = int(file_name_list[1])
    LANG = 'chi_sim' if last_ch < 3 else 'mydit'
    if enhance == 1:
        img = enhance_when_modify_img(img)
    text = parse_image(LANG, img)
    if LANG == 'mydit':
        try:
            int(text)
        except:
            text = parse_image('eng', img)
        if text and text[0] not in ['+', '-']:
            text = '-' + text
    # print(text)
    total_num += 1
    create_json_data(text, last_ch, file_name)


def check(text, file_name):
    global error_files, error_num
    if text not in users_temp:

        if '清' in text or '揽' in text or '幽' in text:
            text = '揽清幽'
        elif '立' in text or '熊' in text or '伟' in text:
            text = '熊立伟'
        elif 'z' in text or 'h' in text or '_' in text:
            text = 'zh_ch'
        elif 'k' in text or 'm' in text:
            text = 'iamok'
        elif '马' in text or '千' in text or '里' in text:
            text = '干里马'
        elif '卡' in text or '网' in text:
            text = '网卡'
        else:
            print('>>>>>>>>>>名字识别错误<<<<<<<<<<<<\n')
            if file_name not in error_files:
                error_files.append(file_name)
            error_num += 1
            print(error_num, text, file_name)
    return text


def check_scores(file_name):
    global scores
    global error_num
    sum = 0
    try:
        scores_int = list(map(lambda x: int(x), scores))
        sum = reduce(lambda x, y: x + y, scores_int)
    except Exception as errors:
        print(errors)
        print('=============识别非数字==========')
        error_num += 1
        error_files.append(file_name)
        print(error_num, '\t', scores, file_name)
    if sum != 0:
        error_num += 1
        print('<<<<<<<<<<<计算错误>>>>>>>>>>>>>>')
        print(error_num, '\t', scores, file_name)
        if file_name not in error_files:
            error_files.append(file_name)


def create_json_data(text, i, file_name):
    global users
    global error_num, time_users_scores_dict
    global scores
    if i < 3:
        text = check(text, file_name)
        users.append(text)
    else:
        scores.append(text)
    if i >= 5:
        check_scores(file_name)
        users_scores_dict = dict(zip(users, scores))
        time_users_scores_dict[file_name] = users_scores_dict
        users = []
        scores = []


def enhance_when_modify_img(img):
    new_img = ImageEnhance.Contrast(img).enhance(10)
    # new_img.show()
    return new_img


def open_image_file(dir_path):
    for file in os.listdir(dir_path):
        img = Image.open(dir_path+file)
        yield img, file


def enhance_all_img(dir_path):
    for img, file in open_image_file(dir_path):
        file_name = file.split('.')[0]
        if file_name not in list(time_users_scores_dict.keys()):
            new_img = img.convert('L')
            img_ed = new_img.filter(
                ImageFilter.SMOOTH_MORE).filter(ImageFilter.SHARPEN)
            img_ed.save(PATH_L+file)


def modify_img(PATH):
    global error_files
    error_files_temp = error_files
    error_files = []
    if error_files_temp:
        for file in error_files_temp:
            for i in range(6):
                error_file = file+'_%s' % i + '.jpg'
                parse_one_image(PATH + error_file, enhance=1)


def manual_modify():
    global time_users_scores_dict, error_files
    answer = ''
    while answer not in ['y', 'Y', 'n', 'N']:
        answer = input("需要手动修复吗？？(y/n)")
        if answer in ['y', 'Y']:
            print('共有%d个数据需要修复！' % (len(error_files)))
            for file_name in error_files:
                print('请输入三个玩家的姓名：')
                names = input()
                users = names.split(',')
                print('请输入三个对应的分数：')
                score = input()
                scores = score.split(',')
                users_scores_dict = dict(zip(users, scores))
                time_users_scores_dict[file_name] = users_scores_dict
            error_files = []
            return
        elif answer in ['n', 'N']:
            return


def main():
    global error_num, error_files, time_users_scores_dict, total_num
    time_users_scores_dict = load_from_file(PATH_JSON)
    crop_all_image(PATH_IMAGE)
    enhance_all_img(PATH_CROPPED)
    parse_all_image(PATH)
    print("\n数据总数：%s" % total_num)
    if total_num:
        print('矫正前识别错误总数：{0:}\t\t占总数的：{1:.2%}\n'.format
              (error_num, error_num/total_num))
    else:
        print('没有加入新的图片！\n')
    error_num = 0
    total_num = 0
    error_files = list(set(error_files))
    print('------------------矫正前错误文件---------------\n', error_files)
    modify_img(PATH)
    error_files = list(set(error_files))
    print('---------------矫正后错误文件-------------\n', error_files)
    if error_files:
        manual_modify()
    if error_files:
        for key in error_files:
            print(key, time_users_scores_dict[key])
            time_users_scores_dict.pop(key)
    write_to_file(time_users_scores_dict)


if __name__ == '__main__':
    # time_begin = time.perf_counter()
    # main()
    # time_end = time.perf_counter()
    # print("程序运行总耗时：{:.2f}秒\n".format(time_end-time_begin))
    temp_dict = load_from_file(PATH_JSON)
    temp_dict['20200320191212']={"揽清幽":"+260","zh_ch":"-175","iamok":"-85"}
    write_to_file(temp_dict)