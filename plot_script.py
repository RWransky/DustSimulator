import sys
import numpy as np
import matplotlib.pyplot as plt
from plot_helpers import *

# Plotting constants
NUM_BINS = 500
XLIM_MAX = 1000
BAR_WIDTH = 0.1

# constants for landscapes
FIELD_LENGTH = 400
HIVE_CENTER_X = FIELD_LENGTH/2
HIVE_CENTER_Y = FIELD_LENGTH/2
NUM_FIELDS = 15
# MARGIN_WIDTH must be an even number
MARGIN_WIDTH = 10

FIELD_NUMBER = 0
WEEDY_PERCENTAGE = 0


def main():
    landscape = np.load('landscapes/field{}landscape{}.npy'.format(FIELD_NUMBER, WEEDY_PERCENTAGE))
    dirty_field = np.load('landscapes/field{}exposures{}.npy'.format(FIELD_NUMBER, WEEDY_PERCENTAGE))

    # show all forageable points on the map
    # this will take a long time!
    # plot_crops_and_weeds(landscape)

    plt.figure(2)
    plt.imshow(np.uint8(dirty_field))
    plt.xlim(-.1, FIELD_LENGTH+0.1)
    plt.ylim(-.1, FIELD_LENGTH+0.1)
    plt.show()

    exposures = np.loadtxt('exposures/field_{}_bee_exposures_{}.csv'.format(FIELD_NUMBER, WEEDY_PERCENTAGE))
    histogram_exposures(exposures, NUM_BINS, XLIM_MAX, BAR_WIDTH)

if __name__ == '__main__':
    sys.exit(main())
