# -*- coding: utf-8 -*-
"""Registro da 8a afericao (gerencia, em nome proprio; so acrescimo): VERBATIM por entrada, com as disposicoes. AO LADO: (1) passada6.criterio_das_repeticoes
RESTAURADO ao texto original e o da 7a gravado ao lado (8N17); (2) passada7_errata_da_8a: a primeira execucao do teste da 7a falhou (260 caracteres), o nome das
copias mudou, o aplicar_afer7_gerador_prereg_b.py com o seu sha256; «transcrito sintetico» le-se «copia do transcrito real com mensagem sintetica» (8N2/8N18);
(3) a evidencia da 6a regerada dos bytes (8N10). As edicoes desta rodada feitas pela ferramenta Edit (nao por script) ficam com o diff gerado AQUI.
Backup de BYTES conferido; temporario -> tamanho -> substituir -> conferir (8N12: o que a gravacao da 7a prometia e nao fazia nas disposicoes)."""
import glob, hashlib, json, os, re, subprocess, sys, time
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
A8P = os.path.join(HERE, "afericao8_resultado.json"); A8 = json.load(open(A8P, encoding="utf-8"))
ENT = [(g["lente"], a) for g in A8["grupos"] for a in (g.get("itens") or [])]
NOV = A8["novos"]; V8 = {v["i"]: v for v in (A8.get("verificacao") or {}).get("veredictos", [])}
GEN = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")


def gravar(p, novo, conferir_prefixo=None):
    raw = open(p, "rb").read()
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw, "backup nao confere"
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo), "temporario com tamanho errado"
    os.replace(p + ".tmp", p); assert open(p, "rb").read() == novo, "o gravado nao confere"
    if conferir_prefixo is not None:
        assert novo[:len(conferir_prefixo)] == conferir_prefixo
    return bak


# as edicoes feitas pela ferramenta Edit nesta rodada: o diff (de todo o arquivo contra o .bak_antes_afer8) gerado aqui, saida em bytes
_dd = []
for f in ("gerar_candidato_v384.py", "teste_congelamento_v384.py"):
    r = subprocess.run(["diff", "-u", f + ".bak_antes_afer8", f], cwd=HERE, capture_output=True); assert r.returncode == 1, (f, r.returncode)
    _dd.append(r.stdout)
DIFF_EDIT = os.path.join(HERE, "diff_afer8_edicoes_pela_ferramenta_Edit.txt")
_db = b"".join(_dd); open(DIFF_EDIT + ".tmp", "wb").write(_db); assert os.path.getsize(DIFF_EDIT + ".tmp") == len(_db); os.replace(DIFF_EDIT + ".tmp", DIFF_EDIT)
F = {k: os.path.join(HERE, k) for k in ("diff_disposicoes_afer6_edicao_inline_BYTES.txt", "diff_disposicoes_afer6_edicao_inline_BYTES.txt.json", "regerar_diff_disposicoes_afer6.py",
                                         "teste_mata_um_forma_do_rito.sh", "teste_mata_um_forma_do_rito.out", "teste_congelamento_v384.py", "teste_congelamento_v384.json",
                                         "aplicar_afer7_gerador_prereg_b.py", "aplicar_afer8_runtime.py", "aplicar_afer8_lancador_conferidor.py", "aplicar_afer8_gerador_prereg.py",
                                         "aplicar_afer8_gerador_prereg_b.py", "aplicar_afer8_guardas_transcrito.py", "diff_afer8_edicoes_pela_ferramenta_Edit.txt")}
