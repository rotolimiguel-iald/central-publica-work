# -*- coding: utf-8 -*-
"""O HANDOFF da v386 (para a sessao do site e para a proxima sessao): memoria-topico NOVA `handoff-v386-custodia.md` + documento `Nós\\HANDOFF_v386_CUSTODIA.md`
+ a linha no indice (MEMORY.md, antes da linha do handoff v385). Tudo LIDO (leitura_v386.ler); rodar DEPOIS da cadeia do selo, do registro no mapa e do
arquivar (a guarda confere o CONSTRUIR e o conferidor arquivados). Backup de bytes; temporario -> conferir -> substituir. Molde: handoff_v385.py.
A GUARDA: ANTES da primeira gravacao confere (1) o CONSTRUIR_v386_resultado.json (as tres afericoes) e o conferir_rito_v386.py arquivados, (2) a ancora (a
linha do handoff v385) e (3) que o MEMORY.md comporta a linha do handoff (<= 24 000 B); se nao, RECUSA SEM GRAVAR NADA (rc 3). Se, entre a pre-conferencia
e a gravacao do indice, outra sessao encher o MEMORY.md, a linha NAO e' gravada (rc 3, dito); a memoria-topico e o documento ja gravados ficam.
v386: e' o handoff da CUSTODIA CONJUNTA v383 + v384 + v385 + v386 (decisao do operador de 05/10, 09:39 UTC, verbatim); o espelho leva a pedra nova,
TGLExt.lean, TGL/Audit.lean, os stdout, as tres subpastas de pre-registro (pilar, dois lados, ramo B) com PORTA por script; as pendencias ficam ditas.
Ensaio: V386_REMAP_DIR (as tres escritas vao para as copias, NUNCA para o Nos) + V386_WRITE_ROOT; ou o Nos SINTETICO (o documento vai ao Nos sintetico)."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v386 as A
import leitura_v386, textos_v386 as T
AMB = A.ambiente()
REMAP = AMB["remap"]
alvo = (lambda p: os.path.join(REMAP, os.path.basename(p))) if REMAP else (lambda p: p)
UMEM = AMB["umem"]
LIMITE = 24000
V, PROB = leitura_v386.ler()
if PROB:
    print("HANDOFF RECUSADO -- a leitura da rodada tem problema(s):"); [print("  -", p) for p in PROB]; sys.exit(2)
X = T._x(V)
_ARQ = os.path.join(AMB["arq_dest"], "v386")
for _f in (os.path.join(_ARQ, "CONSTRUIR_v386_resultado.json"), os.path.join(_ARQ, "pacote", "conferir_rito_v386.py"), os.path.join(_ARQ, "pacote", "ESPERADOS_v386.json")):
    if not os.path.exists(_f):
        print("HANDOFF RECUSADO (nada gravado): o arquivo arquivado nao existe -- rode o arquivar_v386.py antes:", _f); sys.exit(2)
linha = T.linha_handoff(V)
idx = alvo(os.path.join(UMEM, "MEMORY.md"))
_raw0 = open(idx, "rb").read()
assert b"\r\n" not in _raw0, "MEMORY.md com CRLF: o molde espera LF"


def com_a_linha(raw):
    if b"handoff-v386-custodia.md" in raw:
        return None
    L_ = raw.decode("utf-8").split("\n")
    ks = [i for i, l in enumerate(L_) if "(handoff-v385-custodia.md)" in l]
    if len(ks) != 1:
        print("HANDOFF RECUSADO (nada gravado): a ancora (a linha do handoff v385) aparece %d vez(es) no indice" % len(ks)); sys.exit(3)
    L_.insert(ks[0], linha)
    return "\n".join(L_).encode("utf-8")


_novo0 = com_a_linha(_raw0)
if _novo0 is not None:
    if len(_novo0) > LIMITE:
        print("HANDOFF RECUSADO (nada gravado): o indice ficaria com %d B > %d com a linha do handoff -- liberar folga (regra dos dois arquivos: "
              "compactar_memory_para_v386.py --gravar) e rerodar" % (len(_novo0), LIMITE)); sys.exit(3)
    print("pre-conferencia: o indice ficara com %d B (limite %d)" % (len(_novo0), LIMITE))
else:
    print("pre-conferencia: o indice ja tem a linha do handoff v386")
# ---- o que se le para o corpo
X["arq"] = os.path.join(A.TOOLS_REAL, "v386")
X["tent"] = ", ".join("`%s`" % t for t in V["tentativas"]) or "nenhuma nesta rodada"
X["marcador_p"] = os.path.join(A.PK, ".servidor_parado_pelo_rito")
_o = lambda n: leitura_v386.render_op((V.get("op") or {}).get(n))
for _n in ("custodia", "espelho", "subpasta", "v1_espelho", "w10", "ramo_b", "delegacao", "verbo_def", "nome_posto", "alpha2"):
    X["op_" + _n] = _o(_n)
_pb = [f for f in sorted(os.listdir(A.PRDIR_B)) if os.path.isfile(os.path.join(A.PRDIR_B, f))] if os.path.isdir(A.PRDIR_B) else []
X["prb_n"] = len(_pb); X["prb_bytes"] = format(sum(os.path.getsize(os.path.join(A.PRDIR_B, f)) for f in _pb), ","); X["prb_lista"] = ", ".join("`%s`" % f for f in _pb)
corpo = ("""---
name: handoff-v386-custodia
description: "HANDOFF v386 (%(data)s): CUSTÓDIA CONJUNTA v383 + v384 + v385 + v386 (decisão do operador, 05/10) — o Verbo seleciona [KERNEL + INPUT/ONTO]; o ramo B do ringdown reaberto por pré-registro (V1 por hash, nada aberto); a errata ao lado de R6; o pilar %(qr_curtissima)s; W10; as três subpastas de pré-registro ao espelho com PORTA; gate intocado%(sint)s"
metadata:
  type: project
