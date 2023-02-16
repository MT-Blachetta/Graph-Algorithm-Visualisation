# Dijkstras Algorithmus bis 99 Knoten

inf = 9999

adjazenzliste_zahlen = [[1,2], [3], [4], [2], [0,1,3]]
index_Name = ['A','B','C','D','E']
word_index = {'A':0 ,'B':1, 'C':2, 'D':3, 'E':4}
matrix = [ [0,12,5,inf,inf],[inf,0,inf,7,inf],[inf,inf,0,inf,6],[inf,inf,11,0,inf],[3,9,inf,8,0] ]

distance = {'A':0, 'B':inf, 'C':inf, 'D':inf, 'E':inf}
pred = {'A':'', 'B':'', 'C':'', 'D':'', 'E':''}
T_set = [['B',inf],['C',inf],['D',inf],['E',inf]]

for e in T_set:
	init_distance = matrix[0][word_index[e[0]]]
	e[1] = init_distance
	distance[e[0]] = init_distance
	if init_distance < inf:
		pred[e[0]] = 'A' 


def secondelement(l):
	return l[1]


print(distance)


while T_set:
	# min
	T_set.sort(key=secondelement,reverse=True)
	smalest_Telement = T_set.pop()
	w0 = word_index[ smalest_Telement[0] ]
	w0_d = smalest_Telement[1]
	# decrease key
	for e in T_set:
		c = matrix[w0][word_index[e[0]]]
		if distance[e[0]] > (w0_d + c):
			new_distance = w0_d + c + 0.01
			e[1] = new_distance
			distance[e[0]] = new_distance
			pred[e[0]] = index_Name[w0]
			
for elm in distance:
	distance[elm] = int(distance[elm])
	
print(distance)
print(pred)	
		
t = 'D'
backtrack = []
while t:
	backtrack.append(t)
	t = pred[t]
	

backtrack.reverse()

print(backtrack)



 