F["gerador_do_pre_registro"] = GEN
TC = json.load(open(F["teste_congelamento_v384.json"], encoding="utf-8"))
MO = open(F["teste_mata_um_forma_do_rito.out"], encoding="utf-8", errors="replace").read()
assert "(A) PASSOU" in MO and "(B) PASSOU" in MO, "o teste do mata_um na forma do rito nao passou"
DJ = json.load(open(F["diff_disposicoes_afer6_edicao_inline_BYTES.txt.json"], encoding="utf-8"))
# 6N25: a dispersao por d e por custo, recalculada AQUI das sondas (o mesmo criterio do gerador: teste_tempo_v*, d = 64 com reps >= 3)
_S = {}
for tp in sorted(glob.glob(os.path.join(HERE, "teste_tempo*", "result.json"))):
    nm = os.path.basename(os.path.dirname(tp)); tj = json.load(open(tp, encoding="utf-8"))
    if re.match(r"^teste_tempo_v\d+$", nm) and int((((tj.get("timing") or {}).get("64") or {}).get("reps")) or 0) >= 3:
        _S[nm] = tj["timing"]
_mm = []
for d in ("8", "16", "32", "64"):
    for ck, nk in (("pipeline_s", "instancia"), ("t1_injection_sigma0_s", "injecao do T1"), ("t1_extra_noise_level_s", "ruido do T1")):
        v = [t[d][ck] for t in _S.values() if d in t]
        if max(v) / min(v) > 1.25:
            _mm.append("d = %s %s (%.3f)" % (d, nk, max(v) / min(v)))
