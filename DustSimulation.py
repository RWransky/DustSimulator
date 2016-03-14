# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 08:36:11 2015

@author: michaelwransky
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi








##### WARNING: If you want to iterate the simulation uncomment the line below
#concentrations=iterate_foraging(forage_landscape,area)

pts=foraging_sites2(forage_landscape)
plt.plot(pts[:,1],pts[:,2],'ko')
concentrations = hit_or_miss(pts,500,area)


  
#
num_bins = 500
## the histogram of the data
n, bins, patches = plt.hist(concentrations, num_bins, facecolor='green', alpha=0.5)

plt.figure(2)
plt.xlim(0,9)
plt.bar(bins[0:500],n[0:500],width=0.1)

plt.figure(3)


#plt.plot(points[:,0], points[:,1], 'ko')
#plt.xlim(0 - 0.1, 4000 + 0.1)
#plt.ylim(0 - 0.1, 4000 + 0.1)


            
pts_scatter = validate_foraging(forage_landscape)
n2,bins2,patches2 = plt.hist(pts_scatter,10,facecolor='green',alpha=0.5)



#plt.show()

# plt.imshow(area)
# plt.show()