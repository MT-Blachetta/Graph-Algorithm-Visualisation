import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
#import random
import copy

inf = 999999

class shortestpathstate():
    def __init__(self,distances,pred,names):
        self.distances = distances
        self.pred = pred
        self.prededges = []
        self.nodelabels = {}
        self.names = names
    
        for i in range(len(self.pred)):
            if self.pred[i] >= 0:
                self.prededges.append((self.names[i],self.names[self.pred[i]]))
        
        for d in range(len(self.distances)):
            lb = 'infinite' if self.distances[d] == inf else str(self.distances[d])
            self.nodelabels[self.names[d]] = self.names[d] + '\n d = ' + lb

    def update_labels(self):
        self.prededges = []
        self.nodelabels = {}
        for i in range(len(self.pred)):
            if self.pred[i] >= 0:
                self.prededges.append((self.names[i],self.names[self.pred[i]]))
        
        for d in range(len(self.distances)):
            lb = 'infinite' if self.distances[d] == inf else str(self.distances[d]) 
            self.nodelabels[self.names[d]] = self.names[d] + '\n d = ' + lb

    def __str__(self):
        outstring = 'shortestpathstate instance: \n'
        outstring += 'distances = ' + str(self.distances) + '\n'
        outstring += 'pred = ' + str(self.pred) + '\n'
        outstring += 'prededges = ' + str(self.prededges) + '\n'
        outstring += 'nodelabels = ' + str(self.nodelabels) + '\n\n'
        
        return outstring

class drawInfo():
    def __init__(self,edges,rededges,nodelabels,edgelabels):
        self.graph = nx.DiGraph()
        self.graph.add_edges_from(edges)
        self.rededges = rededges
        self.blackedges = [edge for edge in self.graph.edges() if edge not in rededges]
        self.nodelabels = nodelabels
        self.edgelabels = edgelabels
        self.pos = nx.planar_layout(self.graph)
    
    def __str__(self):
        outstring = 'drawInfo instance: \n'
        outstring += 'graph = ' + str(self.graph) + '\n'
        outstring += 'rededges = ' + str(self.rededges) + '\n'
        outstring += 'blackedges = ' + str(self.blackedges) + '\n'
        outstring += 'edgelabels = ' + str(self.edgelabels) + '\n\n'
        
        return outstring

class phase():
    def __init__(self,oldPhase,newPhase,z_phase,LIST):
        self.oldPhase =  oldPhase
        self.newPhase = newPhase
        self.z_phase = z_phase
        self.LIST = LIST
    
    def __str__(self):
        outstring = 'phase instance: \n'
        outstring += 'oldPhase = ' + str(self.oldPhase) + '\n'
        outstring += 'newPhase = ' + str(self.newPhase) + '\n'
        outstring += 'z_phase = ' + str(self.z_phase) + '\n'
        outstring += 'LIST = ' + str(self.LIST) + '\n\n'
        
        return outstring

def edgeformA(adjlist,costmatrix,names):
    edges = []
    labeldic = {}
    for i in range(len(adjlist)):
        for j in adjlist[i]:
            edges.append((names[i],names[j]))
            labeldic[(names[i],names[j])] = costmatrix[i][j]
    return (edges,labeldic)
    
def writelist(inputliste,inputnamen):
    liste = copy.deepcopy(inputliste)
    namen = copy.deepcopy(inputnamen)
    listtext = '[ '
    if liste:
        listtext += namen[liste[0]]
        del liste[0]
        for i in liste:
            listtext += ', '
            listtext += namen[i]
        listtext += ' ]'
        return listtext
    else: return '(leer)'

def stripAll(stringlist):
    return [ txt.strip() for txt in stringlist ]

def zero_init(nodenumber):
    initial = [ [inf for j in range(nodenumber)] for i in range(nodenumber) ]
    for i in range(nodenumber): initial[i][i] = 0
    return initial

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)



    def plot(self,graphinfo):
        print('enter plot function')
        print(graphinfo)
        self.fig.clf()
        G = graphinfo.graph
        pos = graphinfo.pos
        nodelabels = graphinfo.nodelabels
        edgelabels = graphinfo.edgelabels
        black_edges = graphinfo.blackedges
        red_edges = graphinfo.rededges

        ax = self.fig.add_subplot(111)
        nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), alpha = 0.5, node_size = 500,ax = ax) # , alpha = 0.5,node_color = 'red'
        nx.draw_networkx_nodes(G,pos, nodelist = ['s'],node_size = 500,node_color = 'orange',ax=ax)
        nx.draw_networkx_labels(G, pos,labels = nodelabels,font_color = 'red',font_weight = 'bold',ax = ax )
        nx.draw_networkx_edges(G, pos, edgelist=black_edges,width = 1.1,arrowsize= 20, arrows=True,ax = ax)
        if red_edges: nx.draw_networkx_edges(G, pos, edgelist=red_edges,width = 1.1,arrowsize= 20,style = 'dotted', edge_color='r', arrows=True,ax = ax)
        nx.draw_networkx_edge_labels(G,pos,edge_labels = edgelabels,font_color='blue',font_size=13,ax = ax)

        
        ax.set_title('kürzeste Pfade Graph')
        self.draw()


