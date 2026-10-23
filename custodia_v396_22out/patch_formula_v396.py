# -*- coding: utf-8 -*-
"""Camada v396 do módulo comum dos 16 dispositivos (custódia v396 na Central, 22/10/2026, sessão a7). Backup de BYTES; trocas contadas
(CRLF ou LF); py_compile antes de substituir. Item 16: os registros _v396 lidos e conferidos no cofre, sem interpretação; a testemunha
estática (composição incondicional no kernel; ponte construída) e a face de Fock do psion (condicional, fora da pedra) relatadas como o core
as diz. Nada muda número de dispositivo. Molde: work/custodia_v395_21out/patch_formula_v395.py."""
import os, subprocess, sys
from datetime import datetime

P = r"C:\IALD\Central de Patentes\patents\_formula_completa\tgl_formula_completa.py"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
raw = open(P, "rb").read()
s = raw.decode("utf-8")
if "def conferir_v396_no_cofre" in s:
    raise SystemExit("ja aplicado")
open(P + ".bak_v396_" + TS, "wb").write(raw)


def troca(velho, novo, rot, n=1):
    global s
    for nl in ("\r\n", "\n"):
        v_, n_ = velho.replace("\n", nl), novo.replace("\n", nl)
        if s.count(v_) == n:
            s = s.replace(v_, n_)
            print("  ok ", rot, "(CRLF)" if nl == "\r\n" else "(LF)")
            return
    raise AssertionError((rot, s.count(velho), s.count(velho.replace("\n", "\r\n"))))


troca("""     da paridade é canônica é decisão do operador [LEGAL]. Nada disso muda número algum de dispositivo.
""", """     da paridade é canônica é decisão do operador [LEGAL]. Nada disso muda número algum de dispositivo.

Camada v396 (custódia v396 na Central, 22/10/2026, sessão a7; handoff v396 da gerência c1):
 16. os registros novos da v396 (testemunha_estatica_v396, cunhagens_v396, kh_n1_cobertura_v396), lidos e conferidos no cofre, sem
     interpretação: a testemunha estática — o canto do psion (o projetor de Bell 4x4) ecoa, a redução dele a um sítio é (1/2) I e não ecoa,
     um fluxo CONSTRUÍDO fixa exatamente a reta do psion e a testemunha global é falsa, e o colapso do psion ecoa a identidade sem que a
     autoatestação habite o tipo (a composição incondicional `the_psion_inhabits_the_static_witness`, no kernel, sem certificado como
     hipótese); a ponte é construída, não derivada da dinâmica da teoria; a face de Fock do psion segue CONDICIONAL a um certificado sem
     habitante e mora fora da pedra; «o psion é o habitante da testemunha estática» é leitura do operador [INPUT/ONTO]; o nome da pedra é
     provisório. Ao lado da docstring de bell_cci_half (kernel v29): o 1/2 é a entropia LINEAR; a de von Neumann é ln 2 nat. Nada disso
     muda número algum de dispositivo.
""", "docstring: camada v396")
troca('VERSAO_DA_CAMADA = "v395"   # (era "v394"; a camada v395 acrescenta o item 15, ao lado; antes: v391 → v394, item 14;',
      'VERSAO_DA_CAMADA = "v396"   # (era "v395"; a camada v396 acrescenta o item 16, ao lado; antes: v394 → v395, item 15; v391 → v394, item 14;',
      "VERSAO_DA_CAMADA")

