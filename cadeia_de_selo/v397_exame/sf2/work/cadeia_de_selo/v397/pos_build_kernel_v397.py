# -*- coding: utf-8 -*-
"""pos_build_kernel_v397.py -- DEPOIS de construir_kernel_v397.sh: (1) monta kernel/build_full.log no formato do molde; (2) confere o build (rc, zero erro, zero sorry nas 3 formas do contrato R3.2, 'Build completed successfully',
linha Built/Replayed da pedra Token, da raiz e do Audit, axiomas no trio, cabecalho dos .olean = Lean 4.31.0); (3) le do log do Audit (SO' dele) as linhas TGL_DECL_SOURCE (declaracao -> modulo emitido pelo compilador) e o
axiom_report EFETIVO com as funcoes do PROPRIO um.py v396 selado (parse_lean_axioms_v394/parse_lean_provenance_v394, extraidas por ast de base_v396\\um.py: a MESMA logica que o um.py v397 usara), e deriva FLAGS_v397.json
(as declaracoes NOMEADAS publicas do modulo novo, na politica da v396); (4) copia a ARVORE so-fontes para C:\\t\\k397c\\arvore e varre os tokens proibidos RECURSIVAMENTE com a funcao de varredura do PROPRIO um.py v396 (por ast);
(5) mede os criterios; (6) escreve KH_N1_v397.json, KERNEL_RECIBO_v397.json (contrato KERNEL_RECIBO_R3_2: a pedra tem declaracoes nomeadas, entao nao ha modulo de auditoria sem declaracao) e vinculo/CRITERIOS_v397.json
(x19 = 'nao': a unica pedra do recibo e' Token, nao a LightNetStandardWedgeDataBGL). Molde: pos_build_kernel_v396.py.   Uso: python -I -B -X utf8 pos_build_kernel_v397.py"""
import ast, datetime, hashlib, json, os, re, shutil, subprocess, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v397 as DL  # noqa: E402
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX; ARV = DL.ARVORE
BASE = os.path.join(HERE, DL.BASE_DIR)
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


um_src = rd(os.path.join(BASE, "um.py")).decode("utf-8"); tree = ast.parse(um_src)
fn = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
_ns = {"re": re}
for nome in ("parse_lean_provenance_v394", "parse_lean_axioms_v394"):
    exec(compile(ast.get_source_segment(um_src, fn[nome]), "<base_v396:%s>" % nome, "exec"), _ns)
parse_ax, parse_src = _ns["parse_lean_axioms_v394"], _ns["parse_lean_provenance_v394"]
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v397.json"), encoding="utf-8"))["novos"]
assert isinstance(nov, list) and nov == [DL.STONE_REL], "a lista dos modulos novos (preparar_kernel_v397.py) tem de ser so' a pedra"
NEWMODS = {p[:-len(".lean")].replace("/", ".") for p in nov}
N_NOVOS = len(nov)
core396 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8"))["core"]; axr396 = core396["kernel_formalization"]["axiom_report"]
cov396 = core396["kernel_formalization"].get("axiom_coverage_v392") or {}
E396 = int(core396["external_ladder"]["n_theorems_expected"])

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
chk("linha Built/Replayed do modulo novo (Token), da raiz (TGLExt) e do Audit (TGL.Audit)", all(m in jobs for m in exig), [m for m in exig if m not in jobs][:5])
chk("'Build completed successfully'", bool(re.search(r"(?m)^[ \t]*Build completed successfully\b", LB)), re.findall(r"Build completed successfully[^\n]*", LB))
built_raiz = bool(re.search(r"Built\s+TGLExt\b", LB)); built_audit = bool(re.search(r"Built\s+TGL\.Audit\b", LB))
chk("a raiz e o Audit foram COMPILADOS neste build (linha Built: o build e' incremental; mudaram os dois)", built_raiz and built_audit, [built_raiz, built_audit])
modo_pedra = {m: ("Built" if re.search(r"Built\s+" + re.escape(m) + r"\b", LB) else "Replayed" if re.search(r"Replayed\s+" + re.escape(m) + r"\b", LB) else None) for m in sorted(NEWMODS)}
print("INFO: o modulo da pedra neste build:", modo_pedra, "(Replayed = a pedra ja' estava compilada em .lake/build do k397; o rito real do Nos a compila a frio)")
LIBL = os.path.join(KB, ".lake", "build", "lib", "lean")
hdr = {}
for m in sorted(NEWMODS) + ["TGLExt", "TGL.Audit"]:
    p = os.path.join(LIBL, *m.split(".")) + ".olean"
    h = rd(p)[:96] if os.path.exists(p) else b""
    hdr[m] = (h[:5] == b"olean" and b"4.31.0" in h[:40], re.search(rb"[0-9a-f]{40}", h).group(0).decode() if re.search(rb"[0-9a-f]{40}", h) else None)
