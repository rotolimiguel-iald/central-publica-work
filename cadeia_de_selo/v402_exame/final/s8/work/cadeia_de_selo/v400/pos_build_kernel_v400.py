# -*- coding: utf-8 -*-
"""pos_build_kernel_v400.py -- DEPOIS de construir_kernel_v400.sh (o Audit do sandbox C:\\t\\k400c\\final, copia do kernel da v399; NENHUM modulo novo): (1) monta kernel/build_full.log no formato do molde; (2) confere o build (rc, zero erro, zero sorry nas
formas do contrato R3.2, 'Build completed successfully', linha Built/Replayed da pedra Testemunho, e Built da raiz e do Audit, axiomas no trio, cabecalho dos .olean = Lean 4.31.0); (3) le do log do Audit (SO' dele) as linhas TGL_DECL_SOURCE e o axiom_report EFETIVO
com as funcoes do PROPRIO um.py v399 selado (extraidas por ast) e CONFERE que ele e a proveniencia sao IGUAIS aos do core v399 selado (o kernel da v400 e' o da v399); (4) refaz a ARVORE so-fontes C:\\t\\k400c\\arvore e varre os tokens proibidos RECURSIVAMENTE;
(5) mede os criterios do B(n) CONTRA O KERNEL QUE A BANCADA PINA (a v398: o ANTES do recibo e' o da v398, lido de v399\\base_v398, copia de bytes): o diff v398 -> v400 e' o diff v398 -> v399 (a pedra Testemunho), e o recibo da v400 tem de dizer o MESMO que o da v399;
(6) escreve KERNEL_RECIBO_v400.json (contrato KERNEL_RECIBO_R3_2, versao v400), vinculo/CRITERIOS_v400.json e POS_BUILD_v400.json. NAO escreve FLAGS (nenhuma bandeira nova) nem KH_N1 (o spec kh_n1_cobertura_v399 segue lendo o KH_N1_v399.json da v399).
Molde: pos_build_kernel_v399.py.   Uso: python -I -B -X utf8 pos_build_kernel_v400.py"""
import ast, datetime, hashlib, json, os, re, shutil, subprocess, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX; ARV = DL.ARVORE
B9 = os.path.join(HERE, DL.BASE_DIR)            # a v399 SELADA (o kernel que a v400 tem)
B8 = DL.V399_BASE98                              # a v398 SELADA (o kernel que a Bancada pina): copias de bytes da cadeia v399
TRIO = DL.TRIO_SET
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read()
abs_fw = lambda p: p.replace(os.sep, "/")
sinais = []


def chk(nome, cond, det=None):
    sinais.append({"checagem": nome, "ok": bool(cond), "detalhe": det}); print(("OK   " if cond else "FALHA"), nome, "" if det is None else "-> " + str(det)[:240])
    return bool(cond)


def norm(t):
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    t = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", t)
    return "".join(ch for ch in unicodedata.normalize("NFKC", t) if unicodedata.category(ch) != "Cf")


um9_src = rd(os.path.join(B9, "um.py")).decode("utf-8"); tree9 = ast.parse(um9_src)
fn = {n.name: n for n in tree9.body if isinstance(n, ast.FunctionDef)}
_ns = {"re": re}
for nome in ("parse_lean_provenance_v394", "parse_lean_axioms_v394"):
    exec(compile(ast.get_source_segment(um9_src, fn[nome]), "<base_v399:%s>" % nome, "exec"), _ns)
parse_ax, parse_src = _ns["parse_lean_axioms_v394"], _ns["parse_lean_provenance_v394"]
um8_src = rd(os.path.join(B8, "um.py")).decode("utf-8"); tree8 = ast.parse(um8_src)
nov = DL.STONE_RELS_DESDE_B8                     # as pedras que a Bancada (v398) nunca viu
assert json.load(open(os.path.join(HERE, "kernel_modulos_novos_v400.json"), encoding="utf-8"))["pedras_desde_a_bancada"] == nov, "rode preparar_kernel_v400.py"
NEWMODS = {p[:-len(".lean")].replace("/", ".") for p in nov}
core9 = json.load(open(os.path.join(B9, "um_absoluto.json"), encoding="utf-8"))["core"]; kf9 = core9["kernel_formalization"]; axr9 = kf9["axiom_report"]
core8 = json.load(open(os.path.join(B8, "um_absoluto.json"), encoding="utf-8"))["core"]; axr0 = core8["kernel_formalization"]["axiom_report"]; cov0 = core8["kernel_formalization"].get("axiom_coverage_v392") or {}
E0 = int(core8["external_ladder"]["n_theorems_expected"])
R9 = json.load(open(os.path.join(DL.V399, "kernel", "KERNEL_RECIBO_v399.json"), encoding="utf-8"))     # o recibo da v399: o da v400 tem de dizer o mesmo do kernel

