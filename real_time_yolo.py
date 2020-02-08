import cv2
import numpy as np
import time
import win32com.client
import serial

        # Loading Yolov3 weights and its label

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

        # Loadind coco names in list 
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

        # extracting output layer
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        # Loading Webcam
cap = cv2.VideoCapture(0)

        # Communicating with arduino using serial port
ser1=serial.Serial('COM7',9600)

        # Decoading arduino signal 

button_sig = ser1.readline()
decode_signal = button_sig.decode()
button_output= int(decode_signal.rstrip())

        # This Loop will run while the button is pressed
while button_output==0:

        # Here we again check the button signal
    button_sig = ser1.readline()
    decode_signal = button_sig.decode()
    button_output= int(decode_signal.rstrip())

        # The camera input is being feed into frame 
    _, frame = cap.read()

        # camera feed is send to a dense neural network at 380,380 size
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (380, 380), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    
    class_ids = []
    confidences = []
    objects_count = 0

        # cheaking all the confidence lable in 91 objects
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
                    #filtering  object according to confidence label 
            if confidence > 0.6:
                
                class_ids.append(class_id)

                    #counter for objects
                objects_count=objects_count+1
    label=""
    objectlab=[]
    objectone=[]
    for i in range(objects_count):
        label = str(classes[class_ids[i]])
        objectlab.append(label)

        # counting for each objects eg: 4person 3cup 
    abab= list(dict.fromkeys(objectlab))
    for j in range(len(abab)):
        item_count=objectlab.count(abab[j])
        tempnam=str(item_count)+str(abab[j])
        objectone.append(tempnam)
        
            
            #To feed the dected object to user in the form of voice
    speaker = win32com.client.Dispatch('SAPI.SpVoice')
    speaker.Rate = 2
    speaker.Speak(objectone)
            
    
    
            # escape key is used to terminate the program
    key = cv2.waitKey(1)
    if key == 27:
        break

        # closeing the program window 
cap.release()
cv2.destroyAllWindows()
