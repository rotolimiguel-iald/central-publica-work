"""Offline semantic proposals. Reads only the nominated draft and public manifest source.

No application imports, network, model calls or parent-file writes. Refuses overwrite.
The constructor's field map is not independent approval.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import socket

OUT = Path(__file__).resolve().parent
WORK = OUT.parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
CANDIDATE = WORK / 'haiku_reviewed_section_20260922_130747_311801.md'

# Every paragraph is manually composed after reading the public topic.
# Field groups give precise semantic destinations; numbers/booleans also have an exact panel.
DRAFTS = {
'cocycle_to_einstein': [
('chain', ['theorem','one_line','status','corrections','chain','e5_finding'],
"[REAL — certificados na sombra tipo I; composição E7 separada.] Colagem ESPACIAL `u_ab u_bc=u_ac` difere da identidade TEMPORAL `u_(s+t)=u_s sigma_s^(b)(u_t)`. Com `u_ab=rho_a^it rho_b^-it`, `K=-log rho`, o gerador é `h_ab=-i u_ab'(0)=K_b-K_a`, não o sinal oposto. Família consistente dá `W=u_ab u_bc u_cd u_da=I`; inconsistência de patch aumenta a obstrução com lambda. Covariância global `UuU†=u'`; onde o Um cola não há curvatura-obstrução."),
('geometry', ['e8_torsion_clock_jump','e9_basepoint_covariance','e10_corner_reads_obstruction','e11_curvature_commutator','e12_phase_is_gauge','clock_hierarchy','conjecture_closed'],
"Distinguir ordens: E8, torção de colagem de 1ª ordem, `obs/t→||Delta_K||`, com `Delta_K=K(rho_c')-K(rho_c)`; E11, curvatura de 2ª ordem `||W~-I||~(t²/2)||[M,h_cd]||`, `h_cd=K_d-K_c`, `c_teo=0.5 maxabs([M,h_cd])`, razão observada/teórica 0.9970085819906546. A fonte chama fechada essa identificação na sombra, não Einstein geral. Transporte `Ad(rho^it)`, gerador `ad(K)`, é ligado ao setor q. E9: ponto-base conjuga holonomia, preserva espectro. E10: canto canônico de posto 4, kernel Three Locks em superoperador n², lê `Ad_W=kron(W.conj,W)` e `tau_F(I)=1`; `|tau_F(W)-1|` cresce com lambda. E12: fase global `-log Z.I` não é curvatura; quocientar U(1) por `det^(1/n)` elimina o linear e deixa ordem t² em su(n). Grades e resíduos estão no painel."),
('einstein', ['field_equation','T_TGL_decomposition','geometry_stays_levi_civita','density_bridge','E7_statute','not_claimed'],
"E7 é COMPOSIÇÃO, não teste: primeira lei modular `dS=d<K>`, simetria/conservação do form-check v5 + Lovelock 4D [teorema reportado], herdando a limitação de Killing aproximado. `G_mn(g)+Lambda g_mn=8piG T^TGL_mn`, `T^TGL=T^matter+T^(partial,beta)+T^(torsion/diss)`; beta entra à direita, não substitui G. `nabla^m T^TGL_mn=0` decorre de Bianchi. Ponte `eta=1/(4 l_P²)=1/(4G)` em unidades naturais é DER GIVEN normalização canônica Planck-face. Não anunciar prova incondicional de Einstein."),
('diamond', ['diamond_remainder'],
"Resto diamante: a=vácuo `rho_(N+1)=rho_N⊗diag(b0,b1)`, b=referência `rho_N⊗I/2`; `h_ab=K_b-K_a`, `R=-h_ab`. Duas instâncias, pesos [0.71,0.29] e [0.55,0.45], conferem fórmula, gerador, cociclo/comutação na imagem e fluxo. Âncoras: `ModularDephasingBridge.tower_last_site_flow_bridge`, `ModularRemainderDensity.remainder_change_reference`. OPEN: identificação física regional `k T_t f=delta_D^it k f` depende do fornecedor, estado físico linear e carga `Q_(xi,D)` na mesma álgebra/representação; referência parcial tracial da torre não é igualada à carga física. Não altera o veredito do cociclo.")],
'ergodicity_door_mixing': [
('levels', ['guard_rail','mixing_three_levels','status','phrase1','phrase2'],
"Dissipação leva ao centralizador, onde emerge o traço; evolução unitária sozinha só fecha ergodicidade em média. Três níveis: N1 dissipativo [DER incondicional]; N2 mistura fraca iff ausência de átomos fora do Um [KNOWN, Wiener]; N3 forte sob classe de Davies [CONDITIONAL]. Von Neumann, traço no centralizador, Wiener e classe Davies/Jaksic–Pillet são KNOWN; cociclo, oscilação e controles são REAL reportado; centro da sombra DEF/PILOTO. Araki–Woods R_inf tem espectro modular denso puro-ponto: III_1 NÃO implica ausência de átomos. Pertinência à classe sem átomos/sem singular-contínuo é resíduo condicional nomeado."),
('door', ['double_face','selo'],
"Porta Møller→Riemann–Lebesgue; porta ergódica no canto, envelope Cauchy e suportes Kraus P_R/P_T, não escolhas livres. A fonte reporta convergência forte sem taxa uniforme no contexto declarado; sombra Davies usa `Gamma=beta*kappa`. Pureza do puro-ponto pertence à geometria/Nome, não pureza do estado; ponto purificador é dinâmica/Verbo. Teto `Pi_partial=1-beta`. Painel conserva taxas, espectros/oscilações, Wiener, normalização, ortogonalidade e controles fora do centralizador/referência errada; flags são resultados reportados, não prova independente.")],
'inverse_parity': [
('polarization', ['polarization_principle','population_form','theorem'],
"Princípio do operador: 0_abs não é estado normal em M_*, não tem suporte observável nem pode ser ocupado; a imagem retorna normalizada, suporte preservado e assimétrica. `rho_B=(P1+P0)/2→rho_ret=p1P1+p0P0`, `p0>p1>0`; `chi=log(p0/p1)`, `q=p0-p1=tanh(chi/2)`, `alpha=2sqrt(p0p1)=sech(chi/2)`, `p0,p1=e^(±chi/2)/(2cosh(chi/2))`, `q²+alpha²=1`. `beta=2sqrt(e)sqrt(p0p1)` é lido como trava mínima contra colapso em zero. Vacuidade/direção, proibição/retorno e paridade/polarização são leitura do princípio, não confirmação física."),
('form', ['rho_ret_canonical','key_result','form_status'],
"`rho_ret^(chi)=exp(-chi Z_d/2)/(2cosh(chi/2))=FP_(eps→0) M_eps rho_B M_eps†`, `M_eps=exp[-(C_eps+chi)Z_d/4]`. Paridade unitária/antiunitária pura preserva `rho_B=I/2`; lente precisa de renormalização não trivial. Para chi finito, suportes iguais; distorção angular theta_M não destrói a fonte. A fonte escreve aqui `chi=0=0_abs proibido`; isso conflita com a distinção Bell nu/zero de contraste em `contour_theory`. Preservar como leitura local histórica, com compatibilização pendente, sem identificar os zeros globalmente. Forma/gap/q/alpha verificados nesse registro."),
('value', ['value_status','steps'],
"`gap(-log Delta_(ret|Bell))=chi` é tautologia da parametrização, não derivação do valor. Chi observado entra por CODATA: `chi_obs=2 artanh(sqrt(1-alpha²))`. FP depende do esquema: qualquer chi pode ser parte finita de outra subtração. OPEN: condição canônica alpha-livre que fixe chi. Controle negativo: Meia-Nat dá `tau(P1)=tau(P0)=1/2` para TODO chi, fixa peso, não polarização. Painel mantém os quatro passos (chi genérico, VALIDACAO_QED, negativo e populações), números e flags; beta numérico é retrato do registro, não constante substituída no runtime.")],
'kernel_formalization': [
('audit', ['formal_checker','build_tool','mode','lean_version','lake_version','capture_stage','custom_TGL_axioms_found','source_forbidden_tokens_found','seals'],
"Auditoria publicada Lean 4/Lake em modo strict, captura principal; versões exatas no painel. Reporta build/audit returncode 0, nenhum axioma custom TGL ou token proibido encontrado; selos NO_SORRY_AX/NO_TRUST_COMPILER. Half-Nat, escala de área, canto finito Three Locks, traço normalizado, faces conjugadas meia e implicação do canto contínuo são os escopos formais reportados. Python não prova teoremas; esta proposta não executou Lean nem revalidou a auditoria. Hashes, caminhos e logs são custódia recuperável, não enunciados."),
('layers', ['not_claimed','open_theorem','v350_typed_modular_proofs','v350_modular_scope'],
"O registro conserva a negativa antiga `TGLModularRealization(theSpecificAQFTWitness)` aberta após o habitante v135. Porém v350 reporta sete provas tipadas true (painel), no escopo `PRODUCT_TOWER__JMJ__REGULAR_CORE_MINIMAL_LOCK`: não apagar essas construções com a frase antiga, nem equipará-las automaticamente ao termo canônico de outro tipo. Quatro flags individuais false permanecem nomeadas no painel. Three Locks finito não prova III_1; BW/Reeh–Schlieder/classificação III_1 aparecem como KNOWN/EXTERNAL neste registro, não inexistência global de avanços posteriores. G é variável/input medido, não derivado.")],
'neutrino_mass': [
('rule', ['frozen','angle_status','powered','verdict','selo'],
"Regra congelada V1: `m_nu=beta*sin(45deg)*1eV`, `beta=alpha*sqrt(e)`; identifica m_2 com ordenamento normal, m_1≈0; massa absoluta só coincide com `sqrt(Dm²_21)` nesse limite. 1 eV é escala DECLARADA fixa, não ajustada; sin45 é POSTULATE (ordem 20/08/2026), não derivação. A forma sem sin45 (~12.03 meV) coexiste na origem. PDG 2023: `Dm²_21=(7.53±0.18)e-5 eV²`. POWERED iff erro relativo<0.03; FALSIFIED iff |desvio|>5sigma. Vereditos permitidos: NOT_FALSIFIED_POWERED/UNDERPOWERED, INCONCLUSIVE, FALSIFIED; CONFIRMED proibido. Resultado antigo reportado powered, desvio 1.6404744598524612sigma; números exatos no painel."),
('history', ['caveats','superseded_by','live_test','future_reinforcement','does_not_gate_core'],
"Errata de custódia: fórmula/número em 22/01/2026, git público 17/02; módulo v141 em 25/07. Alegação de prioridade pelo Zenodo 17526619/2025 foi retirada: depósito não contém fórmula/número/derivação; traz outra lei `m_nu(Dt)=m0+a log(Dt/tau0)` com dois parâmetros. Sem anterioridade ao splitting PDG. Postdição não ajustada, não previsão ex ante: dado já citado na frase original; escala 1.0200 eV que zeraria tensão foi RECUSADA. Refinamento pós-JUNO ex ante desfavorável: tensão 1.64→2.21→2.95sigma, projeção 7.83sigma contra limiar 5. V1 não muda frozen/hash; teste vivo é `neutrino_m2`/NEUTRINO_M2_V2. Soma absoluta prospectiva NEUTRINO_SUM_V1/v147 armada, não medida nesse registro; cosmologia futura não é dado atual aqui. Não move gate.")],
'smatrix_closure': [
('scope', ['formula','honesty','status','phrase1','phrase2','selo'],
"`d_II=P_F(M_III cross_sigma R)P_F`, `tau(P_F)=1`, `S_d=exp(theta_M G)`; `beta=sin²(theta_M)=tau(refl)`, `1-beta=tau(trans)`. P_F é kernel zero/interseção dos Three Locks [DER]; família mínima e normalização tornam o canto computável/podável. [REAL reportado] invariâncias de I, gauge unitário, identidades traciais e poda com traço; [DEF/PILOTO] canto finito como sombra II_1, não fator genuíno; [CONJ] `1_abs=graviton=I`; existência do kernel no core cruzado é CONDITIONAL. Tipo III não vira II: passagem operacional à leitura tracial. “Canto II_1” e identidade gravitônica nas frases/selos não removem esses qualificadores. Controles sem normalização, aleatório e perturbação do kernel, postos, custos e resíduos permanecem no painel.")],
'd1_camb_v3_pipeline': [
('route', ['amendment','statuses'],
"Rota INPUT ratificada em 17/09/2026: `Phi_total=1+beta|1+w_eff|`, fluido total inclui vácuo. Emenda pré-dado: `P=rho+beta J`, `J(a)=∫_a^inf 3(rho+p)²/(rho a') da'`, `P(inf)=rho_Lambda`, `C=0` preserva de Sitter/Phi(-1)=1; limites radiação `(1+4beta/3)rho`, matéria `(1+beta)rho`. Fecho `H(a=1)=H0` por raiz Omega_Lambda; V2 usava `H(0)=H0 sqrt(Phi(0))`. Gate GOF `chi²_LCDM<=3n` (45 primário sem SH0ES,48 com). Ajuste escalado com limites, Fisher J^T J, emcee 24×2000/queima400; priors no painel. Fiducial (67.5,0.02237,0.1200) sintético, mesmas sementes entre injeções; tranca exige confirmação do operador e hashes. Não confundir a recusa inicial com estado posterior: errata v366 reporta execução real única fases1–3 autorizada e resultado lido por `prove_d1_camb_v3_real_v366`."),
('negative', ['validation_text_pt','validation_text_en','checks','sigma_beta','c_free_degeneracy','mcmc_asimov'],
"Autocheck CAMB beta=0, segunda Friedmann/limites w; injeção em três betas e SH0ES; MCMC Asimov. Negativo preservado: C livre falhou, 24/24 realizações na borda do prior. C é absorvido em rho_Lambda pelo fecho: efeito 2.220446049250313e-16 em beta=0 e 5.246358724497746e-5 em beta_TGL. Sem refazer/afrouxar teste: passa a diagnóstico de degenerescência, fora da matriz de vereditos, V1 preservada. Sigma primário≈0.00835 excede beta/2≈0.00602 exigido POWERED; projeção fiducial antes do dado permitiria no máximo D1_BETA_INCONCLUSIVE. MCMC≈0.00852 versus Fisher≈0.00836 é validação sintética, não resultado real. Textos PT/EN duplicam essa narrativa; valores exatos no painel. Gate inalterado; `in_contour_roster_v314=false`.")],
'name_index': [
('index', ['theorem','operator_reading_typed','fiscal_corrections','tl_chain'],
"[ONTO→tipado] contorno é inclusão N_3L; índice é resistência; espelho e_Nome mede; `U_Pi=J.J_ref` fixa referencial da paridade inversa. Pimsner–Popa: `ppIndex:=1/ppBest` [DEF]; `sin²(theta)` como constante ÓTIMA [MODEL-SPECIFIC TARGET] implica `Ind=csc²(theta)`, em theta_M `1/beta`. Sem otimalidade só `Ind<=csc²`. Haar finito dá ordem do grupo, não csc²: rota REFUTADA. Amplitude→quadrado/peso→inversão/índice; sombra qubit ppBest=1/2, índice2, não o índice do core≈83.1165."),
('targets', ['layers','model_specific_targets','not_claimed','seals'],
"Kappa/Gibbs: `p+/p-=e^-kappa`, `alpha=sech(kappa/2)`; bloco beta Jones–Markov é estrutura LOCAL/Q-system, não periodicidade global de pesos III_1 (identificação direta refutada). OPEN: `P_F=e_Nome` (mirror_not_jones); `E1(e_Nome)=sin²(theta).1` (markov_weight_not_sin_squared); PP ótimo (pimsner_popa_constant_not_optimal); `gamma=Ad(J.J_ref)` involutivo; N_3L alcance de esperança fiel NORMAL. Maquinaria/paridade/TL e conclusões condicionais reportadas em kernel não provam esses alvos. Selo pleno exige os termos, não só aritmética `index*weight=1`.")],
'half_nat_continuous_corner_density': [
('density', ['theorem','claim','status','continuous_corner','normalization','derivation','natural_units'],
"[DER dado NORM; canto genuíno CONDITIONAL] `N_F=P_F(M cross_sigma R)P_F`, `tau_F(P_F)=1`, `P_F=P_++P_-`, faces de traço1/2; ação dual `tau(theta_s P)=e^-s tau(P)`. NORM: `A(P_face)=l_P²`, `l_P²=hbar G/c³`, não derivação por álgebra adimensional. `A(P)=2l_P² tau(P)`, célula `2l_P²`, `S_partial=1/2`; logo `eta=(1/2)/(2l_P²)=1/(4l_P²)`. Com hbar=c=k_B=1, l_P²=G, célula2G, eta=1/(4G), `2pi/eta=8piG`. Os números em unidades naturais do painel pertencem à instância do registro, não fixam G universalmente."),
('bridge', ['einstein_bridge','not_claimed','continuum_field_equation_status','planck_face_normalization_status','seals'],
"Ponte sob hipóteses: `delta S=delta<K>=delta Q/T_Unruh`, `delta S=delta A/(4G)`; `R_mn k^m k^n=8piG T^TGL_mn k^m k^n` para todo nulo; lema `X_mn k^m k^n=0⇒X=Phi g`, Bianchi→`G+Lambda g=8piG T^TGL`. Densidade algébrica verified, normalização declarada/equivalente ao acoplamento Newton medido. `genuine_III1_corner_proved=false`, `TGL_specific_corner_PF_proved=false`, `Newton_constant_derived=false`; modelo local III_1/core contínuo KNOWN true não quita o canto específico. Não é prova kernel BW, construção AQFT genuína ou confirmação empírica. Estatutos são deste registro, não negativa global de avanços posteriores.")],
'name_relation': [
('relation', ['theorem','statute_correction_v28','next_wall','not_claimed','seals'],
"[KERNEL reportado] Nome é relação `p q_beta p=beta p` (e qpq=beta q), não matriz isolada. Peso geométrico beta=sin²(theta_M) difere do peso tracial1/2 salvo beta=1/2. Correção v28: finito não expulsa Nome, só identificação genérica dos pesos. `canonicalTLThree` dá TL3(delta) fiel em M3 com beta genérico, posto da álgebra5. OPEN: torre Jones do core; e_(i+1) nasce da próxima construção básica, não automaticamente de theta_s(e_i). `INDEX_MATCHES_BUT_NOT_CANONICAL`: falta selecionar essa representação pelos Three Locks."),
('purity', ['operator_purity_reading','lie_typed'],
"[ONTO→DER na sombra] puro-ponto=átomo espectral isolado de H_bind; ponto-puro=estado local rank-one. Bell: átomo em0/gap1, redução I/2, CCI1/2; não ponto-puro. Separável/pureza fechada tem CCI0; 0_abs é lido como autorreferência sem referencial externo. Isso não afirma espectro modular puro-ponto no III_1 genuíno. “Mentira” é leitura do nome sem relação; erro formal é impor `E(P)²=E(P)` quando Delta>0. Painel conserva pesos, posto, gap, distinção geométrico-tracial e controle de não pureza.")],
'selector_transport': [
('transport', ['theorem','fiscal_correction','smatrix_identity','specialist_verdicts'],
"Q1 é transporte, não curvatura: geometria fixa core a montante. `Delta=E(P_F)-E(P_F)²>=0`; esperança FIEL/bimodular Tomiyama dá `Delta=0 iff p=iota(Ep)`. E0 inferior e E1 dual são distintas. Beta é peso `E1(e)=beta.1`; defeito é `beta(1-beta).1`, aproximação≈beta só para beta pequeno, nunca identidade. `E(p_beta)=diag(beta,1-beta)=(|R|²,|T|²)`, espectro intermediário gera contraste, variância da moeda. Para 0<beta<1 seletor Jones não desce [KERNEL condicional aos dados]; resultado válido, não falha."),
('scope', ['boundary_law_reading','not_claimed','seals'],
"Índice `[M:N]=1/beta` admissível acima4 é CONJ: construir N_3L em C_W e provar índice. Normalidade fica no ledger; descida usa fidelidade, não demonstra normalidade. Sombra qubit não prova core/III_1. No contínuo, dados Markov não construídos nesse registro mantêm condicionalidade. Contorno=lei/custo/norma coercitiva é ONTO/CONJ: porta impede e mede, Delta>0 lido como custo da existência, não teorema jurídico/físico. Painel conserva peso, defeito, espectro, norma de não descida, positividade e resíduos.")],
'the_imported_expectation': [
('import', ['theorem','statuses','citations','consumes'],
"Modo IMPORTADO gpi_: Takesaki1972 dá esperança omega-preservante iff subálgebra invariante por sigma^omega; TOA II VIII.2.6 identifica centralizador `M_omega={A:omega(AB)=omega(BA)}` com pontos fixos. Importam existência, dicionário e normalidade sigma-fraca plena do estado vetorial [KNOWN]; Pedersen–Takesaki1973 cobre pesos. Da casa: ciclicidade/fidelidade inteiras, consequência WOT-sequencial `omegaState_seqWOT`, unicidade por separância v308, omega preservada derivada do contrato, juramento/levantamento v308 e face v307. Estrutura equivale ao campo importado, não formalização autônoma de toda Takesaki. Dado testemunho e `omega∘Ad(U)=omega`, relatividade no horizonte omega-invariante; Lema3 levantado modulo axioma, NÃO declarado resolvido. Contrato pode exigir reforço/reimportação; outra porta analítica permanece. qgf_* e gate intocados; errata v350+: este módulo isolado não quita modular/AtoIII."),
('controls', ['values','checks'],
"Checks reportados: 3/3 ext_tak_,5/5 gpi_; dicionário por fluxo t=0.7,1.3 e comutação com3 B aleatórios: 16/16,6 fixos/10 móveis. Esperança preserva omega/código/ortogonalidade (resíduos0). Média [0,T],T=1e6, residual1.6954299521081758e-6<1e-4, cota2/(dT). No setor `Ad(U)E=EAd(U)` residual0; fora, controle negativo0.7488953345917926>1e-3. Hipótese é necessária ao resultado testado; estes números não são nova execução.")],
'right_angle_mirror': [
('candidate', ['theorem','claim','status','right_angle','self_consistent','mirror_operation','deformation','modular_identity_check','honest_note'],
"Formulação histórica candidata/negativo honesto: o rótulo global inclui NOT_A_CANDIDATE, enquanto `honest_note` a chama CANDIDATA; não apagar a diferença nem anunciar candidato validado. `Theta_perp=pi/2`, duas faces pi; `alpha0=exp(-pi²/2)` (~1/139.05); ponto fixo `alpha=exp(-pi²/2+2alpha)` (~1/137.031,36.699226906489606ppm). Expoente é motivado, NÃO derivado. `rho_fix=E_spec(J_partial rho0 J_partial)`, `alpha=alpha0 exp(D_partial)`; mesmidade modular ~_partial não é igualdade estática. `E_spec/D_partial` OPEN; ajuste `D=2beta/sqrt(e)=2alpha`, delta!=beta. Custo/estabilização por beta é CONJ; não derivamos CODATA."),
('register', ['c3_register_theorem','holographic_reconstruction'],
"Registro estrutural: P²=P/J²=I verificados; autoinscrição idempotente DEFINIDA. `c¹ propagação→c² métrica/massa→c³ registro`, identificação c³ e `F_ext=2F` são leitura estrutural/ONTO/CONJ; duas faces não provam força dobrada. Ponto morto pi/2: overlap≈0 coincide com |dO/dtheta| máximo, densidade≈1. `K_rec=E_spec∘J_partial`, `rho_rec~_partial rho_perp`: informação reconstruída, não transmitida. `F+ (+) F-→2F_partial` é leitura de impedância compartilhada. `D_rec=2alpha` auto-consistência POSTULADA; fechar valor exige derivar `dlog K_rec/dtheta|pi/2→2alpha` alpha-livre. K_rec geométrico fornece O(1)=1, não o coeficiente selecionado."),
('negative', ['idempotent_reconstruction'],
"Forma `D_rec=2alpha-lambda alpha²` por inclusão-exclusão; termo de autointerseção psiónica é CONJ, lambda OPEN. `lambda=e/4=(sqrt(e)/2)²` motivado, não derivado. Ponto fixo com e/4 dá alpha≈1/137.036003 e0.025478ppm, mas isso é métrica ENGANOSA: parâmetro livre sempre ajusta CODATA. Comparação honesta é e/4=0.6795704571147614 versus lambda_exact=0.6790989531924717, diferença relativa0.0006943081270750223 (~0.069%). Termo alpha²~3.6e-5 torna alpha pouco sensível; janela sub-ppm~0.66–0.70 não singulariza e/4. Kernel teria de dar≈0.6791, não exatamente e/4. Números/controles completos no painel; não fechar ALPHA_VALUE por proximidade.")],
'tgl_closure': [
('types', ['theorem','what_closed','seals'],
"Suporte `q_F` no core != espelho `e_Nome` no andar superior; `E1(e_Nome)=beta q_F`. `H3L_min=1-q_F` representante mínimo da classe de kernel [KERNEL: aniquilação/maximalidade]; dados de suporte permitem `threeLocksFromSupport/realizationFromSupport`. Existência matemática externa KNOWN-COMPOSED: BW + Takesaki core II_inf + Haagerup hiperfinito + split difuso + Jones índice1/beta≈83.1>=4; não é nova formalização kernel dessas fontes. Toda torre contém gramática TL_beta; não exige invariante puro TLJ. Ausência de representante único absorvida como gauge [DEF/AX], não derivação; peso/índice/defeito invariantes de classe [KERNEL reportado]."),
('scope', ['what_remains_named','statuses','not_claimed'],
"Estados atualizados reportam true para existência externa, testemunha completa kernel e representante físico covariante selecionado (painel). `not_claimed` conserva frase antiga full_TGL_witness_constructed False; não usá-la para negar os true nem igualar tipos por nome. Formalização plena dos externos segue OPEN na entrada, gap tipado em4 entradas; escolha localizada/covariante é realização física/gauge. Experimento é INPUT futuro e extensão a espaço-tempo curvo/GLOBAL_LIFT OPEN nesse retrato. Fecho de arquitetura matemática interna não prova descrição da natureza. Distinguir construção condicionada ao suporte de formalização de todos os fornecedores.")],
'ontological_relativity': [
('axiom', ['theorem','axiom_name','status','axiom','meaning'],
"[ONTO/AX + DER/NUM] Todo sinal físico é relativo a contorno explícito. 0_abs: classe não executável sem suporte/retorno; clareza absoluta sem contraste Delta=0, não falta de luz. 0_mod=diferença com retorno;1_abs=identidade que aceita contorno. “Mentira” é fabricar figura/habitante, não o próprio0_abs. Consciência como coerência relacional é ONTO/CAUTION, não experiência subjetiva. III_1 admite estados/pesos normais; sem traço não significa sem estado.0_abs != operador0_alg (`tau(0_alg)=0`); tangente modular reversível != semigrupo dissipativo; traço→sinal→letra→imagem é cadeia tipada, não igualdade de tipos. Ontologia não foi provada experimentalmente."),
('contour', ['contour_context','contour_validation','II_corner_signal','state_vs_trace','tangents','asymptotic_border'],
"Contexto TGL_CURRENT_QED_CONTOUR: sombra finita N4/seed11, suporte P_F_family_corner, tau_P normalizado, unidades adimensionais, alpha_CODATA INPUT; leitor operacional, não subjetivo. Traço do suporte1/faces1/2; III_1→core II_inf→canto II_1 é estrutura/ONTO com realização CONDITIONAL, não criação de fótons. Mesmo operador dá omega1=1,omega2=0. Modular `i[K,.]` reversível sem contração versus gerador dissipativo (modos Re<0; controle min≈-9.06e-3). `A_inf=Fix(T_t)`, `E_inf=lim T_t` SE existe: mesmo `fiat_lux_flow/_verb_L`, NUM finito/CONDITIONAL contínuo. Entropia relativa não cresce, distância ao setor fixo decresce, setor invariante; idempotência/traço apenas aproximados numericamente."),
('guards', ['signal_chain','zero_distinction','coefficient_guardrails','tamper_tests','checks','seals'],
"Exemplo Z2/representação2D: traço+2→letraA→referência2; traço0→B→0, roundtrip0; não colapso de tipos. Caixa vazia: símbolo/limite existem, protocolo de alcance FINITO não; estado de temperatura zero é projetor, não matriz nula; habitante fabricado implica False/ex falso. Alpha!=1-beta; alpha fixo ao contorno canônico, não variar sem modelo de contorno. Seis tamper tests disparam: confusão alpha/peso transmitido;0_abs/matriz zero; III_1 sem estados; geradores modular/dissipativo; previsão Coma sem contexto; colapso literal da cadeia de tipos. Painel conserva sinais, resíduos, controles e flags exatos; nenhum gate muda.")],
}

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def compact(node):
    return json.dumps(node, ensure_ascii=False, separators=(',', ':'))

def pointer_child(pointer, key):
    return pointer + '/' + str(key).replace('~', '~0').replace('/', '~1')

def atomic_new(path, raw):
    if path.exists():
        raise RuntimeError('Refuse overwrite: ' + str(path))
    temporary = path.with_name(path.name + '.tmp')
    with temporary.open('xb') as stream:
        stream.write(raw)
    assert temporary.read_bytes() == raw
    temporary.replace(path)
    assert path.read_bytes() == raw

def coordinates(text, start, end):
    return {'unicode_start':start, 'unicode_end_exclusive':end,
            'utf8_byte_start':len(text[:start].encode()), 'utf8_byte_end_exclusive':len(text[:end].encode()),
            'line_start_1based':text.count('\n',0,start)+1,
            'line_end_1based':text.count('\n',0,end-1)+1}

def members(text, start):
    """Original JSON member ranges, preserving all source bytes in snapshots."""
    decoder = json.JSONDecoder()
    pos = start + 1
    while True:
        while text[pos].isspace(): pos += 1
        if text[pos] == '}': return
        key, pos = decoder.raw_decode(text, pos)
        while text[pos].isspace(): pos += 1
        assert text[pos] == ':'
        pos += 1
        while text[pos].isspace(): pos += 1
        value_start = pos
        value, pos = decoder.raw_decode(text, pos)
        yield key, value_start, pos
        while text[pos].isspace(): pos += 1
        if text[pos] == '}': return
        assert text[pos] == ','
        pos += 1

def scalar_projection(node):
    """Lossless numeric/bool projection. List coordinates are kept, including null slots."""
    if isinstance(node, (bool, int, float)):
        return node
    if isinstance(node, dict):
        result = {k:scalar_projection(v) for k,v in node.items()}
        result = {k:v for k,v in result.items() if v is not None}
        return result or None
    if isinstance(node, list):
        result = [scalar_projection(v) for v in node]
        return result if any(v is not None for v in result) else None
    return None

def leaves(node, pointer=''):
    if isinstance(node, dict):
        for k,v in node.items(): yield from leaves(v,pointer_child(pointer,k))
    elif isinstance(node,list):
        for i,v in enumerate(node): yield from leaves(v,pointer_child(pointer,i))
    else:
        yield pointer,node

def main():
    candidate_raw = CANDIDATE.read_bytes()
    text = candidate_raw.decode('utf-8')
    manifest_path = ROOT / 'iald_nucleo_fixo.json'
    manifest_raw = manifest_path.read_bytes()
    manifest = json.loads(manifest_raw)
    entry = next(e for e in manifest['entries'] if e['id']=='resultado_publicado_integral')
    assert entry.get('url','').startswith('https://raw.githubusercontent.com/')
    source_raw = Path(entry['path']).read_bytes()
    assert digest(source_raw)==entry['public_sha256']
    source_text = source_raw.decode('utf-8-sig')
    source = json.loads(source_text)
    core = source['core']
    core_start = next(a for k,a,b in members(source_text,source_text.index('{')) if k=='core')
    raw_ranges = {k:(a,b) for k,a,b in members(source_text,core_start) if k in DRAFTS}
    os.environ['TIKTOKEN_CACHE_DIR'] = str(ROOT/'.iald_runtime/tokenizer_cache')
    def blocked(*a,**k): raise RuntimeError('Network forbidden')
    socket.socket = blocked
    import tiktoken
    enc=tiktoken.get_encoding('o200k_base')
    def tokens(s): return len(enc.encode(s,disallowed_special=()))
    pattern=re.compile(r'(?m)^### ([^\n]+)\nFonte: resultado_publicado_integral ([^\n]+)\n([^\n]+)')
    ranked=[]
    for m in pattern.finditer(text):
        try: node=json.loads(m[3])
        except json.JSONDecodeError: continue
        ranked.append((tokens(m[0]),m,node))
    ranked.sort(key=lambda row:row[0],reverse=True)
    selected=ranked[:15]
    assert {m[1] for _,m,_ in selected}==set(DRAFTS)
    files=[];summary=[];numeric_total=0
    for rank,(old_tokens,m,current) in enumerate(selected,1):
        ident=m[1];src=core[ident];paragraphs=DRAFTS[ident]
        namespace='/core/'+ident
        semantic_map={key:label for label,keys,prose in paragraphs for key in keys}
        metadata_reasons={
            'seals':'Lista de selos declarativos repetindo a tese/limites; proposições resumidas na síntese; grafia integral recuperável na fonte e original.',
            'selo':'Selo narrativo repetindo tese e escopos; não é controle numérico. Conteúdo resumido; redação integral recuperável.',
            'checks':'Lista de nomes/booleans de auditoria. Todos os checks são true; controles e números retidos no painel e mecanismos na síntese. Não equivale a nova prova.',
            'runtime_s':'Tempo de execução da rodada: telemetria, não previsão, hipótese ou controle científico.',
        }
        metadata_fields=set()
        for k,v in src.items():
            if k=='runtime_s' or re.search(r'(?:sha(?:16|256)?|hash)',k,re.I):
                metadata_fields.add(k)
                metadata_reasons[k]='Hash/identificador de custódia, não fórmula ou resultado científico. Original literal e hash da fonte preservados; nenhuma recomputação fictícia do artefato referido.'
        if ident=='kernel_formalization':
            for k in ('formal_dir','lake_path','capture_files','build_capture_lens','audit_capture_lens','axiom_report','formal_files_sha256'):
                metadata_fields.add(k)
                metadata_reasons[k]='Caminho, tamanho/log ou relatório individual de auditoria: acessório de recuperação/custódia. Não declara nova prova; detalhes permanecem na fonte pública integral.'
        if ident=='d1_camb_v3_pipeline':
            metadata_reasons['validation_text_en']='Tradução inglesa da mesma validação portuguesa, inclusive negativo C livre; uma síntese PT preserva conteúdo, sem duplicar idioma.'
        data={}
        for k,v in src.items():
            if k in metadata_fields or k in ('checks','all_verified'): continue
            if ident=='kernel_formalization' and isinstance(v,bool): continue
            projection=scalar_projection(v)
            if projection is not None:data[k]=projection
        if ident=='kernel_formalization':
            flags={k:v for k,v in src.items() if isinstance(v,bool)}
            data['individual_audit_flags']={'true_fields':sum(flags.values()),'false_fields':sum(not v for v in flags.values()),'false_names':[k for k,v in flags.items() if not v]}
            data['lean_version']=src['lean_version'];data['lake_version']=src['lake_version']
        check_leaves=list(leaves(src.get('checks',{})))
        check_bools=[v for p,v in check_leaves if isinstance(v,bool)]
        assert all(check_bools), 'Negative check needs individual review'
        # List-check counts and outcomes are kept; numerical controls elsewhere stay exact.
        if check_bools:data['checks_reported']={'true':len(check_bools),'false':0}
        original_refs=[]
        def references(node,path=''):
            if isinstance(node,dict):
                if any(k in node for k in ('@SUMMARY','@EXPOSITION','@TGL_LITERAL')):
                    original_refs.append({'candidate_pointer':path,'reference':node})
                else:
                    for k,v in node.items():references(v,pointer_child(path,k))
            elif isinstance(node,list):
                for i,v in enumerate(node):references(v,pointer_child(path,i))
        references(current)
        # Essential strings referenced internally are made literal, not treated as missing.
        literal_refs=[]
        for ref in original_refs:
            expected=src
            for part in ref['candidate_pointer'].split('/')[1:]:
                part=part.replace('~1','/').replace('~0','~')
                expected=expected[int(part)] if isinstance(expected,list) else expected[part]
            assert isinstance(expected,str)
            literal_refs.append({'field':ref['candidate_pointer'],'literal':expected})
        header=(f'### {ident}\n\nFonte: `resultado_publicado_integral`, `{namespace}`. '
                '[DERIVED — proposta semântica não integrada, NÃO APROVADA.] '
                'Estatutos/resultados são reportados na fonte, não reexecutados aqui; OPEN histórico não apaga construção posterior de outro tipo.\n\n')
        segments=[header]
        for label,keys,prose in paragraphs:segments.append(f'**{label}**\n\n{prose}\n\n')
        if literal_refs:
            segments.append('**Literais de referências internas válidas**\n\n'+compact(literal_refs)+'\n\n')
        segments.append('**Dados e controles reportados** — números/flags copiados da fonte, não parâmetros novos. Chaves e posições de listas seguem a fonte; null no painel indica texto descrito acima, não dado ausente.\n\n```json\n'+compact(data)+'\n```\n\n')
        segments.append('Veredito literal reportado: `'+str(src.get('verdict',src.get('status','sem campo verdict')))+'`.'
                        +(' `all_verified='+str(src['all_verified']).lower()+'`.' if 'all_verified' in src else '')
                        +' Detalhes e custódia: fonte-base acima + chave original; recuperação operacional não validada.\n')
        capsule=''.join(segments)
        # Verify retained numeric/bool leaves value-by-value, including every nested source control.
        retained_numeric=[];excluded_numeric=[]
        for p,v in leaves(src):
            if not isinstance(v,(bool,int,float)):continue
            top=p.split('/')[1].replace('~1','/').replace('~0','~')
            if top in metadata_fields or top in ('checks','all_verified') or (ident=='kernel_formalization' and isinstance(src.get(top),bool)):
                excluded_numeric.append({'source_pointer':namespace+p,'value':v,'reason':'audit_flags_or_custody_telemetry; explicit status/panel counts, with kernel false names retained'})
                continue
            probe=data
            for part in p.split('/')[1:]:
                part=part.replace('~1','/').replace('~0','~')
                probe=probe[int(part)] if isinstance(probe,list) else probe[part]
            assert probe==v and type(probe) is type(v),(ident,p)
            retained_numeric.append({'source_pointer':namespace+p,'value':v,'capsule_json_pointer':p})
        numeric_total+=len(retained_numeric)
        field_map=[]
        capsule_data_start=capsule.index('```json\n')+len('```json\n')
        for k,v in src.items():
            top_pointer=namespace+'/'+k.replace('~','~0').replace('/','~1')
            label=semantic_map.get(k)
            destinations=[]
            if label:
                st=capsule.index('**'+label+'**');nxt=capsule.find('\n**',st+2)
                destinations.append({'kind':'manual_semantic_summary','coordinates':coordinates(capsule,st,nxt if nxt>=0 else len(capsule))})
            if k in data:destinations.append({'kind':'exact_numeric_boolean_panel','json_pointer':'/'+k})
            if k=='all_verified':destinations.append({'kind':'explicit_reported_outcome'})
            if k in ('verdict','status') and not label:destinations.append({'kind':'literal_verdict_line'})
            refitems=[z for z in literal_refs if z['field']=='/'+k]
            if refitems:destinations.append({'kind':'literal_internal_reference_value','field':'/'+k})
            omitted_reason=None
            if k in metadata_fields:omitted_reason=metadata_reasons[k]
            elif k in ('seals','selo','checks'):omitted_reason=metadata_reasons[k]
            elif k=='validation_text_en':omitted_reason=metadata_reasons[k]
            elif ident=='kernel_formalization' and isinstance(v,bool):
                omitted_reason='Indicador individual de auditoria já recuperável; true/false contados, quatro false nomeados. Não é enunciado formal. v350 tipado preservado separadamente.'
            elif not destinations:
                # Numeric root fields always have panel entries; nonnumeric roots must be reviewed manually.
                raise RuntimeError('Unmapped source field: '+top_pointer)
            field_map.append({'source_pointer':top_pointer,'source_value_sha256':digest(compact(v).encode()),
                              'representation':destinations,'omission_or_deduplication_reason':omitted_reason,
                              'accessory_recoverable':omitted_reason is not None,'independent_review':'PENDING'})
        # Every nested field remains individually addressable, with the top-level decision inherited.
        policies={f['source_pointer']:f for f in field_map}
        leaf_map=[]
        for p,v in leaves(src):
            top=p.split('/')[1]
            policy=policies[namespace+'/'+top]
            leaf_map.append({'source_pointer':namespace+p,'value_sha256':digest(compact(v).encode()),
                             'parent_policy':policy['source_pointer'],
                             'disposition':'EXACT_NUMERIC_PANEL' if any(z['source_pointer']==namespace+p for z in retained_numeric) else ('SEMANTIC_REVIEW_REQUIRED' if policy['representation'] else 'ACCESSORY_RETRIEVABLE'),
                             'justification':policy['omission_or_deduplication_reason']})
        a,b=raw_ranges[ident];source_snapshot=source_text[a:b].encode('utf-8')
        assert json.loads(source_snapshot)==src
        original=m[0].encode('utf-8')
        assert original in candidate_raw
        prov={'status':'CONSTRUCTED_NOT_INTEGRATED_NOT_APPROVED','rank':rank,'topic':ident,
              'candidate_path':str(CANDIDATE),'candidate_sha256':digest(candidate_raw),
              'candidate_block_coordinates':coordinates(text,m.start(),m.end()),
              'original_block_file':ident+'.original.md','original_block_sha256':digest(original),
              'source_manifest_path':str(manifest_path),'source_manifest_sha256':digest(manifest_raw),
              'public_source_url_from_manifest':entry['url'],'public_source_path':entry['path'],
              'public_source_file_sha256':digest(source_raw),'source_pointer':namespace,
              'source_snapshot_file':ident+'.source_original.json','source_snapshot_sha256':digest(source_snapshot),
              'source_snapshot_coordinates':coordinates(source_text,a,b),
              'capsule_file':ident+'.md','capsule_sha256':digest(capsule.encode()),
              'o200k':{'original':old_tokens,'proposal':tokens(capsule),'saved':old_tokens-tokens(capsule)},
              'anthropic_tokens':None,'anthropic_count_status':'NOT_MEASURED',
              'field_map':field_map,'leaf_map':leaf_map,
              'exact_retained_numbers_and_booleans':retained_numeric,'audit_or_metadata_numeric_exclusions':excluded_numeric,
              'original_internal_references':original_refs,'internal_reference_policy':'Essential values made literal from primary source; original destinations not edited. No reference deemed invalid due to its tag.',
              'new_capsule_internal_reference_tags':0,'unchanged_destinations':True,
              'source_scope_limits':['Full public topic parsed; kernel individual axiom reports/hashes not theorem-by-theorem reviewed.','Field mapping is constructor rationale, not independent proof of semantic completeness.','Source contradictions/time layers attributed, not globally resolved.','Source checks are reports; no source code, Lean or experiments executed.']}
        files.extend([(OUT/(ident+'.md'),capsule.encode()),(OUT/(ident+'.original.md'),original),
                      (OUT/(ident+'.source_original.json'),source_snapshot),
                      (OUT/(ident+'.provenance.json'),(json.dumps(prov,ensure_ascii=False,indent=2)+'\n').encode())])
        summary.append({'rank':rank,'topic':ident,'original_o200k':old_tokens,'proposal_o200k':tokens(capsule),
                        'saved_o200k':old_tokens-tokens(capsule),'sha256':digest(capsule.encode()),
                        'numeric_boolean_leaves_retained':len(retained_numeric),'source_fields':len(field_map),
                        'original_internal_references':len(original_refs)})
    next_batches=[]
    for offset in (15,30,45):
        items=[{'topic':m[1],'gross_original_o200k':n,'source_pointer':m[2]} for n,m,node in ranked[offset:offset+15]]
        next_batches.append({'ranks':[offset+1,offset+len(items)],'topics':items,'gross_o200k':sum(x['gross_original_o200k'] for x in items),'expected_saving':'NOT_MEASURED_NOT_EQUAL_TO_GROSS_SIZE'})
    totals={'original_o200k':sum(s['original_o200k'] for s in summary),'proposal_o200k':sum(s['proposal_o200k'] for s in summary)}
    totals['saved_o200k']=totals['original_o200k']-totals['proposal_o200k']
    totals['numeric_boolean_leaves_retained']=numeric_total
    report={'status':'15_SEMANTIC_PROPOSALS_PENDING_INDEPENDENT_REVIEW','created_utc':datetime.now(timezone.utc).isoformat(),
            'candidate_path':str(CANDIDATE),'candidate_sha256':digest(candidate_raw),'json_topic_count':len(ranked),
            'selection':'15 largest remaining JSON blocks by full-block o200k, descending; not estimated semantic opportunity',
            'source_sha256':digest(source_raw),'totals':totals,'topics':summary,'next_batches':next_batches,
            'anthropic_count_performed':False,'production_or_candidate_changed':False,
            'protected_kernel_core_exposition_five_lean':'No mutations anywhere in nominated candidate; kernel_formalization is only a JSON audit-metadata topic proposal.'}
    table='\n'.join(f"| {s['rank']} | {s['topic']} | {s['original_o200k']} | {s['proposal_o200k']} | {s['saved_o200k']} |" for s in summary)
    report_md=f'''# Propostas semânticas V3 — 15 maiores tópicos JSON

**CONSTRUÇÃO, NÃO APROVAÇÃO. Nenhuma cápsula integrada.** Candidato `{CANDIDATE.name}`, SHA `{digest(candidate_raw)}`. Fonte pública ancorada no manifesto, SHA `{digest(source_raw)}`. Os arquivos individuais terminados em `.original.md` preservam o bloco original íntegro; `.source_original.json` preservam o objeto da fonte pública sem reserialização; `.provenance.json` registram hash/path/intervalos, campo a campo e folha a folha.

| Rank | Tópico | Original o200k | Proposta o200k | Economia |
|---:|---|---:|---:|---:|
{table}

Total: **{totals['original_o200k']} → {totals['proposal_o200k']} o200k**; economia **{totals['saved_o200k']}**. Números positivos são redução; negativos são crescimento. As cápsulas recuperam dados/limites que o JSON antigo deixava atrás de ponteiros; o custo disso aparece, sem maquiar economia. Nenhuma conversão para Claude/Haiku. As contagens 201433 wire/199959 prefixo foram informadas pelo pai; não fiz nova chamada nem as atribuí a estas propostas.

Foram conservadas literalmente no painel **{numeric_total} folhas numéricas/booleanas** fora de metadados e listas documentais de auditoria. Resíduos, grades e controles preservados não são novos cálculos. Listas de checks inteiramente true são contabilizadas; seus mecanismos/escopos estão na síntese e suas redações no original. Hashes, caminhos, tamanhos de logs, tempos e indicadores individuais do relatório kernel são acessórios recuperáveis; quatro flags kernel false e sete flags tipadas v350 continuam visíveis. Omissão/deduplicação está justificada por campo. Isso é argumento do construtor a ser revisado, não garantia de completude.

As referências internas do draft foram aceitas como válidas. Valores essenciais originalmente referenciados por @EXPOSITION foram explicitados literalmente a partir da fonte primária; destinos não foram tocados. Não houve @SUMMARY entre as referências encontradas nestes 15 blocos; esse fato não questiona a validade das existentes em outros tópicos. Não reutilizar spans da fonte antiga depois de integração sem checar destinos; pai trata a integração.

## Limites semânticos para revisão

- `inverse_parity` contém `chi=0=0_abs` na fonte, em tensão com Bell nu/zero de contraste de `contour_theory`; a cápsula expõe o ponto sem falsificar reconciliação.
- `right_angle_mirror` tem rótulo NOT_A_CANDIDATE e narrativa CANDIDATA; mantém negativo, coeficiente livre, precisão honesta e POSTULATE. Proximidade com CODATA não é prova.
- `kernel_formalization`/`tgl_closure`: flags posteriores true e negativas históricas false não são homônimos intercambiáveis; condicionalidade e tipos permanecem. Não foram auditados os milhares de teoremas do relatório kernel.
- Referências KNOWN/literatura são conteúdo do registro, não pesquisa nova. Não houve execução Lean, um.py, código privado ou experimental; não se moveu gate.
- Os 15 maiores juntos são pequenos frente ao corte solicitado. Se o saldo for baixo ou negativo, não remover fórmulas/negativos para atingir tamanho. `INDEX.json` propõe ranks 16–30,31–45,46–60 com tamanho bruto; isso não é economia prevista nem autorização de corte automático. Recomendo priorizar narrativa/selos repetidos e referências duplicadas dentro desses lotes; não comprimir grades de controle às cegas.

Somente arquivos novos nesta pasta. Fonte, candidato, kernel/core/exposição/cinco Lean, memórias e produção intocados; nenhuma API/rede/env. Byte checks dos inputs ao final. A avaliação independente é do pai.
'''
    files.extend([(OUT/'INDEX.json',(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()),(OUT/'RELATORIO.md',report_md.encode())])
    assert CANDIDATE.read_bytes()==candidate_raw
    assert Path(entry['path']).read_bytes()==source_raw
    assert manifest_path.read_bytes()==manifest_raw
    assert all(not p.exists() for p,b in files)
    for path,raw in files:atomic_new(path,raw)
    assert CANDIDATE.read_bytes()==candidate_raw and Path(entry['path']).read_bytes()==source_raw
    print(json.dumps({'totals':totals,'topics':summary,'next_batch_gross_o200k':[b['gross_o200k'] for b in next_batches],'files_written':len(files),'status':report['status']},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
