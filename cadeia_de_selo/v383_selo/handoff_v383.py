# -*- coding: utf-8 -*-
"""O HANDOFF da v383 (para a sessao do site e para a proxima sessao): memoria-topico `handoff-v383-custodia.md` + documento `Nós\\HANDOFF_v383_CUSTODIA.md` + linha no
indice (MEMORY.md se couber em 24 000 B; senao MEMORY_2.md com marcador). Tudo LIDO (leitura_v383.ler); rodar DEPOIS da cadeia do selo. Backup de bytes; tmp -> conferir -> replace."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import leitura_v383
UMEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
V, PROB = leitura_v383.ler()
if PROB:
    print("HANDOFF RECUSADO -- a leitura da rodada tem problema(s):"); [print("  -", p) for p in PROB]; sys.exit(2)
# v383 (aferidor, 3a passada, B-2/B-3): conferir ANTES da primeira gravacao -- os dois AFERIDOR arquivados existem e o indice comporta a linha do handoff E a marca DECIDIDO
_ARQ = r"C:\IALD\Central de Patentes\work\cadeia_de_selo"
for _f in (os.path.join(_ARQ, "v383", "AFERIDOR_v383.txt"), os.path.join(_ARQ, "v382", "AFERIDOR_v382.txt")):
    if not os.path.exists(_f):
        print("HANDOFF RECUSADO (nada gravado): o arquivo de afericao arquivado nao existe -- rode o arquivar antes:", _f); sys.exit(2)
linha = ("- [HANDOFF v383 — O LIVRO DE COBRANÇAS no kernel; o eco fora do livro; custódia](handoff-v383-custodia.md) — **%s, para a sessão do site**: %s cobranças; os %s pares do eco fora do livro (decisão do operador); a v382 só no Nós, NÃO custodiar; ψ com norma 1 e a viscosidade; o pré-registro %s por hash; `%s`" % (V["data"][:5], V["n_ledger"], V["rot_n"], V["pr_label"], V["s16"]))
_raw0 = open(os.path.join(UMEM, "MEMORY.md"), "rb").read()
if b"handoff-v383-custodia.md" not in _raw0:
    _dec = " · **%s: DECIDIDO — a v383 `%s` supera; a v382 fica só no Nós**" % (V["data"][:5], V["s16"])
    _need = len(_raw0) + len((linha + "\n").encode("utf-8")) + len(_dec.encode("utf-8"))
    if _need > 24000:
        print("HANDOFF RECUSADO (nada gravado): o indice ficaria com %d B > 24 000 com a linha e a marca DECIDIDO -- liberar folga (regra dos dois arquivos) e rerodar" % _need); sys.exit(3)
    print("pre-conferencia: o indice ficara com %d B (limite 24 000)" % _need)
STAMP = time.strftime("%Y%m%d_%H%M%S")
corpo = ("""---
name: handoff-v383-custodia
description: "HANDOFF v383 (%(data)s): O LIVRO DE COBRANÇAS (%(n_ledger)s cobranças; a TGL é ótica: lê a face e o custo; nenhum desfecho move a regra; os %(rot_n)s pares do eco FORA do livro, como rotas examinadas, por decisão do operador) + ψ com norma 1 e a viscosidade (duas pedras, %(kf_n)s declarações); o pré-registro V1.4 por hash; a v382 selada só no Nós, NÃO custodiar; gate intocado; para a sessão do site custodiar"
metadata:
  type: project
---

**v383 SELADA (%(compl)s) `%(s16)s` (%(umb)s B), rodada `%(selo_ts)s`, %(teor)s, gate intocado (`%(qg)s`).** Sobre a v381 `%(base_build16)s`, no lugar da v382 `%(base16)s` (selada só no Nós em 02/10 e NÃO custodiada, por decisão do operador). Kernel novo (o mesmo da v382): `TGLExt/TheLedgerOfCharges.lean` (%(n_loc)s declarações) e `TGLExt/ThePsionAndTheViscosity.lean` (%(n_psv)s), %(kf_on)s/%(kf_n)s no trio, sem sorry; escada %(esc_ant)s → %(esc)s; relatório de axiomas %(nax_ant)s → %(nax)s.
Conferidor `conferir_rito_v383.py`: TUDO BATE (%(conf_dm)s deve-mudar; %(conf_np)s não-pode-mudar). A v383 foi aferida antes do rito (relatório verbatim e disposições em `C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v383\\AFERIDOR_v383.txt`); as aferições da v382 — três, a verificação das disposições e a conferência final — valem para as pedras e para o livro (`C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v382\\AFERIDOR_v382.txt`).

