import os

class queuing():
	def __init__(self,mu):
		self.__controller={}
		self.__mu=mu
		self.__arrival={}


	def updateAssignment(self,s,c,d_node):
		if c not in self.__controller:
			self.__controller[c]=[]
			self.__arrival[c]=0
		self.__controller[c].append(s)
		self.__arrival[c]=self.__arrival[c]+d_node

	def queuingTime(self,s,c,d_node):
		if c not in self.__controller:
			self.__arrival[c]=0
		arrival=self.__arrival[c]+d_node
		t=1/(self.__mu-arrival)
		return t

	def getMu(self):
		return self.__mu

	def getAssignment(self):
		return self.__controller
