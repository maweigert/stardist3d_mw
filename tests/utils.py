import os
import numpy as np
from tifffile import imread
from skimage.measure import label
from scipy.ndimage.filters import gaussian_filter


def random_image(shape=(128, 128)):
    img = gaussian_filter(np.random.normal(size=shape), min(shape) / 20)
    img = img > np.percentile(img, 80)
    img = label(img)
    img[img > 255] = img[img > 255] % 254 + 1
    return img


def circle_image(shape=(128, 128), center=None):
    if center is None:
        center = (0,)*len(shape)
    xs = tuple(np.linspace(-1, 1, s) for s in shape)
    Xs = np.meshgrid(*xs, indexing="ij")
    R = np.sqrt(np.sum([(X - c) ** 2 for X, c in zip(Xs, center)], axis=0))
    img = R < .5
    return img


def overlap_image(shape=(128, 128)):
    img1 = circle_image(shape, center=(0.1,) * len(shape))
    img2 = circle_image(shape, center=(-0.1,) * len(shape))
    img = np.maximum(img1, 2 * img2)
    overlap = np.count_nonzero(np.bitwise_and(img1 > 0, img2 > 0))
    A1 = np.count_nonzero(img1 > 0)
    A2 = np.count_nonzero(img2 > 0)

    iou = overlap / min(A1, A2)
    return img, iou


def real_image2d():
    root = os.path.dirname(os.path.abspath(__file__))
    img = imread(os.path.join(root, 'data', 'mask2d.tif'))
    return img


def real_image3d():
    root = os.path.dirname(os.path.abspath(__file__))
    img = imread(os.path.join(root, 'data', 'mask3d.tif'))
    return img


def check_similar(x, y):
    delta = np.abs(x - y)
    debug = 'avg abs err = %.10f, max abs err = %.10f' % (np.mean(delta), np.max(delta))
    assert np.allclose(x, y), debug
