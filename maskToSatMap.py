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

import numba as nb

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
    avg_color: tuple[int, int, int] = (255, 0, 255)

    @staticmethod
    def get_mask_avg_col_map(surfaces: list[Surface]):
        map = {}
        nmap={}
        for surf in surfaces:
            map[surf.mask_color] = surf.avg_color
            nmap[surf.mask_color] = surf.name
        return map, nmap

        

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

def unique_scikit(ar):
    if ar.ndim != 2:
        raise ValueError("unique_rows() only makes sense for 2D arrays, "
                         "got %dd" % ar.ndim)
    # the view in the next line only works if the array is C-contiguous
    ar = np.ascontiguousarray(ar)
    # np.unique() finds identical items in a raveled array. To make it
    # see each row as a single item, we create a view of each row as a
    # byte string of length itemsize times number of columns in `ar`
    ar_row_view = ar.view('|S%d' % (ar.itemsize * ar.shape[1]))
    _, unique_row_indices, idx = np.unique(ar_row_view, return_index=True, return_inverse=True)
    ar_out = ar[unique_row_indices]
    return ar_out, idx

def replace_mask_color(mask_path, surfaces: Dict[str, Surface], target_path):
    """replaces the mask colors with the average colors of the corresponding texture as defined in layers.cfg"""
    img = Image.open(mask_path).convert('RGB')
    logging.info(f"Mask loaded {img.size}px")
    mask = np.array(img)

    # create lookup table and corresponding index array from input image
    logging.info("Preprocessing mask image, this might take a while ...")
    lut, idx_arr = np.unique(mask.reshape(-1, mask.shape[2]), return_inverse=True, axis=0)
    idx_arr = idx_arr.reshape(mask.shape[0:2])

    # get color map from loaded layers.cfg and contained textures average colors
    logging.info("Building colormap from textures")
    color_map, name_map = Surface.get_mask_avg_col_map(surfaces.values())

    # build new lookup table with average texture colors
    logging.info("Building new lookup table")
    new_lut = np.zeros_like(lut)
    for i, col in enumerate(lut):
        col = tuple(col)
        try:
            new_lut[i] = color_map[col]
            # check for unused colors in mask by comparing with list from layers.cfg
            # this removes all colors in mask from this color map, if not empty by end, it contains unused textures/colors
            name_map.pop(col)
        except KeyError:
            logging.warning(f"Mask color {col} not in lookup table! Not replacing. If you think this is an error, check your layers.cfg and materials.")
            new_lut[i] = col

    # check unused textures
    if name_map:
        logging.warning(f"Unused textures:\n {name_map.values()}")

    # apply new lookup table to index array to get new sat image
    logging.info("Applying new lookup table")
    sat_map = new_lut[idx_arr]

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
    """ Reads a arma3 paa file and returns the average color as tuple RGBA

    param path: the path to the paa file
    returns:
    """
    # path = Path(find_paa_path(path))
    # data = np.memmap(path, dtype=np.uint8)
    # if not(data[1] == 0xFF and data[0] == 0x01): return (0, 0, 0) # dxt1 file?

    # avg = data[0x0e:0x12] # bgra
    # avg_r = avg[2]
    # avg_g = avg[1]
    # avg_b = avg[0]
    # avg_a = avg[3]
    avg_r, avg_g, avg_b = random.randbytes(3)
    return (avg_r, avg_g, avg_b) #, avg_a)

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
    tim = time.time()
    replace_mask_color(mask, surfaces, output)
    logging.info(f"Elapsed {tim-time.time()}")
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
    # parser = argparse.ArgumentParser()
    # parser.add_argument("layers", type=str, help="path of the layers.cfg file")
    # parser.add_argument("mask", type=str, help="the terrain mask .tiff image file")
    # parser.add_argument("-wd", "--workdrive", type=str, default="P:\\", help="drive letter of the Arma3 tools work drive")
    # parser.add_argument("-o", "--output", type=str, default="./sat_img.tiff", help="path of the resulting sat view image file")
    # parser.add_argument("-D","--Debug", action="store_true", help="increases verbosity")
    # # parser.add_argument("-cwd, --working_directory", help="working directory of this python file")
    # # args = parser.parse_args(sys.argv)
    # args = parser.parse_args()
    
    # assert os.path.exists(args.layers), f"Layers file {args.layers} does not exist"
    # assert os.path.exists(args.mask),   f"Mask file {args.mask} does not exist"
    
    # if (args.output != "./sat_img.tiff"):
    #     assert os.path.exists(args.output),  f"Output directory {args.output} does not exist"
    

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

    # start(args.layers,args.mask,args.output)
    start("a3_SourceData/layers.cfg","a3_SourceData/mask_underground.tiff", "a3_SourceData/sat_map.tiff")
    
