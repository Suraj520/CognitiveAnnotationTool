#importing the modules
import dlib
import cv2
import numpy as np
import os
from distutils.dir_util import mkpath
#defining the functions
#******************************************************************************
#defining the function for BBox capture
def run(im, multi=False):
    im_disp = im.copy()
    im_draw = im.copy()
    window_name = "Select bounding box."
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, im_draw)

    # List containing top-left and bottom-right to crop the image.
    pts_1 = []
    pts_2 = []

    rects = []
    run.mouse_down = False

    def callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
	    if multi == False and len(pts_2) == 1:
		print "WARN: Cannot select another object in SINGLE OBJECT TRACKING MODE."
		print "Delete the previously selected object using key `d` to mark a new location."
		return
            run.mouse_down = True
            pts_1.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP and run.mouse_down == True:
            run.mouse_down = False
            pts_2.append((x, y))
            print "Object selected at [{}, {}]".format(pts_1[-1], pts_2[-1])
        elif event == cv2.EVENT_MOUSEMOVE and run.mouse_down == True:
            im_draw = im.copy()
            cv2.rectangle(im_draw, pts_1[-1], (x, y), (255,255,255), 3)
            cv2.imshow(window_name, im_draw)

    print "Press and release mouse around the object to be tracked. \n You can also select multiple objects."
    cv2.setMouseCallback(window_name, callback)

    print "Press key `p` to continue with the selected points."
    print "Press key `q` to quit the program."

    while True:
        # Draw the rectangular boxes on the image
        window_name_2 = "Objects to be tracked."
        for pt1, pt2 in zip(pts_1, pts_2):
            rects.append([pt1[0],pt2[0], pt1[1], pt2[1]])
            cv2.rectangle(im_disp, pt1, pt2, (255, 255, 255), 3)
        # Display the cropped images
        cv2.namedWindow(window_name_2, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name_2, im_disp)
        key = cv2.waitKey(30)
        if key == ord('p'):
            # Press key `s` to return the selected points
            cv2.destroyAllWindows()
            point= [(tl + br) for tl, br in zip(pts_1, pts_2)]
            corrected_point=check_point(point)
            return corrected_point
        elif key == ord('q'):
            # Press key `q` to quit the program
            print "Quitting without saving."
            exit()
    cv2.destroyAllWindows()
    point= [(tl + br) for tl, br in zip(pts_1, pts_2)]
    corrected_point=check_point(point)

    return corrected_point
#function for collecting Bbox points
def check_point(points):
    out=[]
    for point in points:
        minx=point[0]
        #to find min and max x coordinates
        if point[0]<point[2]:
            maxx=point[2]
        else:
            minx=point[2]
            maxx=point[0]
        #to find min and max y coordinates
        if point[1]<point[3]:
            miny=point[1]
            maxy=point[3]
        else:
            miny=point[3]
            maxy=point[1]
        out.append((minx,miny,maxx,maxy))

    return out


#creating a GUI layout
from Tkinter import *

#Definition of Functions on button click


def SubmitUserName():
   User = str(UserName.get())
   print type(User)
   mkpath(User)
   path = str(os.getcwd())+"/"+(User)
   #going to the directory
   os.chdir(path)




