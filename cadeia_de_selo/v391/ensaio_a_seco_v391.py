# -*- coding: utf-8 -*-
"""ensaio_a_seco_v391.py -- ENSAIO A SECO da v391 (molde: ensaio_a_seco_v390.py), SEM a GPU do rito e SEM o kernel do rito.
uso: python ensaio_a_seco_v391.py <candidato.py> <rotulo>
(1) copia o candidato; (2) importa (o rito NAO roda); UM_VERSION v391; (3) os registros vizinhos recomputados com o core da v390 selada (a v389 le o sucessor
do titulo; a v390 igual); (4) o FLUXO PRINCIPAL v391; (5) unidade (verbatim adulterado; rito falsificado; GPU com discordancia; leitura faltando);
(6) build_pt/build_en, pdflatex x2, DEVE, sumario, variante sem o registro; (7) .md e manifesto; (8) o conferidor de citacoes."""
import copy, io, json, os, re, shutil, subprocess, sys, ast, textwrap
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(HERE); sys.path.insert(0, os.path.join(WK, "v390_pacote"))
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
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v391.json"), encoding="utf-8")); assert CM["sha16"] == h16
rep = {"candidato": cand, "sha16": h16, "kernel_materializado": len(EMB), "SEM_GPU_SEM_KERNEL": "o core da v390 selada; nenhum kernel novo nesta versao"}
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
assert um.UM_VERSION == "v391"
R0 = json.load(open(CORE0P, encoding="utf-8")); core0, verdict = R0["core"], R0["verdict"]
assert "fundacao_v390" in core0 and "estatuto_da_prova_v391" not in core0
core_s = json.loads(json.dumps(core0))
_el = um.prove_external_ladder(1.0, core_s["kernel_formalization"]); rep["escada"] = [_el.get("n_theorems_clean"), _el.get("n_theorems_expected")]
assert rep["escada"] == [6163, 6163], rep["escada"]
_v9 = um.text_label_errata_v389(core_s); _v0 = um.fundacao_v390(core_s)
rep["v389_recomputado"] = {"verdict_igual": _v9["verdict"] == core0["text_label_errata_v389"]["verdict"], "all_verified": _v9["all_verified"],
                           "titulo": [x for x in _v9["text_sites"] if x["id"] in ("T02_intro_PT", "T03_intro_EN")]}
rep["v390_recomputado"] = {"verdict_igual": _v0["verdict"] == core0["fundacao_v390"]["verdict"], "all_verified": _v0["all_verified"]}
viz_ok = _v9["all_verified"] is True and rep["v389_recomputado"]["verdict_igual"] and _v0["all_verified"] is True and rep["v390_recomputado"]["verdict_igual"]
print("vizinhos:", json.dumps({"v389": rep["v389_recomputado"]["verdict_igual"], "v390": rep["v390_recomputado"]["verdict_igual"], "titulo": rep["v389_recomputado"]["titulo"]}, ensure_ascii=False)[:900])
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][0]; lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if "v391" in l}; comeca = [st for st in main.body if st.lineno in tagged]
ns = dict(vars(um)); ns["core"] = core_s
code = "\n".join(textwrap.dedent("\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:v391>", "exec"), ns); _err = None
except Exception as e:  # noqa
    _err = repr(e)
finally:
    _mf = sys.stdout.getvalue(); sys.stdout = _o
c = ns["core"]; NOVAS = ["estatuto_da_prova_v391"]; _f = c.get("estatuto_da_prova_v391") or {}
rep["mainflow"] = {"comeca": len(comeca), "erro": _err, "chaves_novas": sorted(k for k in c if k not in core0), "stdout": _mf.strip().splitlines(),
                   "estatuto": {x: _f.get(x) for x in ("verdict", "all_verified", "falhas")}}
print("fluxo:", json.dumps({k: v for k, v in rep["mainflow"].items() if k != "stdout"}, ensure_ascii=False)[:2500])
V = str(_f.get("verdict"))
mf_ok = (not _err and len(comeca) == 2 and rep["mainflow"]["chaves_novas"] == NOVAS and _f.get("all_verified") is True
         and all(t in V for t in ("__PROVED_AS_LOGICAL_CLOSURE__", "KERNEL_6163_OF_6163", "RITES_11_CHARGES_0_FALSIFIED", "HUBBLE_RATIO_LNB_LCDM_P9P17_ZDISC_P4P28_OFFICIAL_INCONCLUSIVE_SYSTEMATICS",
                                     "GPU_T2_672_OF_672_T4_21100_CPU_0_DISAGREEMENTS", "CONFIRMATION_IS_CREDITATION_NOT_VALIDITY_NOT_DECLARED", "CERTIFIED_BY_SELF_HASH_" + h16)))
