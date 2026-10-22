# Einstein–sigma S³: operador completo, álgebra causal e alcance da quantização local

09/09/2026. Análise e demonstração próprias. **[DERIVED — prova escrita, sem nova formalização Lean.]** As leituras de arquivos e seus hashes são medidas no manifesto acompanhante. Nenhum `um.py` foi executado ou importado; nenhum original foi alterado.

**Resultado principal.** Sobre o habitante curvo já construído, a matéria tangente à esfera tem operador de Jacobi `J=D²−2/a²`. A Hessiana completa de Einstein–sigma, após calibre de de Donder e uma normalização algébrica invertível, tem símbolo principal `g⁻¹(ζ,ζ) I₁₃`. Isso fornece propagadores causais locais e uma álgebra CCR dos observáveis lineares invariantes por calibre. Um estado Hadamard positivo existe para o bloco de matéria com a métrica fixada, por um teorema de feixe positivo com hipóteses verificadas aqui. Positividade Hadamard física do sistema acoplado e a execução da construção BV renormalizada permanecem obrigações distintas.

**Distinção decisiva.** A extensão quântica ambiente permite variar g e φ independentemente. Na família categórica mínima de cinco pesos e posto quatro, todas as variações induzidas de `(g[P],φ[P])` são difeomorfias locais. Demonstra-se isso na seção 9. Assim, a quantização ambiente é uma ampliação explicitamente assumida; não se identifica com uma quantização dos cinco pesos apenas.

## 1. Ação, convenções e região de trabalho

[INPUT] A ação ambiente escolhida é

\[
S[g,\phi]= -\frac1{2\kappa}\int\mu_g(R-2\Lambda)
 +\frac c2\int\mu_g\,g^{\mu\nu}\langle\partial_\mu\phi,\partial_\nu\phi\rangle,
\qquad \phi:M\longrightarrow S^3\subset\mathbb R^4.
\]

Adotam-se assinatura `+---`, `□=g^{μν}∇μ∇ν` e
`R^ρ{}_{σμν}=∂μΓ^ρ_{νσ}−∂νΓ^ρ_{μσ}+Γ^ρ_{μλ}Γ^λ_{νσ}−Γ^ρ_{νλ}Γ^λ_{μσ}`,
`Ric_{σν}=R^ρ{}_{σρν}`. Todas as integrais de variação usam suporte compacto; fatores `d⁴x` ficam implícitos em `μ_g`.

[DERIVED, referência local anterior] O fundo é

\[
g=dr^2-a(r)^2h_{S^3},\quad a(r)=2\cos(r/2),\quad\phi(r,z)=z,
\quad c=\frac{k}{\pi\cosh^2k}>0,\quad\Lambda=\frac34,\quad\kappa=\frac4c.
\]

Ele satisfaz `G+Λg=κT` e a equação sigma. O documento anterior [HABITANTE_CURVO_SIGMA_E_AREA.md](../HABITANTE_CURVO_SIGMA_20260909_202000/HABITANTE_CURVO_SIGMA_E_AREA.md) contém a dedução e o recibo de 14 controles simbólicos exatos. Aqui não se declara nova compilação dessa geometria.

Trabalhamos numa vizinhança `O` suficientemente pequena, causalmente convexa e globalmente hiperbólica, contida estritamente em `(0,π)×S³_+`. Uma vizinhança desse tipo existe em torno de cada ponto interior. Escolhemos orientação temporal `∂r` e uma carta contrátil do alvo que contenha a imagem pertinente. O cilindro do octante inteiro não é declarado globalmente hiperbólico; as faces `z_a=0`, o extremo `a=0` e condições de contorno não são incluídos.

## 2. Eliminação correta da restrição e Jacobi tangente

Use `E=φ*TS³`, de posto três, com a métrica positiva induzida de R⁴. Uma perturbação física da aplicação sigma é uma seção `ξ∈Γ(E)`, logo `φ·ξ=0`. A parametrização `φ_ε=Exp_φ(εξ)` preserva `|φ_ε|²=1` exatamente; não se quantizam quatro componentes independentes impondo a restrição apenas depois.

Escreva `u_μ=∂μφ`, `W_μν=〈u_μ,u_ν〉`, `Q=g^{μν}W_μν`. A conexão do alvo puxada para E é

\[
D_\mu\xi=\partial_\mu\xi+\phi\langle u_\mu,\xi\rangle.
\]

Ela é a projeção tangente da derivada ambiente e preserva a métrica de E. A tensão sigma, em R⁴, é `τ=□φ+Qφ`. Na linguagem com multiplicador, `−c□φ+λφ=0` e `λ=−cQ`; a formulação intrínseca elimina tanto λ quanto a direção normal. No fundo,

\[
Q=-3/a^2,\qquad \Box\phi=3\phi/a^2,\qquad\tau=0.
\]

Para o alvo de curvatura seccional +1, com `Rᴺ(X,Y)Z=〈Y,Z〉X−〈X,Z〉Y`, a derivada tangente da tensão é

\[
J\xi=D^\mu D_\mu\xi+R^N(\xi,u_\mu)u^\mu
=D^2\xi+Q\xi-\mathcal K\xi,
\qquad\mathcal K\xi=g^{\mu\nu}u_\mu\langle u_\nu,\xi\rangle.
\tag{2.1}
\]

Uma verificação sem depender de uma convenção nominal de Jacobi: variar `□φ+Qφ` com g fixada fornece

\[
\delta\tau=\Box\xi+Q\xi+2\phi\langle u^\mu,\partial_\mu\xi\rangle.
\]

De `φ·ξ=0`, `τ=0` e da fórmula de D segue
`D²ξ=□ξ+2φ〈u^μ,∂μξ〉+𝒦ξ`; substituindo, recupera-se (2.1), inclusive o sinal do potencial.

No exemplo, `u_r=0`, enquanto `dφ` é a identidade tangente na esfera espacial. Portanto `𝒦|E=−a⁻² I_E`, e

\[
\boxed{J=D^2-\frac2{a^2}I_E.}
\tag{2.2}
\]

Numa base ortonormal local de E, a matriz de potencial covariante é explicitamente
`diag(−2/a²,−2/a²,−2/a²)`. Coeficientes de conexão ainda aparecem quando D² é escrito em componentes; não se omitem esses termos declarando três Klein–Gordon independentes.

Identificando E com o fibrado tangente espacial S³,

