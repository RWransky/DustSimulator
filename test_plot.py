import numpy as np
import matplotlib.pyplot as plt
from landscape_helpers import *
from forage_helpers import *
from plot_helpers import *

#constants used to create landscape
FIELD_LENGTH = 400
HIVE_CENTER_X = FIELD_LENGTH/2
HIVE_CENTER_Y = FIELD_LENGTH/2
FORAGE_RADIUS = 250
PERCENT_WEEDY = 0.125
NUM_ITERATIONS = 2
NUM_FIELDS = 25
#MARGIN_WIDTH must be an even number
MARGIN_WIDTH = 100
SHOW_PLOT =False
NUM_BINS = 500
XLIM_MAX = 10
BAR_WIDTH = 0.1

test = np.load('field1exposures0%.npy')

plt.figure(3)
plt.imshow(np.uint8(test))
plt.xlim(-.1,FIELD_LENGTH+0.1)
plt.ylim(-.1,FIELD_LENGTH+0.1)
plt.show()
