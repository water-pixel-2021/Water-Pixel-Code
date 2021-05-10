#!/usr/bin/env python3

"""
Copyright (C) 2019, Clément Cazorla <clement.cazorla@univ-reims.fr>
Copyright (C) 2018, Quentin Delannoy <quentin.delannoy@univ-reims.fr>

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
from skimage import measure


class Markers:
    def __init__(self, image, distance):
        self.image = image
        self.distance = distance

    def get_markers(self, secure_dist):

        """
        This function computes the markers map of the initial image according the super voxel size called distance

        Attributes
        ----------
        :return: Markers map
        :rtype: Numpy array"""

        if len(self.image.shape) != 3:
            self.image = np.expand_dims(self.image, axis=2)
        # estimation of the voxels number in each direction:
        image_size_x, image_size_y, image_size_z = self.image.shape

        # Number of segments in the image in each direction :

        nb_segment_x = int(np.ceil(image_size_x / self.distance))
        nb_segment_y = int(np.ceil(image_size_y / self.distance))
        nb_segment_z = int(np.ceil(image_size_z / self.distance))

        # Lef limit of parallelepiped:

        indice_x = np.array(range(0, nb_segment_x)) * self.distance
        indice_y = np.array(range(0, nb_segment_y)) * self.distance
        indice_z = np.array(range(0, nb_segment_z)) * self.distance

        # Initialization of the markers map:

        markers = np.zeros_like(self.image)

        # Computation of min value in each voxel :

        markers_nb = 0  # Marker number in each supervoxel of the images

        for x_left_lim in indice_x:
            for y_left_lim in indice_y:
                for z_left_lim in indice_z:

                    markers_nb += 1

                    if secure_dist is not None:
                        # if secure distance is set to a value
                        if image_size_z == 1:
                            thumbnail = self.image[x_left_lim + secure_dist:(x_left_lim + self.distance) - secure_dist,
                                                   y_left_lim + secure_dist:(y_left_lim + self.distance) - secure_dist,
                                                   z_left_lim]
                        else:
                            thumbnail = self.image[x_left_lim + secure_dist:(x_left_lim + self.distance) - secure_dist,
                                                   y_left_lim + secure_dist:(y_left_lim + self.distance) - secure_dist,
                                                   z_left_lim + secure_dist:(z_left_lim + self.distance) - secure_dist]
                    else:
                        thumbnail = self.image[x_left_lim:(x_left_lim + self.distance),
                                               y_left_lim:(y_left_lim + self.distance),
                                               z_left_lim:(z_left_lim + self.distance)]

                    ind_first_min = np.unravel_index(np.argmin(thumbnail, axis=None),
                                                     thumbnail.shape)  # Return index of one min only

                    ind = np.array(np.where(thumbnail == thumbnail[ind_first_min]))
                    # min indexes in column in a 2D array

                    if ind.shape[1] == 1:
                        # Switch from the thumbnail to the initial image coordinates
                        if secure_dist is not None:
                            if image_size_z == 1:
                                ind = np.reshape(ind, newshape=[2]) + np.array([x_left_lim + secure_dist, y_left_lim +
                                                                                secure_dist])
                            else:
                                ind = np.reshape(ind, newshape=[3]) + np.array([x_left_lim + secure_dist, y_left_lim +
                                                                                secure_dist, z_left_lim + secure_dist])
                        else:
                            ind = np.reshape(ind, newshape=[3]) + np.array([x_left_lim, y_left_lim, z_left_lim])
                        markers[tuple(ind)] = markers_nb

                    # min reached several times
                    else:

                        # Binary matrix: 1 for min values 0 else
                        voxel_min = np.zeros_like(thumbnail)

                        for j in range(ind.shape[1]):
                            voxel_min[tuple(ind[:, j])] = 1

                        # Each connected area has its own label
                        label_connected_region = measure.label(voxel_min, connectivity=2)

                        unique_elements, counts_elements = np.unique(
                            label_connected_region[label_connected_region != 0], return_counts=True)

                        label_mode = unique_elements[np.argsort(counts_elements)][-1]
                        if secure_dist is not None:
                            if image_size_z == 1:
                                ind_final = np.array(np.where(label_connected_region == label_mode))[:, 0] + np.array(
                                    [x_left_lim + secure_dist, y_left_lim + secure_dist])
                            else:
                                ind_final = np.array(np.where(label_connected_region == label_mode))[:, 0] + np.array(
                                    [x_left_lim + secure_dist, y_left_lim + secure_dist, z_left_lim + secure_dist])
                        else:
                            ind_final = np.array(np.where(label_connected_region == label_mode))[:, 0] + np.array(
                                [x_left_lim, y_left_lim, z_left_lim])

                        markers[tuple(ind_final)] = markers_nb

        return markers
