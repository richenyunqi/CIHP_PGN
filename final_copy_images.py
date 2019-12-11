import os
import shutil
import sys
from time import time
import cv2

image_count = 0


def imwrite_png(img, result_path):
    paths = os.path.splitext(result_path)
    if paths[1] != '.png':
        result_path = paths[0] + '.png'
    cv2.imwrite(result_path, img)


#调整大小、写入
def image_resize_output(image_path, result_path, original_image_path,
                        new_image_name):
    img = cv2.imread(image_path)
    types = ['_binary', '_vis']
    for t in types:
        if new_image_name.find(t) != -1:
            new_image_name = new_image_name.replace(t, '')
    print('original: ' + original_image_path + '/' +
          new_image_name.replace('.png', '.JPG'))
    original_height, original_width = cv2.imread(
        original_image_path + '/' +
        new_image_name.replace('.png', '.JPG')).shape[:2]
    new_img = cv2.resize(img, (original_width, original_height))
    imwrite_png(new_img, result_path + '/' + new_image_name)
    print('output ' + result_path)


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print('create ' + path)
    dirs = ['mask', 'cut', 'combine']
    for i in dirs:
        if not os.path.exists(path + '/' + i):
            os.mkdir(path + '/' + i)
            print('create ' + path + '/' + i)


def create_combine_png(original_image_path, mask_image_path, result_path):
    global image_count
    image_count += 1
    img_original = cv2.imread(original_image_path)
    img_mask = cv2.imread(mask_image_path)
    for i in range(img_original.shape[0]):
        for j in range(img_original.shape[1]):
            if img_mask[i, j, 0] == 0 and img_mask[i, j, 1] == 0 and img_mask[
                    i, j, 2] == 0:
                img_original[i, j] = (0, 0, 0)
    cv2.imwrite(result_path + '/' + os.path.split(mask_image_path)[1],
                img_original)
    print('create combine png: ' + result_path + '/' +
          os.path.split(mask_image_path)[1])


def create_dir_combine_png(original_path, result_path):
    print(result_path)
    names = os.listdir(result_path)
    if 'mask' in names:
        mask_path = result_path + '/mask'
        combine_path = result_path + '/combine'
        names = os.listdir(mask_path)
        for name in names:
            create_combine_png(
                original_path + '/' + name.replace('.png', '.JPG'),
                mask_path + '/' + name, combine_path)
    else:
        for name in names:
            create_dir_combine_png(original_path + '/' + name,
                                   result_path + '/' + name)


def copy_images(input_path, result_path, original_image_path):
    global image_count
    names = os.listdir(input_path)
    dir_str = {'_binary': 'mask', '_vis': 'cut'}
    for name in names:
        if os.path.isfile(input_path + '/' + name):
            s = name.split('_')
            dir_name = s[0] + '_' + s[1]
            create_dir(result_path + '/' + dir_name)
            new_image_name = s[2]
            for i in range(3, len(s)):
                new_image_name += '_' + s[i]
            for k, v in dir_str.items():
                if name.find(k) != -1:
                    image_count += 1
                    image_resize_output(input_path + '/' + name,
                                        result_path + '/' + dir_name + '/' + v,
                                        original_image_path + '/' + dir_name,
                                        new_image_name)
                    break
    create_dir_combine_png(original_image_path, result_path)


if __name__ == '__main__':
    input_path = 'G:/result/20191209_9_groups'
    result_path = 'G:/result/20191209'
    original_image_path = 'G:/20191209'
    start = time()
    copy_images(input_path, result_path, original_image_path)
    stop = time()
    use_time = stop - start
    print('处理' + str(image_count) + '张图片用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')