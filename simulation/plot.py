import matplotlib
import matplotlib.pyplot as plt

class plot():
	def __init__(self,ctrCount,nodeCount):
		self.__ctrCount=ctrCount
		self.__nodeCount=nodeCount

	def diagramPlot(self):
		plt.bar(range(len(self.__ctrCount)), self.__ctrCount.values(), align='center')
		#plt.bar(range(len(nodeCount)), nodeCount.values(), align='center')
		plt.xticks(range(len(self.__ctrCount)), self.__ctrCount.keys(),rotation='vertical')

		plt.show()