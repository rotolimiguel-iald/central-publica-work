# -*- coding: utf-8 -*-
"""Registro da 6a afericao (gerencia, em nome proprio; so acrescimo): VERBATIM por ENTRADA, com as disposicoes; a ERRATA AO LADO da disposicao do 4N6 da 5a (a
edicao do filtro do mata_um foi por python inline num heredoc, nao por script salvo; o diff c73f5623...); as duplicatas contadas pelo mesmo criterio em todas as
passadas (qualquer «= x» na disposicao); o texto do pre-registro acrescido da 6a. Backup de BYTES; temporario -> conferir -> substituir."""
import hashlib, json, os, re, sys, time
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
A6P = os.path.join(HERE, "afericao6_resultado.json"); A6 = json.load(open(A6P, encoding="utf-8"))
ENT = [(g["lente"], a) for g in A6["grupos"] for a in (g.get("itens") or [])]
NOV = A6["novos"]; V6 = {v["i"]: v for v in (A6.get("verificacao") or {}).get("veredictos", [])}
DIFF5 = os.path.join(HERE, "diff_lancador_afer5_com_edicao_manual.txt")
ACAO_IT = {
    "5N5": "o pre-registro diz agora: abortar e' kill -TERM no Git Bash (PID do MSYS), e o TaskStop da ferramenta da gerencia NAO para o lancador.",
    "4N5": "o comentario do ensaio diz W08/W08b sem a marca e o W08c com ela, os quatro conferidos por nome e executados a parte; a docstring cita a ausencia da frase da CPU no sucesso.",
    "4N6": "ERRATA AO LADO da disposicao 4N6 da 5a: as edicoes da 5a no lancador foram nove pares por aplicar_afer5_lancador.py, UMA edicao por python inline num heredoc (nao salva) no filtro do mata_um (ProcessId -ne $RW e Name python), e o aplicar_afer5_lancador_b.py, que corrigiu o escape; o diff do .bak_antes_afer5 ao estado auditado esta em diff_lancador_afer5_com_edicao_manual.txt (sha256 %s). Na 6a, todas as edicoes foram por scripts salvos." % h(DIFF5)[:16],
}
ACAO_NOV = {
    0: "result_file_absent pelo FATO (o resultado existia ou nao), nao pelo motivo.",
    1: "o _qp_retry tenta de novo SO PermissionError; a docstring diz isso.",
    2: "«nunca sobrevive» -> «nunca passa por desta rodada», com a trava dita (o arquivo fica, os erros vao ao registro, o selo grava NOT_THIS_RUN).",
    3: "a falha da gravacao do parcial do D128 deixa marca (partial_write_error) -- trabalhador 0c9ba7fd.",
    4: "MEDIO tratado: o mata_um e' fail-closed (o PID nativo do subshell do rito; senao os descendentes com a sentinela MATA_OK e a data de criacao; senao FALHA VISIVEL no log e em rito_v384_sinal.txt, onde tambem vai o RITO_RC=SINAL); testada so em leitura a consulta de reserva.",
    5: "o conferidor devolve toda linha AVISO/FALHA VISIVEL do log do lancador e diz «RELIGADO COM AVISO».",
    6: "a caminhada aceita o filho so se a data de criacao for >= a do pai; e o caminho principal e' o PID nativo do subshell do rito.",
    7: "o cabecalho e o pre-registro dizem: kill -TERM no Git Bash (PID do MSYS), nao no PowerShell; um .rito_v384.pid velho e' dito no log.",
    8: "MEDIO tratado: errata ao lado da disposicao 4N6 com o diff (ver 4N6).",
    9: "= 5.",
    10: "as duplicatas contadas pelo mesmo criterio em todas as passadas: qualquer «= x» na disposicao (a 5a da 8, nao 7).",
    11: "com o resumo falho, a frase da CPU nao afirma ausencia; sem registro, diz so «nao ha registro da comparacao»; a ausencia vem do codigo.",
    12: "a ausencia composta do CODIGO (CPUREF_JSON_ABSENT) em cada lingua; «did not check» -> «did not match» (e «nao bateu» no PT).",
    13: "MEDIO tratado: a causa (3) do desvio recalculada com TODAS as sondas validas (o plano B com margem por sonda, o prazo de inicio que ele exigiria, o fim, a dispersao), e a conclusao vem dos numeros.",
    14: "= 10.",
    15: "a guarda recusa negacao explicita; o rascunho diz que a guarda e' lexical e a conferencia final e' a leitura humana do verbatim.",
    16: "no congelamento, o V1 tem de ser igual ao rascunho apresentado fora dos campos volateis (id, titulo, gerado, ratificacao, evidencias, afericao), senao recusa.",
    17: "as sondas da variabilidade entram nas evidencias (copiadas no congelamento); criterio dito; ilegivel = falha visivel; as fora do criterio listadas com o motivo.",
    18: "a causa «veredito rederivado ausente ou diferente» entra na arvore.",
    19: "a copia ao Nos calcula o sha256 do temporario (com novas tentativas) ANTES da troca e so entao marca copied_to_out.",
    20: "= 0.",
    21: "= 5 (e o lancador reconfere a porta 30 s depois de um AVISO, so tirando o marcador se ela ainda escutar).",
    22: "= 8.",
    23: "= 10.",
    24: "= 12.",
    25: "= 17 (e a frase «a margem cobre a faixa» calculada: maior sonda / corrente por custo).",
}
c6 = Counter(a["estado"] for _, a in ENT)
falta = sorted({a["id"] for _, a in ENT if a["estado"] not in ("RESOLVIDO", "ACHADO_REFUTADO")} - set(ACAO_IT)); assert not falta, falta
assert set(ACAO_NOV) == set(range(len(NOV))), (len(NOV), sorted(set(range(len(NOV))) - set(ACAO_NOV)))
dupc = lambda d: sum(1 for v in d.values() if re.search(r"(^|: )= ", str(v)))
sob6 = sum(1 for i in range(len(NOV)) if not (V6.get(i) or {}).get("refutado"))
L = ["\n" + "=" * 80, "6a PASSADA -- conferencia das correcoes da 5a e verificacao dos seus achados novos (VERBATIM de afericao6_resultado.json, sha256 %s; POR ENTRADA) e DISPOSICOES (%s)" % (h(A6P), time.strftime("%d/%m/%Y %H:%M")), "=" * 80]
for l, a in ENT:
    L.append("\n%s [%s] ESTADO: %s" % (a["id"], l, a["estado"])); L.append("EVIDENCIA: " + a["evidencia"])
    if a.get("falta"):
        L.append("FALTA: " + a["falta"])
    if a["id"] in ACAO_IT and a["estado"] not in ("RESOLVIDO", "ACHADO_REFUTADO"):
        L.append("DISPOSICAO DA GERENCIA: " + ACAO_IT[a["id"]])
