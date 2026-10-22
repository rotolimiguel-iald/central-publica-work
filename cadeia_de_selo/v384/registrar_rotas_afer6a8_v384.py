# -*- coding: utf-8 -*-
"""Registro no MAPA DE ROTAS (regra de 28/09): as afericoes 6a, 7a e 8a do pilar quantico da v384, o teste do congelamento, o teste do mata_um na forma do
rito, as sondas do trabalhador 0c9ba7fd e os rascunhos v9 (RESULTADO da rota dos rascunhos). Os numeros sao LIDOS dos artefatos aqui; o sha256 dos artefatos e'
calculado pela ferramenta."""
import json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
QUEM = "Claude Opus 5.5 -- gerencia, sessao 6da8f00d (Central de Patentes)"
P = lambda *a: os.path.join(HERE, *a)
D = json.load(open(P("disposicoes_afericoes_v384.json"), encoding="utf-8"))
TC = json.load(open(P("teste_congelamento_v384.json"), encoding="utf-8"))
RB = json.load(open(P("rascunho_prereg_v9", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_REDUZIDO.json"), encoding="utf-8"))
RA = json.load(open(P("rascunho_prereg_v9", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_AMPLIADO_D64.json"), encoding="utf-8"))
MO = json.load(open(P("teste_motor_v8", "result.json"), encoding="utf-8")); TT = json.load(open(P("teste_tempo_v9", "result.json"), encoding="utf-8"))


def pas(n):
    x = D["passada%d" % n]
    return "%d entradas %s; %d novos, %d sobreviventes, severidades %s, %d repetem outro" % (x["n_entradas"], json.dumps(x["entradas"]), x["novos"], x["sobreviventes"],
                                                                                         json.dumps(x["severidades_ajustadas"]), x["repetem_outro"])


REG = [
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_afericao_6a_passada", "dominio": "QUANTICA", "titulo": "a 6a afericao: as correcoes da 5a conferidas e a verificacao adversarial dos achados da 5a",
     "pergunta": "as correcoes da 5a fecham, e os achados que a 5a nao verificou sobrevivem?", "dados": ["o codigo do pilar (trabalhador, runtime, artigo, lancador, conferidor, gerador do pre-registro)"],
     "metodo": "agentes aferidores por lente + verificador adversarial; disposicoes por achado no registro verbatim", "resultado": pas(6), "veredito": "AFERICAO_6A_TRATADA",
     "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False, "defeito": "uma gravacao das disposicoes por python inline nao salvo (errata ao lado na 7a; diff regerado dos bytes na 8a)",
     "nao_refazer": "os achados e as disposicoes estao no AFERIDOR_v384.txt e em disposicoes_afericoes_v384.json", "proximo_passo": "a 7a",
     "onde": "scratchpad v384 (sessao 6da8f00d)", "artefatos": [P("afericao6_resultado.json")], "refs": ["quantica.pilar_v384_afericao_5a_passada"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_afericao_7a_passada", "dominio": "QUANTICA", "titulo": "a 7a afericao: as correcoes da 6a; a regressao ALTA da comparacao V1 x rascunho",
     "pergunta": "as correcoes da 6a fecham sem regressao?", "dados": ["o codigo do pilar"], "metodo": "aferidores por lente + verificador adversarial",
     "resultado": pas(7) + "; a regressao: a comparacao do V1 com o rascunho (chaves int x str) recusava TODO congelamento -> formas canonicas; o caminho do congelamento testado",
     "veredito": "AFERICAO_7A_TRATADA", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
     "defeito": "o teste do congelamento da 7a: a primeira execucao falhou (260 caracteres); a docstring prometia um caso de sonda nao rodado (erratas ao lado na 8a)",
     "nao_refazer": "registrado verbatim", "proximo_passo": "a 8a", "onde": "scratchpad v384", "artefatos": [P("afericao7_resultado.json")], "refs": ["quantica.pilar_v384_afericao_6a_passada"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_afericao_8a_passada", "dominio": "QUANTICA", "titulo": "a 8a afericao: as correcoes da 7a; so achados de severidade BAIXA",
     "pergunta": "as correcoes da 7a fecham? o que resta?", "dados": ["o codigo do pilar"], "metodo": "aferidores por lente (congelamento, runtime/artigo/ensaio, lancador/conferidor, regressao) + verificador adversarial",
     "resultado": pas(8) + "; todos tratados: dispersao das sondas por d e custo, transcrito registrado e recusado se de teste, gravacao transacional, PID logo depois da guarda, giro do log so depois da ultima recusa",
     "veredito": "AFERICAO_8A_TRATADA", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False, "defeito": "",
     "nao_refazer": "registrado verbatim (AFERIDOR_v384.txt) com as disposicoes", "proximo_passo": "apresentar os rascunhos v9 ao operador para a ratificacao",
     "onde": "scratchpad v384", "artefatos": [P("afericao8_resultado.json"), P("disposicoes_afericoes_v384.json"), P("AFERIDOR_v384.txt")], "refs": ["quantica.pilar_v384_afericao_7a_passada"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_teste_do_congelamento", "dominio": "QUANTICA", "titulo": "o caminho do CONGELAMENTO do pre-registro testado numa pasta de teste",
     "pergunta": "o gerador congela o V1 so quando o operador ratifica o rascunho apresentado, e recusa todo o resto sem deixar rastro?",
     "dados": ["copia do transcrito real com mensagem(ns) SINTETICA(s) acrescentada(s)", "copia minima do pacote com uma sonda SINTETICA do mesmo trabalhador (C2)"],
     "metodo": "8 casos: A igual (aceito); B outra escolha, C ordens diferentes, C2 outra sonda do mesmo trabalhador, D negacao, E as duas escolhas (recusados, sem pasta nem temporario); F grafia 8.3 e prefixo longo da pasta permanente com a variavel de teste (recusa na guarda, pasta intacta)",
     "resultado": "; ".join("%s %s" % (k, "PASSOU" if v["passou"] else "FALHOU") for k, v in TC.items()), "veredito": "TESTE_DO_CONGELAMENTO_%d_DE_%d" % (sum(1 for v in TC.values() if v["passou"]), len(TC)),
     "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False, "defeito": "transcrito e sonda sinteticos (marcados); nao e' o congelamento real",
     "nao_refazer": "o caminho do congelamento ja foi exercitado; o real e' ato do operador", "proximo_passo": "o congelamento real com a mensagem do operador",
     "onde": "teste_congelamento_v384.py", "artefatos": [P("teste_congelamento_v384.py"), P("teste_congelamento_v384.json")], "refs": ["quantica.pilar_v384_afericao_8a_passada"]},
    {"tipo": "ROTA", "rota_id": "infra.rito_v384_mata_um_forma_do_rito", "dominio": "INFRAESTRUTURA", "titulo": "o encerramento da arvore do um.py (mata_um) testado na forma do rito",
     "pergunta": "com ( echo 1 | python um.py > f 2>&1 ) &, o caminho principal (PID nativo do subshell) e a reserva (descendentes) encerram o python?",
     "dados": ["um.py FALSO (le a entrada e dorme)"], "metodo": "(A) taskkill /T no winpid do subshell; (B) a consulta da reserva + taskkill; contagem de python um.py vivos antes/depois",
     "resultado": "(A) PASSOU e (B) PASSOU; o W do subshell e' o sh.exe pai do python (diferente do teste so de leitura da 7a, em que o subshell virava o proprio python)",
     "veredito": "MATA_UM_FORMA_DO_RITO_A_E_B_PASSARAM", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False, "defeito": "",
     "nao_refazer": "os dois caminhos do mata_um ja foram exercitados na forma do rito", "proximo_passo": "",
     "onde": "rito_v384.sh mata_um", "artefatos": [P("teste_mata_um_forma_do_rito.sh"), P("teste_mata_um_forma_do_rito.out")], "refs": []},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_sondas_0c9ba7fd", "dominio": "QUANTICA", "titulo": "as sondas do trabalhador 0c9ba7fd: o motor E1..E8 e o tempo (so hardware: analiticos e aleatorios)",
     "pergunta": "o motor do trabalhador corrente passa o autoteste, e quanto custa cada pedaco na RTX 5090?", "dados": ["operadores analiticos e aleatorios (nenhum operador da teoria)"],
     "metodo": "modos engine e timing do trabalhador", "resultado": "motor %s; d = 64: instancia %.2f s, injecao do T1 %.2f s" % (MO.get("verdict"), TT["timing"]["64"]["pipeline_s"], TT["timing"]["64"]["t1_injection_sigma0_s"]),
     "veredito": str(MO.get("verdict")), "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False, "defeito": "a dispersao entre sondas chega a 1,32 (d = 32 instancia) e 1,26 (d = 64 injecao), acima da margem x1,25",
     "nao_refazer": "as sondas deste trabalhador sao as do orcamento", "proximo_passo": "", "onde": "pilar_quantico_worker.py",
     "artefatos": [P("teste_motor_v8", "result.json"), P("teste_tempo_v9", "result.json")], "refs": ["quantica.pilar_v384_sondas_variabilidade"]},
    {"tipo": "RESULTADO", "rota_id": "quantica.pilar_v384_rascunhos_b_reduzido_e_a", "dominio": "QUANTICA", "titulo": "os rascunhos v9: B_REDUZIDO e B_AMPLIADO_D64 (a alternativa A virou B_AMPLIADO_D64 na 4a afericao)",
     "pergunta": "qual especificacao o operador ratifica?", "dados": ["sonda de tempo teste_tempo_v9", "autoteste teste_motor_v8"],
     "metodo": "o gerador do pre-registro (sha256 no rascunho); nenhum operador da teoria calculado",
     "resultado": "B_REDUZIDO spec %s, %.1f min de GPU (%.1f com a margem); B_AMPLIADO_D64 spec %s, %.1f min (%.1f com a margem)" % (
         RB["spec_sha256"][:16], RB["orcamento_estimado"]["total_min"], RB["orcamento_estimado"]["total_com_margem_min"], RA["spec_sha256"][:16],
         RA["orcamento_estimado"]["total_min"], RA["orcamento_estimado"]["total_com_margem_min"]),
     "veredito": "RASCUNHOS_V9_AGUARDAM_A_RATIFICACAO_DO_OPERADOR", "estatuto": "INPUT", "status": "EM_CURSO", "olhou_dados": False, "defeito": "",
     "nao_refazer": "", "proximo_passo": "a mensagem do operador nomeando «b reduzido» ou «b ampliado»; entao o congelamento do V1",
     "onde": "rascunho_prereg_v9/", "artefatos": [P("rascunho_prereg_v9", f) for f in sorted(os.listdir(P("rascunho_prereg_v9")))], "refs": ["quantica.pilar_v384_afericao_8a_passada"]},
]
os.makedirs(P("rotas_afer8"), exist_ok=True)
for i, r in enumerate(REG):
    f = P("rotas_afer8", "%02d_%s.json" % (i, r["rota_id"])); json.dump(r, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    o = subprocess.run([sys.executable, R, "registrar", f, "--quem", QUEM], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(r["rota_id"], "rc", o.returncode, (o.stdout + o.stderr).strip().splitlines()[-1][:200] if (o.stdout + o.stderr).strip() else "")
