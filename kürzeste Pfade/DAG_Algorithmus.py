
inf = 99999

adjazenzliste_zahlen = [[1,2], [2,3], [3,4], [5], [5], [] ]
index_Name = ['s','A','B','C','D','E']
#word_index = {'s':0 'A':1 ,'B':2, 'C':3, 'D':4, 'E':5}
matrix = [ [0,1,3,inf,inf,inf], [inf,0,1,5,inf,inf], [inf,inf,0,2,7,inf], [inf,inf,inf,0,inf,6], [inf,inf,inf,inf,0,4], [inf,inf,inf,inf,inf,0] ]

distance = [0, inf, inf, inf, inf, inf]
pred = [-1, -1, -1, -1, -1, -1]


#def second(e):
#	return e[1]

def remove_all(liste,element):
	for t in liste:
		if element in t: t.remove(element)
	return liste


def topologischeSortierung(knoten,adjazenzliste):
	
	# erstelle liste von eingehenden Kanten
	indizenzliste = []
	for n in knoten:
		indizenzliste.append([])
	for idx in range(len(knoten)):
		for k in range(len(adjazenzliste)):
			if idx in adjazenzliste[k]:
				indizenzliste[idx].append(k)
	
	#print(indizenzliste)	
	#indizenzliste_anzahl = []
	#for i in range(len(knoten)):
	#	indizenzliste_anzahl.append( (i,len(indizenzliste[i])) )
	
	toposort = []
	
	for n in knoten:
		j = 0
		
		while indizenzliste[j]:
			j += 1
		
		indizenzliste[j].append(999999)
		indizenzliste = remove_all(indizenzliste,j)
		toposort.append(j)
		
	
	#return [ knoten[i] for i in toposort ]
	return toposort
	
	
tlist = topologischeSortierung(index_Name,adjazenzliste_zahlen)

#print(tlist)

for n in tlist:
	for m in adjazenzliste_zahlen[n]:
		if distance[m] > distance[n]+matrix[n][m]:
			distance[m] = distance[n]+matrix[n][m]
			pred[m] = n
					
		
	
	
	
		
		


print(pred)
print(distance)