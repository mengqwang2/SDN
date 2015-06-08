class MCFGraph():
	def __init__(self,adj,u_edge,phi,flow,cost):
		self.__adj=adj
		self.__l={}
		self.__uedge=u_edge
		self.__phi=phi
		self.__flow=flow
		self.__cost=cost
		self.__controller=[]
		self.__switch=[]

	def graphUpdate(self,gamma,ca,ds,d):
		for node,edge in self.__adj.iteritems():
			if node not in self.__l:
				self.__l[node]={}
			for k,v in edge.iteritems():
				if node!=k:
					if k not in self.__l:
						self.__l[k]={}
					l1=gamma/self.__uedge[str(node)][str(k)]
					self.__l[node][k]=l1
					w1=l1+(ds[node][str(k)]/300000000)*self.__phi[str(node)][str(k)]
				else:
					l1=gamma/(3*d[str(node)])
					w1=l1
				l2=gamma/self.__uedge[str(k)][str(k)]
				self.__l[k][k]=l2
				w2=l2+(1/ca.getMu())*self.__phi[str(k)][str(k)]
				self.__adj[node][k]=w1+w2



	def relaxation(self,epsilon,B,cur_demand,s,c_found,ca,ds):
		if s!=c_found:
			self.__phi[s][c_found]=self.__phi[s][c_found]*(1+epsilon*ds[s][c_found]/B)
		st=ca.queuingTime(c_found)
		self.__uedge[c_found][c_found]=self.__uedge[c_found][c_found]-cur_demand
		self.__phi[c_found][c_found]=self.__phi[c_found][c_found]*(1+epsilon*st/B)


		for node,edge in self.__adj.iteritems():
			for k,v in edge.iteritems():
				if (k==c_found):
					if node!=k:
						l1=self.__l[node][k]*(1+epsilon*self.__flow[node][k]/self.__uedge[node][k])
						self.__l[node][k]=l1
						l2=self.__l[k][k]*(1+epsilon*self.__flow[k][k]/self.__uedge[k][k])
						self.__l[k][k]=l2
						w1=l1+(ds[node][str(k)]/300000000)*self.__phi[node][str(k)]
						w2=l2+(ca.queuingTime(k)/300000000)*self.__phi[str(k)][str(k)]
						self.__adj[node][str(k)]=w1+w2
					else:
						l2=self.__l[k][k]*(1+epsilon*self.__flow[k][k]/self.__uedge[k][k])
						self.__l[k][k]=l2


	def updateFlow(self,s,c_found,cur_demand):
		if s!=c_found:
			self.__flow[s][c_found]=cur_demand
		self.__flow[c_found][c_found]=self.__flow[c_found][c_found]+cur_demand

	def updateCost(self,s,rtt):
		self.__cost[s]=rtt
		#print self.__cost

	def calculateCost(self):
		#print self.__cost
		#maxCost=float(0)
		totalCost=float(0)
		for k,v in self.__cost.iteritems():
			totalCost=totalCost+v
		#print self.__cost
		return totalCost

	def getGraph(self):
		return self.__adj

	def getCost(self):
		return self.__cost

	def getCapacity(self):
		return self.__uedge

	def getFlow(self):
		return self.__flow