import os
import shutil
import sys

import cv2


def imwrite_png(img, output_path):
    paths = os.path.splitext(output_path)
    if paths[1] != '.png':
        output_path = paths[0] + '.png'
    cv2.imwrite(output_path, img)


#调整大小、写入
def image_resize_output(image_path, output_path, original_path,
                        new_image_name):
    img = cv2.imread(image_path)
    types = ['_binary', '_vis', '_combine']
    for t in types:
        if new_image_name.find(t) != -1:
            new_image_name = new_image_name.replace(t, '')
    print('original: ' + original_path + '/' +
          new_image_name.replace('.png', '.JPG'))
    original_height, original_width = cv2.imread(
        original_path + '/' + new_image_name.replace('.png', '.JPG')).shape[:2]
    new_img = cv2.resize(img, (original_width, original_height))
    imwrite_png(new_img, output_path + '/' + new_image_name)
    print('output ' + output_path)


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        print('create ' + path)
    dirs = ['mask', 'cut', 'combine']
    for i in dirs:
        if not os.path.exists(path + '/' + i):
            os.mkdir(path + '/' + i)
            print('create ' + path + '/' + i)


def copy_images(input_path, output_path, original_path):
    names = os.listdir(input_path)
    dir_str = {'_binary': 'mask', '_vis': 'cut', '_combine': 'combine'}
    for name in names:
        s = name.split('_')
        dir_name = s[0] + '_' + s[1]
        create_dir(output_path + '/' + dir_name)
        new_image_name = s[2]
        for i in range(3, len(s)):
            new_image_name += '_' + s[i]
        for k, v in dir_str.items():
            if name.find(k) != -1:
                image_resize_output(input_path + '/' + name,
                                    output_path + '/' + dir_name + '/' + v,
                                    original_path + '/' + dir_name,
                                    new_image_name)
                break


if __name__ == '__main__':
    input_path = input('Please input the input_path: ')
    output_path = input('Please input the output_path: ')
    original_path = input('Please input the original_path: ')
    copy_images(input_path, output_path, original_path)
    print('--------------end-----------------')