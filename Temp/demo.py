# Import the required modules
import dlib
import cv2
import argparse as ap
import get_points
import Tkinter
import tkMessageBox
from Tkinter import *
#importing library for
from distutils.dir_util import mkpath
from get_points import *
import subprocess
import os
#importing directory for executing bash commands in python
def StartWebCam():
    source =0


#def Register():



def run( dispLoc=False):

    #initialising a .xml file for the same





    #initialising the GUI frame work
    master = Tk()
    master.title('IntelligentAnnotationTool')
    User = StringVar()
    root.maxsize(400,400)
    root.minsize(200,200)
    Label(master, text="Enter User Name",fg ='blue').grid(row=1)
    e1 = Entry(master,textvariable='User')
    e1.grid(row=1, column=1)


    Button(master, text='Quit', command=master.quit ,fg ='yellow',bg='black' ).grid(row=4, column=2, sticky=W, pady=4)
    Button(master, text='Submit User Name' ,command=Register,fg ='yellow',bg='black' ).grid(row=3, column=1, sticky=W, pady=4)
    Button(master, text='Record Annotation' ,fg ='yellow',bg='black', ).grid(row=3, column=2, sticky=W, pady=4)
    Button(master, text='Start Webcam Feed', command=StartWebCam ,fg ='yellow',bg='black').grid(row=4, column=1, sticky=W, pady=4)
    Button(master, text='Capture Bounding Box(s)' ,fg ='yellow',bg='black').grid(row=4, column=0, sticky=W, pady=4)
    Label(master, text="Step 1 : Submit User Name to create a directory where Images and .xml will be stored" ,fg='blue').grid(row=5)
    Label(master, text="Step 2 : Start WebCam Feed" ,fg ='blue').grid(row=6)
    Label(master, text="Step 3 : Capture Bounding Box(s) using mouse clicks" ,fg ='blue').grid(row=7)
    Label(master, text="Step 4: Ensure Proper Tracking , then press Record Annotation" ,fg ='blue').grid(row=8)
    Label(master, text="Step 5 : Once Done ! Press quit" ,fg ='blue').grid(row=9)
    Label(master, text="@ Suraj" ,fg ='red').grid(row=10)
    #print UserName
    UserName = self.e1.get()
    mkpath(UserName)
    path = os.getcwd()+"/"+UserName
    #going to the directory
    os.chdir(path)
    f= open("annotation.xml","w+")
    root.mainloop()
    #writing to the annonation file
    s = []
    s.append("<?xml version='1.0' encoding='ISO-8859-1'?>")
    s.append("<?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?>")
    s.append("<dataset>")
    s.append("<name>Dlib-C++ compatible dataset</name>")
    s.append("<comment>Created by Suraj @ IIITG - email : hrishabhsuraj52@gmail.com. </comment> ")
    s.append("<images>")
    for i in range(6):
        f.write(s[i]+"\n")
    #creating a  Gui button for saving images
#    B = Tkinter.Button(top, text ="Start Annonations", command = StartAnnotate)
#    B.pack()
#    top.mainloop()

    # Create the VideoCapture object
    # Retrieve an image and Display it.
    cam = cv2.VideoCapture(0)


    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print("Video device or file couldn't be opened")
        exit()

    print("Press key `p` to pause the video to start tracking")
    while True:
        retval, img = cam.read()
        if not retval:
            print("Cannot capture frame device")
            exit()
        if(cv2.waitKey(10)==ord('p')):
            break
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)
    cv2.destroyWindow("Image")

    # Co-ordinates of objects to be tracked
    points = get_points.run(img, multi=True)
    # will be stored in a list named `points`

    if not points:
        print("ERROR: No object to be tracked.")
        exit()

    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", img)


    # Initial co-ordinates of the object to be tracked
    # Create the tracker object
    tracker = [dlib.correlation_tracker() for _ in range(len(points))]
    # Provide the tracker the initial position of the object
    [tracker[i].start_track(img, dlib.rectangle(*rect)) for i, rect in enumerate(points)]

    while True:
        # Read frame from device or file
        retval, img = cam.read()
        if not retval:
            print("Cannot capture frame device | CODE TERMINATION :( ")
            exit()
        # Update the tracker
        for i in range(len(tracker)):
            tracker[i].update(img)
            # Get the position of th object, draw a
            # bounding box around it and display it.
            rect = tracker[i].get_position()
            pt1 = (int(rect.left()), int(rect.top()))
            pt2 = (int(rect.right()), int(rect.bottom()))
            cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
            #here append it to the xml file you have opened
            print("Object {} tracked at [{}, {}] \r".format(i, pt1, pt2),)
            annotate=[]
        #    annotate.append("<image file='./"+i +".jpg'>")
        #    annotate.append("<box top='275' left='165' width='115' hei ght='155'/>")
        #    </image>

            if dispLoc:
                loc = (int(rect.left()), int(rect.top()-20))
            txt = "Object tracked at [{}, {}]".format(pt1, pt2)
            cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", img)








        # Continue until the user presses ESC key
        if cv2.waitKey(1) == 27:
            break

    # Relase the VideoCapture object
    cam.release()



if __name__ == "__main__":
    # Parse command line arguments
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--deviceID", help="Device ID")
    group.add_argument('-v', "--videoFile", help="Path to Video File")
    parser.add_argument('-l', "--dispLoc", dest="dispLoc", action="store_true")
    args = vars(parser.parse_args())

    # Get the source of video
    if args["videoFile"]:
        source = args["videoFile"]
    else:
        source = int(args["deviceID"])

    run(source, args["dispLoc"])
