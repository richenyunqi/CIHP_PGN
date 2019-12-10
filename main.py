import os
import shutil
import sys
from time import time

import cv2

from my_test_pgn import Test
from circle import detect_circle
from trans_rgb import trans_background_bgr, trans_mark_bgr
from write_txt import *

image_count = 0


def imwrite_png(img, output_path):
    paths = os.path.splitext(output_path)
    if paths[1] != '.png':
        output_path = paths[0] + '.png'
    cv2.imwrite(output_path, img)


# 调整大小、翻转、写入
# def image_resize_output(image_path, output_path, max_height):
#     image_name = os.path.split(image_path)[1]
#     img = cv2.imread(image_path)
#     height, width = img.shape[:2]
#     new_width = 0
#     new_height = 0
#     if height >= width:
#         new_height = max_height
#         new_width = int(width * max_height / height)
#         new_img = cv2.resize(img, (new_width, new_height))

#         imwrite_png(new_img, output_path + '/' + image_name)
#     else:
#         new_width = max_height
#         new_height = int(height * max_height / width)
#         new_img = cv2.resize(img, (new_width, new_height))
#         new_img = cv2.flip(new_img, 0)
#         new_img = cv2.transpose(new_img)
#         imwrite_png(new_img, output_path + '/' + image_name)
#         new_width, new_height = new_height, new_width
#     print('output ' + output_path)
#     return new_width, new_height

# 写入
# def image_resize_output(image_path, output_path, max_height):
#     image_name = os.path.split(image_path)[1]
#     img = cv2.imread(image_path)
#     height, width = img.shape[:2]
#     imwrite_png(img, output_path + '/' + image_name)
#     print('output ' + output_path)
#     return width, height


