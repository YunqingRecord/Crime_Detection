import os


def GetVNum(strls):
    num = []
    for i in strls:
        num.append(int(i[:-4]))
    return max(num)+1


def GetInfoFromls(AVIS):
    global video
    videostr = []
    for i in AVIS:
        i = i.replace('\\', '/')
        videostr.append(i.split('/')[-1])
        video = GetVNum(videostr)
    return video


def GetInfoFromPath(file_dir):
    global video
    AVIS = []
    for dirpath, dirnames, filenames in os.walk(file_dir, topdown=False):
        for filename in filenames:  # 遍历所有有文件的文件夹
            # 输出文件所在文件夹路径
            if filename[-4:] == '.avi':
                AVIS.append(dirpath+'/'+filename)
    video = GetInfoFromls(AVIS)
    return video


def GetInput():
    rawpath = input('please input the path (to the mainfolder):')
    realpath = rawpath.replace('\\', '/')
    Mfolder = realpath.split('/')[-1]   # 找到 output  = format {3}
    vnum = GetInfoFromPath(realpath)
    frames = input('input your frame list (seperated by ","):')
    pts = input('input the process points:')
    md = eval(input('input the model sequence:  1-cmu_640x360,2-cmu_640x480, 3-mobilenet_thin_432x368 '))
    if md == 1:
        modelname = 'cmu_640x360'
    elif md == 2:
        modelname = 'cmu_640x480'
    else:
        modelname = 'mobilenet_thin_432x368'
    framelist = frames.split(",")
    framesint = [int(x) for x in framelist]
    return framesint, vnum, realpath, Mfolder, pts, modelname


def CreateNewDir(framesls, path, pt, modelname):  # 创建新的data文件夹，用来装后续生成的txt文件
    for m in framesls:
        try:
            NewPath = path + '/' + str(pt) + 'points/' + modelname + '/data_' + str(m) + '/'
            os.makedirs(NewPath)
        except FileExistsError:
            pass


def ToDoc(framesls, vnum, MFolder, pt, modelname):
    doc = open('out.txt', 'w')
    for frame in framesls:
        for video_index in range(vnum):
            index = str(video_index)
            print('python src/{3}points/run_video_output{2}.py --video ../../../CRIME/{1}/{0}.avi --output ../../../CRIME/output_coor/{0}.txt  --model {4}'.format(index, MFolder, frame, pt, modelname), file=doc)
# {0}=index, {1}=MFolder,{2}=frame,{3}=pt,{4}=modelname
    doc.close()
# 循环创建全部指令，输出至文件


def ReadDoc():  # 从文件中读入全部指令放入列表
    result = []
    with open('out.txt', 'r') as f:
        for line in f.readlines():
            lines = line.strip('\n')
            result.append(lines)
    return result


def RunCMD(comm):  # 运行生成的所有cmd指令，将文件输出至新生成的data文件夹中
    m = 0
    for i in range(len(comm)):
        os.system(comm[i])
        m += 1
        if m % 10 == 0:
            print("按任意键继续")
            os.system("pause")


def Gettxts(framelist, activity, peo, vnum, mpath):
    txtlist = []
    for k in framelist:
        for i in activity:
            for j in range(peo):
                for m in range(vnum):
                    s = str(m)
                    filename = mpath + '/data_' + str(k) + '/' + i + '/'+s.zfill(2)+'.txt'
                    txtlist.append(filename)                       # 生成所有txt文件路径，并且存进一个列表中；返回列表的同时返回主路径名
    return txtlist


def deleteline(txtlist):
    for i in txtlist:       # 对列表中的txt文件逐一进行读取
        readfile = open(i)
        lines = readfile.readlines()      # 读入文件的某一行，并存入列表中
        readfile.close()
        w = open(i, 'w')
        w.writelines([item for item in lines[:-1]])       # 将删除了最后一行的txt文件写回原文件
        w.close()


frame, videonum, path, MainFolder, points, model = GetInput()

CreateNewDir(frame, path, points, model)

ToDoc(frame, videonum, MainFolder, points, model)

cmd = ReadDoc()
RunCMD(cmd)

# txtname=Gettxts(frame,action,people,videonum,path)
# deleteline(txtname)
