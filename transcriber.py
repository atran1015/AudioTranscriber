#!/usr/bin/env python3

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import speech_recognition as sr
import pydub
import os, shutil
from pydub import AudioSegment
from pydub.silence import split_on_silence
import time
import threading

#from ffmpeg_progress_yield import FfmpegProgress
#from tkinterdnd2 import DND_FILES, TkinterDnD
#import tkinterdnd2

# setting up the window of app
window = tk.Tk()
window.geometry("900x700")
window.title("Audio Transcriber")

def get_large_audio_transcription(path, lang):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    r = sr.Recognizer()
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language=lang)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                #text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
                #print(whole_text)
    
    longtext = "texts.txt"

    # for prediction in text:
    #     print(" " + prediction["text"] + " (" + str(prediction["confidence"]*100) + "%)")

    with open(longtext, "w", encoding="utf-8") as f:
        f.write(whole_text)
    # return the text for all chunks detected
    return whole_text


def ToText(lang):
    """ Convert .wav audio to texts and provide text output """
    filenamefullpath = uploadfilelabel['text']
    filetotext = os.path.split(filenamefullpath)[1]
    r = sr.Recognizer()
    with sr.AudioFile(filetotext) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language=lang)
        # print(text)
    
    outputfile = "texts.txt"
    with open(outputfile, "w", encoding="utf-8") as f:
         f.write(text)

def PopUpWindow():
    """ Show popup window for texts """
    popup = tk.Toplevel()
    popup.wm_title("Text retrieved")
   
    textbox = Text(popup, height = 13, width = 54)
    
    if os.path.isfile('./texts.txt'):
        with open("texts.txt", "r", encoding="utf-8") as f:
            retrievedtext = f.read()
    else:
        retrievedtext = "Text file does not exist."
    
    textbox.pack()
    
    # insert texts
    textbox.configure(state='normal')
    textbox.insert(tk.END, retrievedtext)
    textbox.configure(state='disabled')
    
    b = ttk.Button(popup, text="Close", command=popup.destroy)
    b.grid(row=1, column=0)
    


def UploadAction(event=None):
    """ Upload file to prepare for .wav to text conversion """
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    uploadfilelabel['text'] = filename

def UploadConvertAction(event=None):
    """ Upload file to prepare for .mp4 to .wav audio conversion """
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    uploadconvertlabel['text'] = filename

def UploadProgress():
    """ Upload Progress Bar settings """
    for i in range(101):
        uploadProgressBar['value'] = i
        i += .0125

def ConvertAction(event=None):
    try:
            """ Uses ffmpeg to convert .mp4 to .wav audio """
            # get file name
            filetoconvert = uploadconvertlabel['text']
            convertedfile = os.path.split(filetoconvert)[1]

            # command to convert
            command2mp3 = "ffmpeg -y -i " + convertedfile + " convertedmp3.mp3"
            command2wav = "ffmpeg -y -i convertedmp3.mp3 convertedwav.wav"

            # calling system to convert
            os.system(command2mp3)
            os.system(command2wav)

            # for upload progress bar
            threading.Thread(target=UploadProgress).start()
            uploadsuccesslabel['text'] = "Success!"
            uploadsuccesslabel.config(background="green") 
            if os.system(command2mp3)!=0 or os.system(command2wav) != 0:
                raise UserWarning
    except UserWarning:
        uploadsuccesslabel['text'] = "Error occurred"
        uploadsuccesslabel.config(background="red")
    

def ClearAudio():
    curr_path = os.getcwd()
    path = curr_path + '/audio-chunks'
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    clearaudiolabel['text'] = "Success!"
    

def Progress():
    """ Progress Bar settings """
    for i in range(101):
        progressBar['value'] = i
        i += .0125
        #window.update()


# testing the long func
def GetText():
    """" Get Text button functionality which includes error checking and selecting language
    to prepare for conversion """
    progressBar['value'] = 0
    
    #start_time = time.time()
    #print("this is start time: ", start_time)     
    #print('This is the value from the option menu:',variable.get())
    #print('This is the file:',uploadfilelabel['text'])
    default_option = "Select a language"
    default_file = "Please choose a file"
    if default_option == variable.get() and default_file == (uploadfilelabel['text']):
        confirmationlabel['text'] = "Please select a language and upload a file"
        confirmationlabel.config(background="red")
    elif default_option == variable.get():
        confirmationlabel['text'] = "Please select a language"
        confirmationlabel.config(background="red")
    elif default_file == (uploadfilelabel['text']) or (uploadfilelabel['text']) =="" :
         confirmationlabel['text'] = "Please upload a file"
         confirmationlabel.config(background="red")
    else:
        file = uploadfilelabel['text']
        filename = os.path.split(file)[1]
        if filename.endswith('.wav'):
            threading.Thread(target=Progress).start()
            confirmationlabel['text'] = "Success!"
            confirmationlabel.config(background="green", font='Helvetica 18 bold')  
        else:
            confirmationlabel['text'] = "Please upload the correct file extension (.wav)"
            confirmationlabel.config(background="red")
        
    filenamefullpath = uploadfilelabel['text']
    if variable.get() == "Mandarin":
        lang = 'zh-CN'
        get_large_audio_transcription(filenamefullpath, lang)
    elif variable.get() == "French":
        lang = 'fr-FR'
        get_large_audio_transcription(filenamefullpath, lang)
    elif variable.get() == "Spanish":
        lang = 'es-ES'
        get_large_audio_transcription(filenamefullpath, lang)
    elif variable.get() == "Japanese":
        lang = 'ja'
        get_large_audio_transcription(filenamefullpath, lang)
    else:
        lang = 'en-US'
        confirmationlabel['text'] = "Please select a language"
        confirmationlabel.config(background="red")

    

