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
import shutil
from dataclasses import dataclass
import logging
from tempfile import TemporaryDirectory

from pathlib import Path
from typing import Dict
import numpy as np
from PIL import Image
import tifffile
import numba as nb
Image.MAX_IMAGE_PIXELS = None

WORKDRIVE = Path("P:\\")

ERRORCOLOR = 255, 0, 255

MEMMAP = True
TEMPDIR = None

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
        logger.debug(f"Mapping {surf.mask_color:06X} to {surf.avg_color}")
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
            logger.error(f"Duplicate mask color entry in layers.cfg: {name} - {(r,g,b)}. Entry ignored!")
            continue

        if name in surfaces.keys():
            logger.error(f"Duplicate texture entry in layers.cfg: {name}. Entry ignored!")
            continue

        mask_colors.append(color_32)        
        surfaces[name] = Surface(name=name, path="", mask_color=color_32)

    for key in surfaces.keys():
        pattern_name_path = r"class\s+" + key + r"\s+{\s+.*\n\s*material\w*=\w*(.*)"

        matches = re.findall(pattern_name_path, file_contents)
        if matches:
            surfaces[key].path = matches[0].replace(";", "").replace('"', "")
        else:
            logger.error(f"No material file path found for texture entry in layers.cfg: {key}.")

    
    logger.debug("layers.cfg read")
    logger.debug (surfaces)
    return surfaces

def replace_mask_color(mask_path, surfaces: Dict[str, Surface]):
    """replaces the mask colors with the average colors of the corresponding texture as defined in layers.cfg"""

    # get color map from loaded layers.cfg and contained textures average colors, maps int32 colors (index) to RGB tuples from paa files
    logger.info("Building colormap from textures")
    color_map, name_map = get_mask_avg_col_map(surfaces.values())

    mask = load_image(mask_path)

    # apply new lookup table to index array to get new sat image
    logger.info("Creating sat map")
    strt = time.time()
    if MEMMAP:
        sat_map = np.memmap(TEMPDIR.name  + "/temp_satmap.dat", mode="w+", dtype=np.uint8, shape=mask.shape)
    else:
        sat_map = np.empty(dtype=np.uint8, shape=mask.shape)

    if MEMMAP:
        mask_32 = np.memmap(TEMPDIR.name  + "/temp_mask32.dat", mode="w+", dtype=np.uint32, shape=(*mask.shape[:2],))
    else:
        mask_32 = np.empty(dtype=np.uint32, shape=(*mask.shape[:2],))

    sat_map[:], mask_32[:] = vec_build_sat_map(mask, color_map)

    del mask
    logger.debug(f"Built sat map in {time.time() - strt:.2f} s")

    check_mask_errors(color_map, mask_32, name_map)

    return sat_map

@nb.guvectorize(["void(uint8[:,:], uint8[:,:], uint8[:,:], uint32[:])"], "(m,n),(o,n)->(m,n),(m)", target="parallel", cache=True)
def vec_build_sat_map(mask, color_map, sat_out, mask_out):
    # convert rgb tuple into 32 bit int 0x00RRGGBB, by shifting and adding
    # mask_32 = np.empty(mask.shape[0], dtype=np.uint32)
    for i in range(mask.shape[0]):
        mask_out[i] = (mask[i,0] << 16) + (mask[i,1] << 8) + (mask[i,2] << 0)
    sat_out[:] = color_map[mask_out]

