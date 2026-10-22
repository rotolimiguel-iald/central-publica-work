# -*- coding: utf-8 -*-
"""ensaio_a_seco_v384.py -- ENSAIO A SECO do artigo e do fluxo principal da v384 (molde: ensaio_a_seco_v383.py), SEM a GPU do rito.

uso: python ensaio_a_seco_v384.py <candidato.py> <rotulo> <resultado_de_fumaca.json>

(1) copia o CANDIDATO para dry_<rotulo>/um.py e materializa ali o kernel EMBUTIDO dele;
(2) IMPORTA o candidato (stdout silenciado; o rito NAO roda: main() nao e chamado);
(3) o FLUXO PRINCIPAL: as instrucoes de main() que COMECAM numa linha marcada v384 (exceto as do terceiro balde, que leem variaveis locais do main e sao
    conferidas por nome e executadas A PARTE, em bloco, com core sintetico) sao EXECUTADAS com o core da v383 (o canonico selado), com
    quantum_pillar_start_v384 / quantum_pillar_finish_v384 SUBSTITUIDOS por stubs: o start NAO lanca a GPU; o finish devolve o registro montado pela
    PROPRIA _qp_summary do candidato a partir de um resultado de FUMACA do trabalhador (contagens minimas, especificacao de fumaca com hash proprio),
    com o veredito marcado ENSAIO -- nunca resultado;
(4) build_pt / build_en (+ _tex_guard_nan), pdflatex x2 com -halt-on-error; o markdown canonico e o manifesto (carimbo v384);
(5) confere as palavras que TEM de estar (a introducao e a nota), as que NAO podem estar (a frase da referencia na CPU no artigo de sucesso) e a guarda do
    rito (vereditos proibidos). Nada fora do pacote."""
import copy, hashlib, io, json, os, re, shutil, subprocess, sys, time, ast, builtins, textwrap
if sys.flags.optimize:   # as guardas sao assert: com -O elas sumiriam sem aviso (10a afericao)
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "v383"))
from carregar_embutido import carregar  # noqa: E402

NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
CORE0P = os.path.join(NOS, "um_absoluto.json")     # o core da v383 SELADA (o canonico)
CACHE0 = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache")
cand, rot, fumaca = sys.argv[1], sys.argv[2], os.path.abspath(sys.argv[3])
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
rep = {"candidato": cand, "sha16": h16, "kernel_materializado_no_dry": len(EMB), "core0_sha16": hashlib.sha256(open(CORE0P, "rb").read()).hexdigest()[:16],
       "fumaca": fumaca, "fumaca_sha16": hashlib.sha256(open(fumaca, "rb").read()).hexdigest()[:16]}

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
R0 = json.load(open(CORE0P, encoding="utf-8"))
core0, verdict = R0["core"], R0["verdict"]
assert "the_ledger_of_charges_v383" in core0 and "quantum_pillar_v384" not in core0
print("import ok (%.1f s); FORMAL_DIR = dry; CACHE = %s" % (rep["import_s"], um.CACHE))

# o registro do pilar a partir da FUMACA, pela propria _qp_summary do candidato (o mesmo codigo do rito)
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
       "summary": um._qp_summary(RF), "all_verified": False, "reuse": {"reused": False, "reading": "ENSAIO", "saved_to_cache": "ENSAIO_SEM_CACHE"}, "does_not_gate_core": True}
CALLS = {"start": 0, "finish": 0}


def _stub_start():
    CALLS["start"] += 1
    return {"mode": "ENSAIO"}


def _stub_finish(st, core):
    CALLS["finish"] += 1
    assert st.get("mode") == "ENSAIO"
    return copy.deepcopy(FIX)