RE_SORRY = re.compile(r"declaration\s+uses\s*[`'\u2018\u201c\"]sorry|\bsorryAx\b", re.I)
LB = norm(rd(os.path.join(KD, "lake_build.log")).decode("utf-8")); AL = norm(rd(os.path.join(KD, "audit.log")).decode("utf-8"))
AL_RAW = rd(os.path.join(KD, "audit.log")).decode("utf-8")
marcas = open(os.path.join(KD, "construir_marcas.txt"), encoding="utf-8").read()
rb = int(re.search(r"rc_build=(\d+)", marcas).group(1)); ra = int(re.search(r"rc_audit=(\d+)", marcas).group(1))
ini = re.search(r"^inicio (.*)$", marcas, re.M).group(1); fim = re.search(r"^fim (.*)$", marcas, re.M).group(1)
chk("rc do lake build == 0 e rc do Audit == 0", rb == 0 and ra == 0, [rb, ra])
n_err = len(re.findall(r"(?m)^error:|: error:", LB + "\n" + AL)); n_sorry = len(RE_SORRY.findall(LB + "\n" + AL)) + len(RE_SORRY.findall(re.sub(r"\s+", " ", LB + "\n" + AL)))
chk("zero erro; zero sorry/sorryAx (formas: crase, aspas, sorryAx; com e sem quebra)", n_err == 0 and n_sorry == 0, [n_err, n_sorry])
RE_JOB = re.compile(r"(?m)^[^\[\n]*\[\d+/\d+\][ \t]+(?:Built|Replayed)[ \t]+([^\s(]+)")
jobs = set(RE_JOB.findall(LB)); exig = ["TGLExt", "TGL.Audit"] + sorted(NEWMODS)
chk("linha Built/Replayed da pedra (Testemunho), da raiz (TGLExt) e do Audit (TGL.Audit)", all(m in jobs for m in exig), [m for m in exig if m not in jobs][:5])
chk("'Build completed successfully'", bool(re.search(r"(?m)^[ \t]*Build completed successfully\b", LB)), re.findall(r"Build completed successfully[^\n]*", LB))
built_raiz = bool(re.search(r"Built\s+TGLExt\b", LB)); built_audit = bool(re.search(r"Built\s+TGL\.Audit\b", LB))
chk("a raiz e o Audit foram COMPILADOS neste build (linha Built: construir_kernel_v400.sh apaga os artefatos dos dois para forca-los)", built_raiz and built_audit, [built_raiz, built_audit])
modo_pedra = {m: ("Built" if re.search(r"Built\s+" + re.escape(m) + r"\b", LB) else "Replayed" if re.search(r"Replayed\s+" + re.escape(m) + r"\b", LB) else None) for m in sorted(NEWMODS)}
print("INFO: o modulo de cada pedra neste build:", modo_pedra, "(Replayed = a pedra ja' estava compilada na copia do sandbox da v399)")
LIBL = os.path.join(KB, ".lake", "build", "lib", "lean")
hdr = {}
for m in sorted(NEWMODS) + ["TGLExt", "TGL.Audit"]:
    p = os.path.join(LIBL, *m.split(".")) + ".olean"
    h = rd(p)[:96] if os.path.exists(p) else b""
    hdr[m] = (h[:5] == b"olean" and b"4.31.0" in h[:40], re.search(rb"[0-9a-f]{40}", h).group(0).decode() if re.search(rb"[0-9a-f]{40}", h) else None)
