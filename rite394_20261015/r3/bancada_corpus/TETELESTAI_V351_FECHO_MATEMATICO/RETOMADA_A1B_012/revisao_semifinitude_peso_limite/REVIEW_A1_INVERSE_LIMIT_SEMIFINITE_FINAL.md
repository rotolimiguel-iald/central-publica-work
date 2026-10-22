2026-09-14T23:34:20.794691-03:00

**A1_INVERSE_LIMIT_SEMIFINITE_REVIEW_ACCEPTED__TRACIAL_FINITE_MINORANTS_OPEN**

[REAL] **Sem achados P0/P1/P2.** Três teoremas públicos + um helper privado; módulo completo e auditor próprios rc0. Três #check com universos e axiomas exclusivamente do trio permitido. Aceite limitado aos tipos efetivamente verificados.

[REAL — tipos e objeto] Três teoremas públicos, nenhum def novo. O domínio inicial é a : scalarWeightLeftIdeal P do MESMO ν; δ>0 é explícito. A primeira conclusão avalia scalarInverseLimitWeight P (TGLV351.positiveSquare P (a.val * regularDomainCut P δ)) e fornece a cota ENNReal.ofReal(δ⁻¹)·ν(a*a), uniforme no regulador ε da definição do limite. A segunda conclui <⊤. A terceira identifica o fecho WOT do conjunto de operadores de N com quadrado finito para esse MESMO peso limite com N inteiro, sem antecedente extra sobre P.

[REAL — ordem correta] Para cada ε=1/(n+1), s é a raiz ORIGINAL hilbertPositiveSqrt(Bε), q=qδ e b=q s. A pertença b∈E usa as pertenças já provadas de q e s, e c=√(δ⁻¹)I também pertence a E. O cálculo é bb*=q(ss*)q=q Bε q=Bε q²≤δ⁻¹I=cc*. Usa apenas q auto-adjunto e sua comutação com Bε; não comuta a com q ou s, não supõe comutação de a com Bε e nem necessita provar q s=s q neste argumento. scalarWeight_right_perturbed_mono recebe precisamente bb*≤cc* e a∈nν. A desigualdade de pesos não é inferida por ordem falsa dos sanduíches.

[REAL — supremum, finitude e Haar] A igualdade entre o corte do quadrado de aq e ν(b* a*a b) é associatividade/estrela no CLM, transportada por congrArg explícito de dualQuadraticIntegral. Para c, homogeneidade existente e δ>0 dão o fator real δ⁻¹; ←Complex.ofReal_inv resolve a coerção, sem trocar ℝ por uma ordem complexa indevida. A cota é independente de n, logo iSup_le a passa ao limite. ENNReal.mul_lt_top consome ofReal finito e a.property; não converte valor infinito com toReal. Mesmo dualQuadraticIntegral, regularVacuum e normalização Haar herdados, sem redefinição ou fator novo.

[REAL — densidade WOT e não circularidade] Para cada a∈nν, aq_(1/(n+1)) pertence ao conjunto square-finite de τ pela segunda conclusão e converge fortemente a a pelo teorema de q_n já entregue; a multiplicação à esquerda usa apenas continuidade do CLM fixo a. strong_tendsto_wot e mem_closure_of_tendsto colocam todo nν no fecho WOT desse conjunto. closure_mono, o ANTIGO scalarWeight_square_finite_wot_closure de ν e closure_closure dão N⊆fecho. O sentido contrário usa somente a WOT-fechadura de N. Não se pressupõe semifinitude de τ, não se identifica nτ com nν e não se postula uma família de minorantes positivos finitos de ν.

[REAL — auxiliar e fornecedores antigos] O único helper privado hilbert_sqrt_mul_star é genérico em Hilbert complexo completo e consome CFC.sqrt_nonneg/sqrt_mul_sqrt_self para ss*=B. Seus axiomas são auditados transitivamente pelas três conclusões. V350FixedBaseEquivalence, V351ExtendedBaseDualWeight e V351ScalarWeightSemifiniteness foram copiados de OLD/kernel após igualdade de bytes OLD=K; construídos do fonte em V, com 5+14+2 prints antigos, todos permitidos. São três fornecedores adicionais, não novos resultados. Não se instalou objeto autoral ou DEV nem se refez o GNS.