TAG = "v384"
src = open(os.path.join(DRY, "um.py"), encoding="utf-8").read(); tree = ast.parse(src)
main = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"][0]
lines = src.splitlines()
tagged = {i + 1 for i, l in enumerate(lines) if TAG in l}
_txt_st = lambda st: NL.join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])
NL = chr(10)
# os enunciados do TERCEIRO BALDE (W08, W08b e o W08c, que leva a marca v384 na linha) leem variaveis locais do main (_not_sealed, _formais, _recusas,
# _computacao): saem do fluxo executado, sao conferidos por nome e o bloco inteiro roda a parte, abaixo (4a e 5a afericoes)
comeca = [st for st in main.body if st.lineno in tagged and "_computacao" not in _txt_st(st)]
contem = [st for st in main.body if st not in comeca and "_computacao" not in _txt_st(st) and any(ln in tagged for ln in range(st.lineno, (st.end_lineno or st.lineno) + 1))]
def assigned_before(lineno):
    a = set()
    for node in ast.walk(main):
        if getattr(node, "lineno", 10 ** 9) < lineno:
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store): a.add(node.id)
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)): a.add(node.name)
            if isinstance(node, ast.arg): a.add(node.arg)
    return a


# os enunciados do TERCEIRO BALDE: W08 e W08b sem a marca v384 na linha, o W08c com ela; os quatro saem do fluxo executado, sao conferidos por NOME aqui
# e o bloco inteiro roda a parte, abaixo (3a a 6a afericoes)
balde = [st for st in main.body if "_computacao" in _txt_st(st)]
bad = []
for st in balde:
    ab = assigned_before(st.lineno); loc = {m.id for m in ast.walk(st) if isinstance(m, ast.Name) and isinstance(m.ctx, ast.Store)}
    for node in ast.walk(st):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and not (hasattr(um, node.id) or hasattr(builtins, node.id) or node.id in ab or node.id in loc):
            bad.append((node.lineno, node.id))
for st in comeca + contem:
    ab = assigned_before(st.lineno); loc = {m.id for m in ast.walk(st) if isinstance(m, ast.Name) and isinstance(m.ctx, ast.Store)}
    for node in ast.walk(st):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            if st in contem and node.lineno not in tagged:
                continue
            if not (hasattr(um, node.id) or hasattr(builtins, node.id) or node.id in ab or node.id in loc or node.id in ("core", "_QP_ST_V384")):
                bad.append((node.lineno, node.id))
ns = dict(vars(um)); ns["core"] = json.loads(json.dumps(core0))
ns["quantum_pillar_start_v384"] = _stub_start; ns["quantum_pillar_finish_v384"] = _stub_finish
code = "\n".join(textwrap.dedent("\n".join(lines[st.lineno - 1:(st.end_lineno or st.lineno)])) for st in comeca)
_o = sys.stdout; sys.stdout = io.StringIO()
try:
    exec(compile(code, "<main:%s>" % TAG, "exec"), ns)
    _mf_out = sys.stdout.getvalue(); _mf_err = None
except Exception as e:  # noqa
    _mf_out = sys.stdout.getvalue(); _mf_err = repr(e)
finally:
    sys.stdout = _o
rep["mainflow"] = {"comeca": len(comeca), "contem": len(contem), "terceiro_balde": len(balde), "nomes_nao_resolvidos": bad, "erro": _mf_err, "stubs_chamados": dict(CALLS),
                   "chaves_novas_no_core": [k for k in ns["core"] if k not in core0], "stdout": _mf_out.strip().splitlines()}
print("fluxo principal:", json.dumps({k: v for k, v in rep["mainflow"].items() if k != "stdout"}, ensure_ascii=False))
c = ns["core"] if "quantum_pillar_v384" in ns["core"] else dict(copy.deepcopy(core0), quantum_pillar_v384=copy.deepcopy(FIX))

NAO_DEVE_CPU = {"pt": ["A referência na CPU, nesta rodada", "A referência na CPU não estava presente", "Não há registro da comparação com a CPU", "A comparação com a CPU"],
                "en": ["The CPU reference, in this run", "The CPU reference was not present", "There is no record of the CPU comparison", "The CPU comparison"]}   # 7a afericao
