import os
import shutil
import sys
import cv2


def create_mask_png(input_path):
    names = os.listdir(input_path)
    for n in names:
        if '_combine.png' in n:
            img = cv2.imread(input_path + '/' + n)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if img[i, j, 0] != 255 or img[i, j,
                                                  1] != 255 or img[i, j,
                                                                   2] != 255:
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
        if os.path.isdir(os.path.join(input_path, n)):
            copy_images(os.path.join(input_path, n),
                        os.path.join(result_path, n))
        elif '_binary.png' in n or '_combine.png' in n or '_vis2.png' in n:
            shutil.copy(input_path + '/' + n, result_path)
            print('copy ' + input_path + '/' + n, result_path)


if __name__ == '__main__':
    input_path = 'F:/human/temp_result/result/original/20200903'
    create_mask_png(input_path)
    print('--------------end-----------------')