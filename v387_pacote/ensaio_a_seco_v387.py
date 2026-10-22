# -*- coding: utf-8 -*-
"""ensaio_a_seco_v387.py -- ENSAIO A SECO da v387 (molde: ensaio_a_seco_v386.py), SEM a GPU do rito e SEM o kernel do rito.
uso: python ensaio_a_seco_v387.py <candidato.py> <rotulo>
(1) copia o CANDIDATO para dry_<rotulo>/um.py e materializa ali o kernel EMBUTIDO; (2) IMPORTA o candidato (o rito NAO roda); UM_VERSION v387;
(3) o FLUXO PRINCIPAL da v387: as instrucoes do main() que COMECAM numa linha marcada v387 sao EXECUTADAS com o core da v386 selada (o canonico);
(4) testes de UNIDADE (hash errado; arquivo ausente; JSON adulterado; funcao adulterada; beta errado; verbatim adulterado; palavra proibida injetada);
(5) build_pt / build_en, pdflatex x2 -halt-on-error; DEVE/NAO_DEVE; o sumario (.toc) com as secoes novas e a da v386; a variante (V1 nao lidos) compila;
(6) o markdown canonico (carimbo v387; a linha «Ao lado (v387)»); a guarda do rito; (7) o conferidor de citacoes (estrito) com rc 0."""
import copy, hashlib, io, json, os, re, shutil, subprocess, sys, time, ast, builtins, textwrap
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
CORE0P = os.path.join(NOS, "um_absoluto.json")     # o core da v386 SELADA
cand, rot = sys.argv[1], sys.argv[2]
DRY = os.path.join(HERE, "dry_" + rot)
if os.path.isdir(DRY):
    shutil.rmtree(DRY)
os.makedirs(DRY)
shutil.copyfile(os.path.join(HERE, cand), os.path.join(DRY, "um.py"))
EMB, _, _, h16 = carregar(os.path.join(DRY, "um.py"))
for rel, content in EMB.items():
    p = os.path.join(DRY, "tgl_kernel", *rel.split("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="").write(content)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v387.json"), encoding="utf-8"))
assert CM["sha16"] == h16, "o candidato copiado nao e' o do registro"
rep = {"candidato": cand, "sha16": h16, "kernel_materializado_no_dry": len(EMB), "core0_sha16": hashlib.sha256(open(CORE0P, "rb").read()).hexdigest()[:16],
       "SINTETICO": "o core e' o da v386 selada; nenhuma GPU; nenhum kernel do rito"}
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
t0 = time.time()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
rep["import_s"] = round(time.time() - t0, 1)
assert os.path.normcase(um.FORMAL_DIR) == os.path.normcase(os.path.join(DRY, "tgl_kernel")), um.FORMAL_DIR
assert um.UM_VERSION == "v387" and um._QP_REUSE_V386 is True
R0 = json.load(open(CORE0P, encoding="utf-8"))
core0, verdict = R0["core"], R0["verdict"]
assert "the_verb_v386" in core0 and "three_stress_tests_v387" not in core0
print("import ok (%.1f s); UM_VERSION %s" % (rep["import_s"], um.UM_VERSION))
core_s = json.loads(json.dumps(core0))
_el = um.prove_external_ladder(1.0, core_s["kernel_formalization"])
rep["escada"] = [_el.get("n_theorems_clean"), _el.get("n_theorems_expected")]
assert rep["escada"] == [6137, 6137], rep["escada"]

TAG = "v387"
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][0]
lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if TAG in l}
NL = chr(10)
comeca = [st for st in main.body if st.lineno in tagged]
bad = []
for st in comeca:
    _lig = {h.name for h in ast.walk(st) if isinstance(h, ast.ExceptHandler) and h.name}
    for node in ast.walk(st):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if not (hasattr(um, node.id) or hasattr(builtins, node.id) or node.id == "core" or node.id in _lig):
                bad.append((node.lineno, node.id))
