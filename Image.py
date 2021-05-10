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

import os

import nibabel
import numpy as np
from scipy.misc import imsave

from scipy.ndimage import imread


def save_as_nifti(img, filename, header):
    """
    Save a numpy array as a NIFTI image

    Attributes
    ----------
    :param img: Image to be saved
    :type img: Numpy array
    :param filename: Output file name
    :type img: Numpy array
    :param img: Image to be saved
    :type img: Numpy array
    """
    res = NiFTI(img, np.eye(4), header)
    res.to_filename(filename + '.nii.gz')


def save_as_jpeg(img, filename):
    """
    Save a numpy array as a jpeg image

    Attributes
    ----------

    :param img: Image to be saved
    :type img: Numpy array
    """
    imsave(filename + '.png', img, 'png')


def get_header(img):
    """
    Gets the header of a NIFTI image

    Attributes
    ----------

    :param img: NIFTI image
    :type img: Image
    :return: Image header
    :rtype: nibabel.nifti1.Nifti1Header"""
    return img.header


class Image:

    def __init__(self, path):
        self.path = path

    def get_image(self):
        """
        Stores the raw image into a Numpy array

        Attributes
        ----------
        :return: Matrix
        :rtype: Numpy array"""
        image = None
        img = None
        if self.path.endswith('nii.gz'):
            img = nibabel.load(self.path)
            image = np.array(img.dataobj)
        elif self.path.endswith('png') or self.path.endswith('jpg') or self.path.endswith('jpeg'):
            image = imread(self.path, mode='F')
            img = None
        return image, img


class NiFTI (nibabel.Nifti1Image):
    def update_header(self):
        pass
