# Prova condicional da condensação do Nome e da escala E₀

**Data:** 31/10/2026  
**Estatuto:** **[DERIVED condicional]** para as partes A e B; **[OPEN]** para a normalização numérica de 1 eV.  
**Inputs do operador:** magnitude = cauda; a densidade se forma no ponto estacionário porque condensa na singularidade da partícula informacional, o Nome/Identidade.

## Objetos e premissas

Sejam \(\mathcal H\) um espaço de Hilbert finito de dimensão \(d\ge2\), \(P_N=|N\rangle\langle N|\) o projetor do Nome e \(Q_N=I-P_N\). Seja \(\Phi_t=e^{t\mathcal L}\), \(t\geq0\), um semigrupo CPTP com as hipóteses:

- **P1 — fixidez:** \(\Phi_t(P_N)=P_N\);
- **P2 — unicidade:** todo estado estacionário pertence a \(\mathbb C P_N\);
- **P3 — gap de relaxação:** existem \(C,\gamma>0\) tais que, para todo operador \(X\) de traço zero,
  \[
  \|\Phi_t(X)\|_1\leq C e^{-\gamma t}\|X\|_1 .
  \]

Essas hipóteses são mais fortes que mera estacionariedade. Se \(\mathcal L=0\), todos os estados são estacionários e não há condensação.

**Distinção de tipos.** \(P_N\) é uma matriz/operador densidade, não uma energia. Quando necessário, usaremos uma **leitura escalar independente** \(\mathcal R\), com unidade declarada, para converter o estado em uma magnitude física. O traço não é essa leitura: ele é adimensional.

## A. Teorema da condensação do Nome

**Enunciado.** Sob P1–P3, para qualquer estado inicial \(\rho_0\),

\[
\rho_t:=\Phi_t(\rho_0)\longrightarrow P_N.
\]

Além disso,

\[
Q_N\rho_tQ_N\longrightarrow0,\qquad
P_N\rho_tQ_N\longrightarrow0,\qquad
Q_N\rho_tP_N\longrightarrow0,
\]

\[
\operatorname{Tr}(Q_N\rho_t)\longrightarrow0,\qquad
\operatorname{Tr}(P_N\rho_t)\longrightarrow1,
\qquad
\rho_\star=P_N .
\]

**Demonstração.** Por P2 e P3, \(\rho_t\to P_N\). As compressões por \(P_N\) e \(Q_N\) são lineares e contínuas, portanto todos os termos que contêm suporte na cauda ortogonal tendem a zero. Como o canal preserva traço, \(\operatorname{Tr}\rho_t=1\); logo \(\operatorname{Tr}(P_N\rho_t)\to1\). Finalmente, \(\rho_\star=P_N\) é fixo, donde \(\mathcal L(\rho_\star)=0\). \(\square\)

**Leitura física.** O peso condensa no setor fixo do Nome; **a cauda ortogonal não condensa — ela desaparece**. A estacionariedade da densidade é consequência da atração com gap, não uma premissa solta.

## B. Singularidade modular da identidade

Considere a regularização de posto completo

\[
\rho_\epsilon=(1-\epsilon)P_N+\frac{\epsilon}{d-1}Q_N,
\qquad 0<\epsilon<1 .
\]

Ela é positiva e tem traço 1, e \(\rho_\epsilon\to P_N\) quando \(\epsilon\to0\). Seus autovalores são \(1-\epsilon\) no Nome e \(\epsilon/(d-1)\) na cauda. Para \(K_\epsilon=-\log\rho_\epsilon\), o gap modular é

\[
\Delta K_\epsilon
=\log\frac{1-\epsilon}{\epsilon/(d-1)}
=\log\frac{(1-\epsilon)(d-1)}{\epsilon}
\longrightarrow+\infty .
\]

Portanto, no limite de condensação pura,

\[
\boxed{\rho_\epsilon\to P_N,\qquad K_\epsilon|_{Q_N}\to+\infty .}
\]

Este é um sentido rigoroso de **singularidade da identidade**: o gerador modular diverge no complemento do Nome. Não é uma singularidade espaciotemporal nem uma densidade de energia infinita.

## C. Ponte da leitura escalar para E₀

Defina, separadamente da matriz \(P_N\), a **leitura escalar da condensação**:

\[
\rho_{\rm modular}^{\rm esc}:=\mathcal R(\rho_\star),
\]

