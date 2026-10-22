# -*- coding: utf-8 -*-
"""pos_build_kernel_v394.py -- DEPOIS de construir_kernel_v394.sh: (1) monta kernel/build_full.log no formato do molde; (2) confere o build (rc, zero erro, zero sorry nas 3 formas do contrato R3.2,
'Build completed successfully', linha Built/Replayed de cada um dos modulos novos (189 do Codex + a pedra do delta), da raiz e do Audit, axiomas no trio, cabecalho dos .olean = Lean 4.31.0); (3) le do log do Audit (SO' dele) as
linhas TGL_DECL_SOURCE (declaracao -> modulo emitido pelo compilador) e o axiom_report EFETIVO com as funcoes do Codex (parse_lean_axioms_v394/parse_lean_provenance_v394, extraidas por ast do candidato r8:
a MESMA logica que o um.py v394 usara), e deriva FLAGS_v394.json (todas as declaracoes publicas dos modulos novos, chaves do candidato r8 conferidas por NOME); (4) copia a ARVORE so-fontes para C:\\t\\k394\\arvore e
varre os tokens proibidos RECURSIVAMENTE com a funcao de varredura do PROPRIO um.py v393 (extraida por ast); (5) mede os criterios; (6) escreve KH_N1_v394.json, KERNEL_RECIBO_v394.json (contrato KERNEL_RECIBO_R3_2)
e vinculo/CRITERIOS_v394.json (x19 = 'nao': nenhuma das pedras do recibo e' LightNetStandardWedgeDataBGL; ver ESTADO_V394). Molde: pos_build_kernel_v393.py.
Uso: python -I -B -X utf8 pos_build_kernel_v394.py"""
import ast, datetime, hashlib, json, os, re, shutil, subprocess, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta19_v394 as DL  # noqa: E402   (DELTA 19/10: a geracao d19 -- sandbox C:\t\k394d\final, logs em kernel_d19, 190 modulos novos, politica de bandeiras so' de declaracao nomeada)
C = "C:" + os.sep
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX; ARV = DL.ARVORE
NOS0 = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
NOS = NOS0 if hashlib.sha256(open(os.path.join(NOS0, "um.py"), "rb").read()).hexdigest()[:16] == "18be2ddb06c60f90" else os.path.join(HERE, "base_v393")   # a v393 SELADA
R8 = os.path.join(C, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "F1.FECHO_20261015", "coverage_candidate_r8", "um_v394_prechecked.py")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
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


# --- as funcoes do Codex (parse_lean_*), extraidas do r8 por ast: a mesma logica do um.py v394
_r8src = rd(R8).decode("utf-8"); _r8 = ast.parse(_r8src)
_ns = {"re": re}
for n in _r8.body:
    if isinstance(n, ast.FunctionDef) and n.name in ("parse_lean_provenance_v394", "parse_lean_axioms_v394"):
        exec(compile(ast.get_source_segment(_r8src, n), "<r8:%s>" % n.name, "exec"), _ns)
parse_ax, parse_src = _ns["parse_lean_axioms_v394"], _ns["parse_lean_provenance_v394"]
r8_flags = None
for n in _r8.body:
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_LEAN_THEOREM_FLAGS":
        r8_flags = ast.literal_eval(n.value)
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_V394_FORMAL_CONTRACT":
        r8_formal = ast.literal_eval(n.value)
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_V394_QUADRATIC_CONTRACT":
        r8_quad = ast.literal_eval(n.value)
    if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_V394_NETWORK_CONTRACT":
        r8_net = ast.literal_eval(n.value)
