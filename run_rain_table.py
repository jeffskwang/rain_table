import os, sys

# the file location
this_dir = os.path.dirname(__file__)

# if commands given
if len(sys.argv) > 1:
    # argument for python 3 runtime
    if sys.argv[1] == '--python3':
        os.system('python3 ' + os.path.join(this_dir, 'src', 'rain_table.py'))
    else:
        os.system('python ' + os.path.join(this_dir, 'src', 'rain_table.py'))
else: 
    os.system('python ' + os.path.join(this_dir, 'src', 'rain_table.py'))
