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
FORAGE_RADIUS = 25
NUM_ITERATIONS = 1

# MARGIN_WIDTH must be an even number
MARGIN_WIDTH = 100
SHOW_PLOT = False
NUM_BINS = 500
XLIM_MAX = 10
BAR_WIDTH = 0.1


def main():
    levels = ['0'] # ['0', '125', '25', '50', '75', '100']
    for i in range(0, NUM_LANDSCAPES):
        for level in levels:
            print 'procssing fields with {} percent weedy'.format(level)
            forage_landscape = np.load('landscapes/field'+str(i)+'landscape' + str(level) + '.npy')

            field_exposures = np.load('landscapes/field'+str(i)+'exposures' + str(level) + '.npy')

            exposures = Markov_foraging(forage_landscape, field_exposures, HIVE_CENTER_X, HIVE_CENTER_Y, FORAGE_RADIUS, NUM_ITERATIONS)
            np.savetxt('exposures/field_'+str(i)+'_bee_exposures_' + str(level) + '.csv', exposures, delimiter=",")
            histogram_exposures(exposures, NUM_BINS, XLIM_MAX, BAR_WIDTH)


if __name__ == '__main__':
    sys.exit(main())
