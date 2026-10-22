# Domínio dos quatro relógios físicos e localização da classe causal

10/09/2026, etapa088. [DERIVED — auditoria matemática escrita de domínio] [KNOWN — importações primárias delimitadas]. Nenhuma execução matemática, CAS, Lean, importação/execução de um.py ou alteração de fontes canônicas. Esta nota não constrói a homotopia BV nem declara remoção de anomalias.

## 1. Resultado efetivo

A inversa de E=(dφ̄,dX̄), com X=g⁻¹·φ*γ, é uma operação natural de jatos finitos, real e analítica onde E tem posto quatro. Esse domínio contém todo M=(0,π)×S³ do fundo físico069. A construção pode ser global no fibrado φ̄*TS³⊕ℝ; não depende de três coordenadas escalares globais em S³. Em cada compacto interior, a inversa e suas derivadas são regulares e a condição de posto persiste em uma vizinhança dos fundos.

Isso NÃO a coloca na classe universal regular074: aquela classe proíbe explicitamente as inversões de jatos que retiram os mapas constantes. Aqui há uma localização concreta da classe de coeficientes. Ela é matematicamente legítima, mas não se identifica automaticamente com toda a liberdade de normalização Q2. A distinção não é nominal: mostramos um polo real de ζ em uma família analítica de fundos não degenerados, e impossibilidade de estender a própria inversa ao sigma constante. Uma primitiva particular pode ter cancelamentos adicionais; a singularidade da receita não exclui todas as outras receitas.

## 2. Qual contrato está sendo consumido

| Fonte e domínio | Consequência para a rota088 |
|---|---|
| [Q2_069, §§1–3](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md:5>) | Fundo físico on-shell; flutuações, ghosts e antifields off-shell; ξ é seção de φ̄*TS³; testes compactos interiores. Coeficientes de vértices são locais e suaves nos dados de fundo. |
| [Contrato072, §§3–5](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md:36>) | Primitiva de densidade, ordem finita e peso correto são condições necessárias. Ainda contam regularidade, escala da extensão, aplicações multilineares D_n, inserções, realidade e contatos. |
| [Ward072, §§6–8](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md:118>) | Coeficientes externos suaves multiplicam os produtos do esquema T₀, com Leibniz sobre suas derivadas. Não se diferencia informalmente o propagador; não se identificam todos os esquemas de fundos distintos. |
| [Classe074, §1](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_E_CURVATURA_B0_074_20260910/NORMALIZACAO_S_E_OBSTRUCAO_EULER.md:13>) | Jatos derivados polinomiais, valores sigma suaves, métricas inversíveis; linha18 exclui inversões de dφ/curvaturas que eliminem os controles constantes. A classe localizada abaixo é diferente. |
| [Aplicação075, §§3–5](<C:/IALD/Central de Patentes/Chatgpt/APLICACAO_DESCIDA_OFFSHELL_075_20260910_022420_157704/APLICACAO_OFFSHELL_E_FONTES_CENTRAIS.md:30>) | A consistência e a descida usam jatos dinâmicos livres; B₀ fica na categoria causal disponível. Restringir/localizar somente os coeficientes não impõe EOM aos ghosts ou antifields. Fontes de ghost positivo não podem ser escondidas nos coeficientes. |

Naturalidade significa transportar conjuntamente espaço-tempo, métrica de fundo e mapa sigma. Não significa invariância BRST dos fundos quando eles são mantidos inertes. A apresentação é MÉTRICA, conforme a [precisão de frame074](<C:/IALD/Central de Patentes/Chatgpt/HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/PRECISAO_FRAME_LOCAL_074.md:34>); não se importam regras para um ghost Lorentz independente.

## 3. Inversa intrínseca e aberto de jatos

Para um fundo B=(g,φ), defina

\[
 X_B=g^{\mu\nu}\gamma_{AB}(\phi)\partial_\mu\phi^A\partial_\nu\phi^B,
 \qquad E_B:TM\longrightarrow\phi^*TS^3\oplus\mathbb R,
 \quad v\longmapsto(d\phi(v),dX_B(v)).                 \tag{1}
\]

E usa jatos de φ até ordem dois e de g até ordem um. É inversível precisamente quando rank(dφ)=3 e dX não se anula na reta ker(dφ). Esse critério é independente de cartas. Seja Ω=φ*vol_γ e defina Δ por

\[
 dX\wedge\Omega=\Delta\,\mathrm{vol}_g.              \tag{2}
\]

