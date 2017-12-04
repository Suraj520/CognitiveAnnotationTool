# Cognitive Annotation Tool

A Tool aimed to help Researchers get rid of annotating images manually for Object Detection Tasks. The Tool currently creates annotation of images as .xml files compatible with dlib- C++ machine learning library (https://github.com/davisking/dlib). The Images and its corresponding annotation files are saved in the folder named as the Username asked during the initialisation of the software.
The software is capable of annotating huge number of images needed to create high quality custom machine learning and Deep learning based object detectors.This tool acts as a Automatic version of Imglab(an annotation tool supported by dlib).

## Getting Started


### Prerequisites
 
1. Install and compile dlib-C++ library using the github repository ((https://github.com/davisking/dlib) or using pip commands 

```
//for python 2
>>>$ sudo pip install dlib 
//for python 3
>>>$ sudo pip3 install dlib
```
Once installed open python2/ python3 accordingly and check if dlib is installed by importing it.

```
>>import dlib

```
2. Install and compile OpenCV from (http://milq.github.io/install-opencv-ubuntu-debian/) and check if it is installed.

```
>>import cv2

```
3. Check if Tkinter is installed, If not Install  using 

```
\\for Python2
>>>sudo apt-get install python-tk
\\for Python3
>>>$sudo apt-get install python3-tk
```
If installed Check by importing
```
>>from Tkinter import *

```
### Executing

Open the terminal and run the code as
```
>>$python main.py
\\for python3
>>$python3 main.py
```

Once the GUI of the Software appears

Follow the steps mentioned below:

```
1.Enter the username or a custom class name for which you want the Images to be annotated then click on the button " Submit User Name". To ensure that username is accepted check that the path from which the code is run must contain a Folder named with the submitted username. "Avoid Clicking the Submit User Name to many times as it may lead to creation of multiple Folders".

2.Once the username is submitted, Click on the Capture Bounding Box(s) button until two image windows containing snapshots of Image captured from the webcam appears. The two Image windows may be overlapping, slide the window to find the image window named aos  'Window for Drawing bounding box'.

3.Using Mouse Release and Hold events draw bounding box(s) around the objects you wish to annotate. If you want to create a object detector capable of detecting  multiple objects draw multiple bounding box(s) around the object. (Keep track of the number of objects annotated from the terminal. If by mistake a wrong bounding box is drawn use 'd' key to delete.)

4.Once bounding box(s) is/are drawn, press p to start automatic annotation of images from Realtime webcam feed. The annotated images(Images and the annotation.xml file containing the coordinates of the bounding box[dlib- compatible] are saved in the directory named by the usename.)

(Multiple object annotation depends upon the processing power of the system on which the code is executed as lag persists as more than 10 objects are annotated over webcam feed using a 2.5 Ghz (quadcore Intel pentium, 4 GB Ram) system.

```
###Editing the annotation.xml file
```
Edit the path of the image mentioned in the annotation.xml file by using a Sublime Text/gedit/emacs/atom or equivalent editor by replacing the path mentioned in single quotes using find all and replace all command

In Sublime text go to Find >> then go to Find.. >> then follow the steps mentioned in the below example.

for example
For changing
<image file='/home/abc/Desktop/Username/Username_x.jpg'>
by 
<image file='/ghf/xyz/newpath/Username/Username_x.jpg'>
paste /home/abc/Desktop/Username/ to find all in the above mentioned editor
and once all changes are found
replace by /ghf/xyz/newpath/Username/ by pasting it in replace all tab of Sublime Text for example

```



## Training custom object detectors

Once annotated images(images and annotation.xml files ) are generated, It can be used to create custom object detectors using dlib-C++
machine learning library. To train machine learning hogg detectors using dlib, Use  train_object_detector.py on dlib repository(https://github.com/davisking/dlib/blob/master/python_examples/train_object_detector.py). Edit the hyperparameters by adjusting the epsilon and C in the file
```
Change epsilon according to the performance of the object detector
>>>options.epsilon = 1e-6
```
For training deep learning based object detectors use dnn_mmod_ex.cpp (https://github.com/davisking/dlib/blob/master/examples/dnn_mmod_ex.cpp) and accordingly tune the hyperparameters for preventing the object detector from over fitting as the annotated images are captured regularly from the webcam so there is a chance that deep learning object detectors might overfit if trained on annotated images that don't show any significant temporal or spatial change in the environment around the object. Moreover after editing the dnn_mmod_ex.cpp don't forget to make and execute the executable as ./dnnmmod with path of the xml file{as per the output file}



## Steps to Follow inorder to get the best use of this Software.
Suppose you are willing to create an object detector for a Water Bottle, now as you are aware that inorder to create robust object detectors, The model must be trained on a variety of in the wild images.

Let's us assume different scenarios we might prefer for creating a good object detector
Case 1: varying light conditions, Case 2: varying angle of image capture, Case 3: varying background etc

We will run the software for each of the above mentioned scenarios.

For case 1 : Put user name as Case 1 , submit and record the annotated images of the Water bottle for some time. The annotations for each automatically labelled image will be stored in Case1.xml.

Similarly run it for Case 2, Case 3,... Case n.. so that finally we get .xml files corresponding to each case. 

Now, put all images in a single folder, copy and paste all annotations recorded in a single annotation.xml file
(Remember that while doing the task of appending all the annotation in single .xml file, path conflicts will rise so to overcome this change path using a editor like gedit, Sublime Text which has an inbuilt find all and replace all feature , replace all path of xml labels to the current path where all images are stored.)


Finally you will have a large dataset for training your dlib custom object detector using dnn_mmod_ex.cpp or the corresponding python alternative.




* [davisking/dlib](https://github.com/davisking/dlib)- Machine learning library.


## Built With

* [davisking/dlib](https://github.com/davisking/dlib)- Machine learning library.




## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details



