import tkinter as tk
from tkinter import ttk
from collections import deque
from frames import Timer , Settings

# ----- Windows only configuration -----
try: #try-except, becasue this code will not run in MacOS or Linux
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1) #to increase screen Dpi of Tkinter objects in Windows10
except:
    pass

# ----- create widget class ------
class PomodoroTimer(tk.Tk): #class inheriting from tk.Tk
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # customize widget/window using tk.Tk-methods using class variables
        self.title("Pomodoro Timer") #set title
        self.columnconfigure(0, weight=1) #center content of first row
        self.rowconfigure(1, weight=1) 

        # create class variables
        self.pomodoro = tk.StringVar(value=25)
        self.short_break = tk.StringVar(value=5)
        self.long_break = tk.StringVar(value=15)
        self.timer_order = ["pomodoro", "short_break", "pomodoro", "short_break", "pomodoro", "long_break"]
        self.timer_schedule = deque(self.timer_order) #create deck to cycle through timer_order items
        self.label_text = {"pomodoro":"Pomodoro, get to work!!!", "short_break":"Take a short break", "long_break":"Long break! Go grab some coffee :)"}

        # save a ttk frame - object in a variable named "container"
        container = ttk.Frame(self) 
        container.grid() #position the frame in the parent widget in a grid
        container.columnconfigure(0, weight=1)

        # create dictionary to keep track of frames
        self.frames = dict()

        # ----- add timer frame that is placed within "container"
        self.timer_frame = Timer(container, self, lambda: self.show_frame(Settings)) #initiate Timer-class and pass self as the controller
        self.timer_frame.grid(row=0, column=0, sticky="NESW") #configure timer frame placed in the first row and first column and to fill the entire frame ("container")

        # ----- add settings frame -----
        self.settings_frame = Settings(container, self, lambda: self.show_frame(Timer))
        self.settings_frame.grid(row=0, column=0, sticky="NESW") 

        # add both frames to dict
        self.frames[Timer] = self.timer_frame
        self.frames[Settings] = self.settings_frame

        # start with timer_frame in front
        self.show_frame(Timer)

    # ----- function that brings frame on the back to the front -----
    def show_frame(self, container):
        # indicate which frame to bring to front
        frame = self.frames[container]
        #brings indicated frame to the front
        frame.tkraise() 
        # if timer is not running, automatically reset time on frame change to changes times
        if not self.timer_frame.timer_running:
            self.timer_frame.reset_timer()  
 
# ----- run app -----
app = PomodoroTimer()

app.mainloop()