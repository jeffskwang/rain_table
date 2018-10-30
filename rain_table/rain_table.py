
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

from . import events
from . import utils
from . import widgets
from .slider_manager import SliderManager, MiniManager, Val

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
        self.fig = plt.figure()
        self.fig.canvas.set_window_title('SedEdu -- drainage basin simulation')
        
        self.map_ax = self.fig.add_axes((0, 0.45, 1, 0.5))
        self.map_ax.get_xaxis().set_visible(False)
        self.map_ax.get_yaxis().set_visible(False)

        self.graph_ax = self.fig.add_axes((0.5, 0.1, 0.45, 0.30))
        self.graph_ax.set_xlabel("time (hr)")
        self.graph_ax.set_ylabel("relative discharge (-)")


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

        # self.config._toggle_stream = True

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


        self.gui = gui
        self.fig = gui.fig
        self.map_ax = gui.map_ax
        self.graph_ax = gui.graph_ax
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
        self._toggle_stream = Val(True)
        self._baseflow = Val(self.sm.baseflow)
        self.baseflow_threshold = self.config.baseflowmax - self._baseflow.val

        # cloud sizes
        self._cloud = Val(self.config.cloudinit)

        #aerial photo
        self.aerial_image = Image.open(os.path.join(self.priv_path, 'aerial.png'))
        self.aerial_array = np.array(self.aerial_image)
        self.aerial_array[:, :, 3] = (1 - (self.config.transpinit / 100)) * 255

        ############################
        ###ARRAYS###
        ############################
        self.DEM_array = np.zeros((self.res_width,self.res_height),dtype=int)
        self.flow_array = np.zeros((self.res_width,self.res_height,4),dtype=int)
        self.prev_array = np.zeros((self.res_width,self.res_height,4),dtype=int)
        self.AREA_old = np.zeros((self.res_width,self.res_height),dtype=int)
        self.AREA_new = np.zeros((self.res_width,self.res_height),dtype=int)

        #hydrograph gauge location
        self.hydro_y, self.hydro_x = np.unravel_index(self.AREA.argmax(), self.AREA.shape)
        self.hydro_m = 1812 
        self.hydro_f = 1/600 # hydrograph scaling factor to convert mm/hr per pixel to m3/s (not used)
        self.hydro_nqw = 1000
        self.hydro_t_min = -240
        self.hydro_t = np.linspace(self.hydro_t_min, 0, self.hydro_nqw)
        self.qw = np.repeat(0.0001, self.hydro_nqw)

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

        # hydrograph plot artists
        
        self.bfull_line = self.graph_ax.plot([self.hydro_t_min, -self.hydro_t_min*0.1], [1, 1], ls='--', color='k')
        self.bfull_text = self.graph_ax.text(self.hydro_t_min*0.95, 1.1, 'bankfull discharge')
        self.hydrograph, = self.graph_ax.plot(self.hydro_t, self.qw)
        self.graph_ax.set_ylim(0, 3)
        self.graph_ax.set_xlim(self.hydro_t_min, -self.hydro_t_min*0.1)

        # prefill flow array with equilib
        # self.AREA_old[np.transpose(self.AREA) >= self.baseflow_threshold ] = np.transpose(self.AREA[(self.AREA) >= self.baseflow_threshold ])  

        # connect press events
        mouseon_cid  = self.fig.canvas.mpl_connect('button_press_event', 
                                                   lambda e: events.on_click(e, self.mm))
        mouseoff_cid = self.fig.canvas.mpl_connect('button_release_event', 
                                                   lambda e: events.off_click(e, self.mm))
        mousemv_cid  = self.fig.canvas.mpl_connect('motion_notify_event', 
                                                   lambda e: events.mouse_move(e, self.mm, 
                                                   self.map_ax, self.scale))
        
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

        # stream toggle switch handler
        stream_changed = self.sm.chk_baseflow.on_clicked(lambda e: events.check_switch(e,
                                                                             self._toggle_stream))


    def __call__(self, i):

        # toggle base_flow
        if self._toggle_stream.val:
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

        # ROUTE THE RAINFALL
        self.AREA_new[ :-1,  :-1] += self.AREA_old[1:  , 1:  ] * self.direction[1:  , 1:  , 0]
        self.AREA_new[ :  ,  :-1] += self.AREA_old[ :  , 1:  ] * self.direction[ :  , 1:  , 1]
        self.AREA_new[1:  ,  :-1] += self.AREA_old[ :-1, 1:  ] * self.direction[ :-1, 1:  , 2]
        self.AREA_new[ :-1,  :  ] += self.AREA_old[1:  ,  :  ] * self.direction[1:  ,  :  , 3]
        self.AREA_new[1:  ,  :  ] += self.AREA_old[ :-1,  :  ] * self.direction[ :-1,  :  , 4]
        self.AREA_new[ :-1, 1:  ] += self.AREA_old[1:  ,  :-1] * self.direction[1:  ,  :-1, 5]
        self.AREA_new[ :  , 1:  ] += self.AREA_old[ :  ,  :-1] * self.direction[ :  ,  :-1, 6]
        self.AREA_new[1:  , 1:  ] += self.AREA_old[ :-1,  :-1] * self.direction[ :-1,  :-1, 7]
        
        # UPDATE THE FLOW ARRAY
        self.flow_array[:,:,:] = 0
        color_factor = (0.75 -  0.75 * np.log(self.AREA_new[self.AREA_new > 0]) / np.log(np.max(self.AREA) + 0.01))
        self.flow_array[:,:,0][self.AREA_new > 0] = 255 * color_factor
        self.flow_array[:,:,1][self.AREA_new > 0] = 255 * color_factor
        self.flow_array[:,:,2][self.AREA_new > 0] = 255
        self.flow_array[:,:,3][self.AREA_new > 0] = 255

        # UPDATE THE HYDROGRAPH
        self.qw[:-1] = self.qw[1:]
        self.qw[-1] = ((self.AREA_new[self.hydro_x][self.hydro_y]) / self.hydro_m)
        self.hydrograph.set_ydata(self.qw)

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
               self.flow_surface, self.prev_surface, self.hydrograph



class Runner(object):
    def __init__(self):

        gui = GUI()

        gui.map = Map(gui)

        anim = animation.FuncAnimation(gui.fig, gui.map, 
                                       interval=10, blit=True)

        plt.show()

        # plt.figure()
        # plt.imshow(gui.map.AREA)
        # plt.show()




if __name__ == '__main__':
    runner = Runner()
