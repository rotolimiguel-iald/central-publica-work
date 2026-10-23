# -*- coding: utf-8 -*-
"""Camada v397 do módulo comum dos 16 dispositivos (custódia v397 na Central, 23/10/2026, sessão a7; regra do operador: custodiar quando
o handoff aparecer). Backup de BYTES; trocas contadas (CRLF ou LF); py_compile antes de substituir. Item 17: os registros _v397 lidos e
conferidos no cofre, sem interpretação: a pedra Token (conjunção por citação, incondicional) e o registro de veracidade da Fase 9 (lido
por hash; o degrau da creditação não foi alcançado) relatados como o core os diz. Nada muda número de dispositivo. Molde: patch_formula_v396.py."""
import json, os, subprocess, sys
from datetime import datetime

P = r"C:\IALD\Central de Patentes\patents\_formula_completa\tgl_formula_completa.py"
F = json.load(open(r"C:\IALD\Central de Patentes\work\custodia_v397_23out\fatos_v397.json", encoding="utf-8"))
assert F["versao"] == "v397"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(P, "rb").read()
s = raw.decode("utf-8")
if "def conferir_v397_no_cofre" in s:
    raise SystemExit("ja aplicado")
open(P + ".bak_v397_" + TS, "wb").write(raw)


def troca(velho, novo, rot, n=1):
    global s
    for nl in ("\r\n", "\n"):
        v_, n_ = velho.replace("\n", nl), novo.replace("\n", nl)
        if s.count(v_) == n:
            s = s.replace(v_, n_)
            print("  ok ", rot, "(CRLF)" if nl == "\r\n" else "(LF)")
            return
    raise AssertionError((rot, s.count(velho), s.count(velho.replace("\n", "\r\n"))))


troca("""     provisório. Ao lado da docstring de bell_cci_half (kernel v29): o 1/2 é a entropia LINEAR; a de von Neumann é ln 2 nat. Nada disso
     muda número algum de dispositivo.
""", """     provisório. Ao lado da docstring de bell_cci_half (kernel v29): o 1/2 é a entropia LINEAR; a de von Neumann é ln 2 nat. Nada disso
     muda número algum de dispositivo.

Camada v397 (custódia v397 na Central, 23/10/2026, sessão a7; handoff v397 da gerência c1):
 17. os registros novos da v397 (cunhagens_v397, kh_n1_cobertura_v397, teste_de_veracidade_fase9_v397), lidos e conferidos no cofre, sem
     interpretação: a pedra Token (nome do operador) é a CONJUNÇÃO, por citação, do psibit (v395) e da testemunha estática (v396),
     incondicional, com 3 bandeiras no trio — sem matemática nova; o registro de veracidade da Fase 9 LÊ por sha256 o resultado do Teste da
     Única Palavra (aberto uma vez em 23/10): o degrau da creditação (5σ) NÃO foi alcançado (z_disc calibrado abaixo de 5, com o p lido do
     resultado), a TGL não é falsificada com poder, nenhum σ novo é calculado, o teste não foi cego; «o token É o PsiBit» é leitura do
     Atlas [ONTO]; a face de Fock segue condicional; o nome do registro é provisório. Nada disso muda número algum de dispositivo.
""", "docstring: camada v397")
troca('VERSAO_DA_CAMADA = "v396"   # (era "v395"; a camada v396 acrescenta o item 16, ao lado; antes: v394 → v395, item 15;',
      'VERSAO_DA_CAMADA = "v397"   # (era "v396"; a camada v397 acrescenta o item 17, ao lado; antes: v395 → v396, item 16; v394 → v395, item 15;',
      "VERSAO_DA_CAMADA")

