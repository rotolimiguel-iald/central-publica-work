# -*- coding: utf-8 -*-
"""Adapta o gerador do pre-registro a decisao do MAGMA em todo tamanho: argumentos (os cinco artefatos do estresse), a especificacao (linalg; contagens de d = 64
como camada de ESCALA; prazos), o desvio do plano B (com a alternativa A orcada para o operador escolher), a secao do estresse e a nota da dependencia."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
s = open(P, encoding="utf-8").read()
b = P + ".bak_antes_magma"; open(b, "w", encoding="utf-8", newline="").write(s)


def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (c, old[:100]); s = s.replace(old, new)


rep('Uso: python gerar_preregistro_pilar_quantico_03out.py <worker.py> <timing_result.json> <engine_result.json> <estresse_eig.json> <estresse_eig_grande.json> <max_n_magma>"""',
    'Uso: python gerar_preregistro_pilar_quantico_03out.py <worker.py> <timing_result.json> <engine_result.json> <pasta com os cinco artefatos do estresse>"""')
rep('WORKER, TIMING, ENGINE, EST1, EST2, MAXN = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], int(sys.argv[6])',
    'WORKER, TIMING, ENGINE, ESTD = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]\n'
    'EST = {k: os.path.join(ESTD, f) for k, f in (("pequeno", "estresse_eig.json"), ("grande", "estresse_eig_grande.json"), ("caracterizacao", "caracterizar_queda_cusolver.json"),\n'
    '                                            ("variantes", "variantes_cusolver.json"), ("durabilidade", "durabilidade_pipeline.json"))}\n'
    'MAXN = 10 ** 9   # MAGMA em TODO tamanho')
rep('est1 = json.load(open(EST1, encoding="utf-8")); est2 = json.load(open(EST2, encoding="utf-8"))',
    'ESTJ = {k: json.load(open(p, encoding="utf-8")) for k, p in EST.items()}\n'
    'assert all(v["rc"] == 0 for v in ESTJ["durabilidade"].values()), "a durabilidade com o MAGMA nao passou"\n'
    'assert not any(v["caiu"] for k, v in ESTJ["caracterizacao"].items() if k.startswith("magma")), "o MAGMA caiu na caracterizacao"')
rep('''    "linalg": {"nonhermitian_eig_backend": {"magma_up_to_n": MAXN, "cusolver_above": MAXN},
               "nota": "autovalores nao Hermitianos: MAGMA ate n = magma_up_to_n e cuSOLVER acima (o cuSOLVER padrao derrubou o processo em n = 64; estresse por hash)"},''',
    '''    "linalg": {"nonhermitian_eig_backend": {"magma_up_to_n": MAXN},
               "nota": ("autovalores nao Hermitianos pelo MAGMA em TODO tamanho: o cuSOLVER padrao do PyTorch 2.11 derruba o processo de modo deterministico e dependente da "
                        "matriz (8 de 9 tamanhos de 16 a 576); o MAGMA nao caiu em nenhum; dependencia declarada: o PyTorch avisa que o backend MAGMA esta em descontinuacao")},''')
rep('"execution": {"um_py_timeout_s": 14400, "progress_every_s": 300,', '"execution": {"um_py_timeout_s": 18000, "progress_every_s": 300,')
rep('"T2": {"d": [8, 16, 32, 64], "nc": [2, 3, 4], "gamma_lo": 1e-4, "gamma_hi": 1e2, "n_gamma": {"8": 64, "16": 64, "32": 64, "64": 32},',
    '"T2": {"d": [8, 16, 32, 64], "nc": [2, 3, 4], "gamma_lo": 1e-4, "gamma_hi": 1e2, "n_gamma": {"8": 64, "16": 64, "32": 64, "64": 12},')
rep('"T1": {"d_counts": {"8": 2000, "16": 1000, "32": 200, "64": 20}, "noise_subset": {"8": 200, "16": 100, "32": 20, "64": 3},',
    '"T1": {"d_counts": {"8": 2000, "16": 1000, "32": 200, "64": 5}, "noise_subset": {"8": 200, "16": 100, "32": 20, "64": 1},')
rep('"T4": {"d_counts": {"8": 15000, "16": 5000, "32": 1000, "64": 100}, "nc": [2, 3, 4], "dt": 0.05, "steps": 64},',
    '"T4": {"d_counts": {"8": 15000, "16": 5000, "32": 1000, "64": 30}, "nc": [2, 3, 4], "dt": 0.05, "steps": 64},')
