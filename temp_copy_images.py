import os
import shutil
from time import time
import os

image_count = 0


def removeFiles(path):
    names = os.listdir(path)
    for name in names:
        p = os.path.join(path, name)
        if os.path.isdir(p):
            removeFiles(p)
        elif 'COMBINE' in name:
            os.remove(p)
            print('remove', p)


def copy_images(input_path, output_path, suffix):
    # print(output_path)
    # if not os.path.exists(output_path):
    #     os.makedirs(output_path)
    #     print('create ' + output_path)
    global image_count
    names = os.listdir(input_path)
    for name in names:
        image_path = os.path.join(input_path, name)
        if os.path.isfile(image_path):
            shutil.copyfile(
                image_path,
                os.path.join(output_path,
                             name.replace('.JPG', '_' + suffix + '.JPG')))
            image_count += 1
        else:
            print('错误！' + image_path + '是一个目录')
    print('copy', input_path)


def copy_main():
    start = time()
    start_path = 'F:/human/result'
    start_data_path = 'F:/human/data'
    output_path = os.path.join(start_path, 't')
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open('./input.txt', 'r') as f:
        for path in f.readlines():
            path = path.rstrip('\n')
            p = path.split('_')
            input_path = os.path.join(start_path, 'final', p[0], path)
            input_data_path = os.path.join(start_data_path, p[0], path)
            # for i in ['COMBINE']:
            for i in ['MASK', 'COMBINE', 'PARSING']:
                copy_images(os.path.join(input_path, path + '_' + i),
                            output_path, path + '_' + i)
            copy_images(input_data_path, output_path, path + '_adata')
    stop = time()
    use_time = stop - start
    print('拷贝' + str(image_count) + '张图片用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')


if __name__ == '__main__':
    copy_main()
    # removeFiles('F:/human/result/temp')