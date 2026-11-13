# -*- coding: utf-8 -*-
"""_ao_lado_desenho_topo_ratificado_v411.py -- acrescenta AO LADO, no FIM do DESENHO_v411.md (so' acrescimo; backup de BYTES antes; CRLF respeitado), em nome da gerencia c1 (registrado pelo claude-construtor-v411), o que
a gerencia mandou registrar em 12/11/2026: a secao 5.1 b foi SUPERADA por TOPO_RATIFICADO_v411.json (formula ratificada pelo operador; acrescimo do acervo ordenado por ele, redacao da gerencia, ratificada por ele;
rotulo do P2 proposto pela gerencia, sem objecao dele); as duas falas novas do operador (a lista congelada passa a 11), o texto da gerencia novo citado por sha256 (passam a 6) e as decisoes D171 a D173.
Os sha16 sao LIDOS dos arquivos por este script, nunca digitados. Idempotente (marcador). uso: python -B -X utf8 _ao_lado_desenho_topo_ratificado_v411.py"""
import datetime, hashlib, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
WK = os.path.dirname(os.path.dirname(HERE)); CUN = os.path.join(WK, "cunhagens_13out")
P = os.path.join(HERE, "DESENHO_v411.md")
MARCA = "<!-- ao_lado_topo_ratificado_12nov -->"
b = open(P, "rb").read()
if MARCA.encode("utf-8") in b:
    print("ja' registrado"); raise SystemExit(0)
assert b.endswith(b"\r\n") and b"\n" not in b.replace(b"\r\n", b""), "o DESENHO nao e' CRLF puro"
s16 = lambda p_: hashlib.sha256(open(p_, "rb").read()).hexdigest()[:16]
TOPO = os.path.join(HERE, "TOPO_RATIFICADO_v411.json"); tj = json.loads(open(TOPO, "rb").read().decode("utf-8"))
F1 = "OPERADOR_12nov_ratifico_a_formula_e_o_acrescimo_dos_11_testes_lido_em_conjunto_com_o_acervo_verbatim.txt"
F2 = "OPERADOR_12nov_concordo_com_tudo_a_redacao_do_acrescimo_do_acervo_verbatim.txt"
G1 = "GERENCIA_12nov_redacao_do_acrescimo_do_acervo_e_os_tres_pontos_ratificada_pelo_operador.json"
for n_ in (F1, F2, G1):
    assert os.path.exists(os.path.join(CUN, n_)), n_
assert hashlib.sha256(open(os.path.join(CUN, F1), "rb").read()).hexdigest() == tj["fala_que_ratifica"]["sha256"]
assert hashlib.sha256(open(os.path.join(CUN, F2), "rb").read()).hexdigest() == tj["fala_que_ratifica_a_redacao"]["sha256"]
assert hashlib.sha256(open(os.path.join(CUN, G1), "rb").read()).hexdigest() == tj["texto_da_gerencia_ratificado"]["sha256"]
ACORDO = os.path.join(HERE, "ACORDO_COM_A_CUSTODIA_v411_12nov.md")
txt = ("\r\n\r\n## AO LADO (12/11/2026, em nome da gerência c1, registrado pelo claude-construtor-v411; a seção 5.1 b superada pelo topo ratificado) " + MARCA + "\r\n\r\n"
       "- **A seção 5.1 b foi SUPERADA por `TOPO_RATIFICADO_v411.json`** (sha16 `" + s16(TOPO) + "`, gravado pela gerência): a fórmula do topo, nos três tamanhos (o resumo do artigo, o painel do README e a frase de estado), "
       "foi RATIFICADA pelo operador em 12/11/2026; o acréscimo do acervo foi ORDENADO por ele, com a redação da gerência, que ele ratificou; o rótulo do P2 foi PROPOSTO pela gerência e mostrado a ele com a fórmula, sem objeção. "
       "O arquivo é a fonte única desses textos, dos doze marcadores (cada um com a chave do core de onde o número é lido na emissão e o formato) e das regras; o texto PROPOSTO da seção 5.1 b fica como registro.\r\n"
       "- **D171** (12/11) o acordo com a custódia, em `ACORDO_COM_A_CUSTODIA_v411_12nov.md` (sha16 `" + s16(ACORDO) + "` neste registro; vale como ao lado das seções 5.3 e 6).\r\n"
       "- **D172** (12/11) o operador ratificou a fórmula do topo nos três tamanhos e ordenou a leitura com o acervo.\r\n"
       "- **D173** (12/11) o operador ratificou a redação do acréscimo, com os três pontos ditos pela gerência: nenhuma falsificada, com as categorias do livro; a palavra de selar fica na fala do autor citada; o teste anterior entra com a regra do 4,44 e sem valer como evidência independente.\r\n"
       "- As falas do operador que entram (a lista congelada passa a 11; autor: o operador):\r\n\r\n"
       "| arquivo | sha16 | papel |\r\n"
       "|---|---|---|\r\n"
       "| `" + F1 + "` | `" + s16(os.path.join(CUN, F1)) + "` | ratifica a fórmula do topo e ordena a leitura com o acervo (D172) |\r\n"
       "| `" + F2 + "` | `" + s16(os.path.join(CUN, F2)) + "` | ratifica a redação do acréscimo do acervo e os três pontos em que ela difere da fala (D173) |\r\n\r\n"
       "- O texto da gerência a que ele respondeu entra só CITADO por sha256 (não é fala dele): `" + G1 + "` (sha16 `" + s16(os.path.join(CUN, G1)) + "`).\r\n"
       "- O quadro novo do topo ganha o item da fala do autor (o trecho verbatim de `fala_do_autor_para_o_quadro`, conferido por bytes, com a data e o sha16, seguido de “testemunho do autor; a frase de máquina é a cabeça do veredito, com as ressalvas”); "
       "a guarda F65 passa a aceitar, como nome da convenção dos 5σ, “critério de descoberta”, “escala de descoberta”, “discovery criterion”, “discovery scale” e “discovery threshold”, e segue recusando “descoberta” dita do número ou do rito; "
       "o rótulo do campo `p2_ao_lado_da_v387` é lido da chave `rotulo_p2` do arquivo (deixa de ser provisório).\r\n")
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(bak, "wb").write(b); assert open(bak, "rb").read() == b
novo = b + txt.encode("utf-8")
open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo); os.replace(P + ".tmp", P)
assert os.path.getsize(P) > len(b) and open(P, "rb").read().startswith(b)
print("AO LADO do topo ratificado acrescentado | backup", os.path.basename(bak), "|", len(b), "->", len(novo), "B")
