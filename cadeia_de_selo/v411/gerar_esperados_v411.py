# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] ESCRITO DE NOVO (varrido, nao remendado) a partir do molde v410/gerar_esperados_v410.py para uma versao SEM modulo novo: UM registro com funcao (h0dn_bg1_v411), os specs cunhagens_v411 e kh_n1_cobertura_v411; os quatro registros com funcao da v410 e os specs da v410 viram HERANCA (registros_funcao_v410, estrelas_v410, bundle_v410_sha256...); o esquema das chaves e' o da v410 subido de rotulo (409 -> 410, 410 -> 411)
"""gerar_esperados_v411.py -- ESPERADOS_v411.json LIDOS dos artefatos (molde: gerar_esperados_v410.py FINAL). A v411 NAO tem modulo novo no kernel (o da v410, byte a byte; escada e cobertura iguais); tem UM registro com funcao,
h0dn_bg1_v411 (16 checagens: o teste H0DN x BG1 aberto uma vez, RECALCULADO no rito a partir dos bytes embutidos; o primario sob o modelo de erros publicado e, ao lado, as Cefeidas livres; retrodicao sem ajuste, emenda posterior a
guarda, teste nao cego; provado e' validade, nao creditacao; o gate nao se move), e os dois por spec cunhagens_v411 (as 11 falas de 11 e 12/11 CITADAS por data e sha256, nao transcritas, lidas de DL.FALAS_V411; D159 a D181, DL.DECISOES_V411; as erratas E41 a E44 ao lado) e kh_n1_cobertura_v411.
O ESQUEMA e' o do ESPERADOS_v410 com os rotulos subidos: as chaves `*_v410` de ESTADO DA BASE (vereditos_v410, flags_true_v410, qg_closure_v410_*, selo_registros_v410...) descrevem a v410 SELADA (base_v410); `registros_funcao_v411`,
`vereditos_novos_v411`, `registros_v411`, `titulo_secao_v411`, `md_h0dn_v411` sao os desta versao; `registros_funcao_v410` (iald2, aescala/a_escala, h0dn, hms13), `estrelas_v410`, `estrelas_aescala_v410`, `bundle_v410_sha256` e os
titulos/linhas da v410 sao HERANCA (RECRIADOS no ensaio e iguais ao selado; lidos do ESPERADOS_v410). `estrelas_v411`, `bundle_sha256`, `bandeiras_novas_*` ficam VAZIOS (nenhum modulo, nenhuma bandeira nova).
A TROCA DITA e' a do ensaio (so' numeros e o hash proprio do um.py no estatuto da prova); nenhuma de texto; NENHUMA chave antiga muda. O GATE NAO SE MOVE (o qg_closure do rito tem de ser o da v410 selada).
Nada digitado: cada numero e hash vem do manifesto do candidato (ou do ARTEFATO DE ENSAIO do topo proposto, com V411_ENSAIO_TOPO_PROPOSTO=1: NAO e' candidato), do ensaio a seco, do core/selo da v410 (base_v410), do ESPERADOS_v410,
do FORMAL_MAP, de kernel\\FLAGS_v411.json e kernel\\KH_N1_v411.json. Os registros novos e herdados sao lidos do ensaio (chave do registro no ensaio_a_seco_v411.json) ou, se o ensaio nao os traz no topo, do core que o
proprio ensaio gravou (DL.DRY_DIR\\core_ensaio.json): e' o mesmo calculo, no ponto de chamada real. ORDEM DE USO: depende do ensaio (veredito TUDO PASSOU e o sha16 do artefato): sem ele PARA (fail-closed). `--seco` roda so' a parte
estrutural. uso: python -B -X utf8 gerar_esperados_v411.py [--seco]   (`--ensaio CAMINHO` e `--saida CAMINHO` so' para o ensaio do proprio script)"""
import ast, datetime, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv
_arg = lambda nome_, padrao_: (sys.argv[sys.argv.index(nome_) + 1] if nome_ in sys.argv else padrao_)
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
import registros_v411 as RG  # noqa: E402
sys.modules.setdefault("delta_v410", DL)   # (a ponte por sys.modules, como no ensaio e no conferidor: a copia do quadro_v397.py importa o delta pelo nome antigo; ele usa so' F9_CAMINHOS e lido(), herdados no delta_v411)
import quadro_v397 as QV  # noqa: E402
import guarda_frases_v411 as GF  # noqa: E402
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
J = lambda x: json.dumps(x, sort_keys=True, default=str)
BASE = os.path.join(HERE, DL.BASE_DIR)
D10 = DL.D10
_nrm = lambda p_: os.path.normcase(os.path.normpath(str(p_)))
_VED = _nrm(DL.H0DN_PASTA_VEDADA)
_sob_ved = lambda p_: _nrm(p_) == _VED or _nrm(p_).startswith(_VED + os.sep)


