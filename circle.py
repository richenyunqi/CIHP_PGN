import os
import cv2
import numpy as np
import queue


def dfs(img, x, y, direction):
    img[x, y] = (255, 255, 255)
    q = queue.Queue()
    q.put((x, y))
    height, width = img.shape[:2]
    while not q.empty():
        i, j = q.get()
        for ii, jj in direction:
            if ii + i >= 0 and ii + i < height and jj + j >= 0 and jj + j < width and (
                    img[i + ii, j + jj, 0] < 30 and img[i + ii, j + jj, 1] < 30
                    and img[i + ii, j + jj, 2] < 30):
                q.put((ii + i, jj + j))
                img[ii + i, jj + j] = (255, 255, 255)


def detect_circle(image):
    dst = cv2.GaussianBlur(image, (13, 15), 15)  # 使用高斯模糊，修改卷积核ksize也可以检测出来
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray,
                               cv2.HOUGH_GRADIENT,
                               1,
                               20,
                               param1=50,
                               param2=30,
                               minRadius=50,
                               maxRadius=250)
    height, width = image.shape[:2]
    if circles is not None and len(circles) > 0:
        circles = np.uint16(np.floor(circles))  # around对数据四舍五入，为整数
        direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for circle in circles[0, :]:
            x, y, r = circle
            q = queue.Queue()
            q.put((y, x))
            while not q.empty():
                i, j = q.get()
                if image[i, j, 0] < 30 and image[i, j, 1] < 30 and image[
                        i, j, 2] < 30:
                    dfs(image, i, j, direction)
                    break
                else:
                    for ii, jj in direction:
                        if ii + i >= 0 and ii + i < height and jj + j >= 0 and jj + j < width and (
                                ii + i)**2 + (jj + j)**2 <= r**2:
                            q.put((ii + i, jj + j))
    print('circle detected')
    return image


def detect_circle_demo(image, image_path, image_name):
    dst = cv2.GaussianBlur(image, (13, 15), 15)  # 使用高斯模糊，修改卷积核ksize也可以检测出来
    gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray,
                               cv2.HOUGH_GRADIENT,
                               1,
                               20,
                               param1=50,
                               param2=30,
                               minRadius=50,
                               maxRadius=250)
    height, width = image.shape[:2]
    if circles is not None and len(circles) > 0:
        circles = np.uint16(np.around(circles))  # around对数据四舍五入，为整数
        direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for circle in circles[0, :]:
            x, y, r = circle
            if y < 0 or y >= height or x < 0 or x >= width:
                continue
            q = queue.Queue()
            q.put((y, x))
            while not q.empty():
                i, j = q.get()
                if image[i, j, 0] < 30 and image[i, j, 1] < 30 and image[
                        i, j, 2] < 30:
                    dfs(image, i, j, direction)
                    break
                else:
                    for ii, jj in direction:
                        if ii + i >= 0 and ii + i < height and jj + j >= 0 and jj + j < width and (
                                ii + i)**2 + (jj + j)**2 <= r**2:
                            q.put((ii + i, jj + j))
    cv2.imwrite(image_path + '/' + image_name.replace('.JPG', '.png'), image)
    print('circle ' + image_path + '/' + image_name.replace('.JPG', '.png'))
    return image


if __name__ == '__main__':
    images_path = 'G:/black/original'
    images_dir = os.listdir(images_path)
    for image in images_dir:
        src = cv2.imread(images_path + '/' + image)
        detect_circle_demo(src, 'G:/black/r', image)