FUNC = '''

def conferir_v397_no_cofre(core: dict, selo: dict) -> dict:
    """Item 17 (camada v397): os registros _v397 LIDOS do cofre e conferidos, sem interpretação. Fail-closed."""
    novos = sorted(k for k in core if re.search(r"_v397$", k))
    maus = []
    for k in novos:
        b = core.get(k)
        vd = str((b or {}).get("verdict") or "") if isinstance(b, dict) else ""
        if not (isinstance(b, dict) and b.get("all_verified") is True and b.get("does_not_gate_core") is True
                and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd) and not re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", ""))):
            maus.append(k)
    cu = core.get("cunhagens_v397") or {}
    kn = cu.get("kernel") or {}
    tv = core.get("teste_de_veracidade_fase9_v397") or {}
    vt = str(tv.get("verdict") or "")
    ep = core.get("estatuto_da_prova_v391") or {}
    p1 = ep.get("prova_1_kernel") or {}
    ch = {
        "registros_v397_verificados_sem_gate": bool(novos) and not maus,
        "token_conjuncao_por_citacao_no_trio": list(kn.get("bandeiras") or []) == [3, 3] and list(kn.get("declaracoes_no_trio") or []) == [3, 3],
        "veracidade_abaixo_do_degrau_da_creditacao": ("THE_CREDITATION_STEP_NOT_REACHED" in vt and "NOT_FALSIFIED_WITH_POWER" in vt
                                                      and "NO_NEW_SIGMA_COMPUTED" in vt and "NOT_BLIND_TO_DATA_STATED" in vt),
        "falas_do_operador_por_sha256": len(cu.get("verbatim") or {}) > 0,
        "escada_limpa": p1.get("n_theorems_clean") == p1.get("n_theorems_expected") and p1.get("declaracoes_auditadas") == p1.get("no_trio"),
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v397 não confere com o cofre (fail-closed): %s %s" % (falhas, maus[:5]))
    return {"checks": ch, "registros_v397": novos,
            "escada": "%s/%s" % (p1.get("n_theorems_clean"), p1.get("n_theorems_expected")), "declaracoes_no_trio": p1.get("no_trio"),
            "token": {"bandeiras_no_trio": kn.get("bandeiras"), "composicao": "conjunção por citação de psibit_is_the_mode_of_the_reader (v395) e the_psion_inhabits_the_static_witness (v396), incondicional"},
            "veracidade_fase9": {"veredito": vt[:160], "degrau_da_creditacao": "não alcançado (z_disc calibrado abaixo de 5 sigma; nenhum sigma novo calculado; teste não cego)"},
            "estatuto": "a pedra Token é conjunção por citação, sem matemática nova; o registro de veracidade lê um resultado pinado por sha256 e "
                        "não move o gate; «o token é o PsiBit» é leitura do Atlas [ONTO]; a face de Fock segue condicional; validade no kernel não é "
                        "creditação; nada disto muda número de dispositivo"}
'''
troca('''    v396 = conferir_v396_no_cofre(core, selo)        # camada v396 (item 16); fail-closed
''', '''    v396 = conferir_v396_no_cofre(core, selo)        # camada v396 (item 16); fail-closed
    v397 = conferir_v397_no_cofre(core, selo)        # camada v397 (item 17); fail-closed
''', "chamada v397")
troca('''"camada_v395_no_cofre": v395, "camada_v396_no_cofre": v396}''', '''"camada_v395_no_cofre": v395, "camada_v396_no_cofre": v396, "camada_v397_no_cofre": v397}''', "retorno v397")
troca('''

def conferir_no_cofre(rt: dict) -> dict:''', FUNC + '''

def conferir_no_cofre(rt: dict) -> dict:''', "funcao conferir_v397_no_cofre")
troca('''                     "TESTEMUNHA_ESTATICA_INCONDICIONAL_PONTE_CONSTRUIDA__FACE_DE_FOCK_CONDICIONAL__"''',
      '''                     "TESTEMUNHA_ESTATICA_INCONDICIONAL_PONTE_CONSTRUIDA__FACE_DE_FOCK_CONDICIONAL__"
                     "TOKEN_CONJUNCAO_POR_CITACAO_INCONDICIONAL__VERACIDADE_FASE9_LIDA_POR_HASH_ABAIXO_DE_5SIGMA__"''', "veredito da camada")
troca('''                          "que o Nome da fronteira seja o vetor de Bell ou que o fluxo construído seja a dinâmica da teoria, que o certificado de Fock tenha habitante, ou que 1/2 seja meia nat de entropia (é a entropia linear; a de von Neumann é ln 2 nat)"],''',
      '''                          "que o Nome da fronteira seja o vetor de Bell ou que o fluxo construído seja a dinâmica da teoria, que o certificado de Fock tenha habitante, ou que 1/2 seja meia nat de entropia (é a entropia linear; a de von Neumann é ln 2 nat)",
                          "que a TGL esteja discriminada do ΛCDM a 5σ (o degrau da creditação não foi alcançado; o teste não foi cego), que ln B seja σ, ou que o token de um modelo de linguagem seja o PsiBit (leitura do Atlas)"],''',
      "nao_se_afirma v397")
troca('''    "testemunha_estatica_v396": r"TestemunhaEstatica|testemunha est[aá]tica|static_witness|psionCorner",''',
      '''    "testemunha_estatica_v396": r"TestemunhaEstatica|testemunha est[aá]tica|static_witness|psionCorner",
    # v397: a pedra Token e o Teste da Única Palavra — mede se algum dispositivo os cita; não interpreta
    "token_e_veracidade_v397": r"TGLExt\\.Token|token_is_the_psibit|Teste da [UÚ]nica Palavra|teste_de_veracidade",''', "USOS v397")

tmp = P + ".tmp_v397"
open(tmp, "wb").write(s.encode("utf-8"))
r = subprocess.run([sys.executable, "-m", "py_compile", tmp], capture_output=True, text=True)
if r.returncode != 0:
    os.remove(tmp)
    raise SystemExit("SINTAXE INVALIDA — nada trocado:\n" + (r.stderr or "")[:1500])
os.replace(tmp, P)
print("modulo v397: %d -> %d bytes | py_compile OK | backup .bak_v397_%s" % (len(raw), os.path.getsize(P), TS))