hashes_lean = sorted({v[1] for v in hdr.values()})
chk("cabecalho de TODO .olean (pedra + raiz + Audit): magic 'olean' e versao 4.31.0; um unico githash do Lean", all(v[0] for v in hdr.values()) and len(hashes_lean) == 1, [len(hdr), hashes_lean])
# --- o log do Audit: leitura SO' dele (licao KH-N1) com as funcoes do um.py v399 selado
ax = parse_ax(AL_RAW); src = parse_src(AL_RAW)
chk("parse_lean_axioms_v394 e parse_lean_provenance_v394 sobre o log do Audit: sem erro", ax["ok"] and src["ok"], [ax["errors"][:3], src["errors"][:3]])
axm, srcm = ax["axioms"], src["sources"]
fora = {k: v for k, v in axm.items() if not set(v) <= TRIO}
chk("todo axioma lido no log do Audit esta no trio", not fora and len(axm) > 0, [len(axm), list(fora)[:3]])
chk("a palavra sorryAx NAO aparece no log do Audit (nem no lake build)", ("sorryAx" not in AL) and ("sorryAx" not in LB), [AL.count("sorryAx"), LB.count("sorryAx")])
m_cov = re.search(r"TGL_AXIOM_COVERAGE_TOTAL decl=(\d+) thm=(\d+) fora_do_trio=(\d+)", AL)
kh_cov = [int(x) for x in m_cov.groups()] if m_cov else None
chk("KH-N1: linha TGL_AXIOM_COVERAGE_TOTAL presente, fora_do_trio=0", bool(m_cov) and kh_cov[2] == 0, kh_cov)
chk("KH-N1: uma linha de axiomas e uma de proveniencia por constante (TOTAL.decl == #axiom_report == #TGL_DECL_SOURCE)", bool(m_cov) and kh_cov[0] == len(axm) == len(srcm), [kh_cov, len(axm), len(srcm)])
chk("proveniencia e axiom_report cobrem EXATAMENTE os mesmos nomes", set(axm) == set(srcm), [len(set(axm) ^ set(srcm))])
# --- O KERNEL DA v400 E' O DA v399: o axiom_report efetivo e a proveniencia lidos AGORA do Audit == os do core v399 SELADO; a cobertura idem
cov9 = kf9.get("axiom_coverage_v392") or {}
chk("o axiom_report EFETIVO lido agora do log do Audit == o do core v399 selado (mesmos nomes, mesmas listas de axiomas)", axm == axr9, [len(axm), len(axr9), sum(1 for n in axr9 if axm.get(n) != axr9[n])])
chk("a proveniencia lida agora (TGL_DECL_SOURCE) == a do core v399 selado", srcm == (kf9.get("declaration_sources_v394") or {}), [len(srcm), len(kf9.get("declaration_sources_v394") or {})])
chk("a linha TOTAL (decl, thm) de agora == a cobertura do core v399 selado", kh_cov[0] == int(cov9.get("decl", -1)) and kh_cov[1] == int(cov9.get("thm", -1)), [kh_cov, [cov9.get("decl"), cov9.get("thm")]])
# --- a duracao
mm_ = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", marcas, re.M)}
dur_audit = mm_["epoch_audit_fim"] - mm_["epoch_build_fim"]; dur_build = mm_["epoch_build_fim"] - mm_["epoch_inicio"]
chk("KH-N1: duracao do `lake env lean TGL/Audit.lean` bem abaixo do timeout de 1800 s do um.py (< 900 s)", dur_audit < 900, {"audit_s": dur_audit, "build_s": dur_build})
bf = "inicio %s\n%s\nrc_build=%d\n%s\nrc_audit=%d\n%s\nfim %s\n" % (ini, LB.rstrip("\n"), rb, AL.rstrip("\n"), ra, "rc=0" if (rb == 0 and ra == 0) else "rc=1", fim)
open(os.path.join(KD, "build_full.log"), "w", encoding="utf-8", newline="\n").write(bf)
# --- arvore so-fontes e varredura recursiva
if os.path.isdir(ARV):
    shutil.rmtree(ARV)
os.makedirs(ARV)
for rel in ("TGL", "TGLExt"):
    shutil.copytree(os.path.join(KB, rel), os.path.join(ARV, rel), copy_function=shutil.copy2)
for f in os.listdir(KB):
    p = os.path.join(KB, f)
    if os.path.isfile(p) and not f.startswith("TGLExt.lean.bak"):
        shutil.copy2(p, os.path.join(ARV, f))
