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
	d_lower=1500
	d_upper=3000

	allFiles=os.listdir("../dataset/archive/")
	outFiles="../dataset/demand/"

	for modules in allFiles:
		if ("graphml" in modules):
			filePath="../dataset/archive/"+modules

			#graph parsing
			gi=graphInput.graphInput(filePath)
			gi.graphParser()
			valid=gi.isValidGraph()
			connected=gi.isConnected()


			if valid==1 and connected==1:
				fo=open(outFiles+modules[:-8]+".txt","w+")
				d={}
				ng=NetworkGraph.NetworkGraph(gi)
				switch=ng.getSwitch()

				for s in switch:
					d[str(s)]=d_lower+random.random()*(d_upper-d_lower)
					outLine=str(d[str(s)])+"\n"
					fo.write(outLine)
				fo.close()



	


				







