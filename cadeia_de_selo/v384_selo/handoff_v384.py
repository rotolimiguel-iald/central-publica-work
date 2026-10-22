# -*- coding: utf-8 -*-
"""O HANDOFF da v384 (para a sessao do site e para a proxima sessao): memoria-topico NOVA `handoff-v384-custodia.md` + documento `Nós\\HANDOFF_v384_CUSTODIA.md`
+ a linha no indice (MEMORY.md, antes da linha do handoff v383). Tudo LIDO (leitura_v384.ler); rodar DEPOIS da cadeia do selo, do registro no mapa e do
arquivar (a guarda confere o AFERIDOR arquivado). Backup de bytes; temporario -> conferir -> substituir.
A GUARDA DO MOLDE (v383, 3a passada do aferidor, B-2/B-3), restaurada: ANTES da primeira gravacao confere (1) o AFERIDOR e as disposicoes arquivados,
(2) a ancora (a linha do handoff v383) e (3) que o MEMORY.md comporta a linha do handoff (<= 24 000 B); se nao, RECUSA SEM GRAVAR NADA (rc 3) -- liberar
folga pela regra dos dois arquivos e rerodar. Nao ha mais desvio para o MEMORY_2. Se, entre a pre-conferencia e a gravacao do indice, outra sessao encher o
MEMORY.md, a linha NAO e' gravada (rc 3, dito); a memoria-topico e o documento ja gravados ficam (a reexecucao e' idempotente).
O texto e' da CLASSE do pilar: fora do ramo 9 diz o que o arquivo do pilar no Nos E (o resultado, o parcial ou o MARCADOR desta rodada), a pasta da rodada
com os arquivos que EXISTEM, e nunca afirma sucesso. As pendencias da v383 sao HERDADAS, lidas da memoria-topico handoff-v383-custodia.md.
Ensaio: V384_REMAP_DIR (as tres escritas vao para as copias, NUNCA para o Nos) + V384_WRITE_ROOT; ou o Nos SINTETICO (o documento vai ao Nos sintetico)."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v384 as A
import leitura_v384, textos_v384 as T
AMB = A.ambiente()
REMAP = AMB["remap"]
alvo = (lambda p: os.path.join(REMAP, os.path.basename(p))) if REMAP else (lambda p: p)
UMEM = AMB["umem"]
LIMITE = 24000
V, PROB = leitura_v384.ler()
if PROB:
    print("HANDOFF RECUSADO -- a leitura da rodada tem problema(s):"); [print("  -", p) for p in PROB]; sys.exit(2)
X = T._x(V)
# ---- a GUARDA, toda ela ANTES da primeira gravacao
_ARQ = os.path.join(AMB["arq_dest"], "v384")
for _f in (os.path.join(_ARQ, "AFERIDOR_v384.txt"), os.path.join(_ARQ, "disposicoes_afericoes_v384.json")):
    if not os.path.exists(_f):
        print("HANDOFF RECUSADO (nada gravado): o arquivo de afericao arquivado nao existe -- rode o arquivar_v384.py antes:", _f); sys.exit(2)
linha = T.linha_handoff(V)
idx = alvo(os.path.join(UMEM, "MEMORY.md"))
_raw0 = open(idx, "rb").read()
assert b"\r\n" not in _raw0, "MEMORY.md com CRLF: o molde espera LF"


def com_a_linha(raw):
    """o MEMORY.md com a linha do handoff v384 inserida antes da do handoff v383 (None se ja a tem)."""
    if b"handoff-v384-custodia.md" in raw:
        return None
    L_ = raw.decode("utf-8").split("\n")
    ks = [i for i, l in enumerate(L_) if "(handoff-v383-custodia.md)" in l]
    if len(ks) != 1:
        print("HANDOFF RECUSADO (nada gravado): a ancora (a linha do handoff v383) aparece %d vez(es) no indice" % len(ks)); sys.exit(3)
    L_.insert(ks[0], linha)
    return "\n".join(L_).encode("utf-8")


_novo0 = com_a_linha(_raw0)
if _novo0 is not None:
    if len(_novo0) > LIMITE:
        print("HANDOFF RECUSADO (nada gravado): o indice ficaria com %d B > %d com a linha do handoff -- liberar folga (regra dos dois arquivos: "
              "compactar_memory_para_v384.py --gravar) e rerodar" % (len(_novo0), LIMITE)); sys.exit(3)
    print("pre-conferencia: o indice ficara com %d B (limite %d)" % (len(_novo0), LIMITE))
else:
    print("pre-conferencia: o indice ja tem a linha do handoff v384")
# ---- o que se le para o corpo
_ev = os.path.join(A.PRDIR, "evidencias_PREREGISTRO_V1")
_evb = sum(os.path.getsize(os.path.join(_ev, f)) for f in os.listdir(_ev)) if os.path.isdir(_ev) else 0
X["ev_bytes"] = format(_evb, ","); X["arq"] = os.path.join(A.TOOLS_REAL, "v384")
X["tent"] = ", ".join("`%s`" % t for t in V["tentativas"]) or "nenhuma nesta rodada"
X["marcador_p"] = os.path.join(A.PK, ".servidor_parado_pelo_rito")
# as pendencias da v383, HERDADAS: lidas da memoria-topico handoff-v383-custodia.md (a copia de ensaio, se houver; senao a real -- so leitura)
_h383 = [p for p in (alvo(os.path.join(UMEM, "handoff-v383-custodia.md")), os.path.join(UMEM, "handoff-v383-custodia.md"), os.path.join(A.UMEM_REAL, "handoff-v383-custodia.md")) if os.path.exists(p)]
_pend = ""
if _h383:
    for _l in open(_h383[0], encoding="utf-8").read().split("\n"):
        if _l.startswith("**Pendências ditas (decisões do operador):**"):
            _pend = _l[len("**Pendências ditas (decisões do operador):**"):].strip(); break
X["pend383"] = ("ainda abertas, herdadas da v383 (verbatim de [[handoff-v383-custodia]]): " + _pend) if _pend else "a lista da v383 NÃO foi lida — conferir em [[handoff-v383-custodia]]"
if T._ramo9(V):
    X["deu"] = ("`%(qp_v)s` — %(qp_classe_txt)s. (T2) atrator único em %(t2_unique)s de %(t2_points)s pontos; NAME_IN_CORE %(t2_name)s/%(t2_configs)s; FOLDS_WINDOW %(t2_folds)s/%(t2_configs)s. "
                "(T1) %(t1_inj)s injeções; %(t1_frase)s. (T3) %(t3_ctl)s controles falharam como exigido. (T4) %(t4_n)s instâncias; %(t4_viol)s violações de identidade. (D128) %(d128_txt)s. "
                "(CPU) %(cpu_cmp)s comparados, %(cpu_dis)s discordâncias. **Negativos honestos:** %(qp_negativos)s. Cadeia de custódia: resultado `%(qp_res16)s` = o arquivo do pilar no Nós "
                "= o hash no selo `%(qp_selo16)s`; pasta `%(qp_run_dir)s`; %(qp_cache)s." % X)
else:
    X["deu"] = ("`%(qp_v)s` — %(qp_classe_txt)s. **Computação não concluída** (o terceiro balde do selo: %(balde)s): é resultado, dito como tal; nenhuma frase de sucesso se aplica. "
                "Lançamento: %(qp_lanc_txt)s. Custódia: %(qp_custodia_txt)s; %(qp_cache)s.%(extra_txt)s" % X)
if V["qp_arq_tipo"] == "NAO_ESCRITO":
    X["espelho_pilar"] = "**NÃO espelhar** `um_absoluto_pilar_quantico.json`: %s" % V["qp_arq_txt"]
else:
    X["espelho_pilar"] = "`um_absoluto_pilar_quantico.json` (%s; hasheado pelo selo)" % V["qp_arq_txt"]
if not V["qp_pasta_arquivos"]:
    X["espelho_pasta"] = "a pasta da rodada: %s" % V["qp_pasta_txt"]
elif str(V["qp_resultjson"]).startswith("AUSENTE"):
    X["espelho_pasta"] = ("a pasta da rodada %s — nenhum arquivo dela é amarrado por sha256 (não há resultado registrado nesta rodada); o que houver nela é o registro do "
                          "que aconteceu" % V["qp_pasta_txt"])
else:
    X["espelho_pasta"] = "a pasta da rodada %s — os sha256 dos arquivos amarrados estão no resultado e no selo" % V["qp_pasta_txt"]
corpo = ("""---
name: handoff-v384-custodia
description: "HANDOFF v384 (%(data)s): O PILAR QUÂNTICO NA GPU [COMPUTED] — o sistema aberto H_LD + cinco saltos de Lindblad calculado em paralelo com o kernel e os ritos, sob o pré-registro V1 ratificado pelo operador (%(pr_escolha)s) por hash; registro próprio ao lado do gate; kernel = o da v383; gate intocado; o pilar: %(qp_classe_curta)s; para a sessão do site custodiar; decisões pendentes do operador%(sint)s"
metadata:
  type: project
