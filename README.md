# profesto
Measures and visualizes computer productivity on Linux

## About the app
STATUS = `functionally complete`

'Profesto' is what I got from Google Translate when I translated 'workday' to Latin.

Performance is not ideal. Due to the nature of matplotlib and the timeouts I have to use 
to sync the program, there is stutter during data collection. Please allow a few seconds between 
every (and I do mean every) interaction with the program.

## Dependencies
- python3-xlib
- psutil
- matplotlib (only version 3.0.3)
- pysimplegui

## Installation for dependencies
This will depend on your system. I use Fedora Linux.
```bash
dnf install python3-xlib
pip3 install psutil
pip3 install matplotlib==3.0.3
pip3 install pysimplegui
```

## Running the program
Due to the nature of the keyboard reader, you cannot run the program as a regular user. 
You must use `sudo`. As such, I cannot provide a Bash script to easily execute the 
program. In addition, because this is Python, there is no executable.
```
sudo nohup python3 app/main.py &
```
You are free to close the terminal window afterwards.

To close the program, close the window or click the Exit button.

## Data gathered
- Keyboard data > reading the file `/dev/eventX`, where X is the keyboard device number
- Mouse position > `xlib`
- Current active window > `xprop` and regex
- Computer system data > `psutil` and `platform`

## Other programs
- `PySimpleGUI` for the GUI
