# -*- coding: utf-8 -*-
"""derivar_derivador_v399.py -- gera derivar_servico_v399.py a partir de v398\\bancada_B3_servico\\derivar_servico_v398.py por SUBIDA DE VERSAO de uma passada
(fronteira de digitos): v395..v398 -> +1 (tambem V39x_ e rel39x); variaveis de caminho V6S->V7S, V7S->V8S, V7->V8; "23/10" (data do rito real anterior) -> "24/10";
a tupla de restos ("394","395","396","V398_","v399") (apos o +1: V398_) -> ("395","396","397","V398_","v400").
Regras que NAO sao subida de versao, todas com contagem exata (assert):
  (1) o molde v398 (os tres scripts que RODARAM em 24/10) ja' traz o bloco do cruzamento com o B(n) anterior (rb_ant / ger_ant / assert n_esp == ger_ant + 1) UMA vez no recibo_religamento:
      a regra SUB da v398 (que reduzia DUAS copias a UMA) passa a INVARIANTE com contagem exata 1 (aplicada a' fonte v398 ela nao casaria: 0 != 1); o comentario e a docstring que a descreviam sao reescritos;
      os textos historicos «(v398: o molde v397 trazia este bloco DUAS vezes ...)» NAO sobem de versao (seriam falsos): a docstring e' reescrita por regex localizada, contagem exata 1;
  (2) DEFEITO DO MOLDE REVELADO PELO RITO REAL DE 24/10 (comparacao do que o servico fez de verdade com o que o script dizia): a nota do recibo_parada dizia «e a parada que precede este recibo e ato do operador,
      pelo PID, nao desta cadeia», e o RECIBO_PARADA_v398.json real traz, no campo autorizacao_do_operador do mesmo recibo, «executada pela gerencia c1 em 24/10» (sob a ordem geral do operador): a nota atribuia
      ao operador um ato que o proprio recibo diz executado pela gerencia. Uma regra SUB (contagem exata 1) troca a atribuicao; uma regra INV (contagem 0) garante que a frase sumiu; e a conferencia com o rito real
      ganha uma 20a condicao que MOSTRA a divergencia no recibo real da v398 (a condicao falha no real, por isso a regra; o script nao aborta por ela);
  (3) a docstring registra tudo isto.
Nao executa o derivador gerado (so ast.parse). Registra entrada/saida com sha256 em DERIVACAO_DERIVADOR_v399.json. Nao sobrescreve.
uso: python -I -B -X utf8 derivar_derivador_v399.py"""
import ast
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
CS = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(CS, "v398", "bancada_B3_servico", "derivar_servico_v398.py")
DST = os.path.join(HERE, "derivar_servico_v399.py")
sha = lambda b: hashlib.sha256(b).hexdigest()


def uma_vez(t, a, novo, rotulo):
    """troca exata de `a` por `novo`, com contagem exata 1 (assert)."""
    assert t.count(a) == 1, (rotulo, t.count(a))
    return t.replace(a, novo)


bruto = open(SRC, "rb").read()
t = bruto.decode("utf-8")
assert "\r" not in t
cont = {}
# ---- subida de versao (+1), uma passada, com a contagem por token medida na fonte v398
por = {}
RE_VER = re.compile(r"(?<![0-9A-Za-z])(v|V|rel)(39)([5-8])(?![0-9])")


def mais_um(m):
    por[m.group(1) + m.group(2) + m.group(3)] = por.get(m.group(1) + m.group(2) + m.group(3), 0) + 1
    return m.group(1) + m.group(2) + str(int(m.group(3)) + 1)