---

**v384 SELADA (%(compl)s) `%(s16)s` (%(umb_fmt)s B), rodada `%(selo_ts)s`, %(teor)s, gate intocado (`%(qg)s`, %(n18)s/18).**%(sint)s Sobre a v383 `%(base16)s`. Kernel: %(kernel_decl)s; escada %(esc)s; %(n_ver_iguais)s de %(n_ver)s vereditos da v383 inalterados; %(n_av_iguais)s de %(n_av)s módulos com o mesmo all_verified do estado selado da v383; por termo %(hvals)s. Conferidor `conferir_rito_v384.py` (cópia byte a byte do pacote): %(conf_res)s (%(conf_dm)s deve-mudar; %(conf_np)s não-pode-mudar; JSON `%(conf16)s`).%(conf_aceite_txt)s A v384 foi aferida antes do rito em %(n_afer)s passadas (relatório verbatim e disposições arquivados em `%(arq)s\\AFERIDOR_v384.txt` e `disposicoes_afericoes_v384.json`).

**O que entrou:** %(n_patches)s patches sobre a v383 (%(patches)s): o trabalhador da GPU embutido no `um.py` (`pilar_quantico_worker.py`, `%(pr_worker16)s`), lançado logo depois da inscrição do Um, em paralelo com o kernel e os ritos; a espera, a conferência do sha256 e a REDERIVAÇÃO do veredito pela mesma árvore; o registro no core (`quantum_pillar_v384`), no selo (ao lado do gate; leitura `the_quantum_pillar_reading_v384`; o arquivo do pilar no hash do selo; o terceiro balde `computacao_nao_concluida`, se o pilar não concluir) e no artigo (a introdução e a nota da GPU). **O pré-registro** `%(pr_id)s` (JSON `%(pr_json16)s`, MD `%(pr_md16)s`, especificação `%(pr_spec16)s`; %(pr_ev)s evidências por sha256; conferência do congelamento: %(pr_conf)s), ratificado pelo operador (%(pr_quando_txt)s), verbatim: «%(pr_verbatim)s» — escolha `%(pr_escolha)s`.

