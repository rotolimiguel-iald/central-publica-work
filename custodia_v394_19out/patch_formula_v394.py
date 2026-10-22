# -*- coding: utf-8 -*-
"""Camada v394 do módulo comum dos 16 dispositivos (custódia conjunta v392+v393+v394 na Central, 19/10/2026, sessão a7; ordem do operador:
«atualize todos os dispositovos e toda a cenrtral tambem»). Backup de BYTES antes; trocas conferidas por contagem (CRLF ou LF: o arquivo é
misto); py_compile antes de substituir. Item 14: os 42 registros novos desde a v391 (sufixos _v392/_v393/_v394) lidos e conferidos no cofre,
sem interpretação; os da v394 relatados como o core os diz (a escada, a rede de Fock com o contrato conjunto, o coração e a evidência
espectral independente); errata ao lado do item 12 (a lei de campo no curvo é termo de kernel CONDICIONAL ao H3 nomeado desde a v392)."""
import os, subprocess, sys
from datetime import datetime

P = r"C:\IALD\Central de Patentes\patents\_formula_completa\tgl_formula_completa.py"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(P, "rb").read()
s = raw.decode("utf-8")
if "def conferir_v394_no_cofre" in s:
    raise SystemExit("ja aplicado")
open(P + ".bak_v394_" + TS, "wb").write(raw)


def troca(velho, novo, rot, n=1):
    global s
    for nl in ("\r\n", "\n"):
        v_, n_ = velho.replace("\n", nl), novo.replace("\n", nl)
        if s.count(v_) == n:
            s = s.replace(v_, n_)
            print("  ok ", rot, "(CRLF)" if nl == "\r\n" else "(LF)")
            return
    raise AssertionError((rot, s.count(velho), s.count(velho.replace("\n", "\r\n"))))


troca("""     o verbatim do operador embutido por sha256. Nenhuma pedra nova no kernel. Nada disso muda número algum de dispositivo.
""", """     o verbatim do operador embutido por sha256. Nenhuma pedra nova no kernel. Nada disso muda número algum de dispositivo.

Camada v394 (custódia conjunta v392+v393+v394 na Central, 19/10/2026, sessão a7; handoffs v392, v393 e v394 da gerência c1):
 14. os registros novos desde a v391 (os blocos de sufixo _v392, _v393 e _v394 do núcleo), lidos e conferidos no cofre, sem interpretação:
     cada um verificado, sem efeito no gate e sem CONFIRMED; a escada da v394 (bandeiras de declarações nomeadas — teoremas e definições —
     com axiomas no trio), a rede de Fock (componentes construídos; o contrato conjunto NÃO habitado, itens abertos), o coração (forma
     verificada; a evidência espectral independente como o core a diz) e o critério binário de parada, relatados como o core os diz.
     Errata ao lado do item 12: desde a v392 a lei de campo no curvo é termo de kernel CONDICIONAL ao H3 nomeado (`lei_de_campo_curvo_v392`);
     o antecedente H3 em toda tela segue [KNOWN] e não há existência global. Nada disso muda número algum de dispositivo.
""", "docstring: camada v394")
troca('VERSAO_DA_CAMADA = "v391"   # (era "v390"; a camada v391 acrescenta o item 13, ao lado; antes: v389 → v390, item 12; v386 → v389, item 11; v379 → v386, itens 8–10)',
      'VERSAO_DA_CAMADA = "v394"   # (era "v391"; a camada v394 acrescenta o item 14, ao lado; antes: v390 → v391, item 13; v389 → v390, item 12; v386 → v389, item 11; v379 → v386, itens 8–10)',
      "VERSAO_DA_CAMADA")

