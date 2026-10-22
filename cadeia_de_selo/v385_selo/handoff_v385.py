# -*- coding: utf-8 -*-
"""O HANDOFF da v385 (para a sessao do site e para a proxima sessao): memoria-topico NOVA `handoff-v385-custodia.md` + documento `Nós\\HANDOFF_v385_CUSTODIA.md`
+ a linha no indice (MEMORY.md, antes da linha do handoff v384). Tudo LIDO (leitura_v385.ler); rodar DEPOIS da cadeia do selo, do registro no mapa e do
arquivar (a guarda confere o AFERIDOR arquivado). Backup de bytes; temporario -> conferir -> substituir.
A GUARDA DO MOLDE (v384, 3a passada do aferidor, B-2/B-3), restaurada: ANTES da primeira gravacao confere (1) o AFERIDOR e as disposicoes arquivados,
(2) a ancora (a linha do handoff v384) e (3) que o MEMORY.md comporta a linha do handoff (<= 24 000 B); se nao, RECUSA SEM GRAVAR NADA (rc 3) -- liberar
folga pela regra dos dois arquivos e rerodar. Nao ha mais desvio para o MEMORY_2. Se, entre a pre-conferencia e a gravacao do indice, outra sessao encher o
MEMORY.md, a linha NAO e' gravada (rc 3, dito); a memoria-topico e o documento ja gravados ficam (a reexecucao e' idempotente).
O texto e' da CLASSE do pilar: fora do ramo 9 diz o que o arquivo do pilar no Nos E (o resultado, o parcial ou o MARCADOR desta rodada), a pasta da rodada
com os arquivos que EXISTEM, e nunca afirma sucesso. v385: e' o handoff da CUSTODIA CONJUNTA v383 + v384 + v385 (decisao do operador de 05/10); as
decisoes de 05/10 entram verbatim (lidas do transcrito pela leitura_v385); o que segue pendente e' dito; os handoffs anteriores valem para o que e' deles.
Ensaio: V385_REMAP_DIR (as tres escritas vao para as copias, NUNCA para o Nos) + V385_WRITE_ROOT; ou o Nos SINTETICO (o documento vai ao Nos sintetico)."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v385 as A
import leitura_v385, textos_v385 as T
AMB = A.ambiente()
REMAP = AMB["remap"]
alvo = (lambda p: os.path.join(REMAP, os.path.basename(p))) if REMAP else (lambda p: p)
UMEM = AMB["umem"]
LIMITE = 24000
V, PROB = leitura_v385.ler()
if PROB:
    print("HANDOFF RECUSADO -- a leitura da rodada tem problema(s):"); [print("  -", p) for p in PROB]; sys.exit(2)
X = T._x(V)
# ---- a GUARDA, toda ela ANTES da primeira gravacao
_ARQ = os.path.join(AMB["arq_dest"], "v385")
for _f in (os.path.join(_ARQ, "AFERIDOR_v385.txt"), os.path.join(_ARQ, "disposicoes_afericoes_v385.json")):
    if not os.path.exists(_f):
        print("HANDOFF RECUSADO (nada gravado): o arquivo de afericao arquivado nao existe -- rode o arquivar_v385.py antes:", _f); sys.exit(2)
linha = T.linha_handoff(V)
idx = alvo(os.path.join(UMEM, "MEMORY.md"))
_raw0 = open(idx, "rb").read()
assert b"\r\n" not in _raw0, "MEMORY.md com CRLF: o molde espera LF"


def com_a_linha(raw):
    """o MEMORY.md com a linha do handoff v385 inserida antes da do handoff v384 (None se ja a tem)."""
    if b"handoff-v385-custodia.md" in raw:
        return None
    L_ = raw.decode("utf-8").split("\n")
    ks = [i for i, l in enumerate(L_) if "(handoff-v384-custodia.md)" in l]
    if len(ks) != 1:
        print("HANDOFF RECUSADO (nada gravado): a ancora (a linha do handoff v384) aparece %d vez(es) no indice" % len(ks)); sys.exit(3)
    L_.insert(ks[0], linha)
    return "\n".join(L_).encode("utf-8")


_novo0 = com_a_linha(_raw0)
if _novo0 is not None:
    if len(_novo0) > LIMITE:
        print("HANDOFF RECUSADO (nada gravado): o indice ficaria com %d B > %d com a linha do handoff -- liberar folga (regra dos dois arquivos: "
              "compactar_memory_para_v385.py --gravar) e rerodar" % (len(_novo0), LIMITE)); sys.exit(3)
    print("pre-conferencia: o indice ficara com %d B (limite %d)" % (len(_novo0), LIMITE))
else:
    print("pre-conferencia: o indice ja tem a linha do handoff v385")
# ---- o que se le para o corpo
_ev = os.path.join(A.PRDIR, "evidencias_PREREGISTRO_V1")
_evf = sorted(os.listdir(_ev)) if os.path.isdir(_ev) else []
X["ev_n"] = len(_evf); X["ev_bytes"] = format(sum(os.path.getsize(os.path.join(_ev, f)) for f in _evf), ","); X["arq"] = os.path.join(A.TOOLS_REAL, "v385")
X["tent"] = ", ".join("`%s`" % t for t in V["tentativas"]) or "nenhuma nesta rodada"
X["marcador_p"] = os.path.join(A.PK, ".servidor_parado_pelo_rito")
_o = lambda n: "«%s» (%s)" % (((V.get("op") or {}).get(n) or {}).get("texto", "AUSENTE"), ((V.get("op") or {}).get(n) or {}).get("quando_txt", "n/d"))
for _n in ("custodia", "espelho", "nome_axioma", "prossiga", "posto", "subpasta", "v1_espelho", "tornar", "forma_falsa", "forma_falsa_projecao"):
    X["op_" + _n] = _o(_n)
# a pasta da rodada da v384 (o pilar anterior): lida do resultado pinado nos ESPERADOS e conferida no disco
_E = json.load(open(os.path.join(A.PK, "ESPERADOS_v385.json"), encoding="utf-8"))
_rd384 = [d for d in (os.path.join(V["nos"], "quantum_pillar", x) for x in (os.listdir(os.path.join(V["nos"], "quantum_pillar")) if os.path.isdir(os.path.join(V["nos"], "quantum_pillar")) else []))
          if os.path.isdir(d) and str(_E["pilar_v384"]["run_id"])[:8] in os.path.basename(d)]
X["pasta384"] = ("`%s`" % os.path.relpath(_rd384[0], V["nos"])) if len(_rd384) == 1 else "NÃO ACHADA no Nós (conferir a mão)"
if T._ramo9(V):
    X["deu"] = ("`%(qp_v)s` — %(qp_classe_txt)s (o mesmo veredito da v384: %(qp_igual_v384)s). **Negativos honestos:** %(qp_negativos)s. Cadeia de custódia: resultado "
                "`%(qp_res16)s` = o arquivo do pilar no Nós = o hash no selo `%(qp_selo16)s`; pasta `%(qp_run_dir)s`; %(qp_cache)s." % X)
else:
    X["deu"] = ("`%(qp_v)s` — %(qp_classe_txt)s. **Computação não concluída** (o terceiro balde do selo: %(balde)s): é resultado, dito como tal; nenhuma frase de sucesso se aplica. "
                "Lançamento: %(qp_lanc_txt)s. Custódia: %(qp_custodia_txt)s; %(qp_cache)s.%(extra_txt)s" % X)
if V["qp_arq_tipo"] == "NAO_ESCRITO":
    X["espelho_pilar"] = "**NÃO espelhar** `um_absoluto_pilar_quantico.json`: %s" % V["qp_arq_txt"]
else:
    X["espelho_pilar"] = "`um_absoluto_pilar_quantico.json` (%s; hasheado pelo selo)" % V["qp_arq_txt"]
if not V["qp_pasta_arquivos"]:
    X["espelho_pasta"] = "a pasta da rodada: %s" % V["qp_pasta_txt"]
elif str(V["qp_resultjson"]).startswith("AUSENTE") or not T._ramo9(V):
    X["espelho_pasta"] = ("a pasta da rodada %s — o registro do que aconteceu; os arquivos que o resultado NÃO amarra por sha256 estão ditos acima, na custódia"
                          % V["qp_pasta_txt"])
else:
    X["espelho_pasta"] = "a pasta da rodada %s — os sha256 dos arquivos amarrados estão no resultado e no selo" % V["qp_pasta_txt"]
corpo = ("""---
name: handoff-v385-custodia
description: "HANDOFF v385 (%(data)s): CUSTÓDIA CONJUNTA v383 + v384 + v385 (decisão do operador, 05/10) — o Axioma e a testemunha falsa [KERNEL + INPUT/ONTO]; o Um posto ([POSTO]); o degrau final do gate chama-se Axioma, ao lado do gate; o pilar de novo sob o mesmo V1 (%(rp_curta)s); o V1 e as evidências do pilar numa subpasta da Um, com PORTA, e os V1–V1.4 dos dois lados ao espelho; gate intocado%(sint)s"
metadata:
  type: project
