#All the imports go here
import numpy as np
import cv2
import time
import datetime as date
import logging as log
import pandas
import bokeh

#Initializing the face and eye cascade classifiers from xml files
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

#Variable store execution state
first_read = True

#Starting the video capture
cap = cv2.VideoCapture(0)
ret, img = cap.read()
log.basicConfig(filename='app.log', filemode='w',format='%(asctime)s - %(message)s', level=log.INFO)
log.info('Camera Initialized')
first_frame=None

#variable declaration
blinktimes = 0
statuslis = [0]
timeevents = []


while(ret):

    timeelasped = time.time()
    ret,img = cap.read()
    #Coverting the recorded image to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray2=cv2.GaussianBlur(gray,(21,21),0)
    delta_frame=cv2.absdiff(ret,gray)
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)
    #Applying filter to remove impurities
    gray = cv2.bilateralFilter(gray,5,1,1)

    #Detecting the face for region of image to be fed to eye classifier
    faces = face_cascade.detectMultiScale(gray, 1.3, 5,minSize=(200,200))
    if(len(faces)>0):
        timeelasped = time.time()
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

            #roi_face is face which is input to eye classifier
            roi_face = gray[y:y+h,x:x+w]
            roi_face_clr = img[y:y+h,x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_face,1.3,5,minSize=(50,50))

            #Examining the length of eyes object for eyes
            if(len(eyes)>=2):
                #Check if program is running for detection 
                if(first_read):
                    cv2.putText(img, "Eye detected press s to begin", (70,70), cv2.FONT_HERSHEY_PLAIN, 3,(0,255,0),2)
                    log.info("eyes detected " + str(len(eyes)) + " at " + str(date.datetime.now()))
                    status = 2
                    statuslis.append(status)
                    if statuslis[-1] == statuslis[-2]:
                        timeevents.append(date.datetime.now())

                else:
                    cv2.putText(img, "Eyes open!", (70,70), cv2.FONT_HERSHEY_PLAIN, 2,(255,255,255),2)
                    log.info("eyes open " + str(len(eyes)) + " at " + str(date.datetime.now()))
            else:

                if(first_read):
                    timenoeye = time.time()
                    #To ensure if the eyes are present before starting
                    cv2.putText(img, "No eyes detected", (70,70), cv2.FONT_HERSHEY_PLAIN, 3,(0,0,255),2)
                    log.info("unindentified eyes" + " at " + str(date.datetime.now()))
                    status = 1
                    statuslis.append(status)
                else:
                    #This will print on console and restart the algorithm
                    print("Blink detected--------------")
                    cv2.waitKey(3000)
                    first_read=True

    else:
        cv2.putText(img,"No face detected",(100,100),cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0),2)
        status = 0
        statuslis.append(status)

    #Controlling the algorithm with keys
    cv2.imshow('img',img)
    cv2.imshow('img2', delta_frame)
    cv2.imshow('img3', thresh_frame)
    a = cv2.waitKey(1)

    print(status)
    if(a==ord('q')):
        print(blinktimes)
        print(statuslis)
        print(timeevents)
        break
    elif(a==ord('s') and first_read):
        #This will start the detection
        first_read = False

cap.release()
cv2.destroyAllWindows()
