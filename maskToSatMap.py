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

WORKDRIVE = "P:\\"

@dataclass
class Surface:
    name: str = ""
    path: str = "path"
    mask_color: int = 0xFFFFFF
    avg_color: tuple[int,int,int] = (255, 0, 255)


def get_mask_avg_col_map(surfaces: list[Surface]):
    """build colormap from loaded mask colors to loaded average texture colors
    
    param surfaces: list of Surface objects
    returns: array(256^3,3) colormap, dict[int,str] mask color to texture name map
    """
    col_map = np.full((256**3,3), (255,0,255), dtype=np.uint8)
    nmap={}
    for surf in surfaces:
        col_map[surf.mask_color] = surf.avg_color
        nmap[surf.mask_color] = surf.name
    return col_map, nmap
  

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
        r, g, b = int(match.group(2)), int(match.group(3)), int(match.group(4))
        # load color as 32 bit int for performance reasons
        surfaces[match.group(1)] = Surface(name=match.group(1), path="", mask_color=((r << 16) + (g << 8) + b))

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
    # load mask
    img = Image.open(mask_path)
    logging.info(f"Mask loaded {img.size}px")
    mask = np.array(img)

    # convert rgb tuple into 32 bit int 0x00RRGGBB, by shifting and adding via dot product
    logging.info("Processing mask")
    mask_32 = mask.dot(np.array([0x10000, 0x100, 0x1], dtype=np.int32))

    # get color map from loaded layers.cfg and contained textures average colors, maps int32 colors (index) to RGB tuples from paa files
    logging.info("Building colormap from textures")
    color_map, name_map = get_mask_avg_col_map(surfaces.values())

    # apply new lookup table to index array to get new sat image
    logging.info("Creating sat map")
    sat_map = color_map[mask_32]

    # check for missing textures, 0xFF00FF (pink) is default value of color map
    color_map_32: np.ndarray = color_map.dot(np.array([0x10000, 0x100, 0x1], dtype=np.int32))
    error_pixels_cnt = np.count_nonzero(color_map_32[mask_32] == 0xFF00FF)
    if error_pixels_cnt:
        logging.warning(f"There are missing textures. Areas will show as pink on sat map. Total pixel errors: {error_pixels_cnt}")

    # check colors used
    used_colors = np.unique(mask_32)
    # check for unused textures
    for col in used_colors:
        name_map.pop(col, "")
    if name_map:
        logging.warning("Unused textures: " + ", ".join(name_map.values()))

    # export
    logging.info(f"Exporting sat map to {target_path}")
    out = Image.fromarray(sat_map)
    out.save(target_path)


def find_paa_path(rvmat_path):
    """Extracts the path of the paa file corresponding to the given rvmat file"""
    with open(WORKDRIVE + rvmat_path) as file:
        for line in file:
            if "_CO.paa" in line:
                return WORKDRIVE + line.split("=")[1].replace(";", "").replace('"', "").strip()

def get_paa_avg_col(path):
    """ Reads a arma3 paa file and returns the average color as tuple RGB

    param path: the path to the paa file
    returns:
    """
    path = Path(find_paa_path(path))
    data = np.memmap(path, dtype=np.uint8)
    if not(data[1] == 0xFF and data[0] == 0x01): return (0, 0, 0) # dxt1 file?

    avg = data[0x0e:0x12] # bgra
    avg_r = avg[2]
    avg_g = avg[1]
    avg_b = avg[0]
    # avg_a = avg[3]
    # avg_r, avg_g, avg_b = random.randbytes(3)
    return avg_r, avg_g, avg_b

def load_average_colors(surfaces: dict[str, Surface]):
    for surf in surfaces.values():
        # calculate average color from texture stored in surface
        surf.avg_color = get_paa_avg_col(surf.path)
    return surfaces


def start(layers, mask, output):
    logging.info("Starting ...")
    logging.info("Reading layers.cfg")
    surfaces = read_layers_cfg(layers)
    logging.info("Loading average colors from textures")
    surfaces = load_average_colors(surfaces)
    logging.info("Starting sat map generation")
    replace_mask_color(mask, surfaces, output)
    logging.info("... Done")
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    # print(sys.argv)
    parser = argparse.ArgumentParser()
    parser.add_argument("layers", type=str, help="path of the layers.cfg file")
    parser.add_argument("mask", type=str, help="the terrain mask .tiff image file")
    parser.add_argument("-wd", "--workdrive", type=str, default="P:\\", help="drive letter of the Arma3 tools work drive")
    parser.add_argument("-o", "--output", type=str, default="./sat_img.tiff", help="path of the resulting sat view image file")
    parser.add_argument("-D","--Debug", action="store_true", help="increases verbosity")
    # parser.add_argument("-cwd, --working_directory", help="working directory of this python file")
    # args = parser.parse_args(sys.argv)
    args = parser.parse_args()
    
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

    start(args.layers, args.mask, args.output)
    # start("a3_SourceData/layers.cfg","a3_SourceData/mask_underground.tiff", "a3_SourceData/sat_map.tiff")
    
