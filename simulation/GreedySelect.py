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

class GreedySelect():
	def __init__(self,switch,ng):
		self.__switch=switch
		self.__ng=ng
		self.__ns=dict()

	def greedySelection(self,mu,theta,d_dict):
		s=list(self.__switch)
		c=list(self.__switch)

		switch=self.__ng.getSwitch()
		edge=self.__ng.getGraph()
		
		sp=shortest_path.shortest_path(switch,edge)
		node_dist=dict()
		for n in s:
			node_dist[n]=sp.shortestPath(n)

		ctr_cnt=0
		ctr=[]

		ns=dict()
		while s:
			node_asg={}
			nodehp=priority_dict.priority_dict()
			for ele in c:
				node_asg[ele]=[]
				neighbour=[]
				cnt=0
				ca=queuing.queuing(mu)

				for n,dist in node_dist[ele].iteritems():
					if n in s:
						if n!=ele:
							d=d_dict[n]
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
			ns[c_node]=node_asg[c_node]


			ctr_cnt=ctr_cnt+1
			s.remove(c_node)
			c.remove(c_node)

			for node in node_asg[c_node]:
				if node in s:
					s.remove(node)
				if node in c:
					c.remove(node)

		#print ns
		#print ctr
		for k,v in ns.iteritems():
			ns[k].append(k)
		self.__ns=ns
		return ctr_cnt

	def getNodeAsg(self):
		return self.__ns

