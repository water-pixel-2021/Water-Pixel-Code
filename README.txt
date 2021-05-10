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

```
python3 Watershed.py -p "image/path/"
```

All optionnal arguments can be seen using command

```
python3 Watershed.py --help
```

Example:

```
python3 Watershed.py -p "/home/user/image.nii.gz" -d 9 -a 0.7 -rn "result" -se 3
```

You can try to run on Images folder test images with all the dafault parameters and compare with the result you should obtain which is stored in the same directory.


