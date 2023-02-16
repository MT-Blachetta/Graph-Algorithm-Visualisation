import networkx as nx
import matplotlib.pyplot as plt

def edgeformA(adjlist,costmatrix,names):
	edges = []
	labeldic = {}
	for i in range(len(adjlist)):
		for j in adjlist[i]:
			edges.append((names[i],names[j]))
			labeldic[(names[i],names[j])] = costmatrix[i][j]
	return (edges,labeldic)

def edgeformB(adjlist,names):
	edges = []
	labeldic = {}
	for i in range(len(adjlist)):
		for j in adjlist[i]:
			edges.append( (names[i],names[j[0]]) )
			labeldic[(names[i],names[j[0]])] = j[1]
	
	return (edges,labeldic)
	
def pathgraph(path,names):
	pathedges = []
	for i in range(len(path)-1):
		pathedges.append( (names[path[i]],names[path[i+1]]) )
	return pathedges
	
	


inf = 99999

adjazenzliste_zahlen = [[1,2], [3], [4], [2], [0,1,3]]
index_Name = ['A','B','C','D','E']
#word_index = {'A':0 ,'B':1, 'C':2, 'D':3, 'E':4}
matrix = [ [0,12,5,inf,inf],[inf,0,inf,7,inf],[inf,inf,0,inf,6],[inf,inf,11,0,inf],[-1,9,inf,8,0] ]

distance = [0, inf, inf, inf, inf]
pred = [-1, -1, -1, -1, -1]

# del l[0] Dequeue
# l.append(x) Enqueue
liste = [0]

oldPhase = 1
newPhase = 0
z = 0


transformed = edgeformA(adjazenzliste_zahlen,matrix,index_Name)

Edges = transformed[0]
labeldictionary = transformed[1]

print(Edges)
print(labeldictionary)

print('Phase: 0')
print(liste)

while liste:
	
	i = liste[0]
	del liste[0]
		
	oldPhase -= 1
	
	for j in adjazenzliste_zahlen[i]:
		i_dist = distance[i] + matrix[i][j] + 0.001
		if distance[j] > i_dist:
			distance[j] = i_dist
			pred[j] = i
			if j not in liste: 
				liste.append(j)
				newPhase += 1
				
	if not oldPhase:
		z +=1
		print('Phase: '+str(z))
		print(liste)
		oldPhase = newPhase
		newPhase = 0
		
	if z > len(index_Name):
		print('FEHLER: Graph hat negative Kreise')
		break
				
	
				
			

distance = [ int(e) for e in distance ] 

backtrack = []
t = 3

while t >= 0:
	#backtrack.append(index_Name[t])
	backtrack.append(t)
	t = pred[t]

backtrack.reverse()
	
pfad = pathgraph(backtrack,index_Name)

print('ALGORITHMUS ABGESCHLOSSEN')

G = nx.DiGraph()
G.add_edges_from(Edges)

#val_map = {'A': 1.0, 'D': 0.5714285714285714, 'H': 0.0}
#values = [val_map.get(node, 0.25) for node in G.nodes()]

red_edges = pfad

#print(red_edges)

black_edges = [edge for edge in G.edges() if edge not in red_edges]

pos = nx.planar_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = 500) # , node_color = values
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)

nx.draw_networkx_edge_labels(G,pos,edge_labels = labeldictionary,font_color='red')
plt.axis('off')


plt.show()