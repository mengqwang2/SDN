import priority_dict

class shortest_path():
	def __init__(self,node,edge):
		self.__node=node
		self.__edge=edge

	def shortestPath(self,n):

		wl=priority_dict.priority_dict()

		found=priority_dict.priority_dict()

		for ele in self.__node:
			if ele!=n:
				wl[ele]=999999999999

		found[n]=0

		#initialize: relaxation
		for ele in found:
			if ele in self.__edge:
				for key,value in self.__edge[ele].iteritems():
					wl[key]=value


		while wl:
			# dequeue the cloest node
			found[wl.smallest()]=wl[wl.smallest()]
			#print wl.smallest(), wl[wl.smallest()]
			wl.pop_smallest()

			# relaxation
			for k1,v1 in wl.iteritems():
				for k2,v2 in found.iteritems():
					if k2 in self.__edge:
						if k1 in self.__edge[k2]:
							if found[k2]+self.__edge[k2][k1]<wl[k1]:
								wl[k1]=found[k2]+self.__edge[k2][k1]

		return found


	

