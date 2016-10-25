import sys
import numpy as np
import matplotlib.pyplot as plt
from plot_helpers import *

# Plotting constants
NUM_BINS = 500
XLIM_MAX = 7
BAR_WIDTH = 0.1

# constants for landscapes
FIELD_LENGTH = 2000
HIVE_CENTER_X = FIELD_LENGTH/2
HIVE_CENTER_Y = FIELD_LENGTH/2
NUM_FIELDS = 25
# MARGIN_WIDTH must be an even number
MARGIN_WIDTH = 10

FIELD_NUMBER = 0
WEEDY_PERCENTAGE = 0


def main():

    exposures = np.loadtxt('exposures/field_{}_bee_exposures_{}.csv'.format(FIELD_NUMBER, WEEDY_PERCENTAGE))
    histogram_exposures(exposures, NUM_BINS, XLIM_MAX, BAR_WIDTH)

if __name__ == '__main__':
    sys.exit(main())
