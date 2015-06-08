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
				fo=open(thetaPath+".txt","w+")
				fo.write("1000")
				fo.close()