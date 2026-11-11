# -*- coding: utf-8 -*-
"""_adapt_deposito_rotas_parte2_v410.py -- o registro do construtor no Mapa de Rotas (depositar_construtor_v410.py) ganha, na parte 2: (a) a REFERENCIA as rotas estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov e kernel.a_escala_tres_faces_v410_09nov (ja' registradas pela gerencia; conferidas no livro por rotas.py ver);
(b) uma ANOTACAO na rota da ORDEM ao Kimi: o recibo documental HMS/13 (D80) entrou na PREPARACAO da v410 como registro aditivo e posterior ao FREEZE_R2. Trocas exatas; backup de BYTES; temporario -> conferir tamanho -> substituir; ast.parse. Nao deposita nem registra nada."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "depositar_construtor_v410.py")
b0 = open(P, "rb").read(); NL = "\r\n" if b0.count(b"\r\n") else "\n"; t = b0.decode("utf-8")


def troca(a, b):
    global t
    c = t.count(a); assert c == 1, (c, a[:120]); t = t.replace(a, b)


troca('"refs": ["cadeia.preparacao_v409", "um_py.v410_preparacao_aberta_06nov"],',
      '"refs": ["cadeia.preparacao_v409", "um_py.v410_preparacao_aberta_06nov", "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov", "kernel.a_escala_tres_faces_v410_09nov"],   # (parte 2) a ORDEM ao Kimi (o H0DN e o recibo HMS/13) e a candidata AEscala, rotas da gerencia')
troca('if _ANT else "")}]' + NL,
      'if _ANT else "")},' + NL
      + '        {"tipo": "ANOTACAO", "rota_id": "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov", "estatuto": "REAL", "olhou_dados": False,   # (parte 2, D80) a anotacao na rota da ORDEM ao Kimi: o recibo documental entrou na PREPARACAO; o pos-rito anota o selo' + NL
      + '         "titulo": "o recibo documental HMS/13 (D80) entrou na preparacao da v410: candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]),' + NL
      + '         "resultado": "o registro h0dn_fontes_hms13_v410, ADITIVO e POSTERIOR ao FREEZE_R2, embute por sha256 quatro artefatos documentais da revisao independente (18 fontes primarias dos 13 calibradores): cobertura documental de fontes, não covariância física fechada; nada aberto. O teste H0DN x BG1 segue pré-registrado; nenhum dado observado lido; em rito nada da pasta da entrega e\' aberto (a excecao D80 vale so\' para os seis artefatos documentais, por sha256, lidos no build). A preparacao NAO e\' o selo: nada instalado, o rito nao rodou.",' + NL
      + '         "proximo_passo": "G3/G4 seguem abertos (a covariancia fisica conjunta, a decomposicao completa dentro de cada SN, a matriz completa entre os 13, a revisao fisica independente); o pos-rito da v410 anota o selo nesta mesma rota",' + NL
      + '         "refs": ["cadeia.preparacao_v410", "kernel.a_escala_tres_faces_v410_09nov"]}]' + NL)
nb = t.encode("utf-8"); ast.parse(nb)
open(P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_pre_rotas_parte2", "wb").write(b0)
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb) > len(b0); os.replace(P + ".tmp", P)
print("depositar_construtor_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16], "| fim de linha", repr(NL))
