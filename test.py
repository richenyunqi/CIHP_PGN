import os, cv2
import shutil


def copy_images(input_path, result_path):
    names = os.listdir(input_path)
    count = 0
    for name in names:
        if os.path.isdir(os.path.join(input_path, name)):
            copy_images(os.path.join(input_path, name), result_path)
        else:
            shutil.copyfile(
                os.path.join(input_path, name),
                os.path.join(result_path,
                             os.path.split(input_path)[1] + '-' + name))
            count += 1
        print("进度:{}%".format(round((count) * 100 / len(names))), end="/r")
    print()
    print(len(names))


def copy_combine_images(input_path, result_path, houzhui):
    names = os.listdir(input_path)
    count = 0
    for name in names:
        if os.path.isdir(os.path.join(input_path, name)):
            copy_images(os.path.join(input_path, name), result_path)
        else:
            shutil.copyfile(
                os.path.join(input_path, name),
                os.path.join(result_path,
                             os.path.split(input_path)[1] + '-' + name))
            count += 1
        print("进度:{}%".format(round((count) * 100 / len(names))), end="/r")
    print()
    print(len(names))


if __name__ == '__main__':
    path = 'F:/human/temp_result/result/terrible'
    result_path = 'F:/human/result/original'
    for dir_name in os.listdir(path):
        for image_name in os.listdir(os.path.join(path, dir_name)):
            img = cv2.imread(os.path.join(path, dir_name, image_name))
            if '_combine.png' in image_name:
                height, width = img.shape[:2]
                for i in range(height):
                    for j in range(width):
                        if all(k == 0 for k in img[i, j]):
                            img[i, j] = (255, 255, 255)
                cv2.imwrite(os.path.join(result_path, dir_name, image_name),
                            img)
            else:
                shutil.copyfile(
                    os.path.join(path, dir_name, image_name),
                    os.path.join(result_path, dir_name, image_name))
            print(image_name)
