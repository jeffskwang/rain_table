#python game
#written by jeffrey kwang
#email: jeffskwang@gmail.com
#version = alpha_1

############################
###LIBRARIES###
############################

# import pygame
import os
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
# import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import events
import utils
from PIL import Image

import widgets
from slider_manager import SliderManager, MiniManager, SliderVal

class GUI(object):

    """     
    main GUI object that selects parameters for initialization and
    handles creation of all the needed parts of the model. This class is
    initialized below by class Runner if this file is run as __main__ 
    """

    def __init__(self):
        # initial conditions
        self._paused = False
        
        # setup the figure
        plt.rcParams['toolbar'] = 'None'
        plt.rcParams['figure.figsize'] = 12, 8
        # self.fig, (self.map_ax, self.graph_ax) = plt.subplots(2, 1)
        self.fig = plt.figure()
        self.map_ax = self.fig.add_axes((0, 0.45, 1, 0.5))
        self.graph_ax = self.fig.add_axes((0.5, 0.1, 0.45, 0.30))
        # plt.subplots_adjust(left=0, top=1, right=1, bottom=0.45)
        self.fig.canvas.set_window_title('SedEdu -- drainage basin simulation')
        self.map_ax.get_xaxis().set_visible(False)
        self.map_ax.get_yaxis().set_visible(False)

        # self.fig.subplots()
        
        # self.map_ax.set_xlabel("channel belt (km)")
        # self.map_ax.set_ylabel("stratigraphy (m)")
        # plt.ylim(-config.yView, 0.1*config.yView)
        # plt.xlim(-config.Bb/2, config.Bb/2)
        # self.map_ax.xaxis.set_major_formatter( plt.FuncFormatter(
                            # lambda v, x: str(v / 1000).format('%0.0f')) )

        # add sliders
        self.config = utils.Config

        self.config.baseflowmin = 500
        self.config.baseflowmax = 3000
        self.config.baseflowinit = 2000
        self.config.baseflowstep = 100

        self.config.cloudmin = 50
        self.config.cloudmax = 200
        self.config.cloudinit = 100
        self.config.cloudstep = 10

        self.config.transpmin = 0
        self.config.transpmax = 100
        self.config.transpinit = 20
        self.config.transpstep = 10

        self.config._toggle_stream = True


        self.sm = SliderManager(self)


    def pause_anim(self, event):
        """
        pause animation by altering hidden var
        """
        if self._paused:
            self._paused = False
        else:
            self._paused = True