def CapBBox():
    a =0
    User = str(UserName.get())
    cam = cv2.VideoCapture(0)
    f= open("annotation.xml","w+")
    s = []
    s.append("<?xml version='1.0' encoding='ISO-8859-1'?>")
    s.append("<?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?>")
    s.append("<dataset>")
    s.append("<name>Dlib-C++ compatible dataset</name>")
    s.append("<comment>Created by Suraj @ IIITG - email : hrishabhsuraj52@gmail.com. linkedin:https://in.linkedin.com/in/suraj-b85555109 </comment> ")
    s.append("<images>")
    for i in xrange(6):
        f.write(s[i]+"\n")
    print "Press key `p` to pause the video to start tracking"
    while True:
    # Retrieve an image and Display it.
          retval, img = cam.read()
          if not retval:
             print "Cannot capture frame device"
             exit()
          break
          cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
          cv2.imshow("Image", img)
    cv2.destroyWindow("Image")

    # Co-ordinates of objects to be tracked
    # will be stored in a list named `points`
    points = run(img, multi=True)

    if not points:
       print "ERROR: No object to be tracked."
       exit()

    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", img)

   # Initial co-ordinates of the object to be tracked
   # Create the tracker object
    tracker = [dlib.correlation_tracker() for _ in xrange(len(points))]
   # Provide the tracker the initial position of the object
    [tracker[i].start_track(img, dlib.rectangle(*rect)) for i, rect in enumerate(points)]

    while True:
         User = str(UserName.get())
    # Read frame from device or file
         retval, img = cam.read()
         if not retval:
            print "Cannot capture frame device | CODE TERMINATION :( "
            exit()
    # Update the tracker
         for i in xrange(len(tracker)):
             tracker[i].update(img)
        # Get the position of th object, draw a
        # bounding box around it and display it.
             rect = tracker[i].get_position()
             pt1 = (int(rect.left()), int(rect.top()))
             pt2 = (int(rect.right()), int(rect.bottom()))
             cv2.rectangle(img, pt1, pt2, (255, 255, 255), 1)
             print "Object {} tracked at [{}, {}] \r".format(i, pt1, pt2),
             annotate=[]

             annotate.append("<image file=" +"'" +str(os.getcwd())+"/"+str(User)+"_"+str(a) +".jpg'>")
             annotate.append("<box top="+"'"+str(int(round(abs(rect.top()))))+"'" +" left="+"'"+str(int(round(abs(rect.left()))))+"'" + " width="+"'"+str(int(round(abs(rect.right())))-int(round(abs(rect.left()))))+ "'" +  " height="+"'"+str(int(round(abs(rect.bottom())))- int(round(abs(rect.top()))))+"'" +" />")
             annotate.append("</image>")
             for i in xrange(3):
                 f.write(annotate[i]+"\n")
             cv2.imwrite(str(User)+"_"+str(a)+".jpg",img)
             a = a+1

             loc = (int(rect.left()), int(rect.top()-20))
         txt = "Object tracked at [{}, {}]".format(pt1, pt2)
         cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
         cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
         cv2.imshow("Image", img)
         if cv2.waitKey(1)==27:
            s=[]
            s.append("</images>")
            s.append("</dataset>")
            for i in xrange(2):
                f.write(s[i]+"\n")
            cam.release()
            cv2.destroyAllWindows()
            break
    # Continue until the user presses ESC key
    #if cv2.waitKey(1) == 27:



'''
def CamSet():
    # Create the VideoCapture object
    cam = cv2.VideoCapture(0)
    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print "Video device or file couldn't be opened"
        exit()
    CapBBox()
'''

def Exit():

    exit()



root = Tk()
root.title('CogntiveAnnotationTool')
Label(root, text="Welcome User to the CognitiveAnnotationTool", fg="blue")
Label(root, text="Enter User Name",fg ='blue').grid(row=1,column=0)
#creating a text field for User
UserName= Entry(root, bd =1)
UserName.grid(row=1 ,column=1)
#creating a submit button for the UserRegistration
Button(root, text='Submit User Name' ,command=SubmitUserName,fg ='yellow',bg='black' ).grid(row=3, column=1, sticky=W, pady=4)
#Button(root, text='Start WebCam Feed' ,command=CamSet,fg ='yellow',bg='black' ).grid(row=4, column=1, sticky=W, pady=4)
Button(root, text='Capture Bounding Box(s)',command=CapBBox ,fg ='yellow',bg='black').grid(row=5, column=0, sticky=W, pady=4)
#Button(master, text='Record Annotation' ,fg ='yellow',bg='black', command = RecordAnnotation ).grid(row=4, column=2, sticky=W, pady=4)
Button(root, text='Quit', command=Exit ,fg ='yellow',bg='black' ).grid(row=5, column=1, sticky=W, pady=4)
#writing the main function

#Instruction to use'
Label(root, text="Steps to Use the software :>>>>>>>>>>>>>>>>>>>>>>>>",fg ='red').grid(row=6,column=0)
Label(root, text="1. Enter User Name and Click <<Submit User Name>> Only Once**",fg ='blue').grid(row=7,column=0)
Label(root, text="2.Click Capture Bounding Box(s)",fg ='blue').grid(row=8,column=0)
Label(root, text="3. Slide the Image window appearing and Use mouse click to create Bounding Box",fg ='blue').grid(row=9,column=0)
Label(root, text="4. Hit 'p' on your keyboard once BBox(s) are created",fg ='blue').grid(row=10,column=0)
Label(root, text="Note : **Please Move objects in BBox slowly to create better annotations**",fg ='red').grid(row=11,column=0)
Label(root, text="5. Want to stop Annotation Press 'esc'on keyboard once then Button exit on the GUI",fg ='blue').grid(row=12,column=0)
Label(root, text="*********CopyRight : Suraj*********************",fg ='red').grid(row=13,column=0)


root.mainloop()





i = 0
for i in range(1):
    SubmitUserName()
    i= i+1
cam = cv2.VideoCapture(0)