Então E é inversível se e somente se Δ≠0. Em qualquer apresentação de (1), sua inversa é a matriz adjunta dividida pelo determinante. As mudanças de base dos dois fibrados cancelam nos produtos; pela unicidade da inversa, essas expressões colam. Em particular não há escolha de frame global. Sob uma isometria alvo A∈O(4), dφ ganha dA, X não muda e E⁻¹ compõe com dA⁻¹ no primeiro bloco. Portanto E⁻¹(ξ,δX) transforma como vetor de espaço-tempo. Se A inverte a orientação alvo, Ω e Δ mudam de sinal juntos, sem alterar a conclusão.

Uma fórmula para a coluna temporal torna a ausência de escolhas explícita: defina n por ι_n vol_g=Ω. Logo dφ(n)=0 e dX(n)=Δ, donde

\[
 E^{-1}(0,u)=\frac{u}{\Delta}n.                     \tag{3}
\]

Não se exigiu que ker(dφ) fosse temporal ou não nula para o critério geral; a inversão completa é apenas a de um mapa de fibrados. No fundo físico a reta é temporal. Também não se usou um inverso de operador diferencial ou um Green: esta inversa é pontual, de uma matriz feita de jatos.

Denote por J_clk o aberto Δ≠0 do espaço de jatos. No anel tensorial regular, admitir Δ⁻¹ produz uma localização; com coeficientes suaves ou analíticos trata-se da restrição correspondente a J_clk. A derivada horizontal continua definida, pois d_H(Δ⁻¹)=−Δ⁻²d_HΔ. Para a referência inerte, sΔ=0. Não é uma avaliação de todos os jatos de B₀ em constantes.

## 4. O fundo físico pertence ao domínio em todo o interior

Para a(r)=2cos(r/2), ḡ=dr²−a²γ e φ̄(r,z)=z,

\[
 \bar X=-\frac3{a^2}=-\frac3{4\cos^2(r/2)},\qquad
 \bar X'=\frac{6a'}{a^3}=-\frac{3\sin(r/2)}{4\cos^3(r/2)}<0
 \quad(0<r<\pi).                                  \tag{4}
\]

Como dφ̄ identifica o fator espacial e anula ∂r, Ē é inversível. Nas coordenadas produto, a componente temporal de Ē⁻¹(ξ,u) é u/X̄′ e a espacial é ξ. Intrinsecamente, n=a⁻³∂r e Δ=X̄′/a³. Além disso, (φ̄,X̄) é um difeomorfismo global

\[
 (0,\pi)\times S^3\ \longrightarrow\ S^3\times(-\infty,-3/4).
                                                               \tag{5}
\]

Usou-se a monotonicidade e os limites de (4); não se postulou uma carta ℝ³ cobrindo S³. Para fundos gerais, posto quatro fornece somente uma inversa LOCAL do mapa de relógios; não fornece sozinho injetividade global, propriedade de cobertura ou suporte uniforme de observáveis relacionais.

Se K⊂M é compacto, escolha um aberto de fecho compacto contendo K. Em normas auxiliares positivas sobre os fibrados, o menor valor singular de Ē tem mínimo estritamente positivo nesse fecho. Dependência contínua dos jatos prova persistência do posto em uma vizinhança C² dos dados ali. As normas servem só à prova de abertura, não são novos coeficientes da construção natural. A hiperbologia global continua uma condição da categoria causal; não decorre do posto de E.

Em toda a variedade não compacta, não se infere uma margem única no sentido da topologia compacta-aberta. Pode-se trabalhar compacto a compacto, como Q2, ou usar uma topologia fina apropriada. Os extremos temporais não foram acrescentados a M.

## 5. Regularidade, suporte e finitude que de fato sobrevivem

Soma, produto, derivação e inversão de matriz no aberto de matrizes inversíveis são suaves; a inversa é real-analítica. Portanto E⁻¹ é um operador natural de jatos finitos C∞ em J_clk e analítico em famílias já analíticas que permanecem nele. Isso é uma afirmação local em parâmetros e em compactos: uma família que alcança Δ=0 não está no domínio do teorema.

Na expansão g=ḡ+t h, φ=Exp_φ̄(tξ), a variação escalar δX contém h e uma derivada de ξ. Logo ζ=Ē⁻¹(ξ,δX) tem ordem diferencial finita e é linear nos jatos dinâmicos. A diferenciação de ζ prolonga essa ordem finitamente. Usar E dos campos completos formalmente também é possível quanto à inversão: o termo constante Ē é inversível, e cada coeficiente da série inversa requer somente finitíssimos produtos de coeficientes anteriores. Não se afirma convergência em t, nem invertibilidade diferencial da mudança completa de variáveis BV.