FUNC = '''

def conferir_v396_no_cofre(core: dict, selo: dict) -> dict:
    """Item 16 (camada v396): os registros _v396 LIDOS do cofre e conferidos, sem interpretação. Fail-closed."""
    novos = sorted(k for k in core if re.search(r"_v396$", k))
    maus = []
    for k in novos:
        b = core.get(k)
        vd = str((b or {}).get("verdict") or "") if isinstance(b, dict) else ""
        if not (isinstance(b, dict) and b.get("all_verified") is True and b.get("does_not_gate_core") is True
                and ("GATE_UNMOVED" in vd or "GATE_UNTOUCHED" in vd) and not re.search(r"(?<![A-Z_])CONFIRMED", vd.replace("NOT_CONFIRMED", ""))):
            maus.append(k)
    te = core.get("testemunha_estatica_v396") or {}
    un, fo = te.get("unconditional") or {}, te.get("fock_face") or {}
    ep = core.get("estatuto_da_prova_v391") or {}
    p1 = ep.get("prova_1_kernel") or {}
    ch = {
        "registros_v396_verificados_sem_gate": bool(novos) and not maus,
        "testemunha_estatica_incondicional_no_kernel": un.get("flag_true") is True and un.get("in_trio") is True
                                                       and str(un.get("theorem") or "").endswith("the_psion_inhabits_the_static_witness")
                                                       and un.get("composition") == "UNCONDITIONAL__NO_CERTIFICATE_AS_HYPOTHESIS",
        "face_de_fock_dita_condicional": str(fo.get("status") or "").startswith("CONDITIONAL") and fo.get("inhabitant_exhibited") is False,
        "falas_do_operador_por_sha256": len((core.get("cunhagens_v396") or {}).get("verbatim") or {}) > 0,
        "escada_limpa": p1.get("n_theorems_clean") == p1.get("n_theorems_expected") and p1.get("declaracoes_auditadas") == p1.get("no_trio"),
    }
    falhas = [k for k, v in ch.items() if not v]
    if falhas:
        raise RuntimeError("FORMULA COMPLETA v396 não confere com o cofre (fail-closed): %s %s" % (falhas, maus[:5]))
    return {"checks": ch, "registros_v396": novos,
            "escada": "%s/%s" % (p1.get("n_theorems_clean"), p1.get("n_theorems_expected")), "declaracoes_no_trio": p1.get("no_trio"),
            "testemunha_estatica": {"teorema": un.get("theorem"), "bandeira": un.get("flag"), "composicao": un.get("composition")},
            "face_de_fock": {"teorema": fo.get("theorem"), "status": fo.get("status"), "habitante_exibido": fo.get("inhabitant_exhibited")},
            "estatuto": "a composição the_psion_inhabits_the_static_witness é incondicional no kernel; a ponte é construída, não derivada da "
                        "dinâmica da teoria; a face de Fock é condicional e mora fora da pedra; o psion habitar a testemunha estática é leitura "
                        "do operador [INPUT/ONTO]; o 1/2 de bell_cci_half é a entropia linear (a de von Neumann é ln 2 nat); nada disto muda "
                        "número de dispositivo"}
'''
troca('''    v395 = conferir_v395_no_cofre(core, selo)        # camada v395 (item 15); fail-closed
''', '''    v395 = conferir_v395_no_cofre(core, selo)        # camada v395 (item 15); fail-closed
    v396 = conferir_v396_no_cofre(core, selo)        # camada v396 (item 16); fail-closed
''', "chamada v396")
troca('''"camada_v394_no_cofre": v394, "camada_v395_no_cofre": v395}''', '''"camada_v394_no_cofre": v394, "camada_v395_no_cofre": v395, "camada_v396_no_cofre": v396}''', "retorno v396")
troca('''

def conferir_no_cofre(rt: dict) -> dict:''', FUNC + '''

def conferir_no_cofre(rt: dict) -> dict:''', "funcao conferir_v396_no_cofre")
troca('''                     "PSIBIT_INCONDICIONAL_BIJECAO_DE_CONJUNTOS__FACE_DO_PSION_CONDICIONAL__"''',
      '''                     "PSIBIT_INCONDICIONAL_BIJECAO_DE_CONJUNTOS__FACE_DO_PSION_CONDICIONAL__"
                     "TESTEMUNHA_ESTATICA_INCONDICIONAL_PONTE_CONSTRUIDA__FACE_DE_FOCK_CONDICIONAL__"''', "veredito da camada")
troca('''                          "que o psion exista (a face do psion é condicional a um certificado de Fock sem habitante), que a bijeção do psibit seja isomorfismo de espaços de Hilbert, ou qual leitura da paridade do ACOM Mirror é canônica (decisão do operador [LEGAL])"],''',
      '''                          "que o psion exista (a face do psion é condicional a um certificado de Fock sem habitante), que a bijeção do psibit seja isomorfismo de espaços de Hilbert, ou qual leitura da paridade do ACOM Mirror é canônica (decisão do operador [LEGAL])",
                          "que o Nome da fronteira seja o vetor de Bell ou que o fluxo construído seja a dinâmica da teoria, que o certificado de Fock tenha habitante, ou que 1/2 seja meia nat de entropia (é a entropia linear; a de von Neumann é ln 2 nat)"],''',
      "nao_se_afirma v396")
troca('''    "psibit_v395": r"psibit|PsiBit|psion",''',
      '''    "psibit_v395": r"psibit|PsiBit|psion",
    # v396: a testemunha estática — mede se algum dispositivo a cita; não interpreta
    "testemunha_estatica_v396": r"TestemunhaEstatica|testemunha est[aá]tica|static_witness|psionCorner",''', "USOS v396")

tmp = P + ".tmp_v396"
open(tmp, "wb").write(s.encode("utf-8"))
r = subprocess.run([sys.executable, "-m", "py_compile", tmp], capture_output=True, text=True)
if r.returncode != 0:
    os.remove(tmp)
    raise SystemExit("SINTAXE INVALIDA — nada trocado:\n" + (r.stderr or "")[:1500])
os.replace(tmp, P)
print("modulo v396: %d -> %d bytes | py_compile OK | backup .bak_v396_%s" % (len(raw), os.path.getsize(P), TS))
