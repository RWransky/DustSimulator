import numpy as np

#dust drift function
#NOTE INPUT IS IN METERS
def dust_drift(meter):
    if meter == 0:
        return 46.62
    elif meter <= 10:
        return 19.69
    elif meter <= 50:
        return 5.19
    elif meter <= 100:
        return 4.5
    else:
        return 0


    concentration = a*np.exp(b*meter)+c*np.exp(d*meter)
    return concentration

#function for the distance to the hive
def dist_hive(x,y,HIVE_CENTER_X,HIVE_CENTER_Y):
    distance_to_hive = np.sqrt(pow((x-HIVE_CENTER_X),2)+pow((y-HIVE_CENTER_Y),2))
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
    
def foraging_sites2(forage_points,HIVE_CENTER_X,HIVE_CENTER_Y):
    numb_points=len(forage_points)
    points=np.zeros((numb_points,3))
    
    for i in range(0,numb_points):
        distance=dist_hive(forage_points[i][0],forage_points[i][1],HIVE_CENTER_X,HIVE_CENTER_Y)
        points[i][0]=distance
        points[i][1]=forage_points[i][0]
        points[i][2]=forage_points[i][1]
        
    points.view('i8,i8,i8').sort(order=['f0'], axis=0)
    
    ten_percent=round(.01*numb_points)
    seventy_percent=round(.7*numb_points)
    
    five_points=points[np.random.randint(0,ten_percent,size=7),:]
    three_points=points[np.random.randint(ten_percent,seventy_percent,size=2),:]
    two_points=points[np.random.randint(seventy_percent,numb_points,size=1),:]
    
    visit_points=np.zeros((10,3))
    visit_points[0:7][:]=five_points
    visit_points[7:9][:]=three_points
    visit_points[9:10][:]=two_points
            
    return visit_points
            
def print_concentrations(top10,area):
    for i in range(0,10):
        print area[top10[i,0]][top10[i,1]]

def random_walk(startx,starty,area):
    landscape_size = np.size(area,1)
    newx = startx
    newy = starty
    total_exp = area[int(newx),int(newy)]
    for i in range(0,9):
        previousx=newx; previousy=newy
        np.random.seed()
        concent = 0
        if area[int(previousx),int(previousy)]==0:
            horiz = np.random.randint(-1,2,size=(1,1))
            vert = np.random.randint(-1,2,size=(1,1))
            newx = previousx+horiz if 0<previousx+horiz<landscape_size else previousx
            newy = previousy+vert if 0<previousy+vert<landscape_size else previousy
            concent = area[int(newx),int(newy)]
        else:
            while concent==0:
                horiz = np.random.randint(-1,2,size=(1,1))
                vert = np.random.randint(-1,2,size=(1,1))
                newx = previousx+horiz if 0<previousx+horiz<landscape_size else previousx
                newy = previousy+vert if 0<previousy+vert<landscape_size else previousy
                concent = area[int(newx),int(newy)]
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
            print(i*1000+j)
           
    return bee_exposure

def select_patch(forage_points,x,y,radius):
    numb_points = len(forage_points)
    rand_point = forage_points[np.random.randint(numb_points,size=(1,1))]
    while dist_hive(x,y,rand_point[0],rand_point[1]) > radius:
        rand_point = forage_points[np.random.randint(numb_points,size=(1,1))]

    return rand_point[0], rand_point[1]

def hit_or_miss2(top10,radius,area,forage_points):
    bee_exposure=np.zeros((1000,1))
    for i in range(0,10):
        for j in range(0,100):
            centerx, centery = select_patch(forage_points,top10[i,1],top10[i,2],radius)
            bee_exposure[int((i*100)+j)]=random_walk(centerx,centery,area)
            print(i*100+j)

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