hashes_lean = sorted({v[1] for v in hdr.values()})
chk("cabecalho de TODO .olean (pedra + raiz + Audit): magic 'olean' e versao 4.31.0; um unico githash do Lean", all(v[0] for v in hdr.values()) and len(hashes_lean) == 1, [len(hdr), hashes_lean])
# --- o log do Audit: leitura SO' dele (licao KH-N1) com as funcoes do um.py v396 selado
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
# --- FLAGS: a politica da v396 (so' declaracao NOMEADA); a escada = a da v396 + as bandeiras desta pedra
por_mod = {}
for nme, rel in srcm.items():
    mod = rel[:-len(".lean")].replace("/", ".")
    if mod in NEWMODS:
        por_mod.setdefault(mod, []).append(nme)
chk("o compilador emite declaracoes do modulo da pedra (e so' dos modulos novos entre os novos)", set(por_mod) == NEWMODS, sorted(por_mod))
novas_todas = sorted(n for L in por_mod.values() for n in L)
pub = sorted(n for n in novas_todas if not n.startswith("_private."))
priv = sorted(n for n in novas_todas if n.startswith("_private."))
nomeadas = [n for n in pub if DL.classe(n) == "nomeada"]; aux = [n for n in pub if DL.classe(n) != "nomeada"]
cl_aux = {c: sum(1 for x in aux if DL.classe(x) == c) for c, _ in DL.AUX_CLASSES}
chk("o teorema do registro (a composicao incondicional) esta no Audit, no modulo da pedra, nomeado, no trio", DL.THEOREM in nomeadas and set(axm[DL.THEOREM]) <= TRIO, [t for t in (DL.THEOREM,) if t not in nomeadas])
chk("a face de Fock do psion NAO esta nesta pedra: o compilador a emite no modulo de Psibit (v395), nao no da pedra; e os %d termos de suporte (kernel antigo) estao no Audit, no trio" % len(DL.SUPPORT_THEOREMS),
    srcm.get(DL.FOCK_FACE_THEOREM) == DL.FOCK_FACE_PATH and DL.FOCK_FACE_THEOREM not in nomeadas and all(t in axm and set(axm[t]) <= TRIO and t in srcm for t in DL.SUPPORT_THEOREMS), [srcm.get(DL.FOCK_FACE_THEOREM), [t for t in DL.SUPPORT_THEOREMS if t not in axm][:3]])
