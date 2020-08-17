import os
import shutil
from time import time
import sys
import cv2
from copy_input_images import copy_main
from my_test_pgn import Test
# from circle import detect_circle
from trans_rgb import trans_background_bgr
from write_txt import (write_image_list, write_train, write_train_id,
                       write_train_rev, write_val, write_val_id)
import queue
image_count = 0


# 还没有重构
def trans_bgr(img):
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # trans_mark_bgr(img, i, j)
            trans_background_bgr(img, i, j)


# 调整大小


def image_resize(image_path):
    img = cv2.imread(image_path)
    # img = detect_circle(img)
    height, width = img.shape[:2]
    new_height = 400
    new_width = int(new_height * width / height)
    if height > width:
        new_width = 400
        new_height = int(new_width * height / width)
    return cv2.resize(img, (new_width, new_height)), new_width, new_height


# 调整大小、写入
def image_resize_output(image_path, output_path, result_path):
    global image_count
    image_count += 1
    file_path = os.path.split(image_path)
    image_name = file_path[1]
    dir_name = os.path.split(file_path[0])[1]
    new_img, new_width, new_height = image_resize(image_path)
    cv2.imwrite(
        os.path.join(result_path,
                     dir_name + '_' + image_name[:-4] + '_adata.png'), new_img)
    print('output ' +
          os.path.join(result_path, dir_name + '_' + image_name[:-4] +
                       '_adata.png'))
    trans_bgr(new_img)
    # new_img = detect_circle(new_img)
    cv2.imwrite(
        os.path.join(output_path, dir_name + '_' + image_name[:-4] + '.png'),
        new_img)
    print('output ' +
          os.path.join(output_path, dir_name + '_' + image_name[:-4] + '.png'))
    return new_width, new_height


def black_image_resize_output(input_image_path, output_image_path, width,
                              height):
    img = cv2.imread(input_image_path)
    new_img = cv2.resize(img, (width, height))
    cv2.imwrite(output_image_path[:-4] + '.png', new_img)
    print('output ' + output_image_path)


def create_black_image(image_name, output_path, width, height):
    for dirn in ['/edges', '/labels', '/labels_rev']:
        output_image_dir_path = output_path + dirn
        if not os.path.exists(output_image_dir_path):
            os.mkdir(output_image_dir_path)
        black_image_resize_output(
            './datasets/CIHP/edges/0026375.png',
            os.path.join(output_image_dir_path, image_name), width, height)


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
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    shutil.copy('./datasets/CIHP/tool/reverse_label.m', output_path)
    shutil.copy('./datasets/CIHP/tool/write_edge.m', output_path)


def create_test_data(input_path, output_path, result_path):
    images_names = os.listdir(input_path)
    print('Process ' + input_path)
    # if os.path.exists(output_path):
    #     shutil.rmtree(output_path, True)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    for name in images_names:
        if os.path.isdir(os.path.join(input_path, name)):
            create_test_data(os.path.join(input_path, name), output_path,
                             result_path)
        elif '.txt' not in name:
            if not os.path.exists(output_path + '/images'):
                os.mkdir(output_path + '/images')
            width, height = image_resize_output(
                os.path.join(input_path, name),
                os.path.join(output_path, 'images'), result_path)
            create_black_image(
                os.path.split(input_path)[1] + '_' + name, output_path, width,
                height)
    if os.path.isfile(os.path.join(input_path, images_names[0])):
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


def bfs(img, img_hat, x, y):
    visit = set([(x, y)])
    q = queue.Queue()
    q.put((x, y))
    direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    height, width = img.shape[:2]
    flag = True
    while not q.empty():
        i, j = q.get()
        for ii, jj in direction:
            if ii + i >= 0 and ii + i < height and jj + j >= 0 and jj + j < width and not (
                    ii + i, jj + j) in visit and img_hat[ii + i, jj + j] != 0:
                q.put((ii + i, jj + j))
                visit.add((ii + i, jj + j))
                if (ii + i > 0 and img[ii + i - 1, jj + j] == 0
                        and img_hat[ii + i - 1, jj + j] == 0
                    ) or (ii + i < height - 1 and img[ii + i + 1, jj + j] == 0
                          and img_hat[ii + i + 1, jj + j] == 0) or (
                              jj + j > 0 and img[ii + i, jj + j - 1] == 0
                              and img_hat[ii + i, jj + j - 1] == 0) or (
                                  jj + j < width - 1
                                  and img[ii + i, jj + j + 1] == 0
                                  and img_hat[ii + i, jj + j + 1] == 0):
                    flag = False
    return flag and len(visit) < 200, visit


