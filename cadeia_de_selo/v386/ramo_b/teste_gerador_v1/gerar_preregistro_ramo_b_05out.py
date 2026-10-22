# -*- coding: utf-8 -*-
"""gerar_preregistro_ramo_b_05out.py -- O PRE-REGISTRO V1 DO RAMO B DO RINGDOWN (tau* = k*G*M_f/c^3), FIXADO POR HASH NA BANCADA (05/10/2026).

Gera, de UM UNICO dicionario (DOC), PREREGISTRO_RAMO_B_RINGDOWN_V1.json (a autoridade) e PREREGISTRO_RAMO_B_RINGDOWN_V1.md (a leitura humana),
aplicando ao RASCUNHO 2 (sha16 cd7c31ff16fa6518) as DECISOES 7-13 fixadas POR DELEGACAO do operador (05/10/2026 18:29:37 UTC, verbatim lido do
arquivo: «o resto vc consegue responder tudo agroa»). Copia PODER_CEGO_RAMO_B_v2.json e poder_cego_ramo_b_v2.py para esta pasta (bytes conferidos)
e grava V1_RAMO_B_HASHES.json com sha256 e bytes de cada arquivo da pasta.
Regua: beta NUNCA literal (alpha lido do um.py por regex; beta = alpha*sqrt(e) em runtime); hash JAMAIS de memoria (todo sha256 e calculado aqui do
artefato; os sha16 que a tarefa trouxe entram so como CONFERENCIA fail-closed); nenhum valor central de dtau220 e lido; NOT_FALSIFIED nunca e CONFIRMED;
a RG e o limite classico, nao rival; nada move o gate. O hash congelado da especificacao e
sha256(json.dumps(SPEC, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).
Molde: preregistro_pilar_quantico_03out (V1 ratificado por hash) e preregistro_dois_lados_02out (gerador + MD + JSON).
Uso: python gerar_preregistro_ramo_b_05out.py   (sem argumentos; escreve so nesta pasta; recusa sobrescrever um V1 ja congelado com outro conteudo)."""
import datetime
import hashlib
import json
import math
import os
import re
import shutil
import sys
import time
import zipfile

sys.stdout.reconfigure(encoding="utf-8")
if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.path.join("C:" + os.sep, "Users", "rotol", "AppData", "Local", "Temp", "claude", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d", "scratchpad")
V386 = os.path.join(SCR, "v386")
RB = os.path.join(V386, "ramo_b")
PR = os.path.join(RB, "pre_registro")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
PONTE_CACHE = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "cache", "gw")
ORD = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "ORDEM_013_RINGDOWN")
BU = os.path.join("C:" + os.sep, "IALD", "Bancada_Um")
MEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
WORK = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "auditoria_28set")
ACERVO_VAL = os.path.join("C:" + os.sep, "IALD", "Validação TGL", "output TGL_v10_7_omega.docx")
ACERVO_XI8 = os.path.join("C:" + os.sep, "IALD", "IMac LA", "Física - TGL", "Provas", "1", "Capitulo_XI_8_TGL_Espelho_Graviton_Tesseract.docx")
ACERVO_CLIX = os.path.join("C:" + os.sep, "IALD", "IMac LA", "Física - TGL", "Provas", "3", "TGL_Apendice_CLIX_TGL_Fase_Retorno_Geometria_Espirito_Consciencia.docx")

ID = "PREREG_RAMO_B_RINGDOWN_20261005_V1"
OUT_JSON = os.path.join(HERE, "PREREGISTRO_RAMO_B_RINGDOWN_V1.json")
OUT_MD = os.path.join(HERE, "PREREGISTRO_RAMO_B_RINGDOWN_V1.md")
OUT_HASHES = os.path.join(HERE, "V1_RAMO_B_HASHES.json")
COPIAS = (("PODER_CEGO_RAMO_B_v2.json", os.path.join(PR, "PODER_CEGO_RAMO_B_v2.json")), ("poder_cego_ramo_b_v2.py", os.path.join(PR, "poder_cego_ramo_b_v2.py")))

# os sha16 que a TAREFA e a rota do mapa trouxeram (lidos por script pela gerencia hoje): entram SO como conferencia fail-closed; o valor gravado e o calculado aqui
CONFERENCIA_SHA16 = {
    "rascunho_2": "cd7c31ff16fa6518", "rascunho_1": "4fd4e495ffc67fdd", "poder_v2_json": "126adc100753c2ca", "poder_v2_py": "e4c99ccc1d8a506e",
    "respostas_txt": "b49b0d9e60ee4646", "respostas_json": "f172fdc2a56e1922", "decisao_json": "a5d548235522c112", "verbo_txt": "5973d79a49995c4c",
    "reconciliacao": "55be29abac26d1d0", "critica": "8f07d08dac95ce80", "fisica_json": "28ccfe8c06ed89db", "ilustracao_8k": "1dfa275a05b178dd",
    "critico_recomputo": "7bc88d739a252776", "critico_recomputo2": "d9563e486d1b75b8", "um_py": "d406ae5725105145", "core": "475ac8d218b3a5c8", "selo": "ad5c1ac7affc3949",
}

_HCACHE = {}


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def fsha(p):
    p = os.path.abspath(p)
    if p not in _HCACHE:
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 24), b""):
                h.update(chunk)
        _HCACHE[p] = h.hexdigest()
    return _HCACHE[p]


