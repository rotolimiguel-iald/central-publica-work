# Interação local geral: cociclo e dinâmica sem comutação par a par

[REAL — escopo compilado] Cinco fontes novas, **82 teoremas e 17 outras declarações**, com 99 termos auditados. O núcleo geral passou na primeira build (quatro folhas + agregador, cinco processos). A testemunha passou em build separada (uma folha + agregador, dois processos), preservando o primeiro diagnóstico e seu backup. Todas as execuções aceitas terminaram com exit 0, sem avisos e com axiomas apenas em propext, Classical.choice e Quot.sound. Nenhum um.py foi executado ou importado.

## O contrato e a dedução

[LocalInteractionData](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionData.lean:12>) recebe um perfil canônico P e uma sequência de operadores efetivos. Exige auto-adjunção de cada termo, suporte do termo j no andar j+1 e somabilidade de Σ‖term j‖. Não recebe comutação entre termos, pertença ao centralizador, cociclo pronto, dinâmica perturbada pronta ou estado novo.

O prefixo V_N soma os termos j<N. Como j+1≤N, ele pertence ao andar N. A somabilidade absoluta constrói V=Σ′term j e o limite dos prefixos. O potencial e os prefixos são auto-adjuntos e pertencem ao fator; a norma é limitada por Σ‖term j‖. A cauda e_N=Σ′‖term(j+N)‖ é não negativa, antítona e tende a zero, com ‖V−V_N‖≤e_N. A continuidade em norma da órbita α_t(V) é derivada por aproximação uniforme pelas órbitas locais finitas, não presumida para todos os operadores.

Referências: [local_prefix_mem_level](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionData.lean:30>), [local_prefix_tendsto](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionData.lean:53>), [local_potential_selfadjoint](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionData.lean:57>), [local_cutoff_error](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionData.lean:88>), [norm_tail_tendsto](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionData.lean:108>), [local_orbit_continuous](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionData.lean:151>).

Para cada corte, u_N(t)=exp(it(H_N+V_N))exp(−itH_N), usando o Hamiltoniano modular finito real da torre. O espectador H_M−H_N comuta com todo operador do andar menor; essa propriedade local dispensa a comutação dos termos de V entre si. Duhamel e a cauda dão ‖u_N(t)−u_M(t)‖≤2|t|e_min(N,M). As hipóteses de CocycleApproximation são assim preenchidas por provas da família concreta. O limite u existe por completude, pertence ao fator, é unitário e contínuo; a convergência dos cortes é uniforme em compactos de tempo e u(s+t)=u(s)α_s(u(t)), com u(0)=1.

Referências: [local_cutoff_ordered_bound](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionCocycle.lean:72>), [localApproximation](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionCocycle.lean:107>), [local_cutoff_uniform_on_compact](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionCocycle.lean:141>), [local_cocycle_twisted](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionCocycle.lean:133>).

A convergência dos geradores dos cortes e o controle linear do erro dão u′(0)=iV. A identidade torcida propaga essa derivada para todo tempo: u′(t)=u(t)α_t(iV). O coeficiente fica à direita nessa convenção. A dinâmica β_t(A)=u(t)α_t(A)u(t)* é então construída como equivalência de álgebras com adjunto: β_0=id, β_s∘β_t=β_(s+t), inversa β_(−t), preservação de norma e pertença ao fator nos dois sentidos. A continuidade temporal em norma é provada para observáveis com órbita canônica contínua, incluindo V.

Referências: [local_cocycle_generator_zero](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionGenerator.lean:19>), [local_cocycle_generator_equation](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionGenerator.lean:28>), [localDynamics](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionDynamics.lean:16>), [local_dynamics_group](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionDynamics.lean:37>), [local_dynamics_factor_iff](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionDynamics.lean:86>), [local_dynamics_potential_orbit_continuous](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/LocalInteractionDynamics.lean:120>).

## Testemunha não comutante efetiva

A folha separada usa os mesmos operadores sitePauliX/Y/Z no mesmo TowerHilbert P: A=X₀X₁ e B=Z₁Z₂. Demonstra AB=−iX₀Y₁Z₂, BA=iX₀Y₁Z₂ e portanto [A,B]=−2iX₀Y₁Z₂≠0. O produto de três sítios tem inversa esquerda explícita e a identidade é não nula; não se usa aproximação numérica.

A sequência term 0=A, term 1=B, demais termos zero satisfaz integralmente LocalInteractionData P. Seu potencial é A+B≠0 e seu cociclo não é identicamente 1. Esta última conclusão permite retornos em tempos particulares; não declara u(t)≠1 para todo t≠0.

Referências: [two_bonds_commutator](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/NoncommutingLocalWitness.lean:80>), [two_bonds_do_not_commute](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/NoncommutingLocalWitness.lean:87>), [noncommutingLocalData](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/NoncommutingLocalWitness.lean:137>), [certified_terms_do_not_commute](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/NoncommutingLocalWitness.lean:143>), [noncommuting_data_potential](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/NoncommutingLocalWitness.lean:147>), [noncommuting_cocycle_nontrivial](<C:/IALD/Central de Patentes/Chatgpt/INTERACAO_LOCAL_GERAL_20260909_164621_372960/NoncommutingLocalWitness.lean:183>).

## Revisão, preservação e alcance

[REAL] A raiz leu integralmente e aprovou semanticamente as quatro fontes do núcleo. Outro revisor leu integralmente Generator/Dynamics e confirmou a derivação do limite, a mesma ação modular, a ausência de circularidade e os limites de continuidade/estado. Essas revisões são leituras independentes, não recompilações independentes. A raiz também leu integralmente e aprovou a testemunha: confirmou o sinal −2i, o suporte e a não nulidade do potencial sem assumir não comutação. REVISAO_TESTEMUNHA.json registra o parecer e os pins.

[OPEN] O domínio é o das perturbações locais **somáveis em norma**, cujo potencial total é limitado. Não inclui automaticamente interações extensivas com soma de normas divergente, potenciais não limitados, reconstrução do UV relativista ou anomalias gerais. O vínculo entre sítios e regiões físicas, fonte gravitacional e lei de área exige correspondência própria.

[OPEN] Estes módulos não constroem um estado perturbado normalizado, não demonstram identificação KMS nem identificam u como [Dφ:Dω] de um estado normalizado. Ao compor com uma perturbação de Araki, é preciso verificar hipóteses, sinal do potencial e normalização; uma fase central não altera Ad_u, mas isso não fornece a normalização do estado.

[REAL] As quatro fontes do núcleo e a testemunha final estão congeladas. O builder foi copiado sem mudança e consumiu caches flat com status PASS_COMPILED_SCOPE, conferindo fontes/artefatos por bytes e pins antes/depois. Ele não recompilou dependências locais/transitivas. Nenhum arquivo canônico, cópia anterior, flag ou gate foi modificado. O registro DEDUCAO_PREVIA.md preserva o estado inicial da construção; o presente documento fornece o resultado posterior.

Para transposição futura, conservar namespaces e reescrever somente os imports locais listados no manifesto para TGLExt. Não é necessária nova instância local ou flag de fechamento. As 99 declarações têm exatamente um #print axioms em suas fontes.

## Inventário

| Fonte | Teoremas | Outras declarações |
|---|---:|---:|
| LocalInteractionData.lean | 21 | 6 |
| LocalInteractionCocycle.lean | 21 | 4 |
| LocalInteractionGenerator.lean | 6 | 0 |
| LocalInteractionDynamics.lean | 16 | 2 |
| NoncommutingLocalWitness.lean | 18 | 5 |