---

**v386 SELADA (%(compl)s) `%(s16)s` (%(umb_fmt)s B), rodada `%(selo_ts)s`, %(teor)s, gate intocado (`%(qg)s`, %(n18)s/18).**%(sint)s Sobre a v385 `%(base16)s`. Escada %(esc_v385)s → %(esc)s; %(n_ver_iguais)s de %(n_ver)s vereditos da v385 inalterados (inclusive o do pilar); %(n_av_iguais)s de %(n_av)s módulos com o mesmo all_verified do estado selado da v385; por termo %(hvals)s. Conferidor `conferir_rito_v386.py` (cópia byte a byte do pacote): %(conf_res)s (%(conf_dm)s deve-mudar; %(conf_np)s não-pode-mudar; %(conf_md)s muda-e-é-dito; JSON `%(conf16)s`).%(conf_aceite_txt)s Aferida antes do rito em %(n_afer)s lentes adversariais (`CONSTRUIR_v386_resultado.json` `%(construir16)s`, arquivado em `%(arq)s`).

**O que entrou:** %(n_patches)s patches sobre a v385 (%(patches)s): a pedra `TGLExt/TheVerbSelectsTheAction.lean` (`%(vb_pedra16)s`; %(vb_n_pedra)s declarações) e os %(vb_n_ang)s termos do regime angular fiados na escada; `TGLExt.lean` `%(stone_tglext16)s` e `TGL/Audit.lean` `%(stone_audit16)s`; os registros `the_verb_v386` (`%(vb_v)s`), `ramo_b_preregistration_v386` (`%(rb_v)s`), `ledger_errata_v386` (`%(le_v)s`) e `quantum_pillar_reuse_v386` (`%(qr_v)s`) no core e no selo; a leitura `the_verb_reading_v386` e o token `verb_typing_stone_name_v386` (lido do kernel: `%(vb_token)s`); no artigo PT/EN a seção «Ao lado (v386)», a errata de R6, o V1 lido e o W10; no `.md` canônico a errata AO LADO de R6.

**O Verbo** (cunhagem: %(op_verbo_def)s; o Nome é o posto: %(op_nome_posto)s): o que a pedra prova está nos nomes dos termos (diário da linhagem desta data); c = β_TGL é [INPUT], nunca literal — o operador escreveu %(op_alpha2)s e a régua do signo lê β_TGL = α·√e (citação fica; correção ao lado). **O ramo B** (%(op_ramo_b)s): V1 `%(rb_id)s` lido por hash (JSON `%(rb_json16)s`, MD `%(rb_md16)s`, spec `%(rb_spec16)s`; %(rb_disk_txt)s); OUTRA LEI %(rb_forma)s, k = %(rb_k)s, M = %(rb_M)s; só o conjunto D (%(rb_nD)s de O4) testa, cego; `%(rb_vered_v1)s`; NADA ABERTO; as %(rb_erratas_n)s erratas ao lado no registro; decidido por delegação (%(op_delegacao)s). **A errata de R6:** o livro v383 intacto (%(le_n)s); F2b `%(le_f2b_token)s`; F2 e R2 como estão. **O pilar:** %(qr_txt)s; a reprodutibilidade v385 nesta rodada `%(rp_v)s` (%(rp_txt)s). **W10** (%(op_w10)s): %(w10_txt)s.

