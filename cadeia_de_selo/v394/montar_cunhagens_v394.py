# -*- coding: utf-8 -*-
"""montar_cunhagens_v394.py -- reune as CUNHAGENS do operador de 14 a 19/10/2026 (levantamento §b.1 e §b.2, + as do lado c1) como arquivos DURAVEIS em insumos\\cunhagens (copia de BYTES, sha256 conferido contra o sha16 do
levantamento e contra o arquivo de origem) e escreve cunhagens_v394_dados.json (lido por registros_v394.py). Nada e' digitado: o texto de cada cunhagem e' o do arquivo. As 4 cunhagens de 14/10 que a v393 ja' embute
(acaeb291.., c37fccba.., 426b8ab0.., 7ce148ad..) ficam FORA (o registro cunhagens_regra_v393 as cobre). A definicao do Um absoluto e as falas de 17/10 do lado c1 saem da memoria da gerencia (posto-e-rank-10out.md)
por extracao de citacao entre « » com marcadores, num arquivo novo (insumos\\cunhagens\\UM_ABSOLUTO_17out_extraido_da_memoria.txt): ESTATUTO [DECLARADO] (original na sessao; a memoria o transcreve).
uso: python -I -B -X utf8 montar_cunhagens_v394.py"""
import hashlib, json, os, re, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
C = "C:" + os.sep
LEV = os.path.join(C, "IALD", "Central de Patentes", "work", "levantamento_chatgpt_19out", "LEVANTAMENTO_CHATGPT.md")
MEM = os.path.join(C, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "posto-e-rank-10out.md")
ACH = json.load(open(os.path.join(HERE, "scratch", "cunhagens_achadas.json"), encoding="utf-8"))
OUTD = os.path.join(HERE, "insumos", "cunhagens"); os.makedirs(OUTD, exist_ok=True)
sha256 = lambda b: hashlib.sha256(b).hexdigest()
JA_V393 = {"acaeb291cb41fa4e", "c37fccba3b7f1c89", "426b8ab01b5edf31", "7ce148ad0d814917"}
lev = open(LEV, encoding="utf-8").read()
b1 = lev.split("### b.1")[1].split("### b.2")[0]; b2 = lev.split("### b.2")[1].split("Nota: o PENDENCIAS")[0]
datas = {}
for line in b1.splitlines():
    m = re.match(r"\|\s*([^|]+?)\s*\|(.*)\|\s*`([0-9a-f]{16})`\s*\|", line)
    if m and not line.startswith("|---"):
        datas[m.group(3)] = m.group(1).strip()
# b.2: linhas por data
passo = {}
for line in b2.splitlines():
    m = re.match(r"^(\d{2}/\d{2}(?: e \d{2}/\d{2})?)(?: \([^)]*\))?:", line)
    if not m:
        m = re.match(r"^(\d{2}(?: e \d{2})?/\d{2}) \(", line)
    if m:
        dt = m.group(1)
        for s in re.findall(r"`([0-9a-f]{16})`", line):
            passo[s] = dt
        continue
    m = re.match(r"^(\d{2}/\d{2}[^:]*):", line)
    if m:
        for s in re.findall(r"`([0-9a-f]{16})`", line):
            passo[s] = m.group(1)
itens = []
for s16 in ACH["b1"] + ACH["b2"]:
    if s16 in JA_V393:
        continue
    srcs = ACH["achados"][s16]
    src = srcs[0]
    b = open(src, "rb").read()
    assert sha256(b)[:16] == s16, (s16, src)
    nome = "%s_%s" % (s16, os.path.basename(src))
    dst = os.path.join(OUTD, nome)
    if not os.path.exists(dst):
        open(dst + ".tmp", "wb").write(b); os.replace(dst + ".tmp", dst)
    assert open(dst, "rb").read() == b
    grupo = "conceitual" if s16 in ACH["b1"] else "conducao"
    quando = datas.get(s16) or passo.get(s16) or "?"
    t = b.decode("utf-8")
    itens.append({"sha16": s16, "grupo": grupo, "quando": quando, "arquivo": dst, "fonte_original": src, "sha256": sha256(b), "bytes": len(b), "text": t,
                  "multiplas_copias_na_origem": len(srcs)})
# --- o lado c1: a definicao do Um absoluto e as falas de 17/10 (memoria da gerencia), extracao por marcadores
mem = open(MEM, encoding="utf-8").read()
quotes = []


def pega(marca):
    # a linha da memoria que contem a marca; devolve (linha, [citacoes entre « »])
    for l in mem.splitlines():
        if marca in l:
            return l, re.findall(r"«([^»]+)»", l)
    raise SystemExit("marca nao achada na memoria: " + marca)


l30, q30 = pega("AO LADO (17/10/2026, cunhagem do operador, verbatim):")
l31, q31 = pega("CORREÇÃO AO LADO (17/10/2026, verbatim do operador)")
l32, q32 = pega("RATIFICADO (17/10/2026, operador:")
l33, q33 = pega("«expressão reflexiva do observador=leitura»")
l34, q34 = pega("FORMA FINAL (17/10/2026")
l35, q35 = pega("«Aqui também é a defasagem")
l38, q38 = pega("FECHADO (17/10/2026, operador:")
assert q30 and q31 and q32 and q33 and q34 and q35 and q38
linhas = ["# Falas do operador de 17/10/2026 (lado c1) sobre o Um absoluto, extraidas por script da memoria da gerencia posto-e-rank-10out.md, uma citacao entre « » por linha, na ordem do arquivo.",
          "# ESTATUTO: [DECLARADO] -- a memoria transcreve a fala; o original esta na sessao; nao ha arquivo de origem verbatim."]
rot = [("definicao_inicial", q30[0]), ("correcao_expressao_reflexiva", q31[0]), ("ratificacao", q32[0]), ("expressao_reflexiva_igual_leitura", q33[0]), ("forma_final", q34[0]), ("defasagem_igual_limite_assintotico", q35[0]), ("fechamento_da_mentira", q38[0])]
for k, q in rot:
    linhas.append("[%s] %s" % (k, q))
txt = "\n".join(linhas) + "\n"
dst = os.path.join(OUTD, "UM_ABSOLUTO_17out_extraido_da_memoria.txt")
open(dst + ".tmp", "w", encoding="utf-8", newline="\n").write(txt); os.replace(dst + ".tmp", dst)
b = open(dst, "rb").read()
itens.append({"sha16": sha256(b)[:16], "grupo": "conceitual_c1", "quando": "17/10", "arquivo": dst, "fonte_original": MEM + " (linhas com os marcadores citados; extracao por script)", "sha256": sha256(b), "bytes": len(b), "text": b.decode("utf-8"),
              "multiplas_copias_na_origem": 1, "declarado": True})
out = {"quando": "19/10/2026", "n": len(itens), "itens": itens, "ja_na_v393": sorted(JA_V393), "forma_final_um_absoluto": q34[0], "mem_sha256_na_extracao": sha256(open(MEM, "rb").read())}
json.dump(out, open(os.path.join(HERE, "cunhagens_v394_dados.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({"n": len(itens), "por_grupo": {g: sum(1 for i in itens if i["grupo"] == g) for g in sorted({i["grupo"] for i in itens})}, "sem_data": [i["sha16"] for i in itens if i["quando"] == "?"], "forma_final": q34[0]}, ensure_ascii=False))
