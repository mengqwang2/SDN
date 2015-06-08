import graphml_parser
import os
import networkx as nx
from geopy.distance import vincenty
import shortest_path
import graphInput
import priority_dict
import math


class NetworkGraph():
	def __init__(self,gi):
		self.__graph=gi
		self.__switch=self.__graph.getSwitch()
		self.__controller=self.__graph.getController()
		self.__edges=self.__graph.getGraph()
		self.__graphDiameter=0
		self.__sp={}

	def calculateGraphDiameter(self):
		connected=self.__graph.isConnected()
		if connected==1:
			diameter={}
			for s in self.__switch:
				self.__sp[s]=priority_dict.priority_dict()
				diameter[s]=0
				sp=shortest_path.shortest_path(self.__switch,self.__edges)
				dist=sp.shortestPath(s)
				
				self.__sp[s]=dist.copy()

				while (dist and dist[dist.smallest()]!=999999999999):
					diameter[s]=dist[dist.smallest()]
					dist.pop_smallest()

			i=0
			max_d=0
			for k,v in diameter.iteritems():
				if i==0:
					max_d=diameter[k]
				else:
					if (diameter[k]>max_d):
						max_d=diameter[k]
				i=i+1
			self.__graphDiameter=max_d

		#print "Switches are {}".format(self.__switch)
		#print "Controllers are {}".format(self.__controller)
				
			#print "Current diameter is: {}".format(self.__graphDiameter)
		#else:
			#print "Current diameter does not exist."


	def getMaxControlDist(self,controller):
		maxDist=0
		sp=shortest_path.shortest_path(self.__switch,self.__edges)
		
		for s in self.__switch:
			dist=sp.shortestPath(s)

			while (dist and dist[dist.smallest()]!=999999999999):
				if dist.smallest() in controller:
					if dist[dist.smallest()]>maxDist:
						maxDist=dist[dist.smallest()]
				dist.pop_smallest()

		return maxDist

	#def graphStrip(self,theta):


	def getShortestPath(self):
		return self.__sp


	def getDiameter(self):
		return self.__graphDiameter

	def getGraph(self):
		return self.__edges

	def getSwitch(self):
		return self.__switch

	def getController(self):
		return self.__controller

	def getDistPQ(self):
		return self.__sp

