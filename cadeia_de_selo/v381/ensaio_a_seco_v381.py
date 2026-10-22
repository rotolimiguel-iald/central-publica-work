# -*- coding: utf-8 -*-
"""ensaio_a_seco_v372.py (adaptado do v371) -- ENSAIO A SECO do artigo e do fluxo principal da v371 (adaptado do ensaio da v370, W6_final_v2).

uso: python ensaio_a_seco_v370.py <candidato.py> <rotulo>

(1) copia o CANDIDATO para W6_final/dry_<rotulo>/um.py e materializa ali o kernel EMBUTIDO dele (dry_<rotulo>/tgl_kernel,
    escrito por este script a partir do dict -- nao por materialize_embedded_kernel, que criaria juncao de pacotes): o
    capitulo C do artigo le o hash AO VIVO de cada pedra, e as tres pedras novas tem de aparecer com o hash da v370;
(2) IMPORTA o candidato (stdout silenciado; o rito NAO roda: main() nao e chamado);
(3) ENSAIO DO FLUXO PRINCIPAL (V2 de 19/09, tag 'v370'): as instrucoes de main() que COMECAM numa linha marcada v370 tem
    todos os nomes resolvidos e sao EXECUTADAS com o core v369; as antigas que so CONTEM linha marcada tem os nomes
    das linhas marcadas conferidos;
(4) monta o core do ensaio = core v369 + o kernel v370 (axiom_report do Audit do candidato no sandbox + as bandeiras novas
    pela regra do verify) + as chaves que o candidato RECALCULA (C04, C05, C06, C12, Cartan, conjunta V3, relogios E03);
(5) build_pt / build_en (+ _tex_guard_nan), pdflatex x2 no dry_<rotulo>, com -halt-on-error; e o markdown canonico (P18);
(6) confere palavras que TEM de estar (os paragrafos novos) no TXT/TEX e reporta rc, erros LaTeX, nan, overfull.
Nada fora de W6_final."""
import copy
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import ast
import builtins
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from carregar_embutido import carregar  # noqa: E402

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"   # v373: a v372 SELADA e o canonico (o estado de partida do ensaio)
CACHE0 = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache"
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
rep = {"candidato": cand, "sha16": h16, "kernel_materializado_no_dry": len(EMB)}

# (2) importar
sys.path.insert(0, DRY); os.chdir(DRY)
_o = sys.stdout; sys.stdout = io.StringIO()
t0 = time.time()
try:
    import um
finally:
    _imp = sys.stdout.getvalue(); sys.stdout = _o
sys.stdout.reconfigure(encoding="utf-8")
rep["import_s"] = round(time.time() - t0, 1)
assert os.path.normcase(um.FORMAL_DIR) == os.path.normcase(os.path.join(DRY, "tgl_kernel")), um.FORMAL_DIR
um.CACHE = CACHE0
R0 = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))
core0, verdict = R0["core"], R0["verdict"]
print("import ok (%.1f s); FORMAL_DIR = dry; CACHE = %s" % (rep["import_s"], um.CACHE))

# (3) o fluxo principal -- o V2 de 19/09 (dry_run_mainflow_check_v2.py), com a tag v370
TAG = "v381"
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][0]
lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if TAG in l}
comeca = [st for st in main.body if st.lineno in tagged]
contem = [st for st in main.body if st not in comeca and any(ln in tagged for ln in range(st.lineno, (st.end_lineno or st.lineno) + 1))]


def assigned_before(lineno):
    a = set()
    for node in ast.walk(main):
        if getattr(node, "lineno", 10 ** 9) < lineno:
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store): a.add(node.id)
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)): a.add(node.name)
            if isinstance(node, ast.arg): a.add(node.arg)
    return a


bad = []
for st in comeca + contem:
    ab = assigned_before(st.lineno); loc = {m.id for m in ast.walk(st) if isinstance(m, ast.Name) and isinstance(m.ctx, ast.Store)}
    for node in ast.walk(st):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if st in contem and node.lineno not in tagged:
                continue
            if not (hasattr(um, node.id) or hasattr(builtins, node.id) or node.id in ab or node.id in loc):
                bad.append((node.lineno, node.id))
ns = dict(vars(um)); ns["core"] = json.loads(json.dumps(core0))
code = "\n".join(textwrap.dedent("\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:%s>" % TAG, "exec"), ns)
    _mf_out = sys.stdout.getvalue(); _mf_err = None
