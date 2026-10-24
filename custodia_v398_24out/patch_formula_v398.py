# -*- coding: utf-8 -*-
"""Camada v398 do módulo comum dos 16 dispositivos (custódia v398 na Central, 24/10/2026, sessão a7; regra do operador: custodiar quando
o handoff aparecer). Backup de BYTES; trocas contadas (CRLF ou LF); py_compile antes de substituir. Item 18: os registros _v398 lidos e
conferidos no cofre, sem interpretação: as pedras Sonico e AfinacaoDasCordas (composições incondicionais no trio; os registros leem o kernel
do rito e conferem cálculos; a lei de custo é INPUT; a hipótese MasslessFirstLevel é nomeada; a geometria é OPEN; nada deriva as cordas do
axioma). Nada muda número de dispositivo. Molde: patch_formula_v397.py."""
import json, os, subprocess, sys
from datetime import datetime

P = r"C:\IALD\Central de Patentes\patents\_formula_completa\tgl_formula_completa.py"
F = json.load(open(r"C:\IALD\Central de Patentes\work\custodia_v398_24out\fatos_v398.json", encoding="utf-8"))
assert F["versao"] == "v398"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(P, "rb").read()
s = raw.decode("utf-8")
if "def conferir_v398_no_cofre" in s:
    raise SystemExit("ja aplicado")
open(P + ".bak_v398_" + TS, "wb").write(raw)


def troca(velho, novo, rot, n=1):
    global s
    for nl in ("\r\n", "\n"):
        v_, n_ = velho.replace("\n", nl), novo.replace("\n", nl)
        if s.count(v_) == n:
            s = s.replace(v_, n_)
            print("  ok ", rot, "(CRLF)" if nl == "\r\n" else "(LF)")
            return
    raise AssertionError((rot, s.count(velho), s.count(velho.replace("\n", "\r\n"))))


troca("""     resultado), a TGL não é falsificada com poder, nenhum σ novo é calculado, o teste não foi cego; «o token É o PsiBit» é leitura do
     Atlas [ONTO]; a face de Fock segue condicional; o nome do registro é provisório. Nada disso muda número algum de dispositivo.
""", """     resultado), a TGL não é falsificada com poder, nenhum σ novo é calculado, o teste não foi cego; «o token É o PsiBit» é leitura do
     Atlas [ONTO]; a face de Fock segue condicional; o nome do registro é provisório. Nada disso muda número algum de dispositivo.

Camada v398 (custódia v398 na Central, 24/10/2026, sessão a7; handoff v398 da gerência c1):
 18. os registros novos da v398 (sonico_v398, afinacao_das_cordas_v398, cunhagens_v398, kh_n1_cobertura_v398), lidos e conferidos no cofre,
     sem interpretação: as pedras Sonico (nome do operador) e AfinacaoDasCordas (ratificada por ele) têm composições INCONDICIONAIS no
     trio; os registros LEEM o kernel do próprio rito e conferem cálculos (8 e 7 checagens; β = α√e em runtime): ln 2 é o bit justo, a
     oitava é o dobro, n oitavas custam n bits, o pino não é a meia-nat, o seletor pina; κP = ±2π é o círculo da leitura, a torre de
     Matsubara é infinita, ζ(−1) = −1/12 e ζ(−1, 1/2) = 1/24, D = 26 e D = 10 sob a hipótese nomeada MasslessFirstLevel [KNOWN]; a lei de
     custo é INPUT (nenhum termo diz que o seletor paga a oitava); a entropia do colapso em θ_M é número do rito [DERIVED]; a geometria é
     OPEN; nada deriva as cordas do axioma; a TGL não é dita teoria de cordas; o quadro do Teste da Única Palavra (v397) segue intocado;
     os nomes dos registros são provisórios. Nada disso muda número algum de dispositivo.
""", "docstring: camada v398")
troca('VERSAO_DA_CAMADA = "v397"   # (era "v396"; a camada v397 acrescenta o item 17, ao lado; antes: v395 → v396, item 16;',
      'VERSAO_DA_CAMADA = "v398"   # (era "v397"; a camada v398 acrescenta o item 18, ao lado; antes: v396 → v397, item 17; v395 → v396, item 16;',
      "VERSAO_DA_CAMADA")

