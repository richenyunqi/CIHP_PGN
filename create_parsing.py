import os
import shutil
import sys
import cv2
from time import time
image_count = 0


def create_parsing_png(input_path):
    names = os.listdir(input_path)
    global image_count
    clothes_rgb = set([(0, 128, 0), (0, 85, 85), (255, 85, 0), (0, 0, 85),
                       (0, 119, 221)])  #分割出来的衣服颜色
    for n in names:
        # if os.path.exists(os.path.join(input_path, n.replace('_vis',
        #                                                      '_vis2'))):
        #     continue
        if '_vis.png' in n:
            image_count += 1
            img = cv2.imread(input_path + '/' + n)
            mask_img = cv2.imread(input_path + '/' +
                                  n.replace('_vis', '_binary'))
            original_img = cv2.imread(input_path + '/' + n.replace('_vis', ''))
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    (b, g, r) = img[i, j]
                    (bm, gm, rm) = mask_img[i, j]
                    (bo, go, ro) = original_img[i, j]
                    parsing_rgb = (r, g, b)
                    mask_rgb = (rm, gm, bm)
                    if mask_rgb == (0, 0, 0):
                        img[i, j] = (0, 0, 0)
                    elif parsing_rgb == (255, 0, 0) or parsing_rgb == (
                            128, 0, 0) or parsing_rgb == (0, 0, 255):
                        continue
                    elif parsing_rgb in clothes_rgb or (
                            parsing_rgb == (0, 0, 0)
                            and not (ro > 70 and go > 40 and bo > 20
                                     and int(ro) - int(go) >= 10
                                     and int(go) - int(bo) >= 10)):
                        img[i, j] = (0, 255, 0)  #衣服颜色
                    else:
                        img[i, j] = (128, 0, 128)  #皮肤颜色
            cv2.imwrite(input_path + '/' + n.replace('_vis', '_vis2'), img)
            print('create ' + input_path + '/' + n)


if __name__ == '__main__':
    input_path = 'F:\\human\\result\\original\\20200117'
    start = time()
    create_parsing_png(input_path)
    stop = time()
    use_time = stop - start
    print('处理' + input_path + '中的' + str(image_count) + '张图片用时为' +
          str(use_time // 3600) + '小时:' + str(use_time % 3600 // 60) + '分:' +
          str(use_time % 60) + '秒')
    print('--------------end-----------------')