def check_mask_errors(color_map, mask_32, name_map):
    strt = time.time()
    # check for missing textures, 0xFF00FF (pink) is default value of color map
    color_map_32: np.ndarray = color_map.dot(np.array([0x10000, 0x100, 0x1], dtype=np.int32))
    error_pixels_cnt = np.count_nonzero(color_map_32[mask_32] == ERRORCOLOR_32)
    if error_pixels_cnt: logger.warning(f"There is missing texture information. Areas will show as pink on sat map. Total pixel errors: {error_pixels_cnt}")
    # check colors used
    used_colors = np.nonzero(np.bincount(mask_32.ravel()))
    logger.debug(f"Mask colors: " + ', '.join('{:06X}'.format(a) for a in used_colors[0].flat))
    # check for unused textures
    for col in used_colors[0].flat:
        name_map.pop(col, "")
    if name_map:
        logger.warning("Unused textures: " + ", ".join(name_map.values()))
    logger.debug(f"Error checking took {time.time() - strt:.2f} s")



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
        logger.error(f"Cannot extract paa path from rvmat file {path}")
        return ERRORCOLOR

    try:
        data = np.memmap(paa_path, dtype=np.uint8)
    except FileNotFoundError:
        logger.error(f"Cannot open paa file {paa_path}")
        return ERRORCOLOR

    if not(data[1] == 0xFF and data[0] == 0x01): 
        logger.error(f"Not DXT1 format {paa_path}")
        return ERRORCOLOR # dxt1 file?

    avg_b, avg_g, avg_r  = data[0x0e:0x11] # bgr
    logger.debug(f"Avg color for {paa_path}: {avg_r, avg_g, avg_b}")
    return avg_r, avg_g, avg_b

def load_average_colors(surfaces: dict[str, Surface]):
    for surf in surfaces.values():
        if not surf.path:
            logger.error(f"Texture {surf.name} has no material path.")
            continue
        # calculate average color from texture stored in surface
        surf.avg_color = get_paa_avg_col(surf.path)
        logger.debug(surf)
    return surfaces

def rgb_noise_generation(sat_map, rgb_variation, noise_coverage):
    """generates a noise for a given threshold and a given pixel variation range"""
    if not isinstance(rgb_variation, list) and not len(rgb_variation) == 3:  
        logger.error(f"Color variation wrong datatype. Must be list of 3 ints!")
        return sat_map
    # checking inputs
    if noise_coverage == 0:
        logger.info(f"Skipping noise generation - The rgb threshold was set to 0 or not given")
        return sat_map
    elif sum(rgb_variation) == 0:
        logger.info(f"Skipping noise generation - The rgb variation was set to 0,0,0 or not given")
        return sat_map

    strt = time.time()
    sat_map[:] = vec_rgb_noise(sat_map, np.array(rgb_variation, dtype=np.uint8), noise_coverage)
    logger.debug(f"Generated noise in {time.time() - strt:.2f} s")
    
    return sat_map

    
@nb.guvectorize(["void(uint8[:,:], uint8[:], float64, uint8[:,:])"], "(m,n),(n),() -> (m,n)", target="parallel", cache=True)
def vec_rgb_noise(row, variation, noise_coverage, out):
    thresh = (np.random.randint(0, 100, size=(row.shape[0],)) > (noise_coverage*100))
    randr = np.random.randint(variation[0]*-1, variation[0], size=(row.shape[0],))
    randg = np.random.randint(variation[1]*-1, variation[1], size=(row.shape[0],))
    randb = np.random.randint(variation[2]*-1, variation[2], size=(row.shape[0],))
    
    rand = np.dstack((randr, randg, randb)).reshape(row.shape[0],3)

    rand[thresh] = np.array([0,0,0], dtype=np.int8)

    out[:] = np.clip(row + rand, a_min=0, a_max=255).astype(np.uint8)

    
def lum_noise_generation(sat_map, lum_variation, noise_coverage):
    """generates a noise for a given threshold and a given pixel variation range"""
    # checking inputs
    if not isinstance(lum_variation,int):  
        logger.error(f"Luminance variation wrong datatype. Must be int!")
        return sat_map
    if noise_coverage == 0:
        logger.info(f"Skipping noise generation - The noise coverage was set to 0 or not given")
        return sat_map
    elif lum_variation == 0:
        logger.info(f"Skipping noise generation - The luminance variation was set to 0 or not given")
        return sat_map

    strt = time.time()
    sat_map[:] =  vec_lum_noise(sat_map, lum_variation, noise_coverage)
    logger.debug(f"Generated noise in {time.time() - strt:.2f} s")
    return sat_map


@nb.guvectorize(["void(uint8[:,:], int32, float64, uint8[:,:])"], "(m,n),(),() -> (m,n)", target="parallel", cache=True)
def vec_lum_noise(row, variation, noise_coverage, out):
    thresh = (np.random.randint(0, 100, size=(row.shape[0],)) > (noise_coverage*100))
    rand = np.random.randint(variation*-1, variation, size=(row.shape[0],))
    rand[thresh] = 0
    rand = rand.repeat(row.shape[1]).reshape(row.shape)
    out[:] = np.clip(row + rand, a_min=0, a_max=255).astype(np.uint8)
   
