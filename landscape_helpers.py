import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi



from voronoi import *
from polygon_helpers import *
from forage_helpers import *

def create_voronoi_points(field_length,num_fields):
    points=np.random.randint(field_length,size=(num_fields,2))
    return points

def tesselate_points(field_length,num_fields):
	points=create_voronoi_points(field_length,num_fields)
	area=np.zeros((field_length,field_length))
	vor=Voronoi(points)
	regions, vertices = voronoi_finite_polygons_2d(vor)
	return area, regions, vertices, points

def euc_dist(x1,y1,x2,y2):
	return np.sqrt(pow((x1-x2),2)+pow((y1-y2),2))

def find_exp(x,y,edge):
	dists=[]
	for i in range(0,len(edge[0])):
		dists.append(euc_dist(x,y,edge[0][i],edge[1][i]))
	return dust_drift(min(dists))

def plant_all_crops_weeds(field_length,num_fields,margin_width,show_plot):
	area, regions, vertices, points = tesselate_points(field_length,num_fields)

	order = np.arange(num_fields)
	np.random.shuffle(order)
	
	zero_landscape, zero_area = plant_crops_and_weeds(area, regions, vertices, points, field_length,num_fields,margin_width,show_plot,0,order)
	twelve_landscape, twelve_area = plant_crops_and_weeds(area, regions, vertices, points, field_length,num_fields,margin_width,show_plot,0.125,order)
	twentyfive_landscape, twentyfive_area = plant_crops_and_weeds(area, regions, vertices, points, field_length,num_fields,margin_width,show_plot,0.25,order)
	fifty_landscape, fifty_area = plant_crops_and_weeds(area, regions, vertices, points, field_length,num_fields,margin_width,show_plot,0.5,order)
	seventyfive_landscape, seventyfive_area = plant_crops_and_weeds(area, regions, vertices, points, field_length,num_fields,margin_width,show_plot,0.75,order)
	hundred_landscape, hundred_area = plant_crops_and_weeds(area, regions, vertices, points, field_length,num_fields,margin_width,show_plot,1.0,order)

	fig_num = np.random.randint(100)
	plt.figure(fig_num)
	plt.imshow(np.uint8(zero_area))
	plt.xlim(-.1,field_length+0.1)
	plt.ylim(-.1,field_length+0.1)
	plt.show()

	return zero_landscape, zero_area, twelve_landscape, twelve_area, twentyfive_landscape, twentyfive_area, fifty_landscape, fifty_area, seventyfive_landscape, seventyfive_area, hundred_landscape, hundred_area 




def plant_crops_and_weeds(area, regions, vertices, points, field_length,num_fields,margin_width,show_plot,percent_weedy,order):

	forage_landscape=[]

	num_corn=np.uint32(num_fields*0.4)

	num_weedy_corn=np.uint32(num_corn*percent_weedy)

	if num_weedy_corn==0:
		if percent_weedy>0:
			num_weedy_corn=1
		
	num_weedy_soy = np.uint32((num_fields-num_corn)*.45)

	marker=[]
	#for marker 0=soy no weeds 1=soy weeds 2=corn no weeds 3=corn weeds
	for i in range(0,num_corn):
		if i<num_weedy_corn:
			marker.append(3)
		else:
			marker.append(2)
	for j in range(0,(num_fields-num_corn)):
		if j<num_weedy_soy:
			marker.append(1)
		else:
			marker.append(0)

	if show_plot:
		plt.figure(1)

	for index in range(0,num_fields):

		is_corn=False
		is_soy=False
		if marker[index]>1:
			is_corn=True
		else:
			is_soy=True

		region = regions[order[index]]
		polygon = format_polygon(vertices[region],field_length)
		centroid = points[order[index]]

		if show_plot:
			if is_corn:
				plt.fill(*zip(*polygon), facecolor='y')
			else:
				plt.fill(*zip(*polygon), facecolor='g')

		if marker[index]>0:

			polygon2=polygon.reshape(-1,1,2).astype(np.int32)
			matrix =np.zeros((field_length,field_length),dtype=np.uint8)
			poly =np.zeros((field_length,field_length),dtype=np.int32)
			cv2.drawContours(poly,[polygon2],-1,(1),thickness= -1);
			field=np.nonzero(poly)

			if marker[index]>1:
				outline=np.zeros((field_length,field_length),dtype=np.uint8)
				cv2.drawContours(matrix,[polygon2],-1,(1),thickness= -1);
				kernel = np.ones((3,3),np.uint8)
				matrix = cv2.dilate(matrix,kernel,iterations = 1)
				outline = matrix-poly

				# cv2.polylines(outline,[polygon2],False,1)

				# matrix2=matrix.astype(np.uint8)
				# contours = cv2.findContours(matrix2, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
				# cnt=contours[0]
				# M = cv2.moments(cnt)
				# cx = int(M['m10']/M['m00'])
				# cy = int(M['m01']/M['m00'])
				# overlay=cv2.circle(matrix,(int(centroid[0]),int(centroid[1])), int(1.5*margin_width), (1), -1)
				# overlay2=overlay-poly
				# margin=np.nonzero(overlay2)
				edge=np.nonzero(outline)

			if marker[index]==1:
				for i in range(0,len(field[0][:])):
					forage_landscape.append((field[0][i],field[1][i]))
			if marker[index]==2:
				forage_landscape, area = spread_dust(poly,edge, margin_width,field_length,forage_landscape,area)
				del(edge); 
			if marker[index]==3:
				forage_landscape, area = spread_dust(poly,edge, margin_width,field_length,forage_landscape,area)
				del(edge); 
				for j in range(0,len(field[0][:])):
					forage_landscape.append((field[0][j],field[1][j]))
					area[field[0][j],field[1][j]]=area[field[0][j],field[1][j]]+dust_drift(0)
			del(field); del(matrix); del(poly);
	if show_plot:
		plt.xlim(0-0.1,field_length+0.1)
		plt.ylim(0-0.1,field_length+0.1)
		plt.show()

	# kernel = np.ones((5,5),np.uint8)
	# area = cv2.dilate(area,kernel,iterations = 1)
	return forage_landscape, area

