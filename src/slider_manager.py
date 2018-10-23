import matplotlib.pyplot as plt

import widgets
import utils

class SliderManager(object):
    def __init__(self, gui):

        self._toggle_stream = True

        widget_color = 'lightgoldenrodyellow'

        # inputs of ranges to initialize
        slide_baseflow_ax = plt.axes([0.565, 0.275, 0.36, 0.05], facecolor=widget_color)
        self.slide_baseflow = widgets.MinMaxSlider(slide_baseflow_ax, 'baseflow discharge (m$^3$/s)', 
                                        gui.config.baseflowmin, gui.config.baseflowmax, 
                                        valinit=gui.config.baseflowinit, valstep=gui.config.baseflowstep, 
                                        valfmt="%0.0f", transform=gui.map_ax.transAxes)

        slide_cloud_ax = plt.axes([0.565, 0.175, 0.36, 0.05], facecolor=widget_color)
        self.slide_cloud = widgets.MinMaxSlider(slide_cloud_ax, 'cloud radius (km)', 
                                         gui.config.cloudmin, gui.config.cloudmax, 
                                         valinit=gui.config.cloudinit, valstep=gui.config.cloudstep, 
                                         valfmt="%g", transform=gui.map_ax.transAxes)

        # slide_Ta_ax = plt.axes([0.565, 0.665, 0.36, 0.05], facecolor=widget_color)
        # self.slide_Ta = widgets.MinMaxSlider(slide_Ta_ax, 'avulsion timescale (yr)', 
        #                                 gui.config.Tamin, gui.config.Tamax, 
        #                                 valinit=gui.config.Tainit, valstep=gui.config.Tastep, 
        #                                 valfmt="%i", transform=gui.map_ax.transAxes)

        # rad_col_ax = plt.axes([0.565, 0.45, 0.225, 0.15], facecolor=widget_color)
        # self.rad_col = widgets.RadioButtons(rad_col_ax, ('Deposit age', 
        #                                             'Water discharge',
        #                                             'Subsidence rate',
        #                                             'Avulsion number'))
        
        # slide_yView_ax = plt.axes([0.565, 0.345, 0.36, 0.05], facecolor=widget_color)
        # self.slide_yView = widgets.MinMaxSlider(slide_yView_ax, 'stratigraphic view (m)', 
        #                                    gui.config.yViewmin, gui.config.yViewmax, 
        #                                    valinit=gui.config.yViewinit, valstep=gui.config.yViewstep, 
        #                                    valfmt="%i", transform=gui.map_ax.transAxes)

        # slide_Bb_ax = plt.axes([0.565, 0.24, 0.36, 0.05], facecolor=widget_color)
        # self.slide_Bb = widgets.MinMaxSlider(slide_Bb_ax, 'Channel belt width (km)', 
        #                                 gui.config.Bbmin, gui.config.Bbmax, 
        #                                 valinit=gui.config.Bbinit/1000, valstep=gui.config.Bbstep, 
        #                                 valfmt="%g", transform=gui.map_ax.transAxes)

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

        # # initialize a few more things
        # self.col_dict = {'Water discharge': 'baseflow', 
        #             'Avulsion number': 'avul',
        #             'Deposit age': 'age',
        #             'Subsidence rate':'cloud'}

        # read the sliders for values
        self.get_all()
        # self.D50 = gui.config.D50
        # self.cong = gui.config.cong
        # self.Rep = gui.config.Rep
        # self.dt = gui.config.dt
        # self.Df = gui.config.Df
        # self.Bast = gui.config.Bast
        # self.dxdtstd = gui.config.dxdtstd
        # self.Bbmax = gui.config.Bbmax
        # self.yViewmax = gui.config.yViewmax

    def get_display_options(self):
        # self.colFlag = self.col_dict[self.rad_col.value_selected]
        # self.yView = self.slide_yView.val
        pass

    def get_calculation_options(self):
        # self.Bb = self.slide_Bb.val * 1000
        self.baseflow = self.slide_baseflow.val
        self.cloud = self.slide_cloud.val
        # self.Ta = self.slide_Ta.val

    def get_all(self):
        self.get_display_options()
        self.get_calculation_options()