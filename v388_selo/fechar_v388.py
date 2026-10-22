# -*- coding: utf-8 -*-
"""fechar_v388.py -- DEPOIS da cadeia pos-rito (molde: fechar_v387.py): (1) o manifesto de incorporacao v388 -> v388_selo e a pasta das ferramentas; (2) o ARQUIVO do pacote,
do kernel (so os fontes e o log, nunca o .lake) e da cadeia -> work\\cadeia_de_selo\\v388 (+_selo, +_kernel); (3) o HANDOFF (memory\\handoff-v388-custodia.md + Nos\\HANDOFF_v388_CUSTODIA.md).
Guarda: a leitura sem problema. Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""
import os, sys, json, hashlib, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v388 as L
import textos_v388 as T
V, PROB = L.ler()
if PROB:
    print("FECHAR RECUSADO:", PROB); sys.exit(2)
PK = L.PK; NOS = L.NOS; KD = os.path.join(os.path.dirname(HERE), "v388_kernel")
TOOLS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "cadeia_de_selo")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
ST = time.strftime("%Y%m%d_%H%M%S"); s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]; s64 = lambda b: hashlib.sha256(b).hexdigest()


def grava(p, b):
    if os.path.exists(p):
        if open(p, "rb").read() == b:
            print("  igual:", p); return
        raw = open(p, "rb").read(); bk = p + ".bak_" + ST + "_f388"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_f388_" + ST; open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b; print("  gravado:", p, len(b), "B")


ap, app = L._aplicado()
PKF = sorted(f for f in os.listdir(PK) if os.path.isfile(os.path.join(PK, f)) and f.endswith((".py", ".json", ".pysnip", ".sh", ".txt", ".out")) and os.path.getsize(os.path.join(PK, f)) < 5 * 1024 * 1024)
m = {"stamp": ST, "versao": "v388", "instalacao": os.path.basename(app), "base_v387": V["base16"], "um_py_sha16": V["s16"], "um_py_bytes": V["umb"], "pacote": {f: s16(os.path.join(PK, f)) for f in PKF},
     "kernel": {"sandbox": os.path.join(KD, "kernel_src"), "pedra_sha16": V["pedra16"], "build_full_log_sha16": s16(os.path.join(KD, "build_full.log"))}, "patches": V["patches"], "teoremas": V["teor"],
     "rodada": V["compl"], "horarios": V["horarios"], "gate": V["qg"], "conferidor": {"deve_mudar": V["conf_dm"], "nao_pode_mudar": V["conf_np"], "json_sha16": V["conf16"], "servidor": V["servidor"]},
     "registros_v388": {k: V[k] for k in L.REG}, "beta_escalar": V["br"], "fase9": {"files": V["fase9_files"], "veredito": V["ho"].get("verdict_of_the_frozen_function"),
     "contrafactual_NAO_veredito": V["ho"].get("counterfactual_with_sources_NOT_a_verdict")}, "verbatins": V["verbatins"], "pilar": V["pilar"],
     "artefatos_nos": {k: V["h_" + k] for k in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md")}, "artigos": V["artigos"]}
mb = json.dumps(m, ensure_ascii=False, indent=1, default=str).encode("utf-8")
print("(1) manifesto"); grava(os.path.join(HERE, "v388_incorporacao_manifesto.json"), mb); grava(os.path.join(TOOLS, "v388_incorporacao_manifesto.json"), mb)
arq = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "arquivos": {}, "nao_arquivado": {}}


def copia(src, dst):
    b = open(src, "rb").read(); os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not (os.path.exists(dst) and open(dst, "rb").read() == b):
        tmp = dst + ".tmp_f388"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, dst)
    arq["arquivos"][dst] = {"de": src, "bytes": len(b), "sha256": s64(b)}


print("(2) arquivo")
EXCL = (".pdf", ".tex", ".aux", ".toc", ".pyc", ".log")
for raiz, dirs, fs in os.walk(PK):
    dirs[:] = [d for d in dirs if not d.startswith(("dry_", "__pycache__"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if f.endswith(EXCL) or ".bak_" in f or ".tmp" in f or f.startswith("."):
            continue
        if os.path.getsize(p) > 5 * 1024 * 1024:
            arq["nao_arquivado"][p] = "%d B (> 5 MB)" % os.path.getsize(p); continue
        copia(p, os.path.join(TOOLS, "v388", os.path.relpath(p, PK)))
for f in ("build_full.log", "AUDIT_NOMES_v388.txt", "TGLExt.lean.ANTES_v388", "Audit.lean.ANTES_v388"):
    p = os.path.join(KD, f)
    if os.path.getsize(p) <= 5 * 1024 * 1024:
        copia(p, os.path.join(TOOLS, "v388_kernel", f))
    else:
        arq["nao_arquivado"][p] = "%d B (> 5 MB)" % os.path.getsize(p)
copia(os.path.join(KD, "kernel_src", "TGLExt", "TheCouplingRunsBoundedBelow.lean"), os.path.join(TOOLS, "v388_kernel", "TheCouplingRunsBoundedBelow.lean"))
arq["nao_arquivado"][os.path.join(KD, "kernel_src")] = "o sandbox inteiro (13,9 GB com o .lake): fica em work\\v388_kernel, dito"
for raiz, dirs, fs in os.walk(HERE):
    dirs[:] = [d for d in dirs if (raiz != HERE or d == "conferidor") and not d.startswith(("ensaio", "__pycache__"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if ".bak_" in f or ".tmp" in f or f.endswith(".pyc"):
            continue
        if raiz == HERE and not (f.endswith((".py", ".sh", "_out.txt")) or f in ("v388_incorporacao_manifesto.json",)):
            continue
        copia(p, os.path.join(TOOLS, "v388_selo", os.path.relpath(p, HERE)))
grava(os.path.join(TOOLS, "v388", "MANIFESTO_ARQUIVO_v388.json"), json.dumps(arq, ensure_ascii=False, indent=1).encode("utf-8"))
print("  arquivados: %d; fora (ditos): %d" % (len(arq["arquivos"]), len(arq["nao_arquivado"])))
doc = ("---\nname: handoff-v388-custodia\ndescription: \"HANDOFF v388 (%s) para a sessão do site: β escalar ≥ β₀ tipado (a pedra TheCouplingRunsBoundedBelow); a Fase 9 aberta pela função congelada (INCONCLUSIVE, leitores declarados); `%s`; custódia + pendências do operador\"\n"
       "metadata:\n  type: project\n---\n\n# HANDOFF v388 — CUSTÓDIA (%s)\n\n"
       "**O que é:** `um.py` **v388** `%s` (%s B) sobre a v387 `%s`; %s; COMPLETA; rc %s; selftest PASSED; gate intocado; conferidor `%s` (deve mudar %s; não pode mudar %s); pilar %s pela chave. "
       "Selo `%s`.\n\n**O que entrou e o que mediu:** %s.\n\n"
       "**Para a sessão do site (custódia):** o `um.py` v388, `rodada_v388_stdout.txt`, os artigos PT/EN (%s), a pedra `TGLExt/TheCouplingRunsBoundedBelow.lean` (`%s`), e a subpasta "
       "`Bancada_Um\\investigacao\\fase9_hubble_abertura\\` (resultado da Fase 9, por hash: %s) com PORTA gerada por script; site + cofre + runner + os 16 dispositivos; commit/push = operador.\n\n"
       "**Pendências SÓ do operador:** fontes públicas da Fase 9 por sha256 (D-H) — mesmo com elas, z_disc < 5 sob este V1 (contrafactual dito); qual especificação da Fase 9 governa (o V1 da "
       "gerência × o rascunho do Codex, 283 componentes); qual μ cada rito usa (β(μ) [OPEN]); D1–D11 / D-A..D-H tomados por delegação (ratificar); nomes dos tokens; reiniciar o MCP "
       "`bancada-um`; commit/push. Nota de método: o sandbox Lean antigo perdeu os pacotes da Mathlib; a pedra foi compilada num sandbox novo `work\\v388_kernel\\kernel_src` (cópia de bytes do "
       "`tgl_kernel` do Nós, 13,9 GB), dito.\n\nPacote `work\\v388_pacote`; cadeia `work\\v388_selo`; arquivo `work\\cadeia_de_selo\\v388` (+`_selo`, +`_kernel`). NOT_FALSIFIED nunca é confirmação; "
       "a RG/ΛCDM é o limite clássico.\n\n[[missao-ultima-flag-um-py]] [[beta-escalar-limitado-inferiormente-06out]] [[fase9-razao-de-hubble-05out]] [[handoff-v387-custodia]]\n") % (
    V["data"], V["s16"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"],
    "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), V["selo_ts"], T._num(V), ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), V["pedra16"],
    ", ".join("%s `%s`" % (k, v[:16]) for k, v in V["fase9_files"].items()))
print("(3) handoff")
grava(os.path.join(UMEM, "handoff-v388-custodia.md"), doc.encode("utf-8"))
grava(os.path.join(NOS, "HANDOFF_v388_CUSTODIA.md"), doc.split("---\n", 2)[2].lstrip("\n").encode("utf-8"))
print("FECHADO v388:", V["s16"])
