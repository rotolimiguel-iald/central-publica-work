# -*- coding: utf-8 -*-
"""O HANDOFF da v380 (para a sessao do site e para a proxima sessao): memoria-topico `handoff-v380-custodia.md` + documento `Nós\\HANDOFF_v380_CUSTODIA.md` + linha no
indice (MEMORY.md se couber em 24 000 B; senao MEMORY_2.md com marcador). Tudo LIDO (leitura_v380.ler); rodar DEPOIS da cadeia do selo. Backup de bytes; tmp -> conferir -> replace."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v380
UMEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
V, PROB = leitura_v380.ler()
if PROB:
    print("HANDOFF RECUSADO -- a leitura da rodada tem problema(s):"); [print("  -", p) for p in PROB]; sys.exit(2)
STAMP = time.strftime("%Y%m%d_%H%M%S")
m = json.load(open(os.path.join(HERE, "v380_incorporacao_manifesto.json"), encoding="utf-8"))
corpo = ("""---
name: handoff-v380-custodia
description: "HANDOFF v380 (%(data)s): as Fases 5, 6 (ECO V3 + V4 + V5) e 7 da Bancada, o banco de GW e seis erratas da auditoria (+1 da v378, +1 nota) ao lado, lidos por hash; SEM kernel novo; gate intocado; para a sessão do site custodiar"
metadata:
  type: project
---

**v380 SELADA (%(compl)s) `%(s16)s` (%(umb)s B), rodada `%(selo_ts)s`, %(teor)s, gate intocado (`%(qg)s`).** Sobre a v379 `%(base16)s`. SEM kernel novo (escada %(esc)s inalterada; %(kmat)s).
Conferidor `conferir_rito_v380.py`: TUDO BATE (%(conf_dm)s deve-mudar; %(conf_np)s não-pode-mudar). Aferidor independente ANTES do rito (relatório em `scratchpad\\v380\\AFERIDOR_v380.txt`).

**O que entrou (runtime, por hash):** `prove_bancada_fases_5_6_7_v380` = `%(bancada_fases_5_6_7_v380)s`. Fase 5: H₀ da escada %(h0_v)s ± %(h0_s)s (z %(h0_z)s); δ sombra z %(p5_z)s. Fase 6 (ECO V3): KMS todos â = %(k6_a)s ± %(k6_s)s, z_excl %(k6_z1)s/%(k6_z2)s (sist. %(k6_sys)s); O4 cego z_excl %(o6_z1)s/%(o6_z2)s; MAY inconclusivo (sist. %(m6_sys)s); V4 (não cega) sin 2θ × MAY z_excl %(v4_z2)s, controles %(v4_ctrl)sσ; V5 (cega para a lei nova, DEC = 2GM_f/(β c³) do acervo de dez/2025): z_excl %(v5_z1)s/%(v5_z2)s (O4 %(v5_o1)s/%(v5_o2)s), o par do documento (β) sem poder (%(v5_r3p)sσ; rótulo da regra %(v5_r3lab)s; cláusula V5 %(v5_clausula)s). Fase 7: T z do ganho %(t7_diag)s → %(t7_m20)s; U ln B(sombra/acumulada) %(u7_diag)s → %(u7_m20)s. Banco: %(gb_ok)s/%(gb_n)s. Selo: `um_version` = %(um_version)s; EV-06 (conjunta V3; D1 V3 real) no selo; md canônico carimbado: %(md_carimbo)s.

**Estatuto dito na v380:** falsificar o PAR (leitura, lei de atraso) não falsifica a teoria; as leis de atraso são [INPUT/ONTO/DECLARADO]; sin 2θ é [CONJECTURE]; o peso da resposta da fronteira ao gráviton e a lei de atraso são decisões do operador; a leitura «sombra» é [OPEN/ONTO]; «todos» na covariância é faixa; o «100σ» de dezembro segue retirado (v340). PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED.

