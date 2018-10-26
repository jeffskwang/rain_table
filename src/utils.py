
from matplotlib.colors import LinearSegmentedColormap

def terrain_cmap():
    cdict = {'red':     ((0,    0.2,            0.2),
                        (0.125, 0.50588,            0.50588),
                        (0.25,  1,          1),
                        (0.5,   0.95686,            0.95686),
                        (0.625, 0.4,            0.4),
                        (0.75,  0.4,            0.4),
                        (1,     1,          1)),
             'green':   ((0,    0.4,            0.4),
                        (0.125, 0.76471,            0.76471),
                        (0.25,  1,          1),
                        (0.5,   0.74118,            0.74118),
                        (0.625, 0.2,            0.2),
                        (0.75,  0.2,            0.2),
                        (1,     1,          1)),
             'blue':    ((0,    0,          0),
                        (0.125, 0.12157,            0.12157),
                        (0.25,  0.8,            0.8),
                        (0.5,   0.27059,            0.27059),
                        (0.625, 0.047059,           0.047059),
                        (0.75,  0,          0),
                        (1,     1,          1))
             }

    return LinearSegmentedColormap('terrain2', cdict)


class Config: 
    """
    dummy config class for storing info during generation of GUI
    """

    pass

