import IPython
import pandas as pd
import keras
import itertools
import argparse
import logging
import time
import os
import common
import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout, TimeDistributed, Activation
from keras.layers import LSTM
from sklearn.model_selection import train_test_split

from keras.models import model_from_json
from keras.models import load_model

from estimator import TfPoseEstimator
from networks import get_graph_path, model_wh
cnt = 0
logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
storage = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
fps_time = 0
record = []

X_vector_dim = 18
y_vector_dim = 2
input_shape =(30, 18)
# timesteps = 10
batch_size = 32
_dropout = 0.1
_activation = 'relu'
_optimizer = 'Adam'
model_weights_path = r"P:\CRIME\LearnDec\1\pose_model.h5"  # PATH  #


def cal_dis(coor1, coor2):   # calculate the Euclidean distance of two coordinates
    global out
    if coor1 != (0, 0) and coor2 != (0, 0):
        out = np.square(coor1.x-coor2.x)+np.square(coor1.y-coor2.y)
    elif coor1 != (0, 0) and coor2 == (0, 0):
        out = np.square(coor1.x)+np.square(coor1.y)
    elif coor2 != (0, 0) and coor1 == (0, 0):
        out = np.square(coor2.x)+np.square(coor2.y)
    elif coor1 != (0, 0) and coor2 == (0, 0):
        out = 0
    return np.sqrt(out)


model = Sequential()
model.add(TimeDistributed(Dense(X_vector_dim, activation=_activation), input_shape=input_shape))

model.add(TimeDistributed(Dense(X_vector_dim * 2, activation=_activation)))  # (5, 80)

model.add(TimeDistributed(Dense(X_vector_dim * 2, activation=_activation)))  # (5, 80)

model.add(TimeDistributed(Dense(X_vector_dim, activation=_activation)))  # (5, 40)

model.add(TimeDistributed(Dense(int(X_vector_dim / 2), activation=_activation)))  # (5, 20)

model.add(TimeDistributed(Dense(int(X_vector_dim / 4), activation=_activation)))  # (5, 10)

model.add(LSTM(int(X_vector_dim / 4), dropout=_dropout, recurrent_dropout=_dropout))
model.add(Dense(y_vector_dim, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer=_optimizer, metrics=['accuracy'])
model.summary()

model.load_weights(model_weights_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--video', type=str, default='16.mp4')
    parser.add_argument('--camera', type=int, default=0)
    parser.add_argument('--model', type=str, default='mobilenet_thin_432x368', help='cmu_640x480 / cmu_640x360 / mobilenet_thin_432x368')
    parser.add_argument('--show-process', type=bool, default=False,
                        help='for debug purpose, if enabled, speed for inference is dropped.')
    args = parser.parse_args()
    logger.debug('initialization %s : %s' % (args.model, get_graph_path(args.model)))
    w, h = model_wh(args.model)
    e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    logger.debug('cam read+')
    cam = cv2.VideoCapture(args.video)
    ret_val, image = cam.read()
    logger.info('cam image=%dx%d' % (image.shape[1], image.shape[0]))

    while True:
        try:
            ret_val, image = cam.read()

            humans = e.inference(image)

            #logger.debug('postprocess+')
            image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

            cv2.putText(image,
                        "FPS: %f" % (1.0 / (time.time() - fps_time)),
                        (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)
            cv2.imshow('tf-pose-estimation result', image)
            fps_time = time.time()
            if cv2.waitKey(1) == 27:
                break

            if len(humans) >= 2:  # 能检测到两个人的情况（包含很多子情况）
                for i in range(common.CocoPart.Background.value):

                    if i in humans[0].body_parts.keys() and i in humans[1].body_parts.keys():
                        record.append(cal_dis(humans[0].body_parts[i], humans[1].body_parts[i]))
                        storage[i] = cal_dis(humans[0].body_parts[i], humans[1].body_parts[i])
                        cnt = cnt + 1

                    else:
                        record.append(storage[i])
                        cnt = cnt + 1

                    if cnt % 540 is 0:
                        X = np.array(record)
                        test_sample = X
                        # print("test_sample shape:", test_sample.shape)
                        test_sample_y_hat = model.predict(test_sample.reshape(1, 30, 18))
                        # print(test_sample_y_hat)

                        record = []
                        if test_sample_y_hat[0][1] > 0.5:
                            print("Violence Dectected !!")

                        if test_sample_y_hat[0][0] >= 0.5:
                            print("No Warning")
                        test_sample_y_hat = []

            else:
                for i in range(common.CocoPart.Background.value):  # 只有0/1个人时，直接append 0 进去
                    record.append(0)
                    storage[i] = 0
                    cnt = cnt + 1

                if cnt % 540 is 0:
                    X = np.array(record)
                    test_sample = X
                    # print("test_sample shape:", test_sample.shape)
                    test_sample_y_hat = model.predict(test_sample.reshape(1, 30, 18))
                    # print(test_sample_y_hat)
                    record = []
                    if test_sample_y_hat[0][1] > 0.5:
                        print("Violence Dectected")

                    if test_sample_y_hat[0][0] >= 0.5:
                        print("No Warning")
                    test_sample_y_hat = []
        except AttributeError:
            print("No more frames")
            break

    cv2.destroyAllWindows()
