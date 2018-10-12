import numpy as np
import matplotlib.pyplot as plt

def on_key(event, m):
    # print('you pressed', event.key, event.xdata, event.ydata)
    # # keyboard input
    # if event.type == pygame.KEYDOWN:
    if event.key == ' ':
        m._toggle_stream = not m._toggle_stream
        # area_threshold = area_threshold_list[area_threshold_index]
    # elif event.key == pygame.K_UP and key_down == 0:
    #     key_down = 1
    #     rad += 5
    # elif event.key == pygame.K_DOWN and key_down == 0:
    #     key_down = 1
    #     rad -= 5
    #     if rad <=0:
    #         rad = 5
    # elif event.key == pygame.K_LEFT and key_down == 0:
    #     key_down = 1
    #     area_threshold_index -= 1
    #     if area_threshold_index <= 0:
    #         area_threshold_index = 0
    #     area_threshold = area_threshold_list[area_threshold_index]
    # elif event.key == pygame.K_RIGHT and key_down == 0:
    #     key_down = 1
    #     area_threshold_index += 1
    #     if area_threshold_index >= len(area_threshold_list):
    #         area_threshold_index = len(area_threshold_list) - 1
    #     area_threshold = area_threshold_list[area_threshold_index]
    # elif event.key == pygame.K_1:
    #     transparency_int = 1
    # elif event.key == pygame.K_2:
    #     transparency_int = 2
    # elif event.key == pygame.K_3:
    #     transparency_int = 3
    # elif event.key == pygame.K_4:
    #     transparency_int = 4
    # elif event.key == pygame.K_5:
    #     transparency_int = 5
    # elif event.key == pygame.K_6:
    #     transparency_int = 6
    # elif event.key == pygame.K_7:
    #     transparency_int = 7
    # elif event.key == pygame.K_8:
    #     transparency_int = 8
    # elif event.key == pygame.K_9:
    #     transparency_int = 9


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
