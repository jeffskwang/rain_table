import matplotlib.pyplot as plt

from . import widgets
from . import utils

class SliderManager(object):
    def __init__(self, gui):

        # self._toggle_stream = True

        widget_color = 'lightgoldenrodyellow'

        # inputs of ranges to initialize
        slide_baseflow_ax = plt.axes([0.16, 0.35, 0.215, 0.05], facecolor=widget_color)
        self.slide_baseflow = widgets.MinMaxSlider(slide_baseflow_ax, 'baseflow threshold (m$^2$)', 
                                        gui.config.baseflowmin, gui.config.baseflowmax, 
                                        valinit=gui.config.baseflowinit, valstep=gui.config.baseflowstep, 
                                        valfmt="%0.0f", transform=gui.map_ax.transAxes)

        slide_cloud_ax = plt.axes([0.075, 0.225, 0.3, 0.05], facecolor=widget_color)
        self.slide_cloud = widgets.MinMaxSlider(slide_cloud_ax, 'cloud radius (km)', 
                                         gui.config.cloudmin, gui.config.cloudmax, 
                                         valinit=gui.config.cloudinit, valstep=gui.config.cloudstep, 
                                         valfmt="%g", transform=gui.map_ax.transAxes)

        slide_transp_ax = plt.axes([0.075, 0.1, 0.3, 0.05], facecolor=widget_color)
        self.slide_transp = widgets.MinMaxSlider(slide_transp_ax, 'image transparency (%)', 
                                        gui.config.transpmin, gui.config.transpmax, 
                                        valinit=gui.config.transpinit, valstep=gui.config.transpstep, 
                                        valfmt="%i", transform=gui.map_ax.transAxes)

        chk_baseflow_ax = plt.axes([0.075, 0.35, 0.05, 0.05], facecolor=widget_color)
        self.chk_baseflow = widgets.TightCheckButtons(chk_baseflow_ax, ('on',), (True,))
        
        # btn_slidereset_ax = plt.axes([0.565, 0.14, 0.2, 0.04])
        # self.btn_slidereset = widgets.NoDrawButton(btn_slidereset_ax, 'Reset sliders', color=widget_color, hovercolor='0.975')
        # # self.btn_slidereset.on_clicked(gui.slide_reset)
        # self.btn_slidereset.on_clicked(lambda x: utils.slide_reset(event=x, gui=gui))

        # btn_axisreset_ax = plt.axes([0.565, 0.09, 0.2, 0.04])
        # self.btn_axisreset = widgets.NoDrawButton(btn_axisreset_ax, 'Reset stratigraphy', color=widget_color, hovercolor='0.975')
        # # self.btn_axisreset.on_clicked(gui.strat_reset)
        # self.btn_axisreset.on_clicked(lambda x: utils.strat_reset(event=x, gui=gui))

        # btn_pause_ax = plt.axes([0.565, 0.03, 0.2, 0.04])
        # self.btn_pause = widgets.NoDrawButton(btn_pause_ax, 'Pause', color=widget_color, hovercolor='0.975')
        # self.btn_pause.on_clicked(gui.pause_anim)

        self.get_all()

    def get_calculation_options(self):
        # self.Bb = self.slide_Bb.val * 1000
        self.baseflow = self.slide_baseflow.val
        self.cloud = self.slide_cloud.val
        

    def get_all(self):
        # self.get_display_options()
        self.get_calculation_options()


class Val(object):
    """generic value holder"""
    def __init__(self, val):
        self.val = val

class MiniManager(object):
    def __init__(self):
        self._lclicked = False
        self._rclicked = False
        self._inax = False
        # self._toggle_stream = True
        self._baseflow = 2000
