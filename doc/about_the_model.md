## About the model

(1) `rain_table.py`: This file contains the source code to run the rain table simulation. Simply run the model in python, and click the screen to drop rain on the screen. The rain will be routed on the landscape in accordance to the d8, steepest decent algorithm (see O’Callaghan and Mark, 1984).

(2) `dem.txt`: this file contains the digital elevaiton model that is rendered on the screen. This DEM's source is the 1/3 arcsecond USGS DEM product. These watershesd drainge diredtly into the Columbia River in Washington state (LOC: Lat 47°10'03.8"N, Long 120°07'31.9"W). File is a ersi formatted ascii.

(3) `dir.txt`: this file contains the d8 flow direction data. File is a ersi formatted ascii.

(4) `area.txt`: this file contains the drainage area data. File is a ersi formatted ascii.

(5) `erial.png` this is the aerial photograph of the drainage basin

Current user defined parameters in `rain_table.py`:
scale -> this parameter scales the original dem grid (pixel length by pixel width) to window that is [(pixel length x scale) by (pixel width x scale)]

rad -> this parameter controls the pixel radius of the rain cloud

f_rate -> this parameter controls the frame rate of the simulation. It is set to 60 as the default because most computer screens' refresh rates are 60 Hz.

alpha -> this parameters controls the transparency of the rain cloud.

## References

O’Callaghan, J. F. and Mark, D. M.: The extraction of drainage networks from digital elevation data, Computer Vision, Graphics, and Image Processing, 28(3), 323–344, doi:10.1016/S0734-189X(84)80011-0, 1984.