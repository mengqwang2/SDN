import graphml_parser
import os
import networkx as nx
from geopy.distance import vincenty
import shortest_path

class graphInput():
	def __init__(self,filepath):
		self.__path=filepath
		self.__switch=[]
		self.__controller=[]
		self.__graph={}
		self.__parse=graphml_parser.graphml_parser(str(self.__path))
		self.__isConnected=1
		self.__geoCord=dict()

	def graphParser(self):
		self.__parse=graphml_parser.graphml_parser(str(self.__path))
		g = nx.read_graphml(str(self.__path))
		graph = self.__parse
		graph.getTree()
		keyDict=graph.getKeyDict()
		dataDict=graph.getDataDict()
		nodeDict=graph.getNodeDict()
		edgeDict=graph.getEdgeDict()

		valid=self.isValidGraph()

		if valid==1:
			la_id=""
			long_id=""
			for k,v in keyDict.iteritems():
				for vname,vvalue in v.iteritems():
					if vname=="attr.name":
						if vvalue=="Latitude":
							la_id=k
						if vvalue=="Longitude":
							long_id=k

			node=g.nodes()

			edge=dict()
			nodeConnected=[]

			for link in g.edges():
				if (link[0] not in edge):
					edge[link[0]]=dict()
					nodeConnected.append(link[0])
				if (link[1] not in edge):
					edge[link[1]]=dict()
					nodeConnected.append(link[1])


				la_0=nodeDict[link[0]][la_id]
				long_0=nodeDict[link[0]][long_id]
				la_1=nodeDict[link[1]][la_id]
				long_1=nodeDict[link[1]][long_id]

				dist=vincenty((la_0,long_0), (la_1,long_1)).meters
				edge[link[0]][link[1]]=dist
				edge[link[1]][link[0]]=dist

				if (link[0] not in self.__geoCord):
					self.__geoCord[link[0]]=(la_0,long_0)
				if (link[1] not in self.__geoCord):
					self.__geoCord[link[1]]=(la_1,long_1)

			s=[]
			c=[]

			for ele in node:
				s.append(ele)
				c.append(ele)

			for n in node:
				if n not in nodeConnected:
					self.__isConnected=0

			self.__switch=s
			self.__controller=c
			self.__graph=edge



	def isValidGraph(self):
		self.__parse.getTree()
		kd=self.__parse.getKeyDict()
		nd=self.__parse.getNodeDict()

		#validate kd
		la_id=""
		long_id=""
		for k,v in kd.iteritems():
			for vname,vvalue in v.iteritems():
				if vname=="attr.name":
					if vvalue=="Latitude":
						la_id=k
					if vvalue=="Longitude":
						long_id=k
		if la_id=="" or long_id=="":
			return 0

		#validate nd
		v1=0
		v2=0
		for k,v in nd.iteritems():
			for e1,e2 in v.iteritems():
				if e1==la_id:
					v1=v1+1
				if e1==long_id:
					v2=v2+1
		if v1!=len(nd) or v2!=len(nd):
			return 0

		return 1

	def isConnected(self):
		return self.__isConnected

	def getGraph(self):
		return self.__graph

	def getSwitch(self):
		return self.__switch

	def getController(self):
		return self.__controller

	def getGeoCord(self):
		return self.__geoCord


