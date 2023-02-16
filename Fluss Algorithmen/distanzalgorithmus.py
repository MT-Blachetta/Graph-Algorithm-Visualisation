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
	

#print(distancefunction)

#n = len(pred)


def validedge(index,distancefunction,restkapazität,pred,flow,restmatrix,path):
	for r in restkapazität[index]:
		if distancefunction[index] == distancefunction[r[0]] + 1:
			pred[r[0]] = index
			index = r[0]
			if index == t:
				backtrack = []
				node_j = t
				smallest = inf
				while node_j > 0:
					backtrack.append(node_j)
					node_i = pred[node_j]		
					smallest = min(smallest,restmatrix[node_i][node_j])
					node_j = node_i
		
				backtrack.append(0)
				backtrack.reverse()
				path.append((backtrack,smallest))
				print(path)
				flow += smallest
				
				for k in range(len(backtrack)-1):
					extract = [   m[0] for m in restkapazität[ backtrack[k] ]  ]
					cidx = extract.index(backtrack[k+1])
					Rij = restkapazität[backtrack[k]][cidx][1]
					if Rij-smallest == 0: 
						del restkapazität[backtrack[k]][cidx]
					else:
						restkapazität[backtrack[k]][cidx] = (restkapazität[backtrack[k]][cidx][0],Rij-smallest)
			
					extract = [   m[0] for m in restkapazität[ backtrack[k+1] ]  ]
					if backtrack[k] in extract:
						cidx = extract.index(backtrack[k])
						restkapazität[backtrack[k+1]][cidx] = ( restkapazität[backtrack[k+1]][cidx][0],restkapazität[backtrack[k+1]][cidx][1]+smallest )
					else:
						restkapazität[backtrack[k+1]].append( (backtrack[k],smallest) )
			
					restmatrix[backtrack[k]][backtrack[k+1]] -= smallest
					restmatrix[backtrack[k+1]][backtrack[k]] += smallest
				
				index = 0
				
			return (index,distancefunction,restkapazität,pred,flow,restmatrix)
	
	return []
		
				


while distancefunction[0] < tau:
	print('index: '+str(index))
	res = validedge(index,distancefunction,restkapazität,pred,flow,restmatrix,path)
	if res:
		index = res[0]
		#distancefunction = res[1]
		restkapazität = res[2]
		pred = res[3]
		flow = res[4]
		restmatrix = res[5]
	else:
		print('keine zulässige Kante')
		dj = tau
		for j in restkapazität[index]:
			dj = min(dj,distancefunction[j[0]])
		distancefunction[index] = dj + 1
		if index: index = pred[index]
		print(distancefunction)
		
	