DEVE = {"pt": ["Introdução: o que este código faz agora (v384)", "três coisas", "ao mesmo tempo", "Nota: o que se calcula na GPU e como", "Os quatro testes",
               "A escala e a referência", "O que é e o que não é", "não falsificado não é confirmado", "Ao lado (v383) --- O livro de cobranças e a viscosidade"],
        "en": ["Introduction: what this code does now (v384)", "three things", "at the same time", "Note: what is computed on the GPU and how", "The four tests",
               "Scale and reference", "What it is and what it is not", "not falsified is not confirmed", "Beside (v383) --- The ledger of charges and the viscosity"]}
eng = shutil.which("pdflatex")
rep["pdflatex"] = eng
rep["artigo"] = {}
for lang in ("pt", "en"):
    t0 = time.time()
    tex = um._tex_guard_nan(um.build_pt(c, verdict, CORE0P) if lang == "pt" else um.build_en(c, verdict, CORE0P))
    txt = um._tex_to_txt(tex)
    nome = "dry_v384_%s" % lang
    open(os.path.join(DRY, nome + ".tex"), "w", encoding="utf-8").write(tex)
    open(os.path.join(DRY, nome + ".txt"), "w", encoding="utf-8").write(txt)
    rcs = []
    for _ in range(2):
        r = subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", nome + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800)
        rcs.append(r.returncode)
    log = open(os.path.join(DRY, nome + ".log"), encoding="latin-1", errors="replace").read()
    rep["artigo"][lang] = {"pdflatex_rc": rcs, "pdf_ok": os.path.exists(os.path.join(DRY, nome + ".pdf")),
                           "pdf_bytes": (os.path.getsize(os.path.join(DRY, nome + ".pdf")) if os.path.exists(os.path.join(DRY, nome + ".pdf")) else None),
                           "latex_errors": [l for l in log.splitlines() if l.startswith("! ")][:6], "tex_bytes": len(tex), "txt_bytes": len(txt),
                           "faltam": [w for w in DEVE[lang] if w not in txt and w not in tex],
                           # o SUCESSO nao traz a frase da referencia na CPU (so os vereditos anulados pela CPU a trazem; 5a afericao)
                           "nao_devia_ter": [w for w in NAO_DEVE_CPU[lang] if w in txt],
                           "nan": len(re.findall(r"(?<![A-Za-z])nan(?![A-Za-z])", txt)), "overfull": log.count("Overfull \\hbox"), "s": round(time.time() - t0, 1)}
    print("artigo", lang, json.dumps(rep["artigo"][lang], ensure_ascii=False))
    shutil.copyfile(os.path.join(DRY, nome + ".log"), os.path.join(HERE, "pdflatex_%s_%s.log" % (rot, lang)))
    i0 = txt.find("Introdu"); rep["artigo"][lang]["trecho"] = txt[i0:i0 + 2500] if i0 >= 0 else None
