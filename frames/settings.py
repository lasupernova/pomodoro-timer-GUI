# ----- import libraries and modules -----
from tkinter import ttk

# ----- create settings class to incorporate into app.py -----

class Settings(ttk.Frame):
    def __init__(self, parent, controller, show_timer):
        super().__init__(parent)

        #  ----- Aestetics -----
        self['style'] = "Background.TFrame"

        # create container and define location in Settings-widget
        settings_container = ttk.Frame(
            self,
            padding="30 15 30 15",
            style="Background.TFrame"
        )

        settings_container.grid(row=0, column=0, sticky="EW", padx=10, pady=10)

        settings_container.columnconfigure(0, weight=1)
        settings_container.rowconfigure(1, weight=1)

        # ----- Labels -----

        # pomodoro label
        pomodoro_label = ttk.Label(
            settings_container,
            text = "Pomodoro",
            style="LightText.TLabel"
        )
        pomodoro_label.grid(row=0, column=0, sticky="W")

        # short break label
        short_break_label = ttk.Label(
            settings_container,
            text = "Short Break",
            style="LightText.TLabel"
        )
        short_break_label.grid(row=1, column=0, sticky="W")

        # long break label
        long_break_label = ttk.Label(
            settings_container,
            text = "Long Break",
            style="LightText.TLabel"
        )
        long_break_label.grid(row=2, column=0, sticky="W")

        # sound label
        sound_label = ttk.Label(
            settings_container,
            text = "Notification Sound",
            style="LightText.TLabel"
        )
        sound_label.grid(row=3, column=0, sticky="W")


        # ----- Spinboxes (Input) -----

        # pomodoro box
        pomodoro_input = ttk.Spinbox(
            settings_container,
            from_=1,
            to=120,
            increment=1,
            justify="center",
            textvariable=controller.pomodoro,
            width=10
        )
        pomodoro_input.grid(row=0, column=1, sticky="EW") 
        pomodoro_input.focus()

        # short break box
        short_break_input = ttk.Spinbox(
            settings_container,
            from_=1,
            to=15,
            increment=1,
            justify="center",
            textvariable=controller.short_break,
            width=10
        )
        short_break_input.grid(row=1, column=1, sticky="EW") 
        short_break_input.focus()

        # long break box
        long_break_input = ttk.Spinbox(
            settings_container,
            from_=1,
            to=45,
            increment=1,
            justify="center",
            textvariable=controller.long_break,
            width=10
        )
        long_break_input.grid(row=2, column=1, sticky="EW") 
        long_break_input.focus()

        # long break box
        sound_input = ttk.Combobox(
            settings_container,
            justify="center",
            textvariable=controller.sound,
            width=10,
            values=['Gong (default)','Rooster','Beer Can','Santa Claus','Party Horn','Service Bell','Spooky Water Drops']
        )
        sound_input.grid(row=3, column=1, sticky="EW") 
        sound_input.focus()

        # ----- button container -----
        button_container = ttk.Frame(self, style="Background.TFrame")
        button_container.grid(sticky="EW", padx=10)
        button_container.columnconfigure(0, weight=1)

                # ----- Button ------
        # add timer button, that toggles to timer frame
        timer_button = ttk.Button(
            button_container,
            text = "⟵ back to Timer",
            command = show_timer,
            cursor="hand2",
            style="PomodoroButton.TButton"
        )
        timer_button.grid(row=0, column=0, sticky="EW", padx=2)

        # ----- aestetics -----

        # iterate over all items in settings_container
        for child in settings_container .winfo_children():
            # add padding
            child.grid_configure(padx=5, pady=5)
            
            # print(child) #uncomment for troubleshooting
