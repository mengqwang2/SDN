import shortest_path
import math
import priority_dict

class kmeans():
	def __init__(self,networkGraph):
		self.__gi=networkGraph
		self.__graph=self.__gi.getGraph()
		self.__switch=self.__gi.getSwitch()
		self.__distPQ=self.__gi.getDistPQ().copy()

	def initialCluster(self,k):
		#print self.__distPQ
		selected=[]
		allNodes=self.__switch
		remainNodes=allNodes

		selected.append(self.findInitialPoint())

		#print self.__distPQ

		while (len(selected)<=k):
			maxC=0
			nodeSelect=''
			for n1 in remainNodes:
				sumC=0
				for n2 in remainNodes:
					if n2!=n1:
						dist=self.__distPQ[n2][n1]
						D=self.findSmallest(self.__distPQ[n2],n2,selected)
						#print D
						sumC+=max(D-dist,0)
				if sumC>maxC:
					nodeSelect=n1
					maxC=sumC

			selected.append(nodeSelect)

		return selected


	def findSmallest(self,distPQ,n,selected):
		minDist=999999999999
		for k,v in distPQ.iteritems():
			if v<minDist and k in selected:
				minDist=v
		return minDist

	def findInitialPoint(self):
		allNodes=self.__switch
		sumMin=0
		nodeFind=''
		i=0
		for n1 in allNodes:
			sumNode=0
			for n2 in allNodes:
				if n2!=n1:
					dist=self.__distPQ[n1][n2]
					sumNode=sumNode+dist
			if i==0:
				sumMin=sumNode
			else:
				if sumNode<sumMin:
					nodeFind=n1
			i=i+1
		return nodeFind








		

			
