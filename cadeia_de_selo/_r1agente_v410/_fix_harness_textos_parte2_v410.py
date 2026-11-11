# -*- coding: utf-8 -*-
"""_fix_harness_textos_parte2_v410.py -- ACHADOS da primeira rodada do harness dos textos na v410 (09/11, 20:55 a 21:07; o harness nunca tinha rodado nesta versao):
(B) dois controles negativos tiravam do stdout a linha do bloco herdado da v408 por um ROTULO errado (subida mecanica de rotulo: dizia que os registros por spec eram da v409; o candidato e a leitura dizem v408): a mutacao nao tirava nada e o controle nao reprovava. Conserto: o rotulo certo.
(C) o controle do a_escala_v410 tirava a forma canonica do Clay so' do campo estatuto; a leitura confere a frase no TEXTO do registro (estatuto, scope, limites, diz, nao_diz), como a c7 do proprio registro: a frase seguia nos outros campos e o controle nao reprovava.
    Conserto: o controle tira a frase de TODOS os campos de texto que a leitura le (a leitura nao muda).
(A) textos_v410._dl(): a assercao passa a DIZER o que leu (o arquivo do delta e os valores), para a causa ficar visivel se cair de novo (fail-closed com motivo).
Backup de BYTES; temporario -> conferir tamanho -> substituir; ast.parse. Nao muda o candidato, o delta nem a leitura."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")


def aplicar(nome, trocas):
    p = os.path.join(HERE, "pos_rito", nome); b0 = open(p, "rb").read(); crlf = b0.count(b"\r\n") > 0; t = b0.decode("utf-8").replace("\r\n", "\n")
    for a, b, n in trocas:
        c = t.count(a); assert c == n, (nome, c, n, a[:140]); t = t.replace(a, b)
    nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8"); ast.parse(nb)
    open(p + ".bak_" + TS + "_pre_fix_harness_parte2", "wb").write(b0)
    open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb); os.replace(p + ".tmp", p)
    print(nome, len(b0), "->", len(nb), "| sha16", hashlib.sha256(b0).hexdigest()[:16], "->", hashlib.sha256(nb).hexdigest()[:16])


aplicar("harness_textos_ensaio_v410.py", [
    ('"[v408] o registro do terminal e os registros por spec da v409"', '"[v408] o registro do terminal e os registros por spec da v408"', 2),
    ('variante("%s: o texto sem a forma canonica do Clay no estatuto" % AE_, f_core=lambda c: c[AE_].update(estatuto=c[AE_]["estatuto"].replace(DLX.FRASE_CLAY_CANONICA_PT, "XXXX")), espera=MAE_),',
     'variante("%s: o texto sem a forma canonica do Clay (tirada de todos os campos de texto que a leitura le)" % AE_, f_core=lambda c: c[AE_].update({k_: json.loads(json.dumps(c[AE_].get(k_), ensure_ascii=False).replace(DLX.FRASE_CLAY_CANONICA_PT, "XXXX")) for k_ in ("estatuto", "scope", "limites", "diz", "nao_diz")}), espera=MAE_),   # (09/11, achado da 1a rodada: a frase mora em varios campos; tirar so\' do estatuto nao a tira do texto)', 1),
])
aplicar("textos_v410.py", [
    ('[DL_.FECHO_REGISTRO, DL_.AESCALA_REGISTRO, DL_.H0DN_REGISTRO, DL_.HMS13_REGISTRO], "o delta lido nao e\' o da v410 (parte 2: os quatro registros com funcao)"',
     '[DL_.FECHO_REGISTRO, DL_.AESCALA_REGISTRO, DL_.H0DN_REGISTRO, DL_.HMS13_REGISTRO], ("o delta lido nao e\' o da v410 (parte 2: os quatro registros com funcao)", getattr(DL_, "__name__", None), getattr(DL_, "__file__", None), getattr(DL_, "UM_VERSION", None), getattr(DL_, "FECHO_REGISTRO", None), list(getattr(DL_, "REGISTROS_FUNCAO", [])), getattr(_qd(), "__file__", None))', 1),
])