ns = dict(vars(um)); ns["core"] = core_s
code = NL.join(textwrap.dedent(NL.join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:%s>" % TAG, "exec"), ns)
    _mf_out = sys.stdout.getvalue(); _mf_err = None
except Exception as e:  # noqa
    _mf_out = sys.stdout.getvalue(); _mf_err = repr(e)
finally:
    sys.stdout = _o
c = ns["core"]
NOVAS = ["hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387", "three_stress_tests_v387"]
rep["mainflow"] = {"comeca": len(comeca), "nomes_nao_resolvidos": bad, "erro": _mf_err, "chaves_novas_no_core": sorted(k for k in c if k not in core0), "stdout": _mf_out.strip().splitlines()}
for k in NOVAS:
    rep["mainflow"][k] = {x: (c.get(k) or {}).get(x) for x in ("verdict", "all_verified", "errors")}
print("fluxo principal:", json.dumps({k: v for k, v in rep["mainflow"].items() if k != "stdout"}, ensure_ascii=False)[:3500])
mf_ok = (not bad and not _mf_err and len(comeca) == 8 and   # 4 try (os registros) + 4 print (o anuncio de cada um)
         rep["mainflow"]["chaves_novas_no_core"] == NOVAS and all((c.get(k) or {}).get("all_verified") is True for k in NOVAS)
         and str(c["hubble_ratio_v387"]["verdict"]).startswith("TGL_HUBBLE_RATIO_V387__V1_READ_BY_HASH_") and str(c["primordial_v387"]["verdict"]).startswith("TGL_PRIMORDIAL_V387__V1_READ_BY_HASH_")
         and "__KERNEL_6137_OF_6137__" in c["three_stress_tests_v387"]["verdict"] and "__NONE_OF_THE_THREE_FAILED__" in c["three_stress_tests_v387"]["verdict"] and c["three_stress_tests_v387"].get("none_of_the_three_failed") is True and c["three_stress_tests_v387"]["n_forbidden_word_as_verdict"] == 0)

# (4) testes de UNIDADE
U = {}
P9 = um._V387_FASE9_V1
_p = copy.deepcopy(P9); _p["files"]["json"]["sha256"] = "0" * 64
um._V387_FASE9_V1 = _p
try:
    _h1 = um.hubble_ratio_v387(core_s)
finally:
    um._V387_FASE9_V1 = P9
U["fase9_sha_errado"] = _h1["all_verified"] is False and "V1_NOT_READ__FILES_MISMATCH" in _h1["verdict"]
_p = copy.deepcopy(P9); _p["files"]["md"]["path"] = os.path.join(DRY, "NAO_EXISTE.md")
um._V387_FASE9_V1 = _p
try:
    _h2 = um.hubble_ratio_v387(core_s)
finally:
    um._V387_FASE9_V1 = P9
U["fase9_arquivo_ausente"] = _h2["all_verified"] is False and "V1_NOT_READ" in _h2["verdict"] and bool(_h2["errors"].get("md"))
_bj = open(P9["files"]["json"]["path"], "rb").read()
_bj2 = _bj.replace(b'"primario": 5.913', b'"primario": 9.913')
assert _bj2 != _bj
_adu = os.path.join(DRY, "V1_f9_adulterado.json"); open(_adu, "wb").write(_bj2)
_p = copy.deepcopy(P9); _p["files"]["json"].update(path=_adu, sha256=hashlib.sha256(_bj2).hexdigest(), bytes=len(_bj2))
um._V387_FASE9_V1 = _p
try:
    _h3 = um.hubble_ratio_v387(core_s)
finally:
    um._V387_FASE9_V1 = P9
U["fase9_json_adulterado_com_hash_trocado_pega_pelo_spec"] = _h3["all_verified"] is False and "SPEC_SHA256_MISMATCH" in _h3["verdict"]
_p = copy.deepcopy(P9); _p["funcao_sha256"] = "1" * 64
um._V387_FASE9_V1 = _p
try:
    _h4 = um.hubble_ratio_v387(core_s)
finally:
    um._V387_FASE9_V1 = P9
U["fase9_funcao_pinada_diferente"] = _h4["all_verified"] is False and ("HASHES_FILE_MISMATCH" in _h4["verdict"] or "FUNCTION_MISMATCH" in _h4["verdict"])
_h5 = um.hubble_ratio_v387(dict(core_s, beta=float(core_s["beta"]) * 1.01))
U["fase9_beta_errado"] = _h5["all_verified"] is False and "BETA_MISMATCH" in _h5["verdict"]
_h6 = um.hubble_ratio_v387(core_s)
U["fase9_tudo_certo"] = (_h6["all_verified"] is True and _h6["read_ok"] and _h6["funcao_ok"] and _h6["beta_ok"] and _h6["transcribed"]["BG1_H0"] == 68.531
                         and _h6["nothing_opened"] is True and "AWAITING_DATA__NOTHING_OPENED__NOT_A_CONFIRMATION__GATE_UNTOUCHED" in _h6["verdict"])
P8 = um._V387_FASE8_V1
_p = copy.deepcopy(P8); _p["files"]["hashes"]["sha256"] = "0" * 64
um._V387_FASE8_V1 = _p
try:
    _q1 = um.primordial_v387(core_s)
finally:
    um._V387_FASE8_V1 = P8
U["fase8_sha_errado"] = _q1["all_verified"] is False and "V1_NOT_READ" in _q1["verdict"]
_q2 = um.primordial_v387(core_s)
U["fase8_tudo_certo"] = (_q2["all_verified"] is True and _q2["transcribed"]["controle_D3_passou"] is True and abs(_q2["transcribed"]["delta_N_eff"] - 0.11946607525373273) < 1e-12
                         and "UNDERPOWERED_PREDETERMINED" in _q2["verdict"])
_tt = um._V387_TRES_TESTES; _tt2 = copy.deepcopy(_tt); _tt2["text"] += " "
um._V387_TRES_TESTES = _tt2
try:
    _t1 = um.three_stress_tests_v387(core_s)
finally:
    um._V387_TRES_TESTES = _tt
U["tres_testes_verbatim_adulterado"] = _t1["all_verified"] is False and _t1["verbatim"]["ok"] is False
_cf = json.loads(json.dumps(core_s)); _cf["neff_channel"]["verdict"] = "TGL_X_" + "CONF" + "IRMED"
_t2 = um.three_stress_tests_v387(_cf)
U["tres_testes_palavra_proibida_injetada"] = _t2["all_verified"] is False and _t2["n_forbidden_word_as_verdict"] == 1
_cl = json.loads(json.dumps(core_s)); _cl.pop("the_ledger_of_charges_v383")
_t3 = um.three_stress_tests_v387(_cl)
U["tres_testes_sem_livro"] = _t3["all_verified"] is False and "NOT_RECORDED_THIS_RUN__LEDGER_MISSING" in _t3["verdict"]
_pd = um._V387_POS_DICAO; _pd2 = copy.deepcopy(_pd); _pd2["text"] = _pd2["text"][:-1]
um._V387_POS_DICAO = _pd2
try:
    _r1 = um.retrodiction_reading_v387()
finally:
    um._V387_POS_DICAO = _pd
U["retro_verbatim_adulterado"] = _r1["all_verified"] is False and "VERBATIM_HASH_FAILED" in _r1["verdict"]
_cfx = json.loads(json.dumps(core_s)); _cfx["the_ledger_of_charges_v383"]["counts"]["FALSIFIED"] = 1
_t4 = um.three_stress_tests_v387(_cfx)
U["tres_testes_C1_livro_com_falsificada_diz_qual_pilar"] = _t4.get("none_of_the_three_failed") is False and "PILLARS_THAT_FAILED_RITES" in _t4["verdict"] and "NONE_OF_THE_THREE_FAILED" not in _t4["verdict"]
rep["unidade"] = U
print("unidade:", U)

# (5) o artigo
DEVE = {"pt": ["Os três testes de estresse, conjuntos", "Ao lado (v387): a razão de Hubble e a era da radiação pré-registradas", "A lei da prova",
               "estudar hipóteses para depois formular testes para saber o caminho correto do teste também não é pós-dicção", "é a própria prova diabólica do Direito",
               "retrodição sem ajuste", "periélio de Mercúrio", "A razão de Hubble (Fase 9), pré-registrada", "Nada foi aberto", "A era da radiação (Fase 8), pré-registrada",
               "TGL_HUBBLE_RATIO_V387__V1_READ_BY_HASH_", "TGL_PRIMORDIAL_V387__V1_READ_BY_HASH_", "TGL_THREE_STRESS_TESTS_V387__CORE_", "TGL_RETRODICTION_READING_V387__",
               "um só teste de estresse conjunto", "três testes de estresse conjuntos", "Ao lado (v386): o Verbo seleciona", "Nenhum dos três falhou nesta rodada (lido:", "leitura da gerência por linha, condicionada ao estado lido", "rotas do eco excluídas pelo dado, fora do livro"],
        "en": ["The three stress tests, taken together", "Beside (v387): the Hubble ratio and the radiation era preregistered", "The law of proof",
               "estudar hipóteses para depois formular testes para saber o caminho correto do teste também não é pós-dicção", "é a própria prova diabólica do Direito",
               "retrodiction without adjustment", "Mercury's perihelion", "The Hubble ratio (Phase 9), preregistered", "Nothing was opened", "The radiation era (Phase 8), preregistered",
               "TGL_HUBBLE_RATIO_V387__V1_READ_BY_HASH_", "TGL_PRIMORDIAL_V387__V1_READ_BY_HASH_", "TGL_THREE_STRESS_TESTS_V387__CORE_", "TGL_RETRODICTION_READING_V387__",
               "one joint stress test", "three joint stress tests", "Beside (v386): the Verb selects", "None of the three failed in this run (read:", "a per-row reading by the management, conditioned on the state read", "echo routes excluded by the data, outside the ledger"]}
TOC_DEVE = {"pt": ["testes de estresse", "Ao lado (v387)", "Ao lado (v386)", "Ao lado (v385)"], "en": ["stress tests, taken together", "Beside (v387)", "Beside (v386)", "Beside (v385)"]}
NAO_DEVE = {"pt": ["α²", "α^2", "alpha^2", "QG confirmada", "gravidade quântica confirmada", "pós-dição declarada; zero", "pós-dição não ajustada"],
            "en": ["α²", "α^2", "alpha^2", "QG confirmed", "quantum gravity confirmed", "declared postdiction; zero", "an unadjusted postdiction"]}
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
eng = shutil.which("pdflatex")
rep["artigo"] = {}


def compilar(cv, nome, lang, duas=True):
    tex = um._tex_guard_nan(um.build_pt(cv, verdict, CORE0P) if lang == "pt" else um.build_en(cv, verdict, CORE0P))
    txt = um._tex_to_txt(tex)
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex)
    open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = []
    for _ in range(2 if duas else 1):
        r = subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800)
        rcs.append(r.returncode)
    log = open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()
    return tex, txt, rcs, log


