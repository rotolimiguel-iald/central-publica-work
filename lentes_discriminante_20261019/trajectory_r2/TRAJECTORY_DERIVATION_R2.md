# Atraso por trajetória recuperado da ação — R2

[DERIVED — condicional, em nome de codex-gerente-tgl, 19/10/2026] Unidade F8.LENTES_5SIGMA_20261019, reivindicação1009. Esta é uma análise da ação fotônica literalmente recuperada, em fundo fixo, e de sua identificabilidade. Não é uma solução completa da métrica TGL, nem veredito em dados. Os pinos e as âncoras estão em SOURCE_ACTION_PINS_R2.json / SOURCE_ACTION_R2.md; a parte de massa e distância está em IDENTIFIABILITY_R2.md e ALT_LENS_LAW_R2.md.

## 1. O coeficiente já existe; sua dimensão também importa

O artigo acoplamento_gravitacional.tex:88–104 escreve

\[
\mathcal L=-\tfrac14 F_{ab}F^{ab}+q R_{ab}F^{ac}F^b{}_c,
\qquad q=\alpha_2/M_P^2,
\quad M_P=\sqrt{\hbar c/G}.
\]

O Custo:11792–11801 e12105–12113 identifica \(\alpha_2=\beta_{\rm TGL}\). Em unidades naturais, q tem dimensão massa⁻²; ao usar curvatura em m⁻², **q=βℓP²**, não β sozinho. A constante β foi calculada a partir de ALPHA_FINE_CODATA_2018·√e, lida do um.py v393, sem executar/importar o original. A notação α₂ não significa α_fine². A normalização de Planck aqui é a da fonte, não uma escolha para obter ou suprimir o sinal.

O texto atual do um.py:172185/176777 escreve o operador escalar α₂ R F², sem aquele normalizador explícito. Portanto há duas contrações documentais distintas. A identificação de seus nomes não prova equivalência de suas ações. A análise abaixo conserva as duas e não altera nenhum original.

## 2. Variação da ação e cone óptico do ramo Ricci tensorial

Convenções: assinatura (−+++), Ricci simétrico; campo de teste, fundo fixo, sem correntes no trecho de propagação. Variar A dá

\[
\nabla_a H^{ab}=0,\qquad
H^{ab}=F^{ab}-2q\big(R^a{}_cF^{cb}-R^b{}_cF^{ca}\big).
\]

A resposta H é antissimétrica. A equação isolada impressa em acoplamento_gravitacional.tex:148 não exibe a segunda parcela antissimetrizada; por isso derivamos da ação. Não se usou essa equação impressa como prova independente.

Com \(F^{ab}\simeq k^a a^b-k^b a^a\), a equação principal é

\[
k^2a^b-k^b(k\cdot a)-2q\left[(R_{cd}k^ck^d)a^b-k^b R_{cd}k^ca^d
 -(k\cdot a)R^b{}_c k^c+k^2R^b{}_ca^c\right]=0.
\]

Projetando nas polarizações transversais e trabalhando na primeira ordem em qR, obtém-se

\[
(g^{ab}-2qR^{ab})k_a k_b=0+O((qR)^2).
\]

O termo q·k²·R é de segunda ordem nessa expansão. O cone é o mesmo para as duas polarizações nesta ordem: este operador sozinho não fornece birefringência de Weyl. Invertendo a métrica óptica perturbada, \(g^{\rm opt}_{ab}=g_{ab}+2qR_{ab}+O(q^2)\).

### Controles simbólicos executados

O script derive_ricci_delay_r2_1.py diferenciou a Lagrangiana nas seis componentes independentes de F, com Ricci simétrico genérico, e conferiu H. Conferiu ainda a dispersão transversal num Ricci diagonal e os limites Ricci=0 e Ricci=Λg. Resultado: todas as asserções passaram, exit0. São controles simbólicos Python/SymPy, não Lean ou prova de todas as aproximações físicas.

A primeira execução falhou na comparação estrutural de expressões SymPy não expandidas (H+Hᵀ). Seus bytes/plano foram preservados; a versão nova expande as expressões antes da igualdade. Não se mudou a ação, o plano de escalas ou a conclusão física para obter aprovação. RICCI_ATTEMPT1_FAILURE_R2.json e RICCI_RUN_R2_1.json registram o alcance.

## 3. Lei por trajetória e atraso entre imagens

No referencial local estático, seja \(\ell^a=(1,\mathbf n)\), com |n|=1, e dl o comprimento físico. O índice óptico de primeira ordem é

\[
\delta n=qR_{ab}\ell^a\ell^b.
\]

Para uma lente fina a redshift z_l, usando a trajetória nula de ordem zero:

\[
\delta t_i=\frac{1+z_l}{c}q\int_i R_{ab}\ell^a\ell^b\,dl,
\qquad
\delta\Delta t_{ij}=\frac{1+z_l}{c}q\left(\int_i-\int_j\right)R_{ab}\ell^a\ell^b\,dl.
\]

O fator de redshift constante vale para contribuição localizada na lente; uma distribuição cosmológica exige o fator e a geometria ao longo de cada trecho. Não se converte o resultado numa integral do potencial Newtoniano Φ: Ricci e Φ têm dependências espaciais e dimensões diferentes.