def format_polygon(polygon,field_length):
	newPoly = polygon
	for j in range(0,len(polygon[:])):
		for i in range(0,2):
			if polygon[j][i]<0:
				newPoly[j][i] = 0
			elif polygon[j][i]>field_length:
				newPoly[j][i] = field_length
			else:
				newPoly[j][i] = polygon[j][i]
	return newPoly


def spread_dust(poly,polygon,margin_width,field_length,forage_landscape,area):
	numbp = len(polygon[0])
	for border in range(0,numbp):
		if (border == numbp-1):
			x1 = polygon[0][border]; y1 = polygon[1][border]
			x2 = polygon[0][0]; y2 = polygon[1][0]
		else:
			x1 = polygon[0][border]; y1 = polygon[1][border]
			x2 = polygon[0][border+1]; y2 = polygon[1][border+1]
		if x1<=x2:
			xstart=x1; xend=x2
		else:
			xstart=x2; xend=x1
		if y1<=y2:
			ystart=y1; yend=y2;
		else:
			ystart=y2; yend=y1
		deltax = x2-x1; deltay = y2-y1;
		if (deltax == 0):
			if x1<=x2:
				xstart=x1; xend=x2
				ystart=y1; yend=y2
			else:
				xstart=x2; xend=x1
				ystart=y2; yend=y1
			for y in range(int(ystart),int(yend)):
				for margin_patch in range(-margin_width/2,margin_width/2):
					x = xstart
					if 0<y<field_length:
						if 0<x+margin_patch<field_length:
							newX=int(x+margin_patch)
							newY=int(y)
							if (poly[newX,newY]==0) & ((margin_patch+margin_width/2)>0):
								forage_landscape.append((newX,newY))
								area[newX,newY]=area[newX,newY]+dust_drift(abs(margin_patch+margin_width/2))
		elif (deltay==0):
			if x1<=x2:
				xstart=x1; xend=x2
				ystart=y1; yend=y2
			else:
				xstart=x2; xend=x1
				ystart=y2; yend=y1
			for x in range(int(xstart),int(xend)):
				for margin_patch in range(-margin_width/2,margin_width/2):
					y = ystart
					if 0<y<field_length:
						if 0<x+margin_patch<field_length:
							newX=int(x+margin_patch)
							newY=int(y)
							if (poly[newX,newY]==0) & ((margin_patch+margin_width/2)>0):
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
							if (poly[newX,newY]==0) & ((margin_patch+margin_width/2)>0):
								forage_landscape.append((newX,newY))
								area[newX,newY]=area[newX,newY]+dust_drift(abs(margin_patch+margin_width/2))
	return forage_landscape, area

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
		print(region)
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
		plt.xlim(0-0.1,field_length+0.1)
		plt.ylim(0-0.1,field_length+0.1)
		plt.show()

	kernel = np.ones((5,5),np.uint8)
	area = cv2.dilate(area,kernel,iterations = 1)
	return forage_landscape, area
