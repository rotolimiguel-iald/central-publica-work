# JS positivo e auto-adjunto na torre de perfil — 05/09/2026

## Resultado e alcance

**[DERIVED] Para todo `SiteProfile P` da casa, o operador fechado S construído nesta bancada satisfaz JS = D, onde D é positivo e auto-adjunto no domínio máximo descrito abaixo. Portanto, definindo Δ = D², temos JS = Δ¹ᐟ² e S = JΔ¹ᐟ², com igualdade dos domínios.** Aqui J é precisamente `towerJ P`, não uma conjugação escolhida posteriormente.

Esta é uma demonstração matemática escrita para a realização por estados produto da torre. Não é uma demonstração para qualquer operador involutivo S e qualquer conjugação J. A identificação depende dos pesos, das ações locais e da identidade de teste já construída.

**[REAL — Lean]** `DiagonalOperator.lean` verifica auto-adjunticidade e positividade do operador diagonal máximo em ℓ²(ℕ). `ModularProbe.lean` verifica a identidade de teste no domínio COMPLETO do JS da casa. Os arquivos anteriores verificam S fechado, JS fechado e suas ações locais. **[OPEN — Lean]** A construção da base infinita abaixo, sua transformação unitária U e o transporte final de igualdade dos operadores ainda não foram codificados. Não se anuncia um teorema Lean `IsSelfAdjoint (closedModulatorCandidate P)` já existente.

## 1. Objetos e convenções

Sejam H = `TowerHilbert P`, Ω = `hOmega P`, M = `theFactorObject P`, S = fecho de S₀(AΩ)=A*Ω, A∈M, e J=`towerJ P`. O produto interno é linear no segundo argumento. Já se verificaram em Lean: domínio denso e gráfico fechado de S; antilinearidade; J antiunitário involutivo; A:=JS linear fechado com Dom(A)=Dom(S).

No andar N, H_N é o espaço de matrizes de ordem 2^(N+1), com produto interno

\[
\langle a,b\rangle_N=\operatorname{Tr}(\rho_N a^*b),\qquad
\rho_N=\bigotimes_{n=0}^N\operatorname{diag}(p_n,q_n),\quad
p_n=P.w(n),\ q_n=1-p_n>0.
\]

Os embeddings são a↦a⊗I. Pelas definições `towerW`, `tInner` e `towerStep`, esse é o próprio sistema indutivo da casa. Nos vetores locais:

\[
A[a]=[\rho_N^{1/2}a\rho_N^{-1/2}],\qquad
J[a]=[\rho_N^{1/2}a^*\rho_N^{-1/2}].
\]

O primeiro enunciado corresponde a `modulatorCandidate_local`. Não se assume que A seja limitado.

## 2. Base ortonormal explícita

Em cada sítio n, escreva p=p_n, q=q_n e tome

\[
b_{n,0}=I,\quad b_{n,1}=\begin{pmatrix}\sqrt{q/p}&0\\0&-\sqrt{p/q}\end{pmatrix},
\quad b_{n,2}=\frac{E_{01}}{\sqrt q},\quad
b_{n,3}=\frac{E_{10}}{\sqrt p}.
\]

O produto ponderado dá normas quadradas 1, q+p, 1, 1. O único produto misto diagonal potencialmente não nulo é p√(q/p)−q√(p/q)=0; os demais são zero por suas posições matriciais. Logo os quatro vetores formam uma base ortonormal. São autovetores da meia potência local, com autovalores

\[
r_{n,0}=r_{n,1}=1,\qquad r_{n,2}=\sqrt{p_n/q_n},\qquad
r_{n,3}=\sqrt{q_n/p_n}.
\]

Seja I o conjunto das sequências ν:ℕ→{0,1,2,3} com suporte finito. Defina e_ν pelo tensor dos b_{n,ν(n)}, até qualquer andar contendo o suporte. Acrescentar fatores b_{n,0}=I preserva o vetor no colimite: a definição é independente do andar escolhido.

Pela fatoração do produto interno, ⟨e_ν,e_μ⟩=δ_νμ. Em cada andar, os tensores correspondentes aos 4^(N+1) rótulos formam uma base, por dimensão e ortonormalidade. A união dos andares é densa em H. Assim (e_ν) é uma base ortonormal completa de H, indexada por um conjunto contável infinito. Escolher uma enumeração permite trabalhar em ℓ²(ℕ), como no arquivo Lean.

