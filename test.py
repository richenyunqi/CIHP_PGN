import os
import cv2
import numpy as np
import queue
from time import time


def bfs(img, x, y):
    visit = set([(x, y)])
    q = queue.Queue()
    q.put((x, y))
    direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    height, width = img.shape[:2]
    while not q.empty():
        i, j = q.get()
        for ii, jj in direction:
            if ii + i >= 0 and ii + i < height and jj + j >= 0 and jj + j < width and not (
                    ii + i, jj + j) in visit and img[ii + i, jj + j] == 0:
                q.put((ii + i, jj + j))
                visit.add((ii + i, jj + j))
                if len(visit) > 150:
                    return False, visit
    return True, visit


def create_binary_png(result_path):
    names = os.listdir(result_path)
    for n in names:
        if n.find('.png') != -1 and n.find('_vis') != -1:
            img = cv2.imread(os.path.join(result_path, n))
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            r, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if img[i, j] == 0:
                        flag, visit = bfs(img, i, j)
                    if flag:
                        for x, y in visit:
                            img[x, y] = 255
            cv2.imwrite(
                os.path.join(result_path, n.replace('_vis', '_binary_vis')),
                img)
            print('create ' +
                  os.path.join(result_path, n.replace('_vis', '_binary_vis')))


def create_inRange_png(result_path):
    names = os.listdir(result_path)
    for n in names:
        if n.find('.png') != -1 and n.find('_combine.png') != -1:
            img = cv2.imread(os.path.join(result_path, n))
            img = cv2.inRange(img, np.array([0, 0, 0]),
                              np.array([149, 149, 149]))
            cv2.imwrite(
                os.path.join(result_path,
                             n.replace('_black', '_binary_black.png')), img)
            print('create ' + os.path.join(
                result_path, n.replace('_black', '_binary_black.png')))


#黑色变白色
def create_combine_png(result_path):
    names = os.listdir(result_path)
    for n in names:
        if n.find('.png') != -1 and n.find('_binary') != -1:
            img1 = cv2.imread(os.path.join(result_path, n))
            img2 = cv2.imread(
                os.path.join(result_path, n.replace('_binary', '')))
            for i in range(img1.shape[0]):
                for j in range(img1.shape[1]):
                    if img1[i, j, 0] == 0 and img1[i, j, 1] == 0 and img1[
                            i, j, 2] == 0:
                        img2[i, j] = (255, 255, 255)
                    elif 140 < img2[i, j, 0] < 160 and 140 < img2[
                            i, j, 1] < 160 and 140 < img2[i, j, 2] < 160:
                        img1[i, j] = (0, 0, 0)
                        img2[i, j] = (255, 255, 255)
            cv2.imwrite(os.path.join(result_path, n), img1)
            cv2.imwrite(
                os.path.join(result_path, n.replace('_binary', '_combine')),
                img2)
            print('create ' +
                  os.path.join(result_path, n.replace('_binary', '_combine')))
            img2 = cv2.imread(
                os.path.join(result_path, n.replace('_binary', '')))
            for i in range(img1.shape[0]):
                for j in range(img1.shape[1]):
                    if img1[i, j, 0] != 0 or img1[i, j, 1] != 0 or img1[
                            i, j, 2] != 0:
                        img2[i, j] = (255, 255, 255)
            cv2.imwrite(
                os.path.join(result_path, n.replace('_binary', '_combine_2')),
                img2)
            print(
                'create ' +
                os.path.join(result_path, n.replace('_binary', '_combine_2')))


if __name__ == '__main__':
    result_path = 'C:/Users/jf/Desktop/13-4'
    start = time()
    # create_binary_png(result_path)
    create_combine_png(result_path)
    # create_inRange_png(result_path)
    stop = time()
    use_time = stop - start
    print('处理用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')