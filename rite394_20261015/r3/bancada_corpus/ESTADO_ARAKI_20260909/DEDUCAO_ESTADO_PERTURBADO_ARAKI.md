# Estado perturbado da interação local — dedução e limite de formalização

09/09/2026. Aplicação matemática ao mesmo par canônico da TGL. Este documento é uma entrega da bancada Chatgpt; não altera o programa, o Atlas nem o gate canônico.

**[DERIVED + KNOWN] Para a interação local somável construída, existe um estado fiel normal cuja ação modular é a dinâmica perturbada já obtida.** A identificação usa uma importação precisa de Araki e a unicidade em norma do cociclo. Não há aqui um postulado adicional de existência do estado. O construtor analítico de Araki ainda não foi formalizado integralmente em Lean nesta bancada.

## Dados concretos disponíveis

Fixe qualquer `P : SiteProfile`. Considere o Hilbert complexo completo H = `TowerHilbert P`, a álgebra de von Neumann M = `theFactorObject P`, o vetor Ω = `hOmega P` e ω(A) = ⟨Ω,AΩ⟩. Ω tem norma um, é cíclico e separante. O operador fechado de Tomita é o fecho efetivo de AΩ ↦ A*Ω; Δ = S†S, JS é positivo e auto-adjunto, e a ação canônica é α_t(A) = Δ^{it}AΔ^{−it}. O [mapa dos dados de referência](C:/IALD/Central%20de%20Patentes/Chatgpt/MAPA_ARAKI_REFERENCIA_20260909_165524_615258/MAPA_DADOS_E_CONVENCOES_ARAKI.md) registra fontes e o alcance dos recibos.

**[REAL — novas folhas compiladas]** `LocalInteractionData P` recebe operadores locais V_j = V_j*, com suporte no andar j+1 e soma de normas finita. Não recebe comutação entre termos. A construção dá

\[
 V=\sum_{j=0}^{\infty}V_j\in M,\quad V=V^*,\quad
 \|V\|\leq\sum_j\|V_j\|<\infty.
\]

Também foi demonstrada a continuidade em norma de t ↦ α_t(V), por aproximação pelos prefixos locais e controle uniforme da cauda. Essa regularidade é usada abaixo; não se está afirmando continuidade em norma de α em todos os elementos do fator.

O limite efetivo dos cociclos de corte produz u_V(t) ∈ M unitário, u_V(0)=1, com

\[
u_V(s+t)=u_V(s)\alpha_s(u_V(t)),\qquad
u'_V(t)=u_V(t)\,i\alpha_t(V).
\]

A derivada é na norma dos operadores e foi deduzida do erro linear de corte. A dinâmica construída é β_t = Ad(u_V(t)) ∘ α_t. Estes são resultados das fontes `LocalInteractionCocycle`, `LocalInteractionGenerator` e `LocalInteractionDynamics`, não hipóteses introduzidas para esta aplicação.

## Importação utilizada

