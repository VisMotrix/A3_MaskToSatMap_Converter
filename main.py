# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# ToDo
# 1 read and save layers cfg
# 2 Read in tile images
# 3 Read mask
# 4 refer mask color to tile image by layers cfg
# 5 create Satmap
import re
from dataclasses import dataclass

from pathlib import Path
import numpy as np

@dataclass
class Surface:
    name: str = ""
    path: str = "path"
    color: tuple[int,int,int] = (255, 255, 255)





def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


def paa_image_avg(path):
    """ Reads a arma3 paa file and returns the average color as tuple RGBA

    param path: the path to the paa file
    returns:
    """
    path = Path(path)
    data = np.fromfile(path, dtype=np.uint8)
    if not( data[1] == 0xFF and data[0] == 0x01): return None # dxt1 file!

    avg = data[0x0e:0x12] # bgra
    avg_r = avg[2]
    avg_g = avg[1]
    avg_b = avg[0]
    avg_a = avg[3]
    return (avg_r, avg_g, avg_b, avg_a)


def read_layers_cfg(path):
    layers_cfg = open(path, "r")
    all = "".join(layers_cfg.readlines())

    surfaces = {}


    pattern_name_rgb = r"\s+(\w+)\[\s*\]\s*=\s*{\s*{\s*(\s*\d{1,3}\s*),(\s*\d{1,3}\s*),(\s*\d{1,3}\s*)"

    matches = re.finditer(pattern_name_rgb, all)

    for match in matches:
        surfaces[match.group(1)] = Surface(name=match.group(1), path="", color=(int(match.group(2)), int(match.group(3)), int(match.group(4))))

    for key in surfaces.keys():
        pattern_name_path = r"class\s+" + key + r"\s+{\s+.*\n\s*material\w*=\w*(.*)"

        matches = re.finditer(pattern_name_path, all)

        for match in matches:
            surfaces[key].path = match.group(1).replace(";", "").replace('"', "")

    print(surfaces)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    avgc = paa_image_avg("a3_SourceData/cyt_ung_texture_01_co.paa")
    print(avgc)
    read_layers_cfg('a3_SourceData/layers.cfg')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
