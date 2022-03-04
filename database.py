import sqlite3
import hashlib
import datetime
import MySQLdb
from flask import session
from datetime import datetime
#from tensorflow.keras.preprocessing.image import ImageDataGenerator
#from tensorflow.keras.applications import VGG16
#from tensorflow.keras.layers import AveragePooling2D
#from tensorflow.keras.layers import Dropout
#from tensorflow.keras.layers import Flatten
##from tensorflow.keras.layers import Dense
#from tensorflow.keras.layers import Input
#from tensorflow.keras.models import Model
#from tensorflow.keras.optimizers import Adam
#from tensorflow.keras.utils import to_categorical
#from sklearn.preprocessing import LabelBinarizer
#from sklearn.model_selection import train_test_split
#from sklearn.metrics import classification_report
#from sklearn.metrics import confusion_matrix
#from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2
import os
#from tensorflow.keras.preprocessing import image
#from tensorflow.keras.preprocessing.image import ImageDataGenerator
#from tensorflow.keras.models import load_model
#from tensorflow.keras.preprocessing import image
import numpy as np
import os
import numpy as np
import cv2
import natsort
import xlwt
import datetime

from color_equalisation import RGB_equalisation
from global_histogram_stretching import stretching
from hsvStretching import HSVStretching
from sceneRadiance import sceneRadianceRGB 
 
 

def db_connect():
    _conn = MySQLdb.connect(host="localhost", user="root",
                            passwd="root", db="logo")
    c = _conn.cursor()

    return c, _conn

# -------------------------------register-----------------------------------------------------------------
def user_reg(id,username, password, email, mobile, address,):
    try:
        c, conn = db_connect()
        print(id,username, password, email,
               mobile, address)
        j = c.execute("insert into register (id,username,password,email,mobile,address) values ('"+id+"','"+username +
                      "','"+password+"','"+email+"','"+mobile+"','"+address+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))
# -------------------------------------Login --------------------------------------
def user_loginact(username, password):
    try:
        c, conn = db_connect()
        j = c.execute("select * from register where username='" +
                      username+"' and password='"+password+"'")
        data = c.fetchall()
        print(data)
        for a in data:
           session['uname'] = a[0]
       
        c.fetchall()
        conn.close()
        return j
    except Exception as e:
        return(str(e))
#-------------------------------------Upload Image------------------------------------------
def user_upload(id,name, image):
    try:
        c, conn = db_connect()
        print(name,image)
        username = session['username']
        j = c.execute("insert into upload (id,name,image,username) values ('"+id+"','"+name+"','"+image +"','"+username +"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

#---------------------------------------View Images---------------------------------------
def user_viewimages(username):
    c, conn = db_connect()
    c.execute("select * from upload where  username='"+username +"'")
    result = c.fetchall()
    conn.close()
    print("result")
    return result

#------------------------------------Track----------------------------------------------------
def v_image(name):
    c, conn = db_connect()
    c.execute("Select * From images where name='"+name+"'")
    result = c.fetchall()
    conn.close()
    print("result")
    return result
# ----------------------------------------------Update Items------------------------------------------

def image_info(image_path):
    # folder = "C:/Users/Administrator/Desktop/UnderwaterImageEnhancement/NonPhysical/UCM"
    folder = "C:\\Users\\shiny\\Underwater Image Enhancement-web\\static\\img\\"
    starttime = datetime.datetime.now()
    path = folder + "/InputImages"
    files = os.listdir(path)
    files =  natsort.natsorted(files)

    for i in range(len(files)):
        file = files[i]
        filepath = path + "/" + file
        prefix = file.split('.')[0]
        if os.path.isfile(filepath):
            print('********    file   ********',file)
            # img = cv2.imread('InputImages/' + file)
            img = cv2.imread(folder + '/InputImages/' + file)
            # print('Number',Number)
            sceneRadiance = RGB_equalisation(img)
            sceneRadiance = stretching(sceneRadiance)
            # # cv2.imwrite(folder + '/OutputImages/' + Number + 'Stretched.jpg', sceneRadiance)
            sceneRadiance = HSVStretching(sceneRadiance)
            sceneRadiance = sceneRadianceRGB(sceneRadiance)
            cv2.imwrite(folder +prefix + 'UCM.jpg', sceneRadiance)

    endtime = datetime.datetime.now()
    time = endtime-starttime
    print('time',time)
    return "enhanced_image"    

if __name__ == "__main__":
    print(db_connect())
