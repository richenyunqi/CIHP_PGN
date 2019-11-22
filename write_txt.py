import os, shutil
import sys

def write_image_list(images_path):
    image_names = os.listdir(images_path)
    image_list_path = os.path.dirname(images_path) + '/list/img_list.txt'
    image_list_file = open(image_list_path, 'w')
    for image_name in image_names:
        name, ext = os.path.splitext(image_name)
        image_path = name
        image_list_file.write(image_path + '\n')
    image_list_file.close()

def write_train(images_path):
    image_names = os.listdir(images_path)
    train_path = os.path.dirname(images_path) + '/list/train.txt'
    train_file = open(train_path, 'w')
    for image_name in image_names:
        image_path = '/images/' + image_name
        label_path = '/labels/' + image_name
        train_file.write(image_path + ' ' + label_path + '\n')
    train_file.close()

def write_train_id(images_path):
    image_names = os.listdir(images_path)
    train_id_path = os.path.dirname(images_path) + '/list/train_id.txt'
    train_id_file = open(train_id_path, 'w')
    for image_name in image_names:
        name, ext = os.path.splitext(image_name)
        train_id_file.writelines(name + '\n')
    train_id_file.close()

def write_train_rev(images_path):
    image_names = os.listdir(images_path)
    train_rev_path = os.path.dirname(images_path) + '/list/train_rev.txt'
    train_rev_file = open(train_rev_path, 'w')
    for image_name in image_names:
        image_path = '/images/' + image_name
        label_path = '/labels/' + image_name
        label_rev_path = '/labels_rev/' + image_name
        train_rev_file.write(image_path + ' ' + label_path + ' ' + label_rev_path + '\n')
    train_rev_file.close()

def write_val(images_path):
    image_names = os.listdir(images_path)
    val_path = os.path.dirname(images_path) + '/list/val.txt'
    val_file = open(val_path, 'w')
    for image_name in image_names:
        image_path = '/images/' + image_name
        label_path = '/labels/' + image_name
        val_file.write(image_path + ' ' + label_path + '\n')
    val_file.close()

def write_val_id( images_path):
    image_names = os.listdir(images_path)
    val_id_path = os.path.dirname(images_path) + '/list/val_id.txt'
    val_id_file = open(val_id_path, 'w')
    for image_name in image_names:
        name, ext = os.path.splitext(image_name)
        val_id_file.writelines(name + '\n')
    val_id_file.close()
