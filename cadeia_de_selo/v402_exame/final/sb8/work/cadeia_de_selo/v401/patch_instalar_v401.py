# -*- coding: utf-8 -*-
"""patch_instalar_v401.py -- aplica, por substituicoes de contagem EXATA, a logica da v401 sobre instalar_v401.py (origem v399) e reverter_v401.py: o recibo pre_selo da v401 e' GERADO e PINADO antes da instalacao (em ensaio contra a Bancada de producao, que JA pina a v400);
o instalador confere que a Bancada ainda pina o que o recibo diz (o sha256 do manifesto dela == o do pino) -- licao da v400 --; o modulo novo e' a pedra FalsidadeDaInercia (nome dado pelo operador). Recusa rodar duas vezes."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")


def aplica(P, subs, marca):
    t = open(P, encoding="utf-8").read()
    assert marca not in t, "o patch ja foi aplicado: " + P
    for old, new, n in subs:
        assert t.count(old) == n, (P, old[:100], t.count(old), n)
        t = t.replace(old, new)
    t = t.replace("\n", "\n", 1)
    ast.parse(t) if P.endswith(".py") else None
    open(P + ".tmp", "w", encoding="utf-8", newline="").write(t); os.replace(P + ".tmp", P)
    print("patch aplicado:", P)


aplica("instalar_v401.py", [
    ("(a licao da v400: o recibo e' gerado e pinado ANTES da instalacao);", "(a licao da v400: o recibo e' gerado e pinado ANTES da instalacao; aqui GERADO NOVO, em ensaio contra a Bancada que JA pina a v400) e a Bancada de producao tem de seguir pinando o que o recibo diz (o sha256 do manifesto dela == o do pino);", 1),
    ("(a v401 traz UM modulo novo de kernel, Testemunho [nome provisorio]; o numero e' lido de kernel_modulos_novos_v401.json: o proprio rito o materializa a partir do corpo embutido)", "(a v401 traz UM modulo novo de kernel, FalsidadeDaInercia [nome dado pelo operador: «falsidade (simulacro) da inercia»]; o numero e' lido de kernel_modulos_novos_v401.json: o proprio rito o materializa a partir do corpo embutido)", 1),
    ("(b) o modulo novo da v401 (Testemunho) NAO esta la ainda.", "(b) o modulo novo da v401 (FalsidadeDaInercia) NAO esta la ainda.", 1),
    ('PINO["versao_nos"] == "v400" and PINO["um_py_sha16_do_nos"] == h16(raw0), "o recibo pre_selo nao e\' utilizavel ou nao e\' do um.py que esta no Nos -- nao instalo"\n',
     'PINO["versao_nos"] == "v400" and PINO["um_py_sha16_do_nos"] == h16(raw0), "o recibo pre_selo nao e\' utilizavel ou nao e\' do um.py que esta no Nos -- nao instalo"\n'
     '_bmp = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "canonical_contracts.json"); _bmb = open(_bmp, "rb").read(); _bm = json.loads(_bmb.decode("utf-8"))\n'
     'assert hashlib.sha256(_bmb).hexdigest() == PINO["valido_enquanto"]["bancada_pina"]["manifesto_sha256"] and _bm["canonical"].get("version") == "v400" == PINO["valido_enquanto"]["bancada_pina"]["version"], "a Bancada de producao nao pina mais o que o recibo pre_selo diz (re-pino antes do B(n)): o recibo ficou obsoleto -- nao instalo"\n', 1),
], "aqui GERADO NOVO, em ensaio")