rep('"D128": {"d": 128, "nc": 3, "gamma_diss": 1.0, "rk4_dt": 0.002, "rk4_steps": 5000, "start_deadline_s": 7200},',
    '"D128": {"d": 128, "nc": 3, "gamma_diss": 1.0, "rk4_dt": 0.002, "rk4_steps": 5000, "start_deadline_s": 10800},')
rep('"cpuref": {"d_all": [8, 16], "d_pick": {"32": [[3, 0], [3, 16], [3, 32], [3, 48], [3, 63], [2, 32], [4, 32]], "64": [[3, 16]]},',
    '"cpuref": {"d_all": [8, 16], "d_pick": {"32": [[3, 0], [3, 16], [3, 32], [3, 48], [3, 63], [2, 32], [4, 32]], "64": [[3, 6]]},')
# o orcamento: o D128 nao faz expm nem Choi -- estimativa pelo espectro (eigvals) e nao pela instancia inteira
rep('est["D128"] = c_pipe[64] * 64.0   # n^3: (16384/4096)^3 = 64 [DERIVED, estimativa; nao medido -- a VRAM do servidor impede medir antes do rito]',
    'EIGV4096 = ESTJ["grande"]["eigvals_magma_4096"]; _ev = json.loads(EIGV4096["saida"])["s_por_chamada"]\n'
    'est["D128"] = _ev * 64.0 + 120.0   # o espectro em n = 16384 por n^3 a partir do eigvals do MAGMA em 4096 (medido no estresse), mais ~2 min de LU e RK4 [DERIVED, estimativa]')
# o desvio: o plano B e a alternativa A orcada
rep('''PLANO_B = {"T1": {"8": 2000, "16": 2000, "32": 1000, "64": 100}, "T4_d8": 20000, "T2_pontos_d64": 96}''',
    '''PLANO_B = {"T1": {"8": 2000, "16": 2000, "32": 1000, "64": 100}, "T4_d8": 20000, "T4_d64": 100, "T2_pontos_d64": 96}
ALT_A = {"T1_d64": 20, "T1_ruido_d64": 3, "T4_d64": 100, "T2_gamma_d64": 32}
_extra_A = ((ALT_A["T1_d64"] - SPEC["T1"]["d_counts"]["64"]) * c_t1[64] + 2 * (ALT_A["T1_ruido_d64"] - SPEC["T1"]["noise_subset"]["64"]) * c_nz[64]
            + (ALT_A["T4_d64"] - SPEC["T4"]["d_counts"]["64"]) * c_pipe[64] + (ALT_A["T2_gamma_d64"] - SPEC["T2"]["n_gamma"]["64"]) * len(SPEC["T2"]["nc"]) * c_pipe[64])''')
rep('''    "plano_B": PLANO_B, "esta_especificacao": {"T1": SPEC["T1"]["d_counts"], "T4_d8": SPEC["T4"]["d_counts"]["8"], "T2_pontos_d64": SPEC["T2"]["n_gamma"]["64"] * len(SPEC["T2"]["nc"])},''',
    '''    "plano_B": PLANO_B, "esta_especificacao": {"T1": SPEC["T1"]["d_counts"], "T4_d8": SPEC["T4"]["d_counts"]["8"], "T4_d64": SPEC["T4"]["d_counts"]["64"],
                                               "T2_pontos_d64": SPEC["T2"]["n_gamma"]["64"] * len(SPEC["T2"]["nc"])},
    "alternativa_A": {"contagens_d64": ALT_A, "minutos_a_mais_estimados": round(_extra_A / 60, 1), "minutos_a_mais_com_margem": round(_extra_A * MARGEM / 60, 1),
                      "leitura": "manter d = 64 como no plano B (T4 100, T2 96 pontos, T1 20): estatistica de d = 64 mais forte, rito mais longo; escolha do operador"},''')
rep('''    "razao": ("o plano B (planejar_carga_v384.json, 03/10) estimava a injecao do T1 em d = 64 em 3,4 s; medido, com o gerador inteiro e as conferencias do ramo, a injecao "
              "custa %.1f s sem ruido (mais %.1f s por nivel de ruido); restaurar T1 em d = 32 (1000) e d = 64 (100) somaria cerca de %.0f min. O T4 em d = 8 fica em 15 000 "
              "(o limite de falha a 95%% muda de 0,015%% para 0,02%%). O T2 em d = 64 volta aos 96 pontos do plano.") % (c_t1[64], c_nz[64], (800 * c_t1[32] + 80 * c_t1[64]) / 60),''',
    '''    "razao": ("duas causas medidas: (1) o plano B (planejar_carga_v384.json, 03/10) estimava a injecao do T1 em d = 64 em 3,4 s; com o gerador inteiro e as conferencias "
              "do ramo ela custa %.0f s; (2) o cuSOLVER padrao derruba o processo (achado de 03/10, mapa seq 312-314) e o MAGMA, o unico estavel, custa em d = 64 %.1f s por "
              "instancia (o cuSOLVER custava ~12 s). Por isso d = 64 vira camada de ESCALA (T4 30, T2 36 pontos, T1 5) e a estatistica forte fica em d <= 32 (T4 21 000; "
              "T2 576 pontos; T1 3 200). O T4 em d = 8 fica em 15 000 (o limite a 95%% muda de 0,015%% para 0,02%%).") % (c_t1[64], c_pipe[64]),''')
