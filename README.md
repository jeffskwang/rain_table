# rain_table

Interactive rain table model written by Jeffrey Kwang at UIUC.

<img src="https://github.com/sededu/rain_table/blob/master/private/rain_table_demo.gif" alt="demo_gif">


The version in this (SedEdu) repository is different than the original by Jeffrey.
This version retains most of the functionality, but does not rely on the Pygame dependency.
The cost is that this simulation runs a little bit slower, but is still fast enough to be fun.
[See Jeffrey's original implementation at here.](https://github.com/jeffskwang/rain_table)

This repository is also linked into the [SedEdu suite of education modules](https://github.com/sededu/sededu), and can be accessed there as well.


## About the model

The model uses a D8 routing scheme to route rainfall over the surface of a DEM.
All flow is assumed to be surface runoff.
The hydrograph is scaled to the maximum baseflow equilibrium condition. 
These watersheds drain directly into the Columbia River in Washington state, (Lat 47°10'03.8"N, Lon 120°07'31.9"W).



## Installing the module

This module depends on Python 3, `tkinter`, and the Python packages `numpy`, `pillow`, and `matplotlib`. 


### Installing Python 3

If you are new to Python, it is recommended that you install Anaconda, which is an open source distribution of Python which includes many basic scientific libraries, some of which are used in the module. 
Anaconda can be downloaded at https://www.anaconda.com/download/ for Windows, macOS, and Linux. 
If you do not have storage space on your machine for Anaconda or wish to install a smaller version of Python for another reason, see below on options for Miniconda or vanilla Python.

1. Visit the website for Anaconda https://www.anaconda.com/download/ and select the installer for your operating system.
__Be sure to select the Python 3.x installation.__
2. Start the installer.
3. If prompted, select to "install just for me", unless you know what you are doing.
4. When prompted to add Anaconda to the path during installation, select _yes_ if you __know__ you do not have any other Python installed on your computer; otherwise select _no_.

See below for detailed instructions on installing `rain_table` for your operating system.


### Installing the module

If you installed Anaconda Python or Miniconda, you can follow the instructions below for your operating system. 
Otherwise see the instructions for PyPi installation below.

__Please__ [open an issue](https://github.com/sededu/rain_table/issues) if you encounter any troubles installing or any error messages along the way! 
Please include 1) operating system, 2) installation method, and 3) copy-paste the error.


#### Windows users

1. Open your "start menu" and search for the "Anaconda prompt"; start this application.

2. Install with the module type the following command and hit "enter":
```
conda install -c sededu rain_table
```
If asked to proceed, type `Y` and press "enter" to continue installation. 
3. This process may take a few minutes as the necessary source code is downloaded.
If the installation succeeds, proceed below to the "Run the module" section.

__Note on permissions:__ you may need to run as administrator on Windows.


#### Mac OSX and Linux users

__Linux users:__ you will need to also install `tkinter` before trying to install the module below package through `conda` or `pip3`.
On Ubuntu this is done with `sudo apt install python3-tk`.
<!-- Windows and Mac distributions should come with `python3-tk` installed. -->

1. Install the module by opening a terminal and typing the following command.
```
conda install -c sededu rain_table
```
If asked to proceed, type `Y` and press enter to continue installation.

2. This process may take a few minutes as the necessary source code is downloaded.
If the installation succeeds, proceed below to the "Run the module" section.

__Note on permissions:__ you may need to use `sudo` on OSX and Linux.


#### Advanced user installations
To install with `pip` from Pypi use (not recommended for entry-level users):
```
pip3 install pyqt rain_table
```

See below instructions for downloading the source code if you wish to be able to modify the source code for development or for exploration.


### Run the module

1. Open a Python shell by typing `python` (or `python3`) at the terminal (OSX and Linux users) or at the Conda or Command Prompt (Windows users).
2. Run the module from the Python shell with:
```
import rain_table
```
Instructions will indicate to use the following command to then run the module:
```
rain_table.run()
```

Alternatively, you can do this in one line from the standard terminal with:
```
python -c "import rain_table; rain_table.run()"
```

Alternatively, run the module with provided script (this is the hook used for launching from SedEdu):
```
python3 <path-to-installation>run_rain_table.py
```

Please [open an issue](https://github.com/sededu/rain_table/issues) if you encounter any additional error messages! 
Please include 1) operating system, 2) installation method, and 3) copy-paste the error.


#### Smaller Python installation options
Note that if you do not want to install the complete Anaconda Python distribution you can install [Miniconda](https://conda.io/miniconda.html) (a smaller version of Anaconda), or you can install Python alone and use a package manager called pip to do the installation. 
You can get [Python and pip together here](https://www.python.org/downloads/).



