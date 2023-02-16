inf = 999999

# <INPUT> DATENSTRUKTUR FLUSSNETZWERK
network = [ [(1,2),(2,3)], [(3,4),(4,6)], [(4,5),(5,2)], [(6,9)], [(6,1)], [(5,5)], [] ]
knotennamen = ['s','A','B','C','D','E','t']
restkapazität = [ [(1,2),(2,3)], [(3,4),(4,6)], [(4,5),(5,2)], [(6,9)], [(6,1)], [(6,5)], [] ]
restmatrix = [[0,2,3,0,0,0,0],[0,0,0,4,6,0,0],[0,0,0,0,5,2,0],[0,0,0,0,0,0,9], [0,0,0,0,0,0,1], [0,0,0,0,0,0,5], [0,0,0,0,0,0,0]] 

# ALGORITHMUS DATENSTRUKTUR INITIALISIERUNG
predinit = [-1,-1,-1,-1,-1,-1,-1]
pred = [-1,-1,-1,-1,-1,-1,-1]
t = len(pred)-1
markiert = {t}
path = []
flow = 0

# ALGORITHMUS AUSFÜHRUNG
while t in markiert:
	markiert = set([])
	#for all j in range(len(pred)):
	pred = predinit
	markiert.add(0)
	LIST = [0]
	while LIST and t not in markiert:
		i = LIST[0]
		del LIST[0]
		for j in restkapazität[i]:
			if j[0] not in markiert:
				markiert.add(j[0])
				LIST.append(j[0])
				pred[j[0]] = i
	
	#print(markiert)
	#print(pred)
	if t in markiert:
		backtrack = []
		node_j = t
		smallest = inf
		while node_j > 0:
			backtrack.append(node_j)
			node_i = pred[node_j]
			#print(smallest)
			smallest = min(smallest,restmatrix[node_i][node_j])
			node_j = node_i
		
		backtrack.append(0)
		backtrack.reverse()
		path.append((backtrack,smallest))
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
			 
			

# AUSGABE	
print('Fluss = ' + str(flow))
print(restkapazität)