t, cont["versoes_mais_um"] = RE_VER.subn(mais_um, t)
cont["versoes_mais_um_por_token"] = dict(sorted(por.items()))
assert cont["versoes_mais_um"] == 152, cont["versoes_mais_um"]        # v398 50 + v397 73 + v396 10 + rel396 3 + rel397 5 + V398 7 + V397 4 (inventario medido na fonte)
assert por == {"v398": 50, "v397": 73, "v396": 10, "rel396": 3, "rel397": 5, "V398": 7, "V397": 4}, por
# ---- variaveis de caminho (nenhuma V8/V8S pre-existente colide)
RE_V8 = re.compile(r"(?<![0-9A-Za-z_])V8S?(?![0-9A-Za-z_])")
assert not RE_V8.search(open(SRC, encoding="utf-8").read()), "a fonte ja tem V8/V8S"
RE_VAR = re.compile(r"(?<![0-9A-Za-z_])(V7S|V6S|V7)(?![0-9A-Za-z_])")
VAR = {"V7S": "V8S", "V6S": "V7S", "V7": "V8"}
t, cont["variaveis_de_caminho"] = RE_VAR.subn(lambda m: VAR[m.group(1)], t)
assert cont["variaveis_de_caminho"] == 14, cont["variaveis_de_caminho"]      # V7 5 + V7S 7 + V6S 2 (inventario da fonte)
# ---- a data do rito real anterior
t = uma_vez(t, "rito REAL de 23/10 gravou (RECIBO_PARADA_v398.json", "rito REAL de 24/10 gravou (RECIBO_PARADA_v398.json", "data na docstring")
t = uma_vez(t, "contra o que o rito REAL de 23/10 gravou.", "contra o que o rito REAL de 24/10 gravou.", "data na docstring da conferencia")
assert "23/10" not in t
cont["data_do_rito_real"] = 2
# ---- a tupla de restos (depois do +1: V397_ virou V398_; v399 nao muda porque o +1 so' vai a 8)
a = '("394", "395", "396", "V398_", "v399")'
t = uma_vez(t, a, '("395", "396", "397", "V398_", "v400")', "tupla de restos")
cont["tupla_de_restos"] = 1
# ---- (1) o bloco do cruzamento com o B(n) anterior: a fonte (v398 final) traz UMA copia; a regra deixa de ser SUB e passa a INV (contagem exata 1)
a = '        ("n_confere_com_o_B_n_da_v398__bloco_uma_so_vez", SUB, r"^" + re.escape(CRUZA_BLOCO + CRUZA_BLOCO[len(N_ESP_LINHA):]), CRUZA_BLOCO, 1),'
t = uma_vez(t, a, '        ("n_confere_com_o_B_n_da_v398__bloco_uma_so_vez", INV, r"^" + re.escape(CRUZA_BLOCO), None, 1),', "regra do cruzamento")
cont["regra_do_cruzamento_de_SUB_para_INV"] = 1
a = "# a linha do molde que calcula n; a SUBSTITUICAO acrescenta, logo depois dela, o cruzamento com o B(n) da v398"
t = uma_vez(t, a, "# a linha do molde que calcula n; o cruzamento com o B(n) da v398 (CRUZA_BLOCO) ja' esta' no molde v398, UMA vez, logo depois dela", "comentario do cruzamento")
cont["comentario_do_cruzamento"] = 1
# a docstring: o bloco historico SUBSTITUICAO (3 linhas) e' reescrito (localizado por regex, 1 casamento de 3 linhas)
rx = re.compile(r"^   - SUBSTITUICAO \(uma so', no religamento\):.*?contagem exata 1\);\n", re.M | re.S)
achados = rx.findall(t)
assert len(achados) == 1 and achados[0].count("\n") == 3 and "DUAS vezes" in achados[0], (len(achados), achados[:1])
NOVO_BLOCO_DOC = (
    "       * religamento: alem de calcular n a partir do manifesto anterior do proprio recibo do B(n) da v399, o script cruza esse n com a geracao que o recibo do B(n) da v398\n"
    "         (RECIBO_SINCRONIZACAO_v398_*.json, manifesto_novo.deployment_id) deixou na Bancada: «n = geracao do manifesto anterior (lida do recibo do B(n) da v398) + 1»; assert com mensagem clara;\n"
    "         o bloco do cruzamento esta UMA vez no molde v398 (os tres scripts que RODARAM em 24/10): contagem exata 1 (a regra que na v398 reduzia duas copias a uma passou a invariante);\n"
    "   - SUBSTITUICAO (uma so', na parada; novidade da v399): a nota do recibo de parada dizia «e a parada que precede este recibo e ato do operador, pelo PID, nao desta cadeia», e o rito REAL de 24/10 gravou,\n"
    "     no campo autorizacao_do_operador do MESMO recibo, «executada pela gerencia c1 em 24/10»; a regra troca a atribuicao por «feita pelo PID (nunca por nome), nao por este script; quem a executou e sob que\n"
    "     ordem do operador consta em autorizacao_do_operador», contagem exata 1; a conferencia com o rito real ganha a 20a condicao, que falha no recibo real da v398 e mostra a divergencia;\n")
