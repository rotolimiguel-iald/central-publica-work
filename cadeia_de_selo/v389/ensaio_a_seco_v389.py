# -*- coding: utf-8 -*-
"""ensaio_a_seco_v389.py -- ENSAIO A SECO da v389 (molde: ensaio_a_seco_v388.py), SEM a GPU do rito e SEM o kernel do rito (a v389 nao muda o kernel).
uso: python ensaio_a_seco_v389.py <candidato.py> <rotulo>
(1) copia o candidato para dry_<rotulo>/um.py e materializa o kernel EMBUTIDO; (2) importa (o rito NAO roda); UM_VERSION v389; a escada recomputada do core v388 = 6154;
(3) o registro iii1_net_image RECOMPUTADO pela v389 (o rotulo novo; tudo o mais igual ao core v388 selado) e o FLUXO PRINCIPAL v389 executado;
(4) unidade (exame com sha errado; rotulo antigo no core; ledger adulterado; frase velha de volta no fonte); (5) build_pt/build_en, pdflatex x2, DEVE/NAO_DEVE, sumario,
a variante (registro ausente); (6) o .md canonico (o rotulo novo; o velho ausente) e o manifesto; (7) o conferidor de citacoes."""
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
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v389.json"), encoding="utf-8")); assert CM["sha16"] == h16
rep = {"candidato": cand, "sha16": h16, "kernel_materializado": len(EMB)}
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    import um
finally:
    sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
assert um.UM_VERSION == "v389"
R0 = json.load(open(CORE0P, encoding="utf-8")); core0, verdict = R0["core"], R0["verdict"]
assert "hubble_ratio_opening_v388" in core0 and "text_label_errata_v389" not in core0
core_s = json.loads(json.dumps(core0))
_el = um.prove_external_ladder(1.0, core_s["kernel_formalization"]); rep["escada"] = [_el.get("n_theorems_clean"), _el.get("n_theorems_expected")]
assert rep["escada"] == [6154, 6154], rep["escada"]
# o iii1_net_image recomputado: so o rotulo e o campo da errata mudam
_im = um.prove_iii1_net_shadow_image(1.0); _im0 = core0["iii1_net_image"]
_d = sorted(k for k in set(_im) | set(_im0) if json.dumps(_im.get(k), sort_keys=True, default=str) != json.dumps(_im0.get(k), sort_keys=True, default=str))
_sd = [i for i, (a, b) in enumerate(zip(_im["seals"], _im0["seals"])) if a != b]
rep["iii1_net_image"] = {"chaves_que_mudaram": _d, "selos_que_mudaram": _sd, "novo": _im["seals"][2], "verdict_igual": _im["verdict"] == _im0["verdict"]}
iii1_ok = _d == ["seals", "seals_errata_v389"] and _sd == [2] and _im["seals"][2] == "CLOCK_TORSION_VERIFIED_ON_PHYSICAL_NET" and _im["verdict"] == _im0["verdict"]
print("iii1_net_image:", rep["iii1_net_image"])
core_s["iii1_net_image"] = json.loads(json.dumps(_im, default=str))
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][0]; lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if "v389" in l}; comeca = [st for st in main.body if st.lineno in tagged]
ns = dict(vars(um)); ns["core"] = core_s
code = "\n".join(textwrap.dedent("\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:v389>", "exec"), ns); _err = None
except Exception as e:  # noqa
    _err = repr(e)
finally:
    _mf = sys.stdout.getvalue(); sys.stdout = _o
c = ns["core"]; NOVAS = ["text_label_errata_v389"]
_t = c.get("text_label_errata_v389") or {}
rep["mainflow"] = {"comeca": len(comeca), "erro": _err, "chaves_novas": sorted(k for k in c if k not in core0), "stdout": _mf.strip().splitlines(),
                   "text_label_errata_v389": {x: _t.get(x) for x in ("verdict", "all_verified", "errors", "ledger", "text_sites_ok", "exam_ok")}}
print("fluxo:", json.dumps({k: v for k, v in rep["mainflow"].items() if k != "stdout"}, ensure_ascii=False)[:2500])
mf_ok = (not _err and len(comeca) == 2 and rep["mainflow"]["chaves_novas"] == NOVAS and _t.get("all_verified") is True and "_3_CORRIGIR_ADDRESSED__" in str(_t.get("verdict"))
         and "LEDGER_1025_UNIQUE_PLUS_156_OUTSIDE_156_IN_O16" in str(_t.get("verdict")) and all(x["new_present"] and x["old_absent"] for x in _t.get("text_sites") or [{}]))
U = {}
P = um._V389_EXAME; _p = copy.deepcopy(P); _p["files"]["exame_json"]["sha256"] = "0" * 64; um._V389_EXAME = _p
try:
    _u = um.text_label_errata_v389(core_s)
