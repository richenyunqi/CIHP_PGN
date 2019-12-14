import os
import cv2


def is_background(img, x, y):
    return (all([img[x, y, i] > 165 for i in range(3)]) and all([
        abs(int(img[x, y, i]) - img[x, y, (i + 1) % 3]) < 20 for i in range(3)
    ]))


def is_mark(img, x, y):
    return (img[x, y, 0] < 100 and img[x, y, 1] > 100 and img[x, y, 2] < 100
            and int(img[x, y, 1]) - int(img[x, y, 0]) > 60
            and int(img[x, y, 1]) - int(img[x, y, 2]) > 60
            and abs(int(img[x, y, 0]) - int(img[x, y, 2])) <= 20) or (
                img[x, y, 0] > 70 and img[x, y, 1] > 10 and img[x, y, 2] > 70
                and int(img[x, y, 0]) - int(img[x, y, 1]) > 50
                and int(img[x, y, 2]) - int(img[x, y, 1]) > 50)


def trans_bgr(img, x, y, new_bgr, f):
    if f(img, x, y):
        img[x, y] = new_bgr


def trans_mark_bgr(img, x, y):
    trans_bgr(img, x, y, (66, 108, 153), is_mark)


def trans_background_bgr(img, x, y):
    trans_bgr(img, x, y, (150, 150, 150), is_background)


if __name__ == '__main__':
    images_path = 'C:/Users/jf/Desktop/1'
    images_dir = os.listdir(images_path)
    for image in images_dir:
        img = cv2.imread(os.path.join(images_path, image))
        print('read ' + os.path.join(images_path, image))
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                trans_background_bgr(img, i, j)
                trans_mark_bgr(img, i, j)
        cv2.imwrite('C:/Users/jf/Desktop/test/2/mark' + '/' + image, img)
