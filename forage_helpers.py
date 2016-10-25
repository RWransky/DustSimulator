import numpy as np
import time
from tqdm import *
from scipy.spatial import distance


# dust drift function
# NOTE INPUT IS IN METERS


def dust_drift(meter):
    if meter == 0:
        return 4.47 + 1.95
    elif meter <= 1:
        return 2.08
    elif meter <= 10:
        return 1.95
    elif meter <= 50:
        return 1.45
    elif meter <= 100:
        return 0.98
    else:
        return 0


def contaminate(flower, corn):
    ll = (flower[0]-200, flower[1]-200)  # lower-left
    ur = (flower[0]+200, flower[1]+200)  # upper-right
    inidx = np.where((corn <= ur).all(axis=1) & (corn >= ll).all(axis=1))
    if corn[inidx].shape[0] == 0:
        return 0
    else:
        dist = distance.cdist(corn[inidx], np.reshape(flower, (1, 2)), 'euclidean')
        lowest_dist = np.min(dist)
        return dust_drift(lowest_dist)


# function for the distance to the hive
def dist_hive(x, y, HIVE_CENTER_X, HIVE_CENTER_Y):
    distance_to_hive = np.sqrt(pow((x-HIVE_CENTER_X), 2)+pow((y-HIVE_CENTER_Y), 2))
    return distance_to_hive

#function to pick the 10 foraging locations
#function takes a random sample of potential foraging locations
#returns 10 most likely foraging sites based on distance to hive
# def foraging_sites(forage_points):
#     visit_prob=[]; number_list=[]
#     numb_points=len(forage_points)
#     pick20 = np.random.randint(numb_points,size=(100,1))
#     def getKey(item):
#         return item[0]
#     for i in range(0,100):
#         prob=dist_hive(forage_points[pick20[i]][0],forage_points[pick20[i]][1])
#         #prob=0.1227*np.exp(-0.002151*dist_hive(forage_points[pick20[i]][0],forage_points[pick20[i]][1]))
#         visit_prob.append([prob,forage_points[pick20[i]][0],forage_points[pick20[i]][1]])

#     sorted_20=sorted(visit_prob,key=getKey)

#     top10=sorted_20[0:10]
#     top10_points=np.zeros((10,2))
#     top10_prob=np.zeros((10,1))
#     for i in range(0,10):
#         top10_points[i,0]=top10[i][1]
#         top10_points[i,1]=top10[i][2]
#         top10_prob[i]=top10[i][0]

#     return top10_prob, top10_points


def group_indices(arr, value):
    ind = np.where((arr == value))
    if len(ind[0]) == 0:
        return []
    elif len(ind[0]) <= value:
        return ind[0]
    else:
        if value == 0:
            value = 1
        np.random.shuffle(ind)
        return ind[0][0:value]


def bin_and_select(arr):
    indices = []
    max_val = np.max(arr)
    seq = np.uint32(np.around(np.linspace(0, max_val+10, num=((max_val+20)/10)), decimals=-1))
    bin_amounts = np.histogram(arr, bins=seq)
    for i in range(len(seq)-1):
        if bin_amounts[0][i] > 0:
            inds = group_indices(arr, seq[i])
            for ind in inds:
                indices.append(ind)
    return indices


def foraging_sites2(forage_points, HIVE_CENTER_X, HIVE_CENTER_Y):
    numb_points = forage_points.shape[0]
    points = np.zeros((numb_points, 3))

    for i in range(numb_points):
        distance = dist_hive(forage_points[i][0], forage_points[i][1], HIVE_CENTER_X, HIVE_CENTER_Y)
        points[i][0] = (0.1204)*np.exp(-0.001404*distance)
        points[i][1] = forage_points[i][0]
        points[i][2] = forage_points[i][1]

    min_apv = np.min(points[:, 0])
    points[:, 0] /= min_apv
    points[:, 0] = np.around(points[:, 0], decimals=-1)
    indices = bin_and_select(points[:, 0])
    np.random.shuffle(indices)
    visit_points = np.zeros((10, 3))
    for i in range(10):
        visit_points[i] = points[indices[i]]
    return visit_points


def print_concentrations(top10, area):
    for i in range(0,10):
        print area[top10[i,0]][top10[i,1]]

def random_walk(startx, starty, area):
    landscape_size = np.size(area, 1)
    newx = startx
    newy = starty
    total_exp = area[int(newx), int(newy)]
    for i in range(0, 9):
        num_tries = 0
        previousx = newx
        previousy = newy
        np.random.seed()
        concent = 0
        if area[int(previousx),int(previousy)] == 0:
            horiz = np.random.randint(-1, 2, size=(1, 1))
            vert = np.random.randint(-1,2,size=(1,1))
            newx = previousx+horiz if 0<previousx+horiz<landscape_size else previousx
            newy = previousy+vert if 0<previousy+vert<landscape_size else previousy
            concent = area[int(newx),int(newy)]
        else:
            while concent == 0 & num_tries < 10:
                horiz = np.random.randint(-1, 2, size=(1,1))
                vert = np.random.randint(-1, 2, size=(1,1))
                newx = previousx+horiz if 0 < previousx+horiz<landscape_size else previousx
                newy = previousy+vert if 0 < previousy+vert<landscape_size else previousy
                concent = area[int(newx), int(newy)]
                num_tries += 1
        total_exp += concent

    return (total_exp/10)


