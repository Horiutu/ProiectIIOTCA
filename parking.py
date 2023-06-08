# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 23:29:55 2023

@author: Timotei
"""

import cv2
import easyocr
import keyboard
import pyrebase
import re


print('Connecting to firebase database')

config = {
    'apiKey': 'AIzaSyAbXlaAYcsovACZIAygJEo9nGEue3d4Hyw',
    'authDomain': 'parking-iiotca.firebase.com',
    'databaseURL': 'https://parking-iiotca-default-rtdb.firebaseio.com/',
    'storageBucket': 'parking-iiotca.appspot.com'
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

# initialize camera
print('Initializing camera')
camera=cv2.VideoCapture(1)

# initialize text-detector
print('Initializing cv algorithms')
reader = easyocr.Reader(['en'], gpu = False)

park_score = {}
frames_running = 0

while True:
    # get image from camera
    _,image=camera.read()
    cv2.imshow('Text detection', image)
    
    frames_running = frames_running + 1
    
    # process image
    if cv2.waitKey(2):
        # detect text
        results = reader.readtext(image)
        
        # get parking codes
        park_codes = [x[1] for x in results]
        
        # divide mixed parking codes
        park_codes_corr = []
        for code in park_codes:
            code = code.replace(' ','')
            code = code.replace('S','5')
            codes = re.split(r'[|I() l\\/]', code)
            park_codes_corr = park_codes_corr + codes
            
        # keep only valid parking codes
        park_codes_checked = []
        for code in park_codes_corr:
            if len(code) == 2 and code[0].isalpha() and code[1].isdigit():
                park_codes_checked.append(code)
                
        print(park_codes)
        print(park_codes_corr)
        print(park_codes_checked)
        
        # add free score to parking slot
        for code in park_codes_checked:
            if code not in park_score.keys():
                park_score[code] = 1
            else:
                park_score[code] = park_score[code] + 1
        
        # update firebase database
        data = {
            'Free parking spaces' : park_codes_checked,
            'Frames free' : park_score,
            'Frames on' : frames_running
        }
        
        db.update(data)
        print('Sent to Firebase')
        
    # exit condition
    if keyboard.is_pressed('a'):
        break
        
# turn off camera
camera.release()
cv2.destroyAllWindows()






### se repeta la un interval de timp
# face poza
# scoate cuvintele
# cautam codurile de parcare
# le transformam intr-o lista
# o trimitem pe server