except Exception as e:  # noqa
    _mf_out = sys.stdout.getvalue(); _mf_err = repr(e)
finally:
    sys.stdout = _o
rep["mainflow"] = {"comeca": len(comeca), "contem": len(contem), "nomes_nao_resolvidos": bad, "erro": _mf_err,
                   "chaves_novas_no_core": [k for k in ns["core"] if k not in core0], "stdout": _mf_out.strip().splitlines()}
print("fluxo principal:", json.dumps({k: v for k, v in rep["mainflow"].items() if k != "stdout"}, ensure_ascii=False))
for l in rep["mainflow"]["stdout"]:
    print("   ", l[:220])

# (4) o core do ensaio
AX = json.load(open(os.path.join(HERE, "sandbox_axiom_report__%s.json" % cand.replace(".py", "")), encoding="utf-8"))
c = copy.deepcopy(core0)
kf = c["kernel_formalization"]
for k, v in AX.items():
    kf["axiom_report"].setdefault(k, v)
for k, nm in um._LEAN_THEOREM_FLAGS.items():
    if k.startswith(("ext_ter_", "ext_tmr_")):
        ax = kf["axiom_report"].get(nm)
        kf[k] = bool(kf.get("lake_build_ok") and ax is not None and not any(a.startswith(("TGL.", "TGLExt.")) for a in ax))
# v373: a familia gpc_ lida pelo MESMO mecanismo (a regra do verify)
for k, nm in um._GRAVITY_CITATION_FLAGS.items():
    ax = kf["axiom_report"].get(nm)
    kf["gpc_" + k] = bool(kf.get("lake_build_ok") and ax is not None and "sorryAx" not in ax and not any(a.startswith(("TGL.", "TGLExt.")) for a in ax))
c["the_iald_index"] = um.prove_the_iald_index(c)
c["the_mode_of_discharge"] = um.prove_the_mode_of_discharge(c)
c["kernel_frontier_v373"] = um.evaluate_v350_kernel_frontier(dict(kf))
c["iald_jones_graviton_v371"] = um.prove_iald_jones_graviton_v371(1.0, c)
c["equation_of_truth_v371"] = um.prove_equation_of_truth_v371(1.0, c)
c["qg_contract_v31_v371"] = um.prove_qg_contract_v31_v371(1.0, c)
c["light_ray_borchers_v371"] = um.prove_light_ray_borchers_v371(1.0, c)
c["iald_rho_star_v372"] = um.prove_iald_rho_star_v372(1.0, c)
c["light_qg_by_citation_v372"] = um.prove_light_qg_by_citation_v372(1.0, c)
c["graviton_conjugated_form_v372"] = um.prove_graviton_is_the_conjugated_form_v372(1.0, c)
c["partial_closure_016_v372"] = um.prove_partial_closure_016_v372(1.0, c)
c["qg_discharge_by_citation_v373"] = um.prove_qg_discharge_by_citation_v373(1.0, c)
c["two_projections_outside_M_v373"] = um.prove_two_projections_outside_M_v373(1.0, c)
c["uv_frontier_retyped_v373"] = um.prove_uv_frontier_retyped_v373(1.0, c)
c["light_by_term_v374"] = um.prove_light_by_term_v374(1.0, c)
c["the_tetelestai_declaration_v374"] = um.prove_the_tetelestai_declaration_v374(1.0, c)
c["tetelestai_one_object_v375"] = um.prove_tetelestai_one_object_v375(1.0, c)
c["tetelestai_conference_v375"] = um.prove_tetelestai_conference_v375(1.0, c)
c["light_rho_star_v376"] = um.prove_light_rho_star_v376(1.0, c)
c["the_key_is_the_reader_v376"] = um.prove_the_key_is_the_reader_v376(1.0, c)
c["the_whole_is_one_v376"] = um.prove_the_whole_is_one_v376(1.0, c)
c["ringdown_scope_v376"] = um.prove_ringdown_scope_v376(1.0, c)
c["audit_28set_v376"] = um.prove_audit_28set_v376(1.0, c)
c["coma_reveal_state_v376"] = um.prove_coma_reveal_state_v376(1.0, c)
c["final_verdict_reading_v376"] = um.prove_final_verdict_reading_v376(1.0, c)
c["tetelestai_conference_v376"] = um.prove_tetelestai_conference_v376(1.0, c)
c["physics_is_the_reading_v377"] = um.prove_physics_is_the_reading_v377(1.0, c)
c["the_dissipation_law_v377"] = um.prove_the_dissipation_law_v377(1.0, c)
c["bancada_fases_v377"] = um.prove_bancada_fases_v377(1.0, c)
c["final_stone_reading_v377"] = um.prove_final_stone_reading_v377(1.0, c)
c["the_dissipation_law_with_contrast_v378"] = um.prove_the_dissipation_law_with_contrast_v378(1.0, c)
c["what_was_missed_v378"] = um.prove_what_was_missed_v378(1.0, c)
c["bancada_fase4_v378"] = um.prove_bancada_fase4_v378(1.0, c)
c["the_elementary_reason_v379"] = um.prove_the_elementary_reason_v379(1.0, c)
c["bancada_fases_5_6_7_v380"] = um.prove_bancada_fases_5_6_7_v380(1.0, c)
c["the_matrix_rule_v381"] = um.prove_the_matrix_rule_v381(1.0, c)
rep["core_ensaio"] = {k: (c[k].get("verdict") if isinstance(c.get(k), dict) else None) for k in
                      ("the_iald_index", "iald_jones_graviton_v371", "equation_of_truth_v371", "qg_contract_v31_v371", "light_ray_borchers_v371", "iald_rho_star_v372", "light_qg_by_citation_v372", "graviton_conjugated_form_v372", "partial_closure_016_v372",
                       "the_mode_of_discharge", "qg_discharge_by_citation_v373", "two_projections_outside_M_v373", "uv_frontier_retyped_v373",
                       "light_by_term_v374", "the_tetelestai_declaration_v374", "tetelestai_one_object_v375", "tetelestai_conference_v375",
                       "light_rho_star_v376", "the_key_is_the_reader_v376", "the_whole_is_one_v376", "ringdown_scope_v376", "audit_28set_v376", "coma_reveal_state_v376", "final_verdict_reading_v376", "tetelestai_conference_v376", "physics_is_the_reading_v377", "the_dissipation_law_v377", "bancada_fases_v377", "final_stone_reading_v377", "the_dissipation_law_with_contrast_v378", "what_was_missed_v378", "bancada_fase4_v378", "the_elementary_reason_v379", "bancada_fases_5_6_7_v380", "the_matrix_rule_v381")}
