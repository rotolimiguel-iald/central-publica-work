import sys,os
OUT=r"C:\t\k411c\revisao_A"
lines=open(os.path.join(OUT,"mydiff.diff"),"rb").read().decode("utf-8","surrogateescape").split("\n")
want=set(int(x) for x in sys.argv[1].split(","))
maxw=int(sys.argv[2]) if len(sys.argv)>2 else 600
maxl=int(sys.argv[3]) if len(sys.argv)>3 else 60
i=-1;n=0
for l in lines:
    if l.startswith("@@"):
        i+=1;n=0
    if i in want:
        n+=1
        if n<=maxl:
            print(l.replace("\r","")[:maxw])
        elif n==maxl+1: print("...")
