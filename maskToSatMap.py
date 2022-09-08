#     A Arma 3 Mask To SatMap Converter
#     Copyright (C) 2022  VisMotrix, rk-exxec

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re
import argparse
import sys
import os
from dataclasses import dataclass


from pathlib import Path
from typing import Dict
import numpy as np
from PIL import Image

DEBUGGING = False
WORKDRIVE = "P:\\"

@dataclass
class Surface:
    name: str = ""
    path: str = "path"
    mask_color: tuple[int, int, int] = (255, 255, 255)

def read_layers_cfg(path):
    """ Reads a arma3 layers.cfg and graps mask color to suface material information

    param path: the path to the layers.cfg file
    returns: dict of [texturename, Surface]
    """
    print("Reading Layers.cfg")
    layers_cfg = open(path, "r")
    all = "".join(layers_cfg.readlines())
    surfaces = {}
    
    pattern_name_rgb = r"\s+(\w+)\[\s*\]\s*=\s*{\s*{\s*(\s*\d{1,3}\s*),(\s*\d{1,3}\s*),(\s*\d{1,3}\s*)"

    matches = re.finditer(pattern_name_rgb, all)

    for match in matches:
        surfaces[match.group(1)] = Surface(name=match.group(1), path="", mask_color=(int(match.group(2)), int(match.group(3)), int(match.group(4))))

    for key in surfaces.keys():
        pattern_name_path = r"class\s+" + key + r"\s+{\s+.*\n\s*material\w*=\w*(.*)"

        matches = re.finditer(pattern_name_path, all)

        for match in matches:
            surfaces[key].path = match.group(1).replace(";", "").replace('"', "")

    
    if DEBUGGING:
        print ("layers.cfg read")
        print (surfaces)
    return surfaces

def replace_mask_color(mask_path, surfaces: Dict[str, Surface], target_path):
    """replaces the mask colors with the average colors of the corresponding texture as defined in layers.cfg"""
    img = Image.open(mask_path).convert('RGB')
    print("Mask loaded")
    data = np.array(img)

    for surf in surfaces.values():
        # calculate average color from texture stored in surface
        paa_path = find_paa_path(surf.path)
        avg_c = get_paa_avg_col(paa_path)
        # replace color from surface with average color in mask
        data[(data == surf.mask_color).all(axis = -1)] = avg_c
        print(f"replaced color for material {surf.name}: {surf.mask_color} to {avg_c}")

    print(f"Exporting sat map to {target_path}")
    out = Image.fromarray(data)
    out.save(target_path)


def find_paa_path(rvmat_path):
    """Extracts the path of the paa file corresponding to the given rvmat file"""
    with open(WORKDRIVE + rvmat_path) as file:
        for line in file:
            if "_CO.paa" in line:
                return WORKDRIVE + line.split("=")[1].replace(";", "").replace('"', "").strip()

def get_paa_avg_col(path):
    """ Reads a arma3 paa file and returns the average color as tuple RGBA

    param path: the path to the paa file
    returns:
    """
    path = Path(path)
    data = np.fromfile(path, dtype=np.uint8)
    if not( data[1] == 0xFF and data[0] == 0x01): return (0, 0, 0) # dxt1 file?

    avg = data[0x0e:0x12] # bgra
    avg_r = avg[2]
    avg_g = avg[1]
    avg_b = avg[0]
    avg_a = avg[3]
    return (avg_r, avg_g, avg_b) #, avg_a)


def start(layers, mask, output):
    print("Starting ...")
    surfaces = read_layers_cfg(layers)
    replace_mask_color(mask, surfaces, output)
    print("... Done")
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument("layers", type=str, help="path of the layers.cfg file")
    parser.add_argument("-m", "--mask", type=str, help="the terrain mask image file")
    parser.add_argument("-wd", "--workdrive", type=str, default="P:\\", help="drive letter of the Arma3 tools work drive")
    parser.add_argument("-o", "--output", type=str, default="./sat_img.tiff", help="path of the resulting sat view image file")
    parser.add_argument("-D","--Debug", action="store_true", help="increases verbosity")
    parser.add_argument("-cwd, --working-directory", help="working directory of this python file")
    args = parser.parse_args(sys.argv)


    if args.working_directory: 
        assert Path(args.working_directory ).exists, "invalid working directory"
        os.chdir(args.working_directory)

    assert Path(args.layers).exists, f"Layers file {args.layers} does not exist"
    assert Path(args.output).exists, f"Output file {args.output} does not exist"
    assert Path(args.mask).exists, f"Mask file {args.mask} does not exist"
    

    if args.Debug: DEBUGGING = True
    if args.workdrive: 
        assert Path(args.workdrive), "invalid workdrive"
        drv:str = args.workdrive
        if not drv.endswith("\\") and not drv.endswith("/"):
            drv += "\\"
        WORKDRIVE = drv

    start(args.layers,args.mask,args.output)
    
