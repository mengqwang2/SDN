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

def isTight(ctr,ctrCover,s_found,uncovered):
	s_list=ctrCover[ctr]
	if s_found in s_list:
		for s in s_list:
			if s in uncovered:
				return 1
			return 0
	else:
		return 0
	

def allCovered(cost):
	ac=1
	for k,v in cost.iteritems():
		if v==0:
			ac=0

	return ac


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
				
				edge=ng.getGraph()
				diameter=ng.getDiameter()

				dens=ng.getDiameter()

				theta=float((2*diameter/300000000+5))/1000
				print theta

				fo=open(demandPath+".txt","r+")
				for s in switch:
					line=fo.readline()
					d[str(s)]=float(line[:-2])

				fo.close()

				c=ng.getController()
				
				ca=queuing.queuing(mu)
				nc=NodeCover.NodeCover(ng,ca,d,theta,c,mu)
				nc.ctrCover()
				nc.calculateNodeFreq()

				freq_pq=priority_dict.priority_dict()
				freq_pq=nc.getNodeFreqPair()
				ctrCover=nc.getCtrCover()
				cost=dict()
				for s in switch:
					cost[s]=0

				ctrList=[]
				ctrCand=[]
				uncovered=list(switch)
				ns=dict()
				for c in ctrCover:
					ctrCand.append(c)

				while (freq_pq):
					#print freq_pq.smallest()
					s_found=freq_pq.smallest()
					freq_pq.pop_smallest()
					if s_found in uncovered:
						cost[s_found]=1
					
						for ctr in ctrCand:
							if isTight(ctr,ctrCover,s_found,uncovered)==1:
								ctrList.append(ctr)
								ctrCand.remove(ctr)
								c_cover=[]
								for s in ctrCover[ctr]:
									add=1
									for k,v in ns.iteritems():
										if s in v:
											add=0
									if add==1:
										c_cover.append(s)
									if s in uncovered:
										uncovered.remove(s)
								if ctr not in c_cover:
									c_cover.append(ctr)
								ns[ctr]=c_cover
						
						if allCovered(cost):
							break
				
				ctr=len(ctrList)
				print ns
				print ctr

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

				#fo=open("A4_lb.csv","a")
				#line=str(modules[:-8])+","+str(maxN)+","+str(minN)+","+str(avgN)+","+str(len(switch))+"\n"
				#fo.write(line)
				#fo.close()


				
















