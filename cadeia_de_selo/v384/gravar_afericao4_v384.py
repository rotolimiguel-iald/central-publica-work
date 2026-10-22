# -*- coding: utf-8 -*-
"""Registro da 4a afericao (gerencia, em nome proprio; AO LADO, so acrescimo): acrescenta ao AFERIDOR_v384.txt a 4a passada VERBATIM (afericao4_resultado.json)
com a disposicao de cada item nao resolvido e de cada achado novo, e atualiza disposicoes_afericoes_v384.json (passada4, disposicoes_4a e o texto do pre-registro).
Backup de BYTES antes; temporario -> conferir -> substituir."""
import hashlib, json, os, sys, time
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
A4P = os.path.join(HERE, "afericao4_resultado.json"); A4 = json.load(open(A4P, encoding="utf-8"))
IT = {a["id"]: (g["lente"], a) for g in A4["grupos"] for a in (g.get("itens") or [])}
V4 = {v["i"]: v for v in (A4.get("verificacao") or {}).get("veredictos", [])}
NOV = A4["novos"]
ACAO_IT = {
    "#6": "o modo zero do D128 conta INDEPENDENTE de ran (zero_mode_ok is False basta): uma queda depois do espectro nao apaga a violacao. NO_ZERO_EIGENVALUE nao criado (a violacao anula com a causa).",
    "#36": "(1) o pre-registro e a memoria da v384 dizem que a custodia leva a pasta da rodada (Nos/quantum_pillar/run_<...>/), e o handoff da v384 o repetira; (2) o conferidor da versao final confere details_sha256 e cpuref_sha256 contra os arquivos do run_dir; (3) o pre-registro diz que, numa rodada reaproveitada, o run_dir aponta para o cache que a rodada completa seguinte substitui, e que o selo de uma intermediaria nao vai a custodia.",
    "N8": "a volta do cache antigo tem o erro registrado: RuntimeError com o erro da troca E o da volta (e onde o antigo ficou).",
    "#9": "(1) antes do Start-ScheduledTask, espera ate 60 s que nenhum stop_iald_llama.ps1 esteja vivo; (2) religar ignora TERM/HUP/INT; (3) a memoria da v384 manda a gerencia conferir o marcador se nao houver rodada seguinte; (4) o marcador grava e a leitura respeita restaurar=0|1.",
    "#14": "tarefa DESABILITADA com o servidor a restaurar -> recusa (codigo 15) antes de parar; o conferidor le o log do lancador e diz, como informacao, se o servidor foi religado, se nao estava ligado ou se a porta nao escutou.",
    "N3": "REGRESSAO tratada: RITO_INICIADO marca a fase; um sinal antes do rito so restaura (nao chama mata_um nem toca o stdout da tentativa anterior); durante, encerra a arvore do um.py e grava RITO_RC=SINAL_<x>.",
    "N18": "REGRESSAO tratada: os enunciados com _computacao saem de comeca/contem; o bloco inteiro da custodia de sentido e' extraido do candidato e executado a parte (pilar nao concluido e concluido), conferindo o balde e a linha impressa (testado contra o candidato de ensaio).",
    "N19": "o bloco da custodia executado a parte (N18); variantes novas: d128_rodado e sem_cache_d128, com as frases no DEVE.",
    "N25": "a selecao corrigida (N18); o ensaio roda sobre o candidato FINAL depois da ratificacao e da fumaca, antes do gerar_esperados (a ordem da cadeia).",
    "N15": "a frase das janelas sem o parentese: «em X das Y configuracoes ha ao menos um ponto de atrator unico ...» (PT/EN).",
    "N24": "com summary_error, a contagem do motor diz «nao resumido nesta rodada (ver acima)». «Foi calculado» mantido: o veredito de sucesso diz que foi; a frase do erro do resumo explica a falta dos numeros.",
    "N14": "a linha da Execucao rotula o volume do ESTRESSE e soma, em n = 4096, as chamadas das sondas de tempo deste trabalhador (lidas).",
    "N16": "REGRESSAO tratada: «a construcao foi conferida por LEITURA, contra as fontes fixadas por sha256, na 1a afericao; nem o E1..E8 nem a CPU a conferem».",
}
ACAO_NOV = {
    0: "se o marcador falhar, o arquivo do pilar no Nos e' REMOVIDO (o selo registra a ausencia); se a copia do resultado falhar, CUSTODY_CHAIN_INCOMPLETE, all_verified False e nada ao cache; o registro do selo leva copied_to_out, copy_to_out_error, out_marker_error e out_file_removed.",
    1: "as docstrings do trabalhador dizem E1..E8 (o E8, o comparador da CPU) e o modo zero na lista do identity_check.",
    2: "not_comparable so com meta_ok, child_rc == 0 e nenhuma linha da GPU faltando; o E8 ganhou o caso «perto do limiar + marca errada -> nao e' NOT_COMPARABLE».",
    3: "a leitura do marcador respeita restaurar=0|1 (com 0, registra e remove); a mensagem do codigo 13 diz a ORIGEM do «ligado».",
    4: "REFUTADO pelo verificador; ainda assim o cabecalho e o pre-registro dizem: INT/HUP so com o lancador em PRIMEIRO PLANO, e ele roda em primeiro plano.",
    5: "= N18.",
    6: "a lacuna fechada: o estado do conferidor auditado na 3a (sha256 fe466024...) foi reconstituido byte a byte (pela reconstituicao do verificador da 4a) e guardado como conferir_rito_v384.py.bak_antes_afer3_RECONSTITUIDO; antes das correcoes da 4a, backup de bytes de TODOS os arquivos do pacote (.bak_antes_afer4).",
    7: "o rotulo do motor no pre-registro e' lido da contagem (E1..E<n>); a chave virou autoteste_do_motor, com o arquivo e o sha256 do resultado.",
    8: "sem ruido abaixo de 100%: a fracao por dimensao com k de n (PT/EN).",
    9: "o artigo separa o hash da ESPECIFICACAO do hash do DOCUMENTO (JSON e MD).",
    10: "_tx4 so ASCII.",
    11: "= #6.",
    12: "= 2.",
    13: "= 7.",
    14: "a frase do plano B sem margem e' comparada por script com o prazo de inicio DESTA especificacao (acima/abaixo; com/sem margem).",
    15: "«n(c2) so como INFORMACAO, relatado em max_diffs (n(c3) a CPU nem calcula)».",
    16: "a alternativa renomeada B_AMPLIADO_D64 (o «A» de 03/10 era o nivel LEVE); a ratificacao exige que a mensagem do operador NOMEIE a escolha («b reduzido» ou «b ampliado»).",
    17: "as evidencias por caminho completo e sha256 no pre-registro; no congelamento, copiadas byte a byte para evidencias_PREREGISTRO_V1/ na pasta permanente; o autoteste e o AFERIDOR citados com sha256.",
    18: "a arvore diz as tres condicoes do PARCIAL/CUSTODY (codigo e especificacao conferidos e veredito rederivado; o primeiro parcial so depois do T3; CUSTODY so fora de RESULTS_VOID/NOT_RUN) e a cadeia que nao fecha quando o resultado nao chega ao Nos.",
    19: "«em cerca de metade delas (sorteio por instancia, p = 1/2; o numero de rotacionadas e' relatado)».",
    20: "= N3.",
    21: "= 2.",
    22: "o ramo morto do _cpu4 removido; nos vereditos RESULTS_VOID com CPU_REFERENCE_ o artigo diz a situacao da referencia (lidos, comparados, perto do limiar, discordancias, marca, codigo do filho).",
    23: "= #6.",
    24: "= 7 (e as docstrings do trabalhador, no 1).",
    25: "= 6.",
}
c4 = Counter(a["estado"] for _, a in IT.values())
falta = [k for k, (_, a) in IT.items() if a["estado"] != "RESOLVIDO" and k not in ACAO_IT]
assert not falta, falta
assert set(ACAO_NOV) == set(range(len(NOV))), (len(NOV), sorted(set(range(len(NOV))) - set(ACAO_NOV)))
sob4 = sum(1 for i in range(len(NOV)) if not (V4.get(i) or {}).get("refutado"))
L = ["\n" + "=" * 80, "4a PASSADA -- conferencia das correcoes da 3a (VERBATIM de afericao4_resultado.json, sha256 %s) e DISPOSICOES (gravadas em %s)" % (h(A4P), time.strftime("%d/%m/%Y %H:%M")), "=" * 80]
for k, (lente, a) in IT.items():
    L.append("\n%s [%s] ESTADO: %s" % (k, lente, a["estado"]))
    L.append("EVIDENCIA: " + a["evidencia"])
    if a.get("falta"):
        L.append("FALTA: " + a["falta"])
    if k in ACAO_IT:
        L.append("DISPOSICAO DA GERENCIA: " + ACAO_IT[k])
