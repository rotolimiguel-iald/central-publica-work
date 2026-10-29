# -*- coding: utf-8 -*-
"""compactar_indice_memoria_v404.py -- decisao da gerencia c1 (28/10/2026) sobre a UNICA checagem reprovada do p00 da v404:
o MEMORY.md (indice) nao comporta a linha do handoff da v404 (bytes hoje + 900 >= 24000). A regra dos dois arquivos (18/09/2026):
NADA se corta -- a linha sai INTEGRA para o MEMORY_2.md e fica no indice um ponteiro curto. Quatro linhas sao movidas/encurtadas:
(1) o handoff da v402 (dobra na linha consolidada v392-v401 -> v392-v402); (2) a linha das cunhagens de 07-11/10 (ja ponteiro, titulo longo);
(3) a linha consolidada dos handoffs (lista de arquivos); (4) a linha da memoria cientifica da fila (os marcadores HTML FICAM no indice, na mesma linha,
e os tres marcadores soltos das linhas vizinhas sobem para ela: a fila os procura por substring).
Backup de BYTES dos dois arquivos antes; temporario -> conferir -> substituir; o pino e' refeito logo em seguida (memoria.py pinar).
Uso: python -I -B -X utf8 compactar_indice_memoria_v404.py [--seco]"""
import hashlib
import os
import sys
import time

SECO = "--seco" in sys.argv
MEM = os.path.join(os.environ["USERPROFILE"], ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
P1 = os.path.join(MEM, "MEMORY.md")
P2 = os.path.join(MEM, "MEMORY_2.md")
TS = time.strftime("%Y%m%d_%H%M%S")
HANDOFF_BYTES_PREVISTOS = 900     # o que o p00 exige de folga para a linha do handoff da v404
LIMITE_BYTES = 24000
LIMITE_LINHAS = 195


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16]


def gravar(p, b):
    tmp = p + ".tmp_" + TS
    with open(tmp, "wb") as f:
        f.write(b)
    assert os.path.getsize(tmp) == len(b), ("tamanho do temporario nao bate", tmp)
    os.replace(tmp, p)


b1 = open(P1, "rb").read()
b2 = open(P2, "rb").read()
assert b"\r\n" not in b1, "o MEMORY.md tem CRLF: este script supoe LF (pare e olhe)"
linhas = b1.split(b"\n")
print("MEMORY.md antes: %d linhas, %d bytes, sha16 %s" % (len(linhas) - 1 if linhas and linhas[-1] == b"" else len(linhas), len(b1), sha16(b1)))


def achar(prefixo):
    ix = [i for i, l in enumerate(linhas) if l.startswith(prefixo.encode("utf-8"))]
    assert len(ix) == 1, ("a linha tem de existir UMA vez no indice", prefixo[:60], ix)
    return ix[0]


# (1) o handoff da v402 sai integro; a linha consolidada passa a v392-v402
i_v402 = achar("- [HANDOFF v402 — ponte da escala dual")
i_cons = achar("- [HANDOFFs v392–v401 (todos PUBLICADOS/CUSTODIADOS")
# (2) as cunhagens de 07-11/10
i_cun = achar("- [Cunhagens de 07–11/10 consolidadas (6):")
# (4) a memoria cientifica da fila e os tres marcadores soltos
i_fila = achar("- [Memória científica da fila (13/10–28/10:")
i_m1 = achar("<!-- IALD_ORDEM019_ADENDO003_COORD_20261007 -->")
i_m2 = achar("<!-- IALD_ORDEM019_ADENDO004_COORD_20261007 -->")
i_m3 = achar("<!-- IALD_QUEUE_MEMORY_V401_20261025 -->")

# (5) quatro linhas do «Ler primeiro»/«Estado corrente» com titulo longo: a integra vai ao MEMORY_2.md, fica o ponteiro curto (a primeira rodada liberou 542 B; faltavam ~400)
i_nomes = achar("- **[NOMES DAS PEDRAS E A IDENTIDADE = VERDADE (13/10)]")
i_g1 = achar("- **[G1 — custodiar.py: a custódia numa só ordem (24/10)]")
i_cons_d = achar("- **[CONSULTA DIÁRIA: patentes do acervo e e-mails da IALD pelo ChatGPT (26/10)]")
i_massa = achar("- **[A TRANSIÇÃO PARA A MASSA (28/10)]")
L_nomes = linhas[i_nomes]; L_g1 = linhas[i_g1]; L_cons_d = linhas[i_cons_d]; L_massa = linhas[i_massa]
NOVA_nomes = ("- **[NOMES DAS PEDRAS E A IDENTIDADE = VERDADE (13/10)](nomes-das-pedras-e-a-identidade-verdade-13out.md)** — Posto · Santo · IALD/Verbo Vivo; não perguntar de novo · **28/10: o triplo inteiro = Jo 8,32 (`Jo8v32`, v404); sen45° derivado** · íntegra no MEMORY_2.md (movida 28/10)").encode("utf-8")
NOVA_g1 = ("- **[G1 — custodiar.py: a custódia numa só ordem (24/10)](custodiar-g1-24out.md)** — `vigiar/sondar/planejar --seco/executar/auditar`; **L17 é decisão do operador** · [lições da cadeia v403 (28/10)](licoes-cadeia-v403-28out.md) · íntegra no MEMORY_2.md (movida 28/10)").encode("utf-8")
NOVA_cons_d = ("- **[CONSULTA DIÁRIA: patentes do acervo e e-mails da IALD pelo ChatGPT (26/10)](consulta-diaria-patentes-e-emails-26out.md)** — **ordem do operador**: diária nos dias úteis, à noite, aviso só com novidade; ORDEM 027 ao Codex · íntegra no MEMORY_2.md (movida 28/10)").encode("utf-8")
NOVA_massa = ("- **[A TRANSIÇÃO PARA A MASSA (28/10)](transicao-para-a-massa-28out.md)** — **levantamento**: a única massa de β é o neutrino (E₀ DECLARADA); nenhum «= β»; **pergunta viva: E₀** · íntegra no MEMORY_2.md (movida 28/10)").encode("utf-8")

