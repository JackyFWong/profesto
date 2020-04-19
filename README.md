# profesto
Measures and visualizes computer productivity on Linux

## About the app
STATUS = `incomplete`

'Profesto' is what I got from Google Translate when I translated 'workday' to Latin.

## Dependencies
- python3-xlib
- psutil

## Running the program
```
nohup python3 /path/to/this/repo/app/main.py &
```
You are free to close the terminal window afterwards.

To close the program, find the process with
```
ps ax | grep main.py
```
and kill it.
```
kill [PID]
```

## Data gathered
- Keyboard data > reading the file `/dev/eventX`, where X is the keyboard device number
- Mouse position > `xlib`
- Current active window > `xprop` and a lot of regular expressions
- Computer system data > `psutil` and `platform`

## Other programs
- `tkinter` for the GUI
- `notify2` for notification popups