for i, a in enumerate(NOV):
    v = V4.get(i) or {}
    L.append("\n[4N%d] (%s/%s -> %s, severidade ajustada %s) %s" % (i, a["origem"], a["severidade"], "REFUTADO" if v.get("refutado") else "SOBREVIVE", v.get("severidade_ajustada"), a["arquivo_linha"]))
    L.append("AFIRMACAO: " + a["afirmacao"]); L.append("EVIDENCIA: " + a["evidencia"]); L.append("CORRECAO PEDIDA: " + a["correcao"])
    L.append("VERIFICADOR: " + v.get("razao", "")); L.append("DISPOSICAO DA GERENCIA: " + ACAO_NOV[i])
L.append("\nO QUE CADA LENTE EXAMINOU (4a passada, verbatim):")
for g in A4["grupos"]:
    for x in g.get("examinado") or []:
        L.append("- [%s] %s" % (g["lente"], x))
bloco = ("\n".join(L) + "\n").encode("utf-8")
p = os.path.join(HERE, "AFERIDOR_v384.txt"); raw = open(p, "rb").read()
if b"4a PASSADA -- conferencia das correcoes da 3a" in raw:
    print("a 4a passada ja esta gravada no AFERIDOR")
else:
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    novo = raw + bloco; open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw); os.replace(p + ".tmp", p)
    assert open(p, "rb").read()[:len(raw)] == raw
    print("AFERIDOR_v384.txt:", len(raw), "->", len(novo), "; backup", os.path.basename(bak))
