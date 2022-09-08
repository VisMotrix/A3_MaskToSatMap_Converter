# A3_MaskToSatMap_Converter <!-- omit in toc -->
[![License](https://img.shields.io/badge/license-GNU-v3.svg?style=flat)](https://www.gnu.org/licenses/gpl-3.0.txt)

A Arma 3 Mask To SatMap Converter

# Table of Contents <!-- omit in toc -->
- [Info](#info)
- [Images](#images)
- [Usage](#usage)
- [Build](#build)
- [Contribute](#contribute)

# Info
This converter helps you to quickly create a pixel accurate satmap.

The tool takes the Mask image and looks at each pixel color, according to the layer.cfg it grabs the ground texture of the pixel color and saves the average color of this texture.
In that way we can use the mask and the ground texture to generate a nice satmap really fast.

# Images
<img src="imgs\surfacefade_1.jpg" alt="drawing" style="max-width:60%; text-align: center;"/>
<details>
<summary style="font-size:14pt">See More</summary>
<img src="imgs\surfacefade_2.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>
<img src="imgs\surfacefade_3.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>
<img src="imgs\surfacefade_4.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>
<img src="imgs\surfacefade_5.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>
<img src="imgs\surfacefade_6.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>
<img src="imgs\surfacefade_7.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>
</details>  

Surface and Satmap texture blends pretty good
  

# Usage

```sh
python maskToSatMap.py [layers] [mask] [-o, --output OUTPUT] [-wd, --workdrive WORKDRIVE] [-cwd, --working_directory  DIRECTORY] [-D, --Debug] 
- OR -
maskToSatMap.exe [layers] [mask] [-o, --output OUTPUT] [-wd, --workdrive WORKDRIVE] [-cwd, --working_directory  DIRECTORY] [-D, --Debug] 
```  
  
| Parameter | Function |  Default |
| ---- | ----- | ---- |  
| layers | path to layers.cfg file |  |  
| mask | path to terrain mask image file |   |  
| -o, --output | path and filename of output file | ./sat_map.tiff |  
| -wd, --workdrive |  drive letter of Arma3 workdrive | P:\ |  
| -cwd, --working_directory | set the working directory of the program<br/>paths will be relative to this directory | ./ |
| -D, --Debug |  enables verbose output |  |  

Example:
```sh
maskToSatMap.exe "layers.cfg" "Mask\mask_underground.tiff"
```
```sh
maskToSatMap.exe "layers.cfg" "Mask\mask_underground.tiff" -o "Sat\sat_map.tiff" -cwd "P:\cytech\Cytech_Underground_Map\Cytech_Underground_Terrain\source\Images"
```

# Build

```
pip install pyinstaller
pyinstaller maskToSatMap.py -F -w
```

# Contribute
If you have any improvements or feature requests feel free to open an issue or a pull request.  

