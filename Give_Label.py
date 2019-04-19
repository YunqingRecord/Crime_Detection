'''
Goal: give label to samples

Methods: every txt file have m*30*18 datas.
So firstly, we should:
1. find the m, can be acquired by dividing the number of data with 30
2. For each file, we can give m labels, depending on which class it belongs to
'''
import os
import re


def Findm(ActFile):
    '''
    :param ActFile: the file to be given label
    :return:  the number of samples in this file
    '''
    num = 0
    with open(ActFile, 'r') as f:
        for line in f.readlines():
            num += 1
        m = num//20    # divide by frames you want
    return m


def Write_Label(Filepath, output_path, flag):
    '''
    :param Filename:  The considered label file
    :param m: number of samples in this file
    :return: write the label to the new file, named by the corresponding index
    '''
    file_list = os.listdir(Filepath)
    for file in file_list:
        m = Findm(os.path.join(Filepath, file))
        n = re.findall("\d+", file)[0]
        label_file_temp = open(os.path.join(output_path, str(n)+'.txt').replace('\\', '/'), 'w')
        for i in range(m):
            label_file_temp.writelines(str(int(flag)))
            label_file_temp.writelines('\n')
        print('Successfully write:', str(n)+' file label')
        label_file_temp.close()


Write_Label(Filepath=r'P:\CRIME\20frame\output_coor\NW', output_path=r'P:\CRIME\20frame\output_coor', flag=0)

