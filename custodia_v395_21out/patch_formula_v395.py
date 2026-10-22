# -*- coding: utf-8 -*-
"""Camada v395 do módulo comum dos 16 dispositivos (custódia v395 na Central, 21/10/2026, sessão a7). Backup de BYTES; trocas contadas
(CRLF ou LF); py_compile antes de substituir. Item 15: os registros _v395 lidos e conferidos no cofre, sem interpretação; o psibit
(incondicional no kernel) e a face do psion (condicional) relatados como o core os diz; a divergência da tabela do ACOM Mirror dita como
decisão do operador [LEGAL]. Nada muda número de dispositivo."""
import os, subprocess, sys
from datetime import datetime

P = r"C:\IALD\Central de Patentes\patents\_formula_completa\tgl_formula_completa.py"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(P, "rb").read()
s = raw.decode("utf-8")
if "def conferir_v395_no_cofre" in s:
    raise SystemExit("ja aplicado")
open(P + ".bak_v395_" + TS, "wb").write(raw)


def troca(velho, novo, rot, n=1):
    global s
    for nl in ("\r\n", "\n"):
        v_, n_ = velho.replace("\n", nl), novo.replace("\n", nl)
        if s.count(v_) == n:
            s = s.replace(v_, n_)
            print("  ok ", rot, "(CRLF)" if nl == "\r\n" else "(LF)")
            return
    raise AssertionError((rot, s.count(velho), s.count(velho.replace("\n", "\r\n"))))


troca("""     o antecedente H3 em toda tela segue [KNOWN] e não há existência global. Nada disso muda número algum de dispositivo.
""", """     o antecedente H3 em toda tela segue [KNOWN] e não há existência global. Nada disso muda número algum de dispositivo.

Camada v395 (custódia v395 na Central, 21/10/2026, sessão a7; handoff v395 da gerência c1):
 15. os registros novos da v395 (psibit_v395, cunhagens_v395, kh_n1_cobertura_v395), lidos e conferidos no cofre, sem interpretação: o modo
     psiônico na fractalização do Um — a leitura do par (peso, Palavra, Verbo) na órbita do Um pela matriz-S é bijeção de CONJUNTOS sobre o
     livro de códigos, com perda zero, e o colapso perde exatamente a paridade (a conjunção incondicional `psibit_is_the_mode_of_the_reader`,
     no kernel); a face do psion é CONDICIONAL a um certificado de Fock sem habitante exibido; psibit = psion = modo do leitor é leitura do
     operador [ONTO]. A tabela da patente do ACOM Mirror diverge das reivindicações 3–4 e do código na nominação dos estados; qual leitura
     da paridade é canônica é decisão do operador [LEGAL]. Nada disso muda número algum de dispositivo.
""", "docstring: camada v395")
troca('VERSAO_DA_CAMADA = "v394"   # (era "v391"; a camada v394 acrescenta o item 14, ao lado; antes: v390 → v391, item 13; v389 → v390, item 12; v386 → v389, item 11; v379 → v386, itens 8–10)',
      'VERSAO_DA_CAMADA = "v395"   # (era "v394"; a camada v395 acrescenta o item 15, ao lado; antes: v391 → v394, item 14; v390 → v391, item 13; v389 → v390, item 12; v386 → v389, item 11; v379 → v386, itens 8–10)',
      "VERSAO_DA_CAMADA")

