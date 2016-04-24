import numpy as np

num_fields=25
percent_weedy=0.5

num_corn=np.uint32(num_fields*0.4)

num_weedy_corn=np.uint32(num_corn*percent_weedy)

if num_weedy_corn==0:
	if percent_weedy>0:
		num_weedy_corn=1
	
num_weedy_soy = np.uint32((num_fields-num_corn)*.45)


order = np.arange(num_fields)
np.random.shuffle(order)
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

print(marker)
print(num_corn)
print(num_weedy_corn)
print(num_weedy_soy)