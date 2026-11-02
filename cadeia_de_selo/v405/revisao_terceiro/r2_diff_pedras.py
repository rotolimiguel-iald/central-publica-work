import glob,hashlib,os,subprocess,sys,difflib
sys.stdout.reconfigure(encoding="utf-8")
W="C:/IALD/Central de Patentes/work/"
R1={"PonteDaMassa":"fbe1e27e9aa22fa5","MassaTensaoPura":"e70dc0d06a92805e","Identidade":"edd72109c090b62c","ObservadorTerminal":"959aaf88ea811e4d","LeiDoDiminuto":"6495f2de1de92683","TonicaDoHamiltoniano":"ff8ec9e0169a6764","DiscoDeEuler":"680725337c9edf91","PontoZeroDoPsion":"a50c68a59162fa36"}
out=open(W+"cadeia_de_selo/v405/revisao_terceiro/r2_diff_pedras.txt","w",encoding="utf-8")
for n,h in R1.items():
    cand=glob.glob(W+"**/"+n+".lean*",recursive=True)
    old=None
    for p in cand:
        try:
            if hashlib.sha256(open(p,"rb").read()).hexdigest()[:16]==h: old=p;break
        except: pass
    new=W+"cadeia_de_selo/v405/pedra/"+n+".lean"
    print(n,"R1 file:",old,"novo",hashlib.sha256(open(new,"rb").read()).hexdigest()[:16],hashlib.sha256(open("C:/t/k405c/final/TGLExt/"+n+".lean","rb").read()).hexdigest()[:16])
    if old:
        a=open(old,encoding="utf-8").read().split("\n");b=open(new,encoding="utf-8").read().split("\n")
        out.write("\n######## "+n+"\n")
        for l in difflib.unified_diff(a,b,lineterm="",n=0):
            if l.startswith(("---","+++")): continue
            out.write(l+"\n")
