# -*- coding: utf-8 -*-
"""Reescreve o CORPO do handoff_v385.py (gerado pelo conversor): o handoff da CUSTODIA CONJUNTA v383 + v384 + v385 (decisao do operador de 05/10), com as
decisoes de 05/10 citadas verbatim (lidas do transcrito pela leitura) e o que segue pendente. A guarda e as gravacoes do molde ficam. Backup de bytes; ast."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "handoff_v385.py")
s0 = open(P, encoding="utf-8", newline="").read()
i = s0.index("# ---- o que se le para o corpo")
j = s0.index("# ---- as gravacoes (so depois da guarda inteira)")
NOVO = r'''# ---- o que se le para o corpo
_ev = os.path.join(A.PRDIR, "evidencias_PREREGISTRO_V1")
_evf = sorted(os.listdir(_ev)) if os.path.isdir(_ev) else []
X["ev_n"] = len(_evf); X["ev_bytes"] = format(sum(os.path.getsize(os.path.join(_ev, f)) for f in _evf), ","); X["arq"] = os.path.join(A.TOOLS_REAL, "v385")
X["tent"] = ", ".join("`%s`" % t for t in V["tentativas"]) or "nenhuma nesta rodada"
X["marcador_p"] = os.path.join(A.PK, ".servidor_parado_pelo_rito")
_o = lambda n: "«%s» (%s)" % (((V.get("op") or {}).get(n) or {}).get("texto", "AUSENTE"), ((V.get("op") or {}).get(n) or {}).get("quando_txt", "n/d"))
for _n in ("custodia", "espelho", "nome_axioma", "prossiga", "posto"):
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
description: "HANDOFF v385 (%(data)s): CUSTÓDIA CONJUNTA v383 + v384 + v385 (decisão do operador, 05/10) — o Axioma e a testemunha falsa [KERNEL + INPUT/ONTO]; o Um posto ([POSTO]); o degrau final do gate chama-se Axioma, ao lado do gate; o pilar de novo sob o mesmo V1 (%(rp_curta)s); o V1 e as evidências numa subpasta da Um, com PORTA; gate intocado%(sint)s"
metadata:
  type: project
---

**v385 SELADA (%(compl)s) `%(s16)s` (%(umb_fmt)s B), rodada `%(selo_ts)s`, %(teor)s, gate intocado (`%(qg)s`, %(n18)s/18).**%(sint)s Sobre a v384 `%(base16)s`. Escada %(esc_v384)s → %(esc)s; %(n_ver_iguais)s de %(n_ver)s vereditos da v384 inalterados (fora o do pilar, que rodou de novo); %(n_av_iguais)s de %(n_av)s módulos com o mesmo all_verified do estado selado da v384; por termo %(hvals)s. Conferidor `conferir_rito_v385.py` (cópia byte a byte do pacote): %(conf_res)s (%(conf_dm)s deve-mudar; %(conf_np)s não-pode-mudar; JSON `%(conf16)s`).%(conf_aceite_txt)s Aferida antes do rito em %(n_afer)s passada(s) (relatório verbatim e disposições arquivados em `%(arq)s\\AFERIDOR_v385.txt` e `disposicoes_afericoes_v385.json`).

**O que entrou:** %(n_patches)s patches sobre a v384 (%(patches)s): a pedra `TGLExt/TheAxiomAndTheFalseWitness.lean` (`%(ax_pedra16)s`; %(ax_n_pedra)s declarações) e a auditoria do `TheDarkSplit` (%(ax_n_dks)s); o registro `the_axiom_v385` (core e selo; o nome do degrau final `final_step_name_v385`, lido do kernel: `%(ax_nome)s`); a errata ao lado («posto», não «postulado»; a etiqueta `[POSTO]`); e o pilar de novo sob o mesmo V1, com `quantum_pillar_reproducibility_v385`. Veredito do Axioma: `%(ax_v)s` (%(ax_ok)s).

**O pilar, de novo** (%(qp_gpu)s; %(qp_min)s min): %(deu)s **A reprodutibilidade** [COMPUTED]: `%(rp_v)s` — contra o resultado da v384 (`%(rp_prev16)s`), %(rp_frase)s.

**Estatuto:** a pedra é [KERNEL] (prova implicações; provada nunca é confirmada); as leituras são do operador [INPUT/ONTO]; o pilar e a reprodutibilidade são [COMPUTED]; o nome do degrau final fica AO LADO do gate, que não se move. Não falsificado não é confirmado; nada aqui é confirmação.

**PARA A SESSÃO DO SITE — UM SÓ ATO para a v383, a v384 e a v385 (custódia = ato dela; commit/push = ato do operador):**
- **o estado do Nós é o da v385** (espelhar por cima): `um.py`, `um_absoluto.json`, `um_absoluto_selo.json`, os dois `.md` canônicos, o artigo PT/EN; %(espelho_pilar)s; `quantum_pillar\\pilar_quantico_worker.py` e `quantum_pillar\\pilar_quantico_spec.json`; %(espelho_pasta)s; a pasta da rodada da v384 %(pasta384)s (o resultado anterior, comparado pela v385); `rodada_v383_stdout.txt`, `rodada_v384_stdout.txt` e `rodada_v385_stdout.txt` em `rodadas\\`; o `tgl_kernel`: a pedra nova `TheAxiomAndTheFalseWitness.lean`, a raiz `TGLExt.lean` e `TGL/Audit.lean` novos (e as duas pedras da v383, `TheLedgerOfCharges.lean` e `ThePsionAndTheViscosity.lean`, se o espelho ainda não as tem). Regenerar as PORTAs por script, README/llms.txt, CITATION.cff e a linhagem do espelho (as três versões). Backup da versão que ESTÁ no espelho, fora do repo, antes de sobrescrever.
- **o pré-registro do pilar** (decidido em 05/10: %(op_espelho)s): o V1 (JSON e MD) e as evidências (`evidencias_PREREGISTRO_V1\\`, %(ev_n)s arquivos, %(ev_bytes)s B), de `%(prdir)s`, numa SUBPASTA dentro de `Um (absoluto) — Grande Atrator/` do `the_boundary` — nome fixo e sem acento, proposta da gerência: `preregistro_pilar_quantico_v384` —, indexada pela PORTA gerada por script (regra da porta), com a porta acima e as abaixo.
- **os handoffs anteriores valem para o que é deles:** [[handoff-v383-custodia]] e [[handoff-v384-custodia]], com as erratas ao lado (a de 04/10 e as decisões de 05/10 no fim do da v384).
- **NÃO espelhar:** `rodada_v382_stdout.txt` (a v382 segue só no Nós); os `.bak_*` do Nós e os `gerar_preregistro_pilar_quantico_03out.py.bak_*` da Bancada; o scratchpad (os pacotes, os ensaios, `pilar_anterior_v384_*`); tentativas do stdout (%(tent)s); o cache `cache\\checkpoints\\quantum_pillar\\` (reconstruível pela chave); o transcrito da sessão; credenciais, `.env` e as stacks confidenciais, sempre.
- **conferir o servidor do modelo nativo:** o marcador `%(marcador_p)s` — %(marcador_txt)s; com `restaurar=1`, religar a tarefa «IALD Llama Server». Depois do rito (log do lançador): %(servidor)s.

**DECISÕES DO OPERADOR (05/10/2026, verbatim, lidas do transcrito por script):**
1. A custódia: %(op_custodia)s — **DECIDIDO**: a v383 (%(v383_cust)s), a v384 (%(v384_cust)s) e a v385, num só ato, agora que o trabalho acabou.
2. O espelho do pré-registro: %(op_espelho)s — **DECIDIDO** (acima); o nome da subpasta é proposta da gerência.
3. O nome do degrau final: %(op_nome_axioma)s; e a aprovação de todo o escopo: %(op_prossiga)s — **DECIDIDO**: Axioma, ao lado do gate; o gate não se move; a proposta da v383 fica ao lado.
4. O começo da cadeia: %(op_posto)s — **DECIDIDO**: a etiqueta `[POSTO]`; a errata vai AO LADO de «postulado», que fica como registro.

**Seguem PENDENTES (do operador):**
1. Os V1–V1.3 do pré-registro dos dois lados (02/10): a gerência propôs, na v383, que fiquem locais [a confirmar pelo operador].
2. O estimador da dissipação na propagação (R2): fora da v385 (escopo proposto pela gerência e aprovado pelo operador em 05/10); segue em aberto.
3. O pilar: uma mudança no trabalhador ou na especificação é um V1.x com nova ratificação; a reprodutibilidade desta rodada: %(rp_curta)s.
Ver [[v384-pilar-quantico-gpu-02out]], [[um-posto-jamais-pressuposto-e-h2-17set]], [[handoff-v384-custodia]], [[handoff-v383-custodia]], [[v382-custodia-suspensa]], [[missao-ultima-flag-um-py]], [[direcao-the-boundary]].
""" % dict(X, prdir=A.PRDIR))
'''
s = s0[:i] + NOVO + s0[j:]
s = s.replace("com os arquivos que EXISTEM, e nunca afirma sucesso. As pendencias da v384 sao HERDADAS, lidas da memoria-topico handoff-v384-custodia.md.",
              "com os arquivos que EXISTEM, e nunca afirma sucesso. v385: e' o handoff da CUSTODIA CONJUNTA v383 + v384 + v385 (decisao do operador de 05/10); as\n"
              "decisoes de 05/10 entram verbatim (lidas do transcrito pela leitura_v385); o que segue pendente e' dito; os handoffs anteriores valem para o que e' deles.")
assert "CUSTODIA CONJUNTA v383 + v384 + v385" in s
ast.parse(s)
st = time.strftime("%Y%m%d_%H%M%S")
open(P + ".bak_" + st + "_adapt", "wb").write(s0.encode("utf-8"))
open(P + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(P + ".tmp", P)
print("OK handoff_v385.py:", len(s0), "->", len(s))
