import matplotlib.pyplot as plt

def histogram_exposures(concentrations,NUM_BINS,XLIM_MAX,BAR_WIDTH):
	n, bins, patches = plt.hist(concentrations, NUM_BINS, facecolor='green', alpha=0.5)
	plt.figure(2)
	plt.xlim(0,XLIM_MAX)
	plt.bar(bins[0:NUM_BINS],n[0:NUM_BINS],width=BAR_WIDTH)