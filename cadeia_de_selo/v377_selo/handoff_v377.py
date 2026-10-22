# -*- coding: utf-8 -*-
"""O HANDOFF da v377 (para a sessao do site e para a proxima sessao): memoria-topico `handoff-v377-custodia.md` + documento `Nós\\HANDOFF_v377_CUSTODIA.md` + linha no
indice (MEMORY.md se couber em 24 000 B; senao MEMORY_2.md com marcador). Tudo LIDO (leitura_v377.ler); rodar DEPOIS da cadeia do selo. Backup de bytes; tmp -> conferir -> replace."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v377
UMEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
V, PROB = leitura_v377.ler()
if PROB:
    print("HANDOFF RECUSADO -- a leitura da rodada tem problema(s):"); [print("  -", p) for p in PROB]; sys.exit(2)
STAMP = time.strftime("%Y%m%d_%H%M%S")
m = json.load(open(os.path.join(HERE, "v377_incorporacao_manifesto.json"), encoding="utf-8"))
pedras = "; ".join("`%s` `%s`" % (k, v) for k, v in m["pedras_materializadas"].items())
corpo = ("""---
name: handoff-v377-custodia
description: "HANDOFF v377 (%(data)s): A LEI DA DISSIPAÇÃO PROVADA (dephasing = lei do fluxo = vazamento) — H₀_local = H₀_fundo·(1+z)^β como implicação no kernel; a física é a leitura (o leitor é a sombra do Um); as três fases da Bancada por hash; o desvio de β como foco; gate intocado; para a sessão do site custodiar"
metadata:
  type: project
---

**v377 SELADA (%(compl)s) `%(s16)s` (%(umb)s B), rodada `%(selo_ts)s`, %(teor)s, gate intocado (`%(qg)s`).** Sobre a v376 `%(base16)s`.
Conferidor `conferir_rito_v377.py`: TUDO BATE (%(conf_dm)s deve-mudar; %(conf_np)s não-pode-mudar). Aferidor independente ANTES do rito (relatório em `scratchpad\\v377\\AFERIDOR_v377.txt`).

**O que entrou (kernel, `[REAL]`):** %(pedras)s — %(kmat)s; bandeiras novas %(n_flags_on)s/%(n_flags)s (ext_pir_ 10, ext_dis_ 15); escada %(esc)s.
**Vereditos (lidos do core):** `the_dissipation_law_v377` = `%(the_dissipation_law_v377)s` · `physics_is_the_reading_v377` = `%(physics_is_the_reading_v377)s` ·
`bancada_fases_v377` = `%(bancada_fases_v377)s` · `final_stone_reading_v377` = `%(final_stone_reading_v377)s`. Selo: `um_version` = %(um_version)s; md canônico carimbado: %(md_carimbo)s.
Números da rodada: K = (1+z*)^β = %(K)s (z* = %(zstar)s; N* = %(Nstar)s nats; f_leak = %(fleak)s; H₀_local de 67,4 = %(H0loc)s); Fase 2: β̂ = %(f2_b)s ± %(f2_s)s por nat (α√e a %(f2_z)sσ),
pull da escada %(f2_pt)sσ no TGL contra %(f2_pl)sσ no ΛCDM, ln B %(f2_lnb)s; Fase 3: leitores de sombra %(f3_zum)sσ acima da face, %(f3_zlei)sσ contra K com o fundo efetivo, %(f3_D)sσ com o Planck 2018.

**Erratas ao lado ditas na v377:** módulo de Coma v39 «CONJECTURE_DECLARED» → `%(coma_v377)s` (a chave antiga fica) · artigo «o porquê está tipado, não provado» (E10) · D1 V3 (v349/v366): a tensão de 3–4σ é condicional ao mapa de R (E11) · o fator (1+z*)^β chamava-se «K» nos relatórios da Fase 3 → F_D1a.

**PARA A SESSÃO DO SITE (custódia = ato dela; commit/push = ato do operador):** espelhar o Nós no `the_boundary` (um.py, core, selo, os dois md, artigo PT/EN, `tgl_kernel`, `rodada_v377_stdout.txt` em `rodadas\\`),
regenerar as PORTAs por script, README/llms.txt, CITATION.cff (fonte única do Zenodo), e o `MEMORIA_DA_LINHAGEM.md` do espelho. Backup da versão anterior fora do repo antes de sobrescrever (regra da custódia).
Copiar também `A Ponte e o Um\\cache\\bancada_30set\\` (os artefatos das fases lidos por hash pelo rito).