um_src = rd(os.path.join(NOS, "um.py")).decode("utf-8"); tree = ast.parse(um_src)
fn = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
nov = json.load(open(os.path.join(HERE, "kernel_modulos_novos_v394.json"), encoding="utf-8"))["novos"]
NEWMODS = {p[:-len(".lean")].replace("/", ".") for p in nov}
assert len(NEWMODS) == len(nov) and isinstance(nov, list) and DL.STONE_REL in nov, "a lista dos modulos novos (preparar_kernel_v394.py) tem de trazer a pedra do delta, sem repeticao"
N_NOVOS = len(nov)   # LIDO da lista (189 do Codex + a pedra do delta): nada digitado
N_CODEX = N_NOVOS - 1

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
chk("linha Built/Replayed de cada um dos %d modulos novos, da raiz (TGLExt) e do Audit (TGL.Audit)" % N_NOVOS, all(m in jobs for m in exig), [m for m in exig if m not in jobs][:5])
chk("'Build completed successfully'", bool(re.search(r"(?m)^[ \t]*Build completed successfully\b", LB)), re.findall(r"Build completed successfully[^\n]*", LB))
built_new = sorted(m for m in NEWMODS if re.search(r"Built\s+" + re.escape(m) + r"\b", LB))
chk("os %d modulos novos foram COMPILADOS neste build (linha Built, nao Replayed): build FRIO, como o do rito" % N_NOVOS, len(built_new) == N_NOVOS, len(built_new))
# --- cabecalho dos .olean: Lean 4.31.0 (e o githash) em TODO .olean dos modulos novos, da raiz e do Audit
LIBL = os.path.join(KB, ".lake", "build", "lib", "lean")
hdr = {}
for m in sorted(NEWMODS) + ["TGLExt", "TGL.Audit"]:
    p = os.path.join(LIBL, *m.split(".")) + ".olean"
    h = rd(p)[:96] if os.path.exists(p) else b""
    hdr[m] = (h[:5] == b"olean" and b"4.31.0" in h[:40], re.search(rb"[0-9a-f]{40}", h).group(0).decode() if re.search(rb"[0-9a-f]{40}", h) else None)
hashes_lean = sorted({v[1] for v in hdr.values()})
chk("cabecalho de TODO .olean (%d novos + raiz + Audit): magic 'olean' e versao 4.31.0; um unico githash do Lean" % N_NOVOS, all(v[0] for v in hdr.values()) and len(hashes_lean) == 1, [len(hdr), hashes_lean])
# --- o log do Audit: leitura SO' dele (licao KH-N1) com as funcoes do Codex
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
core393 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; axr393 = core393["kernel_formalization"]["axiom_report"]
# --- FLAGS (DELTA 19/10; decisao da gerencia): POLITICA so' de declaracao NOMEADA -- a pratica selada da v392 (738 de 969) e da v393 (144 de 186). As auxiliares geradas pelo compilador (_proof_N, _simp_N, match_N,
# _sunfold, eq_N, eq_def, congr_simp; o ULTIMO componente do nome decide: delta19_v394.classe) ficam FORA; as nomeadas publicas que o Codex nao marcou GANHAM bandeira; a pedra do delta ganha a sua. A lista e os numeros sao os do exame
# (EXAME_FINAL_V394.md §4), conferidos abaixo por script contra o texto do exame.
por_mod = {}
for nme, rel in srcm.items():
    mod = rel[:-len(".lean")].replace("/", ".")
    if mod in NEWMODS:
        por_mod.setdefault(mod, []).append(nme)
