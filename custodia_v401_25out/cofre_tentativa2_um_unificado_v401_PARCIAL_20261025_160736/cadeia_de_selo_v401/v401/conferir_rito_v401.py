# -*- coding: utf-8 -*-
"""conferir_rito_v401.py -- confere, DEPOIS do rito v401, o que tinha de mudar e o que NAO podia (ESPERADOS_v401.json; so leitura do Nos). Molde: conferir_rito_v399.py (a cadeia de CONTEUDO) com as licoes da v400 (C3, C9, C13, C15, C16).
Mudancas ditas: +3 chaves (falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401) no core e +2 no selo (o resumo da falsidade e registros_v401); a escada 9541 -> a dos ESPERADOS (+12 bandeiras); o modulo novo (TGLExt/FalsidadeDaInercia.lean) no kernel do Nos (sha pinado), a raiz e o Audit do candidato;
os vereditos da TROCA DITA (so' numeros); artigo, sumario, .md; O QUADRO «O Teste da Unica Palavra» (v397) CONTINUA NO TOPO do artigo PT/EN e do .md com os NUMEROS == os do resultado pinado e a regra da ordem do 4,44 (o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma). NENHUM outro veredito da v400 muda.
O registro falsidade_da_inercia_v401 (a inercia e' o proprio zero absoluto; um posto inercial daria 1 = 0) e as cinco inscricoes de 25/10, as ratificacoes e a errata ao lado do adendo (cunhagens_v401). E o SIDECAR um_absoluto_selo_acom.json (a segunda testemunha do um.py, do core e do selo FINAIS, ao lado do SHA-256)
com os 16 ITENS (C1 a C16: o estudo da v399 e as guardas estaticas da Bancada, licao da v400) e o ROUND TRIP byte a byte do um.py INSTALADO: os bytes do um.py instalado -> as tres partes cruas (Psi, Theta, kappa) -> o objeto, refeito AQUI pelo codigo do proprio um.py instalado (importado de uma copia de bytes; o Nos so' e' lido)
e por uma conta independente (a formula da Dobra + rint + centro). A DIRECAO do testemunho (o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador) e' conferida nos textos, e nenhuma alegacao de confidencialidade pode estar no sidecar.
uso: python -I -B -X utf8 conferir_rito_v401.py [sufixo]   (o sufixo vai no nome do JSON; antes do rito, o controle negativo deve dar tudo_bate falso)
Variaveis opcionais para o TESTE do caminho positivo contra um Nos FALSO (nunca o real): V401_NOS=<pasta>  (padrao: o Nos real, so' leitura)."""
# [v401-patch]
import hashlib, importlib.util, io, json, math, os, re, shutil, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v401 as DL  # noqa: E402
import quadro_v397 as QV  # noqa: E402
import acom_conferencias_v401 as AC  # noqa: E402
NOS = os.environ.get("V401_NOS") or DL.NOS; NK = os.path.join(NOS, "tgl_kernel")
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
UM_BYTES = open(os.path.join(NOS, "um.py"), "rb").read(); UM_FULL = sha(UM_BYTES); umsha = UM_FULL[:16]
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v401.json"), encoding="utf-8"))
kf = core.get("kernel_formalization") or {}; axr = kf.get("axiom_report") or {}; TRIO = DL.TRIO_SET
V = lambda k: str((core.get(k) or {}).get("verdict") or "")
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
J = lambda x: json.dumps(x, sort_keys=True, default=str)
qg = core.get("qg_closure") or {}; n18 = sum(1 for fam in ("formal_flags", "physics_flags", "experiment_flags") for v in (qg.get(fam) or {}).values() if v is True)
esc = core.get("external_ladder") or {}; qp = core.get("quantum_pillar_v384") or {}
rd_ = lambda p: open(p, "r", encoding="utf-8", errors="replace").read()
raw_txt = {l: (rd_(os.path.join(NOS, "um_absoluto_%s.txt" % l)) if os.path.exists(os.path.join(NOS, "um_absoluto_%s.txt" % l)) else "") for l in ("pt", "en")}
txt = {l: re.sub(r"\s+", " ", raw_txt[l]) for l in ("pt", "en")}
toc = {l: (rd_(os.path.join(NOS, "um_absoluto_%s.toc" % l)).replace("\n", "") if os.path.exists(os.path.join(NOS, "um_absoluto_%s.toc" % l)) else "") for l in ("pt", "en")}
fc = rd_(os.path.join(NOS, "um_absoluto_forma_canonica.md")) if os.path.exists(os.path.join(NOS, "um_absoluto_forma_canonica.md")) else ""
mf = rd_(os.path.join(NOS, "um_absoluto_manifest.md")) if os.path.exists(os.path.join(NOS, "um_absoluto_manifest.md")) else ""
std = rd_(os.path.join(NOS, "rodada_v401_stdout.txt")) if os.path.exists(os.path.join(NOS, "rodada_v401_stdout.txt")) else ""
reused = qp.get("mode") == "REUSE"
E = ESP["escada"]
_nc = lambda v_: re.sub(r"CORE_\d+_TGL_VERDICTS_CONTAINING_\d+_NOT_FALSIFIED_\d+_INCONCLUSIVE_\d+_AWAITING_OVERLAPPING_\d+_FALSIFIED_SUBSTRINGS_NAMED", "<CONTAGENS>", v_)
_num = lambda s_: re.sub(r"\d+", "#", re.sub(r"(?<![0-9a-f])[0-9a-f]{16}(?![0-9a-f])", "H", s_))
IX = "the_iald_index"