**Pendências ditas:** Fase 4 (o desvio de β): a variável assintótica é decisão do operador; a pergunta do ângulo (BAO) com o fator (1+β) no mapa efetivo; o servidor da Bancada (18777) só vê `sh0es_local` depois de reiniciado;
o teste independente da lei (leitores novos além dos seis; z-dependência não é discriminante pela cunhagem «a escada lê da sombra»). Ver [[fase1-eff-30set]], [[fase2-dois-setores-30set]], [[fase3-leitores-h0-30set]],
[[lei-e-fato-correlatos-regra-matriz-30set]], [[desvio-de-beta-foco-dos-testes-30set]], [[pedra-final-espelhamento-30set]], [[missao-ultima-flag-um-py]], [[direcao-the-boundary]]. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED.
""" % dict(V, pedras=pedras, umb=format(V["umb"], ",")))
p = os.path.join(UMEM, "handoff-v377-custodia.md")
assert not os.path.exists(p), "ja existe: " + p
open(p + ".tmp", "wb").write(corpo.encode("utf-8")); os.replace(p + ".tmp", p); print("OK", p, len(corpo.encode("utf-8")), "B")
# o documento no Nós (para a sessão do site), com o mesmo corpo sem o frontmatter
doc = os.path.join(V["nos"], "HANDOFF_v377_CUSTODIA.md")
if not os.path.exists(doc):
    body = "# HANDOFF v377 — custódia (gerado por handoff_v377.py em %s; tudo lido do selo)\n\n" % time.strftime("%Y-%m-%d %H:%M:%S") + corpo.split("---\n", 2)[2]
    open(doc + ".tmp", "wb").write(body.encode("utf-8")); os.replace(doc + ".tmp", doc); print("OK", doc, len(body.encode("utf-8")), "B; sha16", hashlib.sha256(body.encode("utf-8")).hexdigest()[:16])
linha = ("- [HANDOFF v377 — A LEI DA DISSIPAÇÃO; custódia](handoff-v377-custodia.md) — **%s, para a sessão do site**: a lei provada como implicação; a física é a leitura; "
         "as fases 1–3 por hash; `%s`" % (V["data"][:5], V["s16"]))
idx = os.path.join(UMEM, "MEMORY.md"); raw = open(idx, "rb").read()
assert b"\r\n" not in raw
if b"handoff-v377-custodia.md" in raw:
    print("indice: ja tem a linha"); sys.exit(0)
txt = raw.decode("utf-8"); anc = "- [HANDOFF v376 — O TODO É UM; custódia](handoff-v376-custodia.md)"
assert txt.count(anc) == 1
novo = txt.replace(anc, linha + "\n" + anc).encode("utf-8")
alvo = idx if len(novo) <= 24000 else os.path.join(UMEM, "MEMORY_2.md")
if alvo == idx:
    bak = idx + ".bak_" + STAMP + "_handoff377"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(idx + ".tmp", "wb").write(novo); assert open(idx, "rb").read() == raw; os.replace(idx + ".tmp", idx)
    print("OK MEMORY.md", len(raw), "->", len(novo), "B")
else:
    raw2 = open(alvo, "rb").read(); nl = "\r\n" if raw2.count(b"\r\n") > raw2.count(b"\n") // 2 else "\n"
    bak = alvo + ".bak_" + STAMP + "_handoff377"; open(bak, "wb").write(raw2); assert open(bak, "rb").read() == raw2
    bloco = nl * 2 + "## %s — linha do índice que não coube no MEMORY.md (limite 24 000 B; %d B com ela)" % (V["data"], len(novo)) + nl * 2 + linha + nl
    n2 = raw2 + bloco.encode("utf-8"); open(alvo + ".tmp", "wb").write(n2); os.replace(alvo + ".tmp", alvo)
    print("OK MEMORY_2.md (o índice ficaria com %d B > 24000): linha do handoff no fim do MEMORY_2" % len(novo))