dp = os.path.join(HERE, "disposicoes_afericoes_v384.json"); D = json.load(open(dp, encoding="utf-8"))
bakd = dp + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bakd, "wb").write(open(dp, "rb").read())
D["passada4"] = {"arquivo": os.path.basename(A4P), "sha256": h(A4P), "itens_da_3a": dict(c4), "novos": len(NOV), "sobreviventes": sob4}
D["disposicoes_4a_itens"] = ACAO_IT; D["disposicoes_4a_novos"] = {str(k): v for k, v in ACAO_NOV.items()}
base = D["texto_para_o_pre_registro"].split("; 4ª passada")[0]
D["texto_para_o_pre_registro"] = base + ("; 4ª passada (conferência das correções da 3ª): dos itens da 3ª, %d resolvidos, %d parciais e %d regressões; %d achados novos, %d sobreviventes à verificação "
                                         "(quase todos de severidade baixa); tratados no código ou no texto antes deste documento") % (c4.get("RESOLVIDO", 0), c4.get("PARCIAL", 0), c4.get("REGRESSAO", 0), len(NOV), sob4)
b = json.dumps(D, ensure_ascii=False, indent=1).encode("utf-8"); open(dp + ".tmp", "wb").write(b); os.replace(dp + ".tmp", dp)
print("disposicoes atualizadas:", hashlib.sha256(b).hexdigest()[:16]); print(D["texto_para_o_pre_registro"])
