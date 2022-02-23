#!/usr/bin/env python3

import cv2
import depthai as dai
import time

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)

xoutVideo.setStreamName("video")

# Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.RGB)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setVideoSize(1920, 1080)

xoutVideo.input.setBlocking(False)
xoutVideo.input.setQueueSize(1)

# Linking
camRgb.video.link(xoutVideo.input)
count=0
# Connect to device and start pipeline
prev_frame_time = 0
new_frame_time = 0
with dai.Device(pipeline) as device:

    video = device.getOutputQueue(name="video", maxSize=1, blocking=False)

    while True:
        videoIn = video.get()
        new_frame_time = time.time()
        Frame=videoIn.getCvFrame()
        fps = str(4/(new_frame_time-prev_frame_time))
        prev_frame_time = new_frame_time
        #fps = str(int(1/(time.time()-new_frame_time)))
        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(Frame, fps+' '+str(Frame.shape), (7, 70), font, 1, (100, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(Frame, str(fps)+' '+' '+str(Frame.shape) , (7, 70), font, 1, (0, 225, 225), 2, cv2.LINE_AA)
        cv2.imshow("video", Frame)
        if cv2.waitKey(1)==ord('p'):
            count+=1
            cv2.imwrite('image'+str(count)+'.jpg',Frame)
        if cv2.waitKey(1) == ord('q'):
            break
