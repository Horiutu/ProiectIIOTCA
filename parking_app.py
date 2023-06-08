# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 23:02:47 2023

@author: Timotei
"""

# Import the required libraries
import tkinter as tk
import pyrebase
import matplotlib.pyplot as plt


# connecting to the Firebase databae
print('Connecting to firebase database')

config = {
    'apiKey': 'AIzaSyAbXlaAYcsovACZIAygJEo9nGEue3d4Hyw',
    'authDomain': 'parking-iiotca.firebase.com',
    'databaseURL': 'https://parking-iiotca-default-rtdb.firebaseio.com/',
    'storageBucket': 'parking-iiotca.appspot.com'
}

firebase = pyrebase.initialize_app(config)




# Create an instance of tkinter frame or window
win = tk.Tk(className='Parking System')

# Set the size of the tkinter window
win.geometry("700x350")

# Define a function update the label text
def on_click():
    db = firebase.database()
    data = db.get()
    print(data.val())
    if 'Free parking spaces' in data.val():
        label["text"] = 'Free parking spaces: ' + str(data.val()['Free parking spaces'])
    else:
        label['text'] = 'Free parking spaces: None'
        
# Define a function update the label text
def on_click1():
    db = firebase.database()
    data = db.get()
    
    divider = data.val()['Frames on']
    data = data.val()['Frames free']
    
    for name in list(data.keys()):
        data[name] = data[name]/divider * 100
    
    names = list(data.keys())
    values = list(data.values())

    plt.bar(range(len(data)), values, tick_label=names)
    plt.show()
    



# Title
title = tk.Label(win, text="Parking System",
font=('Calibri 20 bold'))
title.pack(pady=20)

# Create a label widget
label = tk.Label(win, text="Click the button bellow to see which parking slots are free",
font=('Calibri 15'))
label.pack(pady=20)

# Create a button to update the label widget
b = tk.Button(win, text="Get parking slots", command=on_click)
b.pack(pady=20)

# Create a button to update the label widget
b1 = tk.Button(win, text="Get parking statistics", command=on_click1)
b1.pack(pady=20)


win.mainloop()