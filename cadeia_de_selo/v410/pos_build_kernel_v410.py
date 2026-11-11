# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] pos_build do bundle de UM modulo (IALD2): contagens e textos das checagens; KH_N1 com delta_vs_v409 (_adapt_pos_build_v410.py)
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409 -- marca herdada da v409] pos_build do bundle de UM modulo (TraducaoTuring): contagens e textos das checagens; KH_N1 com delta_vs_v408
# (v410: o bundle e' de UM modulo de TGLExt/ (IALD2); ancoras = os #print axioms da fonte normalizada, contados pelo recibo da gerencia; bandeiras ext_iald2_410_*; a origem do sandbox e' C:\t\k409c\final)
"""pos_build_kernel_v410.py -- DEPOIS de construir_kernel_v410.sh (build a FRIO do modulo novo de TGLExt/ no sandbox C:\\t\\k410c\\final): (1) monta kernel/build_full.log no formato do molde;
(2) confere o build (rc, zero erro, zero sorry nas 3 formas do contrato R3.2, 'Build completed successfully', linha BUILT (nao Replayed) do modulo novo, da raiz (TGLExt) e do Audit (TGL.Audit), axiomas no trio,
cabecalho dos .olean = Lean 4.31.0); (3) le do log do Audit (SO' dele) as linhas TGL_DECL_SOURCE (declaracao -> modulo emitido pelo compilador) e o axiom_report EFETIVO com as funcoes do PROPRIO um.py v409 selado
(parse_lean_axioms_v394/parse_lean_provenance_v394, extraidas por ast de base_v409\\um.py: a MESMA logica que o um.py v410 usara), confere as ANCORAS da pedra (delta_v410.ANCORAS) e deriva FLAGS_v410.json (as declaracoes
NOMEADAS publicas do modulo, politica da v394: UMA serie ext_tu410_NNNN, ordenada por (modulo, nome)); (4) copia a ARVORE so-fontes para C:\\t\\k410c\\arvore e varre os tokens proibidos RECURSIVAMENTE com a funcao de varredura do
PROPRIO um.py v409 (por ast); (5) mede os criterios; (6) escreve KH_N1_v410.json, KERNEL_RECIBO_v410.json (contrato KERNEL_RECIBO_R3_2: uma entrada por modulo do bundle), vinculo/CRITERIOS_v410.json (x19 = 'nao': nenhum modulo do
recibo e' a LightNetStandardWedgeDataBGL, que ja' esta no kernel desde a v392), kernel/POS_BUILD_v410.json e kernel/LOGS_COPIADOS_v410.json. A Bancada JA pina a v409 (B18): o ANTES do recibo e' o kernel da v409.
Fail-closed: cada checagem e' um sinal; falha e' REGISTRADA (nunca conserta o kernel nem os logs); saida existente ganha backup de BYTES (.bak_<data>) antes de ser substituida; escrita por temporario + os.replace.
Molde: v394/pos_build_kernel_v394.py (bundle) e v409/pos_build_kernel_v409.py (o mais recente).   Uso: python -I -B -X utf8 pos_build_kernel_v410.py"""
import ast, datetime, hashlib, json, os, re, shutil, subprocess, sys, traceback, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
KD = os.path.join(HERE, DL.KERNEL_DIR); KB = DL.SANDBOX; ARV = DL.ARVORE
BASE = os.path.join(HERE, DL.BASE_DIR)
TRIO = DL.TRIO_SET
VD = os.path.join(HERE, "vinculo")
sha = lambda b: hashlib.sha256(b).hexdigest()
rd = lambda p: open(p, "rb").read()
abs_fw = lambda p: p.replace(os.sep, "/")
sinais = []
BACKUPS = []


def chk(nome, cond, det=None, informativo=False):
    """uma checagem = um sinal; `informativo` NAO gateia o `ok` (a falha e' dita no relatorio, mas nao aborta o resto)."""
    s = {"checagem": nome, "ok": bool(cond), "detalhe": det}
    if informativo:
        s["informativo"] = True
    sinais.append(s)
    print(("OK   " if cond else ("INFO-FALHA" if informativo else "FALHA")), nome, "" if det is None else "-> " + str(det)[:240])
    return bool(cond)


def norm(t):
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    t = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", t)
    return "".join(ch for ch in unicodedata.normalize("NFKC", t) if unicodedata.category(ch) != "Cf")


def salvar(path, dados):
    """grava `dados` (bytes) por temporario + os.replace; se `path` ja' existe, copia os BYTES para .bak_<AAAAMMDD_HHMMSS> antes (regra do backup imediato); confere o tamanho."""
    if os.path.exists(path):
        bak = path + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        n = 0
        while os.path.exists(bak):
            n += 1; bak = path + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_%d" % n
        shutil.copyfile(path, bak)
        assert rd(bak) == rd(path), ("o backup nao e' copia de bytes", bak)
        BACKUPS.append(bak)
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(dados)
    assert os.path.getsize(tmp) == len(dados), ("escrita truncada", path)
    os.replace(tmp, path)
    assert os.path.getsize(path) == len(dados)