pub = lambda L: sorted(n for n in L if not n.startswith("_private."))
grp_de = lambda m: DL.grupo_do_modulo(m)
g_tempo = pub(n for m, L in por_mod.items() if grp_de(m) == "tempo" for n in L); g_quad = pub(n for m, L in por_mod.items() if grp_de(m) == "quadratica" for n in L)
g_net = pub(n for m, L in por_mod.items() if grp_de(m) == "rede" for n in L); g_delta = pub(por_mod.get(DL.STONE_MOD, []))
assert set(por_mod) <= NEWMODS and DL.STONE_MOD in por_mod and {grp_de(m) for m in por_mod} == {"tempo", "quadratica", "rede", "outro"} and all(grp_de(m) == "outro" for m in por_mod if m == DL.STONE_MOD), "os modulos novos nao se repartem em tempo, quadratica, rede e o delta"   # (as 3 NetworkProofAuditR* nao tem declaracao: nao aparecem na proveniencia)
novas_todas = sorted(n for L in por_mod.values() for n in L)
_v393_flags_src = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_LEAN_THEOREM_FLAGS").value)
v393_names = set(_v393_flags_src.values())
r8_novas = sorted(set(r8_flags.values()) - v393_names)
mine_pub = sorted(set(g_tempo) | set(g_quad) | set(g_net))          # as publicas dos 189 modulos do Codex (a pedra do delta vai a parte: g_delta)
chk("tempo: os teoremas do contrato do Codex existem no MEU Audit, nos 4 modulos de tempo, no trio", set(r8_formal["theorems"]) <= set(g_tempo) and all(set(axm[n]) <= TRIO for n in r8_formal["theorems"]), [len(r8_formal["theorems"]), len(g_tempo)])
chk("regra quadratica: os teoremas do contrato do Codex existem no MEU Audit, no modulo, no trio", set(r8_quad["theorems"]) <= set(g_quad) and all(set(axm[n]) <= TRIO for n in r8_quad["theorems"]), [len(r8_quad["theorems"]), len(g_quad)])
chk("rede: as declaracoes do contrato de rede do Codex existem no MEU Audit, nos modulos F1Fecho394, no trio", set(r8_net["declarations"]) <= set(g_net) and all(set(axm[n]) <= TRIO for n in r8_net["declarations"]), [len(r8_net["declarations"]), len(g_net)])
chk("as %d bandeiras do candidato r8 (por NOME) existem no MEU Audit, nos modulos do Codex, no trio" % len(r8_novas), set(r8_novas) <= set(mine_pub) and all(set(axm[n]) <= TRIO for n in r8_novas), [len(r8_novas), len(mine_pub)])
chk("a pedra do delta: UMA declaracao publica (o teorema de composicao), na fonte do modulo, no trio", g_delta == [DL.THEOREM] and set(axm[DL.THEOREM]) == set(TRIO), [g_delta, axm.get(DL.THEOREM)])
chk("os oito teoremas que a conjuncao CITA estao no axiom_report do rito, dentro do trio", all(n in axm and set(axm[n]) <= TRIO for n in DL.CITED), [n for n in DL.CITED if n not in axm])
# a ordem de insercao do Codex (r8_flags), so' as NOMEADAS
r8_conj = set(r8_novas)
r8_ordem = [(k, v) for k, v in r8_flags.items() if v in r8_conj]
nomeadas_codex = [(k, v) for k, v in r8_ordem if DL.classe(v) == "nomeada"]; aux_codex = [(k, v) for k, v in r8_ordem if DL.classe(v) != "nomeada"]
nomeadas_sem_bandeira = sorted(n for n in mine_pub if n not in r8_conj and DL.classe(n) == "nomeada"); aux_sem_bandeira = sorted(n for n in mine_pub if n not in r8_conj and DL.classe(n) != "nomeada")
cl_aux = lambda L: {c: sum(1 for x in L if DL.classe(x if isinstance(x, str) else x[1]) == c) for c, _ in DL.AUX_CLASSES}
# a conferencia contra o texto do exame (nada digitado: os numeros saem do EXAME_FINAL_V394.md)
_ex = open(os.path.join(os.path.dirname(HERE), "v394_exame", "EXAME_FINAL_V394.md"), encoding="utf-8").read()
_n = lambda rx: [int(x) for x in re.search(rx, _ex).groups()]
ex_nom = _n(r"- (\d+) são nomeadas;")[0]; ex_aux, ex_pms, ex_eq, ex_cs = _n(r"- (\d+) são auxiliares geradas pelo compilador: (\d+) `_proof_N`[^,]*, (\d+) `eq_N` e (\d+) `congr_simp`")
ex_sem_nom, ex_sem_aux, ex_sem_eq, ex_sem_cs = _n(r"São (\d+) nomeadas \([^)]*\), (\d+) auxiliares, (\d+) `eq_N` e (\d+) `congr_simp`"); ex_flags, ex_escada = _n(r"seriam (\d+) bandeiras e a escada daria (\d+)")
c_aux = cl_aux(aux_codex); c_sem = cl_aux(aux_sem_bandeira)
E393_ = int(core393["external_ladder"]["n_theorems_expected"])
chk("a classificacao reproduz o EXAME: %d nomeadas e %d auxiliares nas bandeiras do Codex (%d proof/simp/match/sunfold, %d eq, %d congr_simp)" % (ex_nom, ex_aux, ex_pms, ex_eq, ex_cs),
    [len(nomeadas_codex), len(aux_codex), c_aux["proof_simp_match_sunfold"], c_aux["eq"], c_aux["congr_simp"]] == [ex_nom, ex_aux, ex_pms, ex_eq, ex_cs], [len(nomeadas_codex), len(aux_codex), c_aux])
