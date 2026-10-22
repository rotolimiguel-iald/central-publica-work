# Dedução prévia — protocolo misto quadrático

[INPUT] Mantém-se a referência ρ₀=diag(p,1−p), com k=1/2 log(p/(1−p)), e agora fixa-se W=X+Z. A medição é E±=(I±Z)/2, isto é, a álgebra espectral da própria referência. Escolhe-se explicitamente o parâmetro de preparação s=velocity²·t². Esta mudança de relógio/probe é uma escolha de protocolo, não uma consequência já derivada da teoria.

[DERIVED] logρ₀+sW=aI+sX+(k+s)Z, r(s)=√((k+s)²+s²). A exponencial hermitiana dá m_z(s)=(k+s)tanh(r)/r e q±(s)=(1±m_z(s))/2. Para k>0, r(s)>0 para todo s, r(0)=k e r′(0)=1. Logo
m_z′(0)=tanh(k)/k+k[(k sech²k−tanh k)/k²]=sech²k.
A derivada q+′(0)=sech²k/2.

A base q₀ é (1±tanh k)/2 e log(q₀−/q₀+) = −2k. Assim S′ com respeito a s = −k sech²k, sem escolher T. Com o probe quadrático,
ΔShannon/t² → −k sech²k velocity².
O tangent com respeito a t é zero, o Fisher temporal na origem é zero e D diagonal/t²→0. Pela identidade D=ΔK−ΔS, o incremento modular da medição tem o mesmo coeficiente.

[DERIVED — identificação precisa] Como E± diagonaliza ρ₀, Σ_i(−log q₀i)E_i=−logρ₀. Portanto o incremento modular medido é exatamente Tr((ρ_s−ρ₀)(−logρ₀)), para todo s. Isso difere do protocolo inclinado de controle, cujo observável K_E não era o gerador modular da referência.

Para k>0, o coeficiente entrópico é negativo e a razão −coeficiente/π é positiva. No setor k=0, a referência é tracial e a resposta de ordem t² se anula; para k<0, o mesmo protocolo tem sinal oposto. A folha inicial será explicitamente k>0. O potencial X+Z não comuta com logρ₀ quando k≠0; a componente transversal X permanece efetiva, enquanto a componente Z fornece a resposta modular de primeira ordem.

[OPEN/INPUT] O matching de área, o significado físico do probe e a identificação com calor geométrico continuam leis explícitas da composição. Nenhum T entra na definição da curva. Não se mede custo de colapso nem Meia-Nat. A formalização escalar não conta como nova demonstração Lean da identidade matricial de Gibbs ou do teorema geral de Araki; essas identificações recebem demonstração escrita separada.
