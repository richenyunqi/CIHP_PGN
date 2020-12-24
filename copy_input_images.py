import os
import shutil
from time import time
from PIL.ExifTags import TAGS
import os
import pyexiv2 as ev
import cv2

image_count = 0


def rotate_image_90(input_image_path, output_image_path):
    img = cv2.imread(input_image_path)
    img = cv2.flip(img, 0)
    img = cv2.transpose(img)
    cv2.imwrite(output_image_path, img)
    print(output_image_path, 'has been rotated 90')


def copy_images(input_path, output_path):
    print(output_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print('create ' + output_path)
    global image_count
    names = os.listdir(input_path)
    for name in names:
        image_path = os.path.join(input_path, name)
        if os.path.isfile(image_path):
            image_count += 1
            output_image_path = os.path.join(output_path, name)
            exiv_image = ev.Image(image_path)
            orientation = exiv_image.read_exif()['Exif.Image.Orientation']
            if orientation == '1' and name[0] not in 'HN':
                rotate_image_90(image_path, output_image_path)
            else:
                shutil.copyfile(image_path, output_image_path)
        else:
            os.makedirs(os.path.join(output_path, name))
            copy_images(image_path, os.path.join(output_path, name))


def copy_main(output_path, start_path='p'):
    start = time()
    if start_path == 'p':
        with open('./input.txt', 'r') as f:
            for path in f.readlines():
                path = path.rstrip('\n')
                p = path.split('_')
                input_images_path = start_path + ':/' + p[
                    0] + '/' + 'data_four_pose/' + p[1] + '/' + p[2].lstrip(
                        '0') + '/' + p[3] + '_' + p[4]
                output_images_path = os.path.join(output_path, path)
                copy_images(input_images_path, output_images_path)
    else:
        copy_images(start_path, output_path)
    stop = time()
    use_time = stop - start
    print('拷贝' + str(image_count) + '张图片用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')


if __name__ == '__main__':
    copy_main('F:\\human\\data\\20200113')