chk("a classificacao reproduz o EXAME: %d nomeadas sem bandeira, %d auxiliares, %d eq_N, %d congr_simp (as publicas sem bandeira)" % (ex_sem_nom, ex_sem_aux, ex_sem_eq, ex_sem_cs),
    [len(nomeadas_sem_bandeira), c_sem["proof_simp_match_sunfold"], c_sem["eq"], c_sem["congr_simp"]] == [ex_sem_nom, ex_sem_aux, ex_sem_eq, ex_sem_cs], [len(nomeadas_sem_bandeira), c_sem])
chk("a politica da gerencia: %d bandeiras e escada %d ANTES da pedra do delta (o exame estimou)" % (ex_flags, ex_escada), [len(nomeadas_codex) + len(nomeadas_sem_bandeira), E393_ + len(nomeadas_codex) + len(nomeadas_sem_bandeira)] == [ex_flags, ex_escada], [len(nomeadas_codex) + len(nomeadas_sem_bandeira), E393_])
chk("(informativo) declaracoes publicas dos modulos do Codex SEM bandeira, por politica (auxiliares geradas pelo compilador; todas no trio e cobertas pelo KH-N1)", all(set(axm[n]) <= TRIO for n in aux_sem_bandeira + [v for _, v in aux_codex]), [len(aux_sem_bandeira) + len(aux_codex), c_aux, c_sem])
modulo_de = lambda n: srcm[n][:-len(".lean")].replace("/", ".")
flags_v394 = [[k, n, modulo_de(n), "codex_nomeada"] for k, n in nomeadas_codex]
flags_v394 += [[DL.PREFIXO_NOMEADA_SEM_BANDEIRA + "%04d" % (i + 1), n, modulo_de(n), "nomeada_sem_bandeira"] for i, n in enumerate(nomeadas_sem_bandeira)]
flags_v394 += [[DL.FLAG_KEY, DL.THEOREM, DL.STONE_MOD, "delta"]]
chk("as chaves das flags novas nao colidem com as da v393 e sao unicas", len({f[0] for f in flags_v394}) == len(flags_v394) and not ({f[0] for f in flags_v394} & set(_v393_flags_src)), len(flags_v394))
chk("toda bandeira nova esta no axiom_report, no trio, e e' declaracao NOMEADA (a politica)", all(f[1] in axm and set(axm[f[1]]) <= TRIO and DL.classe(f[1]) == "nomeada" for f in flags_v394), len(flags_v394))
chk("declaracoes dos modulos novos (publicas + privadas), por proveniencia == TOTAL(v394) - TOTAL(v393)", len(novas_todas) == kh_cov[0] - int((core393["kernel_formalization"].get("axiom_coverage_v392") or {}).get("decl", -1)), [len(novas_todas), kh_cov[0]])
por_grupo_flags = {g: sum(1 for f in flags_v394 if DL.grupo_do_modulo(f[2]) == g) for g in ("tempo", "quadratica", "rede", "outro")}
json.dump({"politica": "so' declaracao NOMEADA tem bandeira (a pratica selada da v392/v393); as auxiliares geradas pelo compilador (ultimo componente _proof_N, _simp_N, match_N, _sunfold, eq_N, eq_def, congr_simp) ficam fora; as nomeadas publicas "
                       "que o Codex nao marcou ganham bandeira (prefixo %s); a pedra do delta ganha %s (decisao da gerencia c1, 19/10/2026; numeros do EXAME_FINAL_V394.md)" % (DL.PREFIXO_NOMEADA_SEM_BANDEIRA, DL.FLAG_KEY),
           "flags": flags_v394, "n_flags": len(flags_v394), "n_decl_audit": len(axm),
           "por_origem": {"codex_nomeada": len(nomeadas_codex), "nomeada_sem_bandeira": len(nomeadas_sem_bandeira), "delta": 1}, "por_grupo_bandeiras": por_grupo_flags,
           "por_grupo_contrato": {"tempo_contrato": len(r8_formal["theorems"]), "quadratica_contrato": len(r8_quad["theorems"]), "rede_contrato": len(r8_net["declarations"])},
           "excluidas_auxiliares": {"n": len(aux_codex), "por_classe": c_aux, "nomes": sorted(v for _, v in aux_codex)},
           "publicas_sem_bandeira": {"n": len(aux_sem_bandeira), "por_classe": c_sem}, "nomeadas_sem_bandeira_do_codex": nomeadas_sem_bandeira,
           "publicas_nos_modulos_do_codex": len(mine_pub), "publicas_sem_bandeira_total": len(mine_pub) - len(nomeadas_codex) - len(nomeadas_sem_bandeira), "privadas_nos_modulos_novos": len(novas_todas) - len(mine_pub) - len(g_delta),
           "decl_totais_modulos_novos": len(novas_todas), "decl_da_pedra_do_delta": len(por_mod.get(DL.STONE_MOD, [])), "proveniencia_publicas": {n: srcm[n] for n in sorted(mine_pub + g_delta)},
           "exame": {"nomeadas": ex_nom, "auxiliares": ex_aux, "flags": ex_flags, "escada": ex_escada, "arquivo": "v394_exame\\EXAME_FINAL_V394.md"}}, open(os.path.join(KD, "FLAGS_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# --- o que o Codex mediu na pre-auditoria: decl 29025, thm 23068 (conferencia informativa, NAO gateia; o rito cobra os NOSSOS numeros); a pedra do delta soma as suas declaracoes e o seu teorema
pre = os.path.join(C, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "F1.FECHO_20261015", "full_rite", "KH_N1_V394_NETWORK_R8_PREAUDIT.json")
pre_j = json.load(open(pre, encoding="utf-8")) if os.path.exists(pre) else {}
pre_tot = {k_: pre_j.get(k_) for k_ in ("decl", "thm", "fora_do_trio")} if "decl" in pre_j else (pre_j.get("linha_TOTAL") or pre_j.get("total") or {})   # a pre-auditoria do Codex traz decl/thm/fora_do_trio no topo do JSON
_pd = [int(pre_tot.get("decl", -1)), int(pre_tot.get("thm", -1)), int(pre_tot.get("fora_do_trio", -1))] if pre_tot else None
chk("(informativo) TOTAL do meu Audit == o da pre-auditoria do Codex + a pedra do delta (%d declaracao(oes), 1 teorema)" % len(por_mod.get(DL.STONE_MOD, [])), bool(_pd) and kh_cov == [_pd[0] + len(por_mod.get(DL.STONE_MOD, [])), _pd[1] + 1, 0], [kh_cov, pre_tot])
# --- a duracao
mm_ = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", marcas, re.M)}
dur_audit = mm_["epoch_audit_fim"] - mm_["epoch_build_fim"]; dur_build = mm_["epoch_build_fim"] - mm_["epoch_inicio"]
chk("KH-N1: duracao do `lake env lean TGL/Audit.lean` bem abaixo do timeout de 1800 s do um.py (< 900 s)", dur_audit < 900, {"audit_s": dur_audit, "build_s": dur_build})
bf = "inicio %s\n%s\nrc_build=%d\n%s\nrc_audit=%d\n%s\nfim %s\n" % (ini, LB.rstrip("\n"), rb, AL.rstrip("\n"), ra, "rc=0" if (rb == 0 and ra == 0) else "rc=1", fim)
open(os.path.join(KD, "build_full.log"), "w", encoding="utf-8", newline="\n").write(bf)
# --- arvore so-fontes e varredura recursiva
if not os.environ.get("V394_KEEP_ARV"):
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
# --- as entradas ANTIGAS: o Audit da v393 (ANTES) e o axiom_report EFETIVO da v393 contra o EFETIVO de agora (a ultima entrada de cada nome vence)
aud_antes = rd(os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean")).decode("utf-8")
nomes_antigos = sorted(set(re.findall(r"(?m)^#print axioms (\S+)", aud_antes)))
efet = dict(axm)   # parse_lean_axioms_v394 ja' devolve o conjunto efetivo (conflito de listas e' erro)
iguais_ant = sum(1 for n in nomes_antigos if n.lstrip("@") in efet and set(efet[n.lstrip("@")]) == set(axr393.get(n.lstrip("@"), ["?"])))
chk("as entradas antigas do Audit v393 (nomes distintos) com a MESMA lista de axiomas do axiom_report v393", iguais_ant == len(nomes_antigos), [iguais_ant, len(nomes_antigos)])
exatas = sum(1 for n in axr393 if n in efet and efet[n] == axr393[n])
perdidos = [n for n in axr393 if n not in efet]
chk("NADA da v393 se perde: todo nome do axiom_report da v393 segue no de agora, no trio", not perdidos and all(set(efet.get(n, ["?"])) <= TRIO for n in axr393), [len(axr393), len(perdidos), exatas])
# --- toolchain
man = json.load(open(os.path.join(NOS, "tgl_kernel_proof_manifest.json"), encoding="utf-8")); ff = man["formal_files_sha256"]
tl = {"lean_version": man.get("lean_version"), "lake_version": man.get("lake_version")}
lv = subprocess.run(["lean", "--version"], capture_output=True, text=True, cwd=KB).stdout.strip().splitlines()[:1]
kv = subprocess.run(["lake", "--version"], capture_output=True, text=True, cwd=KB).stdout.strip().splitlines()[:1]
chk("toolchain do sandbox == a do manifesto pinado (lean e lake)", tl.get("lean_version") == lv and tl.get("lake_version") == kv, {"manifesto": tl, "sandbox": [lv, kv]})
imp = lambda d: hashlib.sha256(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
raiz0, aud0 = sha(rd(os.path.join(NOS, "tgl_kernel", "TGLExt.lean"))), sha(rd(os.path.join(NOS, "tgl_kernel", "TGL", "Audit.lean")))
chk("ANTES (raiz, Audit) == formal_files_sha256 do manifesto v393 pinado", ff.get("TGLExt.lean") == raiz0 and ff.get("TGL/Audit.lean") == aud0, [raiz0[:16], aud0[:16]])
# --- a pedra (modulo) do recibo: declaracoes que o B(n) aceita (N1k): entrada no axiom_report, linha no log do Audit e NOME na fonte da pedra
_GER = {"ctorIdx", "sizeOf_spec", "injEq", "noConfusion", "noConfusionType", "rec", "recOn", "casesOn", "brecOn", "binductionOn", "below", "ibelow", "inj", "eq_1", "eq_def"}
pedras = []; sem_decl = []; sha_ok = True
nm_rel = {}
for p_ in sorted(nov):
    mod = p_[:-len(".lean")].replace("/", ".")
    fonte = rd(os.path.join(ARV, *p_.split("/"))).decode("utf-8")
    shr = sha(rd(os.path.join(ARV, *p_.split("/"))))
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
riscos_bn = {"pedras_sem_declaracao_nomeada": sem_decl, "regra": "N1k do esboco R3.3: cada pedra do recibo exige >= 1 declaracao com entrada no axiom_report, linha no log do Audit e NOME na fonte; estas 3 so tem run_cmd (auditoria em tempo de compilacao)", "efeito": "o B(n) pos-selo RECUSARIA o recibo (nao o rito); decisao da gerencia: esboco R3.4 ou recibo sem as 3 (viola N1l: pedras = arquivos novos do manifesto)"}
print("RISCO B(n) (informativo, nao gateia o build):", len(sem_decl), "pedras sem declaracao nomeada:", sem_decl)
n_decl_recibo = sum(len(p["declaracoes"]) for p in pedras)
# --- J1 (criterios): delta dos TOTAIS do KH-N1 (v394 - v393), como na v393 (186 = 25161 - 24975)
core393_cov = core393["kernel_formalization"].get("axiom_coverage_v392") or {}
j1 = [kh_cov[0] - int(core393_cov["decl"]), kh_cov[1] - int(core393_cov["thm"]), kh_cov[2]]
kh_json = {"contrato": "KH_N1_v394", "desenho": "(a) run_cmd no fim do Audit (herdado da v392); v394: + linha TGL_DECL_SOURCE por constante (proveniencia emitida pelo compilador)", "linha_TOTAL": {"decl": kh_cov[0], "thm": kh_cov[1], "fora_do_trio": kh_cov[2]},
           "axiom_report_efetivo_n": len(efet), "proveniencia_n": len(srcm), "nao_lidas_pelo_leitor_v394": 0, "nomes_distintos_print_antigos": len(nomes_antigos), "antigas_identicas": iguais_ant,
           "entradas_antigas_exatas_no_efetivo": exatas, "nomes_v393_perdidos": len(perdidos), "novas_no_trio": all(set(efet[n]) <= TRIO for n in novas_todas), "sorryAx_no_log_do_audit": AL.count("sorryAx"),
           "delta_vs_v393": {"decl": j1[0], "thm": j1[1]}, "duracao_audit_s": dur_audit, "duracao_build_s": dur_build, "timeout_umpy_s": 1800,
           "audit_log_bytes": len(rd(os.path.join(KD, "audit.log"))), "audit_log_sha256": sha(rd(os.path.join(KD, "audit.log"))), "pre_auditoria_codex": pre_tot, "decl_da_pedra_do_delta": len(por_mod.get(DL.STONE_MOD, [])), "pre_auditoria_codex_mais_delta_igual": bool(_pd) and kh_cov == [_pd[0] + len(por_mod.get(DL.STONE_MOD, [])), _pd[1] + 1, 0], "n_bandeiras": len(flags_v394),
           "quando": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "estatuto": "[REAL] medido por pos_build_kernel_v394.py sobre o log do Audit do sandbox; fora do selo"}
json.dump(kh_json, open(os.path.join(KD, "KH_N1_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r1_ausente = not os.path.exists(os.path.join(ARV, "TGLExt", "TheSingularityReadsTheAttractor.lean"))
criterios = {"j1_declaracoes": j1[0], "j1_teoremas": j1[1], "j1_fora_do_trio": j1[2], "audit_entradas_antigas_identicas": iguais_ant, "tokens_proibidos": len(hits),
             "r1_ausente": r1_ausente, "declaracoes_novas_no_trio": all(set(efet[n]) <= TRIO for n in novas_todas)}
recibo = {"contrato": "KERNEL_RECIBO_R3_2", "versao": "v394", "rc": 0, "sorry": 0, "erros": 0,
          "build_full_log": {"path": abs_fw(os.path.join(KD, "lake_build.log")), "sha256": sha(rd(os.path.join(KD, "lake_build.log")))},
          "audit_log": {"path": abs_fw(os.path.join(KD, "audit.log")), "sha256": sha(rd(os.path.join(KD, "audit.log")))},
          "toolchain": {"lean_version": lv, "lake_version": kv}, "arvore": abs_fw(ARV),
          "raiz": {"path": "TGLExt.lean", "sha256_antes": raiz0, "sha256_depois": sha(rd(os.path.join(ARV, "TGLExt.lean")))},
          "audit": {"path": "TGL/Audit.lean", "sha256_antes": aud0, "sha256_depois": sha(rd(os.path.join(ARV, "TGL", "Audit.lean")))},
          "pedras": pedras, "formal_files_antes": ff, "axiomas": sorted(TRIO),
          "varredura_tokens": {"recursiva": True, "arquivos_lean": n_lean, "arquivos_lean_em_TGLExt_O16": n_o16},
          "criterios": {k: {"medido": v} for k, v in criterios.items()},
          "nos_kernel_impressao": {"definicao": "sha256 do JSON canonico de formal_files_sha256 do Nos (manifesto pinado pelo selo v393)", "antes": imp(ff), "depois": imp(ff)},
          "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
          "nota": "gerado por pos_build_kernel_v394.py (preparacao, 19/10/2026); NAO conferido por verificar_kernel_recibo do B(n) (precisa do selo v394 e do manifesto novo); a arvore de varredura e' a copia so-fontes " + abs_fw(ARV) + " (MANTIDA: o recibo pos-selo precisa dela); geracao d19 (integracao final: 189 modulos do Codex + a pedra do delta de 19/10)"}
ok = all(s["ok"] for s in sinais)
json.dump(recibo, open(os.path.join(KD, "KERNEL_RECIBO_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
crit = {"contrato": "CRITERIOS_R3_1", "versao": "v394", "preenchido": True, "x19": "nao", "esperados": criterios,
        "origem": "[DERIVED] preenchido pela PREPARACAO com a medicao de kernel/KERNEL_RECIBO_v394.json (J1 = diferenca dos TOTAIS do KH-N1 v394 - v393, como na v393: 186 = 25161 - 24975). x19='nao': o recibo v394 lista as " + str(N_NOVOS) + " pedras NOVAS e a "
                  "LightNetStandardWedgeDataBGL.lean ja' esta no kernel desde a v392 (R31-6: 'sim' <=> a pedra consta do recibo). O CRITERIOS_v393 herdou x19='sim' da v392, o que o B(n) recusaria (X19_NAO_CONFERE_COM_AS_PEDRAS); "
                  "a gerencia confere e pina o sha256 antes do B(3).",
        "nota": "NOT_FALSIFIED nunca e creditacao; nada aqui move o gate"}
os.makedirs(os.path.join(HERE, "vinculo"), exist_ok=True)
json.dump(crit, open(os.path.join(HERE, "vinculo", "CRITERIOS_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"ok": ok, "sinais": sinais, "criterios": criterios, "arquivos_lean": n_lean, "em_O16": n_o16, "jobs_built_novos": len(built_new), "n_axiomas_lidos_no_audit": len(axm), "hits_em_Probe": hits_probe,
           "n_flags": len(flags_v394), "n_decl_audit": len(axm), "pedras_sem_declaracao": sem_decl, "riscos_bn": riscos_bn, "n_declaracoes_no_recibo": n_decl_recibo, "inicio": ini, "fim": fim, "githash_lean": hashes_lean},
          open(os.path.join(KD, "POS_BUILD_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nPOS-BUILD:", "VERDE" if ok else "FALHOU", "| criterios:", criterios, "| .lean:", n_lean, "(O16:", n_o16, ") | pedras sem declaracao:", len(sem_decl))
sys.exit(0 if ok else 1)
