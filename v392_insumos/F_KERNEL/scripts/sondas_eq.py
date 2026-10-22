import os,sys,json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leanlib as L
F=L.F; OV=os.path.join(F,"ov"); INST=os.path.join(F,"inst"); CONJ=os.path.join(F,"conj"); LOG=os.path.join(F,"logs","S")
res=[]
res.append(L.run_lean("S0_EqRealizada", os.path.join(INST,"TGLExt","Sonda","EqRealizada.lean"), INST, os.path.join(OV,"TGLExt","Sonda","EqRealizada.olean"), LOG, kernel_lib=OV))
res.append(L.run_lean("S0b_EqRealizada2", os.path.join(INST,"TGLExt","Sonda","EqRealizada2.lean"), INST, os.path.join(OV,"TGLExt","Sonda","EqRealizada2.olean"), LOG, kernel_lib=OV))
for nome in ["S1_EqNoKernel","S3_DuasRealizacoesEq1","S4_ListaSondas"]:
    res.append(L.run_lean(nome, os.path.join(CONJ,nome+".lean"), CONJ, None, LOG, kernel_lib=OV))
for r in res:
  out=open(r["log"],"rb").read().decode("utf-8","replace")
  print(r["nome"], "rc", r["rc"], "s", r["segundos"])
  print("   ", "\n    ".join(l for l in out.splitlines() if l.startswith("SONDA") or "error" in l)[:2500])
print(L.dump({"sondas":res}, os.path.join(F,"RESULTADO_S_sondas_eq.json")))
