import os, shutil
import sys

names = os.listdir('./output/cihp_parsing_maps/')
for n in names:
    if n.find('.png') != -1 and n.find('_vis') != -1:
        shutil.copy('./output/cihp_parsing_maps/' + n, './copy')