**Estatuto:** a pedra e a fiação angular são [KERNEL] (provam implicações; provada nunca é confirmada); as leituras são do operador e da gerência [INPUT/ONTO]; o V1 é [INPUT por hash]; o pilar é [COMPUTED]; o gate não se move. Não falsificado não é confirmado; nada aqui é confirmação.

**PARA A SESSÃO DO SITE — UM SÓ ATO para a v383, a v384, a v385 e a v386 (custódia = ato dela; commit/push = ato do operador; decisão do operador: %(op_custodia)s):**
- **o estado do Nós é o da v386** (espelhar por cima): `um.py`, `um_absoluto.json`, `um_absoluto_selo.json`, os dois `.md` canônicos, o artigo PT/EN (com o W10); `um_absoluto_pilar_quantico.json` (%(qp_arq_txt)s); `quantum_pillar\\pilar_quantico_worker.py` e `quantum_pillar\\pilar_quantico_spec.json`; a pasta da rodada do pilar da v385 (o resultado reaproveitado aqui; cache `%(qp_run_dir)s`, não se espelha o cache); `rodada_v383_stdout.txt`, `rodada_v384_stdout.txt`, `rodada_v385_stdout.txt` e `rodada_v386_stdout.txt` em `rodadas\\`; o `tgl_kernel`: a pedra nova `TheVerbSelectsTheAction.lean`, a da v385 `TheAxiomAndTheFalseWitness.lean`, a raiz `TGLExt.lean` e `TGL/Audit.lean` novos (e as duas pedras da v383, `TheLedgerOfCharges.lean` e `ThePsionAndTheViscosity.lean`, se o espelho ainda não as tem). Regenerar as PORTAs por script, README/llms.txt, CITATION.cff e a linhagem do espelho (as quatro versões). Backup da versão que ESTÁ no espelho, fora do repo, antes de sobrescrever.
- **o pré-registro do pilar** (decidido em 05/10: %(op_espelho)s; nome CONCORDADO: %(op_subpasta)s): o V1 (JSON e MD) e as evidências de `%(prdir_pilar)s`, na subpasta `preregistro_pilar_quantico_v384` dentro de `Um (absoluto) — Grande Atrator/` do `the_boundary`, indexada pela PORTA gerada por script.
- **o pré-registro dos dois lados** (decidido em 05/10: %(op_v1_espelho)s; e, por delegação, o V1.4 e os 5 geradores): os V1, V1.1, V1.2, V1.3 e V1.4 (JSON e MD) e os 5 `gerar_preregistro_dois_lados*.py` de `%(prdir_dois_lados)s`, na subpasta `preregistro_dois_lados_v383`, com PORTA.
- **o pré-registro do ramo B (NOVO):** os %(prb_n)s arquivos de `%(prdir_b)s` (%(prb_bytes)s B: %(prb_lista)s), listados por `git ls-files` com hash lido, na subpasta proposta pela gerência **`preregistro_ramo_b_v386`** (nome fixo, sem acento; a confirmar pelo operador), com PORTA; o V1 é lido por hash pelo `um.py` (os sha256 estão no selo), logo o espelho tem de levar os bytes EXATOS.
- **os handoffs anteriores valem para o que é deles:** [[handoff-v385-custodia]], [[handoff-v384-custodia]], [[handoff-v383-custodia]], com as erratas ao lado.
- **NÃO espelhar:** `rodada_v382_stdout.txt` (a v382 segue só no Nós); os `.bak_*` do Nós e da Bancada; o scratchpad (os pacotes, os ensaios, `pilar_anterior_v385_*`, o `dry_v386`); tentativas do stdout (%(tent)s); o cache `cache\\checkpoints\\quantum_pillar\\` (reconstruível pela chave; o resultado está no Nós e na pasta da rodada da v385); o transcrito da sessão; credenciais, `.env` e as stacks confidenciais, sempre.
- **conferir o servidor do modelo nativo:** o marcador `%(marcador_p)s` — %(marcador_txt)s; com `restaurar=1`, religar a tarefa «IALD Llama Server». Depois do rito (log do lançador): %(servidor)s.