def _feq(a, b):
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_feq(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_feq(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float):
        return a == b or abs(a - b) <= 1e-12 * max(1.0, abs(a), abs(b))
    return a == b


# ===================================================================== PARTE ESTRUTURAL (nao precisa do ensaio; `--seco` para aqui)
CM = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8")); assert CM["sha16"] == h16(DL.CANDIDATO_ARQ), "o manifesto nao e' do arquivo do candidato/artefato"
assert bool(CM.get("ensaio_topo_proposto")) == DL.ENSAIO_TOPO_PROPOSTO, "o manifesto e o modo da rodada divergem (ensaio x real)"
assert h16(os.path.join(BASE, "um.py")) == CM["base_v410_sha16"] == DL.BASE_SHA16_DA_ORDEM, "a base nao e' a v410 selada que a ordem deu"
R0 = json.load(open(os.path.join(BASE, "um_absoluto.json"), encoding="utf-8")); core0 = R0["core"]; selo0 = json.load(open(os.path.join(BASE, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
E410 = json.load(open(os.path.join(DL.V410, "ESPERADOS_v410.json"), encoding="utf-8")); assert E410["candidato_sha16"] == CM["base_v410_sha16"], "o ESPERADOS_v410 nao e' da v410 selada"
kf = core0["kernel_formalization"]; qp0 = core0["quantum_pillar_v384"]; axr0 = kf["axiom_report"]
V = lambda k: str((core0.get(k) or {}).get("verdict") or "")
# ---- o kernel desta versao: NENHUM modulo novo, NENHUMA bandeira nova (o da v410 byte a byte); a cobertura igual
F = json.load(open(DL.FORMAL_MAP_ARQ, encoding="utf-8"))
FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v411.json"), encoding="utf-8")); KH = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, DL.KH_N1_INSUMO), encoding="utf-8"))
assert FJ["n_flags"] == CM["n_bandeiras"] == 0 and not FJ["flags"] and CM["kernel"]["modulos_novos"] == 0 and CM["escada"][0] == CM["escada"][1] == E410["escada"][1], ("a v411 nao tem modulo nem bandeira nova", CM["escada"])
assert all(F.get(r_) == s_ for r_, s_ in kf["formal_files_sha256"].items() if r_ in F) and len(F) == CM["formal_files_n"], "o FORMAL_MAP do candidato diverge do hash formal da v410 selada num arquivo embutido"
VBASE = {k: V(k) for k, m in core0.items() if isinstance(m, dict) and m.get("verdict")}   # o estado SELADO da v410 (a base)
REG_V410 = list(D10.REGISTROS_FUNCAO)   # iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410
SEL_KEYS = tuple(E410["selo_registros_v409"]) + tuple(REG_V410) + ("registros_v410",)   # as chaves do selo das versoes anteriores (as da v410 entram como heranca)
assert all(k in selo0 for k in SEL_KEYS), [k for k in SEL_KEYS if k not in selo0]
# ---- o QUADRO do topo (v397) e o resultado pinado do Teste da Unica Palavra: o que a v410 pinou == o que esta em disco
res9 = json.load(open(os.path.join(DL.F9_DIR_DURAVEL, DL.F9_RESULTADO_NOME), encoding="utf-8"))
numeros9 = {k: DL.lido(res9, c) for k, c in DL.F9_CAMINHOS.items()}
assert E410["veracidade"]["numeros_do_resultado"] == numeros9 and E410["veracidade"]["resultado"]["sha256"] == DL.F9_RESULTADO_SHA256_DA_ORDEM, "o que a v410 pinou do Teste da Unica Palavra != o resultado em disco"
a_pt, mach_pt = QV.esperados(res9, "pt"); a_en, mach_en = QV.esperados(res9, "en")
assert mach_pt == E410["quadro"]["linha_de_maquina_pt"] and mach_en == E410["quadro"]["linha_de_maquina_en"], "a linha de maquina do quadro da v397 mudou: o quadro NAO se mexe"
# ---- o artigo e o .md da v411: os titulos LIDOS do delta (do DESENHO); as marcas e as frases de «nao selou» LIDAS do PROPRIO candidato (as funcoes do runtime v411), nunca digitadas
_cand_txt = open(DL.CANDIDATO_ARQ, "rb").read().decode("utf-8")
_cand_tree = ast.parse(_cand_txt)
_fns = {n_.name: ast.get_source_segment(_cand_txt, n_) for n_ in _cand_tree.body if isinstance(n_, ast.FunctionDef) and n_.name in ("_v411_secao_tex", "_v411_quadro_tex")}
assert set(_fns) == {"_v411_secao_tex", "_v411_quadro_tex"}, "as funcoes do artigo da v411 nao estao no candidato"
_BS = chr(92)


def _marcas_pt_en(src_):
    """os \\textbf{...} sem LaTeX dentro que acabam em ponto (as marcas da secao), por idioma pela ordem em que aparecem: a primeira metade PT, a segunda EN (o corpo da funcao rende PT e depois EN)."""
    return re.findall(re.escape(_BS + "textbf{") + r"([^{}$" + re.escape(_BS) + r"]+[.:])\}", src_)


_ns_tu = {}
exec(compile(ast.get_source_segment(_cand_txt, next(n_ for n_ in _cand_tree.body if isinstance(n_, ast.FunctionDef) and n_.name == "_v411_tex_unicode")), "<candidato:_v411_tex_unicode>", "exec"), _ns_tu)
_tu = _ns_tu["_v411_tex_unicode"]   # (a MESMA funcao do candidato que poe o titulo no LaTeX: o titulo no artigo e no sumario e' esta forma; o TXT a rende com $×$)
TIT411 = {"pt": _tu(DL.TITULO_SECAO_PT), "en": _tu(DL.TITULO_SECAO_EN)}   # (como o titulo_secao_h0dn_v410: a forma LaTeX; o conferidor aplica _tt)
_ms = [m_ for m_ in _marcas_pt_en(_fns["_v411_secao_tex"]) if not m_.startswith(("Nesta rodada", "This round"))]
_i_en = next(i_ for i_, m_ in enumerate(_ms) if m_.startswith("The law and the question"))
MARCAS411 = {"pt": [TIT411["pt"]] + _ms[:_i_en], "en": [TIT411["en"]] + _ms[_i_en:]}
assert min(len(MARCAS411["pt"]), len(MARCAS411["en"])) >= 8 and MARCAS411["pt"][1].startswith("A lei e a pergunta") and MARCAS411["en"][1].startswith("The law and the question"), MARCAS411   # (o numero pode diferir por idioma: uma marca EN traz LaTeX dentro e nao entra)
_nao = re.findall(re.escape(_BS + "textbf{") + r"((?:Nesta rodada|This round)[^{}]*?)(?:\\texttt\{[^{}]*\}[^{}]*?)?(?=[:.])", _fns["_v411_quadro_tex"] + _fns["_v411_secao_tex"])
NAO411 = {"pt": sorted({re.sub(r"\s+", " ", x_).strip() for x_ in _nao if x_.startswith("Nesta rodada") and "texttt" not in x_}), "en": sorted({re.sub(r"\s+", " ", x_).strip() for x_ in _nao if x_.startswith("This round") and "texttt" not in x_})}
NAO411 = {l_: [x_ for x_ in v_ if not any(y_ != x_ and y_.startswith(x_) for y_ in v_) and ("NÃO selou" in x_ or "did NOT seal" in x_)] for l_, v_ in NAO411.items()}   # (so' as frases inteiras: o recorte antes de um \texttt nao entra)
assert NAO411["pt"] and NAO411["en"], ("as frases de «nao selou» da v411 nao foram achadas no candidato", _nao)
MD_H0DN_V411 = re.match(r"^> \*\*(.+?):\*\*$", DL.MD_ROTULO_H0DN_V411).group(1)
assert ("> **" + MD_H0DN_V411 + ":**") in _cand_txt and _cand_txt.index("> **" + MD_H0DN_V411 + ":**") < _cand_txt.index("> **" + E410["md_iald2"] + ":**"), "a linha do .md da v411 tem de vir antes da da IALD2 (v410) no candidato"
# ---- as falas (as de DL.FALAS_V411, 11 desde a ordem da gerencia de 12/11, por sha256; o numero == o do manifesto), as decisoes (DL.DECISOES_V411, D159 a D173) e as erratas (E41, E42, E43): o candidato == o delta == os registros
# (D181, R1 de 12/11 noite) as falas entram CITADAS (data, sha256, papel, autor): sem texto, sem trecho e sem o nome do arquivo; os ESPERADOS tambem nao levam o nome (a chave e' derivada do sha256)
_vd = dict(RG.FALAS_CITADAS)
assert len(_vd) == DL.N_FALAS_V411 == len(DL.FALAS_V411) == CM["falas_citadas"] and [v_["sha256"] for v_ in _vd.values()] == [f_["sha256"] for f_ in DL.FALAS_V411] and all(DL.sha256_arquivo(f_["arquivo"]) == f_["sha256"] for f_ in DL.FALAS_V411)
CUN = {k_: {"sha256": v_["sha256"], "quando": v_["quando"], "papel": v_["papel"], "autor": v_["autor"]} for k_, v_ in _vd.items()}
assert _cand_txt.count("_V411_FALAS_CITADAS = ") == 1 and _cand_txt.count("_V411_VERBATINS2 = {}") == 1 and all(v_["sha256"] in _cand_txt for v_ in CUN.values()), "as falas da v411 nao estao no candidato por sha256 (citadas) ou o _V411_VERBATINS2 nao esta' vazio"
CH = CM["h0dn"]; assert CH["registro"] == DL.FECHO_REGISTRO and CH["n_checks"] == DL.N_CHECKS_FECHO and len(CH["insumos"]) == len(DL.INSUMOS_V411) and all(CH["insumos"][i_["nome"]]["sha256"] == i_["sha256"] for i_ in DL.INSUMOS_V411)
_src_self = open(os.path.abspath(__file__), encoding="utf-8").read()
_usados = {}
for _n in ast.walk(ast.parse(_src_self)):
    if isinstance(_n, ast.Attribute) and isinstance(_n.value, ast.Name) and _n.value.id in ("DL", "RG", "QV", "GF", "D10"):
        _usados.setdefault(_n.value.id, set()).add(_n.attr)
_mods = {"DL": DL, "RG": RG, "QV": QV, "GF": GF, "D10": D10}
_faltam = sorted("%s.%s" % (m_, a_) for m_, ats_ in _usados.items() for a_ in ats_ if not hasattr(_mods[m_], a_))
assert not _faltam, ("atributos usados que nao existem nos modulos da cadeia", _faltam)
if SECO:
    print("SECO: parte estrutural OK | artefato %s (%s) | marcas v411 %d/%d | nao-selou %s | md %s | falas %d" % (CM["sha16"], DL.ROTULO_DO_ARTEFATO, len(MARCAS411["pt"]), len(MARCAS411["en"]), NAO411, MD_H0DN_V411, len(CUN)))
    sys.exit(0)

# ===================================================================== PARTE DO ENSAIO (fail-closed: sem o ensaio o script PARA)
_ens_p = _arg("--ensaio", DL.saida("ensaio_a_seco_v411.json"))
assert os.path.exists(_ens_p), "falta %s: o ensaio a seco tem de rodar ANTES deste script" % _ens_p
ens = json.load(open(_ens_p, encoding="utf-8")); assert ens["veredito"] == "TUDO PASSOU" and ens["sha16"] == CM["sha16"], (ens.get("veredito"), ens.get("sha16"))
_core_dry_p = os.path.join(DL.DRY_DIR, "core_ensaio.json"); assert os.path.exists(_core_dry_p), "falta o core do ensaio (%s)" % _core_dry_p
CE = json.load(open(_core_dry_p, encoding="utf-8"))["core"]
assert h16(os.path.join(DL.DRY_DIR, "um.py")) == CM["sha16"], "o dry do ensaio e' de outra geracao"


def _nck(r_):
    n_ = r_.get("n_checks")
    return n_ if n_ is not None else (r_.get("mechanics") or {}).get("n_checks")


def _reg(nome_):
    """o registro com este nome: do topo do ensaio (se o ensaio o traz) ou do core que o ensaio gravou (o mesmo calculo, no ponto de chamada real); as checagens c1..cN todas ok."""
    r_ = ens.get(nome_) if isinstance(ens.get(nome_), dict) and ens[nome_].get("verdict") else CE.get(nome_)
    assert isinstance(r_, dict) and r_.get("verdict"), "nem o ensaio nem o core do ensaio trazem o registro %r" % nome_
    cks_ = (r_.get("mechanics") or {}).get("checks")
    if cks_ is not None and nome_ not in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO):
        assert [c_["id"] for c_ in cks_] == ["c%d" % (i_ + 1) for i_ in range(len(cks_))] and all(c_["ok"] is True for c_ in cks_) and len(cks_) == _nck(r_), ("checagem nao ok no ensaio", nome_, [c_["id"] for c_ in cks_ if c_.get("ok") is not True])
    return dict(r_, n_checks=_nck(r_))


_viz = ens["vizinhos"]; mud = _viz["mudaram"]; te_ = _viz["troca_esperada_so_o_hash_proprio"]
assert "troca_dita_v411" not in CM, "o candidato declara uma troca dita de texto: este script foi adaptado para NENHUMA"
assert not ((ens.get("troca_dita_v411") or {}).get("declarada_no_candidato") or []), "o ensaio diz que ha troca dita de texto"
troca_dita_textual = {}
for k_ in ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "traducao_turing_v409") + tuple(REG_V410) + (D10.CUNHAGENS_REGISTRO, D10.KH_REGISTRO):
    assert k_ not in mud and k_ not in te_, ("o veredito de %s mudou no ensaio: na v411 NENHUMA chave antiga muda" % k_, mud.get(k_) or te_.get(k_))
troca = sorted(set(mud) | set(te_))   # o que muda: so' numeros e o hash proprio do um.py (estatuto da prova); a v411 nao muda o kernel, logo a escada e a cobertura NAO estao aqui
assert set(te_) <= {"estatuto_da_prova_v391"} and set(troca) <= set(E410["troca_dita"]) | {"estatuto_da_prova_v391"}, ("a troca do ensaio excede o que pode mudar numa versao sem modulo", troca)
mf = ens["mainflow"]
difere_selo = next((v_ for k_, v_ in ens["selo"].items() if k_.startswith("difere_do_selo_v410")), None)
assert difere_selo is not None, "o ensaio nao traz selo.difere_do_selo_v410"
selo_chaves_que_mudam = sorted(k for k in SEL_KEYS if k in difere_selo and k not in troca)
assert set(selo_chaves_que_mudam) <= {"registros_v410"}, ("uma chave do selo de versao anterior mudou", selo_chaves_que_mudam)
vr = ens["veracidade_registro"]
assert all(vr["lido"].get(k) == v for k, v in numeros9.items()), "os numeros lidos pelo registro no ensaio != os do resultado pinado"
sa, dc, sc = ens["selo_acom_registro"], ens["declaracao_registro"], ens["sidecar"]
_MFk = next((k_ for k_ in mf if k_.startswith("registros_novos_v411")), None)
MF4 = mf[_MFk] if _MFk else {n_: {"verdict": CE[n_]["verdict"], "all_verified": CE[n_]["all_verified"]} for n_ in list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]}
assert sorted(MF4) == sorted(list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]) and all(v_["all_verified"] is True for v_ in MF4.values()), MF4
# ---- o registro NOVO com funcao: h0dn_bg1_v411 (o resultado da abertura RECALCULADO no ponto de chamada; as 16 checagens; as chaves congeladas com a custodia)
PH = _reg(DL.FECHO_REGISTRO); HV = PH["values"]
assert PH["all_verified"] is True and PH["n_checks"] == DL.N_CHECKS_FECHO == CH["n_checks"] and PH["verdict"] == MF4[DL.FECHO_REGISTRO]["verdict"] and PH["verdict"].startswith(DL.VEREDITO_OK_PREFIXO) and PH["verdict"].endswith(DL.VEREDITO_SUFIXO), (PH.get("verdict"), PH.get("n_checks"))
assert DL.PREFIXO_DA_FAIXA in PH["verdict"] and "BESIDE_FREE_CEPHEIDS_" in PH["verdict"] and "PRIMARY_UNDER_THE_PUBLISHED_MODEL_" in PH["verdict"] and not GF.violacoes(PH["verdict"]) and not any(t_ in PH["verdict"] for t_ in DL.TOKENS_PROIBIDOS_V411), PH["verdict"]
for _k in ("verdict", "all_verified", "opened_once", "cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres", "ressalvas_secao8", "o_que_o_teste_nao_decide"):
    assert _k in PH, ("chave congelada com a custodia ausente no registro", _k)
