# -*- coding: utf-8 -*-
"""ensaio_a_seco_v388.py -- ENSAIO A SECO da v388 (moldes: ensaio_a_seco_v386.py / _v387.py), SEM a GPU do rito e SEM o kernel do rito.
uso: python ensaio_a_seco_v388.py <candidato.py> <rotulo>
(1) copia o candidato para dry_<rotulo>/um.py e materializa ali o kernel EMBUTIDO; (2) importa (o rito NAO roda); UM_VERSION v388; as 17 bandeiras no dicionario;
(3) o FLUXO PRINCIPAL v388 executado com o core da v387 selada + as 17 bandeiras SINTETICAS (do relatorio do kernel do sandbox) -- a escada 6137 -> 6154;
(4) testes de UNIDADE (bandeira faltando; verbatim adulterado; beta do core errado; resultado da Fase 9 adulterado; arquivo ausente; veredito nao reproduzido);
(5) build_pt/build_en, pdflatex x2; DEVE/NAO_DEVE; o sumario; a variante (registros nao lidos) compila; (6) o .md canonico; (7) o conferidor de citacoes."""
import copy, hashlib, io, json, os, re, shutil, subprocess, sys, time, ast, builtins, textwrap
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós"); CORE0P = os.path.join(NOS, "um_absoluto.json")
cand, rot = sys.argv[1], sys.argv[2]
DRY = os.path.join(HERE, "dry_" + rot)
if os.path.isdir(DRY):
    shutil.rmtree(DRY)
os.makedirs(DRY); shutil.copyfile(os.path.join(HERE, cand), os.path.join(DRY, "um.py"))
EMB, _, _, h16 = carregar(os.path.join(DRY, "um.py"))
for rel, content in EMB.items():
    p = os.path.join(DRY, "tgl_kernel", *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8", newline="").write(content)
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v388.json"), encoding="utf-8")); assert CM["sha16"] == h16
rep = {"candidato": cand, "sha16": h16, "kernel_materializado": len(EMB), "SINTETICO": "as 17 bandeiras da v388 vem do relatorio do kernel do SANDBOX (nao do rito); nenhuma GPU"}
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
assert um.UM_VERSION == "v388" and len(um._CPL_FLAGS_V388) == 17 and all(f in um._LEAN_THEOREM_FLAGS for f in um._CPL_FLAGS_V388)
R0 = json.load(open(CORE0P, encoding="utf-8")); core0, verdict = R0["core"], R0["verdict"]
assert "three_stress_tests_v387" in core0 and "beta_runs_bounded_below_v388" not in core0
core_s = json.loads(json.dumps(core0)); core_s["kernel_formalization"] = dict(core_s["kernel_formalization"], **{f: True for f in um._CPL_FLAGS_V388})
_el = um.prove_external_ladder(1.0, core_s["kernel_formalization"]); rep["escada"] = [_el.get("n_theorems_clean"), _el.get("n_theorems_expected")]
assert rep["escada"] == [CM["escada"][1]] * 2 == [6154, 6154], rep["escada"]
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][0]; lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if "v388" in l}; comeca = [st for st in main.body if st.lineno in tagged]
ns = dict(vars(um)); ns["core"] = core_s
code = "\n".join(textwrap.dedent("\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:v388>", "exec"), ns); _err = None
except Exception as e:  # noqa
    _err = repr(e)
finally:
    _mf = sys.stdout.getvalue(); sys.stdout = _o
c = ns["core"]; NOVAS = ["beta_runs_bounded_below_v388", "hubble_ratio_opening_v388"]
rep["mainflow"] = {"comeca": len(comeca), "erro": _err, "chaves_novas": sorted(k for k in c if k not in core0), "stdout": _mf.strip().splitlines()}
for k in NOVAS:
    rep["mainflow"][k] = {x: (c.get(k) or {}).get(x) for x in ("verdict", "all_verified", "errors")}
print("fluxo:", json.dumps({k: v for k, v in rep["mainflow"].items() if k != "stdout"}, ensure_ascii=False)[:2500])
_b = c.get("beta_runs_bounded_below_v388") or {}; _h = c.get("hubble_ratio_opening_v388") or {}
mf_ok = (not _err and len(comeca) == 4 and rep["mainflow"]["chaves_novas"] == NOVAS and _b.get("all_verified") is True and _h.get("all_verified") is True
         and "__KERNEL_17_OF_17__" in str(_b.get("verdict")) and _h.get("same_verdict") is True and "INCONCLUSIVE_SYSTEMATICS" in str(_h.get("verdict_of_the_frozen_function")))
