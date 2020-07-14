import os
import shutil
import sys
import math


def images_count(flag, names):
    return len([i for i in names if flag in i])


def statics(terrible_path):
    original_path = terrible_path.replace('terrible', 'original')
    names = os.listdir(terrible_path)
    for n in names:
        terrible_images_path = os.path.join(terrible_path, n)
        original_images_path = os.path.join(original_path, n)
        terrible_images_names = os.listdir(terrible_images_path)
        terrible_M = images_count('_M_', terrible_images_names) / 5
        terrible_W = images_count('_W_', terrible_images_names) / 5
        original_images_names = os.listdir(original_images_path)
        original_M = images_count('_M_', original_images_names) / 6
        original_W = images_count('_W_', original_images_names) / 6
        print(n, ':', '{M:', terrible_M, original_M,
              terrible_M / original_M if original_M != 0 else math.inf,
              '},{W:', terrible_W, original_W,
              terrible_W / original_W if original_W != 0 else math.inf, '}')


if __name__ == '__main__':
    # statics('F:/human/result/terrible')
    print('{0:d}'.format(1))