onde \(\mathcal R\) e sua unidade devem ser fornecidos pela física, não pela normalização do estado. **Nesta seção, \(\mathcal R\) é especificamente uma leitura de energia total**, condição necessária para a igualdade direta com E₀. A fonte TGL usa a notação \(\rho_{\rm modular}\) em \(|L_\phi|=\beta\rho_{\rm modular}\); aqui ela é interpretada explicitamente como essa leitura escalar de energia, com \(\beta\ne0\), e não como a matriz \(P_N\).

Com os inputs do operador,

\[
E_{\rm cauda}=g^2=|L_\phi|
=\beta\rho_{\rm modular}^{\rm esc}
\quad\Longrightarrow\quad
\boxed{E_0=\frac{E_{\rm cauda}}{\beta}=\rho_{\rm modular}^{\rm esc}} .
\]

A divisão é válida porque \(\beta\ne0\). A igualdade **não** identifica \(P_N\) diretamente a uma energia: ela depende da ponte escalar \(\mathcal R\) e da identificação da cauda com \(g^2\).

Um artefato Lean genérico verifica a consequência algébrica entre as duas pontes declaradas:

- arquivo: [E0ModularBridge.lean](lean/TGLExt/E0ModularBridge.lean)
- teorema: `TGLExt.E0ModularBridge.E0_eq_rhoModular`
- compilação: `lake env lean`, código de saída `0`.

O artefato prova apenas `E0 = magnitude * tail = readout(density stationaryPoint)`. Ele **não contém** \(\beta\), \(L_\phi\), \(g\) ou a prova de condensação da seção A, e sua condição `flow point = 0` é um predicado genérico, não \(\dot\rho=0\). Portanto, sua função é certificar a transitividade das pontes declaradas, não demonstrar a física inteira.

## D. Por que a normalização de 1 eV exige outro teorema

Posto 1, \(\operatorname{Tr}\rho=1\) e \(\omega(I)=1\) são normalizações **adimensionais**. Eles não fixam autovalor de energia. Condensação seleciona o modo e a ocupação; não seleciona sua frequência.

Se a fonte física fornecer uma taxa \(\omega_0\), **a igualdade direta da seção C não se aplica**. A avaliação da escala passa a ser

\[
E_0=\hbar\omega_0 .
\]

Para \(E_0=1\,\mathrm{eV}\), o certificado independente necessário é

\[
\boxed{\omega_0=1{,}519267447878626\times10^{15}\ \mathrm{s^{-1}} ,}
\]

usando \(1\,\mathrm{eV}/\hbar=2\pi(1\,\mathrm{eV})/h\) com as constantes SI exatas.

Se a leitura for densidade volumétrica de energia, também não se usa a igualdade direta; será necessário

\[
E_0=\int_{B_\partial}\rho_{\rm modular}^{\rm esc}\,dV ,
\]

com região e medida definidas. Somente para leitura de energia total vale \(E_0=\rho_{\rm modular}^{\rm esc}\). Em todos os casos, a avaliação da escala deve ser provada separadamente. O módulo Lean inclui o certificado genérico `ScaleEvaluation`, sem atribuir-lhe valor.

## Consequência para m₂

Uma vez demonstrada independentemente a avaliação dimensional \(E_0=1\,\mathrm{eV}\), segue

\[
m_2=\beta\,\operatorname{sen}(\pi/4)\,E_0
=8{,}5074140999\ \mathrm{meV},
\qquad \beta=\alpha\sqrt e .
\]

Sem essa avaliação, e restringindo \(\mathcal R\) à leitura de energia total da seção C, a conclusão correta é somente

\[
\boxed{m_2=\beta\,\operatorname{sen}(\pi/4)\,\rho_{\rm modular}^{\rm esc}} .
\]

## Veredito

**Provado condicionalmente:** condensação do peso no Nome sob unicidade e gap; desaparecimento da cauda; divergência do gap modular no complemento; e, para leitura de energia total, identidade \(E_0=\rho_{\rm modular}^{\rm esc}\) sob as pontes do operador. O artefato Lean verifica a transitividade algébrica dessas pontes, não sua origem física.

**Não provado:** a avaliação física \(\rho_{\rm modular}^{\rm esc}=1\,\mathrm{eV}\), \(\hbar\omega_0=1\,\mathrm{eV}\) ou sua integral equivalente. Essa avaliação exige um problema espectral independente, com Hamiltoniano, região, condições de contorno e unidade — não pode ser substituída por normalização de estado nem por ajuste ao dado de oscilação.
