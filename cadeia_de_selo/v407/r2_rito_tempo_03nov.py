# -*- coding: utf-8 -*-
"""03/11/2026 16:1x, gerencia c1 (R2): o comentario TEMPO ESPERADO do rito_v407.sh trazia os numeros do build R1 (379 s / 245 s; soma 295 s; maximo 35 s); o conferidor do instalar/rito exige
os numeros MEDIDOS do build corrente (kernel/construir_marcas.txt). Aqui os numeros sao LIDOS de construir_marcas.txt (build = epoch_build_fim - epoch_inicio; Audit = epoch_audit_fim -
epoch_build_fim) e de lake_build.log (soma e maximo dos «Built TGLExt.<modulo> (NNs)» dos 9 modulos), nunca digitados, e entram no lugar dos antigos por regex. Troca em bytes com backup;
`sh -n` depois. Escrito pelo Write."""
import os, re, time
V7 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v407"; TS = time.strftime("%Y%m%d_%H%M%S")
tm = open(os.path.join(V7, "kernel", "construir_marcas.txt"), encoding="utf-8").read()
mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", tm, re.M)}
build_s = mm["epoch_build_fim"] - mm["epoch_inicio"]; audit_s = mm["epoch_audit_fim"] - mm["epoch_build_fim"]
MODS = ("PsionCanto", "Par", "APonteDoAtrito", "OUmInscrito", "KEhATangente", "AChaveDaGuarda", "OGuarda", "LeituraPreservada", "OIgual")
log = open(os.path.join(V7, "kernel", "lake_build.log"), encoding="utf-8", errors="replace").read()
tempos = {}
for m_ in MODS:
    hits = re.findall(r"Built TGLExt\.%s \((\d+(?:\.\d+)?)(ms|s)\)" % re.escape(m_), log)
    assert len(hits) == 1, (m_, hits)
    v, u = hits[0]; tempos[m_] = float(v) / (1000.0 if u == "ms" else 1.0)
soma = int(round(sum(tempos.values()))); mx_mod = max(tempos, key=tempos.get); mx = int(round(tempos[mx_mod]))
novo_trecho = "= %d s e 1 Audit = %d s (a soma dos tempos por modulo e' %d s, o maximo de um modulo %d s, %s)" % (build_s, audit_s, soma, mx, mx_mod)
print("medido:", novo_trecho)
arq = os.path.join(V7, "rito_v407.sh"); b = open(arq, "rb").read(); s = b.decode("utf-8")
rx = re.compile(r"= \d+ s e 1 Audit = \d+ s \(a soma dos tempos por modulo e' \d+ s, o maximo de um modulo \d+ s, \w+\)")
achados = rx.findall(s); assert len(achados) == 1, achados
print("antes: ", achados[0])
novo = rx.sub(novo_trecho, s).encode("utf-8")
bak = arq + ".bak_r2_tempo_" + TS; open(bak, "xb").write(b); assert open(bak, "rb").read() == b
tmp = arq + ".tmp_" + TS; open(tmp, "xb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, arq); assert open(arq, "rb").read() == novo
assert b.count(b"\r\n") == novo.count(b"\r\n")
print("rito_v407.sh: %d -> %d B; backup %s" % (len(b), len(novo), os.path.basename(bak)))
