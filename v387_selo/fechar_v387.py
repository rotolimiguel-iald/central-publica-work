# -*- coding: utf-8 -*-
"""fechar_v387.py -- DEPOIS da cadeia pos-rito (moldes: manifesto_v386.py, arquivar_v386.py, handoff_v386.py, enxutos):
 (1) o MANIFESTO de incorporacao v387 (tudo LIDO: a instalacao, o pacote por sha256, a rodada) -> v387_selo e a pasta das ferramentas (o atlas_indice.py o carrega);
 (2) o ARQUIVO: o pacote (work\\v387_pacote, filtrado: sem candidatos > 5 MB, sem dry_*, sem PDFs/tex/aux/toc) e a cadeia v387_selo (lista permitida: *.py, *.sh,
     *_out.txt, o manifesto, o JSON do mapa, o conferidor) -> work\\cadeia_de_selo\\v387 e \\v387_selo; copia byte a byte conferida; MANIFESTO_ARQUIVO_v387.json;
 (3) o HANDOFF: a memoria-topico `handoff-v387-custodia.md` + `Nos\\HANDOFF_v387_CUSTODIA.md` (a linha do indice ja entrou pelas superficies).
Guarda: a leitura sem problema. Backup de bytes se o alvo existir; temporario -> conferir -> substituir; nunca apaga. Idempotente."""
import os, sys, json, hashlib, time, shutil
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v387 as L
import textos_v387 as T
V, PROB = L.ler()
if PROB:
    print("FECHAR RECUSADO:", PROB); sys.exit(2)
PK = L.PK; NOS = L.NOS
TOOLS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "cadeia_de_selo")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
ST = time.strftime("%Y%m%d_%H%M%S")
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
s64 = lambda b: hashlib.sha256(b).hexdigest()


def grava(p, b):
    if os.path.exists(p):
        if open(p, "rb").read() == b:
            print("  igual (idempotente):", p); return
        bk = p + ".bak_" + ST + "_f387"; raw = open(p, "rb").read(); open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_f387_" + ST
    open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, "rb").read() == b
    print("  gravado:", p, len(b), "B")


# (1) o manifesto
ap, app = L._aplicado()
PKF = sorted(f for f in os.listdir(PK) if os.path.isfile(os.path.join(PK, f)) and f.endswith((".py", ".json", ".pysnip", ".sh", ".txt", ".out")) and os.path.getsize(os.path.join(PK, f)) < 5 * 1024 * 1024)
m = {"stamp": ST, "versao": "v387", "instalacao": os.path.basename(app), "instalado_em": ap["ts"], "base_v386": V["base16"], "um_py_sha16": V["s16"], "um_py_bytes": V["umb"],
     "pacote": {f: s16(os.path.join(PK, f)) for f in PKF}, "patches": V["patches"], "teoremas": V["teor"], "rodada": V["compl"], "horarios": V["horarios"], "gate": V["qg"], "n18": V["n18"],
     "conferidor": {"deve_mudar": V["conf_dm"], "nao_pode_mudar": V["conf_np"], "json_sha16": V["conf16"], "servidor_depois_do_rito": V["servidor"]},
     "vereditos_v386_inalterados": "%d/%d" % (V["n_ver"] - V["n_ver_mudaram"], V["n_ver"]),
     "registros_v387": {k: V[k] for k in L.REG}, "tres_testes": {"contagens": V["tt"], "kernel": V["tt_kernel"], "gpu": V["tt_gpu"], "livro": V["tt_ledger"], "conjunta": V["tt_joint"]},
     "V1": V["V1"], "verbatins": V["verbatins"], "retrodicao": V["retro_sites"], "pilar": V["pilar"],
     "artefatos_nos": {k: V["h_" + k] for k in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md")}, "artigos": V["artigos"],
     "funcoes": list(L.REG), "target": os.path.join(NOS, "um.py")}
mb = json.dumps(m, ensure_ascii=False, indent=1, default=str).encode("utf-8")
print("(1) manifesto"); grava(os.path.join(HERE, "v387_incorporacao_manifesto.json"), mb); grava(os.path.join(TOOLS, "v387_incorporacao_manifesto.json"), mb)
# (2) o arquivo
D1 = os.path.join(TOOLS, "v387"); D2 = os.path.join(TOOLS, "v387_selo"); os.makedirs(D1, exist_ok=True); os.makedirs(D2, exist_ok=True)
EXCL = (".pdf", ".tex", ".aux", ".toc", ".pyc", ".log")
arq = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "arquivos": {}, "nao_arquivado": {}}