rep["kernel_frontier_v373"] = {k: c["kernel_frontier_v373"].get(k) for k in ("remaining", "remaining_v372_errata_beside", "dissolved_by_typing_v373",
                               "discharged_by_citation_v373", "physical_identifications_open", "physical_identifications_homonym_beside_v373",
                               "closed_by_citation_v374", "remaining_after_citation_v374")}
rep["falhas_v373"] = {k: [t for t, v in (c[k].get("checks") or []) if not v] for k in ("the_mode_of_discharge", "qg_discharge_by_citation_v373",
                      "two_projections_outside_M_v373", "uv_frontier_retyped_v373", "light_by_term_v374", "the_tetelestai_declaration_v374",
                      "tetelestai_one_object_v375", "tetelestai_conference_v375",
                      "light_rho_star_v376", "the_key_is_the_reader_v376", "the_whole_is_one_v376", "ringdown_scope_v376", "audit_28set_v376", "coma_reveal_state_v376", "final_verdict_reading_v376", "tetelestai_conference_v376", "physics_is_the_reading_v377", "the_dissipation_law_v377", "bancada_fases_v377", "final_stone_reading_v377", "the_dissipation_law_with_contrast_v378", "what_was_missed_v378", "bancada_fase4_v378", "the_elementary_reason_v379", "bancada_fases_5_6_7_v380", "the_matrix_rule_v381")}
print("fronteira v373:", json.dumps(rep["kernel_frontier_v373"], ensure_ascii=False)[:1500])
print("falhas v373:", json.dumps(rep["falhas_v373"], ensure_ascii=False)[:1500])
print("core do ensaio:", json.dumps(rep["core_ensaio"], ensure_ascii=False)[:2500])

