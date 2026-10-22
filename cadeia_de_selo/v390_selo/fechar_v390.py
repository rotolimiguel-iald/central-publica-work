# -*- coding: utf-8 -*-
"""fechar_v390.py -- DEPOIS da cadeia pos-rito (molde: fechar_v388.py): (1) o manifesto de incorporacao v390 -> v390_selo e a pasta das ferramentas; (2) o ARQUIVO do pacote,
do kernel (so os fontes e o log, nunca o .lake), da pasta da ordem e da cadeia -> work\\cadeia_de_selo\\v390 (+_selo, +_kernel, +_ordem); (3) o HANDOFF (memory\\handoff-v390-custodia.md +
Nos\\HANDOFF_v390_CUSTODIA.md) para a sessao do site. Guarda: a leitura sem problema. Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""
import os, sys, json, hashlib, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v390 as L
import textos_v390 as T
V, PROB = L.ler()
if PROB:
    print("FECHAR RECUSADO:", PROB); sys.exit(2)
PK = L.PK; NOS = L.NOS; WK = os.path.dirname(HERE)
KD = os.path.join(WK, "v390_kernel"); KS = os.path.join(WK, "v388_kernel", "kernel_src"); OD = os.path.join(WK, "superposicao_passagem_07out")
TOOLS = os.path.join(WK, "cadeia_de_selo")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
ST = time.strftime("%Y%m%d_%H%M%S"); s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]; s64 = lambda b: hashlib.sha256(b).hexdigest()


def grava(p, b):
    if os.path.exists(p):
        if open(p, "rb").read() == b:
            print("  igual:", p); return
        raw = open(p, "rb").read(); bk = p + ".bak_" + ST + "_f390"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_f390_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b; print("  gravado:", p, len(b), "B")


ap, app = L._aplicado()
PKF = sorted(f for f in os.listdir(PK) if os.path.isfile(os.path.join(PK, f)) and f.endswith((".py", ".json", ".pysnip", ".sh", ".txt", ".out", ".diff")) and os.path.getsize(os.path.join(PK, f)) < 5 * 1024 * 1024)
m = {"stamp": ST, "versao": "v390", "instalacao": os.path.basename(app), "base_v389": V["base16"], "um_py_sha16": V["s16"], "um_py_bytes": V["umb"], "pacote": {f: s16(os.path.join(PK, f)) for f in PKF},
     "kernel": {"sandbox": KS, "pedra_sha16": V["pedra16"], "build_full_log_sha16": s16(os.path.join(KD, "build_full.log"))}, "patches": V["patches"], "teoremas": V["teor"],
     "rodada": V["compl"], "horarios": V["horarios"], "gate": V["qg"], "conferidor": {"deve_mudar": V["conf_dm"], "nao_pode_mudar": V["conf_np"], "json_sha16": V["conf16"], "servidor": V["servidor"]},
     "registros_v390": {k: V[k] for k in L.REG}, "fundacao": V["fd"], "verbatins": V["verbatins"], "ledger": V["ledger"], "pilar": V["pilar"],
     "ordem": {f: s16(os.path.join(OD, f)) for f in sorted(os.listdir(OD)) if os.path.isfile(os.path.join(OD, f))},
     "artefatos_nos": {k: V["h_" + k] for k in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md")}, "artigos": V["artigos"]}
mb = json.dumps(m, ensure_ascii=False, indent=1, default=str).encode("utf-8")
print("(1) manifesto"); grava(os.path.join(HERE, "v390_incorporacao_manifesto.json"), mb); grava(os.path.join(TOOLS, "v390_incorporacao_manifesto.json"), mb)
arq = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "arquivos": {}, "nao_arquivado": {}}


def copia(src, dst):
    b = open(src, "rb").read(); os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not (os.path.exists(dst) and open(dst, "rb").read() == b):
        tmp = dst + ".tmp_f390"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, dst)
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
        copia(p, os.path.join(TOOLS, "v390", os.path.relpath(p, PK)))
for f in sorted(os.listdir(KD)):
    p = os.path.join(KD, f)
    if os.path.isfile(p) and ".tmp" not in f:
        if os.path.getsize(p) <= 5 * 1024 * 1024:
            copia(p, os.path.join(TOOLS, "v390_kernel", f))
        else:
            arq["nao_arquivado"][p] = "%d B (> 5 MB)" % os.path.getsize(p)
copia(os.path.join(KS, "TGLExt", "Fundacao.lean"), os.path.join(TOOLS, "v390_kernel", "Fundacao.lean"))
arq["nao_arquivado"][KS] = "o sandbox inteiro (com o .lake): fica em work\\v388_kernel\\kernel_src, dito"
for f in sorted(os.listdir(OD)):
    if os.path.isfile(os.path.join(OD, f)):
        copia(os.path.join(OD, f), os.path.join(TOOLS, "v390_ordem", f))
for raiz, dirs, fs in os.walk(HERE):
    dirs[:] = [d for d in dirs if (raiz != HERE or d == "conferidor") and not d.startswith(("ensaio", "__pycache__"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if ".bak_" in f or ".tmp" in f or f.endswith(".pyc"):
            continue
        if raiz == HERE and not (f.endswith((".py", ".sh", "_out.txt", ".out")) or f in ("v390_incorporacao_manifesto.json",)):
            continue
        copia(p, os.path.join(TOOLS, "v390_selo", os.path.relpath(p, HERE)))
grava(os.path.join(TOOLS, "v390", "MANIFESTO_ARQUIVO_v390.json"), json.dumps(arq, ensure_ascii=False, indent=1).encode("utf-8"))
print("  arquivados: %d; fora (ditos): %d" % (len(arq["arquivos"]), len(arq["nao_arquivado"])))
stone_nos = os.path.join(NOS, "tgl_kernel", "TGLExt", "Fundacao.lean")
doc = ("---\nname: handoff-v390-custodia\ndescription: \"HANDOFF v390 (%s) para a sessão do site: a Fundação (TGLExt.Fundacao; a cláusula Ágape) — o GLOBAL_LIFT lido como a superposição, fecho LÓGICO; `%s`; custódia + pendências do operador\"\n"
       "metadata:\n  type: project\n---\n\n# HANDOFF v390 — CUSTÓDIA (%s)\n\n"
       "**O que é:** `um.py` **v390** `%s` (%s B) sobre a v389 `%s`; %s; COMPLETA; rc %s; selftest PASSED; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); pilar %s pela chave. "
       "Selo `%s`.\n\n**O que entrou e o que mediu:** %s.\n\n"
       "**Para a sessão do site (custódia):** somar à custódia conjunta v383→v389 (`handoff-custodia-conjunta-v383-v389-06out.md`, onde cada arquivo já tem o estado no espelho): o `um.py` v390, "
       "`rodada_v390_stdout.txt`, o selo, o core, o .md canônico e o manifesto, os artigos PT/EN (%s), a pedra `TGLExt/Fundacao.lean` (`%s`) com as costuras `TGLExt.lean` e `TGL/Audit.lean`, e a pasta da "
       "ordem `work\\superposicao_passagem_07out\\` (os dois verbatins do operador por sha256: `%s`, `%s`; a ordem; a pedra) — com PORTA gerada por script. Backup da versão que está no espelho, fora do repo; "
       "blob conferido; o um.py tem > 5 MB (a porta é o raw). Site + cofre + runner + os 16 dispositivos: a camada v390 (a Fundação; o GLOBAL_LIFT com fecho lógico). Commit/push = operador.\n\n"
       "**Pendências SÓ do operador:** vetar ou ratificar a v390 (o fecho LÓGICO: definição + recusa provada + passagem local [KNOWN]); a custódia; commit/push. A Fase 9 (bandeiras do V1, executor D6) "
       "ficou FORA desta versão, por ordem. Nota de método: o pino do ledger da v389 foi recontado (%s; a pedra nova entra no ledger), errata ao lado; o desenho do registro da v388 foi consertado "
       "(a leitura do disco da memória viva fora de qualquer veredito).\n\nPacote `work\\v390_pacote`; kernel `work\\v390_kernel` (sandbox `work\\v388_kernel\\kernel_src`); cadeia `work\\v390_selo`; arquivo "
       "`work\\cadeia_de_selo\\v390` (+`_selo`, +`_kernel`, +`_ordem`). NOT_FALSIFIED nunca é confirmação; a RG/ΛCDM é o limite clássico; o gate não se move.\n\n"
       "[[missao-ultima-flag-um-py]] [[superposicao-e-a-passagem-07out]] [[o-fechamento-lema3-impossiveis]] [[handoff-custodia-conjunta-v383-v389-06out]]\n") % (
    V["data"], V["s16"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
    "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), V["selo_ts"], T._num(V), ", ".join("%s `%s`" % kv for kv in V["artigos"].items()),
    s16(stone_nos) if os.path.exists(stone_nos) else V["pedra16"], V["verbatins"]["cunhagem_07out"]["sha256"][:16], V["verbatins"]["nomes_07out"]["sha256"][:16], V["ledger"])
assert "CONF" + "IRMED" not in doc.replace("NOT_CONF" + "IRMED", "")
print("(3) handoff")
grava(os.path.join(UMEM, "handoff-v390-custodia.md"), doc.encode("utf-8"))
grava(os.path.join(NOS, "HANDOFF_v390_CUSTODIA.md"), doc.split("---\n", 2)[2].lstrip("\n").encode("utf-8"))
print("FECHADO v390:", V["s16"], "| handoff", s16(os.path.join(UMEM, "handoff-v390-custodia.md")), "| Nos", s16(os.path.join(NOS, "HANDOFF_v390_CUSTODIA.md")))
