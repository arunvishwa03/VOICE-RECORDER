#Import section
from tkinter import *
from tkinter import filedialog
import pygame
from mutagen.wave import WAVE
import tkinter.ttk as ttk
import glob
import os
import wave
import time
import threading
import tkinter as tk
import pyaudio
from PIL import ImageTk,Image
from tkinter import simpledialog

splash_root = Tk()
# Adjust size
splash_root.geometry("600x400+350+140")
#splash_root.geometry("200x200")
splash_root.overrideredirect(True)
cur_path = os.getcwd()
# Define image
bg = PhotoImage(file=cur_path+"/images/800 TP Mechanical.png")
# Create a canvas
my_canvas = Canvas(splash_root, width=600, height=400, highlightthickness=0)
my_canvas.pack(fill="both", expand=True)
# Set image in canvas
my_canvas.create_image(0,0, image=bg, anchor="nw")

def main():
    #destroy splash window
    splash_root.destroy()
    root =  Tk()
    root.title("VOICE RECORDER")
    root.geometry("607x573+375+45")
    root.iconbitmap()
    root.resizable(False,False)
    
    # Initialize Pygame
    pygame.mixer.init()
    cur_path = os.getcwd()
    
    # Create Function To Deal With Time
    def play_time():
            # Check to see if song is stopped
            if stopped:
                    return
            
            # Grab Current Song Time
            current_time = pygame.mixer.music.get_pos() / 1000
            # Convert Song Time To Time Format
            converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
            
            # Reconstruct song with directory structure stuff
            song = playlist_box.get(ACTIVE)
            val = None
            for evl in mylist:
                if song+"\.wav" in evl:
                    val = evl.replace("\.wav",".wav")
                    song = val
                elif song+'.wav' in evl:
                    val = evl
                    song = val

            # Find Current Song Length
            song_mut = WAVE(song)
            global song_length
            song_length = song_mut.info.length
            # Convert to time format
            converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
            
            # Check to see if song is over
            if int(song_slider.get()) == int(song_length):
                    stop()

            elif paused:
                    # Check to see if paused, if so - pass
                    pass
            
            else: 
                    # Move slider along 1 second at a time
                    next_time = int(song_slider.get()) + 1
                    # Output new time value to slider, and to length of song
                    song_slider.config(to=song_length, value=next_time)

                    # Convert Slider poition to time format
                    converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

                    # Output slider
                    status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')

            # Add Current Time To Status Bar
            if current_time > 0:
                    status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}  ')
            
            # Create Loop To Check the time every second
            status_bar.after(1000, play_time)

    # Create Play Function
    def play():
            # Set Stopped to False since a song is now playing
            global stopped
            stopped = False
            global mylist
            # Reconstruct song with directory structure stuff
            song = playlist_box.get(ACTIVE)            
            val = None
            for evl in mylist:
                if song+"\.wav" in evl:
                    val = evl.replace("\.wav",".wav")
                    song = val
                elif song+'.wav' in evl:
                    val = evl
                    song = val
                    
            #Load song with pygame mixer       
            pygame.mixer.music.load(song)
            #Play song with pygame mixer
            pygame.mixer.music.play(loops=0)

            # Get Song Time
            play_time()

    # Create Stopped Variable
    global stopped
    stopped = False 
    def stop():
            # Stop the song
            pygame.mixer.music.stop()
            # Clear Playlist Bar
            playlist_box.selection_clear(ACTIVE)

            status_bar.config(text='Time Elapsed: 00:00 of 00:00  ')

            # Set our slider to zero
            song_slider.config(value=0)

            # Set Stop Variable To True
            global stopped
            stopped = True


            
    # Create Function To Play The Next Song
    def next_song():
            # Reset Slider position and status bar
            status_bar.config(text='Time Elapsed: 00:00 of 00:00  ')
            song_slider.config(value=0)

            #Get current song number
            next_one = playlist_box.curselection()
            # Add One To The Current Song Number Tuple/list
            next_one = next_one[0] + 1

            # Grab the song title from the playlist
            song = playlist_box.get(next_one)
            # Add directory structure stuff to the song title
            song = cur_path+'\{}'.format(song)+'.wav'
            #Load song with pygame mixer
            pygame.mixer.music.load(song)
            #Play song with pygame mixer
            pygame.mixer.music.play(loops=0)

            # Clear Active Bar in Playlist
            playlist_box.selection_clear(0, END)

            # Move active bar to next song
            playlist_box.activate(next_one)

            # Set Active Bar To next song
            playlist_box.selection_set(next_one, last=None)

    # Create function to play previous song
    def previous_song():
            # Reset Slider position and status bar
            status_bar.config(text='Time Elapsed: 00:00 of 00:00  ')
            song_slider.config(value=0)

            #Get current song number
            next_one = playlist_box.curselection()
            # Add One To The Current Song Number Tuple/list
            next_one = next_one[0] - 1

            # Grab the song title from the playlist
            song = playlist_box.get(next_one)
            # Add directory structure stuff to the song title
            song = cur_path+'\{}'.format(song)+'.wav'
            #Load song with pygame mixer
            pygame.mixer.music.load(song)
            #Play song with pygame mixer
            pygame.mixer.music.play(loops=0)

            # Clear Active Bar in Playlist
            playlist_box.selection_clear(0, END)

            # Move active bar to next song
            playlist_box.activate(next_one)

            # Set Active Bar To next song
            playlist_box.selection_set(next_one, last=None)


    # Create Paused Variable
    global paused 
    paused = False

    # Create Pause Function
    def pause(is_paused):
            global paused
            paused = is_paused

            if paused:
                    #Unpause
                    pygame.mixer.music.unpause()
                    paused = False
            else:
                    #Pause
                    pygame.mixer.music.pause()
                    paused = True

    #Create Volume Function
    def volume(x):
            pygame.mixer.music.set_volume(volume_slider.get())

    # Create a Slide Function For Song Positioning
    def slide(x):
            # Reconstruct song with directory structure stuff
            song = playlist_box.get(ACTIVE)
            #song = cur_path+'\{}'.format(song)+'.wav'
            val = None
            for evl in mylist:
                if song+"\.wav" in evl:
                    val = evl.replace("\.wav",".wav")
                    song = val
                elif song+'.wav' in evl:
                    val = evl
                    song = val
            
            #Load song with pygame mixer
            pygame.mixer.music.load(song)
            #Play song with pygame mixer
            pygame.mixer.music.play(loops=0, start=song_slider.get())
    def Cloning(li1):
        li_copy = li1[:]
        return li_copy
    global out
    outname = []
    global fname
    fname = []
    def refresh():
            playlist_box.delete(0,END)
            mylist.append(retVal+"\\.wav")
            fname.append(retVal)
            out = os.path.basename(retVal)
            outname.append(out)
            mynewlist = Cloning(mylist)
            itlist = []
            num = 0
            n=int(len(fname))
            for y in mynewlist:
                for z in range(0,n):
                    if fname[z] in y:
                        y = y.replace(fname[z], outname[z])
                        itlist.append(y)
                        num += 1
            for h in range(num):
                mynewlist.pop()
            mynewlist.extend(itlist)
            for x in mynewlist:
                x = x.replace(cur_path+'\\',   "")
                x = x.replace("\\.wav", "")
                x = x.replace(".wav", "")
                
                playlist_box.insert(END,x)
            
    global recording
    recording = False
    def rec():
        global recording
        if recording:
            recording = False
            rec_button.config(image = rec_btn_img_on)       
            recstop_btn.config(image = recstop_btn_img_on)
            rec_button['command'] = rec
            recstop_btn['command'] = 0
            
        else:
            recording = True
            threading.Thread(target = record).start()
            rec_button.config(image = rec_btn_img_on)    
            recstop_btn.config(image = recstop_btn_img_on)
            rec_button['command'] = 0
            recstop_btn['command'] = rec
        
    def record():
        audio = pyaudio.PyAudio()
        stream = audio.open(format = pyaudio.paInt16, channels =2,rate = 48000, input = True, frames_per_buffer=1024)
        frames = []
        start = time.time()
        while recording:
            data = stream.read(1024)
            frames.append(data)
            passed = time.time() - start
            secs = passed % 60
            mins = passed //60
            hours = mins // 60
            t_label.config(text=f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}")
        t_label.config(text="00:00:00")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        #Create a new temporary "parent"
        newWin = Tk()
        #But make it invisible
        newWin.withdraw()
        #Now this works without throwing an exception:
        global retVal
        retVal=None
        retVal = filedialog.asksaveasfilename(initialdir=cur_path+'/',title="SAVE FILE AS",filetypes=(("WAV Files", "*.wav" ), ))
        #Destroy the temporary "parent"
        newWin.destroy()
        if retVal==None or retVal=='':
            return
        sound_file = wave.open(f""+retVal+".wav","wb")
        sound_file.setnchannels(2)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(48000)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()
        refresh()
    global dark
    dark = False
    def night():
        global dark
        if dark:
            dark=False
            main_frame['bg']='black'
            control_frame['bg']='black'
            status_bar['bg']='black'
            volume_frame['bg']='black'
            playlist_box['bg']='black'
            playlist_box['selectforeground']='black'
            toplabel['bg']='black'
            bottomlabel['bg']='black'
            style.configure("TScale", background="black")
            back_button['bg']='black'
            forward_button['bg']='black'
            play_button['bg']='black'
            pause_button['bg']='black'
            stop_button['bg']='black'
            rec_button['bg']='black'
            recstop_btn['bg']='black'
            t_label['bg']='black'
            night_btn['bg']='black'
            night_btn['image']=sun_img
        else:
            dark = True
            main_frame['bg']='white'
            control_frame['bg']='white'
            status_bar['bg']='white'
            volume_frame['bg']='white'
            playlist_box['bg']='white'
            playlist_box['selectforeground']='white'
            toplabel['bg']='white'
            bottomlabel['bg']='white'
            style.configure("TScale", background="white")
            back_button['bg']='white'
            forward_button['bg']='white'
            play_button['bg']='white'
            pause_button['bg']='white'
            stop_button['bg']='white'
            rec_button['bg']='white'
            recstop_btn['bg']='white'
            t_label['bg']='white'
            night_btn['bg']='white'
            night_btn['image']=night_img
            playlist_box['relief']='raised'
        # Create Function To Add One Song To Playlist
    def add_song():
            song = filedialog.askopenfilename(initialdir=cur_path+'/', title="Choose A Song", filetypes=(("WAV Files", "*.wav" ), ))
            # Strip out directory structure and .wav from song title
            #print(song)
            mylist.append(song)
            song = os.path.basename(song)
            #song = song.replace("C:/audio/", "")
            song = song.replace(".wav", "")
            # Add To End of Playlist
            playlist_box.insert(END, song)

    # Create Function To Add Many Songs to Playlist
    def add_many_songs():
            songs = filedialog.askopenfilenames(initialdir=cur_path+'/', title="Choose A Song", filetypes=(("WAV Files", "*.wav" ), ))
            
            # Loop thru song list and replace directory structure and WAV from song name
            for song in songs:
                    mylist.append(song)
                    song = os.path.basename(song)
                    # Strip out directory structure and .wav from song title
                    #song = song.replace("C:/audio/", "")
                    song = song.replace(".wav", "")
                    # Add To End of Playlist
                    playlist_box.insert(END, song)

    # Create Function To Delete One Song From Playlist
    def delete_song():
            # Delete Highlighted Song From Playlist
            remove = playlist_box.get(ANCHOR)
            for i in mylist:
                if remove in i:
                    mylist.remove(i)
            playlist_box.delete(ANCHOR)
            

    # Create Function To Delete All Songs From Playlist
    def delete_all_songs():
            # Delete ALL songs
            mylist.clear()
            playlist_box.delete(0, END)

            
    # Create main Frame
    main_frame = Frame(root, bg='black')
    main_frame.pack(fill = BOTH, expand = True)

    # Create Playlist Box
    playlist_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground='black',bd = 6,font=('ds-digital',14))
    playlist_box.grid(row=0,column=0,columnspan=1,padx=25,pady=25)
    global mylist
    mylist = glob.glob(cur_path+"\*.wav")
    for x in mylist:
        x = x.replace(cur_path+'\\',   "")
        x = x.replace(".wav", "")      
        playlist_box.insert(END,x)

    # Style slider using ttk widget
    style = ttk.Style()
    style.configure("TScale", background="black")
    
    # Create volume slider frame
    volume_frame = LabelFrame(main_frame, text="VOLUME",font=('ds-digital',14),bg="black",fg="green")
    volume_frame.grid(row=1,column=0,sticky=E,padx=25)

    # Create Volume Slider
    toplabel=Label(volume_frame,text="+",bg="black",fg="green")
    toplabel.pack()
    volume_slider = ttk.Scale(volume_frame, from_=1, to=0, orient=VERTICAL, length=110, value=1, command=volume,style="TScale")
    volume_slider.pack()
    bottomlabel=Label(volume_frame,text="-",bg="black",fg="green")
    bottomlabel.pack()
    
    # Create Song Slider
    song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=455, value=0, command=slide,style="TScale")
    song_slider.grid(row=2, column=0, pady=10, padx=25, sticky=W)	

    # Define Button Images For Controls
    back_btn_img = PhotoImage(file=cur_path+'/images/prev_img.png')
    forward_btn_img = PhotoImage(file=cur_path+'/images/next_img.png')
    play_btn_img = PhotoImage(file=cur_path+'/images/play_img.png')
    pause_btn_img = PhotoImage(file=cur_path+'/images/pause_img.png')
    stop_btn_img = PhotoImage(file=cur_path+'/images/stop_img.png')
    rec_btn_img = PhotoImage(file=cur_path+'/images/speaking_off.png')         
    rec_btn_img_on = PhotoImage(file=cur_path+'/images/speaking_on.png')
    recstop_btn_img = PhotoImage(file=cur_path+'/images/rec_stop_off.png')    
    recstop_btn_img_on = PhotoImage(file=cur_path+'/images/rec_stop_on.png')
    night_img = PhotoImage(file=cur_path+'/images/moon_brightness.png')
    sun_img = PhotoImage(file=cur_path+'/images/sun_brightness.png')
    
    # Create Button Frame
    control_frame = tk.Frame(main_frame,bg="black")
    control_frame.grid(row=1,column=0,sticky=W,padx=25)

    # Create Play/Stop etc Buttons
    back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song,bg="black")
    forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song,bg="black")
    play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play,bg="black")
    pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused),bg="black")
    stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop,bg="black")
    rec_button = Button(control_frame,image=rec_btn_img_on, borderwidth=0, command=rec,bg="black")       
    recstop_btn = Button(control_frame,image=recstop_btn_img_on, borderwidth=0, command=0,bg="black")
    
    back_button.grid(row=0, column=0, padx=10)
    forward_button.grid(row=0, column=1, padx=10)
    play_button.grid(row=0, column=2, padx=10)
    pause_button.grid(row=0, column=3, padx=10)
    stop_button.grid(row=0, column=4, padx=10)
    rec_button.grid(row=1, column=1, padx=10)       
    recstop_btn.grid(row = 1,column=3,padx =10)
    
    #timer
    t_label = Label(control_frame,text="00:00:00",font = ("ds-digital",20,"bold"),bg="black",fg="green")
    t_label.grid(row=2,column=0,rowspan=2,columnspan=6)
    
    # Dark mode
    night_btn = Button(main_frame,image=sun_img,borderwidth=0,command=night,bg="black")
    night_btn.grid(row=2,column=0,sticky=E,pady=25,padx=25)

    # Create Status Bar
    status_bar = Label(main_frame,text='Time Elapsed: 00:00 of 00:00  ', bd=1,bg="black",fg="green")
    status_bar.grid(row=2,column=0,sticky=SW,pady=25,padx=25)

    # Create Main Menu
    my_menu = Menu(root)
    root.config(menu=my_menu)

    # Create Add Song Menu Dropdows
    add_song_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
    # Add One Song To Playlist
    add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
    # Add Many Songs to Playlist
    add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

    # Create Delete Song Menu Dropdowns
    remove_song_menu = Menu(my_menu, tearoff=0)
    my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
    remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
    remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

    mainloop()
    
splash_root.after(5000,main)#1000 - 1SEC
# Execute tkinter
mainloop()
