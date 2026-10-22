# -*- coding: utf-8 -*-
"""Disposicoes da afericao de TEXTO da v385 no gerador do candidato (gerar_candidato_v385.py):
 achado 4: 22 declaracoes da pedra (a forma exponencial) + 7 do TheDarkSplit = 29; as contagens das mensagens, LIDAS das listas (nada de literal);
 achado 7: a errata do .md cobre tambem «o postulado `ω(I)=1`» (L101 do .md);
 N7: a leitura do selo separa o que e' do operador (cunhagens e leituras ratificadas) e NAO carrega fatos da rodada (o TheDarkSplit auditado e o pilar
   rodado de novo estao nos registros calculados -- the_axiom_v385 e quantum_pillar_reproducibility_v385 --, nao numa string fixa).
Backup de bytes; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "gerar_candidato_v385.py")
s0 = open(P, encoding="utf-8", newline="").read(); s = s0
T = [("assert len(AXM) == 21 and len(DKS) == 7 and len(FLAGS) == 28 and len({f for f, _ in FLAGS}) == 28",
      "assert len(AXM) == len(NOMES[\"TheAxiomAndTheFalseWitness\"]) == 22 and len(DKS) == len(NOMES[\"TheDarkSplit\"]) == 7 and len(FLAGS) == 29 and len({f for f, _ in FLAGS}) == 29"),
     ('add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v385 (05/10/2026; o Axioma e a testemunha falsa -- os dois pontos fixos da leitura -- e a auditoria do TheDarkSplit): axm (21) + dks (7)" + CRLF',
      'add("V01_bandeiras", "G_PEDRAS", A01, A01 + "    # v385 (05/10/2026; o Axioma e a testemunha falsa -- os dois pontos fixos da leitura -- e a auditoria do TheDarkSplit): axm (%d) + dks (%d)" % (len(AXM), len(DKS)) + CRLF'),
     ('"_LEAN_THEOREM_FLAGS: +28 (ext_axm_ 21, ext_dks_ 7).")', '"_LEAN_THEOREM_FLAGS: +%d (ext_axm_ %d, ext_dks_ %d)." % (len(FLAGS), len(AXM), len(DKS)))'),
     ('"external_ladder: +28 (5998 -> 6026).")', '"external_ladder: +%d." % len(FLAGS))'),
     ("""            "the_axiom_reading_v385": "OPERATOR_COINAGES_2026_10_05__THE_ONE_IS_POSTED_BY_THE_OBSERVER_NOT_POSTULATED_TAG_POSTO__THE_AXIOM_IS_THE_ZERO_MODE_OF_WEIGHT_ONE_THE_DARK__'""",
      """            "the_axiom_reading_v385": "OPERATOR_COINAGES_AND_RATIFIED_READINGS_2026_10_05__THE_ONE_IS_POSTED_BY_THE_OBSERVER_NOT_POSTULATED_TAG_POSTO__THE_AXIOM_IS_THE_ZERO_MODE_OF_WEIGHT_ONE_THE_DARK__'"""),
     ("""    + 'THE_POST_IS_THE_MODULAR_ZERO__FINAL_STEP_NAMED_AXIOMA_BESIDE_THE_GATE__THE_DARK_SPLIT_AUDITED__THE_PILLAR_RERUN_UNDER_THE_SAME_V1_FOR_REPRODUCIBILITY__'""",
      """    + 'THE_POST_IS_THE_MODULAR_ZERO__FINAL_STEP_NAMED_AXIOMA_BESIDE_THE_GATE__THE_RUN_FACTS_ARE_IN_THE_COMPUTED_RECORDS_NOT_IN_THIS_STRING__'"""),
     ("""Onde abaixo se lê «o postulado irredutível», leia-se *posto*.""",
      """Onde abaixo se lê «o postulado irredutível» ou «o postulado `ω(I)=1`», leia-se *posto*."""),
     ("(2) PATCHES (count(old) == 1): bandeiras ext_axm_ (21) + ext_dks_ (7) e escada (5998 -> 6026);",
      "(2) PATCHES (count(old) == 1): bandeiras ext_axm_ (22) + ext_dks_ (7) e escada (+29, lida do core da v384);")]
for a, b in T:
    n = s.count(a)
    assert n == 1, ("a troca nao e unica", n, a[:100])
    s = s.replace(a, b)
ast.parse(s)
st = time.strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + st + "_afer2", "wb").write(s0.encode("utf-8"))
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
print("OK gerar_candidato_v385.py:", len(T), "trocas")