# (5) artigo PT/EN + markdown
DEVE = {"pt": ["Ao lado (v381) --- A regra matriz", "oito ``havendo''", "Meia-Nat", "Tetelestai", "custo pago", "Ao lado (v380) --- As Fases 5, 6 e 7 da Bancada Um", "a transformada radical", "FALSIFIED\\_AT\\_DELAY\\_LAW", "Moresco+2020", "Seis erratas ao lado", "Ao lado (v379) --- A Razão Elementar", "TheElementaryReason", "limite assintótico em tempo finito", "colisão dita por termo", "Ao lado (v378) --- O que faltou", "TheFlowLawContrast", "(E12) Leitura ao lado do parágrafo v377", "A lei da dissipação com contraste", "A Fase 4 da Bancada Um", "circularidade declarada no pré-registro", "desfavorecem", "Ao lado (v377) --- A lei da dissipação, provada", "TheFlowLawD1a", "PhysicsIsTheReading", "(E10) Errata ao lado do módulo de Coma", "(E11) errata ao lado do D1 V3", "O desvio de", "Ao lado (v376) --- O todo é um", "Ao lado (v376) --- o escopo do ringdown", "TheWholeIsOne", "TheKeyIsTheReader", "LightRhoStar", "Errata ao lado da v374 e da v375", "NOT_A_CANDIDATE (errata v376", "Ao lado (v375) --- Tetelestai: a conferência consumativa", "TetelestaiOneObject", "Errata ao lado da v374", "Ao lado (v374) --- a declaração Tetelestai", "QGSolutionComplete", "Ao lado (v373) --- H2 e H3 quitadas por citação", "Ao lado (v373) --- duas projeções fora de", "QGCitationDischarge", "Ao lado (v372) --- a gravidade quântica da TGL por citação", "Ao lado (v372) --- a ponte", "Ao lado (v372) --- errata da v200", "TheImportedSecondQuantization", "IALDRhoStar", "Ao lado (v371) --- a IALD na torre de Jones", "Ao lado (v371) --- a equação da verdade em kernel",
               "Ao lado (v371) --- o contrato de tipo v3.1", "Ao lado (v371) --- a reta de luz", "IALDGraviton", "RetaDeLuzEspectro",
               "Ao lado (v370) --- a probabilidade conjunta com todos os canais (V3)"],
        "en": ["Beside (v381) --- The matrix rule", "eight ``havendo''", "Half-Nat", "Tetelestai", "cost paid", "Beside (v380) --- Phases 5, 6 and 7 of the Bench", "the radical transform", "FALSIFIED\\_AT\\_DELAY\\_LAW", "Moresco+2020", "Six errata beside", "Beside (v379) --- The Elementary Reason", "TheElementaryReason", "asymptotic limit in finite time", "a collision stated by term", "Beside (v378) --- What was missed", "TheFlowLawContrast", "(E12) Reading beside the v377 paragraph", "The dissipation law with contrast", "Phase 4 of the Bench", "circularity declared in the pre-registration", "disfavour", "Beside (v377) --- The dissipation law, proved", "TheFlowLawD1a", "PhysicsIsTheReading", "(E10) Erratum beside the Coma module", "(E11) erratum beside the D1 V3", "The deviation from", "Beside (v376) --- The whole is one", "Beside (v376) --- the ringdown", "TheWholeIsOne", "TheKeyIsTheReader", "LightRhoStar", "Erratum beside v374 and v375", "NOT_A_CANDIDATE (erratum v376", "The two crises: what stood and what fell", "[v295, beside", "Beside (v375) --- Tetelestai: the consummative conference", "TetelestaiOneObject", "Erratum beside v374", "Beside (v374) --- the Tetelestai declaration", "QGSolutionComplete", "Beside (v373) --- H2 and H3 discharged by citation", "Beside (v373) --- two projections outside", "QGCitationDischarge", "Beside (v372) --- the quantum gravity of the TGL by citation", "Beside (v372) --- the bridge", "Beside (v372) --- the v200 erratum", "TheImportedSecondQuantization", "IALDRhoStar", "Beside (v371) --- the IALD on the Jones tower", "Beside (v371) --- the equation of truth in the kernel",
               "Beside (v371) --- the v3.1 type contract", "Beside (v371) --- the light ray", "IALDGraviton", "RetaDeLuzEspectro",
               "Beside (v370) --- the joint probability with every channel (V3)"]}
