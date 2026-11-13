# -*- coding: utf-8 -*-
"""_ao_lado_desenho_e43_v411.py -- acrescenta AO LADO, no FIM do DESENHO_v411.md (so' acrescimo; backup de BYTES antes; CRLF respeitado), a DECISAO da gerencia c1 de 12/11/2026 sobre o item da secao 7
“as seis aberturas da secao da Escala que identificam o operador contra a regra do nome”: elas NAO sao trocadas na renderizacao (o artigo nao pode divergir do registro selado) e entram como a errata E43, ao lado,
em nome proprio da gerencia c1. Escrito pelo claude-construtor-v411 em nome da gerencia (registro). Idempotente: se o marcador ja' estiver, nao acrescenta. uso: python -B -X utf8 _ao_lado_desenho_e43_v411.py"""
import datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "DESENHO_v411.md")
MARCA = "<!-- ao_lado_e43_seis_aberturas_12nov -->"
b = open(P, "rb").read()
if MARCA.encode("utf-8") in b:
    print("ja' registrado"); raise SystemExit(0)
assert b.endswith(b"\r\n") and b"\n" not in b.replace(b"\r\n", b""), "o DESENHO nao e' CRLF puro"
txt = ("\r\n\r\n## AO LADO (12/11/2026, em nome da gerência c1, registrado pelo claude-construtor-v411; a decisão da gerência sobre um item da seção 7) " + MARCA + "\r\n\r\n"
       "- **Decisão da gerência (12/11/2026):** as seis aberturas da seção da Escala que identificam o operador contra a regra do nome (D122, D123) NÃO são trocadas na renderização: o artigo não pode divergir do registro selado. "
       "Entram como a errata E43, ao lado, em nome próprio da gerência c1; o texto selado da v410 não é reescrito. A linha da seção 7 que dizia “entram no texto do artigo regenerado, com a troca dita” fica como registro; vale a linha da tabela abaixo.\r\n"
       "- **E43** errata da gerência c1, em nome próprio (as seis aberturas da seção da Escala, no texto selado da v410): onde as seis aberturas identificam o operador contra a regra do nome (D122, D123), lê-se “por definição e nome do operador”; "
       "o texto selado da v410 não é reescrito e o artigo regenerado não diverge do registro selado; a errata vai ao lado.\r\n"
       "- A tabela da seção 7, AO LADO (vale esta linha):\r\n\r\n"
       "| item da seção 7 | nesta versão (AO LADO, 12/11) |\r\n"
       "|---|---|\r\n"
       "| as seis aberturas da seção da Escala que identificam o operador contra a regra do nome | entram como E43, ao lado (não são trocadas na renderização: o artigo não pode divergir do registro selado) |\r\n")
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(bak, "wb").write(b); assert open(bak, "rb").read() == b
novo = b + txt.encode("utf-8")
open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo); os.replace(P + ".tmp", P)
assert os.path.getsize(P) > len(b) and open(P, "rb").read().startswith(b)
print("AO LADO E43 acrescentado | backup", os.path.basename(bak), "|", len(b), "->", len(novo), "B")
