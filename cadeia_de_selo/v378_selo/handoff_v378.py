# -*- coding: utf-8 -*-
"""O HANDOFF da v378 (para a sessao do site e para a proxima sessao): memoria-topico `handoff-v378-custodia.md` + documento `Nós\\HANDOFF_v378_CUSTODIA.md` + linha no
indice (MEMORY.md se couber em 24 000 B; senao MEMORY_2.md com marcador). Tudo LIDO (leitura_v378.ler); rodar DEPOIS da cadeia do selo. Backup de bytes; tmp -> conferir -> replace."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v378
UMEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
V, PROB = leitura_v378.ler()
if PROB:
    print("HANDOFF RECUSADO -- a leitura da rodada tem problema(s):"); [print("  -", p) for p in PROB]; sys.exit(2)
STAMP = time.strftime("%Y%m%d_%H%M%S")
m = json.load(open(os.path.join(HERE, "v378_incorporacao_manifesto.json"), encoding="utf-8"))
pedras = "; ".join("`%s` `%s`" % (k, v) for k, v in m["pedras_materializadas"].items())
corpo = ("""---
name: handoff-v378-custodia
description: "HANDOFF v378 (%(data)s): O QUE FALTOU (o núcleo derivado D1b tipado, K = E(z*)^{2β/3}, nunca testado na Bancada; a leitura da dupla contagem de β nas Fases 2–3, ao lado, E12); a lei da dissipação com contraste; a Fase 4 (o desvio) na convenção do artigo — a escada lê o fator, os relógios intermediários desfavorecem o fluxo acumulado; gate intocado; para a sessão do site custodiar"
metadata:
  type: project
---

**v378 SELADA (%(compl)s) `%(s16)s` (%(umb)s B), rodada `%(selo_ts)s`, %(teor)s, gate intocado (`%(qg)s`).** Sobre a v377 `%(base16)s`.
Conferidor `conferir_rito_v378.py`: TUDO BATE (%(conf_dm)s deve-mudar; %(conf_np)s não-pode-mudar). Aferidor independente ANTES do rito (relatório em `scratchpad\\v378\\AFERIDOR_v378.txt`).

**O que entrou (kernel, `[REAL]`):** %(pedras)s — %(kmat)s; bandeiras novas %(n_flags_on)s/%(n_flags)s (ext_dlc_); escada %(esc)s.
**Vereditos (lidos do core):** `the_dissipation_law_with_contrast_v378` = `%(the_dissipation_law_with_contrast_v378)s` · `what_was_missed_v378` = `%(what_was_missed_v378)s` ·
`bancada_fase4_v378` = `%(bancada_fase4_v378)s`. Selo: `um_version` = %(um_version)s; md canônico carimbado: %(md_carimbo)s.
Números da rodada: K_D1b = E(z*)^{2β/3} = %(Kb)s contra K_D1a = %(Ka)s (I_b = %(Ib)s nats; N* = %(Nstar)s; δ/β previsto = %(dpred)s); Fase 4: a escada δ = %(P_delta)s ± %(P_sigma)s por nat (%(P_z)sσ), pull %(P_pull)sσ, ln B %(P_lnB)s;
os %(cc_n)s cronômetros sozinhos: β̂ = %(T_bhat)s ± %(T_sigma)s (δ %(T_z)sσ), ganho da lei %(T_gain)sσ, ln B %(T_lnB)s (erros diagonais); conjunto %(S_z)sσ; controle empilhado %(ctrl_z)sσ; reanálise da Fase 3 (não-cega) `%(w_h)s`: leitores de sombra %(w_seis)sσ da lei D1b com o Planck ΛCDM.

**Leituras ao lado ditas na v378:** (E12) as Fases 2–3 e o parágrafo v377 aplicaram a lei sobre o fundo efetivo (β no fundo + lei); «dupla contagem» é leitura da gerência sob a convenção do artigo [DERIVED], não medida (aferidor B4); os números ficam · módulo de Coma v39: `flow_layer_kernel_v378` = `%(coma_v378)s` ao lado das antigas. Aferidor v378 aplicado antes do rito (0 A, 6 B, 7 C): vigia fail-closed; «não leem» → «desfavorecem» (P(β > 0) = %(T_frac0)s); D1b «nunca testado NA BANCADA»; a NEC dita na prosa, não hipótese de teorema; a circularidade transportada ao artigo.