def create_binary_png(result_path):
    names = os.listdir(result_path)
    for n in names:
        if n.find('.png') != -1 and n.find('_vis') != -1:
            img = cv2.imread(os.path.join(result_path, n))
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            r, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)
            kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (14, 14))
            img_hat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernal)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if img_hat[i, j] != 0:
                        flag, visit = bfs(img, img_hat, i, j)
                        if flag:
                            for x, y in visit:
                                img[x, y] = 255
            cv2.imwrite(
                os.path.join(result_path, n.replace('_vis', '_binary')), img)
            print('create ' +
                  os.path.join(result_path, n.replace('_vis', '_binary')))


#黑色变白色
def create_combine_png(result_path):
    names = os.listdir(result_path)
    for n in names:
        if n.find('.png') != -1 and n.find('_binary') != -1:
            img1 = cv2.imread(os.path.join(result_path, n))
            img2 = cv2.imread(
                os.path.join(result_path, n.replace('_binary', '')))
            for i in range(img1.shape[0]):
                for j in range(img1.shape[1]):
                    if img1[i, j, 0] == 0 and img1[i, j, 1] == 0 and img1[
                            i, j, 2] == 0:
                        img2[i, j] = (255, 255, 255)
            cv2.imwrite(
                os.path.join(result_path, n.replace('_binary', '_combine')),
                img2)
            print('create ' +
                  os.path.join(result_path, n.replace('_binary', '_combine')))
            img2 = cv2.imread(
                os.path.join(result_path, n.replace('_binary', '')))
            for i in range(img1.shape[0]):
                for j in range(img1.shape[1]):
                    if img1[i, j, 0] != 0 or img1[i, j, 1] != 0 or img1[
                            i, j, 2] != 0:
                        img2[i, j] = (255, 255, 255)
            cv2.imwrite(
                os.path.join(result_path, n.replace('_binary', '_combine_2')),
                img2)
            print(
                'create ' +
                os.path.join(result_path, n.replace('_binary', '_combine_2')))


def copy_images(DATA_DIR, result_path):
    names = os.listdir(DATA_DIR + '/images/')
    for n in names:
        shutil.copy(DATA_DIR + '/images/' + n, result_path)
        print('copy ' + DATA_DIR + '/images/' + n, result_path)
    names = os.listdir('./output/cihp_parsing_maps/')
    for n in names:
        if n.find('.png') != -1 and n.find('_vis') != -1:
            img = cv2.imread('./output/cihp_parsing_maps/' + n)
            cv2.imwrite(result_path + '/' + n, img)
            print('copy ' + './output/cihp_parsing_maps/' + n, result_path)


if __name__ == '__main__':
    input_path = 'F:/human/data/20200114'
    output_path = 'G:/program/CIHP_PGN/datasets/20200114'
    result_path = 'F:/human/result/original/20200114'
    time_path = './time.txt'
    # copy_main(input_path)
    if os.path.exists(result_path):
        shutil.rmtree(result_path, True)
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    with open(time_path, 'a') as f:
        start = time()
        create_test_data(input_path, output_path, result_path)
        test(output_path, result_path)
        stop = time()
        use_time = stop - start
        print('处理' + input_path + '中的' + str(image_count) + '张图片用时为' +
              str(use_time // 3600) + '小时:' + str(use_time % 3600 // 60) +
              '分:' + str(use_time % 60) + '秒')
        f.write('处理' + input_path + '中的' + str(image_count) + '张图片用时为' +
                str(use_time // 3600) + '小时:' + str(use_time % 3600 // 60) +
                '分:' + str(use_time % 60) + '秒\n')
        print('--------------end-----------------')
