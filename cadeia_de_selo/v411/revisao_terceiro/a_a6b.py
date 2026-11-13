"""A6b: a guarda de material privado (a funcao da E03 da G1, so' leitura) sobre: os blobs DECODIFICADOS do candidato, as 11 falas embutidas, as linhas novas do candidato, o TOPO. Imprime so' contagens."""
import base64, hashlib, json, os, re, sys
import a_lib
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import espelho_pares as E
priv = E.carregar_marcadores_privados()
print("marcadores privados carregados:", len(priv), "| termos da casa:", len(E.GUARDA))
f = a_lib.Fonte(a_lib.CAND, "cand")
ns = f.carregar(["_V411_H0DN_CONTRACT", "_V411_H0DN_INSUMOS", "_V410_H0DN_INSUMOS", "_V411_VERBATINS2"])
INS, INS10, VB = ns["_V411_H0DN_INSUMOS"], ns["_V410_H0DN_INSUMOS"], ns["_V411_VERBATINS2"]
D = r"C:\t\k411c\revisao_A\blobs"; os.makedirs(D, exist_ok=True)
tot = 0
for nome, ent in INS.items():
    if "reuso_v410" in ent: ent = INS10[ent["reuso_v410"]]
    p = os.path.join(D, nome); open(p, "wb").write(base64.b64decode(ent["b64"]))
    n = E.guarda_conta(p, priv); tot += (n or 0);
    print("  blob %-34s ocorrencias=%s" % (nome, n))
for k, v in VB.items():
    p = os.path.join(D, k + ".txt"); open(p, "wb").write(v["text"].encode("utf-8"))
    n = E.guarda_conta(p, priv); tot += (n or 0); print("  fala %-34s ocorrencias=%s" % (k, n))
# as linhas novas do candidato
diff = open(os.path.join(a_lib.OUT, "mydiff.diff"), "rb").read().decode("utf-8", "surrogateescape").split(chr(10))
novas = [ln[1:] for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
p = os.path.join(D, "linhas_novas.txt"); open(p, "wb").write((chr(10).join(novas)).encode("utf-8", "surrogateescape"))
n = E.guarda_conta(p, priv); tot += (n or 0); print("  linhas novas do candidato ocorrencias=%s (%d B)" % (n, os.path.getsize(p)))
p = os.path.join(a_lib.V, "TOPO_RATIFICADO_v411.json"); n = E.guarda_conta(p, priv); tot += (n or 0); print("  TOPO ocorrencias=%s" % n)
# o core do ensaio, so' os 3 registros novos
c = json.load(open(r"C:\t\k411c\falso_nos_v411\um_absoluto.json", encoding="utf-8"))["core"]
p = os.path.join(D, "registros_novos_core.json"); open(p, "w", encoding="utf-8").write(json.dumps({k: c[k] for k in ("h0dn_bg1_v411", "cunhagens_v411", "kh_n1_cobertura_v411")}, ensure_ascii=False))
n = E.guarda_conta(p, priv); tot += (n or 0); print("  3 registros novos do core ocorrencias=%s" % n)
print("TOTAL de ocorrencias:", tot)
