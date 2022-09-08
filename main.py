from PIL import Image
import numpy as np
from pathlib import Path

# ToDo
# 1 read and save layers cfg
# 2 Read in tile images
# 3 Read mask
# 4 refer mask color to tile image by layers cfg
# 5 create Satmap

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


if __name__ == '__main__':
    avgc = paa_image_avg("a3_SourceData/cyt_ung_texture_01_co.paa")
    print(avgc)