Defina

\[
d_\nu=\prod_{n\in\operatorname{supp}\nu}r_{n,\nu(n)}>0,
\qquad Ux=(\langle e_\nu,x\rangle)_\nu.
\]

U é unitário por completude da base. Temos Ae_ν=d_νe_ν. J troca os rótulos 2 e 3 e fixa 0 e 1, conjugando os coeficientes; se ν̄ denota essa troca, Je_ν=e_ν̄ e d_ν̄=d_ν⁻¹.

**[REAL — controle finito]** `check_modular_geometry.py` verifica simbolicamente a base de um sítio, os autovalores e a permutação por J. Verifica também a matriz de Gram 16×16 de dois sítios com pesos racionais. Esses controles apoiam as fórmulas; a passagem infinita é o argumento de densidade acima.

## 3. Operador diagonal máximo e seu adjunto

Em ℓ²(I), defina

\[
\mathcal D_d=\{c\in\ell^2(I):\sum_\nu d_\nu^2|c_\nu|^2<\infty\},
\qquad (D_dc)_\nu=d_\nu c_\nu.
\]

O domínio é denso porque contém as sequências de suporte finito. D_d é simétrico: as duas expressões ⟨D_dc,z⟩ e ⟨c,D_dz⟩ são a mesma soma, convergente por Cauchy–Schwarz.

Para identificar o adjunto, seja y∈Dom(D_d*) com D_d*y=z. Testar a identidade do adjunto em cada vetor coordenado força z_ν=d_νy_ν. Como z∈ℓ², y∈𝒟_d. Reciprocamente, todo y∈𝒟_d satisfaz a identidade do adjunto por Cauchy–Schwarz. Portanto Dom(D_d*)=𝒟_d e D_d*=D_d, incluindo o domínio.

Além disso,

\[
\langle c,D_dc\rangle=\sum_\nu d_\nu|c_\nu|^2\ge0.
\]

A soma é finita por Cauchy–Schwarz entre c e D_dc. Logo D_d é positivo e auto-adjunto. É injetivo, pois todos os d_ν são estritamente positivos. Isso não fornece uma cota inferior uniforme positiva.

Essas etapas estão em `diagonalAdjoint_coordinates`, `diagonalAdjoint_domain_le`, `diagonalOp_selfadjoint` e `diagonalOp_positive`. Ponha D=U⁻¹D_dU em H.

## 4. Identificação de domínios: A=JS=D

Esta é a etapa que impede inferir auto-adjunticidade apenas das matrizes finitas.

**Primeira inclusão: A⊆D.** O lema Lean `modulator_pairing_local` afirma, para TODO x∈Dom(S) e todo b local:

\[
\langle[b],Ax\rangle=\langle[\rho_N^{1/2}b\rho_N^{-1/2}],x\rangle.
\]

Ele usa a identidade no fecho do gráfico ⟨Sx,R_cΩ⟩=⟨R_c*Ω,x⟩, com c=Jb, e a identidade matricial `modular_twist_of_J`. Não exige que x seja local nem que sua aproximação em MΩ seja local.

Aplicando-o a b=e_ν, temos ⟨e_ν,Ax⟩=d_ν⟨e_ν,x⟩. Como Ax∈H, Parseval dá ∑d_ν²|⟨e_ν,x⟩|²=‖Ax‖²<∞. Logo x∈Dom(D) e Ax=Dx.

**Segunda inclusão: D⊆A.** Seja x∈Dom(D). Escolha conjuntos finitos F_m crescentes que esgotam I, e ponha x_m=∑_{ν∈F_m}⟨e_ν,x⟩e_ν. Cada soma pertence a algum andar local. Portanto x_m∈Dom(A) e Ax_m=Dx_m. As duas caudas satisfazem

\[
\|x-x_m\|^2=\sum_{\nu\notin F_m}|\langle e_\nu,x\rangle|^2\to0,
\quad
\|Dx-Dx_m\|^2=\sum_{\nu\notin F_m}d_\nu^2|\langle e_\nu,x\rangle|^2\to0.
\]

Como A é fechado, x∈Dom(A) e Ax=Dx. As duas inclusões provam A=D, com igualdade de domínios. Em particular, os vetores locais constituem um núcleo para a norma do gráfico de A; essa propriedade foi provada, não suposta.

## 5. Δ, a raiz positiva e a decomposição polar

Defina Δ=U⁻¹ diag(d_ν²) U, com

\[
\operatorname{Dom}(\Delta)=\{x:\sum_\nu d_\nu^4|\langle e_\nu,x\rangle|^2<\infty\}.
\]

Esse domínio coincide com {x∈Dom(D):Dx∈Dom(D)}, pois d²≤1+d⁴ assegura a condição intermediária. Logo Δ=D². O mesmo argumento diagonal mostra que Δ é positivo e auto-adjunto. Sua raiz positiva é D, com o domínio do item 3.

Para o adjunto de um operador antilinear, adote ⟨Sx,y⟩=⟨S†y,x⟩. De S=JD e da auto-adjunticidade de D decorre S†=DJ, no domínio {y:Jy∈Dom(D)}. Isso dá S†S=D²=Δ, também com igualdade de domínios. Portanto

\[
\boxed{JS=\Delta^{1/2},\qquad S=J\Delta^{1/2},\qquad \Delta=S^\dagger S.}
\]

Como D é injetivo e sua imagem contém todos os vetores de suporte finito, sua imagem é densa. J é, assim, a parte antiunitária da decomposição polar, sem componente arbitrária num núcleo. A troca ν↦ν̄ também verifica JΔJ=Δ⁻¹ nos domínios correspondentes.

No perfil tracial p_n=q_n=1/2, D=Δ=I. Para o perfil constante p_n=2/3, aparecem d=(√2)^m e d=(√2)^−m: o operador é ilimitado e os autovalores aproximam zero. A prova cobre ambos os casos, sem supor uma classificação de tipo III.

## 6. Consequência modular analítica

**[DERIVED; ainda não transportada ao Lean]** Defina V_t=Δ^{it} por (UV_tx)_ν=exp(2it log d_ν)(Ux)_ν. Esses operadores são unitários, formam um grupo e são fortemente contínuos: a convergência é imediata em somas finitas e passa ao completamento pela norma unitária.

Em cada andar, V_t[a]=[ρ_N^{it}aρ_N^−it]. Para a local no andar N, calcular em b num andar comum maior dá

\[
V_t\pi(a)V_t^*=\pi(\rho_N^{it}a\rho_N^{-it}).
\]

A igualdade estende-se dos vetores locais a H por limitação dos operadores. A conjugação por V_t preserva a álgebra local e sua inversa é V_−t. Como conjugação unitária transporta comutantes, preserva também seu bicomutante M. Portanto V_t M V_t*=M nesta realização produto.

Isso não constrói ainda no kernel a esperança de Takesaki para cada subálgebra pretendida: a invariância modular dessa subálgebra precisa ser verificada. Tampouco identifica o parâmetro modular com tempo próprio ou com boosts de uma região física sem uma ponte geométrica.

