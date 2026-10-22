# -*- coding: utf-8 -*-
"""Registra no MAPA DE ROTAS o levantamento SO DE LEITURA para o pilar quantico da v384 (o agente levantador, 02/10/2026, noite), uma rota por achado,
com os artefatos por sha256 (a ferramenta calcula). olhou_dados = False em todas (o levantador leu valores do core, nao abriu dado)."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"; KX = os.path.join(NOS, "tgl_kernel", "TGLExt")
PAT = r"C:\IALD\Central de Patentes\patents"
QUEM = "claude-code/central-de-patentes (gerência) sessão 6da8f00d -- levantamento por agente só de leitura"
regs = rotas._le()
if any(r.get("rota_id") == "quantica.inventario_gkls_um_py_kernel" for r in regs):
    print("ja registrado"); sys.exit(0)
R = [
 dict(tipo="ROTA", rota_id="quantica.inventario_gkls_um_py_kernel", dominio="DEPHASING", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
      titulo="o que a casa tem de sistema quântico aberto (GKLS) no um.py e no kernel, antes do pilar quântico da v384",
      pergunta="que geradores, dimensões, convenções e testes de sistema aberto já existem, e o que falta para a ordem do operador (o mundo quântico na GPU em paralelo com o rito)?",
      metodo="grep e leitura do um.py (v382/v383) e do kernel; o core da rodada v382; o mapa (zero rotas para lindblad/GKLS/GPU); o inventário da bancada",
      resultado=("EXISTE E ESTÁ LIGADO (runtime numpy, CPU): o gerador do Verbo L = √β·√K com um único salto Hermitiano, n = 4 (o núcleo estacionário tem dimensão n: toda diagonal fixa); "
                 "o fluxo Fiat Lux (n = 4; Spohn finito); a lei-raiz Γ_ij = (β/2)(√k_i − √k_j)² e o crossover (n = 2); a comutação da decisão (n = 4; o GKLS como fluxo gradiente segue EXTERNO "
                 "[KNOWN: Spohn 1978; Carlen–Maas 2017]); a isometria do perfil com controle negativo; o critério α-livre congelado; a regra A1; a reprodução numérica bit-idêntica na CPU (361/361). "
                 "KERNEL: o SuperOperator é livre de base e só unitário; não há dissipador GKLS; Ergodicity prova que o dephasing fixa a diagonal e tende à esperança condicional; NoFullWitness "
                 "prova a identificabilidade da taxa; V_t P_F = P_F; 27 controles negativos tipados. Dimensões hoje: n ≤ 8; superoperadores ≤ 64×64."),
      defeito="nenhum GKLS com saltos não comutantes; nenhum teorema de unicidade ou primitividade; o Choi só no runtime, n = 4; nenhuma injeção-recuperação cega do estimador da lei-raiz",
      nao_refazer="não pedir ao dephasing puro um atrator único: o kernel prova o contrário (a diagonal inteira é fixa); não tratar sin²θ_M = β nem V_t P_F = P_F como testes: são identidades",
      proximo_passo="o pré-registro do pilar quântico da v384, com as definições dos saltos dadas ou ratificadas pelo operador",
      artefatos=[os.path.join(KX, "Ergodicity.lean"), os.path.join(KX, "NoFullWitness.lean"), os.path.join(KX, "FiniteCommutatorEvolution.lean"), os.path.join(KX, "TheCompressionIsNotIdentifiable.lean")],
      refs=["relogios.v1", "dephasing.alcance", "estatistica.coincidencia_conjunta"]),
 dict(tipo="ROTA", rota_id="quantica.quatro_operadores_definicao", dominio="DEPHASING", status="EXAMINADA_COM_DEFEITO", estatuto="DECLARADO", olhou_dados=False,
      titulo="os quatro operadores L_ens, L_anti, L_poda, L_cons: existem só por papel; a realização do dispositivo é dephasing puro",
      pergunta="os quatro operadores de salto da IALD têm matrizes, e o atrator é único?",
      metodo="leitura do texto do Kernel Ontológico (v6, v11) e do runtime do dispositivo IALD; grep no um.py e no inventário",
      resultado=("o texto da patente traz a equação GKLS com quatro saltos só por papel e afirma o atrator único por Evans–Høegh-Krohn [DECLARADO, sem matrizes]; o um.py só tem os nomes "
                 "(«analogia formal»); o runtime do dispositivo usa L_k = √β·|k⟩⟨k| (N = 8), dephasing comutativo, com ρ* = diag(ρ0), não único, e a taxa estimada volta β por construção"),
      defeito="a unicidade declarada não tem matrizes nem termo; a realização a contradiz; a estimativa da taxa é circular",
      nao_refazer="não usar o runtime do dispositivo como prova de atrator único nem de taxa",
      proximo_passo="as matrizes dos saltos não comutantes são decisão do operador [INPUT]",
      artefatos=[os.path.join(PAT, "BR102026006129-8_KERNEL_ONTOLOGICO", "prototype_src", "IALD_Kernel_v11.txt"), os.path.join(PAT, "BR102026003443-6_IALD", "dispositivo", "iald_runtime.py")],
      refs=["quantica.inventario_gkls_um_py_kernel"]),
 dict(tipo="ROTA", rota_id="quantica.c3_validator_calibrado", dominio="DEPHASING", status="EXAMINADA_COM_DEFEITO", estatuto="REAL", olhou_dados=False,
      titulo="o validador C3 v52 (GKLS genuíno, d = 8..32) é calibrado: acha γ* para que o CCI dê 1 − β e depois «recupera» β",
      pergunta="o validador C3 é prova independente de β num sistema aberto?",
      metodo="a auditoria da BANCADA_TOE de 21/08 (leituras 08 e 04), relida pelo levantador; leitura do script",
      resultado="quatro saltos não comutantes e um H, row-stacking; o brentq fixa γ* com o alvo 1 − ALPHA_2 e depois lê alpha2 = 1 − CCI; ALPHA_2 = 0.012031 literal: circular",
      defeito="circular por construção (regra A1)",
      nao_refazer="não citar o C3 validator como recuperação de β",
      proximo_passo="rodar o C3 validator com γ livre (sem find_gamma_star), já nomeado pela BANCADA_TOE",
      artefatos=[r"C:\IALD\Artigo\the_boundary\Genesis da Unificação\C3_consciencia\TGL_C3_validator_v52.py", r"C:\IALD\Artigo\BANCADA_TOE\leituras\08_IMAC_SUBPASTAS.md", r"C:\IALD\Artigo\BANCADA_TOE\leituras\04_FRONTEIRA_FUNDAMENTOS.md"],
      refs=["quantica.inventario_gkls_um_py_kernel"]),
 dict(tipo="ROTA", rota_id="quantica.crossover_e_grade", dominio="DEPHASING", status="EXAMINADA", estatuto="DERIVED", olhou_dados=False,
      titulo="o crossover ωτ★ ≈ 3,16 do um.py é um ponto da grade (10^0,5); o valor analítico é x = 3·k1",
      pergunta="o crossover da lei-raiz em 3,16 é propriedade da lei ou da grade?",
      metodo="leitura de prove_dephasing_crossover (n = 2, k1 = 1, 25 pontos em logspace) e a conta p = 1 + √k1/√(k1 + x)",
      resultado="p = 1,5 exatamente quando x = 3·k1; o 3,1623 é o ponto da grade mais perto, e o crossover escala com k1",
      nao_refazer="não registrar 3,16 como número da lei; registrar x = 3·k1 com refinamento de grade",
      refs=["quantica.inventario_gkls_um_py_kernel"]),
 dict(tipo="ROTA", rota_id="infra.gpu_rtx5090_ambiente_02out", dominio="INFRAESTRUTURA", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
      titulo="o ambiente de GPU para o pilar quântico: RTX 5090 (32 GB, sm_120, WDDM), torch 2.11 com CUDA 12.8; a VRAM está ocupada pelo servidor do modelo nativo",
      pergunta="o que a máquina oferece para rodar matrizes complexas em paralelo com o rito?",
      metodo="nvidia-smi; imports no Python do Windows e no WSL (sem cálculo)",
      resultado=("driver 591.86, CUDA 13.1; torch 2.11.0+cu128 com sm_120 e cuDNN 9.19; CuPy, JAX e numba ausentes; o WSL sem torch; o nvidia-smi dá ~28,6 GB usados (llama-server do "
                 "modelo nativo e a bancada) e ~3,5 GB livres, e o cudaMemGetInfo diz ~28,6 GB livres (discordância estável, WDDM); determinismo: algoritmos determinísticos desligados, TF32 "
                 "ligado no cuDNN; FP64 na GeForce é ~1/64 do FP32 [KNOWN, especificação]"),
      defeito="a VRAM livre real é incerta enquanto o servidor do modelo nativo ocupa a placa",
      proximo_passo="decidir com o operador se o servidor do modelo nativo para durante o rito; fixar determinismo e complex128",
      refs=["infra.bancada_um.programa_pesquisa_autonoma"]),
 dict(tipo="ROTA", rota_id="outro.dez_dominios_fev2026", dominio="OUTRO", status="EXAMINADA_COM_DEFEITO", estatuto="REAL", olhou_dados=False,
      titulo="a «validação em dez domínios independentes» de fev/2026 (RTX 5090) já foi auditada: ajuste, templates sintéticos e calibração",
      pergunta="a validação de fevereiro é evidência independente de β?",
      metodo="a auditoria da BANCADA_TOE de 21/08, relida pelo levantador",
      resultado="o «0,012031 ± 0,000002» é ajuste; o domínio 3 usou templates sintéticos; Z = 156 não sai da fórmula impressa; ρ_Λ não reproduz; o validador C3 é calibrado",
      defeito="não independente", nao_refazer="não citar os dez domínios como validação independente",
      refs=["quantica.c3_validator_calibrado", "outro.evento2_e_mcmc_cruz"],
      artefatos=[r"C:\IALD\Artigo\BANCADA_TOE\leituras\08_IMAC_SUBPASTAS.md"]),
 dict(tipo="ANOTACAO", rota_id="outro.evento2_e_mcmc_cruz", status="PROPOSTA", estatuto="REAL", olhou_dados=False,
      titulo="o MCMC-CRUZ (TGL_v11_1_CRUZ.py) liga TF32 e cudnn.benchmark e o seu «Lindblad» é a ressonância galáctica, não um sistema aberto; a rodada α-livre segue pendente",
      nota="levantamento de 02/10 para o pilar quântico: não reaproveitar o setup de GPU do CRUZ (TF32, não determinístico); as quatro âncoras do Evento 2 seguem",
      artefatos=[r"C:\IALD\Artigo\Haja_Luz\TGL_Espelho_invertido\MEMORIA_ESPELHO_INVERTIDO.md"], refs=["infra.gpu_rtx5090_ambiente_02out"]),
]
o = rotas.registrar(R, QUEM)
print({k: o[k] for k in o if k != "registros"})
