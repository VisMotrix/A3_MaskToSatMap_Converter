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
import re
import argparse
import sys
import time
from dataclasses import dataclass
import logging

from pathlib import Path
from typing import Dict
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

WORKDRIVE = Path("P:\\")

ERRORCOLOR = 255, 0, 255

ERRORCOLOR_32 = (ERRORCOLOR[0] << 16) + (ERRORCOLOR[1] << 8) + ERRORCOLOR[2]

@dataclass
class Surface:
    name: str = ""
    path: str = ""
    mask_color: int = 0xFFFFFF
    avg_color: tuple[int,int,int] = ERRORCOLOR


def get_mask_avg_col_map(surfaces: list[Surface]):
    """build colormap from loaded mask colors to loaded average texture colors
    
    param surfaces: list of Surface objects
    returns: array(256^3,3) colormap, dict[int,str] mask color to texture name map
    """
    col_map = np.full((256**3,3), ERRORCOLOR, dtype=np.uint8)
    nmap={}
    for surf in surfaces:
        col_map[surf.mask_color] = surf.avg_color
        logging.debug(f"Mapping {surf.mask_color:06X} to {surf.avg_color}")
        nmap[surf.mask_color] = surf.name
    return col_map, nmap
  

def read_layers_cfg(path):
    """ Reads a arma3 layers.cfg and graps mask color to suface material information

    param path: the path to the layers.cfg file
    returns: dict of [texturename, Surface]
    """
    layers_cfg = open(path, "r")
    file_contents = "".join(layers_cfg.readlines())
    surfaces = {}
    
    pattern_name_rgb = r"\s+(\w+)\[\s*\]\s*=\s*{\s*{\s*(\s*\d{1,3}\s*),(\s*\d{1,3}\s*),(\s*\d{1,3}\s*)"

    matches = re.finditer(pattern_name_rgb, file_contents)
    mask_colors = []
    for match in matches:
        r, g, b = int(match.group(2)), int(match.group(3)), int(match.group(4))
        # load color as 32 bit int for performance reasons
        color_32 = ((r << 16) + (g << 8) + b)
        name = match.group(1)

        # check if color already loaded
        if color_32 in mask_colors:
            logging.error(f"Duplicate mask color entry in layers.cfg: {name} - {(r,g,b)}. Entry ignored!")
            continue

        if name in surfaces.keys():
            logging.error(f"Duplicate texture entry in layers.cfg: {name}. Entry ignored!")
            continue

        mask_colors.append(color_32)        
        surfaces[name] = Surface(name=name, path="", mask_color=color_32)

    for key in surfaces.keys():
        pattern_name_path = r"class\s+" + key + r"\s+{\s+.*\n\s*material\w*=\w*(.*)"

        matches = re.findall(pattern_name_path, file_contents)
        if matches:
            surfaces[key].path = matches[0].replace(";", "").replace('"', "")
        else:
            logging.error(f"No material file path found for texture entry in layers.cfg: {key}.")

    
    logging.debug("layers.cfg read")
    logging.debug (surfaces)
    return surfaces

def replace_mask_color(mask_path, surfaces: Dict[str, Surface]):
    """replaces the mask colors with the average colors of the corresponding texture as defined in layers.cfg"""
    if Path("mask.npy").exists():
        mask_32 = np.load("mask.npy")
    else:
        # load mask
        try:
            img = Image.open(mask_path).convert("RGB")
        except Image.DecompressionBombError:
            logging.error("The mask file is too large, try using the -is parameter with your total pixel count.")
        logging.info(f"Mask loaded {img.size}px")
        mask = np.array(img)
        del img

        # convert rgb tuple into 32 bit int 0x00RRGGBB, by shifting and adding via dot product
        logging.info("Processing mask")
        mask_32 = mask.dot(np.array([0x10000, 0x100, 0x1], dtype=np.int32))
        np.save("mask.npy", mask_32)
        del mask

    # get color map from loaded layers.cfg and contained textures average colors, maps int32 colors (index) to RGB tuples from paa files
    logging.info("Building colormap from textures")
    color_map, name_map = get_mask_avg_col_map(surfaces.values())

    # apply new lookup table to index array to get new sat image
    logging.info("Creating sat map")
    sat_map = color_map[mask_32]

    # check for missing textures, 0xFF00FF (pink) is default value of color map
    color_map_32: np.ndarray = color_map.dot(np.array([0x10000, 0x100, 0x1], dtype=np.int32))
    error_pixels_cnt = np.count_nonzero(color_map_32[mask_32] == ERRORCOLOR_32)
    if error_pixels_cnt:
        logging.warning(f"There is missing texture information. Areas will show as pink on sat map. Total pixel errors: {error_pixels_cnt}")

    # check colors used
    used_colors = np.unique(mask_32)
    logging.debug(f"Mask colors: " + ', '.join('{:06X}'.format(a) for a in used_colors))
    # check for unused textures
    for col in used_colors:
        name_map.pop(col, "")
    if name_map:
        logging.warning("Unused textures: " + ", ".join(name_map.values()))

    return sat_map
    

