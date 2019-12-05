import os
import cv2
result_path = 'C:/Users/jf/Desktop/human/result/2019.12.5_PGN'
names = os.listdir(result_path)
for n in names:
    if n.find('.png') != -1 and n.find('_vis') != -1:
        img = cv2.imread(result_path + '/' + n)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if img[i, j, 0] == 221 and img[i, j, 1] == 119 and img[i, j,
                                                                       2] == 0:
                    img[i, j] = (0, 0, 0)
        cv2.imwrite(result_path + '/' + n.replace('.png', '_2.png'), img)
        print('create ' + result_path + '/' + n.replace('.png', '_2.png'))
