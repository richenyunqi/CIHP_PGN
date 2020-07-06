import os
import shutil
import sys
from time import time

image_count = 0


def copy_images(input_path, result_path):
    global image_count
    names = os.listdir(input_path)
    for name in names:
        if '_vis.png' in name:
            image_count += 1
            i = name.find('_', name.find('FRM') + 4)
            dir_name = name[:i]
            result_dir_path = os.path.join(result_path, dir_name,
                                           dir_name + '_ORIGINAL_PARSING')
            if not os.path.exists(result_dir_path):
                os.makedirs(result_dir_path)
            new_image_name = name[i + 1:]
            shutil.copyfile(
                os.path.join(input_path, name),
                os.path.join(result_dir_path,
                             new_image_name.replace('_vis.png', '.png')))
            print(
                'copy', os.path.join(input_path, name), 'to',
                os.path.join(result_dir_path,
                             new_image_name.replace('_vis.png', '.png')))


if __name__ == '__main__':
    input_path = 'F:/human/result/original'
    result_path = 'F:/human/result/final'
    start = time()
    input_dirs = os.listdir(input_path)
    for name in input_dirs:
        copy_images(os.path.join(input_path, name),
                    os.path.join(result_path, name))
    stop = time()
    use_time = stop - start
    print('处理' + str(image_count) + '张图片用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')