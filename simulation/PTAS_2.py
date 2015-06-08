import priority_dict
import graphml_parser
import shortest_path
import os
import graphInput
import MCFGraph
import math
import queuing
import random

class PTAS():
	def __init__(self,alpha,gi,B,ds,theta):
		self.__alpha=alpha
		self.__gi=gi
		self.__sub=[]
		self.__path={}
		self.__B=B
		self.__theta=theta
		self.__ds=ds

	def run(self):
		epsilon=0.1
		beta=0.3
		alpha=self.__alpha
		d={}
		light_speed=3*math.pow(10,5)
		u=30000
		
		d_lower=1500
		d_upper=3000
		mu=30000

		self.__gi.graphParser()
		edge=self.__gi.getGraph()
		switch=self.__gi.getSwitch()
		controller=self.__gi.getController()
		ds=self.__ds

		adj={}

		for s1 in switch:
			adj[s1]={}
			d[s1]=0
			for s2 in switch:
				if s2!=s1:
					adj[s1][s2]=0

		#print adj

		d_node={}
		r_node={}

		count=0
		for node in adj:
			d_node[node]=0
			r_node[node]=0
			count=count+1

		x=math.pow(1+count*epsilon,(1-epsilon)/epsilon)
		x=1/x
		y=math.pow((1-epsilon)/(count*(count-1)),1/epsilon)

		gamma=x*y

		totalCost=4

		for s in switch:
			d[s]=d_lower+random.random()*(d_upper-d_lower)

		path={}
		
		while (totalCost<self.__B):
			print "Current cost is: {}".format(totalCost)

			u_edge={}
			phi={}
			flow={}
			cost={}

			ca=queuing.queuing(d,mu)

			for node in d_node:
				d_node[node]=d_node[node]+beta*d[node]

			for node,edge in adj.iteritems():
				if node not in u_edge:
					u_edge[node]={}
				if node not in flow:
					flow[node]={}
				for k,v in edge.iteritems():
					if k not in u_edge:
						u_edge[k]={}
					if k not in flow:
						flow[k]={}
					phi[k]=gamma/self.__B
					u_edge[node][k]=d_node[node]
					u_edge[k][k]=u
					flow[node][k]=0
					flow[k][k]=0
					cost[k]=0

			mg=MCFGraph.MCFGraph(adj,u_edge,phi,flow,cost)
			mg.graphUpdate(gamma)
			adj_mcf=mg.getGraph()
			path={}

			
			sp=shortest_path.shortest_path(switch,adj_mcf)
			#print adj_mcf
			
			  
			node_dist=priority_dict.priority_dict()

			for s in switch:
				print len(switch), totalCost
				cur_demand=d_node[s]
				u_edge=mg.getCapacity()
				flow=mg.getFlow()

				node_dist[s]=sp.shortestPath(s)
				#print node_dist[s]
				
				c_found=node_dist[s].smallest()

				while (flow[c_found][c_found]+cur_demand>u_edge[c_found][c_found]):
					node_dist[s].pop_smallest()

				c_found=node_dist[s].smallest()

				mg.updateFlow(s,c_found,cur_demand)
				mg.updateCost(c_found)

				path[s]=c_found

				
				dist=ds[s][c_found]

				#print s, c_found, node_dist[s][c_found]

				ca.updateAssignment(s,c_found)
				t=ca.queuingTime(s,c_found)
				
				rtt=dist/light_speed*2+t   
				r_node[s]=cur_demand/d[s]+alpha*(self.__theta-rtt)
				print rtt, self.__theta
				self.__sub.append(self.__theta-rtt)

				mg.relaxation(epsilon,self.__B,cur_demand,s,c_found)
				adj_mcf=mg.getGraph()
				sp=shortest_path.shortest_path(switch,adj_mcf)
				totalCost=mg.calculateCost()

			
			print len(switch), totalCost
			#print "Current path is: {}".format(path)

		i=0
		min_obj=0
		x=math.log((1+epsilon)/gamma,1+epsilon)
		for node in r_node:
			if (i==0):
				r_node[node]=r_node[node]/x
				min_obj=r_node[node]
			else:
				r_node[node]=r_node[node]/x
				if (r_node[node]<min_obj):
					min_obj=r_node[node]
			i=i+1

		self.__path=path
		return min_obj

	def getSubGradient(self):
		return self.__sub

	def getPath(self):
		return self.__path





				


