# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R5, so' orquestrador/pos_treino_v407.py): grava REVISAO_TERCEIRO_v407.json e .md. A R4 ja' foi guardada em bytes (.R4.json/.R4.md).
Todo hash e' lido do arquivo AQUI; o candidato e' relido ao fechar e comparado com o do inicio."""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
RT = R + "revisao_terceiro/"
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
CAND_INICIO = "833121339e649f71"   # lido por mim no inicio da R5
cand_fim = s16(R + "um_v407_candidato.py"); cand_bytes = os.path.getsize(R + "um_v407_candidato.py")
r4 = json.load(open(RT + "REVISAO_TERCEIRO_v407.R4.json", encoding="utf-8"))
assert os.path.getsize(RT + "REVISAO_TERCEIRO_v407.R4.md") > 1000 and r4["rodada"] == "R4"
arquivos_revisados = {k: s16(R + k) for k in r4["arquivos_revisados"]}   # as MESMAS 32 chaves da R4, sha16 atuais
mudaram_desde_r4 = sorted(k for k, v in arquivos_revisados.items() if v != r4["arquivos_revisados"][k])
A4 = r4["achados"]   # [0] nao-objeto, [1] nome-ou-campo, [2] carimbador, [3] EOL, [4] S1b omissao, [5] c16, [6] aspas

carregados = []
for a in A4[2:]:
    onde = a["onde"]
    for pref in ("[CARREGADO da R3, nao tocado nesta rodada] ", "[CARREGADO da R3, nao tocado] ", "[CARREGADO da R2, nao tocado nesta rodada] "):
        onde = onde.replace(pref, "")
    if onde.startswith("rito_v407.sh:255"):
        onde = "[DITO pela gerencia: a ordem de intercalacao de stderr nunca foi contrato; a copia fiel e' o contrato] " + onde
    else:
        onde = "[CARREGADO da R4, nao tocado nesta rodada] " + onde
    carregados.append(dict(a, onde=onde))
assert len(carregados) == 5, len(carregados)
achados = carregados

baixos_da_r4 = [
 {"onde": "R4-1. pos_treino_v407.py:recibo_do_app: RESULTADO que e' JSON valido mas nao objeto derrubava o S10", "estado": "ATENDIDO",
  "evidencia": "Diff contra pos_treino_v407.py.bak_r5_s10_robustez_20261103_184309 (sha16 a6e4fc944a83120b == o da R4): `if not isinstance(rj, dict): continue` logo depois do jload. r5_s10.py / r5_s10_out.txt: lista `[1,2]`, string, `null` e numero -> recibo False SEM excecao (antes: AttributeError). _ensaio_s10(): `negativo_resultado_nao_objeto` true, sem Traceback."},
 {"onde": "R4-2. recibo_do_app: o nome do arquivo bastava mesmo com o campo `ordem` contradizendo", "estado": "ATENDIDO",
  "evidencia": "Agora `_ord = str(rj.get('ordem','') or '').strip()`; com `_ord` nao vazio manda a regex ORDEM_<num> sobre o campo; so' sem o campo vale o nome. Testado: 002_RESULTADO.json com ordem ORDEM_020 -> False (antes True); 999_RESULTADO.json com ordem ORDEM_002 -> True (o campo manda); ordem null, '' e '   ' + nome certo -> True (campo ausente/vazio: vale o nome); ORDEM_020 no campo e nome 020 -> False (nao confunde 2 com 20); ordem inteiro 2 -> False (conservador). Os 3 outros elos seguem exigidos (release errada e pino errado fecham mesmo com `cumprida`). _ensaio_s10(): `negativo_resultado_ordem_divergente` true; 12 de 12, ok true."},
 {"onde": "R4-3. rito_v407.sh:255 carimbador com PYTHONUNBUFFERED: stdout canonico nao e' comparavel byte a byte com o da v406 (ordem de stderr)", "estado": "DITO",
  "evidencia": "Decisao da gerencia: a ordem de intercalacao de stderr nunca foi contrato; o contrato e' a copia fiel do que o um.py emite neste rito (que o carimbador garante, sha256 e tamanho conferidos). rito_v407.sh nao mudou desde a R4 (sha16 igual). Fica carregado em `achados`."},
]

rotas = [
 "A (diff == declarado): orquestrador/pos_treino_v407.py contra o .bak_r5_*: 3 hunks: (1) recibo_do_app, linha 441 -> 4 linhas (isinstance + `_ord` + `desta`); (2) _ensaio_s10: `montar(..., resultado_json=None)` e o ramo que escreve o texto bruto de NNN_RESULTADO.json; (3) dois `montar(...)` negativos novos (lista JSON; nome 002 com campo ORDEM_020 = num + 18) e os dois res[...]. `s1b_revisao` e o resto NAO foram tocados. compile() limpo.",
 "B (os meus dois casos da R4): r5_s10.py (copia da r4_s10.py com expectativas atualizadas, dirs sinteticos em _orq_sandbox, nunca o TUNEL real): _ensaio_s10() 12 de 12 (ok true: positivo, positivo_resultado_json e os 10 negativos), 28 casos meus, 0 inesperados; os dois pontos da R4 agora FECHAM sem excecao.",
 "C (S1b): so' orquestrador/pos_treino_v407.py mudou entre os 32 arquivos_revisados da R4 (sha16 a6e4fc944a83120b -> o atual, lido do arquivo); o candidato (833121339e649f71, 43.065.098 B), o gerador, o carimbador, o rito, o template, a fila_memoria, as pedras, o runtime, o registros/delta/pysnips e os textos do pos_rito: sha16 IGUAIS aos da R4. r5_l_s1b.py / r5_s1b_real_out.txt: com os arquivos_revisados novos ABRE; com a REVISAO da R4 em bytes FECHA (pos_treino mudou); com qualquer arquivo de pos_rito, orquestrador, carimbador, rito, fila ou template alterado FECHA.",
]
ressalvas = [
 "R5 confinada a orquestrador/pos_treino_v407.py. Nao repeti nada do que a R4 aprovou e nao mudou (candidato, kernel, hashes, guardas, README, carimbador, fila_memoria).",
 "O orquestrador original NAO foi executado (so' importado, com ORQ/LOG/ESTADO redirecionados para _orq_sandbox e nada de main; _ensaio_s10 roda em dirs sinteticos). O comportamento do S10 com o app real (TUNEL_CLAUDE_APP) nao foi medido por mim.",
 "arquivos_revisados: as 32 chaves da R4 com os sha16 atuais. Se qualquer arquivo listado mudar, esta revisao nao vale para ele. Os 5 BAIXOS que restam ficam escritos e nenhum impede a aprovacao. A frase selada «0 alto e 0 medio em todas as rodadas» segue verdadeira (R1 0/0/9, R2 0/0/8, R3 0/0/5, R4 0/0/7, R5 0/0/5).",
]
n_alto = 0; n_medio = 0; n_baixo = sum(1 for a in achados if a["sev"] == "BAIXO")
aprovada = bool(cand_fim == CAND_INICIO and n_alto == 0 and n_medio == 0)
out = {"aprovada": aprovada, "candidato_sha16": cand_fim, "candidato_sha16_no_inicio": CAND_INICIO, "candidato_bytes": cand_bytes,
       "revisor": "Claude Sonnet (agente revisor de terceiro; rodada R5; nao construi a v407; mesma familia da R1 a R4 e da revisao de 02/11, outra instancia)",
       "rodada": "R5", "quando": datetime.datetime.now().isoformat(timespec="seconds"),
       "n_alto": n_alto, "n_medio": n_medio, "n_baixo": n_baixo, "achados": achados, "baixos_da_r4": baixos_da_r4,
       "ressalvas": ressalvas, "rotas_examinadas": rotas, "arquivos_revisados": arquivos_revisados, "arquivos_que_mudaram_desde_a_R4": mudaram_desde_r4,
       "candidato_mudou_durante_a_revisao": cand_fim != CAND_INICIO,
       "nota": "aprovada: true so' com 0 ALTO e 0 MEDIO e o candidato integro do inicio ao fim. R4 guardada em bytes: REVISAO_TERCEIRO_v407.R4.json/.R4.md (R3, R2 e R1 em .R3.*, .R2.*, .R1.*). Os 5 BAIXOS que restam ficam escritos (1 DITO pela gerencia, 4 carregados); nenhum impede a aprovacao. Se qualquer arquivo de arquivos_revisados mudar, esta revisao nao vale para ele."}
json.dump(out, open(RT + "REVISAO_TERCEIRO_v407.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
md = ["# REVISAO DE TERCEIRO v407 - RODADA R5 (so' o orquestrador)", "",
      "**%s** | candidato `um_v407_candidato.py` sha16 `%s` (%d bytes; igual ao do inicio: %s) | %s | revisor: %s" % ("APROVADA" if aprovada else "NAO APROVADA", cand_fim, cand_bytes, cand_fim == CAND_INICIO, out["quando"], out["revisor"]), "",
      "ALTO %d | MEDIO %d | BAIXO %d. R4 guardada em `REVISAO_TERCEIRO_v407.R4.json/.md`; R3, R2 e R1 em `.R3.*`, `.R2.*`, `.R1.*`." % (n_alto, n_medio, n_baixo), "", "## Os BAIXOS novos da R4", ""]
for b in baixos_da_r4: md.append("- **%s** - `%s`: %s" % (b["onde"], b["estado"], b["evidencia"]))
md += ["", "## Achados que restam (todos BAIXO)", ""]
for i, a in enumerate(achados, 1):
    md += ["### %d. %s - %s" % (i, a["sev"], a["onde"]), "", a["achado"], "", "*Evidencia:* " + a["evidencia"], "", "*Como corrigir:* " + a["como_corrigir"], ""]
md += ["## Verificacoes", ""] + ["- " + r for r in rotas] + ["", "## Ressalvas", ""] + ["- " + r for r in ressalvas]
md += ["", "## Arquivos que mudaram desde a R4", ""] + ["- `%s`" % k for k in mudaram_desde_r4] + ["", "## arquivos_revisados (sha16, relativo a v407/)", ""] + ["- `%s`: `%s`" % (k, v) for k, v in arquivos_revisados.items()]
open(RT + "REVISAO_TERCEIRO_v407.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print("aprovada:", aprovada, "| cand_fim:", cand_fim, "| inicio:", CAND_INICIO, "| alto/medio/baixo:", n_alto, n_medio, n_baixo, "| arquivos_revisados:", len(arquivos_revisados), "| mudaram desde R4:", mudaram_desde_r4)
