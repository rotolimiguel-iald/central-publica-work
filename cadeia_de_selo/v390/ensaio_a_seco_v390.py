# -*- coding: utf-8 -*-
"""ensaio_a_seco_v390.py -- ENSAIO A SECO da v390 (molde: ensaio_a_seco_v388.py), SEM a GPU do rito e SEM o kernel do rito.
uso: python ensaio_a_seco_v390.py <candidato.py> <rotulo>
(1) copia o candidato e materializa o kernel EMBUTIDO; (2) importa (o rito NAO roda); UM_VERSION v390; as 9 bandeiras no dicionario;
(3) o FLUXO PRINCIPAL v390 com o core da v389 selada + as 9 bandeiras SINTETICAS (do relatorio do kernel do sandbox) -- a escada 6154 -> 6163; e os registros da v389
(o pino do ledger recontado) e da v388 (o desenho consertado) recomputados; (4) unidade; (5) build_pt/build_en, pdflatex x2, DEVE, sumario, variante; (6) .md e manifesto;
(7) o conferidor de citacoes."""
import copy, io, json, os, re, shutil, subprocess, sys, ast, textwrap
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
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v390.json"), encoding="utf-8")); assert CM["sha16"] == h16
rep = {"candidato": cand, "sha16": h16, "kernel_materializado": len(EMB), "SINTETICO": "as 9 bandeiras da v390 vem do relatorio do kernel do SANDBOX (nao do rito); nenhuma GPU"}
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
assert um.UM_VERSION == "v390" and len(um._FND_FLAGS_V390) == 9 and all(f in um._LEAN_THEOREM_FLAGS for f in um._FND_FLAGS_V390)
R0 = json.load(open(CORE0P, encoding="utf-8")); core0, verdict = R0["core"], R0["verdict"]
assert "text_label_errata_v389" in core0 and "fundacao_v390" not in core0
core_s = json.loads(json.dumps(core0)); core_s["kernel_formalization"] = dict(core_s["kernel_formalization"], **{f: True for f in um._FND_FLAGS_V390})
_el = um.prove_external_ladder(1.0, core_s["kernel_formalization"]); rep["escada"] = [_el.get("n_theorems_clean"), _el.get("n_theorems_expected")]
assert rep["escada"] == [CM["escada"][1]] * 2 == [6163, 6163], rep["escada"]
# os registros vizinhos recomputados pela v390
_v9 = um.text_label_errata_v389(core_s); _v8 = um.beta_runs_bounded_below_v388(core_s)
rep["v389_recomputado"] = {"verdict": _v9["verdict"], "all_verified": _v9["all_verified"], "ledger": _v9["ledger"]}
rep["v388_recomputado"] = {"verdict_igual": _v8["verdict"] == core0["beta_runs_bounded_below_v388"]["verdict"], "all_verified": _v8["all_verified"], "memory_file": _v8["memory_file"]}
core_s["text_label_errata_v389"] = json.loads(json.dumps(_v9, default=str)); core_s["beta_runs_bounded_below_v388"] = json.loads(json.dumps(_v8, default=str))   # a lacuna da afericao: o artigo do ensaio usa os recomputados
viz_ok = (_v9["all_verified"] is True and _v9["verdict"] == core0["text_label_errata_v389"]["verdict"] and "LEDGER_1025_UNIQUE_PLUS_156_OUTSIDE_156_IN_O16" in _v9["verdict"]
          and _v8["all_verified"] is True and rep["v388_recomputado"]["verdict_igual"]
          and (_v8["memory_file"].get("copia_congelada") or {}).get("matches_the_pin") is True and "FORA DE QUALQUER VEREDITO" in str(_v8["memory_file"].get("estatuto_v390")))
print("vizinhos:", json.dumps({"v389": rep["v389_recomputado"]["verdict"][-160:], "v388_ok": _v8["all_verified"], "copia": _v8["memory_file"].get("copia_congelada")}, ensure_ascii=False))
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][0]; lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if "v390" in l}; comeca = [st for st in main.body if st.lineno in tagged]
ns = dict(vars(um)); ns["core"] = core_s
code = "\n".join(textwrap.dedent("\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:v390>", "exec"), ns); _err = None
except Exception as e:  # noqa
    _err = repr(e)
finally:
    _mf = sys.stdout.getvalue(); sys.stdout = _o
