import numpy as np
import matplotlib.pyplot as plt

def on_key(event, m):

    if event.key == ' ':        
        m.sm.chk_baseflow.set_active(0)
        if m.sm.chk_baseflow.get_status()[0]:
            m._toggle_stream.val = True
        else:            
            m._toggle_stream.val = False


    
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


def on_click(event, mm):
    
    if event.button == 1: # left click
        mm._lclicked = True
    if event.button == 3: # right click
        mm._rclicked = True


def off_click(event, mm):
    
    if event.button == 1: # left click
        mm._lclicked = False
    if event.button == 3: # right click
        mm._rclicked = False


def mouse_move(event, mm, map_ax, scale):

    x, y = event.xdata, event.ydata

    if event.inaxes == map_ax:
        mm._mx, mm._my = x * scale, y * scale
        mm._inax = True
    else:
        mm._mx, mm._my = x, y
        mm._inax = False


def transp_slider_action(event, aerial_array, aerial_surface):
    newval = (1 - (event / 100)) * 255
    aerial_array[:,:,3] = newval # change the alpha
    aerial_surface.set_data(aerial_array)


def slider_set_to(event, to_set):
    # generic setter for SliderVal class value holders
    to_set.val = event

def check_switch(event, to_set):
    to_set.val = not to_set.val