for lang in ("pt", "en"):
    t0 = time.time()
    tex, txt, rcs, log = compilar(c, "dry_v387_%s" % lang, lang)
    flat = re.sub(r"\s+", " ", txt)
    a = flat.find("Os três testes de estresse, conjuntos" if lang == "pt" else "The three stress tests, taken together"); b = flat.find("Ao lado (v386)" if lang == "pt" else "Beside (v386)")
    sec = flat[a:b] if (a >= 0 and b > a) else ""
    _toc_p = os.path.join(DRY, "dry_v387_%s.toc" % lang); _toc = open(_toc_p, encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(_toc_p) else ""
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v387_%s.pdf" % lang)), "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6],
                           "faltam": [w for w in DEVE[lang] if w not in flat and w not in tex], "nan": len(re.findall(r"(?<![A-Za-z])nan(?![A-Za-z])", txt)),
                           "nd_na_secao": sec.count("n/d") + sec.count("n/a"), "proibidas": [w for w in NAO_DEVE[lang] if w in (sec if w.startswith("α") or w.startswith("alpha") else flat)] + ["GUARDA:" + m.group(0) for m in GUARDA.finditer(sec)],
                           "secao_chars": len(sec), "toc_faltam": [w for w in TOC_DEVE[lang] if w not in _toc], "toc_contentsline": _toc.count("\\contentsline"),
                           "overfull": log.count("Overfull \\hbox"), "s": round(time.time() - t0, 1)}
    rep["artigo"][lang]["trecho"] = sec[:3000]
    print("artigo", lang, json.dumps({k: v for k, v in rep["artigo"][lang].items() if k != "trecho"}, ensure_ascii=False))
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["pdflatex_rc"] != [0, 0] or v["nan"] or v["proibidas"] or v["secao_chars"] < 6000 or v["toc_faltam"]]
# a variante: os dois V1 nao lidos e o registro dos tres testes ausente -- o artigo compila e diz o estado
cv = dict(copy.deepcopy(c), hubble_ratio_v387=_h1, primordial_v387=_q1)
cv.pop("three_stress_tests_v387", None)
cv["the_ledger_of_charges_v383"] = json.loads(json.dumps(c["the_ledger_of_charges_v383"])); cv["the_ledger_of_charges_v383"]["counts"]["FALSIFIED"] = 1   # C1: a frase em bloco tem de mudar
rep["variantes"] = {}
for lang in ("pt", "en"):
    _tex, _txt, _rcs, _log = compilar(cv, "dry_v387_var_%s" % lang, lang, duas=False)
    _flat = re.sub(r"\s+", " ", _txt)
    rep["variantes"][lang] = {"pdflatex_rc": _rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v387_var_%s.pdf" % lang)),
                              "diz_V1_NOT_READ": "V1_NOT_READ" in _flat, "diz_secao_contou_sozinha": "SECTION_COUNTED_ALONE" in _flat or "NOT_RECORDED_THIS_RUN" in _flat,
                              "diz_V1_nao_lido_no_texto": ("NÃO foi lido por hash" in _flat) if lang == "pt" else ("NOT read by hash" in _flat),
                              "C1_diz_qual_pilar_falhou": ("NEM TODOS os pilares passaram --- falhou: RITOS" in _flat.replace("—", "---")) if lang == "pt" else ("NOT ALL pillars passed --- failed: RITOS" in _flat.replace("—", "---"))}