L_v402 = linhas[i_v402]; L_cons = linhas[i_cons]; L_cun = linhas[i_cun]; L_fila = linhas[i_fila]
# os marcadores HTML da linha da fila (ficam TODOS no indice)
import re
marcadores = re.findall(rb"<!--[^>]*-->", L_fila)
assert len(marcadores) == 6, ("a linha da fila tem de ter 6 marcadores", len(marcadores))
marcadores_soltos = [linhas[i_m1], linhas[i_m2], linhas[i_m3]]

NOVA_cons = ("- [HANDOFFs v392–v402 (todos PUBLICADOS/CUSTODIADOS; v399 custodiada junto com a v400; arquivos handoff-vNNN-custodia.md e v393-selada-a-regra-e-o-coracao-14out.md)](MEMORY_2.md) "
             "— linhas íntegras no MEMORY_2.md (v392–v395 movidas 24/10; v396–v398 24/10 noite; v399 25/10; v400 26/10; v401 27/10; v402 28/10, pela regra dos dois arquivos)").encode("utf-8")
NOVA_cun = ("- [Cunhagens de 07–11/10 consolidadas (6)](MEMORY_2.md) — 6 linhas íntegras no MEMORY_2.md (movidas 27/10; a linha-título íntegra movida 28/10, pela regra dos dois arquivos); os tópicos seguem nos arquivos -07out a -11out").encode("utf-8")
NOVA_fila = ("- [Memória científica da fila (13/10–28/10: ordem permanente; v392–v403)](MEMORY_2.md) — linhas íntegras no MEMORY_2.md (movidas 23/10, 27/10 e 28/10 pela regra dos dois arquivos; diário novo nunca aqui) ").encode("utf-8") + b" ".join(marcadores + marcadores_soltos)

novas = list(linhas)
novas[i_cons] = NOVA_cons
novas[i_cun] = NOVA_cun
novas[i_fila] = NOVA_fila
novas[i_nomes] = NOVA_nomes
novas[i_g1] = NOVA_g1
novas[i_cons_d] = NOVA_cons_d
novas[i_massa] = NOVA_massa
# remover: a linha da v402 e os tres marcadores soltos (e um unico branco vizinho que ficaria duplicado)
remover = sorted([i_v402, i_m1, i_m2, i_m3], reverse=True)
for i in remover:
    del novas[i]
# compactar brancos duplicados que a remocao dos marcadores deixou (no maximo um branco seguido)
out = []
for l in novas:
    if l == b"" and out and out[-1] == b"":
        continue
    out.append(l)
nb1 = b"\n".join(out)
n_linhas = len(out) - 1 if out and out[-1] == b"" else len(out)
print("MEMORY.md depois: %d linhas, %d bytes (liberados %d); com o handoff previsto: %d (< %d: %s); linhas + 1 <= %d: %s"
      % (n_linhas, len(nb1), len(b1) - len(nb1), len(nb1) + HANDOFF_BYTES_PREVISTOS, LIMITE_BYTES, len(nb1) + HANDOFF_BYTES_PREVISTOS < LIMITE_BYTES, LIMITE_LINHAS, n_linhas + 1 <= LIMITE_LINHAS))
assert len(nb1) + HANDOFF_BYTES_PREVISTOS < LIMITE_BYTES - 100, "a compactacao NAO abre folga bastante: pare e decida outra linha"
assert n_linhas + 1 <= LIMITE_LINHAS
# nada se perde: cada linha integra movida vai ao MEMORY_2.md
anexo = (b"\n<!-- movidas 28/10 (compactacao do indice para a v404, gerencia c1; regra dos dois arquivos: as linhas INTEGRAS abaixo sairam do MEMORY.md e la ficou um ponteiro curto) -->\n"
         + L_v402 + b"\n" + L_cons + b"\n" + L_cun + b"\n" + L_fila + b"\n" + L_nomes + b"\n" + L_g1 + b"\n" + L_cons_d + b"\n" + L_massa + b"\n")
for l in (L_v402, L_cons, L_cun, L_fila, L_nomes, L_g1, L_cons_d, L_massa):
    assert l in anexo and l not in nb1
for m in marcadores + marcadores_soltos:
    assert m in nb1, ("marcador sumiu do indice", m)
if SECO:
    print("SECO: nada gravado. Linhas que sairiam integras:"); [print("  ", l[:120].decode("utf-8", "replace")) for l in (L_v402, L_cons, L_cun, L_fila, L_nomes, L_g1, L_cons_d, L_massa)]
    sys.exit(0)
# backups de BYTES, depois temporario -> conferir -> substituir
for p, b in ((P1, b1), (P2, b2)):
    bak = p + ".bak_" + TS
    with open(bak, "wb") as f:
        f.write(b)
    assert open(bak, "rb").read() == b
nb2 = b2 + anexo
gravar(P2, nb2)
assert os.path.getsize(P2) == len(b2) + len(anexo) and open(P2, "rb").read().endswith(anexo)
gravar(P1, nb1)
assert open(P1, "rb").read() == nb1
print("GRAVADO: MEMORY.md %d B sha16 %s ; MEMORY_2.md %d B (cresceu %d) ; backups .bak_%s" % (len(nb1), sha16(nb1), len(nb2), len(anexo), TS))
