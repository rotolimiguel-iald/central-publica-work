# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R4): grava REVISAO_TERCEIRO_v407.json e .md. A R3 ja' foi guardada em bytes (.R3.json/.R3.md).
Todo hash e' lido do arquivo AQUI; o candidato e' relido ao fechar e comparado com o do inicio."""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
RT = R + "revisao_terceiro/"
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
CAND_INICIO = "833121339e649f71"   # lido por mim no inicio da R4
cand_fim = s16(R + "um_v407_candidato.py"); cand_bytes = os.path.getsize(R + "um_v407_candidato.py")
r3 = json.load(open(RT + "REVISAO_TERCEIRO_v407.R3.json", encoding="utf-8"))
assert os.path.getsize(RT + "REVISAO_TERCEIRO_v407.R3.md") > 1000
chaves = list(r3["arquivos_revisados"]) + ["carimbar_stdout_v407.py", "rito_v407.sh", "orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md", "pos_rito/fila_memoria_v407.py"]
arquivos_revisados = {k: s16(R + k) for k in chaves}
mudaram_desde_r3 = sorted(k for k in r3["arquivos_revisados"] if s16(R + k) != r3["arquivos_revisados"][k])
novos_na_lista = ["carimbar_stdout_v407.py", "rito_v407.sh", "orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md", "pos_rito/fila_memoria_v407.py"]
R3A = r3["achados"]

novos = [
 {"sev": "BAIXO", "onde": "orquestrador/pos_treino_v407.py:recibo_do_app (bloco RESULTADOS, l. ~434-443)",
  "achado": "O `except` em volta de `jload(p)` cobre o JSON invalido (ignorado: testado, o recibo segue esperando). Mas um RESULTADO que e' JSON VALIDO e nao e' objeto (uma lista `[1,2]`, uma string `\"cumprida\"`) passa pelo jload e estoura em `rj.get(...)`, FORA do try: AttributeError dentro de recibo_do_app. Em s10_app isso cai no `except Exception` externo e o S10 e' marcado FALHOU com traceback: fail-closed e visivel (nunca abre falso), mas um arquivo estranho na pasta RESULTADOS encerra a espera de 24 h em vez de ser ignorado.",
  "evidencia": "revisao_terceiro/r4_s10.py e r4_s10_out.txt: casos «JSON e' uma lista» e «JSON e' string» -> EXCECAO AttributeError; JSON invalido -> False; os demais 17 casos como esperado.",
  "como_corrigir": "`if not isinstance(rj, dict): continue` logo depois do jload. Nao trava."},
 {"sev": "BAIXO", "onde": "orquestrador/pos_treino_v407.py:recibo_do_app (`desta = ... or re.match(...)`)",
  "achado": "O RESULTADO e' tomado como «desta ordem» se o campo `ordem` cita a ordem OU o NOME do arquivo e' `NNN_RESULTADO.json`. Com um arquivo `002_RESULTADO.json` cujo campo diz `ORDEM_020`, o recibo ABRE (o nome basta; testado). Evidencias que se contradizem deveriam recusar, nao aceitar pelo `or`. Os outros tres elos (instalacao PASS, contrato JEV, nucleo fixo conferidos na fonte) continuam exigidos, e com a release errada ou o pino errado o recibo fecha mesmo com RESULTADO cumprida (testado): o dano possivel e' so' o elo (a).",
  "evidencia": "r4_s10_out.txt: «campo ordem de outro numero, nome 002 (o campo diz ORDEM_020)» -> True; «sem campo ordem, nome 002» -> True; «outra ordem: ORDEM_999 em 999_RESULTADO.json» -> False; «ORDEM_0020 no campo e nome 020_RESULTADO.json» -> False (a regex nao confunde 2 com 20).",
  "como_corrigir": "Exigir o campo `ordem` quando existir (se existir e nao citar esta ordem, recusar) e usar o nome so' como reserva. Nao trava."},
 {"sev": "BAIXO", "onde": "rito_v407.sh:255 (linha de lancamento com o carimbador) e o comentario das l. 251-253",
  "achado": "(i) O carimbador e' fiel: gravou byte a byte o que recebeu, com o jsonl coerente (soma dos bytes por linha == bytes_total == tamanho do arquivo; sha256 do registro final == sha256 do arquivo; ultima linha sem terminador marcada), preservou UTF-8, CR e a ultima linha sem \\n, e o RC do subshell foi 0 e 7 como o do processo (pipefail). Testei com um um.py FALSO na pasta _carimbo, reproduzindo a linha do rito; o rito nao foi executado. Sem PYTHONUNBUFFERED o arquivo sai IDENTICO ao `> arquivo 2>&1` da v406. (ii) COM `PYTHONUNBUFFERED=1` (que o rito poe de proposito) a ORDEM relativa das linhas de stderr e stdout muda em relacao a forma antiga (stdout em bloco): mesmas linhas, ordem cronologica em vez da ordem de descarga. Portanto «o stdout canonico segue IDENTICO em bytes» vale para a copia do carimbador, nao para a comparacao com o stdout da v406; e a variavel e' herdada pelos subprocessos python do um.py (so' bufferizacao; o um.py nao despeja o ambiente). (iii) `set -o pipefail` e' extensao do bash sob `#!/bin/sh`: aqui sh == bash 5.2 (msys), funciona; em um sh POSIX estrito (dash) o subshell nao lancaria o um.py. (iv) O mata_um mata a arvore do subshell pelo PID nativo (taskkill /T): pega o um.py e o carimbador.",
  "evidencia": "revisao_terceiro/_carimbo/ (fake_um.py, out_0.txt, out_7.txt, ref.txt, out_nounbuf.txt, t_*.jsonl); `sh -c 'set -o pipefail; false | true; echo $?'` -> 1; `sh --version`: GNU bash 5.2.37 (x86_64-pc-msys).",
  "como_corrigir": "Dizer no comentario do rito que a ordem de stderr/stdout passa a ser cronologica (e que o stdout da v406 nao e' comparavel byte a byte neste ponto) e que o rito exige bash. Nao trava."},
]
carregados = []
for a in R3A[1:]:
    onde = a["onde"]
    for pref in ("[CARREGADO da R2, nao tocado nesta rodada] ", "[CARREGADO da R3, nao tocado] "):
        onde = onde.replace(pref, "")
    carregados.append(dict(a, onde="[CARREGADO da R3, nao tocado nesta rodada] " + onde))
achados = novos + carregados
assert len(carregados) == 4, len(carregados)

baixos_da_r3 = [
 {"onde": "R3-1. gerar_candidato_v407.py:229 (print do rito com «[KNOWN/ONTO] a ponte Bell-TT»)", "estado": "ATENDIDO",
  "evidencia": "Diff do gerador contra os dois .bak_r4_print_onto_* (identicos entre si, sha16 == o do gerador na R3): UMA linha, 229, e dentro dela so' a remocao dos 6 bytes «KNOWN/» (difflib por bytes; mesmos fins de linha, 467 LF em ambos). Candidato novo: «KNOWN/ONTO» ocorre 0 vezes; «[OPEN] o par na face de Fock; [ONTO] a ponte Bell-TT;» ocorre 1 vez (linha 278879); 43.065.104 - 43.065.098 = 6 bytes. PROVA EXATA: desfazendo essa unica substituicao no candidato novo obtenho o candidato da R3 com sha16 62a31fb08a3b7b97. compile() do gerador limpo."},
 {"onde": "R3-2. pos_rito/textos_v407.py: 46 LF isolados normalizados para CRLF", "estado": "DITO",
  "evidencia": "O arquivo nao mudou desde a R3 (sha16 igual ao da R3). Sem efeito semantico, a gerencia nao o reverte nesta versao; o achado fica carregado em `achados`."},
]

rotas = [
 "A/B (candidato): gerar_candidato_v407.py == so' a palavra; candidato 833121339e649f71 (43.065.098 B) ate' o byte: desfazer a unica substituicao reproduz o sha16 da R3. r4_a_intocados.py: 8 funcoes intocadas AST+fonte iguais a base, 25 mudados, 15 novos, 0 removidos; r4_a2_mudados.py: 25 'expected_ladder' 11860->11958; r4_d_kernel.py: 9 embutidos == sandbox == pedra == BUNDLE, 1755 == sandbox; r4_f_hashes.py: 55 conferencias, falhas []; COMPARACAO_V406_v407.json ok (1150 iguais, 25 mudados, 0 sem explicacao); ensaio_a_seco_v407.json TUDO PASSOU (sha16 do candidato novo); PRECONDICOES TODAS PASSARAM (p00_out_r4.txt tem o candidato 833121339e649f71 em ESPERADOS e PINOS_BN); refazer_out RC_REFAZER=0 (FIM 18:23:59); fim_de_cadeia_out RC_FIM=0 (FIM 18:33:48); kernel/POS_BUILD, KERNEL_RECIBO e FLAGS inalterados (15:10).",
 "Dos 28 arquivos de arquivos_revisados da R3 mudaram so' 3: o candidato, o gerador e orquestrador/pos_treino_v407.py. Entram na lista 4 arquivos novos: carimbar_stdout_v407.py, rito_v407.sh, orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md e pos_rito/fila_memoria_v407.py. Pedras, BUNDLE, runtime, registros, delta, pysnips, textos do pos_rito, comparar, ensaio, preparar_bundle e as guardas: sha16 IGUAIS aos da R3.",
 "C-bis (diffs contra os .bak_r4_*): pos_treino_v407.py == docstring + bloco RESULTADOS de recibo_do_app + o caso positivo/negativo do _ensaio_s10 (s1b_revisao NAO foi tocada); ORDEM_RELEASE_APP_TEMPLATE.md == uma frase (elo (a)); fila_memoria_v407.py == uma linha (sem sort_keys; `saida` monta {ok, op} primeiro e o harness do fechar passou standalone e na cadeia); rito_v407.sh == o comentario + o mv do jsonl antigo + a linha de lancamento; compile()/bash -n/sh -n limpos. A linha `echo 1 | python um.py` segue literal; o `wait`/`rc=$?`/`echo RITO_RC` ficaram intocados; o jsonl anterior e' renomeado com data; o carimbador nao decodifica nem reordena (le bytes, grava bytes, confere sha256 e tamanho no fim, rc 3 se diferir).",
 "C (S10): _ensaio_s10() da cadeia: 10 de 10 (positivo, positivo_resultado_json, negativo_resultado_parcial e os sete negativos antigos). r4_s10.py em dirs sinteticos de _orq_sandbox (nunca o TUNEL real): RESULTADO cumprida abre (tambem 'CUMPRIDA ' e sem campo ordem com nome certo); parcial, recusada, incerta, cumprida_parcial, sem estado, de outra ordem, anterior a ordem, JSON invalido FECHAM; release errada e pino errado FECHAM mesmo com RESULTADO cumprida (os outros 3 elos seguem exigidos); sem RELATORIO e sem RESULTADOS fecha; o RELATORIO antigo continua valendo. Dois pontos fora do esperado = achados 1 e 2.",
 "D (S1b): r4_l_s1b.py / r4_s1b_real_out.txt: com os arquivos_revisados novos a S1b ABRE; com um arquivo de pos_rito, de orquestrador, o carimbador ou o rito alterado FECHA; com a REVISAO da R3 em bytes FECHA (o candidato e 3 arquivos mudaram); casos de omissao (campo ausente/vazio/arquivo ausente/'..') seguem ABRINDO como na R2/R3 (carregado).",
 "Guardas P18 e de frases sobre template, carimbador, rito, fila_memoria e gerador: 0 achados (pos_treino_v407.py tem 1 hit P18 PRE-EXISTENTE, igual nos .bak: o texto «NOT_FALSIFIED nunca e' CONFIRMED» de uma regra, nao texto publico).",
 "Mapa de Rotas: consultado na R2; nada novo a consultar para este diff; a gerencia registra.",
]
ressalvas = [
 "R4 confinada ao diff. NAO repeti: os 283 s de lean, os 159 casos fail-closed, a guarda do gerador / comparador / c16 / reading (gerar_candidato, comparar, ensaio e runtime tem o sha16 da R3), nem o README renderizado (registros, delta, pysnips e textos do pos_rito iguais aos da R3).",
 "NAO executei o rito, o instalar, o reverter nem a cadeia; o carimbador foi testado so' com um um.py falso e a MESMA linha de lancamento (pasta _carimbo). O comportamento do carimbador com o um.py real (volume, tempo, kill) nao foi medido por mim.",
 "NAO examinei o EN frase a frase, os PDFs alem do que o ensaio registra, nem o conferidor instalar/rito por dentro (122 invariantes: tomei o p00_out_r4.txt como fonte, `PRECONDICOES: TODAS PASSARAM`).",
 "arquivos_revisados: as 28 chaves da R3 com os sha16 atuais mais 4 (carimbar_stdout_v407.py, rito_v407.sh, ORDEM_RELEASE_APP_TEMPLATE.md, fila_memoria_v407.py). Se qualquer arquivo listado mudar, esta revisao nao vale para ele. A frase selada «0 alto e 0 medio em todas as rodadas» continua verdadeira com esta aprovacao (R1 0/0/9, R2 0/0/8, R3 0/0/5, R4 0/0/7).",
]
n_alto = 0; n_medio = 0; n_baixo = sum(1 for a in achados if a["sev"] == "BAIXO")
aprovada = bool(cand_fim == CAND_INICIO and n_alto == 0 and n_medio == 0)
out = {"aprovada": aprovada, "candidato_sha16": cand_fim, "candidato_sha16_no_inicio": CAND_INICIO, "candidato_bytes": cand_bytes,
       "revisor": "Claude Sonnet (agente revisor de terceiro; rodada R4; nao construi a v407; mesma familia da R1/R2/R3 e da revisao de 02/11, outra instancia)",
       "rodada": "R4", "quando": datetime.datetime.now().isoformat(timespec="seconds"),
       "n_alto": n_alto, "n_medio": n_medio, "n_baixo": n_baixo, "achados": achados, "baixos_da_r3": baixos_da_r3,
       "ressalvas": ressalvas, "rotas_examinadas": rotas, "arquivos_revisados": arquivos_revisados,
       "arquivos_que_mudaram_desde_a_R3": mudaram_desde_r3, "arquivos_novos_na_lista": novos_na_lista,
       "candidato_mudou_durante_a_revisao": cand_fim != CAND_INICIO,
       "nota": "aprovada: true so' com 0 ALTO e 0 MEDIO e o candidato integro do inicio ao fim. R3 guardada em bytes: REVISAO_TERCEIRO_v407.R3.json/.R3.md (R2 e R1 em .R2.* e .R1.*). Os 7 BAIXOS ficam escritos (3 novos desta rodada, 4 carregados); nenhum impede a aprovacao. Se qualquer arquivo de arquivos_revisados mudar, esta revisao nao vale para ele."}
json.dump(out, open(RT + "REVISAO_TERCEIRO_v407.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
md = ["# REVISAO DE TERCEIRO v407 - RODADA R4 (confinada ao diff desde a R3)", "",
      "**%s** | candidato `um_v407_candidato.py` sha16 `%s` (%d bytes; igual ao do inicio: %s) | %s | revisor: %s" % ("APROVADA" if aprovada else "NAO APROVADA", cand_fim, cand_bytes, cand_fim == CAND_INICIO, out["quando"], out["revisor"]), "",
      "ALTO %d | MEDIO %d | BAIXO %d. R3 guardada em `REVISAO_TERCEIRO_v407.R3.json/.md`; R2 em `.R2.*`; R1 em `.R1.*`." % (n_alto, n_medio, n_baixo), "", "## Os BAIXOS da R3", ""]
for b in baixos_da_r3: md.append("- **%s** - `%s`: %s" % (b["onde"], b["estado"], b["evidencia"]))
md += ["", "## Achados que restam (todos BAIXO)", ""]
for i, a in enumerate(achados, 1):
    md += ["### %d. %s - %s" % (i, a["sev"], a["onde"]), "", a["achado"], "", "*Evidencia:* " + a["evidencia"], "", "*Como corrigir:* " + a["como_corrigir"], ""]
md += ["## Verificacoes", ""] + ["- " + r for r in rotas] + ["", "## Ressalvas", ""] + ["- " + r for r in ressalvas]
md += ["", "## Arquivos que mudaram desde a R3", ""] + ["- `%s`" % k for k in mudaram_desde_r3] + ["", "## Arquivos novos na lista", ""] + ["- `%s`" % k for k in novos_na_lista]
md += ["", "## arquivos_revisados (sha16, relativo a v407/)", ""] + ["- `%s`: `%s`" % (k, v) for k, v in arquivos_revisados.items()]
open(RT + "REVISAO_TERCEIRO_v407.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print("aprovada:", aprovada, "| cand_fim:", cand_fim, "| inicio:", CAND_INICIO, "| alto/medio/baixo:", n_alto, n_medio, n_baixo, "| arquivos_revisados:", len(arquivos_revisados), "| mudaram desde R3:", mudaram_desde_r3)
