import os
import queue
from math import ceil
import concurrent.futures as cf
import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
import numpy as np

import data

matplotlib.use('TkAgg')

kb = "kb_out.log"
mo = "mo_out.log"
sy = "sys_out.log"
wn = "wn_out.log"

def draw_figure(canvas, figure):
    fca = FigureCanvasTkAgg(figure, canvas)
    fca.draw()
    fca.get_tk_widget().pack(side='top', fill='both', expand=1)
    return fca

def update_win(new_win, old_win):
    for key in new_win:
        if key in old_win:
            old_win[key] += new_win[key]
        else:
            old_win[key] = new_win[key]
    return old_win

class Gui:
    def __init__(self):
        self.input = data.Data((kb, mo, sy, wn))
        self.gui_queue = queue.Queue()

    def get_data(self, period):
        try:
            with cf.ThreadPoolExecutor() as gui_exe:
                gui_th0 = gui_exe.submit(self.input.get_mouse, period)
                gui_th1 = gui_exe.submit(self.input.get_keyboard, period)
                gui_th2 = gui_exe.submit(self.input.get_system, period)
                gui_th3 = gui_exe.submit(self.input.get_window, period)
        except (KeyboardInterrupt, SystemExit):
            exit()

        while gui_th0.running():
            pass
        while gui_th1.running():
            pass
        while gui_th2.running():
            pass
        while gui_th3.running():
            pass

        return (gui_th0.result(), gui_th1.result(),
            gui_th2.result(), gui_th3.result())

    def launch_gui(self):
        sg.theme('Dark Teal 6')

        mo_tab = [[sg.Canvas(size=(640,480), key='mo_canvas')]]
        kb_tab = [[sg.Canvas(size=(640,480), key='kb_canvas')]]
        sy_tab = [[sg.Canvas(size=(640,480), key='sy_canvas')]]
        wn_tab = [[sg.Multiline(size=(70,20), autoscroll=True, key='wn_canvas')]]
        graph_group = sg.TabGroup([[
            sg.Tab('Mouse', mo_tab),
            sg.Tab('Keyboard', kb_tab),
            sg.Tab('CPU Usage', sy_tab),
            sg.Tab('Windows', wn_tab)]])

        data_col = [
                [sg.Text('Overall Average Mouse Distance')],
                [sg.Text('AAAAAAAAAAAAAAAB', key="-MO_DIST-")],
                [sg.Text('Overall Average WPM')],
                [sg.Text('BBBBBBBBBBBBBBBB', key="-WPM_AVG-")],
                [sg.Text('Ovearll Average CPU Usage')],
                [sg.Text('CCCCCCCCCCCCCCCC', key="-CPU_USG-")],
                [sg.Text('Current Memory Usage')],
                [sg.Text('DDDDDDDDDDDDDDDD / EEEEEEEEEEEEEEEE', key="-MEM_USG-")],
                [sg.Text('Total Disk Usage')],
                [sg.Text('FFFFFFFFFFFFFFFF / GGGGGGGGGGGGGGGG', key="-DISK_USG-")],
                [sg.Text('Total Network usage')],
                [sg.Text('HHHHHHHHHHHHHHHH / IIIIIIIIIIIIIIII', key="-NETW_USG-")],
                [sg.Button('Clear history', button_color=('black','red'), key="-CLEAR-")]
        ]

        layout = [
            [sg.Text('Profesto', justification='center')],
            [graph_group, sg.Column(data_col)],
            [sg.Exit()]
        ]

        window = sg.Window('Profesto', layout)
        window.Finalize()

        # get initial data
        update_interval = 1
        (mo_data, kb_data, sy_data, wn_data) = self.get_data(1)
        time = [0]
        mo_hist = [mo_data['dist']]
        kb_hist = [kb_data['wpm']]
        sy_hist = [sy_data['total_cpu_per']]
        wn_hist = wn_data
        for k in wn_hist:
            wn_hist[k] = ceil(wn_hist[k])

        # mpl setup
        mo_canvas_elem = window['mo_canvas']
        kb_canvas_elem = window['kb_canvas']
        sy_canvas_elem = window['sy_canvas']
        
        mo_fig = plt.figure(0)
        kb_fig = plt.figure(1)
        sy_fig = plt.figure(2)

        mo_ax = mo_fig.add_subplot(111)
        kb_ax = kb_fig.add_subplot(111)
        sy_ax = sy_fig.add_subplot(111)

        mo_agg = draw_figure(mo_canvas_elem.TKCanvas, mo_fig)
        kb_agg = draw_figure(kb_canvas_elem.TKCanvas, kb_fig)
        sy_agg = draw_figure(sy_canvas_elem.TKCanvas, sy_fig)

        while True:
            # side stats
            mo_total_avg = sum(mo_hist) / len(mo_hist)
            kb_total_avg = sum(kb_hist) / len(kb_hist)
            cpu_total_avg = sum(sy_hist) / len(sy_hist)

            window['-MO_DIST-'].update(f"{ceil(mo_total_avg)} pixels")
            window['-WPM_AVG-'].update(f"{ceil(kb_total_avg)} WPM")
            window['-CPU_USG-'].update(f"{ceil(cpu_total_avg)}%")
            window['-MEM_USG-'].update(f"{sy_data['mem_per']}% virtual" +
                f" | {sy_data['swap_per']}% swap")
            window['-DISK_USG-'].update(f"{sy_data['disk_read']} read" +
                f" | {sy_data['disk_write']} write")
            window['-NETW_USG-'].update(f"{sy_data['net_sent']} sent" +
                f" | {sy_data['net_recv']} recieved")

            # update graphs
            mo_ax.cla()
            mo_ax.plot(time, mo_hist)
            mo_agg.draw()

            kb_ax.cla()
            kb_ax.plot(time, kb_hist)
            kb_agg.draw()

            sy_ax.cla()
            sy_ax.plot(time, sy_hist)
            sy_agg.draw()

            # update windows
            out_str = ""
            wn_hist = {k: v for k, v in sorted(wn_hist.items(), key=lambda item: item[1], reverse=True)}
            for key in wn_hist:
                out_str += f"{key} : {ceil(wn_hist[key])}\n"
            window['wn_canvas'].print(f"\n{out_str}")

            event, values = window.read(timeout=100)

            if event in (None, 'Exit'):
                break
            if event == '-CLEAR-':
                mo_hist = [0]
                kb_hist = [0]
                sy_hist = [0]
                wn_hist = {}
                time = [0]

            (mo_data, kb_data, sy_data, wn_data) = self.get_data(update_interval)
            time.append(time[-1]+update_interval)
            mo_hist.append(mo_data['dist'])
            kb_hist.append(kb_data['wpm'])
            sy_hist.append(sy_data['total_cpu_per'])
            wn_hist = update_win(wn_data, wn_hist)

            
        # user exits window
        window.close()
