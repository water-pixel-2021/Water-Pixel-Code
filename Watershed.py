#!/usr/bin/env python3

"""
Copyright (C) 2019, Clement Cazorla <clement.cazorla@univ-reims.fr>

This program is free software: you can use, modify and/or
redistribute it under the terms of the GNU General Public
License as published by the Free Software Foundation, either
version 3 of the License, or (at your option) any later
version. You should have received a copy of this license along
this program. If not, see <http://www.gnu.org/licenses/>.


To the extent possible under law, the authors have dedicated all
copyright and related and neighboring rights to this software to
the public domain worldwide. This software is distributed without
any warranty. You should have received a copy of the CC0 Public
Domain Dedication along with this software. If not, see
<http://creativecommons.org/publicdomain/zero/1.0/>.

This program is provided for research and education only: you can
use and/or modify it for these purposes, but you are not allowed
to redistribute this work or derivative works in source or
executable form. A license must be obtained from the patent right
holders for any other use.
"""

from Image import Image
from Image import save_as_jpeg
from Image import save_as_nifti
from Image import get_header
from contours import plot_2d_contours
from contours import plot_3d_contours
import logging
from skimage.morphology import watershed
from Gradient import Gradient
from DistanceMap import *
from Markers import *
from imageio import imread

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str, help="Path of the image to be processed")
parser.add_argument("-d", "--distance", type=int, help="Size of the super voxels (default: %(default)s voxels)",
                    default=9)
parser.add_argument("-a", "--alpha", type=float, help="Weighting coefficient for the linear combination of distance "
                                                      "map and gradient (default: %(default)s)", default=0.7)
parser.add_argument("-g", "--gradient", type=str, help="Gradient type (mag_gradient, morpho, dilation, erosion, "
                                                       "inverted_image, inverted_plus_erosion) (default: %(default)s)",
                    default="mag_gradient")
parser.add_argument("-sd", "--secure_distance", type=int, help="Security distance in term of supervoxel side pixels to"
                                                               " compute the markers (default: %(default)s)", default=
                                                               None)
parser.add_argument("-rn", "--res_name", type=str, help="Path of the result file")
parser.add_argument("-se", "--structuring_element", type=int, help="Structure size for morphological gradient "
                                                                   "computation")
parser.add_argument("-dt", "--distance_type", type=str, help="Distance type to compute the distance map: euclid, "
                                                             "manhattan or chessboard (default: %(default)s)", default=
                                                             "euclid")
parser.add_argument("-mm", "--m_markers", type=bool, help="Option to apply m-markers or not(default: %(default)s)",
                    default=False)
args = parser.parse_args()

path = args.path
distance = args.distance
alpha = args.alpha
res_name = args.res_name
secure_dist = args.secure_distance
gradient = args.gradient
numb = args.structuring_element
distance_type = args.distance_type
m_markers = args.m_markers

if secure_dist is not None:
    secure_dist = int(secure_dist)
else:
    secure_dist = 2
if secure_dist > 2:
    secure_dist = 2
    logging.warning('secure distance must not be higher than 2, set to 2 by default')

# The image is loaded and stored in an array
img = Image(path=path)
image, imgobj = img.get_image()

# We get the normalized gradient norm
grad_norm = getattr(Gradient(image, numb), gradient)() #eval(f'Gradient(image, {numb}).{gradient}()')

# We get the normalized gradient norm
if distance > min(image.shape):
    distance = min(image.shape)
    logging.warning('Distance parameter has been changed to %s', distance)
if len(image.shape) == 3:
    distance_map = DistanceMap(image.shape, distance).get_3d_dist_map(distance_type)
else:
    # For 2D images
    distance_map = DistanceMap(image.shape, distance).get_2d_dist_map(distance_type)
normalized_distance_map = normalize_dist_map(distance_map)

# Linear combination

comb = alpha * grad_norm + (1 - alpha) * normalized_distance_map

# Markers map computation
if secure_dist is not None:
    markers_map = Markers(grad_norm, distance).get_markers(secure_dist)
    if bool(m_markers) is True:
        if len(image.shape) == 3:
            normalized_distance_map = normalize_dist_map(DistanceMap(image.shape, distance).get_3d_dist_m_markers(
                                                                                                        distance_type,
                                                                                                        markers_map))
        else:
            normalized_distance_map = normalize_dist_map(DistanceMap(image.shape, distance).get_2d_dist_m_markers(
                                                                                                        distance_type,
                                                                                                        markers_map))
        comb = alpha * grad_norm + (1 - alpha) * normalized_distance_map
else:
    markers_map = Markers(comb, distance).get_markers(secure_dist)

# Result
if len(image.shape) == 3:
    labels = watershed(comb, markers_map)
else:
    # For 2D images
    labels = watershed(comb, markers_map[:, :, 0])

# Disordered reorganization of the labels to facilitate visualisation:

labels_list = np.arange(np.amin(labels), np.amax(labels) + 1)
rearranged_list = np.random.permutation(labels_list)
reorganized_labels = np.zeros(labels.shape).astype(int)
if len(image.shape) == 3:
    for i in range(0, labels.shape[0]):
        for j in range(0, labels.shape[1]):
            for k in range(0, labels.shape[2]):
                reorganized_labels[i, j, k] = rearranged_list[labels[i, j, k] - 1]
else:
    # For 2D images
    for i in range(0, labels.shape[0]):
        for j in range(0, labels.shape[1]):
            reorganized_labels[i, j] = rearranged_list[labels[i, j] - 1]
logging.warning('Labels reorganized successfully')

# Store the result in a nifti file
if imgobj is None:
    res = plot_2d_contours(imread(path), labels)
    if res_name is not None:
        save_as_jpeg(res, res_name)
else:
    plot_3d_contours(image, reorganized_labels)
    if res_name is not None:
        init_header = get_header(imgobj)
        save_as_nifti(reorganized_labels, res_name, init_header)