Multiplicação por Ē⁻¹ e operadores diferenciais locais não aumentam o suporte de uma variação compacta. Não introduzem, por si, propagação acausal ou novos pares de pontos singulares. Coeficientes suaves multiplicam distribuições sem ampliar sua frente de onda; derivadas locais tampouco ampliam essa frente. Isso não prova automaticamente todas as cotas de escala das novas inserções.

Há uma composição positiva precisa com075: no anel de coeficientes localizado em Δ̄, a linearização nos geradores dinâmicos Z anula os denominadores de fundo; d_H conserva o anel localizado. Extração de símbolos, divisões por inteiros, quantização covariante e integração por partes continuam finitas. Assim o lema075 de estabilidade dos coeficientes e a DESCIDA HORIZONTAL continuam válidos nesse domínio, desde que todos os geradores de ghost não zero, inclusive as fontes usadas, permaneçam livres e contabilizados. Esse argumento não constrói a homotopia de s nem sua extensão a contratermos.

Quanto a T4/T5, o resultado acima paga a regularidade deste multiplicador na categoria restrita. Não converte uma entrada C∞ em analítica. O [contrato072, §4](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md:58>) não havia imposto nem demonstrado analiticidade conjunta forte em toda família material; a opção adotada deve continuar explícita.

## 6. Peso homogêneo não equivale a admissibilidade causal

Na atribuição geométrica dim(g)=dim(φ)=0, dim(∂)=1 e dim(C)=−1, tem-se dim(X)=2, dim(dX)=3. As duas colunas de E⁻¹ têm pesos −1 e −3. Como dim(ξ)=0 e dim(δX)=2, ambas as parcelas de ζ têm peso −1, compatível com C. Em outra verificação, sob a mudança CONSTANTE g↦μ²g, φ fixo, vale E_μ=diag(1,μ⁻²)E; com h↦μ²h, também δX↦μ⁻²δX. A transformação de ζ é coerente. Essas são duas verificações tipadas, não uma troca silenciosa entre dimensão de engenharia e axioma causal T2.

O denominador não custa valência dinâmica quando pertence só a B₀. A troca linear C/ζ pode conservar o número de fatores; porém sua homotopia BV, o lift cotangente, os contatos de antifields e a filtração de laços/inserções ainda devem ser calculados. A conclusão não vem da palavra “doublet”.

Uma expressão racional de jatos pode ser homogênea e ter ordem finita, mas não ser polinomial nem regular no jato nulo. Portanto o peso acima NÃO prova que ela pertence à classe074 ou ao espaço dos D_n de uma prescrição universal. Na formulação efetiva de Q2, é necessário conferir para cada correção a cota transversal de derivadas da delta, a distribuição de derivadas entre inserções, os pesos de todos os coeficientes, e compatibilidade entre aridades. Os termos dχ de um cutoff e d(E⁻¹) na ação por partes permanecem presentes.

## 7. Dois controles explícitos de não extensão

**Fronteira temporal da receita física.** A métrica de (4) estende-se suavemente a r=0 com a(0)=2 e continua não degenerada. Todavia

\[
 \bar X'=-3r/8+O(r^3),\qquad (\bar X')^{-1}=-8/(3r)+O(r).
                                                               \tag{6}
\]

O polo não é apenas de uma matriz aplicada a argumentos inacessíveis. Tome ξ=0 e uma flutuação com h_{ij}=ḡ_{ij}, h_{rμ}=0, perto do ponto. Então δX=−X̄=3/a² e

\[
 \zeta^r=\frac{\delta X}{\bar X'}=\frac{a}{2a'}\sim-2/r.
                                                               \tag{7}
\]

Isso exclui uma extensão regular desta receita à fatia r=0, mas não invalida sua aplicação a suportes compactos no M de069. Em r=π a própria métrica degenera, outra fronteira que não foi incluída.

**Família analítica de fundos não degenerados.** Em um cilindro fixo, ponha a_ε(r)=2exp(εr), g_ε=dr²−a_ε²γ, φ_ε=id. Para ε≠0, E_ε tem posto quatro em todo o cilindro; para ε=0 perde a coluna temporal. Com a mesma escolha h_{ij}=g_{ε,ij}, ξ=0, obtém-se exatamente ζ^r=1/(2ε). Essa é uma família analítica de dados geométricos admissíveis como jatos, sem degeneração métrica. Não é apresentada como família on-shell da ação física. Ela demonstra que não existe extensão C∞ ou analítica universal da inversa/ζ por ε=0. Não prova falha de T4/T5 nas famílias que ficam estritamente no aberto relógio.

