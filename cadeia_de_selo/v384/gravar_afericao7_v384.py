# -*- coding: utf-8 -*-
"""Registro da 7a afericao (gerencia, em nome proprio; so acrescimo): VERBATIM por entrada, com as disposicoes; ERRATAS AO LADO: (1) a edicao inline do filtro do
mata_um na 5a fez QUATRO trocas (nao duas); (2) na 6a, uma gravacao das disposicoes (a contagem «lidos dos veredictos» e severidades_ajustadas) foi por python
inline nao salvo -- o diff registrado; (3) o criterio das repeticoes descrito como implementado (regex «(^|: )= ») e a disposicao 6N8 contada como repeticao do
item 4N6. Evidencias novas: o teste so de leitura do mata_um e o TESTE DO CONGELAMENTO (cinco casos). Backup de BYTES; temporario -> conferir -> substituir."""
import hashlib, json, os, re, sys, time
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
A7P = os.path.join(HERE, "afericao7_resultado.json"); A7 = json.load(open(A7P, encoding="utf-8"))
ENT = [(g["lente"], a) for g in A7["grupos"] for a in (g.get("itens") or [])]
NOV = A7["novos"]; V7 = {v["i"]: v for v in (A7.get("verificacao") or {}).get("veredictos", [])}
F = {k: os.path.join(HERE, k) for k in ("diff_disposicoes_afer6_edicao_inline.txt", "teste_mata_um_leitura.sh", "teste_mata_um_leitura.out", "teste_congelamento_v384.py", "teste_congelamento_v384.json")}
TC = json.load(open(F["teste_congelamento_v384.json"], encoding="utf-8"))
ACAO_IT = {
    "6N0": "result_file_absent MEDIDO no proprio marcador, no disco (run_dir, ou cache_dir na rodada reaproveitada; result.json ou result_partial.json); null quando nao ha pasta.",
    "6N20": "= 6N0.",
    "6N3": "o item 7 da arvore ressalva: salvo falha da propria gravacao do parcial, registrada em partial_write_error no result.json so se o D128 retornar (o trabalhador nao muda nesta rodada).",
    "6N7": "um .rito_v384.pid de lancador VIVO (kill -0 e /proc/<pid>/cmdline com rito_v384) faz recusar (codigo 16) antes de qualquer parada; o velho e' dito como AVISO.",
    "6N21": "com o vigia morto por prazo, o marcador so sai se nenhuma parada da tarefa (Stop-ScheduledTask) estiver em curso, alem da porta reconferida.",
    "6N13": "a conclusao do desvio condicionada a escolha (B_AMPLIADO_D64: o T1 de d = 64 reduzido) e a folga contra a dispersao CALCULADA.",
    "6N15": "o rascunho diz exatamente o que a guarda recusa («nao» imediatamente antes de ratifico/concordo/aprovo/autorizo).",
    "6N16": "REGRESSAO tratada (ALTO): a comparacao V1 x rascunho sobre as formas CANONICAS dos dois lados; e o caminho do congelamento TESTADO numa pasta de teste com transcrito sintetico: %s." % "; ".join("%s %s" % (k, "PASSOU" if v["passou"] else "FALHOU") for k, v in TC.items()),
    "6N25": "o texto declara o criterio das sondas, as fora do criterio com o motivo e a dispersao maior/menor, e diz se a margem a cobre.",
}
ACAO_NOV = {
    0: "o marcador devolve o sha256 dos BYTES escritos, sem reler o Nos depois da troca.",
    1: "o item 7 da arvore diz que a marca so chega ao result.json se o D128 retornar (o trabalhador nao muda nesta rodada).",
    2: "o conferidor classifica «escutou e PAROU» antes de «nao escutou».",
    3: "= 6N7.",
    4: "o log e o rito_v384_sinal.txt GIRAM (.anterior) no comeco de cada rodada, depois das guardas; o conferidor le o rito_v384_sinal.txt.",
    5: "ERRATA AO LADO: a edicao inline da 5a no filtro do mata_um fez QUATRO trocas: ProcessId -ne $RW, Name python, a regex ancorada e a retirada do teste de CommandLine nao nulo (o diff c73f5623... ja estava completo).",
    6: "o teste so de leitura do mata_um guardado: teste_mata_um_leitura.sh (sha256 %s) e a saida .out (%s)." % (h(F["teste_mata_um_leitura.sh"])[:16], h(F["teste_mata_um_leitura.out"])[:16]),
    7: "a lista do que o sucesso nao pode ter ganhou a forma nova («Nao ha registro...») e «A comparacao com a CPU»; e uma variante nova (resumo falho + NOT_COMPARABLE) confere a ausencia.",
    8: "a ausencia so com o codigo CPUREF_JSON_ABSENT; outro erro: «a comparacao com a CPU falhou (<erro>)» / «the CPU comparison failed (<error>)».",
    9: "ALTO tratado: = 6N16 (formas canonicas; o congelamento testado).",
    10: "MEDIO tratado: as evidencias so sao copiadas depois de TODAS as guardas, por pasta temporaria renomeada (apagada se a copia falhar); testado: as recusas nao deixam pasta nem temporario.",
    11: "a sonda corrente identificada por sha256, com assert de exatamente uma.",
    12: "ERRATA AO LADO: na 6a, uma gravacao das disposicoes (passada6.severidades_ajustadas e «, lidos dos veredictos») foi por python inline NAO salvo; o diff do .bak_20261004_064923 ao estado gravado esta em diff_disposicoes_afer6_edicao_inline.txt (sha256 %s); a contagem em si estava certa (4 MEDIO, lida dos veredictos)." % h(F["diff_disposicoes_afer6_edicao_inline.txt"])[:16],
    13: "a disposicao 6N8 repete o item 4N6 (contada assim, as repeticoes da 6a sao 9); o criterio descrito como implementado: «= x» no comeco da disposicao ou depois de «: ».",
    14: "= 9.",
    15: "= 10.",
    16: "= 2, e os AVISOs do conferidor so das linhas do log() do lancador (HH:MM:SS), fora a saida do stop_iald_llama.ps1.",
    17: "= 6N0.",
    18: "= 1.",
    19: "= 7.",
    20: "= 12.",
    21: "= 4 e = 6N7.",
}
c7 = Counter(a["estado"] for _, a in ENT)
falta = sorted({a["id"] for _, a in ENT if a["estado"] != "RESOLVIDO"} - set(ACAO_IT)); assert not falta, falta
assert set(ACAO_NOV) == set(range(len(NOV))), (len(NOV), sorted(set(range(len(NOV))) - set(ACAO_NOV)))
dupc = lambda d: sum(1 for v in d.values() if re.search(r"(^|: )= ", str(v)))
sev7 = Counter(v["severidade_ajustada"] for v in V7.values() if not v["refutado"])
sob7 = sum(1 for i in range(len(NOV)) if not (V7.get(i) or {}).get("refutado"))
L = ["\n" + "=" * 80, "7a PASSADA -- as correcoes da 6a (VERBATIM de afericao7_resultado.json, sha256 %s; POR ENTRADA) e DISPOSICOES (%s)" % (h(A7P), time.strftime("%d/%m/%Y %H:%M")), "=" * 80]
for l, a in ENT:
    L.append("\n%s [%s] ESTADO: %s" % (a["id"], l, a["estado"])); L.append("EVIDENCIA: " + a["evidencia"])
    if a.get("falta"):
        L.append("FALTA: " + a["falta"])
    if a["estado"] != "RESOLVIDO":
        L.append("DISPOSICAO DA GERENCIA: " + ACAO_IT[a["id"]])
