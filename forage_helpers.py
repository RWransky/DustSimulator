import numpy as np

#dust drift function
#NOTE INPUT IS IN METERS
def dust_drift(meter):
    #coefficients a,b,c,d are from experimental data
    a=6.561
    b=-3.106
    c=1.567
    d=-0.005436

    concentration = a*np.exp(b*meter)+c*np.exp(d*meter)
    return concentration

#function for the distance to the hive
def dist_hive(x,y):
    distance_to_hive = np.sqrt(pow((x-2000),2)+pow((y-2000),2))
    return distance_to_hive

#function to pick the 10 foraging locations
#function takes a random sample of potential foraging locations
#returns 10 most likely foraging sites based on distance to hive
def foraging_sites(forage_points):
    visit_prob=[]; number_list=[]
    numb_points=len(forage_points)
    pick20 = np.random.randint(numb_points,size=(100,1))
    def getKey(item):
        return item[0]
    for i in range(0,100):
        prob=dist_hive(forage_points[pick20[i]][0],forage_points[pick20[i]][1])
        #prob=0.1227*np.exp(-0.002151*dist_hive(forage_points[pick20[i]][0],forage_points[pick20[i]][1]))
        visit_prob.append([prob,forage_points[pick20[i]][0],forage_points[pick20[i]][1]])

    sorted_20=sorted(visit_prob,key=getKey)
    
    top10=sorted_20[0:10]
    top10_points=np.zeros((10,2))
    top10_prob=np.zeros((10,1))
    for i in range(0,10):
        top10_points[i,0]=top10[i][1]
        top10_points[i,1]=top10[i][2]
        top10_prob[i]=top10[i][0]
    
    return top10_prob, top10_points
    
def foraging_sites2(forage_points):
    numb_points=len(forage_points)
    points=np.zeros((numb_points,3))
    
    for i in range(0,numb_points):
        distance=dist_hive(forage_points[i][0],forage_points[i][1])
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
        
def hit_or_miss(top10,radius,area):
    
    bee_exposure=np.zeros((10000,1))
    for i in range(0,10):
        
        centerx=top10[i,1]; centery=top10[i,2]
        for j in range(0,1000):
            np.random.seed()
            minus=np.random.randint(2,size=(1,1))
            concent=0
            while concent==0:
                if minus == 1:
                    numberx=np.random.randint(radius,size=(1,1))
                    numbery=np.random.randint(radius,size=(1,1))
                else:
                    numberx = -1*np.random.randint(radius,size=(1,1))
                    numbery = -1*np.random.randint(radius,size=(1,1))
                
                placex=centerx+numberx; placey=centery+numbery
                if placex>=4000 or placex<0:
                    placex=centerx
                if placey>=4000 or placey<0:
                    placey=centery
                
                concent=area[int(placex),int(placey)]
                
                #print concent
                
            bee_exposure[int((i*1000)+j)]=area[int(placex),int(placey)]
           
    return bee_exposure

#prob,pts = foraging_sites(forage_landscape)
def iterate_foraging(forage_land,area):
    concentrations=[]
    ###### NOTE: If you want to increase the iterations change the range(0,1)
    for i in range(0,1):
        pts=foraging_sites2(forage_land)
        plt.plot(pts[:,1],pts[:,2],'ko')
        bee_levels = hit_or_miss(pts,500,area)
        for j in range(0,10000):
            concentrations.append(bee_levels[j])
            
    return concentrations

def validate_foraging(forage_land):
    point_scatter=[]
    for i in range(0,10):
        pts = foraging_sites2(forage_land)
        for j in range(0,10):
            point_scatter.append(pts[j][0])
            
    return point_scatter