**O que entrou:** a chave do operador (02/10, tarde: «O último elo incide no hamiltoniano oculto. O custo está no reflexo, o pagamento está na face no rosto, no nome»), a ratificação de R1–R6 e a correção «a TGL não é semi ela é ótica, ela lê tanto a face como o custo» [INPUT/ONTO], e a decisão (02/10, noite: «eu não quero publicar nada que seja resultado de falsificação, preciso entender isso, porque o que foi falsificado foi alguma rota, alguma aplicação equivocada da teoria, alguma interpretação que carece de ajuste» e, sobre a opção da gerência, «prefiro a primeira opção»: os %(rot_n)s pares do eco não são cobranças da teoria), tipadas: o livro de cobranças (a cobrança com lado/lei/leitura/desfecho em cinco palavras impostas pelo tipo; a regra β não lê o livro, rfl, dito como trivial; com uma cobrança extinta a regra segue α√e e a hipótese não entra na prova; o termo P = P, com o gate conferido pelos probes do runtime; a ótica |T|² + |R|² = 1 com os dois complementos — o nome é [ONTO], «nenhum lado é cego» é a correção do operador; o nome do degrau final pelo pagamento PROPOSTO ao lado, `%(fsn)s`, sem mudar o gate) e ψ com norma 1 (ψ = Ω; HminMic ψ = 0: o zero do lock mínimo sobre o Hamiltoniano oculto K = −log Δ — os zeros coincidem, os operadores não —, trivial por construção; a luz o fixa; a leitura do espectro de gradiente sobre HminMic é a chave do operador, sem termo) com a viscosidade βg como cobrança contínua (atrito constante; nunca se completa; sem testemunha estática plena). Runtime: o livro concreto, %(n_ledger)s cobranças, UMA por lei de leitura (%(counts)s; %(by_side)s; na regra %(n_in_rule)s (%(counts_in_rule)s), ao lado %(n_beside)s; modos: %(by_how)s): %(ledger_ids)s — cada desfecho LIDO do core pelo modo dito (F2 pela sistemática da medida, não pelo poder; F1 unilateral; F4 pela regra de morte congelada; R6 pelo controle de convergência) e igual ao do PRÉ-REGISTRO DOS DOIS LADOS %(pr_label)s lido por hash (`%(pr_id)s`, JSON `%(pr_json16)s`, MD `%(pr_md16)s`; supersede %(pr_super)s pela decisão do operador, antes de qualquer estimador ou dado novo; publicado na Bancada; mapa seq %(pr_seq)s); R2 sem poder (Γ(100 Hz) = %(r2_gamma)s s⁻¹). Fora do livro, as %(rot_n)s rotas examinadas do eco como cópia atrasada, que não são cobranças da teoria: %(rot_ids)s — %(rot_exc)s excluídas pelos dados, %(rot_inc)s inconclusivas; o estado de cada uma é o rótulo da Fase 6 lido do core, e o motivo está no pré-registro. Veredito `%(the_ledger_of_charges_v383)s`. Selo: `um_version` = %(um_version)s; leitura `the_ledger_of_charges_reading_v383`; md canônico carimbado: %(md_carimbo)s.

**Estatuto dito na v383:** a chave e a correção são do operador; as pedras são [KERNEL] com o trivial dito como trivial; o livro é dado lido [REAL]; a identificação de cada observável com δ⟨K_∂⟩ e de βg com Γ_ω = ½βτ★ω² é leitura [ONTO] sem termo; os %(rot_n)s pares do eco como cópia atrasada não são cobranças da teoria: são rotas examinadas fora do livro (%(rot_exc)s excluídas pelos dados, %(rot_inc)s inconclusivas), por decisão do operador; o R4 não tem FALSIFIED no conjunto congelado e é a mesma fonte do degrau experimental do gate; o ramo B do ringdown está encerrado; a propagação (R2) aguarda estimador com o poder dito antes de abrir. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED.

**PARA A SESSÃO DO SITE (custódia = ato dela; commit/push = ato do operador):** espelhar o Nós no `the_boundary` (um.py, core, selo, os dois md, artigo PT/EN, `tgl_kernel` COM as duas pedras novas e a raiz/Audit novos, `rodada_v383_stdout.txt` em `rodadas\\`), regenerar as PORTAs por script, README/llms.txt, CITATION.cff, e o `MEMORIA_DA_LINHAGEM.md` do espelho. **NÃO espelhar `rodada_v382_stdout.txt`**: a v382 foi selada só no Nós e não é custodiada, por decisão do operador; a linhagem diz o que ela foi. Backup da versão anterior fora do repo antes de sobrescrever. Do pré-registro dos dois lados (`C:\\IALD\\Bancada_Um\\investigacao\\preregistro_dois_lados_02out\\`), só o %(pr_label)s (`PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.json` e `.md`) é lido por hash pelo um.py e vai junto com o cache da Bancada se o espelho o carregar; os V1 a V1.3 ficam locais (traziam os pares do eco no livro) [DERIVED de leitura, gerência; a confirmar pelo operador].