def trans_bgr(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # trans_mark_bgr(img, i, j)
            trans_background_bgr(img, i, j)


# 调整大小、写入
def image_resize_output(image_path, output_path):
    global image_count
    image_count += 1
    file_path = os.path.split(image_path)
    image_name = file_path[1]
    dir_name = os.path.split(file_path[0])[1]
    img = cv2.imread(image_path)
    # img = detect_circle(img)
    height, width = img.shape[:2]
    new_height = 600
    new_width = int(new_height * width / height)
    new_img = cv2.resize(img, (new_width, new_height))
    trans_bgr(new_img)
    # new_img = detect_circle(new_img)
    imwrite_png(new_img, output_path + '/' + dir_name + '_' + image_name)
    print('output ' + output_path)
    return new_width, new_height


def black_image_resize_output(input_image_path, output_image_path, width,
                              height):
    img = cv2.imread(input_image_path)
    new_img = cv2.resize(img, (width, height))
    imwrite_png(new_img, output_image_path)
    print('output ' + output_image_path)


def create_black_image(image_name, output_path, width, height):
    for dirn in ['/edges', '/labels', '/labels_rev']:
        output_image_dir_path = output_path + dirn
        if os.path.exists(output_image_dir_path) == False:
            os.mkdir(output_image_dir_path)
        black_image_resize_output('./datasets/CIHP/edges/0026375.png',
                                  output_image_dir_path + '/' + image_name,
                                  width, height)


def create_list(images_path):
    list_path = os.path.dirname(images_path) + '/list'
    if not os.path.exists(list_path):
        os.makedirs(list_path)
    write_val_id(images_path)
    write_val(images_path)
    write_train_rev(images_path)
    write_train(images_path)
    write_train_id(images_path)
    write_image_list(images_path)


def create_tool(output_path):
    output_path = output_path + '/tool'
    if os.path.exists(output_path) == False:
        os.mkdir(output_path)
    shutil.copy('./datasets/CIHP/tool/reverse_label.m', output_path)
    shutil.copy('./datasets/CIHP/tool/write_edge.m', output_path)


def create_test_data(input_path, output_path):
    images_names = os.listdir(input_path)
    print('Process ' + input_path)
    for name in images_names:
        if os.path.isdir(input_path + '/' + name):
            create_test_data(input_path + '/' + name, output_path)
        else:
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            if os.path.exists(output_path + '/images') == False:
                os.mkdir(output_path + '/images')
            width, height = image_resize_output(input_path + '/' + name,
                                                output_path + '/images')
            create_black_image(
                os.path.split(input_path)[1] + '_' + name, output_path, width,
                height)
    if os.path.isfile(input_path + '/' + images_names[0]):
        create_list(output_path + '/images')
        create_tool(output_path)


def test(test_data_path, result_path):
    print('test ' + test_data_path)
    test_data = Test(test_data_path)
    test_data.main()
    print('copy images')
    copy_images(test_data.DATA_DIR, result_path)
    print('create binary images')
    create_binary_png(result_path)
    create_combine_png(result_path)


# 这里没有办法进行多次test，因为n_classes
# def test(test_data_path, result_path):
#     images_names = os.listdir(test_data_path)
#     for name in images_names:
#         if True:
#             print('test ' + test_data_path)
#             test_data = Test(test_data_path + '/' + name)
#             test_data.main()
#             print('copy images')
#             copy_images(test_data.DATA_DIR, result_path)
#             print('create binary images')
#             create_binary_png(result_path)
#         else:
#             new_dir = result_path + '/' + name
#             if os.path.exists(new_dir) == False:
#                 os.mkdir(new_dir)
#             print('dir: ' + test_data_path + '/' + name)
#             test(test_data_path + '/' + name, new_dir)


def create_binary_png(result_path):
    names = os.listdir(result_path)
    for n in names:
        if n.find('.png') != -1 and n.find('_vis') != -1:
            img = cv2.imread(result_path + '/' + n)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if img[i, j, 0] != 0 or img[i, j, 1] != 0 or img[i, j,
                                                                     2] != 0:
                        img[i, j] = (255, 255, 255)
            cv2.imwrite(result_path + '/' + n.replace('_vis', '_binary'), img)
            print('create ' + result_path + '/' + n.replace('_vis', '_binary'))


def create_combine_png(result_path):
    names = os.listdir(result_path)
    for n in names:
        if n.find('.png') != -1 and n.find('_binary') != -1:
            img1 = cv2.imread(result_path + '/' + n)
            img2 = cv2.imread(result_path + '/' + n.replace('_binary', ''))
            for i in range(img1.shape[0]):
                for j in range(img1.shape[1]):
                    if img1[i, j, 0] == 0 and img1[i, j, 1] == 0 and img1[
                            i, j, 2] == 0:
                        img2[i, j] = (0, 0, 0)
            cv2.imwrite(result_path + '/' + n.replace('_binary', '_combine'),
                        img2)
            print('create ' + result_path + '/' +
                  n.replace('_binary', '_combine'))


def delete_blue(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j, 0] == 221 and img[i, j, 1] == 119 and img[i, j,
                                                                   2] == 0:
                img[i, j] = (0, 0, 0)


def copy_images(DATA_DIR, result_path):
    names = os.listdir(DATA_DIR + '/images/')
    for n in names:
        shutil.copy(DATA_DIR + '/images/' + n, result_path)
        print('copy ' + DATA_DIR + '/images/' + n, result_path)
    names = os.listdir('./output/cihp_parsing_maps/')
    for n in names:
        if n.find('.png') != -1 and n.find('_vis') != -1:
            img = cv2.imread('./output/cihp_parsing_maps/' + n)
            delete_blue(img)
            cv2.imwrite(result_path + '/' + n, img)
            print('copy ' + './output/cihp_parsing_maps/' + n, result_path)


if __name__ == '__main__':
    input_path = 'G:/20191202_human'
    output_path = 'G:/human/CIHP_PGN/datasets/output'
    result_path = 'G:/result/PGN_trans_rgb'
    if os.path.exists(output_path):
        shutil.rmtree(output_path, True)
    start = time()
    create_test_data(input_path, output_path)
    test(output_path, result_path)
    stop = time()
    use_time = stop - start
    print('处理' + str(image_count) + '张图片用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')
