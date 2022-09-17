# A3_MaskToSatMap_Converter <!-- omit in toc -->
[![License](https://img.shields.io/badge/license-GNU-v3.svg?style=flat)](https://www.gnu.org/licenses/gpl-3.0.txt)

A Arma 3 Mask To SatMap Converter by Atom_Monky & ExXeptional

# Table of Contents <!-- omit in toc -->
- [Info](#info)
- [Images](#images)
- [Usage](#usage)
- [quick cmd example for the mask to satMap generator:](#quick-cmd-example-for-the-mask-to-satmap-generator)
- [Options explained:](#options-explained)
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
...</br></br>

# Usage

```sh
python maskToSatMap.py [layers] [mask] [-o, --output OUTPUT] [-wd, --workdrive WORKDRIVE] [-rgbv R_VARIATION G_VARIATION B_VARIATION] [-nc NOISECOVERAGE] [-D, --Debug] 
- OR -
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


\* can only be used in conjunction, be aware that even with the use of multithreading, the noise generation can take a lot of time depending on your map size. Only one noise type can be used (rgbv or lumv).

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
If the average value of any texture happens to be pink, then the program will interpret this as error. In this case please disregard. You can only use -rgbv or -lumv as noise generation

<details>
<summary style="font-size:11pt">More examples</summary>

# quick cmd example for the mask to satMap generator:
- download latest release from git
- open cmd
- navigate to masToSatMap.exe folder
- runn: maskToSatMap.exe "P:\PATH\TO\Layers.cfg" "P:\PATH\TO\mask.tif" -lumv 4 -nc 0.5 -mem
- ( "-" arguments are optional )

# Options explained:
usage: </br>
` maskToSatMap.py layers mask [-h] [-wd WORKDRIVE] [-o OUTPUT] [-rgbv RGBVARIATION RGBVARIATION RGBVARIATION] [-lumv LUMVARIATION] [-nc NOISECOVERAGE] [-mem] [-D] `

| Parameter | Meaning | Example | Optional |
| --------- | ------- | ------- | -------- |
| layers | path to layers.cfg file | "P:\cytech\Cytech_Aboveground_Map\Cytech_Aboveground_Terrain\Source\Images\Layers.cfg"  | |
| mask | path to terrain mask image file | "P:\cytech\Cytech_Aboveground_Map\Cytech_Aboveground_Terrain\Source\Images\Mask\mask_aboveground.tif"  | |
| -wd, --workdrive |  drive letter of Arma3 workdrive | -wd "P:\\" | X |
| -o, --output | path and filename of output file | -o "./sat_map.tiff" | X |
| -rgbv, --rgbvariation |  set rgb variation | -rgbv 3 3 3 | X |
| -nc, --noisecoverage |  noise coverage fraction | -nc 0.5 | X | 
| -mem | Use Hard disk if RAM is exceeded | -mem | X |
| -D, --Debug |  enables verbose output | -D | X |
</details>
...</br></br>

# Build

```
pip install pyinstaller numpy numba Pillow opencv-python
pyinstaller maskToSatMap.py -F
```

# Contribute
If you have any improvements or feature requests feel free to open an issue or a pull request.  
