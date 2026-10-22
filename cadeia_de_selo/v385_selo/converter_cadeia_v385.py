# -*- coding: utf-8 -*-
"""Gera os scripts MECANICOS da cadeia pos-rito v385 a partir dos da v384 (v384_selo), trocando so nomes: v384 -> v385 e v383 -> v384 (nessa ordem), e os
sufixos de backup (_p384 -> _p385 ...). Os nomes que sao CHAVES do core/selo, ou artefatos da v384 que a v385 le, ficam PROTEGIDOS (placeholder antes da
troca, restaurados depois). Os «molde: X_v383.py» viram «molde: X_v384.py» (o molde da v385 e' a cadeia da v384). Nunca sobrescreve um arquivo que ja
exista em v385_selo (as adaptacoes de conteudo sao feitas a mao depois). Imprime quantas linhas mudaram por arquivo, para a revisao.
ERRATA AO LADO (05/10, 1a geracao): a regex dos sufixos de backup pegava tambem _v384 (vindo de _v383) e o empurrava a _v385; agora os sufixos sao trocados
ANTES das versoes e o 'v' fica de fora."""
import os, re, sys, difflib
sys.stdout.reconfigure(encoding="utf-8")
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(SP, "v384_selo"); DST = os.path.join(SP, "v385_selo")
ARQS = ["ambiente_v384.py", "espera_rito_v384.py", "preparar_conferidor_ensaio_v384.py", "conferir_reais_intocados_v384.py", "compactar_memory_para_v384.py",
        "chain_pos_rito_v384.sh", "arquivar_v384.py", "manifesto_v384.py", "patch_arvore_indice_v384.py", "superficies_v384.py", "registrar_resultado_v384.py",
        "leitura_v384.py", "textos_v384.py", "handoff_v384.py", "montar_nos_sintetico_v384.py", "ensaio_v384.py"]
PROTEGE = ["the_quantum_pillar_reading_v384", "quantum_pillar_start_v384", "quantum_pillar_finish_v384", "quantum_pillar_v384", "[v384]", "\\[v384\\]",
           "the_ledger_of_charges_v383", "v384-pilar-quantico-gpu-02out", "fumaca_v384", "conferir_congelamento_v384", "pilar_v384_rodada_completa",
           "pilar_v384_cadeia_ate_o_rito", "pilar_v384_rascunhos_b_reduzido_e_a", "pilar_v384_conferencia_do_congelamento"]
Z = chr(0)


def converte(s):
    ph = {}
    for i, t in enumerate(sorted(PROTEGE, key=len, reverse=True)):
        k = Z + "P%02d" % i + Z; ph[k] = t; s = s.replace(t, k)
    # o molde: «molde: X_v383.py» -> «molde: X_v384.py» (protegido antes da troca)
    s = re.sub(r"(molde: [A-Za-z_]+)_v383", lambda m: m.group(1) + "_" + Z + "MOLDE" + Z, s)
    # os sufixos de backup (_p384, _sup384, _comp384, _handoff384, mapa384), ANTES das versoes; nunca _v38x
    s = re.sub(r"(_(?!v)[a-z]+)384\b", lambda m: m.group(1) + Z + "S" + Z, s)
    s = re.sub(r"(_(?!v)[a-z]+)383\b", lambda m: m.group(1) + "384", s)
    s = s.replace("mapa384", "mapa" + Z + "S" + Z)
    s = s.replace("v384", Z + "N" + Z).replace("V384", Z + "M" + Z)
    s = s.replace("v383", "v384").replace("V383", "V384")
    s = s.replace(Z + "N" + Z, "v385").replace(Z + "M" + Z, "V385").replace(Z + "S" + Z, "385").replace(Z + "MOLDE" + Z, "v384")
    for k, t in ph.items():
        s = s.replace(k, t)
    assert Z not in s
    return s


os.makedirs(DST, exist_ok=True)
for a in ARQS:
    src = os.path.join(SRC, a); dst = os.path.join(DST, a.replace("v384", "v385"))
    if os.path.exists(dst):
        print("== %s: JA EXISTE em v385_selo (nao sobrescrevo)" % os.path.basename(dst)); continue
    s = open(src, encoding="utf-8", newline="").read(); n = converte(s)
    with open(dst + ".tmp", "w", encoding="utf-8", newline="") as f:
        f.write(n)
    os.replace(dst + ".tmp", dst)
    d = [l for l in difflib.unified_diff(s.splitlines(), n.splitlines(), lineterm="", n=0) if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]
    print("== %s -> %s: %d linha(s) mudaram" % (a, os.path.basename(dst), len(d) // 2))