c = ns["core"]; NOVAS = ["fundacao_v390"]; _f = c.get("fundacao_v390") or {}
rep["mainflow"] = {"comeca": len(comeca), "erro": _err, "chaves_novas": sorted(k for k in c if k not in core0), "stdout": _mf.strip().splitlines(),
                   "fundacao_v390": {x: _f.get(x) for x in ("verdict", "all_verified", "kernel_flags_ok", "kernel_flags_total", "verbatim_ok", "borchers")}}
print("fluxo:", json.dumps({k: v for k, v in rep["mainflow"].items() if k != "stdout"}, ensure_ascii=False)[:2500])
mf_ok = (not _err and len(comeca) == 2 and rep["mainflow"]["chaves_novas"] == NOVAS and _f.get("all_verified") is True and "__AGAPE_CLAUSE_KERNEL_9_OF_9__" in str(_f.get("verdict"))
         and "BORCHERS_FORM_UNDER_NAMED_CONTRACT_H2_IN_KERNEL" in str(_f.get("verdict")) and all(x["no_kernel"] for x in _f.get("clausulas") or [{}]))
U = {}
_k2 = dict(core_s["kernel_formalization"]); _k2.pop(um._FND_FLAGS_V390[6]); _u = um.fundacao_v390(dict(core_s, kernel_formalization=_k2))
U["bandeira_faltando"] = _u["all_verified"] is False and "NOT_SEALED_THIS_RUN__KERNEL_8_OF_9" in _u["verdict"]
_vb = um._V390_VERBATINS; _vb2 = copy.deepcopy(_vb); _vb2["nomes_07out"]["text"] += " "; um._V390_VERBATINS = _vb2
try:
    _u = um.fundacao_v390(core_s)
finally:
    um._V390_VERBATINS = _vb
U["verbatim_adulterado"] = _u["all_verified"] is False and "VERBATIM_FAILED" in _u["verdict"]
_vb2 = copy.deepcopy(_vb); _vb2["cunhagem_07out"]["trechos"].append("um trecho que o operador nao escreveu"); um._V390_VERBATINS = _vb2
try:
    _u = um.fundacao_v390(core_s)
finally:
    um._V390_VERBATINS = _vb
U["trecho_inventado"] = _u["all_verified"] is False and "VERBATIM_FAILED" in _u["verdict"]
_ax = dict(core_s["kernel_formalization"]["axiom_report"]); _ax.pop(um._V390_BORCHERS[0]); _k3 = dict(core_s["kernel_formalization"], axiom_report=_ax)
_u = um.fundacao_v390(dict(core_s, kernel_formalization=_k3)); U["borchers_ausente_dito"] = _u["all_verified"] is True and "BORCHERS_FORM_UNDER_NAMED_CONTRACT_H2_NOT_READ_THIS_RUN" in _u["verdict"]
_u = um.fundacao_v390(core_s); U["tudo_certo"] = _u["all_verified"] is True and _u["kernel_flags_ok"] == 9
rep["unidade"] = U; print("unidade:", U)
DEVE = {"pt": ["A Fundação: a superposição é a passagem (a cláusula Ágape)", "não existe acima, o piso limita, tentar estar acima é cair sem fim, infinitamente",
               "esse é o fecho sim, o sistema continua aberto mas fechado logicamente", "Jacobson 1995", "Borchers", "Milburn", "TGL_FUNDACAO_V390__", "A Fundação (v390).",
               "9 de 9 declarações no trio de axiomas", "Ao lado (v389)", "fora de qualquer veredito", "abismo", "Perfeito, concordo com tudo. Magnífico", "fundus", "moto-contínuo de terceira espécie", "contrato H2", "9 de 9 declarações no kernel", "ele contara 1015 caminhos e 166 de fora", "A Parte C conta agora 1026 caminhos", "fechar o um.py"],
        "en": ["The Foundation: the superposition is the passage (the Agape clause)", "não existe acima, o piso limita, tentar estar acima é cair sem fim, infinitamente",
               "esse é o fecho sim, o sistema continua aberto mas fechado logicamente", "Jacobson 1995", "Borchers", "Milburn", "TGL_FUNDACAO_V390__", "The Foundation (v390).",
               "9 of 9 declarations within the axiom trio", "Beside (v389)", "outside every verdict", "abismo", "Perfeito, concordo com tudo. Magnífico", "fundus", "perpetual motion of the third kind", "contract H2", "9 of 9 declarations in the kernel", "it had counted 1015 paths and 166 outside", "Part C now counts 1026 unique", "to close um.py"]}
