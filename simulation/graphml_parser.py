import xml.etree.ElementTree as ET
import libxml2

class graphml_parser():
	def __init__(self,filename):
		self.__filePath=filename
		self.__root=""

	def getTree(self):
		tree = libxml2.parseFile(self.__filePath)
		self.__root=tree.getRootElement()

	def getKeyDict(self):
		child=self.__root.children
		keyDict=dict()
		
		while child is not None:
			kid=""
			if child.name == "key":
				# do something with the child node
				for p in child.properties:
					if p.name=="id":
						keyDict[p.content]=dict()
						kid=p.content
				for p in child.properties:
					if p.name!="id":
						keyDict[kid][p.name]=p.content
			child = child.next
		return keyDict

	def getDataDict(self):
		dataDict=dict()
		child=self.__root.children
		while child is not None:
			if child.name == "graph":
				cur_root=child
				cur_child=cur_root.children
				while cur_child is not None:
					if cur_child.name == "data":
						for p in cur_child.properties:
							if p.name == "key":
								dataDict[p.content] = cur_child.content
					cur_child=cur_child.next
			child = child.next
		return dataDict

	def getNodeDict(self):
		nodeDict=dict()
		id=""
		child=self.__root.children
		while child is not None:
			if child.name == "graph":
				cur_root=child
				cur_child=cur_root.children
				while cur_child is not None:
					if cur_child.name == "node":
						for p in cur_child.properties:
							if p.name == "id":
								nodeDict[p.content]=dict()
								id=p.content
						c_root=cur_child
						c_child=cur_child.children
						while c_child is not None:
							if c_child.name == "data":
								for p in c_child.properties:
									if p.name == "key":
										nodeDict[id][p.content] = c_child.content
							c_child=c_child.next
					cur_child=cur_child.next
			child = child.next
		return nodeDict

	def getEdgeDict(self):
		edgeDict=dict()
		sid=""
		did=""
		child=self.__root.children
		while child is not None:
			if child.name == "graph":
				cur_root=child
				cur_child=cur_root.children
				while cur_child is not None:
					if cur_child.name == "edge":
						for p in cur_child.properties:
							if p.name == "source":
								sid=p.content
							if p.name == "target":
								did=p.content
						edgeDict[(sid,did)]=dict()
						c_root=cur_child
						c_child=cur_child.children
						while c_child is not None:
							if c_child.name == "data":
								for p in c_child.properties:
									if p.name == "key":
										edgeDict[(sid,did)][p.content] = c_child.content
							c_child=c_child.next
					cur_child=cur_child.next
			child = child.next
		return edgeDict

	


