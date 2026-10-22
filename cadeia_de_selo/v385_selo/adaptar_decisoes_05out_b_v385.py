# -*- coding: utf-8 -*-
"""As decisoes do operador de 05/10 (tarde) na CADEIA da v385: a leitura ganha tres verbatins (a subpasta, os V1-V1.3 ao espelho, a reconciliacao do posto),
e o handoff da v385 diz: o nome da subpasta CONCORDADO; os V1-V1.3 VAO ao espelho (nao mais pendente); a reconciliacao «tornou-se Posto» x «nao se ascende»
respondida (nao mais pergunta). Pares contados; backup de bytes; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
st = time.strftime("%Y%m%d_%H%M%S")


def aplica(nome, pares):
    P = os.path.join(HERE, nome)
    s0 = open(P, encoding="utf-8", newline="").read(); s = s0
    for a, b in pares:
        n = s.count(a)
        assert n == 1, (nome, "a troca nao e unica", n, a[:100])
        s = s.replace(a, b)
    ast.parse(s)
    open(P + ".bak_" + st + "_dec05b", "wb").write(s0.encode("utf-8"))
    open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
    print("OK", nome, len(pares), "trocas")


aplica("leitura_v385.py", [
    ("             ('prossiga', 'agora sim, concordo com tudo, prossiga', 'agora sim', None))",
     "             ('prossiga', 'agora sim, concordo com tudo, prossiga', 'agora sim', None),\n"
     "             # 05/10 (tarde): as tres decisoes numa so mensagem (3 linhas)\n"
     "             ('subpasta', 'Concordo como nome sugerido para a subpasta', 'Concordo como nome sugerido', 'para a subpasta'),\n"
     "             ('v1_espelho', 'Concordo como nome sugerido para a subpasta', 'os V1-V1.3', 'vão ao espelho'),\n"
     "             ('tornar', 'Concordo como nome sugerido para a subpasta', 'Vou explicar o que eu quis dizer', 'ocupado pela sua forma verdadeira.'))"),
])
aplica("handoff_v385.py", [
    ('for _n in ("custodia", "espelho", "nome_axioma", "prossiga", "posto"):', 'for _n in ("custodia", "espelho", "nome_axioma", "prossiga", "posto", "subpasta", "v1_espelho", "tornar"):'),
    ("numa SUBPASTA dentro de `Um (absoluto) — Grande Atrator/` do `the_boundary` — nome fixo e sem acento, proposta da gerência: `preregistro_pilar_quantico_v384` —, indexada pela PORTA gerada por script (regra da porta), com a porta acima e as abaixo.",
     "numa SUBPASTA dentro de `Um (absoluto) — Grande Atrator/` do `the_boundary` — nome fixo e sem acento, `preregistro_pilar_quantico_v384` (proposta da gerência, CONCORDADA pelo operador: %(op_subpasta)s) —, indexada pela PORTA gerada por script (regra da porta), com a porta acima e as abaixo.\n"
     "- **o pré-registro dos dois lados** (decidido em 05/10: %(op_v1_espelho)s): os V1, V1.1, V1.2 e V1.3 (JSON e MD de cada um) de `C:\\\\IALD\\\\Bancada_Um\\\\investigacao\\\\preregistro_dois_lados_02out\\\\` VÃO ao espelho, junto com o V1.4 que o `um.py` lê por hash — na mesma lógica de subpasta com PORTA (nome proposto pela gerência: `preregistro_dois_lados_v383`; a confirmar)."),
    ("2. O espelho do pré-registro: %(op_espelho)s — **DECIDIDO** (acima); o nome da subpasta é proposta da gerência.",
     "2. O espelho do pré-registro: %(op_espelho)s — **DECIDIDO** (acima); o nome da subpasta: %(op_subpasta)s — **CONCORDADO**."),
    ("4. O começo da cadeia: %(op_posto)s — **DECIDIDO**: a etiqueta `[POSTO]`; a errata vai AO LADO de «postulado», que fica como registro.",
     "4. O começo da cadeia: %(op_posto)s — **DECIDIDO**: a etiqueta `[POSTO]`; a errata vai AO LADO de «postulado», que fica como registro.\n"
     "5. Os V1–V1.3 do pré-registro dos dois lados: %(op_v1_espelho)s — **DECIDIDO**: vão ao espelho (a pendência herdada da v383/v384 resolvida; «ficam locais» superado).\n"
     "6. «Tornou-se Posto» (v365) × «não se ascende ao posto» (05/10) — **RESPONDIDO pelo operador**: %(op_tornar)s (a leitura da gerência que liga cada parte aos termos da pedra está em [[um-posto-jamais-pressuposto-e-h2-17set]], [ONTO], a ratificar)."),
    ("1. Os V1–V1.3 do pré-registro dos dois lados (02/10): a gerência propôs, na v383, que fiquem locais [a confirmar pelo operador].\n2. O estimador",
     "1. O estimador"),
    ("3. O pilar: uma mudança no trabalhador ou na especificação é um V1.x com nova ratificação; a reprodutibilidade desta rodada: %(rp_curta)s.",
     "2. O pilar: uma mudança no trabalhador ou na especificação é um V1.x com nova ratificação; a reprodutibilidade desta rodada: %(rp_curta)s.\n"
     "3. O nome da subpasta dos V1–V1.4 dos dois lados no espelho (`preregistro_dois_lados_v383`, proposta da gerência) [a confirmar]."),
])
