#准备工作：
#1、将跑不同frame的py文件均放在主文件夹目录下的src文件中，并改名为run_video_output+"frame的数值".py
   #例如：要跑5、10、15、20frame，则需要有四个文件，分别叫“run_video_output5.py、run_video_output10.py、run_video_output15.py、run_video_output20.py”，放在tf-openpose/src里
#2、确保每个动作的每个人下的视频个数都相等，不相等不排除会出错
#3、该文件、src文件夹以及视频主文件夹放在同一层目录中

import os
import shutil

def DataPathDetect(path):
    DataPath = path + '/data'
    if os.path.isdir(DataPath) == True:
        shutil.rmtree(DataPath)
    else:
        pass
#若文件中原有data文件夹，全部删除

def GetInput():
    rawpath = input('please input the path (to the mainfolder):')
    realpath = rawpath.replace('\\', '/')
    Mfolder = realpath.split('/')[-1]
    DataPathDetect(realpath)
    activity = os.listdir(realpath)
    peo=eval(input('input the people numbers:'))
    frames=input('input your frame list (seperated by ","):')
    num=eval(input('input the video numbers:'))
    framelist = frames.split(",")
    framesint=[ int(x) for x in framelist ]
    return activity,peo,framesint,num,realpath,Mfolder
#得到：动作名列表、拍摄人数、每人拍摄视频、路径、主文件夹名、希望处理的帧数

def CreateNewDir(dirs,peo,framesls,path):
    for m in framesls:
        for i in range(len(dirs)):
            for j in range(peo):
                #NewPath = path + '/data/' + dirs[i] + '/' +  str(m) + 'frames/p' + str(j+1) + '/'
                NewPath = path + '/data/' + str(m) + 'frames/' + dirs[i] + '/p' + str(j + 1)
                os.makedirs(NewPath)
#创建新的data文件夹，用来装后续生成的txt文件

def ToDoc(ls,peo,framesls,n,MFolder):
    doc = open('out.txt','w')
    for k in framesls:
        for i in range((len(ls))):
            for m in range(peo):
                for j in range(n):
                    h = str(j)
                    print('python src/run_video_output{4}.py --video ../../../CRIME/{3}/{0}/{2}.avi --output ../../../CRIME/{3}/data/{4}frames/{0}/{2}.txt'.format(ls[i], m+1, h.zfill(2), MFolder,k), file=doc)
    doc.close()
#循环创建全部指令，输出至文件

def ReadDoc():
    result=[]
    with open('out.txt','r') as f:
        for line in f.readlines():
            lines=line.strip('\n')
            result.append(lines)
    return result
#从文件中读入全部指令放入列表

def RunCMD(comm):
    for i in range(len(comm)):
        os.system(comm[i])
#运行生成的所有cmd指令，将文件输出至新生成的data文件夹中

def Gettxts(framelist,activity,peo,vnum,mpath):
    txtlist=[]
    for k in framelist:
        for i in activity:
            for j in range(peo):
                for m in range(vnum):
                    s=str(m)
                    filename=mpath + '/data_' + str(k) + '/' + i + '/' +s  +'.txt'
                    txtlist.append(filename)                       #生成所有实验数据的txt文件路径，并且存进一个列表中；返回列表的同时返回主路径名
    return txtlist

def deleteline(txtlist):
    for i in txtlist:       #对列表中的txt文件逐一进行读取
        readfile = open(i)
        lines = readfile.readlines()      #读入文件的某一行，并存入列表中
        readfile.close()
        w = open(i, 'w')
        w.writelines([item for item in lines[:-1]])       #将删除了最后一行的txt文件写回原文件
        w.close()

action,people,frame,videonum,path,MainFolder=GetInput()
CreateNewDir(action,people,frame,path)
ToDoc(action,people,frame,videonum,MainFolder)
cmd=ReadDoc()
# RunCMD(cmd)
# txtname=Gettxts(frame,action,people,videonum,path)
# deleteline(txtname)