Finalmente, para φ̄ constante, dφ̄=0, X̄=0 e dX̄=0, logo Ē=0. Nenhum mapa L regular pode satisfazer ĒL=Id ali. A referência de sigma constante usada em087 está fora do domínio088. Isso basta para impedir a transferência automática dos argumentos entre as duas classes. Não se tentou homotopar globalmente id:S³→S³ a um mapa constante — os setores topológicos diferem. A obstrução à extensão da fórmula já aparece em jatos locais. Outra primitiva, ou cancelamentos específicos numa expressão final, exigiria exame próprio.

## 8. O que as primárias permitem importar

[KNOWN] Hollands0705.3340v4 exige T4/T5 para famílias de métricas e T2 para escala. Em §3.6, eqs.250–256, a liberdade é uma hierarquia local na diagonal, com covariância e identidade de derivação; seu argumento universal obtém dependência polinomial em curvaturas, massa e campos. Isso não autoriza substituir essa hierarquia por qualquer densidade racional local. Também não demonstra uma proibição de inversas em uma categoria previamente restringida. A adaptação sigma/fundos materiais precisa conservar o contrato indicado em072. [Primária](https://arxiv.org/pdf/0705.3340v4), pp.39–41 e63–65.

[KNOWN] Brunetti–Fredenhagen–Rejzner1306.1058v5, §2.5, admite coordenadas construídas de matéria e restringe a vizinhança de configurações para controlar imagens e suportes dos testes. O texto também separa seus funcionais relacionais da classe local compactamente suportada original. Isso sustenta a necessidade de declarar o domínio, mas não identifica seu modelo de quatro escalares livres com o sigma S³, nem seus funcionais relacionais com nossos contratermos. [Primária](https://arxiv.org/html/1306.1058v5#S2.SS5).

Aqui a operação examinada é E⁻¹ no mesmo ponto, e não a substituição não linear de testes por coordenadas dependentes de campos. Se essa segunda operação for acrescentada, a compatibilidade de suportes e a classe de funcionais deverão ser tratadas separadamente.

## 9. Contrato mínimo consumível pela próxima construção

[DERIVED] Pode-se trabalhar no aberto J_clk, com a subcategoria causal que transporta B₀ e preserva o posto, suporte compacto interior e a mesma apresentação global de ξ. A inversa é natural, real, suave/analítica conforme a entrada, local de ordem finita, e admite expansão formal coeficiente a coeficiente. A localização conserva a descida horizontal075. A identidade proposta s₀ζ=C, uma vez derivada com as regras e normalizações do modelo, tem portanto um domínio geométrico real onde pode ser usada.

[OPEN — obrigações determinadas] Para uma remoção Q2, ainda se exige: (i) mudança BV/homotopia demonstrada na mesma álgebra localizada, incluindo antifields e todos os jatos; (ii) preservação da completação por laço, valência e fontes; (iii) construção dos D_n com cotas de escala, realidade, independência funcional, ação por partes e contatos de todas as inserções; (iv) regularidade na categoria de fundos escolhida e, se pretendido, comparação de esquemas por acordo perturbativo. A observação de coeficientes suaves no fundo fixo não paga essas quatro condições juntas.

Uma conclusão restrita ao aberto dos relógios pode ser correta mesmo sem extensão ao sigma constante. Inversamente, para reivindicar o mesmo resultado na categoria universal074, é necessário produzir uma extensão regular da EXPRESSÃO FINAL ou uma receita que dispense o denominador; os polos acima impedem simplesmente reusar E⁻¹. Nenhuma dessas distinções é uma prova de anomalia efetiva, de inexistência de quantização ou de QME.

## 10. Custódia e escopo da leitura

Foram lidos Q2_069, o contrato072 e a nota075; Ward072 foi conferida especialmente nas §§6–9; as fontes074 foram consultadas na definição de classe, controle de regularidade/escala e precisão métrica. Os sete arquivos estão pinados antes/depois no manifesto. As primárias foram consultadas pela ferramenta web, sem fabricar hashes locais de seus PDFs. A busca ampla encontrou permissões negadas em pacotes antigos não pertinentes; nenhuma das sete fontes exigidas ficou inacessível.

Esta é uma auditoria independente de DOMÍNIO. Não aprova por antecipação as folhas088 da derivação de ζ ou da homotopia BV, não reexecuta087, não recaptura canônicos e não atualiza memórias originais. O manifesto distingue verificações documentais da demonstração escrita.
