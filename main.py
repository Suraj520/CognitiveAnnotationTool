#importing the modules
import dlib
import cv2
import numpy as np
import os
from distutils.dir_util import mkpath
from tkinter import *
#*********************************************************************************************************************************
#defining the functions
#*********************************************************************************************************************************

#defining the function for drawing bounding box
def run(im, multi=False):
    #duplicating the image as 2 sets, one for displaying and the other one being the image over which the user will initialise the annotation by drawing annotation.
    im_disp = im.copy()
    im_draw = im.copy()
    #naming the image window
    window_name = "Window for Drawing Bounding Box"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    #displaying the image window on which user can draw
    cv2.imshow(window_name, im_draw)

    # Defining the list for containing top-left and bottom-down coordinates for the image".
    pts_1 = []
    pts_2 = []

    rects = []
    #initialising the mouse down action event to be initially False
    run.mouse_down = False

#defining the function for annotating the image in two modes : Single Object and Multiple Object Annotation Mode."
    def callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
                if multi == False and len(pts_2) == 1:
                       print("Warning : Single Tracking mode currently enabled can't select multiple.")
                       print("You can delete the previously selected image by Pressing d button on the Keyboard!.")
                       return
                run.mouse_down = True
                pts_1.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP and run.mouse_down == True:
            run.mouse_down = False
            pts_2.append((x, y))
            print("Object Coordinates : [{}, {}]".format(pts_1[-1], pts_2[-1]))
        elif event == cv2.EVENT_MOUSEMOVE and run.mouse_down == True:
            im_draw = im.copy()
            cv2.rectangle(im_draw, pts_1[-1], (x, y), (255,255,255), 3)
            cv2.imshow(window_name, im_draw)

    print("Firstly Press then release the mouse around the object that you wish to annotate \nFor multiple object annotation you can repeat the press and release multiple times")
    cv2.setMouseCallback(window_name, callback)

    print("To continue with the selected objects to annotate, Press P.")
    print("Press esc, followed by closing the gui to exit the program.")

    while True:
        # Use Mouse to draw the rectangular boxes around the image.
        window_name_2 = "Objects to be annotated"
        for pt1, pt2 in zip(pts_1, pts_2):
            rects.append([pt1[0],pt2[0], pt1[1], pt2[1]])
            cv2.rectangle(im_disp, pt1, pt2, (255, 255, 255), 3)
        # Displaying the cropped images
        cv2.namedWindow(window_name_2, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name_2, im_disp)
        key = cv2.waitKey(30)
        if key == ord('p'):
            # Press key `s` to return the selected points
            cv2.destroyAllWindows()
            point= [(tl + br) for tl, br in zip(pts_1, pts_2)]
            corrected_point=check_point(point)
            return corrected_point
    cv2.destroyAllWindows()
    point= [(tl + br) for tl, br in zip(pts_1, pts_2)]
    corrected_point=check_point(point)

    return corrected_point

#function for collecting Bounding box points from the annotations drawn over the image using mouse press and release events
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



#Definition of Functions on button click


