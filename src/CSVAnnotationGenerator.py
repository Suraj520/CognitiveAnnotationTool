#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import scipy.ndimage.interpolation as snd
import matplotlib.pyplot as plt
import glob
import os
#sudo pip install bs4 incase you find import error
from bs4 import BeautifulSoup

#Author: Suraj
#Contact No: +918486656592
#Email: hrishabhsuraj52@gmail.com
#Website: https://suraj.glitch.me


# In[ ]:


#function to parse xml files and then search the data between a specific tag
def xml_parse(file):
    f = open(file)
    xml = f.read()
    soup = BeautifulSoup(xml)
    return soup
#Please provide the Classname down here:
#Eg: Dog, Cat, Hand, BasketBall, Car, Plane or any custom class etc
ClassName= "ClassName"

#Author: Suraj
#Contact No: +918486656592
#Email: hrishabhsuraj52@gmail.com
#Website: https://suraj.glitch.me


# In[ ]:


import xml.etree.ElementTree as ET
#Provide the path to the xml file which you want to convert down here... 
tree = ET.parse('/home/dl/Dataset/annotation.xml')
root = tree.getroot()
labels =[]
name=[]
print('Bounding Box:')
for element in root.iter(tag='image'):
    name.append(element.attrib)
    print(element.attrib)
    print(element.text)

for element in root.iter(tag= 'box'):
    labels.append(element.attrib)
    print(element.attrib)
    print(element.text)


#Author: Suraj
#Contact No: +918486656592
#Email: hrishabhsuraj52@gmail.com
#Website: https://suraj.glitch.me


# In[ ]:


#Extracting images name
file_names =[]
coordinates =[]
for i in xrange(len(labels)):
    file_names.append(str(str(name[i]).split(':')[1]).split('\'')[1])
    list= str(str(str(labels[i]).split(':'))).split("'")[7],str(str(str(labels[i]).split(':'))).split("'")[11],str(str(str(labels[i]).split(':'))).split("'")[3],str(str(str(labels[i]).split(':'))).split("'")[15]
    #print(list)
    print(list)
    coordinates.append(list)

#Expected Verbose after succesful run of this cell
# For eg : ('106', '328', '224', '348')


#Author: Suraj
#Contact No: +918486656592
#Email: hrishabhsuraj52@gmail.com
#Website: https://suraj.glitch.me


# In[ ]:


features =[]
labels_matrix=[]
for counter in ((xrange(len(file_names)))):
    print(file_names[counter])
    for file in (glob.glob(file_names[counter])):
        coordinates[counter]= [coordinates[counter][0], coordinates[counter][1], str(int(coordinates[counter][0]) + int(coordinates[counter][2])), str(int(coordinates[counter][3])+ int(coordinates[counter][1]))]
        print(coordinates[counter])
        labels_matrix.append(coordinates[counter])

        
#Expected Verbose after succesful run of this cell.
# For eg" /home/dl/Download/images_73.jpg
#For eg: ['106', '329', '328', '675']

#Author: Suraj
#Contact No: +918486656592
#Email: hrishabhsuraj52@gmail.com
#Website: https://suraj.glitch.me


# In[ ]:


#Please provide the absolute system path where you wish to generate the Faster RCNN compatible label text file.
f= open("/home/dl/Dataset/annotations.txt","w+")
for i in range(len(labels_matrix)):
    f.write(str(file_names[i])+","+ str(labels_matrix[i][0])+ "," + str(labels_matrix[i][1])+ ","+str(labels_matrix[i][2])+ ","+ str(labels_matrix[i][3])+ ","+str(ClassName) +"\n")
print("The annotation file in faster RCNN compatible text/retinanet format succesfully generated in the path!!")
f.close()

#Author: Suraj
#Contact No: +918486656592
#Email: hrishabhsuraj52@gmail.com
#Website: https://suraj.glitch.me


# In[ ]:





# In[ ]:




