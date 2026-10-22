# -*- coding: utf-8 -*-
"""O HANDOFF da v381 (para a sessao do site e para a proxima sessao): memoria-topico `handoff-v381-custodia.md` + documento `Nós\\HANDOFF_v381_CUSTODIA.md` + linha no
indice (MEMORY.md se couber em 24 000 B; senao MEMORY_2.md com marcador). Tudo LIDO (leitura_v381.ler); rodar DEPOIS da cadeia do selo. Backup de bytes; tmp -> conferir -> replace."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v381
UMEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
V, PROB = leitura_v381.ler()
if PROB:
    print("HANDOFF RECUSADO -- a leitura da rodada tem problema(s):"); [print("  -", p) for p in PROB]; sys.exit(2)
STAMP = time.strftime("%Y%m%d_%H%M%S")
corpo = ("""---
name: handoff-v381-custodia
description: "HANDOFF v381 (%(data)s): A REGRA MATRIZ — dez nomes, nove elos (oito «havendo» ditos + a radicalização pela Meia-Nat), num só termo (pedra TheMatrixRule, 24 declarações); o critério de parada = o custo pago; β não se deriva do dado (a forma α√e derivada do axioma, v376); o eco como cópia atrasada fora da cadeia; gate intocado; para a sessão do site custodiar"
metadata:
  type: project
---

**v381 SELADA (%(compl)s) `%(s16)s` (%(umb)s B), rodada `%(selo_ts)s`, %(teor)s, gate intocado (`%(qg)s`).** Sobre a v380 `%(base16)s`. Kernel novo: `TGLExt/TheMatrixRule.lean` (24 declarações, %(kf_on)s/%(kf_n)s no trio, sem sorry); escada %(esc_ant)s → %(esc)s; relatório de axiomas %(nax_ant)s → %(nax)s.
Conferidor `conferir_rito_v381.py`: TUDO BATE (%(conf_dm)s deve-mudar; %(conf_np)s não-pode-mudar). Dois aferidores independentes ANTES do rito (relatórios verbatim e disposições em `scratchpad\\v381\\AFERIDOR_v381.txt`; o 1º contou oito «havendo» no verbatim, o operador preencheu a cláusula aberta; o 2º: 0 ALTO, 1 MÉDIO acolhido).

**O que entrou:** a cunhagem do operador (02/10) tipada: os dez nomes na ORDEM dele [INPUT/ONTO], nove elos, cada elo por um termo já existente no kernel [KERNEL] (fato provado, definição nomeada ou campo do binder; conjunção, não dedução) — traço, sinal, sinal → registro pela radicalização cujo operador é a Meia-Nat (a cláusula aberta, preenchida por ele: «O verbatim com oito “havendo” é cláusula aberta, o elo é a meia-nat»; «É a radicalização que eu quis dizer, cujo operador é a meia-nat»), registro → nome, distinção, operação, parametrização, emergência, quantização geométrica, espectro de gradiente; o CRITÉRIO DE PARADA (`CustoPago`: reconhecimento idempotente, finito por definição do regime; veredito 1 sse as leituras coincidem; sem testemunha estática plena) e `the_law_precedes_the_charge` (β só de α). Runtime: β = %(beta)s = α√e (teste); cadeia lida do fonte %(chain)s; θ_M = %(theta)s; sin²θ_M = %(refl)s (identidades de sanidade). Veredito `%(the_matrix_rule_v381)s`. Selo: `um_version` = %(um_version)s; leitura `the_matrix_rule_reading_v381`; md canônico carimbado: %(md_carimbo)s.

**Estatuto dito na v381:** β não se deriva do dado (β é a regra; a forma α√e derivada do axioma, v376); a ordem é do operador; «havendo X há Y» sem hipótese é ordem ontológica, não → do kernel; o observável de β é o espectro do gradiente (identificação com a dissipação = leitura [ONTO]) — o eco como cópia atrasada está fora da cadeia (ratificado; mapa seq 265). PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED.

