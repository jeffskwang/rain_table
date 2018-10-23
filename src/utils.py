
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
