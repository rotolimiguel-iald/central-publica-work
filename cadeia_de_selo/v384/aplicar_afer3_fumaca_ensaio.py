# -*- coding: utf-8 -*-
"""3a afericao na FUMACA (so com o pre-registro V1 ratificado do lugar permanente; sai com codigo != 0 se o trabalhador falhar ou nao gravar resultado)
e no ENSAIO A SECO (as frases novas do DEVE; o registro de ENSAIO com forma de SUCESSO, para os paragrafos dos testes serem construidos; variantes de
falha, de reaproveitamento e de T1 sem solucao finita; a fumaca conferida -- marca da rodada, especificacao de fumaca, o MESMO trabalhador do candidato,
veredito completo; os nomes do terceiro balde conferidos)."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))


def patch(fn, pairs):
    p = os.path.join(HERE, fn); raw = open(p, "rb").read(); s = raw.decode("utf-8")
    if not os.path.exists(p + ".bak_antes_afer3"):
        open(p + ".bak_antes_afer3", "wb").write(raw)
    for old, new in pairs:
        c = s.count(old); assert c == 1, (fn, c, old[:100])
        s = s.replace(old, new)
    ast.parse(s)
    open(p + ".tmp", "wb").write(s.encode("utf-8")); os.replace(p + ".tmp", p); print("ok", fn)


patch("fumaca_v384.py", [
    ('''PJ = json.load(open(sys.argv[1], encoding="utf-8")); WK = os.path.abspath(sys.argv[2])''',
     '''PJ = json.load(open(sys.argv[1], encoding="utf-8")); WK = os.path.abspath(sys.argv[2])
# a fumaca CALCULA com os operadores da teoria: so com o pre-registro V1 RATIFICADO, do lugar permanente (3a afericao)
_pp = os.path.abspath(sys.argv[1]).replace(chr(92), "/")
assert _pp.startswith("C:/IALD/Bancada_Um/investigacao/preregistro_pilar_quantico_03out/") and "RASCUNHO" not in _pp.upper(), "a fumaca so roda com o V1 do lugar permanente: " + _pp
assert (PJ.get("ratificacao_do_operador") or {}).get("verbatim"), "o pre-registro nao foi ratificado pelo operador -- a fumaca nao roda"
assert hashlib.sha256(open(WK, "rb").read()).hexdigest() == PJ["spec"]["worker_sha256"], "o trabalhador nao e' o congelado no pre-registro"'''),
    ('''print("fases (s):", R.get("phase_seconds"), "| cpuref:", {k: (R.get("cpuref_compare") or {}).get(k) for k in ("compared", "disagreements", "ok")})''',
     '''print("fases (s):", R.get("phase_seconds"), "| cpuref:", {k: (R.get("cpuref_compare") or {}).get(k) for k in ("read", "compared", "disagreements", "ok")})'''),
    ('''if r.returncode != 0:
    print(r.stdout[-3000:]); print(r.stderr[-3000:])''',
     '''if r.returncode != 0 or not R:
    print(r.stdout[-3000:]); print(r.stderr[-3000:])
    print("FUMACA FALHOU (rc %s; resultado %s)" % (r.returncode, "presente" if R else "AUSENTE")); sys.exit(1)   # fail-closed (3a afericao)
print("resultado da fumaca:", os.path.join(OUT, "result.json"))'''),
])

patch("ensaio_a_seco_v384.py", [
    ('''# o registro do pilar a partir da FUMACA, pela propria _qp_summary do candidato (o mesmo codigo do rito)
RF = json.load(open(fumaca, encoding="utf-8"))
FIX = {"theorem": "ENSAIO A SECO -- registro montado de um resultado de FUMACA (contagens minimas); NAO e resultado", "status": "[ENSAIO]",
       "preregistration": {"spec_sha256": um._QP_SPEC_SHA256}, "key": "ENSAIO_SEM_CHAVE", "mode": "COMPUTE",
       "verdict": "ENSAIO__" + str(RF.get("verdict")), "custody_chain_ok": False, "summary": um._qp_summary(RF), "all_verified": False,
       "reuse": {"reused": False, "reading": "ENSAIO"}, "does_not_gate_core": True}''',
     '''# o registro do pilar a partir da FUMACA, pela propria _qp_summary do candidato (o mesmo codigo do rito)
RF = json.load(open(fumaca, encoding="utf-8"))
# a fumaca conferida (3a afericao): desta forma de fumaca, do MESMO trabalhador embutido no candidato, completa
_spf = os.path.join(os.path.dirname(fumaca), "spec_fumaca.json")
_SF = json.load(open(_spf, encoding="utf-8"))
assert RF.get("run_id") and str(_SF.get("id", "")).endswith("__FUMACA"), "o resultado nao e' de uma fumaca"
assert RF.get("spec_sha256") == hashlib.sha256(open(_spf, "rb").read()).hexdigest() != um._QP_SPEC_SHA256, "a especificacao da fumaca nao confere"
assert RF.get("worker_sha256") == hashlib.sha256(um._QP_WORKER_SRC.encode("utf-8")).hexdigest(), "a fumaca e' de OUTRO trabalhador que o embutido no candidato"
assert str(RF.get("verdict", "")).startswith("TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__"), "a fumaca nao completou: %s" % RF.get("verdict")
# o registro de ENSAIO tem FORMA DE SUCESSO (para os paragrafos dos testes serem construidos), com a marca ENSAIO no meio do veredito
FIX = {"theorem": "ENSAIO A SECO -- registro montado de um resultado de FUMACA (contagens minimas); NAO e resultado", "status": "[ENSAIO]",
       "preregistration": {"spec_sha256": um._QP_SPEC_SHA256}, "key": "ENSAIO_SEM_CHAVE", "mode": "COMPUTE",
       "verdict": str(RF.get("verdict")).replace("__GATE_UNTOUCHED", "__ENSAIO_FUMACA_NAO_E_RESULTADO__GATE_UNTOUCHED"), "custody_chain_ok": True,
       "summary": um._qp_summary(RF), "all_verified": False, "reuse": {"reused": False, "reading": "ENSAIO", "saved_to_cache": "ENSAIO_SEM_CACHE"}, "does_not_gate_core": True}'''),
    ('''DEVE = {"pt": ["Introdução: o que este código faz agora (v384)", "três coisas ao mesmo tempo", "Nota: o que se calcula na GPU e como", "Os quatro testes",
               "A escala e a referência", "O que é e o que não é", "não falsificado não é confirmado", "Ao lado (v383) --- O livro de cobranças e a viscosidade"],
        "en": ["Introduction: what this code does now (v384)", "three things at the same time", "Note: what is computed on the GPU and how", "The four tests",
               "Scale and reference", "What it is and what it is not", "not falsified is not confirmed", "Beside (v383) --- The ledger of charges and the viscosity"]}''',
     '''DEVE = {"pt": ["Introdução: o que este código faz agora (v384)", "três coisas", "ao mesmo tempo", "Nota: o que se calcula na GPU e como", "Os quatro testes",
               "A escala e a referência", "O que é e o que não é", "não falsificado não é confirmado", "Ao lado (v383) --- O livro de cobranças e a viscosidade"],
        "en": ["Introduction: what this code does now (v384)", "three things", "at the same time", "Note: what is computed on the GPU and how", "The four tests",
               "Scale and reference", "What it is and what it is not", "not falsified is not confirmed", "Beside (v383) --- The ledger of charges and the viscosity"]}'''),
    ('''bad = []
for st in comeca + contem:''', '''# os enunciados do TERCEIRO BALDE (W08/W08b/W08c) nao levam a marca na linha: conferidos por inteiro (3a afericao)
balde = [st for st in main.body if st not in comeca and st not in contem and "_computacao" in "\\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])]
bad = []
for st in balde:
    ab = assigned_before(st.lineno); loc = {m.id for m in ast.walk(st) if isinstance(m, ast.Name) and isinstance(m.ctx, ast.Store)}
    for node in ast.walk(st):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and not (hasattr(um, node.id) or hasattr(builtins, node.id) or node.id in ab or node.id in loc):
            bad.append((node.lineno, node.id))
for st in comeca + contem:'''),
    ('''rep["mainflow"] = {"comeca": len(comeca), "contem": len(contem), "nomes_nao_resolvidos": bad,''',
     '''rep["mainflow"] = {"comeca": len(comeca), "contem": len(contem), "terceiro_balde": len(balde), "nomes_nao_resolvidos": bad,'''),
    ('''um.OUT = DRY
um.emit_canonical_md(c, verdict)''', '''# as VARIANTES do registro (3a afericao): falha, reaproveitamento e T1 com estimativas sem solucao finita -- o artigo tem de compilar e dizer cada uma
import math as _m
_RFi = copy.deepcopy(RF)
for _dv in (_RFi.get("T1") or {}).values():
    for _sg in ("sigma_1e-08",):
        if isinstance(_dv.get(_sg), dict):
            _dv[_sg]["median_beta_rel_err"] = float("inf"); _dv[_sg]["n_nonfinite_beta"] = _dv[_sg].get("n") or 1
VARS = {"falha": (dict(copy.deepcopy(FIX), verdict="TGL_QUANTUM_PILLAR_V1__NOT_RUN__LAUNCH_FAILED__ENSAIO__GATE_UNTOUCHED", custody_chain_ok=False, summary={}),
                  {"pt": ["não produziu resultado válido"], "en": ["produced no valid result"]}),
        "reaproveitado": (dict(copy.deepcopy(FIX), reuse={"reused": True, "from_run_finished": "ENSAIO", "cache_dir": "ENSAIO"}),
                          {"pt": ["reaproveitado"], "en": ["reused"]}),
        "t1_sem_solucao": (dict(copy.deepcopy(FIX), summary=um._qp_summary(_RFi)), {"pt": ["sem solução finita"], "en": ["no finite solution"]})}
rep["variantes"] = {}
for _vn, (_vfix, _vdeve) in VARS.items():
    _cv = dict(copy.deepcopy(core0), quantum_pillar_v384=_vfix)
    for lang in ("pt", "en"):
        _tex = um._tex_guard_nan(um.build_pt(_cv, verdict, CORE0P) if lang == "pt" else um.build_en(_cv, verdict, CORE0P)); _txt = um._tex_to_txt(_tex)
        _nm = "dry_v384_%s_%s" % (_vn, lang)
        open(os.path.join(DRY, _nm + ".tex"), "w", encoding="utf-8").write(_tex)
        _r = subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", _nm + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800)
        rep["variantes"]["%s_%s" % (_vn, lang)] = {"pdflatex_rc": _r.returncode, "pdf_ok": os.path.exists(os.path.join(DRY, _nm + ".pdf")), "faltam": [w for w in _vdeve[lang] if w not in _txt]}
print("variantes:", json.dumps(rep["variantes"], ensure_ascii=False))
mau_var = [k for k, v in rep["variantes"].items() if v["pdflatex_rc"] != 0 or not v["pdf_ok"] or v["faltam"]]
um.OUT = DRY
um.emit_canonical_md(c, verdict)'''),
    ('''ok = (not mau and not bad and not _mf_err''', '''ok = (not mau and not mau_var and not bad and not _mf_err'''),
    ('''rep["veredito"] = "TUDO PASSOU" if ok else ("FALHOU: " + json.dumps({"artigo": mau, "nomes": bad,''', '''rep["veredito"] = "TUDO PASSOU" if ok else ("FALHOU: " + json.dumps({"artigo": mau, "variantes": mau_var, "nomes": bad,'''),
])
