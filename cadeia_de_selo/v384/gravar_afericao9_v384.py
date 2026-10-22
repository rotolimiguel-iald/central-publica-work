# -*- coding: utf-8 -*-
"""Registro da 9a afericao (gerencia, em nome proprio; so acrescimo): VERBATIM por entrada, com as disposicoes. AO LADO: (1) no trecho da 6a do texto do
pre-registro, o numero da 6a RESTAURADO («8 deles repetem...») com o da 7a ao lado («9 pela contagem corrigida na 7a») -- a gravacao da 7a o tinha trocado
por cima (9N... / 8N17 parcial); (2) o gravar_afericao8_v384.py registrado com o seu sha256 (passada8.gravador). Evidencias novas: os scripts da 9a, o teste
dos orfaos e o teste do congelamento. Backup de BYTES conferido; temporario -> tamanho -> substituir -> conferir."""
import hashlib, json, os, re, sys, time
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
A9P = os.path.join(HERE, "afericao9_resultado.json"); A9 = json.load(open(A9P, encoding="utf-8"))
ENT = [(g["lente"], a) for g in A9["grupos"] for a in (g.get("itens") or [])]
NOV = A9["novos"]; V9 = {v["i"]: v for v in (A9.get("verificacao") or {}).get("veredictos", [])}
GEN = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")


def gravar(p, novo, conferir_prefixo=None):
    raw = open(p, "rb").read()
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw, "backup nao confere"
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo), "temporario com tamanho errado"
    os.replace(p + ".tmp", p); assert open(p, "rb").read() == novo, "o gravado nao confere"
    if conferir_prefixo is not None:
        assert novo[:len(conferir_prefixo)] == conferir_prefixo
    return bak


F = {k: os.path.join(HERE, k) for k in ("salvar_afericao9.py", "aplicar_afer9_lancador_conferidor.py", "aplicar_afer9_gerador_prereg.py", "aplicar_afer9_guardas_e_teste.py",
                                         "teste_orfaos_v384.py", "teste_orfaos_v384.json", "teste_congelamento_v384.py", "teste_congelamento_v384.json", "gravar_afericao9_v384.py")}
