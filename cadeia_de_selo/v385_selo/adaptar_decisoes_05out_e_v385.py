# -*- coding: utf-8 -*-
"""Na cadeia da v385: (1) a frase do operador de 14:40 (a forma falsa = a projecao da testemunha falsa) -- verbatim na leitura, no diario e no handoff;
(2) a INTERVENCAO de ambiente (prioridade do trabalhador BelowNormal -> Normal as 11:47) LIDA do registro do pacote (INTERVENCAO_PRIORIDADE_v385.json) pela
leitura e DITA no diario (rodada) e no handoff, ao lado da reprodutibilidade. Pares contados; backup de bytes; ast.parse."""
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
    open(P + ".bak_" + st + "_dec05e", "wb").write(s0.encode("utf-8"))
    open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
    print("OK", nome, len(pares), "trocas")


aplica("leitura_v385.py", [
    ("             ('forma_falsa', 'tem uma coisa errada no que vc prop', 'tem uma coisa errada', None))   # 05/10 14:35: a correcao -- a forma falsa tem qualquer conteudo menos o do posto",
     "             ('forma_falsa', 'tem uma coisa errada no que vc prop', 'tem uma coisa errada', None),   # 05/10 14:35: a correcao -- a forma falsa tem qualquer conteudo menos o do posto\n"
     "             ('forma_falsa_projecao', 'a \"forma falsa\" é a projeção', 'a \"forma falsa\" é a projeção', None))   # 05/10 14:40: a forma falsa = a projecao da testemunha falsa, ela mesma a superposicao"),
    ("    _mk = os.path.join(PK, '.servidor_parado_pelo_rito')",
     "    # ---- (v385) a INTERVENCAO de ambiente durante o rito, LIDA do registro do pacote (se houver): dita no diario e no handoff, ao lado da reprodutibilidade\n"
     "    _ip = os.path.join(PK, 'INTERVENCAO_PRIORIDADE_v385.json')\n"
     "    if os.path.exists(_ip):\n"
     "        _I = json.load(open(_ip, encoding='utf-8'))\n"
     "        V['intervencao_txt'] = ('**Intervenção de ambiente durante o rito, dita (gerência, em nome próprio):** %s (%s) — motivo medido: %s; depois: %s; causa: %s; o que não muda: %s. [%s]'\n"
     "                               % (_I.get('o_que'), _I.get('quando_local'), _I.get('por_que'), _I.get('o_que_aconteceu_depois'), _I.get('causa'), _I.get('o_que_nao_muda'), _I.get('estatuto')))\n"
     "    else:\n"
     "        V['intervencao_txt'] = ''\n"
     "    _mk = os.path.join(PK, '.servidor_parado_pelo_rito')"),
])
aplica("textos_v385.py", [
    ("_op(V, 'nome_axioma'), _op(V, 'subpasta'), _op(V, 'v1_espelho'), _op(V, 'tornar'), _op(V, 'forma_falsa')))",
     "_op(V, 'nome_axioma'), _op(V, 'subpasta'), _op(V, 'v1_espelho'), _op(V, 'tornar'), _op(V, 'forma_falsa'), _op(V, 'forma_falsa_projecao')))"),
    ("«a forma falsa = o ponto fixo 0», fica retratada: a forma falsa é o complemento do posto, 1 − P; ver [[um-posto-jamais-pressuposto-e-h2-17set]]). \"\n",
     "«a forma falsa = o ponto fixo 0», fica retratada: a forma falsa é o complemento do posto, 1 − P; ver [[um-posto-jamais-pressuposto-e-h2-17set]]); e a frase das 14:40 — %s. \"\n"),
    ("    if V.get('tentativas'):\n        t += \" Tentativas anteriores preservadas ao lado: %s.\" % \", \".join(\"`%s`\" % x for x in V['tentativas'])\n    return t",
     "    if V.get('tentativas'):\n        t += \" Tentativas anteriores preservadas ao lado: %s.\" % \", \".join(\"`%s`\" % x for x in V['tentativas'])\n"
     "    if V.get('intervencao_txt'):\n        t += ' ' + V['intervencao_txt']\n    return t"),
])
aplica("handoff_v385.py", [
    ('for _n in ("custodia", "espelho", "nome_axioma", "prossiga", "posto", "subpasta", "v1_espelho", "tornar", "forma_falsa"):',
     'for _n in ("custodia", "espelho", "nome_axioma", "prossiga", "posto", "subpasta", "v1_espelho", "tornar", "forma_falsa", "forma_falsa_projecao"):'),
    ("**A reprodutibilidade** [COMPUTED]: `%(rp_v)s` — contra o resultado da v384 (`%(rp_prev16)s`), %(rp_frase)s.",
     "**A reprodutibilidade** [COMPUTED]: `%(rp_v)s` — contra o resultado da v384 (`%(rp_prev16)s`), %(rp_frase)s. %(intervencao_txt)s"),
    ("a leitura refeita está ao lado, [ONTO], a ratificar: pendência 4).",
     "a leitura refeita está ao lado, [ONTO], a ratificar: pendência 4); e a frase das 14:40: %(op_forma_falsa_projecao)s (leitura refinada ao lado, idem)."),
])