chk("os %d teoremas do contrato do registro estao no Audit, nomeados, no modulo da pedra, no trio" % len(DL.CONTRACT_THEOREMS), all(t in nomeadas and set(axm[t]) <= TRIO and srcm[t] == DL.STONE_REL for t in DL.CONTRACT_THEOREMS), [t for t in DL.CONTRACT_THEOREMS if t not in nomeadas])
chk("o teorema incondicional depende so' do trio (conferido por inclusao)", set(axm[DL.THEOREM]) <= TRIO, [axm[DL.THEOREM]])
flags_v397 = [[DL.FLAG_PREFIX + "%04d" % (i + 1), n, DL.STONE_MOD, "token_nomeada"] for i, n in enumerate(nomeadas)]
v396_flags = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_LEAN_THEOREM_FLAGS").value)
chk("as chaves das flags novas nao colidem com as da v396 e sao unicas; os NOMES nao repetem os de uma bandeira existente", len({f[0] for f in flags_v397}) == len(flags_v397) and not ({f[0] for f in flags_v397} & set(v396_flags)) and not ({f[1] for f in flags_v397} & set(v396_flags.values())), len(flags_v397))
chk("toda bandeira nova esta no axiom_report, no trio, e e' declaracao NOMEADA (a politica)", all(f[1] in axm and set(axm[f[1]]) <= TRIO and DL.classe(f[1]) == "nomeada" for f in flags_v397), len(flags_v397))
reatribuidas = {n: {"antes": (core396["kernel_formalization"].get("declaration_sources_v394") or {}).get(n), "agora": srcm[n]} for n in sorted(novas_todas) if n in axr396}   # ja' no axiom_report da v396 e agora atribuidas a pedra pela proveniencia (o Lean gera a auxiliar eq_1 de TGLExt.diagFlow tambem nela)
novas_reais = [n for n in novas_todas if n not in axr396]
chk("declaracoes NOVAS do modulo novo (publicas + privadas, por proveniencia, menos as reatribuidas) == TOTAL(v397) - TOTAL(v396); as reatribuidas sao auxiliares (sem bandeira)", len(novas_reais) == kh_cov[0] - int(cov396.get("decl", -1)) and all(DL.classe(n) != "nomeada" for n in reatribuidas), [len(novas_reais), kh_cov[0], cov396.get("decl"), reatribuidas])
chk("os nomes do Audit da v396 (axiom_report do core v396) seguem todos no axiom_report de agora (nada se perde), com a MESMA lista", all(n in axm and axm[n] == axr396[n] for n in axr396), [len(axr396), sum(1 for n in axr396 if n not in axm)])
chk("o axiom_report de agora tem exatamente os nomes do v396 mais as declaracoes do modulo novo", set(axm) == set(axr396) | set(novas_todas), [len(axm), len(axr396), len(novas_todas)])
chave_de = {f[1]: f[0] for f in flags_v397}
json.dump({"politica": "so' declaracao NOMEADA tem bandeira (a pratica selada da v392, v393, v394 e v396); as auxiliares geradas pelo compilador (ultimo componente _proof_N, _simp_N, match_N, _sunfold, eq_N, eq_def, congr_simp) ficam fora; "
                       "chaves %sNNNN, em ordem alfabetica do nome (decisao da gerencia c1, 23/10/2026; a regra e' a da v394, v395 e v396, os numeros saem do Audit desta geracao)" % DL.FLAG_PREFIX,
           "flags": flags_v397, "n_flags": len(flags_v397), "n_decl_audit": len(axm), "por_origem": {"token_nomeada": len(flags_v397)},
           "por_grupo_bandeiras": {"token": len(flags_v397)},
           "excluidas_auxiliares": {"n": len(aux), "por_classe": cl_aux, "nomes": aux},
           "publicas_no_modulo": len(pub), "privadas_no_modulo": len(priv), "decl_totais_modulo_novo": len(novas_todas), "decl_novas_do_modulo": len(novas_reais), "reatribuidas_a_pedra": reatribuidas,
           "bandeira_do_teorema_incondicional": chave_de[DL.THEOREM], "suporte_do_contrato": {t: srcm[t] for t in DL.SUPPORT_THEOREMS}, "fock_face_declarada_em": srcm[DL.FOCK_FACE_THEOREM],
           "proveniencia_publicas": {n: srcm[n] for n in pub}},
          open(os.path.join(KD, "FLAGS_v397.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# --- a duracao
mm_ = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", marcas, re.M)}
dur_audit = mm_["epoch_audit_fim"] - mm_["epoch_build_fim"]; dur_build = mm_["epoch_build_fim"] - mm_["epoch_inicio"]
chk("KH-N1: duracao do `lake env lean TGL/Audit.lean` bem abaixo do timeout de 1800 s do um.py (< 900 s)", dur_audit < 900, {"audit_s": dur_audit, "build_s": dur_build})
bf = "inicio %s\n%s\nrc_build=%d\n%s\nrc_audit=%d\n%s\nfim %s\n" % (ini, LB.rstrip("\n"), rb, AL.rstrip("\n"), ra, "rc=0" if (rb == 0 and ra == 0) else "rc=1", fim)
open(os.path.join(KD, "build_full.log"), "w", encoding="utf-8", newline="\n").write(bf)
# --- arvore so-fontes e varredura recursiva
if not os.environ.get("V397_KEEP_ARV"):
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
exec(compile(ast.get_source_segment(um_src, fn["_lean_strip_comments_and_strings"]), "<um.strip>", "exec"), ns)
TOKS = [ast.literal_eval(ast.get_source_segment(um_src, n.value)) for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_LEAN_FORBIDDEN_TOKENS"][0]
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
# --- as entradas ANTIGAS: o Audit da v396 (ANTES) e o axiom_report EFETIVO da v396 contra o EFETIVO de agora
emb396 = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_EMBEDDED_KERNEL_FILES").value)
aud_antes = emb396["TGL/Audit.lean"]
nomes_antigos = sorted(set(re.findall(r"(?m)^#print axioms (\S+)", aud_antes)))
iguais_ant = sum(1 for n in nomes_antigos if n.lstrip("@") in axm and set(axm[n.lstrip("@")]) == set(axr396.get(n.lstrip("@"), ["?"])))
chk("as entradas antigas do Audit v396 (nomes distintos) com a MESMA lista de axiomas do axiom_report v396", iguais_ant == len(nomes_antigos), [iguais_ant, len(nomes_antigos)])
exatas = sum(1 for n in axr396 if n in axm and axm[n] == axr396[n]); perdidos = [n for n in axr396 if n not in axm]
chk("NADA da v396 se perde: todo nome do axiom_report da v396 segue no de agora, no trio", not perdidos and all(set(axm.get(n, ["?"])) <= TRIO for n in axr396), [len(axr396), len(perdidos), exatas])
# --- toolchain e o manifesto pinado
man = json.load(open(os.path.join(BASE, "tgl_kernel_proof_manifest.json"), encoding="utf-8")); ff = man["formal_files_sha256"]
tl = {"lean_version": man.get("lean_version"), "lake_version": man.get("lake_version")}
lv = subprocess.run(["lean", "--version"], capture_output=True, text=True, cwd=KB).stdout.strip().splitlines()[:1]
kv = subprocess.run(["lake", "--version"], capture_output=True, text=True, cwd=KB).stdout.strip().splitlines()[:1]
chk("toolchain do sandbox == a do manifesto pinado (lean e lake)", tl.get("lean_version") == lv and tl.get("lake_version") == kv, {"manifesto": tl, "sandbox": [lv, kv]})
imp = lambda d: hashlib.sha256(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
raiz0, aud0 = sha(emb396["TGLExt.lean"].encode("utf-8")), sha(aud_antes.encode("utf-8"))
chk("ANTES (raiz, Audit) == formal_files_sha256 do manifesto v396 pinado", ff.get("TGLExt.lean") == raiz0 and ff.get("TGL/Audit.lean") == aud0, [raiz0[:16], aud0[:16]])
# --- a pedra (modulo) do recibo: declaracoes que o B(n) aceita (N1k): entrada no axiom_report, linha no log do Audit e NOME na fonte da pedra
pedras = []; sem_decl = []
for p_ in sorted(nov):
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
chk("a pedra do recibo tem >= 1 declaracao nomeada (N1k do esboco): nenhum modulo de auditoria sem declaracao nesta versao", not sem_decl and all(p["declaracoes"] for p in pedras), [len(p["declaracoes"]) for p in pedras])
n_decl_recibo = sum(len(p["declaracoes"]) for p in pedras)
j1 = [kh_cov[0] - int(cov396["decl"]), kh_cov[1] - int(core396["kernel_formalization"]["axiom_coverage_v392"]["thm"]), kh_cov[2]]
kh_json = {"contrato": "KH_N1_v397", "desenho": "(a) run_cmd no fim do Audit (herdado da v392); (b) linha TGL_DECL_SOURCE por constante (proveniencia emitida pelo compilador, v396)", "linha_TOTAL": {"decl": kh_cov[0], "thm": kh_cov[1], "fora_do_trio": kh_cov[2]},
           "axiom_report_efetivo_n": len(axm), "proveniencia_n": len(srcm), "nao_lidas_pelo_leitor_v394": 0, "nomes_distintos_print_antigos": len(nomes_antigos), "antigas_identicas": iguais_ant,
           "entradas_antigas_exatas_no_efetivo": exatas, "nomes_v396_perdidos": len(perdidos), "novas_no_trio": all(set(axm[n]) <= TRIO for n in novas_todas), "sorryAx_no_log_do_audit": AL.count("sorryAx"),
           "delta_vs_v396": {"decl": j1[0], "thm": j1[1]}, "duracao_audit_s": dur_audit, "duracao_build_s": dur_build, "timeout_umpy_s": 1800,
           "audit_log_bytes": len(rd(os.path.join(KD, "audit.log"))), "audit_log_sha256": sha(rd(os.path.join(KD, "audit.log"))), "n_bandeiras": len(flags_v397), "decl_do_modulo_novo": len(novas_todas), "decl_novas_do_modulo": len(novas_reais), "reatribuidas_a_pedra": reatribuidas,
           "quando": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "estatuto": "[REAL] medido por pos_build_kernel_v397.py sobre o log do Audit do sandbox; fora do selo"}
json.dump(kh_json, open(os.path.join(KD, "KH_N1_v397.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r1_ausente = not os.path.exists(os.path.join(ARV, "TGLExt", "TheSingularityReadsTheAttractor.lean"))
criterios = {"j1_declaracoes": j1[0], "j1_teoremas": j1[1], "j1_fora_do_trio": j1[2], "audit_entradas_antigas_identicas": iguais_ant, "tokens_proibidos": len(hits),
             "r1_ausente": r1_ausente, "declaracoes_novas_no_trio": all(set(axm[n]) <= TRIO for n in novas_todas)}
recibo = {"contrato": "KERNEL_RECIBO_R3_2", "versao": "v397", "rc": 0, "sorry": 0, "erros": 0,
          "build_full_log": {"path": abs_fw(os.path.join(KD, "lake_build.log")), "sha256": sha(rd(os.path.join(KD, "lake_build.log")))},
          "audit_log": {"path": abs_fw(os.path.join(KD, "audit.log")), "sha256": sha(rd(os.path.join(KD, "audit.log")))},
          "toolchain": {"lean_version": lv, "lake_version": kv}, "arvore": abs_fw(ARV),
          "raiz": {"path": "TGLExt.lean", "sha256_antes": raiz0, "sha256_depois": sha(rd(os.path.join(ARV, "TGLExt.lean")))},
          "audit": {"path": "TGL/Audit.lean", "sha256_antes": aud0, "sha256_depois": sha(rd(os.path.join(ARV, "TGL", "Audit.lean")))},
          "pedras": pedras, "formal_files_antes": ff, "axiomas": sorted(TRIO),
          "varredura_tokens": {"recursiva": True, "arquivos_lean": n_lean, "arquivos_lean_em_TGLExt_O16": n_o16},
          "criterios": {k: {"medido": v} for k, v in criterios.items()},
          "nos_kernel_impressao": {"definicao": "sha256 do JSON canonico de formal_files_sha256 do Nos (manifesto pinado pelo selo v396)", "antes": imp(ff), "depois": imp(ff)},
          "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
          "nota": "gerado por pos_build_kernel_v397.py (preparacao, 23/10/2026); NAO conferido por verificar_kernel_recibo do B(n) (precisa do selo v397 e do manifesto novo); a arvore de varredura e' a copia so-fontes " + abs_fw(ARV) + " (MANTIDA: o recibo pos-selo precisa dela); "
                  "o build do sandbox e' INCREMENTAL (a pedra pode ja' estar compilada em C:/t/k397/final numa versao anterior do texto; o rito real do Nos compila a frio)"}
ok = all(s["ok"] for s in sinais)
json.dump(recibo, open(os.path.join(KD, "KERNEL_RECIBO_v397.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
crit = {"contrato": "CRITERIOS_R3_1", "versao": "v397", "preenchido": True, "x19": "nao", "esperados": criterios,
        "origem": "[DERIVED] preenchido pela PREPARACAO com a medicao de kernel/KERNEL_RECIBO_v397.json (J1 = diferenca dos TOTAIS do KH-N1 v397 - v396, como na v393, v394 e v396). x19='nao': o recibo v397 lista so' a pedra NOVA Token e a LightNetStandardWedgeDataBGL.lean "
                  "ja' esta no kernel desde a v392 (R31-6: 'sim' <=> a pedra consta do recibo); a gerencia confere e pina o sha256 antes do B(n).",
        "nota": "NOT_FALSIFIED nunca e creditacao; nada aqui move o gate"}
os.makedirs(os.path.join(HERE, "vinculo"), exist_ok=True)
json.dump(crit, open(os.path.join(HERE, "vinculo", "CRITERIOS_v397.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"ok": ok, "sinais": sinais, "criterios": criterios, "arquivos_lean": n_lean, "em_O16": n_o16, "modo_da_pedra_no_build": modo_pedra, "n_axiomas_lidos_no_audit": len(axm), "hits_em_Probe": hits_probe,
           "n_flags": len(flags_v397), "n_decl_audit": len(axm), "pedras_sem_declaracao": sem_decl, "n_declaracoes_no_recibo": n_decl_recibo, "inicio": ini, "fim": fim, "githash_lean": hashes_lean, "E396": E396},
          open(os.path.join(KD, "POS_BUILD_v397.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nPOS-BUILD:", "VERDE" if ok else "FALHOU", "| criterios:", criterios, "| .lean:", n_lean, "| bandeiras:", len(flags_v397), "| escada esperada:", E396 + len(flags_v397))
sys.exit(0 if ok else 1)
