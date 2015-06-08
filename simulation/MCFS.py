from heapq import heappush, heappop
import priority_dict
import graphml_parser
import geopy
import shortest_path
import os
import matplotlib
from collections import deque
from os import listdir
import matplotlib.pyplot as plt
import graphInput
import MCFGraph
import NetworkGraph
import kmeans
import math
import PTAS
import random


if __name__=="__main__":

	allFiles=os.listdir("../dataset/archive/")

	for modules in allFiles:
		if ("graphml" in modules):

			filePath="../dataset/archive/"+modules
			d_upper=3000
			d_lower=1500
			u=30000
			B=20
			r=[]
			light_speed=300000000
			d={}
			

			#graph parsing
			gi=graphInput.graphInput(filePath)

			gi.graphParser()
			valid=gi.isValidGraph()
			connected=gi.isConnected()
			

			if valid==1 and connected==1:
				print "Graph is valid and connected."
				ng=NetworkGraph.NetworkGraph(gi)
				ng.calculateGraphDiameter()
				switch=ng.getSwitch()
				print "Total number of switches is: {}".format(len(switch))

				requestSum=0
				for s in switch:
					d[str(s)]=d_lower+random.random()*(d_upper-d_lower)
					requestSum=requestSum+d[str(s)]

				numController=requestSum/u+1

				km=kmeans.kmeans(ng)
				ds=ng.getShortestPath()

				diameter=ng.getDiameter()
				print "Diameter is {}".format(diameter)
				

				pt=PTAS.PTAS(ng,ds,km,d,numController)
				pt.run()



				'''
				controllers=km.initialCluster(mid)
				print controllers
				pt=PTAS.PTAS(ng,0.050,ds,controllers)
				pt.run()
				lamda=pt.getLamda()
				print "Lamda is {}".format(lamda)
				

				while(lamda!=1):
					if (lamda>1):
						upper=mid
					else:
						lower=mid
					mid=(lower+upper)/2
					
					controllers=km.initialCluster(mid)
					print controllers
					maxControlDist=ng.getMaxControlDist()
					theta=maxControlDist*2/light_speed+5/1000
					pt=PTAS.PTAS(ng,theta,ds,controllers,d)
					pt.run()
					lamda=pt.getLamda()
					print "Lamda is {}".format(lamda)
				'''
				
				