**O que a GPU deu** (%(qp_gpu)s; %(qp_min)s min; orçamento pré-registrado %(pr_orc_min)s min, %(pr_orc_margem)s com a margem): %(deu)s

**Estatuto dito na v384:** o pilar é [COMPUTED] — cálculo do sistema da teoria, não medição; registro próprio AO LADO do gate, que não se move; as identidades só falham se o motor errar; a hierarquia das dobras é matemática; o T1 testa o instrumento; «o Nome como matriz» é [ONTO]; a ordem e a ratificação são do operador [INPUT]. Não falsificado não é confirmado; nada aqui é confirmação.

**PARA A SESSÃO DO SITE (custódia = ato dela; commit/push = ato do operador):**
- **espelhar do Nós:** `um.py`, `um_absoluto.json`, `um_absoluto_selo.json`, os dois `.md` canônicos, o artigo PT/EN; %(espelho_pilar)s; `quantum_pillar\\pilar_quantico_worker.py` e `quantum_pillar\\pilar_quantico_spec.json` (materializados pelo `um.py` a partir do texto embutido); %(espelho_pasta)s; `rodada_v384_stdout.txt` em `rodadas\\`; o `tgl_kernel` não muda (o mesmo da v383). Regenerar as PORTAs por script, README/llms.txt, CITATION.cff e a linhagem do espelho. Backup da versão anterior fora do repo antes de sobrescrever.
- **do pré-registro do pilar** (`%(prdir)s`): o V1 (JSON e MD) e a pasta `evidencias_PREREGISTRO_V1\\` (%(pr_ev)s; %(ev_bytes)s B) — o `um.py` confere o V1 por hash (informativo; a especificação embutida, conferida pelo hash, é a congelada).
- **NÃO espelhar:** `rodada_v382_stdout.txt` (a v382 segue só no Nós); os `.bak_*` do Nós e os `gerar_preregistro_pilar_quantico_03out.py.bak_*` da Bancada; os rascunhos não escolhidos e o scratchpad; tentativas do stdout (%(tent)s); o cache `cache\\checkpoints\\quantum_pillar\\` (reconstruível pela chave); o transcrito da sessão (o V1 guarda só o sha256 das linhas da mensagem do operador); credenciais, `.env` e as stacks confidenciais, sempre.
- **conferir o servidor do modelo nativo:** o marcador `%(marcador_p)s` — %(marcador_txt)s; com `restaurar=1`, religar a tarefa «IALD Llama Server» (a regra da memória [[v384-pilar-quantico-gpu-02out]]). Depois do rito (log do lançador): %(servidor)s.

