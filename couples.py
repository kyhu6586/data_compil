r=open("couples2xo4.txt","r")
s=open("couples2xo4_new.txt","w+")
for line in r:
    split=line.split()
    if split[7]=="HA":
        s.write(line)
