# -*- coding: utf-8 -*-
"""patch de construcao (R3.4, parte 2): o FIM de ../controles_negativos_r3_4.py -- confere a presenca dos 401 controles da R3.3 e grava CONTROLES_NEGATIVOS_R3_4.json."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "controles_negativos_r3_4.py"
t = P.read_text(encoding="utf-8")


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (t.count(old), old[:120])
    t = t.replace(old, new)


sub('R33 = AQUI.parent / "R3_3"', 'R33 = AQUI.parent / "R3_3"\nGERAR_CADEIA = AQUI / "gerar_cadeia_de_selos.py"')
sub('NOVOS_R33 = [x for x in nomes if x not in set(R32_NOMES)]\n', '''R33_RES = json.loads((R33 / "CONTROLES_NEGATIVOS_R3_3.json").read_bytes())
R33_NOMES = [c["controle"] for c in R33_RES["controles"]]
faltam_r33 = sorted(set(R33_NOMES) - set(nomes))
NOVOS_R33 = [x for x in R33_NOMES if x not in set(R32_NOMES)]
NOVOS_R34 = [x for x in nomes if x not in set(R33_NOMES)]
MUDARAM_R34 = {}
for x_ in RES:
    if x_["controle"] in R33_NOMES and any(str(c_) in (VR, VR_ERRADA) for c_ in (x_.get("comando") or [])):
        MUDARAM_R34.setdefault(x_["controle"], []).append("R3.4: a familia b1 (a copia que pina o Nos REAL) usa a versao do Nos real de hoje (%s) onde a R3.3 usava v391, e o b1 e derivado da "
                                                           "producao ATUAL (B3) re-pinada para esse Nos (montar_sandbox R3.4); a recusa esperada nao mudou" % VR)
for x_, motivo_ in (("RUN_1a_pre_selo_b1_nos_real", "R3.4: contra o Nos REAL v393 (a v391 nao esta mais no caminho real) com a bateria POR VERSAO gerada por script (T12 repinado para o um.py medido); "
                                                     "as conferencias de sha usam SBM.nos_real; o recibo traz pinos_da_versao conferidos"),
                    ("RUN_1b_pre_selo_b2_nos_copia", "R3.4: a copia v391 do Nos vem da custodia (the_boundary_BACKUPS/um_v391_*) e a bateria e a POR VERSAO gerada para ela (T12 repinado, na copia, "
                                                     "para o um.py da copia): o pre-registro congelado pinava o um.py v391 no caminho real, que hoje e v393")):
    if x_ in R33_NOMES:
        MUDARAM_R34.setdefault(x_, []).append(motivo_)
''')
sub('revisao="R3.3 (13/10/2026)", raiz=', 'revisao="R3.4 (19/10/2026)", raiz=')
sub('           n_da_R3_2=len(R32_NOMES), da_R3_2_presentes',
    '           n_da_R3_3=len(R33_NOMES), da_R3_3_presentes=len(R33_NOMES) - len(faltam_r33), da_R3_3_ausentes=faltam_r33, n_novos_R3_4=len(NOVOS_R34), novos_R3_4=NOVOS_R34,' + chr(10) +
    '           controles_da_R3_3_que_mudaram_de_formato=[dict(controle=k_, motivos=v_) for k_, v_ in sorted(MUDARAM_R34.items())], n_controles_da_R3_3_que_mudaram_de_formato=len(MUDARAM_R34),' + chr(10) +
    '           gerar_bateria_sha256=sha(GEN_BAT), driver_t12_sha256=sha(DRV_BAT), gerar_cadeia_sha256=sha(GERAR_CADEIA), sandbox_manifest_sha256=sha(RAIZ / "SANDBOX_MANIFEST_R3_4.json"),' + chr(10) +
    '           n_da_R3_2=len(R32_NOMES), da_R3_2_presentes')
sub('and not faltam_r32 and not juncoes_restantes', 'and not faltam_r32 and not faltam_r33 and not juncoes_restantes')
sub('(AQUI / "CONTROLES_NEGATIVOS_R3_3.json").write_bytes(texto.encode("utf-8"))', '(AQUI / "CONTROLES_NEGATIVOS_R3_4.json").write_bytes(texto.encode("utf-8"))')
sub('''      "R3.2 presentes %d/%d" % (out["da_R3_2_presentes"], len(R32_NOMES)), "novos R3.3 %d" % len(NOVOS_R33), "%.0f s" % out["segundos"])''',
    '''      "R3.2 presentes %d/%d" % (out["da_R3_2_presentes"], len(R32_NOMES)), "R3.3 presentes %d/%d" % (out["da_R3_3_presentes"], len(R33_NOMES)), "novos R3.4 %d" % len(NOVOS_R34),
      "%.0f s" % out["segundos"])''')
P.write_text(t, encoding="utf-8", newline="")
print("ok")
