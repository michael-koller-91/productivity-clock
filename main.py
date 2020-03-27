from time import time
import datetime
import tkinter as tk


class Menu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent


class Main(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # when running, refresh labels every "refresh_after" milliseconds
        self.refresh_after = 1000
        self.column_width = 20

        self.running = False
        self.timer_running = False
        self.pause_running = False

        self.timer_started = None
        # 40.1 hours corresponds to 40 hours and 6 minutes
        # this corresponds to 8 hours 1 minute and 12 seconds per day
        self.time_start_to_end = datetime.timedelta(hours=8, minutes=1, seconds=12)
        self.timer_end = None

        self.pause_started = None
        self.total_pause_time = None

        self.create_widgets()
        self.startup()

        # capturing keyboard events
        self.key_pause = '<space>'
        self.key_reset = '<Control-r>'
        self.bind('<Return>', self.start)

    def create_widgets(self):
        # row 0
        self.button_start = tk.Button(self, text='Start', width=self.column_width, command=self.start)
        # row 1
        self.button_pause = tk.Button(
            self, text='Pause', width=self.column_width, command=self.pause, state='disabled')
        # row 1
        self.label_timer_started = tk.Label(self)
        self.label_timer_started_nr = tk.Label(self)
        # row 2
        self.label_timer = tk.Label(self)
        self.label_timer_nr = tk.Label(self)
        # row 3
        self.label_countdown = tk.Label(self)
        self.label_countdown_nr = tk.Label(self)
        # row 4
        self.label_pause = tk.Label(self)
        self.label_pause_nr = tk.Label(self)
        # row 5
        self.label_timer_end = tk.Label(self)
        self.label_timer_end_nr = tk.Label(self)
        # row 6
        self.button_reset = tk.Button(
            self, text='Reset', width=2*self.column_width, command=self.reset, state='disabled')

    def startup(self):
        # row 0
        row = 0
        self.button_start.grid(row=row, column=0)
        self.button_start.configure(text='Start')
        self.button_pause.grid(row=row, column=1)
        self.button_pause.configure(text='Pause')
        self.button_pause.config(state='disabled')
        # row 1
        row += 1
        self.label_timer_started.grid(row=row, column=0)
        self.label_timer_started.configure(text='Timer Started:')
        self.label_timer_started_nr.grid(row=row, column=1)
        self.label_timer_started_nr.configure(text='00:00:00')
        # row 2
        row += 1
        self.label_timer.grid(row=row, column=0)
        self.label_timer.configure(text='Timer:')
        self.label_timer_nr.grid(row=row, column=1)
        self.label_timer_nr.configure(text='0:00:00')
        # row 3
        row += 1
        self.label_countdown.grid(row=row, column=0)
        self.label_countdown.configure(text='Countdown:')
        self.label_countdown_nr.grid(row=3, column=1)
        self.label_countdown_nr.configure(text=str(self.time_start_to_end)[:7])
        # row 4
        row += 1
        self.label_pause.grid(row=row, column=0)
        self.label_pause.configure(text='Pause Timer:')
        self.label_pause_nr.grid(row=row, column=1)
        self.label_pause_nr.configure(text='0:00:00')
        # row 5
        row += 1
        self.label_timer_end.grid(row=row, column=0)
        self.label_timer_end.configure(text='Timer End:')
        self.label_timer_end_nr.grid(row=row, column=1)
        self.label_timer_end_nr.configure(text='00:00:00')
        # row 6
        row += 1
        self.button_reset.grid(row=row, column=0, columnspan=2)
        self.button_reset.configure(text='Reset')
        self.button_reset.config(state='disabled')

    def start(self, _events=None):
        # system has been running (the button shows "Stop")
        if self.running:
            self.running = False
            self.timer_running = False
            self.pause_running = False

            # enable reset key (and key bind)
            self.button_reset.config(state='normal')
            self.bind(self.key_reset, self.reset)
            # disable pause key (and key bind)
            self.button_pause.config(state='disabled')
            self.unbind(self.key_pause)

            # switch button text from "Stop" to "Start"
            self.button_start.configure(text='Start')

        # system has not been running (the button shows "Start")
        else:
            self.running = True
            self.timer_running = True
            self.pause_running = False

            self.total_pause_time = datetime.timedelta(seconds=0.0)
            self.timer_started = datetime.datetime.now()
            self.label_timer_started_nr.configure(text=self.timer_started.strftime('%H:%M:%S'))
            self.refresh_timer_end_label(self.total_pause_time)

            # disable reset key (and key bind)
            self.button_reset.config(state='disabled')
            self.unbind(self.key_reset)
            # enable pause key (and key bind)
            self.button_pause.config(state='normal')
            self.bind(self.key_pause, self.pause)

            # switch button text from "Start" to "Stop"
            self.button_start.configure(text='Stop')

            # start the update loop
            self.update_labels()

    def update_labels(self):
        # arbitrarily use this label to create an update loop
        self.label_timer_started.after(self.refresh_after, self.update_labels)

        # system is not paused
        if self.timer_running:
            self.refresh_timer_label()
            self.refresh_countdown_label()

        # system is paused
        if self.pause_running:
            current_total_pause_time = datetime.datetime.now() - self.pause_started + self.total_pause_time
            self.refresh_pause_label(current_total_pause_time)
            self.refresh_timer_end_label(current_total_pause_time)

    def refresh_pause_label(self, total_pause):
        self.label_pause_nr.configure(text=str(total_pause)[:7])

    def refresh_timer_label(self):
        total_timer_time = datetime.datetime.now() - self.timer_started - self.total_pause_time
        self.label_timer_nr.configure(text=str(total_timer_time)[:7])

    def refresh_timer_end_label(self, total_pause):
        self.timer_end = self.timer_started + self.time_start_to_end + total_pause
        self.label_timer_end_nr.configure(text=self.timer_end.strftime('%H:%M:%S'))

    def refresh_countdown_label(self):
        total_timer_time = datetime.datetime.now() - self.timer_started - self.total_pause_time
        if (self.time_start_to_end - total_timer_time).total_seconds() >= 0:
            self.label_countdown_nr.configure(text=str(self.time_start_to_end-total_timer_time)[:7])
        # if the countdown has reached 0, continue with negative numbers (counting up in absolute value)
        else:
            self.label_countdown_nr.configure(text='-'+str(total_timer_time-self.time_start_to_end)[:7])

    def pause(self, _events=None):
        # if system has not been started, return immediately
        if not self.running:
            return

        # if pause has been running and the pause button is clicked (the button shows "Continue")
        if self.pause_running:
            self.timer_running = True
            self.pause_running = False

            self.total_pause_time += datetime.datetime.now() - self.pause_started
            self.refresh_timer_end_label(self.total_pause_time)
            self.refresh_pause_label(self.total_pause_time)

            # switch button text from "Continue" to "Pause"
            self.button_pause.configure(text='Pause')

        # if pause has not been running and the pause button is clicked (the button shows "Pause")
        else:
            self.timer_running = False
            self.pause_running = True

            self.pause_started = datetime.datetime.now()

            # switch button text from "Pause" to "Continue"
            self.button_pause.configure(text='Continue')

    def reset(self, _events=None):
        self.running = False
        self.timer_running = False
        self.pause_running = False
        self.startup()


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title('Productivity Clock')

        self.main = Main(self)
        self.main.grid()
        # keyboard focus
        self.main.focus_set()

        self.menu = Menu(self)
        self.menu.grid()

        # place window in bottom right corner
        self.parent.update()
        wh = self.main.winfo_height()
        ww = self.main.winfo_width()
        sw = self.parent.winfo_screenwidth() - ww - 15
        sh = self.parent.winfo_screenheight() - wh - 80
        self.parent.geometry('{}x{}+{}+{}'.format(ww, wh, sw, sh))
        self.parent.resizable(0, 0)


def main():
    root = tk.Tk()
    MainApplication(root).pack(expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()
