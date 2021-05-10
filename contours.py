"""
Copyright (C) 2019, Clément Cazorla <clement.cazorla@univ-reims.fr>

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

import numpy as np


def plot_2d_contours(image, res):

    from skimage.measure import regionprops
    zero_pad = np.pad(res, 1, 'constant')
    x = regionprops(zero_pad)

    image_copy = image.copy()
    for label in x:
        for coords in label['coords']:
            if (label['_label_image'][tuple(coords)] == label["_label_image"][coords[0] - 1, coords[1]],
                label['_label_image'][tuple(coords)] == label["_label_image"][coords[0] + 1, coords[1]],
                label['_label_image'][tuple(coords)] == label["_label_image"][coords[0], coords[1] - 1],
                label['_label_image'][tuple(coords)] == label["_label_image"][coords[0], coords[1] + 1]) != \
                    (True, True, True, True):
                image_copy[coords[0] - 1, coords[1] - 1, :] = 0

    import matplotlib.pyplot as plt
    plt.figure(1)
    plt.imshow(image_copy)
    plt.title('Super segmented image')
    plt.show()
    return image_copy

def plot_3d_contours(image, res):

    from skimage.measure import regionprops
    zero_pad = np.pad(res[:, :, 10], 1, 'constant')
    x = regionprops(zero_pad)

    image_copy = image[:, :, 10].copy()
    for label in x:
        for coords in label['coords']:
            if (label['_label_image'][tuple(coords)] == label["_label_image"][coords[0] - 1, coords[1]],
                label['_label_image'][tuple(coords)] == label["_label_image"][coords[0] + 1, coords[1]],
                label['_label_image'][tuple(coords)] == label["_label_image"][coords[0], coords[1] - 1],
                label['_label_image'][tuple(coords)] == label["_label_image"][coords[0], coords[1] + 1]) != \
                    (True, True, True, True):
                image_copy[coords[0] - 1, coords[1] - 1] = 0

    import matplotlib.pyplot as plt
    plt.figure(1)
    plt.imshow(image_copy)
    plt.title('Super segmented image')
    plt.show()