print("variantes:", rep["variantes"])
mau_var = [k for k, v in rep["variantes"].items() if v["pdflatex_rc"] != [0] or not v["pdf_ok"] or not v["diz_V1_NOT_READ"] or not v["diz_secao_contou_sozinha"] or not v["diz_V1_nao_lido_no_texto"] or not v["C1_diz_qual_pilar_falhou"]]
# (6) o markdown canonico e o manifesto
um.OUT = DRY
um.emit_canonical_md(c, verdict)
md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown"] = {"carimbo": "**Versão v387**" in md, "ao_lado_v387": "Ao lado (v387, 06/10/2026)" in md, "errata_v386_fica": "Errata ao lado (v386, 05/10/2026, o operador)" in md,
                   "todos_os_modulos": "TODOS OS MODULOS COM VEREDITO" in md}
mani = os.path.join(DRY, "um_absoluto_manifest.md")
um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c)
rep["manifest"] = {"carimbo": "**Versão v387**" in open(mani, encoding="utf-8").read()}
print("markdown:", rep["markdown"], "| manifesto:", rep["manifest"])
_proib = [k for k, _m in c.items() if isinstance(_m, dict) and (GUARDA.search(str(_m.get("verdict") or "")) or "CONSCIOUSNESS_PROVED" in str(_m.get("verdict") or ""))]
rep["guarda_do_rito_vereditos_proibidos"] = _proib
# (7) as citacoes
_cc = subprocess.run([sys.executable, os.path.join(HERE, "conferir_citacoes_v387.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_do_operador"] = {"rc": _cc.returncode, "ultimas": (_cc.stdout.strip().splitlines() or [""])[-1:]}
print("citacoes:", rep["citacoes_do_operador"])
ok = (mf_ok and all(v_ is True for v_ in U.values()) and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"]["carimbo"] and not _proib
      and rep["citacoes_do_operador"]["rc"] == 0)
rep["veredito"] = "TUDO PASSOU" if ok else ("FALHOU: " + json.dumps({"fluxo": mf_ok, "unidade": {k: v for k, v in U.items() if v is not True}, "artigo": mau, "variantes": mau_var,
                                                                     "md": rep["markdown"], "mani": rep["manifest"], "proib": _proib, "citacoes_rc": rep["citacoes_do_operador"]["rc"]}, ensure_ascii=False))
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_%s.json" % rot), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"]))
sys.exit(0 if ok else 1)