[KNOWN — contexto] A separação entre fechabilidade, polar e invariância modular é discutida por Jonathan Sorce em [A short proof of Tomita’s theorem](https://arxiv.org/html/2309.16762v2). Aqui a prova usa especificamente a estrutura produto já presente no acervo.

## 7. Fronteira formal e preservação

Os logs datados de `DiagonalOperator`, `ModularProbe` e `GeneralNullCone` identificam os fontes compilados por SHA-256. Os resultados principais impressos dependem somente de `propext`, `Classical.choice` e `Quot.sound`. As tentativas recusadas permanecem em logs anteriores e não são certificações finais.

A ligação unitária U, sua completude e a igualdade A=D estão demonstradas neste texto, mas continuam [OPEN] como termos Lean. A raiz e o grupo modular acima têm o mesmo estatuto de demonstração escrita. Não houve execução integral do `um.py`, reconstrução integral das dependências, aprovação adversarial independente, selo canônico novo ou alteração de arquivos originais.


## ADENDO — 05/09/2026: JS positivo e auto-adjunto agora verificado no Lean

[REAL — Lean] A continuação provou `JS_positive_selfadjoint` para o próprio `closedModulatorCandidate P`, no domínio completo. `LocalTowerProjections.lean` constrói as projeções ortogonais dos andares e sua convergência. `ModulatorSelfAdjoint.lean` caracteriza o gráfico inteiro por testes locais e prova igualdade com o adjunto. `ModulatorPositive.lean` passa a forma quadrática positiva local ao limite em norma de gráfico. `ModulatorPolar.lean` prova injetividade, imagem densa e reúne a fatoração S=J(JS) com parte positiva auto-adjunta.

Esta rota supera a pendência de formalizar uma base infinita para obter positividade e auto-adjunticidade: a conclusão foi verificada sem precisar dessa representação. A demonstração escrita por diagonalização continua disponível. [OPEN — Lean] O objeto Δ no domínio do quadrado, a identidade com S†S e o cálculo espectral ainda não foram tipados nesta bancada. A reconstrução geométrica e as hipóteses físicas continuam abertas.

O estado atual e as provas estão descritos em `FECHO_FORMAL_JS.md`. As verificações finais dos quatro módulos retornaram código 0, sem avisos ou sorryAx. Os principais teoremas imprimiram somente propext, Classical.choice e Quot.sound. Os metadados consolidam hashes lidos dos fontes e dos objetos compilados. Não houve selo canônico, aprovação independente nem alteração dos originais ou das memórias canônicas.


## ADENDO — 05/09/2026: Δ e S†S agora construídos e verificados

[REAL — Lean] `ModularSquare.lean` constrói `towerDeltaClosed P` no domínio x∈Dom(JS) e JSx∈Dom(JS), prova densidade, positividade e coincidência com `towerDeltaLevel` nos andares. `ModularSquareAdjoint.lean` prova auto-adjunticidade e fechamento por uma estimativa de energia que controla as duas condições de domínio. `TomitaAdjoint.lean` constrói o adjunto antilinear S†=(JS)J, prova sua identidade e maximalidade, e verifica S†S=Δ com o domínio de composição. `ModularInverse.lean` prova injetividade de Δ e JΔJ=Δ⁻¹ como equivalência de gráficos.

Estas construções superam as pendências formais de quadrado e adjunto descritas anteriormente. JS é uma raiz quadrada positiva auto-adjunta explicitamente construída de Δ. [OPEN — Lean] Permanecem o cálculo funcional espectral, sua operação de raiz e unicidade geral, o grupo Δ^{it} e a invariância modular tipados. As pontes geométricas e físicas permanecem abertas.

O registro atual é `DELTA_FORMAL.md`. Os quatro arquivos finais compilaram com código 0 e sem avisos; as listas de axiomas impressas foram conferidas e contêm somente propext, Classical.choice e Quot.sound. Os hashes foram lidos dos fontes e objetos compilados. As tentativas recusadas, incluindo um excesso de inferência e uma detecção de mudança do fonte durante verificação, permanecem preservadas; não são o resultado final validado. Nenhum original, memória canônica ou selo foi alterado.


## ADENDO — 05/09/2026: potência imaginária, grupo e invariância modular verificados

[REAL — Lean] Foi construído `deltaImaginaryPower P t`, um grupo unitário fortemente contínuo no Hilbert da torre. A caracterização espectral foi verificada: os vetores locais E_ij pertencem ao domínio de Δ, têm autovalores λ=w_i/w_j>0, geram um span denso e recebem a fase exp(it log λ). O operador limitado com essa ação é único. A construção, portanto, liga a potência imaginária ao Δ existente.

[REAL — Lean] Também foram provadas a conjugação da representação local, a invariância do bicomutante `theFactorObject P`, Ω fixo e a invariância de `omegaState P` sob a conjugação. Não se presumiu o grupo nem a invariância como campos de um contrato. A invariância do estado usa Ω fixo e unitariedade, não apenas ω(I)=1.

Esses resultados superam a pendência de formalizar o grupo Δ^{it}, sua continuidade forte e a invariância de M para esta torre produto. [OPEN] Permanecem a biblioteca geral de cálculo funcional, a construção da esperança condicional para as subálgebras pretendidas e as pontes geométricas/físicas. O parâmetro modular não foi identificado automaticamente com tempo próprio ou geometria.

O registro atual é `FLUXO_MODULAR_FORMAL.md`. Os seis módulos finais, de `ModularFlowLevel` a `ModularPower`, compilaram com código 0, sem avisos, sorry ou novos axiomas. As listas impressas foram conferidas contra propext, Classical.choice e Quot.sound. Os hashes e a contagem de teoremas foram lidos dos artefatos. Os 290 originais do manifesto foram rehasheados; o resultado de preservação acompanha a verificação consolidada. Nenhuma memória canônica ou selo foi alterado.
