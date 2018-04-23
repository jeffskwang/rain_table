#python game
#written by jeffrey kwang
#email: jeffskwang@gmail.com
#version = alpha_1

############################
###LIBRARIES###
############################

import pygame
import numpy as np
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

############################
###PARAMETERS###
############################
#scale of screen_res / DEM_res
scale = 3

#radius of rain cloud
rad = 80

#frame rate
f_rate = 60

#transparency of cloud
alpha = 0.1

############################
###RASTERS###
############################

#this path
this_dir = os.path.dirname(__file__)
this_path = os.path.join(this_dir,'')
priv_path = os.path.abspath(os.path.join(this_path, os.pardir, 'private'))

#load dem
DEM = np.loadtxt(os.path.join(priv_path, 'dem.txt'),skiprows=6)
res_height,res_width = DEM.shape
min_ele = np.min(DEM[DEM!=-9999])
max_ele = np.max(DEM)
DEM[DEM==-9999] = min_ele

#load drainage area
AREA = np.loadtxt(os.path.join(priv_path, 'area.txt'),skiprows=6)

#0|1|2
#3|x|4
#5|6|7
#load direction, covert the arcgis direction values to values between 0 and 7
DIR = np.loadtxt(os.path.join(priv_path, 'dir.txt'),dtype = int, skiprows=6)
DIR[DIR==8] = 5
DIR[DIR==4] = 6
DIR[DIR==2] = 7
DIR[DIR==1] = 4
DIR[DIR==32] = 0
DIR[DIR==64] = 1
DIR[DIR==128] = 2 
DIR[DIR==16] = 3

############################
###FUNCTIONS###
############################

def plot_setup(plot_array,x,y,xlabel,ylabel,Q_max):
    width_pixel,height_pixel = plot_array.shape[0], plot_array.shape[1]
    fig = Figure(figsize=(float(width_pixel)/100.,float(height_pixel)/100.),dpi=100)
    ax = fig.gca()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(t[0],t[-1])
    ax.set_ylim(0,Q_max)
    ax.plot(x,y,color='b')
        
    fig.tight_layout()
    canvas = FigureCanvas(fig)

    canvas.draw()
    
    buf = fig.canvas.tostring_rgb()
    ncols,nrows = fig.canvas.get_width_height()
    buf = np.fromstring(buf, dtype=np.uint8).reshape(nrows, ncols, 3)

    return np.transpose(buf,(1, 0, 2))

############################
###PYGAME###
############################

#initialize pygame
x = pygame.init()

#make game display
gameDisplay = pygame.display.set_mode((scale*res_width,int(scale*res_height * 1.5)))

#set title of game
pygame.display.set_caption('SedEdu -- Drainage basins')

#update screen
pygame.display.update()

#set gameExit to false to enter the main loop
gameExit = False

#set clock for framerate lock
clock = pygame.time.Clock()

############################
###INITIALIZATION###
############################
#intialize parameters
#background streams on/off
toggle_stream = 0

#key press down/up
key_down = 0

#update matplotlib every # frame to improve performance
frame_number = plot_every_frame = 10

#threshold for channelization
area_threshold_index = 18

#define a base flow to scale hydrograph
base_flow = 2539.

#control tranparency of the aerial image
transparency_int = 7
transparency_list = np.linspace(0,255,9)

#hydrograph gauge location
y_hydro, x_hydro = np.unravel_index(AREA.argmax(), AREA.shape)

#aerial photo
aerial_surface = pygame.image.load(os.path.join(priv_path, 'aerial.png')).convert(24)
aerial_surface_scaled = pygame.transform.scale(aerial_surface,(int(res_width * scale),int(res_height * scale)))

#contols
controls_surface = pygame.image.load(os.path.join(priv_path, 'rain_table_controls.png'))
controls_surface_scaled  = pygame.transform.scale(controls_surface,(int(res_height * scale * 0.5),int(res_height * scale * 0.5)))
gameDisplay.blit(controls_surface_scaled,(res_width*scale - int(res_height*scale * 0.5),res_height*scale))