def load_image(path):
    strt = time.time()
    img = Image.open(path)
    imshape = (*img.size,len(img.getbands()))
    if MEMMAP:
        mask = np.memmap(TEMPDIR.name  + "/temp_mask.dat", mode="w+", dtype=np.uint8, shape=imshape)
    else:
        mask= np.empty(imshape, dtype=np.uint8)

    mask[:] = np.array(img)
    logger.debug(f"Loaded mask image in {time.time() - strt:.2f} s")
    # mask = cv2.imread(str(mask_path)).squeeze()
    logger.info(f"Mask loaded {mask.shape[:2]}px")
    return mask

def export_map(sat_map, target_path):
    # export
    logger.info(f"Exporting sat map to {target_path}")
    tifffile.imwrite(target_path, sat_map, compression="zlib", compressionargs={'level':5}, predictor=True, tile=(256,256))

def start(layers, mask, output, variation, noise_coverage, luminance_noise):
    global MEMMAP, TEMPDIR
    logger.info("Starting ...")
    strt = time.time()
    if MEMMAP:
        logger.info("Creating tempdir")
        TEMPDIR = TemporaryDirectory(prefix="satmapconv_", ignore_cleanup_errors=False)
    logger.info("Reading layers.cfg")
    surfaces = read_layers_cfg(layers)
    logger.info("Loading average colors from textures")
    surfaces = load_average_colors(surfaces)
    logger.info(f"\tElapsed {time.time() - strt:.2f} s")
    logger.info("Starting sat map generation")
    sat_map = replace_mask_color(mask, surfaces)
    logger.info(f"\tElapsed {time.time() - strt:.2f} s")
    logger.info("Starting sat map noise generation")

    if luminance_noise:
        sat_map = lum_noise_generation(sat_map, variation, noise_coverage)
    else:
        sat_map = rgb_noise_generation(sat_map, rgb_variation, noise_coverage)

    logger.info(f"\tElapsed {time.time() - strt:.2f} s")
    logger.info("Saving sat map")
    export_map(sat_map ,output)
    del sat_map
    
    if MEMMAP:
        shutil.rmtree(TEMPDIR.name)
        # TEMPDIR.cleanup()
    logger.info("... Done")
    logger.info(f"\tElapsed {time.time() - strt:.2f} s")
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
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
    parser.add_argument("-lumv", "--lumvariation", type=int, default=0, help="slight variation of the average ground texture brightness in +/- range")
    parser.add_argument("-nc", "--noisecoverage", type=float, default=0.0, help="percentage of overall rgb variation")
    parser.add_argument("-mem", "--memory-saver", help="conserve memory by storing arrays on disk, recommended for large maps", action="store_true")
    parser.add_argument("-D","--Debug", action="store_true", help="increases verbosity")

    args = parser.parse_args()

    layers_path = Path(args.layers)
    mask_path = Path(args.mask)
    out_path = Path(args.output)
    
    noise_coverage = args.noisecoverage

    rgb_variation = args.rgbvariation
    if rgb_variation == 0:
        rgb_variation = [0,0,0]

    lum_variation = args.lumvariation

    assert not(args.rgbvariation != 0 and args.lumvariation !=0), "Can only use one type of variation, rgbv OR lumv!"
    
    assert layers_path.exists(), f"Layers file {args.layers} does not exist"
    assert mask_path.exists(),   f"Mask file {args.mask} does not exist"

    assert out_path.suffix in [".tiff", ".tif"], f"Output file needs to end with .tiff or .tif"

    if args.Debug: 
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if args.memory_saver:
        MEMMAP = True
    else:
        MEMMAP = False

    if args.workdrive: 
        drv = Path(args.workdrive)
        assert drv.exists(), "invalid workdrive"
        WORKDRIVE = drv
    
    if lum_variation:
        start(layers_path, mask_path, out_path, lum_variation, noise_coverage, True)
    else:
        start(layers_path, mask_path, out_path, rgb_variation, noise_coverage, False)
    