F["gerador_do_pre_registro"] = GEN
TC = json.load(open(F["teste_congelamento_v384.json"], encoding="utf-8")); TO = json.load(open(F["teste_orfaos_v384.json"], encoding="utf-8"))
assert all(v["passou"] for v in TC.values()) and all(v["passou"] for v in TO.values()), "um teste nao passou"
_o2o3 = all("V1.json ja existe com outro conteudo" in TO[k]["saida"] for k in ("O2_json_presente_pasta_adulterada", "O3_json_presente_arquivo_a_mais"))
ACAO_IT = {
    "6N25": ("a nota antiga diz o seu escopo (em d = 64: instancia e injecao do T1 sobre a corrente; a maior/menor da INSTANCIA); a frase da nota por d e custo e' "
             "GERADA dos numeros (com a corrente a mais lenta nos pontos fora da margem: «o orcamento (a corrente x1,25) cobre uma rodada ate 25% mais lenta que "
             "ela, nao mais»; senao, os pontos em que nao e'); o cabecalho do paragrafo no MD diz que a lista e' de d = 64 e a nota cobre d = 8 a 64."),
    "8N17": ("no trecho da 6a do texto do pre-registro, o numero da 6a RESTAURADO e o da 7a AO LADO: «8 deles repetem outro achado ou item; 9 pela contagem "
             "corrigida na 7a»; e o gravar_afericao8_v384.py registrado com o seu sha256 (passada8.gravador)."),
}
ACAO_NOV = {
    0: ("o MD e a pasta de evidencias de uma tentativa INTERROMPIDA (sem o JSON) vao para o lado (.incompleto_<data>), nunca apagados, e TODAS as guardas vem "
        "antes de qualquer movimento; testado em teste_orfaos_v384 (O1 PASSOU: o MD e a pasta adulterada foram para o lado com os bytes preservados e o V1 novo "
        "confere); O2 e O3 recusaram sem mover nada%s." % (
            " -- mas pela guarda do V1 ja existente (o campo gerado muda a cada segundo), nao pela guarda nova das evidencias, que so se alcanca com o V1 IGUAL "
            "(relogio fixo, como a 9a mediu); dito aqui" if _o2o3 else "")),
    1: "o temporario que nao puder ser removido vira AVISO e a excecao ORIGINAL e' a relancada.",
    2: ("os casos F passam um trabalhador INEXISTENTE: sem a guarda, o gerador morreria ao abrir o trabalhador, antes de qualquer gravacao; rodados: %s." %
        "; ".join("%s %s" % (k, "PASSOU" if v["passou"] else "FALHOU") for k, v in TC.items() if k.startswith("F_"))),
    3: "o MD mostra o transcrito lido (caminho, de_teste, as linhas e o sha256 delas, o tamanho na leitura).",
    4: "o .rito_v384.pid sai no FIM da restauracao (o trap do EXIT e' «religar; rm -f pid»), nao no comeco do religar: a recusa 16 cobre a restauracao inteira.",
    5: ("o .fase0 de uma tentativa anterior GIRA para .fase0.anterior antes de ser zerado (se nao girar, recusa 17); as recusas 14 vao pelo log(); o texto do "
        "pre-registro diz onde fica o registro de uma tentativa recusada (o .fase0)."),
    6: "a linha do log diz «ha parada (Stop-ScheduledTask ou stop_iald_llama.ps1) ainda em curso»; o conferidor casa a forma nova e a antiga (HAVIA PARADA EM CURSO).",
    7: ("o texto do lancador: o aviso do TaskStop de volta junto do aborto; o giro redigido como e' (o .fase0 toma o lugar do log real; o real anterior e os "
        "sinais vao para .anterior; o de uma tentativa recusada fica no .fase0)."),
    8: "= 4.",
    9: "= 5.",
    10: "a contagem ILEGIVEL tem linha propria no log («a contagem das paradas em curso nao foi legivel») e rotulo proprio no conferidor; o marcador fica.",
    11: ("= 6N25 (a frase gerada dos numeros; o escopo da nota antiga); e AO LADO no bloco 10 da memoria da v384: a frase de la («a sonda corrente e' a mais "
         "lenta ali») vale pelos numeros de hoje, nao por construcao."),
    12: "= 3.",
    13: "= 0 (o giro do MD orfao foi para DEPOIS das guardas das evidencias).",
    14: "o giro do log real e do registro dos sinais e' CONFERIDO: se falhar, FALHA VISIVEL e recusa 17 (o trap restaura o servidor).",
    15: "a espera de 60 s usa a MESMA consulta da reconferencia (Stop-ScheduledTask da tarefa ou stop_iald_llama.ps1); o texto do pre-registro diz as duas.",
    16: "o gerador do pre-registro, o gerar_candidato, a fumaca, o gerar_esperados e o instalador RECUSAM rodar com -O/PYTHONOPTIMIZE; rodados com -O: os cinco recusaram.",
}
c9 = Counter(a["estado"] for _, a in ENT)
falta = sorted({a["id"] for _, a in ENT if a["estado"] != "RESOLVIDO"} - set(ACAO_IT)); assert not falta, falta
assert set(ACAO_NOV) == set(range(len(NOV))), (len(NOV), sorted(set(range(len(NOV))) - set(ACAO_NOV)))
dupc = lambda d: sum(1 for v in d.values() if re.search(r"(^|: )= ", str(v)))
sev9 = Counter(v["severidade_ajustada"] for v in V9.values() if not v["refutado"])
sob9 = sum(1 for i in range(len(NOV)) if not (V9.get(i) or {}).get("refutado"))
L = ["\n" + "=" * 80, "9a PASSADA -- as correcoes da 8a (VERBATIM de afericao9_resultado.json, sha256 %s; POR ENTRADA) e DISPOSICOES (%s)" % (h(A9P), time.strftime("%d/%m/%Y %H:%M")), "=" * 80]
for l, a in ENT:
    L.append("\n%s [%s] ESTADO: %s" % (a["id"], l, a["estado"])); L.append("EVIDENCIA: " + a["evidencia"])
    if a.get("falta"):
        L.append("FALTA: " + a["falta"])
    if a["estado"] != "RESOLVIDO":
        L.append("DISPOSICAO DA GERENCIA: " + ACAO_IT[a["id"]])
for i, a in enumerate(NOV):
    v = V9.get(i) or {}
    L.append("\n[9N%d] (%s/%s -> %s, severidade ajustada %s) %s" % (i, a["origem"], a["severidade"], "REFUTADO" if v.get("refutado") else "SOBREVIVE", v.get("severidade_ajustada"), a["arquivo_linha"]))
    L.append("AFIRMACAO: " + a["afirmacao"]); L.append("EVIDENCIA: " + a["evidencia"]); L.append("CORRECAO PEDIDA: " + a["correcao"])
    L.append("VERIFICADOR: " + v.get("razao", "")); L.append("DISPOSICAO DA GERENCIA: " + ACAO_NOV[i])
