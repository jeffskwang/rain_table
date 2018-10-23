import numpy as np
import matplotlib.pyplot as plt

def on_key(event, m):

    if event.key == ' ':
        m.sm._toggle_stream = not m.sm._toggle_stream
    
    elif event.key == 'up':
        m.sm.slide_cloud.increase_val()
    elif event.key == 'down':
        m.sm.slide_cloud.decrease_val()

    elif event.key == 'left':
        m.sm.slide_baseflow.decrease_val()
    elif event.key == 'right':
        m.sm.slide_baseflow.increase_val()

    elif event.key == 'pageup':
        m.sm.slide_transp.increase_val()
        m._aerial_alpha_changed = True
    elif event.key == 'pagedown':
        m.sm.slide_transp.decrease_val()
        m._aerial_alpha_changed = True
    elif event.key in {'0','1','2','3','4','5','6','7','8','9'}:
        if event.key == '0':
            transp_int = 9
        else:
            transp_int = int(event.key)-1
        scaled = (transp_int / 9) * 100
        newval = m.sm.slide_transp._value_in_bounds(scaled)
        m.sm.slide_transp.set_val(newval)
        m._aerial_alpha_changed = True


def on_click(event, m):
    
    if event.button == 1: # left click
        m._lclicked = True
    if event.button == 3: # right click
        m._rclicked = True


def off_click(event, m):
    
    if event.button == 1: # left click
        m._lclicked = False
    if event.button == 3: # right click
        m._rclicked = False


def mouse_move(event, m):

    x, y = event.xdata, event.ydata
    # print(event.inaxes)
    # print(m.map_ax)

    if event.inaxes == m.map_ax:
        # m._mx, m._my = m.map_ax.transAxes.inverted().transform([x*m.scale, y*m.scale])
        # m._mx, m._my = m.map_ax.transAxes.inverted()
        m._mx, m._my = x * m.scale, y * m.scale
        m._inax = True
    else:
        m._mx, m._my = x, y
        m._inax = False
