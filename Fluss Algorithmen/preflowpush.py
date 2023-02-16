inf = 99999

network = [ [(1,2),(2,3)], [(3,4),(4,6)], [(4,5),(5,2)], [(6,9)], [(6,1)], [(5,5)], [] ]

knotennamen = ['s','A','B','C','D','E','t']

restkapazität = [ [(1,2),(2,3)], [(3,4),(4,6)], [(4,5),(5,2)], [(6,9)], [(6,1)], [(6,5)], [] ]
forDistance = [ [(1,2),(2,3)], [(3,4),(4,6)], [(4,5),(5,2)], [(6,9)], [(6,1)], [(6,5)] ]
restmatrix = [[0,2,3,0,0,0,0],[0,0,0,4,6,0,0],[0,0,0,0,5,2,0],[0,0,0,0,0,0,9], [0,0,0,0,0,0,1], [0,0,0,0,0,0,5], [0,0,0,0,0,0,0]] 

predinit = [-1,-1,-1,-1,-1,-1,-1]
pred = [-1,-1,-1,-1,-1,-1,-1]
t = len(pred)-1
flow = 0
path = []

excess = [0, 0, 0, 0, 0, 0, 0]
FIFO = Queue

activeNodes = []

distancefunction = [ 0,0,0,0,0,0,0 ]
dlevel = 1
#dix = 0
lvlist= [t]
lvnext = []

tau = len(pred)
index = 0



def all_void(liste):
	for l in liste:
		if l: return True
	return False

while all_void(forDistance):
	for i in range(len(forDistance)):
		for z in forDistance[i]:
			if z[0] in lvlist:
				distancefunction[i] = dlevel
				lvnext.append(i)
	#print(lvnext)
	#print(distancefunction)
	dlevel += 1
	
	for id in lvnext: forDistance[id] = []
	lvlist = lvnext
	lvnext = []
	

print(distancefunction)


class Queue:
