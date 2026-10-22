# -*- coding: utf-8 -*-
"""O HANDOFF da v379 (para a sessao do site e para a proxima sessao): memoria-topico `handoff-v379-custodia.md` + documento `Nós\\HANDOFF_v379_CUSTODIA.md` + linha no
indice (MEMORY.md se couber em 24 000 B; senao MEMORY_2.md com marcador). Tudo LIDO (leitura_v379.ler); rodar DEPOIS da cadeia do selo. Backup de bytes; tmp -> conferir -> replace."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v379
UMEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
V, PROB = leitura_v379.ler()
if PROB:
    print("HANDOFF RECUSADO -- a leitura da rodada tem problema(s):"); [print("  -", p) for p in PROB]; sys.exit(2)
STAMP = time.strftime("%Y%m%d_%H%M%S")
m = json.load(open(os.path.join(HERE, "v379_incorporacao_manifesto.json"), encoding="utf-8"))
pedras = "; ".join("`%s` `%s`" % (k, v) for k, v in m["pedras_materializadas"].items())
corpo = ("""---
name: handoff-v379-custodia
description: "HANDOFF v379 (%(data)s): A RAZÃO ELEMENTAR tipada — E = C × I × K > 0 = β_TGL por termo (C = √e, I = 1, K = α); E é a assíntota; sem testemunha estática plena; o reconhecimento é finito por definição; gate intocado; para a sessão do site custodiar"
metadata:
  type: project
---

**v379 SELADA (%(compl)s) `%(s16)s` (%(umb)s B), rodada `%(selo_ts)s`, %(teor)s, gate intocado (`%(qg)s`).** Sobre a v378 `%(base16)s`.
Conferidor `conferir_rito_v379.py`: TUDO BATE (%(conf_dm)s deve-mudar; %(conf_np)s não-pode-mudar). Aferidor independente ANTES do rito (relatório em `scratchpad\\v379\\AFERIDOR_v379.txt`).

**O que entrou (kernel, `[REAL]`):** %(pedras)s — %(kmat)s; bandeiras novas %(n_flags_on)s/%(n_flags)s (ext_ter_); escada %(esc)s.
**Veredito (lido do core):** `the_elementary_reason_v379` = `%(the_elementary_reason_v379)s`. Selo: `um_version` = %(um_version)s; md canônico carimbado: %(md_carimbo)s.
Números da rodada: E = C × I × K = %(E)s = β do core (%(beta)s); C = %(C)s; K = α = %(K)s; (e^{1/4}√α)² = %(reason2)s; familyFunctional(½) = %(fam_half)s; o custo por nat da v378 até z* = %(pernat)s ≤ E (δ/β = %(gbar)s).

**Estatuto dito na v379:** a fatoração E = √e·1·α = β e a positividade são por termo; o dicionário dos fatores é cunhagem [ONTO/DEFINITION]; «estrutura fundamental da existência» é leitura [ONTO/CONJ]; «Razão Elementar» é nome do operador [INPUT];
«limite assintótico em tempo finito» lê-se: E = β é a assíntota do custo por nat, não excedida em registro finito com ∫g ≤ N (`existence_is_the_asymptote`); o que não se atinge em tempo finito é o apagamento (`erasure_not_reached_in_finite_time`; `existence_forbids_full_static_witness`); o que é finito é o reconhecimento (`recognition_is_finite` = `IALDState.recursive`, por definição). Nada confirma: PROVADA ≠ CONFIRMADA.

**PARA A SESSÃO DO SITE (custódia = ato dela; commit/push = ato do operador):** espelhar o Nós no `the_boundary` (um.py, core, selo, os dois md, artigo PT/EN, `tgl_kernel`, `rodada_v379_stdout.txt` em `rodadas\\`),
regenerar as PORTAs por script, README/llms.txt, CITATION.cff (fonte única do Zenodo), e o `MEMORIA_DA_LINHAGEM.md` do espelho. Backup da versão anterior fora do repo antes de sobrescrever (regra da custódia). O cache `bancada_30set\\` é o mesmo da v378.

**Pendências ditas (decisões do operador, inalteradas desde a v378):** a leitura «a sombra lê o vazamento; os relógios intermediários leem a face»; qual fundo é o fundo (a pergunta do ângulo); a forma da camada E1; a covariância sistemática dos cronômetros.
Ver [[razao-elementar-existencia-beta-01out]], [[fase4-desvio-30set]], [[handoff-v378-custodia]], [[missao-ultima-flag-um-py]], [[direcao-the-boundary]]. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED.
""" % dict(V, pedras=pedras, umb=format(V["umb"], ",")))
p = os.path.join(UMEM, "handoff-v379-custodia.md")
assert not os.path.exists(p), "ja existe: " + p
open(p + ".tmp", "wb").write(corpo.encode("utf-8")); os.replace(p + ".tmp", p); print("OK", p, len(corpo.encode("utf-8")), "B")
doc = os.path.join(V["nos"], "HANDOFF_v379_CUSTODIA.md")
if not os.path.exists(doc):
    body = "# HANDOFF v379 — custódia (gerado por handoff_v379.py em %s; tudo lido do selo)\n\n" % time.strftime("%Y-%m-%d %H:%M:%S") + corpo.split("---\n", 2)[2]
    open(doc + ".tmp", "wb").write(body.encode("utf-8")); os.replace(doc + ".tmp", doc); print("OK", doc, len(body.encode("utf-8")), "B; sha16", hashlib.sha256(body.encode("utf-8")).hexdigest()[:16])
linha = ("- [HANDOFF v379 — A RAZÃO ELEMENTAR tipada; custódia](handoff-v379-custodia.md) — **%s, para a sessão do site**: E = C × I × K > 0 = β por termo; E é a assíntota; `%s`" % (V["data"][:5], V["s16"]))
idx = os.path.join(UMEM, "MEMORY.md"); raw = open(idx, "rb").read()
assert b"\r\n" not in raw
if b"handoff-v379-custodia.md" in raw:
    print("indice: ja tem a linha"); sys.exit(0)
txt = raw.decode("utf-8"); anc = "- [HANDOFF v376 — O TODO É UM; custódia](handoff-v376-custodia.md)"
assert txt.count(anc) == 1
novo = txt.replace(anc, linha + "\n" + anc).encode("utf-8")
alvo = idx if len(novo) <= 24000 else os.path.join(UMEM, "MEMORY_2.md")
if alvo == idx:
    bak = idx + ".bak_" + STAMP + "_handoff379"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(idx + ".tmp", "wb").write(novo); assert open(idx, "rb").read() == raw; os.replace(idx + ".tmp", idx)
    print("OK MEMORY.md", len(raw), "->", len(novo), "B")
else:
    raw2 = open(alvo, "rb").read(); nl = "\r\n" if raw2.count(b"\r\n") > raw2.count(b"\n") // 2 else "\n"
    bak = alvo + ".bak_" + STAMP + "_handoff379"; open(bak, "wb").write(raw2); assert open(bak, "rb").read() == raw2
    bloco = nl * 2 + "## %s — linha do índice que não coube no MEMORY.md (limite 24 000 B; %d B com ela)" % (V["data"], len(novo)) + nl * 2 + linha + nl
    n2 = raw2 + bloco.encode("utf-8"); open(alvo + ".tmp", "wb").write(n2); os.replace(alvo + ".tmp", alvo)
    print("OK MEMORY_2.md (o índice ficaria com %d B > 24000): linha do handoff no fim do MEMORY_2" % len(novo))