def copia(src, dst):
    b = open(src, "rb").read()
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not (os.path.exists(dst) and open(dst, "rb").read() == b):
        tmp = dst + ".tmp_f387"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, dst)
    assert open(dst, "rb").read() == b
    arq["arquivos"][dst] = {"de": src, "bytes": len(b), "sha256": s64(b)}


print("(2) arquivo")
for raiz, dirs, fs in os.walk(PK):
    dirs[:] = [d for d in dirs if not d.startswith(("dry_", "__pycache__"))]
    for d in os.listdir(raiz):
        if d.startswith("dry_") and os.path.isdir(os.path.join(raiz, d)):
            arq["nao_arquivado"][os.path.join(raiz, d)] = "o ensaio a seco (kernel materializado, PDFs): fica no pacote, dito"
    for f in fs:
        p = os.path.join(raiz, f)
        if f.endswith(EXCL) or ".bak_" in f or ".tmp" in f or f.startswith("."):
            continue
        if os.path.getsize(p) > 5 * 1024 * 1024:
            arq["nao_arquivado"][p] = "%d B (> 5 MB; o candidato fica no pacote e o canonico no Nos, por sha256)" % os.path.getsize(p); continue
        copia(p, os.path.join(D1, os.path.relpath(p, PK)))
for raiz, dirs, fs in os.walk(HERE):
    dirs[:] = [d for d in dirs if d in ("conferidor",) or raiz != HERE]
    dirs[:] = [d for d in dirs if not d.startswith(("ensaio", "__pycache__"))]
    for f in fs:
        p = os.path.join(raiz, f)
        if ".bak_" in f or ".tmp" in f or f.endswith(".pyc"):
            continue
        if raiz == HERE and not (f.endswith((".py", ".sh", "_out.txt")) or f in ("v387_incorporacao_manifesto.json", "registro_mapa_v387.json")):
            continue
        copia(p, os.path.join(D2, os.path.relpath(p, HERE)))