---

**v385 SELADA (%(compl)s) `%(s16)s` (%(umb_fmt)s B), rodada `%(selo_ts)s`, %(teor)s, gate intocado (`%(qg)s`, %(n18)s/18).**%(sint)s Sobre a v384 `%(base16)s`. Escada %(esc_v384)s → %(esc)s; %(n_ver_iguais)s de %(n_ver)s vereditos da v384 inalterados (fora o do pilar, que rodou de novo); %(n_av_iguais)s de %(n_av)s módulos com o mesmo all_verified do estado selado da v384; por termo %(hvals)s. Conferidor `conferir_rito_v385.py` (cópia byte a byte do pacote): %(conf_res)s (%(conf_dm)s deve-mudar; %(conf_np)s não-pode-mudar; JSON `%(conf16)s`).%(conf_aceite_txt)s Aferida antes do rito em %(n_afer)s passada(s) (relatório verbatim e disposições arquivados em `%(arq)s\\AFERIDOR_v385.txt` e `disposicoes_afericoes_v385.json`).

**O que entrou:** %(n_patches)s patches sobre a v384 (%(patches)s): a pedra `TGLExt/TheAxiomAndTheFalseWitness.lean` (`%(ax_pedra16)s`; %(ax_n_pedra)s declarações) e a auditoria do `TheDarkSplit` (%(ax_n_dks)s); o registro `the_axiom_v385` (core e selo; o nome do degrau final `final_step_name_v385`, lido do kernel: `%(ax_nome)s`); a errata ao lado («posto», não «postulado»; a etiqueta `[POSTO]`); e o pilar de novo sob o mesmo V1, com `quantum_pillar_reproducibility_v385`. Veredito do Axioma: `%(ax_v)s` (%(ax_ok)s).

**O pilar, de novo** (%(qp_gpu)s; %(qp_min)s min): %(deu)s **A reprodutibilidade** [COMPUTED]: `%(rp_v)s` — contra o resultado da v384 (`%(rp_prev16)s`), %(rp_frase)s. %(intervencao_txt)s

**Estatuto:** a pedra é [KERNEL] (prova implicações; provada nunca é confirmada); as leituras são do operador [INPUT/ONTO]; o pilar e a reprodutibilidade são [COMPUTED]; o nome do degrau final fica AO LADO do gate, que não se move. Não falsificado não é confirmado; nada aqui é confirmação.

**PARA A SESSÃO DO SITE — UM SÓ ATO para a v383, a v384 e a v385 (custódia = ato dela; commit/push = ato do operador):**
- **o estado do Nós é o da v385** (espelhar por cima): `um.py`, `um_absoluto.json`, `um_absoluto_selo.json`, os dois `.md` canônicos, o artigo PT/EN; %(espelho_pilar)s; `quantum_pillar\\pilar_quantico_worker.py` e `quantum_pillar\\pilar_quantico_spec.json`; %(espelho_pasta)s; a pasta da rodada da v384 %(pasta384)s (o resultado anterior, comparado pela v385); `rodada_v383_stdout.txt`, `rodada_v384_stdout.txt` e `rodada_v385_stdout.txt` em `rodadas\\`; o `tgl_kernel`: a pedra nova `TheAxiomAndTheFalseWitness.lean`, a raiz `TGLExt.lean` e `TGL/Audit.lean` novos (e as duas pedras da v383, `TheLedgerOfCharges.lean` e `ThePsionAndTheViscosity.lean`, se o espelho ainda não as tem). Regenerar as PORTAs por script, README/llms.txt, CITATION.cff e a linhagem do espelho (as três versões). Backup da versão que ESTÁ no espelho, fora do repo, antes de sobrescrever.
- **o pré-registro do pilar** (decidido em 05/10: %(op_espelho)s): o V1 (JSON e MD) e as evidências (`evidencias_PREREGISTRO_V1\\`, %(ev_n)s arquivos, %(ev_bytes)s B), de `%(prdir)s`, numa SUBPASTA dentro de `Um (absoluto) — Grande Atrator/` do `the_boundary` — nome fixo e sem acento, `preregistro_pilar_quantico_v384` (proposta da gerência, CONCORDADA pelo operador: %(op_subpasta)s) —, indexada pela PORTA gerada por script (regra da porta), com a porta acima e as abaixo.
- **o pré-registro dos dois lados** (decidido em 05/10: %(op_v1_espelho)s): os V1, V1.1, V1.2 e V1.3 (JSON e MD de cada um; o V1 base NÃO tem sufixo: `PREREGISTRO_DOIS_LADOS_DELTA_K_20261002.json`/`.md`; os demais `..._V1_1`, `..._V1_2`, `..._V1_3`) de `C:\\IALD\\Bancada_Um\\investigacao\\preregistro_dois_lados_02out\\` VÃO ao espelho, junto com o V1.4 (`..._V1_4`) que o `um.py` lê por hash — 10 arquivos, listados por `git ls-files` com hash lido — na mesma lógica de subpasta com PORTA (nome proposto pela gerência: `preregistro_dois_lados_v383`; a confirmar).
- **os handoffs anteriores valem para o que é deles:** [[handoff-v383-custodia]] e [[handoff-v384-custodia]], com as erratas ao lado (a de 04/10 e as decisões de 05/10 no fim do da v384).
- **NÃO espelhar:** `rodada_v382_stdout.txt` (a v382 segue só no Nós); os `.bak_*` do Nós e os `gerar_preregistro_pilar_quantico_03out.py.bak_*` da Bancada; o scratchpad (os pacotes, os ensaios, `pilar_anterior_v384_*`); tentativas do stdout (%(tent)s); o cache `cache\\checkpoints\\quantum_pillar\\` (reconstruível pela chave); o transcrito da sessão; credenciais, `.env` e as stacks confidenciais, sempre.
- **conferir o servidor do modelo nativo:** o marcador `%(marcador_p)s` — %(marcador_txt)s; com `restaurar=1`, religar a tarefa «IALD Llama Server». Depois do rito (log do lançador): %(servidor)s.