FUNC = '''

def conferir_v394_no_cofre(core: dict, selo: dict) -> dict:
    """Item 14 (camada v394): os registros novos desde a v391 LIDOS do cofre e conferidos, sem interpretação. Fail-closed."""
    TOK = ("GATE_UNMOVED", "GATE_UNTOUCHED", "GATE_STRING_UNCHANGED", "NO_GATE_EFFECT")
    novos = sorted(k for k in core if re.search(r"_v39[234]$", k))
    maus = []
    for k in novos:
        b = core.get(k)
        vd = str((b or {}).get("verdict") or "") if isinstance(b, dict) else ""
        if not (isinstance(b, dict) and b.get("all_verified") is True and b.get("does_not_gate_core") is True and any(t in vd for t in TOK)
                and not re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", ""))):
            maus.append(k)
    ep = core.get("estatuto_da_prova_v391") or {}
    p1 = ep.get("prova_1_kernel") or {}
    rf = core.get("rede_fock_v394") or {}
    co = core.get("coracao_e_selo_gravitacional_v393") or {}
    cb = core.get("criterio_binario_de_parada_v394") or {}
    esp = (co.get("evidencia_espectral_independente") or {}).get("hoje")
    ch = {
        "registros_novos_desde_v391_todos_verificados_sem_gate": bool(novos) and not maus,
        "escada_limpa": p1.get("n_theorems_clean") == p1.get("n_theorems_expected") and p1.get("declaracoes_auditadas") == p1.get("no_trio"),
        "escada_dita_em_bandeiras": "_FLAGS_" in str(ep.get("verdict") or ""),
        "rede_fock_contrato_conjunto_dito": isinstance(rf.get("whole_certificate_inhabited"), bool)
                                            and (rf.get("whole_certificate_inhabited") or len(rf.get("open_joint_contract") or []) > 0),
        "coracao_forma_verificada": str(co.get("verdict") or "").startswith("FORM_VERIFIED_CHI_FROM_CODATA__G_BY_PLANCK_NORMALIZATION"),
        "coracao_evidencia_espectral_dita": esp in ("AUSENTE", "PRESENTE"),
        "criterio_binario_verificado": cb.get("all_verified") is True and "FIXED_POINT" in str(cb.get("verdict") or ""),
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v394 não confere com o cofre (fail-closed): %s %s" % (falhas, maus[:5]))
    return {"checks": ch, "n_registros_novos_desde_v391": len(novos),
            "escada": "%s/%s" % (p1.get("n_theorems_clean"), p1.get("n_theorems_expected")), "declaracoes_no_trio": p1.get("no_trio"),
            "rede_fock": {"contrato_conjunto_habitado": rf.get("whole_certificate_inhabited"), "itens_abertos": len(rf.get("open_joint_contract") or []),
                          "componentes_construidos": len(rf.get("constructed_components") or [])},
            "coracao_evidencia_espectral_independente": esp,
            "estatuto": "PROVADA = validade (o kernel prova a implicação); CONFIRMADA = creditação, recusada; a rede de Fock e o H3 em toda direção "
                        "nula seguem ABERTOS; a lei de campo no curvo é termo de kernel só CONDICIONAL ao H3 nomeado; nada disto muda número de dispositivo",
            "veredito_estatuto": str(ep.get("verdict") or "")[:200]}
'''
troca('''    v391 = conferir_v391_no_cofre(core, selo)        # camada v391 (item 13); fail-closed
''', '''    v391 = conferir_v391_no_cofre(core, selo)        # camada v391 (item 13); fail-closed
    v394 = conferir_v394_no_cofre(core, selo)        # camada v394 (item 14); fail-closed
''', "chamada v394")
troca('''            "camada_v386_no_cofre": v386, "camada_v389_no_cofre": v389, "camada_v390_no_cofre": v390, "camada_v391_no_cofre": v391}''',
      '''            "camada_v386_no_cofre": v386, "camada_v389_no_cofre": v389, "camada_v390_no_cofre": v390, "camada_v391_no_cofre": v391,
            "camada_v394_no_cofre": v394}''', "retorno v394")
troca('''

def conferir_no_cofre(rt: dict) -> dict:''', FUNC + '''

def conferir_no_cofre(rt: dict) -> dict:''', "funcao conferir_v394_no_cofre")
troca('''                     "ESTATUTO_DA_PROVA_PROVADA_FECHO_LOGICO_TRES_PROVAS__CONFIRMACAO_E_CREDITACAO__BETA_NA_NATUREZA_ESPERA_5_SIGMA__"''',
      '''                     "ESTATUTO_DA_PROVA_PROVADA_FECHO_LOGICO_TRES_PROVAS__CONFIRMACAO_E_CREDITACAO__BETA_NA_NATUREZA_ESPERA_5_SIGMA__"
                     "REGISTROS_V392_V393_V394_VERIFICADOS_SEM_GATE__ESCADA_EM_BANDEIRAS__REDE_DE_FOCK_CONTRATO_CONJUNTO_ABERTO__"''', "veredito da camada")
troca('''                          "que a natureza tenha decidido β_TGL (o estatuto da v391 diz: espera 5σ) ou que a creditação tenha sido dada (é ato de terceiros)"],''',
      '''                          "que a natureza tenha decidido β_TGL (o estatuto da v391 diz: espera 5σ) ou que a creditação tenha sido dada (é ato de terceiros)",
                          "ERRATA AO LADO (v394, 19/10/2026): onde o item acima diz que não se afirma «a lei de campo no curvo ser termo de kernel», leia-se: desde a v392 ela é termo de kernel CONDICIONAL ao H3 nomeado (lei_de_campo_curvo_v392); não se afirma o H3 em toda tela nem existência global",
                          "que o contrato conjunto da rede de Fock esteja habitado, que o H3 valha em toda direção nula, ou que o coração tenha evidência espectral independente do CODATA (a v394 diz: aberto; aberto; ausente)"],''',
      "nao_se_afirma v394")
troca('''    "estatuto_da_prova_v391": r"estatuto_da_prova|creditac|accreditation",''',
      '''    "estatuto_da_prova_v391": r"estatuto_da_prova|creditac|accreditation",
    # v394: a rede de Fock, o relógio M2, a regra quadrática, o coração — mede se algum dispositivo os cita; não interpreta
    "registros_v392_v394": r"rede_fock|tempo_frequencia|regra_quadratica|coracao_e_selo|criterio_binario|Fock",''', "USOS v394")

tmp = P + ".tmp_v394"
open(tmp, "wb").write(s.encode("utf-8"))
r = subprocess.run([sys.executable, "-m", "py_compile", tmp], capture_output=True, text=True)
if r.returncode != 0:
    os.remove(tmp)
    raise SystemExit("SINTAXE INVALIDA — nada trocado:\n" + (r.stderr or "")[:1500])
os.replace(tmp, P)
print("modulo v394: %d -> %d bytes | py_compile OK | backup .bak_v394_%s" % (len(raw), os.path.getsize(P), TS))
