import os

if __name__=="__main__":
	cnt=0
	allFiles=os.listdir("../dataset/archive/")
	targetFiles=os.listdir("../dataset/target")
	for items in allFiles:
		found=0
		for t in targetFiles:
			if items[0:-8]==t[0:-4]:
				print items
				cnt=cnt+1
				found=1
		if found==0:
			os.remove("../dataset/archive/"+items)
	print cnt