import math
import operator
f=open("toSort.txt","r")

class Data:
    num=0
    name=""
    val=0.0
    full=""
    def __init__(self,n,na,v,f):
        self.num=n
        self.name=na
        self.val=v
        self.full=f
sorter=[]
for line in f:
    split=line.split()
    obj=Data(int(split[6]),split[7],float(split[22]),str(line))
    print(obj.full)
    sorter+=[obj]
sorter.sort(key=operator.attrgetter('num'))
r=open('couples2nbr.txt','w+')
for s in sorter:
    r.write(s.full+"")
r.close()
print("File written to couples2nbr.txt")