for _lin, _ks in (("primario", ("z_null", "z_tgl", "D", "p_unilateral", "ramo", "outcome", "cabeca_do_teste", "t", "modelo")), ("cefeidas_livres", ("z_null", "z_tgl", "D", "ramo", "outcome", "t", "modelo"))):
    assert all(k_ in HV[_lin] for k_ in _ks), ("chave congelada ausente em values.%s" % _lin, [k_ for k_ in _ks if k_ not in HV[_lin]])
assert isinstance(PH.get("p2_ao_lado_da_v387"), dict) and PH["p2_ao_lado_da_v387"].get("rotulo") == DL.P2_ROTULO and DL.P2_TOKEN_SELADO in str(PH["p2_ao_lado_da_v387"].get("rotulo_selado_da_v387")), "o P2 ao lado da v387 no registro do ensaio"
assert "atos" in HV and PH.get("opened_once") is True and HV["primario"]["ramo"] == CH.get("ramo_primario", HV["primario"]["ramo"]) and abs(HV["beta"] - core0["beta"]) <= 1e-9 * abs(core0["beta"]), "o registro h0dn_bg1_v411 do ensaio"
assert HV["sob_pasta_vedada"] == [] and not [p_ for p_ in HV.get("caminhos_tocados") or [] if _sob_ved(p_) or any(n_.lower() in os.path.basename(str(p_)).lower() for n_ in DL.H0DN_NOMES_VEDADOS)], "VETO: um caminho tocado pelo registro cai sob a pasta vedada"
assert HV["gate_verdict"] == (core0.get("qg_closure") or {}).get("gate", {}).get("verdict") == selo0.get("qg_closure_verdict") and HV["escada"] == CM["escada"][1], "o gate e a escada do h0dn_bg1_v411 != os da v410 selada"
_FORA = ["caminhos_tocados", "n_caminhos_tocados"]   # dependem da pasta em que o rito roda (o ensaio roda em outra pasta que o rito)
# ---- os specs da v411
PCU = _reg(DL.CUNHAGENS_REGISTRO); PKH = _reg(DL.KH_REGISTRO)
assert PCU["all_verified"] is True and PCU["verdict"].startswith(DL.CUNHAGENS_PREFIXO + "__") and ("ERRATA_%s_BESIDE" % DL.ERRATAS_TOKEN_V411) in PCU["verdict"] and PKH["all_verified"] is True and PKH["verdict"].startswith(DL.KH_PREFIXO + "__"), (PCU.get("verdict"), PKH.get("verdict"))
# ---- os HERDADOS da v410 (recriados; o veredito e' o selado)
RH10 = {}
for _ap, _nm in (("iald2", D10.FECHO_REGISTRO), ("aescala", D10.AESCALA_REGISTRO), ("h0dn", D10.H0DN_REGISTRO), ("hms13", D10.HMS13_REGISTRO)):
    _r = _reg(_nm)
    assert _r["all_verified"] is True and _r["verdict"] == V(_nm) == E410["registros_funcao_v410"][_ap]["verdict"] and _r["n_checks"] == E410["registros_funcao_v410"][_ap]["n_checks"], ("o registro herdado da v410 mudou", _nm)
    _v = {k_: v_ for k_, v_ in (_r.get("values") or {}).items() if k_ not in _FORA}
    RH10[_ap] = {"nome": _nm, "verdict": _r["verdict"], "n_checks": _r["n_checks"], "values": _v, "recriado_na_v411": True}
    if _ap in ("h0dn", "hms13"):
        RH10[_ap]["fora_do_values_porque_dependem_da_pasta_do_rito"] = list(_FORA)