class Map(object):
    def __init__(self, gui):

        # add_ax
        self.gui = gui
        self.fig = gui.fig
        self.map_ax = gui.map_ax
        self.config = gui.config
        self.sm = gui.sm
        self.sm.get_all()
        self.mm = MiniManager() # handles some switch params

        ############################
        ###PARAMETERS###
        ############################
        #scale of screen_res / DEM_res
        self.scale = 3


        ############################
        ###RASTERS###
        ############################

        #this path
        self.this_dir = os.path.dirname(__file__)
        self.this_path = os.path.join(self.this_dir,'')
        self.priv_path = os.path.abspath(os.path.join(self.this_path, os.pardir, 'private'))

        #load dem
        _DEM = np.loadtxt(os.path.join(self.priv_path, 'dem.txt'),skiprows=6)
        self.DEM = _DEM
        self.res_height,self.res_width = self.DEM.shape
        self.min_ele = np.min(self.DEM[self.DEM!=-9999])
        self.max_ele = np.max(self.DEM)
        self.DEM[self.DEM==-9999] = self.min_ele

        #load drainage area
        self.AREA = np.loadtxt(os.path.join(self.priv_path, 'area.txt'),skiprows=6)

        #0|1|2
        #3|x|4
        #5|6|7
        #load direction, covert the arcgis direction values to values between 0 and 7
        self.DIR = np.loadtxt(os.path.join(self.priv_path, 'dir.txt'),dtype = int, skiprows=6)
        self.DIR[self.DIR==8] = 5
        self.DIR[self.DIR==4] = 6
        self.DIR[self.DIR==2] = 7
        self.DIR[self.DIR==1] = 4
        self.DIR[self.DIR==32] = 0
        self.DIR[self.DIR==64] = 1
        self.DIR[self.DIR==128] = 2 
        self.DIR[self.DIR==16] = 3

        ############################
        ###INITIALIZATION###
        ############################
        

      
        #threshold for channelization
        self._baseflow = SliderVal(self.sm.baseflow)
        self.baseflow_threshold = self.config.baseflowmax - self._baseflow.val

        # cloud sizes
        self._cloud = SliderVal(self.config.cloudinit)

        #define a base flow to scale hydrograph
        self.base_flow = 2539

        #hydrograph gauge location
        self.y_hydro, self.x_hydro = np.unravel_index(self.AREA.argmax(), self.AREA.shape)

        #aerial photo
        self.aerial_image = Image.open(os.path.join(self.priv_path, 'aerial.png'))
        self.aerial_array = np.array(self.aerial_image)
        self.aerial_array[:, :, 3] = (1 - (self.config.transpinit / 100)) * 255
        # self._aerial_alpha_changed = False
      
        #contols
        # controls_surface = pygame.image.load(os.path.join(priv_path, 'rain_table_controls.png'))
        # controls_surface_scaled  = pygame.transform.scale(controls_surface,(int(res_height * scale * 0.5),int(res_height * scale * 0.5)))
        # gameDisplay.blit(controls_surface_scaled,(res_width*scale - int(res_height*scale * 0.5),res_height*scale))

        ############################
        ###ARRAYS###
        ############################
        self.DEM_array = np.zeros((self.res_width,self.res_height),dtype=int)
        self.flow_array = np.zeros((self.res_width,self.res_height,4),dtype=int)
        self.prev_array = np.zeros((self.res_width,self.res_height,4),dtype=int)
        self.AREA_old = np.zeros((self.res_width,self.res_height),dtype=int)
        self.AREA_new = np.zeros((self.res_width,self.res_height),dtype=int)

        #hydrograph plot
        # self.plot_hydro = np.zeros((int(self.res_width * self.scale)-int(self.res_height*0.5*self.scale),int(self.res_height*0.5*self.scale),3),dtype=int)

        #hyrograph arrays
        self.t = np.linspace(-100.,0.0,1001)
        self.Q = np.zeros(1001)

        #predifined area thresholds
        # self.baseflow_threshold_list = np.concatenate((np.zeros(1),np.logspace(0,np.log10(np.max(self.AREA)),29)),axis=0)

        #setup direction array
        self.direction = np.zeros((self.res_width,self.res_height,8),dtype=int)
        for i in np.arange(0,8):
            self.direction[:,:,i][np.transpose(self.DIR)==i] = 1

        #coordinate array
        self.coordinates = np.zeros((self.res_width,self.res_height,2))
        for x_temp in np.arange(0,self.res_width):
            for y_temp in np.arange(0,self.res_height):
                self.coordinates[x_temp,y_temp,0] = x_temp * self.scale
                self.coordinates[x_temp,y_temp,1] = y_temp * self.scale

        #DEM array
        self.DEM_array[:,:] = (np.transpose(self.DEM) - self.min_ele) / (self.max_ele - self.min_ele) * 255

        #DEM surface artists for plotting
        self.DEM_cmap = utils.terrain_cmap()
        self.DEM_surface = self.map_ax.imshow(np.transpose(self.DEM_array), cmap=self.DEM_cmap) # , origin="lower"
        self.aerial_surface = self.map_ax.imshow(self.aerial_array, extent=[-1, self.res_width, -1, self.res_height], origin='lower')
        self.flow_surface = self.map_ax.imshow(np.transpose(self.flow_array, axes=(1,0,2)))
        self.prev_surface = self.map_ax.imshow(np.transpose(self.prev_array, axes=(1,0,2)))


        # connect press events
        mouseon_cid = self.fig.canvas.mpl_connect('button_press_event', lambda e: events.on_click(e, self.mm))
        mouseoff_cid = self.fig.canvas.mpl_connect('button_release_event', lambda e: events.off_click(e, self.mm))
        mousemv_cid = self.fig.canvas.mpl_connect('motion_notify_event', lambda e: events.mouse_move(e, self.mm, self.map_ax, self.scale))
        
        key_cid = self.fig.canvas.mpl_connect('key_press_event', lambda e: events.on_key(e, self))

        # dedicated action for transparency slider
        transp_changed = self.sm.slide_transp.on_changed(lambda e: events.transp_slider_action(e,
                                                                             self.aerial_array,
                                                                             self.aerial_surface))

        # dedicated action for baseflow slider
        baseflow_changed = self.sm.slide_baseflow.on_changed(lambda e: events.slider_set_to(e,
                                                                             self._baseflow))

        # dedicated action for cloud slider
        cloud_changed = self.sm.slide_cloud.on_changed(lambda e: events.slider_set_to(e,
                                                                             self._cloud))


    def __call__(self, i):

        #toggle base_flow
        if self.mm._toggle_stream:
            self.baseflow_threshold = self.config.baseflowmax - self._baseflow.val + self.config.baseflowstep
            self.AREA_old[np.transpose(self.AREA) >= self.baseflow_threshold ] += 1

        # mouse_move   
        if self.mm._lclicked:
            if self.mm._inax:
                self.cloud = self._cloud.val
                self.AREA_old[(self.coordinates[:,:,0] - self.mm._mx) ** 2.0 + (self.coordinates[:,:,1] - self.mm._my) ** 2.0 < self.cloud ** 2.0] += 1

        self.prev_array[:,:,:] = 0
        if self.mm._rclicked:
            if self.mm._inax:
                self.cloud = self._cloud.val
                self.prev_array[:,:,0][(self.coordinates[:,:,0] - self.mm._mx) ** 2.0 + (self.coordinates[:,:,1] - self.mm._my) ** 2.0 < self.cloud ** 2.0] = 150
                self.prev_array[:,:,1][(self.coordinates[:,:,0] - self.mm._mx) ** 2.0 + (self.coordinates[:,:,1] - self.mm._my) ** 2.0 < self.cloud ** 2.0] = 150
                self.prev_array[:,:,2][(self.coordinates[:,:,0] - self.mm._mx) ** 2.0 + (self.coordinates[:,:,1] - self.mm._my) ** 2.0 < self.cloud ** 2.0] = 255
                self.prev_array[:,:,3][(self.coordinates[:,:,0] - self.mm._mx) ** 2.0 + (self.coordinates[:,:,1] - self.mm._my) ** 2.0 < self.cloud ** 2.0] = 100

        #ROUTE THE RAINFALL
        self.AREA_new[ :-1,  :-1] += self.AREA_old[1:  , 1:  ] * self.direction[1:  , 1:  , 0]
        self.AREA_new[ :  ,  :-1] += self.AREA_old[ :  , 1:  ] * self.direction[ :  , 1:  , 1]
        self.AREA_new[1:  ,  :-1] += self.AREA_old[ :-1, 1:  ] * self.direction[ :-1, 1:  , 2]
        self.AREA_new[ :-1,  :  ] += self.AREA_old[1:  ,  :  ] * self.direction[1:  ,  :  , 3]
        self.AREA_new[1:  ,  :  ] += self.AREA_old[ :-1,  :  ] * self.direction[ :-1,  :  , 4]
        self.AREA_new[ :-1, 1:  ] += self.AREA_old[1:  ,  :-1] * self.direction[1:  ,  :-1, 5]
        self.AREA_new[ :  , 1:  ] += self.AREA_old[ :  ,  :-1] * self.direction[ :  ,  :-1, 6]
        self.AREA_new[1:  , 1:  ] += self.AREA_old[ :-1,  :-1] * self.direction[ :-1,  :-1, 7]
        
        #UPDATE THE FLOW ARRAY
        self.flow_array[:,:,:] = 0
        self.flow_array[:,:,0][self.AREA_new > 0] = 255 * (0.75 -  0.75 * np.log(self.AREA_new[self.AREA_new > 0]) / np.log(np.max(self.AREA) + 0.01))
        self.flow_array[:,:,1][self.AREA_new > 0] = 255 * (0.75 -  0.75 * np.log(self.AREA_new[self.AREA_new > 0]) / np.log(np.max(self.AREA) + 0.01))
        self.flow_array[:,:,2][self.AREA_new > 0] = 255
        self.flow_array[:,:,3][self.AREA_new > 0] = 255

        #HYDROGRAPH
        # frame_number +=1
        # if plot_every_frame <= frame_number:
            # frame_number = 0
            # Q[:-1] = Q[1:]
            # Q[-1] = float(AREA_new[x_hydro][y_hydro]) / float(base_flow)
            # plot_hydro = plot_setup(plot_hydro,t,Q,r'$t$ [$T$]',r'$Q/Q_b$ [$L^3/T$]',np.max(AREA)/base_flow)
            # plot_to_surface = pygame.surfarray.make_surface(plot_hydro)
            # gameDisplay.blit(plot_to_surface,(0,res_height*scale))
        
        # flow surface
        self.flow_surface.set_data(np.transpose(self.flow_array, axes=(1,0,2)))

        # preview surface
        if np.any(self.prev_surface):
            self.prev_surface.set_data(np.transpose(self.prev_array, axes=(1,0,2)))

        # aerial image surface
        #    The alpha here gets updated outside the
        #    loop, in an action in events.py. This is because it only
        #    happens rarely and checking for the change and reseting on
        #    every loop was a lot of overhead.

        #update area array
        self.AREA_old[:,:] = self.AREA_new[:,:]
        self.AREA_new[:,:] = 0

        return self.DEM_surface, self.aerial_surface, \
               self.flow_surface, self.prev_surface