class App(QMainWindow):

    def __init__(self,algorithmState,phase_state,adjazenzliste,costmatrix):
        super().__init__()
        self.title = 'generischer kürzeste Pfade Algorithmus'

        self.left = 20
        self.top = 20

        self.width = 1024
        self.height = 824
		
		
        self.buttonback = QPushButton('< back', self)
        self.buttonforward = QPushButton('forward >',self)
        self.loadbutton = QPushButton('Load',self)
        self.inputfield = QLineEdit('S:B=12,C=5|B:D=7|C:E=6|D:C=11|E:S=-1,B=9,D=8',self)
		
        self.mainlabel = QLabel("LIST  =  [ s ]",self)
        self.iterationlabel = QLabel('Iteration:\n\n\n0',self)
        self.phaselabel = QLabel('Phase:\n\n\n0',self)
        
        self.algorithmState = algorithmState
        self.phase_state = phase_state
        self.adjazenzliste = adjazenzliste
        self.costmatrix = costmatrix
        self.phaseTrack = [copy.deepcopy(self.phase_state)]
        self.stateTrack = [copy.deepcopy(self.algorithmState)]
        
        self.graph = PlotCanvas(self, width=8, height=6)
		
        self.listindex = 0
        self.finished = False
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

       
        self.graph.move(0,0)


        self.mainlabel.move(1,600)
        self.mainlabel.resize(1022,50)
        self.iterationlabel.move(800,5)
        self.iterationlabel.resize(200,240)
        self.phaselabel.move(800,250)
        self.phaselabel.resize(200,240)
        self.mainlabel.setFont(QtGui.QFont('Arial', 15, QFont.Bold)) 
        self.mainlabel.setAlignment(Qt.AlignCenter)
        self.buttonback.setFont(QtGui.QFont('SansSerif', 16, QFont.Bold)) 
        self.buttonforward.setFont(QtGui.QFont('SansSerif', 16, QFont.Bold)) 
        self.loadbutton.setFont(QtGui.QFont('SansSerif', 16, QFont.Bold)) 
        self.inputfield.setStyleSheet('border: 2px solid;')
        self.buttonback.setStyleSheet('color: Blue; border: 3px solid;')
        self.buttonforward.setStyleSheet('color: Blue; border: 3px solid;')
        self.loadbutton.setStyleSheet('color: Blue; border: 3px solid;')
        self.iterationlabel.setAlignment(Qt.AlignCenter)
        self.iterationlabel.setFont(QtGui.QFont('Arial', 15, QFont.Bold))
        self.phaselabel.setAlignment(Qt.AlignCenter)
        self.phaselabel.setFont(QtGui.QFont('Arial', 15, QFont.Bold))
        self.inputfield.setFont(QtGui.QFont('Arial', 14))
        self.inputfield.setMaxLength(100000)
        self.buttonback.setToolTip('next iteration of the algorithm')
        self.buttonforward.setToolTip('back to last state')
        self.loadbutton.setToolTip('Gebe im Eingabefeld oben nach der vorgegebenen Syntax den Graphen ein und Klicke dann auf den Button')
        self.inputfield.setToolTip('Halte dich bitte an die Beispielsyntax wie im Eingabefeld vorgegeben. Knoten:Adjazenzknoten=Kantenkosten,...|')
        self.buttonback.move(21,745)
        self.buttonback.resize(300,50)
        self.buttonforward.move(362,745)
        self.buttonforward.resize(300,50)
        self.loadbutton.move(693,745)
        self.loadbutton.resize(300,50)
        self.inputfield.move(21,670)
        self.inputfield.resize(972,45)
        transformed = edgeformA(self.adjazenzliste,self.costmatrix,self.algorithmState.names)
        Edges = transformed[0]
        edgelabels = transformed[1]
        nodelabels = self.algorithmState.nodelabels
        predLinks = self.algorithmState.prededges
        self.drawinfos = drawInfo(Edges,predLinks,nodelabels,edgelabels)
        self.graph.plot(self.drawinfos)
        self.buttonforward.clicked.connect(self.nextIteration)
        self.buttonback.clicked.connect(self.lastIteration)
        self.loadbutton.clicked.connect(self.load_graph_from_text)
        self.buttonback.setEnabled(False)

        self.show()

    def lastIteration(self):

        if self.listindex:
            self.listindex -= 1
            self.algorithmState = self.stateTrack[self.listindex]
            self.phase_state = self.phaseTrack[self.listindex]
            transformed = edgeformA(self.adjazenzliste,self.costmatrix,self.algorithmState.names)
            Edges = transformed[0]
            edgelabels = transformed[1]
            nodelabels = self.algorithmState.nodelabels
            predLinks = self.algorithmState.prededges
            self.drawinfos = drawInfo(Edges,predLinks,nodelabels,edgelabels)
            self.graph.plot(self.drawinfos)
            
            self.phaselabel.setText('Phase:\n\n\n'+str(self.phase_state.z_phase))
            self.iterationlabel.setText('Iteration:\n\n\n'+str(self.listindex))
            self.mainlabel.setText('LIST  =  '+writelist(self.phase_state.LIST,self.algorithmState.names))
            self.buttonforward.setText('forward >')
            self.buttonforward.setStyleSheet('color: Blue')
            self.buttonforward.setEnabled(True)
            
            if not self.listindex:
                self.buttonback.setEnabled(False)


    def Agen_Iteration(self):

        if self.phase_state.LIST:
        
            i = self.phase_state.LIST[0]
            del self.phase_state.LIST[0]
            
            self.phase_state.oldPhase -= 1
        
            for j in self.adjazenzliste[i]:
                i_dist = self.algorithmState.distances[i] + self.costmatrix[i][j] # + 0.001
                if self.algorithmState.distances[j] > i_dist:
                    self.algorithmState.distances[j] = i_dist
                    self.algorithmState.pred[j] = i
                    if j not in self.phase_state.LIST: 
                        self.phase_state.LIST.append(j)
                        self.phase_state.newPhase += 1
                    
            if not self.phase_state.oldPhase:
                self.phase_state.z_phase +=1
                print('Phase: '+str(self.phase_state.z_phase))
                print(self.phase_state.LIST)
                self.phase_state.oldPhase = self.phase_state.newPhase
                self.phase_state.newPhase = 0
            
        
            self.algorithmState.update_labels()

            self.phaseTrack.append(copy.deepcopy(self.phase_state))
            self.stateTrack.append(copy.deepcopy(self.algorithmState))
            self.listindex += 1
            self.phaselabel.setText('Phase:\n\n\n'+str(self.phase_state.z_phase))
            self.iterationlabel.setText('Iteration:\n\n\n'+str(self.listindex))
            self.mainlabel.setText('LIST  =  '+writelist(self.phase_state.LIST,self.algorithmState.names))

            if self.phase_state.LIST: return False
            else: return True
    
        else: 
            return True
    
    def nextIteration(self):

        if self.listindex + 1 < len(self.stateTrack):
            terminated = (self.listindex + 1 == len(self.stateTrack) - 1)
            self.listindex += 1
            self.algorithmState = copy.deepcopy(self.stateTrack[self.listindex])
            self.phase_state = copy.deepcopy(self.phaseTrack[self.listindex])

            self.phaselabel.setText('Phase:\n\n\n'+str(self.phase_state.z_phase))
            self.iterationlabel.setText('Iteration:\n\n\n'+str(self.listindex))
            self.mainlabel.setText('LIST  =  '+writelist(self.phase_state.LIST,self.algorithmState.names))

            transformed = edgeformA(self.adjazenzliste,self.costmatrix,self.algorithmState.names)
            Edges = transformed[0]
            edgelabels = transformed[1]
            nodelabels = self.algorithmState.nodelabels
            predLinks = self.algorithmState.prededges
            self.drawinfos = drawInfo(Edges,predLinks,nodelabels,edgelabels)
            self.graph.plot(self.drawinfos)
            if self.phase_state.z_phase > len(self.algorithmState.names):
                self.finished = True
                self.mainlabel.setText('Graph hat negative Kreise !')
                self.mainlabel.setStyleSheet('color: Red')
                self.buttonforward.setText('Error')
                self.buttonforward.setStyleSheet('color: Red')
                self.buttonforward.setEnabled(False)
                self.buttonback.setEnabled(True)
                return

            if terminated and self.finished:
                self.buttonforward.setText('FINISHED')
                self.buttonforward.setEnabled(False)
        else: 
            terminated = self.Agen_Iteration()
            transformed = edgeformA(self.adjazenzliste,self.costmatrix,self.algorithmState.names)
            Edges = transformed[0]
            edgelabels = transformed[1]
            nodelabels = self.algorithmState.nodelabels
            predLinks = self.algorithmState.prededges
            self.drawinfos = drawInfo(Edges,predLinks,nodelabels,edgelabels)
            
            self.graph.plot(self.drawinfos)
            if self.phase_state.z_phase > len(self.algorithmState.names):
                self.finished = True
                self.mainlabel.setText('Graph hat negative Kreise !')
                self.mainlabel.setStyleSheet('color: Red')
                self.buttonforward.setText('Error')
                self.buttonforward.setStyleSheet('color: Red')
                self.buttonforward.setEnabled(False)
                self.buttonback.setEnabled(True)
                return

            if terminated:
                self.finished = True
                self.buttonforward.setText('FINISHED')
                self.buttonforward.setStyleSheet('color: Green')
                self.buttonforward.setEnabled(False)
            
        self.buttonback.setEnabled(True)


    def load_graph_from_text(self):
        inputtext = self.inputfield.text()
        nodes = stripAll(inputtext.split('|'))
        word_index = {}

        if len(nodes) < 2:
            self.mainlabel.setText('Falsche Syntax im Eingabefeld - Trenne Adjazenzlisten der Knoten durch "|" Zeichen\n mindestens 2 Knoten müssen vorkommen')
            return False
        if not(nodes[0].startswith('s') or nodes[0].startswith('S')):
            self.mainlabel.setText('Am Anfang der Eingabe muss der Startknoten mit s oder S stehen')
            return False
        nameList = []
        adjazenz = []
        costmatrix = []
        counter = 0
        for n in nodes:
            nlist = stripAll(n.split(':'))
            if len(nlist) != 2: 
                self.mainlabel.setText('Für die Adjazenzliste jedes Knotens muss sich genau ein : Symbol befinden\n der Knoten von Nachbarn trennt ')
                return False
            nameList.append(nlist[0])
            word_index[nlist[0]] = counter
            counter += 1
            if nlist[1]:
                adl = []
                cost = []
                neighbors = stripAll(nlist[1].split(','))
                for j in neighbors:
                    entry = stripAll(j.split('='))
                    try:
                        cost.append( (entry[0],float(entry[1])) )
                        adl.append(entry[0])
                    except ValueError:
                        self.mainlabel.setText('Ein Distanzwert hat die falsche Form, Gleitkommazahlen werden mit . geschrieben')
                        return False
                adjazenz.append(adl)
                costmatrix.append(cost)
            else:
                adjazenz.append([])
                costmatrix.append([])

        nameList[0] = 's'
        self.costmatrix = zero_init(len(nameList))
        self.adjazenzliste = [ [word_index[j] for j in node ] for node in adjazenz ] #range(len(adjazenz))
        for i in range(len(costmatrix)):
            for j in costmatrix[i]:
                self.costmatrix[i][ word_index[j[0]] ] = j[1]
        dist = [ inf for i in nameList ]
        dist[0] = 0
        pred = [ -1 for i in nameList ]
        self.algorithmState = shortestpathstate(dist,pred,nameList)
        self.phase_state = phase(1,0,0,[0])
        self.phaseTrack = [copy.deepcopy(self.phase_state)]
        self.stateTrack = [copy.deepcopy(self.algorithmState)]
        self.listindex = 0
        self.phaselabel.setText('Phase:\n\n\n'+str(self.phase_state.z_phase))
        self.iterationlabel.setText('Iteration:\n\n\n'+str(self.listindex))
        self.mainlabel.setText('LIST  =  '+writelist(self.phase_state.LIST,self.algorithmState.names))
        transformed = edgeformA(self.adjazenzliste,self.costmatrix,self.algorithmState.names)
        Edges = transformed[0]
        edgelabels = transformed[1]
        nodelabels = self.algorithmState.nodelabels
        predLinks = self.algorithmState.prededges
        self.drawinfos = drawInfo(Edges,predLinks,nodelabels,edgelabels)
        self.finished = False
        self.buttonback.setEnabled(False)
        self.buttonforward.setText('forward >')
        self.buttonforward.setStyleSheet('color: Blue')
        self.buttonforward.setEnabled(True)
        self.graph.plot(self.drawinfos)



if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    adjazenzliste_zahlen = [[1,2], [3], [4], [2], [0,1,3]]
    index_Name = ['s','B','C','D','E']
    matrix = [ [0,12,5,inf,inf],[inf,0,inf,7,inf],[inf,inf,0,inf,6],[inf,inf,11,0,inf],[-1,9,inf,8,0] ]
    distance = [0, inf, inf, inf, inf]
    pred = [-1, -1, -1, -1, -1]
    oldPhase = 1
    newPhase = 0
    z = 0
    liste = [0]
    status = phase(oldPhase,newPhase,z,liste)
    pathstate = shortestpathstate(distance,pred,index_Name)
    tool = App(pathstate,status,adjazenzliste_zahlen,matrix)
    sys.exit(app.exec_())