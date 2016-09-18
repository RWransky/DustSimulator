import sys
import numpy as np
import matplotlib.pyplot as plt
from landscape_helpers import *
from forage_helpers import *
from plot_helpers import *

# constants used to create landscape
NUM_LANDSCAPES = 1
FIELD_LENGTH = 400
HIVE_CENTER_X = FIELD_LENGTH/2
HIVE_CENTER_Y = FIELD_LENGTH/2
NUM_FIELDS = 15
# MARGIN_WIDTH must be an even number
MARGIN_WIDTH = 10
SHOW_PLOT = False


def main():
    for i in range(0, NUM_LANDSCAPES):
        l0, exp0, l125, exp125, l25, exp25, l50, exp50, l75, exp75, l100, exp100 = plant_all_crops_weeds(FIELD_LENGTH,NUM_FIELDS,MARGIN_WIDTH,SHOW_PLOT)

        np.save('landscapes/field'+str(i)+'landscape0', np.array(l0))
        np.save('landscapes/field'+str(i)+'exposures0', np.array(exp0))
        np.save('landscapes/field'+str(i)+'landscape125', l125)
        np.save('landscapes/field'+str(i)+'exposures125', exp125)
        np.save('landscapes/field'+str(i)+'landscape25', l25)
        np.save('landscapes/field'+str(i)+'exposures25', exp25)
        np.save('landscapes/field'+str(i)+'landscape50', l50)
        np.save('landscapes/field'+str(i)+'exposures50', exp50)
        np.save('landscapes/field'+str(i)+'landscape75', l75)
        np.save('landscapes/field'+str(i)+'exposures75', exp75)
        np.save('landscapes/field'+str(i)+'landscape100', l100)
        np.save('landscapes/field'+str(i)+'exposures100', exp100)

        np.savetxt('landscapes/field'+str(i)+'landscape0.csv', l0, delimiter=",")
        np.savetxt('landscapes/field'+str(i)+'exposures0.csv', exp0, delimiter=",")
        np.savetxt('landscapes/field'+str(i)+'landscape125.csv', l125, delimiter=",")
        np.savetxt('landscapes/field'+str(i)+'exposures125.csv', exp125, delimiter=",")
        np.savetxt('landscapes/field'+str(i)+'landscape25.csv', l25, delimiter=",")
        np.savetxt('landscapes/field'+str(i)+'exposures25.csv', exp25, delimiter=",")
        np.savetxt('landscapes/field'+str(i)+'landscape50.csv', l50, delimiter=",")
        np.savetxt('landscapes/field'+str(i)+'exposures50.csv', exp50, delimiter=",")
        np.savetxt('landscapes/field'+str(i)+'landscape75.csv', l75, delimiter=",")
        np.savetxt('landscapes/field'+str(i)+'exposures75.csv', exp75, delimiter=",")
        np.savetxt('landscapes/field'+str(i)+'landscape100.csv', l100, delimiter=",")
        np.savetxt('landscapes/field'+str(i)+'exposures100.csv', exp100, delimiter=",")

if __name__ == '__main__':
    sys.exit(main())
