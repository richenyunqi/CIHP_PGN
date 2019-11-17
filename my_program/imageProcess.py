import cv2
import os

path = './copy/horrible/'
for n in os.listdir(path):
    if not os.path.isdir(n) and n.find('.png') != -1 and n.find('_vis') != -1:
        img = cv2.imread(path + n)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i, j, 0] != 0 or img[i, j, 1] != 0 or img[i, j, 2] != 0:
                    img[i, j] = (255, 255, 255)
        cv2.imwrite(path + os.path.splitext(n)[0] + '_binary.png', img)