############################
###ARRAYS###
############################
DEM_array = np.zeros((res_width,res_height,3),dtype=int)
flow_array = np.zeros((res_width,res_height,3),dtype=int)
prev_array = np.zeros((res_width,res_height,3),dtype=int)
AREA_old = np.zeros((res_width,res_height),dtype=int)
AREA_new = np.zeros((res_width,res_height),dtype=int)

#hydrograph plot
plot_hydro = np.zeros((int(res_width * scale)-int(res_height*0.5*scale),int(res_height*0.5*scale),3),dtype=int)

#hyrograph arrays
t = np.linspace(-100.,0.0,1001)
Q = np.zeros(1001)

#predifined area thresholds
area_threshold_list = np.concatenate((np.zeros(1),np.logspace(0,np.log10(np.max(AREA)),29)),axis=0)

#setup direction array
direction = np.zeros((res_width,res_height,8),dtype=int)
for i in np.arange(0,8):
    direction[:,:,i][np.transpose(DIR)==i] = 1

#coordinate array
coordinates = np.zeros((res_width,res_height,2))
for x_temp in np.arange(0,res_width):
    for y_temp in np.arange(0,res_height):
        coordinates[x_temp,y_temp,0] = x_temp * scale
        coordinates[x_temp,y_temp,1] = y_temp * scale

#DEM array
DEM_array[:,:,0] = (np.transpose(DEM) - min_ele) / (max_ele - min_ele) * 255
DEM_array[:,:,1] = (np.transpose(DEM) - min_ele) / (max_ele - min_ele) * 255
DEM_array[:,:,2] = (np.transpose(DEM) - min_ele) / (max_ele - min_ele) * 255