ACAO_IT = {
    "6N25": ("a dispersao das sondas calculada POR d E POR CUSTO (maior/corrente e maior/menor; instancia, injecao e ruido do T1) e o texto gerado dos numeros: a "
             "margem x1,25 NAO cobre a dispersao maior/menor em %s (%d sondas); a sonda corrente e' a mais lenta em d = 32 e 64, e a maior/corrente fica abaixo da "
             "margem em todo d e custo (o texto do rascunho diz os dois)." % (", ".join(_mm), len(_S))),
    "6N7": ("o cabecalho do lancador e o texto do pre-registro mandam conferir /proc/$(cat .rito_v384.pid)/cmdline (contem rito_v384) antes de abortar; e a janela "
            "da fase 0 fechada (= 8N6)."),
    "7N21": ("= 8N6: o .rito_v384.pid gravado logo depois da guarda, com trap proprio que o remove em qualquer saida antecipada; o religar (que tambem o remove) "
             "o substitui quando a restauracao e' armada."),
}
_ntc = len(TC); _ptc = sum(1 for v in TC.values() if v["passou"])
ACAO_NOV = {
    0: ("o MD primeiro e o JSON (a autoridade) por ultimo, cada um temporario -> tamanho -> substituir, com novas tentativas (40 x 0,25 s) e conferencia dos bytes, "
        "o temporario apagado se falhar; um MD sem o JSON (tentativa interrompida) vai para o lado (.incompleto_<data>), nunca apagado; a pasta de evidencias que ja "
        "existe tem de ter EXATAMENTE os mesmos arquivos (listdir igual); a mensagem «gere um V1.x» (o gerador so grava V1) trocada: versao nova e' ato da gerencia "
        "com gerador novo."),
    1: ("a guarda tambem por os.path.samefile; o V1 registra o transcrito lido (caminho, de_teste, o sha256 das LINHAS brutas da mensagem -- a linha nao muda "
        "quando o transcrito cresce -- e o tamanho na leitura); o gerar_candidato nao-ensaio, a fumaca, o gerar_esperados e o instalar RECUSAM de_teste diferente "
        "de false, e o gerar_candidato recusa caminho diferente do transcrito canonico; testado: os casos F (grafia 8.3 e prefixo longo) recusam na guarda sem "
        "tocar a pasta permanente."),
    2: ("corrigido AO LADO no texto do pre-registro (errata no trecho da 8a) e na docstring do teste; o caso da sonda acrescentado (C2: sonda SINTETICA do mesmo "
        "trabalhador, numa copia minima do pacote -> RECUSADO pelo orcamento); o teste tem agora %d casos, %d como esperado." % (_ntc, _ptc)),
    3: "removido o parametro morto result_present (e o st[\"_qp_result_present\"]); o fato e' medido so no marcador.",
    4: "o st[\"run_dir\"] gravado logo depois do makedirs, antes do Popen: no LAUNCH_FAILED o marcador mede a pasta.",
    5: "o conferidor classifica a parte «ha parada da tarefa ainda em curso» (ESCUTA, MAS HAVIA PARADA DA TAREFA EM CURSO), antes do «AVISO: a porta 8081».",
    6: "= 7N21 (o PID logo depois da guarda).",
    7: ("o log da tentativa vai para .fase0 e so gira (o log real e o registro dos sinais para .anterior) depois da ULTIMA recusa (exit 11), antes do vigia; uma "
        "tentativa recusada em qualquer ponto nao tira do lugar o registro da anterior; o registro dos sinais so recebe linha com o rito iniciado ou no mata_um, "
        "ambos depois do giro."),
    8: "a reconferencia de 30 s conta tambem o stop_iald_llama.ps1 (a mesma consulta da espera de 60 s).",
    9: ("o cabecalho do lancador e o texto do pre-registro (gerador -> MD) dizem o codigo 16, o PID logo depois da guarda, a conferencia da cmdline antes de "
        "abortar, o giro so depois da ultima recusa e o marcador que fica com parada em curso."),
    10: ("o diff REGERADO por script salvo (regerar_diff_disposicoes_afer6.py) a partir dos bytes: diff_disposicoes_afer6_edicao_inline_BYTES.txt, sha256 %s (o "
         "previsto pelo aferidor, 4bc5424c...); o antigo (%s...) fica como registro: decodificado em cp1252 e normalizado para LF, %s com o regerado." % (
             DJ["sha256"][:16], DJ["antigo_transcodificado_fica_como_registro"]["sha256"][:16],
             "confere" if DJ["o_antigo_decodificado_em_cp1252_e_normalizado_para_LF_confere_com_o_regerado"] else "NAO confere")),
    11: ("o teste na FORMA DO RITO, ( echo 1 | python um.py > f 2>&1 ) &: teste_mata_um_forma_do_rito.sh (%s) e .out (%s); o W e' o sh.exe pai do python; (A) o "
         "caminho principal (taskkill /T no W) encerrou a arvore e o python; (B) a reserva achou o python e o encerrou; os dois PASSARAM. O teste so de leitura "
         "da 7a fica como registro, com a ressalva dita aqui: la o caminho (1) lia o proprio python." % (h(F["teste_mata_um_forma_do_rito.sh"])[:16], h(F["teste_mata_um_forma_do_rito.out"])[:16])),
    12: ("esta gravacao confere os bytes do backup e o tamanho do temporario antes de cada substituicao (AFERIDOR e disposicoes), e os bytes depois; a gravacao da "
         "7a fica como foi -- o docstring dela prometia nas disposicoes a conferencia que so fazia no AFERIDOR (dito aqui, ao lado)."),
    13: "= 1 (o transcrito registrado, as recusas nos quatro passos a jusante, samefile; e os casos F no teste).",
    14: "= 5, e o AVISO do PID velho rotulado AVISO_PID_VELHO, listado mas fora do «RELIGADO COM AVISO».",
    15: "= 7 (o giro depois da ultima recusa); o conferidor NAO le o .anterior (misturaria rodadas).",
    16: "as afericoes 6, 7 e 8 OBRIGATORIAS nas evidencias do V1; a 9 opcional.",
    17: ("passada6.criterio_das_repeticoes RESTAURADO ao texto original da 6a e o da 7a gravado AO LADO (passada6.criterio_das_repeticoes_como_implementado_7a), "
         "por este script salvo, com backup de bytes conferido; a disposicao 6a_novos[8] fica como o 7N13 pedia (o texto antigo segue dentro dos parenteses)."),
    18: ("a docstring do teste corrigida ao lado (o caso C e' o das ordens); o TT_OUTRA retirado, com nota; o caso C2 (sonda do MESMO trabalhador) acrescentado e "
         "PASSOU; e AO LADO, nas disposicoes (passada7_errata_da_8a): a PRIMEIRA execucao do teste da 7a FALHOU (a copia das evidencias passou de 260 caracteres), o "
         "que mudou o nome das copias permanentes de <papel>__<nome> para <papel><ext> e trouxe a limpeza da pasta temporaria, pelo aplicar_afer7_gerador_prereg_b.py "
         "(sha256 %s)." % h(F["aplicar_afer7_gerador_prereg_b.py"])[:16]),
}
c8 = Counter(a["estado"] for _, a in ENT)
falta = sorted({a["id"] for _, a in ENT if a["estado"] != "RESOLVIDO"} - set(ACAO_IT)); assert not falta, falta
assert set(ACAO_NOV) == set(range(len(NOV))), (len(NOV), sorted(set(range(len(NOV))) - set(ACAO_NOV)))
dupc = lambda d: sum(1 for v in d.values() if re.search(r"(^|: )= ", str(v)))
sev8 = Counter(v["severidade_ajustada"] for v in V8.values() if not v["refutado"])
sob8 = sum(1 for i in range(len(NOV)) if not (V8.get(i) or {}).get("refutado"))
L = ["\n" + "=" * 80, "8a PASSADA -- as correcoes da 7a (VERBATIM de afericao8_resultado.json, sha256 %s; POR ENTRADA) e DISPOSICOES (%s)" % (h(A8P), time.strftime("%d/%m/%Y %H:%M")), "=" * 80]
for l, a in ENT:
    L.append("\n%s [%s] ESTADO: %s" % (a["id"], l, a["estado"])); L.append("EVIDENCIA: " + a["evidencia"])
    if a.get("falta"):
        L.append("FALTA: " + a["falta"])
    if a["estado"] != "RESOLVIDO":
        L.append("DISPOSICAO DA GERENCIA: " + ACAO_IT[a["id"]])