############################
###PYGAME###
############################

#initialize pygame
# x = pygame.init()

#make game display
# gameDisplay = pygame.display.set_mode((scale*res_width,int(scale*res_height * 1.5)))

#set title of game
# pygame.display.set_caption('SedEdu -- Drainage basins')

#update screen
# pygame.display.update()

#set gameExit to false to enter the main loop
# gameExit = False

#set clock for framerate lock
# clock = pygame.time.Clock()



############################
###MAIN LOOP###
############################
# while not gameExit:
    #event handler (temp event) use pygame events, e.g. contains mouse data, keyboard presses
    # for event in pygame.event.get():
    #     #quit and leave the loop
    #     if event.type == pygame.QUIT:
    #         gameExit = True

    # #mouse location
    # (x_mouse,y_mouse) = pygame.mouse.get_pos()



    # if event.type == pygame.KEYUP:
    #     if event.key == pygame.K_SPACE:
    #         key_down = 0
    #     if event.key == pygame.K_UP:
    #         key_down = 0
    #     if event.key == pygame.K_DOWN:
    #         key_down = 0
    #     if event.key == pygame.K_LEFT:
    #         key_down = 0
    #     if event.key == pygame.K_RIGHT:
    #         key_down = 0
    
    # #mouse pressed
    # if pygame.mouse.get_pressed()[0]:
    #     AREA_old[(coordinates[:,:,0] - x_mouse) ** 2.0 + (coordinates[:,:,1] - y_mouse) ** 2.0 < rad ** 2.0] += 1


    
    #update screen
    # pygame.display.update()
    # clock.tick(f_rate)      
            

#unintialize and quit pygame
# pygame.quit()
# quit()

class Runner(object):
    def __init__(self):

        gui = GUI()

        gui.map = Map(gui)

        anim = animation.FuncAnimation(gui.fig, gui.map, 
                                       interval=10, blit=True)

        plt.show()



if __name__ == '__main__':
    runner = Runner()
