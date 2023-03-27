import cv2 as cv
from multiprocessing import Queue
import torch
from MyNetwork import MyNetwork
import time
from torchvision.transforms import *
import pyttsx3
import threading

#cap = cv.VideoCapture(0)
def videoCap(q) -> None:
    """
    主要模块，输入的q是Queue，
    若有人出现在摄像机前，该模块会往q中放入True，
    若人从摄像机前消失，该模块会往q中放入False。
    """
    # 加载摄像机
    cap = cv.VideoCapture(0)

    # 初始化参数
    state = False
    record = []
    point = 0
    leng = 10
    for i in range(leng):
        record.append(False)

    # 初始化神经网络
    myNetwork = MyNetwork()

    # 加载神经网络模型
    myNetwork.load_state_dict(torch.load('.\\test.pth', map_location=torch.device('cpu')))

    # 初始化图像变换
    trans = Compose([
        ToTensor(),
        Resize([64, 64])
    ])
    while True:
        # 从摄像头中读取视频帧
        ret, frame = cap.read()
        if not ret:
            print("Can not find your camera.")
            break
        # 对读取的帧进行变换
        img = trans(frame)
        img = torch.unsqueeze(img, dim=0)

        # 输入到神经网络中并获得结果
        res = myNetwork(img)
        predict, index = torch.max(res, 1)
        record[point] = index[0].item()
        #record[point] = index[0]
        point = (point+1) % 10

        cv.imshow('frame', frame)
        # 判断是否有人出现
        if judge(record, point) == 1 and not state:
            state = True
            q.put("True")
            print("True")
            thead_frame = threading.Thread(target=say_hello, args=())
            thead_frame.start()
            #say_hello()
        if judge(record, point) == -1 and state:
            state = False
            q.put("False")
            print("False")
        #print(judge(record, point))
        #print(q.empty())
        # 等待100ms，如果按下q键则跳出循环
        if cv.waitKey(100) & 0xff == ord('q'):
            break


def say_hello():
    engine = pyttsx3.init()
    engine.say('您好，有什么可以帮到您的？')
    engine.runAndWait()
    # 朗读一次
    #engine.endLoop()
    engine.stop()


def judge(record, point) -> int:
    """
    如果前六次记录中网络输出5次有人，则认为有人
    如果前六次记录中网络输出5次没人，则认为没人
    """
    tar=6
    tot = 0
    for i in range(tar):
        tot += record[(point-i+len(record)) % len(record)]
    if (tot >= 5):
        return -1
    if (tot <= 1):
        return 1
    return 0


def cap_start():
    q = Queue()
    videoCap(q)

#cap_start()