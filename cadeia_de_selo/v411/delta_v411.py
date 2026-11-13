# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] o DELTA da v411, no molde do delta_v410 (import por caminho do predecessor, com a constante da Bancada FIXADA; depois o que a v411 SOBRESCREVE)
"""delta_v411.py -- A UNICA definicao do DELTA da v411 (claude-construtor-v411, a servico da gerencia c1, 12/11/2026): O TESTE H0DN x BG1 ABERTO UMA VEZ, A EMENDA E O RESULTADO RECALCULADO NO RITO.
NENHUM modulo novo de kernel: o kernel da v411 e' o da v410 byte a byte (DESENHO_v411 secao 1; escada lida do core da base). UM registro com FUNCAO (h0dn_bg1_v411, 16 checagens) e dois por spec
(cunhagens_v411, kh_n1_cobertura_v411). Reaproveita o delta_v410 (import por caminho, com BANCADA_PINA_HOJE da v410 FIXADA, lida do recibo do religamento da v410: ela e' calculada na importacao e
quebraria apos o APLICAR da v411) e, por ele, os deltas anteriores. TUDO o que a v411 especifica e' LIDO do DESENHO_v411.md da gerencia (tabelas e trechos entre crases), nunca digitado aqui; os hashes
sao conferidos contra os arquivos (o arquivo manda). Validade no kernel nao e' creditacao; o gate nao se move. Onde este modulo e o DESENHO divergirem, vale o DESENHO."""
import glob
import hashlib
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
V410 = os.path.join(os.path.dirname(HERE), "v410")           # a cadeia anterior (molde e base, so' leitura)


def _acha_chave(d_, k_):
    if isinstance(d_, dict):
        if k_ in d_ and isinstance(d_[k_], str):
            return d_[k_]
        for v_ in d_.values():
            r_ = _acha_chave(v_, k_)
            if r_:
                return r_
    elif isinstance(d_, list):
        for v_ in d_:
            r_ = _acha_chave(v_, k_)
            if r_:
                return r_
    return None


