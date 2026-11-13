# -*- coding: utf-8 -*-
"""depositar_etapa2a_v411.py -- deposito (so' acrescimo) do claude-construtor-v411 na fila da memoria ao fim da Etapa 2A parcial; fontes com sha256 lido. uso: python -B -X utf8 depositar_etapa2a_v411.py"""
import datetime, hashlib, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "depositos", "claude-construtor-v411")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
P = json.load(open(os.path.join(HERE, "PRONTO_PARA_GERAR_v411.json"), encoding="utf-8"))
fontes = [os.path.join(HERE, n_) for n_ in ("PRONTO_PARA_GERAR_v411.json", "A2_MEDIDA_v411.json", "TESTE_H0DN_OFFLINE_v411.json", "PREVOO_GERADOR_v411.json", "cadeia_v411.sh")]
agora = datetime.datetime.now()
txt = ("v411, Etapa 2A PARCIAL (claude-construtor-v411, 12/11/2026), sem TOPO_RATIFICADO_v411.json: candidato NAO gerado. Feito e testado: (a) o prefixo K_LAW_ na faixa do veredito de maquina (AO LADO no fim do DESENHO_v411, backup de bytes); "
       "(c) a excecao ESTREITA da P18 para a cabeca do teste numa funcao so' (_v411_p18_sem_cabeca), com controles (a exata sai; um caractere trocado e outro n sao recusados); o registro offline segue 16/16 com o recalculo identico ao "
       "resultado da abertura; o patch do A2 no conversor do TXT (medido: o conversor base reproduz o TXT do Nos; grupos de expoente dissolvidos PT 537 -> 17, EN 536 -> 14); o pre-voo com %d patches, guardas limpas no texto renderizado; "
       "as chaves congeladas com a G1 conferidas no registro (ok=%s); a sequencia exata em cadeia_v411.sh (para no primeiro script com a marca de copia mecanica). NAO feito: a troca das seis aberturas (os trechos estao so' em constantes seladas "
       "da v410: precisa troca na renderizacao, decisao da gerencia), a adaptacao dos %d scripts com corpo da v410 e os cinco blocos da custodia no handoff. O gate nao se move; provado e' validade, nao creditacao.\n") % (
    P["pre_voo"]["n_patches"], P["chaves_congeladas_com_a_g1"]["ok"], P["falta"]["n"])
cab = ("---\nquem: claude-construtor-v411\ncasa: Central de Patentes\ntipo: project\nestatuto: REAL\nalvo_sugerido: novo:v411-preparacao-etapa2a-12nov\ndepositado_em: %s\nfontes:\n" % agora.astimezone().isoformat(timespec="seconds")
       + "".join("  - %s  sha256:%s\n" % (p_, sha(p_)) for p_ in fontes) + "---\n")
dst = os.path.join(FILA, agora.strftime("%Y%m%d_%H%M%S") + "_v411-preparacao-etapa2a-12nov.md")
assert not os.path.exists(dst)
b = (cab + txt).encode("utf-8"); open(dst + ".tmp", "wb").write(b); assert os.path.getsize(dst + ".tmp") == len(b); os.replace(dst + ".tmp", dst)
print(dst)