# o BLOCO DA CUSTODIA DE SENTIDO, executado a parte (4a afericao): de `_not_sealed = sorted(` ao print do W08c, com core sintetico e seal = {}
_i0 = next(i for i, l in enumerate(lines) if l.strip().startswith("_not_sealed = sorted("))
_i1 = next(i for i in range(_i0, len(lines)) if "computacao nao concluida: %s" in lines[i])
_i1 = next(i for i in range(_i1, len(lines)) if lines[i].rstrip().endswith('or "nenhuma"))'))
_bloco = textwrap.dedent(NL.join(lines[_i0:_i1 + 1]))
rep["custodia_de_sentido"] = {}
for _cn, _qv, _av in (("pilar_nao_concluido", "TGL_QUANTUM_PILLAR_V1__NOT_RUN__LAUNCH_FAILED__GATE_UNTOUCHED", False),
                      ("pilar_concluido", "TGL_QUANTUM_PILLAR_V1__FIVE_JUMP_GKLS__ENSAIO__GATE_UNTOUCHED", True)):
    _core_s = {"mod_a": {"verdict": "X_OK", "all_verified": True}, "mod_formal": {"verdict": "ALGO_EM_DIVIDA", "all_verified": False},
               "mod_recusa": {"verdict": "Y__INCONCLUSIVE__Z", "all_verified": False}, "quantum_pillar_v384": {"verdict": _qv, "all_verified": _av}}
    _ns_b = {"core": _core_s, "seal": {}}
    _o = sys.stdout; sys.stdout = io.StringIO()
    try:
        exec(compile(_bloco, "<custodia_de_sentido>", "exec"), _ns_b)
        _pr = sys.stdout.getvalue(); _er = None
    except Exception as e:  # noqa
        _pr = sys.stdout.getvalue(); _er = repr(e)
    finally:
        sys.stdout = _o
    _bal = (_ns_b.get("seal") or {}).get("not_sealed_this_run") or {}
    _esp = ["quantum_pillar_v384"] if not _av else []
    _ok_b = (_er is None and _bal.get("computacao_nao_concluida") == _esp and _bal.get("formais") == ["mod_formal"] and _bal.get("recusas_de_dado") == ["mod_recusa"]
             and ("computacao nao concluida: " + (", ".join(_esp) or "nenhuma")) in _pr)
    rep["custodia_de_sentido"][_cn] = {"ok": _ok_b, "erro": _er, "balde": _bal, "impresso": _pr.strip()}
print("custodia de sentido:", json.dumps({k: v["ok"] for k, v in rep["custodia_de_sentido"].items()}))
mau_bloco = [k for k, v in rep["custodia_de_sentido"].items() if not v["ok"]]
# as VARIANTES do registro (3a afericao): falha, reaproveitamento e T1 com estimativas sem solucao finita -- o artigo tem de compilar e dizer cada uma
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
        "t1_sem_solucao": (dict(copy.deepcopy(FIX), summary=um._qp_summary(_RFi)), {"pt": ["sem solução finita"], "en": ["no finite solution"]}),
        # 4a afericao: o D128 rodado (a fumaca nao o roda) e o resultado sem cache por falta do D128
        "d128_rodado": (dict(copy.deepcopy(FIX), summary=dict(copy.deepcopy(FIX["summary"]), D128={"d": 128, "nc": 3, "gamma_diss": 1.0, "started": True, "ran": True, "status_code": "RAN",
                                                                                                   "status": "UNIQUE", "n0": 1, "zero_mode_ok": True, "cci": 0.5, "spectrum_s": 600.0})),
                        {"pt": ["atrator UNIQUE"], "en": ["attractor UNIQUE"]}),
        # 7a afericao: o resumo falho com o veredito anulado pela CPU -- o artigo NAO afirma ausencia nem «nao ha registro»
        "resumo_falho_cpu_nao_comparavel": (dict(copy.deepcopy(FIX), verdict="TGL_QUANTUM_PILLAR_V1__CPU_REFERENCE_NOT_COMPARABLE__RESULTS_VOID__ENSAIO__GATE_UNTOUCHED",
                                                 custody_chain_ok=False, summary={}, summary_error="ENSAIO: resumo falho"),
                                            {"pt": ["não puderam ser resumidos"], "en": ["could not be summarized"]}),
        "sem_cache_d128": (dict(copy.deepcopy(FIX), reuse={"reused": False, "reading": "ENSAIO", "not_cached_code": "D128_NOT_RAN:NOT_RUN_DEADLINE",
                                                           "not_cached_because": "o D128 nao rodou nesta rodada (NOT_RUN_DEADLINE)"}),
                           {"pt": ["não foi guardado para reaproveitamento", "o cache só guarda o resultado completo com ele"],
                            "en": ["not stored for reuse", "the cache keeps only a complete result with it"]})}
