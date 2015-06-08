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

class NodeCover():
	def __init__(self,ng,ca,d,theta,ctr,mu):
		self.__ng=ng
		self.__switch=self.__ng.getSwitch()
		self.__edge=self.__ng.getGraph()
		self.__controller=ctr
		self.__ca=ca
		self.__d=d
		self.__theta=theta
		self.__sp=shortest_path.shortest_path(self.__switch,self.__edge)
		self.__nf=priority_dict.priority_dict()
		self.__minFreq=dict()
		self.__avgFreq=dict()
		self.__res=dict()
		for k in self.__controller:
			self.__res[k]=mu
		self.__cost=[]
		self.__initialSet=dict()
		self.__ctrCover=dict()
		self.__mu=mu


	def initiateSet(self):
		node_dist=dict()
		for n in self.__switch:
			node_dist[n]=self.__sp.shortestPath(n)

		initialSet=dict()

		for i in range(0,len(self.__d)):
			k=self.__d[i][0]
			v=self.__d[i][1]
			pq=node_dist[k]

			loop=1

			while (loop==1):
				try:
					if (pq.smallest() in self.__controller):
						if (self.__res[pq.smallest()]>=v):
							loop=0
					if loop==1:
						pq.pop_smallest()
				except RuntimeError as e:
					print "Capacity bound exceeded."
					loop=-1



			ctrFound=pq.smallest()
			dist=pq[pq.smallest()]
			self.__res[ctrFound]=self.__res[ctrFound]-v

			self.__cost.append(2*dist/300000000+self.__ca.queuingTime(k,ctrFound,v))
			self.__ca.updateAssignment(k,ctrFound,v)

			if (ctrFound not in initialSet):
				initialSet[ctrFound]=[]
			initialSet[ctrFound].append(k)


		self.__initialSet=initialSet

	def ctrCover(self):
		ca1=queuing.queuing(self.__mu)
		node_dist=dict()
		for n in self.__switch:
			node_dist[n]=self.__sp.shortestPath(n)

		for c in self.__controller:
			while (node_dist[c]):
				k=node_dist[c].smallest()
				v=node_dist[c][k]
				demand=self.__d[k]

				t=2*v/300000000+ca1.queuingTime(k,c,demand)
				if (t<self.__theta):
					ca1.updateAssignment(k,c,demand)
				node_dist[c].pop_smallest()

		self.__ctrCover=ca1.getAssignment()

	def calculateNodeFreq(self):
		self.ctrCover()
		nodefreqpair=priority_dict.priority_dict()

		for ele in self.__switch:
			nodefreqpair[ele]=0

		maxFreq=0
		for k,v in self.__ctrCover.iteritems():
			countNode=0
			for ele in self.__switch:
				if ele in v:
					nodefreqpair[ele]=nodefreqpair[ele]+1
		
		self.__nf=nodefreqpair


	def calculateRedundanceList(self):
		redlist=dict()
		for k,v in self.__ctrCover.iteritems():
			if k not in redlist:
				redlist[k]=[]
			for s in v:
				redlist[k].append(self.__nf[s])
		print redlist


	def getInitialSet(self):
		return self.__initialSet

	def getCtrCover(self):
		return self.__ctrCover

	def getNodeFreqPair(self):
		return self.__nf

	def getAvgCost(self):
		return sum(self.__cost)/len(self.__cost)






