
#!/usr/bin/env python3

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
from scipy.ndimage.morphology import distance_transform_edt
from scipy.ndimage.morphology import distance_transform_cdt


class DistanceMap:
    def __init__(self, shape, distance):
        self.shape = shape
        self.distance = distance

    def get_3d_dist_map(self, distance_type):
        """
        This function computes distance map

        Attributes
        ----------
        :param distance_type: Distance type to compute the distance map
        :type distance_type: String
        :return: Distance map
        :rtype: Numpy array"""

        # A reshape might be necessary to compute the distance map

        shape_0, shape_1, shape_2 = self.shape
        if shape_0 % self.distance != 0:
            while shape_0 % self.distance != 0:
                shape_0 += 1
        if shape_1 % self.distance != 0:
            while shape_1 % self.distance != 0:
                shape_1 += 1
        if shape_2 % self.distance != 0:
            while shape_2 % self.distance != 0:
                shape_2 += 1
        matrix = np.ones(shape=(shape_0, shape_1, shape_2))
        i = np.arange(0, shape_0, self.distance)
        j = np.arange(0, shape_1, self.distance)
        k = np.arange(0, shape_2, self.distance)

        for x in i:
            for y in j:
                for z in k:
                    matrix[x + int(np.floor(self.distance/2)), y + int(np.floor(self.distance/2)), z +
                           int(np.floor(self.distance/2))] = 0
        if distance_type == 'euclid':
            carte_distance = distance_transform_edt(matrix)
        elif distance_type == "chessboard":
            carte_distance = distance_transform_cdt(matrix)
        elif distance_type == 'manhattan':
            carte_distance = distance_transform_cdt(matrix, metric='taxicab')

        if (shape_0, shape_1, shape_2) != self.shape:
            carte_distance = carte_distance[:self.shape[0], :self.shape[1], :self.shape[2]]

        return carte_distance

    def get_2d_dist_map(self, distance_type):
        """
        This function computes distance map

        Attributes
        ----------
        :param distance_type: Distance type to compute the distance map
        :type distance_type: String
        :return: Distance map
        :rtype: Numpy array"""

        # A reshape might be necessary to compute the distance map

        shape_0, shape_1 = self.shape
        if shape_0 % self.distance != 0:
            while shape_0 % self.distance != 0:
                shape_0 += 1
        if shape_1 % self.distance != 0:
            while shape_1 % self.distance != 0:
                shape_1 += 1

        matrix = np.ones(shape=(shape_0, shape_1))
        i = np.arange(0, shape_0, self.distance)
        j = np.arange(0, shape_1, self.distance)

        for x in i:
            for y in j:
                matrix[x + int(np.floor(self.distance/2)), y + int(np.floor(self.distance/2))] = 0
        if distance_type == 'euclid':
            carte_distance = distance_transform_edt(matrix)
        elif distance_type == "chessboard":
            carte_distance = distance_transform_cdt(matrix)
        elif distance_type == 'manhattan':
            carte_distance = distance_transform_cdt(matrix, metric='taxicab')

        if (shape_0, shape_1) != self.shape:
            carte_distance = carte_distance[:self.shape[0], :self.shape[1]]

        return carte_distance

    def get_3d_dist_m_markers(self, distance_type, markers_map):
        """
        This function computes the 3D distance map performing the m-markers method

        Attributes
        ----------
        :param distance_type: Distance type to compute the distance map
        :type distance_type: String
        :param markers_map: Markers map
        :type markers_map: Numpy array
        :return: Distance map
        :rtype: Numpy array"""

        from skimage.measure import regionprops
        x = regionprops(markers_map.astype('uint16'))
        liste = np.zeros(len(x), dtype=(int, 3))
        for i in range(0, len(x)):
            liste[i] = x[i].centroid

        # A reshape might be necessary to compute the distance map

        shape_0, shape_1, shape_2 = self.shape
        if shape_0 % self.distance != 0:
            while shape_0 % self.distance != 0:
                shape_0 += 1
        if shape_1 % self.distance != 0:
            while shape_1 % self.distance != 0:
                shape_1 += 1
        if shape_2 % self.distance != 0:
            while shape_2 % self.distance != 0:
                shape_2 += 1
        matrix = np.ones(shape=(shape_0, shape_1, shape_2))

        for j in range(0, len(liste)):
            matrix[liste[j][0], liste[j][1], liste[j][2]] = 0

        if distance_type == 'euclid':
            carte_distance = distance_transform_edt(matrix)
        elif distance_type == "chessboard":
            carte_distance = distance_transform_cdt(matrix)
        elif distance_type == 'manhattan':
            carte_distance = distance_transform_cdt(matrix, metric='taxicab')

        if (shape_0, shape_1, shape_2) != self.shape:
            carte_distance = carte_distance[:self.shape[0], :self.shape[1], :self.shape[2]]

        return carte_distance

    def get_2d_dist_m_markers(self, distance_type, markers_map):
        """
        This function computes the 2D distance map performing the m-markers method

        Attributes
        ----------
        :param distance_type: Distance type to compute the distance map
        :type distance_type: String
        :param markers_map: Markers map
        :type markers_map: Numpy array
        :return: Distance map
        :rtype: Numpy array"""

        from skimage.measure import regionprops
        x = regionprops(markers_map.astype('uint16'))
        liste = np.zeros(len(x), dtype=(int, 2))
        for i in range(0, len(x)):
            liste[i] = x[i].centroid

        # A reshape might be necessary to compute the distance map

        shape_0, shape_1 = self.shape
        if shape_0 % self.distance != 0:
            while shape_0 % self.distance != 0:
                shape_0 += 1
        if shape_1 % self.distance != 0:
            while shape_1 % self.distance != 0:
                shape_1 += 1

        matrix = np.ones(shape=(shape_0, shape_1))
        for j in range(0, len(liste)):
            matrix[liste[j][0], liste[j][1]] = 0

        if distance_type == 'euclid':
            carte_distance = distance_transform_edt(matrix)
        elif distance_type == "chessboard":
            carte_distance = distance_transform_cdt(matrix)
        elif distance_type == 'manhattan':
            carte_distance = distance_transform_cdt(matrix, metric='taxicab')

        if (shape_0, shape_1) != self.shape:
            carte_distance = carte_distance[:self.shape[0], :self.shape[1]]

        return carte_distance

def normalize_dist_map(carte_distance):
    """
    This function normalizes the distance map between 0 and 100

    Attributes
    ----------
    :param carte_distance: Distance map
    :type carte_distance: Numpy array
    :return: Normalized map distance
    :rtype: Numpy array"""
    max_val = np.amax(carte_distance)
    carte_distance = carte_distance / max_val
    carte_distance *= 100
    return carte_distance
