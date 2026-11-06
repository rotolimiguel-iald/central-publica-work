# -*- coding: utf-8 -*-
"""Revisor terceiro v409 (R1): todo token hex de 16 ou 64 caracteres escrito nos textos/codigos NOVOS da v409 (pedras, pysnips, runtime, delta, registros, textos) e' o prefixo
do sha256 de algum arquivo real (universo: v409/**, v407/**, v405/**, cunhagens_13out, conjunto_D, pedras_candidatas_03nov, fechamento_02nov, Nos)? O que nao casa e' listado."""
import glob, hashlib, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
W = "C:/IALD/Central de Patentes/work/"
R = W + "cadeia_de_selo/v409/"
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/"
alvos = [R + f for f in ("DESENHO_v409.md", "RELATORIO_PREPARACAO_v409.md", "PLANO_v409.md", "RETOMADA_CONSTRUTOR_v409.md", "RETOMADA_CONSTRUTOR_v409_2.md", "DEPOSITO_CONSTRUTOR_v409.md", "pos_rito/CUSTODIA_v409_RASCUNHO.txt")]
rx = re.compile(r"(?<![0-9A-Za-z])([0-9a-f]{16}|[0-9a-f]{64})(?![0-9A-Za-z])")
tok = {}
for a in alvos:
    t = open(a, "rb").read().decode("utf-8", "replace")
    for m in rx.finditer(t):
        tok.setdefault(m.group(1), set()).add(os.path.basename(a))
print("tokens distintos:", len(tok))
# universo de arquivos
univ = []
for root in (R, W + "cadeia_de_selo/v408/", W + "cadeia_de_selo/v407/", W + "cadeia_de_selo/v406/", W + "cadeia_de_selo/v405/", W + "cunhagens_13out/", W + "pedras_candidatas_05nov/", W + "conjunto_D_20261029/parametrizacao_03nov/", W + "pedras_candidatas_03nov/", W + "fechamento_02nov/", NOS):
    for dp, dn, fn in os.walk(root):
        if any(x in dp for x in (".lake", "tgl_kernel", "__pycache__", "arvore_simulada_h8", "imp_a5df", "sim_a5df", "conferidor_import", "falso_nos", "dry_v40", "bateria_pre_selo", "bancada_B3", "/kernel/", "\\kernel\\")) and root != NOS: continue
        if "tgl_kernel" in dp: continue
        for f in fn:
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) <= 120 * 1024 * 1024: univ.append(p)
            except OSError: pass
print("arquivos no universo:", len(univ))
hs = {}
for p in univ:
    try:
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    except Exception: continue
    hs[h] = p
H16 = {h[:16]: p for h, p in hs.items()}
nao = []
for t, fs in sorted(tok.items()):
    achou = (t in hs) if len(t) == 64 else (t in H16 or any(h.startswith(t) for h in hs))
    if not achou: nao.append((t, sorted(fs)))
print("tokens sem arquivo correspondente no universo:", len(nao))
for t, fs in nao: print("  ", t, fs)
