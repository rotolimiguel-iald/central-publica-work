# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R3): grava REVISAO_TERCEIRO_v407.json e .md. A R2 ja' foi guardada em bytes (.R2.json/.R2.md).
Todo hash e' lido do arquivo AQUI; o candidato e' relido ao fechar e comparado com o do inicio."""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
RT = R + "revisao_terceiro/"
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
CAND_INICIO = "62a31fb08a3b7b97"   # lido por mim no inicio da R3
cand_fim = s16(R + "um_v407_candidato.py"); cand_bytes = os.path.getsize(R + "um_v407_candidato.py")
r2 = json.load(open(RT + "REVISAO_TERCEIRO_v407.R2.json", encoding="utf-8"))
assert os.path.getsize(RT + "REVISAO_TERCEIRO_v407.R2.md") > 1000
arquivos_revisados = {k: s16(R + k) for k in r2["arquivos_revisados"]}   # as MESMAS 28 chaves da R2, sha16 atuais
mudaram_desde_r2 = sorted(k for k, v in arquivos_revisados.items() if v != r2["arquivos_revisados"][k])
A2 = r2["achados"]

achados = [
 {"sev": "BAIXO", "onde": "gerar_candidato_v407.py:229 (print do cabecalho «O PSION, O CANTO E O PAR [v407 ...]»; no candidato, linha 278879); stdout canonico do rito",
  "achado": "A troca [KNOWN/ONTO] -> [ONTO] da ponte Bell-TT foi feita em delta (ressalva 3), artigo PT/EN, pos_rito/textos_v407.py e textos_v407_novo.pysnip, mas escapou UMA ocorrencia: o print do rito que abre o bloco do psion ainda diz «[OPEN] o par na face de Fock; [KNOWN/ONTO] a ponte Bell-TT». Esse texto vai para rodada_v407_stdout.txt (stdout do rito e' canonico) e fica selado com a etiqueta [KNOWN] sem citacao, o defeito que a R1/R2 apontaram. grep «KNOWN/ONTO» no candidato: 1 ocorrencia; nos arquivos-fonte da v407 (fora dos .bak e dos scripts r2_/correcoes): so' gerar_candidato_v407.py:229; nos 52 textos rendidos do harness: nenhuma.",
  "evidencia": "grep -n KNOWN/ONTO um_v407_candidato.py -> 278879; grep -l em *.py *.pysnip pos_rito orquestrador pedra -> gerar_candidato_v407.py; harness textos: zero.",
  "como_corrigir": "Trocar por [ONTO] na linha 229 do gerador (muda o candidato: pede rodada nova) ou deixar dito. Nao trava: e' etiqueta de um print, a mesma ponte aparece como [ONTO] em todas as outras superficies."},
 {"sev": "BAIXO", "onde": "pos_rito/textos_v407.py (bytes): fins de linha",
  "achado": "O diff contra o .bak_r3_baixos e' exatamente o declarado ao nivel de TEXTO (1 linha: [KNOWN/ONTO] -> [ONTO]). Ao nivel de BYTES ha' uma mudanca nao declarada: o arquivo tinha 1088 CRLF e 46 LF isolados (as 10 primeiras linhas de comentario e 36 linhas em branco) e agora tem 1134 CRLF e 0 LF isolados (o patch normalizou os fins de linha). Sem efeito semantico (o import normaliza \\n; ignorando o fim de linha so' 1 linha difere), mas e' a mudanca que o pedido nao listou.",
  "evidencia": "contagem de b'\\r\\n' e b'\\n' nos dois arquivos (113521 -> 113561 bytes); difflib sobre o texto normalizado: 2 linhas (-/+) = a linha 1099.",
  "como_corrigir": "Dizer no caderno (ja' esta' aqui). Nao trava."},
] + [dict(a, onde="[CARREGADO da R2, nao tocado nesta rodada] " + a["onde"]) for a in (A2[4], A2[5], A2[6])]

baixos_da_r2 = [
 {"onde": "R2-1. rito_v407.sh:22 (comentario de tempo)", "estado": "ATENDIDO",
  "evidencia": "diff contra rito_v407.sh.bak_r3_tempo_*: so' a linha 22; «a medida do sandbox, 379 s + 245 s» -> «337 s + 271 s» e «Audit de 245 s» -> «Audit de 271 s» (== construir_marcas.txt: 337 s e 271 s); bash -n limpo; nenhum comando mudou."},
 {"onde": "R2-2. registros_v407.py:155 (NAO diz 11) x ressalva (6)", "estado": "ATENDIDO",
  "evidencia": "Agora: «que as pedras tenham revisao de terceiro POR DENTRO das provas: em 02/11 o Sonnet reviu tres das sete (docstrings e enunciados); em 03/11 o revisor desta preparacao conferiu as nove por #print axioms, diff contra as origens e docstrings, nao as provas linha a linha». Coerente com a ressalva (6) no paragrafo renderizado por mim (paragrafo_renderizado_R3.txt, 11 de 11 ressalvas, verificar_paragrafo_v407 sem falhas). O escopo da revisao de 02/11 («docstrings e enunciados», sem rodar lean) confere com o cabecalho dela."},
 {"onde": "R2-3. «relidas inteiras» (delta RESSALVAS[4]; artigo PT/EN; README (6))", "estado": "ATENDIDO",
  "evidencia": "delta, artigo PT e artigo EN: «conferidas ... (#print axioms no trio, diff contra as origens e docstrings; nao as provas linha a linha; 0 alto e 0 medio em todas as rodadas; ...)». Descreve com exatidao o meu escopo da R1/R2. Ressalva: «0 alto e 0 medio em todas as rodadas» e' verdadeira para R1 (0/0/9), R2 (0/0/8) e, se esta R3 for aprovada como esta' gravada, R3 (0/0/5); o texto sela uma afirmacao sobre esta rodada, entao so' vale com esta aprovacao."},
 {"onde": "R2-4. papeis dos recibos/saidas R1 (registros_v407.py:55-58)", "estado": "ATENDIDO",
  "evidencia": "As quatro FONTES ganham «[registro R1: a fonte vigente e' a R2, recibo R2 abaixo]» (recibos) e «[registro R1: a saida vigente e' a R2, saida_lean_r3.txt / saida_lean_par_r2.txt]» (saidas): o nome saida_lean_r2.txt deixa de enganar. O candidato traz 4 ocorrencias de «registro R1»."},
 {"onde": "R2-5. S1b fail-open por omissao (campo ausente/vazio, arquivo ausente, '..')", "estado": "NAO_ATENDIDO",
  "evidencia": "pos_treino_v407.py inalterado desde a R2 (sha16 == o da R2); r3_l_s1b_out.txt repete os casos 7-10 (ABRE). Nao tratado pelo pedido da R3; fica escrito (BAIXO, nao impede)."},
 {"onde": "R2-6. c16 so' varre chaves de topo", "estado": "NAO_ATENDIDO",
  "evidencia": "runtime_v407.py inalterado desde a R2. Fica escrito (BAIXO, nao impede)."},
 {"onde": "R2-7. aspas residuais nas pedras e nos resumos do acervo", "estado": "DITO",
  "evidencia": "Pedras nao tocadas (sha16 das 9 == R2); o pedido da R3 diz que ficam para o caderno da v408. Segue em registros_v407.py:234 (ao_lado_de da E19, «psi+ psi- cancelado = vacuo» e «|G> como produto nao emaranhado»): registros_v407.py so' mudou nas linhas 55-58 e 155."},
 {"onde": "R2-8. [KNOWN/ONTO] da ponte Bell-TT", "estado": "NAO_ATENDIDO",
  "evidencia": "PARCIAL: [ONTO] nas superficies pedidas (delta ressalva 3: «[ONTO] (sem citacao [KNOWN] ate' haver fonte)»; artigo PT/EN l.29 «[ONTO]»; textos_v407.py:1099 e textos_v407_novo.pysnip:230; README renderizado). Escapou o print do rito em gerar_candidato_v407.py:229 (achado 1)."},
]

rotas = [
 "A (diff == declarado): diff de cada arquivo contra o seu .bak_r3_*: delta_v407.py (2 linhas: 263 e 266), registros_v407.py (55-58 e 155), artigo_pt/en_v407.pysnip (29 e 32 cada), pos_rito/textos_v407.py (1 linha de texto, 1099; + normalizacao de fim de linha, achado 2), pos_rito/textos_v407_novo.pysnip (230), rito_v407.sh (22): exatamente o declarado. Os .bak tem o sha16 == o da R2 em arquivos_revisados nos 6 arquivos de R2 (rito_v407.sh nao estava na lista). compile() limpo em delta, registros e textos_v407.py; bash -n limpo.",
 "Dos 28 arquivos de arquivos_revisados da R2, mudaram 7: o candidato, registros, delta, os dois pysnips do artigo, pos_rito/textos_v407.py e textos_v407_novo.pysnip — todos com .bak_r3. As 9 pedras, BUNDLE, KERNEL_RECIBO, runtime, gerar_candidato, comparar, ensaio, preparar_bundle, as guardas e pos_treino_v407.py: sha16 IGUAIS aos da R2. kernel/POS_BUILD_v407.json (Built 9, Replayed 0), KERNEL_RECIBO e FLAGS: mtime 15:10, inalterados.",
 "B (candidato novo 62a31fb08a3b7b97, 43.065.104 B): r3_a_intocados.py: 8 funcoes intocadas AST+fonte iguais a base; 25 nomes mudados (= COMPARACAO_V406_v407.json ok: 1150 iguais, 25 mudados, 0 sem explicacao, 0 removidos), 15 novos; r3_a2_mudados.py: 25 'expected_ladder' 11860->11958; r3_d_kernel.py: 9 embutidos == sandbox == pedra == BUNDLE, raiz = raiz v406 + 9 imports, 1755 embutidos == sandbox; r3_f_hashes.py: 55 conferencias, falhas []; ensaio_a_seco_v407.json: TUDO PASSOU, sha16 do candidato novo, artigo PT/EN pdflatex rc 0/0 sem erros; PRECONDICOES: TODAS PASSARAM; refazer_out termina em RC_REFAZER=0 e fim_de_cadeia_out em RC_FIM=0. As frases antigas (relidas inteiras, re-read in full, ponte nao e termo [KNOWN/ONTO], NAO diz 11 antigo) NAO estao mais no candidato; as novas estao (grep -F).",
 "r3_h_paragrafo_e_guardas.py: README renderizado de novo (paragrafo_renderizado_R3.txt), verificar_paragrafo_v407 sem falhas, 11 de 11 ressalvas inteiras, controle negativo reprova; guardas sobre 60 arquivos: so' os dois achados de sempre (o texto das proprias regras); r3_e_citacoes: nenhuma citacao nova.",
 "D (S1b): r3_l_s1b.py (copia _orq_sandbox; ORQ/LOG/ESTADO redirecionados; nenhum main): com o candidato novo e arquivos_revisados integros ABRE; com um arquivo de pos_rito alterado FECHA; com o proprio pos_treino alterado FECHA; aprovada string, sha16 de outro candidato e aprovada False FECHAM; ensaio final com a REVISAO real da R3 em r3_s1b_real_out.txt.",
 "Mapa de Rotas: consultado na R2 («v407»); nada novo a consultar para um diff de texto; a gerencia registra.",
]
ressalvas = [
 "R3 e' confinada ao diff: nao repeti os 283 s de lake env lean nem os 159 casos fail-closed nem a guarda do gerador / comparador / c16 / reading da R2, porque gerar_candidato_v407.py, comparar_v406_v407.py, ensaio_a_seco_v407.py, runtime_v407.py e as pedras tem o mesmo sha16 da R2.",
 "NAO examinei: o EN frase a frase (so' as duas trocas, em paridade com o PT); instalar, reverter, o rito; os PDFs alem do que o ensaio da cadeia registra.",
 "Independencia: mesma familia de modelo (Sonnet) da R1/R2, outra instancia da mesma linha; nada foi escrito fora de revisao_terceiro/.",
 "arquivos_revisados: as MESMAS 28 chaves da R2, com os sha16 atuais; rito_v407.sh segue de fora (so' comentario). Se qualquer arquivo listado mudar, esta revisao nao vale para ele.",
]
n_alto = 0; n_medio = 0; n_baixo = sum(1 for a in achados if a["sev"] == "BAIXO")
aprovada = bool(cand_fim == CAND_INICIO and n_alto == 0 and n_medio == 0)
out = {"aprovada": aprovada, "candidato_sha16": cand_fim, "candidato_sha16_no_inicio": CAND_INICIO, "candidato_bytes": cand_bytes,
       "revisor": "Claude Sonnet (agente revisor de terceiro; rodada R3; nao construi a v407; mesma familia da R1/R2 e da revisao de 02/11, outra instancia)",
       "rodada": "R3", "quando": datetime.datetime.now().isoformat(timespec="seconds"),
       "n_alto": n_alto, "n_medio": n_medio, "n_baixo": n_baixo, "achados": achados, "baixos_da_r2": baixos_da_r2,
       "ressalvas": ressalvas, "rotas_examinadas": rotas, "arquivos_revisados": arquivos_revisados, "arquivos_que_mudaram_desde_a_R2": mudaram_desde_r2,
       "candidato_mudou_durante_a_revisao": cand_fim != CAND_INICIO,
       "nota": "aprovada: true so' com 0 ALTO e 0 MEDIO e o candidato integro do inicio ao fim. R2 guardada em bytes: REVISAO_TERCEIRO_v407.R2.json/.R2.md (e a R1 em .R1.*). Achados BAIXO ficam escritos; nenhum impede a aprovacao. Se qualquer arquivo de arquivos_revisados mudar, esta revisao nao vale para ele."}
json.dump(out, open(RT + "REVISAO_TERCEIRO_v407.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
md = ["# REVISAO DE TERCEIRO v407 - RODADA R3 (confinada ao diff)", "",
      "**%s** | candidato `um_v407_candidato.py` sha16 `%s` (%d bytes; igual ao do inicio: %s) | %s | revisor: %s" % ("APROVADA" if aprovada else "NAO APROVADA", cand_fim, cand_bytes, cand_fim == CAND_INICIO, out["quando"], out["revisor"]), "",
      "ALTO %d | MEDIO %d | BAIXO %d. R2 guardada em `REVISAO_TERCEIRO_v407.R2.json/.md`; R1 em `.R1.*`." % (n_alto, n_medio, n_baixo), "", "## Os BAIXOS da R2", ""]
for b in baixos_da_r2: md.append("- **%s** - `%s`: %s" % (b["onde"], b["estado"], b["evidencia"]))
md += ["", "## Achados que restam (todos BAIXO)", ""]
for i, a in enumerate(achados, 1):
    md += ["### %d. %s - %s" % (i, a["sev"], a["onde"]), "", a["achado"], "", "*Evidencia:* " + a["evidencia"], "", "*Como corrigir:* " + a["como_corrigir"], ""]
md += ["## Verificacoes", ""] + ["- " + r for r in rotas] + ["", "## Ressalvas", ""] + ["- " + r for r in ressalvas]
md += ["", "## Arquivos que mudaram desde a R2", ""] + ["- `%s`" % k for k in mudaram_desde_r2] + ["", "## arquivos_revisados (sha16, relativo a v407/)", ""] + ["- `%s`: `%s`" % (k, v) for k, v in arquivos_revisados.items()]
open(RT + "REVISAO_TERCEIRO_v407.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print("aprovada:", aprovada, "| cand_fim:", cand_fim, "| inicio:", CAND_INICIO, "| alto/medio/baixo:", n_alto, n_medio, n_baixo, "| arquivos_revisados:", len(arquivos_revisados), "| mudaram desde R2:", mudaram_desde_r2)