U = {}
_k2 = dict(core_s["kernel_formalization"]); _k2.pop(um._CPL_FLAGS_V388[0]); _u = um.beta_runs_bounded_below_v388(dict(core_s, kernel_formalization=_k2))
U["beta_bandeira_faltando"] = _u["all_verified"] is False and "NOT_SEALED_THIS_RUN__KERNEL_16_OF_17" in _u["verdict"]
_vb = um._V388_BETA_ESCALA; _vb2 = copy.deepcopy(_vb); k0 = list(_vb2["verbatins"])[0]; _vb2["verbatins"][k0]["text"] += " "
um._V388_BETA_ESCALA = _vb2
try:
    _u = um.beta_runs_bounded_below_v388(core_s)
finally:
    um._V388_BETA_ESCALA = _vb
U["beta_verbatim_adulterado"] = _u["all_verified"] is False and "VERBATIM_FAILED" in _u["verdict"]
_u = um.beta_runs_bounded_below_v388(dict(core_s, beta=float(core_s["beta"]) * 1.01)); U["beta_core_errado"] = _u["all_verified"] is False and "BETA0_MISMATCH" in _u["verdict"]
_u = um.beta_runs_bounded_below_v388(core_s); U["beta_tudo_certo"] = _u["all_verified"] is True and _u["beta_MZ_on_shell"] > _u["beta0"] and abs(_u["beta0_vs_core_rel"]) < 1e-9
P9 = um._V388_FASE9_RES
_p = copy.deepcopy(P9); _p["files"]["resultado_json"]["sha256"] = "0" * 64
um._V388_FASE9_RES = _p
try:
    _u = um.hubble_ratio_opening_v388(core_s)
finally:
    um._V388_FASE9_RES = P9
U["fase9_sha_errado"] = _u["all_verified"] is False and "NOT_READ__FILES_MISMATCH" in _u["verdict"]
_bj = open(P9["files"]["resultado_json"]["path"], "rb").read(); _J = json.loads(_bj.decode("utf-8")); _J["primario"]["entrada_da_funcao"]["n_alvos_declarados"] = 0
_bj2 = json.dumps(_J, ensure_ascii=False, indent=1).encode("utf-8"); _adu = os.path.join(DRY, "RES_adulterado.json"); open(_adu, "wb").write(_bj2)
_p = copy.deepcopy(P9); _p["files"]["resultado_json"].update(path=_adu, sha256=hashlib.sha256(_bj2).hexdigest(), bytes=len(_bj2))
um._V388_FASE9_RES = _p
try:
    _u = um.hubble_ratio_opening_v388(core_s)
finally:
    um._V388_FASE9_RES = P9
U["fase9_entrada_adulterada_com_hash_trocado_nao_reproduz"] = _u["all_verified"] is False and "VERDICT_NOT_REPRODUCED" in _u["verdict"]
_p = copy.deepcopy(P9); _p["files"]["v1_json"]["path"] = os.path.join(DRY, "NAO_EXISTE.json")
um._V388_FASE9_RES = _p
try:
    _u = um.hubble_ratio_opening_v388(core_s)
finally:
    um._V388_FASE9_RES = P9
U["fase9_v1_ausente"] = _u["all_verified"] is False and "FILES_MISMATCH" in _u["verdict"]
_u = um.hubble_ratio_opening_v388(core_s); U["fase9_tudo_certo"] = _u["all_verified"] is True and "NOT_DISCRIMINATED_FROM_LCDM" in str(_u["counterfactual_with_sources_NOT_a_verdict"])
rep["unidade"] = U; print("unidade:", U)
DEVE = {"pt": ["Ao lado (v388):", "corre com a escala, limitado inferiormente; a Fase 9 aberta", "o valor de Betatgl é escalar, mas limitado inferiormente", "TheCouplingRunsBoundedBelow",
               "Errata ao lado:", "não o \\emph{número}", "A Fase 9 aberta.", "reexecutou", "não discriminar", "TGL_BETA_RUNS_BOUNDED_BELOW_V388__", "TGL_HUBBLE_RATIO_OPENING_V388__", "Ao lado (v387)"],
        "en": ["Beside (v388):", "runs with the scale, bounded below; Phase 9 opened", "o valor de Betatgl é escalar, mas limitado inferiormente", "TheCouplingRunsBoundedBelow",
               "Erratum beside:", "Phase 9 opened.", "re-executed", "TGL_BETA_RUNS_BOUNDED_BELOW_V388__", "TGL_HUBBLE_RATIO_OPENING_V388__", "Beside (v387)"]}
