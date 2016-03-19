import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi



from voronoi import *
from polygon_helpers import *
from forage_helpers import *

def create_voronoi_points(field_length,num_fields):
    np.random.seed(1234567)
    points=np.random.randint(field_length,size=(num_fields,2))
    return points

def tesselate_points(field_length,num_fields):
	points=create_voronoi_points(field_length,num_fields)
	area=np.zeros((field_length,field_length))
	vor=Voronoi(points)
	regions, vertices = voronoi_finite_polygons_2d(vor)
	return area, regions, vertices, points

def plant_crops(field_length,num_fields,margin_width,show_plot):
	area, regions, vertices, points = tesselate_points(field_length,num_fields)

	forage_landscape=[]
	np.random.seed()

	count_corn=0
	count_centroids=0

	if show_plot:
		plt.figure(1)

	for region in regions:
		is_corn=False
		if(count_corn % 2)==0:
			is_corn=True
		count_corn+=1

		polygon = vertices[region]
		centroid = points[count_centroids]

		count_centroids+=1

		numbp=len(polygon[:,0])

		if show_plot:
			if is_corn:
				plt.fill(*zip(*polygon), facecolor='y')
			else:
				plt.fill(*zip(*polygon), facecolor='g')

		if is_corn:
			for border in range(0,numbp):
				if (border == numbp-1):
					x1 = polygon[border,0]; y1 = polygon[border,1]
					x2 = polygon[0,0]; y2 = polygon[0,1]
				else:
					x1 = polygon[border,0]; y1 = polygon[border,1]
					x2 = polygon[border+1,0]; y2 = polygon[border+1,1]
				if x1<=x2:
					xstart=x1; xend=x2
				else:
					xstart=x2; xend=x1
				if y1<=y2:
					ystart=y1; yend=y2;
				else:
					ystart=y2; yend=y1
				deltax = x2-x1; deltay = y2-y1;
				if (abs(deltay/deltax) > 10):
					if x1<=x2:
						xstart=x1; xend=x2
						ystart=y1; yend=y2
					else:
						xstart=x2; xend=x1
						ystart=y2; yend=y1
					m = deltay/deltax
					for y in range(int(ystart),int(yend)):
						for margin_patch in range(-margin_width/2,margin_width/2):
							x = xstart
							if 0<y<field_length:
								if 0<x+margin_patch<field_length:
									newX=int(x+margin_patch)
									newY=int(y)
									forage_landscape.append((newX,newY))
									area[newX,newY]=area[newX,newY]+dust_drift(abs(margin_patch+margin_width/2))
				elif (abs(deltay/deltax) < .001):
					if x1<=x2:
						xstart=x1; xend=x2
						ystart=y1; yend=y2
					else:
						xstart=x2; xend=x1
						ystart=y2; yend=y1
					m = deltay/deltax
					for x in range(int(xstart),int(xend)):
						for margin_patch in range(-margin_width/2,margin_width/2):
							y = ystart
							if 0<y<field_length:
								if 0<x+margin_patch<field_length:
									newX=int(x+margin_patch)
									newY=int(y)
									forage_landscape.append((newX,newY))
									area[newX,newY]=area[newX,newY]+dust_drift(abs(margin_patch+margin_width/2))
				else:
					if x1<=x2:
						xstart=x1; xend=x2
						ystart=y1; yend=y2
					else:
						xstart=x2; xend=x1
						ystart=y2; yend=y1
					m = deltay/deltax
					for x in range(int(xstart),int(xend)):
						for margin_patch in range(-margin_width/2,margin_width/2):
							y = (m*(x)) + (ystart-(m*xstart))
							if 0<y<field_length:
								if 0<x+margin_patch<field_length:
									newX=int(x+margin_patch)
									newY=int(y)
									forage_landscape.append((newX,newY))
									area[newX,newY]=area[newX,newY]+dust_drift(abs(margin_patch+margin_width/2))
			
	if show_plot:
		plt.xlim(0-0.1,4000+0.1)
		plt.ylim(0-0.1,4000+0.1)
		plt.show()

	kernel = np.ones((5,5),np.uint8)
	area = cv2.dilate(area,kernel,iterations = 1)
	return forage_landscape, area
