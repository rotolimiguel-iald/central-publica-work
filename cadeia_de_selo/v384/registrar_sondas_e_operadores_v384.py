# -*- coding: utf-8 -*-
"""Registra no MAPA DE ROTAS (03/10/2026, manha) o que a gerencia examinou para responder ao operador sobre a v384:
(1) as duas sondas de tempo da RTX 5090 (so hardware, matrizes aleatorias); (2) os cinco operadores de Lindblad da teoria e as suas matrizes
nas versoes do validador C3; (3) a hierarquia das dobras (M7) e' matematica -- nao pode falhar; (4) a supervisao do servidor do modelo nativo
e a duracao do rito v383. Numeros LIDOS dos JSON/TXT por este script; artefatos por sha256 (a ferramenta calcula)."""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
QUEM = "claude-code/central-de-patentes (gerência) sessão 6da8f00d"
regs = rotas._le()
if any(r.get("rota_id") == "infra.gpu_sonda_tempo_v384" for r in regs):
    print("ja registrado"); sys.exit(0)
s1 = json.load(open(os.path.join(HERE, "sonda_tempo_gpu_v384.json"), encoding="utf-8"))
s2 = json.load(open(os.path.join(HERE, "sonda_pipeline_gpu_v384.json"), encoding="utf-8"))
m = s1["medidas"]; p = s2["por_d"]
tf = m["gemm_complex128_4096"]["tflops_reais"]
r64 = m["d64"]
txt_dobras = open(os.path.join(HERE, "checar_dobras_identidade.txt"), encoding="utf-8").read().strip().splitlines()[0]
hor = open(os.path.join(os.path.dirname(HERE), "v383", "rito_horarios_v383.txt"), encoding="utf-8").read().split()
def seg(h):
    a, b, c = (int(x) for x in h.split(":")); return a * 3600 + b * 60 + c