rep["variantes"] = {}
for _vn, (_vfix, _vdeve) in VARS.items():
    _cv = dict(copy.deepcopy(core0), quantum_pillar_v384=_vfix)
    for lang in ("pt", "en"):
        _tex = um._tex_guard_nan(um.build_pt(_cv, verdict, CORE0P) if lang == "pt" else um.build_en(_cv, verdict, CORE0P)); _txt = um._tex_to_txt(_tex)
        _nm = "dry_v384_%s_%s" % (_vn, lang)
        open(os.path.join(DRY, _nm + ".tex"), "w", encoding="utf-8").write(_tex)
        _r = subprocess.run([eng, "-interaction=nonstopmode", "-halt-on-error", _nm + ".tex"], cwd=DRY, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1800)
        _nd = [w for w in NAO_DEVE_CPU[lang] if w in _txt] if _vn in ("resumo_falho_cpu_nao_comparavel", "d128_rodado", "sem_cache_d128", "t1_sem_solucao", "reaproveitado") else []
        rep["variantes"]["%s_%s" % (_vn, lang)] = {"pdflatex_rc": _r.returncode, "pdf_ok": os.path.exists(os.path.join(DRY, _nm + ".pdf")), "faltam": [w for w in _vdeve[lang] if w not in _txt],
                                                   "nao_devia_ter": _nd}
print("variantes:", json.dumps(rep["variantes"], ensure_ascii=False))
mau_var = [k for k, v in rep["variantes"].items() if v["pdflatex_rc"] != 0 or not v["pdf_ok"] or v["faltam"] or v.get("nao_devia_ter")]
um.OUT = DRY
um.emit_canonical_md(c, verdict)
md = open(os.path.join(DRY, "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
rep["markdown_v376"] = {"carimbo": "**Versão v384**" in md, "todos_os_modulos": "TODOS OS MODULOS COM VEREDITO" in md, "pilar": "quantum_pillar_v384" in md}
mani = os.path.join(DRY, "um_absoluto_manifest.md")
um.write_input_manifest_md({"CHAIN_OF_CUSTODY": {}}, mani, core=c)
rep["manifest_v376"] = {"carimbo": "**Versão v384**" in open(mani, encoding="utf-8").read()}
print("markdown:", rep["markdown_v376"], "| manifesto:", rep["manifest_v376"])
mau = [l for l, v in rep["artigo"].items() if v["latex_errors"] or not v["pdf_ok"] or v["faltam"] or v.get("nao_devia_ter")]
_GUARDA = ['if (re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", _v)', 'or re.search(r"(?<!AP)PROVED_BY", _v)', 'or "TGL_PROVED" in _v or "CONSCIOUSNESS_PROVED" in _v):']
assert all(src.count(g) == 1 for g in _GUARDA), "a guarda do rito mudou no candidato -- atualizar o ensaio"
_proib = [k for k, _m in c.items() if isinstance(_m, dict) and (re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", str(_m.get("verdict") or ""))
          or re.search(r"(?<!AP)PROVED_BY", str(_m.get("verdict") or "")) or "TGL_PROVED" in str(_m.get("verdict") or "") or "CONSCIOUSNESS_PROVED" in str(_m.get("verdict") or ""))]
rep["guarda_do_rito_vereditos_proibidos"] = _proib
ok = (not mau and not mau_var and not mau_bloco and not bad and not _mf_err and CALLS == {"start": 1, "finish": 1} and rep["markdown_v376"]["carimbo"] and rep["markdown_v376"]["todos_os_modulos"]
      and rep["manifest_v376"]["carimbo"] and not _proib and "quantum_pillar_v384" in rep["mainflow"]["chaves_novas_no_core"])
rep["veredito"] = "TUDO PASSOU" if ok else ("FALHOU: " + json.dumps({"artigo": mau, "variantes": mau_var, "custodia": mau_bloco, "nomes": bad, "erro": _mf_err, "stubs": CALLS, "md": rep["markdown_v376"], "mani": rep["manifest_v376"], "proib": _proib}, ensure_ascii=False))
json.dump(rep, open(os.path.join(HERE, "ensaio_a_seco_%s.json" % rot), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("\nVEREDITO DO ENSAIO A SECO (%s): %s" % (rot, rep["veredito"]))
sys.exit(0 if ok else 1)
