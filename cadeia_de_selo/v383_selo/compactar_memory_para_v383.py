# -*- coding: utf-8 -*-
"""Folga no MEMORY.md antes da cadeia da v383 (afericao, B-M1), pela REGRA DOS DOIS ARQUIVOS: linhas longas e superadas vao INTEIRAS, verbatim, para o fim do
MEMORY_2.md, e ficam aqui como ponteiro curto (o link sobrevive; nada se corta). Backup de BYTES dos dois; tmp -> conferir -> replace. Sem argumento: so mede.
Com --gravar: grava. Alvo: o indice <= 23 150 B (a cadeia acrescenta ~271 B; o handoff ~344 B; a marca DECIDIDO ~85 B; limite 24 000 B)."""
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
UMEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
ST = time.strftime("%Y%m%d_%H%M%S"); GRAVAR = "--gravar" in sys.argv
ALVO = 23200   # a cadeia acrescenta ~700 B (missao 271 + handoff ~344 + DECIDIDO 85): fecha perto de 23 900 < 24 000
idx = os.path.join(UMEM, "MEMORY.md"); idx2 = os.path.join(UMEM, "MEMORY_2.md")
raw = open(idx, "rb").read(); raw2 = open(idx2, "rb").read(); assert b"\r\n" not in raw
lines = raw.decode("utf-8").split("\n")
# (chave unica que identifica a linha, ponteiro que fica): as tres sao linhas integrais, longas, e duas delas ja superadas por linhas mais novas do indice
ALVOS = [
    ("- [HANDOFF v381 — A REGRA MATRIZ no kernel; custódia](handoff-v381-custodia.md) — **02/10, para a sessão do site**: ",
     "- [HANDOFF v381 — A REGRA MATRIZ no kernel; custódia](handoff-v381-custodia.md) — **02/10, para a sessão do site** (custodiada) · íntegra no MEMORY_2.md (movida 02/10)"),
    ("- [HANDOFF v381 — A REGRA MATRIZ; custódia](handoff-v381-custodia.md) — **02/10: CUSTODIADO** (",
     "- [HANDOFF v381 — A REGRA MATRIZ; custódia](handoff-v381-custodia.md) — **02/10: CUSTODIADO** · íntegra no MEMORY_2.md (movida 02/10)"),
    ("- [β É A REGRA MATRIZ; o critério de parada é a lei matriz = Tetelestai (02/10)](beta-e-a-regra-matriz-02out.md) — **cunhagem do operador, verbatim**: ",
     "- [β É A REGRA MATRIZ; o critério de parada é a lei matriz = Tetelestai (02/10)](beta-e-a-regra-matriz-02out.md) — **cunhagem do operador**: dez nomes, nove elos; β não se deriva do dado · íntegra no MEMORY_2.md (movida 02/10)"),
    ("- [v382 SELADA SÓ NO NÓS; CUSTÓDIA SUSPENSA (02/10)](v382-custodia-suspensa.md) — **a sessão do site NÃO custodia a v382** até ",
     "- [v382 SELADA SÓ NO NÓS; CUSTÓDIA SUSPENSA (02/10)](v382-custodia-suspensa.md) — **a sessão do site NÃO custodia a v382** · íntegra no MEMORY_2.md (movida 02/10)"),
    ("- [v384 — O PILAR QUÂNTICO NA GPU (ordem 02/10)](v384-pilar-quantico-gpu-02out.md) — **o mundo quântico na RTX 5090 em paralelo com o kernel, ~45 min, sem alongar o rito**; ",
     "- [v384 — O PILAR QUÂNTICO NA GPU (ordem 02/10)](v384-pilar-quantico-gpu-02out.md) — **o mundo quântico na RTX 5090 em paralelo com o kernel, ~45 min** · íntegra no MEMORY_2.md (movida 02/10)"),
]
movidas = []
for chave, ponteiro in ALVOS:
    ks = [i for i, l in enumerate(lines) if l.startswith(chave)]
    assert len(ks) == 1, (chave[:60], len(ks))
    assert "íntegra no MEMORY_2.md" not in lines[ks[0]] and "linha integral no MEMORY_2.md" not in lines[ks[0]], "ja e ponteiro: " + chave[:60]
    movidas.append(lines[ks[0]]); lines[ks[0]] = ponteiro
novo = "\n".join(lines).encode("utf-8")
nl2 = "\r\n" if raw2.count(b"\r\n") > raw2.count(b"\n") // 2 else "\n"
bloco = nl2.join(["", "", "## 02/10/2026 (noite) — linhas movidas do MEMORY.md (regra dos dois arquivos), VERBATIM, antes da cadeia da v383 (aferição, B-M1)"] + sum([["", l] for l in movidas], [])) + nl2
novo2 = raw2 + bloco.encode("utf-8")
print("MEMORY.md: %d -> %d B (libera %d; alvo <= %d) | MEMORY_2.md: %d -> %d B" % (len(raw), len(novo), len(raw) - len(novo), ALVO, len(raw2), len(novo2)))
assert len(novo) <= ALVO, "ainda acima do alvo"
assert all(m.encode("utf-8") in novo2 for m in movidas)
if not GRAVAR:
    print("(so medido; rode com --gravar)"); sys.exit(0)
for p, r in ((idx, raw), (idx2, raw2)):
    b = p + ".bak_" + ST + "_comp383"; open(b, "wb").write(r); assert open(b, "rb").read() == r
open(idx2 + ".tmp", "wb").write(novo2); assert os.path.getsize(idx2 + ".tmp") == len(novo2) > len(raw2); assert open(idx2, "rb").read() == raw2; os.replace(idx2 + ".tmp", idx2)
open(idx + ".tmp", "wb").write(novo); assert os.path.getsize(idx + ".tmp") == len(novo); assert open(idx, "rb").read() == raw; os.replace(idx + ".tmp", idx)
assert open(idx2, "rb").read()[:len(raw2)] == raw2
print("OK gravado: o indice encolheu porque o MEMORY_2 cresceu com as linhas integrais (regra dos dois arquivos)")