def find_paa_path(rvmat_path):
    """Extracts the path of the paa file corresponding to the given rvmat file"""
    try:
        with open(WORKDRIVE / rvmat_path) as file:
            for line in file:
                if "_co.paa" in line.lower():
                    return WORKDRIVE / line.split("=")[1].replace(";", "").replace('"', "").strip()
    except:
        return None

def get_paa_avg_col(path):
    """ Reads a arma3 rvmat file and returns the average color of the corresponding paa file as tuple RGB

    param path: the path to the paa file
    returns: the average color as defined in the paa file as (R,G,B) tuple
    """

    paa_path = find_paa_path(path)
    if not paa_path: 
        logging.error(f"Cannot extract paa path from rvmat file {path}")
        return ERRORCOLOR

    try:
        data = np.memmap(paa_path, dtype=np.uint8)
    except FileNotFoundError:
        logging.error(f"Cannot open paa file {paa_path}")
        return ERRORCOLOR

    if not(data[1] == 0xFF and data[0] == 0x01): 
        logging.error(f"Not DXT1 format {paa_path}")
        return ERRORCOLOR # dxt1 file?

    avg_b, avg_g, avg_r  = data[0x0e:0x11] # bgr
    logging.debug(f"Avg color for {paa_path}: {avg_r, avg_g, avg_b}")
    return avg_r, avg_g, avg_b

def load_average_colors(surfaces: dict[str, Surface]):
    for surf in surfaces.values():
        if not surf.path:
            logging.error(f"Texture {surf.name} has no material path.")
            continue
        # calculate average color from texture stored in surface
        surf.avg_color = get_paa_avg_col(surf.path)
        logging.debug(surf)
    return surfaces

def noise_generation(sat_map, rgb_variation, rgb_threshold):
    """generates a noise for a given threshold and a given pixel variation range"""
    # checking inputs
    if rgb_threshold == 0:
        logging.info(f"Skipping noise generation - The rgb threshold was set to 0 or not given")
        return sat_map
    elif sum(rgb_variation) == 0:
        logging.info(f"Skipping noise generation - The rgb variation was set to 0,0,0 or not given")
        return sat_map

    rand = ((np.random.rand(*sat_map.shape) - 0.5) * rgb_variation * (np.random.random()<rgb_threshold)).astype(np.int8) # uniform distribution
    #rand = (np.random.randn(*sat_map.shape) * rgb_variation).astype(np.int8) # gaussian distribution
    # replacing pixels
    sat_map =  np.clip(sat_map + rand, a_min=0, a_max=255).astype(np.uint8)
    return sat_map

def export_map(sat_map, target_path):
    # export
    logging.info(f"Exporting sat map to {target_path}")
    Image.fromarray(sat_map).save(target_path)#, compression="lzma")

def start(layers, mask, output, rgb_variation, rgb_threshold):
    logging.info("Starting ...")
    logging.info("Reading layers.cfg")
    surfaces = read_layers_cfg(layers)
    logging.info("Loading average colors from textures")
    surfaces = load_average_colors(surfaces)
    logging.info("Starting sat map generation")
    sat_map = replace_mask_color(mask, surfaces)
    logging.info("Starting sat map noise generation")
    strt = time.time()
    sat_map = noise_generation(sat_map, rgb_variation, rgb_threshold)
    logging.info(f"Elapsed {time.time() - strt:.2f} s")
    logging.info("Saving sat map")
    export_map(sat_map ,output)
    logging.info("... Done")
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)

    parser = argparse.ArgumentParser()
    parser.add_argument("layers", type=str, help="path of the layers.cfg file")
    parser.add_argument("mask", type=str, help="the terrain mask .tiff image file")
    parser.add_argument("-wd", "--workdrive", type=str, default="P:\\", help="drive letter of the Arma3 tools work drive")
    parser.add_argument("-o", "--output", type=str, default="./sat_img.tiff", help="path of the resulting sat view image file")
    parser.add_argument("-rgbv", "--rgbvariation", type=int, default=0, nargs=3, help="slight variation of the average ground texture color in +/- color range")
    parser.add_argument("-rgbt", "--rgbthreshold", type=float, default=0.0, help="percentage of overall rgb variation")
    parser.add_argument("-D","--Debug", action="store_true", help="increases verbosity")

    args = parser.parse_args()

    layers_path = Path(args.layers)
    mask_path = Path(args.mask)
    out_path = Path(args.output)
    
    rgb_threshold = args.rgbthreshold
    rgb_variation = args.rgbvariation
    if rgb_variation == 0:
        rgb_variation = [0,0,0]
    
    assert layers_path.exists(), f"Layers file {args.layers} does not exist"
    assert mask_path.exists(),   f"Mask file {args.mask} does not exist"


    if args.Debug: 
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    if args.workdrive: 
        drv = Path(args.workdrive)
        assert drv.exists(), "invalid workdrive"
        WORKDRIVE = drv
    
    

    start(layers_path, mask_path, out_path, rgb_variation, rgb_threshold)
    
