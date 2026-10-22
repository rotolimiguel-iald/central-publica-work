# -*- coding: utf-8 -*-
"""Registra no MAPA DE ROTAS o que a gerencia examinou depois do seq 314: a 2a e a 3a afericoes do pilar quantico, a decisao n(c2) so como informacao com o
E8, as sondas do trabalhador b3bdecab (motor E1..E8 e tempo) e os rascunhos B_REDUZIDO/A. Numeros LIDOS dos artefatos; os sha256, pela ferramenta."""
import json, os, subprocess, sys, tempfile
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROTAS = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
QUEM = "claude-code/central-de-patentes (gerencia) sessao 6da8f00d"
A2 = json.load(open(os.path.join(HERE, "afericao2_resultado.json"), encoding="utf-8"))
A3 = json.load(open(os.path.join(HERE, "afericao3_resultado.json"), encoding="utf-8"))
c3 = Counter(a["estado"] for g in A3["grupos"] for a in (g.get("achados") or []))
M5 = json.load(open(os.path.join(HERE, "teste_motor_v5", "result.json"), encoding="utf-8"))
T6 = json.load(open(os.path.join(HERE, "teste_tempo_v6", "result.json"), encoding="utf-8"))
RB = json.load(open(os.path.join(HERE, "rascunho_prereg_v4", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_REDUZIDO.json"), encoding="utf-8"))
RA = json.load(open(os.path.join(HERE, "rascunho_prereg_v4", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_A.json"), encoding="utf-8"))
P = lambda *a: os.path.join(HERE, *a)
REG = [
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_afericao_2a_passada", "dominio": "QUANTICA",
     "titulo": "a 2a afericao adversarial do pilar quantico da v384 (trabalhador, runtime, artigo, pre-registro, lancador, cadeia)",
     "pergunta": "o pacote da v384 esta pronto para congelar o pre-registro?",
     "dados": ["o pacote da v384 (trabalhador cec9b0c1 e scripts), sem operadores da teoria"],
     "metodo": "workflow wf_3941feb8-ec7: lentes fisica, robustez, preregistro, integracao, artigo; cada achado verificado por agentes independentes",
     "resultado": "%d achados sobreviventes a verificacao (lista vazia de refutados no arquivo)" % len(A2["sobreviventes"]),
     "veredito": "CORRIGIR_ANTES_DE_CONGELAR", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
     "nao_refazer": "os 48 achados estao no AFERIDOR_v384.txt com a disposicao de cada um; a 3a passada mediu o estado",
     "proximo_passo": "ver quantica.pilar_v384_afericao_3a_passada", "onde": "scratchpad/v384/afericao2_resultado.json",
     "artefatos": [P("afericao2_resultado.json")], "refs": ["quantica.pilar_v384_decisao_operador_03out"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_afericao_3a_passada", "dominio": "QUANTICA",
     "titulo": "a 3a afericao: a resolucao dos 48 achados da 2a e a caca de regressoes",
     "pergunta": "as correcoes da 2a passada resolveram o que foi achado, sem regressao?",
     "dados": ["o pacote da v384 (trabalhador 569c6eb4), o rascunho v3 do pre-registro, o candidato de ensaio 4ba3724f"],
     "metodo": "workflow wf_e141878d-92c: 5 aferidores por grupo + 1 cacador de regressoes + 1 verificador adversarial dos novos; testes puros com entradas sinteticas e simulacao do artigo com pdflatex",
     "resultado": "dos 48: %d resolvidos, %d parciais, %d regressoes; %d achados novos, %d sobreviventes" % (c3.get("RESOLVIDO", 0), c3.get("PARCIAL", 0), c3.get("REGRESSAO", 0), len(A3["novos"]),
                                                                                                            sum(1 for v in A3["verificacao"]["veredictos"] if not v["refutado"])),
     "veredito": "CORRIGIR_ANTES_DE_CONGELAR", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
     "nao_refazer": "as disposicoes estao em disposicoes_afericoes_v384.json e no AFERIDOR_v384.txt; a 4a passada confere as correcoes",
     "proximo_passo": "a 4a afericao (conferencia das correcoes) e o rascunho ao operador", "onde": "scratchpad/v384/afericao3_resultado.json",
     "artefatos": [P("afericao3_resultado.json"), P("disposicoes_afericoes_v384.json"), P("AFERIDOR_v384.txt")], "refs": ["quantica.pilar_v384_afericao_2a_passada"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_cpuref_nc2_e_comparador_e8", "dominio": "QUANTICA",
     "titulo": "a referencia na CPU: n(c2) sai da tolerancia (so informacao) e o comparador ganha autoteste (E8) e o estado NOT_COMPARABLE",
     "pergunta": "a comparacao MAGMA x LAPACK perto do limiar de unicidade anula o resultado sem defeito do motor?",
     "dados": ["linhas ja medidas pelos verificadores da 2a passada com operadores ALEATORIOS (MAGMA contra LAPACK)"],
     "metodo": "releitura das linhas medidas (3a afericao, lente preregistro) + teste puro do comparador com linhas sinteticas",
     "resultado": "|delta n(c2)| ate ~9e-6 com gap_rel ~1e-6 [DECLARADO pela afericao]; CCI, pureza, n(c1), gap e Choi sem excesso; E8 passa no trabalhador b3bdecab",
     "veredito": "NC2_INFORMATIVE__E8_PASSED__NOT_COMPARABLE_STATE_ADDED", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
     "nao_refazer": "n(c2) e n(c3) so como informacao; a decisao vai no pre-registro", "onde": "pilar_quantico_worker.py compare_cpuref / engine_selftest E8",
     "artefatos": [P("teste_motor_v5", "result.json"), P("teste_puro_afer3.py")], "refs": ["quantica.pilar_v384_afericao_3a_passada"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_sondas_b3bdecab", "dominio": "QUANTICA",
     "titulo": "as sondas do trabalhador b3bdecab: o motor E1..E8 e o tempo (so hardware: analiticos e aleatorios)",
     "pergunta": "o motor corrigido passa e quanto custa cada instancia?",
     "dados": ["operadores analiticos (E1..E6), matrizes exatas de posto um (E7), linhas sinteticas (E8), operadores aleatorios (tempo)"],
     "metodo": "worker --mode engine e --mode timing, MAGMA em todo tamanho",
     "resultado": "%s; %s; tempo por instancia d=64 %.1f s, injecao T1 d=64 %.1f s" % (M5["verdict"], " ".join("%s=%s" % (c["name"].split("_")[0], c["ok"]) for c in M5["engine_selftest"]["checks"]),
                                                                                    T6["timing"]["64"]["pipeline_s"], T6["timing"]["64"]["t1_injection_sigma0_s"]),
     "veredito": M5["verdict"], "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
     "nao_refazer": "refazer so se o trabalhador mudar (o hash entra na especificacao)", "onde": "scratchpad/v384/teste_motor_v5, teste_tempo_v6",
     "artefatos": [P("teste_motor_v5", "result.json"), P("teste_tempo_v6", "result.json")], "refs": ["quantica.pilar_v384_decisao_operador_03out"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_rascunhos_b_reduzido_e_a", "dominio": "QUANTICA",
     "titulo": "os dois rascunhos do pre-registro: B_REDUZIDO e A (o desvio do plano B, para a escolha do operador)",
     "pergunta": "qual carga cabe no rito robusto com os custos medidos?",
     "dados": ["teste_tempo_v6 (trabalhador b3bdecab)", "planejar_carga_v384.json (o plano B)"],
     "metodo": "orcamento [DERIVED] pela sonda do proprio trabalhador; margem x1,25 nao medida sob a carga do rito",
     "resultado": "B_REDUZIDO: spec %s, %s min (%s com margem); A: spec %s, %s min (%s com margem); plano B inteiro: %s min (%s com margem), nao cabe" % (
         RB["spec_sha256"][:16], RB["orcamento_estimado"]["total_min"], RB["orcamento_estimado"]["total_com_margem_min"],
         RA["spec_sha256"][:16], RA["orcamento_estimado"]["total_min"], RA["orcamento_estimado"]["total_com_margem_min"],
         RB["desvio_do_plano_B"]["plano_B"]["estimativa_com_os_custos_medidos_agora_min"], RB["desvio_do_plano_B"]["plano_B"]["com_margem_min"]),
     "veredito": "AWAITING_OPERATOR_RATIFICATION", "estatuto": "DERIVED", "status": "EM_CURSO", "olhou_dados": False,
     "nao_refazer": "nada se calcula com os operadores da teoria antes da ratificacao", "proximo_passo": "a 4a afericao; levar os dois ao operador",
     "onde": "C:/IALD/Bancada_Um/investigacao/preregistro_pilar_quantico_03out/gerar_preregistro_pilar_quantico_03out.py",
     "artefatos": [P("rascunho_prereg_v4", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_REDUZIDO.json"), P("rascunho_prereg_v4", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_A.json")],
     "refs": ["quantica.pilar_v384_decisao_operador_03out"]},
]
for r in REG:
    fd, tmp = tempfile.mkstemp(suffix=".json", dir=HERE); os.close(fd)
    open(tmp, "w", encoding="utf-8").write(json.dumps(r, ensure_ascii=False))
    out = subprocess.run([sys.executable, ROTAS, "registrar", tmp, "--quem", QUEM], capture_output=True, text=True, encoding="utf-8")
    os.remove(tmp)
    print(r["rota_id"], "rc", out.returncode, (out.stdout or out.stderr).strip().splitlines()[-1:] if (out.stdout or out.stderr) else "")
    assert out.returncode == 0, out.stderr
