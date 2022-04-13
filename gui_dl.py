import getpass
import subprocess
import os
import sys
import time
import youtube_dl
import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from datetime import timedelta

def download_function(url1, format):
    user = (getpass.getuser())
    video_url = url1
    video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
    filename = f"C:\\Users\\{user}\\Downloads\\{video_info['title']}.mp4"

    options={
        'progress_hooks': [callable_hook],
        'format':format,
        'keepvideo':False,
        'outtmpl':filename,
        'source_address': '0.0.0.0' 
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])
    time.sleep(2)
    tkk =  tk.Tk()
    tkk.geometry("150x150")
    messagebox.showinfo("Info","Download complete")   

# check URL before download
def check_url(url):
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
    # dane dotyczące pobierania
    try:
        if response["status"] == "downloading":
            downloaded_percent = int((response["downloaded_bytes"]*100)/response["total_bytes"])
            downloaded_time = (response['eta']) #time sec
            td = timedelta(seconds=downloaded_time)
            percent.append(downloaded_percent)
            time_down.append(str(td))

    except:
        "No data..."

class YouTubeDownload(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        # field options
        options = {'padx': 1, 'pady': 10}
        self.user = (getpass.getuser())

        # LABEL TITLE
        self.title_label = Label(self, text='Video/Audio', font="ariel 15 bold", bg="black", fg="white")
        self.title_label.grid(column=1, row=0, sticky=tk.S, **options)

        # LABEL URL
        self.url_label = Label(self, text="URL:", font="ariel 15 bold")
        self.url_label.place(x=5, y=54)
        
        # result label percent and eta
        self.result_label = Label(self, font="ariel 8 bold")
        self.result_label.grid(padx=0, pady=41, column=1, row=3, sticky=tk.S)
            
        # INPUT URL
        self.url = tk.StringVar()
        self.url_entry = Entry(self, textvariable=self.url)
        self.url_entry.grid(column=1, row=1, ipadx = 110, sticky=tk.SW, **options)
        self.url_entry.focus()
             
        # CHECK BOX VIDEO OR AUDIO  $VIDEO yt still no working
        self.check = tk.StringVar()
        self.check_boxes = Checkbutton(self, text='Video', command=self.agreement_changed, variable=self.check, onvalue='bestvideo/bestaudio/best')
        self.check_boxes.grid(column=1, row=2, sticky=tk.E)
        # Audio
        self.check_boxes = Checkbutton(self, text='Audio', command=self.agreement_changed, variable=self.check, onvalue='bestaudio/best')
        self.check_boxes.grid(column=1, row=2, sticky=tk.S)
        
        # button download url
        self.button_submit = ttk.Button(self, text="Download")
        self.button_submit['command'] = lambda: [self.threading(self.comunicate), self.threading(self.send_url), self.threading(self.update()), self.result_percent_eta()]
        self.button_submit.grid(column=1, row=2, sticky=tk.W)
       
        # button destroy program
        self.button_start = Button(self, text="Cancel", font="ariel 15 bold", bg="black", fg="white")
        self.button_start['command'] = self.cancel_download
        self.button_start.grid(column=0, row=4, sticky=tk.S)
        
        # button path download
        self.button_path = Button(self, text='File Download')
        self.button_path['command'] = self.open_path
        self.button_path.grid(column=0, row=3, sticky=tk.S)
        
        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)
        
    def result_percent_eta(self):
        # return time ETA
        timer = f'{time_down[-1]}s'
        self.result_label.config(text=timer)
        self.after(3000, self.result_percent_eta)
             
    def agreement_changed(self):
        # format for downloader_function
        return self.check.get()
   
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
            # progress bar
        self.pb = ttk.Progressbar(length=240, orient='horizontal', mode='determinate', maximum=100)
        self.pb.place(x=120, y=180, bordermode="outside")
        self.pb['value'] = percent[-1]
        self.after(3000, self.update) # run itself again after 1000 ms    
    
    def open_path(self):
        win_dir = os.path.normpath(f'C:\\Users\\{self.user}\\Downloads')
        subprocess.Popen(f'explorer {win_dir}')
                   
class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('DownloaderDL')
        self.geometry('500x300')
        self.resizable(False, False)
                 
if __name__ == "__main__":
    app = App()
    YouTubeDownload(app)
    app.mainloop()
