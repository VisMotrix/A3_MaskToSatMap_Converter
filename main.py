# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# ToDo
# 1 read and save layers cfg
# 2 Read in tile images
# 3 Read mask
# 4 refer mask color to tile image by layers cfg
# 5 create Satmap
import re
from dataclasses import dataclass

@dataclass
class Surface:
    name = ""
    path = "path"
    color = (255, 255, 255)



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


def read_layers_cfg(path):
    layers_cfg = open(path, "r")
    all = "".join(layers_cfg.readlines())

    surfaces = {}


    pattern_name_rgb = r"\s+(\w+)\[\s*\]\s*=\s*{\s*{\s*(\s*\d{1,3}\s*),(\s*\d{1,3}\s*),(\s*\d{1,3}\s*)"

    matches = re.finditer(pattern_name_rgb, all)

    for match in matches:
        surfaces[match.group(1)] = Surface(name=match.group(1), path="", color=(int(match.group(2)), int(match.group(3)), int(match.group(4))))

    for key in surfaces.keys():
        pattern_name_path = r"class\s+" + key + r"\s+{\s+.*\n\s*material\w*=\w*(.*)"

        matches = re.finditer(pattern_name_path, all)

        for match in matches:
            surfaces[key].path = match.group(1).replace(";", "").replace('"', "")

    print(surfaces)





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    read_layers_cfg('a3_SourceData/layers.cfg')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
