# -*- coding: utf-8 -*-
"""_fix_p00_real_v411.py -- (claude-construtor-v411, retomada, 12/11/2026) o p00 da v411 passa a conferir a cadeia REAL (TOPO_RATIFICADO_v411.json existe; o candidato existe): (1) as contagens das copias e das falas lidas
do delta (18 + 7 + 6 + 11 = 42; 11 falas), nunca digitadas; (2) a saida em DL.saida (pedido do fork B: no ensaio do topo proposto, na pasta de ensaio); (3) o topo ratificado conferido (sha256 do arquivo == o do delta ==
o do manifesto do candidato); (4) o candidato e o que vem depois dele conferidos QUANDO existem (o manifesto, o ensaio a seco TUDO PASSOU deste sha, os ESPERADOS, os dois conferidores, as citacoes do escopo do um.py,
a derivacao do instalar/rito, os pinos do B(n)); o que ainda nao existe fica PENDENTE com o nome do passo que o produz. Backup de BYTES antes. uso: python -B -X utf8 _fix_p00_real_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "p00_precondicoes_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
NOVO_PEND = '''# (9) o topo ratificado, o candidato e o que vem depois dele (conferidos QUANDO existem; senao, PENDENTE com o passo que os produz)
_sha = lambda p_: sha(p_) if os.path.exists(p_) else None
if os.path.exists(DL.TOPO_RATIFICADO_ARQ) and not DL.ENSAIO_TOPO_PROPOSTO:
    tenta("TOPO_RATIFICADO_v411.json (a palavra do operador, D172/D173): o sha256 do arquivo == o lido pelo delta (a fonte unica do topo, 12 marcadores)", lambda: (sha(DL.TOPO_RATIFICADO_ARQ) == DL.TOPO_SHA256 and len(DL.MARCADORES_V411 or {}) == 12, DL.TOPO_SHA256))
elif not DL.ENSAIO_TOPO_PROPOSTO:
    pend("TOPO_RATIFICADO_v411.json (o texto do topo do resumo, com a palavra do operador; DESENHO 5.1 b e secao 8)", "ato da GERENCIA: sem ele o candidato nao e' gerado")
if not os.path.exists(DL.CANDIDATO_ARQ):
    pend("o candidato um_v411_candidato.py e o que vem depois dele (comparacao com a v410, ensaio a seco, ESPERADOS, conferidores, citacoes, diff e pinos, conferir_instalar_rito, fim_de_cadeia com o B20 pre-selo, harnesses)", "gerar_candidato_v411.py (so' depois do TOPO_RATIFICADO_v411.json)")
else:
    _c16 = sha(DL.CANDIDATO_ARQ)[:16]; CMJ = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8")) if os.path.exists(DL.MANIFESTO_ARQ) else {}
    tenta("o candidato e o manifesto dele: o sha16 do arquivo == o do manifesto; escada 12308 sem bandeira nova; o topo do manifesto e' o ratificado (sha256)", lambda: (CMJ.get("sha16") == _c16 and CMJ.get("escada") == [POS["E410"], POS["E410"]] and CMJ.get("n_bandeiras") == 0
                                                                                                                                                                and (DL.ENSAIO_TOPO_PROPOSTO or (CMJ.get("topo") or {}).get("sha256") == DL.TOPO_SHA256), {"sha16": _c16, "manifesto": CMJ.get("sha16")}))
    _DEPOIS = [("ensaio_a_seco_v411.json", "ensaio_a_seco_v411.py", lambda j_: j_.get("veredito") == "TUDO PASSOU" and j_.get("sha16") == _c16),
               ("ESPERADOS_v411.json", "gerar_esperados_v411.py", lambda j_: j_.get("candidato_sha16") == _c16),
               ("conferencia_rito_v411_CONTROLE_NEGATIVO_PRE_RITO.json", "conferir_rito_v411.py --controle-negativo", lambda j_: j_.get("tudo_bate") is False),
               ("conferencia_rito_v411_POSITIVO_FALSO_NOS.json", "teste_conferidor_positivo_v411.py", lambda j_: j_.get("tudo_bate") is True and j_.get("um_py_sha16") == _c16),
               ("conferir_citacoes_v411.json", "conferir_citacoes_v411.py --candidato", lambda j_: j_.get("ok_do_um_py") is True),
               ("DERIVACAO_v411.json", "conferir_instalar_rito_v411.py", lambda j_: not j_.get("falhas")),
               ("PINOS_BN_v411.json", "diff_e_pinos_v411.py", lambda j_: ((j_.get("candidato") or {}).get("sha256") or "")[:16] == _c16)]
    for _arq, _passo, _ok in _DEPOIS:
        _p = DL.saida(_arq)
        if os.path.exists(_p):
            tenta("%s (de %s) e' deste candidato e passou" % (_arq, _passo), (lambda p__=_p, ok__=_ok: (bool(ok__(json.load(open(p__, encoding="utf-8")))), os.path.basename(p__))))
        else:
            pend("%s (o passo %s ainda nao rodou para este candidato)" % (_arq, _passo), "passo da cadeia (cadeia_v411.sh)")
    _cj = DL.saida("conferir_citacoes_v411.json")
    if os.path.exists(_cj) and json.load(open(_cj, encoding="utf-8")).get("ok_do_pos_rito") is False:
        pend("as citacoes em «» do escopo do pos-rito (pos_rito\\\\*_v411*: a outra frente) nao sao todas fala verbatim do operador", "pedido a frente pos-rito em PEDIDOS_ENTRE_FRENTES_v411.md (o escopo do um.py esta' limpo; o relatorio final exige os dois)")
if not os.path.exists(os.path.join(HERE, "PINO_MEMORIA_PY_v411.json")):
'''
PARES = [
    ('tenta("as %d copias duraveis em insumos\\\\ == as origens (sha256), com os sha16 do DESENHO" % (18 + 7 + 5 + 9), lambda: (MI is not None and MI["n"] == 39 and',
     '_NCOP = len(DL.INSUMOS_V411) + len(DL.CITADOS_V411) + len(DL.TEXTOS_DA_GERENCIA_CITADOS) + len(DL.FALAS_V411)   # (12/11: 18 + 7 + 6 + 11, lidas do delta)\n'
     'tenta("as %d copias duraveis em insumos\\\\ == as origens (sha256), com os sha16 do DESENHO e do AO LADO de 12/11" % _NCOP, lambda: (MI is not None and MI["n"] == _NCOP and'),
    ('tenta("a lista congelada das falas: 9, cada uma com o sha256 do arquivo", lambda: (CG is not None and CG["n"] == 9 == len(CG["registro"])',
     'tenta("a lista congelada das falas: %d (9 do DESENHO + 2 do AO LADO de 12/11), cada uma com o sha256 do arquivo" % DL.N_FALAS_V411, lambda: (CG is not None and CG["n"] == DL.N_FALAS_V411 == len(CG["registro"])'),
    ('# (9) pendentes\nif not os.path.exists(DL.TOPO_RATIFICADO_ARQ):\n    pend("TOPO_RATIFICADO_v411.json (o texto do topo do resumo, com a palavra do operador; DESENHO 5.1 b e secao 8)", "ato da GERENCIA: sem ele o candidato nao e\' gerado (gerar_candidato_v411.py recusa); o pre-voo usou a proposta do DESENHO")\n'
     'if not os.path.exists(os.path.join(HERE, DL.CANDIDATO)):\n    pend("o candidato um_v411_candidato.py e o que vem depois dele (comparacao com a v410, ensaio a seco, ESPERADOS, conferidores, citacoes, diff e pinos, conferir_instalar_rito, fim_de_cadeia com o B20 pre-selo, harnesses)", "Etapa 2 da preparacao (so\' depois do TOPO_RATIFICADO_v411.json)")\n'
     'if not os.path.exists(os.path.join(HERE, "PINO_MEMORIA_PY_v411.json")):\n',
     NOVO_PEND),
    ('p = os.path.join(HERE, "PRECONDICOES_v411.json")\n', 'out.update(DL.MARCA_ENSAIO)\np = DL.saida("PRECONDICOES_v411.json")   # (pedido do fork B: no ensaio do topo proposto, na pasta de ensaio)\n'),
]
for a_, n_ in PARES:
    assert t.count(a_) == 1, (a_[:100], t.count(a_))
    t = t.replace(a_, n_)
ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_real"
open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
