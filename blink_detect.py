# All the imports go here
import numpy as np
import cv2
import time
import datetime as date
import logging as log
import pandas
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import socket
import getpass
from flask import Flask

#getting the username
username = getpass.getuser()

#gets the IP address of the client
ipaddr = socket.gethostbyname(socket.gethostname())


# Fetch the service account key JSON file contents
cred = credentials.Certificate('firebaseacc.json')
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://projdatabase-c4059-default-rtdb.europe-west1.firebasedatabase.app/'
})
ref = db.reference('/')

# Initializing the face and eye cascade classifiers from xml files
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

# Variable store execution state
first_read = True

# Starting the video capture
cap = cv2.VideoCapture(0)
ret, img = cap.read()
log.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s', level=log.INFO)
log.info('Camera Initialized')
first_frame = None

# variable declaration
masterState = []
blinktimes = 0
statuslis = []
timeevents = []
nface = []
neyes = []
afrm = []
nfacetot = []
neyestot = []
afrmtot = []
df = pandas.DataFrame(columns=['Nface', 'Neyes', 'Affrm'])
df2 = pandas.DataFrame(columns=[])
df3 = pandas.DataFrame(columns=[])
df5 = pandas.DataFrame(columns=[])
df6 = pandas.DataFrame(columns=[])
df4 = pandas.DataFrame(columns=[])
eventdt = []
facecoords = []
eyecoords1 = []
eyecoords2 = []
timeevents.append([0, date.datetime.now()])
timeevents.append([1,timeevents[0][1],' '])
timeevents.append([2,timeevents[0][1],' ',' '])


sessionStart = date.datetime.now()