finally:
    um._V389_EXAME = P
U["exame_sha_errado"] = _u["all_verified"] is False and "EXAM_FILES" in _u["verdict"]
_u = um.text_label_errata_v389(dict(core_s, iii1_net_image=core0["iii1_net_image"])); U["rotulo_antigo_no_core"] = _u["all_verified"] is False and "SEAL_LABEL" in _u["verdict"]
_L = um._V389_LEDGER_NO_GERADOR; um._V389_LEDGER_NO_GERADOR = [1015, 166, 156]
try:
    _u = um.text_label_errata_v389(core_s)
finally:
    um._V389_LEDGER_NO_GERADOR = _L
U["ledger_adulterado"] = _u["all_verified"] is False and "LEDGER_COUNT" in _u["verdict"]
_T = um._V389_TROCAS; _t2 = copy.deepcopy(_T); _t2[0]["old_parts"] = ["def text_label_", "errata_v389("]; um._V389_TROCAS = _t2   # uma 'frase velha' que ESTA no fonte
try:
    _u = um.text_label_errata_v389(core_s)
finally:
    um._V389_TROCAS = _T
U["frase_velha_presente"] = _u["all_verified"] is False and "TEXT_SITES" in _u["verdict"]
_u = um.text_label_errata_v389(core_s); U["tudo_certo"] = _u["all_verified"] is True and _u["ledger"]["unique_paths"] == 1025
rep["unidade"] = U; print("unidade:", U)
DEVE = {"pt": ["Ao lado (v389):", "as erratas de texto e rótulo do exame da v388", "CLOCK_TORSION_VERIFIED_ON_PHYSICAL_NET", "um único axioma POSTO", "[POSTO]",
               "nesta versão (a abertura está na v388, ao lado)", "caminhos únicos do ledger citável; mais 156", "TGL_TEXT_LABEL_ERRATA_V389__", "Ao lado (v388)", "v389; a cada versão ao lado"],
        "en": ["Beside (v389):", "the text and label errata from the v388 exam", "CLOCK_TORSION_VERIFIED_ON_PHYSICAL_NET", "a single posited axiom", "[POSTO]",
               "in this version (the opening is in v388, beside)", "unique paths of the citable ledger; plus 156", "TGL_TEXT_LABEL_ERRATA_V389__", "Beside (v388)", "v389; each version beside"]}
NAO_DEVE = {"pt": ["parte de um único postulado", "o único postulado. A Parte C", "faz agora (v384)", "Nada foi aberto: baixar", "Dado o axioma da fronteira mínima", "NÃO selou"],
            "en": ["starts from a single postulate", "the single postulate. Part C", "does now (v384)", "Nothing was opened: fetching", "Given the axiom of the minimal", "did NOT seal"]}
DEVE["pt"] += ["Dada a fronteira mínima auto-conjugada", "faz agora (v384 a v389; a cada versão ao lado)", "ele contara 1015 caminhos e 166 de fora", "0 bloqueios e 3 correções"]
DEVE["en"] += ["Given the minimal self-conjugate boundary", "does now (v384 to v389; each version beside)", "it had counted 1015 paths and 166 outside", "0 blockers and 3 corrections"]


def marcadores(nome):
    """os titulos dos marcadores do PDF (.out do hyperref), decodificados (octal -> bytes; UTF-16BE quando ha BOM)"""
    p = os.path.join(DRY, nome + ".out"); out = []
    if not os.path.exists(p):
        return out
    for l in open(p, encoding="latin-1").read().splitlines():
        m_ = re.match(r"\\BOOKMARK \[\d+\]\[-?\]\{[^}]*\}\{(.*)\}\{[^}]*\}\s*%?", l)
        if not m_:
            continue
        b = re.sub(rb"\\([0-7]{3})", lambda x: bytes([int(x.group(1), 8)]), m_.group(1).encode("latin-1")).replace(b"\\(", b"(").replace(b"\\)", b")")
        out.append(b[2:].decode("utf-16-be", "replace") if b.startswith(b"\xfe\xff") else b.decode("latin-1"))
    return out
TOC = {"pt": ["Ao lado (v389)", "Ao lado (v388)", "v389; a cada versão ao lado"], "en": ["Beside (v389)", "Beside (v388)", "v389; each version beside"]}
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
eng = shutil.which("pdflatex"); rep["artigo"] = {}


def compilar(cv, nome, lang, duas=True):
    tex = um._tex_guard_nan(um.build_pt(cv, verdict, CORE0P) if lang == "pt" else um.build_en(cv, verdict, CORE0P)); txt = um._tex_to_txt(tex)
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex); open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = [subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800).returncode for _ in range(2 if duas else 1)]
    return tex, txt, rcs, open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()


