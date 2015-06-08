import networkx as nx
from heapq import heappush, heappop
import priority_dict
import graphml_parser
import geopy
import shortest_path
import os
import matplotlib
from geopy.distance import vincenty
from collections import deque
from os import listdir
import graphInput
import queuing
import NetworkGraph
import random
import plot
import scipy.io
import numpy as np


if __name__=="__main__":
	#initialization
	allFiles=os.listdir("../dataset/archive/")
	count=0
	nodeCount=dict()
	ctrCount=dict()
	

	d_lower=1500
	d_upper=3000
	mu=30000


	for modules in allFiles:
		if ("graphml" in modules):
			cover=[]
			uncover=[]
			d={}
			cost={}
			filePath="../dataset/archive/"+modules
			demandPath="../dataset/demand/"+modules[:-8]
			freqPath="../dataset/freq/"+modules[:-8]
			headPath="../dataset/header/"+modules[:-8]


			#graph parsing
			gi=graphInput.graphInput(filePath)
			gi.graphParser()
			valid=gi.isValidGraph()
			connected=gi.isConnected()


			if valid==1 and connected==1:
				#print "Graph {} is valid and connected".format(filePath)
				ng=NetworkGraph.NetworkGraph(gi)
				ng.calculateGraphDiameter()
				switch=ng.getSwitch()
				edge=ng.getGraph()
				diameter=ng.getDiameter()

				theta=(2*diameter/300000000+5)/1000

				fo=open(demandPath+".txt","r+")

				for s in switch:
					line=fo.readline()
					d[str(s)]=float(line[:-2])
					uncover.append(s)

				fo.close()

				s=ng.getSwitch()

				c=ng.getController()

				sp=shortest_path.shortest_path(s,edge)
				node_dist=dict()
				for n in s:
					node_dist[n]=sp.shortestPath(n)


				initialSet=dict()
				ca=queuing.queuing(mu)

				for n in s:
					initialSet[n]=[]
					for k,v in node_dist[n].iteritems():
						if k!=n:
							t=2*v/300000000+ca.queuingTime(k,n,d)
								
							if t<=theta:
								ca.updateAssignment(k,n,d)
								initialSet[n].append(k)
							
					initialSet[n].append(n)


				nodeFreq=dict()
				nodefreqpair=dict()

				for ele in switch:
					nodeFreq[ele]=[]

				for ele in switch:
					nodefreqpair[ele]=0

				maxFreq=0
				for k,v in initialSet.iteritems():
					countNode=0
					for ele in switch:
						if ele in v:
							nodeFreq[ele].append(-1)
							nodefreqpair[ele]=nodefreqpair[ele]+1
						else:
							nodeFreq[ele].append(0)

				fo=open(headPath+".txt","w+")
				for k,v in nodefreqpair.iteritems():
					outLine=str(k)+" "+str(v)+"\n"
					fo.write(outLine)
				fo.close()

				fo=open(freqPath+".txt","w+")
				
				for k,v in nodeFreq.iteritems():
					outLine=""
					for ele in v:
						outLine=outLine+str(ele)+" "
					outLine=outLine+"\n"
					fo.write(outLine)

				fo.close()
			
				#print initialSet
				

				'''

				numCtr=0

				while (len(cover)<len(switch)):
					#find an uncovered node
					for n in switch:
						if n not in cover:
							nodeFind=n


					#increase cost
					for v in initialSet[nodeFind]:
						if v not in cover:
							cover.append(v)

					numCtr=numCtr+1


					for k1,v1 in initialSet.iteritems():
						if k1!=nodeFind and k1 not in cover:
							if nodeFind in v1:
								numCtr=numCtr+1
								for ele in v1:
									if ele not in cover:
										cover.append(ele)


				ctrCount[modules[:-8]]=numCtr
				nodeCount[modules[:-8]]=len(switch)



	plt=plot.plot(ctrCount,nodeCount)
	plt.diagramPlot()
	'''		
					














