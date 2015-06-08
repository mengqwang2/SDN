import graphml_parser
import os
import networkx as nx
from geopy.distance import vincenty
import shortest_path
import graphInput
import priority_dict
import math
import NodeCover

class FlowRoute():
	def __init__(self,gi,ctr,demand,sp,mu,ca,theta):
		self.__graph=gi
		self.__controller=ctr
		self.__avgDelay=0
		self.__demand=demand
		self.__sp=sp
		self.__res=dict()
		for k in self.__controller:
			self.__res[k]=mu
		self.__ca=ca
		self.__theta=theta
		

	def routeFlow(self):
		for k,v in self.__demand.iteritems():
			#print self.__sp[k]