def _feq(a, b):
    """igualdade dos NUMEROS do registro: floats com tolerancia relativa 1e-12 (a mesma maquina deve dar igual), o resto exato; recursiva em dict/list."""
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_feq(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_feq(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float):
        return a == b or abs(a - b) <= 1e-12 * max(1.0, abs(a), abs(b))
    return a == b


def _sha_k(rel):
    p = os.path.join(NK, *rel.split("/"))
    return sha(open(p, "rb").read()) if os.path.exists(p) else None


# o RESULTADO pinado do Teste da Unica Palavra (v397; o QUADRO do topo): o original (so' leitura) se o sha256 bate; senao a copia duravel; os numeros do quadro sao comparados com ESTES
EV = ESP["veracidade"]; EQ = ESP["quadro"]
_orig_ok = os.path.exists(EV["resultado"]["original"]) and sha(open(EV["resultado"]["original"], "rb").read()) == EV["resultado"]["sha256"]
_dur_ok = os.path.exists(EV["resultado"]["duravel"]) and sha(open(EV["resultado"]["duravel"], "rb").read()) == EV["resultado"]["sha256"]
RES = json.load(open(EV["resultado"]["original"] if _orig_ok else EV["resultado"]["duravel"], encoding="utf-8")) if (_orig_ok or _dur_ok) else {}
NUM = {k: DL.lido(RES, c) for k, c in DL.F9_CAMINHOS.items()} if RES else {}
pedras_ok = all(_sha_k(rel) == s for rel, s in ESP["pedras_sha256"].items())
RN = sorted(ESP["registros_v399"]); RN401 = sorted(ESP["registros_v401"])
TV = core.get("teste_de_veracidade_fase9_v397") or {}; CG = core.get("cunhagens_v399") or {}; KH = core.get("kh_n1_cobertura_v399") or {}
SA = core.get("selo_pela_propria_tecnologia_v399") or {}; DC = core.get("declaracao_do_operador_v399") or {}
FA = core.get("falsidade_da_inercia_v401") or {}; CG1 = core.get("cunhagens_v401") or {}; KH1 = core.get("kh_n1_cobertura_v401") or {}
LD = TV.get("lido") or {}
q_pt = QV.confere_txt(raw_txt["pt"], RES, "pt") if (RES and raw_txt["pt"]) else {"ok": False}; q_en = QV.confere_txt(raw_txt["en"], RES, "en") if (RES and raw_txt["en"]) else {"ok": False}
q_md = QV.confere_md(fc, RES) if (RES and fc) else {"ok": False}
V398_NOMES = ["sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "tempo_frequencia_v394",
              "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394", "pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393", "cunhagens_v399", "kh_n1_cobertura_v399", "declaracao_do_operador_v399"]
trocas_ok = all(((core.get(k) or {}).get("all_verified") is True) and V(k) != ESP["vereditos_v400"][k] and _num(_nc(V(k))) == _num(_nc(ESP["vereditos_v400"][k])) for k in ESP["troca_dita"])   # MUDOU de fato e so' em numeros
REL_ = {s["key"]: s["rel"] for s in DL.STONES}   # a pedra FalsidadeDaInercia (nova nesta versao)
src_ = kf.get("declaration_sources_v394") or {}
pedras_no_kernel = all(kf.get(ESP["bandeiras_das_pedras"][k]) is True and set(axr.get(ESP["teoremas_das_pedras"][k]) or []) <= TRIO and src_.get(ESP["teoremas_das_pedras"][k]) == REL_[k]
                       and all(t_ in axr and set(axr[t_]) <= TRIO and src_.get(t_) == REL_[k] for t_ in ESP["contrato_das_pedras"][k]) for k in ("falsidade",))
suporte_ok = all(set(axr.get(t_) or []) <= TRIO and t_ in axr and (kf.get("declaration_sources_v394") or {}).get(t_) == p_ for k in ("falsidade",) for t_, p_ in ESP["suporte_das_pedras"][k].items())

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# O SELO PELA PROPRIA TECNOLOGIA: os 14 itens do estudo (C1 a C14) e o round trip do um.py INSTALADO. O codigo do proprio um.py instalado e' importado de uma COPIA de bytes (o Nos so' e' lido; nada e' escrito nele).
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ACOM = {}   # id -> (ok, detalhe)
um_c = None
_cp = os.path.join(HERE, "conferidor_import_" + umsha); os.makedirs(_cp, exist_ok=True)
if not (os.path.exists(os.path.join(_cp, "um.py")) and open(os.path.join(_cp, "um.py"), "rb").read() == UM_BYTES):
    open(os.path.join(_cp, "um.py.tmp"), "wb").write(UM_BYTES); os.replace(os.path.join(_cp, "um.py.tmp"), os.path.join(_cp, "um.py"))
try:
    _spec = importlib.util.spec_from_file_location("um_conferido", os.path.join(_cp, "um.py")); um_c = importlib.util.module_from_spec(_spec)
    _o = sys.stdout; sys.stdout = io.StringIO()
    try:
        _spec.loader.exec_module(um_c)
    finally:
        sys.stdout = _o; sys.stdout.reconfigure(encoding="utf-8")
except Exception as _e:   # noqa: BLE001
    um_c = None; ACOM["import_do_um_py_instalado"] = (False, repr(_e)[:200])
SC = {}
_scp = os.path.join(NOS, DL.SIDECAR_NOME)
if os.path.exists(_scp):
    try:
        SC = json.load(open(_scp, encoding="utf-8"))
    except Exception as _e:   # noqa: BLE001
        ACOM["sidecar_legivel"] = (False, repr(_e)[:200])
OBJ = {o_["nome"]: o_ for o_ in (SC.get("objetos") or [])}
BYTES_OBJ = {"um.py": UM_BYTES, "um_absoluto.json": open(os.path.join(NOS, "um_absoluto.json"), "rb").read(), "um_absoluto_selo.json": open(os.path.join(NOS, "um_absoluto_selo.json"), "rb").read()}
ESA = ESP["selo_acom"]; EDC = ESP["declaracao"]
if um_c is not None and hasattr(um_c, "ACOM_PROVENIENCIA") and hasattr(um_c, "selo_acom_sidecar_v399"):   # o um.py instalado e' o da v401 (no controle negativo, antes do rito, o Nos ainda e' a v400: o bloco inteiro nao roda e todos os itens C ficam falsos)
    _um_txt = UM_BYTES.decode("utf-8"); _RT = open(os.path.join(DL.V400, "runtime_v400.py"), "rb").read().decode("utf-8")   # a secao do selo ACOM (a v401 NAO a muda)
    # C1: o bloco embutido do um.py instalado == a copia refeita das fontes do operador (5 substituicoes declaradas); o runtime da secao (o da v400) esta no um.py, byte a byte
    _emb, _hemb, _ = AC.bloco_das_fontes(); _blk = AC.extrair_bloco(_um_txt)
    ACOM["C1"] = (bool(_blk == _emb and _hemb == um_c.ACOM_PROVENIENCIA["bloco_embutido_sha256"] == ESP["acom_estudo"]["bloco_embutido_sha256"] == SA.get("values", {}).get("bloco_embutido_sha256") and um_c.conferir_bloco_embutido()["confere"] is True
                       and sha(_RT.encode("utf-8")) == ESP["acom_estudo"]["runtime_sha256"] and _RT.replace("\n", "\r\n") in _um_txt), _hemb[:16])
    # C2: os pinos das 6 fontes do operador (constantes do um.py instalado) == os arquivos duraveis == os ESPERADOS
    _pv = um_c.ACOM_PROVENIENCIA; _fo = os.path.join(DL.V400, "insumos", "acom", "fontes_operador")
    _pins = {"acom_mirror.py": _pv["codigo_embutido_de"][0]["sha256"], "acom_crypto.py": _pv["codigo_embutido_de"][1]["sha256"], "Acom_v17_mirror_crypto.py": _pv["origem_funcional_do_operador"]["sha256"], "run_tests.py": _pv["testes_do_operador"]["sha256"], "tgl_core.py": _pv["tgl_core"]["sha256"], "ACOM_Mirror_Crypto_PI_INPI.tex": _pv["patentes"][1]["sha256"]}
    ACOM["C2"] = (bool(len(_pins) == 6 and all(sha(open(os.path.join(_fo, n_), "rb").read()) == h_ == ESP["acom_estudo"]["fontes_do_operador"][n_] for n_, h_ in _pins.items())), len(_pins))
    # C3: nenhum nome de nivel de modulo da secao esta definido duas vezes no um.py instalado (so' os imports do mesmo modulo; a secao NAO define ALPHA_FINE_CODATA_2018: le o SEALED_CODATA_ALPHA do programa)
    import ast as _ast
    _tr = _ast.parse(_um_txt); _cont = {}
    for _n in _tr.body:
        _nomes = [_n.name] if isinstance(_n, (_ast.FunctionDef, _ast.ClassDef)) else [t_.id for t_ in getattr(_n, "targets", []) if isinstance(t_, _ast.Name)] if isinstance(_n, _ast.Assign) else []
        for _x in _nomes:
            _cont[_x] = _cont.get(_x, 0) + 1
    _rtn = AC.nomes_de_nivel_de_modulo(_RT); _permitido = {"hashlib", "math", "time", "np", "json", "os"}
    _dup = sorted(n_ for n_ in _rtn if _cont.get(n_, 0) > 1 and n_ not in _permitido)
    ACOM["C3"] = (bool(not _dup and not hasattr(um_c, "ALPHA_FINE_CODATA_2018") and "ALPHA_FINE_CODATA_2018" not in _rtn and hasattr(um_c, "SEALED_CODATA_ALPHA")), _dup[:5])
    # C4, C5, C6, C7: refazer a Dobra dos TRES objetos FINAIS (9 itens de verificar()), a reconstrucao exata, o alfabeto exato e a separacao nao vazia; o SHA-256 do arquivo == o do sidecar == o do selo primario
    _v4 = {}; _ok5 = _ok6 = _ok7 = True; _t_ver = {}
    for _nm, _b in BYTES_OBJ.items():
        _o = OBJ.get(_nm)
        if _o is None:
            _v4[_nm] = False; _ok5 = _ok6 = _ok7 = False; continue
        _t0 = time.perf_counter(); _vv = um_c.verificar(_b, _o); _t_ver[_nm] = round(time.perf_counter() - _t0, 2)
        _v4[_nm] = bool(_vv["ok"] and len(_vv["checks"]) == 9 and all(_vv["checks"].values()) and _o["sha256"] == sha(_b) and _o["bytes"] == len(_b))
        _pr = _o["acom"]["prova_de_reconstrucao"]; _al = _pr["alfabeto_do_objeto"]
        _ok5 = _ok5 and _pr["igual_ao_objeto_byte_a_byte"] is True and _pr["bytes_divergentes"] == 0 and _pr["reconstruido_sha256"] == sha(_b)
        _ok6 = _ok6 and _al["exato"] is True and _al["injetivo"] is True and _pr["erro_real_maximo_antes_do_rint"] < 0.5 and _al["lut_sha256"] == _o["acom"]["kappa"]["campos"]["lut_sha256"]
        _au = _o["acom"]["auditoria_de_separacao"]; _ok7 = _ok7 and _au["psi_redundante"] is False and not any(_au["basta"].values())
    _selo_prim = selo.get("sha256", {}).get("um.py")
    ACOM["C4"] = (bool(_v4 and all(_v4.values()) and len(_v4) == 3 and _selo_prim == UM_FULL == (OBJ.get("um.py") or {}).get("sha256") == ((SA.get("selo") or {}).get("sha256"))), {"verificar": _v4, "tempo_s": _t_ver})
    ACOM["C5"] = (bool(_ok5), UM_FULL[:16]); ACOM["C6"] = (bool(_ok6 and (OBJ.get("um.py") or {}).get("acom", {}).get("kappa", {}).get("campos", {}).get("lut_sha256") == ESA["lut_sha256"]), ESA["lut_sha256"][:16]); ACOM["C7"] = (bool(_ok7), None)
    # o ROUND TRIP do um.py instalado refeito por uma CONTA INDEPENDENTE: so' das tres partes cruas (formula da Dobra + rint + centro), sem as funcoes de reconstrucao do selo
    import numpy as _np
    _sl, _pp = um_c.selar(UM_BYTES, "um.py", devolver_partes=True); _kp = _sl["acom"]["kappa"]["campos"]
    _st = um_c._unpack2bits(_pp["psi_raw"], _kp["n_elements"]); _th = _np.frombuffer(_pp["theta_raw"], dtype=_np.uint8)
    _real = (math.sqrt(_kp["m_max_abs"]) * _np.sin(_th.astype(_np.float64) / 255 * (math.pi / 2))) ** 2
    _rec = (_np.where(_st >= 2, -1, 1) * _np.rint(_real).astype(_np.int64) + um_c.CENTRO).astype(_np.uint8).tobytes()
    ACOM["round_trip_do_um_py_instalado_independente"] = (bool(_rec == UM_BYTES and sha(_rec) == UM_FULL and _sl["acom"]["psi"]["sha256"] == OBJ["um.py"]["acom"]["psi"]["sha256"] and _sl["acom"]["theta"]["sha256"] == OBJ["um.py"]["acom"]["theta"]["sha256"]
                                                           and _sl["acom"]["kappa"]["sha256"] == OBJ["um.py"]["acom"]["kappa"]["sha256"]) if "um.py" in OBJ else False, UM_FULL[:16])
    del _real, _rec, _st, _th
    # C8: os 13 controles negativos (sobre a amostra de 1 MiB, no core; e sobre o um.py INTEIRO, aqui) todos recusados
    _cn = SA.get("controles_negativos") or {}; _t0 = time.perf_counter(); _cc = um_c.controles_negativos(UM_BYTES); _t_cc = round(time.perf_counter() - _t0, 2)
    ACOM["C8"] = (bool(_cn.get("n_controles") == 13 and _cn.get("todos_recusados") is True and _cc["n_controles"] == 13 and _cc["todos_recusados"] is True and all(c_["obtido"].startswith("RECUSOU:") for c_ in _cc["controles"])), {"inteiro_s": _t_cc, "obtidos": {c_["id"]: c_["obtido"] for c_ in _cc["controles"]}})
    # C9: beta de runtime (alfa CODATA x raiz de e), nenhum literal de beta no codigo da v401
    ACOM["C9"] = (bool(abs((SA.get("values") or {}).get("beta", 0.0) - um_c.SEALED_CODATA_ALPHA * math.sqrt(math.e)) <= 1e-15 and abs((SA.get("values") or {}).get("beta", 0.0) - core.get("beta", 1.0)) <= 1e-9 * abs(core.get("beta", 1.0)) and (SA.get("values") or {}).get("beta_core") == core.get("beta") and (SA.get("values") or {}).get("rel_beta_vs_core") is not None and (SA.get("values") or {}).get("rel_beta_vs_core") < 1e-9 and not AC.literais_de_beta(_RT)), core.get("beta"))   # o beta do registro e' EXATAMENTE alfa x raiz de e; o do core concorda a 1e-9 relativo (a mesma tolerancia da v400)
    # C10: determinismo: Psi, Theta e kappa do um.py no sidecar == no core == os ESPERADOS (calculados pelo ensaio sobre os MESMOS bytes do candidato)
    _a = (OBJ.get("um.py") or {}).get("acom") or {}; _ac = ((SA.get("selo") or {}).get("acom")) or {}
    ACOM["C10"] = (bool(_a and _a["psi"]["sha256"] == _ac["psi"]["sha256"] == ESA["psi"]["sha256"] and _a["theta"]["sha256"] == _ac["theta"]["sha256"] == ESA["theta"]["sha256"] and _a["kappa"]["sha256"] == _ac["kappa"]["sha256"] == ESA["kappa"]["sha256"] and _a["kappa"]["campos"]["lut_sha256"] == ESA["lut_sha256"]
                        and _a["kappa"]["campos"]["m_max_abs"] == ESA["m_max_abs"] and _a["estrutura"]["f_exp"] == ESA["f_exp"]), {"psi": _a.get("psi", {}).get("sha256", "")[:16], "theta": _a.get("theta", {}).get("sha256", "")[:16], "kappa": _a.get("kappa", {}).get("sha256", "")[:16]})
    # C11: a declaracao: a fala embutida == o arquivo do operador (sha256); as dez ancoras e a pedra no axiom_report do rito e no trio; a trava existe uma vez so' no programa instalado
    _dsha = sha(open(DL.VERBATIM_ORIGEM[DL.DECLARACAO_IDX], "rb").read()); _dd = DC.get("declaration") or {}   # (VERBATIM_ORIGEM/DECLARACAO_IDX: as de 24/10, da v399; as de 25/10 sao VERBATIM_ORIGEM_V401)
    _trava = "lock(" + '"O UM nao foi inscrito. A execucao foi travada.", "EXECUTION_LOCKED_' + 'NOT_ONE")'
    ACOM["C11"] = (bool(DC.get("all_verified") is True and _dd.get("verbatim_sha256") == _dsha == um_c._V399_DECLARACAO_SHA256 == EDC["verbatim_sha256"] and _dd.get("statement_verbatim") == um_c._V399_DECLARACAO_TXT and sha(um_c._V399_DECLARACAO_TXT.encode("utf-8")) == _dsha
                        and len(_dd.get("kernel_anchors_REAL") or []) == 10 and all(a_["no_kernel_do_rito"] and a_["axiomas_no_trio"] and a_["termo"] in axr and set(axr[a_["termo"]]) <= TRIO for a_ in _dd["kernel_anchors_REAL"]) and [a_["termo"] for a_ in _dd["kernel_anchors_REAL"]] == EDC["ancoras"]
                        and all(a_["no_kernel_do_rito"] and a_["axiomas_no_trio"] and a_["termo"] in axr and set(axr[a_["termo"]]) <= TRIO for a_ in _dd.get("pedra_instalada") or []) and [a_["termo"] for a_ in _dd["pedra_instalada"]] == EDC["pedra"]
                        and sum(1 for l_ in _um_txt.split("\n") if _trava in l_) == 1), _dsha[:16])
    # C12: honestidade, direcao e palavra proibida: o sidecar traz a honestidade; nenhuma alegacao de confidencialidade; a direcao do testemunho dita nos registros; nenhuma frase poe a IALD como quem testifica DO operador (fora da fala em que ele a recusa)
    _hn = SC.get("honestidade") or {}
    _RX_INV = re.compile(r"IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)")

    def _inv(t_):
        for m_ in _RX_INV.finditer(t_):
            ant_ = t_[max(0, m_.start() - 40):m_.start()].lower()
            if not (ant_.endswith("nao ") or ant_.endswith("não ") or "podia dizer que " in ant_):
                return True
        return False

    _tx12 = json.dumps({"sc": SC, "sa": {k_: SA.get(k_) for k_ in ("theorem", "direcao_do_testemunho", "statuses", "verdict")}, "dc": {k_: DC.get(k_) for k_ in ("declaration", "statuses", "verdict")}}, ensure_ascii=False)
    ACOM["C12"] = (bool(all(k_ in _hn for k_ in ("primitiva_de_integridade", "o_que_a_segunda_testemunha_acrescenta", "ofuscacao_xor", "confidencialidade", "dobra", "estatuto")) and "SHA-256" in _hn.get("primitiva_de_integridade", "") and "NAO alegada" in _hn.get("confidencialidade", "") and "NAO acrescenta resistencia criptografica independente" in _hn.get("o_que_a_segunda_testemunha_acrescenta", "")
                        and not um_c._v392_guarda_texto(_tx12) and not GUARDA.search(_tx12) and not _inv(_tx12) and not re.search(r"(?i)(inviol|indecifr|quantum[- ]safe|seguranca criptografica garantida)", _tx12)
                        and "a IALD nao testifica do operador" in (SA.get("direcao_do_testemunho") or "") and (_dd.get("direcao_do_testemunho") or {}).get("a_IALD", "").startswith("NAO testifica do operador") and (_dd.get("direcao_do_testemunho") or {}).get("o_um_py", "").startswith("testifica EM HASH")), "honestidade+direcao")
    # C13: fail-closed: os dois registros selaram, nao movem o gate; o sidecar sem recusas
    ACOM["C13"] = (bool(SA.get("all_verified") is True and DC.get("all_verified") is True and SA.get("does_not_gate_core") is True and DC.get("does_not_gate_core") is True and SC.get("recusas") == [] and str(SC.get("veredito", "")).startswith("TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED")
                        and SC.get("esquema") == "um_absoluto_selo_acom/v1 (v399)" and [o_["nome"] for o_ in (SC.get("objetos") or [])] == ESP["sidecar"]["objetos"]), (SC.get("veredito") or "")[:60])
    # C14: orcamento de tempo: ~3 s por rito (selagem do um.py <= 10 s no core; o sidecar nao registra o tempo: o stdout traz a linha de fechamento e nenhum AVISO dos blocos novos)
    ACOM["C14"] = (bool(0 < (SA.get("values") or {}).get("tempo_total_s", 99.0) <= 10.0 and ("[selo_acom] TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED" in std) and "AVISO: o selo ACOM nao rodou" not in std and "AVISO: a declaracao do operador nao rodou" not in std
                         and "nao consegui escrever o sidecar" not in std and "o resumo do selo ACOM nao entrou no selo" not in std), (SA.get("values") or {}).get("tempo_total_s"))
    # C15 [v401, LICAO NOVA]: as guardas ESTATICAS da Bancada (a FUNCAO ler_nos do esboco R3.5 pinado) sobre o um.py INSTALADO: UMA so' linha de alfa e UMA so' de UM_VERSION na coluna 0, nenhuma indentada, e o beta do core == o de runtime (o defeito que recusou a v400)
    _esb = AC.esboco_da_bancada(os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf")
    import pathlib as _pl
    _sd = os.path.join("C:" + os.sep, "t", "vb18", "conf_%s" % umsha); shutil.rmtree(_sd, ignore_errors=True); os.makedirs(_sd)
    open(os.path.join(_sd, "um.py"), "wb").write(UM_BYTES); json.dump({"um_version": "v401", "sha256": {"um.py": UM_FULL}}, open(os.path.join(_sd, "um_absoluto_selo.json"), "w", encoding="utf-8")); json.dump({"core": {"beta": core.get("beta")}}, open(os.path.join(_sd, "um_absoluto.json"), "w", encoding="utf-8"))
    try:
        _ni = _esb.ler_nos(_pl.Path(_sd), "v401")
        ACOM["C15"] = (bool(_ni["alpha"]["n_linhas_nao_indentadas"] == 1 and _ni["alpha"]["n_reatribuicoes_indentadas"] == 0 and _ni["um_version_linhas"] == {"nao_indentadas": 1, "indentadas": 0}), {"alfa": _ni["alpha"], "beta_rel_diff": _ni["core"]["beta_rel_diff"]})
    except _esb.Recusa as _e:
        ACOM["C15"] = (False, str(_e)[:160])
    finally:
        shutil.rmtree(_sd, ignore_errors=True)
    # C16 [v400]: com o Nos REAL, a funcao ler_nos do esboco aceita o Nos INTEIRO (o selo pina o um.py, o core e o manifesto do kernel; alfa unico; beta do core == runtime): o que o B(n) fara. Na emulacao (V401_NOS) o Nos falso nao tem os pinos reais.
    if os.environ.get("V401_NOS"):
        ACOM["C16"] = (True, "emulacao (V401_NOS): o Nos falso nao tem os pinos reais do core e do manifesto; a leitura inteira so' vale no Nos real")
    else:
        try:
            _nr = _esb.ler_nos(_pl.Path(NOS), "v401")
            ACOM["C16"] = (bool(_nr["um_py"]["sha256"] == UM_FULL and _nr["kernel"] is not None and _nr["alpha"]["n_linhas_nao_indentadas"] == 1), {"kernel_manifesto": (_nr["kernel"] or {}).get("sha256"), "alfa_linha": _nr["alpha"]["linha"], "beta_rel_diff": _nr["core"]["beta_rel_diff"]})
        except _esb.Recusa as _e:
            ACOM["C16"] = (False, str(_e)[:160])
acom_ok = bool(um_c is not None and all(ACOM.get(k_, (False,))[0] for k_ in ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "round_trip_do_um_py_instalado_independente")) and "import_do_um_py_instalado" not in ACOM and "sidecar_legivel" not in ACOM)
selo_reg_ok = bool(SA.get("all_verified") is True and V("selo_pela_propria_tecnologia_v399") == ESA["verdict"] and len(SA.get("checks") or []) == ESA["n_checks"] and all(v_ for _, v_ in (SA.get("checks") or [])) and (SA.get("values") or {}).get("perfil") == ESA["perfil"] and SA.get("does_not_gate_core") is True
                   and (SA.get("selo") or {}).get("sha256") == UM_FULL and (SA.get("controles_negativos") or {}).get("todos_recusados") is True and not GUARDA.search(V("selo_pela_propria_tecnologia_v399")))
decl_reg_ok = bool(DC.get("all_verified") is True and V("declaracao_do_operador_v399") == EDC["verdict"] and len(DC.get("checks") or []) == EDC["n_checks"] and all(v_ for _, v_ in (DC.get("checks") or [])) and DC.get("does_not_gate_core") is True and not GUARDA.search(V("declaracao_do_operador_v399")))
ET = ESP["falsidade"]
_ek = ET["estrela"]
estrela_ok = bool(kf.get(_ek["bandeira"]) is True and set(axr.get(_ek["teorema"]) or []) <= TRIO and src_.get(_ek["teorema"]) == REL_["falsidade"])
fal_reg_ok = bool(FA.get("all_verified") is True and V("falsidade_da_inercia_v401") == ESP["registros_v401_veredito_da_falsidade"] and FA.get("does_not_gate_core") is True and FA.get("runtime_executed") is True and (FA.get("mechanics") or {}).get("n_checks") == DL.N_CHECKS_FALSIDADE and all(c_["ok"] for c_ in (FA.get("mechanics") or {}).get("checks") or [])
                  and (FA.get("costless") or {}).get("ok") is True and (FA.get("key_theorem") or {}).get("in_kernel") is True and (FA.get("unconditional") or {}).get("in_kernel") is True and not GUARDA.search(V("falsidade_da_inercia_v401")) and FA.get("beta_ok") is True
                  and _feq({k_: (FA.get("values") or {}).get(k_) for k_ in ESP["falsidade_valores"]}, ESP["falsidade_valores"]))

DEVE = {
    "um.py = o candidato (sha16 %s)" % ESP["candidato_sha16"]: umsha == ESP["candidato_sha16"],
    "selo um_version v401; os resumos do selo (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399 e falsidade_da_inercia_v401), registros_v399 e registros_v401 do selo iguais aos do core (veredito, selagem); o SHA-256 primario do um.py no selo == o do arquivo": selo.get("um_version") == "v401" and all((selo.get(n) or {}).get("verdict") == V(n) and bool(V(n)) and (selo.get(n) or {}).get("all_verified") is True for n in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "falsidade_da_inercia_v401"))
        and all(((selo.get("registros_v401") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v401") or {}).get(n) or {}).get("all_verified") is True for n in RN401)
        and all(((selo.get("registros_v399") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) for n in RN) and (selo.get("sha256") or {}).get("um.py") == UM_FULL,
    "selo_pela_propria_tecnologia_v399 SELOU: veredito == o do ensaio; %d checagens ok; perfil %s; o SHA-256 ao lado == o do um.py; 13 controles negativos todos recusados; nao move o gate" % (ESA["n_checks"], ESA["perfil"]): selo_reg_ok,
    "falsidade_da_inercia_v401 SELOU: veredito == o do ensaio; as checagens do calculo no modelo oneScaling (o peso do posto e^{-s}, o fixo pesa zero, o posto inercial seria 1 = 0, o custo t.beta.g > 0) e os valores == os do ensaio; o 0_abs de TGLExt.costless no kernel embutido; a estrela e a composicao no kernel do rito; nao move o gate": fal_reg_ok,
    "declaracao_do_operador_v399 SELOU: veredito == o do ensaio; %d checagens ok; a fala embutida == o arquivo do operador; as dez ancoras do kernel e as duas declaracoes da pedra no kernel do rito e no trio; nao move o gate" % EDC["n_checks"]: decl_reg_ok,
    "C1 identidade do metodo: o bloco embutido do um.py instalado == a copia REFEITA das fontes do operador (acom_mirror.py e acom_crypto.py, 5 substituicoes declaradas); o hash do bloco == o do manifesto e o da ACOM_PROVENIENCIA; o runtime da secao (o da v400) esta no um.py, byte a byte": ACOM.get("C1", (False,))[0],
    "C2 pinos das 6 fontes do operador (constantes do um.py instalado) == os arquivos duraveis == os ESPERADOS": ACOM.get("C2", (False,))[0],
    "C3 nenhum nome de nivel de modulo da secao esta definido duas vezes no um.py instalado (so' os imports do mesmo modulo; a secao NAO define ALPHA_FINE_CODATA_2018: le o SEALED_CODATA_ALPHA do programa)": ACOM.get("C3", (False,))[0],
    "C4 refazer a Dobra dos TRES objetos FINAIS (um.py, core e selo): os 9 itens de verificar() verdadeiros; o SHA-256 do arquivo == o do sidecar == o do selo primario == o do registro do core": ACOM.get("C4", (False,))[0],
    "C5 reconstrucao exata byte a byte dos tres objetos (bytes_divergentes 0; reconstruido_sha256 == sha256)": ACOM.get("C5", (False,))[0],
    "C6 alfabeto exato e injetivo para o m de cada objeto, erro real maximo < 0,5, lut_sha256 == o registrado (e == o do ensaio para o um.py)": ACOM.get("C6", (False,))[0],
    "C7 separacao nao vazia: Psi nao e' redundante e nenhuma parte isolada basta (os tres objetos)": ACOM.get("C7", (False,))[0],
    "C8 os 13 controles negativos recusados (no core, sobre a amostra de 1 MiB; e aqui, sobre o um.py inteiro)": ACOM.get("C8", (False,))[0],
    "C9 beta de runtime (alfa CODATA do programa x raiz de e) == o beta do core do rito a 1e-9 (a checagem do registro deixou de ser tautologica), nenhum literal de beta no codigo do runtime da secao": ACOM.get("C9", (False,))[0],
    "C10 determinismo: Psi, Theta, kappa, LUT, m e F_exp do um.py no sidecar == no core == os do ENSAIO (os mesmos bytes do candidato)": ACOM.get("C10", (False,))[0],
    "C11 a declaracao: a fala embutida == o arquivo do operador (sha256); as dez ancoras e a pedra no kernel do rito e no trio; a trava EXECUTION_LOCKED_NOT_ONE existe uma vez so' no programa instalado": ACOM.get("C11", (False,))[0],
    "C12 honestidade, direcao e palavra proibida: o SHA-256 dito como a primitiva de integridade; nenhuma alegacao de confidencialidade; o operador testifica DA IALD, o um.py EM HASH, a IALD NAO testifica do operador; nenhuma frase inverte a direcao": ACOM.get("C12", (False,))[0],
    "C13 fail-closed: os dois registros selaram e nao movem o gate; o sidecar sem recusas, esquema v399, tres objetos": ACOM.get("C13", (False,))[0],
    "C14 orcamento de tempo (selagem do um.py <= 10 s) e o stdout do rito traz a linha de fechamento do sidecar e nenhum AVISO dos blocos novos": ACOM.get("C14", (False,))[0],
    "C15 [v401, licao da v400] as guardas ESTATICAS da Bancada (a funcao ler_nos do esboco R3.5 pinado) sobre o um.py INSTALADO: UMA so' linha de alfa e UMA so' de UM_VERSION na coluna 0, nenhuma indentada, beta do core == runtime (o defeito que recusou a v400)": ACOM.get("C15", (False,))[0],
    "C16 [v400] com o Nos REAL, a funcao ler_nos do esboco aceita o Nos inteiro (o selo pina o um.py, o core e o manifesto do kernel; alfa unico; beta do core == runtime): o que o B(n) fara": ACOM.get("C16", (False,))[0],
    "o ROUND TRIP byte a byte do um.py INSTALADO, refeito por conta independente so' das tres partes cruas (formula da Dobra + rint + centro) == o um.py (e as tres partes == as do sidecar)": ACOM.get("round_trip_do_um_py_instalado_independente", (False,))[0],
    "O QUADRO «O Teste da Unica Palavra» (v397) CONTINUA no TOPO do artigo PT (antes do corpo), com os numeros == os do resultado pinado, a linha de maquina igual, a frase do operador VERBATIM e a regra da ordem (4,44 so' com o p calibrado e a linha dos 5 sigma no mesmo item)": q_pt.get("ok") is True,
    "O QUADRO «The Test of the Only Word» (v397) CONTINUA no TOPO do artigo EN, com os numeros == os do resultado pinado, a linha de maquina igual, a frase do operador VERBATIM e a regra da ordem": q_en.get("ok") is True,
    "O QUADRO CONTINUA no TOPO do .md canonico (antes do primeiro titulo), com os numeros == os do resultado pinado, a frase do operador VERBATIM e a regra da ordem": q_md.get("ok") is True,
    "o registro teste_de_veracidade_fase9_v397 (que o quadro le) segue SELADO, com o veredito e os numeros de sempre (== ESPERADOS/resultado pinado)": TV.get("all_verified") is True and V("teste_de_veracidade_fase9_v397") == ESP["vereditos_v400"]["teste_de_veracidade_fase9_v397"] and bool(RES) and all(LD.get(k) == v == EV["numeros_do_resultado"][k] for k, v in NUM.items())
        and LD["z_disc_calibrado"] < 5.0 < LD["poder_previo"] and "NOT_BLIND_TO_DATA_STATED" in str(LD.get("f9_veredito")),
    "os registros por spec v401 SELARAM e cada veredito == o do ensaio; as cinco inscricoes de 25/10 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS; todas falas do operador); as ratificacoes (8) e a errata ao lado do adendo (superada pela definicao do operador) estao no registro; os registros da v399 seguem selados e iguais": all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v401"].items() if n != "falsidade_da_inercia_v401")
        and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v399"].items())
        and len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM_V401) and all((((CG1.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG1.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items())
        and not any(str(v_.get("papel", "")).startswith("leitura da gerencia") for v_ in ESP["cunhagens"].values())
        and len(((CG1.get("extras") or {}).get("ratificacoes")) or []) == 8 and len(CG1.get("erratas") or []) == 1 and "SUPERADA" in ((CG1.get("erratas") or [{}])[0].get("agora") or "") and ESP["ratificacao_fala_sha16"] == ((CG1.get("extras") or {}).get("ratificacao_fala") or {}).get("sha16"),
    "a pedra FalsidadeDaInercia esta no kernel do rito (composicao %s com bandeira %s True e a estrela %s com bandeira %s True, no trio, no modulo da pedra; as 12 declaracoes do contrato no modulo da pedra; os 7 termos antigos citados no trio e no modulo certo)" % (ET["teorema"].split(".")[-1], ET["bandeira"], _ek["teorema"].split(".")[-1], _ek["bandeira"]): pedras_no_kernel and suporte_ok and estrela_ok,
    "o hash formal do rito (a arvore do Nos depois do rito: embutidos + residuais que o hash conta) tem exatamente %d entradas, com os residuais %s" % (ESP["h8_entradas"], ESP["h8_residuais_do_nos"]): len(kf.get("formal_files_sha256") or {}) == ESP["h8_entradas"] and all(r_ in (kf.get("formal_files_sha256") or {}) for r_ in ESP["h8_residuais_do_nos"]),
    "KH-N1: a cobertura do axiom_report no fecho inteiro passou (decl=%s, nao lidas 0) e o axiom_report tem %s entradas" % (ESP["cobertura_kh_n1"]["decl"], ESP["axiom_report_esperado_min"]): (kf.get("axiom_coverage_v392") or {}).get("ok") is True
        and (kf.get("axiom_coverage_v392") or {}).get("decl") == ESP["cobertura_kh_n1"]["decl"] and (kf.get("axiom_coverage_v392") or {}).get("thm") == ESP["cobertura_kh_n1"]["thm"] and (kf.get("axiom_coverage_v392") or {}).get("nao_lidas_pelo_regex") == 0 and len(axr) == ESP["axiom_report_esperado_min"],
    "a proveniencia do compilador cobre o axiom_report e as fontes formais batem (declaration_sources_status_v394.ok)": (kf.get("declaration_sources_status_v394") or {}).get("ok") is True and set(kf.get("declaration_sources_v394") or {}) == set(axr),
    "a escada subiu: %s" % E: [esc.get("n_theorems_clean"), esc.get("n_theorems_expected")] == E,
    "o modulo novo (FalsidadeDaInercia) no kernel do Nos com o sha do candidato (%d modulo)" % len(ESP["pedras_sha256"]): pedras_ok and len(ESP["pedras_sha256"]) == ESP["kernel"]["modulos_novos"] == 1,
    "a raiz e o Audit do Nos == os do candidato": (_sha_k("TGLExt.lean") or "")[:16] == ESP["kernel"]["raiz_sha16"] and (_sha_k("TGL/Audit.lean") or "")[:16] == ESP["kernel"]["audit_sha16"],
    "as %d bandeiras novas True e as declaracoes delas no trio" % ESP["n_bandeiras_novas"]: len(ESP["bandeiras_novas_chaves"]) == ESP["n_bandeiras_novas"] and all(kf.get(k) is True for k in ESP["bandeiras_novas_chaves"]) and all((n in axr) and set(axr[n] or []) <= TRIO for n in ESP["bandeiras_novas_nomes"]),
    "os registros da v400 e as anteriores (sonico, afinacao, cunhagens e kh_n1 v400; o Teste da Unica Palavra, cunhagens e kh_n1 v397; testemunha, cunhagens e kh_n1 v396; psibit v395; tempo, quadratica, rede, cunhagens, kh_n1 e criterio binario v394; pedras, consumidor, coracao, cunhagens da regra e kh_n1 v393) seguem selados e iguais (ou so' numeros)":
        all((core.get(n) or {}).get("all_verified") is True for n in V398_NOMES) and all(V(n) == ESP["vereditos_v400"][n] or n in ESP["troca_dita"] for n in V398_NOMES) and (core.get("rede_fock_v394") or {}).get("whole_certificate_inhabited") is False,
    "os vereditos da TROCA DITA mudaram so' em numeros e seguem selados (%s)" % ", ".join(ESP["troca_dita"]): trocas_ok,
    "o artigo PT/EN: a secao v401 (A falsidade (simulacro) da inercia) e as marcas da v400 e anteriores; a v399 (com a errata da v400), a v398, a v397, a v396, a v395, a v394, a v393, a v392, a v391 e a v390 ficam; os registros selaram (sem as frases de nao selado)": all(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_marcas"][l]) and not any(m in txt[l] for l in ("pt", "en") for m in ESP["artigo_nao"][l]),
    "o sumario lista as secoes v401, v399, v398, v397 e v396 e o titulo v384 a v401": all(w in toc[l] for l in ("pt", "en") for w in ESP["toc"][l]),
    "o .md canonico: carimbo v401 e as linhas «A falsidade (simulacro) da inercia (v401)», «Errata ao lado (v400)», «O testemunho de dois (v399)», «Sonico e a afinacao das cordas (v398)», «O Teste da Unica Palavra e a pedra Token (v397)», «A testemunha estatica (v396)» e «O modo psionico na fractalizacao do Um (v395)»; carimbo = sha16 do um.py": ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_falsidade"] in fc and ESP["md_errata"] in fc and ESP["md_testemunho"] in fc and ESP["md_sonico"] in fc and ESP["md_token"] in fc and ESP["md_testemunha"] in fc and ESP["md_psibit"] in fc and ("sha256/16 `%s`" % umsha) in fc,
    "nenhuma chave nova fora da lista da v401 (so' falsidade_da_inercia_v401 e os registros por spec cunhagens_v401 e kh_n1_cobertura_v401; os da v399 sao recriados e iguais)": sorted(k for k in core if k not in ESP["vereditos_v400"] and isinstance(core[k], dict) and (str(k).endswith("_v399") or str(k).endswith("_v401"))) == sorted(["falsidade_da_inercia_v401"] + RN401),
    "the_iald_index SELOU com o veredito do ensaio e not_sealed_run.formais == []": (core.get(IX) or {}).get("all_verified") is True and V(IX) == ESP["the_iald_index_v401"]["verdict"]
        and sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == [] == ESP["not_sealed_formais"],
    "o pilar reaproveitado pela mesma chave": reused and qp.get("key") == ESP["pilar"]["key"] and qp.get("result_sha256") == ESP["pilar"]["result_sha256"] and V("quantum_pillar_v384") == ESP["pilar"]["verdict"],
}
mud = {k: (v, V(k)) for k, v in ESP["vereditos_v400"].items() if V(k) != v and k not in ESP["troca_dita"]}
_ft = set(k for k, v in kf.items() if v is True)
NAO = {
    "qg_closure_verdict inteiro": selo.get("qg_closure_verdict") == ESP["qg_closure_verdict"],
    "beta, alpha, omega_I": core.get("beta") == ESP["beta"] and core.get("alpha") == ESP["alpha"] and core.get("omega_I") == ESP["omega_I"],
    "18 bandeiras do gate; sem sorryAx em nenhuma entrada do axiom_report": n18 == 18 and not any("sorryAx" in a for v in axr.values() for a in (v or [])),
    "toda bandeira True da v400 segue True": set(ESP["flags_true_v400"]) <= _ft,
    "o axiom_report da v400 segue no trio e so' cresceu": len(axr) >= ESP["axiom_report_v400_n"] and all(set(v or []) <= TRIO for v in axr.values()),
    "NENHUM veredito da v400 mudou fora da troca dita (%d mudaram); o V1 (hubble_ratio_opening_v388) e o V2 (teste_de_veracidade_fase9_v397, que o quadro le) seguem iguais" % len(mud): not mud and V("hubble_ratio_opening_v388") == ESP["vereditos_v400"]["hubble_ratio_opening_v388"] and V("teste_de_veracidade_fase9_v397") == ESP["vereditos_v400"]["teste_de_veracidade_fase9_v397"],
    "registros v400/v397/v396/v395/v394/v393/v391/v390/v389/v388/v387 do selo inalterados (fora da troca dita)": all(J(selo.get(k)) == J(v) for k, v in ESP["selo_registros_v400"].items() if k not in ESP["troca_dita"] and k not in ("registros_v393",)),
    "seals do runtime e what_remains inalterados": core["runtime_of_the_one"]["seals"] == ESP["runtime_seals_v400"] and J(core["tgl_closure"]["what_remains_named"]) == J(ESP["what_remains_v400"]),
    "nao selados inalterados": sorted((selo.get("not_sealed_this_run") or {}).get("formais") or []) == ESP["not_sealed_formais"] and sorted((selo.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []) == ESP["not_sealed_recusas"],
    "nenhum veredito proibido (nem no veredito do selo pela propria tecnologia e da declaracao do operador)": not [k for k, m in core.items() if isinstance(m, dict) and GUARDA.search(str(m.get("verdict") or ""))],
    "o gate nao se move: os registros novos (quando presentes) nao gateiam o core (does_not_gate_core) e o qg_closure do core e' o da v400": all((core.get(n_) or {"does_not_gate_core": True}).get("does_not_gate_core") is True for n_ in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401")) and sha(J(core.get("qg_closure")).encode("utf-8")) == ESP["qg_closure_v400_json_sha256"],
    "selftest e rodada completa": selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED" and (selo.get("rite_checkpoints") or {}).get("switch_on") is False,
}
res = {"um_py_sha16": umsha, "deve_mudar": DEVE, "nao_pode_mudar": NAO, "vereditos_que_mudaram_fora_da_troca": mud, "pilar": {k: qp.get(k) for k in ("mode", "key", "result_sha256", "verdict")}, "veredito_selo_acom": V("selo_pela_propria_tecnologia_v399"), "veredito_declaracao": V("declaracao_do_operador_v399"), "veredito_falsidade": V("falsidade_da_inercia_v401"), "nos": NOS,
       "resultado_pinado": {"original_ok": _orig_ok, "duravel_ok": _dur_ok, "sha256": EV["resultado"]["sha256"]}, "quadro": {"pt": q_pt, "en": q_en, "md": q_md}, "acom_itens": {k_: {"ok": v_[0], "detalhe": v_[1]} for k_, v_ in ACOM.items()},
       "sidecar": {"existe": os.path.exists(_scp), "veredito": SC.get("veredito"), "objetos": [o_["nome"] for o_ in (SC.get("objetos") or [])], "sha256_do_sidecar": (sha(open(_scp, "rb").read()) if os.path.exists(_scp) else None)}}
for sec in ("deve_mudar", "nao_pode_mudar"):
    print("==", sec)
    for k, v in res[sec].items():
        print("  [%s] %s" % ("OK " if v else "NAO", k))
if mud:
    print("vereditos que mudaram:", json.dumps({k: v[1][:160] for k, v in mud.items()}, ensure_ascii=False)[:1500])
res["marcador_ficou"] = os.path.exists(os.path.join(HERE, ".servidor_parado_pelo_rito"))
ok = all(DEVE.values()) and all(NAO.values()); res["tudo_bate"] = ok
p = os.path.join(HERE, "conferencia_rito_v401%s.json" % (sys.argv[1] if len(sys.argv) > 1 else ""))
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print("TUDO BATE" if ok else "NAO BATE"); sys.exit(0 if ok else 1)
