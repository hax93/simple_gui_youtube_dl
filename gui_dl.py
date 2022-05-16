import getpass
import os
import subprocess
import sys
import threading
import time
import tkinter as tk
from datetime import timedelta
from tkinter import *
from tkinter import messagebox, ttk

import youtube_dl


def download_function(url1, format):
    #   download
    formats_vid_aud = {
        '1080':'bestvideo+bestaudio/best/1080',
        '720':'mp4/720',
        'mp3': 'bestaudio/mp3'
    }
    
    user = (getpass.getuser())
    video_url = url1
    video_info = youtube_dl.YoutubeDL().extract_info(url = video_url, 
                                                     download=False)
    filename = f"C:\\Users\\{user}\\Downloads\\{video_info['title']}"

    options={
        'progress_hooks': [callable_hook],
        'format':formats_vid_aud.get(format),
        'keepvideo':False,
        'outtmpl':filename,
        'source_address': '0.0.0.0', 
        'quiet': True,
    }

    if formats_vid_aud.get(format) == 'bestaudio/mp3':
        options['postprocessors'] = [{'key': 'FFmpegExtractAudio',

                'preferredcodec': 'm4a'}]
    else:
        pass
    
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
    time.sleep(2)
    tkk =  tk.Tk()
    tkk.geometry("150x150")
    dec = messagebox.askquestion(title='Download',
                            message="Download complete, open download folder?")   
    if dec == 'yes':
        win_dir = os.path.normpath(f'C:\\Users\\{user}\\Downloads')
        subprocess.Popen(f'explorer {win_dir}')
    else:
        pass

def check_url(url):
    # check URL before download
    ydl_options = {

        "forcetitle": {url},
        "simulate": {url},
        'quiet': True,
        'source_address': '0.0.0.0' 
    }
    try:
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            ydl.download([url])
    except:
        tkk =  tk.Tk()
        tkk.geometry("150x150")
        messagebox.showerror("ERROR","WRONG URL!")   

percent = [0]
time_down = ['0']

def callable_hook(response):
    # data download
    try:
        if response["status"] == "downloading":
            downloaded_percent = int(
                (response["downloaded_bytes"]*100)/response["total_bytes"])
            downloaded_time = (response['eta'])
            td = timedelta(seconds=downloaded_time)
            percent.append(downloaded_percent)
            time_down.append(str(td))

    except:
        "No data..."

class YouTubeDownload(ttk.Frame):
    formats_video = ['-', '1080', '720']
    formats_audio = ['-', 'mp3']
    
    def __init__(self, container):
        super().__init__(container)
        # field options
        options = {'padx': 1, 'pady': 10}
        self.user = (getpass.getuser())

        # LABEL TITLE
        self.title_label = Label(self, text='Video/Audio', 
                                 font="ariel 15 bold", bg="black", fg="white")
        self.title_label.grid(column=1, row=0, sticky=tk.S, **options)

        # LABEL URL
        self.url_label = Label(self, text="URL:", font="ariel 15 bold")
        self.url_label.place(x=5, y=54)
        
        # result label percent and eta
        self.result_label = Label(self, font="ariel 8 bold")
        self.result_label.grid(padx=0, pady=35, column=1, row=3, sticky=tk.S)
            
        # INPUT URL
        self.url = tk.StringVar()
        self.url_entry = Entry(self, textvariable=self.url)
        self.url_entry.grid(column=1, row=1, ipadx = 110, sticky=tk.SW, **options)
        self.url_entry.focus()
             
        # Option Menu VIDEO OR AUDIO  $VIDEO yt still no working
        self.check_vid = tk.StringVar()
        self.variable_video_set()
        self.check_boxes = OptionMenu(self, self.check_vid,
                                       *YouTubeDownload.formats_video,
                                       command=self.agreement_changed)
        self.check_boxes.grid(column=1, row=2, sticky=tk.E)
        
        # Audio
        self.check_aud = tk.StringVar()
        self.variable_audio_set()
        self.check_boxes = OptionMenu(self, self.check_aud,
                                       *YouTubeDownload.formats_audio,
                                       command=self.agreement_changed)
        self.check_boxes.grid(column=1, row=2, sticky=tk.S)
        
        # button download url
        self.button_submit = ttk.Button(self, text="Download")
        self.button_submit['command'] = lambda: [self.threading(self.comunicate),
                                                 self.threading(self.send_url),
                                                 self.threading(self.update()),
                                                 self.result_percent_eta()]
        self.button_submit.grid(column=1, row=2, sticky=tk.W)
       
        # button destroy program
        self.button_start = Button(self, text="Exit", font="ariel 15 bold",
                                   bg="black", fg="white")
        self.button_start['command'] = self.cancel_download
        self.button_start.grid(column=0, row=4, sticky=tk.S)
        
        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)
    
    def variable_video_set(self):
        self.check_vid.set(YouTubeDownload.formats_video[0]) 

    def variable_audio_set(self):
        self.check_aud.set(YouTubeDownload.formats_audio[0])
        
    def agreement_changed(self):
        # format for downloader_function
        if self.check_vid.get() == '-' and self.check_aud.get() == 'mp3':
            return self.check_aud.get()
        if (self.check_aud.get() == '-' and 
            self.check_vid.get() == '1080' or self.check_vid.get() == '720'):
            return self.check_vid.get()

    def result_percent_eta(self):
        # return time ETA
        timer = f'{time_down[-1]}s'
        self.result_label.config(text=timer)
        self.after(3000, self.result_percent_eta)
             
    def threading(self, work):
        # must for stability window
        t1=threading.Thread(target=work, daemon=True)
        t1.start()
        
    def comunicate(self):
        # check if URL real        
        check_url(self.url.get())
                
    def send_url(self):
        # download video/mp3
        download_function(self.url.get(), self.agreement_changed())
            
    def cancel_download(self):
        sys.exit()
        
    def update(self):
        # update progressbar value
        self.pb = ttk.Progressbar(length=240, orient='horizontal',
                                  mode='determinate', maximum=100)
        self.pb.place(x=120, y=180, bordermode="outside")
        self.pb['value'] = percent[-1]
        self.after(3000, self.update)   
    
class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('DownloaderDL')
        self.geometry('480x300')
        self.resizable(False, False)
                 
if __name__ == "__main__":
    app = App()
    YouTubeDownload(app)
    app.mainloop()
