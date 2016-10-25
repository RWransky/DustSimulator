import sys
import time
from tqdm import *
import numpy as np
import matplotlib.pyplot as plt
from landscape_helpers import *
from forage_helpers import *
from plot_helpers import *
from margin_generator import *

# constants used to create landscape
NUM_LANDSCAPES = 1
FIELD_LENGTH = 4000
HIVE_CENTER_X = FIELD_LENGTH/2
HIVE_CENTER_Y = FIELD_LENGTH/2
NUM_FIELDS = 25
# MARGIN_WIDTH must be an even number
MARGIN_WIDTH = 10
SHOW_PLOT = False


def main():
    for i in range(NUM_LANDSCAPES):
        create_fields(FIELD_LENGTH, NUM_FIELDS, MARGIN_WIDTH, i)


if __name__ == '__main__':
    sys.exit(main())