**DECISÕES DO OPERADOR (05/10/2026, verbatim, lidas do transcrito por script):**
1. A custódia: %(op_custodia)s — **DECIDIDO**: a v383 (%(v383_cust)s), a v384 (%(v384_cust)s) e a v385, num só ato, agora que o trabalho acabou.
2. O espelho do pré-registro: %(op_espelho)s — **DECIDIDO** (acima); o nome da subpasta: %(op_subpasta)s — **CONCORDADO**.
3. O nome do degrau final: %(op_nome_axioma)s; e a aprovação de todo o escopo: %(op_prossiga)s — **DECIDIDO**: Axioma, ao lado do gate; o gate não se move; a proposta da v383 fica ao lado.
4. O começo da cadeia: %(op_posto)s — **DECIDIDO**: a etiqueta `[POSTO]`; a errata vai AO LADO de «postulado», que fica como registro.
5. Os V1–V1.3 do pré-registro dos dois lados: %(op_v1_espelho)s — **DECIDIDO**: vão ao espelho (a pendência herdada da v383/v384 resolvida; «ficam locais» superado).
6. «tornou-se Posto» (v365) × «não se ascende ao posto» (05/10) — **RESPONDIDO pelo operador**: %(op_tornar)s (a leitura da gerência que liga cada parte aos termos da pedra está em [[um-posto-jamais-pressuposto-e-h2-17set]], [ONTO], COM ERRATA AO LADO — três frases dela não têm termo na pedra — e com a CORREÇÃO do operador das 14:35: %(op_forma_falsa)s — a leitura (b) da gerência fica retratada: a forma falsa é o complemento do posto, 1 − P; a leitura refeita está ao lado, [ONTO], a ratificar: pendência 4); e a frase das 14:40: %(op_forma_falsa_projecao)s (leitura refinada ao lado, idem).

