from tkinter import *
from pygame import mixer   #to adjust the volume,play and stop functionality
import tkinter.messagebox   #To create the message box
from tkinter import filedialog  #To open the file
import os  # To get only the name of the basefile
from mutagen.mp3 import MP3  #For Calculating the length of mp3 files 
import time
import threading

#Window Configuration

root = Tk()
root.title("Melody")
root.iconbitmap(r"images/song.ico")

#Mixer Configuration
mixer.init()

status_bar = Label(root,text="Welcome to Melody",relief="sunken",anchor=W)
status_bar.pack(side=BOTTOM,fill=BOTH)

#Functions

def start_count(t):
    global paused
    x=0
    while x<=t and mixer.music.get_busy():#get_busy() function is used to get false value after
        if paused:
            continue
        else:
            mins,secs = divmod(x,60)        #after pressing the pause button
            mins = round(mins)
            secs = round(secs)
            timeformat = "{:02d}:{:02d}".format(mins,secs)
            currenttimelabel["text"] = "Current Time"+"--"+timeformat
            time.sleep(1)
            x+=1
def show_detailes(play_song):
    try:
        #filelabel['text'] = "Song Playing"+"--"+os.path.basename(filename)
        file_data = os.path.splitext(play_song)
        if file_data[1] == '.mp3':
            audio = MP3(play_song)
            total_length = audio.info.length
            
            mins,secs = divmod(total_length,60)
            mins = round(mins)
            secs = round(secs)
            timeformat = "{:02d}:{:02d}".format(mins,secs-1)
            
            
            lengthlabel["text"] = "Total Length" +"--"+timeformat
            t1=threading.Thread(target=start_count,args=(total_length,))
            t1.start()
    except Exception as e:
        tkinter.messagebox.showerror("File Missing","Please select the file and try again.")
        print(e)

def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        status_bar['text'] = "Song Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            status_bar['text'] = "Song Playing"+"--"+os.path.basename(play_it)
            show_detailes(play_it)
        except:
            tkinter.messagebox.showerror("File Not Found","Melody could not found the file.Please check again")
       
        
       
def stop_music():
    mixer.music.stop()
    status_bar['text'] = "Song Stopped"

paused = FALSE
def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    status_bar['text'] = "Song Paused"

def rewind_music():
    play_music()
    status_bar['text'] = "Song Rewinded"


mute =FALSE
def mute_music():
    global mute
    if mute:
        volume_btn.configure(image=btn_photo4)
        mixer.music.set_volume(0.7)
        scale.set(70)
        mute = FALSE
    else:
        volume_btn.configure(image=btn_photo5)
        mixer.music.set_volume(0)
        scale.set(0)
        mute = TRUE
        
def scale_music(value):
    volume = int(value)/100
    mixer.music.set_volume(volume)

def about_us():
    tkinter.messagebox.showinfo("About Melody","This Music Player Application is built using Python Tkinter By Shravankumar")

def browse_file():
    global filename
    filename = filedialog.askopenfilename()
    add_playlist(filename)
playlist = []
def add_playlist(f):
    index = 0
    f = os.path.basename(f) 
    playlistbox.insert(index,f)
    playlist.insert(index,filename)
    print(playlist)
    index+=1
def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)
    
#Adding Menubar and Submenues
menubar = Menu(root)
root.config(menu=menubar)

submenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=submenu)
submenu.add_command(label="Open",command=browse_file)
submenu.add_command(label="Exit",command=root.destroy)

submenu1 = Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help",menu=submenu1)
submenu1.add_command(label="About us",command=about_us)
    
#Adding the Label
leftframe = Frame(root)
leftframe.pack(side=LEFT,padx=20)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = Label(topframe,text="Total length - 00:00")
lengthlabel.pack(pady=10)

playlistbox =Listbox(leftframe)
playlistbox.pack()

btn1 =Button(leftframe,text="+ ADD",command=browse_file)
btn1.pack(side=LEFT)

btn2 = Button(leftframe,text="- DELETE", command=del_song)
btn2.pack()




currenttimelabel =Label(topframe,text="Current Time: --:--",relief=GROOVE)
currenttimelabel.pack(pady=10)
#Creating Frames
middleframe = Frame(rightframe)
middleframe.pack(pady=30,padx=30)

#Adding Photo
btn_photo = PhotoImage(file="images/play.png")
play_btn = Button(middleframe,image=btn_photo,command=play_music)
play_btn.grid(row=0,column=0,padx=10)

btn_photo1 = PhotoImage(file="images/stop.png")
stop_btn = Button(middleframe,image=btn_photo1,command=stop_music)
stop_btn.grid(row=0,column=1,padx=10)

btn_photo2 = PhotoImage(file="images/pause.png")
pause_btn = Button(middleframe,image=btn_photo2,command=pause_music)
pause_btn.grid(row=0,column=2,padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack(pady=30,padx=30)

btn_photo3 = PhotoImage(file="images/rewind.png")
rewind_btn = Button(bottomframe,image=btn_photo3,command=rewind_music)
rewind_btn.grid(row=0,column=0,padx=10)

btn_photo4 = PhotoImage(file="images/speaker.png")
btn_photo5 = PhotoImage(file="images/mute.png")
volume_btn = Button(bottomframe,image=btn_photo4,command=mute_music)
volume_btn.grid(row=0,column=1)


scale = Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL,command=scale_music)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0,column=2,padx=10,pady=10)



def on_clicking():
    stop_music()
    tkinter.messagebox.showinfo("Thank You","Thank you for using this application.")
    root.destroy()
root.protocol("WM_DELETE_WINDOW",on_clicking)
root.mainloop()

