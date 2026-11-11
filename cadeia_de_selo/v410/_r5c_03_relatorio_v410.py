# -*- coding: utf-8 -*-
"""_r5c_03_relatorio_v410.py -- a REVISAO DO CONSTRUTOR, parte 3 (10/11/2026), so' em gerar_relatorio_v410.py:
 (R1) o aviso da R2 dizia «a rodada foi so' de texto: a pedra, o kernel ... NAO mudaram»: com a R5 (D100) a pedra AEscala e o kernel MUDARAM depois, por ordem do operador; a frase passa a dizer as duas coisas;
 (R2) a confirmacao medida do texto-fonte de veredito_h0dn aceitava «nao medido» (None): passa a exigir True (fail-closed);
 (R3) a chave alem_do_r2 ganha a lista da revisao do construtor sobre a adaptacao (as chaves renomeadas e os consertos de texto e de controle).
Idempotente; backup de BYTES; temporario + os.replace; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")
p = os.path.join(HERE, "gerar_relatorio_v410.py"); b0 = open(p, "rb").read(); t = b0.decode("utf-8"); log = []


def tr(a, b, n=1):
    global t
    c = t.count(a)
    if c == 0 and b in t:
        log.append("ja' feito: " + a[:60]); return
    assert c == n, ("contagem", c, "esperado", n, a[:140])
    t = t.replace(a, b); log.append("trocado x%d: %s" % (c, a[:60]))


tr("a rodada foi so' de texto: a pedra, o kernel, os nomes, os enunciados, a guarda das frases e a funcao veredito_h0dn NAO mudaram; ",
   "a correcao do R2 foi so' de texto (os nomes e os enunciados que ja' existiam, a pedra IALD2, a guarda das frases e a funcao veredito_h0dn NAO mudaram); DEPOIS dela, por ordem do operador (D100), a pedra AEscala passou a R5 (so' acrescimo: seis nomes novos; os 62 da R4 com o mesmo nome e enunciado) e o kernel foi reconstruido a frio: ver a chave alem_do_r2; ")
tr('["texto_fonte_de_veredito_h0dn"]["igual"] in (True, None), ("a R5 mexeu no que nao podia: "', '["texto_fonte_de_veredito_h0dn"]["igual"] is True, ("a R5 mexeu no que nao podia (ou o texto-fonte de veredito_h0dn nao foi medido): "')
tr('"runtime_v410_py_a_guarda_das_frases": {"sha16_medido": _med_rt5, "sha16_pinado_antes_da_R5": _pin_rt5, "igual": _med_rt5 == _pin_rt5}}}',
   '"runtime_v410_py_a_guarda_das_frases": {"sha16_medido": _med_rt5, "sha16_pinado_antes_da_R5": _pin_rt5, "igual": _med_rt5 == _pin_rt5}},\n'
   '              "revisao_do_construtor_sobre_a_adaptacao": [\n'
   '                  "a chave do registro que listava os nomes novos da pedra chamava-se nomes_novos_a_ratificar e trazia os 24, 22 deles ja\' ratificados (D101): passa a nomes_novos_da_pedra (o campo de mesmo nome do recibo dos nomes, que e\' insumo, nao muda)",\n'
   '                  "a chave estatuto_dos_nomes_novos dizia RATIFICADOS para a lista de 24, que inclui os 2 auxiliares pendentes: passa a estatuto_dos_nomes_ratificados_d101 (o estatuto dos pendentes mora em ratificacao_pendente)",\n'
   '                  "a frase da clausula de 1 - beta e a clausula do limite vinham coladas sem pontuacao: a juncao e\' UMA constante do delta (ANUNCIO_TETELESTAI_PT/EN: a frase, a clausula do limite entre parenteses, a reconstrucao), usada pelo registro, pela D100, pelo handoff, pelos textos do pos-rito e pelos controles",\n'
   '                  "a linha do .md canonico traz a clausula do limite tambem logo depois da clausula de 1 - beta (duas ocorrencias na linha: D99 e D100); os controles do ensaio e do conferidor exigem as duas",\n'
   '                  "a errata E36 (o limiar de um pixel e\' a decisao exata) ficava sozinha em duas folhas do registro, sem a clausula do limite: no nucleo do texto ela vem sempre com a clausula na mesma folha, e a c8 o exige (fail-closed); o estatuto do registro tambem traz a clausula ao lado do anuncio",\n'
   '                  "frases que envelheceram com a c13, que usa beta de runtime (nenhum numero de beta entra; beta so\' por nome; o registro nem o usa): passam a dizer beta nunca literal (so\' por nome na pedra; na c13, pelo valor de runtime)",\n'
   '                  "comentarios, docstrings e mensagens que ainda diziam nomes novos a ratificar (o texto da D99, registro historico, nao muda); a lista dos temas das falas do registro ganha as duas falas novas"]}')
b1 = t.encode("utf-8")
if b1 != b0:
    ast.parse(t); bak = p + ".bak_" + TS + "_r5c3"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
    tmp = p + ".tmp_r5c"; open(tmp, "wb").write(b1); assert os.path.getsize(tmp) == len(b1) > 0; os.replace(tmp, p); assert open(p, "rb").read() == b1
print("gerar_relatorio_v410.py:", "MUDOU" if b1 != b0 else "igual", log)
