import os
import cv2
from collections import deque
import queue
from trans_rgb import is_skin
from time import time
# image_count = 0


def bfs(adata_img, mask_img, x, y, visit, height, width):
    q = deque([(x, y)])
    visit.add((x, y))
    bfs_visit = set()
    bfs_visit.add((x, y))
    mask_img[x, y] = 255
    while q:
        x, y = q.popleft()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i + x < 0 or i + x >= height or j + y < 0 or j + y >= width or (
                        i + x, j + y) in visit:
                    continue
                (b, g, r) = adata_img[i + x, j + y]
                if mask_img[i + x, j + y] == 255 or is_skin(r, g, b):
                    visit.add((i + x, j + y))
                    bfs_visit.add((i + x, j + y))
                    mask_img[i + x, j + y] = 255
                    q.append((i + x, j + y))
    return bfs_visit


def bfs2(img, img_hat, x, y):
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
                          and img_hat[ii + i + 1, jj + j] == 0) or (
                              jj + j > 0 and img[ii + i, jj + j - 1] == 0
                              and img_hat[ii + i, jj + j - 1] == 0) or (
                                  jj + j < width - 1
                                  and img[ii + i, jj + j + 1] == 0
                                  and img_hat[ii + i, jj + j + 1] == 0):
                    flag = False
    return flag and len(visit) < 200, visit


def fill_up_mask_image(dir_path):
    images_name = os.listdir(dir_path)
    for image_name in images_name:
        if '_vis.png' in image_name:
            mask_img = cv2.imread(os.path.join(dir_path, image_name))
            mask_img = cv2.cvtColor(mask_img, cv2.COLOR_BGR2GRAY)
            r, mask_img = cv2.threshold(mask_img, 0, 255, cv2.THRESH_BINARY)
            adata_img = cv2.imread(
                os.path.join(dir_path, image_name.replace('_vis', '_adata')))
            height, width = mask_img.shape[:2]
            visit = set()
            for i in range(height):
                for j in range(width):
                    (b, g, r) = adata_img[i, j]
                    if (i, j) in visit:
                        continue
                    if ((i == 0 or i == height - 1 or j == 0 or j == width - 1)
                            and is_skin(r, g, b)) or mask_img[i, j] == 255:
                        bfs_visit = bfs(adata_img, mask_img, i, j, visit,
                                        height, width)
                        if len(bfs_visit) < 30:
                            for x, y in bfs_visit:
                                mask_img[x, y] = 0
            img_hat = cv2.morphologyEx(
                mask_img, cv2.MORPH_BLACKHAT,
                cv2.getStructuringElement(cv2.MORPH_RECT, (14, 14)))
            for i in range(mask_img.shape[0]):
                for j in range(mask_img.shape[1]):
                    if img_hat[i, j] != 0:
                        flag, bfs_visit = bfs2(mask_img, img_hat, i, j)
                        if flag:
                            for x, y in bfs_visit:
                                mask_img[x, y] = 255
            cv2.imwrite(
                os.path.join(dir_path, image_name.replace('_vis', '_binary')),
                mask_img)
            print(
                'create',
                os.path.join(dir_path, image_name.replace('_vis', '_binary')))


if __name__ == '__main__':
    input_path = 'C:/Users/jf/Desktop/test/result/original/20200112'
    start = time()
    fill_up_mask_image(input_path)
    stop = time()
    use_time = stop - start
    print('处理' + input_path + '中的' + str(image_count) + '张图片用时为' +
          str(use_time // 3600) + '小时:' + str(use_time % 3600 // 60) + '分:' +
          str(use_time % 60) + '秒')
    print('--------------end-----------------')