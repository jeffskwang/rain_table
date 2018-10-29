import pytest
import platform

import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

import numpy as np
import matplotlib



@pytest.mark.mpl_image_compare(baseline_dir='figs_baseline')
def test_launch_fig():

    from rain_table.rain_table import GUI

    gui = GUI()
    return gui.fig