**Decisões PENDENTES do operador:**
1. A custódia da v383 (`%(base16)s`; %(v383_cust)s): agora, num ato separado, ou junto com a v384 num só ato.
2. Os V1–V1.3 do pré-registro dos dois lados (02/10): a gerência propôs, na v383, que fiquem locais [a confirmar pelo operador].
3. O que do pré-registro do pilar vai ao espelho: o V1 e as evidências inteiras, ou só o V1 com os sha256 das evidências.
4. O pilar (%(qp_classe_curta)s; %(qp_negativos)s): uma mudança no trabalhador ou na especificação é um V1.x com nova ratificação; repetir a rodada sob o MESMO V1 congelado é decisão do operador.
5. As pendências %(pend383)s
Ver [[v384-pilar-quantico-gpu-02out]], [[handoff-v383-custodia]], [[v382-custodia-suspensa]], [[missao-ultima-flag-um-py]], [[direcao-the-boundary]].
""" % dict(X, prdir=A.PRDIR))
# ---- as gravacoes (so depois da guarda inteira)
p = A.pode_escrever(alvo(os.path.join(UMEM, "handoff-v384-custodia.md")), AMB)
if os.path.exists(p):
    if open(p, "rb").read() == corpo.encode("utf-8"):
        print("JA ESTA (idempotente):", p)
    else:
        print("HANDOFF RECUSADO (nada gravado): a memoria-topico ja existe e DIFERE do que esta leitura gera -- conferir a mao:", p); sys.exit(2)
else:
    open(p + ".tmp", "wb").write(corpo.encode("utf-8")); assert os.path.getsize(p + ".tmp") == len(corpo.encode("utf-8")); os.replace(p + ".tmp", p); print("OK", p, len(corpo.encode("utf-8")), "B")
doc = A.pode_escrever(alvo(os.path.join(V["nos"], "HANDOFF_v384_CUSTODIA.md")), AMB)
if not os.path.exists(doc):
    body = "# HANDOFF v384 — custódia (gerado por handoff_v384.py em %s; tudo lido do selo)%s\n\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), V["sint"]) + corpo.split("---\n", 2)[2]
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
bak = idx + ".bak_" + STAMP + "_handoff384"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
open(idx + ".tmp", "wb").write(novo); assert os.path.getsize(idx + ".tmp") == len(novo); assert open(idx, "rb").read() == raw; os.replace(idx + ".tmp", idx)
print("OK MEMORY.md", len(raw), "->", len(novo), "B")