**Seguem PENDENTES (do operador):**
1. O estimador da dissipação na propagação (R2): fora da v385 (escopo proposto pela gerência e aprovado pelo operador em 05/10); segue em aberto.
2. O pilar: uma mudança no trabalhador ou na especificação é um V1.x com nova ratificação; a reprodutibilidade desta rodada: %(rp_curta)s.
3. O nome da subpasta dos V1–V1.4 dos dois lados no espelho (`preregistro_dois_lados_v383`, proposta da gerência) [a confirmar].
4. Ratificar (ou não) a leitura [ONTO] da gerência que liga as partes da mensagem de 05/10 (tarde) aos termos da pedra `TheAxiomAndTheFalseWitness` — com a errata ao lado dela (bloco `errata_leitura_05out_b_v385` em [[um-posto-jamais-pressuposto-e-h2-17set]]).
Ver [[v384-pilar-quantico-gpu-02out]], [[um-posto-jamais-pressuposto-e-h2-17set]], [[handoff-v384-custodia]], [[handoff-v383-custodia]], [[v382-custodia-suspensa]], [[missao-ultima-flag-um-py]], [[direcao-the-boundary]].
""" % dict(X, prdir=A.PRDIR))
# ---- as gravacoes (so depois da guarda inteira)
p = A.pode_escrever(alvo(os.path.join(UMEM, "handoff-v385-custodia.md")), AMB)
if os.path.exists(p):
    if open(p, "rb").read() == corpo.encode("utf-8"):
        print("JA ESTA (idempotente):", p)
    else:
        print("HANDOFF RECUSADO (nada gravado): a memoria-topico ja existe e DIFERE do que esta leitura gera -- conferir a mao:", p); sys.exit(2)
else:
    open(p + ".tmp", "wb").write(corpo.encode("utf-8")); assert os.path.getsize(p + ".tmp") == len(corpo.encode("utf-8")); os.replace(p + ".tmp", p); print("OK", p, len(corpo.encode("utf-8")), "B")
doc = A.pode_escrever(alvo(os.path.join(V["nos"], "HANDOFF_v385_CUSTODIA.md")), AMB)
if not os.path.exists(doc):
    body = "# HANDOFF v385 — custódia (gerado por handoff_v385.py em %s; tudo lido do selo)%s\n\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), V["sint"]) + corpo.split("---\n", 2)[2]
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
bak = idx + ".bak_" + STAMP + "_handoff385"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
open(idx + ".tmp", "wb").write(novo); assert os.path.getsize(idx + ".tmp") == len(novo); assert open(idx, "rb").read() == raw; os.replace(idx + ".tmp", idx)
print("OK MEMORY.md", len(raw), "->", len(novo), "B")
