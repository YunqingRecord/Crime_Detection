import cv2


def Sliding_cut(input_path, frame_length, output_path):
    '''
    :param path: Firstly we point out the video path
    :return:  the cut video by pointed frames
    '''
    video_capture = cv2.VideoCapture(input_path)  # 从文件读取视频
    i = 1
    j = 1
    m = 1  # 每 n 帧 就移动一次窗口
    # 判断视频是否打开
    if video_capture.isOpened():
        print('Successfully Opened')
    else:
        print('Fail to open !')

    fps = video_capture.get(5)  # 获取原视频的帧率

    size = (int(video_capture.get(3)), int(video_capture.get(4)))  # 获取原视频帧的尺寸大小
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

    videoWriter = cv2.VideoWriter(output_path +str(j)+'.avi', fourcc, fps, size)  # 新视频保存路径和参数

    success_read, frame = video_capture.read()  # 读取第一帧

    while success_read:
        try:
            videoWriter.write(frame)  # 写入视频文件, 这时候写入的视频文件仍然是之前指定好的文件序号的那个视频，也就是j
            # 这里从第一帧开始写
            if m % frame_length == 0:  # 当每写入50帧，相当于每50帧切割为一个新的视频并存放在指定位置
                j = j+1      # 保存的视频的名字序号递增
                i -= 30      # 窗口移动的步长
                video_capture.set(1, i)
                videoWriter = cv2.VideoWriter(output_path + str(j) + '.avi', fourcc, fps, size)  # 新视频保存路径和参数
            success_read, frame = video_capture.read()  # 循环读取下一帧
            m += 1    # 每读一帧，数量+1
            i += 1   # 帧序号+1
            print("The temporary frame number:", str(i))  # 输出当前帧数的序号
        except:
            print("cannot sliding window")
            break

