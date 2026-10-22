# Primeira variação do normalizador de Araki

Data: 09/09/2026. [DERIVED + KNOWN] Demonstração escrita, a partir dos domínios e cotas do artigo primário de Araki. Não é um novo teorema Lean compilado.

Referência: H. Araki, Relative Hamiltonian for Faithful Normal States of a von Neumann Algebra, Publ. RIMS 9 (1973), 165–209. [Página primária EMS](https://ems.press/journals/prims/articles/2638). [PDF local conferido](<C:/IALD/Central de Patentes/Chatgpt/ESTADO_ARAKI_20260909/Araki_1973_Relative_Hamiltonian.pdf>). Foram relidas a fórmula (3.1), a cota (3.2), o simplex (4.2) e a série (4.1); as páginas impressas 170 e 174 foram também conferidas visualmente nas imagens deste lote.

## Enunciado e convenção

Seja M uma álgebra de von Neumann no espaço de Hilbert H, Ω cíclico e separante com ‖Ω‖=1, Δ seu operador modular e ω(A)=⟨Ω,AΩ⟩. Seja W=W*∈M limitado. Para s real, tome o vetor de Araki

Φ(s)=Ω(sW)=exp((log Δ+sW)/2)Ω,

e Z(s)=‖Φ(s)‖². A igualdade com o exponencial é a aplicação da Proposição 4.12, pp. 190–191, com H_Ω=−log Δ. A prova abaixo usa a série vetorial: ela não trata log Δ como operador limitado nem diferencia uma exponencial em norma de operadores.

Então, em norma de H,

Φ′(0)=B,  B=∫₀^{1/2} ΔʳWΩ dr,

e as derivadas reais satisfazem

Z′(0)=ω(W),    (log Z)′(0)=ω(W).

O sinal positivo corresponde à convenção de potencial +sW em log Δ+sW. Na convenção de Hamiltoniano relativo físico de Araki, esse potencial corresponde a −sW.

## 1. Domínio e cota dos coeficientes

O Teorema 3.1, p. 170, trata produtos de potências modulares no tubo cuja soma dos tempos imaginários tem módulo até 1/2. Sua extensão vetorial é fortemente contínua no fecho e tem norma limitada pelo produto das normas dos operadores vezes ‖Ω‖. Aplicando-o aos fatores W, a Proposição 4.1, p. 174, fornece a série

Φ(s)=Σ_{n=0}^∞ sⁿ C_n,

C_n=∫_{r_j≥0, Σ_j r_j≤1/2} Δ^{r_n}W ··· Δ^{r_1}WΩ dr₁···dr_n,

com C₀=Ω. Os produtos são tomados em seus domínios do teorema e, nas faces, pela extensão contínua empregada na proposição. Não se afirma que Δʳ seja limitado em H.

O integrando tem norma ≤‖W‖ⁿ. O volume do simplex é (1/2)ⁿ/n!, de modo que

‖C_n‖≤‖W‖ⁿ/(2ⁿ n!).

Esta cota com o fator 2⁻ⁿ foi deduzida aqui do volume explícito; a estimativa suficiente impressa no artigo é mais frouxa. A continuidade forte e a cota no simplex compacto garantem a integral de Bochner.

Para n=1, os vetores ΔʳWΩ são os vetores efetivos do domínio para 0≤r≤1/2. No extremo r=1/2, isso também decorre do domínio de Tomita sobre MΩ; r=0 é imediato. Ω é autovetor modular de autovalor 1, logo ΔʳΩ=Ω.

## 2. Derivada em norma do vetor

Pondo c=|s|‖W‖/2, a cauda após o termo linear satisfaz

‖Φ(s)−Ω−sB‖ ≤ Σ_{n≥2} cⁿ/n! = eᶜ−1−c ≤ c²eᶜ/2.

Assim, o resto dividido por |s| tende a zero dos dois lados, provando Φ′(0)=B em norma de H. Esta etapa não exige W no centralizador nem diferenciabilidade em norma de t↦α_t(W). A regularidade necessária foi fornecida pela série vetorial da perturbação limitada.

## 3. Derivada do normalizador

Como Δʳ é auto-adjunto e os dois vetores estão no domínio,

⟨Ω,ΔʳWΩ⟩=⟨ΔʳΩ,WΩ⟩=ω(W).

A funcional linear contínua dada pelo produto interno com Ω comuta com a integral. Portanto,

⟨Ω,B⟩=ω(W)/2.

W=W* garante que ω(W) é real. Pela regra de derivação da norma ao quadrado,

Z′(0)=2 Re⟨Ω,B⟩=ω(W).

Temos Z(0)=1. O Corolário 4.4 garante que Φ(s) é cíclico e separante, em particular não nulo, para todo s real; para a derivada de log Z na origem bastaria também a positividade local decorrente da continuidade. Logo

(log Z)′(0)=Z′(0)/Z(0)=ω(W).

Não foi usada uma função traço de Gibbs nem um operador densidade global. O argumento vale no fator canônico com P:SiteProfile arbitrário, uma vez aplicados os dados de representação modular já conferidos no [mapa de referência modular](<C:/IALD/Central de Patentes/Chatgpt/MAPA_ARAKI_REFERENCIA_20260909_165524_615258/MAPA_DADOS_E_CONVENCOES_ARAKI.md>) e no [parecer de aplicação de Araki](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_FINAL_ARAKI_20260909_170730_304080/PARECER_FINAL_ARAKI.md>).

## 4. Resposta do estado normalizado

Defina Ω_s=Φ(s)/√Z(s) e ω_s(A)=⟨Ω_s,AΩ_s⟩ para A∈M limitado. Segue por regras de produto e cadeia:

Ω′₀=B−(ω(W)/2)Ω,

ω′₀(A)=⟨B,AΩ⟩+⟨Ω,AB⟩−ω(W)ω(A).

A convenção aqui é produto interno conjugado-linear na primeira entrada. Para A=A*, a soma dos dois primeiros termos é 2 Re⟨B,AΩ⟩. Para um efeito E_i de uma medição previamente fixada, a mesma expressão fornece p′_i(0) com p_i(s)=ω_s(E_i). Esta é uma resposta do mesmo estado construído, antes de escolher T.

Se E_i≥0, E_i≠0 e Σ_iE_i=1, a fidelidade e normalização dos estados de Araki dão p_i(s)>0 e Σ_i p_i(s)=1. A fórmula implica Σ_i p′_i(0)=0, como deve ser: substituindo A=1, ω′₀(1)=0.

## 5. Controle central e limites do resultado

Para c real fixo, a perturbação W−c·1 satisfaz

Φ_{W−c1}(s)=e^{−cs/2}Φ_W(s),    Z_{W−c1}(s)=e^{−cs}Z_W(s).

Logo ω_s permanece igual. Tomar c=ω(W) centra (log Z)′(0), mas não altera p′_i(0) nem a derivada de Shannon. Não resolve, por escolha de uma constante, a condição de equilíbrio S′(0)=0 que um matching de área em t² exigiria.

Esta nota demonstra a primeira variação em torno do estado de referência para V=sW. Para trabalhar em torno de V arbitrário, a rota é aplicar a construção ao estado ω_V e justificar a composição das perturbações; esse passo não está sendo contado aqui como novo teorema compilado.

O normalizador Z não é o operador modular completo. Na representação padrão da construção de Araki, log Δ_V=log Δ+V−JVJ; a constante de normalização não altera Δ_V. O operador de preparação log Δ+V, o módulo completo e o cociclo normalizado Z^{−it}u_V têm papéis distintos.

Nada nesta primeira derivada identifica automaticamente ω(W) com energia local gravitacional, escolhe o observável W, produz o tensor T, paga conservação ou demonstra a lei de área. Também não prova uma igualdade entre Fisher clássico de uma medição e a métrica quântica de informação. É uma resposta matemática concreta do estado, disponível para construir o próximo elo com hipóteses físicas explícitas.