def salvar_json(path, obj):
    salvar(path, json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"))


def principal():
    os.makedirs(KD, exist_ok=True); os.makedirs(VD, exist_ok=True)
    # ------------------------------------------------------------------ as marcas e os logs (se o build nao terminou, ABORTA sem escrever nada)
    marcas = open(os.path.join(KD, "construir_marcas.txt"), encoding="utf-8").read()
    if not re.search(r"(?m)^fim .*$", marcas):
        print("ABORTA: construir_marcas.txt nao tem a linha `fim`: o build ainda nao terminou; nada foi escrito."); sys.exit(3)
    rb = int(re.search(r"rc_build=(\d+)", marcas).group(1)); ra = int(re.search(r"rc_audit=(\d+)", marcas).group(1))
    ini = re.search(r"^inicio (.*)$", marcas, re.M).group(1); fim = re.search(r"^fim (.*)$", marcas, re.M).group(1)
    mm_ = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", marcas, re.M)}
    LB_RAW = rd(os.path.join(KD, "lake_build.log")).decode("utf-8"); AL_RAW = rd(os.path.join(KD, "audit.log")).decode("utf-8")
    LB = norm(LB_RAW); AL = norm(AL_RAW)
    # ------------------------------------------------------------------ a base (v409 selada): o um.py, o core, o manifesto
    um_b = rd(os.path.join(BASE, "um.py")); um_src = um_b.decode("utf-8"); tree = ast.parse(um_src)
    fn = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    chk("a base_v409\\um.py e' a v409 SELADA (sha16 da ordem da gerencia, lido do arquivo)", sha(um_b)[:16] == DL.BASE_SHA16_DA_ORDEM, [sha(um_b)[:16], DL.BASE_SHA16_DA_ORDEM])
    _ns = {"re": re}
    for nome in ("parse_lean_provenance_v394", "parse_lean_axioms_v394"):
        exec(compile(ast.get_source_segment(um_src, fn[nome]), "<base_v409:%s>" % nome, "exec"), _ns)
    parse_ax, parse_src = _ns["parse_lean_axioms_v394"], _ns["parse_lean_provenance_v394"]
    core0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8"))["core"]; axr0 = core0["kernel_formalization"]["axiom_report"]
    cov0 = core0["kernel_formalization"].get("axiom_coverage_v392") or {}
    E0 = int(core0["external_ladder"]["n_theorems_expected"])
    nov = sorted(DL.BUNDLE_RELS); NEWRELS = set(nov); NEWMODS = {p[:-len(".lean")].replace("/", ".") for p in nov}
    N_NOVOS = len(nov)
    chk("a lista dos modulos novos (kernel_modulos_novos_v410.json) == os DOIS do delta (IALD2 e AEscala, D86), sem repeticao",
        N_NOVOS == DL.N_BUNDLE == 2 and len(NEWMODS) == 2 and sorted(json.load(open(os.path.join(HERE, "kernel_modulos_novos_v410.json"), encoding="utf-8"))["novos"]) == nov and DL.MODULO_TESTEMUNHA in NEWRELS, N_NOVOS)
    # ------------------------------------------------------------------ o build
    chk("rc do lake build == 0 e rc do Audit == 0 (marcas: rc=0)", rb == 0 and ra == 0 and bool(re.search(r"(?m)^rc=0$", marcas)), [rb, ra])
    RE_SORRY = re.compile(r"declaration\s+uses\s*[`'\u2018\u201c\"]sorry|\bsorryAx\b", re.I)
    n_err = len(re.findall(r"(?m)^error:|: error:", LB + "\n" + AL)); n_sorry = len(RE_SORRY.findall(LB + "\n" + AL)) + len(RE_SORRY.findall(re.sub(r"\s+", " ", LB + "\n" + AL)))
    chk("zero erro; zero sorry/sorryAx (formas: crase, aspas, sorryAx; com e sem quebra)", n_err == 0 and n_sorry == 0, [n_err, n_sorry])
    RE_JOB = re.compile(r"(?m)^[^\[\n]*\[\d+/\d+\][ \t]+(Built|Replayed)[ \t]+([^\s(]+)(?:[ \t]+\((\d+(?:\.\d+)?)(ms|s)\))?")
    jobs = {}
    for st, md, t_, un in RE_JOB.findall(LB):
        secs = (float(t_) * (0.001 if un == "ms" else 1.0)) if t_ else None
        jobs.setdefault(md, []).append((st, secs))
    exig = ["TGLExt", "TGL.Audit"] + sorted(NEWMODS)
    chk("linha Built/Replayed de CADA um dos %d modulos novos, da raiz (TGLExt) e do Audit (TGL.Audit)" % N_NOVOS, all(m in jobs for m in exig), [m for m in exig if m not in jobs][:5])
    chk("'Build completed successfully'", bool(re.search(r"(?m)^[ \t]*Build completed successfully\b", LB)), re.findall(r"Build completed successfully[^\n]*", LB))
    modo = {m: ("Built" if any(st == "Built" for st, _ in jobs.get(m, [])) else "Replayed" if jobs.get(m) else None) for m in sorted(NEWMODS)}
    n_built = sum(1 for v in modo.values() if v == "Built"); n_repl = sum(1 for v in modo.values() if v == "Replayed")
    chk("os %d modulos novos foram COMPILADOS neste build (linha Built, NAO Replayed): build a FRIO, como o do rito" % N_NOVOS, n_built == N_NOVOS and n_repl == 0, {"Built": n_built, "Replayed": n_repl, "ausentes": [m for m, v in modo.items() if v is None][:5]})
    built_raiz = any(st == "Built" for st, _ in jobs.get("TGLExt", [])); built_audit = any(st == "Built" for st, _ in jobs.get("TGL.Audit", []))
    chk("a raiz (TGLExt) e o Audit (TGL.Audit) foram COMPILADOS neste build (linha Built: mudou a raiz; o Audit a importa)", built_raiz and built_audit, [built_raiz, built_audit])
    tempos = [s for m in NEWMODS for st, s in jobs.get(m, []) if st == "Built" and s is not None]
    build_s_soma, build_s_max = round(sum(tempos), 3), (max(tempos) if tempos else None)
    print("INFO: soma dos tempos (NNs) das linhas Built dos %d modulos: %s s; maximo %s s (%d linhas com tempo)" % (N_NOVOS, build_s_soma, build_s_max, len(tempos)))
    LIBL = os.path.join(KB, ".lake", "build", "lib", "lean")
    hdr = {}
    for m in sorted(NEWMODS) + ["TGLExt", "TGL.Audit"]:
        p = os.path.join(LIBL, *m.split(".")) + ".olean"
        h = rd(p)[:96] if os.path.exists(p) else b""
        hdr[m] = (h[:5] == b"olean" and b"4.31.0" in h[:40], re.search(rb"[0-9a-f]{40}", h).group(0).decode() if re.search(rb"[0-9a-f]{40}", h) else None)
    hashes_lean = sorted({v[1] for v in hdr.values() if v[1]})
    chk("cabecalho de TODO .olean (%d novos + raiz + Audit): magic 'olean' e versao 4.31.0; um unico githash do Lean" % N_NOVOS, all(v[0] for v in hdr.values()) and len(hashes_lean) == 1, [len(hdr), hashes_lean, [m for m, v in hdr.items() if not v[0]][:3]])
    # ------------------------------------------------------------------ o log do Audit: leitura SO' dele (licao KH-N1) com as funcoes do um.py v409 selado
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
    cov_b = re.findall(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL[^\n]*", LB); cov_a = re.findall(r"(?m)^TGL_AXIOM_COVERAGE_TOTAL[^\n]*", AL)
    chk("a linha de cobertura do lake build e a do audit.log sao a mesma (o Audit e' compilado pelo build e rodado a parte)", bool(cov_b) and cov_b == cov_a, [cov_b[:1], cov_a[:1]])
    # ------------------------------------------------------------------ a raiz e o Audit: o sandbox == o Nos v409 selado + o import
    nos_root = rd(os.path.join(DL.NOS, "tgl_kernel", "TGLExt.lean")); nos_aud = rd(os.path.join(DL.NOS, "tgl_kernel", "TGL", "Audit.lean"))
    sb_root = rd(os.path.join(KB, "TGLExt.lean")); sb_aud = rd(os.path.join(KB, "TGL", "Audit.lean"))
    chk("a raiz do sandbox == a raiz do Nos (v409 selada) + o import do delta (ROOT_SUFFIX), em bytes", sb_root == nos_root + DL.ROOT_SUFFIX.encode("utf-8"), [len(sb_root), len(nos_root), len(DL.ROOT_SUFFIX)])
    chk("o Audit do sandbox == o Audit do Nos (bytes): o Audit NAO muda na v410", sb_aud == nos_aud, [len(sb_aud), len(nos_aud)])
    # ------------------------------------------------------------------ as ANCORAS da pedra (os #print axioms da fonte normalizada)
    anc_bad = []
    for n_, a_ in list(DL.ANCORAS.items()) + list(DL.ANCORAS_AESCALA.items()):   # (D86) as ancoras das DUAS pedras
        if not (n_ in axm and set(axm[n_]) <= TRIO and srcm.get(n_) == a_["rel"]):
            anc_bad.append([n_, n_ in axm, axm.get(n_), srcm.get(n_), a_["rel"]])
    chk("as %d ANCORAS da pedra (delta_v410.ANCORAS) existem no Audit, no trio, com proveniencia TGL_DECL_SOURCE == o modulo esperado" % (len(DL.ANCORAS) + len(DL.ANCORAS_AESCALA)), not anc_bad and len(DL.ANCORAS) == sum(len(v_) for v_ in DL.ANCORAS_POR_MODULO.values()) == DL.N_ANCORAS_ESPERADAS and len(DL.ANCORAS_AESCALA) == DL.N_ANCORAS_AESCALA, anc_bad[:3])
    # ------------------------------------------------------------------ FLAGS: a politica da v394 (so' declaracao NOMEADA); UMA serie ext_tt410_NNNN ordenada por (modulo, nome)
    por_rel = {}
    for nme, rel in srcm.items():
        if rel in NEWRELS:
            por_rel.setdefault(rel, []).append(nme)
    # (o modulo do bundle mora em TGLExt/ (nao ha subpasta nova): o invariante e' que ele NAO existia no Nos v409 e que todo modulo emitido pelo compilador fora do bundle e' ANTIGO, isto e', existe no Nos)
    nos_k = os.path.join(DL.NOS, "tgl_kernel")
    ja_no_nos = sorted(r for r in nov if os.path.exists(os.path.join(nos_k, *r.split("/"))))
    chk("nenhum dos %d modulos do bundle existia no kernel do Nos v409 (todos NOVOS: nada e' sobrescrito)" % N_NOVOS, not ja_no_nos, ja_no_nos[:3])
    fora_do_bundle = sorted(rel for rel in set(srcm.values()) if rel not in NEWRELS)
    novos_fora = [r for r in fora_do_bundle if not os.path.exists(os.path.join(nos_k, *r.split("/")))]
    chk("o compilador so' emite declaracoes dos %d modulos do bundle ou de modulos ANTIGOS (os %d fora do bundle existem todos no Nos v409)" % (N_NOVOS, len(fora_do_bundle)), not novos_fora, novos_fora[:3])
    sem_decl_prov = sorted(NEWRELS - set(por_rel))
    chk("(informativo) modulos do bundle SEM nenhuma declaracao na proveniencia do Audit (so' run_cmd/instrumentacao): %d" % len(sem_decl_prov), not sem_decl_prov, sem_decl_prov[:5], informativo=True)
    novas_todas = sorted(n for L in por_rel.values() for n in L)
    pub = sorted(n for n in novas_todas if not n.startswith("_private."))
    priv = sorted(n for n in novas_todas if n.startswith("_private."))
    nomeadas_por_rel = {rel: sorted(n for n in por_rel.get(rel, []) if not n.startswith("_private.") and DL.classe(n) == "nomeada") for rel in nov}
    aux = sorted(n for n in pub if DL.classe(n) != "nomeada")
    cl_aux = {c: sum(1 for x in aux if DL.classe(x) == c) for c, _ in DL.AUX_CLASSES}
    flags_v410 = []
    for rel in DL.BUNDLE_RELS:   # (D86) UMA serie POR MODULO, na ordem do bundle (IALD2, AEscala); dentro de cada serie, por nome (a da IALD2 nao muda)
        mod = rel[:-len(".lean")].replace("/", "."); i_ = 0
        for n in nomeadas_por_rel[rel]:
            i_ += 1; flags_v410.append(["%s%04d" % (DL.FLAG_PREFIX_POR_MODULO[rel], i_), n, mod, DL.ORIGEM_POR_MODULO[rel]])
    base_flags = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "_LEAN_THEOREM_FLAGS").value)
    chk("as chaves das flags novas (%s*) nao colidem com as da base v409 (_LEAN_THEOREM_FLAGS) e sao unicas; os NOMES nao repetem os de uma bandeira existente e sao unicos" % DL.FLAG_PREFIX,
        len({f[0] for f in flags_v410}) == len(flags_v410) and not ({f[0] for f in flags_v410} & set(base_flags)) and not ({f[1] for f in flags_v410} & set(base_flags.values())) and len({f[1] for f in flags_v410}) == len(flags_v410), len(flags_v410))
    chk("toda bandeira nova esta no axiom_report, no trio, e e' declaracao NOMEADA publica (a politica)", all(f[1] in axm and set(axm[f[1]]) <= TRIO and DL.classe(f[1]) == "nomeada" and not f[1].startswith("_private.") for f in flags_v410), len(flags_v410))
    reatribuidas = {n: {"antes": (core0["kernel_formalization"].get("declaration_sources_v394") or {}).get(n), "agora": srcm[n]} for n in novas_todas if n in axr0}
    novas_reais = [n for n in novas_todas if n not in axr0]
    chk("declaracoes NOVAS dos modulos novos (publicas + privadas, por proveniencia, menos as reatribuidas) == TOTAL(v410) - TOTAL(v409); as reatribuidas sao auxiliares (sem bandeira)",
        bool(m_cov) and len(novas_reais) == kh_cov[0] - int(cov0.get("decl", -1)) and all(DL.classe(n) != "nomeada" for n in reatribuidas), [len(novas_reais), kh_cov[0] if kh_cov else None, cov0.get("decl"), list(reatribuidas)[:3]])
    chk("os nomes do axiom_report da v409 (core da base) seguem todos no axiom_report de agora (nada se perde), com a MESMA lista", all(n in axm and axm[n] == axr0[n] for n in axr0), [len(axr0), sum(1 for n in axr0 if n not in axm)])
    chk("o axiom_report de agora tem exatamente os nomes da v409 mais as declaracoes dos modulos novos", set(axm) == set(axr0) | set(novas_todas), [len(axm), len(axr0), len(novas_todas)])
    chave_de = {f[1]: f[0] for f in flags_v410}
    anc_info = {n_: {"flag": chave_de.get(n_), "rel": srcm.get(n_), "axioms": axm.get(n_), "classe": DL.classe(n_)} for n_ in list(DL.ANCORAS) + list(DL.ANCORAS_AESCALA)}
    bandeira_testemunha = {DL.ANCORA_TESTEMUNHA_TEOREMA: chave_de.get(DL.ANCORA_TESTEMUNHA_TEOREMA), DL.ANCORA_TESTEMUNHA: chave_de.get(DL.ANCORA_TESTEMUNHA)}
    chk("a ancora principal (o_enunciado) e a da conjuncao IALD2 (iald2) tem bandeira; as %d ancoras principais (a principal e as de secao) tem bandeira" % len(DL.ANCORAS_PRINCIPAIS), all(bandeira_testemunha.values()) and all(chave_de.get(n_) for n_ in DL.ANCORAS_PRINCIPAIS), bandeira_testemunha)
    chk("(D86) as %d ancoras da AEscala tem bandeira da serie %s (a principal, a_escala, e as 6 de secao entre elas); as da IALD2 seguem na serie %s" % (len(DL.ANCORAS_AESCALA), DL.FLAG_PREFIX_AESCALA, DL.FLAG_PREFIX),
        all((chave_de.get(n_) or "").startswith(DL.FLAG_PREFIX_AESCALA) for n_ in DL.ANCORAS_AESCALA) and all(chave_de.get(n_) for n_ in DL.ANCORAS_PRINCIPAIS_AESCALA) and all((chave_de.get(n_) or DL.FLAG_PREFIX).startswith(DL.FLAG_PREFIX) for n_ in DL.ANCORAS), [n_ for n_ in DL.ANCORAS_AESCALA if not chave_de.get(n_)][:3])
    n_por_modulo = {rel: len(nomeadas_por_rel[rel]) for rel in nov}
    salvar_json(os.path.join(KD, "FLAGS_v410.json"), {
        "politica": "so' declaracao NOMEADA tem bandeira (a pratica selada da v392 a v409); as auxiliares geradas pelo compilador (ultimo componente _proof_N, _simp_N, match_N, _sunfold, eq_N, eq_def, congr_simp) ficam fora; "
                    "UMA serie de chaves POR MODULO (%s), ordenada por nome, para os %d modulos do bundle de TGLExt/ (v410: IALD2, 06/11; AEscala, 09/11, D86; o numero e' MEDIDO do Audit desta geracao)" % (", ".join(p_ + "NNNN" for p_ in DL.FLAG_PREFIX_POR_MODULO.values()), N_NOVOS),
        "flags": flags_v410, "n_flags": len(flags_v410), "n_decl_audit": len(axm), "por_origem": {DL.ORIGEM_POR_MODULO[rel_]: len(nomeadas_por_rel[rel_]) for rel_ in DL.BUNDLE_RELS}, "por_grupo_bandeiras": {DL.GRUPO_POR_MODULO[rel_]: len(nomeadas_por_rel[rel_]) for rel_ in DL.BUNDLE_RELS}, "prefixos": dict(DL.FLAG_PREFIX_POR_MODULO),
        "excluidas_auxiliares": {"n": len(aux), "por_classe": cl_aux, "nomes": aux},
        "publicas_no_modulo": len(pub), "privadas_no_modulo": len(priv), "decl_totais_modulos_novos": len(novas_todas), "decl_novas_dos_modulos": len(novas_reais), "reatribuidas_as_pedras": reatribuidas,
        "proveniencia_publicas": {n: srcm[n] for n in pub}, "n_por_modulo": n_por_modulo, "ancoras": anc_info, "bandeira_da_testemunha": bandeira_testemunha})
    # ------------------------------------------------------------------ a duracao e o build_full.log
    dur_audit = mm_["epoch_audit_fim"] - mm_.get("epoch_audit_inicio", mm_["epoch_build_fim"]); dur_build = mm_["epoch_build_fim"] - mm_["epoch_inicio"]   # (v410: o Audit refeito depois da queda de energia mede a propria rodada)
    chk("KH-N1: duracao do `lake env lean TGL/Audit.lean` bem abaixo do timeout de 1800 s do um.py (< 900 s)", dur_audit < 900, {"audit_s": dur_audit, "build_s": dur_build})
    chk("(informativo) duracao do `lake build` a frio do modulo novo < 2400 s", dur_build < 2400, {"build_s": dur_build}, informativo=True)
    bf = "inicio %s\n%s\nrc_build=%d\n%s\nrc_audit=%d\n%s\nfim %s\n" % (ini, LB.rstrip("\n"), rb, AL.rstrip("\n"), ra, "rc=0" if (rb == 0 and ra == 0) else "rc=1", fim)
    salvar(os.path.join(KD, "build_full.log"), bf.encode("utf-8"))
    # ------------------------------------------------------------------ arvore so-fontes e varredura recursiva
    if os.path.isdir(ARV):
        shutil.rmtree(ARV)
    os.makedirs(ARV)
    ign = shutil.ignore_patterns("*.bak*")
    for rel in ("TGL", "TGLExt"):
        shutil.copytree(os.path.join(KB, rel), os.path.join(ARV, rel), copy_function=shutil.copy2, ignore=ign)
    for f in os.listdir(KB):
        p = os.path.join(KB, f)
        if os.path.isfile(p) and ".bak" not in f:
            shutil.copy2(p, os.path.join(ARV, f))
    ns = {"re": re, "os": os}
    assert "_lean_strip_comments_and_strings" in fn
    exec(compile(ast.get_source_segment(um_src, fn["_lean_strip_comments_and_strings"]), "<um.strip>", "exec"), ns)
    TOKS = [ast.literal_eval(ast.get_source_segment(um_src, n.value)) for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_LEAN_FORBIDDEN_TOKENS"][0]
    n_lean = n_o16 = 0; hits = []; hits_probe = []; links = []; bak_na_arvore = []
    pilha = [ARV]
    while pilha:
        d = pilha.pop()
        with os.scandir(d) as it:
            for e in it:
                if ".bak" in e.name:
                    bak_na_arvore.append(e.path)
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
    chk("arvore so-fontes sem juncao/link e sem .bak", not links and not bak_na_arvore, [links[:3], bak_na_arvore[:3]])
    chk("varredura de tokens proibidos RECURSIVA: zero hits (probes diagnosticos a parte)", not hits, {"hits": hits[:5], "hits_em_Probe": hits_probe[:5], "arquivos_lean": n_lean, "em_TGLExt_O16": n_o16, "tokens": TOKS})
    arv_ok = all(rd(os.path.join(ARV, *r.split("/"))) == rd(os.path.join(KB, *r.split("/"))) for r in ("TGLExt.lean", "TGL/Audit.lean")) and all(os.path.exists(os.path.join(ARV, *r.split("/"))) for r in nov)
    chk("a arvore tem os %d modulos novos e a raiz e o Audit identicos aos do sandbox" % N_NOVOS, arv_ok, N_NOVOS)
    # ------------------------------------------------------------------ as entradas ANTIGAS: o Audit da v409 (ANTES) e o axiom_report EFETIVO da v409 contra o EFETIVO de agora
    emb0 = ast.literal_eval(next(n for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", None) == "_EMBEDDED_KERNEL_FILES").value)
    aud_antes = emb0["TGL/Audit.lean"]
    nomes_antigos = sorted(set(re.findall(r"(?m)^#print axioms (\S+)", aud_antes)))
    iguais_ant = sum(1 for n in nomes_antigos if n.lstrip("@") in axm and set(axm[n.lstrip("@")]) == set(axr0.get(n.lstrip("@"), ["?"])))
    chk("as entradas antigas do Audit v409 (nomes distintos) com a MESMA lista de axiomas do axiom_report v409", iguais_ant == len(nomes_antigos) and len(nomes_antigos) > 0, [iguais_ant, len(nomes_antigos)])
    exatas = sum(1 for n in axr0 if n in axm and axm[n] == axr0[n]); perdidos = [n for n in axr0 if n not in axm]
    chk("NADA da v409 se perde: todo nome do axiom_report da v409 segue no de agora, no trio", not perdidos and all(set(axm.get(n, ["?"])) <= TRIO for n in axr0), [len(axr0), len(perdidos), exatas])
    # ------------------------------------------------------------------ toolchain e o manifesto pinado
    man = json.load(open(os.path.join(BASE, "tgl_kernel_proof_manifest.json"), encoding="utf-8")); ff = man["formal_files_sha256"]
    tl = {"lean_version": man.get("lean_version"), "lake_version": man.get("lake_version")}
    elan = os.path.join(os.path.expanduser("~"), ".elan", "bin")
    exe = lambda nome_: shutil.which(nome_) or os.path.join(elan, nome_ + ".exe")
    lv = subprocess.run([exe("lean"), "--version"], capture_output=True, text=True, cwd=KB).stdout.strip().splitlines()[:1]
    kv = subprocess.run([exe("lake"), "--version"], capture_output=True, text=True, cwd=KB).stdout.strip().splitlines()[:1]
    chk("toolchain do sandbox == a do manifesto pinado (lean e lake)", tl.get("lean_version") == lv and tl.get("lake_version") == kv, {"manifesto": tl, "sandbox": [lv, kv]})
    imp = lambda d: hashlib.sha256(json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    raiz0, aud0 = sha(nos_root), sha(nos_aud)
    chk("ANTES (raiz, Audit) == formal_files_sha256 do manifesto v409 pinado (e == o embutido no um.py da base)", ff.get("TGLExt.lean") == raiz0 == sha(emb0["TGLExt.lean"].encode("utf-8")) and ff.get("TGL/Audit.lean") == aud0 == sha(aud_antes.encode("utf-8")), [raiz0[:16], aud0[:16]])
    # ------------------------------------------------------------------ os modulos (pedras) do recibo: declaracoes que o B(n) aceita (N1k): entrada no axiom_report, linha no log do Audit e NOME na fonte
    pedras = []; sem_decl = []; sha_bad = []
    for p_ in nov:
        fb = rd(os.path.join(ARV, *p_.split("/"))); fonte = fb.decode("utf-8"); shr = sha(fb)
        if shr != DL.BUNDLE_POR_REL[p_]["sha256"]:
            sha_bad.append(p_)
        decl = []
        for n in por_rel.get(p_, []):
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
    chk("o sha256 de cada um dos %d modulos na arvore == o que o preparo do bundle pinou (BUNDLE_v410.json)" % N_NOVOS, not sha_bad, sha_bad[:3])
    riscos_bn = {"pedras_sem_declaracao_nomeada": sem_decl, "regra": "N1k do esboco R3.3: cada pedra do recibo exige >= 1 declaracao com entrada no axiom_report, linha no log do Audit e NOME na fonte", "efeito": "o B(n) pos-selo RECUSARIA o recibo (nao o rito) se houver modulo sem declaracao aceita"}
    print("RISCO B(n) (informativo, nao gateia o build):", len(sem_decl), "modulos sem declaracao aceita:", sem_decl[:10])
    n_decl_recibo = sum(len(p["declaracoes"]) for p in pedras)
    chk("(informativo) cada modulo do recibo tem >= 1 declaracao aceita (N1k do B(n)): %d sem" % len(sem_decl), not sem_decl, sem_decl[:5], informativo=True)
    # ------------------------------------------------------------------ J1 e os criterios
    j1 = [kh_cov[0] - int(cov0["decl"]), kh_cov[1] - int(cov0["thm"]), kh_cov[2]] if kh_cov else [None, None, None]
    kh_json = {"contrato": "KH_N1_v401", "desenho": "(a) run_cmd no fim do Audit (herdado da v392); (b) linha TGL_DECL_SOURCE por constante (proveniencia emitida pelo compilador, v396)", "linha_TOTAL": {"decl": kh_cov[0], "thm": kh_cov[1], "fora_do_trio": kh_cov[2]} if kh_cov else None,
               "axiom_report_efetivo_n": len(axm), "proveniencia_n": len(srcm), "nao_lidas_pelo_leitor_v394": 0, "nomes_distintos_print_antigos": len(nomes_antigos), "antigas_identicas": iguais_ant,
               "entradas_antigas_exatas_no_efetivo": exatas, "nomes_v409_perdidos": len(perdidos), "novas_no_trio": all(set(axm[n]) <= TRIO for n in novas_todas), "sorryAx_no_log_do_audit": AL.count("sorryAx"),
               "delta_vs_v409": {"decl": j1[0], "thm": j1[1]}, "duracao_audit_s": dur_audit, "duracao_build_s": dur_build, "timeout_umpy_s": 1800,
               "audit_log_bytes": len(rd(os.path.join(KD, "audit.log"))), "audit_log_sha256": sha(rd(os.path.join(KD, "audit.log"))), "n_bandeiras": len(flags_v410), "decl_dos_modulos_novos": len(novas_todas), "decl_novas_dos_modulos": len(novas_reais), "reatribuidas_as_pedras": reatribuidas,
               "build_modulos_s_soma": build_s_soma, "build_modulos_s_max": build_s_max, "n_modulos_novos": N_NOVOS,
               "quando": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "estatuto": "[REAL] medido por pos_build_kernel_v410.py sobre o log do Audit do sandbox; fora do selo"}
    salvar_json(os.path.join(KD, "KH_N1_v410.json"), kh_json)
    r1_ausente = not os.path.exists(os.path.join(ARV, "TGLExt", "TheSingularityReadsTheAttractor.lean"))
    criterios = {"j1_declaracoes": j1[0], "j1_teoremas": j1[1], "j1_fora_do_trio": j1[2], "audit_entradas_antigas_identicas": iguais_ant, "tokens_proibidos": len(hits),
                 "r1_ausente": r1_ausente, "declaracoes_novas_no_trio": all(set(axm[n]) <= TRIO for n in novas_todas)}
    x19 = "sim" if any(p["path"].endswith("/LightNetStandardWedgeDataBGL.lean") for p in pedras) else "nao"
    chk("x19 = 'nao': nenhum dos %d modulos do recibo e' a LightNetStandardWedgeDataBGL (R31-6: 'sim' <=> a pedra consta do recibo)" % N_NOVOS, x19 == "nao", x19)
    # ------------------------------------------------------------------ os logs copiados (o construir_kernel_v410.sh escreve DIRETO em kernel\: nada e' copiado, so' CONFERIDO e pinado)
    logs_cop = {}
    for nome in ("lake_build.log", "audit.log", "construir_marcas.txt"):
        b = rd(os.path.join(KD, nome)); logs_cop[nome] = {"bytes": len(b), "sha256": sha(b), "origem": os.path.join(KD, nome), "copiado": False}
    logs_cop["cobertura_linha"] = cov_a
    salvar_json(os.path.join(KD, "LOGS_COPIADOS_v410.json"), logs_cop)
    rc_med = 0 if (rb == 0 and ra == 0) else (rb or ra)
    recibo = {"contrato": "KERNEL_RECIBO_R3_2", "versao": "v410", "rc": rc_med, "sorry": n_sorry, "erros": n_err,
              "build_full_log": {"path": abs_fw(os.path.join(KD, "lake_build.log")), "sha256": sha(rd(os.path.join(KD, "lake_build.log")))},
              "audit_log": {"path": abs_fw(os.path.join(KD, "audit.log")), "sha256": sha(rd(os.path.join(KD, "audit.log")))},
              "toolchain": {"lean_version": lv, "lake_version": kv}, "arvore": abs_fw(ARV),
              "raiz": {"path": "TGLExt.lean", "sha256_antes": raiz0, "sha256_depois": sha(rd(os.path.join(ARV, "TGLExt.lean")))},
              "audit": {"path": "TGL/Audit.lean", "sha256_antes": aud0, "sha256_depois": sha(rd(os.path.join(ARV, "TGL", "Audit.lean")))},
              "pedras": pedras, "formal_files_antes": ff, "axiomas": sorted(TRIO),
              "varredura_tokens": {"recursiva": True, "arquivos_lean": n_lean, "arquivos_lean_em_TGLExt_O16": n_o16},
              "criterios": {k: {"medido": v} for k, v in criterios.items()},
              "nos_kernel_impressao": {"definicao": "sha256 do JSON canonico de formal_files_sha256 do Nos (manifesto pinado pelo selo v409)", "antes": imp(ff), "depois": imp(ff)},
              "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
              "nota": "gerado por pos_build_kernel_v410.py (preparacao, 06/11/2026); NAO conferido por verificar_kernel_recibo do B(n) (precisa do selo v410 e do manifesto novo); a arvore de varredura e' a copia so-fontes " + abs_fw(ARV) + " (MANTIDA: o recibo pos-selo precisa dela); "
                      "o build do sandbox C:/t/k410c/final foi INCREMENTAL no que e' antigo (copia de C:/t/k409c/final, o kernel da v409 compilado, com as fontes conferidas por sha256 contra o Nos v409) e A FRIO no(s) " + str(N_NOVOS) + " modulo(s) novo(s) (IALD2 e AEscala; linha Built); logs em kernel\\; o rito real do Nos compila tudo a frio"}
    ok = all(s["ok"] for s in sinais if not s.get("informativo"))
    salvar_json(os.path.join(KD, "KERNEL_RECIBO_v410.json"), recibo)
    crit = {"contrato": "CRITERIOS_R3_1", "versao": "v410", "preenchido": True, "x19": x19, "esperados": criterios,
            "origem": "[DERIVED] preenchido pela PREPARACAO com a medicao de kernel/KERNEL_RECIBO_v410.json (J1 = diferenca dos TOTAIS do KH-N1 v410 - v409, como na v393, v394, v396, v404, v406 e v409). x19='nao': o recibo v410 lista o(s) " + str(N_NOVOS) + " modulo(s) NOVO(s) de TGLExt/ (IALD2) e a "
                      "LightNetStandardWedgeDataBGL.lean ja' esta no kernel desde a v392 (R31-6: 'sim' <=> a pedra consta do recibo); a gerencia confere e pina o sha256 antes do B(n).",
            "nota": "NOT_FALSIFIED nunca e creditacao; nada aqui move o gate"}
    salvar_json(os.path.join(VD, "CRITERIOS_v410.json"), crit)
    pos = {"ok": ok, "sinais": sinais, "criterios": criterios, "arquivos_lean": n_lean, "em_O16": n_o16, "modo_da_pedra_no_build": modo, "modos_contagem": {"Built": n_built, "Replayed": n_repl}, "n_axiomas_lidos_no_audit": len(axm), "hits_em_Probe": hits_probe,
           "n_flags": len(flags_v410), "n_decl_audit": len(axm), "pedras_sem_declaracao": sem_decl, "riscos_bn": riscos_bn, "n_declaracoes_no_recibo": n_decl_recibo, "inicio": ini, "fim": fim, "githash_lean": hashes_lean, "E409": E0,
           "duracao_build_s": dur_build, "duracao_audit_s": dur_audit, "build_modulos_s_soma": build_s_soma, "build_modulos_s_max": build_s_max, "ancoras": anc_info, "x19": x19,
           "falhas": [s["checagem"] for s in sinais if not s["ok"] and not s.get("informativo")], "falhas_informativas": [s["checagem"] for s in sinais if not s["ok"] and s.get("informativo")], "backups": BACKUPS}
    salvar_json(os.path.join(KD, "POS_BUILD_v410.json"), pos)
    print("\nPOS-BUILD:", "VERDE" if ok else "FALHOU", "| criterios:", criterios, "| .lean:", n_lean, "| bandeiras:", len(flags_v410), "| escada esperada:", E0 + len(flags_v410), "| TOTAL:", kh_cov, "| delta_vs_v409:", j1[:2],
          "| build_s:", dur_build, "audit_s:", dur_audit, "| ancoras:", "ok" if not anc_bad else "FALHA", "| falhas:", pos["falhas"], "| falhas informativas:", pos["falhas_informativas"])
    return ok


if __name__ == "__main__":
    try:
        r = principal()
    except SystemExit:
        raise
    except Exception:
        tb = traceback.format_exc(); print("EXCECAO (fail-closed):\n" + tb)
        try:
            salvar_json(os.path.join(KD, "POS_BUILD_v410.json"), {"ok": False, "excecao": tb, "sinais": sinais, "backups": BACKUPS})
        except Exception:
            pass
        sys.exit(2)
    sys.exit(0 if r else 1)