DEVE["pt"] = [w.replace("não discriminar", "não discrimina") for w in DEVE["pt"]]
TOC = {"pt": ["Ao lado (v388)", "Ao lado (v387)", "testes de estresse"], "en": ["Beside (v388)", "Beside (v387)", "stress tests, taken together"]}
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
eng = shutil.which("pdflatex"); rep["artigo"] = {}


def compilar(cv, nome, lang, duas=True):
    tex = um._tex_guard_nan(um.build_pt(cv, verdict, CORE0P) if lang == "pt" else um.build_en(cv, verdict, CORE0P)); txt = um._tex_to_txt(tex)
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex); open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = [subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800).returncode for _ in range(2 if duas else 1)]
    return tex, txt, rcs, open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()


for lang in ("pt", "en"):
    tex, txt, rcs, log = compilar(c, "dry_v388_%s" % lang, lang); flat = re.sub(r"\s+", " ", txt)
    bb = flat.rfind("Os três testes de estresse, conjuntos" if lang == "pt" else "The three stress tests, taken together"); a = flat.rfind("Ao lado (v388)" if lang == "pt" else "Beside (v388)", 0, bb)   # o cabecalho do CORPO (o titulo tambem esta no sumario)
    sec = flat[a:bb] if (a >= 0 and bb > a) else ""
    tp = os.path.join(DRY, "dry_v388_%s.toc" % lang); toc = open(tp, encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(tp) else ""
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v388_%s.pdf" % lang)), "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6],
                           "faltam": [w for w in DEVE[lang] if w not in flat and w not in tex], "nd_na_secao": sec.count("n/d") + sec.count("n/a"), "secao_chars": len(sec),
                           "guarda": [m_.group(0) for m_ in GUARDA.finditer(sec.replace("_ ", "_"))], "alpha2": [w for w in ("α²", "α^2", "alpha^2") if w in sec], "toc_faltam": [w for w in TOC[lang] if w not in toc]}
    print("artigo", lang, json.dumps(rep["artigo"][lang], ensure_ascii=False))
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["pdflatex_rc"] != [0, 0] or v["guarda"] or v["alpha2"] or v["secao_chars"] < 3000 or v["toc_faltam"] or v["nd_na_secao"]]
cv = dict(copy.deepcopy(c)); cv["hubble_ratio_opening_v388"] = {"verdict": "TGL_HUBBLE_RATIO_OPENING_V388__NOT_READ__FILES_MISMATCH__GATE_UNTOUCHED", "all_verified": False}; cv.pop("beta_runs_bounded_below_v388", None)
rep["variante"] = {}
for lang in ("pt", "en"):
    _t, _x, _r, _l = compilar(cv, "dry_v388_var_%s" % lang, lang, duas=False); fl = re.sub(r"\s+", " ", _x)
    rep["variante"][lang] = {"rc": _r, "diz_nao_reproduzido": ("NÃO foi reproduzido" in fl) if lang == "pt" else ("NOT reproduced" in fl), "diz_ausente": "AUSENTE" in fl or "ABSENT" in fl}
print("variante:", rep["variante"])
mau_var = [k for k, v in rep["variante"].items() if v["rc"] != [0] or not v["diz_nao_reproduzido"] or not v["diz_ausente"]]
um.OUT = DRY; um.emit_canonical_md(c, verdict); md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown"] = {"carimbo": "**Versão v388**" in md, "ao_lado_v388": "Ao lado (v388, 06/10/2026)" in md, "v387_fica": "Ao lado (v387, 06/10/2026)" in md}
mani = os.path.join(DRY, "um_absoluto_manifest.md"); um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c); rep["manifest"] = "**Versão v388**" in open(mani, encoding="utf-8").read()
_proib = [k for k, m_ in c.items() if isinstance(m_, dict) and GUARDA.search(str(m_.get("verdict") or ""))]
_cc = subprocess.run([sys.executable, os.path.join(HERE, "conferir_citacoes_v388.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_rc"] = _cc.returncode
ok = mf_ok and all(U.values()) and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"] and not _proib and _cc.returncode == 0
rep["veredito"] = "TUDO PASSOU" if ok else "FALHOU: " + json.dumps({"fluxo": mf_ok, "unidade": {k: v for k, v in U.items() if not v}, "artigo": mau, "variante": mau_var, "md": rep["markdown"], "mani": rep["manifest"], "proib": _proib, "cit": _cc.returncode}, ensure_ascii=False)
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_%s.json" % rot), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"])); sys.exit(0 if ok else 1)
