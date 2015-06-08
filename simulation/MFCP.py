from heapq import heappush, heappop
import priority_dict
import graphml_parser
import geopy
import shortest_path
import os
import matplotlib
from collections import deque
from os import listdir
import matplotlib.pyplot as plt
import graphInput
import MCFGraph
import SOM
import math


if __name__=="__main__":
	allFiles=os.listdir("../dataset/archive/")

	for modules in allFiles:
		if ("graphml" in modules):
			filePath="../dataset/archive/"+modules
			d_upper=3000
			u=30000

			#graph parsing
			gi=graphInput.graphInput(filePath)
			valid=gi.isValidGraph()
			gi.graphParser()
			gi.calculateGraphDiameter()

			if valid==1:
				left=1
				sList=gi.getSwitch()

				right=len(sList)*d_upper/float(u)

				mid=math.ceil((left+right)/2)

				mid=10
				print "Current B is: {}".format(mid)
				sObj=SOM.SOM(filePath,mid,gi)
				sObj.run()
				result=sObj.getZalpha()

				while(result!=1):
					print "Current B is: {}".format(mid)
					if (result>1):
						right=mid
					elif (result<1):
						left=mid

					sObj=SOM.SOM(filePath,mid)
					sObj.run()
					result=sObj.getZalpha()