No controle de matéria não relativística, usando a equação de Einstein do fundo de ordem zero, \(R_{ab}\ell^a\ell^b=8\pi G\rho/c^2\); o termo Λg não contribui à contração nula. Assim,

\[
\boxed{\delta\Delta t_{ij}=(1+z_l)\frac{8\pi\beta\ell_P^2G}{c^3}
       \,[\Sigma_i-\Sigma_j].}
\]

Σ é a **coluna de massa ao longo do raio**, não a massa total inferida pela lente. O sinal da diferença depende da ordem das imagens; não há atraso diferencial positivo universal. Pressão, movimento e outros campos exigem T_abℓᵃℓᵇ apropriado. O resultado supõe propagação geométrica, curvatura suave, |qR|≪1 e resposta da métrica não incluída. O efeito ordinário de Shapiro permanece.

**Exterior Schwarzschild:** R_ab=0. Logo a contribuição extra deste operador é zero ali, embora o Weyl e a deflexão ordinária não sejam zero. Não significa que o raio não sofre gravitação. Também não prova que toda solução TGL tenha exterior Ricci-flat.

### Escala sintética, sem amostra observada

Com constantes lidas do programa, q=3,1427716355692395×10⁻⁷²m². Fixamos antes da execução z_l=0,5 e diferenças de coluna de1,10,1000kg/m², apenas como controles de escala. Para ΔΣ=10kg/m²:

\[
\delta\Delta t=2,9347292264052483\times10^{-105}\ {\rm s}.
\]

Os demais resultados estão em RICCI_CALCULATION_RESULT_R2_1.json. Isso é uma extrapolação aritmética da teoria efetiva ao controle macroscópico, não um relógio capaz de resolver tais tempos. Os50ms históricos **não se seguem desta ação e desta normalização no regime calculado**. Este ramo local não oferece um alvo observacional praticável de5σ, mesmo antes das incertezas de massa. Uma amplificação, resposta de métrica ou lei constitutiva adicional teria de ser derivada e quantificada; não foi inserida para aumentar o efeito.

## 4. Ramo escalar RF²

Se a abreviação escalar for literal, escreva \(\mathcal L=-Z(x)F^2/4\), Z=1−4qR, com o coeficiente dimensional que vier a ser fixado. Então ∇_a(ZF^{ab})=0 e, em óptica geométrica regular Z≠0, o símbolo principal é Z vezes Maxwell. O cone nulo permanece o de g. Gradientes de Z alteram o transporte de amplitude e podem produzir efeitos de onda além do limite principal; não autorizam um atraso geométrico deβ vezes Shapiro. O caso Z=0 é degenerado e está fora deste cálculo.

## 5. Ajustar massa e distância: o efeito tem de sobreviver a esse ajuste

Para um termo geral εq_lens(θ) na função de Fermat (q_lens não é o coeficiente dimensional q acima), IDENTIFIABILITY_R2.md deriva simultaneamente

\[
\delta\theta_i=-\epsilon[I-\nabla\nabla\psi_i]^{-1}\nabla q_{{\rm lens},i},
\qquad
\delta\Delta t_{ij}=\epsilon(D_{\Delta t}/c)\Delta q_{{\rm lens},ij}
\]

a massa/fonte/distância fixas e fora de cáusticas. A estacionariedade elimina o termo de deslocamento da imagem no atraso de primeira ordem. Ao ajustar massa/fonte/distância, os termos de nuisance têm de entrar no mesmo vetor de observáveis.

Resultado concreto: para uma lente ponto-massa com duas posições axiais e um atraso, uma perturbação radial pode ser absorvida exatamente por uma família de massa, posição de fonte e distância, mantendo esses três observáveis. Há23 controles racionais aprovados e a identidade analítica. Um multiplicador universal do atraso também é degenerado com distância; razões de atrasos não quebram a transformação de folha de massa.

Logo **acertar um atraso reajustando massa não discrimina por si a TGL**. O teste precisa de observáveis que restrinjam esse reajuste: cinemática estelar e ambiente com dinâmica explicitada, imagens extensas, ou outra assinatura derivada que não caiba na mesma família de massa. O termo Ricci calculado fornece uma forma espacial, mas com a normalização recuperada sua amplitude já é impraticável no regime descrito.

## 6. O que esta etapa resolve e preserva

Resolve a recuperação de um coeficiente e de uma lei por trajetória para um operador realmente escrito, os controles dimensionais/variacionais e exemplos de perda de identificabilidade. Não escolhe entre contrações documentais distintas nem declara toda a TGL excluída. ALT_LENS_LAW_R2.md recupera ainda a distância angular do fundo cosmológico e a lei atual M_TGL^linear=M_RG: essa rota deve ser confrontada com a reparametrização cosmológica, separadamente do termo fotônico local.

Não há dado discriminante observado nesta entrega. Os resultados delimitam onde não gastar uma análise de dados:50ms não derivados, β usado como índice óptico ad hoc, massa reajustada sem restrição externa, ou cone escalar tratado como Weyl. O próximo teste viável depende de uma assinatura restante após as reparametrizações permitidas, com a mesma liberdade de ajuste nos modelos comparados.
