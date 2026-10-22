# -*- coding: utf-8 -*-
"""Regra dos dois arquivos (ordem do operador, 18/09): o MEMORY.md ficaria com > 24 000 B com a linha da v380. Move VERBATIM para o fim do MEMORY_2.md
três linhas longas do índice (Fases 1–4; Fases 5–6; Fase 7), com marcador de origem, e deixa no MEMORY.md o ponteiro curto. Nada se corta.
Backup de bytes; tmp -> conferir -> replace. Fail-closed: aborta antes de tocar se não achar exatamente as 3 linhas ou se a economia for < 700 B."""
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
UMEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"; ST = time.strftime("%Y%m%d_%H%M%S"); HOJE = time.strftime("%d/%m/%Y"); D = HOJE[:5]
M1, M2 = os.path.join(UMEM, "MEMORY.md"), os.path.join(UMEM, "MEMORY_2.md")
raw1, raw2 = open(M1, "rb").read(), open(M2, "rb").read()
assert b"\r\n" not in raw1
lines = raw1.decode("utf-8").split("\n")
ALVOS = {
    "(fase7-cc-covariancia-01out.md)": "- [Fase 7 — covariância dos cronômetros (01/10)](fase7-cc-covariancia-01out.md) — íntegra no MEMORY_2.md (movida %s); as Fases 4–5 enfraquecem" % D,
    "(fase5-sh0es-01out.md)": "- [Fase 5 — SH0ES](fase5-sh0es-01out.md) · [Fase 6 — ECO V3/V4/V5](fase6-eco-radical-01out.md) — íntegras no MEMORY_2.md (movida %s); par (√β|sin 2θ, lei) falsificado; desvios do pipeline ditos" % D,
    "(fase1-eff-30set.md)": "- [Fases 1–3 (30/09)](fase1-eff-30set.md) · [Fase 2](fase2-dois-setores-30set.md) · [Fase 3](fase3-leitores-h0-30set.md) · [Fase 4, o desvio](fase4-desvio-30set.md) — íntegras no MEMORY_2.md (movida %s); a Fase 7 enfraquece a leitura dos relógios" % D,
}
movidas = []
for i, l in enumerate(lines):
    for chave, curta in ALVOS.items():
        if chave in l and l.startswith("- ["):
            movidas.append(l); lines[i] = curta
assert len(movidas) == 3, ("esperava mover 3 linhas; achei %d" % len(movidas), [m[:60] for m in movidas])
novo1 = "\n".join(lines).encode("utf-8")
assert len(novo1) <= len(raw1) - 600, ("economia insuficiente", len(raw1), len(novo1))
nl2 = "\r\n" if raw2.count(b"\r\n") > raw2.count(b"\n") // 2 else "\n"
bloco = ("\n\n## %s — linhas do índice movidas VERBATIM do MEMORY.md pela regra dos dois arquivos (compactação para a v380; o MEMORY.md ficaria com > 24 000 B)\n\n" % HOJE + "\n".join(movidas) + "\n").replace("\n", nl2)
novo2 = raw2 + bloco.encode("utf-8")
for p, raw in ((M1, raw1), (M2, raw2)):
    b = p + ".bak_" + ST + "_compact380"; assert not os.path.exists(b); open(b, "wb").write(raw); assert open(b, "rb").read() == raw
for p, novo, raw in ((M2, novo2, raw2), (M1, novo1, raw1)):
    tmp = p + ".tmp_" + ST; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo) and open(p, "rb").read() == raw; os.replace(tmp, p)
print("MEMORY.md %d -> %d B | MEMORY_2.md %d -> %d B | movidas %d linhas (verbatim no fim do MEMORY_2)" % (len(raw1), len(novo1), len(raw2), len(novo2), len(movidas)))
for m in movidas:
    print("  ->", m[:110])
