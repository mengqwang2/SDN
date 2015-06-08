import priority_dict
import graphml_parser
import shortest_path
import os
import graphInput
import MCFGraph
import math
import queuing
import random
import kmeans

class PTAS():
	def __init__(self,ng,ds,km,d,numController):
		self.__path={}
		self.__ds=ds
		self.__ng=ng
		self.__km=km
		self.__cost=0
		self.__lamda=0
		self.__d=d
		self.__B=0
		self.__numController=numController


	def run(self):
		print "Running PTAS"
		epsilon=0.1
		beta=0.3
		d=self.__d
		light_speed=3*math.pow(10,8)
		u=30000
		mu=30000

		numCluster=self.__numController

		controllers=self.__km.initialCluster(numCluster/2)
		maxControlDist=self.__ng.getMaxControlDist(controllers)
		theta=maxControlDist*2/light_speed+5/1000
		self.__B=theta

		controllers=self.__km.initialCluster(numCluster)
		self.__controllers=controllers
		print controllers

		edge=self.__ng.getGraph()
		switch=self.__ng.getSwitch()

		ds=self.__ds

		adj={}

		for s1 in switch:
			adj[s1]={}
			for s2 in self.__controllers:
				adj[s1][s2]=0

		d_node={}

		count=0
		for node in adj:
			d_node[str(node)]=0
			count=count+1

		x=math.pow(1+count*epsilon,(1-epsilon)/epsilon)
		x=1/x
		y=math.pow((1-epsilon)/(count*(count-1)),1/epsilon)

		gamma=x*y

		curCost=float(0)

		bv1=0

		while (curCost<theta*len(switch)):
			
			print "Current budget is: {}".format(theta*len(switch))
			
			u_edge={}
			phi={}
			flow={}
			cost={}
			path={}

			ca=queuing.queuing(mu)

			for node,edge in adj.iteritems():
				if node not in u_edge:
					u_edge[str(node)]={}
				if node not in flow:
					flow[str(node)]={}
				if node not in phi:
					phi[str(node)]={}
				for k,v in edge.iteritems():
					if k not in u_edge:
						u_edge[str(k)]={}
					if k not in flow:
						flow[str(k)]={}
					if k not in phi:
						phi[str(k)]={}

					if node!=k:
						phi[str(node)][str(k)]=gamma/self.__B
						u_edge[str(node)][str(k)]=3*d[str(node)]
						flow[str(node)][str(k)]=0

					phi[str(k)][str(k)]=gamma/self.__B
					u_edge[str(k)][str(k)]=u
					flow[str(k)][str(k)]=0
				cost[node]=0

			mg=MCFGraph.MCFGraph(adj,u_edge,phi,flow,cost)
			mg.graphUpdate(gamma,ca,ds,d)
			adj_mcf=mg.getGraph()

			sp=shortest_path.shortest_path(switch,adj_mcf)
			
			node_dist=priority_dict.priority_dict()

			for c in controllers:
				d_node[str(c)]=d_node[str(c)]+beta*d[str(c)]
				mg.updateFlow(str(c),str(c),d_node[str(c)])
				path[c]=str(c)
				dist=0
				ca.updateAssignment(c,str(c),d_node)
				t=ca.queuingTime(str(c))
				rtt=t
				cur_demand=d_node[str(c)]
				mg.updateCost(c,rtt)
				mg.relaxation(epsilon,self.__B,cur_demand,c,str(c),ca,ds)
				adj_mcf=mg.getGraph()
				sp=shortest_path.shortest_path(switch,adj_mcf)

			totalDemand=0
			for s in switch:
				if s not in controllers:
					if bv1==0:
						d_node[str(s)]=d[str(s)]
						totalDemand=totalDemand+d_node[str(s)]
						cur_demand=d_node[str(s)]
						u_edge=mg.getCapacity()
						flow=mg.getFlow()

						node_dist[s]=sp.shortestPath(s)

						c_found=node_dist[s].smallest()

						
						while (flow[str(c_found)][str(c_found)]+cur_demand>u_edge[str(c_found)][str(c_found)]):
							node_dist[s].pop_smallest()
							if len(node_dist[s])>0:
								if node_dist[s].smallest() in self.__controllers:
									c_found=node_dist[s].smallest()
							else:
								bv1=1
								break

						if bv1==0:
							c_found=node_dist[s].smallest()

							mg.updateFlow(str(s),str(c_found),cur_demand)

							path[s]=str(c_found)

							dist=ds[s][str(c_found)]

							ca.updateAssignment(s,str(c_found),d_node)

							t=ca.queuingTime(str(c_found))

							rtt=dist*2/light_speed+t

							mg.updateCost(s,rtt)

							mg.relaxation(epsilon,self.__B,cur_demand,s,str(c_found),ca,ds)

							adj_mcf=mg.getGraph()

							sp=shortest_path.shortest_path(switch,adj_mcf)
						
			totalCost=mg.calculateCost()
			curCost=float(totalCost)
			print "Total demand is {}.".format(totalDemand)
			print "Cost is {}, K is {}.".format(curCost,len(controllers))
			
			self.__path=path
			self.__cost=curCost

			if bv1==0:
				numCluster=numCluster-1
			else:
				numCluster=numCluster+1
				bv1=0

			controllers=self.__km.initialCluster(numCluster)
			self.__controllers=controllers

			adj={}

			for s1 in switch:
				adj[s1]={}
				for s2 in self.__controllers:
					adj[s1][s2]=0

			print controllers

			print "Iteration ends."


	def getPath(self):
		return self.__path

	def getCost(self):
		return self.__cost

	def getLamda(self):
		return self.__lamda





				


