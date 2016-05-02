import numpy as np
import matplotlib.pyplot as plt
from landscape_helpers import *
from forage_helpers import *
from plot_helpers import *

#constants used to create landscape
FIELD_LENGTH = 4000
HIVE_CENTER_X = FIELD_LENGTH/2
HIVE_CENTER_Y = FIELD_LENGTH/2
NUM_FIELDS = 15
#MARGIN_WIDTH must be an even number
MARGIN_WIDTH = 100
SHOW_PLOT =False

for i in range(0,5):
	l0, exp0, l125, exp125, l25, exp25, l50, exp50, l75, exp75, l100, exp100 = plant_all_crops_weeds(FIELD_LENGTH,NUM_FIELDS,MARGIN_WIDTH,SHOW_PLOT)

	np.save('field'+str(i)+'landscape0%',l0)
	np.save('field'+str(i)+'exposures0%',exp0)
	np.save('field'+str(i)+'landscape125%',l125)
	np.save('field'+str(i)+'exposures125%',exp125)
	np.save('field'+str(i)+'landscape25%',l25)
	np.save('field'+str(i)+'exposures25%',exp25)
	np.save('field'+str(i)+'landscape50%',l50)
	np.save('field'+str(i)+'exposures50%',exp50)
	np.save('field'+str(i)+'landscape75%',l75)
	np.save('field'+str(i)+'exposures75%',exp75)
	np.save('field'+str(i)+'landscape100%',l100)
	np.save('field'+str(i)+'exposures100%',exp100)