def SubmitUserName():
   User = str(UserName.get())
   print("Directory Created !")
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
    s.append("<comment>Created by Suraj @ IIITG - email : hrishabhsuraj52@gmail.com., Linkedin: https://in.linkedin.com/in/suraj52  </comment> ")
    s.append("<images>")
    for i in range(6):
        f.write(s[i]+"\n")
    print("Press `p` to start with automatic annotation of selected objects ")
    while True:
    # Retrieve an image and Display it.
          retval, img = cam.read()
          if not retval:
             print("Frame/ device not accessible, Please check the device id in CV2.VideoCapture or your webcam.")
             exit()
          break
          cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
          cv2.imshow("Image", img)
    cv2.destroyWindow("Image")

    
    points = run(img, multi=True)

    if not points:
       print("ERROR: No object to be annotated")
       exit()

    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", img)

   # Initial co-ordinates of the object to be tracked using dlib correlation tracker
   # Create the tracker object
    tracker = [dlib.correlation_tracker() for _ in range(len(points))]
   # Provide the tracker the initial position of the object
    [tracker[i].start_track(img, dlib.rectangle(*rect)) for i, rect in enumerate(points)]
    alpha=0
    while True:
         User = str(UserName.get())
    # Read frame from device or file
         retval, img = cam.read()
         if not retval:
            print("Device not accessible ")
            exit()
            # Update the tracker
         for i in range(len(tracker)):
             tracker[i].update(img)
            #Get the position of th object, draw a
            #bounding box around it and display it.
             rect = tracker[i].get_position()
             pt1 = (int(rect.left()), int(rect.top()))
             pt2 = (int(rect.right()), int(rect.bottom()))
             cv2.rectangle(img, pt1, pt2, (255, 255, 255), 2)
             print("Object {} Location [{}, {}] \r".format(i, pt1, pt2),)
             if alpha%5==0:
                cv2.imwrite(str(User)+"_"+str(alpha)+".jpg",img)
                annotate=[]
                annotate.append("<image file=" +"'" +str(os.getcwd())+"/"+str(User)+"_"+str(alpha) +".jpg'>")
                annotate.append("<box top="+"'"+str(int(round(abs(rect.top()))))+"'" +" left="+"'"+str(int(round(abs(rect.left()))))+"'" + " width="+"'"+str(int(round(abs(rect.right())))-int(round(abs(rect.left()))))+ "'" +  " height="+"'"+str(int(round(abs(rect.bottom())))- int(round(abs(rect.top()))))+"'" +" />")
#	        annotate.append("</image>")
                for i in range(len(points)+1):
                    f.write(annotate[i]+"\n")
                list1=[]
                list1.append("</image>")
                f.write(list1[0]+"\n") 
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
            for i in range(2):
                f.write(s[i]+"\n")
            cam.release()
            cv2.destroyAllWindows()
            break
         alpha+=1
    # Continue until the user presses ESC key
    #if cv2.waitKey(1) == 27:




def CamSet():
    # Create the VideoCapture object
    cam = cv2.VideoCapture(0)
    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print("Video device or file couldn't be opened")
        exit()
    CapBBox()


def Exit():

    exit()



root = Tk()
root.title('Cogntive Annotation Tool')
Label(root, text="Welcome User to the CognitiveAnnotationTool", fg="blue")
Label(root, text="Enter User Name",fg ='blue').grid(row=1,column=0)
#creating a text field for User
UserName= Entry(root, bd =1)
UserName.grid(row=1 ,column=1)
Button(root, text='Submit User Name' ,command=SubmitUserName,fg ='yellow',bg='black' ).grid(row=3, column=1, sticky=W, pady=4)
Button(root, text='Capture Bounding Box(s)',command=CapBBox ,fg ='yellow',bg='black').grid(row=5, column=0, sticky=W, pady=4)


#Instruction to use'
Label(root, text=">>>>>>>>Steps to Use the software :>>>>>>>>>>>>>>>>>>>>>>>>",fg ='red').grid(row=6,column=0)
Label(root, text="1. Enter User Name and Click <<Submit User Name>> Only Once**",fg ='blue').grid(row=7,column=0)
Label(root, text="2.Click Capture Bounding Box(s)",fg ='blue').grid(row=8,column=0)
Label(root, text="3.Select the `Window for Drawing Bounding Box` and draw the bounding box using mouse around the objects to be annotated",fg ='blue').grid(row=9,column=0)
Label(root, text="4. Press'p' on your keyboard once BBox(s) are created to start annotation",fg ='blue').grid(row=10,column=0)
Label(root, text="Note : **Please Move objects in BBox slowly to create better annotations.**",fg ='red').grid(row=11,column=0)
Label(root, text="5. Want to stop Annotation Press 'esc'on keyboard once then press cross on the gui to close or (win + esc)",fg ='blue').grid(row=12,column=0)
Label(root, text="*********Created by : Suraj*********************",fg ='red').grid(row=13,column=0)
Label(root,text ="Email Id : hrishabhsuraj52@gmail.com. LinkedIn: https://in.linkedin.com/in/suraj52 ",fg='black').grid(row=14,column=0)
Label(root,text ="Use the tool for research purpose only! ",fg='black').grid(row=14,column=0)

root.mainloop()





i = 0
for i in range(1):
    SubmitUserName()
    i= i+1
cam = cv2.VideoCapture(0)
