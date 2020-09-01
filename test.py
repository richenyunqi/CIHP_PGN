import os
import cv2
import shutil


def main(input_path, result_path):
    image_names = os.listdir(input_path)
    for name in image_names:
        if any(i in name for i in ['MASK', 'COMBINE', 'PARSING']):
            name_split = name.replace('.JPG', '').split('_')
            dir_name = name_split[-6:]
            cur_result_path = os.path.join(result_path, dir_name[0],
                                           '_'.join(dir_name[0:5]),
                                           '_'.join(dir_name))
            shutil.copyfile(
                os.path.join(
                    cur_result_path, '_'.join(name_split[:(
                        4 if name_split[4].startswith('2020') else 5)])) +
                '.JPG',
                os.path.join(
                    input_path,
                    name.replace('MASK', 'ZMASK').replace(
                        'COMBINE', 'ZCOMBINE').replace('PARSING', 'ZPARSING')))
            print(
                'copy',
                os.path.join(cur_result_path, '_'.join(name_split[:-6])) +
                '.JPG', 'to',
                os.path.join(
                    input_path,
                    name.replace('MASK', 'ZMASK').replace(
                        'COMBINE', 'ZCOMBINE').replace('PARSING', 'ZPARSING')))


if __name__ == '__main__':
    main('H:/images', 'F:/human/result/final')
