#!/usr/bin/env python

import pyaudio
import wave
import numpy as np
from datetime import datetime

import fcntl
import termios, sys, os
import time, sys
import sys

import time

import rospy
from std_msgs.msg import Float32 

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

threshold = 0.01

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = chunk
)

cnt     = 0
MAX_VOL = 10000
start   = False
check   = True
def getVolume():
    data = stream.read(chunk)
    x = np.frombuffer(data, dtype="int16") 

    return x.max()
def pubVolume():
    pub = rospy.Publisher('volume', Float32, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    r = rospy.Rate(100) # 10hz
    counter=0
    sumVol=0
    while not rospy.is_shutdown():
        
        volume = getVolume()
        sumVol =sumVol+abs(volume)
        counter = counter+1
        if counter%3==0:
            pub.publish(sumVol/3)
            print(sumVol/3)
            sumVol=0
            r.sleep()

if __name__ == '__main__':
    try:
        pubVolume()
    except rospy.ROSInterruptException:
        stream.close()
        p.terminate()

                
    