for i, a in enumerate(NOV):
    v = V8.get(i) or {}
    L.append("\n[8N%d] (%s/%s -> %s, severidade ajustada %s) %s" % (i, a["origem"], a["severidade"], "REFUTADO" if v.get("refutado") else "SOBREVIVE", v.get("severidade_ajustada"), a["arquivo_linha"]))
    L.append("AFIRMACAO: " + a["afirmacao"]); L.append("EVIDENCIA: " + a["evidencia"]); L.append("CORRECAO PEDIDA: " + a["correcao"])
    L.append("VERIFICADOR: " + v.get("razao", "")); L.append("DISPOSICAO DA GERENCIA: " + ACAO_NOV[i])
L.append("\nEVIDENCIAS NOVAS DA GERENCIA NESTA RODADA (sha256): " + "; ".join("%s %s" % (k, h(p)[:16]) for k, p in F.items()))
L.append("\nO TESTE DO CONGELAMENTO (8a): " + "; ".join("%s %s" % (k, "PASSOU" if v["passou"] else "FALHOU") for k, v in TC.items()))
L.append("\nERRATA DA GERENCIA AO LADO (8a): a docstring do aplicar_afer8_lancador_conferidor.py prometia que o conferidor leria o rito_v384_sinal.txt.anterior; "
         "isso NAO foi feito, de proposito (misturaria rodadas) -- dito na propria docstring, ao lado. As edicoes desta rodada feitas pela ferramenta Edit "
         "(gerar_candidato_v384.py: a recusa do transcrito nao canonico; teste_congelamento_v384.py: docstring, C2, F, TT_OUTRA) estao no diff %s." % os.path.basename(DIFF_EDIT))
L.append("\nO QUE CADA LENTE EXAMINOU (8a passada, verbatim):")
for g in A8["grupos"]:
    for x in g.get("examinado") or []:
        L.append("- [%s] %s" % (g["lente"], x))
p = os.path.join(HERE, "AFERIDOR_v384.txt"); raw = open(p, "rb").read()
if b"8a PASSADA -- as correcoes da 7a" in raw:
    print("a 8a ja esta gravada no AFERIDOR")
else:
    novo = raw + ("\n".join(L) + "\n").encode("utf-8"); gravar(p, novo, conferir_prefixo=raw); print("AFERIDOR_v384.txt:", len(raw), "->", len(novo))
