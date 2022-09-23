# A3_MaskToSatMap_Converter <!-- omit in toc -->
[![License](https://img.shields.io/badge/license-GNU-v3.svg?style=flat)](https://www.gnu.org/licenses/gpl-3.0.txt)

A Arma 3 Mask To SatMap Converter by Atom_Monky & ExXec

# Table of Contents <!-- omit in toc -->
- [Info](#info)
- [Images](#images)
- [Usage](#usage)
    - [GUI version](#gui-version)
    - [Command line version](#command-line-version)
- [Build](#build)
- [Contribute](#contribute)

# Info
This converter helps you to quickly create a pixel accurate satmap.

The tool takes the Mask image and looks at each pixel color, according to the layer.cfg it grabs the ground texture of the pixel color and saves the average color of this texture.
In that way we can use the mask and the ground texture to generate a nice satmap really fast.

# Images
<img src="imgs\conversion_1.png" alt="drawing" style="max-width:100%; text-align: center;"/>
<details>
<summary style="font-size:14pt">Ground texture to Satellite map fade examples</summary>
<img src="imgs\surfacefade_1.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>
<img src="imgs\surfacefade_2.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>
<img src="imgs\surfacefade_3.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>
<img src="imgs\surfacefade_4.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>
<img src="imgs\surfacefade_5.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>
<img src="imgs\surfacefade_6.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>
<img src="imgs\surfacefade_7.jpg" alt="drawing" style="max-width:50%; text-align: center;"/>

<img src="imgs\noise_generation_1.png" alt="drawing" style="max-width:80%; text-align: center;"/>
</details>  
</br></br>

# Usage

## GUI version

Simply execute `maskToSatMapGUI.exe`

---

## Command line version

```sh
maskToSatMap.exe [layers] [mask] [-o, --output OUTPUT] [-wd, --workdrive WORKDRIVE] [-rgbv R_VARIATION G_VARIATION B_VARIATION] [-lumvv VARIATION] [-nc NOISECOVERAGE] [-mem] [-D, --Debug] 
```  
  
| Parameter | Function |  Default | |
| ---- | ----- | ---- | ---- |
| layers | path to layers.cfg file |  |  |
| mask | path to terrain mask image file |   |  |
| -o, --output | path and filename of output file | ./sat_map.tiff |  |
| -wd, --workdrive |  drive letter of Arma3 workdrive | P:\ |  |
| -rgbv, --rgbvariation |  set rgb variation | 0 0 0 | * |
| -lumv, --lumvariation | set luminance variation | 0 | * |
| -nc, --noisecoverage |  noise coverage fraction | 0.0 |  * |
| -mem, --memory-saver | conserve memory if possible, recommended for large maps | | |
| -D, --Debug |  enables verbose output |  |   |


\* can only be used together, be aware that even with the use of multithreading, the noise generation can take a lot of time depending on your map size. Only one noise type can be used (rgbv or lumv).

Example:
```sh
maskToSatMap.exe "layers.cfg" "Mask\mask_underground.tiff"
```
```sh
maskToSatMap.exe "layers.cfg" "Mask\mask_underground.tiff" -o "Sat\sat_map.tiff" -rgbv 5 5 5 -nc 0.90
```
```sh
maskToSatMap.exe "layers.cfg" "Mask\mask_underground.tiff" -o "Sat\sat_map.tiff" -lumv 5 -nc 0.90 -mem
```

Please note:  
If there are missing textures, the areas will show as pink (#FF00FF) on the sat map. Our program checks for any pink pixels after sat map creation and prints an error if it finds any.
If the average value of any texture happens to be pink, then the program will interpret this as error. In this case please disregard.

# Build

Install python, version 3.10 recommended.

```
pip install -r requirements.txt
pip install pyinstaller 
pyinstaller maskToSatMap.spec
```

Instead of building the exe, you can also directly call the python script with arguments
```sh
python maskToSatMap.py [layers] [mask] [-o, --output OUTPUT] [-wd, --workdrive WORKDRIVE] [-rgbv R_VARIATION G_VARIATION B_VARIATION] [-nc NOISECOVERAGE] [-D, --Debug] 
```

# Contribute
If you have any improvements or feature requests feel free to open an issue or a pull request.  