**Pendências ditas (decisões do operador):** a cunhagem definitiva do nome do degrau final do gate (o proposto fica ao lado; renomear é ato dele); o estimador da dissipação na propagação (R2): construção da gerência, poder dito antes de abrir.
Ver [[beta-e-a-regra-matriz-02out]], [[regra-dos-dois-regimes]], [[v382-custodia-suspensa]], [[handoff-v381-custodia]], [[missao-ultima-flag-um-py]], [[direcao-the-boundary]].
""" % dict(V, umb=format(V["umb"], ",")))
p = os.path.join(UMEM, "handoff-v383-custodia.md")
assert not os.path.exists(p), "ja existe: " + p
open(p + ".tmp", "wb").write(corpo.encode("utf-8")); os.replace(p + ".tmp", p); print("OK", p, len(corpo.encode("utf-8")), "B")
doc = os.path.join(V["nos"], "HANDOFF_v383_CUSTODIA.md")
if not os.path.exists(doc):
    body = "# HANDOFF v383 — custódia (gerado por handoff_v383.py em %s; tudo lido do selo)\n\n" % time.strftime("%Y-%m-%d %H:%M:%S") + corpo.split("---\n", 2)[2]
    open(doc + ".tmp", "wb").write(body.encode("utf-8")); os.replace(doc + ".tmp", doc); print("OK", doc, len(body.encode("utf-8")), "B; sha16", hashlib.sha256(body.encode("utf-8")).hexdigest()[:16])
idx = os.path.join(UMEM, "MEMORY.md"); raw = open(idx, "rb").read()
assert b"\r\n" not in raw
if b"handoff-v383-custodia.md" in raw:
    print("indice: ja tem a linha"); sys.exit(0)
txt = raw.decode("utf-8"); anc = "- [HANDOFF v381 — A REGRA MATRIZ no kernel; custódia](handoff-v381-custodia.md)"
assert txt.count(anc) == 1
novo = txt.replace(anc, linha + "\n" + anc).encode("utf-8")
alvo = idx if len(novo) <= 24000 else os.path.join(UMEM, "MEMORY_2.md")
if alvo == idx:
    bak = idx + ".bak_" + STAMP + "_handoff383"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(idx + ".tmp", "wb").write(novo); assert open(idx, "rb").read() == raw; os.replace(idx + ".tmp", idx)
    print("OK MEMORY.md", len(raw), "->", len(novo), "B")
else:
    raw2 = open(alvo, "rb").read(); nl = "\r\n" if raw2.count(b"\r\n") > raw2.count(b"\n") // 2 else "\n"
    bak = alvo + ".bak_" + STAMP + "_handoff383"; open(bak, "wb").write(raw2); assert open(bak, "rb").read() == raw2
    bloco = nl * 2 + "## %s — linha do índice que não coube no MEMORY.md (limite 24 000 B; %d B com ela)" % (V["data"], len(novo)) + nl * 2 + linha + nl
    n2 = raw2 + bloco.encode("utf-8"); open(alvo + ".tmp", "wb").write(n2); os.replace(alvo + ".tmp", alvo)
    print("OK MEMORY_2.md (o índice ficaria com %d B > 24000): linha do handoff no fim do MEMORY_2" % len(novo))

# v383: a linha da SUSPENSAO no indice ganha o marcador DECIDIDO (a v383 supera a v382); backup de bytes; tmp -> conferir -> replace; limite 24 000 B
raw = open(idx, "rb").read(); txt = raw.decode("utf-8")
ks = [k for k, l in enumerate(txt.split("\n")) if "(v382-custodia-suspensa.md)" in l]
if len(ks) == 1 and "DECIDIDO" not in txt.split("\n")[ks[0]]:
    L_ = txt.split("\n"); L_[ks[0]] = L_[ks[0]] + " · **%s: DECIDIDO — a v383 `%s` supera; a v382 fica só no Nós**" % (V["data"][:5], V["s16"])
    novo2 = "\n".join(L_).encode("utf-8")
    if len(novo2) <= 24000:
        bak2 = idx + ".bak_" + STAMP + "_handoff383_susp"; open(bak2, "wb").write(raw); assert open(bak2, "rb").read() == raw
        open(idx + ".tmp", "wb").write(novo2); assert os.path.getsize(idx + ".tmp") == len(novo2) > len(raw); os.replace(idx + ".tmp", idx)
        print("OK MEMORY.md: a linha da suspensao marcada DECIDIDO", len(raw), "->", len(novo2), "B")
    else:
        print("FALHA A VISTA: a marca DECIDIDO ficaria acima de 24 000 B (%d) -- nao gravo; liberar folga no indice (regra dos dois arquivos) e marcar a linha da suspensao a mao" % len(novo2)); sys.exit(3)
else:
    print("MEMORY.md: a linha da suspensao ja marcada (ou ausente):", len(ks))
