import os
import datetime
import tkinter as tk


class MessageBox:
    def __init__(self, parent, title, text):
        self.top = tk.Toplevel(parent)
        self.top.title(title)

        self.label = tk.Label(self.top, text=text)
        self.label.pack()

        self.button = tk.Button(self.top, text="OK", command=self.ok)
        self.button.pack(pady=5)

        self.top.focus_force()

    def ok(self):
        self.top.destroy()


class Core(tk.Frame):
    def __init__(self, parent, hours, minutes, outfile, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.outfile = outfile + '.csv'
        self.save_to_csv = False
        self.save_to_csv_tk = tk.BooleanVar()

        # when running, refresh labels every "refresh_after" milliseconds
        self.refresh_after = 1000
        self.column_width = 20

        self.running = False
        self.timer_running = False
        self.pause_running = False

        self.timer_started = None
        self.time_start_to_end = datetime.timedelta(hours=hours, minutes=minutes)
        self.timer_end = None

        self.countdown_reached_zero = False

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
        # row 7
        self.checkbox = tk.Checkbutton(
            self,
            text='Save to .csv',
            variable=self.save_to_csv_tk,
            onvalue=True,
            offvalue=False,
            command=self.create_outfile
        )

    def create_outfile(self):
        self.save_to_csv = self.save_to_csv_tk.get()

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
        self.label_timer_started.configure(text='Started:')
        self.label_timer_started_nr.grid(row=row, column=1)
        self.label_timer_started_nr.configure(text='00:00:00')
        # row 2
        row += 1
        self.label_timer.grid(row=row, column=0)
        self.label_timer.configure(text='Running:')
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
        self.label_pause.configure(text='Paused:')
        self.label_pause_nr.grid(row=row, column=1)
        self.label_pause_nr.configure(text='0:00:00')
        # row 5
        row += 1
        self.label_timer_end.grid(row=row, column=0)
        self.label_timer_end.configure(text='End:')
        self.label_timer_end_nr.grid(row=row, column=1)
        self.label_timer_end_nr.configure(text='00:00:00')
        # row 6
        row += 1
        self.button_reset.grid(row=row, column=0, columnspan=2)
        self.button_reset.configure(text='Reset')
        self.button_reset.config(state='disabled')
        # row 7
        row += 1
        self.checkbox.grid(row=row, column=0, columnspan=2)

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

            if self.save_to_csv:
                with open(self.outfile, 'a') as f:
                    f.write(',(Stop)')
                    f.write(datetime.datetime.now().strftime('%H:%M'))

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

            if self.save_to_csv:
                date_today = datetime.date.today().strftime('%Y-%m-%d')
                if not os.path.exists(self.outfile):
                    with open(self.outfile, 'w') as f:
                        f.write(date_today)
                        f.write(',(Start)')
                        f.write(datetime.datetime.now().strftime('%H:%M'))
                else:
                    if not os.path.getsize(self.outfile) == 0:
                        # read last line
                        with open(self.outfile, 'r') as f:
                            for line in f:
                                pass
                        line0 = line.split(',')[0]
                    else:
                        line0 = ''

                    # if there is not already an entry for today
                    if line0 != date_today:
                        with open(self.outfile, 'a') as f:
                            if len(line0):
                                f.write('\n')
                            f.write(date_today)
                            f.write(',(Start)')
                            f.write(datetime.datetime.now().strftime('%H:%M'))
                    else:
                        with open(self.outfile, 'a') as f:
                            f.write(',(Start)')
                            f.write(datetime.datetime.now().strftime('%H:%M'))

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
            # show a dialog box if this happens for the first time
            if not self.countdown_reached_zero:
                self.countdown_reached_zero = True
                MessageBox(self.parent, 'Goal Achieved', 'The countdown has reached 0.')
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

            if self.save_to_csv:
                with open(self.outfile, 'a') as f:
                    f.write(',(Continue)')
                    f.write(datetime.datetime.now().strftime('%H:%M'))

        # if pause has not been running and the pause button is clicked (the button shows "Pause")
        else:
            self.timer_running = False
            self.pause_running = True

            self.pause_started = datetime.datetime.now()

            # switch button text from "Pause" to "Continue"
            self.button_pause.configure(text='Continue')

            if self.save_to_csv:
                with open(self.outfile, 'a') as f:
                    f.write(',(Pause)')
                    f.write(datetime.datetime.now().strftime('%H:%M'))

    def reset(self, _events=None):
        self.running = False
        self.timer_running = False
        self.pause_running = False
        self.countdown_reached_zero = False
        self.startup()
