import os
import cv2
from time import time

image_count=0
# 调整大小、写入
def image_resize_output(image_path, output_path):
    global image_count
    image_count += 1
    file_path = os.path.split(image_path)
    image_name = file_path[1]
    dir_name = os.path.split(file_path[0])[1]
    img = cv2.imread(image_path)
    # img = detect_circle(img)
    height, width = img.shape[:2]
    if height == 3456 and width == 5184:
        img = cv2.flip(img, 0)
        img = cv2.transpose(img)
        cv2.imwrite(image_path, img)
        height, width = width, height
    new_height = 400
    new_width = int(new_height * width / height)
    if height > width:
        new_width = 400
        new_height = int(new_width * height / width)
    new_img = cv2.resize(img, (new_width, new_height))
    # trans_bgr(new_img)
    # new_img = detect_circle(new_img)
    cv2.imwrite(
        os.path.join(output_path, dir_name + '_' + image_name[:-4] + '.png'),
        new_img)
    print('output ' +
          os.path.join(output_path, dir_name + '_' + image_name[:-4] + '.png'))
    return new_width, new_height


if __name__ == '__main__':
    image_path = 'C:/Users/jf/Desktop/1/2.JPG'
    output_path = 'C:/Users/jf/Desktop/2'
    start = time()
    image_resize_output(image_path, output_path)
    stop = time()
    use_time = stop - start
    print('处理用时为' + str(use_time // 3600) + '小时:' +
          str(use_time % 3600 // 60) + '分:' + str(use_time % 60) + '秒')
    print('--------------end-----------------')