# o deployment da v410 (o que a Bancada de producao pina desde o B(n) da v410), LIDO do recibo do religamento da v410 (nunca digitado)
_DEP_V410 = _acha_chave(json.load(open(os.path.join(V410, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v410.json"), encoding="utf-8")), "deployment_id")
_m_dep = re.match(r"B(\d+)-v410-\d{8}-R1$", str(_DEP_V410))
assert _m_dep, ("o recibo do religamento da v410 nao traz o deployment da v410", _DEP_V410)
_src410 = open(os.path.join(V410, "delta_v410.py"), "rb").read().decode("utf-8")
_rx_alvo = re.compile(r"^BANCADA_PINA_HOJE = _bancada_pina_hoje\(\)", re.M)
assert len(_rx_alvo.findall(_src410)) == 1, "a linha BANCADA_PINA_HOJE do delta_v410 nao esta' como esperado"
_src410 = _rx_alvo.sub('BANCADA_PINA_HOJE = {"version": "v410", "deployment_id": %r, "n": %d}   # (fixada pelo delta_v411, lida do recibo do religamento da v410)' % (_DEP_V410, int(_m_dep.group(1))), _src410, count=1)
_mod410 = importlib.util.module_from_spec(importlib.util.spec_from_loader("delta_v410_carregado_pelo_v411", loader=None))
_mod410.__file__ = os.path.join(V410, "delta_v410.py")
exec(compile(_src410, _mod410.__file__, "exec"), _mod410.__dict__)
_MOD10 = _mod410
globals().update({k: v for k, v in vars(_MOD10).items() if not k.startswith("__")})   # tudo da v410 (e, por ela, da v409 ... v399) e depois o que a v411 SOBRESCREVE
D10 = _MOD10                                                   # delta_v410, o predecessor imediato
D9 = D10.D9                                                    # delta_v409
D8 = D10.D8
# nomes da v410 que eram o "atual" la' e que aqui NAO valem como atual (a v411 nao tem bundle nem pedra nova; quem precisar da v410 le DL.D10.<nome>): retirados para que um uso errado falhe a vista
for _n_ in ("BUNDLE_LISTA_ARQ", "BUNDLE_ARQ", "BUNDLE_RELS", "BUNDLE_MODS", "N_BUNDLE", "BUNDLE_POR_REL", "BUNDLE_DA_BANCADA", "BUNDLE_DA_GERENCIA", "ROOT_SUFFIX", "AUDIT_PREFIX",
            "FLAG_PREFIX", "FLAG_PREFIX_AESCALA", "FLAG_PREFIX_POR_MODULO", "GRUPO_BUNDLE", "PEDRAS_V410", "TESTEMUNHA", "N_CHECKS_FECHO", "FECHO_REGISTRO", "CUNHAGENS_REGISTRO", "KH_REGISTRO",
            "REGISTRO_ANTERIOR", "CUNHAGENS_ANTERIOR", "KH_ANTERIOR", "TAG_FECHO", "VEREDITO_OK_PREFIXO", "VEREDITO_SUFIXO", "VEREDITO_RECUSA", "REGISTROS_FUNCAO", "CANDIDATO", "DESENHO_SHA16",
            "PLANO_ARQ", "N_FALAS_V410", "bundle_fontes", "testemunha_fonte"):
    globals().pop(_n_, None)

HERE = os.path.dirname(os.path.abspath(__file__))              # (o update acima trouxe o HERE da v410: aqui e' a pasta da v411)
V410 = os.path.join(os.path.dirname(HERE), "v410")
V409 = D10.V409
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))                    # ...\Central de Patentes\work
CENTRAL = os.path.dirname(WK)
SANDBOX_PAI = os.path.join(C, "t", "k411c")                    # sandbox NOVO (copia de C:\t\k410c\final; fontes conferidas por sha256 contra o Nos v410: CONFERENCIA_FONTES_K411C_v411.json)
SANDBOX = os.path.join(SANDBOX_PAI, "final")                   # NENHUM modulo acrescentado (a v411 nao tem bundle)
ARVORE = os.path.join(SANDBOX_PAI, "arvore")
SANDBOX_ORIGEM = os.path.join(C, "t", "k410c", "final")
PACKAGES_ORIGEM = os.path.join(C, "t", "k404c", "final", ".lake", "packages")
KERNEL_DIR = "kernel"
CANDIDATO = "um_v411_candidato.py"
BASE_DIR = "base_v410"
UM_VERSION = "v411"
BASE_VERSION = "v410"
DESENHO_ARQ = os.path.join(HERE, "DESENHO_v411.md")
assert os.path.exists(DESENHO_ARQ)
_DESENHO_RAW = open(DESENHO_ARQ, "rb").read()
DESENHO_SHA16 = hashlib.sha256(_DESENHO_RAW).hexdigest()[:16]
_DESENHO_TXT = _DESENHO_RAW.decode("utf-8").replace("\r\n", "\n")   # (o DESENHO e' CRLF: as regexes leem a forma LF; o sha e' o dos bytes)
_m_base = re.search(r"Base: a v410 selada `([0-9a-f]{16})`", _DESENHO_TXT)
assert _m_base, "o DESENHO_v411 nao traz a base"
BASE_SHA16_DA_ORDEM = _m_base.group(1)                         # a v410 selada (LIDO do DESENHO_v411; conferido contra o selo e contra o arquivo: o arquivo manda)
SANDBOX_CURTO = os.path.join(C, "t", "vb22")
KH_N1_INSUMO = "KH_N1_v411.json"
TOPO_RATIFICADO_ARQ = os.path.join(HERE, "TOPO_RATIFICADO_v411.json")   # gravado pela GERENCIA (DESENHO 5.1 b); sem ele o candidato nao e' gerado


def _bancada_pina_hoje():
    """o que a Bancada de producao pina HOJE, LIDO do arquivo dela: ANTES do B(n) APLICAR e' a v410 (o passo da v411 e' simples, B20); DEPOIS do APLICAR e' a v411. Os dois estados sao legitimos."""
    d_ = json.load(open(_BANCADA_CONTRATOS, encoding="utf-8"))
    dep_ = str(d_.get("deployment_id", ""))
    m_ = re.match(r"B(\d+)-(v\d+)-", dep_)
    assert m_ and m_.group(2) in (BASE_VERSION, UM_VERSION), ("a Bancada de producao nao pina nem a base (v410) nem esta versao (v411): o B(n) nao seria um passo simples", dep_)
    return {"version": m_.group(2), "deployment_id": dep_, "n": int(m_.group(1))}


BANCADA_PINA_HOJE = _bancada_pina_hoje()
BANCADA_JA_APLICADA = (BANCADA_PINA_HOJE["version"] == UM_VERSION)
B_N_SEGUINTE = "B%d" % ((BANCADA_PINA_HOJE["n"] + 1) if not BANCADA_JA_APLICADA else BANCADA_PINA_HOJE["n"])   # o rotulo do B(n) da v411 (B20), antes e depois do APLICAR

# ======================================================================================= O QUE O DESENHO_v411 ESPECIFICA (LIDO, nunca digitado)


def _secao(n_):
    m_ = re.search(r"^## %d\. [^\n]*\n(.*?)(?=^## \d+\. |\Z)" % n_, _DESENHO_TXT, re.M | re.S)
    assert m_, ("secao ausente no DESENHO_v411", n_)
    return m_.group(1)


_S1, _S2, _S3, _S4, _S5, _S6, _S7, _S8 = (_secao(i_) for i_ in range(1, 9))
_m = re.search(r"^`FECHO_REGISTRO = \"([a-z0-9_]+)\"`", _S2, re.M); assert _m
FECHO_REGISTRO = _m.group(1); assert FECHO_REGISTRO == "h0dn_bg1_v411"
H0DN_REGISTRO_V411 = FECHO_REGISTRO
_m = re.search(r"\*\*`N_CHECKS_FECHO = (\d+)`\*\*", _S2); assert _m
N_CHECKS_FECHO = int(_m.group(1)); assert N_CHECKS_FECHO == 16
_m = re.search(r"mec[aâ]nica `([a-z0-9_]+)\(beta_, core_, c_\)`", _S2); assert _m
MECANICA_NOME = _m.group(1)
_m = re.search(r"Ok come[cç]a com `([A-Z0-9_]+__)` e termina em `(__GATE_UNMOVED)`", _S2); assert _m
VEREDITO_OK_PREFIXO, VEREDITO_SUFIXO = _m.group(1), _m.group(2)
_m = re.search(r"no meio, MONTADO do rec[aá]lculo \(nunca digitado\): `([^`]+)`", _S2); assert _m
VEREDITO_MEIO_MOLDE = _m.group(1)                              # os marcadores <n> e <faixa ...> sao preenchidos do recalculo
_m = re.search(r"ganha o PREFIXO FIXO `([A-Z_]+)`", _DESENHO_TXT); assert _m, "o AO LADO de 12/11 (decisao (a) da gerencia: o prefixo da faixa) nao esta' no DESENHO"
PREFIXO_DA_FAIXA = _m.group(1); assert PREFIXO_DA_FAIXA == "K_LAW_"   # (decisao (a) da gerencia c1, 12/11: a faixa de |Z contra K| se le sozinha; o texto da faixa segue LIDO do literal)
_m = re.search(r"Recusa: `(TGL_H0DN_BG1_V411__REFUSED_%s__GATE_UNMOVED)`", _S2); assert _m
VEREDITO_RECUSA = _m.group(1)
TAG_FECHO = "TGL_H0DN_BG1_V411"
_m = re.search(r"`cunhagens_v411` \(prefixo `([A-Z0-9_]+)`\)", _S2); assert _m
CUNHAGENS_REGISTRO, CUNHAGENS_PREFIXO = "cunhagens_v411", _m.group(1)
_m = re.search(r"`kh_n1_cobertura_v411` \(prefixo `([A-Z0-9_]+)`\)", _S2); assert _m
KH_REGISTRO, KH_PREFIXO = "kh_n1_cobertura_v411", _m.group(1)
CUNHAGENS_ANTERIOR, KH_ANTERIOR = "cunhagens_v410", "kh_n1_cobertura_v410"
REGISTROS_FUNCAO = [FECHO_REGISTRO]
REGISTROS_FUNCAO_V410 = ["iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410"]   # recriados no mesmo ponto (DESENHO §2), seguem selados
_m = re.search(r"_V411_H0DN_CONTRACT", _S2); assert _m
CONTRATOS_DE_REGISTRO_FORA_DA_ESCADA = ["_V411_H0DN_CONTRACT"]   # (D135) dizer no handoff: contrato de REGISTRO, sem escada de teoremas

# ---- as 16 checagens: o texto de cada uma, LIDO do DESENHO (vira a descricao no registro)
_CHK = re.findall(r"^- (c\d+) (.+?)(?=;\n- c\d+ |\.\n\n|\n\n)", _S2.split("**`N_CHECKS_FECHO")[1], re.M | re.S)
CHECAGENS_DO_DESENHO = {k_: " ".join(v_.split()) for k_, v_ in _CHK}
assert list(CHECAGENS_DO_DESENHO) == ["c%d" % i_ for i_ in range(1, N_CHECKS_FECHO + 1)], list(CHECAGENS_DO_DESENHO)

# ---- os insumos EMBUTIDOS (tabela da secao 2: papel | arquivo sob work\ | sha16), conferidos contra o arquivo
_TAB = re.findall(r"^\| ([^|]+?) \| `([^`]+)` \| `([0-9a-f]{16})` \|$", _S2, re.M)
assert len(_TAB) == 18, ("a tabela de insumos do DESENHO nao tem 18 linhas", len(_TAB))
INSUMOS_V411 = []
for _papel, _rel, _s16 in _TAB:
    _p = os.path.join(WK, *_rel.split("\\"))
    assert os.path.exists(_p), ("insumo do DESENHO ausente", _p)
    _b = open(_p, "rb").read()
    assert hashlib.sha256(_b).hexdigest()[:16] == _s16, ("o sha16 do insumo no DESENHO nao e' o do arquivo", _rel)
    INSUMOS_V411.append({"papel": _papel.strip(), "rel": _rel, "arquivo": _p, "nome": os.path.basename(_p), "sha256": hashlib.sha256(_b).hexdigest(), "bytes": len(_b), "reuso_v410": "reuso v410" in _papel})
assert sum(1 for i_ in INSUMOS_V411 if i_["reuso_v410"]) == 2
INSUMO_POR_PAPEL = {i_["papel"]: i_ for i_ in INSUMOS_V411}
INSUMO_POR_NOME = {i_["nome"]: i_ for i_ in INSUMOS_V411}
assert len(INSUMO_POR_NOME) == 18, "dois insumos com o mesmo nome de arquivo"

# ---- os CITADOS por sha256, NAO embutidos
_m = re.search(r"\*\*Citados por sha256, N[ÃA]O embutidos:\*\* (.+)", _S2); assert _m
_CIT = re.findall(r"`([^`]+)` \(`([0-9a-f]{16})`\)", _m.group(1))
assert len(_CIT) == 7, _CIT
H0DN_V411_DIR = os.path.join(WK, "h0dn_bg1_v411_emenda_11nov")
H0DN_V410_DIR = os.path.join(WK, "astra_bell_fock_tt_05nov", "h0dn_bg1_06nov")
PUBLICACAO_DIR = os.path.join(WK, "pre_registro_h0dn_publicacao_12nov")
CITADOS_V411 = []
for _rel, _s16 in _CIT:
    _cands = [os.path.join(H0DN_V411_DIR, *_rel.split("\\")), os.path.join(WK, *_rel.split("\\"))]
    _p = [c_ for c_ in _cands if os.path.exists(c_)]
    assert len(_p) >= 1, ("citado do DESENHO ausente", _rel)
    _b = open(_p[0], "rb").read()
    assert hashlib.sha256(_b).hexdigest()[:16] == _s16, ("o sha16 do citado no DESENHO nao e' o do arquivo", _rel)
    CITADOS_V411.append({"rel": _rel, "arquivo": _p[0], "nome": os.path.basename(_p[0]), "sha256": hashlib.sha256(_b).hexdigest(), "bytes": len(_b)})
assert all("kimi" not in c_["arquivo"].lower().split(os.sep) for c_ in CITADOS_V411), "veto: nada da pasta do Kimi entra como pino"
H0DN_PASTA_VEDADA_V410 = os.path.join(WK, "h0dn_bg1_v410_09nov", "kimi")      # o veto herdado (DESENHO §2): nada daqui e' lido em rito nem entra como pino

# ---- as falas (secao 3: arquivo | sha16 | papel), conferidas contra o arquivo
CUN = os.path.join(WK, "cunhagens_13out")
_FT = re.findall(r"^\| `(OPERADOR_[^`]+_verbatim\.txt)` \| `([0-9a-f]{16})` \| ([^|]+?) \|$", _S3, re.M)
assert len(_FT) == 9, ("a lista congelada da secao 3 nao tem 9 falas", len(_FT))
FALAS_V411 = []
for _n, _s16, _papel in _FT:
    _p = os.path.join(CUN, _n); _b = open(_p, "rb").read()
    assert hashlib.sha256(_b).hexdigest()[:16] == _s16, ("o sha16 da fala no DESENHO nao e' o do arquivo", _n)
    FALAS_V411.append({"nome": _n, "arquivo": _p, "sha256": hashlib.sha256(_b).hexdigest(), "bytes": len(_b), "papel": _papel.strip(), "autor": "operador", "text": _b.decode("utf-8")})
N_FALAS_V411 = len(FALAS_V411)
FALA_POR_NOME = {f_["nome"]: f_ for f_ in FALAS_V411}
_GT = re.findall(r"`(GERENCIA_1[12]nov_[^`]+\.json)` \(sha16 `([0-9a-f]{16})`\)", _S3)
assert len(_GT) == 5, _GT
TEXTOS_DA_GERENCIA_CITADOS = []
for _n, _s16 in _GT:
    _p = os.path.join(CUN, _n); _b = open(_p, "rb").read()
    assert hashlib.sha256(_b).hexdigest()[:16] == _s16, ("o sha16 do texto da gerencia no DESENHO nao e' o do arquivo", _n)
    TEXTOS_DA_GERENCIA_CITADOS.append({"nome": _n, "arquivo": _p, "sha256": hashlib.sha256(_b).hexdigest(), "bytes": len(_b), "autor": "gerencia c1 (citado por sha256; nao e' fala do operador)"})
_m = re.search(r"`(OPERADOR_11nov_quero_sua_opiniao[^`]+_verbatim\.txt)`", _S3); assert _m
VERBATIM_FORA_DO_DESENHO_V411_NOMEADAS = [_m.group(1)]       # as outras de 11/11 fora sao por TEMA (o fecho (H, U), a torcao...); a lista por nome e' da gerencia
FALA_ORDEM_V411 = [f_ for f_ in FALAS_V411 if "chegou_a_hora_da_v411" in f_["nome"]][0]
FALA_TESTEMUNHO_V411 = [f_ for f_ in FALAS_V411 if "conseguimos_provamos" in f_["nome"]][0]
# ---- o AO LADO de 12/11 (a secao 5.1 b SUPERADA por TOPO_RATIFICADO_v411.json): as duas falas novas (a lista congelada passa a 11), o texto da gerencia novo (passam a 6) e as decisoes D171 a D173, LIDOS do bloco marcado
_m_aoT = re.search(r"<!-- ao_lado_topo_ratificado_12nov -->\n(.*?)(?=\n## |\Z)", _DESENHO_TXT, re.S); assert _m_aoT, "o AO LADO do topo ratificado (12/11) nao esta' no DESENHO"
_FT2 = re.findall(r"^\| `(OPERADOR_[^`]+_verbatim\.txt)` \| `([0-9a-f]{16})` \| ([^|]+?) \|$", _m_aoT.group(1), re.M)
assert len(_FT2) == 2, ("o AO LADO do topo ratificado nao traz as 2 falas novas", len(_FT2))
for _n, _s16, _papel in _FT2:
    _p = os.path.join(CUN, _n); _b = open(_p, "rb").read()
    assert hashlib.sha256(_b).hexdigest()[:16] == _s16, ("o sha16 da fala no AO LADO nao e' o do arquivo", _n)
    FALAS_V411.append({"nome": _n, "arquivo": _p, "sha256": hashlib.sha256(_b).hexdigest(), "bytes": len(_b), "papel": _papel.strip(), "autor": "operador", "text": _b.decode("utf-8")})
N_FALAS_V411 = len(FALAS_V411); assert N_FALAS_V411 == 11
FALA_POR_NOME = {f_["nome"]: f_ for f_ in FALAS_V411}
_GT2 = re.findall(r"`(GERENCIA_12nov_[^`]+\.json)` \(sha16 `([0-9a-f]{16})`\)", _m_aoT.group(1)); assert len(_GT2) == 1, _GT2
for _n, _s16 in _GT2:
    _p = os.path.join(CUN, _n); _b = open(_p, "rb").read()
    assert hashlib.sha256(_b).hexdigest()[:16] == _s16, ("o sha16 do texto da gerencia no AO LADO nao e' o do arquivo", _n)
    TEXTOS_DA_GERENCIA_CITADOS.append({"nome": _n, "arquivo": _p, "sha256": hashlib.sha256(_b).hexdigest(), "bytes": len(_b), "autor": "gerencia c1 (citado por sha256; nao e' fala do operador)"})
assert len(TEXTOS_DA_GERENCIA_CITADOS) == 6
FALA_RATIFICA_TOPO_V411 = [f_ for f_ in FALAS_V411 if "ratifico_a_formula" in f_["nome"]][0]


def _quando_da_fala(nome_):
    m_ = re.match(r"OPERADOR_(\d\d)nov_", nome_); assert m_, nome_
    return "%s/11/2026" % m_.group(1)


# (D181, 12/11, noite) O QUE O PROGRAMA LEVA NO LUGAR DO TEXTO das 11 falas: so' a CITACAO (a data, o sha256 do arquivo da casa lido na construcao, o papel da tabela do DESENHO e o autor): sem o texto, sem trecho e sem o nome do arquivo
# (o nome carrega as primeiras palavras da fala). O campo "text" de FALAS_V411 e' da CASA (preparacao e conferencia: a guarda_conversa_v411 o le); nunca vai ao candidato, ao core, ao artigo nem a saida do rito.
FALAS_CITADAS_V411 = [{"quando": _quando_da_fala(f_["nome"]), "sha256": f_["sha256"], "papel": f_["papel"], "autor": f_["autor"]} for f_ in FALAS_V411]
assert len(FALAS_CITADAS_V411) == N_FALAS_V411 == 11 and all(re.fullmatch(r"[0-9a-f]{64}", c_["sha256"]) for c_ in FALAS_CITADAS_V411)

# ---- decisoes e erratas (secao 4), o texto LIDO do DESENHO
_DEC = re.findall(r"\*\*(D1[56789]\d|D170)\*\* (.+?)(?= \*\*D1\d\d\*\* |\n)", _S4)
DECISOES_V411 = {k_: " ".join(v_.split()) for k_, v_ in _DEC}
assert set(DECISOES_V411) == {"D159", "D162", "D167", "D168", "D169", "D170"}, sorted(DECISOES_V411)
DECISOES_V411.update({k_: " ".join(v_.split()) for k_, v_ in re.findall(r"^- \*\*(D17[123])\*\* (.+)$", _m_aoT.group(1), re.M)})   # (AO LADO de 12/11: D171 o acordo com a custodia, D172 e D173 as ratificacoes)
# ---- o AO LADO de 12/11 (noite): a D181 (a ordem do operador sobre a conversa interna), a errata E44 e os fechos/rotulos da revisao de terceiro (TEXTO DA GERENCIA: lidos do bloco marcado, byte a byte, nunca redigitados)
_m_aoD = re.search(r"<!-- ao_lado_d181_conversa_interna_12nov -->\n(.*?)(?=\n## |\Z)", _DESENHO_TXT, re.S); assert _m_aoD, "o AO LADO da D181 (12/11, noite) nao esta' no DESENHO"
_AO_D181 = _m_aoD.group(1)
DECISOES_V411.update({k_: " ".join(v_.split()) for k_, v_ in re.findall(r"^- \*\*(D181)\*\* (.+)$", _AO_D181, re.M)})   # (D181: conversa entre os autores nao se transcreve no programa nem no artigo; cita-se so' por data e sha256)
assert list(DECISOES_V411)[-4:] == ["D171", "D172", "D173", "D181"] and len(DECISOES_V411) == 10, sorted(DECISOES_V411)
DECISOES_TOKEN_V411 = "_".join(DECISOES_V411)                  # D159_D162_D167_D168_D169_D170_D171_D172_D173_D181 (o sufixo do veredito do spec cunhagens_v411)
_mreg = re.search(r"`(OPERADOR_12nov_nao_precisa_transcrever[^`]+\.txt)` \(sha16 `([0-9a-f]{16})`\)", _AO_D181); assert _mreg
FALA_REGRA_CONVERSA_V411 = {"nome": _mreg.group(1), "arquivo": os.path.join(CUN, _mreg.group(1))}   # a ordem do operador sobre a conversa interna: NAO entra na lista das falas da versao (e' regra da casa); a guarda de conversa confere que o nome dela tem 0 ocorrencias
_b_reg = open(FALA_REGRA_CONVERSA_V411["arquivo"], "rb").read()
assert hashlib.sha256(_b_reg).hexdigest()[:16] == _mreg.group(2), "o sha16 da ordem sobre a conversa nao e' o do arquivo"
FALA_REGRA_CONVERSA_V411["sha256"] = hashlib.sha256(_b_reg).hexdigest()
_m41 = re.search(r"^- \*\*E41\*\* (.+)$", _S4, re.M); _m42 = re.search(r"^- \*\*E42\*\* (.+)$", _S4, re.M); assert _m41 and _m42
ASSINA = "gerencia c1 / claude-construtor-v411, em nome proprio, 12/11/2026"
ERRATA_E41 = {"id": "E41", "texto": _m41.group(1).strip(), "assinatura": "gerencia c1, em nome proprio (DESENHO_v411 secao 4)", "ao_lado_de": "o docstring de veredito_h0dn_v411 (modulo pinado codigo\\veredito_v411.py; nao e' tocado)"}
ERRATA_E42 = {"id": "E42", "texto": _m42.group(1).strip(), "assinatura": "gerencia c1, em nome proprio (DESENHO_v411 secao 4)", "ao_lado_de": "o colchete das duas linhas da v410 (texto selado nao reescrito)"}
# ---- E43 (AO LADO de 12/11, decisao da gerencia c1: as seis aberturas da secao da Escala NAO sao trocadas na renderizacao; entram como errata, ao lado): LIDA do bloco AO LADO marcado, nunca digitada
_m_ao43 = re.search(r"<!-- ao_lado_e43_seis_aberturas_12nov -->\n(.*?)(?=\n## |\Z)", _DESENHO_TXT, re.S); assert _m_ao43, "o AO LADO da E43 (decisao da gerencia de 12/11) nao esta' no DESENHO"
_m43 = re.search(r"^- \*\*E43\*\* (.+)$", _m_ao43.group(1), re.M); assert _m43
ERRATA_E43 = {"id": "E43", "texto": _m43.group(1).strip(), "assinatura": "gerencia c1, em nome proprio (DESENHO_v411, AO LADO de 12/11/2026)", "ao_lado_de": "as seis aberturas da secao da Escala no texto selado da v410 (nao trocadas na renderizacao; o artigo nao diverge do registro selado)"}
# ---- E44 (AO LADO de 12/11, noite; achados B-03 e B-08 da revisao de terceiro): a errata da gerencia c1 sobre a secao da v410 sobre o teste da razao de Hubble; PT e EN, LIDAS do bloco marcado, nunca digitadas
_m44 = re.search(r"^- \*\*E44\*\* (.+)$", _AO_D181, re.M); _m44en = re.search(r"^- \*\*E44 \(EN\)\*\* (.+)$", _AO_D181, re.M); assert _m44 and _m44en
ERRATA_E44 = {"id": "E44", "texto": _m44.group(1).strip(), "texto_en": _m44en.group(1).strip(), "assinatura": "gerencia c1, em nome proprio (DESENHO_v411, AO LADO de 12/11/2026, noite)",
              "ao_lado_de": "a secao da v410 sobre o teste pre-registrado da razao de Hubble (H0DN x BG1), que o artigo da v411 traz igual, e os dois trechos antigos sobre beta a 5 sigma (o paragrafo 'O que nao se declara', da v392, e a cadeia de maquina do registro estatuto_da_prova_v391); o texto selado nao e' reescrito"}
ERRATAS_V411 = [ERRATA_E41, ERRATA_E42, ERRATA_E43, ERRATA_E44]
ERRATAS_IDS_V411 = [e_["id"] for e_ in ERRATAS_V411]
ERRATAS_TOKEN_V411 = "_".join(ERRATAS_IDS_V411)               # E41_E42_E43_E44 (o sufixo do veredito do spec cunhagens_v411)
# ---- os fechos e os rotulos da revisao de terceiro (achados B-01, B-04, B-09): texto da gerencia, lido do DESENHO
_mf4 = re.search(r"O fecho da frase AO LADO do estatuto da prova[^\n]*?:\*\* PT “([^”]+)” EN “([^”]+)”", _AO_D181); assert _mf4
FECHO_ESTATUTO_PT, FECHO_ESTATUTO_EN = _mf4.group(1), _mf4.group(2)     # (B-04) depois da frase ao lado do estatuto da prova e do item do quadro “O coracao”
_mfb = re.search(r"O fecho dos dois blocos da se[çc][ãa]o nova[^\n]*?:\*\* PT “([^”]+)” EN “([^”]+)” O marcador [ée] o Z das Cefeidas livres", _AO_D181); assert _mfb
FECHO_BLOCOS_PT, FECHO_BLOCOS_EN = _mfb.group(1), _mfb.group(2)         # (B-01) no fim dos blocos dos estresses e do esperado pelos agregados; o marcador e' o Z das Cefeidas livres (lido do core no formato do topo)
assert "⟨Z das Cefeidas livres⟩" in FECHO_BLOCOS_PT and "⟨Z of the free Cepheids⟩" in FECHO_BLOCOS_EN, "o marcador do fecho dos blocos nao e' o do topo"
_mrl = re.search(r"Os r[óo]tulos do bloco do esperado pelos agregados[^\n]*? PT (.+?) EN (.+?); chave desconhecida cai no pr[óo]prio nome", _AO_D181); assert _mrl
ROTULOS_AGREGADOS_PT = dict(re.findall(r"`([A-Za-z0-9_]+)` → “([^”]+)”", _mrl.group(1)))     # (B-09)
ROTULOS_AGREGADOS_EN = dict(re.findall(r"`([A-Za-z0-9_]+)` → “([^”]+)”", _mrl.group(2)))
assert len(ROTULOS_AGREGADOS_PT) == len(ROTULOS_AGREGADOS_EN) == 5 and list(ROTULOS_AGREGADOS_PT) == list(ROTULOS_AGREGADOS_EN), (ROTULOS_AGREGADOS_PT, ROTULOS_AGREGADOS_EN)
TEXTOS_DA_GERENCIA_V411 = {"fecho_estatuto": {"pt": FECHO_ESTATUTO_PT, "en": FECHO_ESTATUTO_EN}, "fecho_blocos": {"pt": FECHO_BLOCOS_PT, "en": FECHO_BLOCOS_EN},
                           "rotulos_agregados": {"pt": dict(ROTULOS_AGREGADOS_PT), "en": dict(ROTULOS_AGREGADOS_EN)}, "e44": {"pt": ERRATA_E44["texto"], "en": ERRATA_E44["texto_en"]}}
_m = re.search(r"^- \*\*O que o teste n[ãa]o decide\*\* \(se[çc][ãa]o 6 do pr[ée]-registro\): (.+)$", _S4, re.M); assert _m
def _divide_fora_de_parenteses(s_, sep_=";"):
    out_, cur_, nivel_ = [], "", 0
    for ch_ in s_:
        nivel_ += (ch_ == "(") - (ch_ == ")")
        if ch_ == sep_ and nivel_ == 0:
            out_.append(cur_); cur_ = ""
        else:
            cur_ += ch_
    return out_ + [cur_]


NAO_DECIDE_RESUMO_PT = [x_.strip().rstrip(".") for x_ in _divide_fora_de_parenteses(_m.group(1))]   # o RESUMO da gerencia no DESENHO (texto que passa na P18); o verbatim da secao 6 e' lido do pre-registro embutido em rito
assert len(NAO_DECIDE_RESUMO_PT) == 5, NAO_DECIDE_RESUMO_PT
_m = re.search(r"^- \*\*As sete ressalvas\*\* \(.+?\): (.+)$", _S4, re.M); assert _m
RESSALVAS_ROTULOS_PT = [re.sub(r"^\d+ ", "", x_.strip()).rstrip(".") for x_ in _divide_fora_de_parenteses(_m.group(1))]
assert len(RESSALVAS_ROTULOS_PT) == 7, RESSALVAS_ROTULOS_PT

# ---- o topo do artigo (secao 5.1): os titulos LIDOS do DESENHO
_m = re.search(r"T[íi]tulo: “([^”]+)”", _S5); assert _m
TITULO_QUADRO_TOPO_PT = _m.group(1)
_m = re.search(r"PT: “(O teste decisivo[^”]+)”", _S5); assert _m
TITULO_SECAO_PT = _m.group(1)
_m = re.search(r"EN: “(The decisive test[^”]+)”", _S5); assert _m
TITULO_SECAO_EN = _m.group(1)
_m = re.search(r"ganha uma frase AO LADO \(v411\): “([^”]+)”", _S5); assert _m
FRASE_ESTATUTO_DA_PROVA_AO_LADO_PT = _m.group(1)
_m = re.search(r"passa a dizer “(os efeitos de β na natureza[^”]+)”", _S5); assert _m
FRASE_EFEITOS_DE_BETA_PT = _m.group(1)
_m = re.search(r"`TOPICO_NOVO = \"([^\"]+)\"`", _S5); assert _m
TOPICO_NOVO = _m.group(1)
MD_ROTULO_H0DN_V411 = "> **H0DN × BG1 ABERTO (v411, 12/11/2026):**"
assert MD_ROTULO_H0DN_V411 in _S5

# ======================================================================================= TEXTOS DA GERENCIA (conectivos; os numeros vem do core em rito)
# As quatro OBRIGACOES da guarda (DESENHO secao 4): onde aparecer o Z do primario contra o nulo, a cabeca do teste ou “provado na natureza” ligado a este teste, no MESMO paragrafo/bloco:
# (a) o modelo publicado, (b) a linha das Cefeidas livres com o numero, (c) validade, nao creditacao, (d) retrodicao e nao cego.
OBRIG_MODELO_PT, OBRIG_MODELO_EN = "sob o modelo de erros publicado", "under the published error model"
OBRIG_VALIDADE_PT, OBRIG_VALIDADE_EN = "validade, não creditação", "validity, not creditation"
OBRIG_RETRO_PT, OBRIG_RETRO_EN = "retrodição", "retrodiction"
OBRIG_NAO_CEGO_PT, OBRIG_NAO_CEGO_EN = "não cego", "not blind"
OBRIG_CEFEIDAS_PT, OBRIG_CEFEIDAS_EN = "Cefeidas livres", "free Cepheids"
FRASE_MOLDURA_V411_PT = ("o teste pré-registrado da razão de Hubble local/fundo foi aberto uma vez, depois do commit público do pré-registro; " + OBRIG_MODELO_PT + " o primário lê %s contra o nulo e %s contra K (ramo %s); "
                         "ao lado, no mesmo item, as " + OBRIG_CEFEIDAS_PT + " leem %s (ramo %s); " + OBRIG_RETRO_PT + " sem ajuste, com emenda posterior à guarda, teste " + OBRIG_NAO_CEGO_PT + "; provado é " + OBRIG_VALIDADE_PT + "; o gate não se move")
FRASE_MOLDURA_V411_EN = ("the pre-registered test of the local/background Hubble ratio was opened once, after the public commit of the pre-registration; " + OBRIG_MODELO_EN + " the primary reads %s against the null and %s against K (branch %s); "
                         "beside it, in the same item, the " + OBRIG_CEFEIDAS_EN + " read %s (branch %s); " + OBRIG_RETRO_EN + " without fit, with an amendment made after the guard, test " + OBRIG_NAO_CEGO_EN + "; proved is " + OBRIG_VALIDADE_EN + "; the gate does not move")
FRASE_SEM_PODER_CERTIFICADO_PT = "o poder é de desenho no modelo publicado; as linhas de estresse vão ao lado"
FRASE_SUPORTE_PT = "o vetor fora do suporte é propriedade do modelo publicado (três versões de âncora das 37 hospedeiras tratadas como uma só medida) e do vetor publicado; a colaboração resolve por pseudoinversa"
FRASE_ESPECIFICIDADE_PT = "o Z contra o nulo mede a tensão de Hubble nesta combinação de dados; o que é próprio da lei K é o tamanho do desvio sem parâmetro livre, e isso é o Z contra K"

# ---- tokens (DESENHO secao 4)
TOKENS_PROIBIDOS_V411 = tuple(D10.TOKENS_PROIBIDOS_V410)      # os da v410, herdados (CONFIRMED, PROVED_BY, P_EQUALS_NP, TURING_SOLVED, CLAY_SOLVED, MILLENNIUM, IALD_SOLVES, POLYNOMIAL_TURING)
TOKENS_PERMITIDOS_DA_CABECA = ("PROVED_IS_VALIDITY_NOT_CREDITATION", "BETA_TGL_PROVED_IN_NATURE_AT_")
TOL_RECALCULO = 1e-9                                           # c6/c9 (DESENHO): numeros a 1e-9
TOL_K = 1e-12                                                  # c10: a mesma tolerancia da v410 (tolerancias.K do contrato da v410)

# ---- A lista herdada da v410 (secao 7): LIDA da tabela
_T7 = re.findall(r"^\| ([^|]+?) \| ([^|]+?) \|$", _S7, re.M)
TABELA_SECAO7 = [{"item": a_.strip(), "nesta_versao": b_.strip()} for a_, b_ in _T7 if a_.strip() not in ("item", "---")]
assert len(TABELA_SECAO7) == 10, len(TABELA_SECAO7)
# a linha AO LADO (E43, 12/11): vale ela; a da secao 7 fica como registro (campo "na_secao_7")
_T7AO = re.findall(r"^\| ([^|]+?) \| ([^|]+?) \|$", _m_ao43.group(1), re.M)
_T7AO = [(a_.strip(), b_.strip()) for a_, b_ in _T7AO if not a_.strip().startswith(("item", "---"))]
assert len(_T7AO) == 1, _T7AO
for _r7 in TABELA_SECAO7:
    if _r7["item"] == _T7AO[0][0]:
        _r7["na_secao_7"] = _r7["nesta_versao"]; _r7["nesta_versao"] = _T7AO[0][1]; _r7["ao_lado"] = "AO LADO de 12/11/2026 (decisao da gerencia c1; E43)"
assert sum(1 for r_ in TABELA_SECAO7 if r_.get("ao_lado")) == 1, "a linha AO LADO da E43 nao casa com um item da tabela da secao 7"

# ======================================================================================= O MODO DE ENSAIO DO TOPO PROPOSTO (ordem da gerencia de 12/11: depurar a cadeia ANTES do topo ratificado)
# Com V411_ENSAIO_TOPO_PROPOSTO=1 no ambiente, TODA a cadeia le e grava numa pasta FORA de work\ (C:\t\k411c\ensaio_topo_proposto): o artefato e' um_v411_ENSAIO_TOPO_PROPOSTO.py (o texto PROPOSTO do topo,
# DESENHO 5.1 b), NUNCA chamado de candidato; o manifesto dele e' MANIFESTO_ENSAIO_TOPO_PROPOSTO_v411.json; os ESPERADOS, o ensaio a seco, a arvore simulada e o falso Nos da rodada ficam nessa pasta; nada e' instalado;
# o hash dele nao entra em arquivo nenhum da pasta da cadeia. Sem a variavel, a cadeia e' a real: o candidato (so' com TOPO_RATIFICADO_v411.json) e as saidas na pasta da cadeia; as copias do kernel por rodada em C:\t\k411c (D135).
ENSAIO_TOPO_PROPOSTO = os.environ.get("V411_ENSAIO_TOPO_PROPOSTO") == "1"
ENSAIO_DIR = os.path.join(SANDBOX_PAI, "ensaio_topo_proposto")
ENSAIO_ARTEFATO = "um_v411_ENSAIO_TOPO_PROPOSTO.py"
SAIDA = ENSAIO_DIR if ENSAIO_TOPO_PROPOSTO else HERE          # onde a rodada le e grava os seus artefatos (candidato/artefato, manifesto, ensaio, ESPERADOS, conferencias, DIFF, PINOS)
RODADA_PAI = ENSAIO_DIR if ENSAIO_TOPO_PROPOSTO else SANDBOX_PAI   # onde ficam as copias por rodada (dry_v411, falso_nos_v411, imp_*, arvore_simulada_*): FORA de work\ (D135)
CANDIDATO_ARQ = os.path.join(SAIDA, ENSAIO_ARTEFATO if ENSAIO_TOPO_PROPOSTO else CANDIDATO)
MANIFESTO_ARQ = os.path.join(SAIDA, "MANIFESTO_ENSAIO_TOPO_PROPOSTO_v411.json" if ENSAIO_TOPO_PROPOSTO else "CANDIDATO_v411.json")
FORMAL_MAP_ARQ = os.path.join(SAIDA, "FORMAL_MAP_v411.json")
PINS_ARQ = os.path.join(SAIDA, "v411_pins.py")
DRY_DIR = os.path.join(RODADA_PAI, "dry_v411")
FALSO_NOS_DIR = os.path.join(RODADA_PAI, "falso_nos_v411")
ROTULO_DO_ARTEFATO = "artefato de ENSAIO do topo proposto (NAO e' candidato)" if ENSAIO_TOPO_PROPOSTO else "candidato"
MARCA_ENSAIO = {"ensaio_topo_proposto": True, "nota": "artefato de ENSAIO com o texto PROPOSTO do topo (DESENHO 5.1 b), pendente da palavra do operador: NAO e' candidato, nao se instala, o hash nao entra na cadeia"} if ENSAIO_TOPO_PROPOSTO else {}


# ======================================================================================= O P2 AO LADO DA v387 (aditivo da gerencia c1, 12/11/2026; achado da custodia)
# O token P2_NOT_DETERMINED e' parte do veredito SELADO de three_stress_tests_v387 (segue no core; um gerador do espelho o confere): NAO muda. A leitura nova do P2 vai AO LADO, num campo NOVO do registro h0dn_bg1_v411
# (p2_ao_lado_da_v387). O rotulo e' lido de UM lugar so': TOPO_RATIFICADO_v411.json, chave rotulo_p2, quando existir; ate' la' o PROVISORIO da gerencia, marcado como proposta. Nenhum numero digitado no rotulo
# (so' o limiar 5SIGMA e o marcador <n>, que o recalculo preenche).
P2_REGISTRO_SELADO = "three_stress_tests_v387"
P2_TOKEN_SELADO = "P2_NOT_DETERMINED"
P2_ROTULO_PROVISORIO = "P2_READ_ABOVE_5SIGMA_IN_ONE_CHANNEL_UNDER_THE_PUBLISHED_MODEL__VALIDITY_NOT_CREDITATION"
P2_CANAL = "razão de Hubble, H0DN × BG1"
P2_NOTA = "o rótulo da v387 fica como registro selado; esta leitura vai ao lado; nos demais canais nada discrimina a RG à sensibilidade disponível"
_tj_p2 = json.loads(open(TOPO_RATIFICADO_ARQ, "rb").read().decode("utf-8")) if (os.path.exists(TOPO_RATIFICADO_ARQ) and not ENSAIO_TOPO_PROPOSTO) else {}
if isinstance(_tj_p2.get("rotulo_p2"), str) and _tj_p2["rotulo_p2"].strip():
    P2_ROTULO, P2_ROTULO_E_PROPOSTA, P2_ROTULO_DE = _tj_p2["rotulo_p2"].strip(), False, "TOPO_RATIFICADO_v411.json, chave rotulo_p2"
else:
    P2_ROTULO, P2_ROTULO_E_PROPOSTA, P2_ROTULO_DE = P2_ROTULO_PROVISORIO, True, "PROVISORIO da gerencia c1 (12/11; proposta, ate' a chave rotulo_p2 do TOPO_RATIFICADO_v411.json)"
assert not re.search(r"\d", P2_ROTULO.replace("<n>", "").replace("P2_", "").replace("5SIGMA", "")), ("numero digitado no rotulo do P2 (o sigma vem do recalculo, pelo marcador <n>)", P2_ROTULO)
assert P2_TOKEN_SELADO not in P2_ROTULO and re.fullmatch(r"[A-Z0-9_<>n]+", P2_ROTULO), ("o rotulo do P2 nao pode trazer o token selado e e' de maquina", P2_ROTULO)
P2_AO_LADO = {"registro": P2_REGISTRO_SELADO, "token_selado": P2_TOKEN_SELADO, "rotulo": P2_ROTULO, "rotulo_e_proposta": P2_ROTULO_E_PROPOSTA, "rotulo_de": P2_ROTULO_DE, "canal": P2_CANAL, "nota": P2_NOTA,
              "campo": "p2_ao_lado_da_v387", "preenchido_so_quando": "o registro passa e o ramo primario recalculado e' o 4 (em recusa: nulo)"}


# ======================================================================================= O TOPO RATIFICADO (D172, D173): os textos, os DOZE marcadores dirigidos por tabela, as regras e a fala do autor (LIDOS do arquivo da gerencia)
TOPO_J = json.loads(open(TOPO_RATIFICADO_ARQ, "rb").read().decode("utf-8")) if os.path.exists(TOPO_RATIFICADO_ARQ) else None
TOPO_SHA256 = hashlib.sha256(open(TOPO_RATIFICADO_ARQ, "rb").read()).hexdigest() if TOPO_J is not None else None
# a FONTE de cada marcador, em forma de maquina, derivada do campo `fonte` do arquivo (o caminho pontuado quando o arquivo o da'; os tres da Fase 9 V2 pelas chaves que o quadro “O Teste da Unica Palavra” ja' le,
# _V397_CHAVES_NUM do um.py; o ⟨n⟩ e' a parte inteira do z contra o nulo, o mesmo n da cabeca do teste). Marcador sem fonte resolvida = PARAR.
_FASE9_POR_MARCADOR = {"⟨z_disc⟩": ("z_disc", "z_disc_calibrado"), "⟨z_delta⟩": ("z_δ", "z_delta_calibrado"), "⟨lnB⟩": ("ln B", "lnB_lcdm")}


def marcadores_de_maquina(topo_j_):
    """{marcador PT: {"en", "caminho" (lista de chaves no core), "inteiro_de" (bool), "casas", "com_sinal", "fonte", "formato"}} a partir da tabela `marcadores` do TOPO_RATIFICADO_v411.json."""
    out_ = {}
    for mk_, d_ in topo_j_["marcadores"].items():
        fonte_, fmt_ = d_["fonte"], d_["formato"]
        m_ = re.match(r"^(?:parte inteira de )?([a-z0-9_]+(?:\.[A-Za-z0-9_]+)+)", fonte_)
        if mk_ in _FASE9_POR_MARCADOR:
            nome_, chave_ = _FASE9_POR_MARCADOR[mk_]
            assert fonte_.startswith("teste_de_veracidade_fase9_v397:") and nome_ in fonte_, ("a fonte do marcador da Fase 9 V2 nao e' a que o gerador sabe ler", mk_, fonte_)
            cam_ = ["teste_de_veracidade_fase9_v397", "lido", chave_]
        else:
            assert m_, ("marcador sem fonte de maquina: PARAR", mk_, fonte_)
            cam_ = m_.group(1).split(".")
        inteiro_ = fmt_.strip().startswith("inteiro")
        casas_ = int(re.match(r"^(\d+) casas", fmt_).group(1)) if not inteiro_ else 0
        out_[mk_] = {"en": d_["en"], "caminho": cam_, "inteiro_de": fonte_.startswith("parte inteira de "), "inteiro": inteiro_, "casas": casas_, "com_sinal": "com sinal" in fmt_, "fonte": fonte_, "formato": fmt_}
    return out_


if TOPO_J is not None:
    MARCADORES_V411 = marcadores_de_maquina(TOPO_J)
    assert len(MARCADORES_V411) == 12, len(MARCADORES_V411)
    REGRAS_DO_TOPO_V411 = list(TOPO_J["regras"])
    assert "fala_do_autor_para_o_quadro" not in TOPO_J, "o TOPO_RATIFICADO_v411.json ainda traz a chave fala_do_autor_para_o_quadro: a D181 (12/11, noite) a retirou; o item da fala do autor nao entra no artigo (PARAR)"
    assert isinstance(TOPO_J.get("ao_lado_d181_12nov"), dict), "o TOPO_RATIFICADO_v411.json nao traz o registro da retirada (ao_lado_d181_12nov)"
else:
    MARCADORES_V411 = REGRAS_DO_TOPO_V411 = None


def saida(nome_):
    """o caminho de um artefato da rodada (na pasta da cadeia, ou na de ensaio)."""
    return os.path.join(SAIDA, nome_)


if ENSAIO_TOPO_PROPOSTO:
    assert os.path.normcase(os.path.abspath(ENSAIO_DIR)).startswith(os.path.normcase(os.path.join(C, "t"))) and os.path.normcase(WK) not in os.path.normcase(os.path.abspath(ENSAIO_DIR)), "a pasta de ensaio tem de ficar FORA de work\\"
    os.makedirs(ENSAIO_DIR, exist_ok=True)


def sha16_arquivo(p_):
    return hashlib.sha256(open(p_, "rb").read()).hexdigest()[:16]


def sha256_arquivo(p_):
    return hashlib.sha256(open(p_, "rb").read()).hexdigest()