# a secao do estresse: os cinco artefatos
rep('''    "estresse_dos_autovalores": {"pequeno": {"arquivo": os.path.basename(EST1), "sha256": fsha(EST1), "resultado": {k: v.get("rc") for k, v in est1.items()}},
                                 "grande": {"arquivo": os.path.basename(EST2), "sha256": fsha(EST2), "resultado": {k: v.get("rc") for k, v in est2.items()}},
                                 "leitura": "rc 0 = 1 500/150/8 (pequeno) ou o numero de chamadas declarado (grande) sem queda; 3221225477 = violacao de acesso"},''',
    '''    "estresse_dos_autovalores": {k: {"arquivo": os.path.basename(p), "sha256": fsha(p)} for k, p in EST.items()},
    "estresse_leitura": ("o cuSOLVER (o padrao) caiu com violacao de acesso (3221225477) em 8 de 9 tamanhos de 16 a 576, de modo DETERMINISTICO e dependente da matriz "
                         "(a mesma semente cai na mesma chamada com ou sem determinismo, sincronizacao ou cache limpo); o MAGMA fez %d chamadas na caracterizacao sem queda; "
                         "a durabilidade do pipeline inteiro com o MAGMA: %d instancias de operadores aleatorios, d de 8 a 32, sem queda") % (
        sum(v["sobreviveu_ate"] for k, v in ESTJ["caracterizacao"].items() if k.startswith("magma")), sum(v["ate"] for v in ESTJ["durabilidade"].values())),''')
rep('''        "a biblioteca dos autovalores não Hermitianos é escolhida pelo tamanho (MAGMA até n = %d; cuSOLVER acima), porque o cuSOLVER padrão do PyTorch 2.11 derrubou o processo (violação de acesso) em n = 64 no estresse de 03/10; o estresse está nos artefatos" % MAXN],''',
    '''        "os autovalores não Hermitianos vão pelo MAGMA em TODO tamanho: o cuSOLVER padrão do PyTorch 2.11 derruba o processo de modo determinístico e dependente da matriz; o MAGMA não caiu em nenhum tamanho e passou na durabilidade do pipeline inteiro (artefatos por sha256). Dependência declarada: o PyTorch avisa que o backend MAGMA está em descontinuação; a chave do reaproveitamento inclui a versão do torch, então uma atualização força recalcular, e se o MAGMA sair o trabalhador terá de ser revisto às claras (novo V1.x)"],''')
rep('''A("## O estresse dos autovalores (a escolha da biblioteca)"); A("")
A("```json"); A(json.dumps(DOC["estresse_dos_autovalores"], ensure_ascii=False, indent=1)); A("```"); A("")''',
    '''A("## O estresse dos autovalores (a escolha da biblioteca)"); A("")
A(DOC["estresse_leitura"]); A("")
A("```json"); A(json.dumps(DOC["estresse_dos_autovalores"], ensure_ascii=False, indent=1)); A("```"); A("")''')
rep('''A("| T4 em d = 8 | %s | %s |" % (PLANO_B["T4_d8"], SPEC["T4"]["d_counts"]["8"]))''',
    '''A("| T4 em d = 8 | %s | %s |" % (PLANO_B["T4_d8"], SPEC["T4"]["d_counts"]["8"]))
A("| T4 em d = 64 | %s | %s |" % (PLANO_B["T4_d64"], SPEC["T4"]["d_counts"]["64"]))''')
rep('''A(""); A(DESVIO["razao"]); A("")''',
    '''A(""); A(DESVIO["razao"]); A("")
A("**Alternativa A (escolha do operador):** %s — cerca de %s min a mais de GPU (%s com margem). %s" % (json.dumps(DESVIO["alternativa_A"]["contagens_d64"], ensure_ascii=False),
  DESVIO["alternativa_A"]["minutos_a_mais_estimados"], DESVIO["alternativa_A"]["minutos_a_mais_com_margem"], DESVIO["alternativa_A"]["leitura"])); A("")''')
