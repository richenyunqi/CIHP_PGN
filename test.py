import os
import shutil
import sys
import cv2
from time import time

image_count = 0


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


if __name__ == '__main__':
    original_path = 'G:/20191209'
    result_path = 'G:/result/20191209'
    start = time()
    create_dir_combine_png(original_path, result_path)
    stop = time()
    use_time = stop - start
    print('处理' + str(image_count) + '张图片用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')