t, k = rx.subn(lambda m: NOVO_BLOCO_DOC, t)
assert k == 1
cont["docstring_substituicao_reescrita"] = 1
# ---- (2) o defeito do molde revelado pelo rito real: a nota da parada
a = '        ("recibo_da_parada_v399", INV, re.escape(\'"RECIBO_PARADA_v399.json"\'), None, 1),\n'
NOVAS_REGRAS_PARADA = (
    a +
    """        ("nota_nao_atribui_a_parada_ao_operador", SUB,
         re.escape('"e a parada que precede este recibo e ato do operador, pelo PID, nao desta cadeia" % (rel398.get("passo"), pid_ultimo)),'),
         '"e a parada que precede este recibo e feita pelo PID (nunca por nome), nao por este script; quem a executou e sob que ordem do operador consta em autorizacao_do_operador" % (rel398.get("passo"), pid_ultimo)),', 1),
        ("nota_sem_a_frase_ato_do_operador", INV, r"e ato do operador", None, 0),
""")
t = uma_vez(t, a, NOVAS_REGRAS_PARADA, "ancora das regras da parada")
cont["regra_sub_da_nota_da_parada"] = 1
cont["regra_inv_nota_sem_a_frase"] = 1
a = '''    chk("parada: a nota cita o passo e o PID do religamento anterior", str(r394["passo"]) in rp["nota"] and str(r394["pid"]) in rp["nota"], [r394["passo"], r394["pid"]], "ambos contidos")\n'''
NOVA_CONDICAO = (
    a +
    """    chk("parada: a nota nao atribui ao operador o ato que a autorizacao do mesmo recibo diz executado pela gerencia",
        not ("e ato do operador" in rp["nota"] and "executada pela gerencia" in str(rp.get("autorizacao_do_operador") or "")),
        [rp["nota"][-90:], str(rp.get("autorizacao_do_operador") or "")[-70:]], "a nota nao diz «e ato do operador» quando a autorizacao diz «executada pela gerencia»")
""")
t = uma_vez(t, a, NOVA_CONDICAO, "ancora da 20a condicao")
cont["condicao_nova_da_conferencia"] = 1
# ---- invariantes do resultado: o mapa de versoes do derivador novo tem de ser v398->v399, v397->v398
a = 'MAPA = {"v398": "v399", "v397": "v398", "rel397": "rel398", "V398_AUTORIZACAO_OPERADOR": "V399_AUTORIZACAO_OPERADOR"}'
assert t.count(a) == 1, "mapa de versoes do derivador novo nao e o esperado"
a = 'RE_MAPA = re.compile(r"V398_AUTORIZACAO_OPERADOR|v398|v397|rel397")'
assert t.count(a) == 1
for pad in ('V8S = os.path.join(V8, "bancada_B3_servico")', 'V8 = os.path.join(CS, "v398")', 'V7S = os.path.join(CS, "v397", "bancada_B3_servico")'):
    assert t.count(pad) == 1, pad
assert not re.search(r"(?<![0-9A-Za-z])(v|V|rel)396(?![0-9])", t)
assert t.count('("nota_nao_atribui_a_parada_ao_operador", SUB,') == 1 and t.count("SUBSTITUICAO (uma so', na parada") == 1
assert t.count("SUB, r\"^\"") == 0     # nenhuma regra SUB do cruzamento sobrou
ast.parse(t)
out = t.encode("utf-8")
if os.path.exists(DST):
    raise SystemExit("ja existe: " + DST)
rp = os.path.join(HERE, "DERIVACAO_DERIVADOR_v399.json")
if os.path.exists(rp):
    raise SystemExit("ja existe: " + rp)
with open(DST + ".tmp", "wb") as fh:
    fh.write(out)
assert os.path.getsize(DST + ".tmp") == len(out)
os.replace(DST + ".tmp", DST)
me = os.path.abspath(__file__)
rel = {"derivador": {"path": me, "sha256": sha(open(me, "rb").read())}, "entrada": {"path": SRC, "sha256": sha(bruto), "bytes": len(bruto)}, "saida": {"path": DST, "sha256": sha(out), "bytes": len(out)},
       "contagens": cont, "ast_parse": "ok", "executado": False}
with open(rp, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(rel, ensure_ascii=False, indent=1) + "\n")
print(json.dumps(rel, ensure_ascii=False))
