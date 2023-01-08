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

<img src="imgs\gui_prv.png" alt="drawing" style="max-width:100%; text-align: center;"/>

It has several elements:  
1. Enter the path to your layers.cfg here, you can use the `Open` button to browse the files.
2. Enter the path to your mask image file here. Can be any image format. Use the `Open` button to browse for the file.
3. Enter the desired output path and filename for the generated sat map. Or use the `Save as` button to open a dialog. Supported file format is tiff.
4. Noise setting. Options include `No noise`, `BW noise` (brighter and darker spots) and `RGB noise` (slight color variation for each pixel)
5. Noise strenght. This defines the maximum possible change of pixel values for the noise generator. It will pick randomly from range +-strength to apply to a pixel. Strength consists of one value for BW noise and 3 values for RGB noise (each color individually).
6. Noise coverage defines how many pixels are affected by the noise. In percent. Each pixel has this chance of having noise.
7. A3 Tools workdrive. Is used to complete texture files paths from your layers.cfg or the rvmat files, e.g `myMod/mytextures/ground.rvmat` + `P:/` -> `P:/myMod/mytextures/ground.rvmat`. Adjust according to your texture file locations.  
8. Click to start the process
9. Click to open results folder.
10. Log. Contains information about progress and possible errors.

## layers.cfg
Due to regex beeing regex use this layers.cfg format and pay attention to spacing:
<details>

```c#
class layers
{
	class cyt_ung_texture_01
	{
		texture="";
		material="cytech\cytech_underground_map\cytech_underground_data\groundtextures\cyt_ung_texture_01.rvmat";
	};
};
class legend
{
	picture="cytech\cytech_underground_map\cytech_underground_terrain\source\images\maplegend.png";
	class colors
	{
		cyt_ung_texture_01[]={{238,130,238}};
	};
};
```

</details>  
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

## GUI version 

```
pip install -r requirements_gui.txt
pip install pyinstaller 
pyinstaller build_GUI.spec
```

## Command line version

```
pip install -r requirements.txt
pip install pyinstaller 
pyinstaller build_CMD.spec
```

Instead of building the exe, you can also directly call the python script with arguments
```sh
python maskToSatMap.py [layers] [mask] [-o, --output OUTPUT] [-wd, --workdrive WORKDRIVE] [-rgbv R_VARIATION G_VARIATION B_VARIATION] [-nc NOISECOVERAGE] [-D, --Debug] 
```

# Contribute
If you have any improvements or feature requests feel free to open an issue or a pull request.  