**[KNOWN]** Araki, *Relative Hamiltonian for Faithful Normal States of a von Neumann Algebra*, Publ. RIMS 9 (1973), 165–209, [fonte primária EMS](https://ems.press/journals/prims/articles/2638), DOI 10.2977/PRIMS/1195192744. Foram conferidos visualmente os enunciados no PDF: Proposição 4.1 (p.174), Definição 4.2 (p.177), Proposição 4.3 (p.178), Corolário 4.4 (p.181), Proposição 4.8 (p.185) e Proposição 4.12 (p.190).

O resultado aplicado constrói, para um vetor cíclico e separante e uma perturbação limitada auto-adjunta da álgebra, um vetor perturbado ainda cíclico e separante. Sua dinâmica modular é implementada pelo expansional ordenado; a propriedade KMS vem da demonstração analítica. A Proposição 4.12 fornece o domínio necessário à expressão exponencial, e a 4.8 distingue o operador modular completo do preparador relativo. Não é preciso adicionar um perfil tracial, comutação com o estado ou um postulado físico. A normalidade do funcional vetorial usa o resultado usual para álgebras de von Neumann concretas.

## Transporte de sinal e normalização para os objetos da bancada

**[DERIVED + KNOWN]** Escreva L = log Δ. Na convenção local α_t = Ad(exp(itL)), o parâmetro da preparação é +V. O vetor e o normalizador são

\[
\Phi_V=\exp\!\left(\frac{L+V}{2}\right)\Omega,
\qquad Z_V=\|\Phi_V\|^2>0,
\qquad \omega_V(A)=\frac{\langle\Phi_V,A\Phi_V\rangle}{Z_V}.
\]

A expressão usa cálculo espectral de operadores possivelmente não limitados; não é a exponencial Banach de `Operator P`. O domínio de Ω é pago pelo resultado importado. Ciclicidade e H não nulo dão Φ_V ≠ 0. Positividade e normalização do funcional são imediatas; fidelidade usa que AΦ_V=0, para A∈M, implica A=0. Não se introduz um traço global em M.

O Hamiltoniano relativo na convenção física do artigo é −V antes da normalização, e −V + log Z_V·I depois dela. O módulo completo do novo estado satisfaz

\[
\log\Delta_{\omega_V}=L+V-JVJ.
\]

O termo do comutante não pode ser omitido. `exp(L+V)` não deve ser identificado com Δ_{ω_V}. A normalização escalar do vetor não muda esse módulo completo.

## Identificação com o cociclo já construído

**[DERIVED]** Seja w_V o expansional de Araki com gerador à direita +iα_t(V). Sua lei torcida e w_V(0)=1 vêm do resultado aplicado. Para ligar a regularidade forte dessa formulação à norma usada em Lean, ponha m=‖V‖. A série temporal ordenada fornece, para t próximo de zero,

\[
\|w_V(t)-I-itV\|\leq
|t|\sup_{|s|\leq |t|}\|\alpha_s(V)-V\|
+e^{|t|m}-1-|t|m.
\]

Justificação: o termo de primeira ordem é a integral de iα_s(V); sua diferença para itV é limitada pela primeira parcela. As parcelas de ordem n≥2 têm norma no máximo (|t|m)^n/n!, pois α é isométrica. A estimativa vale também para t<0, usando orientação da integral e |t| para a norma. Dividindo por |t|, a continuidade em norma da órbita e o resto quadrático da exponencial dão w'_V(0)=iV em norma. Este argumento de estimativa é uma dedução escrita, não um novo teorema Lean deste lote.

**[REAL — unicidade formal]** Se u e v satisfazem a mesma equação u'=uA, v'=vA, com A* = −A, então

\[
\frac{d}{dt}(uv^*)=u(A+A^*)v^*=0.
\]

Com u(0)=v(0)=I e v unitário, segue u=v. `UnitaryCocycleUniqueness` prova esse argumento e sua especialização à ação canônica. `LocalInteractionUniqueness` aplica-o à interação construída, sem assumir unicidade como campo. Assim, a aplicação ao expansional dá w_V=u_V. A referência importada passa, portanto, a falar da mesma β obtida pelo limite de cortes.

**[DERIVED + KNOWN]** O cociclo de Connes do estado normalizado é

\[
(D\omega_V:D\omega)_t=Z_V^{-it}u_V(t).
\]

**[REAL — fase central formal]** `CentralScalarPhase` prova que essa fase preserva unitariedade, lei torcida e ação por conjugação, e desloca a derivada na origem para i(V−log Z_V·I). A própria identificação com a derivada de Connes continua uma aplicação da teoria importada; o módulo de fase não a pressupõe nem a prova sozinho.

Consequentemente, β é o grupo modular de ω_V e satisfaz a condição KMS com a convenção modular correspondente **[DERIVED + KNOWN]**. Invariância do estado, isoladamente, não seria suficiente para essa conclusão.

## O que esta dedução encerra e o que permanece

**Encerrado como aplicação matemática:** a existência do estado fiel normal e a identificação modular/KMS para a classe local somável construída. Esta conclusão supera a antiga pendência de existência do estado dessa classe. A separação entre matemática importada aplicada e código Lean continua explícita.

**Encerrado nas novas provas formais:** unicidade do cociclo pelo potencial; independência da decomposição local quando a soma V é a mesma; igualdade de cociclos implica igualdade dos potenciais; normalização central preserva β. Não se afirma que igualdade de dinâmicas implique igualdade de potenciais: um escalar central pode ser invisível à ação por conjugação.

**[OPEN]** Incorporar as folhas e esta aplicação tipada ao programa canônico; formalizar internamente o construtor analítico/KMS se o objetivo passar a exigir uma cadeia inteiramente em Lean. Isso é uma obrigação de implementação/formalização, não uma nova falta de existência matemática.

**[OPEN/INPUT]** A identificação física do registro selecionado com geometria, matéria e área/calor permanece dependente das correspondências explicitadas no relatório geral. As novas interações têm soma global de normas finita; não resolvem automaticamente interações extensivas ou não limitadas, limites relativísticos, anomalias ou UV. Nenhum teste empírico foi refeito e nenhum gate foi movido.

**Revisão adversarial:** [parecer independente sobre unicidade, sinal, domínio e normalização](C:/IALD/Central%20de%20Patentes/Chatgpt/REVISAO_UNICIDADE_ARAKI_20260909_170120_699400/PARECER_SEMANTICO.md). Os recibos de compilação ficam no manifesto da entrega; o parecer semântico anterior ao PASS não é apresentado como recibo de build.