RH10["a_escala"] = RH10["aescala"]   # (a leitura do pos-rito le a chave curta a_escala; o conferir_rito le aescala)
for _n in (D10.CUNHAGENS_REGISTRO, D10.KH_REGISTRO):
    _r = _reg(_n); assert _r["all_verified"] is True and _r["verdict"] == V(_n), ("o spec da v410 mudou de veredito", _n)
# os herdados de antes da v410 (recriados no ensaio; veredito == o selado)
for _nm in (DL.D9.FECHO_REGISTRO, DL.D8.FECHO_REGISTRO, DL.D7.FECHO_REGISTRO, DL.D6.FECHO_REGISTRO):
    _r = _reg(_nm); assert _r["all_verified"] is True and _r["verdict"] == V(_nm), ("um registro herdado mudou de veredito", _nm)
PC7 = _reg(DL.D7.FECHO_REGISTRO); chaves_v407_esperadas = dict(PC7["values"]["chaves"])
assert chaves_v407_esperadas == E410["chaves_v407_esperadas"], "as chaves que o psion_canto_v407 le mudaram (nenhuma chave antiga muda)"
_recr = next((v_ for k_, v_ in mf.items() if k_.startswith("recriados_v393_a_v")), None)
assert isinstance(_recr, dict) and _recr and all(d_["all_verified"] is True for d_ in _recr.values()), "o ensaio nao traz mainflow.recriados_v393_a_v4xx selados"
qg0 = core0.get("qg_closure") or {}
assert (qg0.get("gate") or {}).get("verdict") == selo0.get("qg_closure_verdict"), "o gate da base"
_qgE = (CE.get("qg_closure") or {})
assert J(_qgE) == J(qg0), "o qg_closure do core do ensaio difere do da v410 selada: o gate se moveu"
nm0 = core0["neutrino_mass"]; rb0 = core0["ramo_b_preregistration_v386"]
pvk = ens["pasta_vedada_kimi"]
assert _nrm(pvk["pasta"]) == _VED and pvk["tocados_sob_vedada"] == [] and pvk["controle_negativo_detecta"] is True and isinstance(pvk["n_caminhos_vistos"], int) and pvk["n_caminhos_vistos"] > 0, ("o ensaio nao mediu o veto (ou tocou a pasta vedada)", pvk)
# ---- o artigo do ensaio: as marcas, os titulos e o sumario da v411 estao no TXT e no .toc que o ensaio rendeu (o que o conferidor vai cobrar do rito)
_rd = lambda p_: open(p_, encoding="utf-8", errors="replace").read()
_txt = {l_: re.sub(r"\s+", " ", _rd(os.path.join(DL.DRY_DIR, "dry_v411_%s.txt" % l_))) for l_ in ("pt", "en")}
_toc = {l_: re.sub(r"(\\[A-Za-z]+) (?=[$}0-9])", r"\1", _rd(os.path.join(DL.DRY_DIR, "dry_v411_%s.toc" % l_)).replace("\n", "")) for l_ in ("pt", "en")}
_tt = lambda m_: re.sub(r"\\[td]?frac\s*(\d)\s*(\d)", r"\1/\2", m_.replace(_BS + "beta", "β").replace(_BS + "times", "×"))
_falta_txt = {l_: [m_ for m_ in MARCAS411[l_] if re.sub(r"\s+", " ", _tt(m_)) not in _txt[l_]] for l_ in ("pt", "en")}
assert not any(_falta_txt.values()), ("marca da v411 ausente do TXT do artigo do ensaio", _falta_txt)
TOC = {"pt": [TIT411["pt"]] + [w for w in E410["toc"]["pt"] if not w.startswith("v384 a ")] + ["v384 a " + DL.UM_VERSION], "en": [TIT411["en"]] + [w for w in E410["toc"]["en"] if not w.startswith("v384 to ")] + ["v384 to " + DL.UM_VERSION]}
_falta_toc = {l_: [w for w in TOC[l_] if w not in _toc[l_]] for l_ in ("pt", "en")}
assert not any(_falta_toc.values()), ("o sumario do artigo do ensaio nao lista o que o conferidor vai cobrar (o titulo da v411 na forma LaTeX, as secoes anteriores, v384 a v411)", _falta_toc)

