#!/usr/bin/env python
from cv2 import VideoCapture, imencode, imwrite
import pika
import base64
import time

cam_port = 0
cam = VideoCapture(cam_port) 

count = 0

max_count = 50

while count < max_count:

    print("about to take a picture")
    time.sleep(2)
    result, image = cam.read() 

    if result: 
        imwrite("GeeksForGeeks.png", image)
    
    jpg_img = imencode('.jpg', image)
    b64_string = base64.b64encode(jpg_img[1]).decode('utf-8')

    connection = pika.BlockingConnection(pika.ConnectionParameters('10.42.42.123'))
    channel = connection.channel()

    channel.queue_declare(queue='images', durable=True)

    f = open("image.base64", "r")
    lines = f.readlines()

    #print(lines[0])

    channel.basic_publish(exchange='',
                        routing_key='images',
                        body=b64_string)
    print(" [x] Sent 'Image!'")

    connection.close()
    count+=1