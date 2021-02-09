## All rights reserved to Suraj ####
### Please note the code is non-optimized intentionally to restrict its reproducibility in its exact form and I may give the optimized code upon your query for a commercial license.

# If you are reviewing the code for assesment for any applied research/dev positions. kindly review: https://github.com/Suraj520/Python_developer_track with more weightage.

#importing the modules
import dlib
import cv2
import sys
import os
from distutils.dir_util import mkpath
from tkinter import *
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
                       print("Single Tracking mode currently enabled can't select multiple.")
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
    print("Press esc, followed by pressing the exit button.")
## All rights reserved to Suraj ####
### Please note the code is non-optimized intentionally to restrict its reproducibility in its exact form and I may give the optimized code upon your query for a commercial license.
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
            #destroying the window by this time
            cv2.destroyAllWindows()
            point= [(tl + br) for tl, br in zip(pts_1, pts_2)]
            corrected_point=check_point(point)
            return corrected_point
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()
    #cv2.destroyAllWindows()
    point= [(tl + br) for tl, br in zip(pts_1, pts_2)]
    corrected_point=check_point(point)

    return corrected_point
## All rights reserved to Suraj ####
### Please note the code is non-optimized intentionally to restrict its reproducibility in its exact form and I may give the optimized code upon your query for a commercial license.
#function for collecting Bounding box points_suraj_tool from the annotations drawn over the image using mouse press and release events
def check_point(points_suraj_tool):
    out=[]
    for point in points_suraj_tool:
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
## All rights reserved to Suraj ####
### Please note the code is non-optimized intentionally to restrict its reproducibility in its exact form and I may give the optimized code upon your query for a commercial license.
#Definition of Functions on button click
## All rights reserved to Suraj ####
### Please note the code is non-optimized intentionally to restrict its reproducibility in its exact form and I may give the optimized code upon your query for a commercial license.
def SubmitUserName():
   User = str(UserName.get())
   print("Directory created!!")
   mkpath(User)
   path = str(os.getcwd())+"/"+(User)
   #going to the directory
   os.chdir(path)
## All rights reserved to Suraj ####
### Please note the code is non-optimized intentionally to restrict its reproducibility in its exact form and I may give the optimized code upon your query for a commercial license.
def CapBBox():
    a =0
    User = str(UserName.get())
    cam = cv2.VideoCapture(0)
    f= open("annotation.xml","w+")
    suraj_list = []
    suraj_list.append("<?xml version='1.0' encoding='ISO-8859-1'?>")
    suraj_list.append("<?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?>")
    suraj_list.append("<dataset>")
    suraj_list.append("<name>Dlib-C++ compatible dataset</name>")
    suraj_list.append("<comment>Created by Suraj - email : hrishabhsuraj52@gmail.com.,linkedin:https://in.linkedin.com/in/suraj52 </comment> ")
    suraj_list.append("<images>")
    for i in range(6):
        f.write(suraj_list[i]+"\n")
    print("Press `p` to start with automatic annotation of selected objects ")
    ## All rights reserved to Suraj ####
### Please note the code is non-optimized intentionally to restrict its reproducibility in its exact form and I may give the optimized code upon your query for a commercial license.
    frame_count = 0
    while True:
         User = str(UserName.get())
         retval, img = cam.read()
         #Freeze at frame 1 and prompt for user annotation.
         #let the user annotate on frame 1 and then accordingly as per the number of bounding boxes, initialise the trackers
         if frame_count == 0:
             points_suraj_tool = run(img, multi=True)
             if not points_suraj_tool:
                print("ERROR: No object to be annotated")
                exit()
             # Create the tracker object
             tracker = [dlib.correlation_tracker() for _ in range(len(points_suraj_tool))]
             # Provide the tracker the initial position of the object
             [tracker[i].start_track(img, dlib.rectangle(*rect)) for i, rect in enumerate(points_suraj_tool)]
             frame_count+=1
         #start writing from frame 2 onwards
         cv2.imwrite(str(User)+"_"+str(a)+".jpg",img)
         if not retval:
            print("Device not accessible ")
            exit()
         # Update the tracker
         annotate=[]
         annotate.append("<image file=" +"'" +str(os.getcwd())+"/"+str(User)+"_"+str(a) +".jpg'>")
         for i in range(len(tracker)):
             tracker[i].update(img)
        # Get the position of th object, draw a
        # bounding box around it and display it.
             rect = tracker[i].get_position()
             pt1 = (int(rect.left()), int(rect.top()))
             pt2 = (int(rect.right()), int(rect.bottom()))
             cv2.rectangle(img, pt1, pt2, (255, 255, 255), 2)
             print("Object {} Location [{}, {}] \r".format(i, pt1, pt2),)
             annotate.append("<box top="+"'"+str(int(round(abs(rect.top()))))+"'" +" left="+"'"+str(int(round(abs(rect.left()))))+"'" + " width="+"'"+str(int(round(abs(rect.right())))-int(round(abs(rect.left()))))+ "'" +  " height="+"'"+str(int(round(abs(rect.bottom())))- int(round(abs(rect.top()))))+"'" +" />")

         for i in range(len(points_suraj_tool)+1):
             f.write(annotate[i]+"\n")
         list1=[]
         list1.append("</image>")
         f.write(list1[0]+"\n")
         a = a+1
