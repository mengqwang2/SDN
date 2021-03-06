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
import operator
import NodeCover
import GraphStrip
import GreedySelect

if __name__=="__main__":
	allFiles=os.listdir("../dataset/archive/")
	count=0
	nodeCount=dict()
	ctrCount=dict()

	mu=30000

	for modules in allFiles:
		d={}
		if ("graphml" in modules):
			filePath="../dataset/archive/"+modules
			demandPath="../dataset/demand/"+modules[:-8]
			thetaPath="../dataset/theta/"+modules[:-8]
			
			#graph parsing
			gi=graphInput.graphInput(filePath)
			gi.graphParser()
			valid=gi.isValidGraph()
			connected=gi.isConnected()

			if valid==1 and connected==1:
				print "Graph {} is valid and connected".format(filePath)
				ng=NetworkGraph.NetworkGraph(gi)
				ng.calculateGraphDiameter()
				
				switch=ng.getSwitch()
				dens=ng.getDiameter()
				edge=ng.getGraph()
				diameter=ng.getDiameter()

				theta=float((2*diameter/300000000+5))/1000
				print theta

				fo=open(demandPath+".txt","r+")
				for s in switch:
					line=fo.readline()
					d[str(s)]=float(line[:-2])

				fo.close()

				c=ng.getController()

				s=ng.getSwitch()
				greedyS=GreedySelect.GreedySelect(s,ng)
				ctr=greedyS.greedySelection(mu,theta,d)
				ns=dict()
				ns=greedyS.getNodeAsg()
				print ns
				
				maxN=0
				minN=len(switch)
				sumN=0
				avgN=0
				for k,v in ns.iteritems():
					if len(v)>maxN:
						maxN=len(v)
					if len(v)<minN:
						minN=len(v)
					sumN=sumN+len(v)

				avgN=sumN/ctr
				

				print ctr
				print switch
				#print maxN,minN,avgN

				#fo=open("A1_lb.csv","a")
				#line=str(modules[:-8])+","+str(maxN)+","+str(minN)+","+str(avgN)+","+str(len(switch))+"\n"
				#fo.write(line)
				#fo.close()





				