while ret:

    ret, img = cap.read()
    # Converting the recorded image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray, (21, 21), 0)

    gray = cv2.bilateralFilter(gray, 5, 1, 1)

    # Detecting the face for region of image to be fed to eye classifier
    faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(200, 200))
    eyes1 = eye_cascade.detectMultiScale(gray, 1.3, 5, minSize=(50, 50))
    if (len(faces) > 0):
        timeelasped = time.time()
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            crop_img = img[y:y + h, x:x + w]
            cv2.imshow('cropped window',crop_img)
            # roi_face is face which is input to eye classifier
            roi_face = gray[y:y + h, x:x + w]
            roi_face_clr = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_face, 1.3, 5, minSize=(50, 50))
            z = x + w
            t = y + h
            outdingtext = 'x,y,z,t= ' + str([x,y,z,t])
            cv2.putText(img,outdingtext, (x,y-20),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),2)
            facecoords = [x,y,z,t]

        for (x1, y1, w1, h1) in eyes1:
            img = cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
            z1 = x1 + w1
            t1 = y1 + h1
            outdingtext2 = 'x1,y1,z1,t1= ' + str([x1, y1, z1, t1])
            cv2.putText(img, outdingtext2, (x1, y1 - 20), cv2.FONT_HERSHEY_PLAIN,.5 , (0, 255, 0), 2)
            eyecoords1 = [x1, y1, z1, t1]
            # Examining the length of eyes object for eyes

            if (len(eyes) >= 2):
                # Check if program is running for detection
                if (first_read):
                    cv2.putText(img, "Eye detected", (70, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)
                    log.info("eyes detected " + str(len(eyes)) + " at " + str(date.datetime.now()))
                    status = 2
                    statuslis.append(status)
                    timeevents.append([2, date.datetime.now(), facecoords, eyecoords1, crop_img])
                    #if statuslis[-1] != statuslis[-2]:
                    #    timeevents.append([2, date.datetime.now(), facecoords, eyecoords1, crop_img])
                    #    cv2.imwrite(str(timeevents[-1]),crop_img)
                    #else:
                    #    timeevents.append([2, date.datetime.now(), facecoords, eyecoords1])

            else:

                if (first_read):
                    # To ensure if the eyes are present before starting
                    cv2.putText(img, "No eyes detected", (70, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 139), 2)
                    log.info("unindentified eyes" + " at " + str(date.datetime.now()))
                    status = 1
                    statuslis.append(status)
                    timeevents.append([1, date.datetime.now(), facecoords, '', crop_img])

    else:
        cv2.putText(img, "No face detected", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
        status = 0
        statuslis.append(status)
        timeevents.append([0, date.datetime.now()])

    # Controlling the algorithm with keys
    cv2.imshow('img', img)
    a = cv2.waitKey(1)

    if (a == ord('q')):
        print(blinktimes)
        if status != 0:
            timeevents.append([0, date.datetime.now()])
        timeevents.append([1, timeevents[-1][1], ' '])
        timeevents.append([2, timeevents[-1][1], ' ', ' '])
        timeend = date.datetime.now()
        cap.release()
        cv2.destroyAllWindows()
        break
    elif (a == ord('s') and first_read):
        # This will start the detection
        first_read = False

timeevents.append([6, 'nani'])

#State classification and prepping for the graph
for i in range(0, len(timeevents)):
    # df=df.append({"Start":str(timeevents[i][0]),"End":timeevents[i]},ignore_index=True)
    if timeevents[i][0] == 0:
        df = df.append({"Nface": str(timeevents[i])}, ignore_index=True)
    elif timeevents[i][0] == 1:
        df = df.append({"Neyes": str(timeevents[i])}, ignore_index=True)
    elif timeevents[i][0] == 2:
        df = df.append({"Affrm": str(timeevents[i])}, ignore_index=True)

df.to_csv("Times.csv")

if timeevents[0][0] == 0: nface.append(timeevents[0])
elif timeevents[0][0] == 1: neyes.append(timeevents[0])
else : afrm.append(timeevents[0])

for i in range(len(timeevents)-1):
    if timeevents[i][0] != timeevents[i+1][0]:
        if timeevents[i][0] == 0:
            nface.append(timeevents[i])
        elif timeevents[i][0] == 1:
            neyes.append(timeevents[i])
        elif timeevents[i][0] == 2:
            afrm.append(timeevents[i])
        if timeevents[i+1][0] == 0:
            nface.append(timeevents[i+1])
        elif timeevents[i+1][0] == 1:
            neyes.append(timeevents[i+1])
        elif timeevents[i+1][0] == 2:
            afrm.append(timeevents[i+1])

for i in range(len(nface)):
    df2 = df2.append({"Nface": nface[i][1]}, ignore_index=True)
for i in range(len(neyes)):
    df2 = df2.append({"Neyes": neyes[i][1]}, ignore_index=True)
for i in range(len(afrm)):
    df2 = df2.append({"Affirm": afrm[i][1]}, ignore_index=True)

df2.to_csv("StrEnd.csv")

for i in range(0,len(nface),2):
    df3=df3.append({"Start":nface[i][1],"End":nface[i+1][1]},ignore_index=True)

for i in range(0,len(neyes),2):
    df5=df5.append({"Start":neyes[i][1],"End":neyes[i+1][1],'Face Pos Str':str(neyes[i][2]),'Face Pos End':str(neyes[i+1][2])},ignore_index=True)

for i in range(0,len(afrm),2):
    df6=df6.append({"Start":afrm[i][1],"End":afrm[i+1][1],'Face Pos Str':str(afrm[i][2]),'Face Pos End':str(afrm[i+1][2])},ignore_index=True)

#calculate time difference and judging

timeelasped = timeend - sessionStart
timethreshold = timeelasped/9

datetime_object = date.datetime.now()
datetime_object = datetime_object-datetime_object
inittime = datetime_object
inittime2 = datetime_object


for i in range(0,len(nface),2):
    nfacetot.append(nface[i+1][1]-nface[i][1])
for i in range(len(nfacetot)):
    datetime_object += nfacetot[i]

for i in range(0,len(neyes),2):
    neyestot.append(neyes[i+1][1]-neyes[i][1])
for i in range(len(neyestot)):
    inittime += neyestot[i]

for i in range(0,len(afrm),2):
    afrmtot.append(afrm[i+1][1]-afrm[i][1])
for i in range(len(afrmtot)):
    inittime2 += afrmtot[i]

inittime0 = [datetime_object]
inittime = [inittime]
inittime2 = [inittime2]
timeelasped = [timeelasped]

if inittime0[0] >= timethreshold: inittime0.append('Khong tap trung')
else: inittime0.append('tap trung')

if inittime[0] >= timethreshold: inittime.append('Khong tap trung')
else: inittime.append('tap trung')

if inittime2[0] > timethreshold*18 and inittime[0] < timethreshold or inittime0[0] < timethreshold: inittime2.append('tap trung')
else: inittime2.append('khong tap trung')

timeelasped.append(inittime2[1])

masterState = masterState + inittime0 + inittime + inittime2 + timeelasped

for i in range(0,len(masterState),2):
    df4 = df4.append({'nfce / neyes / affrm / TOT': masterState[i], "State": masterState[i + 1]}, ignore_index=True)
df4 = df4.append({'nfce / neyes / affrm / TOT': '', "State": ''}, ignore_index=True)
df4 = df4.append({'State': 'FINAL JUDGEMENT:', "nfce / neyes / affrm / TOT": masterState[-1]}, ignore_index=True)
df4.to_csv('SumState.csv')

stnf = []
for i in range(0,len(nface),2):
    temps = str(nface[i][1]) + ' - ' + str(nface[i+1][1])
    stnf += temps + ' -- '
stnft = ''
stnft = stnft.join(stnf)

stne = []
for i in range(0,len(neyes),2):
    tempss = str(neyes[i][1]) + ' - ' + str(neyes[i+1][1])
    stne += tempss + ' -- '
stnftne = ''
stnftne = stnftne.join(stne)

staf = []
for i in range(0,len(afrm),2):
    tempsss = str(afrm[i][1]) + ' - ' + str(afrm[i+1][1])
    staf += tempsss + ' -- '
stnftaf = ''
stnftaf = stnftaf.join(staf)

userre = ref.child('Ip Addr')
userre.update({
    str(username): ipaddr
})
stat = ref.child('Status')
stat.update({
    username:
    {
        'Ip add': ipaddr,
        'No face time inteval: ': stnft,
        'No eyes time inteval: ': stnftne,
        'Affirmative: ': stnftaf,
        'Status': masterState[-1]
    }
})

print(timeevents[18][1])

timeevents2 = timeevents
for i in range(len(timeevents2)):
    timeevents2[i][1] = str(timeevents2[i][1])

index = 0

def datetimesearch():
    reference = input('Nhap timestamp: ')
    for i in range(len(timeevents2)):
        if timeevents2[i][1] == reference: index = i
    if len(timeevents2[index]) <= 2:
        print('Face/eye coordinates are unavailable at this particular interval')
    else:
        try:
            print('toa do mat', timeevents2[index][2], 'toa do eyes', timeevents2[index][3])
        except Exception:
            print('toa do mat', timeevents2[index][2])

cap.release()
cv2.destroyAllWindows()