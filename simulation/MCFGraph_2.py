class MCFGraph():
	def __init__(self,adj,u_edge,phi,flow,cost):
		self.__adj=adj
		self.__l={}
		self.__uedge=u_edge
		self.__phi=phi
		self.__flow=flow
		self.__cost=cost

	def graphUpdate(self,gamma):
		for node,edge in self.__adj.iteritems():
			if node not in self.__l:
				self.__l[node]={}
			for k,v in edge.iteritems():
				if k not in self.__l:
					self.__l[k]={}
				l1=gamma/self.__uedge[node][k]
				self.__l[node][k]=l1
				l2=gamma/self.__uedge[k][k]
				self.__l[k][k]=l2
				w1=l1
				w2=l2+1*self.__phi[k]
				self.__adj[node][k]=w1+w2

	def relaxation(self,epsilon,B,cur_demand,s,c_found):
		for node,edge in self.__adj.iteritems():
			for k,v in edge.iteritems():
				if (k==c_found):
					l1=self.__l[node][k]*(1+epsilon*self.__flow[node][k]/self.__uedge[node][k])
					self.__l[node][k]=l1
					l2=self.__l[k][k]*(1+epsilon*self.__flow[k][k]/self.__uedge[k][k])
					self.__l[k][k]=l2
					self.__phi[k]=self.__phi[k]*(1+epsilon*1/B)
					w1=l1
					w2=l2+1*self.__phi[k]
					self.__adj[node][k]=w1+w2

					self.__uedge[k][k]=self.__uedge[k][k]-self.__flow[k][k]

					#self.__cost[k]=self.calculateCost()

	def updateFlow(self,s,c_found,cur_demand):
		self.__flow[s][c_found]=cur_demand
		for node,edge in self.__adj.iteritems():
			for k,v in edge.iteritems():
				if (k==c_found):
					self.__flow[k][k]=self.__flow[k][k]+cur_demand

	def updateCost(self,c_found):
		self.__cost[c_found]=1
		#print self.__cost


	def calculateCost(self):
		c=0
		for k,v in self.__cost.iteritems():
			if (v==1):
				c=c+1
		return c


	def getGraph(self):
		return self.__adj

	def getCost(self):
		return self.__cost

	def getCapacity(self):
		return self.__uedge

	def getFlow(self):
		return self.__flow