import tensorflow as tf
import sys
import os
import picamera
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
#for motor wheels
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
#for go forward
def forward():
    GPIO.output(7, False)
    GPIO.output(11,True)
    GPIO.output(13,True)
    GPIO.output(15,False)
#for robotic arm up down
GPIO.setup(35,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)
def down(tf):
    GPIO.output(35, False)
    GPIO.output(36,True)
    time.sleep(tf)
    GPIO.cleanup()
def up(tf):
    GPIO.output(35, True)
    GPIO.output(36,False)
    time.sleep(tf)
    GPIO.cleanup()

#for robotic arm open close
GPIO.setup(37,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)
def opn(tf):
    GPIO.output(37, False)
    GPIO.output(38,True)
    time.sleep(tf)
    GPIO.cleanup()
def close(tf):
    GPIO.output(37, True)
    GPIO.output(38,False)
    time.sleep(tf)
    GPIO.cleanup()
#for ultrasonic sensor
GPIO.setup(12,GPIO.OUT)
GPIO.setup(16,GPIO.IN)

GPIO.output(12.False)
while GPIO.input(16) == 0:
    nosig = time.time()
while gpio.input(16) == 1:
    sig = time.time()
t1 = sig - nosig
distance = t1 / 0.000058

# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

#to capture the image infront of the bot
camera = picamera.PiCamera()
camera.capture(‘new.jpg’)

image_path = "testing.jpg"

if image_path:

    # Read the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                       in tf.gfile.GFile("tf_files/retrained_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("tf_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            score = predictions[0][node_id]
            if score > 0.80:
                while(distance<2 or distance > 4):
                    forward()

                GPIO.cleanup()
                down(1)
                time.sleep(1)
                opn(3)
                time.sleep(1)
                forward(1)
                time.sleep(1)
                close(3)
                time.sleep(1)
                up(1)
                GPIO.cleanup()
