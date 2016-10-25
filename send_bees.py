import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from forage_helpers import *
from plot_helpers import *

# constants used to create landscape
NUM_LANDSCAPES = 1
FIELD_LENGTH = 4000
HIVE_CENTER_X = FIELD_LENGTH/2
HIVE_CENTER_Y = FIELD_LENGTH/2
FORAGE_RADIUS = 250
NUM_ITERATIONS = 1

# MARGIN_WIDTH must be an even number
MARGIN_WIDTH = 10
SHOW_PLOT = False
NUM_BINS = 500
XLIM_MAX = 7
BAR_WIDTH = 0.1


def main():
    levels = [0, 12, 25, 50, 80, 100]
    for i in range(0, NUM_LANDSCAPES):
        for percent in levels:
            print 'procssing field {} with {}% percent weedy corn'.format(str(i), str(percent))
            corn_landscape = np.load('landscapes/corn{}_percent{}.npy'.format(str(i), str(percent)))
            forage_landscape = np.load('landscapes/flowers{}_percent{}.npy'.format(str(i), str(percent)))

            exposures = Markov_foraging_fast(forage_landscape, corn_landscape, HIVE_CENTER_X, HIVE_CENTER_Y, FIELD_LENGTH, FORAGE_RADIUS, NUM_ITERATIONS)
            print 'Highest exposure recorded {}'.format(str(np.max(exposures)))
            np.savetxt('exposures/field_{}_bee_exposures_{}.csv'.format(str(i), str(percent)), exposures, delimiter=",")
            # histogram_exposures(exposures, NUM_BINS, XLIM_MAX, BAR_WIDTH)


if __name__ == '__main__':
    sys.exit(main())
