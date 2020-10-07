import os  # this is imported so as to show the main filename_path of the music playing
from tkinter import *  # Importing everything from tkinter
from tkinter import filedialog  # Importing module class
import tkinter.messagebox  # same
from pygame import mixer
from mutagen.mp3 import MP3
import time
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk

root = tk.ThemedTk()  # This Tk func creates a window and stores it in variable root
root.get_themes()
root.set_theme("arc")
statusbar = ttk.Label(root, text="Welcome to Rhythm", relief=SUNKEN,anchor=W,font ='verdana 10 bold')  # relief is used to put the text in a box and anchor for direction of text
statusbar.pack(side=BOTTOM,fill=X)  # to put statusbar at the bottom n fill used to expand the box of msg to the X axis

root.title("Rhythm")  # Giving title to the window
root.iconbitmap(r'Rhythm.ico')  # r means raw string and we put the location inside Rhythm
menubar = Menu(root)  # to create a empty menu bar
root.config(menu=menubar)  # this function should remain on top and to make it to hold the submenus
submenu = Menu(menubar, tearoff=0)  # to create a submenus


def aboutus():
    tkinter.messagebox.showinfo('Welcome people', 'This is our music player.Hope you enjoy!')  # funct for msgbox of about us

playlist = []

# playlist- contains the filename path and filename
#laylistbox- contains just the filename
#fullpath and filename is required to play muisc in play_music load function


def browsesong():  # function to browse song to play
    global filename_path  # made this variable global to use it anywhere
    filename_path = filedialog.askopenfilename()  # to make the New song submenu work and find for songs
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename= os.path.basename(filename)
    index= 0
    Playlistbox.insert(index, filename)
    playlist.insert(index,filename_path)
    index += 1


menubar.add_cascade(label="File", menu=submenu)  # to add a submenu now and cascade means dropdown bar
submenu.add_command(label="New Song", command=browsesong)  # to make a option inside submenu
submenu.add_command(label="New")
submenu.add_command(label="Exit", command=root.destroy)  # second parameter is to exit the app

submenu = Menu(menubar, tearoff=0)  # to create a submenus
menubar.add_cascade(label="Info", menu=submenu)  # to add a submenu now and cascade means dropdown bar
submenu.add_command(label="About us", command=aboutus)  # to make a option inside submenu

mixer.init()  # initializing the mixer class

leftframe= Frame (root)
leftframe.pack(side= LEFT, padx= 30)

Playlistbox= Listbox(leftframe)
Playlistbox.pack()

addbtn= ttk.Button(leftframe, text= "+ Add", command= browsesong)
addbtn.pack(side= LEFT)

def del_song():
    selected_song = Playlistbox.curselection()  # curselection is use to play the selected song
    selected_song = int(selected_song[0])
    Playlistbox.delete(selected_song)
    playlist.pop(selected_song)

delbtn= ttk.Button(leftframe, text= "- Del",command =del_song)
delbtn.pack(side= LEFT)

rightframe= Frame (root)
rightframe.pack(pady=10)

topframe= Frame (rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text='Total Length :- 00:00',font = 'Arial 10 bold')  # giving parameters for label and label is a widget
lengthlabel.pack(pady=5)  # we cannot add widgets to window without packing them

currenttimelabel = ttk.Label(topframe, text='Current time : --:--',relief=GROOVE,font = 'Arial 10 bold')  # giving parameters for label and label is a widget
currenttimelabel.pack(pady=5)  # we cannot add widgets to window without packing them


def showdet(play_song):  # fuct. for showing the length of the song


    filedata= os.path.splitext(play_song)# splits the name and extension in a list
    if filedata[1] == '.mp3':
         audio = MP3(play_song)
         totallength = audio.info.length
    else:
        a = mixer.Sound(play_song)  # to load the music here
        totallength = a.get_length()  # to get the total length of the music

    mins,secs = divmod(totallength,60)#div takes total length and divide it by 60 and mod takes the mod out of div by 60
    mins= round(mins)#to roundof
    secs= round(secs)
    timeformat = '{:02d} : {:02d}'.format(mins,secs)#for formatting the time showen
    lengthlabel['text']= "Total Time" + ' - ' +timeformat#changing the label declared above
    t1 = threading.Thread(target=start_count,args=(totallength,))
    t1.start()