rep('''        "D128": {"tipo": "ESCALA",
                 "o_que": "uma instância canônica em d = 128 (superoperador 16 384 × 16 384; n_c = 3; γ_diss = 1): espectro inteiro, estado estacionário, CCI e dobras; Spohn por RK4 na forma d × d (5 000 passos de 0,002) só como INFORMAÇÃO (o RK4 não é um canal; fora do veredito). Sem a conferência de CP em d = 128 (dita). Roda por último, com prazo de início de 2 h desde o começo do trabalhador. Estados distintos no veredito: rodou (o status do atrator), NOT_RUN_DEADLINE, NOT_RUN_ERROR_<tipo> e INTERRUPTED (o processo morreu depois de começar)."},''',
    '''        "D128": {"tipo": "ESCALA",
                 "o_que": "uma instância canônica em d = 128 (superoperador 16 384 × 16 384; n_c = 3; γ_diss = 1): espectro inteiro, estado estacionário, CCI e dobras; Spohn por RK4 na forma d × d (5 000 passos de 0,002) só como INFORMAÇÃO (o RK4 não é um canal; fora do veredito). Sem a conferência de CP em d = 128 (dita). Roda por último, com prazo de início de 3 h desde o começo do trabalhador. Estados distintos no veredito: rodou (o status do atrator), NOT_RUN_DEADLINE, NOT_RUN_ERROR_<tipo> e INTERRUPTED (o processo morreu depois de começar)."},''')
rep('''"T2": {"tipo": "ESTRUTURAL (pode falhar) + IDENTIDADES",
               "o_que": "o sistema canônico em d ∈ {8,16,32,64}, n_c ∈ {2,3,4}, γ_diss em grade log [1e−4, 1e2] (64 pontos em d ≤ 32; 32 em d = 64).''',
    '''"T2": {"tipo": "ESTRUTURAL (pode falhar) + IDENTIDADES",
               "o_que": "o sistema canônico em d ∈ {8,16,32,64}, n_c ∈ {2,3,4}, γ_diss em grade log [1e−4, 1e2] (64 pontos em d ≤ 32; 12 em d = 64, a camada de escala).''')
rep('''T4": {"tipo": "IDENTIDADES sob estresse (zero violações exigidas) + ESTRUTURAL (frequência de unicidade, relatada)",
               "o_que": "instâncias do molde dos cinco saltos com coeficientes, decaimentos, alcance, taxas (×[1/3, 3]), γ_diss (log-uniforme [1e−4, 1e2]), K, β (log-uniforme [1e−4, 1e−1]), H (μ, J, ε sorteados) e, em metade delas, uma rotação de base de Haar: d = 8 (15 000), 16 (5 000), 32 (1 000), 64 (100).''',
    '''T4": {"tipo": "IDENTIDADES sob estresse (zero violações exigidas) + ESTRUTURAL (frequência de unicidade, relatada)",
               "o_que": "instâncias do molde dos cinco saltos com coeficientes, decaimentos, alcance, taxas (×[1/3, 3]), γ_diss (log-uniforme [1e−4, 1e2]), K, β (log-uniforme [1e−4, 1e−1]), H (μ, J, ε sorteados) e, em metade delas, uma rotação de base de Haar: d = 8 (15 000), 16 (5 000), 32 (1 000), 64 (30, a camada de escala).''')
rep('''Ruído σ ∈ {1e−10, 1e−8} só num subconjunto (d = 8: 200; 16: 100; 32: 20; 64: 3).''', '''Ruído σ ∈ {1e−10, 1e−8} só num subconjunto (d = 8: 200; 16: 100; 32: 20; 64: 1). Contagens: d = 8: 2 000; 16: 1 000; 32: 200; 64: 5.''')
rep('''        "prazo CONGELADO: execution.um_py_timeout_s = 4 h desde o lançamento; passado, o um.py encerra o trabalhador e usa o resultado parcial (o que não rodou fica dito); a CPU de referência tem 1 h",''',
    '''        "prazo CONGELADO: execution.um_py_timeout_s = 5 h desde o lançamento; passado, o um.py encerra o trabalhador e usa o resultado parcial (o que não rodou fica dito); a CPU de referência tem 1 h; o ponto d = 128 só começa até 3 h depois do início do trabalhador",''')
ast.parse(s)
open(P + ".tmp", "w", encoding="utf-8", newline=chr(10)).write(s); os.replace(P + ".tmp", P); print("ok")