[REAL — ficha e histórico] Ficha 23:10:26 antecede a primeira tentativa e reutiliza a busca de seis modalidades da ficha25, cujo consumidor já era a densidade do domínio de τ. As sete entradas de fornecedores foram verificadas por linha, enunciado e hash. O adendo 23:14:09 documenta a reprodução antiga já feita e é posterior ao primeiro DEV; não foi apresentado aqui como anterior a todo código. Quatro DEV rc1 foram preservados/excluídos: congr1/timeout, tentativa instrumentada, homogeneidade/isDefEq e cast de inverso complexo; o final 23:20:29 passou limpo. Os pins históricos apontam a snapshots reais, com localização viva apenas como texto. A auditoria autoral standalone rc0 e a recusa Type mismatch do negativo BadLimitSemifiniteInfiniteCut foram relidas/pinadas, sem reexecutar o negativo.

[REAL — proveniência] 690 objetos próprios anteriores preservados; 5 novos objetos construídos (três fornecedores antigos + alvo + auditor), total 695. Run próprio rc0 em 86.683 s; zero avisos do alvo/auditor, 178 mensagens de fornecedores com origem separada no JSON. Traces de compilação restringem LEAN_PATH a V e seus pacotes. Cache de pacotes pinado/herdado; quantidade total de jobs do Lake não é quantidade de recompilações. Stderr completo preservado, inclusive aviso herdado do pacote aesop, se presente.

| Artefato | SHA256 lido |
|---|---|
| Fonte final (K=cópia própria) | 0af32fbe3a7f0a36ef61f8e247c24a6117fab4f2b2b778890492b21e13f2f7a1 |
| .olean próprio | 2cdab1103e507815974946e215d6fea11ed5c4c54ecd9808d0bd9c57fb1f453c |
| .olean autoral standalone (só comparação) | 2cdab1103e507815974946e215d6fea11ed5c4c54ecd9808d0bd9c57fb1f453c |

Igualdade binária medida do alvo: True.

| Fornecedor antigo | Igualdade fonte OLD=K=V | .olean próprio = autoral |
|---|---|---|
| TGLExt.V350FixedBaseEquivalence | True | True |
| TGLExt.V351ExtendedBaseDualWeight | True | True |
| TGLExt.V351ScalarWeightSemifiniteness | True | True |

[OPEN — limites] Aceite26: três teoremas públicos, um helper privado transitivo, zero definições; os três fornecedores antigos e seus 21 prints são contados separadamente. P é o mesmo SiteProfile; δ>0 e a∈nν são hipóteses da estimativa/finitude, descarregadas na sequência usada para a densidade. A cota depende de δ, não de ε; não se afirma finitude de τ(a*a) para todo a∈nν. Com as leis de peso/normalidade anteriormente aceitas, o fecho WOT aqui provado é o critério usual de semifinitude do MESMO scalarInverseLimitWeight. Não é prova de tracialidade nem do campo finite-positive-minorants de RegularCoreTraceData; não é entrega do traço completo A1(b). Nenhuma afirmação de convergência em norma de operadores, gap, novo GNS, igualdade de domínios algébricos ou núcleo analítico inteiro. Não foram examinadas novas rotas de tracialidade nesta revisão. Somente V e esta pasta de revisão receberam novas saídas. K, OLD, pareceres/pins anteriores, memórias, writers e monólito preservados; pacote Mathlib e objetos próprios anteriores herdados com limites explícitos.

Artefatos de evidência:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\compilation.json>) — SHA256 91b40c91a49aedb81dcb6dbbea20f1365fb4b00b029f459d78e18af30d5318f4.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\independent_20260914_232652_905782\run.json>) — SHA256 816fe0b6669b3e30f365779cafe82ad51c5a84b45d0342e746d0a5d2dfd9b86b.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\independent_20260914_232652_905782\type_axiom_audit.json>) — SHA256 6dd36b1a81acc1a54c1793183047eb9fc7adf609737818eca270888f285d7e2f.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\history_read.json>) — SHA256 0b92dbba85ebc8c0b08188914c94d7f69fec84ab12d3c2be139c657623576658.
- [fornecedores](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\old_suppliers_read_v2.json>) — SHA256 fb48b14b2a255b21a9baca04a1b8b9d30bf7c04250ae60639820bd256c4a4279.
