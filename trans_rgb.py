import os
import cv2


def is_skin(r, g, b):
    return r > 70 and g > 40 and b > 20 and int(r) - int(g) >= 10 and int(
        g) - int(b) > 10


def is_background(img, x, y):
    return (all([img[x, y, i] > 165 for i in range(3)]) and all([
        abs(int(img[x, y, i]) - img[x, y, (i + 1) % 3]) < 20 for i in range(3)
    ]))


def is_mark(r, g, b):
    yellow = 140 < r < 220 and 120 < g < 210 and 10 < b < 100 and 0 < (
        int(r) - int(g)) < 25 and 100 < (int(r) - int(b))
    purple = 20 < r < 80 and 30 < g < 80 and 60 < b < 160 and 0 < (
        int(g) - int(r)) < 30 and 40 < (int(b) - int(r)) < 90
    return yellow or purple


def trans_bgr(img, x, y, new_bgr, f):
    if f(img, x, y):
        img[x, y] = new_bgr


def trans_mark_bgr(img, x, y):
    trans_bgr(img, x, y, (66, 108, 153), is_mark)


def trans_background_bgr(img, x, y):
    trans_bgr(img, x, y, (150, 150, 150), is_background)


if __name__ == '__main__':
    # images_path = 'C:/Users/jf/Desktop/1'
    # images_dir = os.listdir(images_path)
    # for image in images_dir:
    #     img = cv2.imread(os.path.join(images_path, image))
    #     print('read ' + os.path.join(images_path, image))
    #     for i in range(img.shape[0]):
    #         for j in range(img.shape[1]):
    #             trans_background_bgr(img, i, j)
    #             # trans_mark_bgr(img, i, j)
    #     cv2.imwrite('C:/Users/jf/Desktop/test/2/mark' + '/' + image, img)
    pass