for lang in ("pt", "en"):
    tex, txt, rcs, log = compilar(c, "dry_v389_%s" % lang, lang); flat = re.sub(r"\s+", " ", txt)
    bb = flat.rfind("A cunhagem." if lang == "pt" else "The coinage."); a = flat.rfind("Ao lado (v389)" if lang == "pt" else "Beside (v389)", 0, bb)
    sec = flat[a:bb] if (a >= 0 and bb > a) else ""
    tp = os.path.join(DRY, "dry_v389_%s.toc" % lang); toc = open(tp, encoding="utf-8", errors="replace").read().replace("\n", "") if os.path.exists(tp) else ""
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, "dry_v389_%s.pdf" % lang)), "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6],
                           "faltam": [w for w in DEVE[lang] if w not in flat.replace("_ ", "_") and w not in tex], "sobram": [w for w in NAO_DEVE[lang] if w in flat],
                           "nd_na_secao": sec.count("n/d") + sec.count("n/a"), "secao_chars": len(sec), "guarda_no_texto_todo": [m_.group(0) for m_ in GUARDA.finditer(flat.replace("_ ", "_")) if "CLOCK" in flat[max(0, m_.start() - 30):m_.start()]],
                           "guarda_na_secao": [m_.group(0) for m_ in GUARDA.finditer(sec.replace("_ ", "_"))], "toc_faltam": [w for w in TOC[lang] if w not in toc.replace("$\\to $", "→")],
                           "marcador_intro": [x for x in marcadores("dry_v389_%s" % lang) if x.startswith(("Introdução", "Introduction"))]}
    rep["artigo"][lang]["marcador_ok"] = (len(rep["artigo"][lang]["marcador_intro"]) == 1 and ("v384 a v389" if lang == "pt" else "v384 to v389") in rep["artigo"][lang]["marcador_intro"][0])
    print("artigo", lang, json.dumps(rep["artigo"][lang], ensure_ascii=False))
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v["sobram"] or v["pdflatex_rc"] != [0, 0] or v["guarda_na_secao"] or v["guarda_no_texto_todo"]
       or v["secao_chars"] < 1500 or v["toc_faltam"] or v["nd_na_secao"] or not v["marcador_ok"]]
cv = dict(copy.deepcopy(c)); cv.pop("text_label_errata_v389", None)
rep["variante"] = {}
for lang in ("pt", "en"):
    _t_, _x, _r, _l = compilar(cv, "dry_v389_var_%s" % lang, lang, duas=False); fl = re.sub(r"\s+", " ", _x)
    rep["variante"][lang] = {"rc": _r, "diz_ausente": "AUSENTE" in fl or "ABSENT" in fl, "frase_guarda": ("NÃO selou" in fl) if lang == "pt" else ("did NOT seal" in fl),
                             "nao_inventa_zero": ("0 bloqueios" not in fl) if lang == "pt" else ("0 blockers" not in fl)}
print("variante:", rep["variante"])
mau_var = [k for k, v in rep["variante"].items() if v["rc"] != [0] or not v["diz_ausente"] or not v["frase_guarda"] or not v["nao_inventa_zero"]]
um.OUT = DRY; um.emit_canonical_md(c, verdict); md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown"] = {"carimbo": "**Versão v389**" in md, "ao_lado_v389": "Ao lado (v389, 06/10/2026)" in md, "v388_fica": "Ao lado (v388, 06/10/2026)" in md,
                   "rotulo_novo": "CLOCK_TORSION_VERIFIED_ON_PHYSICAL_NET" in md, "rotulo_velho_ausente": ("CLOCK_TORSION_" + "CONF" + "IRMED") not in md}
mani = os.path.join(DRY, "um_absoluto_manifest.md"); um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c); rep["manifest"] = "**Versão v389**" in open(mani, encoding="utf-8").read()
_proib = [k for k, m_ in c.items() if isinstance(m_, dict) and GUARDA.search(str(m_.get("verdict") or ""))]
_cc = subprocess.run([sys.executable, os.path.join(HERE, "conferir_citacoes_v389.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
rep["citacoes_rc"] = _cc.returncode
ok = iii1_ok and mf_ok and all(U.values()) and not mau and not mau_var and all(rep["markdown"].values()) and rep["manifest"] and not _proib and _cc.returncode == 0
rep["veredito"] = "TUDO PASSOU" if ok else "FALHOU: " + json.dumps({"iii1": iii1_ok, "fluxo": mf_ok, "unidade": {k: v for k, v in U.items() if not v}, "artigo": mau, "variante": mau_var, "md": rep["markdown"], "mani": rep["manifest"], "proib": _proib, "cit": _cc.returncode}, ensure_ascii=False)
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_%s.json" % rot), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"])); sys.exit(0 if ok else 1)
