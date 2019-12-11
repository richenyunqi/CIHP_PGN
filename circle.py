import os
import cv2
import numpy as np
import queue
from math import pi


def bfs(img, x, y, direction, r):
    visit = set([(x, y)])
    q = queue.Queue()
    q.put((x, y))
    height, width = img.shape[:2]
    while not q.empty():
        i, j = q.get()
        for ii, jj in direction:
            if ii + i >= 0 and ii + i < height and jj + j >= 0 and jj + j < width and not (
                    ii + i,
                    jj + j) in visit and (img[i + ii, j + jj, 0] < 60
                                          and img[i + ii, j + jj, 1] < 60
                                          and img[i + ii, j + jj, 2] < 60):
                q.put((ii + i, jj + j))
                visit.add((ii + i, jj + j))
                if len(visit) > np.around(pi * r**2) * 1.5:
                    return False, visit
    return True, visit


def detect_circle(image):
    dst = cv2.GaussianBlur(image, (13, 15), 15)  # 使用高斯模糊，修改卷积核ksize也可以检测出来
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray,
                               cv2.HOUGH_GRADIENT,
                               1,
                               200,
                               param1=50,
                               param2=20,
                               minRadius=50,
                               maxRadius=250)
    # 1,200,50,20,50,250
    # 1,50,50,10,0,30
    height, width = image.shape[:2]
    if circles is not None and len(circles) > 0:
        circles = np.uint16(np.around(circles))  #around对数据四舍五入，为整数
        direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for circle in circles[0, :]:
            x, y, r = circle
            print('circle=' + str(circle))
            if y < 0 or y >= height or x < 0 or x >= width:
                continue
            q = queue.Queue()
            q.put((y, x))
            visit = set([(y, x)])
            while not q.empty():
                i, j = q.get()
                if image[i, j, 0] < 60 and image[i, j, 1] < 60 and image[
                        i, j, 2] < 60:
                    f, v = bfs(image, i, j, direction, r)
                    if f:
                        for k in v:
                            image[k[0], k[1]] = (150, 150, 150)
                    break
                else:
                    for ii, jj in direction:
                        if ii + i >= 0 and ii + i < height and jj + j >= 0 and jj + j < width and not (
                                ii + i, jj + j) in visit and (
                                    ii + i - y)**2 + (jj + j - x)**2 <= r**2:
                            q.put((ii + i, jj + j))
                            visit.add((ii + i, jj + j))
    print('circle detected')
    return image


def detect_circle_demo(image):
    dst = cv2.GaussianBlur(image, (13, 15), 15)  # 使用高斯模糊，修改卷积核ksize也可以检测出来
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray,
                               cv2.HOUGH_GRADIENT,
                               1,
                               200,
                               param1=50,
                               param2=20,
                               minRadius=50,
                               maxRadius=250)
    # 1,200,50,20,50,250
    # 1,50,50,10,0,30
    height, width = image.shape[:2]
    if circles is not None and len(circles) > 0:
        circles = np.uint16(np.around(circles))  #around对数据四舍五入，为整数
        for i in circles[0, :]:
            print('circle=' + str(i))
            cv2.circle(image, (i[0], i[1]), i[2], (0, 0, 255), 2)
            cv2.circle(image, (i[0], i[1]), 2, (255, 0, 0), 2)  #圆心
    print('circle detected')
    return image


if __name__ == '__main__':
    images_path = 'G:/20191209/FRM_0108'
    output_path = 'C:/Users/jf/Desktop/output'
    images_dir = os.listdir(images_path)
    for image in images_dir:
        src = cv2.imread(images_path + '/' + image)
        src_circle = cv2.imread(images_path + '/' + image)
        cv2.imwrite(output_path + '/' + image, detect_circle(src))
        cv2.imwrite(output_path + '/' + image.replace('.JPG', '_circle.JPG'),
                    detect_circle_demo(src_circle))
