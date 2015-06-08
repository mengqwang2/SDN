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


class GraphStrip():
	def __init__(self,gi,ng,theta):
		self.__gi=gi
		self.__ng=ng
		self.__geoCord=dict()
		self.__theta=theta
		self.__newGraph=dict()

	def graphReconstruct(self):
		edge=self.__ng.getGraph()
		edge_new=dict()
		switch=self.__ng.getSwitch()
		sp=shortest_path.shortest_path(switch,edge)
		self.__geoCord=self.__gi.getGeoCord()

		for s in switch:
			dist=sp.shortestPath(s)
			if s not in edge_new:
				edge_new[s]=priority_dict.priority_dict()
			edge_new[s]=dist

		self.__newGraph=edge_new

		for k,v in self.__geoCord.iteritems():
			lat=v[0]
			longi=v[1]
			if v[1]<0:
				longi=180+abs(v[1])
			self.__geoCord[k]=(float(lat),float(longi))


	def findLeftMostNode(self,nodeLeft):
		leftCord=360
		nodeFound=''
		for s in nodeLeft:
			longi=self.__geoCord[s][1]
			if longi<leftCord:
				leftCord=longi
				nodeFound=s
		return (nodeFound,leftCord)

	def findUpperMostNode(self,nodeLeft):
		upperCord=-180
		nodeFound=''
		for s in nodeLeft:
			lat=self.__geoCord[s][0]
			if lat>upperCord:
				upperCord=lat
				nodeFound=s
		return (nodeFound,upperCord)

	def findRightMostNode(self,nodeLeft):
		rightCord=0
		nodeFound=''
		for s in nodeLeft:
			longi=self.__geoCord[s][1]
			if longi>rightCord:
				rightCord=longi
				nodeFound=s
		return (nodeFound,rightCord)

	def findLowerMostNode(self,nodeLeft):
		lowerCord=180
		nodeFound=''
		for s in nodeLeft:
			lat=self.__geoCord[s][0]
			if lat<lowerCord:
				lowerCord=lat
				nodeFound=s
		return (nodeFound,lowerCord)


	def graphStripe(self):
		#Divide the regions on the graph map according to the geolocation and theta
		geoCord=self.__geoCord
		theta=self.__theta
		switch=self.__ng.getSwitch()
		edge=self.__newGraph

		total1=list(switch)
		propDist=theta*300000000

		nodeDist=[]

		while (total1):
			st=self.findLeftMostNode(total1)[0]
			nodeBag=[]

			for k,v in edge[st].iteritems():
				if v<=propDist:
					if k in total1:
						nodeBag.append(k)

			rightCord=self.findRightMostNode(nodeBag)[1]


			for s in switch:
				if geoCord[s][1]<=rightCord:
					if (s in total1) and (s not in nodeBag):
						nodeBag.append(s)

			for ele in nodeBag:
				total1.remove(ele)

			nodeDist.append(nodeBag)


		nodeGrid=[]

		for horiNode in nodeDist:
			total2=list(horiNode)
			while (total2):
				st=self.findUpperMostNode(total2)[0]

				nodeBag=[]

				for k,v in edge[st].iteritems():
					if v<=propDist:
						if k in total2:
							nodeBag.append(k)

				lowerCord=self.findLowerMostNode(nodeBag)[1]

				for s in switch:
					if geoCord[s][0]>=lowerCord:
						if ((s in total2) and (s not in nodeBag)):
							nodeBag.append(s)

				for ele in nodeBag:
					total2.remove(ele)

				nodeGrid.append(nodeBag)

		return nodeGrid