for i, a in enumerate(NOV):
    v = V7.get(i) or {}
    L.append("\n[7N%d] (%s/%s -> %s, severidade ajustada %s) %s" % (i, a["origem"], a["severidade"], "REFUTADO" if v.get("refutado") else "SOBREVIVE", v.get("severidade_ajustada"), a["arquivo_linha"]))
    L.append("AFIRMACAO: " + a["afirmacao"]); L.append("EVIDENCIA: " + a["evidencia"]); L.append("CORRECAO PEDIDA: " + a["correcao"])
    L.append("VERIFICADOR: " + v.get("razao", "")); L.append("DISPOSICAO DA GERENCIA: " + ACAO_NOV[i])
L.append("\nEVIDENCIAS NOVAS DA GERENCIA NESTA RODADA (sha256): " + "; ".join("%s %s" % (k, h(p)[:16]) for k, p in F.items()))
L.append("\nO QUE CADA LENTE EXAMINOU (7a passada, verbatim):")
for g in A7["grupos"]:
    for x in g.get("examinado") or []:
        L.append("- [%s] %s" % (g["lente"], x))
p = os.path.join(HERE, "AFERIDOR_v384.txt"); raw = open(p, "rb").read()
if b"7a PASSADA -- as correcoes da 6a" in raw:
    print("a 7a ja esta gravada")
