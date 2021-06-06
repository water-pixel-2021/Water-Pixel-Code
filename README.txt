This program is written by Clément Cazorla <clement.cazorla@univ-reims.fr> and Quentin Delannoy <quentin.delannoy@univ-reims.fr> and
distributed under the terms of the GPLv3 license.

# Watervoxel algorithm

This  Python 3 program performs a 3D MRI image segmentation using the watershed algorithm.

### Installing

First install all the requirements:
```
cd /project/repository/
pip install -r requirements.txt

## Running the code

Watershed.py -p fig1 -d 25 -a 0.059 -sd 1 -rn fig1a -mm True -se 3