ns = {"re": re, "os": os}
assert "_lean_strip_comments_and_strings" in fn
exec(compile(ast.get_source_segment(um9_src, fn["_lean_strip_comments_and_strings"]), "<um.strip>", "exec"), ns)
TOKS = [ast.literal_eval(ast.get_source_segment(um9_src, n.value)) for n in tree9.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_LEAN_FORBIDDEN_TOKENS"][0]
n_lean = n_o16 = 0; hits = []; hits_probe = []; links = []
pilha = [ARV]
while pilha:
    d = pilha.pop()
    with os.scandir(d) as it:
        for e in it:
            if e.is_junction() or e.is_symlink():
                links.append(e.path)
            elif e.is_dir(follow_symlinks=False):
                pilha.append(e.path)
            elif e.is_file(follow_symlinks=False) and e.name.lower().endswith(".lean"):
                n_lean += 1; rel = os.path.relpath(e.path, ARV).replace(os.sep, "/"); n_o16 += rel.startswith("TGLExt/O16/")
                code = ns["_lean_strip_comments_and_strings"](rd(e.path).decode("utf-8"))
                for tok in TOKS:
                    if re.search(r"\b%s\b" % re.escape(tok), code):
                        (hits_probe if os.path.basename(rel).startswith("Probe") else hits).append("%s:%s" % (rel, tok))
chk("arvore so-fontes sem juncao/link", not links, links[:3])
chk("varredura de tokens proibidos RECURSIVA: zero hits (probes diagnosticos a parte)", not hits, {"hits": hits[:5], "hits_em_Probe": hits_probe[:5], "arquivos_lean": n_lean, "em_TGLExt_O16": n_o16, "tokens": TOKS})
chk("o numero de .lean e de .lean em TGLExt/O16 == os do recibo da v399 (a mesma arvore)", n_lean == R9["varredura_tokens"]["arquivos_lean"] and n_o16 == R9["varredura_tokens"]["arquivos_lean_em_TGLExt_O16"], [n_lean, n_o16])
# --- as entradas ANTIGAS: o Audit da v398 (ANTES; o que a Bancada pina) e o axiom_report EFETIVO da v398 contra o EFETIVO de agora
emb0 = ast.literal_eval(next(n for n in tree8.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_EMBEDDED_KERNEL_FILES").value)
aud_antes = emb0["TGL/Audit.lean"]
nomes_antigos = sorted(set(re.findall(r"(?m)^#print axioms (\S+)", aud_antes)))
iguais_ant = sum(1 for n in nomes_antigos if n.lstrip("@") in axm and set(axm[n.lstrip("@")]) == set(axr0.get(n.lstrip("@"), ["?"])))
chk("as entradas antigas do Audit v398 (nomes distintos) com a MESMA lista de axiomas do axiom_report v398", iguais_ant == len(nomes_antigos), [iguais_ant, len(nomes_antigos)])
exatas = sum(1 for n in axr0 if n in axm and axm[n] == axr0[n]); perdidos = [n for n in axr0 if n not in axm]
chk("NADA da v398 se perde: todo nome do axiom_report da v398 segue no de agora, no trio", not perdidos and all(set(axm.get(n, ["?"])) <= TRIO for n in axr0), [len(axr0), len(perdidos), exatas])
# --- toolchain e o manifesto pinado (o da v398: o ANTES; o da v399 selada: o DEPOIS)
man8 = json.load(open(os.path.join(HERE, DL.BASE98_DIR, "tgl_kernel_proof_manifest.json"), encoding="utf-8")); ff = man8["formal_files_sha256"]
man9 = json.load(open(os.path.join(B9, "tgl_kernel_proof_manifest.json"), encoding="utf-8")); ff9 = man9["formal_files_sha256"]
tl = {"lean_version": man9.get("lean_version"), "lake_version": man9.get("lake_version")}
lv = subprocess.run(["lean", "--version"], capture_output=True, text=True, cwd=KB).stdout.strip().splitlines()[:1]
kv = subprocess.run(["lake", "--version"], capture_output=True, text=True, cwd=KB).stdout.strip().splitlines()[:1]
chk("toolchain do sandbox == a do manifesto pinado (lean e lake)", tl.get("lean_version") == lv and tl.get("lake_version") == kv, {"manifesto": tl, "sandbox": [lv, kv]})
imp = lambda d: hashlib.sha256(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
raiz0, aud0 = sha(emb0["TGLExt.lean"].encode("utf-8")), sha(aud_antes.encode("utf-8"))
chk("ANTES (raiz, Audit) == formal_files_sha256 do manifesto v398 pinado", ff.get("TGLExt.lean") == raiz0 and ff.get("TGL/Audit.lean") == aud0, [raiz0[:16], aud0[:16]])
raiz1, aud1 = sha(rd(os.path.join(ARV, "TGLExt.lean"))), sha(rd(os.path.join(ARV, "TGL", "Audit.lean")))
chk("DEPOIS (raiz, Audit, pedra) da arvore == formal_files_sha256 do manifesto que o selo v399 pina (o kernel da v400 e' o da v399)", ff9.get("TGLExt.lean") == raiz1 and ff9.get("TGL/Audit.lean") == aud1
    and all(ff9.get(p) == sha(rd(os.path.join(ARV, *p.split("/")))) for p in nov), [raiz1[:16], aud1[:16]])
# --- as pedras (modulos) do recibo: declaracoes que o B(n) aceita (N1k): entrada no axiom_report, linha no log do Audit e NOME na fonte da pedra
por_mod = {}
for nme, rel in srcm.items():
    por_mod.setdefault(rel[:-len(".lean")].replace("/", "."), []).append(nme)
pedras = []; sem_decl = []
for p_ in nov:
    mod = p_[:-len(".lean")].replace("/", ".")
    fonte = rd(os.path.join(ARV, *p_.split("/"))).decode("utf-8"); shr = sha(rd(os.path.join(ARV, *p_.split("/"))))
    decl = []
    for n in por_mod.get(mod, []):
        curto = n.split(".")[-1].strip("\u00ab\u00bb")
        if n.startswith("_private.") or not curto:
            continue
        if not re.search(r"(?<![\w'.])" + re.escape(curto) + r"(?![\w'])", fonte):
            continue
        decl.append(n)
    decl = sorted(set(decl))
    if not decl:
        sem_decl.append(p_)
    pedras.append({"path": p_, "sha256": shr, "declaracoes": decl})
chk("cada pedra do recibo tem >= 1 declaracao nomeada (N1k do esboco): nenhum modulo de auditoria sem declaracao nesta versao", not sem_decl and all(p["declaracoes"] for p in pedras), [len(p["declaracoes"]) for p in pedras])
novas_todas = sorted(n for L in (por_mod.get(m, []) for m in NEWMODS) for n in L)
novas_reais = [n for n in novas_todas if n not in axr0]
j1 = [kh_cov[0] - int(cov0["decl"]), kh_cov[1] - int(core8["kernel_formalization"]["axiom_coverage_v392"]["thm"]), kh_cov[2]]
r1_ausente = not os.path.exists(os.path.join(ARV, "TGLExt", "TheSingularityReadsTheAttractor.lean"))
criterios = {"j1_declaracoes": j1[0], "j1_teoremas": j1[1], "j1_fora_do_trio": j1[2], "audit_entradas_antigas_identicas": iguais_ant, "tokens_proibidos": len(hits),
             "r1_ausente": r1_ausente, "declaracoes_novas_no_trio": all(set(axm[n]) <= TRIO for n in novas_todas)}
recibo = {"contrato": "KERNEL_RECIBO_R3_2", "versao": "v400", "rc": 0, "sorry": 0, "erros": 0,
          "build_full_log": {"path": abs_fw(os.path.join(KD, "lake_build.log")), "sha256": sha(rd(os.path.join(KD, "lake_build.log")))},
          "audit_log": {"path": abs_fw(os.path.join(KD, "audit.log")), "sha256": sha(rd(os.path.join(KD, "audit.log")))},
          "toolchain": {"lean_version": lv, "lake_version": kv}, "arvore": abs_fw(ARV),
          "raiz": {"path": "TGLExt.lean", "sha256_antes": raiz0, "sha256_depois": raiz1},
          "audit": {"path": "TGL/Audit.lean", "sha256_antes": aud0, "sha256_depois": aud1},
          "pedras": pedras, "formal_files_antes": ff, "axiomas": sorted(TRIO),
          "varredura_tokens": {"recursiva": True, "arquivos_lean": n_lean, "arquivos_lean_em_TGLExt_O16": n_o16},
          "criterios": {k: {"medido": v} for k, v in criterios.items()},
          "nos_kernel_impressao": {"definicao": "sha256 do JSON canonico de formal_files_sha256 do Nos (manifesto pinado pelo selo v398: o kernel que a Bancada de producao pina)", "antes": imp(ff), "depois": imp(ff)},
          "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
          "nota": "gerado por pos_build_kernel_v400.py (preparacao, 24/10/2026); NAO conferido por verificar_kernel_recibo do B(n) (precisa do selo v400 e do manifesto novo); o ANTES e' o kernel da v398 porque a Bancada de producao AINDA pina a v398 "
                  "(o B(n) da v400 e' um passo simples v398 -> v400: o diff do kernel e' o da v399, a pedra Testemunho; a v400 nao acrescenta modulo); o build do sandbox " + abs_fw(KB) + " e' uma COPIA do kernel da v399, "
                  "com a raiz e o Audit recompilados; a arvore de varredura e' a copia so-fontes " + abs_fw(ARV) + " (MANTIDA: o recibo pos-selo precisa dela)"}
# o recibo da v400 diz o MESMO do kernel que o da v399 (so' mudam versao, logs, arvore, hora e nota)
igual_v399 = {k: (recibo[k] == R9[k]) for k in ("rc", "sorry", "erros", "toolchain", "raiz", "audit", "pedras", "formal_files_antes", "axiomas", "varredura_tokens", "criterios")}
igual_v399["nos_kernel_impressao(antes,depois)"] = (recibo["nos_kernel_impressao"]["antes"], recibo["nos_kernel_impressao"]["depois"]) == (R9["nos_kernel_impressao"]["antes"], R9["nos_kernel_impressao"]["depois"])   # (a `definicao` e' texto: muda de redacao)
chk("o recibo da v400 diz o MESMO do kernel que o recibo da v399 (rc, toolchain, raiz, Audit, pedras, formal_files_antes, axiomas, varredura, criterios, impressao)", all(igual_v399.values()), [k for k, v in igual_v399.items() if not v])
ok = all(s["ok"] for s in sinais)
json.dump(recibo, open(os.path.join(KD, "KERNEL_RECIBO_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
crit = {"contrato": "CRITERIOS_R3_1", "versao": "v400", "preenchido": True, "x19": "nao", "esperados": criterios,
        "origem": "[DERIVED] preenchido pela PREPARACAO com a medicao de kernel/KERNEL_RECIBO_v400.json (J1 = diferenca dos TOTAIS do KH-N1 v400 - v398: o ANTES e' o kernel que a Bancada pina; os mesmos numeros da v399). x19='nao': o recibo lista so' a pedra Testemunho "
                  "(NOVA para a Bancada) e a LightNetStandardWedgeDataBGL.lean ja' esta no kernel desde a v392 (R31-6); a gerencia confere e pina o sha256 antes do B(n).",
        "nota": "NOT_FALSIFIED nunca e creditacao; nada aqui move o gate"}
os.makedirs(os.path.join(HERE, "vinculo"), exist_ok=True)
json.dump(crit, open(os.path.join(HERE, "vinculo", "CRITERIOS_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"ok": ok, "sinais": sinais, "criterios": criterios, "arquivos_lean": n_lean, "em_O16": n_o16, "modo_da_pedra_no_build": modo_pedra, "n_axiomas_lidos_no_audit": len(axm), "hits_em_Probe": hits_probe,
           "n_decl_audit": len(axm), "pedras_sem_declaracao": sem_decl, "inicio": ini, "fim": fim, "githash_lean": hashes_lean, "E_v398": E0, "recibo_igual_ao_da_v399_nos_campos": igual_v399},
          open(os.path.join(KD, "POS_BUILD_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nPOS-BUILD:", "VERDE" if ok else "FALHOU", "| criterios:", criterios, "| .lean:", n_lean, "| escada da v398:", E0)
sys.exit(0 if ok else 1)
