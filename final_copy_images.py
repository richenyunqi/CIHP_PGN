import os
import shutil
import sys
from time import time
import cv2
import create_mask
from create_parsing import create_parsing_png
from t import fill_up_mask_image
image_count = 0


#调整大小、写入
def image_resize_output(image_path, result_path, original_image_path,
                        new_image_name):
    new_image_name = new_image_name.replace('_binary', '')
    new_image_name = new_image_name.replace('_vis2', '')
    img = cv2.imread(image_path)
    original_height, original_width = cv2.imread(
        os.path.join(original_image_path,
                     new_image_name[:-4] + '.JPG')).shape[:2]
    new_img = cv2.resize(img, (original_width, original_height))
    cv2.imwrite(os.path.join(result_path, new_image_name[:-4] + '.JPG'),
                new_img)
    print('output ' + os.path.join(result_path, new_image_name[:-4] + '.JPG'))


def create_dir(path, dir_name):
    if not os.path.exists(path):
        os.makedirs(path)
        print('create ' + path)
    dirs = ['MASK', 'COMBINE', 'PARSING', 'ORIGINAL_PARSING']
    for i in dirs:
        p = os.path.join(path, dir_name + '_' + i)
        if not os.path.exists(p):
            os.makedirs(p)
            print('create ' + p)


def create_dir_combine_JPG(original_path, result_path):
    print(result_path)
    global image_count
    names = os.listdir(result_path)
    if any([i.endswith('_MASK') for i in names]):
        dir_name = os.path.split(result_path)[1]
        mask_path = os.path.join(result_path, dir_name + '_MASK')
        combine_path = os.path.join(result_path, dir_name + '_COMBINE')
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
        os.makedirs(result_path)
        print('create ' + result_path)
    global image_count
    names = os.listdir(input_path)
    dir_str = {'_binary': 'MASK', '_vis2': 'PARSING'}
    for name in names:
        if os.path.isfile(os.path.join(input_path, name)):
            i = name.find('_', name.find('FRM') + 4)
            dir_name = name[:i]
            create_dir(result_path + '/' + dir_name, dir_name)
            new_image_name = name[i + 1:]
            for k, v in dir_str.items():
                if k in name:
                    image_count += 1
                    image_resize_output(
                        os.path.join(input_path, name),
                        os.path.join(os.path.join(result_path, dir_name),
                                     dir_name + '_' + v),
                        os.path.join(original_image_path, dir_name),
                        new_image_name)
                    break
            if '_vis.png' in name:
                shutil.copyfile(
                    os.path.join(input_path, name),
                    os.path.join(result_path, dir_name,
                                 dir_name + '_ORIGINAL_PARSING',
                                 new_image_name.replace('_vis.png', '.png')))
        else:
            copy_images(os.path.join(input_path, name), result_path,
                        original_image_path)
    create_dir_combine_JPG(original_image_path, result_path)


if __name__ == '__main__':
    # terrible_path = 'F:/human/result/terrible/20200111'
    # input_path = 'F:/human/result/original/20200111'
    # result_path = 'F:/human/result/final/20200111'
    # original_image_path = 'F:/human/data/20200111'
    # start = time()
    # create_mask.create_mask_png(terrible_path)
    # create_mask.copy_images(terrible_path, input_path)
    # create_parsing_png(input_path)
    # copy_images(input_path, result_path, original_image_path)
    # stop = time()
    # use_time = stop - start
    # print('处理' + str(image_count) + '张图片用时为' + str(use_time // 3600) + '小时:' +
    #       str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    # print('--------------end-----------------')
    input_path = 'F:/human/result/original'
    result_path = 'F:/human/result/final'
    original_image_path = 'F:/human/data'
    start = time()
    for dir_name in os.listdir(input_path):
        input_dir_path = os.path.join(input_path, dir_name)
        result_dir_path = os.path.join(result_path, dir_name)
        original_dir_path = os.path.join(original_image_path, dir_name)
        fill_up_mask_image(input_dir_path)
        create_parsing_png(input_dir_path)
        copy_images(input_dir_path, result_dir_path, original_dir_path)
    stop = time()
    use_time = stop - start
    print('处理' + str(image_count) + '张图片用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')