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


def pickMax(tupleArr):
	maxFreq=tupleArr[0][1]
	optList=[]
	for i in range (0,len(tupleArr)):
		if tupleArr[i][1]==maxFreq:
			optList.append(tupleArr[i][0])
	return optList


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

				#fo=open(thetaPath+".txt","r+")
				#ratio=fo.read()
				#fo.close()
				#ratio=int(ratio)

				theta=float((2*diameter/300000000+5))/1000

				fo=open(demandPath+".txt","r+")
				for s in switch:
					line=fo.readline()
					d[str(s)]=float(line[:-2])

				fo.close()

				sorted_d_tuple=[(k,v) for v,k in sorted([(v,k) for k,v in d.items()],reverse=True)]

				s=ng.getSwitch()
				n_ctr=len(s)

				c=ng.getController()

				ca=queuing.queuing(mu)
				nc=NodeCover.NodeCover(ng,ca,sorted_d_tuple,theta,c,mu)
				nc.ctrCover()
				nc.initiateSet()
			
				avg_rt=nc.getAvgCost()
				costDif=avg_rt
				
				while (avg_rt<theta):
					#Find the controller to remove
					ctrRemove=''
					costDif=9999

					for ele in c:
						c_test=list(c)
						c_test.remove(ele)
						ca=queuing.queuing(mu)
						nc=NodeCover.NodeCover(ng,ca,sorted_d_tuple,theta,c_test,mu)
						nc.initiateSet()
						
						if (nc.getAvgCost()-avg_rt<costDif):
							ctrRemove=ele
							costDif=nc.getAvgCost()-avg_rt

					c.remove(ctrRemove)
					avg_rt=costDif+avg_rt

				ctr=len(c)
				print ctr

				fo=open("A2.txt","a")
				line=str(modules[:-8])+" "+str(ctr)+" "+str(len(switch))+"\n"
				fo.write(line)
				fo.close()