dp = os.path.join(HERE, "disposicoes_afericoes_v384.json"); D = json.load(open(dp, encoding="utf-8"))
assert "passada8" not in D, "a 8a ja esta nas disposicoes"
D0 = json.load(open(dp + ".bak_antes_afer7", encoding="utf-8"))
D["passada6"]["criterio_das_repeticoes_como_implementado_7a"] = D["passada6"]["criterio_das_repeticoes"]
D["passada6"]["criterio_das_repeticoes"] = D0["passada6"]["criterio_das_repeticoes"]   # o original da 6a, restaurado (8N17)
D["passada7_errata_da_8a"] = {
    "primeira_execucao_do_teste_do_congelamento": "FALHOU: a copia das evidencias passou do limite de 260 caracteres do Windows numa pasta funda",
    "mudanca": "o nome das copias permanentes de <papel>__<nome base> para <papel><extensao>; a pasta temporaria apagada se a copia falhar",
    "script": {"arquivo": "aplicar_afer7_gerador_prereg_b.py", "sha256": h(F["aplicar_afer7_gerador_prereg_b.py"])},
    "texto": "«com transcrito sintetico» le-se «com uma copia do transcrito real e uma mensagem sintetica acrescentada»; o caso da sonda prometido pela docstring nao foi rodado na 7a (entrou na 8a como C2)",
    "evidencia_da_6a_regerada": {"arquivo": "diff_disposicoes_afer6_edicao_inline_BYTES.txt", "sha256": DJ["sha256"]}}
t = D["texto_para_o_pre_registro"]
assert "; 8ª passada" not in t
t += ("; 8ª passada (as correções da 7ª): %d entradas — %d resolvidas e %d parciais; %d achados novos, %d sobreviventes à verificação (%d repetem outro achado ou "
      "item; severidades: %s), tratados no código ou no texto antes deste documento; o teste do congelamento ganhou o caso da sonda do mesmo trabalhador e os "
      "casos da grafia equivalente da pasta permanente (%d de %d casos como esperado); e, AO LADO: na 7ª, «com transcrito sintético» lê-se «com uma cópia do "
      "transcrito real e uma mensagem sintética acrescentada», e a primeira execução daquele teste FALHOU (cópia acima de 260 caracteres), o que mudou o nome das "
      "cópias das evidências; uma evidência da 6ª (o diff da gravação inline) foi regerada dos bytes") % (
    len(ENT), c8.get("RESOLVIDO", 0), c8.get("PARCIAL", 0) + c8.get("REGRESSAO", 0), len(NOV), sob8, dupc({str(k): v for k, v in ACAO_NOV.items()}),
    ", ".join("%s %d" % (k, v) for k, v in sorted(sev8.items())), _ptc, _ntc)
assert c8.get("REGRESSAO", 0) == 0, "ha regressao na 8a: o texto tem de dize-la"
D["texto_para_o_pre_registro"] = t
D["passada8"] = {"arquivo": os.path.basename(A8P), "sha256": h(A8P), "entradas": dict(c8), "n_entradas": len(ENT), "novos": len(NOV), "sobreviventes": sob8,
                 "severidades_ajustadas": dict(sev8), "repetem_outro": dupc({str(k): v for k, v in ACAO_NOV.items()}),
                 "criterio_das_repeticoes": "«= x» no comeco da disposicao ou depois de «: » (regex (^|: )= )",
                 "evidencias_novas": {k: h(p_) for k, p_ in F.items()}, "teste_congelamento": {k: v["passou"] for k, v in TC.items()}}
D["disposicoes_8a_itens"] = ACAO_IT; D["disposicoes_8a_novos"] = {str(k): v for k, v in ACAO_NOV.items()}
b = json.dumps(D, ensure_ascii=False, indent=1).encode("utf-8")
gravar(dp, b)
print("disposicoes:", hashlib.sha256(b).hexdigest()[:16], "| 8a:", dict(c8), "novos", len(NOV), "sob", sob8, "sev", dict(sev8), "| repeticoes", D["passada8"]["repetem_outro"])
print("6N25:", ACAO_IT["6N25"])
print(t[-900:])