**PARA A SESSÃO DO SITE (custódia = ato dela; commit/push = ato do operador):** espelhar o Nós no `the_boundary` (um.py, core, selo, os dois md, artigo PT/EN, `tgl_kernel` inalterado, `rodada_v380_stdout.txt` em `rodadas\\`), regenerar as PORTAs por script, README/llms.txt, CITATION.cff, e o `MEMORIA_DA_LINHAGEM.md` do espelho. Backup da versão anterior fora do repo antes de sobrescrever. O cache `bancada_01out\\` e `gw\\` (com `ECHO_ANCHORED_V3_RESULT.json` e `GWOSC_O4_32S_V1.manifest.json`) é o que o um.py lê por hash: espelhar junto. Os 350 npz de O4 (`Bancada_Um\\fontes_externas\\gwosc_o4`, 38 GB de hdf5 + 350 janelas) NÃO vão ao espelho: ficam na custódia local (manifesto com sha256 no cache).

**Pendências ditas (decisões do operador):** a lei de atraso do eco (as três do acervo estão medidas: MAY inconclusiva; KMS e DEC falsificadas para √β e sin 2θ) e o peso da resposta da fronteira ao gráviton (CT-03); a leitura «sombra»; qual fundo é o fundo; a forma da E1; a entrada do NuFIT (RNC-01); o nome do gate (GV-01/02).
Ver [[fase6-eco-radical-01out]], [[fase7-cc-covariancia-01out]], [[fase5-sh0es-01out]], [[handoff-v379-custodia]], [[missao-ultima-flag-um-py]], [[direcao-the-boundary]].
""" % dict(V, umb=format(V["umb"], ",")))
p = os.path.join(UMEM, "handoff-v380-custodia.md")
assert not os.path.exists(p), "ja existe: " + p
open(p + ".tmp", "wb").write(corpo.encode("utf-8")); os.replace(p + ".tmp", p); print("OK", p, len(corpo.encode("utf-8")), "B")
doc = os.path.join(V["nos"], "HANDOFF_v380_CUSTODIA.md")
if not os.path.exists(doc):
    body = "# HANDOFF v380 — custódia (gerado por handoff_v380.py em %s; tudo lido do selo)\n\n" % time.strftime("%Y-%m-%d %H:%M:%S") + corpo.split("---\n", 2)[2]
    open(doc + ".tmp", "wb").write(body.encode("utf-8")); os.replace(doc + ".tmp", doc); print("OK", doc, len(body.encode("utf-8")), "B; sha16", hashlib.sha256(body.encode("utf-8")).hexdigest()[:16])
linha = ("- [HANDOFF v380 — as Fases 5–7 da Bancada por hash; custódia](handoff-v380-custodia.md) — **%s, para a sessão do site**: o par (√β ou sin 2θ, 2π/κ e DEC) falsificado; MAY inconclusivo; cronômetros com covariância; sem kernel novo; `%s`" % (V["data"][:5], V["s16"]))
idx = os.path.join(UMEM, "MEMORY.md"); raw = open(idx, "rb").read()
assert b"\r\n" not in raw
if b"handoff-v380-custodia.md" in raw:
    print("indice: ja tem a linha"); sys.exit(0)
txt = raw.decode("utf-8"); anc = "- [HANDOFF v379 — A RAZÃO ELEMENTAR; custódia](handoff-v379-custodia.md)"
assert txt.count(anc) == 1
novo = txt.replace(anc, linha + "\n" + anc).encode("utf-8")
alvo = idx if len(novo) <= 24000 else os.path.join(UMEM, "MEMORY_2.md")
if alvo == idx:
    bak = idx + ".bak_" + STAMP + "_handoff380"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(idx + ".tmp", "wb").write(novo); assert open(idx, "rb").read() == raw; os.replace(idx + ".tmp", idx)
    print("OK MEMORY.md", len(raw), "->", len(novo), "B")
else:
    raw2 = open(alvo, "rb").read(); nl = "\r\n" if raw2.count(b"\r\n") > raw2.count(b"\n") // 2 else "\n"
    bak = alvo + ".bak_" + STAMP + "_handoff380"; open(bak, "wb").write(raw2); assert open(bak, "rb").read() == raw2
    bloco = nl * 2 + "## %s — linha do índice que não coube no MEMORY.md (limite 24 000 B; %d B com ela)" % (V["data"], len(novo)) + nl * 2 + linha + nl
    n2 = raw2 + bloco.encode("utf-8"); open(alvo + ".tmp", "wb").write(n2); os.replace(alvo + ".tmp", alvo)
    print("OK MEMORY_2.md (o índice ficaria com %d B > 24000): linha do handoff no fim do MEMORY_2" % len(novo))