## All rights reserved to Suraj ####
### Please note the code is non-optimized intentionally to restrict its reproducibility in its exact form and I may give the optimized code upon your query for a commercial license.
         loc = (int(rect.left()), int(rect.top()-20))
         txt = "Object tracked at [{}, {}]".format(pt1, pt2)
         cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
         cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
         cv2.imshow("Image", img)
         if cv2.waitKey(1)==27:
            suraj_list=[]
            suraj_list.append("</images>")
            suraj_list.append("</dataset>")
            for i in range(2):
                f.write(suraj_list[i]+"\n")
            cam.release()
            cv2.destroyAllWindows()
            break
## All rights reserved to Suraj ####
### Please note the code is non-optimized intentionally to restrict its reproducibility in its exact form and I may give the optimized code upon your query for a commercial license.
def Exit():
    sys.exit()
## All rights reserved to Suraj ####
### Please note the code is non-optimized intentionally to restrict its reproducibility in its exact form and I may give the optimized code upon your query for a commercial license.
if __name__ == "__main__":
    root = Tk()
    root.title('Cogntive Annotation Tool')
    Label(root, text="Welcome User to the CognitiveAnnotationTool", fg="blue")
    Label(root, text="Enter User Name",fg ='blue').grid(row=1,column=0)
    #creating a text field for User
    UserName= Entry(root, bd =1)
    UserName.grid(row=1 ,column=1)
    Button(root, text='Submit User Name' ,command=SubmitUserName,fg ='yellow',bg='black' ).grid(row=3, column=1, sticky=W, pady=4)
    Button(root, text='Capture Bounding Box(s)',command=CapBBox ,fg ='yellow',bg='black').grid(row=5, column=0, sticky=W, pady=4)
    Button(root, text='Exit',command=Exit ,fg ='yellow',bg='black').grid(row=18, column=1, sticky=W, pady=4)
## All rights reserved to Suraj ####
### Please note the code is non-optimized intentionally to restrict its reproducibility in its exact form and I may give the optimized code upon your query for a commercial license.
                                  #Instruction to use the software
    Label(root, text=">>>>>>>>>>>>>>>>>>>>>>>>Steps to Use the software :>>>>>>>>>>>>>>>>>>>>>>>>",fg ='red').grid(row=6,column=0)
    Label(root, text="1. Enter User Name and Click <<Submit User Name>> Only Once**",fg ='blue').grid(row=7,column=0)
    Label(root, text="2.Click Capture Bounding Box(s)",fg ='blue').grid(row=8,column=0)
    Label(root, text="3.Select the `Window for Drawing Bounding Box` and draw the bounding box using mouse around the ROI(s)",fg ='blue').grid(row=9,column=0)
    Label(root, text="4.Press'p' on your keyboard once BBox(s) are created to start annotation,close the annotation by pressing esc buttom",fg ='blue').grid(row=10,column=0)
    Label(root, text="Note : **Please Move objects in BBox slowly to create quality annotations.**",fg ='red').grid(row=11,column=0)
    Label(root, text="5. Close the software by pressing the exit button on GUI.",fg ='blue').grid(row=12,column=0)
    Label(root, text="**Created by : Suraj : Linkedin: https://www.linkedin.com/in/suraj52/**",fg ='red').grid(row=13,column=0)
    Label(root,text ="Only for Research Purposes!",fg='black').grid(row=14,column=0)

    root.mainloop()
    SubmitUserName()
## All rights reserved to Suraj ####
### Please note the code is non-optimized intentionally to restrict its reproducibility in its exact form and I may give the optimized code upon your query for a commercial license.
#Support if you like the software :)
