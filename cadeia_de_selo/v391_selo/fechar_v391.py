# -*- coding: utf-8 -*-
"""fechar_v391.py -- DEPOIS da cadeia pos-rito (molde: fechar_v390.py): (1) o manifesto de incorporacao v391 -> v391_selo e a pasta das ferramentas; (2) o ARQUIVO do
pacote e da cadeia -> work\\cadeia_de_selo\\v391 (+_selo); (3) o HANDOFF (memory\\handoff-v391-custodia.md + Nos\\HANDOFF_v391_CUSTODIA.md) para a sessao do site.
Guarda: a leitura sem problema. Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""
import os, sys, json, hashlib, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v391 as L
import textos_v391 as T
V, PROB = L.ler()
if PROB:
    print("FECHAR RECUSADO:", PROB); sys.exit(2)
PK = L.PK; NOS = L.NOS; WK = os.path.dirname(HERE)
OD = PK   # v391: o verbatim do operador mora no proprio pacote; nenhum kernel novo
TOOLS = os.path.join(WK, "cadeia_de_selo")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
ST = time.strftime("%Y%m%d_%H%M%S"); s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]; s64 = lambda b: hashlib.sha256(b).hexdigest()


def grava(p, b):
    if os.path.exists(p):
        if open(p, "rb").read() == b:
            print("  igual:", p); return
        raw = open(p, "rb").read(); bk = p + ".bak_" + ST + "_f391"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_f391_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b; print("  gravado:", p, len(b), "B")


ap, app = L._aplicado()
PKF = sorted(f for f in os.listdir(PK) if os.path.isfile(os.path.join(PK, f)) and f.endswith((".py", ".json", ".pysnip", ".sh", ".txt", ".out", ".diff")) and os.path.getsize(os.path.join(PK, f)) < 5 * 1024 * 1024)
m = {"stamp": ST, "versao": "v391", "instalacao": os.path.basename(app), "base_v390": V["base16"], "um_py_sha16": V["s16"], "um_py_bytes": V["umb"], "pacote": {f: s16(os.path.join(PK, f)) for f in PKF},
     "kernel": "nenhum kernel novo na v391", "patches": V["patches"], "teoremas": V["teor"],
     "rodada": V["compl"], "horarios": V["horarios"], "gate": V["qg"], "conferidor": {"deve_mudar": V["conf_dm"], "nao_pode_mudar": V["conf_np"], "json_sha16": V["conf16"], "servidor": V["servidor"]},
     "registros_v391": {k: V[k] for k in L.REG}, "estatuto": V["ep"], "verbatim": V["verbatim"], "fundacao_v390": V["fd390"], "pilar": V["pilar"],
     "ordem": {"OPERADOR_07out_estatuto_verbatim.txt": s16(os.path.join(PK, "OPERADOR_07out_estatuto_verbatim.txt"))},
     "artefatos_nos": {k: V["h_" + k] for k in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md")}, "artigos": V["artigos"]}
mb = json.dumps(m, ensure_ascii=False, indent=1, default=str).encode("utf-8")
print("(1) manifesto"); grava(os.path.join(HERE, "v391_incorporacao_manifesto.json"), mb); grava(os.path.join(TOOLS, "v391_incorporacao_manifesto.json"), mb)
arq = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "arquivos": {}, "nao_arquivado": {}}


def copia(src, dst):
    b = open(src, "rb").read(); os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not (os.path.exists(dst) and open(dst, "rb").read() == b):
        tmp = dst + ".tmp_f391"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, dst)
    arq["arquivos"][dst] = {"de": src, "bytes": len(b), "sha256": s64(b)}


print("(2) arquivo")
EXCL = (".pdf", ".tex", ".aux", ".toc", ".pyc", ".log")
for raiz, dirs, fs in os.walk(PK):
    dirs[:] = [d for d in dirs if not d.startswith(("dry_", "__pycache__", "pilar_anterior"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if f.endswith(EXCL) or ".bak_" in f or ".tmp" in f or f.startswith("."):
            continue
        if os.path.getsize(p) > 5 * 1024 * 1024:
            arq["nao_arquivado"][p] = "%d B (> 5 MB)" % os.path.getsize(p); continue
        copia(p, os.path.join(TOOLS, "v391", os.path.relpath(p, PK)))
for raiz, dirs, fs in os.walk(HERE):
    dirs[:] = [d for d in dirs if (raiz != HERE or d == "conferidor") and not d.startswith(("ensaio", "__pycache__"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if ".bak_" in f or ".tmp" in f or f.endswith(".pyc"):
            continue
        if raiz == HERE and not (f.endswith((".py", ".sh", "_out.txt", ".out")) or f in ("v391_incorporacao_manifesto.json",)):
            continue
        copia(p, os.path.join(TOOLS, "v391_selo", os.path.relpath(p, HERE)))
grava(os.path.join(TOOLS, "v391", "MANIFESTO_ARQUIVO_v391.json"), json.dumps(arq, ensure_ascii=False, indent=1).encode("utf-8"))
print("  arquivados: %d; fora (ditos): %d" % (len(arq["arquivos"]), len(arq["nao_arquivado"])))
doc = ("---\nname: handoff-v391-custodia\ndescription: \"HANDOFF v391 (%s) para a sessão do site: o estatuto da prova — provada (validade); a confirmação recusada é creditação; `%s`; custódia + README/site + pendências do operador\"\n"
       "metadata:\n  type: project\n---\n\n# HANDOFF v391 — CUSTÓDIA (%s)\n\n"
       "**O que é:** `um.py` **v391** `%s` (%s B) sobre a v390 `%s`; %s; COMPLETA; rc %s; selftest PASSED; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); pilar %s pela chave. "
       "Selo `%s`.\n\n**O que entrou e o que mediu:** %s.\n\n"
       "**Para a sessão do site (custódia):** o `um.py` v391, `rodada_v391_stdout.txt`, o selo, o core, o .md canônico e o manifesto, os artigos PT/EN (%s) e o verbatim do operador "
       "(`work\\v391_pacote\\OPERADOR_07out_estatuto_verbatim.txt`, sha16 `%s`) — com PORTA gerada por script; backup da versão no espelho, fora do repo; blob conferido; o um.py tem > 5 MB (a porta é o raw). "
       "O README e o site com o estatuto da prova foram preparados pela gerência c1 (sem subir; ver a memória `estatuto-da-prova-07out.md`). Commit/push = operador.\n\n"
       "**Pendências SÓ do operador:** vetar ou ratificar a v391; a custódia; subir o README e o site; commit/push. A Fase 9 (bandeiras do V1, executor D6) segue fora, decisão dele.\n\n"
       "Pacote `work\\v391_pacote`; cadeia `work\\v391_selo`; arquivo `work\\cadeia_de_selo\\v391` (+`_selo`). NOT_FALSIFIED nunca é confirmação; o gate não se move.\n\n"
       "[[missao-ultima-flag-um-py]] [[estatuto-da-prova-07out]] [[handoff-v390-custodia]]\n") % (
    V["data"], V["s16"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
    "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), V["selo_ts"], T._num(V), ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), str(V["verbatim"].get("sha256"))[:16])
assert "CONF" + "IRMED" not in doc.replace("NOT_CONF" + "IRMED", "")
print("(3) handoff")
grava(os.path.join(UMEM, "handoff-v391-custodia.md"), doc.encode("utf-8"))
grava(os.path.join(NOS, "HANDOFF_v391_CUSTODIA.md"), doc.split("---\n", 2)[2].lstrip("\n").encode("utf-8"))
print("FECHADO v391:", V["s16"], "| handoff", s16(os.path.join(UMEM, "handoff-v391-custodia.md")), "| Nos", s16(os.path.join(NOS, "HANDOFF_v391_CUSTODIA.md")))
