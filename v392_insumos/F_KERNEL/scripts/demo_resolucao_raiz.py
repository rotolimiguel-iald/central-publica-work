# DEMONSTRACAO (achado da 1a execucao, reproduzido): com o LEAN_PATH comecando nos .olean do kernel do Nos e uma pasta
# EXTRA do sandbox com TGLExt/V351DualScalingBridge.olean, o import TGLExt.V351DualScalingBridge FALHA -- o lean so
# procura o modulo da raiz TGLExt na 1a pasta que contem TGLExt. Consequencia: pedras novas TGLExt.* que importam
# outras pedras novas so compilam fora do kernel numa sobreposicao (ov) ou numa arvore completa do kernel (como a v390).
import os,sys,json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leanlib as L
F=L.F; INST=os.path.join(F,"inst"); DEMO=os.path.join(F,"demo_build"); LOG=os.path.join(F,"logs","B0")
r1=L.run_lean("B0_ponte_em_pasta_extra", os.path.join(INST,"TGLExt","V351DualScalingBridge.lean"), INST,
              os.path.join(DEMO,"TGLExt","V351DualScalingBridge.olean"), LOG)              # kernel_lib=None: Nos primeiro
r2=L.run_lean("B0_agape_com_pasta_extra", os.path.join(INST,"TGLExt","AgapeNonVacuity.lean"), INST, None, LOG,
              extra_paths=[DEMO])                                                           # Nos primeiro + pasta extra
for r in (r1,r2):
    print(r["nome"],"rc",r["rc"],"s",r["segundos"],"erros",[e[-260:] for e in r["erros"][:1]])
print(L.dump({"demo":[r1,r2]}, os.path.join(F,"RESULTADO_B0_resolucao_raiz.json")))
