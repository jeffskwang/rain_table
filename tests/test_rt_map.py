import pytest
import platform

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np
import matplotlib



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline', remove_text=True)
def test_launch_fig_with_map():

    from rain_table.rain_table import GUI
    from rain_table.rain_table import Map


    gui = GUI()
    gui.map = Map(gui)

    return gui.fig