mp = os.path.join(D1, "MANIFESTO_ARQUIVO_v387.json")
grava(mp, json.dumps(arq, ensure_ascii=False, indent=1).encode("utf-8"))
print("  arquivados: %d; fora (ditos): %d" % (len(arq["arquivos"]), len(arq["nao_arquivado"])))
# (3) o handoff
h = V["hr_tr"]; p8 = V["pr_tr"]
doc = ("---\nname: handoff-v387-custodia\ndescription: \"HANDOFF v387 (%s) para a sessão do site: os três testes conjuntos; as Fases 9 e 8 pré-registradas por hash (nada aberto); retrodição sem ajuste; `%s`; custódia + pendências do operador\"\n"
       "metadata:\n  type: project\n---\n\n"
       "# HANDOFF v387 — CUSTÓDIA (%s)\n\n"
       "**O que é:** `um.py` **v387** `%s` (%s B) sobre a v386 `%s`; %s; COMPLETA; rc %s; selftest PASSED; gate intocado (18/18); conferidor `%s` (deve mudar %s; não pode mudar %s); %d/%d vereditos "
       "da v386 inalterados; o pilar %s pela chave (resultado `%s`). Selo `%s`.\n\n"
       "**O que entrou:** %s.\n\n**Os V1 lidos por hash (nada aberto):** %s.\n\n"
       "**Para a sessão do site (custódia):** levar ao espelho `the_boundary` o `um.py` v387, os stdout `rodada_v387_stdout.txt`, os artigos PT/EN (%s) e as DUAS subpastas novas de "
       "pré-registro com PORTA gerada por script: `%s` e `%s` (somente-leitura; conferir cada sha256 contra o `V1_*_HASHES.json`); site + cofre + runner + os 16 dispositivos pela regra "
       "de cada custódia; commit/push = operador.\n\n"
       "**Pendências SÓ do operador:** (1) Fase 9: baixar as fontes públicas com sha256 (D-H) e dar a palavra para abrir o composto (até lá, abrir = INCONCLUSIVE_SYSTEMATICS, dito no V1); "
       "(2) Fase 8: fontes por sha256 (D8) e, se quiser o mapa C exato, o código de BBN (D5b); (3) os nomes finais dos tokens (D-J, inclusive o do Coma `…NOT_BLIND_UNADJUSTED_POSTDICTION…`); "
       "(4) reiniciar o MCP `bancada-um` (a ferramenta `neff_canal`); (5) commit/push. **Da gerência, ainda:** o passo D (auditar as entregas do Codex em `DO_CHATGPT\\ORDEM_018\\`); "
       "F6 da Fase 8 (`#print axioms` do trio citado).\n\n"
       "**A decisão de selar (06/10):** o operador, comandando pessoalmente a sessão c1, decidiu SELAR a v387 como está; o β escalar limitado inferiormente "
       "(`beta-escalar-limitado-inferiormente-06out.md`) entra na **v388** (dados examinados no mapa, seq 638: o Teorema da Escala já selado no artigo, um.py:165351; "
       "β(M_Z) = 0,012786 on-shell × 0,012886 MS-bar; patentes com β variável não localizadas nos arquivos).\n\n"
       "**Pendências do operador (anotadas a pedido da c1):** fontes públicas por sha256 (Fase 9 D-H; Fase 8 D8); QUAL especificação da Fase 9 governa (o V1 congelado "
       "`d956c8db…`, leitores-resumo, × o rascunho do Codex V01+JAGB, 283 componentes, em construção); D1–D11 (Fase 8) e D-A..D-H (Fase 9) foram tomados pelo PADRÃO por "
       "delegação — ratificar ou não (o Codex os lê como «sem aceite»); nomes finais dos tokens (inclusive o do Coma); reiniciar o MCP `bancada-um`; β escalar → v388; "
       "a errata P4/P5 da Lei da Prova (feita ao lado no CLAUDE.md global por ordem dele, via c1).\n\n"
       "**Ao lado — obrigações do runner R0 (aferição adversarial de 06/10, A1–A3; os V1 congelados NÃO se reescrevem):** Fase 9: o gatilho FALSIFIED de leitor único "
       "(σ_i ≤ 1,0) hoje não alcança nenhum leitor do composto (o menor σ é 1,04, R22) — dito, não corrigido; a referência da dispersão χ²_int/(n−1) e a ordem regra 1 "
       "(β-livre no limite do prior) × FALSIFIED têm de ser fixadas no runner hasheado ANTES de abrir; Fase 8: as «DUAS análises independentes» do gatilho FALSIFIED têm de ser "
       "enumeradas no runner (as cinco listadas partilham Planck). Mudar a regra = V1.x com gerador novo.\n\n"
       "Pacote `work\\v387_pacote`; cadeia `work\\v387_selo`; arquivo `work\\cadeia_de_selo\\v387` (+`_selo`). NOT_FALSIFIED nunca é confirmação; a RG/ΛCDM é o limite clássico.\n\n"
       "[[missao-ultima-flag-um-py]] [[fase9-razao-de-hubble-05out]] [[fase8-universo-primordial-05out]] [[tres-testes-de-estresse-conjuntos-05out]] [[pos-dicao-nao-e-prova-diabolica-05out]] [[handoff-v386-custodia]]\n") % (
    V["data"], V["s16"], V["data"], V["s16"], format(V["umb"], ","), V["base16"], V["teor"], V["rc"], V["conf16"], V["conf_dm"], V["conf_np"], V["n_ver"] - V["n_ver_mudaram"], V["n_ver"],
    "reaproveitado" if V["pilar"]["mode"] == "REUSE" else str(V["pilar"]["mode"]), V["pilar"]["result16"], V["selo_ts"], T._num(V), T._v1(V),
    ", ".join("%s `%s`" % kv for kv in V["artigos"].items()), V["V1"]["fase9"]["pasta"], V["V1"]["fase8"]["pasta"])
print("(3) handoff")
grava(os.path.join(UMEM, "handoff-v387-custodia.md"), doc.encode("utf-8"))
grava(os.path.join(NOS, "HANDOFF_v387_CUSTODIA.md"), doc.split("---\n", 2)[2].lstrip("\n").encode("utf-8"))
print("FECHADO v387:", V["s16"])