L.append("\nEVIDENCIAS NOVAS DA GERENCIA NESTA RODADA (sha256): " + "; ".join("%s %s" % (k, h(p)[:16]) for k, p in F.items()))
L.append("\nOS TESTES (9a): congelamento: " + "; ".join("%s %s" % (k, "PASSOU" if v["passou"] else "FALHOU") for k, v in TC.items())
         + " | orfaos: " + "; ".join("%s %s" % (k, "PASSOU" if v["passou"] else "FALHOU") for k, v in TO.items()))
L.append("\nO QUE CADA LENTE EXAMINOU (9a passada, verbatim):")
for g in A9["grupos"]:
    for x in g.get("examinado") or []:
        L.append("- [%s] %s" % (g["lente"], x))
p = os.path.join(HERE, "AFERIDOR_v384.txt"); raw = open(p, "rb").read()
if b"9a PASSADA -- as correcoes da 8a" in raw:
    print("a 9a ja esta gravada no AFERIDOR")
else:
    novo = raw + ("\n".join(L) + "\n").encode("utf-8"); gravar(p, novo, conferir_prefixo=raw); print("AFERIDOR_v384.txt:", len(raw), "->", len(novo))
dp = os.path.join(HERE, "disposicoes_afericoes_v384.json"); D = json.load(open(dp, encoding="utf-8"))
assert "passada9" not in D, "a 9a ja esta nas disposicoes"
t = D["texto_para_o_pre_registro"]
OLD6 = "26 achados novos, 26 sobreviventes à verificação (9 deles repetem outro achado ou item, contagem corrigida na 7ª;"
NEW6 = "26 achados novos, 26 sobreviventes à verificação (8 deles repetem outro achado ou item; 9 pela contagem corrigida na 7ª;"
assert t.count(OLD6) == 1, "o trecho da 6a nao esta como a 7a o deixou"
t = t.replace(OLD6, NEW6)
assert "; 9ª passada" not in t
t += ("; 9ª passada (as correções da 8ª): %d entradas — %d resolvidas e %d parciais; %d achados novos, %d sobreviventes à verificação (%d repetem outro achado ou "
      "item; severidades: %s), tratados no código ou no texto antes deste documento; o teste do congelamento (%d de %d casos como esperado) e um teste novo dos "
      "órfãos de uma tentativa interrompida (%d de %d%s); e, AO LADO: no trecho da 6ª, o número da 6ª restaurado («8 deles repetem…») com o da 7ª ao lado "
      "(«9 pela contagem corrigida na 7ª»)") % (
    len(ENT), c9.get("RESOLVIDO", 0), c9.get("PARCIAL", 0) + c9.get("REGRESSAO", 0), len(NOV), sob9, dupc({str(k): v for k, v in ACAO_NOV.items()}),
    ", ".join("%s %d" % (k, v) for k, v in sorted(sev9.items())), sum(1 for v in TC.values() if v["passou"]), len(TC), sum(1 for v in TO.values() if v["passou"]), len(TO),
    ("; dois deles recusados pela guarda do V1 já existente, não pela guarda nova das evidências, que só se alcança com o V1 igual" if _o2o3 else ""))
assert c9.get("REGRESSAO", 0) == 0, "ha regressao na 9a: o texto tem de dize-la"
D["texto_para_o_pre_registro"] = t
D["passada8"]["gravador"] = {"arquivo": "gravar_afericao8_v384.py", "sha256": h(os.path.join(HERE, "gravar_afericao8_v384.py")), "registrado_na": "9a afericao (8N17)"}
D["passada9"] = {"arquivo": os.path.basename(A9P), "sha256": h(A9P), "entradas": dict(c9), "n_entradas": len(ENT), "novos": len(NOV), "sobreviventes": sob9,
                 "severidades_ajustadas": dict(sev9), "repetem_outro": dupc({str(k): v for k, v in ACAO_NOV.items()}),
                 "criterio_das_repeticoes": "«= x» no comeco da disposicao ou depois de «: » (regex (^|: )= )",
                 "evidencias_novas": {k: h(p_) for k, p_ in F.items()}, "teste_congelamento": {k: v["passou"] for k, v in TC.items()},
                 "teste_orfaos": {k: v["passou"] for k, v in TO.items()}, "texto_6a_restaurado_com_7a_ao_lado": True}
D["disposicoes_9a_itens"] = ACAO_IT; D["disposicoes_9a_novos"] = {str(k): v for k, v in ACAO_NOV.items()}
b = json.dumps(D, ensure_ascii=False, indent=1).encode("utf-8")
gravar(dp, b)
print("disposicoes:", hashlib.sha256(b).hexdigest()[:16], "| 9a:", dict(c9), "novos", len(NOV), "sob", sob9, "sev", dict(sev9), "| repeticoes", D["passada9"]["repetem_outro"])
print(t[-800:])