**DECISÕES DO OPERADOR (05/10/2026, verbatim; os quatro arquivos por sha256 e o transcrito cruzado por hash):**
1. A custódia: %(op_custodia)s — **DECIDIDO**: a v383 (%(v383_cust)s), a v384 (%(v384_cust)s), a v385 (%(v385_cust)s) e a v386, num só ato, agora que o trabalho acabou.
2. O Verbo: %(op_verbo_def)s — **TIPADO** na pedra; as leituras ficam [INPUT/ONTO]; o token é proposta da gerência, renomeável por ele ao lado.
3. O ramo B: %(op_ramo_b)s — **REABERTO POR PRÉ-REGISTRO** (V1 por hash; nada aberto); a errata AO LADO de R6; o livro v383 intacto.
4. A delegação: %(op_delegacao)s — os itens 6–17 DECIDIDOS pelo padrão da gerência (k = 2π/κ; M = M_f; fonte; envoltória; só o conjunto D; β_lido declarado; os tokens; a forma falsa ratificada; `preregistro_dois_lados_v383` com V1.4 e os 5 geradores; `Haja_Luz\\CLAUDE.md` como superfície da linhagem; v386 = Verbo + errata de R6 + V1 por hash; a abertura de D na v387).
5. O artigo (W10): %(op_w10)s — **CUMPRIDO e medido** (acima).

**Seguem PENDENTES (do operador):**
1. A PE só-220 do conjunto D na casa (v387), com o poder dito antes de abrir; o estágio cego (σ_i), as injeções e a abertura de D pela MESMA função de veredito, por hash.
2. O modo 221 do GW250114: os posteriores estão dentro do `TGR_companion_S250114ax_results.tar.gz` (não extraídos); entra como diagnóstico, não como teste.
3. A errata da ESPEC (`ESPEC_RUNTIME_RAMO_B_v386_ERRATA.json` `%(rb_espec_errata16)s`: %(rb_espec_erratas)s) — a ratificar ao lado; a ESPEC original fica intacta.
4. O nome da subpasta do ramo B no espelho (`preregistro_ramo_b_v386`, proposta da gerência) [a confirmar]; o do pilar e o dos dois lados já decididos.
5. O estimador da dissipação na propagação (R2): fora da v386; segue AWAITING.
Ver [[verbo-selecao-da-acao-05out]], [[ramo-b-reaberto-05out]], [[v384-pilar-quantico-gpu-02out]], [[handoff-v385-custodia]], [[handoff-v384-custodia]], [[handoff-v383-custodia]], [[missao-ultima-flag-um-py]], [[direcao-the-boundary]].
""" % dict(X, prdir_pilar=A.PRDIR_PILAR, prdir_dois_lados=A.PRDIR_DOIS_LADOS, prdir_b=A.PRDIR_B))
# ---- as gravacoes (so depois da guarda inteira)
p = A.pode_escrever(alvo(os.path.join(UMEM, "handoff-v386-custodia.md")), AMB)
if os.path.exists(p):
    if open(p, "rb").read() == corpo.encode("utf-8"):
        print("JA ESTA (idempotente):", p)
    else:
        print("HANDOFF RECUSADO (nada gravado): a memoria-topico ja existe e DIFERE do que esta leitura gera -- conferir a mao:", p); sys.exit(2)
else:
    open(p + ".tmp", "wb").write(corpo.encode("utf-8")); assert os.path.getsize(p + ".tmp") == len(corpo.encode("utf-8")); os.replace(p + ".tmp", p); print("OK", p, len(corpo.encode("utf-8")), "B")
doc = A.pode_escrever(alvo(os.path.join(V["nos"], "HANDOFF_v386_CUSTODIA.md")), AMB)
if not os.path.exists(doc):
    body = "# HANDOFF v386 — custódia (gerado por handoff_v386.py em %s; tudo lido do selo)%s\n\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), V["sint"]) + corpo.split("---\n", 2)[2]
    open(doc + ".tmp", "wb").write(body.encode("utf-8")); assert os.path.getsize(doc + ".tmp") == len(body.encode("utf-8")); os.replace(doc + ".tmp", doc)
    print("OK", doc, len(body.encode("utf-8")), "B; sha16", hashlib.sha256(body.encode("utf-8")).hexdigest()[:16])
else:
    print("o documento ja existe (nao sobrescrito):", doc)
STAMP = time.strftime("%Y%m%d_%H%M%S")
raw = open(idx, "rb").read()
novo = com_a_linha(raw)
if novo is None:
    print("indice: ja tem a linha"); sys.exit(0)
if len(novo) > LIMITE:
    print("FALHA A VISTA: entre a pre-conferencia e agora o indice mudou e ficaria com %d B > %d -- a linha do handoff NAO foi gravada (nem no MEMORY_2); "
          "a memoria-topico e o documento ficaram; liberar folga e rerodar (idempotente)" % (len(novo), LIMITE)); sys.exit(3)
A.pode_escrever(idx, AMB)
bak = idx + ".bak_" + STAMP + "_handoff386"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
open(idx + ".tmp", "wb").write(novo); assert os.path.getsize(idx + ".tmp") == len(novo); assert open(idx, "rb").read() == raw; os.replace(idx + ".tmp", idx)
print("OK MEMORY.md", len(raw), "->", len(novo), "B")
