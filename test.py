import os
import cv2


def create_combine_image(original_image_path, combine_image_path,
                         result_image_path):
    img1 = cv2.imread(original_image_path)
    img2 = cv2.imread(combine_image_path)
    for i in range(img1.shape[0]):
        for j in range(img1.shape[1]):
            (b, g, r) = img2[i, j]
            if b != 0 or g != 0 or r != 0:
                img1[i, j] = (255, 255, 255)
    cv2.imwrite(result_image_path, img1)
    print('create', result_image_path)


def create_dir_combine_image(original_dir_path, combine_dir_path,
                             result_dir_path):
    print(original_dir_path, combine_dir_path, result_dir_path)
    os.mkdir(result_dir_path)
    names = os.listdir(original_dir_path)
    for n in names:
        original_image_path = os.path.join(original_dir_path, n)
        combine_image_path = os.path.join(combine_dir_path, n)
        result_image_path = os.path.join(result_dir_path, n)
        create_combine_image(original_image_path, combine_image_path,
                             result_image_path)


def create_dir_parsing_image(dir_path):
    names = os.listdir(dir_path)
    for n in names:
        print(n)
        if 'PARSING' in n:
            parsing_img = cv2.imread(os.path.join(dir_path, n))
            orginal_img = cv2.imread(
                os.path.join(dir_path, n.replace('PARSING', 'adata')))
            for i in range(parsing_img.shape[0]):
                for j in range(parsing_img.shape[1]):
                    (b, g, r) = parsing_img[i, j]
                    (bo, go, ro) = orginal_img[i, j]
                    if int(g) - int(r) >= 150 and int(g) - int(b) >= 150 and (
                            ro > 70 and go > 40 and bo > 20
                            and int(ro) - int(go) >= 10
                            and int(go) - int(bo) >= 5):
                        parsing_img[i, j] = (128, 0, 128)  #皮肤颜色
            cv2.imwrite(os.path.join(dir_path, n), parsing_img)
            print('create ', os.path.join(dir_path, n))


def fill_up_image(dir_path):
    names = os.listdir(dir_path)
    for n in names:
        print(n)
        if 'PARSING' in n:
            parsing_img = cv2.imread(os.path.join(dir_path, n))
            mask_img = cv2.imread(
                os.path.join(dir_path, n.replace('PARSING', 'MASK')))
            orginal_img = cv2.imread(
                os.path.join(dir_path, n.replace('PARSING', 'adata')))
            height, width = mask_img.shape[:2]
            new_height = 400
            new_width = int(new_height * width / height)
            if height > width:
                new_width = 400
                new_height = int(new_width * height / width)
            parsing_img = cv2.resize(parsing_img, (new_width, new_height))
            mask_img = cv2.resize(mask_img, (new_width, new_height))
            orginal_img = cv2.resize(orginal_img, (new_width, new_height))
            for i in range(mask_img.shape[0]):
                for j in range(mask_img.shape[1]):
                    (bm, gm, rm) = mask_img[i, j]
                    # (bp, gp, rp) = parsing_img[i, j]
                    (bo, go, ro) = orginal_img[i, j]
                    if (rm == bm and rm == gm
                            and rm < 20) and (ro > 70 and go > 40 and bo > 20
                                              and int(ro) - int(go) >= 10
                                              and int(go) - int(bo) >= 5):
                        # if (rm, gm, bm) == (0, 0,
                        #                     0) and (ro > 70 and go > 40 and bo > 20
                        #                             and int(ro) - int(go) >= 10
                        #                             and int(go) - int(bo) >= 5):
                        parsing_img[i, j] = (128, 0, 128)  #皮肤颜色
                        mask_img[i, j] = (255, 255, 255)
            parsing_img = cv2.resize(parsing_img, (width, height))
            mask_img = cv2.resize(mask_img, (width, height))
            cv2.imwrite(os.path.join(dir_path, n), parsing_img)
            cv2.imwrite(os.path.join(dir_path, n.replace('PARSING', 'MASK1')),
                        mask_img)
            print('create ', os.path.join(dir_path, n))
            print('create ',
                  os.path.join(dir_path, n.replace('PARSING', 'MASK')))


if __name__ == '__main__':
    # path = 'H:'
    # for n in os.listdir(path):
    #     create_dir_combine_image(path + '/' + os.path.join(n, n),
    #                              path + '/' + os.path.join(n, n + '_COMBINE'),
    #                              path + '/' + os.path.join(n, n + '_COMBINE2'))
    # create_dir_parsing_image('F:\\human\\result\\co')
    fill_up_image('C:\\Users\\jf\\Desktop\\test1')