**PARA A SESSÃO DO SITE (custódia = ato dela; commit/push = ato do operador):** espelhar o Nós no `the_boundary` (um.py, core, selo, os dois md, artigo PT/EN, `tgl_kernel`, `rodada_v378_stdout.txt` em `rodadas\\`),
regenerar as PORTAs por script, README/llms.txt, CITATION.cff (fonte única do Zenodo), e o `MEMORIA_DA_LINHAGEM.md` do espelho. Backup da versão anterior fora do repo antes de sobrescrever (regra da custódia).
Copiar também `A Ponte e o Um\\cache\\bancada_30set\\` (agora com a Fase 4, a reanálise, a prova de fumaça e os cronômetros, lidos por hash pelo rito).

**Pendências ditas (decisões do operador):** a leitura [OPEN] «a sombra lê o vazamento; os relógios intermediários leem a face» (se vale, a lei é lei da leitura por distância e o C.5b do artigo 1 fica desfavorecido); qual fundo é o fundo (a pergunta do ângulo);
a forma da camada E1 (Bancada «fator sobre o TOTAL» vs artigo √(1+β|1+w|)); a covariância sistemática dos cronômetros (Moresco+2020) para refinar o bloco T; o servidor da Bancada (18777) só vê `cc_moresco`/modo `artigo` depois de reiniciado.
Ver [[fase4-desvio-30set]], [[fase3-leitores-h0-30set]], [[fase2-dois-setores-30set]], [[desvio-de-beta-foco-dos-testes-30set]], [[missao-ultima-flag-um-py]], [[direcao-the-boundary]]. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED.
""" % dict(V, pedras=pedras, umb=format(V["umb"], ",")))
p = os.path.join(UMEM, "handoff-v378-custodia.md")
assert not os.path.exists(p), "ja existe: " + p
open(p + ".tmp", "wb").write(corpo.encode("utf-8")); os.replace(p + ".tmp", p); print("OK", p, len(corpo.encode("utf-8")), "B")
doc = os.path.join(V["nos"], "HANDOFF_v378_CUSTODIA.md")
if not os.path.exists(doc):
    body = "# HANDOFF v378 — custódia (gerado por handoff_v378.py em %s; tudo lido do selo)\n\n" % time.strftime("%Y-%m-%d %H:%M:%S") + corpo.split("---\n", 2)[2]
    open(doc + ".tmp", "wb").write(body.encode("utf-8")); os.replace(doc + ".tmp", doc); print("OK", doc, len(body.encode("utf-8")), "B; sha16", hashlib.sha256(body.encode("utf-8")).hexdigest()[:16])
linha = ("- [HANDOFF v378 — O QUE FALTOU; a lei com contraste; a Fase 4; custódia](handoff-v378-custodia.md) — **%s, para a sessão do site**: D1b tipado (K = E(z*)^{2β/3}); "
         "a escada lê o fator, os relógios intermediários desfavorecem o fluxo acumulado; `%s`" % (V["data"][:5], V["s16"]))
idx = os.path.join(UMEM, "MEMORY.md"); raw = open(idx, "rb").read()
assert b"\r\n" not in raw
if b"handoff-v378-custodia.md" in raw:
    print("indice: ja tem a linha"); sys.exit(0)
txt = raw.decode("utf-8"); anc = "- [HANDOFF v376 — O TODO É UM; custódia](handoff-v376-custodia.md)"
assert txt.count(anc) == 1
novo = txt.replace(anc, linha + "\n" + anc).encode("utf-8")
alvo = idx if len(novo) <= 24000 else os.path.join(UMEM, "MEMORY_2.md")
if alvo == idx:
    bak = idx + ".bak_" + STAMP + "_handoff378"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(idx + ".tmp", "wb").write(novo); assert open(idx, "rb").read() == raw; os.replace(idx + ".tmp", idx)
    print("OK MEMORY.md", len(raw), "->", len(novo), "B")
else:
    raw2 = open(alvo, "rb").read(); nl = "\r\n" if raw2.count(b"\r\n") > raw2.count(b"\n") // 2 else "\n"
    bak = alvo + ".bak_" + STAMP + "_handoff378"; open(bak, "wb").write(raw2); assert open(bak, "rb").read() == raw2
    bloco = nl * 2 + "## %s — linha do índice que não coube no MEMORY.md (limite 24 000 B; %d B com ela)" % (V["data"], len(novo)) + nl * 2 + linha + nl
    n2 = raw2 + bloco.encode("utf-8"); open(alvo + ".tmp", "wb").write(n2); os.replace(alvo + ".tmp", alvo)
    print("OK MEMORY_2.md (o índice ficaria com %d B > 24000): linha do handoff no fim do MEMORY_2" % len(novo))
