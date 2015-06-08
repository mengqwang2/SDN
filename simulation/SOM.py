import PTAS
import graphInput

class SOM():
	def __init__(self,filePath,B,gi):
		self.__zalpha=0
		self.__fp=filePath
		self.__B=B
		self.__r=[]
		self.__mu=1
		self.__h=0.5
		self.__gi=gi

	def run(self):
		alpha=3
		g=1

		gi=self.__gi

		result=0
		ds=gi.getShortestPath()
		diameter=gi.getDiameter()
		theta_lower=2*diameter+5
		theta_upper=2*diameter+10

		theta=2*diameter+5
		

		pt=PTAS.PTAS(alpha,gi,self.__B,ds,theta)
		result=pt.run()
		print "Current result is: {}".format(result)
		self.__r.append(result)
		subList=pt.getSubGradient()
		sub_avg=sum(subList)/float(len(subList))
		square_list=[]
		for s in subList:
			square_list.append(s*s)
		

		while (sub_avg!=0):
			minZalpha=min(self.__r)
			isSortedDecrease=lambda l: all(l[i] >= l[i+1] for i in xrange(len(l)-1))
			if (isSortedDecrease(self.__r)):
				self.__mu=self.__mu*self.__h
			
			g=self.__mu*(minZalpha-result)/sum(square_list)
			alpha=alpha+g*sub_avg
			pt=PTAS.PTAS(alpha,gi,self.__B,ds,theta)		
			result=pt.run()
			self.__r.append(result)
			subList=pt.getSubGradient()
			sub_avg=sum(subList)/float(len(subList))
			square_list=[]
			for s in subList:
				square_list.append(s*s)
			

		self.__zalpha=result

	def getZalpha(self):
		return self.__zalpha




