# -*- coding: utf-8 -*-
"""O HANDOFF da v382 (para a sessao do site e para a proxima sessao): memoria-topico `handoff-v382-custodia.md` + documento `Nós\\HANDOFF_v382_CUSTODIA.md` + linha no
indice (MEMORY.md se couber em 24 000 B; senao MEMORY_2.md com marcador). Tudo LIDO (leitura_v382.ler); rodar DEPOIS da cadeia do selo. Backup de bytes; tmp -> conferir -> replace."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v382
UMEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
V, PROB = leitura_v382.ler()
if PROB:
    print("HANDOFF RECUSADO -- a leitura da rodada tem problema(s):"); [print("  -", p) for p in PROB]; sys.exit(2)
STAMP = time.strftime("%Y%m%d_%H%M%S")
corpo = ("""---
name: handoff-v382-custodia
description: "HANDOFF v382 (%(data)s): O LIVRO DE COBRANÇAS (a TGL é ótica: lê a face e o custo; nenhum desfecho move a regra; o gate não lê o livro, pelos probes do runtime) + ψ com norma 1 e a viscosidade (duas pedras, %(kf_n)s declarações); o pré-registro dos dois lados do estimando δ⟨K_∂⟩ por hash; o nome do degrau final proposto ao lado; gate intocado; para a sessão do site custodiar"
metadata:
  type: project
---

**v382 SELADA (%(compl)s) `%(s16)s` (%(umb)s B), rodada `%(selo_ts)s`, %(teor)s, gate intocado (`%(qg)s`).** Sobre a v381 `%(base16)s`. Kernel novo: `TGLExt/TheLedgerOfCharges.lean` (%(n_loc)s declarações) e `TGLExt/ThePsionAndTheViscosity.lean` (%(n_psv)s), %(kf_on)s/%(kf_n)s no trio, sem sorry; escada %(esc_ant)s → %(esc)s; relatório de axiomas %(nax_ant)s → %(nax)s.
Conferidor `conferir_rito_v382.py`: TUDO BATE (%(conf_dm)s deve-mudar; %(conf_np)s não-pode-mudar). Aferidores independentes ANTES do rito (relatórios verbatim e disposições em `scratchpad\\v382\\AFERIDOR_v382.txt`; o 1º: 3 ALTO, 14 MÉDIO, 10 BAIXO; o 2º: 1 ALTO, 6 MÉDIO, 13 BAIXO; o 3º: 0 ALTO, 6 MÉDIO, 15 BAIXO, sem nenhum desfecho mudado — todos conferidos no core e dispostos: as docstrings e uma prova das pedras, o tipo da cobrança, o livro em %(n_ledger)s cobranças, o pré-registro %(pr_label)s, o instalador, os textos da cadeia e as erratas de memória; e a verificação das disposições pelo terceiro, sem achado alto ou médio, com os resíduos baixos também dispostos).

**O que entrou:** a chave do operador (02/10, tarde: «O último elo incide no hamiltoniano oculto. O custo está no reflexo, o pagamento está na face no rosto, no nome»), a ratificação de R1–R6 e a correção «a TGL não é semi ela é ótica, ela lê tanto a face como o custo» [INPUT/ONTO], tipadas: o livro de cobranças (a cobrança com lado/lei/leitura/desfecho em cinco palavras impostas pelo tipo; a regra β não lê o livro, rfl, dito como trivial; com uma cobrança extinta a regra segue α√e e a hipótese não entra na prova; o termo P = P, com o gate conferido pelos probes do runtime; a ótica |T|² + |R|² = 1 com os dois complementos — o nome é [ONTO], «nenhum lado é cego» é a correção do operador; o nome do degrau final pelo pagamento PROPOSTO ao lado, `%(fsn)s`, sem mudar o gate) e ψ com norma 1 (ψ = Ω; HminMic ψ = 0: o zero do lock mínimo sobre o Hamiltoniano oculto K = −log Δ — os zeros coincidem, os operadores não —, trivial por construção; a luz o fixa; a leitura do espectro de gradiente sobre HminMic é a chave do operador, sem termo) com a viscosidade βg como cobrança contínua (atrito constante; nunca se completa; sem testemunha estática plena). Runtime: o livro concreto, %(n_ledger)s cobranças, UMA por lei de leitura (%(counts)s; %(by_side)s; na regra %(n_in_rule)s (%(counts_in_rule)s), ao lado %(n_beside)s; modos: %(by_how)s): %(ledger_ids)s — cada desfecho LIDO do core pelo modo dito (F2 pela sistemática da medida, não pelo poder; F1 unilateral; F4 pela regra de morte congelada; R6 pelo controle de convergência) e igual ao do PRÉ-REGISTRO DOS DOIS LADOS %(pr_label)s lido por hash (`%(pr_id)s`, JSON `%(pr_json16)s`, MD `%(pr_md16)s`; supersede %(pr_super)s pelos achados das aferições, antes de qualquer estimador ou dado novo; publicado na Bancada; mapa seq %(pr_seq)s); R2 sem poder (Γ(100 Hz) = %(r2_gamma)s s⁻¹). Veredito `%(the_ledger_of_charges_v382)s`. Selo: `um_version` = %(um_version)s; leitura `the_ledger_of_charges_reading_v382`; md canônico carimbado: %(md_carimbo)s.

