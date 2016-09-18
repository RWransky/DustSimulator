import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi

from voronoi import *
from polygon_helpers import *
from landscape_helpers import *


def histogram_exposures(concentrations, NUM_BINS, XLIM_MAX, BAR_WIDTH):
    plt.figure(3)
    n, bins, patches = plt.hist(concentrations, NUM_BINS, facecolor='green', alpha=0.5)
    plt.show()
    plt.figure(4)
    plt.xlim(0, XLIM_MAX)
    plt.bar(bins[0:NUM_BINS], n[0:NUM_BINS], width=BAR_WIDTH)
    plt.show()


def plot_crops_and_weeds(forage_landscape):
    plt.figure(1)
    for point in forage_landscape:
        plt.plot(point[0], point[1], 'ko')

    plt.xlim(-.1, field_length+0.1)
    plt.ylim(-.1, field_length+0.1)
    plt.show()
