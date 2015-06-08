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
	allFiles=os.listdir("../dataset/archive/")
	count=0
	nodeCount=dict()
	ctrCount=dict()

	mu=30000

	d={}

	for modules in allFiles:
		if ("graphml" in modules):
			filePath="../dataset/archive/"+modules
			demandPath="../dataset/demand/"+modules[:-8]
			
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

				theta=(2*diameter/300000000+5)/10000

				fo=open(demandPath+".txt","r+")
				for s in switch:
					line=fo.readline()
					d[str(s)]=float(line[:-2])

				fo.close()

				s=ng.getSwitch()
				n_ctr=len(s)

				c=ng.getController()

				mapping=dict()
				ctr=[]

				sp=shortest_path.shortest_path(s,edge)
				node_dist=dict()
				for n in s:
					node_dist[n]=sp.shortestPath(n)

				ctr_cnt=0
				while s:
					node_asg={}
					nodehp=priority_dict.priority_dict()
					for ele in c:
						#print node_dist[ele]
						node_asg[ele]=[]
						neighbour=[]
						cnt=0
						ca=queuing.queuing(mu)

						for n,dist in node_dist[ele].iteritems():
							if n!=ele:
								#ca.updateAssignment(n,ele,d)
								t=2*dist/300000000+ca.queuingTime(n,ele,d)
								
								if t<=theta:
									ca.updateAssignment(n,ele,d)
									neighbour.append(n)
									cnt=cnt+1
									

						nodehp[ele]=cnt
						node_asg[ele]=neighbour

					largest=""
					c_node=""
					while nodehp:
						c_node=nodehp.smallest()
						nodehp.pop_smallest()

					ctr.append(c_node)
					mapping[c_node]=node_asg[c_node]
					ctr_cnt=ctr_cnt+1
					s.remove(c_node)
					c.remove(c_node)

					for node in node_asg[c_node]:
						if node in s:
							s.remove(node)
						if node in c:
							c.remove(node)

				ctrCount[modules[:-8]]=ctr_cnt
				nodeCount[modules[:-8]]=n_ctr
			

				print "Graph {} with {} nodes is allocated with {} controllers ".format(modules[:-8],nodeCount[modules[:-8]],ctrCount[modules[:-8]])

	#x = ctrCount.keys()
	#y = ctrCount.values()
	#scipy.io.savemat('test.mat', dict(x=x, y=y))
	#scipy.io.savemat('output.mat', mdict={'keys': ctrCount.keys(), 'values': ctrCount.values()})

	plt=plot.plot(ctrCount,nodeCount)
	plt.diagramPlot()


	

	




