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

from __future__ import annotations
import random
import re
import argparse
import sys
import os
from dataclasses import dataclass
import time
import logging

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
    logging.info("Reading Layers.cfg")
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

    
    logging.debug("layers.cfg read")
    logging.debug (surfaces)
    return surfaces

def replace_mask_color(mask_path, surfaces: Dict[str, Surface], target_path):
    """replaces the mask colors with the average colors of the corresponding texture as defined in layers.cfg"""
    img = Image.open(mask_path).convert('RGB')
    logging.info(f"Mask loaded {img.size}px")
    mask = np.array(img)
    mask_size = int(mask.size/3)

    replace_counter = 0

    for surf in surfaces.values():
        # calculate average color from texture stored in surface
        paa_path = find_paa_path(surf.path)
        avg_c = get_paa_avg_col(paa_path)
        # replace color from surface with average color in mask
        # ToDO Add a counter so we can see how many px where replaced ! Must be in sum the same as the mask size !
        replace_px = (mask == surf.mask_color).all(axis = -1)
        mask[replace_px] = avg_c
        cnt = np.count_nonzero(replace_px)
        replace_counter += cnt
        print(f"replaced {cnt} pixels for material {surf.name}: {surf.mask_color}\tto average ground texture color {avg_c}\t\ttotal replaced pixels {replace_counter:,d}/{mask_size:,d}\t {replace_counter/mask_size * 100:3.1f}%")
        

    print(f"Exporting sat map to {target_path}")
    out = Image.fromarray(mask)
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
    data = np.memmap(path, dtype=np.uint8)
    if not(data[1] == 0xFF and data[0] == 0x01): return (0, 0, 0) # dxt1 file?

    avg = data[0x0e:0x12] # bgra
    avg_r = avg[2]
    avg_g = avg[1]
    avg_b = avg[0]
    avg_a = avg[3]
    return (avg_r, avg_g, avg_b) #, avg_a)


def start(layers, mask, output):
    logging.info("Starting ...")
    logging.info("Reading layers.cfg")
    surfaces = read_layers_cfg(layers)
    logging.info("Loading average colors from textures")
    surfaces = load_average_colors(surfaces)
    logging.info("Starting sat map generation")
    tim = time.time()
    replace_mask_color(mask, surfaces, output)
    logging.info(f"Elapsed {tim-time.time()}")
    logging.info("... Done")
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument("layers", type=str, help="path of the layers.cfg file")
    parser.add_argument("mask", type=str, help="the terrain mask .tiff image file")
    parser.add_argument("-wd", "--workdrive", type=str, default="P:\\", help="drive letter of the Arma3 tools work drive")
    parser.add_argument("-o", "--output", type=str, default="./sat_img.tiff", help="path of the resulting sat view image file")
    parser.add_argument("-D","--Debug", action="store_true", help="increases verbosity")
    # parser.add_argument("-cwd, --working_directory", help="working directory of this python file")
    # args = parser.parse_args(sys.argv)
    args = parser.parse_args()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    
    assert os.path.exists(args.layers), f"Layers file {args.layers} does not exist"
    assert os.path.exists(args.mask),   f"Mask file {args.mask} does not exist"
    
    if (args.output != "./sat_img.tiff"):
        assert os.path.exists(args.output),  f"Output directory {args.output} does not exist"
    

    # if args.Debug: 
    #     logger.setLevel(logging.DEBUG)
    # else:
    #     logger.setLevel(logging.INFO)
    # if args.workdrive: 
    #     assert Path(args.workdrive), "invalid workdrive"
    #     drv:str = args.workdrive
    #     if not drv.endswith("\\") and not drv.endswith("/"):
    #         drv += "\\"
    #     WORKDRIVE = drv

    start(args.layers,args.mask,args.output)
    
