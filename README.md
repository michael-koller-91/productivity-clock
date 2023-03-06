# Productivity Clock

<p align="center">
    <img src=productivity_clock_start.png?raw=true>
</p>

Productivity Clock uses `tkinter`.
To start the program, run
```python
python main.py
```

By default, the countdown says two hours and thirty minutes and the output file is `clock.csv`.
This can be changed via command line arguments.
The default setting is equivalent to:
```python
python main.py --hours 2 --minutes 30 --outfile clock
```
## Features

Once `Start` is clicked, the start time is displayed in the line `Started`
and the countdown starts.

<p align="center">
    <img src=productivity_clock_running.png?raw=true>
</p>

To pause the countdown, click `Pause` (the button then displays `Continue`).
The line `Paused` shows how long the clock has been paused.
Clicking `Continue` resumes the countdown.
The line `Running` shows how long the clock has been running since the start time minus the pause time.
`End` predicts when the countdown reaches zero.
The pause time is taken into account.

If the box `Save to .csv` is checked, clicking `Start`, `Stop`, `Pause`, or `Continue` leads to a new entry in a CSV file which by default is called `clock.csv`.
The first entry of the line is today's date, the remaining entries are the times of clicking one of the four mentioned buttons.
