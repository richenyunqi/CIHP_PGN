import os

input_path = 'G:/20191221_human'
output_path = 'G:/human/CIHP_PGN/datasets'
result_path = 'G:/result/original/1221_human_result'
bat_path = './run.bat'
time_path = './time.txt'
if not os.path.exists(result_path):
    os.mkdir(result_path)
if os.path.exists(bat_path):
    os.remove(bat_path)
f = open(bat_path, 'a')
if os.path.exists(time_path):
    os.remove(time_path)
names = os.listdir(input_path)
for name in names:
    if os.path.isdir(os.path.join(input_path, name)):
        new_input_path = os.path.join(input_path, name)
        new_output_path = os.path.join(output_path, name)
        new_result_path = os.path.join(result_path, name)
        f.write('python main.py %s %s %s\n' %
                (new_input_path, new_output_path, new_result_path))
        print('write python main.py %s %s %s' %
              (new_input_path, new_output_path, new_result_path))
f.write('pause')