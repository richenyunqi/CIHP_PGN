import os
import shutil
import sys
from time import time
import cv2

image_count = 0


def copy_images(input_path, output_path):
    print(output_path)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
        print('create ' + output_path)
    global image_count
    names = os.listdir(input_path)
    for name in names:
        image_path = os.path.join(input_path, name)
        if os.path.isfile(image_path):
            image_count += 1
            shutil.copyfile(image_path, os.path.join(output_path, name))
        else:
            print('错误！' + image_path + '是一个目录')


if __name__ == '__main__':
    start = time()
    start_path = input('输入盘符：')
    output_path = input('输出路径：')
    with open('./input.txt', 'r') as f:
        for path in f.readlines():
            path = path.rstrip('\n')
            p = path.split('_')
            input_images_path = start_path + ':/' + p[
                0] + '/' + 'data_four_pose/' + p[1] + '/' + p[2].lstrip(
                    '0') + '/' + p[3] + '_' + p[4]
            output_images_path = os.path.join(output_path, path)
            copy_images(input_images_path, output_images_path)
    stop = time()
    use_time = stop - start
    print('处理' + str(image_count) + '张图片用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')