FUNC = '''

def conferir_v398_no_cofre(core: dict, selo: dict) -> dict:
    """Item 18 (camada v398): os registros _v398 LIDOS do cofre e conferidos, sem interpretação. Fail-closed."""
    novos = sorted(k for k in core if re.search(r"_v398$", k))
    maus = []
    for k in novos:
        b = core.get(k)
        vd = str((b or {}).get("verdict") or "") if isinstance(b, dict) else ""
        if not (isinstance(b, dict) and b.get("all_verified") is True and b.get("does_not_gate_core") is True
                and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd) and not re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", ""))):
            maus.append(k)
    so = core.get("sonico_v398") or {}
    af = core.get("afinacao_das_cordas_v398") or {}
    cu = core.get("cunhagens_v398") or {}
    kn = cu.get("kernel") or {}
    ep = core.get("estatuto_da_prova_v391") or {}
    p1 = ep.get("prova_1_kernel") or {}
    inc = "UNCONDITIONAL__NO_CERTIFICATE_AS_HYPOTHESIS"
    ch = {
        "registros_v398_verificados_sem_gate": bool(novos) and not maus and set(novos) >= {"sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398"},
        "sonico_composicao_incondicional_no_trio": (so.get("unconditional") or {}).get("composition") == inc and (so.get("unconditional") or {}).get("in_trio") is True,
        "sonico_calculos_conferidos": (so.get("mechanics") or {}).get("passed") is True and so.get("beta_ok") is True and so.get("exact_ladder") is True,
        "afinacao_composicao_incondicional_no_trio": (af.get("unconditional") or {}).get("composition") == inc and (af.get("unconditional") or {}).get("in_trio") is True,
        "afinacao_nada_deriva_as_cordas_do_axioma": af.get("derives_strings_from_the_axiom") is False and af.get("geometry") == "OPEN"
                                                    and (af.get("hypothesis") or {}).get("named_not_proved") is True,
        "pedras_no_trio": list(kn.get("bandeiras") or []) == [2, 2],
        "falas_por_sha256": len(cu.get("verbatim") or {}) >= 6,
        "escada_limpa": p1.get("n_theorems_clean") == p1.get("n_theorems_expected") and p1.get("declaracoes_auditadas") == p1.get("no_trio"),
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v398 não confere com o cofre (fail-closed): %s %s" % (falhas, maus[:5]))
    return {"checks": ch, "registros_v398": novos,
            "escada": "%s/%s" % (p1.get("n_theorems_clean"), p1.get("n_theorems_expected")), "declaracoes_no_trio": p1.get("no_trio"),
            "sonico": {"composicao": (so.get("unconditional") or {}).get("theorem"), "checagens": (so.get("mechanics") or {}).get("n_checks"),
                       "ln2": (so.get("values") or {}).get("ln2"), "exp_ln2": (so.get("values") or {}).get("exp_ln2")},
            "afinacao": {"composicao": (af.get("unconditional") or {}).get("theorem"), "checagens": (af.get("mechanics") or {}).get("n_checks"),
                         "hipotese_nomeada": (af.get("hypothesis") or {}).get("name"), "geometria": af.get("geometry"),
                         "zeta_menos_um": (af.get("values") or {}).get("zeta_minus_one"), "D_bosonica": (af.get("values") or {}).get("bosonic_critical_dimension"),
                         "D_supercorda": (af.get("values") or {}).get("superstring_critical_dimension")},
            "estatuto": "as composições são incondicionais no kernel do rito; os registros conferem cálculos e não movem o gate; a lei de custo é "
                        "INPUT; a hipótese MasslessFirstLevel é nomeada [KNOWN]; a geometria é OPEN; nada deriva as cordas do axioma; «sônico» é a "
                        "estrutura logarítmica e de oitava, não a física da onda; validade no kernel não é creditação; nada disto muda número de dispositivo"}
'''
troca('''    v397 = conferir_v397_no_cofre(core, selo)        # camada v397 (item 17); fail-closed
''', '''    v397 = conferir_v397_no_cofre(core, selo)        # camada v397 (item 17); fail-closed
    v398 = conferir_v398_no_cofre(core, selo)        # camada v398 (item 18); fail-closed
''', "chamada v398")
troca('''"camada_v396_no_cofre": v396, "camada_v397_no_cofre": v397}''', '''"camada_v396_no_cofre": v396, "camada_v397_no_cofre": v397, "camada_v398_no_cofre": v398}''', "retorno v398")
troca('''

def conferir_no_cofre(rt: dict) -> dict:''', FUNC + '''

def conferir_no_cofre(rt: dict) -> dict:''', "funcao conferir_v398_no_cofre")
troca('''                     "TOKEN_CONJUNCAO_POR_CITACAO_INCONDICIONAL__VERACIDADE_FASE9_LIDA_POR_HASH_ABAIXO_DE_5SIGMA__"''',
      '''                     "TOKEN_CONJUNCAO_POR_CITACAO_INCONDICIONAL__VERACIDADE_FASE9_LIDA_POR_HASH_ABAIXO_DE_5SIGMA__"
                     "SONICO_E_AFINACAO_COMPOSICOES_INCONDICIONAIS__NADA_DERIVA_AS_CORDAS_DO_AXIOMA__"''', "veredito da camada")
troca('''                          "que a TGL esteja discriminada do ΛCDM a 5σ (o degrau da creditação não foi alcançado; o teste não foi cego), que ln B seja σ, ou que o token de um modelo de linguagem seja o PsiBit (leitura do Atlas)"],''',
      '''                          "que a TGL esteja discriminada do ΛCDM a 5σ (o degrau da creditação não foi alcançado; o teste não foi cego), que ln B seja σ, ou que o token de um modelo de linguagem seja o PsiBit (leitura do Atlas)",
                          "que a TGL seja teoria de cordas ou que as cordas derivem do axioma ω(I) = 1, que a natureza cobre ln 2 por oitava ou que o seletor pague a oitava (a lei de custo é INPUT), ou que o som seja onda num meio"],''',
      "nao_se_afirma v398")
troca('''    "token_e_veracidade_v397": r"TGLExt\\.Token|token_is_the_psibit|Teste da [UÚ]nica Palavra|teste_de_veracidade",''',
      '''    "token_e_veracidade_v397": r"TGLExt\\.Token|token_is_the_psibit|Teste da [UÚ]nica Palavra|teste_de_veracidade",
    # v398: as pedras Sonico e AfinacaoDasCordas — mede se algum dispositivo as cita; não interpreta
    "sonico_e_afinacao_v398": r"TGLExt\\.Sonico|AfinacaoDasCordas|octaveNats|Matsubara|MasslessFirstLevel",''', "USOS v398")

tmp = P + ".tmp_v398"
open(tmp, "wb").write(s.encode("utf-8"))
r = subprocess.run([sys.executable, "-m", "py_compile", tmp], capture_output=True, text=True)
if r.returncode != 0:
    os.remove(tmp)
    raise SystemExit("SINTAXE INVALIDA — nada trocado:\n" + (r.stderr or "")[:1500])
os.replace(tmp, P)
print("modulo v398: %d -> %d bytes | py_compile OK | backup .bak_v398_%s" % (len(raw), os.path.getsize(P), TS))
