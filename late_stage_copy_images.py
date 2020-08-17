import os
import shutil
from time import time
import cv2
# def removeFiles(path):
#     names = os.listdir(path)
#     for name in names:
#         p = os.path.join(path, name)
#         if os.path.isdir(p):
#             removeFiles(p)
#         elif 'COMBINE' in name:
#             os.remove(p)
#             print('remove', p)


def copy_images(input_path, output_path, suffix):
    print(output_path)
    images_num = 0
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print('create ' + output_path)
    global image_count
    names = os.listdir(input_path)
    for name in names:
        image_path = os.path.join(input_path, name)
        if os.path.isfile(image_path):
            shutil.copyfile(
                image_path,
                os.path.join(output_path,
                             name.replace('.JPG', '_' + suffix + '.JPG')))
            images_num += 1
        else:
            print('错误！' + image_path + '是一个目录')
    print('copy', input_path)
    return images_num


def copy_main():
    images_num = 0
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
            for i in ['MASK', 'COMBINE', 'PARSING']:
                images_num += copy_images(
                    os.path.join(input_path, path + '_' + i), output_path,
                    path + '_' + i)
            images_num += copy_images(input_data_path, output_path,
                                      path + '_adata')
    stop = time()
    use_time = stop - start
    print('拷贝' + str(images_num) + '张图片用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')


def copy_fillup_images(fillup_path, path):
    image_names = os.listdir(fillup_path)
    for name in image_names:
        if 'MASK' in name:
            original_img = cv2.imread(
                os.path.join(fillup_path, name.replace('MASK', 'adata')))
            mask_img = cv2.imread(os.path.join(fillup_path, name))
            combine_img = cv2.copyTo(original_img, mask_img)
            cv2.imwrite(
                os.path.join(fillup_path, name.replace('MASK', 'COMBINE')),
                combine_img)
            print('create',
                  os.path.join(fillup_path, name.replace('MASK', 'COMBINE')))
    for name in image_names:
        if any(i in name for i in ['MASK', 'COMBINE', 'PARSING']):
            shutil.copyfile(os.path.join(fillup_path, name),
                            os.path.join(path, name))
            print('copy', os.path.join(fillup_path, name), 'to',
                  os.path.join(path, name))


def return_main(fillup_path, input_path, result_path):
    # copy_fillup_images(fillup_path, input_path)
    images_num = 0
    start = time()
    image_names = os.listdir(input_path)
    for name in image_names:
        if any(i in name for i in ['MASK', 'COMBINE', 'PARSING']):
            name_split = name.replace('.JPG', '').split('_')
            dir_name = name_split[-6:]
            cur_result_path = os.path.join(result_path, dir_name[0],
                                           '_'.join(dir_name[0:5]),
                                           '_'.join(dir_name))
            if not os.path.exists(cur_result_path):
                os.makedirs(cur_result_path)
            shutil.copyfile(
                os.path.join(input_path, name),
                os.path.join(cur_result_path,
                             '_'.join(name_split[:5]) + '.JPG'))
            print(
                'copy', os.path.join(input_path, name), 'to',
                os.path.join(cur_result_path,
                             '_'.join(name_split[:5]) + '.JPG'))
            images_num += 1
    stop = time()
    use_time = stop - start
    print('拷贝' + str(images_num) + '张图片用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')


if __name__ == '__main__':
    # copy_main()
    return_main('F:/human/result/ttt', 'F:/human/result/t',
                'F:/human/result/jieguo')
    # removeFiles('F:/human/result/temp')