U = {}
_vb = um._V391_VERBATIM; _vb2 = copy.deepcopy(_vb); _vb2["text"] += " "; um._V391_VERBATIM = _vb2
try:
    _u = um.estatuto_da_prova_v391(core_s)
finally:
    um._V391_VERBATIM = _vb
U["verbatim_adulterado"] = _u["all_verified"] is False and "NOT_SEALED_THIS_RUN__VERBATIM" in _u["verdict"]
_c2 = copy.deepcopy(core_s); _c2["the_ledger_of_charges_v383"]["counts"]["FALSIFIED"] = 1; _c2["the_ledger_of_charges_v383"]["counts"]["NOT_FALSIFIED"] -= 1
_u = um.estatuto_da_prova_v391(_c2); U["rito_falsificado"] = _u["all_verified"] is False and "RITE_FALSIFIED_1" in _u["verdict"] and "PROVED" not in _u["verdict"]
_c3 = copy.deepcopy(core_s); _c3["three_stress_tests_v387"]["gpu"]["cpuref_disagreements"] = 2
_u = um.estatuto_da_prova_v391(_c3); U["gpu_discorda"] = _u["all_verified"] is False and "GPU" in _u["falhas"]
_c4 = copy.deepcopy(core_s); _c4.pop("hubble_ratio_opening_v388")
_u = um.estatuto_da_prova_v391(_c4); U["leitura_faltando"] = _u["all_verified"] is False and "RITES_READ" in _u["falhas"]
_c5 = copy.deepcopy(core_s); _c5["void_floor_v11"]["verdict"] = "TGL_VOID_FLOOR_INCONCLUSIVE_SYSTEMATICS"
_u = um.estatuto_da_prova_v391(_c5); U["piso_nao_powered"] = _u["all_verified"] is False and "RITES_READ" in _u["falhas"]
_c6 = copy.deepcopy(core_s); _c6["external_ladder"]["n_theorems_clean"] = 6162
_u = um.estatuto_da_prova_v391(_c6); U["kernel_nao_fecha"] = _u["all_verified"] is False and "KERNEL" in _u["falhas"]
_u = um.estatuto_da_prova_v391(core_s); U["tudo_certo"] = _u["all_verified"] is True and not _u["falhas"]
rep["unidade"] = U; print("unidade:", U)
DEVE = {"pt": ["O estatuto da prova: provada; a confirmação recusada é creditação, não validade", "O estatuto da prova (v391).", "eu não proibí a máquina de dizer provado hora nenhuma",
               "a confirmação que eu proibi é de creditação e não de validade", "6163 de 6163 teoremas limpos", "11 cobranças no livro", "672 de 672", "21100 instâncias",
               "0 discordâncias em 392", "Errata ao lado (v391): as frases de época", "Mercúrio", "teste unilateral", "INCONCLUSIVE", "Introdução: o que este código faz agora (v384 a v391",
               "A Fundação (v390).", "A certificação é o próprio código", "provada"],
        "en": ["The status of the proof: proved; the refused confirmation is accreditation, not validity", "The status of the proof (v391).", "eu não proibí a máquina de dizer provado hora nenhuma",
               "a confirmação que eu proibi é de creditação e não de validade", "6163 of 6163 clean theorems", "11 charges in the ledger", "672 of 672", "21100 stress instances",
               "0 disagreements in 392", "Erratum beside (v391): the period sentences", "Mercury", "one-sided test", "INCONCLUSIVE", "Introduction: what this code does now (v384 to v391",
               "The Foundation (v390).", "The certification is the code itself", "proved"]}
TOC = {"pt": ["O estatuto da prova: provada", "v384 a v391", "A Fundação: a superposição é a passagem"], "en": ["The status of the proof: proved", "v384 to v391", "The Foundation: the superposition is the passage"]}
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
eng = shutil.which("pdflatex"); rep["artigo"] = {}


