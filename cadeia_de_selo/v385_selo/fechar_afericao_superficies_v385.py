# -*- coding: utf-8 -*-
"""Fecho da aferição das superfícies (v385): (1) copia ao arquivo da Central as saídas do script de erratas (REAL e SECO), que ele não podia copiar
enquanto as escrevia, e acrescenta-as ao manifesto-complemento (aditivo); (2) acrescenta à linha do HANDOFF v385 no MEMORY.md a marca da errata
(só acréscimo; backup de bytes; ≤ 24.000 B)."""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "cadeia_de_selo", "v385_selo")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
st = time.strftime("%Y%m%d_%H%M%S")
# (1) as saídas ao arquivo + manifesto-complemento
CM = os.path.join(ARQ, "MANIFESTO_ARQUIVO_v385_COMPLEMENTO.json")
comp = json.load(open(CM, encoding="utf-8"))
for fn in ("erratas_afericao_superficies_v385_REAL_out.txt", "erratas_afericao_superficies_v385_SECO_out.txt", os.path.basename(__file__)):
    src = os.path.join(HERE, fn); b = open(src, "rb").read(); h = hashlib.sha256(b).hexdigest()
    dst = os.path.join(ARQ, fn)
    if os.path.exists(dst) and open(dst, "rb").read() == b:
        print("igual", fn); continue
    open(dst + ".tmp", "wb").write(b); assert open(dst + ".tmp", "rb").read() == b; os.replace(dst + ".tmp", dst)
    comp["arquivos"]["v385_selo/" + fn] = {"sha256": h, "bytes": len(b), "estado": "copiado (fecho %s)" % st}
    print("OK arquivo", fn, len(b), "B")
open(CM + ".bak_" + st, "wb").write(open(CM, "rb").read())
json.dump(comp, open(CM + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(CM + ".tmp", CM)
print("manifesto-complemento:", len(comp["arquivos"]), "arquivos;", len(comp["fica_fora"]), "ficam fora")
# (2) MEMORY.md: a linha do HANDOFF v385 ganha a marca da errata (só acréscimo)
P = os.path.join(UMEM, "MEMORY.md"); raw0 = open(P, "rb").read()
MARCA = "errata ao lado da aferição das superfícies"
if MARCA.encode("utf-8") in raw0:
    print("JA ESTA MEMORY.md")
else:
    nl = b"\r\n" if raw0.count(b"\r\n") > raw0.count(b"\n") // 2 else b"\n"
    linhas = raw0.split(nl)
    idx = [i for i, l in enumerate(linhas) if l.startswith(b"- [HANDOFF v385")]
    assert len(idx) == 1, idx
    ad = (" · **05/10 13:20: %s no próprio handoff — V1.4 e os 5 geradores dos dois lados pendentes; sha16 v383 `58abcf20651f4777` repetido; mapa seq 349–351**" % MARCA).encode("utf-8")
    linhas[idx[0]] = linhas[idx[0]] + ad
    novo = nl.join(linhas)
    assert len(novo) <= 24000, len(novo)
    bak = P + ".bak_" + st + "_errata385"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo) > len(raw0); os.replace(P + ".tmp", P)
    # conferência: só a linha do handoff mudou, e só por acréscimo
    novas = open(P, "rb").read().split(nl); assert len(novas) == len(linhas)
    dif = [i for i in range(len(linhas)) if raw0.split(nl)[i] != novas[i]]; assert dif == idx, dif
    assert novas[idx[0]].startswith(raw0.split(nl)[idx[0]])
    print("OK MEMORY.md", len(raw0), "->", len(novo), "B (1 linha, só acréscimo)")