dur = seg(hor[1]) - seg(hor[0])
VAL = r"C:\IALD\projetos_pyhton\acom"
FR = r"C:\IALD\Artigo\the_boundary\Genesis da Unificação"
R = [
 dict(tipo="ROTA", rota_id="infra.gpu_sonda_tempo_v384", dominio="INFRAESTRUTURA", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
      titulo="as sondas de tempo da RTX 5090 para dimensionar o pilar quântico da v384 (só hardware: matrizes aleatórias, nenhum operador da teoria)",
      pergunta="quanto custa, nesta máquina, cada operação e cada instância completa do pipeline GKLS em complex128, para fixar a carga do teste antes do pré-registro?",
      metodo=("sonda 1: GEMM 4096 e, por d em {8,16,32,64}, montar o superoperador (5 saltos aleatórios), expm, eig, SVD, e a CPU (numpy/scipy, 4 fios) ao lado; "
              "sonda 2: a instância inteira (superoperador, espectro por eigvals, estacionário por LU com a linha do traço, propagador expm, trajetória 64x3 com "
              "192 eigh, Choi e o seu menor autovalor); complex128; determinismo ligado; TF32 desligado; o servidor do modelo nativo LIGADO e ocioso"),
      resultado=("GEMM complex128 4096: %.2f TFLOP/s reais; instância completa: d=8 %.3f s, d=16 %.3f s, d=32 %.2f s, d=64 %.1f s (pico %.0f MiB); "
                 "em d=64: eig GPU %.1f s contra numpy %.1f s (4 fios), expm GPU %.1f s contra scipy %.1f s; SVD na GPU lenta (%.0f s em d=64), evitar; "
                 "d=128 estimado por n³: ~10 min e ~25 GB por instância, só com o servidor parado [DERIVED]")
               % (tf, p["d8"]["total"], p["d16"]["total"], p["d32"]["total"], p["d64"]["total"], p["d64"]["mem_pico_MiB"],
                  r64["eig_s"], r64["eig_cpu_numpy_s"], r64["expm_s"], r64["expm_cpu_scipy_s"], r64["svd_nucleo_s"]),
      defeito="o eig não Hermitiano da GPU é híbrido (parte na CPU): durante o lake build pode alongar; medido com o servidor ligado, sem a carga do rito",
      nao_refazer="não medir de novo para decidir a ordem de grandeza; refazer só a sonda final com o servidor parado, se o operador quiser a margem exata",
      proximo_passo="fixar a carga no pré-registro da v384 a partir destes custos, com margem declarada para a disputa de CPU com o lake build",
      onde="scratchpad v384: sonda_tempo_gpu_v384.py, sonda_pipeline_gpu_v384.py",
      artefatos=[os.path.join(HERE, "sonda_tempo_gpu_v384.py"), os.path.join(HERE, "sonda_tempo_gpu_v384.json"),
                 os.path.join(HERE, "sonda_pipeline_gpu_v384.py"), os.path.join(HERE, "sonda_pipeline_gpu_v384.json")],
      refs=["infra.gpu_rtx5090_ambiente_02out", "quantica.inventario_gkls_um_py_kernel"]),
 dict(tipo="ROTA", rota_id="quantica.cinco_operadores_lindblad_matrizes", dominio="DEPHASING", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
      titulo="os cinco operadores de Lindblad da teoria (A Fronteira v5): nomeados na §V.6; matrizes espalhadas pelas versões do validador C3; o L_anti tem a forma do gerador do Verbo",
      pergunta="os cinco operadores de salto que o operador diz já descritos na teoria têm matrizes, e quais?",
      metodo="leitura de A_fronteira_v5.tex (§V.6, linhas ~2072-2084; Apêndice A.3/A.4) e dos validadores C3 v1, v2, v3, v3.3, v4, v5, v5.1, v5.2; grep no um.py (v12 e o gerador do Verbo)",
      resultado=("A Fronteira v5 nomeia CINCO na §V.6: L_reh (reensaio), L_anti (anti-coerência, decoerência seletiva), L_prune (poda), L_cons (consolidação), "
                 "L_diss (dissipação térmica, acoplamento com banho); a tabela A.1/A.4 e a eq. do Protocolo IALD trazem QUATRO (sem L_diss); o um.py v12 traz os "
                 "quatro só por nome («analogia formal»). Matrizes: v1 (07/02/2026) as quatro nomeadas; v2/v3 as quatro, com α₂ no L_anti e no L_prune; v3.3 a "
                 "v5.2 tiram o α₂: o L_anti sai, o L_prune fica sem α₂ e entra L5 = vazamento núcleo -> periferia (o único γ livre, calibrado por brentq para "
                 "CCI = 1 − α₂: a circularidade já registrada). O L_anti de v2/v3 é diag(√(α₂(1+0,1(i−n_c)))) na periferia = √α₂·√K com K = diag(0 no núcleo; "
                 "1+0,1(i−n_c) na periferia): a MESMA forma do gerador do Verbo do um.py (L = √β·√K, linha 2326), lei-raiz Γ_ij = (β/2)(√k_i − √k_j)²; "
                 "ker K = o núcleo = Π (o Nome do −εΠ de H_LD)."),
      defeito="nenhuma versão tem as cinco matrizes juntas; a leitura de L_diss como o vazamento núcleo -> periferia é da gerência [DERIVED de leitura]; o "
              "documento de energia escura de nov/2025 usa outro L_diss (√γ_Λ Ĥ, dephasing de energia)",
      nao_refazer="não procurar as matrizes de novo: estão nos validadores de acom/ (v1-v5.1) e no Genesis (v5.2); não tratar o validador v5.2 como tendo os cinco",
      proximo_passo="o operador ratifica as cinco matrizes (e qual é o L_diss) antes do pré-registro; β nunca calibrado: no T1 entra um valor injetado às cegas",
      artefatos=[os.path.join(FR, "Artigos_fundadores", "A_fronteira_v5.tex"), os.path.join(VAL, "Tgl_c3_consciousness_validator.py"),
                 os.path.join(VAL, "Tgl_c3_consciousness_validator_v2.py"), os.path.join(VAL, "Tgl_c3_consciousness_validator_v3.py"),
                 os.path.join(FR, "C3_consciencia", "TGL_C3_validator_v52.py")],
      refs=["quantica.quatro_operadores_definicao", "quantica.c3_validator_calibrado", "quantica.inventario_gkls_um_py_kernel"]),
 dict(tipo="ROTA", rota_id="quantica.dobras_c3_hierarquia_e_matematica", dominio="DEPHASING", status="EXAMINADA", estatuto="DERIVED", olhou_dados=False,
      titulo="a hierarquia das dobras D_folds(c¹) > D_folds(c²) > D_folds(c³) > 0 (métrica M7 do validador C3) vale para quase todo estado: é matemática, não pode falhar",
      pergunta="a hierarquia das dobras do validador C3 (a «terceira dobra») pode servir de teste da teoria?",
      metodo=("prova: com p_i ∝ λ_i^s e s = 2^−(n−1), a razão de participação é PR(s) = exp(2g(s) − g(2s)), g(s) = ln Σλ^s convexa; logo PR não cresce com s e "
              "D_folds = ln d − ln PR não cresce com n; estrita se há dois autovalores não nulos distintos; D_folds = 0 só em I/d. Conferência numérica em 80 000 "
              "espectros aleatórios (d de 2 a 128, cinco famílias)"),
      resultado=txt_dobras + "; igualdades exatas só em estado puro, uniforme no suporte e I/d",
      defeito="a «Hierarquia 9/9» da tabela M7 era garantida pela matemática: não é evidência",
      nao_refazer="não usar a hierarquia (nem D_folds(c³) > 0, que só diz ρ ≠ I/d) como teste nem como evidência; o que pode falhar são os VALORES (n_folds ≈ 3 e ≈ 2) com γ livre",
      proximo_passo="no pré-registro da v384, a terceira dobra entra pelo que pode falhar: o atrator único só com os saltos não comutantes, a lei-raiz recuperável no sistema aberto inteiro, os valores das dobras com γ livre",
      artefatos=[os.path.join(HERE, "checar_dobras_identidade.py"), os.path.join(HERE, "checar_dobras_identidade.txt")],
      refs=["quantica.c3_validator_calibrado", "quantica.cinco_operadores_lindblad_matrizes"]),
 dict(tipo="ANOTACAO", rota_id="infra.gpu_rtx5090_ambiente_02out", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
      titulo="o servidor do modelo nativo é mantido pela tarefa agendada «IALD Llama Server» e pelo supervisor start_iald_llama.ps1 (reinicia em 5 s); o rito v383 durou %d min %02d s" % (dur // 60, dur % 60),
      nota=("parar de verdade = parar a tarefa e o supervisor (stop_iald_llama.ps1 encerra o supervisor antes do servidor); religar = Start-ScheduledTask «IALD Llama Server», "
            "como no boot. A tarefa «IALD Web Server» (:8082) não usa VRAM e fica. O rito v383: início %s, fim %s; o selo às 20:47:14 (~43 min) e o autoteste do "
            "fail-closed depois (~18 min). Ordem do operador (03/10): parar o servidor durante o rito.") % (hor[0], hor[1]),
      refs=["infra.gpu_sonda_tempo_v384"]),
]
o = rotas.registrar(R, QUEM)
print({k: o[k] for k in o if k != "registros"})