\[
J\xi=\partial_r^2\xi+3\frac{a'}a\partial_r\xi
-\frac1{a^2}(\Delta_h^{\rm rough}+2)\xi.
\tag{2.3}
\]

Aqui `Δrough_h` tem o sinal `Σ∇_A∇_A−∇_{∇_A A}`. O símbolo principal, definido pela substituição formal `∂μ→ζμ`, é `g^{μν}ζμζν I_E`. Na convenção com `iζ`, aparece o sinal global correspondente.

Controle do potencial: para uma rotação constante `Aᵀ=−A`, `ξ=Aφ` é o gerador de uma família exata de isometrias do alvo, logo `Jξ=0`. A fórmula (2.3) reproduz isso, pois um Killing da esfera satisfaz `Δrough_h ξ=−2ξ`. Esses modos são controle geométrico, não uma afirmação de dados de Cauchy compactamente suportados. Hiperbolicidade não implica estabilidade espectral nem a existência de um estado fundamental privilegiado.

## 3. Variação conjunta da tensão e da fonte

Seja `h=δg` covariante, simétrico; `h^{μν}` significa elevar h com o g de fundo. Defina

\[
\bar h_{\mu\nu}=h_{\mu\nu}-\tfrac12g_{\mu\nu}\operatorname{tr}_g h,
\qquad C_\nu(h)=\nabla^\mu\bar h_{\mu\nu},
\qquad B_{\mu\nu}=D_\mu u_\nu.
\]

Na definição de B, D também inclui a conexão de Levi–Civita no índice de covetor do espaço-tempo. Como `δg⁻¹=−h↑↑` e `g^{μν}δΓ^ρ_{μν}=C^ρ`, a derivada completa é

\[
\boxed{\delta\tau=J\xi-h^{\mu\nu}B_{\mu\nu}-C^\rho(h)u_\rho.}
\tag{3.1}
\]

Para o fundo em questão, escrevendo `H=a'/a`,

\[
B_{rr}=0,\quad B_{rA}=B_{Ar}=-H u_A,\quad B_{AB}=0,
\qquad\delta\tau=J\xi+2Hh^{rA}u_A-C^A(h)u_A.
\tag{3.2}
\]

Assim, a mistura métrica→matéria tem no máximo primeira derivada de h. Na superfície de calibre `C=0`, sobra a mistura algébrica `2Hh^{rA}u_A`.

O tensor é `T=c(W−gQ/2)`. Ponha
`A_μν(ξ)=〈Dμξ,uν〉+〈uμ,Dνξ〉`. Então

\[
\delta W_{\mu\nu}=A_{\mu\nu}(\xi),\qquad
\delta Q=-h^{\alpha\beta}W_{\alpha\beta}+2\langle u^\alpha,D_\alpha\xi\rangle,
\]

\[
\boxed{\delta T_{\mu\nu}=c\left[A_{\mu\nu}(\xi)-\frac Q2h_{\mu\nu}
+\frac12g_{\mu\nu}h^{\alpha\beta}W_{\alpha\beta}
-g_{\mu\nu}\langle u^\alpha,D_\alpha\xi\rangle\right].}
\tag{3.3}
\]

Esta fórmula resulta da variação da ação, não de escolher uma fonte à parte. O bloco matéria→métrica tem no máximo primeira derivada de ξ; não há mistura de segunda ordem entre os dois setores. No formalismo com λ, a variação tangente da restrição é zero, justificando a ausência de termos omitidos de `δλ` nesta fórmula intrínseca.

## 4. Hessiana completa e cancelamento do calibre não minimal

Uma forma exata, antes de comutar derivadas, é

\[
\delta\Gamma^\rho_{\mu\nu}=\tfrac12g^{\rho\sigma}
(\nabla_\mu h_{\nu\sigma}+\nabla_\nu h_{\mu\sigma}-\nabla_\sigma h_{\mu\nu}),
\qquad\delta R_{\mu\nu}=\nabla_\rho\delta\Gamma^\rho_{\mu\nu}
-\nabla_\nu\delta\Gamma^\rho_{\mu\rho}.
\]

Com a convenção da seção 1, comutar os índices fornece

\[
\delta G_{\mu\nu}=-\tfrac12\Box\bar h_{\mu\nu}
+\mathcal D(C(h))_{\mu\nu}+\mathcal L_R(h)_{\mu\nu},
\tag{4.1}
\]

onde

\[
\mathcal D(v)_{\mu\nu}=\nabla_{(\mu}v_{\nu)}-\tfrac12g_{\mu\nu}\nabla_\rho v^\rho,
\]

\[
\mathcal L_R(h)_{\mu\nu}=
\tfrac12\left(R_{\rho\mu}h^\rho{}_\nu+R_{\rho\nu}h^\rho{}_\mu
-2R_{\mu\rho\nu\sigma}h^{\rho\sigma}\right)
-\tfrac12Rh_{\mu\nu}+\tfrac12g_{\mu\nu}R_{\rho\sigma}h^{\rho\sigma}.
\tag{4.2}
\]

O termo (4.2) é algébrico em h. Todas as suas entradas estão determinadas pelo fundo; por exemplo `Ric_rr=3/4`, `Ric_AB=(4−3a²/4)h_AB` e `R=3−12/a²`. (4.1) passa o controle `h=2f g` com f constante: `δRic=δG=0`. Para f variável, `δRic=−2∇²f−g□f` em quatro dimensões, o que também verifica os termos principais.

Seja `E_g=G+Λg−κT` e use a parelha não degenerada

\[
\langle(h,\xi),(f,\chi)\rangle_V
=\int\mu_g(h_{\mu\nu}f^{\mu\nu}+\langle\xi,\chi\rangle).
\]

Ela é indefinida no setor métrico. Como o fundo satisfaz ambas as equações, a Hessiana da ação é o operador formalmente autoadjunto

\[
\mathscr H(h,\xi)=\left(\frac1{2\kappa}\delta E_g,\;-c\,\delta\tau\right).
\tag{4.3}
\]

A hipótese on-shell importa: os termos oriundos de variar o volume, o pareamento e a conexão de campo multiplicam as equações de fundo e só então desaparecem.

O adjunto formal de `C:V→T*M`, que ignora ξ, é `C* v=(−𝒟(v),0)`. A identidade decorre de integração por partes:
`〈C(h),v〉=−〈h,𝒟(v)〉`. Acrescente à ação quadrática

\[
S_{gf}^{(2)}=\frac1{4\kappa}\int\mu_g\,C_\nu(h)C^\nu(h).
\]

Logo

\[
\mathscr H_{gf}=\mathscr H+\frac1{2\kappa}C^*C,
\]

e seu bloco métrico é precisamente

\[
\frac1{2\kappa}\left[-\tfrac12\Box\bar h+\mathcal L_R(h)+\Lambda h-\kappa\delta T\right].
\tag{4.4}
\]

O termo `𝒟(C)` de segunda ordem cancelou. O bloco de matéria continua `−c[Jξ−h·B−C(h)·u]`; não se elimina esse termo à mão ao definir o operador sobre todas as configurações.

Denote por `I_tr` a reversão do traço h→bar h. Em dimensão quatro, `I_tr²=I`. Então

\[
\mathscr H_{gf}=\mathcal B\begin{pmatrix}\Box&0\\0&D^2\end{pmatrix}
+\text{operador de ordem no máximo 1},
\quad\mathcal B=\operatorname{diag}\left(-\frac{I_{tr}}{4\kappa},-cI_E\right).
\]

Como `c,κ>0`, `𝓑` é invertível e suave. O operador

\[
\boxed{\mathscr P=\mathcal B^{-1}\mathscr H_{gf},\qquad
\sigma_2(\mathscr P)(x,\zeta)=g^{\mu\nu}\zeta_\mu\zeta_\nu I_{13}}
\tag{4.5}
\]

é normalmente hiperbólico. As misturas de primeira ordem podem ser incorporadas a uma conexão no fibrado direto; não alteram o cone característico. A Hessiana, com sua normalização física (4.3), é preservada ao construir propagadores: se `G_P^±` são os inversos causais de 𝒫, os de `𝓗_gf` são `G_gf^±=G_P^±𝓑⁻¹`.

**[DERIVED + KNOWN] Teorema local aplicável.** Num O globalmente hiperbólico como acima, o sistema linearizado completo em de Donder e o operador fantasma da seção seguinte possuem operadores de Green avançado e retardado únicos, suporte causal e problema de Cauchy bem posto. As hipóteses de suavidade, posto finito e símbolo de onda foram verificadas explicitamente. A existência de Green para operadores de onda em fibrados é o resultado usado de [Bär–Ginoux–Pfäffle, capítulos 2–3](https://arxiv.org/abs/0806.1036). Nenhuma positividade do pareamento métrico é necessária para esse resultado de EDP.

## 5. Simetria linear, fantasmas e identidades exatas

Para um campo vetorial v, a ação infinitesimal de difeomorfismos é

\[
K(v)=(\mathcal L_vg,\mathcal L_v\phi)
=(2\nabla_{(\mu}v_{\nu)},v^\mu u_\mu).
\]

A covariância das equações dá `δE[K(v)]=L_v E=0` no fundo. Assim
`𝓗K=0` e, pela autoadjunticidade, `K*𝓗=0`. O adjunto na parelha da seção 4 é
`K*(f,χ)_ν=−2∇^μ f_μν+〈u_ν,χ〉`.

Calcule diretamente

\[
\boxed{\mathscr Q v=C(Kv)=\Box v_\nu+R_{\nu\rho}v^\rho.}
\tag{5.1}
\]

É o operador vetorial fantasma, real, formalmente autoadjunto e normalmente hiperbólico. Em particular, dados admissíveis podem ser levados a `C=0` resolvendo `𝒬v=−C(h)`; os calibres residuais satisfazem `𝒬v=0`.

Sem descartar termos de matéria, temos as duas identidades

\[
\mathscr H_{gf}K=\frac1{2\kappa}C^*\mathscr Q,
\qquad K^*\mathscr H_{gf}=\frac1{2\kappa}\mathscr Q C.
\tag{5.2}
\]

Elas pagam a propagação do calibre e a descida da forma causal aos observáveis físicos, e são mais fortes que apenas olhar o símbolo principal.

## 6. Álgebra causal linear: construção efetiva

Seja

\[
\mathcal V_{obs}=\frac{\ker K^*\cap\Gamma_c(V)}{\mathscr H\Gamma_c(V)}.
\]

O denominador está no numerador por `K*𝓗=0`. Seja `E_gf=G_gf^ret−G_gf^adv`, fixando essa convenção também no comutador. Para `f∈ker K*`, (5.2), unicidade causal e `𝒬*=𝒬` implicam

\[
C G_{gf}^{\pm}f=0,\qquad
\mathscr H G_{gf}^{\pm}f=f,\qquad\mathscr H E_{gf}f=0.
\tag{6.1}
\]

Por outro lado, `G_gf^± C*=2κ K G_Q^±`, consequência da primeira identidade (5.2). Portanto, para seção teste q,

\[
E_{gf}\mathscr Hq=-K E_Q Cq.
\tag{6.2}
\]

Defina

\[
\sigma([f],[f'])=\langle f,E_{gf}f'\rangle_V.
\]

(6.2) e `K*f=0` mostram que σ independe dos representantes. A autoadjunticidade de `𝓗_gf` implica `E_gf* =−E_gf`, logo σ é antissimétrica. Seu suporte causal implica σ=0 para suportes separados espacialmente. Isso dá uma forma **pré-simplética**; não se presume que seu radical seja zero em toda topologia/domínio.

A álgebra polinomial CCR é gerada por `Φ([f])` com linearidade real, `Φ([f])* =Φ([f])` e

\[
[\Phi([f]),\Phi([f'])]=i\hbar\,\sigma([f],[f'])\,1.
\tag{6.3}
\]

**Este é um resultado de quantização algébrica linear, aplicável ao operador acoplado deduzido.** Não é apenas uma proposta de calcular o propagador no futuro. Também não seleciona um estado, um vácuo ou uma representação física Hadamard. A construção é da mesma família de métodos de [Hack–Schenkel, seções 3–4](https://arxiv.org/html/1205.3484v2); as identidades específicas necessárias foram demonstradas acima. O trabalho de [Hack, seções 2.2–2.4](https://arxiv.org/html/1403.3957v2) trata o Einstein–Klein–Gordon acoplado on-shell; é um antecedente próximo, mas o alvo S³ e seu potencial de Jacobi foram deduzidos aqui, não importados desse caso escalar.

## 7. Hadamard: conclusão positiva que se pode dar e limite que resta

**[DERIVED + KNOWN] Matéria tangente em g fixada.** O operador J em E é real, normalmente hiperbólico e formalmente autoadjunto: D é métrica, a integração por partes dá a simetria de D², e `−2/a² I` é um potencial real simétrico. E tem métrica positiva e conjugação real após complexificação. O teorema 4 e corolário 5 de [Fewster–Strohmaier, arXiv:2510.11492v2](https://arxiv.org/html/2510.11492v2) aplicam-se e fornecem um estado quase livre Hadamard positivo para a álgebra do campo real tangente. A constante positiva c apenas reescala a normalização canônica e não obstrui o resultado.

A normalização de sinal também confere: o artigo usa `G_J^adv−G_J^ret` para o operador `J`. A Hessiana física de matéria aqui é `−cJ`, de modo que `G_{−cJ}^ret−G_{−cJ}^adv=(G_J^adv−G_J^ret)/c`, exatamente a convenção da seção 6. Se `W_J` é a covariância do artigo com ℏ=1, a do campo com coeficiente cinético c é `W_m=(ℏ/c)W_J`, preservando positividade e a condição de Hadamard.

**[OPEN nesta entrega] Sistema Einstein–sigma acoplado.** O pareamento cinético do setor métrico é indefinido. O teorema de feixe positivo anterior não pode ser aplicado à soma de treze componentes. Propagadores de Green e parametrizes de onda controlam a causalidade e as singularidades; ainda é preciso construir bisoluções com as identidades de calibre e provar positividade no quociente físico. Nem a existência de um Feynman parametrix, nem `𝓗_gf` autoadjunto formal, provam essas propriedades por si.

O resultado de [Gérard, arXiv:2311.11043](https://arxiv.org/abs/2311.11043) estabelece estados Hadamard para gravidade linearizada sobre **espaço-tempo Einstein** com Cauchy compacta. Nosso fundo é Einstein–matéria, com `Ric_rr=3/4` e `Ric_AB=(4−3a²/4)h_AB`, incompatíveis com `Ric=λg` para λ único. Além disso, escolhemos uma região local. Assim, esse teorema não quita automaticamente o contrato acoplado.

O estado da matéria tangente J também não é o estado de quatro campos livres que satisfazem `□φ_a=0`. O fundo atual tem `□φ_a=3φ_a/a²`. Não se pode transportar a realização por deslocamento CCR livre da nota anterior ao setor sigma sem nova demonstração. Os pesos Gibbs auxiliares continuam sendo estados/protocolos finitos próprios; a nota não os identifica com o estado Hadamard da teoria de campos.

## 8. BRST/BV: parte clássica explícita e obrigação quântica

Nas variáveis completas, escolha a convenção de derivação ímpar à esquerda

\[
s g=\mathcal L_{\mathfrak c}g,\quad s\phi=\mathcal L_{\mathfrak c}\phi,
\quad s\mathfrak c^\mu=\mathfrak c^\nu\partial_\nu\mathfrak c^\mu,
\quad s\bar{\mathfrak c}_\mu=b_\mu,\quad sb_\mu=0.
\tag{8.1}
\]

A identidade de Lie graduada implica `s²g=s²φ=0`. Para conferir o sinal em escalares: `s²φ=(s𝔠^μ−𝔠^ν∂ν𝔠^μ)∂μφ−𝔠^μ𝔠^ν∂μ∂νφ=0`. O último termo zera por antissimetria. A identidade de Jacobi graduada dá `s²𝔠=0`, e o par `(bar𝔠,b)` é contrátil. A condição `|φ|²=1` é preservada por (8.1). Rotações O(4) do alvo são simetrias globais, não um novo calibre local introduzido aqui.

A ação BV mínima adiciona a S os termos `∫g*·L_𝔠g+φ*·L_𝔠φ+𝔠*·(𝔠∂𝔠)` e o par não minimal `∫bar𝔠*·b`, com antifields densitizados e anticolchete consistente. A invariância de S e o fechamento fora das soluções em (8.1) dão a equação mestra **clássica**. Um férmion de calibre baseado em `C(h)` produz o calibre de de Donder e, no grau quadrático, o operador fantasma (5.1); o parâmetro de b é escolhido para reproduzir o termo da seção 4. Não há inferência de nilpotência quântica a partir dessa identidade clássica.

**[KNOWN]** O formalismo BV renormalizado substitui a expressão divergente informal de Laplaciano BV por um termo local de anomalia na identidade mestra de Ward; a equação mestra quântica controla a simetria perturbativa. Esse é o resultado metodológico usado de [Fredenhagen–Rejzner](https://arxiv.org/html/1110.5232v3). [Brunetti–Fredenhagen–Rejzner, seção 3.4 e conclusões](https://arxiv.org/html/1306.1058v4) executam a construção para gravidade pura como séries formais e explicitam condições sobre a representação física; a extensão com matéria não é um teorema já executado ali para este sigma.

**Contrato quântico preciso.** Expandir a ação pelo mapa exponencial do alvo, construir produtos ordenados com extensão às diagonais que respeite causalidade e localidade, determinar a anomalia local `A_N` na primeira ordem N em que houver quebra, e provar `s A_N+d B_N=0`. Se `A_N=s C_N+d D_N`, redefinir os contra-termos por `−C_N` remove essa quebra. Repetir ordem a ordem fornece a equação mestra quântica como identidade de séries formais. A conclusão é condicional à trivialidade da classe apropriada e à realização dos produtos/identidades; a presente nota não mediu nem compilou essa sequência de contra-termos.

### Anomalia de difeomorfismos e anomalia do traço

[KNOWN, escopo] A classificação de [Barnich–Brandt–Henneaux, seções 2, 4 e 10.4](https://arxiv.org/pdf/hep-th/9505173) contempla sistemas normais Einstein–matéria e identifica as candidatas locais. Em quatro dimensões, sem calibre interno quiral, os escalares reais deste modelo não trazem o mecanismo usual de anomalia gravitacional local quiral. As candidatas topológicas de vielbein listadas ali começam em outras dimensões. O resultado não identifica automaticamente um formalismo global de sigma com alvo S³ com a álgebra de jatos considerada no artigo.

[DERIVED — contrato delimitado] Localmente, a carta do alvo é contrátil e há três escalares reais com Hessiana cinética não degenerada (`c>0`). Isso é compatível com aplicar a classificação no regime perturbativo local. Para fechar a inferência cohomológica completa, deve-se justificar sua passagem da álgebra polinomial de jatos do artigo à expansão formal dos coeficientes não polinomiais do sigma. Essa passagem e a implementação dos contra-termos não foram realizadas aqui: registra-se ausência do mecanismo quiral usual e uma rota cohomológica concreta, não um recibo de anomalia zero do modelo completo. Anomalias globais, junções de cartas e bordas continuam fora deste contrato local.

A expressão “trace type” naquela classificação refere-se a classes ligadas a fatores abelianos internos; não deve ser trocada automaticamente pela anomalia de Weyl de `T^μ_μ`. O nosso modelo minimal em quatro dimensões nem sequer é classicamente conforme: `T^μ_μ=−cQ` já é geralmente não zero. Preservar a Ward de difeomorfismos (`∇T` apropriado) não impõe traço zero. O resultado de [Hollands–Wald](https://arxiv.org/abs/gr-qc/0404074) garante uma escolha consistente com conservação para interações escalares polinomiais arbitrárias em espaço-tempo curvo fixo, dimensão maior que dois; ele não é uma construção de gravidade dinâmica sigma completa.

## 9. A família mínima de cinco probabilidades tem somente variações de calibre local

Este ponto distingue o que foi construído do que pode ser quantizado sem ampliar entradas.

**[DERIVED — proposição.]** Considere a mesma regra de Fisher refletido, rótulo selecionado 0, exatamente cinco probabilidades positivas normalizadas e diferencial de posto quatro. Fixe os mesmos k e as mesmas funções da construção. Toda perturbação suave local de P que preserve essas condições induz, em `(g[P],φ[P])`, uma transformação infinitesimal de difeomorfismos. Em particular, sua classe no quociente linear de calibre é zero.

**Prova.** Defina os campos

\[
R(x)=2\arcsin\sqrt{P_0(x)},\qquad
Z_a(x)=\sqrt{\frac{P_a(x)}{1-P_0(x)}}.
\]

A aplicação `F_P:x↦(R(x),Z(x))` tem domínio e imagem de dimensão quatro. Positividade e posto quatro tornam `F_P` um difeomorfismo local, pelo teorema da função inversa. A regra da métrica e a aplicação sigma são exatamente os pullbacks dos dados fixos da variedade `(0,π)×S³_+`:

\[
g[P]=F_P^*\big(dR^2-a(R)^2h_{S^3}\big),\qquad
\phi[P]=Z\circ F_P.
\tag{9.1}
\]

Para uma família Pε, escreva localmente `F_{Pε}=F_{P0}∘fε`, com `f0=id`. Então `g[Pε]=fε*g[P0]` e `φ[Pε]=fε*φ[P0]`. Derivar em ε fornece `δg=L_vg` e `δφ=L_vφ`, onde `v=(d/dε)fε|0`. Isso é K(v), como definido na seção 5. □

Controle explícito na carta do fundo: sejam `χ=δR` e `ξ=δZ`, com `Z·ξ=0`. O campo v é determinado unicamente por `v(R)=χ` e `dZ(v)=ξ`; a identidade de variação é

\[
\delta g_{\mu\nu}=2\partial_{(\mu}R\,\partial_{\nu)}\chi
-2aa'\chi W_{\mu\nu}-a^2 A_{\mu\nu}(\xi)
=\mathcal L_vg_{\mu\nu},\qquad\xi=\mathcal L_v\phi.
\tag{9.2}
\]

Consequências exatas:

- O habitante curvo permanece uma solução válida; a proposição não altera suas contas de Einstein, conservação ou área.
- A estacionariedade do pullback da ação acompanha a invariância por difeomorfismos. Ela não fornece quatro modos locais novos de matéria/gráviton para essa família mínima.
- Quantizar a ação ambiente da seção 1 admite perturbações `(h,ξ)` que não são da forma (9.2). Essa ampliação é [INPUT]. Não é deduzida apenas dos cinco pesos do exemplo.
- O argumento usa exatamente a igualdade entre a dimensão do simplex e a do espaço-tempo, o posto completo e a regra universal (9.1). Ele não prova que todas as famílias TGL sejam puro calibre. Com mais categorias, o mapa pode ser uma imersão em dimensão maior e a conclusão deixa de seguir; ainda seria preciso provar a dinâmica e os graus de liberdade dessa extensão.
- Não se conclui ausência de efeitos globais, bordas, transições de posto, observadores adicionais ou mudanças do rótulo selecionado. Tais dados não estão no contrato local acima.

Leitura relacionada nesta mesma sessão: [NOTA_DEGENERESCENCIA_E_RECIPROCO.md](../DEGENERESCENCIA_VARIACIONAL_FISHER_20260909_205440_2995947/NOTA_DEGENERESCENCIA_E_RECIPROCO.md) constrói um controle mais amplo com categorias subdivididas e direções normais invisíveis em primeira ordem, inclusive um contraexemplo ao recíproco variacional para constantes diferentes. A proposição acima foi deduzida diretamente para o caso mínimo e não depende de tomar essa outra análise como premissa.

## 10. Interações, EFT e o que o parâmetro positivo realmente garante

A ação sigma já possui vértices de derivadas. Em uma carta em torno de um ponto do alvo, usando `φ=(y,√(1−|y|²))`,

\[
\frac c2|d\phi|_g^2
=\frac c2\left(|dy|_g^2+\frac{(y\cdot dy)^2_g}{1-|y|^2}\right).
\]

Para o campo canônico `ψ=√c y`,

\[
\mathcal L_m=\frac12|d\psi|_g^2+
\frac1{2c}\frac{(\psi\cdot d\psi)^2_g}{1-|\psi|^2/c}.
\tag{10.1}
\]

Em unidades físicas de quatro dimensões, o coeficiente com dimensão de massa ao quadrado é a escala sigma; o número adimensional c do exemplo exige a calibração de unidades já apontada na nota do habitante. Após essa calibração, os termos `ψ^{2n}(dψ)²` têm acoplamentos de dimensão negativa. A expansão gravitacional também possui acoplamento de dimensão negativa. Logo não há fechamento por contagem de potências em um número fixo dos termos originais. Podem surgir invariantes com mais derivadas, como `R²`, `R_μνR^{μν}`, `R|dφ|²`, `( |dφ|² )²` e contrações distintas de quatro derivadas; é preciso fixar coeficientes de Wilson e condições de renormalização.

O regime EFT é uma expansão formal controlada por energias e curvaturas pequenas comparadas às escalas físicas escolhidas, até ordem finita especificada. Não se demonstrou convergência da série, remoção não perturbativa do corte, limite UV ou unicidade dos coeficientes de alta energia. Reabsorver uma anomalia por contra-termos locais preserva uma simetria; isso não prova renormalizabilidade com finitos parâmetros nem completude UV.

A literatura sigma algébrica encontrada [Carfora–Dappiaggi–Drago–Rinaldi](https://arxiv.org/html/1809.07652v2) trabalha com base **Riemanniana bidimensional**, operador elíptico e fluxo de Ricci na renormalização. É uma fonte primária pertinente para a técnica geométrica sigma, mas não um teorema de quantização Lorentziana Einstein–sigma em quatro dimensões. Não se importa seu alcance por semelhança de nomes.

O sinal `c>0` da ação mantém a métrica cinética tangente positiva. Se um protocolo auxiliar Gibbs usa um relógio orientado `s=αv²t²` com `α<0`, a resposta de entropia pode mudar de sinal mantendo os pesos positivos. Isso altera a orientação do protocolo; não justifica substituir c por uma cinética negativa em (10.1), nem introduz um ghost físico na ação. Estados de campos renormalizados também podem ter diferenças de energia negativas sem que sua norma seja negativa; identificá-los com o protocolo requer uma construção adicional.

## 11. Contratos encerrados por esta demonstração e próximos contratos

| Item | Estatuto nesta entrega | Conteúdo exato |
|---|---|---|
| Jacobi da matéria sigma | DERIVED | Fórmulas (2.1)–(2.3), potencial `−2/a² I₃`, condição tangente |
| Hessiana completa | DERIVED | Fórmulas (3.1)–(4.5), misturas até ordem um, símbolo `□I₁₃` |
| Green causal local | DERIVED + KNOWN | Contrato de onda em O globalmente hiperbólico satisfeito |
| Calibre e álgebra CCR acoplada | DERIVED | (5.2), (6.1)–(6.3), forma pré-simplética no quociente |
| Hadamard de matéria em g fixada | DERIVED + KNOWN | Teorema de feixe real positivo aplicável a J |
| Estado Hadamard físico acoplado | OPEN | Bisolução de calibre, positividade no quociente e representação |
| Nilpotência BRST clássica | DERIVED | (8.1), equação mestra clássica da ação escolhida |
| BV renormalizado do sigma acoplado | OPEN/contrato | Produtos, anomalia e contra-termos não executados nesta nota |
| Família mínima de cinco P | DERIVED | Variações locais são K(v); extensão ambiente é INPUT |
| UV / modelo quântico completo | OPEN | Não segue de nenhum dos resultados acima |

**Uma folha formal concreta recomendada:** `MinimalCategoricalPullbackGauge.lean`. Registrar uma aplicação suave localmente invertível F entre variedades de dimensão quatro, uma família Fε e tensores/alvos fixos; provar que a derivada de `Fε*G` e `Φ∘Fε` é a ação de Lie do mesmo v. Especializar a identidade algébrica (9.2) aos dados `(R,Z)` e à regra Fisher refletida. Esta folha é uma proteção de escopo efetiva para o modelo: impede que um teste de normalização ou um habitante curvo seja promovido a existência de modos gravitacionais quânticos locais nessa família mínima. Não se declarou essa folha já escrita ou compilada.

Para continuar a quantização ambiente, o próximo contrato analítico é construir uma covariância Hadamard compatível com (5.2) e positiva em `𝒱_obs`, ou fornecer um teorema primário que cubra exatamente o sistema Einstein–sigma on-shell com suas hipóteses verificadas. Para quantizar somente dados P, o próximo contrato anterior a esse é escolher e provar uma extensão com modos locais fora de K(v). São duas tarefas matemáticas distintas.

## 12. Proveniência e limites de custódia

As fontes locais de entrada são a nota do habitante, seu recibo e manifesto, a folha de métrica Fisher selecionada e a folha de variação da densidade escalar. Os caminhos e hashes são lidos do disco pelo script acompanhante. A compilação PASS histórica dessas folhas não é uma compilação desta nota, nem dos propagadores, da álgebra CCR ou do BV.

Os links externos acima apontam somente a fontes primárias consultadas. A nota separa resultados importados da literatura das deduções específicas do exemplo, e distingue passagem condicional de hipótese verificada. Nenhum estado do gate canônico é alterado por esta entrega. O trabalho não declara gravidade quântica resolvida, confirmada ou completa.
