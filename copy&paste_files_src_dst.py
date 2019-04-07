import os
import shutil


def objFileName(new_filw_length):
    obj_name_list = []
    for i in range(1, new_filw_length+1):
        obj_name_list.append(str(i)+'.avi')
    return obj_name_list  # [1.avi, 2.avi, ..., 4000.avi]


if __name__ == '__main__':

    name_list = objFileName(new_filw_length=4000)
    new_path = r"P:\CRIME\output"    # 指定了保存的新目录
    main_path = 'P:\CRIME\output1'   # 旧目录地址
    second = os.listdir(main_path)   # 二级目录  outpu\01
    i = 1
    while i <= 4000:
        for path in second:
            avi_name = os.listdir(os.path.join(main_path, path))  # 二级目录下的video名字
            for avi in avi_name:                                  # 遍历视频名字
                obj = os.path.join(main_path, path, avi)          # 得到视频的绝对路径
                shutil.copy(obj, os.path.join(new_path, str(i)+'.avi'))   # （绝对路径，新路径）
                print('successfully copy', str(i)+'.avi')
                i += 1

