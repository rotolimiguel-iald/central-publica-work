# -*- coding: utf-8 -*-
"""Registro da 5a afericao (gerencia, em nome proprio; so acrescimo): a 5a passada VERBATIM, por ENTRADA (lente x item, sem colapsar ids), com a disposicao de
cada entrada nao resolvida e de cada achado novo; o verificador adversarial da 5a NAO rodou (sessao OAuth expirada) -- dito; o texto do pre-registro corrigido
(a 4a passada com as duplicatas contadas) e acrescido da 5a. Backup de BYTES antes; temporario -> conferir -> substituir."""
import hashlib, json, os, sys, time
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
A5P = os.path.join(HERE, "afericao5_resultado.json"); A5 = json.load(open(A5P, encoding="utf-8"))
ENT = [(g["lente"], a) for g in A5["grupos"] for a in (g.get("itens") or [])]
NOV = A5["novos"]
ACAO_IT = {
    "4N0": "out_file_sha256 = o sha256 do que o runtime escreveu no Nos nesta rodada (resultado ou marcador); o SELO (W09b) so hasheia o arquivo do pilar se ele for esse, senao NOT_THIS_RUN; escrita e remocao com novas tentativas (40 x 0,25 s); o .tmp_qp apagado na falha; o marcador diz o motivo (result_file_absent so quando nao ha resultado); o registro do selo leva out_file_sha256 e out_file_remove_error; o texto diz NOT_THIS_RUN.",
    "4N1": "o comentario do passo 2 da arvore cita o modo zero (T2, T4 e D128); o trabalhador mudou (fb974f9d) e a especificacao e os rascunhos foram regenerados.",
    "#9": "(a) o indice da memoria e o bloco 9 passam a dar o caminho ABSOLUTO do marcador; (b) o vigia NAO e' mais morto: o religar apaga a bandeira e espera ele sair sozinho (ate 120 s), e a espera pelos stop registra quando expira.",
    "N19": "a variante sem_cache_d128 exige a frase propria do ramo («o cache so guarda o resultado completo com ele» / «the cache keeps only a complete result with it»).",
    "4N5": "o comentario e a docstring do ensaio dizem que o W08c leva a marca na linha e que os enunciados do terceiro balde saem do fluxo, sao conferidos por nome e executados a parte.",
    "4N6": "declarado: as edicoes da 4a no conferidor e no lancador foram MANUAIS (Edit), com backup .bak_antes_afer4; os diffs estao em diff_conferidor_afer4_manual.txt (sha256 8f1e0ab5...) e diff_lancador_afer4_manual.txt (76e5ecd5...); as edicoes da 5a no lancador foram por script aplicar_* com count == 1.",
    "4N25": "o diff da 3a no conferidor (do .bak_antes_afer3_RECONSTITUIDO, fe466024..., ao .bak_antes_afer4) gravado em diff_conferidor_afer3.txt (sha256 f0aa6e0f...).",
    "4N8": "a fracao do T1 truncada (int(1000 f)/10): nunca aparece 100,0% para uma fracao menor que 1 (testado: 0,9996 -> 99,9%).",
    "4N22": "REGRESSAO tratada: a frase da CPU so nos vereditos anulados pela CPU (CPU_REFERENCE_NOT_COMPARABLE ou DISAGREES_OR_ABSENT), nunca no sucesso; com a referencia AUSENTE diz «nao estava presente» com o erro, e o codigo do filho sem o «None» (testado nos 40 casos sinteticos: a frase so aparece nos anulados pela CPU).",
    "N14": "o rotulo do volume do MAGMA na leitura do estresse: «no estresse e na caracterizacao, por n (sem as sondas de tempo)».",
    "4N16": "a ratificacao exige EXATAMENTE uma escolha nomeada, com fronteira de palavra, aceitando hifen e sublinhado como espaco; recusa a mensagem que nomeie as duas.",
    "4N17": "os caminhos do trabalhador, das sondas e do pacote entram ABSOLUTOS no documento.",
}
ACAO_NOV = {
    0: "o parcial do D128 e' gravado logo depois do espectro, com n0 e zero_mode_ok: a violacao do modo zero sobrevive a uma morte do processo (trabalhador fb974f9d).",
    1: "MEDIO tratado: o vigia nao e' morto; dorme em passos de 1 s conferindo a bandeira, termina a parada em curso e sai; o religar espera ate 120 s (AVISO e kill so se nao sair); a espera pelos stop registra a expiracao.",
    2: "a sonda da tarefa DESABILITADA e' fail-closed (codigo 14).",
    3: "tres estados: depois do rito (RITO_INICIADO=2) o sinal so restaura e devolve o rc do rito.",
    4: "o mata_um so encerra os python um.py DESCENDENTES do lancador (cadeia de ParentProcessId a partir do PID nativo do lancador), nunca os de outra casa; testado so em leitura com um python um.py filho: acha so ele.",
    5: "o PID do lancador em .rito_v384.pid (removido no religar); o cabecalho e o pre-registro dizem: abortar = kill -TERM nesse PID; o TaskStop da ferramenta nao para o lancador.",
    6: "= 4N22 (a frase da CPU so nos anulados pela CPU).",
    7: "out_file_remove_error (e out_file_sha256) no registro do selo; e o selo grava NOT_THIS_RUN quando o arquivo nao e' o desta rodada.",
    8: "MEDIO tratado: = 4N22 (inclusive na rodada reaproveitada a frase nao aparece mais).",
    9: "a referencia AUSENTE e' dita como ausencia (com o erro gravado) e o codigo do filho sem «None» (none -> «nao terminou ou foi encerrado pelo prazo»).",
    10: "o rascunho diz as palavras exigidas na ratificacao; hifens aceitos.",
    11: "o pre-registro diz o lancador como ele e': recusa com a tarefa desabilitada so quando o servidor seria religado; espera ate 60 s.",
    12: "a arvore: o PARCIAL exige especificacao, trabalhador, beta e marca; o CUSTODY pode vir junto do PARCIAL, e o artigo le o composto como invalido.",
    13: "no congelamento, o rascunho apresentado (JSON e MD) e o gerador entram nas evidencias; as evidencias obrigatorias sao exigidas (so a afericao_6 e' opcional).",
    14: "o texto da 4a passada diz quantos dos novos eram duplicatas.",
    15: "o criterio do T1 com sigma > 0: beta dentro de 5% (relativo) e p dentro de 0,05 (absoluto).",
    16: "= 4N22.",
    17: "= 9.",
    18: "o artigo le o composto PARTIAL+CUSTODY como resultado nao valido (_part4 exige a ausencia do CUSTODY); a arvore diz que os dois podem coexistir.",
    19: "= 2.",
    20: "= 7.",
    21: "= 10.",
    22: "= 3.",
}
c5 = Counter(a["estado"] for _, a in ENT)
nao = [(l, a) for l, a in ENT if a["estado"] != "RESOLVIDO"]
falta = sorted({a["id"] for _, a in nao} - set(ACAO_IT)); assert not falta, falta
assert set(ACAO_NOV) == set(range(len(NOV))), (len(NOV), sorted(set(range(len(NOV))) - set(ACAO_NOV)))
dup5 = sum(1 for v in ACAO_NOV.values() if v.startswith("= "))
L = ["\n" + "=" * 80, "5a PASSADA -- conferencia das correcoes da 4a (VERBATIM de afericao5_resultado.json, sha256 %s; POR ENTRADA lente x item) e DISPOSICOES (gravadas em %s)" % (h(A5P), time.strftime("%d/%m/%Y %H:%M")),
     "AVISO: o verificador adversarial dos achados novos da 5a NAO rodou (a sessao OAuth do agente expirou); os achados novos ficam sem veredito de verificacao -- a 6a passada os verifica.", "=" * 80]