def random_walk_fast(startx, starty, corn, field_length, forage):
    landscape_size = field_length
    newx = startx
    newy = starty
    total_exp = contaminate([newx, newy], corn)
    for i in range(0, 7):
        num_tries = 0
        previousx = newx
        previousy = newy
        np.random.seed()
        horiz = np.random.randint(-1, 2, size=(1, 1))
        vert = np.random.randint(-1, 2, size=(1, 1))
        newx = previousx+horiz if 0 < previousx+horiz < landscape_size else previousx
        newy = previousy+vert if 0 < previousy+vert < landscape_size else previousy
        concent = 0
        if not valid_patch(forage, [int(newx), int(newy)]):
            while not valid_patch(forage, [int(newx), int(newy)]) & num_tries < 10:
                horiz = np.random.randint(-1, 2, size=(1, 1))
                vert = np.random.randint(-1, 2, size=(1, 1))
                newx = previousx+horiz if 0 < previousx+horiz < landscape_size else previousx
                newy = previousy+vert if 0 < previousy+vert < landscape_size else previousy
                num_tries += 1

            if num_tries < 10:
                concent = contaminate([int(newx), int(newy)], corn)
            else:
                concent = 0
        else:
            concent = contaminate([int(newx), int(newy)], corn)

        total_exp += concent

    return (total_exp/10)


def hit_or_miss(top10,radius,area):
    stretch = np.sqrt(pow(radius,2)/2)
    bee_exposure=np.zeros((10000,1))
    for i in range(0,10):
        for j in range(0,1000):
            centerx=top10[i,1]+np.random.randint(-stretch,stretch,size=(1,1))
            centery=top10[i,2]+np.random.randint(-stretch,stretch,size=(1,1))
            bee_exposure[int((i*1000)+j)]=random_walk(centerx,centery,area)

    return bee_exposure


def valid_patch(forage_points, pt):
    inidx = np.where((forage_points == pt).all(axis=1))
    if forage_points[inidx].shape[0] > 0:
        return True
    else:
        return False


def select_patch(forage_points, x, y, radius, landscape_size):
    half_radii = round(radius/2)
    horiz = np.random.randint(-half_radii, half_radii, size=(1, 1))
    vert = np.random.randint(-half_radii, half_radii, size=(1, 1))
    newx = x+horiz if 0 < x+horiz < landscape_size else x
    newy = y+vert if 0 < y+vert < landscape_size else y
    while not valid_patch(forage_points, (int(newx), int(newy))):
        horiz = np.random.randint(-half_radii, half_radii, size=(1, 1))
        vert = np.random.randint(-half_radii, half_radii, size=(1, 1))
        newx = x+horiz if 0 < x+horiz < landscape_size else x
        newy = y+vert if 0 < y+vert < landscape_size else y
    return int(newx), int(newy)


def hit_or_miss2(top10, radius, area, forage_points):
    bee_exposure = np.zeros((1000,1))
    for i in range(0, 10):
        print 'foraging group {}'.format(i)
        for j in range(0, 100):
            centerx, centery = select_patch(forage_points, top10[i, 1], top10[i, 2], radius)
            bee_exposure[int((i*100)+j)] = random_walk_fast(centerx, centery, area)

    return bee_exposure


def hit_or_miss2_fast(top10, radius, corn, forage, field_length):
    bee_exposure = np.zeros((1000, 1))
    for i in range(10):
        print 'foraging group {}'.format(i)
        for j in range(100):
            centerx, centery = select_patch(forage, top10[i, 1], top10[i, 2], radius, field_length)
            bee_exposure[int((i*100)+j)] = random_walk_fast(centerx, centery, corn, field_length, forage)

    return bee_exposure


#prob,pts = foraging_sites(forage_landscape)
def iterate_foraging(forage_land,radius,area,hiveX,hiveY,iterations):
    concentrations=[]
    ###### NOTE: Large iterations will kill your cpu
    for i in range(0,iterations):
        pts=foraging_sites2(forage_land,hiveX,hiveY)
        bee_levels = hit_or_miss2(pts,radius,area,forage_land)
        for j in range(0,1000):
            concentrations.append(bee_levels[j][0])
            
    return concentrations


def iterate_foraging_fast(forage, corn, hiveX, hiveY, field_length, radius, iterations):
    concentrations = []
    for i in range(iterations):
        pts = foraging_sites2(forage, hiveX, hiveY)
        bee_levels = hit_or_miss2_fast(pts, radius, corn, forage, field_length)
        for j in range(1000):
            concentrations.append(bee_levels[j][0])
            
    return concentrations


def validate_foraging(forage_land):
    point_scatter=[]
    for i in range(0,10):
        pts = foraging_sites2(forage_land)
        for j in range(0,10):
            point_scatter.append(pts[j][0])
            
    return point_scatter


def Markov_foraging(forage_points,area,HIVE_CENTER_X,HIVE_CENTER_Y,FORAGE_RADIUS,NUM_ITERATIONS):
    concentrations = iterate_foraging(forage_points,FORAGE_RADIUS,area,HIVE_CENTER_X,HIVE_CENTER_Y,NUM_ITERATIONS)
    return concentrations


def Markov_foraging_fast(forage_pts, corn_pts, HIVE_CENTER_X, HIVE_CENTER_Y, FIELD_SIZE, FORAGE_RADIUS, NUM_ITERATIONS):
    concentrations = iterate_foraging_fast(np.array(forage_pts), np.array(corn_pts), HIVE_CENTER_X, HIVE_CENTER_Y, FIELD_SIZE, FORAGE_RADIUS, NUM_ITERATIONS)
    return concentrations