**PARA A SESSÃO DO SITE (custódia = ato dela; commit/push = ato do operador):** espelhar o Nós no `the_boundary` (um.py, core, selo, os dois md, artigo PT/EN, `tgl_kernel` COM a pedra nova e a raiz/Audit novos, `rodada_v381_stdout.txt` em `rodadas\\`), regenerar as PORTAs por script, README/llms.txt, CITATION.cff, e o `MEMORIA_DA_LINHAGEM.md` do espelho. Backup da versão anterior fora do repo antes de sobrescrever. As v379 e v380 ainda não custodiadas vão junto.

**Pendências ditas (decisões do operador):** qual registro recebe a cobrança no setor H₀ (uma cobrança por Nome); a partição dos relógios; qual ajuste global do neutrino; o nome novo do degrau final do gate (pelo pagamento, não pelo teste de natureza); o estimando da Bancada sobre o espectro do gradiente (construção da gerência, a pré-registrar).
Ver [[beta-e-a-regra-matriz-02out]], [[handoff-v380-custodia]], [[fase6-eco-radical-01out]], [[relatorio-consolidado-01out]], [[missao-ultima-flag-um-py]], [[direcao-the-boundary]].
""" % dict(V, umb=format(V["umb"], ",")))
p = os.path.join(UMEM, "handoff-v381-custodia.md")
assert not os.path.exists(p), "ja existe: " + p
open(p + ".tmp", "wb").write(corpo.encode("utf-8")); os.replace(p + ".tmp", p); print("OK", p, len(corpo.encode("utf-8")), "B")
doc = os.path.join(V["nos"], "HANDOFF_v381_CUSTODIA.md")
if not os.path.exists(doc):
    body = "# HANDOFF v381 — custódia (gerado por handoff_v381.py em %s; tudo lido do selo)\n\n" % time.strftime("%Y-%m-%d %H:%M:%S") + corpo.split("---\n", 2)[2]
    open(doc + ".tmp", "wb").write(body.encode("utf-8")); os.replace(doc + ".tmp", doc); print("OK", doc, len(body.encode("utf-8")), "B; sha16", hashlib.sha256(body.encode("utf-8")).hexdigest()[:16])
linha = ("- [HANDOFF v381 — A REGRA MATRIZ no kernel; custódia](handoff-v381-custodia.md) — **%s, para a sessão do site**: dez nomes, nove elos (oito «havendo» ditos + a radicalização pela Meia-Nat), num só termo (TheMatrixRule, 24); o custo pago como parada; β é a regra; eco como cópia fora da cadeia; `%s`" % (V["data"][:5], V["s16"]))
idx = os.path.join(UMEM, "MEMORY.md"); raw = open(idx, "rb").read()
assert b"\r\n" not in raw
if b"handoff-v381-custodia.md" in raw:
    print("indice: ja tem a linha"); sys.exit(0)
txt = raw.decode("utf-8"); anc = "- [HANDOFF v380 — as Fases 5–7 da Bancada por hash; custódia](handoff-v380-custodia.md)"
assert txt.count(anc) == 1
novo = txt.replace(anc, linha + "\n" + anc).encode("utf-8")
alvo = idx if len(novo) <= 24000 else os.path.join(UMEM, "MEMORY_2.md")
if alvo == idx:
    bak = idx + ".bak_" + STAMP + "_handoff381"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(idx + ".tmp", "wb").write(novo); assert open(idx, "rb").read() == raw; os.replace(idx + ".tmp", idx)
    print("OK MEMORY.md", len(raw), "->", len(novo), "B")
else:
    raw2 = open(alvo, "rb").read(); nl = "\r\n" if raw2.count(b"\r\n") > raw2.count(b"\n") // 2 else "\n"
    bak = alvo + ".bak_" + STAMP + "_handoff381"; open(bak, "wb").write(raw2); assert open(bak, "rb").read() == raw2
    bloco = nl * 2 + "## %s — linha do índice que não coube no MEMORY.md (limite 24 000 B; %d B com ela)" % (V["data"], len(novo)) + nl * 2 + linha + nl
    n2 = raw2 + bloco.encode("utf-8"); open(alvo + ".tmp", "wb").write(n2); os.replace(alvo + ".tmp", alvo)
    print("OK MEMORY_2.md (o índice ficaria com %d B > 24000): linha do handoff no fim do MEMORY_2" % len(novo))