# main left frame
frame = tk.Frame(master=window, width=800, height=600, background="#A7C7E7")
frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# welcome label
welcomelabel = tk.Label(master=frame, text="Welcome!", font='Helvetica 18 bold', bg="#A7C7E7")
welcomelabel.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
welcomelabel.pack(pady=15)

# instruction frame
instructionframe = tk.Frame(master=frame, width=500, height=200, background="#D3D3D3")
instructionframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
instructionframe.pack()

# text widget
textWidget = Text(instructionframe, height = 13, width = 54)
 
# create instruction label
instructionlabel = Label(instructionframe, text = "Follow the instructions below to start.")
instructionlabel.config(font =("Courier", 14))
 
# instruction texts
instructions = """1. Select a language

2. Upload your .wav file that is less than 1 minute

3. Click the "Get Text" button

4. A text file should be generated from the same path where the file is and a "success" confirmation should appear

5. You now have the text version of your audio, enjoy!"""
 
# create close button
closeInstructionButton = Button(instructionframe, text = "Close instructions",
            command = instructionframe.destroy)
 
instructionlabel.pack(fill=X)
textWidget.pack()
closeInstructionButton.pack()

 
# insert the instructions
textWidget.configure(state='normal')
textWidget.insert(tk.END, instructions)
textWidget.configure(state='disabled')


# frame for converting
convertframe = tk.Frame(master=frame, width=500, height=200, bg="#D3D3D3")
convertframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
convertframe.pack(pady=40)

# convert label
convertlabel = Label(convertframe, text = "Need help with converting your .mp4 to .wav?")
convertlabel.config(font =("Courier", 14))

# upload convert button
uploadconvertbutton = Button(convertframe, text='Upload', command=UploadConvertAction)

# showing label and button
convertlabel.pack(fill=X)
uploadconvertbutton.pack()

# upload convert label
uploadconvertlabel = Label(convertframe, text='Please choose a file', bg="#D3D3D3")
uploadconvertlabel.pack(pady=10)

# conversion progress bar
s = ttk.Style()
s.theme_use('alt')
s.configure("green.Horizontal.TProgressbar", background='green')
uploadProgressBar = ttk.Progressbar(convertframe,orient = HORIZONTAL,
        length = 200, mode = 'determinate', style='green.Horizontal.TProgressbar')      
uploadProgressBar.pack(pady=10) 

# convert button
convertbutton = Button(convertframe, text='Convert', command=ConvertAction)
convertbutton.pack()

# upload success label
uploadsuccesslabel = Label(convertframe, text='Waiting...', bg="#D3D3D3")
uploadsuccesslabel.pack(pady=10)




# ------------- right side of app --------------------
# first item - dropdown
OPTIONS = [
    "Mandarin",
    "French",
    "Spanish",
    "Japanese"
]
variable = StringVar(window)
variable.set("Select a language") # default value
w = OptionMenu(window, variable, *OPTIONS)
w.pack(pady=10)


# second item - upload file
button = tk.Button(window, text='Open', command=UploadAction)
button.pack()
uploadfilelabel = tk.Label(text='Please choose a file')
uploadfilelabel.pack(pady=10)

# third item - text file progress
progressBar = ttk.Progressbar(window,orient = HORIZONTAL,
        length = 200, mode = 'determinate', style='green.Horizontal.TProgressbar')      
progressBar.pack(pady=10) 

# fourth item - grab text/run algo
gettextbutton = Button(window, text='Get Text',command=GetText)
gettextbutton.pack()
confirmationlabel = tk.Label(text='Waiting...')
confirmationlabel.pack()

# fifth item - show popup button
showtextbutton = Button(window, text='Show Text', command=PopUpWindow)
showtextbutton.pack(pady=10)


# sixth item - clear audio chunks
clearaudiobutton = Button(window, text='Clear Audio Chunks', command=ClearAudio)
#clearaudiobutton.pack(pady=10, anchor=SE)
#clearaudiobutton.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)
clearaudiobutton.pack(side=BOTTOM)
clearaudiolabel = Label(text='Waiting...')
#clearaudiolabel.place(rely=0.5, relx=1.0, x=0, y=0, anchor=SE)
clearaudiolabel.pack(side=BOTTOM)
window.mainloop()
