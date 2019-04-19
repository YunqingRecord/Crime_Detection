import os


def txt_Merge(filepath, output_path, flag):
    filelist = os.listdir(filepath)
    for file in filelist:
        print('successful read file', str(file))
        ori_file = os.path.join(filepath, file)

        finalfile = open(os.path.join(output_path, str(flag)+'.txt'), 'a')  # 将最终文件打开为追加写模式
        for line in open(ori_file):
            finalfile.writelines(line)  # 将源文件的每一行写入最终文件中
        finalfile.close()

#
# filepath = r'P:\CRIME\data\processed\label1_processed'
# outputpath = r'P:\CRIME\data\processed'
#
# label_Merge(filepath, outputpath, 1)


filepath = r'P:\CRIME\20frame\merged_training_data\label'
outputpath = r'P:\CRIME\20frame\merged_training_data\label'

txt_Merge(filepath, outputpath, 'label')

