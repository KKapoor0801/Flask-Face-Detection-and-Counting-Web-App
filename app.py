'''from flask import Flask, render_template, Response
from camera import Video
import cv2

app=Flask(__name__,template_folder='template')

@app.route("/")
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'-- frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame +
        b'\r\n\r\n')

@app.route("/video")

def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(debug=True)'''

from flask import Flask,render_template,Response
import cv2
import time
import sys
import urllib
import urllib.request


app=Flask(__name__,template_folder='template')
camera=cv2.VideoCapture(0)
def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        
        if not success:
            break
        else:
            faceCascade = cv2.CascadeClassifier(r'C:\Users\kesha\Desktop\People-Counting-in-Real-Time\Face_Detection\haarcascade_frontalface_default.xml')
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                
                scaleFactor=1.2,
                minNeighbors=5
                ,     
                minSize=(20, 20)
            )
            i=0
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                i+=1
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                cv2.putText(frame, 'face num'+str(i),(x-10, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0),2)
                if(x<=320 and y>240 and (x+w)<=320 and (y+h)>240):
                    print("Q1")
                elif(x<320 and y<240 and (x+w)<320 and (y+h)<240):
                    print("Q2")
                elif(x>320 and y<=240 and (x+w)>320 and (y+h)<=240):
                    print("Q3")
                elif(x>320 and y>240 and (x+w)>320 and (y+h)>240):
                    print("Q4")
                else:
                    print("None")
                time.sleep(5)
                print(x,y,(x+w),(y+h), i)

            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)