############################
###MAIN LOOP###
############################
while not gameExit:
    #event handler (temp event) use pygame events, e.g. contains mouse data, keyboard presses
    for event in pygame.event.get():
        #quit and leave the loop
        if event.type == pygame.QUIT:
            gameExit = True

    #mouse location
    (x_mouse,y_mouse) = pygame.mouse.get_pos()

    #keyboard input
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and key_down == 0:
            key_down = 1
            if toggle_stream == 0:
                toggle_stream = 1
            elif toggle_stream == 1:
                toggle_stream = 0
            area_threshold = area_threshold_list[area_threshold_index]
        elif event.key == pygame.K_UP and key_down == 0:
            key_down = 1
            rad += 5
        elif event.key == pygame.K_DOWN and key_down == 0:
            key_down = 1
            rad -= 5
            if rad <=0:
                rad = 5
        elif event.key == pygame.K_LEFT and key_down == 0:
            key_down = 1
            area_threshold_index -= 1
            if area_threshold_index <= 0:
                area_threshold_index = 0
            area_threshold = area_threshold_list[area_threshold_index]
        elif event.key == pygame.K_RIGHT and key_down == 0:
            key_down = 1
            area_threshold_index += 1
            if area_threshold_index >= len(area_threshold_list):
                area_threshold_index = len(area_threshold_list) - 1
            area_threshold = area_threshold_list[area_threshold_index]
        elif event.key == pygame.K_1:
            transparency_int = 1
        elif event.key == pygame.K_2:
            transparency_int = 2
        elif event.key == pygame.K_3:
            transparency_int = 3
        elif event.key == pygame.K_4:
            transparency_int = 4
        elif event.key == pygame.K_5:
            transparency_int = 5
        elif event.key == pygame.K_6:
            transparency_int = 6
        elif event.key == pygame.K_7:
            transparency_int = 7
        elif event.key == pygame.K_8:
            transparency_int = 8
        elif event.key == pygame.K_9:
            transparency_int = 9

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
            key_down = 0
        if event.key == pygame.K_UP:
            key_down = 0
        if event.key == pygame.K_DOWN:
            key_down = 0
        if event.key == pygame.K_LEFT:
            key_down = 0
        if event.key == pygame.K_RIGHT:
            key_down = 0
    
    #mouse pressed
    if pygame.mouse.get_pressed()[0]:
        AREA_old[(coordinates[:,:,0] - x_mouse) ** 2.0 + (coordinates[:,:,1] - y_mouse) ** 2.0 < rad ** 2.0] += 1

    #toggle base_flow
    if toggle_stream == 1:
        AREA_old[np.transpose(AREA) >= area_threshold ] += 1

    #ROUTE THE RAINFALL
    AREA_new[:-1,:-1] += AREA_old[1:,1:] * direction[1:,1:,0]
    AREA_new[:,:-1] += AREA_old[:,1:] * direction[:,1:,1]
    AREA_new[1:,:-1] += AREA_old[:-1,1:] * direction[:-1,1:,2]
    AREA_new[:-1,:] += AREA_old[1:,:] * direction[1:,:,3]
    AREA_new[1:,:] += AREA_old[:-1,:] * direction[:-1,:,4]
    AREA_new[:-1,1:] += AREA_old[1:,:-1] * direction[1:,:-1,5]
    AREA_new[:,1:] += AREA_old[:,:-1] * direction[:,:-1,6]
    AREA_new[1:,1:] += AREA_old[:-1,:-1] * direction[:-1,:-1,7]
    
    flow_array[:,:,:] = 0
    flow_array[:,:,0][AREA_new > 0] = 255 * (0.75 -  0.75 * np.log(AREA_new[AREA_new > 0]) / np.log(np.max(AREA) + 0.01))
    flow_array[:,:,1][AREA_new > 0] = 255 * (0.75 -  0.75 * np.log(AREA_new[AREA_new > 0]) / np.log(np.max(AREA) + 0.01))
    flow_array[:,:,2][AREA_new > 0] = 255
    
    prev_array[:,:,:] = 0
    if pygame.mouse.get_pressed()[2]:
        prev_array[:,:,0][(coordinates[:,:,0] - x_mouse) ** 2.0 + (coordinates[:,:,1] - y_mouse) ** 2.0 < rad ** 2.0] = 150
        prev_array[:,:,1][(coordinates[:,:,0] - x_mouse) ** 2.0 + (coordinates[:,:,1] - y_mouse) ** 2.0 < rad ** 2.0] = 150
        prev_array[:,:,2][(coordinates[:,:,0] - x_mouse) ** 2.0 + (coordinates[:,:,1] - y_mouse) ** 2.0 < rad ** 2.0] = 255

    #HYDROGRAPH
    frame_number +=1
    if plot_every_frame <= frame_number:
        frame_number = 0
        Q[:-1] = Q[1:]
        Q[-1] = float(AREA_new[x_hydro][y_hydro]) / float(base_flow)
        plot_hydro = plot_setup(plot_hydro,t,Q,r'$t$ [$T$]',r'$Q/Q_b$ [$L^3/T$]',np.max(AREA)/base_flow)
        plot_to_surface = pygame.surfarray.make_surface(plot_hydro)
        gameDisplay.blit(plot_to_surface,(0,res_height*scale))
                                          
    #DEM surface
    DEM_surface = pygame.surfarray.make_surface(DEM_array)
    DEM_surface_scaled = pygame.transform.scale(DEM_surface,(res_width * scale,int(res_height * scale)))
    gameDisplay.blit(DEM_surface_scaled,(0,0))

    #aerial surface
    aerial_alpha = transparency_list[transparency_int - 1]
    aerial_surface_scaled.set_alpha(aerial_alpha)
    gameDisplay.blit(aerial_surface_scaled,(0,0))

    # flow surface
    flow_surface = pygame.surfarray.make_surface(flow_array)
    flow_surface_scaled = pygame.transform.scale(flow_surface,(res_width * scale,int(res_height * scale)))
    flow_surface_scaled.set_colorkey((0,0,0))
    gameDisplay.blit(flow_surface_scaled,(0,0))

    # preview surface
    prev_surface = pygame.surfarray.make_surface(prev_array)
    prev_surface_scaled = pygame.transform.scale(prev_surface,(res_width * scale,int(res_height * scale)))
    prev_surface_scaled.set_alpha(100)
    prev_surface_scaled.set_colorkey((0,0,0))
    gameDisplay.blit(prev_surface_scaled,(0,0))

    #update area array
    AREA_old[:,:] = AREA_new[:,:]
    AREA_new[:,:] = 0
    
    #update screen
    pygame.display.update()
    clock.tick(f_rate)      
            

#unintialize and quit pygame
pygame.quit()
quit()