for i, a in enumerate(NOV):
    v = V6.get(i) or {}
    L.append("\n[6N%d] (%s/%s -> %s, severidade ajustada %s) %s" % (i, a["origem"], a["severidade"], "REFUTADO" if v.get("refutado") else "SOBREVIVE", v.get("severidade_ajustada"), a["arquivo_linha"]))
    L.append("AFIRMACAO: " + a["afirmacao"]); L.append("EVIDENCIA: " + a["evidencia"]); L.append("CORRECAO PEDIDA: " + a["correcao"])
    L.append("VERIFICADOR: " + v.get("razao", "")); L.append("DISPOSICAO DA GERENCIA: " + ACAO_NOV[i])
L.append("\nO QUE CADA LENTE EXAMINOU (6a passada, verbatim):")
for g in A6["grupos"]:
    for x in g.get("examinado") or []:
        L.append("- [%s] %s" % (g["lente"], x))
p = os.path.join(HERE, "AFERIDOR_v384.txt"); raw = open(p, "rb").read()
if b"6a PASSADA -- conferencia das correcoes da 5a" in raw:
    print("a 6a ja esta gravada")
else:
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    novo = raw + ("\n".join(L) + "\n").encode("utf-8"); open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw); os.replace(p + ".tmp", p)
    assert open(p, "rb").read()[:len(raw)] == raw; print("AFERIDOR_v384.txt:", len(raw), "->", len(novo))
dp = os.path.join(HERE, "disposicoes_afericoes_v384.json"); D = json.load(open(dp, encoding="utf-8"))
open(dp + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "wb").write(open(dp, "rb").read())
d4 = dupc(D["disposicoes_4a_novos"]); d5 = dupc(D["disposicoes_5a_novos"]); d6 = dupc({str(k): v for k, v in ACAO_NOV.items()})
t = D["texto_para_o_pre_registro"]
t = re.sub(r"(\d+) achados novos, (\d+) sobreviventes à verificação \((\d+) deles duplicatas de outros; quase todos de severidade baixa\)",
           lambda m: "%s achados novos, %s sobreviventes à verificação (%d deles repetem outro achado ou item; quase todos de severidade baixa)" % (m.group(1), m.group(2), d4), t, count=1)
t = re.sub(r"(\d+) achados novos \((\d+) deles duplicatas de outros\), SEM a verificação adversarial",
           lambda m: "%s achados novos (%d deles repetem outro achado ou item), SEM a verificação adversarial na própria passada" % (m.group(1), d5), t, count=1)
t = t.split("; 6ª passada")[0]
t += ("; 6ª passada (conferência das correções da 5ª e verificação dos seus achados novos): %d entradas — %d resolvidas e %d parciais; %d achados novos, %d sobreviventes à "
      "verificação (%d deles repetem outro achado ou item; quatro de severidade média), tratados no código ou no texto antes deste documento; e uma ERRATA da gerência ao lado: "
      "uma edição da 5ª no lançador foi feita por um script não salvo, com o diff registrado") % (len(ENT), c6.get("RESOLVIDO", 0), c6.get("PARCIAL", 0), len(NOV), sob6, d6)
D["texto_para_o_pre_registro"] = t
D["passada6"] = {"arquivo": os.path.basename(A6P), "sha256": h(A6P), "entradas": dict(c6), "n_entradas": len(ENT), "novos": len(NOV), "sobreviventes": sob6, "repetem_outro": d6,
                 "criterio_das_repeticoes": "qualquer «= x» na disposicao (o mesmo nas passadas 4, 5 e 6)", "diff_lancador_afer5": {"arquivo": os.path.basename(DIFF5), "sha256": h(DIFF5)}}
D["passada4"]["repetem_outro"] = d4; D["passada5"]["duplicatas_entre_os_novos"] = d5
D["errata_4N6_da_5a"] = ACAO_IT["4N6"]
D["disposicoes_6a_itens"] = ACAO_IT; D["disposicoes_6a_novos"] = {str(k): v for k, v in ACAO_NOV.items()}
b = json.dumps(D, ensure_ascii=False, indent=1).encode("utf-8"); open(dp + ".tmp", "wb").write(b); os.replace(dp + ".tmp", dp)
print("disposicoes:", hashlib.sha256(b).hexdigest()[:16], "| 6a:", dict(c6), "novos", len(NOV), "sob", sob6, "| repeticoes 4a/5a/6a:", d4, d5, d6)
print(t[-900:])
