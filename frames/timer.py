import tkinter as tk
from tkinter import ttk
from collections import deque
import pygame 
import os

# ----- Windows only configuration -----
try: #try-except, becasue this code will not run in MacOS or Linux
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1) #to increase screen Dpi of Tkinter objects in Windows10
except:
    pass

# ----- create framing class ------
class Timer(ttk.Frame):
    def __init__(self, parent, controller, show_settings):  
        super().__init__(parent)

        # ----- Aestetics -----
        self["style"] = "Background.TFrame" #NOTE: self["style"] can be used for ttk-objects but NOT for tk-objects
 
        # ----- initiate timer variables -----

        self.controller = controller

        # extract variables from controller
        pomodoro_time = int(controller.pomodoro.get())
        short_break_time = int(controller.short_break.get())
        long_break_time = int(controller.long_break.get())
        self.label_text = controller.label_text
        self.sound = controller.sound

        # initiate class variables
        self.current_time = tk.StringVar(value= f"{pomodoro_time:02d}:00")
        self.timer_label = tk.StringVar(value="Click 'Start'")#self.label_text[self.timer_schedule[0]])
        self.timer_running = False
        # self._timer_decrement_jobs = None

        # add label with timer description to current Timer-obeject
        timer_description = ttk.Label(
            self,
            textvariable=self.timer_label,
            style="LightText.TLabel"
        )
        timer_description.grid(row=0, column=0, sticky ="EW", padx=(10,0), pady=(10,0))

        # add settings button, that toggles to settings frame
        settings_button = ttk.Button(
            self,
            text = "Settings",
            command = show_settings,
            cursor="hand2",
            style="PomodoroButton.TButton"
        )
        settings_button.grid(row=0, column=1, sticky="E", padx=10, pady=(10,0))

        # create another frame inside the Timer-object, that will harbour the counter
        timer_frame = ttk.Frame(self, height="100", style="Timer.TFrame")
        timer_frame.grid(row=1, column=0, columnspan =2, pady=(10,0), sticky="NSEW")

        # create label set in timer_frame that sows tghe time
        timer_counter = ttk.Label(
            timer_frame,
            textvariable=self.current_time,
            style="TimerText.TLabel"
        )
        timer_counter.place(relx=0.5, rely=0.5, anchor="center") #use .place() insteada of .grid() to center counter in its frame

        #----- buttons -----
        #add a container for a button
        button_container = ttk.Frame(self,padding=10, style="Button.TFrame")
        button_container.grid(row=2, column=0, columnspan =2, sticky="EW") # add this container to second row and make it stick to letft and right (--> so no vertical growth)
        button_container.columnconfigure((0, 1, 2), weight=1) # configure the container to havetwo columns taking up equal space

        # add buttons 
        self.start_button = ttk.Button(
            button_container,
            text="Start",
            command=self.start_timer,
            cursor="hand2",
            style="PomodoroButton.TButton"
        )
        self.start_button.grid(row=0, column=0, sticky="EW")

        self.stop_button = ttk.Button(
            button_container,
            text="Stop",
            state="disabled",
            command=self.stop_timer,
            cursor="hand2",
            style="PomodoroButton.TButton"
        )
        self.stop_button.grid(row=0, column=1, sticky="EW", padx=5)

        self.reset_button = ttk.Button(
            button_container,
            text="Reset",
            command=self.reset_timer,
            cursor="hand2",
            style="PomodoroButton.TButton"
        )
        self.reset_button.grid(row=0, column=2, sticky="EW")

        # decrease timer by elapsed time
        self.decrement_timer() #custom function defined below

    #  ----- button finctions -----
    # function starting the timer
    def start_timer(self):
        self.timer_running = True
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "enabled"
        self.decrement_timer()

    # function stopping the timer
    def stop_timer(self):
        self.timer_running = False
        self.start_button["state"] = "ensabled"
        self.stop_button["state"] = "disabled"
        self.decrement_timer()

        # if decrement_timer is running: cancel it - to avoid multiple jobs running at the same time
        if self._timer_decrement_jobs:
            self.after_cancel(self._timer_decrement_jobs)
            self._timer_decrement_jobs = None

    # function reseting the timer
    def reset_timer(self):
        self.timer_running = False
        self.start_button["state"] = "enabled"
        self.stop_button["state"] = "disabled"
        self.timer_schedule = deque(self.controller.timer_order)
        pomodoro_time = int(self.controller.pomodoro.get())
        self.current_time.set(f"{pomodoro_time:02d}:00")
        self.timer_label.set(value="Click 'Start'")
        self.decrement_timer()

    # ----- function decreasing the timer one second at a time -----
    def decrement_timer(self):
        # get value saved in current_time 
        current_time = self.current_time.get() #use .get() as this is a ttk.StringVar-object

        if self.timer_running and current_time != "00:00":
            # get correct label
            next_up = self.controller.timer_schedule[0]
        
            # update timer description
            self.timer_label.set(value=self.label_text[next_up])

            #split current time string on ":" and save output to variables
            minutes, seconds = current_time.split(":") 
            
            # adapt/decrease seconds and minutes depending on their value
            if int(seconds) > 0: 
                seconds = int(seconds) - 1
                minutes = int(minutes)
            else:
                seconds = 59
                minutes = int(minutes) - 1

            # save new counter value 
            self.current_time.set(f"{minutes:02d}:{seconds:02d}")

            # re-run function after 1000ms
            self._timer_decrement_jobs = self.after(100, self.decrement_timer)

        elif self.timer_running and current_time == "00:00":
            self.controller.timer_schedule.rotate(-1) #rotate current timer_order item to the end; following item is now in first place
            next_up = self.controller.timer_schedule[0] #save new first-place item in next_up variable
            self.play_sound() #play gong every time a time-section is up

            # set current_time depending on current setting
            if next_up =="pomodoro":
                pomodoro_time = int(self.controller.pomodoro.get())
                self.current_time.set(f"{pomodoro_time:02d}:00")
            elif next_up == "short_break":
                short_break_time = int(self.controller.short_break.get())
                self.current_time.set(f"{short_break_time:02d}:00")
            elif next_up == "long_break":
                long_break_time = int(self.controller.long_break.get())
                self.current_time.set(f"{long_break_time:02d}:00")

            # update timer description
            self.timer_label.set(value=self.label_text[next_up])

            # re-run function after 1000ms
            self._timer_decrement_jobs = self.after(100, self.decrement_timer)

    # ----- function playing sound from an mp3-file -----
    def play_sound(self):
        # dict to map selected sound option to file name
        sounds = {'Gong (default)':'Bell_Sound_Ring',
                  'Rooster':'Rooster_Crowing-43612401',
                  'Beer Can':'Beer_Can_Opening_1428393126',
                  'Santa Claus':'Ho_Ho_Ho_1954250969',
                  'Party Horn':'party_horn-Mike_Koenig-76599891',
                  'Service Bell':'service-bell_daniel_simion',
                  'Spooky Water Drops':'Spooky_Water_Drops_50164895'
                  }
        # get sound selected in Combobox 
        selected = self.controller.sound.get()
        # get mp3 file name associated with selected sound
        mp3_file_name = sounds[selected]
        # path to mp3 file to play
        path = os.path.join(f"media",f"{mp3_file_name}.mp3")
        # initialize pygame mixer and play selected sound
        pygame.mixer.init()
        pygame.mixer.music.load(f"{path}")
        pygame.mixer.music.play(loops=0)