esp = {"candidato_sha16": CM["sha16"], "candidato_bytes": CM["bytes"], "origem_sha16": CM["base_v410_sha16"], "escada": [CM["escada"][1], CM["escada"][1]], "escada_v410_e_v411": [E410["escada"][1], CM["escada"][1]], "n_bandeiras_novas": 0,
       "bandeiras_novas_chaves": [], "bandeiras_novas_nomes": [], "bandeiras_novas_modulos": {},
       "cunhagens": CUN, "cunhagens_v410": E410["cunhagens"], "kernel": {"modulos_novos": 0, "modelo": CM["kernel"]["modelo"], "raiz_sha16": F["TGLExt.lean"][:16], "audit_sha16": F["TGL/Audit.lean"][:16], "pos_build": CM["kernel"].get("pos_build"), "sandbox": CM["kernel"].get("sandbox")},
       "bundle_sha256": {}, "bundle_v410_sha256": E410["bundle_sha256"], "bundle_v409_sha256": E410["bundle_v409_sha256"], "bundle_v408_sha256": E410["bundle_v408_sha256"], "bundle_v407_sha256": E410["bundle_v407_sha256"], "bundle_v406_sha256": E410["bundle_v406_sha256"],
       "formal_files_n": CM["formal_files_n"], "pedras_v405_sha256": E410["pedras_v405_sha256"],
       "qg_closure_verdict": selo0.get("qg_closure_verdict"),
       "qg_closure_v410_json_sha256": hashlib.sha256(J(qg0).encode("utf-8")).hexdigest(),
       "qg_closure_v410_sem_checks_json_sha256": hashlib.sha256(J({k: v for k, v in qg0.items() if k != "checks"}).encode("utf-8")).hexdigest(),
       "qg_closure_v410_checks": json.loads(J(qg0.get("checks"))), "qg_closure_gate_verdict_v410": (qg0.get("gate") or {}).get("verdict"),
       "beta": core0.get("beta"), "alpha": core0.get("alpha"), "omega_I": core0.get("omega_I"),
       "vereditos_v410": VBASE, "troca_dita": troca, "troca_dita_textual": troca_dita_textual, "veredito_da_troca_no_ensaio": {k: (mud.get(k) or te_.get(k) or {}).get("depois") for k in troca},
       "regra_da_mudanca_dita": "so' os vereditos de `troca_dita` podem mudar: na v411 (nenhum modulo novo) so' o estatuto da prova (o hash proprio do um.py) e o que o ensaio mediu como so' numeros; NENHUM de texto (`troca_dita_textual` vazio); nenhuma chave antiga muda; os registros da v410 e anteriores nao mudam de veredito; qualquer outra mudanca reprova",
       "pilar": {"key": qp0["key"], "result_sha256": qp0["result_sha256"], "verdict": V("quantum_pillar_v384")},
       "selo_registros_v410": {k: selo0.get(k) for k in SEL_KEYS}, "selo_chaves_que_mudam": selo_chaves_que_mudam, "selo_difere_do_v410_no_ensaio": difere_selo,
       "not_sealed_formais": sorted((selo0.get("not_sealed_this_run") or {}).get("formais") or []), "not_sealed_recusas": sorted((selo0.get("not_sealed_this_run") or {}).get("recusas_de_dado") or []),
       "flags_true_v410": sorted(k for k, v in kf.items() if v is True), "axiom_report_v410_n": len(axr0),
       "runtime_seals_v410": core0["runtime_of_the_one"]["seals"], "what_remains_v410": core0["tgl_closure"]["what_remains_named"],
       "neutrino_frozen_hash_v410": nm0["frozen_hash"], "neutrino_angle_status_antigo_sha256": hashlib.sha256(nm0["angle_status"].encode("utf-8")).hexdigest(),
       "f2b_antes": E410["f2b_antes"], "f2b_depois": E410["f2b_depois"], "m_nu_meV_v404": nm0["m_nu_meV"],
       "titulo_secao_v411": TIT411, "titulo_secao_v411_unicode": {"pt": DL.TITULO_SECAO_PT, "en": DL.TITULO_SECAO_EN}, "titulo_quadro_v411": _tu(DL.TITULO_QUADRO_TOPO_PT), "titulo_quadro_v411_unicode": DL.TITULO_QUADRO_TOPO_PT, "titulo_secao_v410": E410["titulo_secao_v410"], "titulo_secao_aescala_v410": E410["titulo_secao_aescala_v410"], "titulo_secao_h0dn_v410": E410["titulo_secao_h0dn_v410"],
       "titulo_secao_v409": E410["titulo_secao_v409"], "titulo_secao_v408": E410["titulo_secao_v408"], "titulo_secao_v407": E410["titulo_secao_v407"],
       "vereditos_novos_v411": {k: v["verdict"] for k, v in MF4.items()},
       "registros_v411": {k: v["verdict"] for k, v in MF4.items() if k in (DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO)},
       "registros_v410": {k: V(k) for k in (D10.CUNHAGENS_REGISTRO, D10.KH_REGISTRO)},
       **{"registros_v4%02d" % n_: E410["registros_v4%02d" % n_] for n_ in (9, 8, 7, 6, 5, 4, 3, 2, 1)}, "registros_v399": E410["registros_v399"],
       "ga_values": (ens.get("ga_registro") or {}).get("values", E410["ga_values"]), "gap_values": (ens.get("gap_registro") or {}).get("values", E410["gap_values"]), "ga_window_status": R0["ga_window_status"],
       "veredito_da_falsidade_v410": V("falsidade_da_inercia_v401"),
       "registros_funcao_v411": {"h0dn": {"nome": DL.FECHO_REGISTRO, "verdict": PH["verdict"], "n_checks": PH["n_checks"], "values": {k_: v_ for k_, v_ in HV.items() if k_ not in _FORA}, "fora_do_values_porque_dependem_da_pasta_do_rito": list(_FORA),
                                          "topo": {k_: PH.get(k_) for k_ in ("verdict", "all_verified", "opened_once", "cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres", "ressalvas_secao8", "o_que_o_teste_nao_decide")},
                                          "p2_ao_lado_da_v387": PH.get("p2_ao_lado_da_v387"), "p2_rotulo_de": DL.P2_ROTULO_DE, "p2_rotulo_e_proposta": DL.P2_ROTULO_E_PROPOSTA}},   # (aditivo da gerencia de 12/11: o P2 ao lado da v387; o rotulo lido do TOPO_RATIFICADO, chave rotulo_p2)
       "registros_funcao_v410": RH10, "registros_funcao_v409": E410["registros_funcao_v409"], "registros_funcao_v408": E410["registros_funcao_v408"], "registros_funcao_v407": E410["registros_funcao_v407"], "registros_funcao_v406": E410["registros_funcao_v406"],
       "registros_funcao_v405": E410["registros_funcao_v405"], "registros_funcao_v404": E410["registros_funcao_v404"], "registros_funcao_v403": E410["registros_funcao_v403"],
       "estrelas_v411": {}, "estrelas_v410": E410["estrelas_v410"], "estrelas_aescala_v410": E410["estrelas_aescala_v410"],
       **{"estrelas_v4%02d" % n_: E410["estrelas_v4%02d" % n_] for n_ in (9, 8, 7, 6, 5, 4, 3)},
       "bandeiras_das_pedras_v405": E410["bandeiras_das_pedras_v405"], "teoremas_das_pedras_v405": E410["teoremas_das_pedras_v405"], "contrato_das_pedras_v405": E410["contrato_das_pedras_v405"], "suporte_das_pedras_v405": E410["suporte_das_pedras_v405"],
       "cobertura_kh_n1": ens["verify_kernel_ponta_a_ponta"]["cobertura"], "axiom_report_esperado_min": ens["verify_kernel_ponta_a_ponta"]["axiom_report_n"],
       "selo_acom": {"verdict": sa["verdict"], "all_verified": sa["all_verified"], "perfil": sa["perfil"], "bloco_embutido_sha256": sa["bloco_embutido_sha256"], "sha256_do_um_py": sa["sha256_do_um_py"], "bytes": sa["bytes"], "psi": sa["psi"], "theta": sa["theta"], "kappa": sa["kappa"],
                     "lut_sha256": sa["lut_sha256"], "m_max_abs": sa["m_max_abs"], "f_exp": sa["f_exp"], "entropia_dos_estados_bits": sa["entropia_dos_estados_bits"], "erro_real_maximo_antes_do_rint": sa["erro_real_maximo_antes_do_rint"],
                     "controles": [len(sa["controles"]), all(o_.startswith("RECUSOU:") for _, o_ in sa["controles"])], "controles_obtidos": {i_: o_ for i_, o_ in sa["controles"]}, "n_checks": len(sa["checks"]), "checks": sa["checks"], "auditoria_de_separacao": sa["auditoria_de_separacao"], "tempo_total_s_no_ensaio": sa["tempo_total_s"]},
       "declaracao": {"verdict": dc["verdict"], "all_verified": dc["all_verified"], "verbatim_sha256": dc["verbatim_sha256"], "sha16": dc["verbatim_sha256"][:16], "n_checks": len(dc["checks"]), "checks": dc["checks"], "ancoras": dc["ancoras"], "pedra": dc["pedra"], "linhas_da_trava": dc["linhas_da_trava"],
                      "direcao_do_testemunho": E410["declaracao"]["direcao_do_testemunho"]},
       "sidecar": {"arquivo": DL.SIDECAR_NOME, "esquema": E410["sidecar"]["esquema"], "objetos": [o["nome"] for o in sc["objetos"]], "veredito_esperado_prefixo": E410["sidecar"]["veredito_esperado_prefixo"], "um_py": next(o for o in sc["objetos"] if o["nome"] == "um.py"),
                   "tempo_s_no_ensaio": sc["tempo_s"], "entra_na_custodia": E410["sidecar"]["entra_na_custodia"]},
       "acom_estudo": E410["acom_estudo"],
       "decisoes_da_gerencia": dict(DL.DECISOES, **DL.DECISOES_V411), "decisoes_v411_ids": list(DL.DECISOES_V411), "decisoes_v410_ids": E410["decisoes_v410_ids"],
       "erratas_E24_E27": ["%s -- %s" % (e_["id"], e_["texto"]) for e_ in DL.ERRATAS_V411], "erratas_v411": ["%s -- %s" % (e_["id"], e_["texto"]) for e_ in DL.ERRATAS_V411], "erratas_v410": E410["erratas_v410"],
       "ressalvas": list(DL.RESSALVAS_ROTULOS_PT), "ressalvas_v410": E410["ressalvas"], "leitura_v411": {}, "leitura_v410": E410["leitura_v410"],
       "chaves_v411": [], "chaves_v410": E410["chaves_v410"], "chaves_v409": E410["chaves_v409"], "chaves_v408": E410["chaves_v408"], "chaves_v407": E410["chaves_v407"], "chaves_v407_esperadas": chaves_v407_esperadas,
       "fica_false_por_teorema": list(DL.FICAM_FALSE_POR_TEOREMA), "fica_aberto": E410["fica_aberto"], "regra_do_4_44": DL.REGRA_DO_4_44, "guarda_frases": GF.controle_negativo()["ok"],
       "veracidade": E410["veracidade"], "quadro": E410["quadro"],
       "artigo_marcas": {l_: list(MARCAS411[l_]) + list(E410["artigo_marcas"][l_]) for l_ in ("pt", "en")}, "artigo_nao": {l_: list(E410["artigo_nao"][l_]) + list(NAO411[l_]) for l_ in ("pt", "en")}, "toc": TOC,
       "the_iald_index_v410": {"all_verified": (core0.get("the_iald_index") or {}).get("all_verified"), "verdict": V("the_iald_index")}, "the_iald_index_v411": {"verdict": ens["indice_da_iald"]["verdict"]},
       "md_carimbo": "**Versão %s**" % DL.UM_VERSION, "md_h0dn_v411": MD_H0DN_V411, "md_quadro_v411": DL.TITULO_QUADRO_TOPO_PT,
       **{k_: E410[k_] for k_ in ("md_iald2", "md_aescala", "md_h0dn", "md_hms13", "md_traducao", "md_massa", "md_jo8", "md_caminho", "md_ponte", "md_falsidade", "md_errata", "md_testemunho", "md_sonico", "md_token", "md_testemunha", "md_psibit", "md_fechamento", "md_psion", "md_tetelestai")},
       "ensaio_sha16": h16(_ens_p),
       "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
       "n_bandeiras_por_grupo": {}, "politica_de_bandeiras": {"n_flags": 0, "escada_antes": CM["escada"][0], "escada_depois": CM["escada"][1], "fonte": "FLAGS_v411.json (pos_build_kernel_v411.py): nenhuma bandeira nova, nenhum modulo novo"},
       "candidato_anterior_sha16": CM["base_v410_sha16"],
       "gate_nao_se_move": {"funcoes_identicas_a_base": CM["gate_nao_se_move"]["funcoes_identicas_a_base"], "gate_recomputado_no_ensaio": ens.get("gate_recomputado")},
       "h0dn_v411": dict(CH, pasta_vedada=DL.H0DN_PASTA_VEDADA, contrato_de_registro_fora_da_escada=list(DL.CONTRATOS_DE_REGISTRO_FORA_DA_ESCADA), n_caminhos_vistos_no_ensaio=pvk["n_caminhos_vistos"], veto={"tocados_sob_vedada": [], "controle_negativo_detecta": True}),
       "h0dn": E410["h0dn"], "aescala": E410["aescala"], "hms13": E410["hms13"],
       "tabela_secao7_v411": list(DL.TABELA_SECAO7),
       **DL.MARCA_ENSAIO}