def start_count(t):
    global paused
    x =0
    while x<=t and mixer.music.get_busy():#loop to make change in time everysec and get busy to return false when we stop the music and music stops
        if paused:
            continue
        else:
            mins, secs = divmod(x, 60)  # just changed the variable
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d} : {:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat  # changing the label same as above
            time.sleep(1)  # to delay the time by 1 sec
            x = x + 1  # increase by 1

def playmusic():  # we made a func name playmusic
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused=FALSE  # to make the variable again at false
    else:
        try:
            stopmusic()
            time.sleep(1)
            selected_song = Playlistbox.curselection() #curselection is use to play the selected song
            selected_song= int(selected_song[0])
            play_it= playlist[selected_song]
            mixer.music.load(play_it)  # to load the music inside the program
            mixer.music.play()  # to play the music
            statusbar['text'] = "Playing Music" + '-' + os.path.basename(play_it)  # show main filename_path of the musicplaying
            showdet(play_it)
        except:
            tkinter.messagebox.showerror('Error', 'Open a file first')  # if you press play without specifing a song

def stopmusic():  # a function to stop the music
    mixer.music.stop()  # stop function
    statusbar['text'] = "Music Stopped"

paused= FALSE

def pausemusic():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def rewindmusic():
    playmusic()
    statusbar['text'] = "Music Rewind"

muted = FALSE #before clicking the mude button

def mutemusic():
    global muted
    if muted:# when we click the mute button again to unmute
        mixer.music.set_volume(0.7)
        volbtn.configure(image=volphoto)
        scale.set(70)
        muted=FALSE
        statusbar['text']= "Music Unmuted"
    else:#to mute the music
        mixer.music.set_volume(0)
        volbtn.configure(image=mutephoto)
        scale.set(0)
        muted=TRUE
        statusbar['text']= "Music Muted"


def setvol (val):  # func for volume control and val argument is used by python to send the value from the command function
    volume = float(val) / 100  # to make it in a value between 0 to 1
    mixer.music.set_volume(volume)


# Set_volume takes value only from 0 to 1
middleframe = Frame(rightframe,bg = '#1D94D4')
middleframe.pack(pady=30, padx=30)

playphoto = PhotoImage(file='Play.png')  # To add img we use photoimage func
playbtn = ttk.Button(middleframe, image=playphoto, command=playmusic)  # to make the play image work as button
playbtn.grid(row=0, column=1, padx=10,pady= 10)  # again packing it to display the widget

stopphoto = PhotoImage(file='stopp.png')  # to add img in this function
stopbtn = ttk.Button(middleframe, image=stopphoto, command=stopmusic)  # to make the stop button work as a button
stopbtn.grid(row=0, column=2, padx=10,pady=10)  # packing widget so it comes below the last widget

pausephoto = PhotoImage(file='pause.png')  # to add img in this function
pausebtn = ttk.Button(middleframe, image=pausephoto, command=pausemusic)  # to make the pause button work as a button
pausebtn.grid(row=0, column=3, padx=10,pady=10)  # packing widget so it comes below the last widget

bottomframe = Frame(rightframe)
bottomframe.pack()


rewindphoto = PhotoImage(file='rewind.png')  # to add img in this function
rewindbtn = ttk.Button(bottomframe, image=rewindphoto, command=rewindmusic)  # to make the pause button work as a button
rewindbtn.grid(row=0, column=0)  # packing widget so it comes below the last widget
mutephoto= PhotoImage(file='mute.png')
volphoto= PhotoImage(file='volume.png')
volbtn= ttk.Button(bottomframe,image=volphoto,command= mutemusic)
volbtn.grid(row=0,column=1,padx=10)


scale = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=setvol)  # neeche vala same
scale.set(70)  # set display volume to the no.stated
mixer.music.set_volume(0.7)  # for actually setting the volume to 70
scale.grid(row=0, column=2, pady=15, padx=30)



def on_closing():
    stopmusic()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()  # Using this to engage our window in a loop and every frame of window gets refreshed