for l, a in ENT:
    L.append("\n%s [%s] ESTADO: %s" % (a["id"], l, a["estado"])); L.append("EVIDENCIA: " + a["evidencia"])
    if a.get("falta"):
        L.append("FALTA: " + a["falta"])
    if a["estado"] != "RESOLVIDO":
        L.append("DISPOSICAO DA GERENCIA: " + ACAO_IT[a["id"]])
for i, a in enumerate(NOV):
    L.append("\n[5N%d] (%s/%s; SEM verificacao) %s" % (i, a["origem"], a["severidade"], a["arquivo_linha"]))
    L.append("AFIRMACAO: " + a["afirmacao"]); L.append("EVIDENCIA: " + a["evidencia"]); L.append("CORRECAO PEDIDA: " + a["correcao"])
    L.append("DISPOSICAO DA GERENCIA: " + ACAO_NOV[i])
L.append("\nO QUE CADA LENTE EXAMINOU (5a passada, verbatim):")
for g in A5["grupos"]:
    for x in g.get("examinado") or []:
        L.append("- [%s] %s" % (g["lente"], x))
bloco = ("\n".join(L) + "\n").encode("utf-8")
p = os.path.join(HERE, "AFERIDOR_v384.txt"); raw = open(p, "rb").read()
if b"5a PASSADA -- conferencia das correcoes da 4a" in raw:
    print("a 5a ja esta gravada")
