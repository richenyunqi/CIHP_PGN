import os
import cv2
import numpy as np
import queue


def bfs(img, img_hat, x, y):
    visit = set([(x, y)])
    q = queue.Queue()
    q.put((x, y))
    direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    height, width = img.shape[:2]
    flag = True
    while not q.empty():
        i, j = q.get()
        for ii, jj in direction:
            if ii + i >= 0 and ii + i < height and jj + j >= 0 and jj + j < width and not (
                    ii + i, jj + j) in visit and img_hat[ii + i, jj + j] != 0:
                q.put((ii + i, jj + j))
                visit.add((ii + i, jj + j))
                if (ii + i > 0 and img[ii + i - 1, jj + j] == 0
                        and img_hat[ii + i - 1, jj + j] == 0
                    ) or (ii + i < height - 1 and img[ii + i + 1, jj + j] == 0
                          and img_hat[ii + i + 1, jj + j] == 0):
                    flag = False
    return flag and len(visit) < 150, visit


def create_binary_png(result_path):
    names = os.listdir(result_path)
    for n in names:
        if n.find('.png') != -1 and n.find('_vis') != -1:
            img = cv2.imread(os.path.join(result_path, n))
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            r, img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)
            kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
            cv2.imwrite(
                os.path.join(result_path, n.replace('_vis', '_binary_close')),
                cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernal))
            print(
                'create ' +
                os.path.join(result_path, n.replace('_vis', '_binary_close')))
            img_hat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernal)
            cv2.imwrite(os.path.join(result_path, n.replace('_vis', '_black')),
                        img_hat)
            print('create ' +
                  os.path.join(result_path, n.replace('_vis', '_black')))
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if img_hat[i, j] != 0:
                        flag, visit = bfs(img, img_hat, i, j)
                        if flag:
                            for x, y in visit:
                                img[x, y] = 255
            img_hat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernal)
            cv2.imwrite(
                os.path.join(result_path, n.replace('_vis', '_black_2')),
                img_hat)
            cv2.imwrite(
                os.path.join(result_path, n.replace('_vis', '_binary_2')), img)
            print('create ' +
                  os.path.join(result_path, n.replace('_vis', '_binary_2')))


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


def create_combine_png(result_path):
    print(result_path)
    names = os.listdir(result_path)
    for name in names:
        if name.find('_binary_close') != -1:
            original_img = cv2.imread(
                os.path.join(result_path, name.replace('_binary_close', '')))
            mask_img = cv2.imread(os.path.join(result_path, name))
            combine_img = cv2.copyTo(original_img, mask_img)
            cv2.imwrite(
                os.path.join(result_path,
                             name.replace('_binary_close', '_combine_close')),
                combine_img)
            print('create combine JPG: ' + os.path.join(
                result_path, name.replace('_binary_close', '_combine_close')))
        elif name.find('_binary_2') != -1:
            original_img = cv2.imread(
                os.path.join(result_path, name.replace('_binary_2', '')))
            mask_img = cv2.imread(os.path.join(result_path, name))
            combine_img = cv2.copyTo(original_img, mask_img)
            cv2.imwrite(
                os.path.join(result_path,
                             name.replace('_binary_2', '_combine_2')),
                combine_img)
            print('create combine JPG: ' + os.path.join(
                result_path, name.replace('_binary_2', '_combine_2')))


if __name__ == '__main__':
    result_path = 'C:/Users/jf/Desktop/select'
    create_binary_png(result_path)
    create_combine_png(result_path)
    # create_inRange_png(result_path)
    print('--------------end-----------------')