assert esp["the_iald_index_v410"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v410"], esp["not_sealed_formais"])
assert esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] == E410["h8_entradas"], "a arvore do Nos depois do rito tem de ser a da v410 (nenhum modulo novo)"
assert all(kf["formal_files_sha256"].get(r_) == s_ for r_, s_ in esp["bundle_v410_sha256"].items()) and len(esp["bundle_v410_sha256"]) == E410["kernel"]["modulos_novos"], "os modulos da v410 nao estao todos no hash formal do core selado"
_cb = esp["cobertura_kh_n1"]
assert _cb["decl"] == esp["axiom_report_esperado_min"] == KH["linha_TOTAL"]["decl"] == E410["cobertura_kh_n1"]["decl"] and _cb["thm"] == KH["linha_TOTAL"]["thm"] == E410["cobertura_kh_n1"]["thm"] and _cb.get("fora_do_trio") == 0 == KH["linha_TOTAL"]["fora_do_trio"] and esp["axiom_report_esperado_min"] == esp["axiom_report_v410_n"], _cb
_vn = esp["vereditos_novos_v411"]
assert all("__GATE_UNMOVED" in v_ for v_ in _vn.values()) and not any(GF.violacoes(v_) for v_ in _vn.values()), "um veredito novo afirma demais ou nao diz o gate"
assert esp["qg_closure_gate_verdict_v410"] == E410["qg_closure_gate_verdict_v409"] == esp["qg_closure_verdict"], "o gate da v410 selada nao e' o da v409 (o gate nunca se moveu): conferir a base"
assert esp["selo_acom"]["perfil"] == E410["selo_acom"]["perfil"] and esp["selo_acom"]["controles"] == E410["selo_acom"]["controles"] and esp["selo_acom"]["all_verified"] is True and esp["declaracao"]["all_verified"] is True and esp["declaracao"]["verbatim_sha256"] == E410["declaracao"]["verbatim_sha256"]
assert esp["selo_acom"]["sha256_do_um_py"] != E410["selo_acom"]["sha256_do_um_py"], "o selo ACOM do ensaio tem de ser do um.py NOVO"
# o selo da v411 difere do da v410 SELADA em: o selo ACOM (hashes do novo um.py), a versao, o sha256, as chaves novas (h0dn_bg1_v411, registros_v411) e o que a troca dita carrega; o ensaio EXPLICA chave por chave
assert {"selo_pela_propria_tecnologia_v399", "um_version", "registros_v411", DL.FECHO_REGISTRO} <= set(difere_selo) and ens["selo"].get("difere_e_nao_e_so_o_esperado") == [], (difere_selo, ens["selo"].get("difere_e_nao_e_so_o_esperado"))
assert not (set(SEL_KEYS) - {"registros_v410"} - set(troca)) & set(difere_selo), ("o selo de uma versao anterior mudou: os registros anteriores NAO se mexem (fora da troca dita: o hash proprio do um.py)", sorted((set(SEL_KEYS) - {"registros_v410"} - set(troca)) & set(difere_selo)))
assert esp["veracidade"]["z_disc_abaixo_de_5"] and esp["veracidade"]["poder_previo_acima_de_5"]
assert ens["quadro"]["ok"] is True
out = _arg("--saida", DL.saida("ESPERADOS_v411.json"))
if os.path.exists(out):   # backup de BYTES antes de tocar (regra do backup imediato)
    _bk = out + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); open(_bk, "wb").write(open(out, "rb").read()); assert open(_bk, "rb").read() == open(out, "rb").read()
open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(esp, ensure_ascii=False, indent=1, default=str)); os.replace(out + ".tmp", out)
print("ESPERADOS_v411 (%s): %s | vereditos v410 pinados: %d | flags True v410: %d | troca dita (so' numeros e o hash proprio): %s | selo_chaves_que_mudam: %s | h0dn_bg1_v411: %s, primario ramo %s, Cefeidas livres ramo %s | veto medido (%d caminhos)"
      % (DL.ROTULO_DO_ARTEFATO, esp["candidato_sha16"], len(esp["vereditos_v410"]), len(esp["flags_true_v410"]), troca, selo_chaves_que_mudam, PH["n_checks"], HV["primario"]["ramo"], HV["cefeidas_livres"]["ramo"], pvk["n_caminhos_vistos"]))
