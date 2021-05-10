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
from scipy.ndimage.morphology import morphological_gradient
from scipy.ndimage.morphology import grey_dilation
from scipy.ndimage.morphology import grey_erosion

import logging


class Gradient:
    def __init__(self, image, struct_shape=None):
        self.image = image
        self.struct_shape = struct_shape

    def mag_gradient(self):
        """
        This function computes the gradient of the image using second order accurate central differences in the interior
        points and either first or second order accurate one-sides (forward or backwards) differences at the boundaries

        Attributes
        ----------
        :return: Gradient
        :rtype: Numpy array"""

        grad = np.gradient(self.image)
        norm = 0
        for i in range(0, len(grad)):
            norm += grad[i] ** 2
        norm = np.sqrt(norm)
        max_val = np.amax(norm)
        norm /= max_val
        norm *= 100
        return norm

    def morpho(self):
        """
        This function computes the morphological gradient of the image

        Attributes
        ----------
        :return: Morphological gradient
        :rtype: Numpy array"""

        if isinstance(self.struct_shape, int) is False:
            raise TypeError('structure shape must be an integer')
        shape = np.ones(len(self.image.shape)).astype(int) * self.struct_shape
        morpho = morphological_gradient(self.image, size=shape)
        max_val = np.amax(morpho)
        morpho = morpho / max_val
        morpho *= 100
        return morpho

    def dilation(self):
        """
        This function computes the semi morphological gradient of the image

        Attributes
        ----------
        :return: Semi morphological gradient
        :rtype: Numpy array"""

        if isinstance(self.struct_shape, int) is False:
            raise TypeError('structure shape must be an integer')
        shape = np.ones(len(self.image.shape)).astype(int) * self.struct_shape
        dilatation = grey_dilation(self.image, size=shape)
        result = dilatation - self.image
        max_val = np.amax(result)
        result = result / max_val
        result *= 100
        return result

    def erosion(self):
        """
        This function computes the semi morphological gradient of the image

        Attributes
        ----------
        :return: Semi morphological gradient
        :rtype: Numpy array"""
        if isinstance(self.struct_shape, int) is False:
            raise TypeError('structure shape must be an integer')
        shape = np.ones(len(self.image.shape)).astype(int) * self.struct_shape
        erosion = grey_erosion(self.image, size=shape)
        result = self.image - erosion
        max_val = np.amax(result)
        result = result / max_val
        result *= 100
        return result

    def inverted_image(self):
        """
        This function computes the inverted image

        Attributes
        ----------
        :return: Inverted image
        :rtype: Numpy array"""

        inverted_image = np.amax(self.image) - self.image
        max_val = np.amax(inverted_image)
        inverted_image = inverted_image / max_val
        inverted_image *= 100
        return inverted_image

    def inverted_plus_erosion(self):
        """
        This function computes the inverse of the image erosion

        Attributes
        ----------
        :return: Inverse of the image erosion
        :rtype: Numpy array"""

        if isinstance(self.struct_shape, int) is False:
            raise TypeError('structure shape must be an integer')
        shape = np.ones(len(self.image.shape)).astype(int) * self.struct_shape
        erosion = grey_erosion(self.image, size=shape)
        inverse = np.amax(erosion) - erosion
        max_val = np.amax(inverse)
        inverse = inverse / max_val
        inverse *= 100
        return inverse
