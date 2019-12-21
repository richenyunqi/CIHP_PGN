import os
import shutil
import sys
from time import time
import cv2

image_count = 0


#调整大小、写入
def image_resize_output(image_path, result_path, original_image_path,
                        new_image_name):
    img = cv2.imread(image_path)
    new_image_name = new_image_name.replace('_binary', '')
    new_image_name = new_image_name.replace('_vis', '')
    original_height, original_width = cv2.imread(
        os.path.join(original_image_path,
                     new_image_name[:-4] + '.JPG')).shape[:2]
    new_img = cv2.resize(img, (original_width, original_height))
    cv2.imwrite(os.path.join(result_path, new_image_name[:-4] + '.JPG'),
                new_img)
    print('output ' + os.path.join(result_path, new_image_name[:-4] + '.JPG'))


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print('create ' + path)
    dirs = ['mask', 'cut', 'combine']
    for i in dirs:
        p = os.path.join(path, i)
        if not os.path.exists(p):
            os.mkdir(p)
            print('create ' + p)


def create_dir_combine_JPG(original_path, result_path):
    print(result_path)
    global image_count
    names = os.listdir(result_path)
    if 'mask' in names:
        mask_path = result_path + '/mask'
        combine_path = result_path + '/combine'
        names = os.listdir(mask_path)
        for name in names:
            original_img = cv2.imread(
                os.path.join(original_path, name[:-4] + '.JPG'))
            mask_img = cv2.imread(os.path.join(mask_path, name))
            print('mask img: ' + os.path.join(mask_path, name))
            combine_img = cv2.copyTo(original_img, mask_img)
            cv2.imwrite(os.path.join(combine_path, name[:-4] + '.JPG'),
                        combine_img)
            print('create combine JPG: ' + result_path + '/' +
                  os.path.join(combine_path, name[:-4] + '.JPG'))
            image_count += 1
    else:
        for name in names:
            create_dir_combine_JPG(original_path + '/' + name,
                                   result_path + '/' + name)


def copy_images(input_path, result_path, original_image_path):
    if not os.path.exists(result_path):
        os.mkdir(result_path)
        print('create ' + result_path)
    global image_count
    names = os.listdir(input_path)
    dir_str = {'_binary': 'mask', '_vis': 'cut'}
    for name in names:
        if os.path.isfile(os.path.join(input_path, name)):
            i = name.find('_', name.find('_') + 1)
            dir_name = name[:i]
            create_dir(result_path + '/' + dir_name)
            new_image_name = name[i + 1:]
            for k, v in dir_str.items():
                if name.find(k) != -1:
                    image_count += 1
                    image_resize_output(
                        os.path.join(input_path, name),
                        os.path.join(os.path.join(result_path, dir_name), v),
                        os.path.join(original_image_path, dir_name),
                        new_image_name)
                    break
    create_dir_combine_JPG(original_image_path, result_path)


if __name__ == '__main__':
    input_path = 'G:/result/original/20191209_9_groups'
    result_path = 'G:/result/final/20191209_python'
    original_image_path = 'G:/20191209'
    start = time()
    copy_images(input_path, result_path, original_image_path)
    stop = time()
    use_time = stop - start
    print('处理' + str(image_count) + '张图片用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')