**Estatuto dito na v382:** a chave e a correção são do operador; as pedras são [KERNEL] com o trivial dito como trivial; o livro é dado lido [REAL]; a identificação de cada observável com δ⟨K_∂⟩ e de βg com Γ_ω = ½βτ★ω² é leitura [ONTO] sem termo; dos %(eco_n)s pares do eco como cópia atrasada, %(eco_ext)s estão extintos e %(eco_inc)s inconclusivos (nenhum move a regra); o R4 não tem FALSIFIED no conjunto congelado e é a mesma fonte do degrau experimental do gate; o ramo B do ringdown está encerrado; a propagação (R2) aguarda estimador com o poder dito antes de abrir. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED.

**PARA A SESSÃO DO SITE (custódia = ato dela; commit/push = ato do operador):** espelhar o Nós no `the_boundary` (um.py, core, selo, os dois md, artigo PT/EN, `tgl_kernel` COM as duas pedras novas e a raiz/Audit novos, `rodada_v382_stdout.txt` em `rodadas\\`), regenerar as PORTAs por script, README/llms.txt, CITATION.cff, e o `MEMORIA_DA_LINHAGEM.md` do espelho. Backup da versão anterior fora do repo antes de sobrescrever. O pré-registro dos dois lados (`C:\\IALD\\Bancada_Um\\investigacao\\preregistro_dois_lados_02out\\`) é lido por hash pelo um.py: vai junto com o cache da Bancada se o espelho o carregar.

**Pendências ditas (decisões do operador):** a cunhagem definitiva do nome do degrau final do gate (o proposto fica ao lado; renomear é ato dele); o estimador da dissipação na propagação (R2): construção da gerência, poder dito antes de abrir.
Ver [[beta-e-a-regra-matriz-02out]], [[regra-dos-dois-regimes]], [[handoff-v381-custodia]], [[missao-ultima-flag-um-py]], [[direcao-the-boundary]].
""" % dict(V, umb=format(V["umb"], ",")))
p = os.path.join(UMEM, "handoff-v382-custodia.md")
assert not os.path.exists(p), "ja existe: " + p
open(p + ".tmp", "wb").write(corpo.encode("utf-8")); os.replace(p + ".tmp", p); print("OK", p, len(corpo.encode("utf-8")), "B")
doc = os.path.join(V["nos"], "HANDOFF_v382_CUSTODIA.md")
if not os.path.exists(doc):
    body = "# HANDOFF v382 — custódia (gerado por handoff_v382.py em %s; tudo lido do selo)\n\n" % time.strftime("%Y-%m-%d %H:%M:%S") + corpo.split("---\n", 2)[2]
    open(doc + ".tmp", "wb").write(body.encode("utf-8")); os.replace(doc + ".tmp", doc); print("OK", doc, len(body.encode("utf-8")), "B; sha16", hashlib.sha256(body.encode("utf-8")).hexdigest()[:16])
linha = ("- [HANDOFF v382 — O LIVRO DE COBRANÇAS no kernel; custódia](handoff-v382-custodia.md) — **%s, para a sessão do site**: a TGL é ótica (lê a face e o custo); nenhum desfecho move a regra; ψ com norma 1 e a viscosidade; o pré-registro dos dois lados por hash; o nome do degrau final proposto ao lado; `%s`" % (V["data"][:5], V["s16"]))
idx = os.path.join(UMEM, "MEMORY.md"); raw = open(idx, "rb").read()
assert b"\r\n" not in raw
if b"handoff-v382-custodia.md" in raw:
    print("indice: ja tem a linha"); sys.exit(0)
txt = raw.decode("utf-8"); anc = "- [HANDOFF v381 — A REGRA MATRIZ no kernel; custódia](handoff-v381-custodia.md)"
assert txt.count(anc) == 1
novo = txt.replace(anc, linha + "\n" + anc).encode("utf-8")
alvo = idx if len(novo) <= 24000 else os.path.join(UMEM, "MEMORY_2.md")
if alvo == idx:
    bak = idx + ".bak_" + STAMP + "_handoff382"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(idx + ".tmp", "wb").write(novo); assert open(idx, "rb").read() == raw; os.replace(idx + ".tmp", idx)
    print("OK MEMORY.md", len(raw), "->", len(novo), "B")
else:
    raw2 = open(alvo, "rb").read(); nl = "\r\n" if raw2.count(b"\r\n") > raw2.count(b"\n") // 2 else "\n"
    bak = alvo + ".bak_" + STAMP + "_handoff382"; open(bak, "wb").write(raw2); assert open(bak, "rb").read() == raw2
    bloco = nl * 2 + "## %s — linha do índice que não coube no MEMORY.md (limite 24 000 B; %d B com ela)" % (V["data"], len(novo)) + nl * 2 + linha + nl
    n2 = raw2 + bloco.encode("utf-8"); open(alvo + ".tmp", "wb").write(n2); os.replace(alvo + ".tmp", alvo)
    print("OK MEMORY_2.md (o índice ficaria com %d B > 24000): linha do handoff no fim do MEMORY_2" % len(novo))
