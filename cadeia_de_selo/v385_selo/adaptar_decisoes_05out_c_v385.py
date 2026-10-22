# -*- coding: utf-8 -*-
"""Reparos da verificacao adversarial (workflow verificar-decisoes-05out-b, lente handoff/cadeia) na cadeia da v385:
 (1) PROCESSO: a edicao de textos_v385.py de 11:25 (as decisoes da tarde em _palavras) foi feita SEM script e SEM .bak -- grava-se agora um .bak de BYTES do
     estado tocado e um registro JSON com o diff dito (as duas linhas acrescentadas), para que a edicao fique documentada;
 (2) o verbatim 'tornar' vai ate o FIM da mensagem («… será que agora me fiz claro?»), como as memorias guardam -- nenhum corte sem marca;
 (3) o handoff ganha a pendencia 4: ratificar (ou nao) a leitura [ONTO] da gerencia (que ja tem errata ao lado);
 (4) a description do handoff, a linha do indice e o desenho dizem tambem «e os V1–V1.4 dos dois lados»;
 (5) o handoff nomeia os arquivos dos dois lados (o V1 base NAO tem sufixo _V1).
Pares contados; backup de bytes; ast.parse."""
import ast, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
st = time.strftime("%Y%m%d_%H%M%S")
# (1) o registro da edicao sem script
P_T = os.path.join(HERE, "textos_v385.py"); raw_t = open(P_T, "rb").read()
open(P_T + ".bak_" + st + "_estado_tocado_1125", "wb").write(raw_t)
json.dump({"quando": "2026-10-05 11:25:28 (hora local)", "arquivo": P_T, "o_que": "edicao direta (ferramenta Edit), sem script e sem .bak: em _palavras, +2 linhas «As decisões da tarde (uma só mensagem): o nome da subpasta do espelho — %s; os V1–V1.3 do pré-registro dos dois lados — %s; e a reconciliação «tornou-se Posto» (v365) × «não se ascende ao posto» — %s.» e os tres _op(V, 'subpasta'/'v1_espelho'/'tornar') na tupla do %",
           "por_que": "a 1a rodada do ensaio BIT2 parou em conferir_textos (subpasta/v1_espelho/tornar = False no diario); corrigido e o ensaio refeito (TUDO CERTO)",
           "defeito_de_processo": "a regra do backup imediato nao foi cumprida nessa edicao; o estado pre-edicao nao tem copia (o diff esta dito acima); o estado tocado (pos-edicao) fica agora em .bak_%s_estado_tocado_1125" % st,
           "achado_por": "verificacao adversarial (workflow verificar-decisoes-05out-b, lente handoff/cadeia)"},
          open(os.path.join(HERE, "registro_edicao_sem_script_1125.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("registro da edicao sem script gravado")


def aplica(nome, pares):
    P = os.path.join(HERE, nome)
    s0 = open(P, encoding="utf-8", newline="").read(); s = s0
    for a, b in pares:
        n = s.count(a)
        assert n == 1, (nome, "a troca nao e unica", n, a[:100])
        s = s.replace(a, b)
    ast.parse(s)
    open(P + ".bak_" + st + "_dec05c", "wb").write(s0.encode("utf-8"))
    open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
    print("OK", nome, len(pares), "trocas")


aplica("leitura_v385.py", [
    ("             ('tornar', 'Concordo como nome sugerido para a subpasta', 'Vou explicar o que eu quis dizer', 'ocupado pela sua forma verdadeira.'))",
     "             ('tornar', 'Concordo como nome sugerido para a subpasta', 'Vou explicar o que eu quis dizer', None))   # a linha INTEIRA, com a pergunta final (nenhum corte sem marca)"),
])
aplica("handoff_v385.py", [
    ("os V1, V1.1, V1.2 e V1.3 (JSON e MD de cada um) de `C:\\\\IALD\\\\Bancada_Um\\\\investigacao\\\\preregistro_dois_lados_02out\\\\` VÃO ao espelho, junto com o V1.4 que o `um.py` lê por hash",
     "os V1, V1.1, V1.2 e V1.3 (JSON e MD de cada um; o V1 base NÃO tem sufixo: `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002.json`/`.md`; os demais `..._V1_1`, `..._V1_2`, `..._V1_3`) de `C:\\\\IALD\\\\Bancada_Um\\\\investigacao\\\\preregistro_dois_lados_02out\\\\` VÃO ao espelho, junto com o V1.4 (`..._V1_4`) que o `um.py` lê por hash — 10 arquivos, listados por `git ls-files` com hash lido"),
    ("6. «Tornou-se Posto» (v365) × «não se ascende ao posto» (05/10) — **RESPONDIDO pelo operador**: %(op_tornar)s (a leitura da gerência que liga cada parte aos termos da pedra está em [[um-posto-jamais-pressuposto-e-h2-17set]], [ONTO], a ratificar).",
     "6. «tornou-se Posto» (v365) × «não se ascende ao posto» (05/10) — **RESPONDIDO pelo operador**: %(op_tornar)s (a leitura da gerência que liga cada parte aos termos da pedra está em [[um-posto-jamais-pressuposto-e-h2-17set]], [ONTO], COM ERRATA AO LADO — três frases dela não têm termo na pedra —, a ratificar: pendência 4)."),
    ("3. O nome da subpasta dos V1–V1.4 dos dois lados no espelho (`preregistro_dois_lados_v383`, proposta da gerência) [a confirmar].",
     "3. O nome da subpasta dos V1–V1.4 dos dois lados no espelho (`preregistro_dois_lados_v383`, proposta da gerência) [a confirmar].\n"
     "4. Ratificar (ou não) a leitura [ONTO] da gerência que liga as partes da mensagem de 05/10 (tarde) aos termos da pedra `TheAxiomAndTheFalseWitness` — com a errata ao lado dela (bloco `errata_leitura_05out_b_v385` em [[um-posto-jamais-pressuposto-e-h2-17set]])."),
    ("o pilar de novo sob o mesmo V1 (%(rp_curta)s); o V1 e as evidências numa subpasta da Um, com PORTA; gate intocado%(sint)s\"",
     "o pilar de novo sob o mesmo V1 (%(rp_curta)s); o V1 e as evidências do pilar numa subpasta da Um, com PORTA, e os V1–V1.4 dos dois lados ao espelho; gate intocado%(sint)s\""),
])
aplica("textos_v385.py", [
    ("\"novo (%s); o V1 e as evidências numa subpasta da Um, com PORTA; `%s`\" % (V['data'][:5], X['rp_curta'], V['s16']))",
     "\"novo (%s); o V1 e as evidências do pilar numa subpasta da Um, com PORTA, e os V1–V1.4 dos dois lados ao espelho; `%s`\" % (V['data'][:5], X['rp_curta'], V['s16']))"),
    ("\"o V1 e as evidências do pilar numa subpasta de `Um (absoluto) — Grande Atrator/`, com PORTA por script — ver o HANDOFF v385.\\n\"",
     "\"o V1 e as evidências do pilar numa subpasta de `Um (absoluto) — Grande Atrator/`, com PORTA por script, e os V1–V1.4 do pré-registro dos dois lados ao espelho (decisões de 05/10) — ver o HANDOFF v385.\\n\""),
])