def compilar(cv, nome, lang, duas=True):
    tex = um._tex_guard_nan(um.build_pt(cv, verdict, CORE0P) if lang == "pt" else um.build_en(cv, verdict, CORE0P)); txt = um._tex_to_txt(tex)
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex); open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = [subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800).returncode for _ in range(2 if duas else 1)]
    return tex, txt, rcs, open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()


for lang in ("pt", "en"):
    tex, txt, rcs, log = compilar(c, "dry_v391_%s" % lang, lang); flat = re.sub(r"\s+", " ", txt)
    a = flat.find("O estatuto da prova: provada" if lang == "pt" else "The status of the proof: proved")
    bb = flat.find("A Fundação: a superposição é a passagem" if lang == "pt" else "The Foundation: the superposition is the passage", a + 10)
    sec = flat[a:bb] if (a >= 0 and bb > a) else ""
    tp = os.path.join(DRY, "dry_v391_%s.toc" % lang); toc = open(tp, encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(tp) else ""
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v391_%s.pdf" % lang)), "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6],
                           "faltam": [w for w in DEVE[lang] if w not in flat.replace("_ ", "_") and w not in tex], "nd_na_secao": sec.count("n/d") + sec.count("n/a"), "secao_chars": len(sec),
                           "guarda": [m_.group(0) for m_ in GUARDA.finditer(sec.replace("_ ", "_"))], "toc_faltam": [w for w in TOC[lang] if w not in toc],
                           "resumo_abre_com_estatuto": flat.find("O estatuto da prova (v391)." if lang == "pt" else "The status of the proof (v391).") < flat.find("A proposta." if lang == "pt" else "The proposal.")}
    print("artigo", lang, json.dumps(rep["artigo"][lang], ensure_ascii=False))
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["pdflatex_rc"] != [0, 0] or v["guarda"] or v["secao_chars"] < 5000 or v["toc_faltam"] or v["nd_na_secao"] or not v["resumo_abre_com_estatuto"]]
cv = dict(copy.deepcopy(c)); cv.pop("estatuto_da_prova_v391", None)
rep["variante"] = {}
for lang in ("pt", "en"):
    _t, _x, _r, _l = compilar(cv, "dry_v391_var_%s" % lang, lang, duas=False); fl = re.sub(r"\s+", " ", _x)
    rep["variante"][lang] = {"rc": _r, "frase_guarda": ("NÃO selou" in fl) if lang == "pt" else ("did NOT seal" in fl),
                             "resumo_nao_selado": ("não selado nesta rodada" in fl) if lang == "pt" else ("not sealed in this run" in fl),
                             "nao_diz_provada_no_resumo": ("A gravidade quântica da TGL está provada" not in fl) if lang == "pt" else ("quantum gravity is proved" not in fl)}
print("variante:", rep["variante"])
mau_var = [k for k, v in rep["variante"].items() if v["rc"] != [0] or not all(v[x] for x in ("frase_guarda", "resumo_nao_selado", "nao_diz_provada_no_resumo"))]
um.OUT = DRY; um.emit_canonical_md(c, verdict); md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown"] = {"carimbo": "**Versão v391**" in md, "estatuto_v391": "O estatuto da prova (v391, 07/10/2026)" in md, "v390_fica": "A Fundação (v390, 07/10/2026)" in md}
mani = os.path.join(DRY, "um_absoluto_manifest.md"); um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c); rep["manifest"] = "**Versão v391**" in open(mani, encoding="utf-8").read()
_proib = [k for k, m_ in c.items() if isinstance(m_, dict) and GUARDA.search(str(m_.get("verdict") or ""))]
_cc = subprocess.run([sys.executable, os.path.join(HERE, "conferir_citacoes_v391.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_rc"] = _cc.returncode
ok = viz_ok and mf_ok and all(U.values()) and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"] and not _proib and _cc.returncode == 0
rep["veredito"] = "TUDO PASSOU" if ok else "FALHOU: " + json.dumps({"vizinhos": viz_ok, "fluxo": mf_ok, "unidade": {k: v for k, v in U.items() if not v}, "artigo": mau, "variante": mau_var, "md": rep["markdown"], "mani": rep["manifest"], "proib": _proib, "citacoes": _cc.returncode}, ensure_ascii=False)
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_%s.json" % rot), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"])); sys.exit(0 if ok else 1)