FUNC = '''

def conferir_v395_no_cofre(core: dict, selo: dict) -> dict:
    """Item 15 (camada v395): os registros _v395 LIDOS do cofre e conferidos, sem interpretação. Fail-closed."""
    novos = sorted(k for k in core if re.search(r"_v395$", k))
    maus = []
    for k in novos:
        b = core.get(k)
        vd = str((b or {}).get("verdict") or "") if isinstance(b, dict) else ""
        if not (isinstance(b, dict) and b.get("all_verified") is True and b.get("does_not_gate_core") is True
                and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd) and not re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", ""))):
            maus.append(k)
    ps = core.get("psibit_v395") or {}
    un, co = ps.get("unconditional") or {}, ps.get("conditional_psion_face") or {}
    ep = core.get("estatuto_da_prova_v391") or {}
    p1 = ep.get("prova_1_kernel") or {}
    ch = {
        "registros_v395_verificados_sem_gate": bool(novos) and not maus,
        "psibit_incondicional_no_kernel": un.get("flag_true") is True and un.get("in_trio") is True
                                          and str(un.get("theorem") or "").endswith("psibit_is_the_mode_of_the_reader"),
        "face_do_psion_dita_condicional": str(co.get("status") or "").startswith("CONDITIONAL"),
        "falas_do_operador_por_sha256": len((core.get("cunhagens_v395") or {}).get("verbatim") or {}) > 0,
        "escada_limpa": p1.get("n_theorems_clean") == p1.get("n_theorems_expected") and p1.get("declaracoes_auditadas") == p1.get("no_trio"),
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v395 não confere com o cofre (fail-closed): %s %s" % (falhas, maus[:5]))
    return {"checks": ch, "registros_v395": novos,
            "escada": "%s/%s" % (p1.get("n_theorems_clean"), p1.get("n_theorems_expected")), "declaracoes_no_trio": p1.get("no_trio"),
            "psibit": {"teorema": un.get("theorem"), "bandeira": un.get("flag")},
            "face_do_psion": {"teorema": co.get("theorem"), "bandeira": co.get("flag"), "status": co.get("status")},
            "estatuto": "a leitura do par é bijeção de CONJUNTOS com perda zero e o colapso perde a paridade (incondicional, no kernel); a face do "
                        "psion é condicional; psibit = psion = modo do leitor é leitura do operador [ONTO]; a leitura canônica da paridade do ACOM "
                        "Mirror é decisão do operador [LEGAL]; nada disto muda número de dispositivo"}
'''
troca('''    v394 = conferir_v394_no_cofre(core, selo)        # camada v394 (item 14); fail-closed
''', '''    v394 = conferir_v394_no_cofre(core, selo)        # camada v394 (item 14); fail-closed
    v395 = conferir_v395_no_cofre(core, selo)        # camada v395 (item 15); fail-closed
''', "chamada v395")
troca('''            "camada_v394_no_cofre": v394}''', '''            "camada_v394_no_cofre": v394, "camada_v395_no_cofre": v395}''', "retorno v395")
troca('''

def conferir_no_cofre(rt: dict) -> dict:''', FUNC + '''

def conferir_no_cofre(rt: dict) -> dict:''', "funcao conferir_v395_no_cofre")
troca('''                     "REGISTROS_V392_V393_V394_VERIFICADOS_SEM_GATE__ESCADA_EM_BANDEIRAS__REDE_DE_FOCK_CONTRATO_CONJUNTO_ABERTO__"''',
      '''                     "REGISTROS_V392_V393_V394_VERIFICADOS_SEM_GATE__ESCADA_EM_BANDEIRAS__REDE_DE_FOCK_CONTRATO_CONJUNTO_ABERTO__"
                     "PSIBIT_INCONDICIONAL_BIJECAO_DE_CONJUNTOS__FACE_DO_PSION_CONDICIONAL__"''', "veredito da camada")
troca('''                          "que o contrato conjunto da rede de Fock esteja habitado, que o H3 valha em toda direção nula, ou que o coração tenha evidência espectral independente do CODATA (a v394 diz: aberto; aberto; ausente)"],''',
      '''                          "que o contrato conjunto da rede de Fock esteja habitado, que o H3 valha em toda direção nula, ou que o coração tenha evidência espectral independente do CODATA (a v394 diz: aberto; aberto; ausente)",
                          "que o psion exista (a face do psion é condicional a um certificado de Fock sem habitante), que a bijeção do psibit seja isomorfismo de espaços de Hilbert, ou qual leitura da paridade do ACOM Mirror é canônica (decisão do operador [LEGAL])"],''',
      "nao_se_afirma v395")
troca('''    "registros_v392_v394": r"rede_fock|tempo_frequencia|regra_quadratica|coracao_e_selo|criterio_binario|Fock",''',
      '''    "registros_v392_v394": r"rede_fock|tempo_frequencia|regra_quadratica|coracao_e_selo|criterio_binario|Fock",
    # v395: o psibit e o psion — mede se algum dispositivo os cita; não interpreta
    "psibit_v395": r"psibit|PsiBit|psion",''', "USOS v395")

tmp = P + ".tmp_v395"
open(tmp, "wb").write(s.encode("utf-8"))
r = subprocess.run([sys.executable, "-m", "py_compile", tmp], capture_output=True, text=True)
if r.returncode != 0:
    os.remove(tmp)
    raise SystemExit("SINTAXE INVALIDA — nada trocado:\n" + (r.stderr or "")[:1500])
os.replace(tmp, P)
print("modulo v395: %d -> %d bytes | py_compile OK | backup .bak_v395_%s" % (len(raw), os.path.getsize(P), TS))