else:
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    novo = raw + bloco; open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw); os.replace(p + ".tmp", p)
    assert open(p, "rb").read()[:len(raw)] == raw
    print("AFERIDOR_v384.txt:", len(raw), "->", len(novo))
dp = os.path.join(HERE, "disposicoes_afericoes_v384.json"); D = json.load(open(dp, encoding="utf-8"))
open(dp + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "wb").write(open(dp, "rb").read())
dup4 = sum(1 for v in D["disposicoes_4a_novos"].values() if str(v).startswith("= "))
t = D["texto_para_o_pre_registro"]
old4 = "%d achados novos, %d sobreviventes à verificação (quase todos de severidade baixa)" % (D["passada4"]["novos"], D["passada4"]["sobreviventes"])
assert t.count(old4) == 1, old4
t = t.replace(old4, "%d achados novos, %d sobreviventes à verificação (%d deles duplicatas de outros; quase todos de severidade baixa)" % (D["passada4"]["novos"], D["passada4"]["sobreviventes"], dup4))
t = t.split("; 5ª passada")[0]
t += ("; 5ª passada (conferência das correções da 4ª): %d entradas (item × lente) — %d resolvidas, %d parciais e %d regressão; %d achados novos (%d deles duplicatas de outros), "
      "SEM a verificação adversarial (a sessão do verificador expirou), todos tratados no código ou no texto antes deste documento; a 6ª passada confere as correções e verifica esses achados") % (
    len(ENT), c5.get("RESOLVIDO", 0), c5.get("PARCIAL", 0), c5.get("REGRESSAO", 0), len(NOV), dup5)
D["texto_para_o_pre_registro"] = t
D["passada5"] = {"arquivo": os.path.basename(A5P), "sha256": h(A5P), "entradas": dict(c5), "n_entradas": len(ENT), "novos": len(NOV), "duplicatas_entre_os_novos": dup5,
                 "verificacao_adversarial": "NAO RODOU (sessao OAuth expirada)"}
D["disposicoes_5a_itens"] = ACAO_IT; D["disposicoes_5a_novos"] = {str(k): v for k, v in ACAO_NOV.items()}
b = json.dumps(D, ensure_ascii=False, indent=1).encode("utf-8"); open(dp + ".tmp", "wb").write(b); os.replace(dp + ".tmp", dp)
print("disposicoes:", hashlib.sha256(b).hexdigest()[:16], "| 5a:", dict(c5), "novos", len(NOV), "dup", dup5, "| 4a dup", dup4)