else:
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    novo = raw + ("\n".join(L) + "\n").encode("utf-8"); open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw); os.replace(p + ".tmp", p)
    assert open(p, "rb").read()[:len(raw)] == raw; print("AFERIDOR_v384.txt:", len(raw), "->", len(novo))
dp = os.path.join(HERE, "disposicoes_afericoes_v384.json"); D = json.load(open(dp, encoding="utf-8"))
open(dp + ".bak_" + time.strftime("%Y%m%d_%H%M%S"), "wb").write(open(dp, "rb").read())
D["disposicoes_6a_novos"]["8"] = "= 4N6 (" + D["disposicoes_6a_novos"]["8"] + ")"   # a repeticao explicita (7a afericao, 7N13); o texto antigo segue dentro
d6 = dupc(D["disposicoes_6a_novos"])
D["passada6"]["repetem_outro_corrigido_na_7a"] = d6
D["passada6"]["criterio_das_repeticoes"] = "«= x» no comeco da disposicao ou depois de «: » (regex (^|: )= ), o mesmo nas passadas 4 a 7 -- descrito como implementado (7a afericao)"
t = D["texto_para_o_pre_registro"]
t = re.sub(r"26 achados novos, 26 sobreviventes à verificação \((\d+) deles repetem outro achado ou item;", "26 achados novos, 26 sobreviventes à verificação (%d deles repetem outro achado ou item, contagem corrigida na 7ª;" % d6, t, count=1)
t = t.split("; 7ª passada")[0]
t += ("; 7ª passada (as correções da 6ª): %d entradas — %d resolvidas, %d parciais e %d regressão (a comparação do V1 com o rascunho, que recusava todo congelamento); "
      "%d achados novos, %d sobreviventes à verificação (%d repetem outro achado ou item; severidades: %s), tratados no código ou no texto antes deste documento; o caminho do "
      "congelamento foi TESTADO numa pasta de teste com transcrito sintético (%d de %d casos como esperado); e duas ERRATAS da gerência ao lado (a edição manual da 5ª tinha "
      "quatro trocas; uma gravação das disposições na 6ª foi por script não salvo, com o diff registrado)") % (
    len(ENT), c7.get("RESOLVIDO", 0), c7.get("PARCIAL", 0), c7.get("REGRESSAO", 0), len(NOV), sob7, dupc({str(k): v for k, v in ACAO_NOV.items()}),
    ", ".join("%s %d" % (k, v) for k, v in sorted(sev7.items())), sum(1 for v in TC.values() if v["passou"]), len(TC))
D["texto_para_o_pre_registro"] = t
D["passada7"] = {"arquivo": os.path.basename(A7P), "sha256": h(A7P), "entradas": dict(c7), "n_entradas": len(ENT), "novos": len(NOV), "sobreviventes": sob7,
                 "severidades_ajustadas": dict(sev7), "repetem_outro": dupc({str(k): v for k, v in ACAO_NOV.items()}),
                 "evidencias_novas": {k: h(p_) for k, p_ in F.items()}, "teste_congelamento": {k: v["passou"] for k, v in TC.items()}}
D["disposicoes_7a_itens"] = ACAO_IT; D["disposicoes_7a_novos"] = {str(k): v for k, v in ACAO_NOV.items()}
b = json.dumps(D, ensure_ascii=False, indent=1).encode("utf-8"); open(dp + ".tmp", "wb").write(b); os.replace(dp + ".tmp", dp)
print("disposicoes:", hashlib.sha256(b).hexdigest()[:16], "| 7a:", dict(c7), "novos", len(NOV), "sob", sob7, "sev", dict(sev7), "| 6a repeticoes corrigidas:", d6)
print(t[-700:])
