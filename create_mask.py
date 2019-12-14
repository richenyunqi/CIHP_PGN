import os
import shutil
import sys
import cv2


def create_mask_png(input_path):
    names = os.listdir(input_path)
    for n in names:
        if n.find('.png') != -1 and n.find('_combine') != -1:
            img = cv2.imread(input_path + '/' + n)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if img[i, j, 0] != 255 or img[i, j, 1] != 255 or img[
                            i, j, 2] != 255:
                        img[i, j] = (255, 255, 255)
                    else:
                        img[i, j] = (0, 0, 0)
            cv2.imwrite(input_path + '/' + n.replace('_combine', '_binary'),
                        img)
            print('create ' + input_path + '/' +
                  n.replace('_combine', '_binary'))


def copy_images(input_path, result_path):
    names = os.listdir(input_path)
    for n in names:
        if n.find('.png') != -1 and n.find('_binary') != -1:
            shutil.copy(input_path + '/' + n, result_path)
            print('copy ' + input_path + '/' + n, result_path)


if __name__ == '__main__':
    input_path = 'C:/Users/jf/Desktop/combine'
    result_path = 'G:/result/20191209_9_groups'
    # create_mask_png(input_path)
    copy_images(input_path, result_path)
    print('--------------end-----------------')