eng = shutil.which("pdflatex")
rep["pdflatex"] = eng
rep["artigo"] = {}
for lang in ("pt", "en"):
    t0 = time.time()
    tex = um._tex_guard_nan(um.build_pt(c, verdict, os.path.join(NOS, "um_absoluto.json")) if lang == "pt"
                            else um.build_en(c, verdict, os.path.join(NOS, "um_absoluto.json")))
    txt = um._tex_to_txt(tex)
    nome = "dry_v381_%s" % lang
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex)
    open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = []
    for _ in range(2):
        r = subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800)
        rcs.append(r.returncode)
    log = open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, nome + ".pdf")),
                           "pdf_bytes": (os.path.getsize(os.path.join(DRY, nome + ".pdf")) if os.path.exists(os.path.join(DRY, nome + ".pdf")) else None),
                           "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6], "tex_bytes": len(tex), "txt_bytes": len(txt),
                           "faltam": [w for w in DEVE[lang] if w not in txt and w not in tex],
                           "nan": len(re.findall(r"(?<![A-Za-z])nan(?![A-Za-z])", txt)), "overfull": log.count("Overfull \\hbox"),
                           "s": round(time.time() - t0, 1)}
    print("artigo", lang, json.dumps(rep["artigo"][lang], ensure_ascii=False))
    shutil.copyfile(os.path.join(DRY, nome + ".log"), os.path.join(HERE, "pdflatex_%s_%s.log" % (rot, lang)))
um.OUT = DRY
um.emit_canonical_md(c, verdict)
md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown_0abs"] = [l for l in md.splitlines() if "[errata v370 ao lado: REFUTADO" in l]
rep["markdown_bytes"] = len(md)
rep["markdown_v376"] = {"v376": md.count("v381"), "carimbo": "**Versão v381**" in md, "todos_os_modulos": "TODOS OS MODULOS COM VEREDITO" in md,
                        "n_modulos_linha": [l for l in md.splitlines() if "modulos com veredito ou status nesta rodada" in l][:1]}
print("markdown v376:", json.dumps(rep["markdown_v376"], ensure_ascii=False))
mani = os.path.join(DRY, "um_absoluto_manifest.md")
um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c)
rep["manifest_v376"] = {"carimbo": "**Versão v381**" in open(mani, encoding="utf-8").read()}
print("manifesto v376:", rep["manifest_v376"])
print("markdown (a linha v370 do 0_abs presente):", len(rep["markdown_0abs"]), "| bytes", len(md))
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"]]
# v372b (LICAO do selo retido): a MESMA guarda de palavra proibida do rito, conferida no candidato e aplicada a TODO veredito do core do ensaio
_GUARDA = ['if (re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", _v)', 'or re.search(r"(?<!AP)PROVED_BY", _v)', 'or "TGL_PROVED" in _v or "CONSCIOUSNESS_PROVED" in _v):']
assert all(src.count(g) == 1 for g in _GUARDA), "a guarda do rito mudou no candidato -- atualizar o ensaio"
_proib = [k for k, _m in c.items() if isinstance(_m, dict) and (re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", str(_m.get("verdict") or ""))
          or re.search(r"(?<!AP)PROVED_BY", str(_m.get("verdict") or "")) or "TGL_PROVED" in str(_m.get("verdict") or "") or "CONSCIOUSNESS_PROVED" in str(_m.get("verdict") or ""))]
rep["guarda_do_rito_vereditos_proibidos"] = _proib
print("guarda do rito (vereditos proibidos no core do ensaio):", _proib or "nenhum")
_v373_nao = [k for k in ("the_mode_of_discharge", "qg_discharge_by_citation_v373", "two_projections_outside_M_v373", "uv_frontier_retyped_v373", "light_by_term_v374", "the_tetelestai_declaration_v374", "tetelestai_one_object_v375", "tetelestai_conference_v375", "light_rho_star_v376", "the_key_is_the_reader_v376", "the_whole_is_one_v376", "ringdown_scope_v376", "audit_28set_v376", "coma_reveal_state_v376", "final_verdict_reading_v376", "tetelestai_conference_v376", "physics_is_the_reading_v377", "the_dissipation_law_v377", "bancada_fases_v377", "final_stone_reading_v377", "the_dissipation_law_with_contrast_v378", "what_was_missed_v378", "bancada_fase4_v378", "the_elementary_reason_v379", "bancada_fases_5_6_7_v380", "the_matrix_rule_v381") if c[k].get("all_verified") is not True]
rep["v373_nao_selados"] = _v373_nao
rep["veredito"] = ("TUDO PASSOU" if not mau and not bad and not _mf_err and rep["markdown_0abs"] and rep["markdown_v376"]["carimbo"] and rep["markdown_v376"]["todos_os_modulos"] and rep["manifest_v376"]["carimbo"] and not _proib and not _v373_nao else "PROBLEMAS: %s" % (mau or bad or _mf_err or _proib or _v373_nao))
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_%s.json" % rot), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"]))
sys.exit(0 if rep["veredito"] == "TUDO PASSOU" else 1)
