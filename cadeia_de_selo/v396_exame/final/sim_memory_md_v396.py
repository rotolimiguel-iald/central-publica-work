# -*- coding: utf-8 -*-
"""sim_memory_md_v396.py -- exame final v396: reproduz, sobre uma COPIA do MEMORY.md real (memoria_copia/), a logica do passo 9 de
superficies_v396.py (troca do gancho da missao, a linha do handoff ANTES da do handoff v395, a compactacao de corridas de ganchos antigos
e os limites de 24.000 B / 195 linhas, alvo 192). O texto novo (gancho e handoff) e' um marcador do mesmo tamanho do que a cadeia escreve
(o tamanho real depende do V do rito). Nada real e' tocado."""
import sys, os
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
raw = open(os.path.join(H, "memoria_copia", "MEMORY.md"), "rb").read()
assert b"\r\n" not in raw
lines = raw.decode("utf-8").split("\n")
LIMITE, LIMITE_LINHAS = 24000, 195
k = [i for i, l in enumerate(lines) if "(missao-ultima-flag-um-py.md)" in l and l.startswith("- [")]
print("linhas antes:", len(lines) - 1, "bytes:", len(raw), "| gancho da missao:", k)
assert len(k) == 1
V = {"data": "22/10/2026", "s16": "0a4395a89eeebbb7", "teor": "9498/9498"}   # os textos REAIS de textos_v396.marca_missao / linha_handoff, com o V do candidato
lines[k[0]] = "- [Missão: mover a última flag do um.py](missao-ultima-flag-um-py.md) — " + ("**v396 SELADA %s `%s` %s COMPLETA (a testemunha estática na fractalização do Um; gate intocado)** · " % (V["data"][:5], V["s16"], V["teor"])) + "íntegra anterior no MEMORY_2.md (movida %s)" % V["data"][:5]
kh = [i for i, l in enumerate(lines) if "(handoff-v395-custodia.md)" in l and l.startswith("- [HANDOFF v395")]
print("ancora do handoff v395:", kh)
assert len(kh) == 1
lines.insert(kh[0], "- [HANDOFF v396 — a testemunha estática; custódia](handoff-v396-custodia.md) — **%s, para a sessão do site** · `%s`" % (V["data"][:5], V["s16"]))
gancho = lambda l: l.startswith("- [") and "MEMORY_2.md (" in l and "**" not in l and "linhas íntegras" not in l and "handoff-v39" not in l and "Ganchos antigos" not in l
ALVO = LIMITE_LINHAS - 3
print("depois da troca e do handoff:", len(lines) - 1, "linhas; alvo", ALVO)
corridas = []; i = 0
while i < len(lines):
    if gancho(lines[i]):
        j = i
        while j + 1 < len(lines) and gancho(lines[j + 1]):
            j += 1
        if j > i:
            corridas.append((i, j))
        i = j + 1
    else:
        i += 1
print("corridas compactaveis (inicio, fim, tamanho):", [(a + 1, b + 1, b - a + 1) for a, b in corridas])
print("linhas que sao gancho:", sum(1 for l in lines if gancho(l)), "| reducao maxima possivel:", sum(b - a for a, b in corridas))
falta = (len(lines) - 1) - ALVO; esc = []
if falta > 0:
    for a, b in sorted(corridas, key=lambda ab: -(ab[1] - ab[0])):
        if falta <= 0:
            break
        esc.append((a, b)); falta -= (b - a)
print("escolhidas:", [(a + 1, b + 1) for a, b in esc], "falta depois:", falta)
for a, b in sorted(esc, reverse=True):
    print("  compacta:", [l[:90] for l in lines[a:b + 1]])
    lines[a:b + 1] = ["- [Ganchos antigos consolidados (%d)](MEMORY_2.md) — %d linhas íntegras no MEMORY_2.md (movidas 22/10 pela regra dos dois arquivos)" % (b - a + 1, b - a + 1)]
novo = "\n".join(lines).encode("utf-8")
print("RESULTADO:", "RECUSA rc 3" if (falta > 0 or len(novo) > LIMITE or novo.count(b"\n") > LIMITE_LINHAS) else "COMPACTA E GRAVA", "| linhas", novo.count(b"\n"), "bytes", len(novo))
# folga: quantas linhas a mais (de fora da cadeia, antes do passo 9) a compactacao ainda absorveria
print("folga: a cadeia absorve ate", sum(b - a for a, b in corridas) - ((194 - ALVO)), "linha(s) a mais no indice antes do passo 9 (se nada mudar nas corridas)")
