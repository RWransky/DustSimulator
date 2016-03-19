import numpy as np
import matplotlib.pyplot as plt
from landscape_helpers import *
from forage_helpers import *
#constants used to create landscape
FIELD_LENGTH = 4000
HIVE_CENTER_X = FIELD_LENGTH/2
HIVE_CENTER_Y = FIELD_LENGTH/2
NUM_FIELDS = 25
#MARGIN_WIDTH must be an even number
MARGIN_WIDTH = 150
SHOW_PLOT = False


forage_landscape, exposure_concentrations = plant_crops(FIELD_LENGTH,NUM_FIELDS,MARGIN_WIDTH,SHOW_PLOT)

plt.imshow(exposure_concentrations,interpolation='nearest')
plt.xlim(-.1,4000.1)
plt.ylim(-.1,4000.1)
plt.show()

# If we want to save landscapes we can use this function
# np.save('test',exposure_concentrations)

Markov_foraging(HIVE_CENTER_X,HIVE_CENTER_Y)