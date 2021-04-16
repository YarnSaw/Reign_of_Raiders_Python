import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ['images','maps','text','music']
build_exe_options = {"packages": ["os"], "excludes": ["tkinter",'numpy'],'include_files':includefiles}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Reign of Raiders",
        version = "1.0",
        description = "Be the best raider around!",
        author = 'Clan of Raiders',
        options = {"build_exe": build_exe_options},
        executables = [Executable("Reign of Raiders.py", base=base,
                                  icon = 'ror icon.ico')])

#use python setup.py bdist_msi


'''
use this stuff here in the main game, where you load the files. what it does is check
to see if the game was frozen (ie an exe file) to go through the files

def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = path.dirname(__file__)
    return path.join(datadir, filename)

map_folder = find_data_file('maps')
img_folder = find_data_file('images')
text_folder = find_data_file('text')
music_folder = find_data_file('music')
'''