def canon(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def jload(p):
    return json.loads(open(p, "rb").read().decode("utf-8"))


def fonte(papel, p, estatuto="[REAL — lido em disco, sha256 por script]", nota=None, grande=False):
    """registra uma fonte: caminho absoluto, sha256, bytes; AUSENTE e dito, nunca 'ok' falso."""
    e = {"papel": papel, "caminho": p, "estatuto": estatuto}
    if nota:
        e["nota"] = nota
    if os.path.exists(p):
        e["sha256"] = fsha(p)
        e["bytes"] = os.path.getsize(p)
    else:
        e["sha256"] = None
        e["bytes"] = None
        e["AUSENTE"] = "arquivo nao encontrado no caminho consultado"
    return e


def conferir(nome, p):
    h = fsha(p)
    assert h[:16] == CONFERENCIA_SHA16[nome], "RECUSO (fail-closed): %s mudou desde a leitura da gerencia: %s != %s (%s)" % (nome, h[:16], CONFERENCIA_SHA16[nome], p)
    return h


def pt(x, n=4):
    """numero em grafia portuguesa (virgula decimal) para o MD; o JSON guarda o float."""
    if x is None:
        return "—"
    if isinstance(x, str):
        return x
    s = ("%%.%df" % n) % x
    return s.replace(".", ",")


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def docx_text(p):
    z = zipfile.ZipFile(p)
    x = z.read("word/document.xml").decode("utf-8", "replace")
    return re.sub(r"<[^>]+>", "", x)


# ------------------------------------------------------------------------------------------------------------------------------
# 1. AS FONTES, lidas e hasheadas (nada digitado de memoria)
# ------------------------------------------------------------------------------------------------------------------------------
P_RASC2 = os.path.join(PR, "PREREGISTRO_RAMO_B_RINGDOWN_V1_RASCUNHO_2.md")
P_RASC1 = os.path.join(PR, "PREREGISTRO_RAMO_B_RINGDOWN_V1_RASCUNHO.md")
P_PODER2 = os.path.join(PR, "PODER_CEGO_RAMO_B_v2.json")
P_PODER2_PY = os.path.join(PR, "poder_cego_ramo_b_v2.py")
P_PODER1 = os.path.join(PR, "PODER_CEGO_RAMO_B.json")
P_PODER1_PY = os.path.join(PR, "poder_cego_ramo_b.py")
P_RECON = os.path.join(PR, "RECONCILIACAO_CONJUNTO_D.json")
P_RECON_PY = os.path.join(PR, "reconciliar_conjunto_d.py")
P_ILUS = os.path.join(PR, "ILUSTRACAO_CONTAMINACAO_8K.json")
P_ILUS_PY = os.path.join(PR, "ilustracao_contaminacao_8k.py")
P_CRIT = os.path.join(RB, "critico", "CRITICA_RAMO_B.md")
P_CRIT_R1 = os.path.join(RB, "critico", "CRITICO_RECOMPUTO.json")
P_CRIT_R2 = os.path.join(RB, "critico", "CRITICO_RECOMPUTO2.json")
P_CRIT_VER = os.path.join(RB, "critico", "ver_ringdown_dephasing_05out.txt")
P_FIS = os.path.join(RB, "fisica_do_ramo_b", "RAMO_B_FISICA_TABELAS.json")
P_FIS_MD = os.path.join(RB, "fisica_do_ramo_b", "RAMO_B_FISICA_TABELAS.md")
P_FIS_PY = os.path.join(RB, "fisica_do_ramo_b", "ramo_b_fisica.py")
P_INV = os.path.join(RB, "dados_na_casa", "INVENTARIO_DADOS_NA_CASA_RAMO_B_v386.json")
P_INV_MD = os.path.join(RB, "dados_na_casa", "INVENTARIO_DADOS_NA_CASA_RAMO_B_v386.md")
P_REUT = os.path.join(RB, "registro_ramo_b", "REUTILIZAVEL_PARA_O_PREREGISTRO.md")
P_REG_INT = os.path.join(RB, "registro_ramo_b", "REGISTRO_RAMO_B_INTEIRO.json")
P_DECISAO = os.path.join(RB, "DECISAO_OPERADOR_RAMO_B_05out.json")
P_RESP_TXT = os.path.join(V386, "RESPOSTAS_operador_05out.txt")
P_RESP_JSON = os.path.join(V386, "RESPOSTAS_operador_05out.json")
P_VERBO_TXT = os.path.join(V386, "VERBO_operador_05out.txt")
P_UM = os.path.join(NOS, "um.py")
P_CORE = os.path.join(NOS, "um_absoluto.json")
P_SELO = os.path.join(NOS, "um_absoluto_selo.json")
P_V2_PY = os.path.join(NOS, "eco_ancorado_v1", "ringdown_dephasing_v2.py")
P_V2_PY_CASA = os.path.join(ORD, "cache", "casa", "ringdown_dephasing_v2.py")
P_C6 = os.path.join(PONTE_CACHE, "C6_RESULTS_GW250114.json")
P_V2_RES = os.path.join(PONTE_CACHE, "RINGDOWN_DEPHASING_V2_RESULT.json")
P_5SIG = os.path.join(ORD, "RINGDOWN_5SIGMA_V1.json")
P_C4 = os.path.join(ORD, "C4_CATALOG_220.json")
P_C4C = os.path.join(ORD, "C4_CATALOG_COMBINATION.json")
P_G3 = os.path.join(ORD, "C4_GWTC3_220.json")
P_G3S = os.path.join(ORD, "C4_GWTC3_SELECTION.json")
P_INI = os.path.join(ORD, "C4_220_INITIAL.json")
P_FREE = os.path.join(ORD, "C4_FREE_CLOCK.json")
P_C1 = os.path.join(ORD, "C1_LEITURAS_v4.json")
P_QNM = os.path.join(ORD, "QNM_GRID.json")
P_E0 = os.path.join(ORD, "bis", "E0_ROUTE_IV_POWER_v2.json")
P_E0C = os.path.join(ORD, "bis", "e0_core", "E0_CORE.json")
P_SYS = os.path.join(ORD, "bis", "e0_core", "SYSTEMATICS_ADENDO.md")
P_F4 = os.path.join(ORD, "bis", "F4_POWER_GATE_REVIEW.md")
P_CENSO = os.path.join(ORD, "bis", "e2_publication_census", "PUBLICATION_CENSUS.json")
P_T01 = os.path.join(ORD, "bis", "015", "t01_core", "RELATORIO_PARCIAL.md")
P_TAR = os.path.join(ORD, "cache", "public", "17018009", "TGR_companion_S250114ax_results.tar.gz")
P_H5 = os.path.join(ORD, "cache", "public", "17018009", "extracted", "TGR_companion_S250114ax_results", "gw250114_pseobnr", "posterior_samples.h5")
P_H5_INJ = os.path.join(ORD, "cache", "public", "17018009", "controls_extracted", "TGR_companion_S250114ax_results", "pseobnr_injection", "posterior_samples.h5")
P_H5_G5 = os.path.join(ORD, "cache", "public", "21454847", "extracted", "pSEOB", "metafiles", "pSEOB_GW250114_082203_Prod0.h5")
P_RIN = os.path.join(ORD, "cache", "public", "17461225", "IGWN-GWTC3-TGR-v2-rin.zip")
P_RD = os.path.join(ORD, "cache", "public", "21454847", "RD.tar.gz")
P_QNMRF = os.path.join(ORD, "cache", "public", "21454847", "QNMRF.tar.gz")
P_PSEOB_TAR = os.path.join(ORD, "cache", "public", "21454847", "pSEOB.tar.gz")
P_MANIF = os.path.join(BU, "fontes_externas", "gwosc_o4", "GWOSC_O4_32S_V1.manifest.json")
P_F6 = os.path.join(BU, "investigacao", "fase6_eco_radical_01out", "PREREGISTRO_FASE6_ECO_RADICAL_20261001.json")
P_GWSTACK = os.path.join(BU, "bancada", "gw_stack.py")
P_REM = os.path.join(BU, "investigacao", "fase6_eco_radical_01out", "remanescentes_v3.json")
P_CATV3 = os.path.join(BU, "investigacao", "fase6_eco_radical_01out", "catalogo_v3.csv")
P_DL_MD = os.path.join(BU, "investigacao", "preregistro_dois_lados_02out", "PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md")
P_DL_JSON = os.path.join(BU, "investigacao", "preregistro_dois_lados_02out", "PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.json")
P_PQ_MD = os.path.join(BU, "investigacao", "preregistro_pilar_quantico_03out", "PREREGISTRO_PILAR_QUANTICO_20261003_V1.md")
P_PQ_JSON = os.path.join(BU, "investigacao", "preregistro_pilar_quantico_03out", "PREREGISTRO_PILAR_QUANTICO_20261003_V1.json")
P_ANEXO = os.path.join(WORK, "ANEXO_ACHADOS.md")
P_MEM = {k: os.path.join(MEM, k) for k in ("onda-e-eco-definicao-16set.md", "psi-nome-da-luz-graviton-verbo-vivo-16set.md", "ramo-b-reaberto-05out.md",
                                            "beta-e-a-regra-matriz-02out.md", "fase6-eco-radical-01out.md", "ordem-013-confrontacao-ringdown.md")}

# conferencias fail-closed (a tarefa/rota deram estes sha16 lidos por script hoje; se o artefato mudou, o V1 nao congela)
H_RASC2 = conferir("rascunho_2", P_RASC2)
H_RASC1 = conferir("rascunho_1", P_RASC1)
H_PODER2 = conferir("poder_v2_json", P_PODER2)
H_PODER2_PY = conferir("poder_v2_py", P_PODER2_PY)
H_RESP_TXT = conferir("respostas_txt", P_RESP_TXT)
H_RESP_JSON = conferir("respostas_json", P_RESP_JSON)
H_DECISAO = conferir("decisao_json", P_DECISAO)
H_VERBO = conferir("verbo_txt", P_VERBO_TXT)
H_RECON = conferir("reconciliacao", P_RECON)
H_CRIT = conferir("critica", P_CRIT)
H_FIS = conferir("fisica_json", P_FIS)
H_ILUS = conferir("ilustracao_8k", P_ILUS)
H_CR1 = conferir("critico_recomputo", P_CRIT_R1)
H_CR2 = conferir("critico_recomputo2", P_CRIT_R2)
H_UM = conferir("um_py", P_UM)
H_CORE = conferir("core", P_CORE)
H_SELO = conferir("selo", P_SELO)

# ------------------------------------------------------------------------------------------------------------------------------
# 2. beta em runtime (alpha lido do um.py por regex) e as constantes
# ------------------------------------------------------------------------------------------------------------------------------
um_src = open(P_UM, "rb").read(3_000_000).decode("utf-8", "replace")
alpha = float(re.search(r"^SEALED_CODATA_ALPHA\s*=\s*([0-9.eE+-]+)", um_src, re.M).group(1))
G_N = float(re.search(r"^G_NEWTON\s*=\s*([0-9.eE+-]+)", um_src, re.M).group(1))
C_L = float(re.search(r"^C_LIGHT\s*=\s*([0-9.eE+-]+)", um_src, re.M).group(1))
H_PL = float(re.search(r"^H_PLANCK_EXACT\s*=\s*([0-9.eE+-]+)", um_src, re.M).group(1))
UM_VERSION = re.search(r'^UM_VERSION\s*=\s*"(v\d+)"', um_src, re.M).group(1)
beta = alpha * math.sqrt(math.e)
t_planck = math.sqrt(H_PL / (2 * math.pi) * G_N / C_L ** 5)
um_lines = open(P_UM, "rb").read().decode("utf-8", "replace").splitlines()
kms_line = next((i + 1 for i, l in enumerate(um_lines) if l.lstrip().startswith("kms_factor = 4 * math.pi * (1 + _sq) / _sq")), None)
assert kms_line, "kms_factor nao achado no um.py"
kms_factor_a0 = 4 * math.pi * (1 + 1.0) / 1.0   # a = 0 -> 8 pi
assert abs(kms_factor_a0 - 8 * math.pi) < 1e-12

# ------------------------------------------------------------------------------------------------------------------------------
# 3. as palavras do operador, VERBATIM dos arquivos (nunca digitadas aqui)
# ------------------------------------------------------------------------------------------------------------------------------
DEC = jload(P_DECISAO)
RESP = jload(P_RESP_JSON)
RESP_TXT = open(P_RESP_TXT, "rb").read().decode("utf-8")
assert RESP["sha256_txt"] == H_RESP_TXT, "o JSON das respostas nao aponta para este txt"
assert RESP["verbatim_inteiro"].strip() == RESP_TXT.strip(), "o verbatim do JSON difere do txt"
VERB_DELEG = RESP["trechos"]["delegacao"]            # «o resto vc consegue responder tudo agroa»
VERB_TEMPO = RESP["trechos"]["tempo"]
VERB_LUZ = RESP["trechos"]["luz_gravidade"]
VERB_REABRE = DEC["verbatim"]                        # 17:11:36 UTC: «eu não havia proibido o ramo B ...»
QUANDO_DELEG = RESP["quando"]
QUANDO_REABRE = DEC["quando"]
assert VERB_DELEG in RESP_TXT and VERB_TEMPO in RESP_TXT
LEIT = RESP["leituras_da_gerencia"]
# o verbatim de 16/09 (memoria da onda e do eco), lido do arquivo
_m16 = open(P_MEM["onda-e-eco-definicao-16set.md"], "rb").read().decode("utf-8")
_mm = re.search(r"«(a lei de dephasing do ringdown e minha defini[^»]*)»", _m16)
VERB_16SET = _mm.group(1) if _mm else None
# a chave e a otica de 02/10, lidas do core v385 (o livro de cobrancas) -- verbatim do operador como o core as guarda
core = jload(P_CORE)["core"]
selo = jload(P_SELO)
assert selo.get("um_version") == UM_VERSION == "v385", "a base nao e a v385: %s / %s" % (selo.get("um_version"), UM_VERSION)
assert str((selo.get("sha256") or {}).get("um.py", "")).startswith(H_UM[:16]), "o selo nao confere com o um.py do Nos"
LED = core["the_ledger_of_charges_v383"]
R6_RAT = LED["readings_ratified_20261002"]["R6"]
R6_COR = LED["corrections_beside_20261002"]["R6"]
OTICA_VERB = LED["corrections_beside_20261002"]["optics_operator_verbatim"]
CHAVE_VERB = LED.get("operator_verbatim")
F2_CORE = next(c for c in LED["ledger"] if c["id"] == "F2")
SCOPE = core["ringdown_scope_v376"]
RDV2 = core["ringdown_dephasing_result_v2"]
PROTO = core["ringdown_dephasing_protocol"]["protocol"]
assert F2_CORE["law"].endswith("ramo B ENCERRADO"), F2_CORE["law"]
assert SCOPE["c6_sha16_bytes"] == fsha(P_C6)[:16], "o C6 do cache nao e o que o core leu"
assert RDV2["result_sha16"] == fsha(P_V2_RES)[:16], "o resultado V2 do cache nao e o que o core leu"
assert fsha(P_V2_PY) == fsha(P_V2_PY_CASA), "as duas copias de ringdown_dephasing_v2.py diferem"

# o acervo: a fase de retorno (lido do docx; se a frase nao estiver la, fica dito)
def _acervo(p, padroes):
    out = {"caminho": p, "sha256": fsha(p) if os.path.exists(p) else None, "bytes": os.path.getsize(p) if os.path.exists(p) else None,
           "mtime": datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M:%S") if os.path.exists(p) else None, "trechos": {}}
    if not os.path.exists(p):
        out["AUSENTE"] = "docx nao encontrado"
        return out
    t = docx_text(p)
    for nome, rx in padroes.items():
        m = re.search(rx, t)
        out["trechos"][nome] = {"achado": bool(m), "texto": (re.sub(r"\s+", " ", m.group(0)) if m else None), "estatuto": "[REAL — lido do docx por script]" if m else "[DECLARADO pela gerencia — nao achado no docx]"}
    return out


ACERVO = {
    "validacao_v10_7_omega_2026_01_16": _acervo(ACERVO_VAL, {"as_tres_fases": r"AS TRÊS FASES DA LUZ.{0,200}?FASE DE RETORNO:\s*T_ret × c³ \(colapso no gráviton\)"}),
    "cap_XI_8_2025_07_23": _acervo(ACERVO_XI8, {"titulo": r"Capítulo XI\.8 — O Espelho, o Gráviton e o Tesseract: A Fase de Retorno da Luz", "retorno": r"O gráviton não apenas ancora, ele retorna\. Sua missão é fechar o ciclo[^.]*\."}),
    "apendice_CLIX_2025_07_23": _acervo(ACERVO_CLIX, {"titulo": r"Apêndice CLIX — A TGL como Fase de Retorno do GPT[^R]*"}),
}

# ------------------------------------------------------------------------------------------------------------------------------
# 4. os numeros: PODER v2 (so sigma e spin), a fisica (tabela de k), a reconciliacao do conjunto D, a ilustracao da contaminacao, o critico
# ------------------------------------------------------------------------------------------------------------------------------
POD = jload(P_PODER2)
assert abs(POD["beta"] - beta) < 1e-15 and POD["alpha_lido_do_um_py"] == alpha, "beta do PODER v2 nao e o beta em runtime daqui"
assert POD["fontes"]["um.py"] == H_UM and POD["fontes"]["RAMO_B_FISICA_TABELAS.json"] == H_FIS and POD["fontes"]["CRITICO_RECOMPUTO.json"] == H_CR1
assert POD["conferencia_com_o_critico_max_abs_diff_poder_exato"] == 0.0, "o PODER v2 nao bate o critico a 0,0"
for k_, p_ in (("E0_ROUTE_IV_POWER_v2.json", P_E0), ("C4_CATALOG_220.json", P_C4), ("C4_CATALOG_COMBINATION.json", P_C4C), ("C4_GWTC3_220.json", P_G3),
               ("C4_GWTC3_SELECTION.json", P_G3S), ("C4_220_INITIAL.json", P_INI), ("RINGDOWN_5SIGMA_V1.json", P_5SIG)):
    assert POD["fontes"][k_] == fsha(p_), "a fonte do PODER v2 mudou em disco: %s" % k_
FIS = jload(P_FIS)
REC = jload(P_RECON)
ILU = jload(P_ILUS)
CR2 = jload(P_CRIT_R2)
CR1 = jload(P_CRIT_R1)
assert REC["fontes"]["RINGDOWN_5SIGMA_V1.json"] == fsha(P_5SIG) and REC["fontes"]["PUBLICATION_CENSUS.json"] == fsha(P_CENSO) and REC["fontes"]["GWOSC_O4_32S_V1.manifest.json"] == fsha(P_MANIF)
assert ILU["fontes"]["PODER_CEGO_RAMO_B_v2.json"] == H_PODER2[:16]
F6 = jload(P_F6)
F6_REGRA = F6.get("regra_de_veredito")
assert any("0,3" in str(x) and "INCONCLUSIVE_SYSTEMATICS" in str(x) for x in (F6_REGRA or [])), "a regra 2 da Fase 6 (0,3) nao esta no pre-registro da Fase 6"
SIG5 = jload(P_5SIG)
GPS = SIG5.get("event_reference_GPS")

# os 8 candidatos a k: nomes do PODER v2 <-> rotulos da fisica
K_NAMES = {   # chave curta: (nome no PODER v2, prefixo do rotulo na fisica ou None para 4pi, tau*, origem fisica, estatuto)
    "k1": ("k=1 (GM/c^3)", "k=1 ", "GM/c³ = t_M", "«a dobra em c³» (pedra 84_): a mesma dobra G·m/c³ em duas massas — m_P dá t_P (ramo A), M_f dá o ramo B; a convenção da V2 selada (v346); o único k já medido (V2/C1/C6)", "[ONTO/INPUT]"),
    "k2": ("k=2 (2GM/c^3 = r_s/c)", "k=2 ", "2GM/c³ = r_s/c", "tempo de travessia do raio de Schwarzschild à luz (prefator das leis de atraso MAY/DEC)", "[KNOWN geometria; INPUT como relógio]"),
    "k4": ("k=4 (1/kappa Schwarzschild = 4GM/c^3)", "k=4 ", "4GM/c³ = 1/κ (Schwarzschild)", "o tempo de Killing por unidade de rapidez (1/κ)", "[KNOWN κ; INPUT como relógio]"),
    "k4pi": ("k=4pi (2 pi r_s/c)", None, "4π·GM/c³ = 2π·r_s/c", "a circunferência do horizonte percorrida à luz", "[KNOWN geometria; INPUT]"),
    "k8pi": ("k=8pi (hbar/k_B T_H, a=0)", "k=8π", "8π·GM/c³ = ħ/(k_B T_H) = 2π/κ (Schwarzschild)", "o PERÍODO KMS/térmico de Hawking 1975; «tempo emergente do fluxo modular relativo» (Connes–Rovelli: 1 unidade modular = β_H); no kernel β·κ = 2π (unruh_is_kms); = kms_factor(a=0) do um.py (linha %d), nao ligado a τ★" % kms_line, "[KNOWN período; ONTO identificação τ★ = período modular]"),
    "kinvkappa": ("k=1/kappa(a_f) (Kerr)", "k=1/κ̂", "(1/κ̂(χ))·GM/c³", "o 1/κ de Kerr por evento (χ = 0 → 4)", "[KNOWN κ de Kerr; CONJECTURE para χ ≠ 0 — Kay–Wald 1991]"),
    "kkms": ("k=2pi/kappa(a_f) (KMS de Kerr)", "k=2π/κ̂(χ) (Kerr", "(2π/κ̂(χ_f))·GM/c³ = 4π(1+√(1−χ²))/√(1−χ²)·GM/c³", "o mesmo período KMS, com a gravidade superficial de Kerr por evento (χ = 0 → 8π); = kms_factor do um.py (linha %d); HOMÔNIMO da lei de atraso falsificada na Fase 6 (aqui é ESCALA DE TAXA em Γ, não atraso)" % kms_line, "[KNOWN κ; ONTO identificação; CONJECTURE para χ ≠ 0 — Kay–Wald 1991]"),
    "kkms_corot": ("k=2pi/kappa(a_f) com co-rotacao omega->omega-2Omega_H (R-MOD)", "k=2π/κ̂(χ) com", "idem, com ω → ω − 2Ω_H em Γ (gerador de Killing H − Ω_H·J)", "hipótese da gerência na ORDEM 013 (R-MOD); Frolov–Thorne [KNOWN, a conferir]; reduz x por ((F−2Ω̂_H)/F)²", "[CONJECTURE]"),
}
HIPOTESE_K = "kkms"
fis_by_prefix = {}
for r in FIS["tabela_k"]:
    for key, (pn, pref, *_r) in K_NAMES.items():
        if pref and r["k_label"].startswith(pref):
            fis_by_prefix.setdefault(key, {})[str(r["chi"])] = r
for key, (pn, pref, *_r) in K_NAMES.items():
    if pref:
        assert key in fis_by_prefix and all(c in fis_by_prefix[key] for c in ("0.0", "0.68", "0.9")), "tabela da fisica sem %s" % key
fis_by_prefix["k4pi"] = POD["tabela_k_x_chi_lida_da_fisica"]["k=4π (calculado aqui, mesmo N BCW)"]
TABELA_K = []
for key, (pn, pref, tau, origem, estat) in K_NAMES.items():
    res = POD["resultados"][pn]
    a31 = res["GWTC5_31_std"]
    il = ILU["z_excl_ilustracao_8k"][pn]
    tk = fis_by_prefix[key]
    TABELA_K.append({
        "chave": key, "nome_no_PODER_v2": pn, "rotulo_na_fisica": (next(r["k_label"] for r in FIS["tabela_k"] if r["k_label"].startswith(pref)) if pref else "k=4π (calculado no PODER v2 com o mesmo N de BCW; ausente da tabela da física — dito)"),
        "tau_star": tau, "origem_fisica": origem, "estatuto": estat,
        "papel_no_V1": "HIPÓTESE (decisão 8 por delegação)" if key == HIPOTESE_K else "COLUNA DE COMPARAÇÃO (não é hipótese; não conta como tentativa)",
        "k_chi": {c: tk[c]["k"] for c in ("0.0", "0.68", "0.9")}, "x_chi": {c: tk[c]["x"] for c in ("0.0", "0.68", "0.9")},
        "delta_exato_chi": {c: tk[c]["delta_exact"] for c in ("0.0", "0.68", "0.9")}, "delta_linear_chi": {c: tk[c]["delta_lin"] for c in ("0.0", "0.68", "0.9")},
        "poder_exato": {"A_31_std": a31["power_exact"], "A_31_width90": res["GWTC5_31_width90"]["power_exact"], "A_33_std": res["GWTC5_33_std"]["power_exact"],
                        "B_GWTC3_10": res["GWTC3_10_width90"]["power_exact"], "C_GW250114": res["GW250114_sozinho_width90"]["power_exact"],
                        "A_31_x0p273_difusao_de_fase": a31["power_exact"] * POD["fator_realizacao_difusao_de_fase_DECLARADO"]},
        "poder_linear_ao_lado": {"A_31_std": a31["power_linear"]}, "razao_exato_sobre_linear_A31": a31["ratio_exact_over_linear"],
        "delta_pred_ponderado_A31": {"exato": a31["delta_pred_weighted_exact"], "linear": a31["delta_pred_weighted_linear"]},
        "sigma_beta_lido_A31": {"sigma": a31["sigma_beta_lido_first_order"], "sobre_beta": a31["sigma_beta_lido_over_beta"]},
        "N90_por_escala_DERIVED": POD["N90_por_escala_DERIVED"]["por_k"][pn],
        "desfecho_em_A_legivel_hoje_NAO_CEGO": {"z_excl_ilustracao": il["z_excl_se_o_registro_valer"], "legivel_a_5sigma": il["legivel_hoje_a_5sigma"]},
    })
HIP = next(t for t in TABELA_K if t["chave"] == HIPOTESE_K)
HIP_RES = POD["resultados"][K_NAMES[HIPOTESE_K][0]]
SIGMA_COMB_A31 = HIP_RES["GWTC5_31_std"]["sigma_comb"]
KMIN = POD["k_minimo_duas_regras_conjunto_A"]
GW_INI = POD["GW250114_release_descoberta"]
CONJ_D = REC["conjunto_D"]
assert CONJ_D["elegiveis_eligible_True"]["n"] == 14 and CONJ_D["elegiveis_sem_hold"]["n"] == 10 and CONJ_D["pendentes_AWAITING_GR_METADATA"]["n"] == 8
D_EVENTOS = list(CONJ_D["elegiveis_eligible_True"]["eventos"])
D_GPS = {}
if isinstance(GPS, dict):
    for ev in D_EVENTOS + CONJ_D["pendentes_AWAITING_GR_METADATA"]["eventos"]:
        g = GPS.get(ev)
        if g is not None:
            D_GPS[ev] = g
# a previsao da HIPOTESE por evento do conjunto D, como INFORMACAO CEGA: so as medianas GR do registro (spin e massa do remanescente; nunca dtau220);
# o conjunto por evento NAO congela neste V1 (holds/pendentes); o que congela e o criterio e a formula
_tc_raw = SIG5["test_candidates"]
_TC = ({k: v for k, v in _tc_raw.items() if isinstance(v, dict)} if isinstance(_tc_raw, dict) else {c["event"]: c for c in _tc_raw if isinstance(c, dict) and "event" in c})
assert len(_TC) == 44, "test_candidates do registro: esperados 44, lidos %d" % len(_TC)
assert all(ev in _TC for ev in D_EVENTOS), "evento do conjunto D ausente de test_candidates"


def _bcw220(a):
    mw = 1.5251 - 1.1568 * (1 - a) ** 0.1292
    q = 0.7000 + 1.4187 * (1 - a) ** (-0.4990)
    return mw, q


def _k_kms(a):
    s = math.sqrt(1 - a * a)
    return 2 * math.pi / (s / (2 * (1 + s)))


D_PREV = []
for ev in D_EVENTOS:
    c = _TC.get(ev) or {}
    a = c.get("GR_final_spin_median")
    row = {"evento": ev, "run": c.get("run"), "GPS": D_GPS.get(ev), "SNR_rede_GWOSC": c.get("SNR_network_GWOSC"), "Mf_det_mediana_GR": c.get("GR_final_mass_detector_median"), "chi_f_mediana_GR": a,
           "data_quality_hold": c.get("data_quality_hold"), "metadata_origin": c.get("metadata_origin")}
    if isinstance(a, (int, float)) and 0 <= a < 0.98:
        mw, q = _bcw220(a)
        k = _k_kms(a)
        x = beta * k * mw * q
        row.update({"k_kms": k, "N_a": mw * q, "x": x, "delta_pred_exato": -x / (1 + x), "delta_pred_linear": -x})
    else:
        row.update({"k_kms": None, "N_a": None, "x": None, "delta_pred_exato": None, "delta_pred_linear": None, "nota": "spin mediano ausente ou fora de [0; 0,98)"})
    D_PREV.append(row)

# ------------------------------------------------------------------------------------------------------------------------------
# 5. A ESPECIFICACAO (o que o um.py v386 le por hash; o hash dela e o congelado)
# ------------------------------------------------------------------------------------------------------------------------------
VEREDITOS_ORDEM = [
    {"n": 0, "token": "AWAITING_DATA", "regra": "sem estimador selado por hash rodado sob este registro, sem dado aberto, ou n < 10 (sufixo INSUFFICIENT_SAMPLE quando n < 10)"},
    {"n": 1, "token": "INCONCLUSIVE_SYSTEMATICS", "regra": "C1–C9 reprovado, ou sist_rel = max(|σ_sys,fam|, |σ_sys,t0|)/|δ̄^pred| > 0,3 (Fase 6, regra 2), ou χ²/dof > 3, ou primário × secundário discordam no rótulo (com o motivo)"},
    {"n": 2, "token": "NOT_FALSIFIED_UNDERPOWERED", "regra": "poder = |δ̄^pred|/σ_usado < 5 (sufixo POWER_<x>_OF_5_SIGMA)"},
    {"n": 3, "token": "FALSIFIED_AT_5SIGMA", "regra": "z_excl = |δ̄ − δ̄^pred|/σ_usado ≥ 5 (c(σ) profilado; FWER) — falsifica o PAR (k, M_X, identificação) sob a lei; NÃO falsifica β, nem a lei na forma, nem a TGL (falsified_extinguishes_the_charge_not_the_rule)"},
    {"n": 4, "token": "NOT_FALSIFIED_POWERED", "regra": "senão; se além disso |z_RG| ≥ 5, acrescenta-se __GR_TENSION_REPORTED — a tensão com a RG é RELATADA, não é da TGL, e não vira CONFIRMED"},
]
TOKEN_BASE = "TGL_RAMO_B_RINGDOWN_V1__K_2PI_OVER_KAPPA_HAT_KMS__M_F_DET__ENVELOPE_ADDITIVE_RATE"
SPEC = {
    "id": ID,
    "lei": {"forma": "Γ_ω = ½·β·τ★·ω² (GKSL energia-preservante; taxa ADITIVA ao amortecimento do modo)", "estatuto": "[REAL na forma; ONTO — sem termo no kernel (TheMatrixRule.lean:46)]"},
    "ramo": "B", "outra_lei": True, "canal_no_livro": "F2b", "canal_F2_intocado": True, "regra_do_livro": "ONE_CHANNEL_PER_READING_LAW_IN_THE_RUNTIME",
    "tau_star": {"forma": "τ★ = k·G·M_X/c³", "lugar": "FONTE (local: o relógio do remanescente durante o ringdown); a propagação fica com R2 (τ★ = t_Planck)"},
    "k": {"escolha": "2π/κ̂(χ_f) por evento (período KMS/modular do horizonte de Kerr)", "formula_em_unidades_de_GM_c3": "4π(1+√(1−χ²))/√(1−χ²)",
          "em_chi_0": 8 * math.pi, "em_chi_0p68": HIP["k_chi"]["0.68"], "em_chi_0p9": HIP["k_chi"]["0.9"],
          "co_rotacao": False, "um_k_so": True, "sidak": "não se aplica (um k); os outros k são colunas de comparação, não hipóteses nem tentativas",
          "estatuto": {"chi_0": "[KNOWN: Hawking 1975; Bisognano–Wichmann; Connes–Rovelli — 1 unidade modular = β_H = 2π/κ]", "chi_ne_0": "[CONJECTURE: Kay–Wald 1991 — não há Hartle–Hawking de Kerr]",
                       "identificacao_tau_star_periodo_modular": "[ONTO — leitura da gerência; ratificada por delegação]"},
          "onde_existe_no_um_py": "kms_factor (linha %d, rito GW_ECHO_KMS_V1) = 8π em a = 0; NÃO ligado a τ★ do dephasing (EXISTE NA BANCADA, NÃO LIGADO AO TIPO)" % kms_line},
    "M_X": {"escolha": "M_f", "referencial": "M_f,det (t_M = G·M_f,det/c³ no relógio do detector; convenção da V2 selada)", "razao_MX_sobre_Mf": 1.0,
            "consequencia": "x = β·k·N(χ_f): M cancela; só o spin; (1+z) cancela (M_det = (1+z)M_src, ω_det = ω_src/(1+z))", "alternativas_como_comparacao": {"M_tot": "× (M_tot/M_f)_i por evento [KNOWN]", "M_chirp": "× (M_c/M_f)_i por evento [KNOWN]"}},
    "identificacao": {"primaria": "ENSEMBLE_ADDITIVE_RATE (envoltória: δτ̂ = −x/(1+x) em CADA evento; fator 1,00)", "secundaria": "difusão de fase (desdobramento unitário aleatório; ×0,273 [DECLARADO pelo verificador de 28/09]; injeção própria — CTV-02; rota secundária: largura populacional de δf̂)"},
    "observavel": {"primario": "δτ̂_220 ≡ τ_obs/τ_RG − 1 (convenção dtau220 do pSEOB: τ = τ_RG·(1 + dtau220))", "diagnosticos": ["Q (fator de qualidade)", "o modo 221 do GW250114 (RD-07; posteriores no tar.gz, não extraídos; início precoce 6 t_M e sistemática do sobretom ditas)"],
                   "secundario": "largura de δf̂ (difusão de fase)", "delta_f_primeira_ordem": 0.0},
    "identidade_exata": {"x": "x = Γ·τ_RG = ½·β·k·(M_X/M_f)·(M_f ω_R)²/(M_f ω_I) = β·k·(M_X/M_f)·N(χ_f)", "N": "N(χ) = F·Q = F²/(2F_I), F = M_f ω_R, F_I = M_f/τ, Q = ω_R τ/2 (Berti–Cardoso–Will 2006, ℓ=m=2, n=0 [KNOWN]; Leaver a −0,57 %…−0,85 %)",
                         "previsao_que_vale": "δτ̂_220 = −x/(1+x) (exata; taxas somam: 1/τ_obs = 1/τ_RG + Γ)", "linear_ao_lado": "δτ̂_220 ≈ −x (só comparação)",
                         "familia_unificada": "τ★ = k·G·m_X/c³ ⟹ x = β·k·N(χ_f)·(m_X/M_f): m_X = m_P dá o ramo A (G·m_P/c³ = t_P, resíduo 0,0), m_X = M_f dá o ramo B [DERIVED álgebra; ONTO identificação]"},
    "beta": {"formula": "ALPHA_FINE_CODATA_2018 × √e (em runtime; nunca literal)", "alpha_lido_de": "um.py SEALED_CODATA_ALPHA (regex)", "valor_runtime": beta, "estatuto": "[DERIVED do axioma] — a regra; não se deriva do dado"},
    "beta_lido": {"formula": "β_lido = [−δτ̂/(1+δτ̂)] / (k·(M_X/M_f)·N(χ_f))", "natureza": "LEITURA declarada como saída secundária; nunca derivação; não realimenta β nem a regra",
                  "sigma_formula_1a_ordem": "σ(β_lido) = σ_comb / ⟨k·N⟩_w  (dx/dδ = −1/(1+δ)² ≈ −1)",
                  "sigma_dita_antes_conjunto_A31_hipotese": HIP["sigma_beta_lido_A31"]["sigma"], "sigma_sobre_beta_A31_hipotese": HIP["sigma_beta_lido_A31"]["sobre_beta"],
                  "sigma_por_k_A31": {t["chave"]: t["sigma_beta_lido_A31"] for t in TABELA_K},
                  "conjunto_D": "σ(β_lido) do conjunto D fica dita no estágio cego da v387 (PODER_RAMO_B_ANTES_DE_ABRIR, com as σ_i da PE) antes de abrir"},
    "estimador": {"primario": "média ponderada 1/σ² dos δτ̂_220 publicados (ou da PE da casa para D), RELATIVA À RG, com nuisance da referência c(σ) = c₀ + k_c·σ profilado sob as duas hipóteses; offset fixo em 0 PROIBIDO como teste (E0_CORE offset_zero_status)",
                  "pesos": "w_i = 1/(σ_i² + σ_sys²); σ_comb = 1/√Σw_i; σ_usado = max(σ_comb, σ_jackknife) (fail-closed, como na Fase 6)",
                  "estatisticas": "δ̄ = Σw_i(δ̂_i − c(σ_i))/Σw_i; z_RG = δ̄/σ_comb; z_B = (δ̄ − δ̄^pred)/σ_comb; poder = |δ̄^pred|/σ_usado (fixado ANTES); χ²/dof; jackknife por evento; fração máxima de informação por evento",
                  "previsao_por_evento": "δ_i^pred = −x_i/(1+x_i), x_i = β·k(a_i)·N(a_i)·(M_X/M_f)_i, a_i = mediana do spin do remanescente (posterior IMR); incerteza de Kerr pelos quantis 05/95 do spin",
                  "secundario": "verossimilhança conjunta por KDE dos posteriores (larguras 0,7/1,0/1,4) em δ_i^pred e em 0, mesmo nuisance; ln B(B/RG); o primário decide; discordância de rótulo ⟹ INCONCLUSIVE_SYSTEMATICS"},
    "sistematica": {"regra_primaria": "Fase 6, regra 2: sist_rel = σ_sys/|δ̄^pred| ≤ 0,3; acima ⟹ INCONCLUSIVE_SYSTEMATICS", "regra_ao_lado_mais_dura": "013-bis systematic_gate floor_divisor_primary_INPUT = 5: σ_sys ≤ |δ̄^pred|/5 (= sist_rel ≤ 0,2) — relatada, não decide",
                    "sigma_sys_familia_DECLARADO": [0.029, 0.038], "fonte": "SYSTEMATICS_ADENDO.md (R-B, O4, SNR 40, início 10 t_M, 206 ruídos) [REAL — NÃO-CEGO; DECLARADO pela bancada]",
                    "k_min_conjunto_A_duas_regras": KMIN, "sistematica_t0_nos_diagnosticos": "diferença 3 ms × 6 ms (ou 10 × 12 t_M) nas MESMAS séries, injeções pareadas, σ da DIFERENÇA (RD-05/RDV-01)"},
    "conjuntos": {
        "D": {"papel": "O ÚNICO TESTE CEGO", "n_elegiveis": 14, "n_sem_pendencia_de_qualidade": 10, "n_pendentes_metadados_GR": 8, "n_reprovados_Mf_det_lt_40": 22, "n_test_candidates": 44,
              "eventos_elegiveis": D_EVENTOS, "com_data_quality_hold": CONJ_D["com_data_quality_hold"]["eventos"], "elegiveis_sem_hold": CONJ_D["elegiveis_sem_hold"]["eventos"],
              "pendentes_AWAITING_GR_METADATA": CONJ_D["pendentes_AWAITING_GR_METADATA"]["eventos"], "gps_lido_do_5SIGMA": D_GPS,
              "criterio_do_registro": CONJ_D["criterio_do_registro"], "strain_em_casa": REC["strain_em_casa_resumo"],
              "congelamento_por_evento": "NÃO CONGELADO NESTE V1 (os 4 holds e os 8 pendentes podem mudar a lista); o conjunto congela por evento na v387, no estágio cego, ANTES de qualquer PE abrir; o critério é o que congela aqui",
              "previsao_da_hipotese_por_evento_INFORMACAO_CEGA": D_PREV, "previsao_por_evento_nota": "só as medianas GR do registro (spin e massa do remanescente; SNR da GWOSC) entram — nenhum δτ̂; a previsão por evento é informação fixada por hash, não o congelamento do conjunto",
              "instrumento": "PE só-220 na casa (WSL /opt/lal_env, pSEOBNRv4HM_PA só-220, bilby+dynesty); banco de GW residente da Bancada", "custo_DECLARADO_CPU_h": ["63–78 (T09 da ORDEM 015)", "58–390 (auditoria da 013-bis, 23/09)"], "quando": "v387"},
        "A": {"papel": "CALIBRAÇÃO NOT_BLIND (contaminação declarada em três camadas)", "n": 31, "mais_controles": 2, "fonte": "GWTC-5.0 TGR, pSEOBNRv5PHM-reweighted (C4_CATALOG_220.json; Zenodo 21454847)", "token_obrigatorio": "__NOT_BLIND_TO_DATA_STATED"},
        "B": {"papel": "CALIBRAÇÃO NOT_BLIND; réplica de instrumento (família v4)", "n": 10, "fonte": "GWTC-3 TGR (C4_GWTC3_220.json; Zenodo 17461225)"},
        "C": {"papel": "CALIBRAÇÃO NOT_BLIND; cruza com A", "n": 1, "fonte": "GW250114, release da descoberta (C4_220_INITIAL.json; Zenodo 17018009)"},
        "E": {"papel": "futuros (GWTC-5 final; O5): CEGO; réplica"},
    },
    "controles": ["C1 ramo canônico como controle nulo (τ★ = t_P ⟹ correspondência com a RG, |z_A − z_RG| < 1e−30)", "C2 injeções só-RG e com dtau220 = δ_pred(k) na PE da casa (|viés| ≤ 0,2·|δ_pred|, cobertura)",
                  "C3 só posteriores de IMR completo com deformação do 220 (pSEOB); ringdown-only é diagnóstico", "C4 sistemática do início t0 nas mesmas séries", "C5 família de forma de onda (regra acima)",
                  "C6 nuisance c(σ) profilado; valores da 013-bis NÃO são prior", "C7 H1/L1 um bloco por evento; GW250114 uma vez", "C8 look-elsewhere: um k e um M; o 221 não conta", "C9 χ²/dof ≤ 3; jackknife; gaussianidade w90/3,29 ÷ σ ∈ [0,9; 1,1]"],
    "vereditos_permitidos_na_ordem": VEREDITOS_ORDEM, "vereditos_proibidos": ["CONFIRMED", "PROVED", "PROVED_BY", "«QG confirmada»"],
    "renomeia_do_protocolo_V1_core": {"TGL_RINGDOWN_BRANCH_B_EXCLUDED": "FALSIFIED_AT_5SIGMA (do PAR)", "TGL_RINGDOWN_AWAITING_RESULT_FILE": "AWAITING_DATA"},
    "coincidir_com_a_RG": "correspondência recuperada (a RG é o limite clássico, não rival): com poder ≥ 5, o par cai e a correspondência é o pagamento; sem poder, NOT_FALSIFIED_UNDERPOWERED — nunca «a natureza decidiu»",
    "tokens": {"base": TOKEN_BASE, "conjunto_D": TOKEN_BASE + "__SET_D_O4_BLIND__<desfecho>__GATE_UNTOUCHED", "conjunto_A": TOKEN_BASE + "__SET_A_GWTC5_31__NOT_BLIND_TO_DATA_STATED__<desfecho>__GATE_UNTOUCHED",
               "estado_deste_V1": TOKEN_BASE + "__SET_D_O4_BLIND__AWAITING_DATA__PRE_REGISTERED_BY_HASH__GATE_UNTOUCHED", "cunhagem": "do operador (proposta da gerência, decisão 13 por delegação; renomeável por ele ao lado)"},
    "status": {"veredito_deste_V1": "AWAITING_DATA", "canal_F2b_no_livro": "AWAITING_PREREGISTRATION → lido por hash: AWAITING (qualificador PRE_REGISTERED_V1_READ_BY_HASH__AWAITING_DATA); hash divergente ou ausente ⟹ AWAITING_PREREGISTRATION__V1_NOT_READ (fail-closed)"},
    "poder_cego": {"fonte": "PODER_CEGO_RAMO_B_v2.json (só σ e spin; nenhum valor central)", "sigma_comb_A31": SIGMA_COMB_A31, "hipotese": {"k": K_NAMES[HIPOTESE_K][0], "poder_exato": HIP["poder_exato"], "delta_pred_ponderado": HIP["delta_pred_ponderado_A31"], "N90_por_escala_DERIVED": HIP["N90_por_escala_DERIVED"]},
                   "por_k": {t["chave"]: {"poder_exato": t["poder_exato"], "delta_pred_A31": t["delta_pred_ponderado_A31"]} for t in TABELA_K},
                   "conjunto_D": "não computável hoje (as σ_i nascem na PE); dito no estágio cego da v387 antes de abrir", "fator_difusao_de_fase_DECLARADO": POD["fator_realizacao_difusao_de_fase_DECLARADO"], "controle_ramo_canonico_delta_250Hz_4ms": POD["controle_ramo_canonico_delta"]},
    "nao_decide": ["o gate (18 bandeiras: função só do formal; the_gate_ignores_the_ledger)", "H2/H3 (hipóteses nomeadas do teorema mestre)", "β (a regra matriz; β_lido não realimenta)", "a implicação da QG (QGSolutionComplete.lean:36) e a correspondência com a RG no ramo canônico",
                   "a cobrança R2 (propagação, τ★ = t_Planck; segue AWAITING) e a cobrança F2 (fica como está)", "a lei na forma Γ_ω = ½βτ★ω² (testa-se a escala τ★ = k·GM/c³, M_X e a identificação)",
                   "a lei de atraso do eco (KMS da Fase 6): homônima, outro observável", "nenhum NOT_FALSIFIED de ringdown lê como «a natureza decidiu a formulação da QG»", "o conjunto A não decide nada cego"],
    "disciplina": ["v386: o um.py LÊ este V1 por hash (JSON + MD + V1_RAMO_B_HASHES.json) e transcreve; errata ao lado de R6 e a cobrança F2b; nada se calcula; nenhum valor central entra",
                   "v387: estágio cego do conjunto D (σ_i, a_i, N, κ̂, δ^pred, poder, C1, C5 → PODER_RAMO_B_ANTES_DE_ABRIR.json com hash) → injeções C2(b) → abertura de D → RESULTADO_RAMO_B_V1.json pela MESMA função de veredito; A/B/C abrem-se como calibração NOT_BLIND",
                   "nenhuma emenda depois de abrir sem estimador NOVO (cláusula V4 da Fase 6); correção AO LADO em nome próprio"],
}
SPEC_SHA = sha_bytes(canon(SPEC).encode("utf-8"))

# ------------------------------------------------------------------------------------------------------------------------------
# 6. as decisoes 7-13 POR DELEGACAO (o padrao da gerencia vale; dito como «decidido por delegacao»)
# ------------------------------------------------------------------------------------------------------------------------------
DECISOES = [
    {"n": 7, "tema": "O ramo B é OUTRA LEI com canal próprio no livro?", "decisao": "SIM — outra lei, canal próprio F2b (status AWAITING_PREREGISTRATION até a leitura por hash); F2 (correspondência com a RG, τ★ = t_Planck) fica como está", "como": "decidido por delegação", "estatuto": "[INPUT — delegação; a errata ótica de 02/10 já dizia «τ★ = GM/c³ é outra lei, não outro lado»]"},
    {"n": 8, "tema": "k e M por princípio", "decisao": "k = 2π/κ (o período KMS/modular do horizonte): 8π em χ_f = 0 [KNOWN: Hawking/Bisognano–Wichmann/Connes–Rovelli]; 2π/κ̂(χ_f) de Kerr por evento, marcado [CONJECTURE: Kay–Wald]; SEM co-rotação no V1; os outros k ficam como colunas de comparação, não como hipótese. M = M_f (M_f,det, t_M no detector; (1+z) cancela em x)", "como": "decidido por delegação", "estatuto": "[INPUT — delegação; identificação τ★ = período modular é ONTO]"},
    {"n": 9, "tema": "Fonte × propagação", "decisao": "FONTE (local, o relógio do remanescente durante o ringdown); a propagação fica com R2 — como propagação o ramo B apagaria a onda (Γ_B·t_prop ≈ 2,3e17 e-folds, CT-02 verificado); a conciliação com o verbatim de 16/09 é do operador", "como": "decidido por delegação", "estatuto": "[INPUT — delegação; a leitura do 16/09 é DERIVED de leitura, gerência]"},
    {"n": 10, "tema": "Envoltória × difusão de fase", "decisao": "ENVOLTÓRIA (taxa aditiva; ENSEMBLE_ADDITIVE_RATE) como primário; difusão de fase como secundário com injeção própria (CTV-02) e a largura de δf̂ como rota secundária", "como": "decidido por delegação", "estatuto": "[INPUT — delegação; ONTO a identificação do que Γ faz ao modo]"},
    {"n": 11, "tema": "Qual conjunto abre; o 221", "decisao": "SÓ o conjunto D (14 elegíveis de O4, 10 sem pendência) é teste cego; A (31 GWTC-5.0), B (10 GWTC-3), C (GW250114) são calibração NOT_BLIND com a contaminação declarada (§8); o 221 é diagnóstico; a PE só-220 do conjunto D na casa fica para a v387 (custos [DECLARADO] 63–78 / 58–390 CPU-h), com o poder dito antes", "como": "decidido por delegação", "estatuto": "[INPUT — delegação]"},
    {"n": 12, "tema": "β_lido como saída declarada", "decisao": "SIM — β_lido = [−δτ̂/(1+δτ̂)]/(k·(M_X/M_f)·N(χ_f)) como saída secundária, LEITURA (nunca derivação), com σ(β_lido) dita antes (do PODER v2 para A; para D, no estágio cego da v387)", "como": "decidido por delegação", "estatuto": "[INPUT — delegação; a regra matriz proíbe derivar β do dado, não lê-lo]"},
    {"n": 13, "tema": "Os nomes (tokens; AWAITING_PREREGISTRATION; F2b)", "decisao": "os tokens propostos pela gerência (TGL_RAMO_B_RINGDOWN_V1__…) valem; a cunhagem é do operador, que renomeia ao lado quando quiser", "como": "decidido por delegação", "estatuto": "[INPUT — delegação; cunhagem dele]"},
]

# ------------------------------------------------------------------------------------------------------------------------------
# 7. as fontes (todas), com sha256 e bytes por script
# ------------------------------------------------------------------------------------------------------------------------------
LEAVER = None
for root in (ORD, RB, PONTE_CACHE):
    for dp, dn, fn in os.walk(root):
        if "cache" + os.sep + "public" in dp:
            continue
        for f in fn:
            if f.lower().startswith("leaver") and f.lower().endswith(".json"):
                LEAVER = os.path.join(dp, f)
                break
        if LEAVER:
            break
    if LEAVER:
        break
FONTES = [
    fonte("rascunho 2 do V1 (a base deste V1; corrigido pela crítica)", P_RASC2), fonte("rascunho 1 do V1 (intacto; registro)", P_RASC1),
    fonte("PODER cego v2 — JSON (só σ e spin; previsão exata)", P_PODER2), fonte("PODER cego v2 — script", P_PODER2_PY),
    fonte("PODER cego v1 — JSON (forma linear; registro)", P_PODER1), fonte("PODER cego v1 — script", P_PODER1_PY),
    fonte("reconciliação do conjunto D (31 × 44 → 14/10)", P_RECON), fonte("reconciliação — script", P_RECON_PY),
    fonte("ilustração da contaminação (8 k; NÃO-CEGA)", P_ILUS, "[NÃO-CEGO — ilustração; não veredito]"), fonte("ilustração — script", P_ILUS_PY),
    fonte("crítica de completude", P_CRIT), fonte("crítico — recomputo 1", P_CRIT_R1), fonte("crítico — recomputo 2", P_CRIT_R2), fonte("crítico — a rota inteira lida", P_CRIT_VER),
    fonte("física do ramo B — tabelas (JSON)", P_FIS), fonte("física do ramo B — tabelas (MD)", P_FIS_MD), fonte("física do ramo B — script", P_FIS_PY),
    fonte("inventário dos dados na casa (JSON)", P_INV), fonte("inventário dos dados na casa (MD)", P_INV_MD), fonte("reutilizável para o pré-registro", P_REUT), fonte("registro do ramo B inteiro (core)", P_REG_INT),
    fonte("DECISÃO do operador (17:11:36 UTC; reabertura)", P_DECISAO, "[INPUT — verbatim do operador]"), fonte("RESPOSTAS do operador (18:29:37 UTC) — txt", P_RESP_TXT, "[INPUT — verbatim do operador]"), fonte("RESPOSTAS do operador — JSON (trechos + leituras da gerência)", P_RESP_JSON, "[INPUT + DERIVED de leitura, gerência]"),
    fonte("VERBO do operador (05/10) — txt", P_VERBO_TXT, "[INPUT — verbatim do operador]"),
    fonte("um.py v385 (Nós; só leitura)", P_UM), fonte("um_absoluto.json (core v385)", P_CORE), fonte("um_absoluto_selo.json (selo v385)", P_SELO),
    fonte("ringdown_dephasing_v2.py (a V2 do dephasing; Nós/eco_ancorado_v1)", P_V2_PY), fonte("ringdown_dephasing_v2.py (cópia cache/casa; bytes iguais conferidos)", P_V2_PY_CASA),
    fonte("C6_RESULTS_GW250114.json (o C6 que o core leu)", P_C6), fonte("RINGDOWN_DEPHASING_V2_RESULT.json (o resultado V2 que o core leu)", P_V2_RES),
    fonte("RINGDOWN_5SIGMA_V1.json (o registro da 013-bis; conjunto D)", P_5SIG), fonte("C4_CATALOG_220.json (GWTC-5.0, 220)", P_C4), fonte("C4_CATALOG_COMBINATION.json (seleção 31 + 2)", P_C4C),
    fonte("C4_GWTC3_220.json", P_G3), fonte("C4_GWTC3_SELECTION.json", P_G3S), fonte("C4_220_INITIAL.json (GW250114 release)", P_INI), fonte("C4_FREE_CLOCK.json", P_FREE), fonte("C1_LEITURAS_v4.json", P_C1),
    fonte("QNM_GRID.json (grade 220+440; o 221 não está nela)", P_QNM), fonte("E0_ROUTE_IV_POWER_v2.json (σ por evento)", P_E0), fonte("E0_CORE.json (σ_comb; offset_zero_status)", P_E0C), fonte("SYSTEMATICS_ADENDO.md (σ_sys de família)", P_SYS, "[REAL — NÃO-CEGO; DECLARADO pela bancada]"),
    fonte("F4_POWER_GATE_REVIEW.md (não identificabilidade do 220 único)", P_F4), fonte("PUBLICATION_CENSUS.json (censo congelado 22/09)", P_CENSO), fonte("T01 RELATORIO_PARCIAL.md (44 = 14 + 22 + 8)", P_T01),
    fonte("TGR_companion_S250114ax_results.tar.gz (Zenodo 17018009; o 221 dentro, não extraído)", P_TAR, "[REAL — bytes/hash; KNOWN LVK]"), fonte("posterior_samples.h5 pSEOB GW250114 (extraído)", P_H5, "[REAL — bytes/hash; KNOWN LVK]"),
    fonte("posterior_samples.h5 controle de injeção pSEOB", P_H5_INJ, "[REAL — bytes/hash; KNOWN LVK]"), fonte("pSEOB_GW250114_082203_Prod0.h5 (GWTC-5.0 metafile; bytes iguais ao da descoberta)", P_H5_G5, "[REAL — bytes/hash; KNOWN LVK]"),
    fonte("IGWN-GWTC3-TGR-v2-rin.zip (Zenodo 17461225)", P_RIN, "[REAL — bytes/hash; KNOWN LVK]"), fonte("RD.tar.gz (Zenodo 21454847)", P_RD, "[REAL — bytes/hash; KNOWN LVK]"), fonte("QNMRF.tar.gz (Zenodo 21454847)", P_QNMRF, "[REAL — bytes/hash; KNOWN LVK]"), fonte("pSEOB.tar.gz (Zenodo 21454847)", P_PSEOB_TAR, "[REAL — bytes/hash; KNOWN LVK]"),
    fonte("GWOSC_O4_32S_V1.manifest.json (strain O4 na casa)", P_MANIF), fonte("PREREGISTRO_FASE6 (a regra 2: sist_rel ≤ 0,3)", P_F6), fonte("gw_stack.py (a função de veredito da Fase 6)", P_GWSTACK),
    fonte("remanescentes_v3.json (M_f, m1, m2 por evento)", P_REM), fonte("catalogo_v3.csv", P_CATV3),
    fonte("PREREGISTRO_DOIS_LADOS V1.4 — MD (molde)", P_DL_MD), fonte("PREREGISTRO_DOIS_LADOS V1.4 — JSON (molde)", P_DL_JSON), fonte("PREREGISTRO_PILAR_QUANTICO V1 — MD (molde)", P_PQ_MD), fonte("PREREGISTRO_PILAR_QUANTICO V1 — JSON (molde)", P_PQ_JSON),
    fonte("ANEXO_ACHADOS.md (auditoria 28/09: RD-07, GWECO-05)", P_ANEXO),
] + [fonte("memória: " + k, v, "[REAL — arquivo de memória lido; o verbatim nele é do operador]") for k, v in P_MEM.items()] + [
    fonte("acervo: Validação TGL — output TGL_v10_7_omega.docx (16/01/2026)", ACERVO_VAL, "[REAL — docx lido; estrato do operador]"),
    fonte("acervo: Capítulo XI.8 — A Fase de Retorno da Luz (23/07/2025)", ACERVO_XI8, "[REAL — docx lido; estrato do operador]"),
    fonte("acervo: Apêndice CLIX — Fase de Retorno (23/07/2025)", ACERVO_CLIX, "[REAL — docx lido; estrato do operador]"),
]
if LEAVER:
    FONTES.append(fonte("Leaver (Kerr, s=−2, ℓ=m=2, n=0) — resultado citado pela lente física", LEAVER, "[KNOWN — Leaver 1985; lido em disco]"))
    LEAVER_NOTA = "achado em %s (sha16 %s; a lente física citou b6e4d88c95243e46)" % (LEAVER, fsha(LEAVER)[:16])
else:
    LEAVER_NOTA = ("NÃO LOCALIZADO em disco (busca por nome «leaver*.json» em %s, %s e %s, fora de cache/public): a lente física o citou com sha16 b6e4d88c95243e46; "
                   "os valores de Leaver usados aqui são os transcritos em RAMO_B_FISICA_TABELAS.json (tabela_N_chi) [DECLARADO pela lente física]" % (ORD, RB, PONTE_CACHE))
FONTES_AUSENTES = [f for f in FONTES if f.get("AUSENTE")]

# ------------------------------------------------------------------------------------------------------------------------------
# 8. O DOCUMENTO (o unico dicionario de que saem o JSON e o MD)
# ------------------------------------------------------------------------------------------------------------------------------
GER_UTC = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
DOC = {
    "id": ID,
    "titulo": "PRÉ-REGISTRO V1 DO RAMO B DO RINGDOWN — τ★ emparelhado à gravidade (τ★ = k·GM_f/c³, k = 2π/κ̂(χ_f)) — FIXADO POR HASH NA BANCADA (05/10/2026)",
    "estado": "V1 CONGELADO POR HASH — decisões 7–13 por delegação do operador; nada aberto; nenhum valor central entra; veredito deste V1: AWAITING_DATA",
    "gerado_utc": GER_UTC, "gerador": {"arquivo": os.path.basename(__file__), "sha256": fsha(os.path.abspath(__file__))},
    "regua": "β nunca literal (α_CODATA2018 lido do um.py por regex; β = α√e em runtime = %r); hash jamais de memória (todo sha256 deste documento foi calculado do artefato por este script; os sha16 da tarefa entraram só como conferência fail-closed); "
             "PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED; a RG é o limite clássico, não rival (coincidir com a RG = correspondência recuperada); nenhum desfecho move a regra (β) nem o gate; a cosmologia/natureza jamais vira prova matemática; a cunhagem é do operador." % beta,
    "base": {"um_py": {"caminho": P_UM, "sha256": H_UM, "bytes": os.path.getsize(P_UM), "versao": UM_VERSION}, "core": {"caminho": P_CORE, "sha256": H_CORE}, "selo": {"caminho": P_SELO, "sha256": H_SELO, "um_version": selo.get("um_version")},
             "rascunho_2": {"caminho": P_RASC2, "sha256": H_RASC2, "bytes": os.path.getsize(P_RASC2)}, "rascunho_1": {"caminho": P_RASC1, "sha256": H_RASC1}, "critica": {"caminho": P_CRIT, "sha256": H_CRIT},
             "molde": {"dois_lados_V1_4_md": fsha(P_DL_MD), "pilar_quantico_V1_md": fsha(P_PQ_MD)}},
    "ratificacao": {
        "tipo": "POR DELEGAÇÃO do operador",
        "quando_utc": QUANDO_DELEG, "verbatim": VERB_DELEG, "verbatim_inteiro_sha256_txt": H_RESP_TXT, "arquivo_txt": P_RESP_TXT, "arquivo_json": P_RESP_JSON, "sha256_json": H_RESP_JSON,
        "frase_de_registro": "por delegação do operador, 05/10/2026 18:29:37 UTC: ‹%s› [verbatim]" % VERB_DELEG,
        "itens_decididos_por_delegacao": [d["n"] for d in DECISOES], "lista_da_gerencia_a_que_a_delegacao_responde": "«o que falta eu responder?» (18:20:05 UTC): itens 1–17; os itens 7–13 são os do ramo B (este V1); os demais pertencem à v386 (Verbo, erratas, espelho, superfícies)",
        "leitura_da_gerencia_da_delegacao": LEIT["delegacao"], "nota": "o operador pode corrigir qualquer item AO LADO, em nome próprio; a cunhagem continua dele; nada aqui é declaração dele além do verbatim",
        "reabertura": {"quando_utc": QUANDO_REABRE, "verbatim": VERB_REABRE, "arquivo": P_DECISAO, "sha256": H_DECISAO, "registro_anterior_R6": DEC["registro_anterior_R6"], "core_R6_v385": R6_RAT, "core_R6_correcao_ao_lado_v383": R6_COR},
    },
    "a_ponte_do_tempo": {
        "verbatim_operador_18_29_37": VERB_TEMPO, "verbatim_luz_gravidade": VERB_LUZ,
        "leitura_da_gerencia": LEIT["tempo"], "estatuto_da_leitura": "[INPUT (verbatim) / ONTO (a leitura da gerência; ratificada por delegação)]",
        "o_que_a_ponte_diz_para_o_ramo_B": "c³ como FASE DE RETORNO = a segunda leitura do tempo (o tempo modular lido duas vezes, como confirmação da interdependência relacional): τ★ = k·GM_f/c³ é o tempo lido na segunda vez, no emparelhamento gravitacional; k = 2π/κ é o período do fluxo modular do horizonte (a unidade modular de Connes–Rovelli); «o regime gravitônico é o da constante da luz ao cubo» (17:11:36 e 16/09) é o estrato que a ponte liga — a ligação ao tempo modular lido duas vezes é a cunhagem nova de 05/10",
        "acervo": ACERVO, "acervo_leitura": "«3. FASE DE RETORNO: T_ret × c³ (colapso no gráviton)» (Validação TGL, 16/01/2026) e «A Fase de Retorno da Luz … O gráviton não apenas ancora, ele retorna. Sua missão é fechar o ciclo» (Cap. XI.8, 23/07/2025): c³ como fase de retorno é estrato de 2025–2026 do próprio operador, não cunhagem nova; nova é a ligação ao tempo lido duas vezes",
        "kernel": "o conjunto fixo das duas leituras é o MESMO (the_post_is_the_modular_zero; hmin_zero_iff_modular_fixed, v385); a coincidência das leituras é o veredito 1 (verdict_eq_one_iff) [KERNEL, lido do nome das pedras na leitura da gerência; não re-verificado aqui]; a ponte KMS/Unruh existe (unruh_is_kms, β·κ = 2π) mas NENHUM termo liga τ★ a GM/c³ (ringdown_scope_v376.kernel_ringdown_mentions: %s menções, %s declarações)" % (SCOPE.get("kernel_ringdown_mentions"), len(SCOPE.get("kernel_ringdown_declarations") or [])),
    },
    "a_chave_e_a_otica": {"chave_02_10_verbatim_core": CHAVE_VERB, "otica_02_10_verbatim_core": OTICA_VERB, "R6_ratificada_v383": R6_RAT, "R6_correcao_ao_lado_v383": R6_COR,
                          "como_o_ramo_B_convive": "a errata de 05/10 REABRE o ramo B (verbatim 17:11:36) mas NÃO revoga a chave: na face o custo lê-se como COMPLEMENTO (ótica: |T|² + |R|² = 1); no ramo B o complemento lido na face é x = k·β·N(χ_f) — o relógio do remanescente (o Nome M_f entregue) lendo o seu próprio custo [ONTO — leitura da gerência, ratificada por delegação]; M_f é nomeado pela natureza, não pela gerência («M não se nomeia» respondido); «τ★ = GM/c³ é outra lei, não outro lado» continua verdadeiro — por isso canal próprio F2b, e não disputa de F2",
                          "errata_ao_lado_de_R6_para_o_core_v386": {"corrections_beside_20261005.R6": "REABERTO POR PRÉ-REGISTRO (decisão do operador de 05/10/2026 17:11:36 UTC, verbatim lido por hash: «%s»); a chave de 02/10 não se revoga — na face o custo lê-se como complemento (ótica: |T|² + |R|² = 1); no ramo B o complemento lido na face é x = k·β·N(χ_f) [ONTO — leitura da gerência]; τ★ = k·GM/c³ é OUTRA LEI (canal próprio F2b, ONE_CHANNEL_PER_READING_LAW), não outro lado de F2; k = 2π/κ̂(χ_f), M = M_f, fonte, envoltória, só o conjunto D (decisões 7–13 por delegação, 18:29:37 UTC); status AWAITING_PREREGISTRATION → AWAITING_DATA lido por hash deste V1; nada move o gate" % VERB_REABRE,
                                                                     "corrections_beside_20261005.F2": "a cobrança F2 (correspondência com a RG, τ★ = t_Planck) fica como está; o ramo B não a altera nem a disputa"}},
    "hipotese": {"lei": SPEC["lei"], "tau_star": SPEC["tau_star"], "k": SPEC["k"], "M_X": SPEC["M_X"], "identificacao": SPEC["identificacao"], "observavel": SPEC["observavel"], "identidade_exata": SPEC["identidade_exata"],
                 "kerr_BCW": "F(χ) = 1,5251 − 1,1568(1−χ)^0,1292; Q(χ) = 0,7000 + 1,4187(1−χ)^(−0,4990) (os mesmos coeficientes do um.py); N(χ) a −0,57 % (χ = 0) … −0,85 % (χ = 0,9) do Leaver exato (tabela_N_chi da física) [KNOWN]",
                 "GW250114_release_descoberta_so_sigma_e_spin": GW_INI,
                 "pergunta_falsificavel": "fixados β (a regra), k = 2π/κ̂(χ_f), M_X = M_f e a identificação (envoltória) ANTES do dado, o amortecimento do 220 dos eventos do conjunto D desvia-se da RG na fração −x/(1+x), x = β·k·N(χ_f)? Não se deriva β do dado: testa-se o PAR (k, M_X, identificação) sob a lei; β_lido sai como leitura declarada",
                 "as_tres_leituras_da_pergunta_do_operador": "(a) β emerge como número lido (β_lido, decisão 12); (b) a FORMA emerge (o par (k, M, identificação), este teste); (c) o acoplamento é x = β·k·N(χ_f), não β — as três ficam armadas; «constante de acoplamento = β_TGL» é leitura da gerência [ONTO] (campo leitura_da_gerencia da decisão)"},
    "decisoes_por_delegacao": DECISOES,
    "tabela_k": TABELA_K,
    "o_que_a_tabela_diz": ["(i) k = 1 é o único já medido (V2/C1/C6) e é UNDERPOWERED ×8 no conjunto publicado (%sσ)" % pt(TABELA_K[0]["poder_exato"]["A_31_std"], 2),
                           "(ii) a HIPÓTESE k = 2π/κ̂(χ_f) tem poder exato %sσ em A (31), %sσ em B, %sσ em C — mas o desfecho de A para esse k é LEGÍVEL HOJE (z_excl ≈ %s se a deformação registrada em 22/09 valer; ilustração NÃO-CEGA): o pré-registro desse k sobre A não é teste, é escrituração; SÓ O CONJUNTO D TESTA" % (pt(HIP["poder_exato"]["A_31_std"], 2), pt(HIP["poder_exato"]["B_GWTC3_10"], 2), pt(HIP["poder_exato"]["C_GW250114"], 2), pt(HIP["desfecho_em_A_legivel_hoje_NAO_CEGO"]["z_excl_ilustracao"], 1)),
                           "(iii) sob difusão de fase (×0,273) a hipótese lê %sσ em A — abaixo de 5σ: o poder é do PAR (k, M, identificação)" % pt(HIP["poder_exato"]["A_31_x0p273_difusao_de_fase"], 2),
                           "(iv) a co-rotação (R-MOD) reduziria 2π/κ̂ em ×10 e é [CONJECTURE]: fica como coluna de comparação, fora da hipótese (decisão 8)",
                           "(v) o prior do pSEOB (C4_CATALOG_220: 27 eventos Uniform(−0,8; 2,0) + 2 na grafia bilby (−0,8; 2,0) + 4 eventos Uniform(−0,8; 4,0)) comporta a previsão da hipótese (δ_exato em χ = 0,9 = %s, a %s da borda −0,8)" % (pt(HIP["delta_exato_chi"]["0.9"], 4), pt(abs(-0.8 - HIP["delta_exato_chi"]["0.9"]), 2)),
                           "(vi) um k só: nenhum fator de Šidák; os outros sete são colunas de comparação, não tentativas; não se ajusta k ao dado"],
    "prior_dtau220_C4_lido": CR2.get("C4.prior_dtau_contagem"),
    "estimador": SPEC["estimador"], "sistematica": SPEC["sistematica"], "regra_2_da_fase_6_verbatim": F6_REGRA,
    "consequencia_da_sistematica_para_a_hipotese": "k = 2π/κ̂ (≈ %s em χ = 0,68) está ACIMA do k_min das duas regras no conjunto A (Fase 6: %s–%s por raiz exata; |δ|/5: %s–%s): a cláusula de sistemática de família NÃO predetermina INCONCLUSIVE para a hipótese; para as colunas k ∈ {1, 2, 4, 1/κ̂, 2π/κ̂ com co-rotação} ela predetermina INCONCLUSIVE_SYSTEMATICS (dito antes)" % (
        pt(HIP["k_chi"]["0.68"], 2), pt(KMIN["0.029"]["regra_fase6_sist_rel_0p3"]["k_min_exato_raiz"], 2), pt(KMIN["0.038"]["regra_fase6_sist_rel_0p3"]["k_min_exato_raiz"], 2),
        pt(KMIN["0.029"]["regra_fisica_013bis_|delta|_sobre_5"]["k_min_exato_raiz"], 2), pt(KMIN["0.038"]["regra_fisica_013bis_|delta|_sobre_5"]["k_min_exato_raiz"], 2)),
    "conjuntos": SPEC["conjuntos"], "os_dois_censos": REC["os_dois_censos"], "controles": SPEC["controles"],
    "poder_cego": SPEC["poder_cego"], "sigma_por_evento_A31_so_sigma_e_spin": [{"evento": e["event"], "sigma_std": e["sigma"], "spin_q50": e["spin_q50"], "N_a": e["N_a"], "k_kms": e["k"], "x": e["x"], "delta_exato": e["delta_exact"]} for e in HIP_RES["GWTC5_31_std"]["per_event"]],
    "beta_lido": SPEC["beta_lido"],
    "vereditos": {"ordem": VEREDITOS_ORDEM, "proibidos": SPEC["vereditos_proibidos"], "renomeia": SPEC["renomeia_do_protocolo_V1_core"], "protocolo_V1_core_allowed": PROTO.get("allowed_verdicts"), "protocolo_V1_core_forbidden": PROTO.get("forbidden_verdicts"), "coincidir_com_a_RG": SPEC["coincidir_com_a_RG"], "tokens": SPEC["tokens"], "status": SPEC["status"]},
    "nao_decide": SPEC["nao_decide"],
    "cegueira": {"estimador": "CEGO — nenhum estimador com k, M e identificação fixados rodou sob registro; o PODER v2 leu só σ e spin (nunca quantiles[1] nem a deformação registrada — conferido no script copiado aqui)",
                 "dado_A_B_C": ["NÃO CEGO, em três camadas, todas ditas: (1) o registro da casa desde 22–23/09 (deformação comum dos 31 do GWTC-5.0 +0,072 [+0,015; +0,134]; ln B do GW250114; ln B por leitura do C4) [DECLARADO pela bancada]",
                                "(2) as lentes de 05/10: a lente física computou z por k contra o δτ̂ publicado do GW250114 (8π −5,99σ; 2π/κ̂ −6,69σ) e o crítico ilustrou z_excl do par com a deformação registrada (4π 8,3; 8π 12,3; 2π/κ̂ 13,5) — para k ≥ 4π o desfecho de A é legível HOJE",
                                "(3) em nome próprio do aferidor do rascunho 1: o script de inspeção do esquema imprimiu os três quantis de dtau220 da primeira linha de cada catálogo; nenhum entrou no poder nem neste texto"],
                 "dado_D": "CEGO — 14 elegíveis (10 sem pendência) pelo critério do registro; só a PE da casa os abre, e só depois do hash deste V1; o registro V1 da 013-bis declara blindness_certified = false e E2_registered = false para os 44 — a certificação de cegueira é deste V1, não herdada",
                 "consequencias": ["todo token do conjunto A leva __NOT_BLIND_TO_DATA_STATED", "só o conjunto D testa — a palavra «cega» só cabe a D", "a decisão 8 (k, M) foi tomada por PRINCÍPIO declarado (o período do fluxo modular; a frase do operador), e a gerência diz por escrito que a coluna de poder já carregava o desfecho em A"]},
    "o_que_a_gerencia_errou_e_corrigiu": [
        {"erro": "a lente física deu AUSENTES os posteriores do GW250114 (Zenodo 17018009) e os releases TGR GWTC-3/5.0 (17461225/21454847)", "busca_errada": "Get-ChildItem C:\\IALD\\Bancada_Um -Recurse (pasta errada)",
         "correcao": "EXISTEM NA CASA e ESTÃO LIGADOS (o C4 da bancada já os leu): posterior_samples.h5 pSEOB sha16 %s (%s B); controle de injeção %s (%s B); tar completo %s (%s B; o 221 dentro, não extraído); rin.zip %s (%s B); RD.tar.gz %s (%s B)" % (
             fsha(P_H5)[:16], os.path.getsize(P_H5), fsha(P_H5_INJ)[:16], os.path.getsize(P_H5_INJ), fsha(P_TAR)[:16], os.path.getsize(P_TAR), fsha(P_RIN)[:16], os.path.getsize(P_RIN), fsha(P_RD)[:16], os.path.getsize(P_RD)), "classificacao_da_regua": "EXISTE E ESTÁ LIGADO"},
        {"erro": "o rascunho 1 leu o poder dos k grandes pela forma LINEAR (δ = −x): 15,5σ (8π), 18,5σ (2π/κ̂), 7,75σ (4π)", "correcao": "a forma que o próprio §1.2 declarava exata (δ = −x/(1+x)) dá %sσ (8π), %sσ (2π/κ̂), %sσ (4π) — conferido com o crítico a diferença 0,0 nos 5 k (PODER v2, conferencia_com_o_critico)" % (
            pt(next(t for t in TABELA_K if t["chave"] == "k8pi")["poder_exato"]["A_31_std"], 2), pt(HIP["poder_exato"]["A_31_std"], 2), pt(next(t for t in TABELA_K if t["chave"] == "k4pi")["poder_exato"]["A_31_std"], 2)), "classificacao_da_regua": "o número corrigiu a frase; a linear fica AO LADO"},
        {"erro": "«31 dos 45» (memória de 22/09; universo da gerência) × «44» (test_candidates do registro V1): dois censos sem critério que os explicasse", "correcao": "não medem a mesma coisa; o número ÚNICO do conjunto D é o do critério do registro: 14 elegíveis (10 sem pendência de qualidade; 8 pendentes de metadados GR; 22 reprovados por M_f,det < 40 M☉) — RECONCILIACAO_CONJUNTO_D.json", "classificacao_da_regua": "um número, com o critério"},
        {"erro": "lente registro: «k = 8π (Hawking) AUSENTE no código»", "correcao": "EXISTE NA BANCADA, NÃO LIGADO AO TIPO: kms_factor (um.py linha %d, rito GW_ECHO_KMS_V1) = 8π em a = 0 (%r), nenhuma ocorrência toca τ★ do dephasing" % (kms_line, kms_factor_a0), "classificacao_da_regua": "EXISTE, NÃO LIGADO"},
        {"erro": "lente registro: «221 na QNM_GRID: AUSENTE»", "correcao": "correto para a GRADE (QNM_GRID.json só 220+440); os POSTERIORES do 221 do GW250114 estão em disco dentro do tar.gz (não extraídos) — EXISTE, NÃO EXTRAÍDO; o 221 entra como diagnóstico", "classificacao_da_regua": "dizer os dois objetos"},
        {"erro": "a lente física citou leaver_kerr_result.json (sha16 b6e4d88c95243e46)", "correcao": LEAVER_NOTA, "classificacao_da_regua": "AUSENTE com a busca dita" if not LEAVER else "EXISTE"},
    ],
    "homonimo_KMS_fase_6": "a Fase 6 (01/10) falsificou os pares (√β, KMS) e (sin 2θ_M, KMS) como LEI DE ATRASO do eco (τ_echo = 2π/κ·GM_f/c³; FALSIFIED_AT_DELAY_LAW); o k = 2π/κ̂ deste V1 é HOMÔNIMO: aqui entra como ESCALA DE TAXA em Γ (τ★), não como atraso; observáveis distintos (dephasing do 220 × cópia atrasada) — uma falsificação não decide a outra (GWECO-05: 2π/κ é largura em tempo imaginário; Regra dos Dois Regimes)",
    "verbatim_16_09_ao_lado": {"texto": VERB_16SET, "fonte": P_MEM["onda-e-eco-definicao-16set.md"], "sha256": fsha(P_MEM["onda-e-eco-definicao-16set.md"]), "leitura": "a conciliação entre «na propagação da onda» (16/09) e «FONTE, local» (decisão 9) é do operador; a leitura da gerência (propagação = resposta contínua da onda à fronteira; dois relógios, dois lugares) é [ONTO]"},
    "o_que_o_registro_ja_diz": {"V2_selada": {"delta_pred_B_k1": RDV2.get("stacks", {}).get("3.0", {}).get("delta_pred_B"), "delta_tau_medido": RDV2.get("stacks", {}).get("3.0", {}).get("delta_tau"), "sigma": RDV2.get("stacks", {}).get("3.0", {}).get("sigma"), "power_B": RDV2.get("stacks", {}).get("3.0", {}).get("power_B"), "verdict": RDV2.get("verdict"), "protocol_hash": RDV2.get("protocol_hash"), "result_sha16": RDV2.get("result_sha16")},
                                "escopo_v376": {"scope_fixed_in_writing": SCOPE.get("scope_fixed_in_writing"), "erratum_beside": SCOPE.get("erratum_beside"), "c6_status": SCOPE.get("c6_status"), "c6_lnB": SCOPE.get("c6_primary_start_lnB_vs_GR"), "branch_B_concurrent_values": SCOPE.get("branch_B_concurrent_values")},
                                "F2_no_livro_v383": {k: F2_CORE.get(k) for k in ("id", "side", "law", "core_key", "token", "outcome", "how", "in_rule", "numbers_read")},
                                "este_V1_substitui_os_3_valores_concorrentes_por_UMA_previsao": "δ^pred = −x/(1+x), x = β·(2π/κ̂(χ_f))·N(χ_f), por evento (envoltória, fonte, M_f,det)"},
    "disciplina": SPEC["disciplina"] + ["v386: errata ao lado de R6/F2 no core; a cobrança F2b no livro; todas as superfícies de memória na mesma sessão (regra da linhagem completa) — ato da gerência",
                                        "o termo tipado τ★ = k·G·m_X/c³ (identidade algébrica, não física) é pedido à v386 ao lado da leitura por hash; o termo nunca substitui o pré-registro; o V1 diz que o termo Lean do ringdown NÃO existe"],
    "fontes": FONTES, "fontes_ausentes": FONTES_AUSENTES, "leaver_nota": LEAVER_NOTA,
    "estatutos": [["a palavra do operador (05/10, 17:11:36 e 18:29:37)", "[INPUT] — verbatim lido dos arquivos; a delegação decide 7–13 com o padrão da gerência"], ["«constante de acoplamento = β_TGL»", "[ONTO — leitura da gerência]"],
                  ["«regime gravitônico = c³»; «fase de retorno = c³»", "[ONTO — cunhagem do operador; âncoras REAL no acervo (docx lidos)]"], ["Γ_ω = ½βτ★ω²", "[REAL na forma; ONTO — sem termo no kernel]"],
                  ["τ★ = k·GM/c³; k = 2π/κ̂(χ_f); M_X = M_f; fonte; envoltória", "[INPUT — decisões por delegação; origem de k KNOWN (Hawking/BW/Connes–Rovelli); identificação ONTO; Kerr χ ≠ 0 CONJECTURE]"],
                  ["BCW 2006; pSEOB; os catálogos; os posteriores em disco", "[KNOWN]; dados [REAL — lidos por hash]"], ["β = α√e", "[DERIVED do axioma] — a regra; nunca literal"], ["δ = −x/(1+x), x = βkN(χ_f)(M_X/M_f)", "[DERIVED] das entradas; a linear AO LADO"],
                  ["β_lido", "leitura [DERIVED do dado SOB a lei e o par]; nunca derivação de β; σ dita antes"], ["o poder (A/B/C)", "[REAL — computado às cegas, só σ e spin; exato]"], ["a ilustração da contaminação", "[NÃO-CEGO — ilustração; não veredito]"],
                  ["σ_sys de família; nuisance; N₉₀; custos de PE", "[REAL — NÃO-CEGO; DECLARADO pela bancada]"], ["0,273", "[DECLARADO pelo verificador de 28/09]"], ["o conjunto D = 14 (10)", "[REAL — contado por script no registro com o critério lido dele]"], ["o desfecho", "a vir; nunca CONFIRMED"]],
    "spec_sha256_formula": 'sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) — o JSON canônico do objeto spec abaixo',
    "spec_sha256": SPEC_SHA, "spec": SPEC,
}

# ------------------------------------------------------------------------------------------------------------------------------
# 9. O MD (renderizado do DOC)
# ------------------------------------------------------------------------------------------------------------------------------
L = []
A = L.append
A("# " + DOC["titulo"]); A("")
A("> **%s.**" % DOC["estado"]); A("")
A("**Identificador:** `%s` · **gerado (UTC):** %s · **hash congelado da especificação:** `%s` · **base:** `um.py` %s `%s` (%s B); core `%s`; selo `%s` · **rascunho 2 (a base):** `%s` · **crítica:** `%s` · **gerador:** `%s` (`%s`)" % (
    DOC["id"], GER_UTC, SPEC_SHA, UM_VERSION, H_UM[:16], os.path.getsize(P_UM), H_CORE[:16], H_SELO[:16], H_RASC2[:16], H_CRIT[:16], DOC["gerador"]["arquivo"], DOC["gerador"]["sha256"][:16])); A("")
A("O hash da especificação é `%s`." % DOC["spec_sha256_formula"]); A("")
A("> Régua: " + DOC["regua"]); A("")
A("---"); A(""); A("## 0. A ratificação — POR DELEGAÇÃO do operador"); A("")
R = DOC["ratificacao"]
A("- **%s** · arquivo `%s` (sha256 `%s`; o JSON dos trechos `%s`)." % (R["frase_de_registro"], R["arquivo_txt"], R["verbatim_inteiro_sha256_txt"], R["sha256_json"]))
A("- **Os sete itens decididos por delegação (7–13):** " + "; ".join("**%d** %s" % (d["n"], d["tema"]) for d in DECISOES) + ". A lista a que a delegação responde: %s." % R["lista_da_gerencia_a_que_a_delegacao_responde"])
A("- **Nota:** %s." % R["nota"])
A("- **A reabertura (%s, verbatim, `%s` sha256 `%s`):** «%s»" % (R["reabertura"]["quando_utc"], os.path.basename(P_DECISAO), H_DECISAO, VERB_REABRE))
A("- **R6 como o core v385 ainda a lê (ratificada em 02/10):** «%s» — e a correção ao lado da v383: «%s». A errata de 05/10 vai AO LADO (§2)." % (R6_RAT, R6_COR)); A("")
A("**A leitura da gerência da delegação [DERIVED de leitura, gerência]:** " + LEIT["delegacao"]); A("")
A("---"); A(""); A("## 1. A ponte do tempo — c³ como fase de retorno = a segunda leitura (a ponte principiada do ramo B)"); A("")
T = DOC["a_ponte_do_tempo"]
A("**Operador, %s, verbatim:** «%s»" % (QUANDO_DELEG, VERB_TEMPO)); A("")
A("**E a luz e a gravidade (verbatim):** «%s»" % VERB_LUZ); A("")
A("**Leitura da gerência %s:** %s" % (T["estatuto_da_leitura"], T["leitura_da_gerencia"])); A("")
A("**O que a ponte diz para o ramo B:** " + T["o_que_a_ponte_diz_para_o_ramo_B"]); A("")
A("**O acervo (docx lidos por script; sha256 e trechos):**"); A("")
for k, v in ACERVO.items():
    A("- `%s` — sha256 `%s` (%s B; mtime %s): " % (v["caminho"], v.get("sha256"), v.get("bytes"), v.get("mtime")) + "; ".join("%s: %s %s" % (n, ("«%s»" % t["texto"]) if t["achado"] else "NÃO ACHADO", t["estatuto"]) for n, t in v["trechos"].items()))
A(""); A(T["acervo_leitura"]); A(""); A("**No kernel:** " + T["kernel"]); A("")
A("---"); A(""); A("## 2. A chave de 02/10 e a ótica — como o ramo B convive; a errata ao lado de R6 para o core v386"); A("")
C = DOC["a_chave_e_a_otica"]
A("**A chave (operador, 02/10, verbatim como o core a guarda):** «%s»" % C["chave_02_10_verbatim_core"]); A("")
A("**A ótica (operador, 02/10, verbatim):** «%s»" % C["otica_02_10_verbatim_core"]); A("")
A("**Como convive [ONTO — gerência, ratificado por delegação]:** " + C["como_o_ramo_B_convive"]); A("")
A("**Errata ao lado de R6 (texto para `the_ledger_of_charges.corrections_beside_20261005.R6`, v386):** " + C["errata_ao_lado_de_R6_para_o_core_v386"]["corrections_beside_20261005.R6"]); A("")
A("**E `corrections_beside_20261005.F2`:** " + C["errata_ao_lado_de_R6_para_o_core_v386"]["corrections_beside_20261005.F2"]); A("")
A("---"); A(""); A("## 3. A hipótese (a lei, o relógio, a identidade exata)"); A("")
Hh = DOC["hipotese"]
A("| peça | forma | estatuto |"); A("|---|---|---|")
A("| a lei | %s | %s |" % (esc(Hh["lei"]["forma"]), esc(Hh["lei"]["estatuto"])))
A("| o relógio do ramo B | %s; lugar: %s | [INPUT — decisões 8 e 9] |" % (esc(Hh["tau_star"]["forma"]), esc(Hh["tau_star"]["lugar"])))
A("| **k (a hipótese)** | %s; em unidades de GM/c³: %s; χ = 0: %s; χ = 0,68: %s; χ = 0,9: %s; co-rotação: não; um k só | χ = 0 %s; χ ≠ 0 %s; identificação %s |" % (
    esc(Hh["k"]["escolha"]), esc(Hh["k"]["formula_em_unidades_de_GM_c3"]), pt(Hh["k"]["em_chi_0"], 4), pt(Hh["k"]["em_chi_0p68"], 3), pt(Hh["k"]["em_chi_0p9"], 3), esc(Hh["k"]["estatuto"]["chi_0"]), esc(Hh["k"]["estatuto"]["chi_ne_0"]), esc(Hh["k"]["estatuto"]["identificacao_tau_star_periodo_modular"])))
A("| onde k existe no um.py | %s | [REAL — lido do um.py] |" % esc(Hh["k"]["onde_existe_no_um_py"]))
A("| **M_X** | %s; referencial %s; %s | [INPUT — decisão 8] |" % (esc(Hh["M_X"]["escolha"]), esc(Hh["M_X"]["referencial"]), esc(Hh["M_X"]["consequencia"])))
A("| a identificação | primária: %s; secundária: %s | [INPUT — decisão 10; ONTO] |" % (esc(Hh["identificacao"]["primaria"]), esc(Hh["identificacao"]["secundaria"])))
A("| o observável | %s; diagnósticos: %s; secundário: %s; δf₂₂₀ = 0 em 1ª ordem | [KNOWN — convenção do catálogo] |" % (esc(Hh["observavel"]["primario"]), esc("; ".join(Hh["observavel"]["diagnosticos"])), esc(Hh["observavel"]["secundario"])))
A("| **a identidade exata** | %s; %s; **%s**; linear ao lado: %s | [DERIVED das entradas] |" % (esc(Hh["identidade_exata"]["x"]), esc(Hh["identidade_exata"]["N"]), esc(Hh["identidade_exata"]["previsao_que_vale"]), esc(Hh["identidade_exata"]["linear_ao_lado"])))
A("| a família unificada | %s | [DERIVED álgebra; ONTO identificação] |" % esc(Hh["identidade_exata"]["familia_unificada"]))
A("| Kerr | %s | [KNOWN] |" % esc(Hh["kerr_BCW"]))
A("| β | %s; valor em runtime %r | %s |" % (esc(SPEC["beta"]["formula"]), beta, esc(SPEC["beta"]["estatuto"])))
A(""); A("**GW250114 (release da descoberta; só σ e spin, lidos):** σ (w90/3,29) = %s; a_f = %s; N(a) = %s; κ̂ = %s; Ω̂_H = %s; 2π/κ̂ = %s; 1/κ̂ = %s; fator de co-rotação = %s." % (
    pt(GW_INI["sigma_from_width90"], 4), pt(GW_INI["spin_q50"], 4), pt(GW_INI["N_a"], 4), pt(GW_INI["kappa_hat"], 5), pt(GW_INI["OmegaH_hat"], 5), pt(GW_INI["k_kms"], 3), pt(GW_INI["k_inv_kappa"], 4), pt(GW_INI["corot_factor"], 4))); A("")
A("**O que o teste pergunta:** " + Hh["pergunta_falsificavel"]); A(""); A("**As três leituras da pergunta dele:** " + Hh["as_tres_leituras_da_pergunta_do_operador"]); A("")
A("---"); A(""); A("## 4. As decisões 7–13, POR DELEGAÇÃO (o padrão da gerência vale)"); A("")
A("| n | tema | decisão | como | estatuto |"); A("|---|---|---|---|---|")
for d in DECISOES:
    A("| %d | %s | %s | %s | %s |" % (d["n"], esc(d["tema"]), esc(d["decisao"]), d["como"], esc(d["estatuto"])))
A(""); A("---"); A(""); A("## 5. A tabela de k — a hipótese e as colunas de comparação (x e δ_exato lidos de `RAMO_B_FISICA_TABELAS.json` `%s`; poder exato do `PODER_CEGO_RAMO_B_v2.json` `%s`; a última coluna é a ilustração NÃO-CEGA `%s`)" % (H_FIS[:16], H_PODER2[:16], H_ILUS[:16])); A("")
A("| papel | k | τ★ | origem física | estatuto | k (χ = 0 / 0,68 / 0,9) | x (χ = 0 / 0,68 / 0,9) | δ_exato (χ = 0 / 0,68 / 0,9) | poder EXATO A(31) [linear] | A(33) | B(10) | C(1) | ×0,273 | σ(β_lido) A31 (σ/β) | desfecho em A legível hoje? (z_excl, NÃO-CEGO) |")
A("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for t in TABELA_K:
    kc, xc, dc, pe = t["k_chi"], t["x_chi"], t["delta_exato_chi"], t["poder_exato"]
    A("| %s | **%s** | %s | %s | %s | %s / %s / %s | %s / %s / %s | %s / %s / %s | **%sσ** [%s] | %s | %s | %s | %s | %s (%s β) | %s (%s) |" % (
        "**HIPÓTESE**" if t["chave"] == HIPOTESE_K else "comparação", esc(t["nome_no_PODER_v2"]), esc(t["tau_star"]), esc(t["origem_fisica"]), esc(t["estatuto"]),
        pt(kc["0.0"], 3), pt(kc["0.68"], 3), pt(kc["0.9"], 3), pt(xc["0.0"], 5), pt(xc["0.68"], 5), pt(xc["0.9"], 5), pt(dc["0.0"], 5), pt(dc["0.68"], 5), pt(dc["0.9"], 5),
        pt(pe["A_31_std"], 2), pt(t["poder_linear_ao_lado"]["A_31_std"], 2), pt(pe["A_33_std"], 2), pt(pe["B_GWTC3_10"], 2), pt(pe["C_GW250114"], 2), pt(pe["A_31_x0p273_difusao_de_fase"], 2),
        pt(t["sigma_beta_lido_A31"]["sigma"], 5), pt(t["sigma_beta_lido_A31"]["sobre_beta"], 2), "SIM" if t["desfecho_em_A_legivel_hoje_NAO_CEGO"]["legivel_a_5sigma"] else "não", pt(t["desfecho_em_A_legivel_hoje_NAO_CEGO"]["z_excl_ilustracao"], 1)))
A(""); A("σ_comb(A, 31, 1/σ²) = **%s**. N₉₀ por escala [DERIVED] (da hipótese): exata %s, linear %s (base: N₉₀(k = 1) = %s do planning do registro)." % (
    pt(SIGMA_COMB_A31, 5), pt(HIP["N90_por_escala_DERIVED"]["escala_exata"], 1), pt(HIP["N90_por_escala_DERIVED"]["escala_linear_1_sobre_k2"], 1), pt(POD["N90_por_escala_DERIVED"]["N90_RB_k1_lido_do_5SIGMA_planning"], 1))); A("")
for x in DOC["o_que_a_tabela_diz"]:
    A("- " + x)
A(""); A("**M_X — a sub-tabela (comparação):** M_f (a hipótese: x = βkN(χ_f); M cancela; (1+z) cancela) · M_tot: × (M_tot/M_f)_i por evento [KNOWN] (GW250114: %s) · M_chirp: × (M_c/M_f)_i [KNOWN] (GW250114: %s) — por evento, do catálogo (`remanescentes_v3.json` `%s`), nunca «≈ 1,03–1,05»." % (
    pt(FIS["massas_GW250114"]["ratio_tot_over_f"], 4), pt(FIS["massas_GW250114"]["ratio_chirp_over_f"], 4), fsha(P_REM)[:16])); A("")
A("---"); A(""); A("## 6. O estimador, a nuisance e a sistemática (regra fixada)"); A("")
E = DOC["estimador"]
for k in ("primario", "pesos", "estatisticas", "previsao_por_evento", "secundario"):
    A("- **%s:** %s" % (k, E[k]))
S = DOC["sistematica"]
A(""); A("**Sistemática de família (C5) — REGRA FIXADA:** %s. **Ao lado, a mais dura:** %s. σ_sys,fam [DECLARADO]: %s (fonte: %s)." % (S["regra_primaria"], S["regra_ao_lado_mais_dura"], ", ".join(pt(v, 3) for v in S["sigma_sys_familia_DECLARADO"]), S["fonte"]))
A("A regra 2 da Fase 6, verbatim do pré-registro da Fase 6 (`%s`): %s" % (fsha(P_F6)[:16], " ".join(F6_REGRA or [])))
A(""); A("| σ_sys | regra | limiar |δ̄| | k_min escala linear | k_min raiz exata |"); A("|---|---|---|---|---|")
for ss, rr in KMIN.items():
    for rn, rv in rr.items():
        A("| %s | %s | %s | %s | %s |" % (ss.replace(".", ","), rn, pt(rv["limiar_|delta|"], 4), pt(rv["k_min_escala_linear_delta1_lin"], 2), pt(rv["k_min_exato_raiz"], 2)))
A(""); A("**Consequência para a hipótese:** " + DOC["consequencia_da_sistematica_para_a_hipotese"]); A("")
A("**Sistemática do início (C4):** " + S["sistematica_t0_nos_diagnosticos"]); A("")
A("---"); A(""); A("## 7. Os conjuntos e a cegueira — SÓ O D TESTA"); A("")
Dd = DOC["conjuntos"]["D"]
A("| conjunto | papel | n | fonte / instrumento | cegueira |"); A("|---|---|---|---|---|")
A("| **D** | %s | **%d elegíveis (%d sem pendência; %d pendentes de metadados GR; %d reprovados; %d test_candidates)** | %s; custo [DECLARADO] %s CPU-h; **quando: %s** | **CEGO** — AWAITING_DATA |" % (
    Dd["papel"], Dd["n_elegiveis"], Dd["n_sem_pendencia_de_qualidade"], Dd["n_pendentes_metadados_GR"], Dd["n_reprovados_Mf_det_lt_40"], Dd["n_test_candidates"], esc(Dd["instrumento"]), " / ".join(Dd["custo_DECLARADO_CPU_h"]), Dd["quando"]))
for key in ("A", "B", "C", "E"):
    c = DOC["conjuntos"][key]
    A("| %s | %s | %s | %s | %s |" % (key, c["papel"], c.get("n", "—"), esc(c.get("fonte", "—")), "NOT_BLIND" if key in ("A", "B", "C") else "CEGO; réplica"))
A(""); A("**O conjunto D — critério do registro (`RINGDOWN_5SIGMA_V1.json` `%s`; censo `%s`; manifesto O4 `%s`):** %s" % (fsha(P_5SIG)[:16], fsha(P_CENSO)[:16], fsha(P_MANIF)[:16], Dd["criterio_do_registro"])); A("")
A("- **14 elegíveis (nomes%s):** %s" % ("; GPS lido do registro quando existe" if D_GPS else "", ", ".join(("%s (GPS %s)" % (e, D_GPS[e])) if e in D_GPS else e for e in D_EVENTOS)))
A("- **com data_quality_hold (4):** %s ⟹ **10 sem pendência:** %s" % (", ".join(Dd["com_data_quality_hold"]), ", ".join(Dd["elegiveis_sem_hold"])))
A("- **pendentes AWAITING_GR_METADATA (8; entram se, com os metadados, passarem a MESMA regra):** %s" % ", ".join(Dd["pendentes_AWAITING_GR_METADATA"]))
A("- **strain em casa (manifesto O4):** %s" % json.dumps(Dd["strain_em_casa"], ensure_ascii=False))
A("- **Congelamento por evento:** %s" % Dd["congelamento_por_evento"]); A("")
A("**A previsão da hipótese por evento do conjunto D (INFORMAÇÃO CEGA: só medianas GR do registro; %s):**" % Dd["previsao_por_evento_nota"]); A("")
A("| evento | run | GPS | SNR rede | M_f,det (GR) | χ_f (GR) | hold | k = 2π/κ̂ | N | x | δ_pred exato |"); A("|---|---|---|---|---|---|---|---|---|---|---|")
for r in D_PREV:
    A("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (r["evento"], r["run"], r["GPS"], pt(r["SNR_rede_GWOSC"], 1), pt(r["Mf_det_mediana_GR"], 1), pt(r["chi_f_mediana_GR"], 2), r["data_quality_hold"], pt(r["k_kms"], 2), pt(r["N_a"], 3), pt(r["x"], 4), pt(r["delta_pred_exato"], 4)))
A("")
A("**Os dois censos, lado a lado:** %s" % DOC["os_dois_censos"]["leitura"]); A("")
Cg = DOC["cegueira"]
A("**Cegueira, canal a canal:**"); A(""); A("- **Estimador:** " + Cg["estimador"])
for x in Cg["dado_A_B_C"]:
    A("- **Dado A/B/C:** " + x)
A("- **Dado D:** " + Cg["dado_D"])
for x in Cg["consequencias"]:
    A("- **Consequência fixada:** " + x)
A(""); A("---"); A(""); A("## 8. O poder, às cegas (só σ e spin) — a hipótese e as colunas; e β_lido com σ dita antes"); A("")
A("Script `poder_cego_ramo_b_v2.py` (`%s`, copiado para esta pasta byte a byte) → `PODER_CEGO_RAMO_B_v2.json` (`%s`, idem). Conferência com o crítico: diferença máxima no poder exato dos 5 k = %r. Controle do ramo canônico (τ★ = t_P, 250 Hz, 4 ms): δ = %r." % (
    H_PODER2_PY[:16], H_PODER2[:16], POD["conferencia_com_o_critico_max_abs_diff_poder_exato"], POD["controle_ramo_canonico_delta"])); A("")
A("**A hipótese k = 2π/κ̂(χ_f):** poder exato A(31) **%sσ** [linear %s; razão %s]; A(33) %s; B(10) %s; C %s; ×0,273 %s; δ̄^pred(A) = %s [linear %s]. **Em D: não computável hoje** — as σ_i nascem na PE; o poder de D é dito no estágio cego da v387 ANTES de abrir." % (
    pt(HIP["poder_exato"]["A_31_std"], 2), pt(HIP["poder_linear_ao_lado"]["A_31_std"], 2), pt(HIP["razao_exato_sobre_linear_A31"], 3), pt(HIP["poder_exato"]["A_33_std"], 2), pt(HIP["poder_exato"]["B_GWTC3_10"], 2), pt(HIP["poder_exato"]["C_GW250114"], 2), pt(HIP["poder_exato"]["A_31_x0p273_difusao_de_fase"], 2),
    pt(HIP["delta_pred_ponderado_A31"]["exato"], 5), pt(HIP["delta_pred_ponderado_A31"]["linear"], 5))); A("")
A("**As σ por evento (A, 31; só σ e spin), com k_KMS(a_f), N(a_f), x e δ_exato da hipótese:**"); A("")
A("| evento | σ (std) | a_f | N(a_f) | k = 2π/κ̂(a_f) | x | δ_exato |"); A("|---|---|---|---|---|---|---|")
for e in DOC["sigma_por_evento_A31_so_sigma_e_spin"]:
    A("| %s | %s | %s | %s | %s | %s | %s |" % (e["evento"], pt(e["sigma_std"], 4), pt(e["spin_q50"], 3), pt(e["N_a"], 3), pt(e["k_kms"], 2), pt(e["x"], 4), pt(e["delta_exato"], 4)))
A(""); B = DOC["beta_lido"]
A("**β_lido (decisão 12):** %s — %s. σ: %s. **Dita antes (A, 31; hipótese): σ(β_lido) = %s = %s β** (a leitura resolveria β a ~%sσ nominais em A — mas A é NOT_BLIND; o que vale é D, com a σ dita na v387). Por k em A: %s." % (
    B["formula"], B["natureza"], B["sigma_formula_1a_ordem"], pt(B["sigma_dita_antes_conjunto_A31_hipotese"], 5), pt(B["sigma_sobre_beta_A31_hipotese"], 2), pt(1.0 / B["sigma_sobre_beta_A31_hipotese"], 1),
    "; ".join("%s %s (%s β)" % (k, pt(v["sigma"], 5), pt(v["sobre_beta"], 2)) for k, v in B["sigma_por_k_A31"].items()))); A("")
A("**Não entrou no poder (dito):** σ_sys de família ainda não somada em quadratura (entra em w_i na rodada); a incerteza de Kerr por evento (RD-02, +4 % em σ, desprezível); a nuisance c(σ) (reduz o poder efetivo; a rodada reporta o poder COM c(σ) profilado); a seleção dos 31 (literal do release)."); A("")
A("---"); A(""); A("## 9. Os controles"); A("")
for x in DOC["controles"]:
    A("- " + x)
A(""); A("---"); A(""); A("## 10. Os VEREDITOS permitidos (na ORDEM; a primeira regra que se aplica decide; CONFIRMED proibido)"); A("")
Vv = DOC["vereditos"]
A("Tokens: base `%s`; conjunto D `%s`; conjunto A `%s`; **estado deste V1: `%s`**. Cunhagem: %s." % (Vv["tokens"]["base"], Vv["tokens"]["conjunto_D"], Vv["tokens"]["conjunto_A"], Vv["tokens"]["estado_deste_V1"], Vv["tokens"]["cunhagem"])); A("")
A("Renomeia do protocolo V1 do core (`allowed_verdicts` = %s; `forbidden` = %s): %s — herda a Fase 6/V1.4 (falsifica o PAR, não a lei) e o piso dos vazios (AWAITING_DATA)." % (json.dumps(Vv["protocolo_V1_core_allowed"]), json.dumps(Vv["protocolo_V1_core_forbidden"]), json.dumps(Vv["renomeia"], ensure_ascii=False))); A("")
for v in VEREDITOS_ORDEM:
    A("%d. **`%s`** — %s" % (v["n"], v["token"], v["regra"]))
A(""); A("**«Coincidir com a RG»:** " + Vv["coincidir_com_a_RG"]); A(""); A("**Status:** veredito deste V1 `%s`; canal F2b no livro: %s." % (Vv["status"]["veredito_deste_V1"], Vv["status"]["canal_F2b_no_livro"])); A("")
A("---"); A(""); A("## 11. O que o resultado NÃO decide (dito antes)"); A("")
for x in DOC["nao_decide"]:
    A("- " + x)
A(""); A("**O homônimo KMS da Fase 6:** " + DOC["homonimo_KMS_fase_6"]); A("")
A("**O verbatim de 16/09, AO LADO (`%s` `%s`):** «%s» — %s" % (os.path.basename(DOC["verbatim_16_09_ao_lado"]["fonte"]), DOC["verbatim_16_09_ao_lado"]["sha256"][:16], DOC["verbatim_16_09_ao_lado"]["texto"], DOC["verbatim_16_09_ao_lado"]["leitura"])); A("")
A("---"); A(""); A("## 12. O que o registro já diz (lido do core v385 por script; nada aqui é novo)"); A("")
A("```json"); A(json.dumps(DOC["o_que_o_registro_ja_diz"], ensure_ascii=False, indent=1)); A("```"); A("")
A("---"); A(""); A("## 13. O que a gerência errou e corrigiu (em nome próprio)"); A("")
A("| erro | correção | régua |"); A("|---|---|---|")
for e in DOC["o_que_a_gerencia_errou_e_corrigiu"]:
    A("| %s%s | %s | %s |" % (esc(e["erro"]), (" (busca: %s)" % esc(e["busca_errada"])) if e.get("busca_errada") else "", esc(e["correcao"]), esc(e["classificacao_da_regua"])))
A(""); A("---"); A(""); A("## 14. A disciplina (ordem de execução; fail-closed)"); A("")
for i, x in enumerate(DOC["disciplina"]):
    A("%d. %s" % (i + 1, x))
A(""); A("---"); A(""); A("## 15. Estatutos"); A(""); A("| objeto | estatuto |"); A("|---|---|")
for o, s in DOC["estatutos"]:
    A("| %s | %s |" % (esc(o), esc(s)))
A(""); A("---"); A(""); A("## 16. Fontes lidas (caminho absoluto · sha256 · bytes) — todas calculadas por este script; nenhuma digitada"); A("")
for f in FONTES:
    A("- **%s**: `%s` — `%s` (%s B) %s%s" % (f["papel"], f["caminho"], f["sha256"], f["bytes"], f["estatuto"], (" — **AUSENTE:** " + f["AUSENTE"]) if f.get("AUSENTE") else ""))
A(""); A("Fontes ausentes: %d. Leaver: %s." % (len(FONTES_AUSENTES), LEAVER_NOTA)); A("")
A("---"); A(""); A("## 17. A especificação congelada (o que o `um.py` v386 lê por hash)"); A("")
A("```json"); A(json.dumps(SPEC, ensure_ascii=False, indent=1)); A("```"); A("")
A("PROVADA ≠ CONFIRMADA. NOT_FALSIFIED nunca é CONFIRMED. A RG é o limite clássico, não rival. Este V1 está CONGELADO pelo hash da especificação `%s`; o desfecho está por vir e nunca será CONFIRMED." % SPEC_SHA)
md = ("\n".join(L) + "\n").encode("utf-8")
raw = json.dumps(DOC, ensure_ascii=False, indent=1).encode("utf-8")

# ------------------------------------------------------------------------------------------------------------------------------
# 10. as guardas e a gravacao (temporario -> tamanho -> substituir); um V1 ja congelado com OUTRO conteudo nao se sobrescreve
# ------------------------------------------------------------------------------------------------------------------------------
_VOL = {"gerado_utc", "gerador"}
if os.path.exists(OUT_JSON):
    _old = jload(OUT_JSON)
    _a = {k: v for k, v in _old.items() if k not in _VOL}
    _b = {k: v for k, v in json.loads(raw.decode("utf-8")).items() if k not in _VOL}
    if canon(_a) != canon(_b):
        _dif = sorted(k for k in set(_a) | set(_b) if canon(_a.get(k)) != canon(_b.get(k)))
        raise SystemExit("RECUSO: %s ja existe com OUTRO conteudo (chaves que diferem: %s); o congelado nao se sobrescreve -- uma versao nova e ato da gerencia com gerador novo" % (OUT_JSON, _dif))
    print("o V1 ja existe com o MESMO conteudo (fora o carimbo): nada regravado")
    raw = open(OUT_JSON, "rb").read(); md = open(OUT_MD, "rb").read()
else:
    for _pth, _b in ((OUT_MD, md), (OUT_JSON, raw)):   # o MD primeiro; o JSON (a autoridade) por ultimo
        open(_pth + ".tmp", "wb").write(_b)
        assert os.path.getsize(_pth + ".tmp") == len(_b)
        os.replace(_pth + ".tmp", _pth)
        assert open(_pth, "rb").read() == _b, "o arquivo gravado nao confere: %s" % _pth
# as copias do PODER v2 (bytes iguais, conferidos)
for nome, src in COPIAS:
    dst = os.path.join(HERE, nome)
    b = open(src, "rb").read()
    if os.path.exists(dst):
        assert open(dst, "rb").read() == b, "a copia existente difere da fonte: %s" % dst
    else:
        open(dst + ".tmp", "wb").write(b); assert os.path.getsize(dst + ".tmp") == len(b); os.replace(dst + ".tmp", dst)
        assert open(dst, "rb").read() == b
# V1_RAMO_B_HASHES.json: sha256 e bytes de cada arquivo da pasta (menos ele proprio, que nao pode conter o proprio hash)
HASHES = {"id": ID, "spec_sha256": SPEC_SHA, "gerado_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "pasta": HERE, "nota": "sha256 e bytes de cada arquivo desta pasta, lidos do disco por script; este arquivo nao lista a si proprio", "arquivos": {}}
for f in sorted(os.listdir(HERE)):
    p = os.path.join(HERE, f)
    if f == os.path.basename(OUT_HASHES) or not os.path.isfile(p) or f.endswith(".tmp"):
        continue
    _HCACHE.pop(os.path.abspath(p), None)
    HASHES["arquivos"][f] = {"caminho": p, "sha256": fsha(p), "bytes": os.path.getsize(p)}
hb = json.dumps(HASHES, ensure_ascii=False, indent=1).encode("utf-8")
open(OUT_HASHES + ".tmp", "wb").write(hb); assert os.path.getsize(OUT_HASHES + ".tmp") == len(hb); os.replace(OUT_HASHES + ".tmp", OUT_HASHES)
print("spec_sha256", SPEC_SHA)
print("json", sha_bytes(open(OUT_JSON, "rb").read()), os.path.getsize(OUT_JSON), OUT_JSON)
print("md  ", sha_bytes(open(OUT_MD, "rb").read()), os.path.getsize(OUT_MD), OUT_MD)
for f, v in HASHES["arquivos"].items():
    print("  %-40s %s %d" % (f, v["sha256"], v["bytes"]))
print("hashes", sha_bytes(hb), len(hb), OUT_HASHES)
print("fontes:", len(FONTES), "ausentes:", len(FONTES_AUSENTES), [f["caminho"] for f in FONTES_AUSENTES])
print("hipotese:", K_NAMES[HIPOTESE_K][0], "| poder exato A31 %.4f B10 %.4f C %.4f x0.273 %.4f | sigma(beta_lido) A31 %.6f (%.3f beta) | sigma_comb A31 %.6f" % (
    HIP["poder_exato"]["A_31_std"], HIP["poder_exato"]["B_GWTC3_10"], HIP["poder_exato"]["C_GW250114"], HIP["poder_exato"]["A_31_x0p273_difusao_de_fase"], HIP["sigma_beta_lido_A31"]["sigma"], HIP["sigma_beta_lido_A31"]["sobre_beta"], SIGMA_COMB_A31))
print("conjunto D:", len(D_EVENTOS), "elegiveis;", len(CONJ_D["elegiveis_sem_hold"]["eventos"]), "sem hold;", len(D_GPS), "com GPS lido")
print("acervo:", {k: {n: t["achado"] for n, t in v["trechos"].items()} for k, v in ACERVO.items()})