TOC = {"pt": ["A Fundação: a superposição é a passagem", "Ao lado (v389)"], "en": ["The Foundation: the superposition is the passage", "Beside (v389)"]}
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
eng = shutil.which("pdflatex"); rep["artigo"] = {}


def compilar(cv, nome, lang, duas=True):
    tex = um._tex_guard_nan(um.build_pt(cv, verdict, CORE0P) if lang == "pt" else um.build_en(cv, verdict, CORE0P)); txt = um._tex_to_txt(tex)
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex); open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = [subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800).returncode for _ in range(2 if duas else 1)]
    return tex, txt, rcs, open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()


for lang in ("pt", "en"):
    tex, txt, rcs, log = compilar(c, "dry_v390_%s" % lang, lang); flat = re.sub(r"\s+", " ", txt)
    bb = flat.rfind("O exame. Por ordem do operador" if lang == "pt" else "The exam. By the operator's order")
    a = flat.rfind("A Fundação: a superposição é a passagem" if lang == "pt" else "The Foundation: the superposition is the passage", 0, bb)
    sec = flat[a:bb] if (a >= 0 and bb > a) else ""
    tp = os.path.join(DRY, "dry_v390_%s.toc" % lang); toc = open(tp, encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(tp) else ""
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v390_%s.pdf" % lang)), "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6],
                           "faltam": [w for w in DEVE[lang] if w not in flat.replace("_ ", "_") and w not in tex], "nd_na_secao": sec.count("n/d") + sec.count("n/a"), "secao_chars": len(sec),
                           "linhas_no_kernel": sec.count("no kernel" if lang == "pt" else "in the kernel"),
                           "guarda": [m_.group(0) for m_ in GUARDA.finditer(sec.replace("_ ", "_"))], "toc_faltam": [w for w in TOC[lang] if w not in toc]}
    print("artigo", lang, json.dumps(rep["artigo"][lang], ensure_ascii=False))
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["pdflatex_rc"] != [0, 0] or v["guarda"] or v["secao_chars"] < 4000 or v["toc_faltam"] or v["nd_na_secao"] or v["linhas_no_kernel"] < 9]
cv = dict(copy.deepcopy(c)); cv.pop("fundacao_v390", None)
rep["variante"] = {}
for lang in ("pt", "en"):
    _t, _x, _r, _l = compilar(cv, "dry_v390_var_%s" % lang, lang, duas=False); fl = re.sub(r"\s+", " ", _x)
    rep["variante"][lang] = {"rc": _r, "frase_guarda": ("NÃO selou" in fl) if lang == "pt" else ("did NOT seal" in fl), "diz_ausente": "AUSENTE" in fl or "ABSENT" in fl,
                             "resumo_nao_selada": ("não selada nesta rodada" in fl) if lang == "pt" else ("not sealed in this run" in fl)}
print("variante:", rep["variante"])
mau_var = [k for k, v in rep["variante"].items() if v["rc"] != [0] or not all(v[x] for x in ("frase_guarda", "diz_ausente", "resumo_nao_selada"))]
um.OUT = DRY; um.emit_canonical_md(c, verdict); md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown"] = {"carimbo": "**Versão v390**" in md, "fundacao_v390": "A Fundação (v390, 07/10/2026)" in md, "v389_fica": "Ao lado (v389, 06/10/2026)" in md}
mani = os.path.join(DRY, "um_absoluto_manifest.md"); um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c); rep["manifest"] = "**Versão v390**" in open(mani, encoding="utf-8").read()
_proib = [k for k, m_ in c.items() if isinstance(m_, dict) and GUARDA.search(str(m_.get("verdict") or ""))]
_cc = subprocess.run([sys.executable, os.path.join(HERE, "conferir_citacoes_v390.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_rc"] = _cc.returncode
ok = viz_ok and mf_ok and all(U.values()) and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"] and not _proib and _cc.returncode == 0
rep["veredito"] = "TUDO PASSOU" if ok else "FALHOU: " + json.dumps({"vizinhos": viz_ok, "fluxo": mf_ok, "unidade": {k: v for k, v in U.items() if not v}, "artigo": mau, "variante": mau_var, "md": rep["markdown"], "mani": rep["manifest"], "proib": _proib, "cit": _cc.returncode}, ensure_ascii=False)
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_%s.json" % rot), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"])); sys.exit(0 if ok else 1)
