# Análise prévia — custo modular e calibração angular nos dois setores053

[DERIVED — cálculo matricial finito, não formalizado neste documento]
Data: 2026-09-07. Autor: agente review_global_cocycle, a pedido da raiz.

Esta nota registra uma análise anterior a qualquer decisão de implementação. Não integra o censo de teoremas053, não anuncia BUILD_PASS de outro lote e não decide iniciar uma continuação054. Os objetos comparados são os mesmos geradores locais brutos usados na053. A construção de uma métrica ou de uma área gravitacional permanece fora do resultado.

## 1. Corte finito e convenções

Fixar uma matriz de densidade fiel finita ρ=diag(w_i), com w_i>0 e soma dos pesos igual a um. Definir K=−logρ e, para A=A*, tomar

    U_t=exp(i t A),   ρ_t=U_t ρ U_t*,
    ΔK(t)=Tr(ρ_t K)−Tr(ρ K).

K é o observável de referência, mantido fixo: não se substitui K por −logρ_t na primeira parcela. A convenção coincide com a leitura ω(U_t* B U_t) da035, pelo traço cíclico.

Na torre, usa-se ρ_N=diag(towerW P N), nos cortes N=0 e N=1. Cada K_N é uma matriz finita e sua imagem towerPi é um observável local limitado. Não se postula uma densidade global trace-class ρ, uma entropia global finita ou um K global igual a −logρ para o fator infinito.

A comparação também pode ser feita inteiramente no corte N=1: para o estado produto, K_1=K_0⊗I+I⊗K_0. O primeiro flip, embutido como X no sítio0, deixa a parcela espectadora inalterada. Seu incremento continua sendo o calculado em N=0. Assim, os números abaixo não resultam de trocar a contribuição do sítio espectador.

## 2. Derivação exata de um flip bruto

Se A=E_ij+E_ji, i≠j, o bloco ativo é a matriz de Pauli X. Escrevendo c_t=cos t e s_t=sin t, a exponencial nesse bloco é c_t I+i s_t X. Logo,

    (ρ_t)_ii = w_i c_t²+w_j s_t²,
    (ρ_t)_jj = w_j c_t²+w_i s_t²,
    (ρ_t)_ij = i(w_j−w_i)s_t c_t.

Os demais pesos diagonais ficam inalterados. Como K é diagonal, as entradas fora da diagonal não contribuem diretamente a Tr(ρ_t K). Portanto,

    ΔK(t)
      = [(w_j−w_i)(−log w_i)+(w_i−w_j)(−log w_j)] sin²t
      = (w_i−w_j) log(w_i/w_j) sin²t.

Definindo C_ij=(w_i−w_j)log(w_i/w_j), obtém-se

    ΔK(t)=C_ij t²+O(t⁴),
    lim_{t→0,t≠0} ΔK(t)/t²=C_ij,
    ΔK''(0)=2 C_ij.

O coeficiente de t² não é a segunda derivada: esta contém um fator dois adicional. O produto C_ij é não negativo, pois log é estritamente crescente, e é positivo se os pesos são distintos.

Mais geralmente, para A autoadjunto finito, a expansão da mesma expressão fornece

    ΔK(t)
      = −(t²/2) Tr(ρ[A,[A,K]])+o(t²)
      = t² Σ_{i<j}(w_i−w_j)log(w_i/w_j)|A_ij|²+o(t²).

O termo linear é zero porque ρ comuta com K. A fórmula exata com sin²t acima basta para os dois testes escolhidos.

## 3. Os dois pares concretos, sem renormalizar o segundo

Tomar p=1/3.

| Objeto | Pesos ativos | Gram GNS real de X,Y | ΔK(t) exato | Coeficiente de t² |
|---|---|---|---|---|
| Primeiro par X₁,Y₁ | 1/3, 2/3 | I₂ | (log2/3)sin²t | log2/3 |
| Par duplo bruto X₂,Y₂, entre00 e11 | 1/9, 4/9 | (5/9)I₂ | (2log2/3)sin²t | 2log2/3 |

No segundo teste, os estados01 e10 são espectadores. X₂ é literalmente doubleFlipX; não foi multiplicado por 3/√5. As segundas derivadas são, respectivamente, 2log2/3 e 4log2/3.

Os pareamentos imaginários são Ω(X₁,Y₁)=Ω(X₂,Y₂)=−1/3. As ações do polarizador real D, no sentido da053, são

    D X₁=(1/3)Y₁,   D Y₁=−(1/3)X₁,
    D X₂=(3/5)Y₂,   D Y₂=−(3/5)X₂.

Aqui as igualdades de D são sobre os vetores GNS correspondentes. Em cada um desses planos, a fase polar orientada é Q=−D/|D|, portanto QX_j=−Y_j e QY_j=X_j. Definindo gΩ(u,v)=Ω(u,Qv), segue

    gΩ(X₁,X₁)=gΩ(X₂,X₂)=1/3.

Esta é a calibração pela forma imaginária e pela fase polar, não a família hε da053 nem sua normalização de traço um. Também não se afirma que um único tempo modular realize Q simultaneamente nas duas frequências: o quarto de volta da frequência simples vira meia-volta na frequência dupla. A definição polar por blocos não é, por si, prova de que essa transformação seja adT de um horizonte global.

Se existisse uma constante α que convertesse gΩ(X,X) no coeficiente de ΔK para ambos os geradores, o primeiro exigiria α=log2 e o segundo α=2log2. Como log2>0, são incompatíveis. A mesma conclusão vale usando as segundas derivadas, com ambas as razões multiplicadas por dois.

## 4. Razão hiperbólica e o fator de frequência ausente

Para um bloco, escrever

    n=w_i+w_j,   κ=log(w_i/w_j),   d=(w_i−w_j)/(w_i+w_j).

Então, por expκ=w_i/w_j,

    d = (expκ−1)/(expκ+1) = tanh(κ/2).

Essa identidade fixa o fator dois no argumento da tangente hiperbólica. Como κ e d têm o mesmo sinal,

    C_ij/n = κ d = |κ| |d|.

O coeficiente de custo relativo ao Gram GNS é, portanto, |κ|·|d|; a forma angular gΩ relativa ao mesmo Gram usa apenas |d|. Para as segundas derivadas, o peso relativo seria 2|κ|·|d|.

No primeiro bloco, κ=−log2 e d=−1/3. No segundo, κ=−2log2 e d=−3/5. Multiplicar pelo Gram bruto n=1 ou n=5/9 recupera os números da tabela.

[DERIVED — alcance exato] A razão limitada d é a leitura hiperbólica tanh(κ/2) da razão logarítmica finita. A comparação torna precisa uma diferença entre essa leitura polar/angular e o peso de custo. Não identifica κ com um operador global logΔ, não identifica Q com J e não transforma uma identidade de matrizes em seleção de assinatura espaço-temporal ou área física.

## 5. Entropia completa, diagonal e reduzida

Em qualquer corte finito que contenha o suporte do gerador, ρ_t e ρ têm o mesmo espectro. A entropia de von Neumann completa satisfaz S(ρ_t)=S(ρ), enquanto o relativo quântico satisfaz exatamente

    D(ρ_t||ρ)=ΔK(t).

Há custo relativo positivo apesar da entropia completa constante. Esta frase não atribui uma entropia finita global à torre infinita.

Se houver descoerência na base diagonal de referência, as probabilidades lidas são q_i(t)=(ρ_t)_ii. Elas mudam em O(t²), e

    S(q(t))−S(w)=C_ij t²+O(t⁴),
    D_cl(q(t)||w)=O(t⁴).

Com efeito, S(q)−S(w)=Σ_i(q_i−w_i)(−logw_i)−D_cl(q||w); o primeiro termo é ΔK e o relativo clássico é quadrático em q−w. O relativo quântico anterior, em contraste, já tem termo de ordem t²: as coerências não podem ser descartadas ao identificar esses objetos.

Reduzir também pode mudar a entropia, mas isso depende da redução. No flip duplo, cada marginal de um sítio é diagonal, com primeira probabilidade

    p_reduzido(t)=1/3+(1/3)sin²t.

Cada entropia marginal tem coeficiente log2/3; a soma tem coeficiente2log2/3. Isso não contradiz a constância da entropia completa dos dois sítios. No flip de um único sítio, conservar o estado completo desse sítio ainda conserva sua entropia; descoerência e traço parcial não são operações intercambiáveis.

Micro021 usa finiteEntropy das probabilidades de uma DiagonalStateCurve e o relativo clássico dessas probabilidades. Aplicá-lo a estas órbitas unitárias requer definir e justificar a leitura diagonal ou a redução. Não se pode substituir automaticamente a entropia da matriz completa pela dessas probabilidades. Tampouco esta curva diagonalizada é automaticamente o perfil anterior1/3−b·h(t): aqui a primeira probabilidade do exemplo cresce.

## 6. Orientação do calor e dívida restante

No protocolo041/043, com área inicial um, o calor integrado de0 até t tem

    Q(t)=−rate·mass·t²/2+o(t²).

Para rate>0 e mass>0 esse coeficiente é negativo, inclusive no germe passado t<0. O segmento orientado de t até0 usa Q_segmento=−Q(t), com coeficiente positivo. A comparação com o custo ΔK≥0 precisa manter essa orientação explícita; trocar o sentido não é derivar uma identidade de calor.

O cálculo aqui demonstra uma incompatibilidade específica: uma única conversão escalar entre a calibração gΩ e o custo modular não funciona nos dois setores efetivos fixados. Ele não resolve microscopicHeatError/t²→0 nem microscopicAreaError/t²→0. Faltam a identificação do custo com constructedHeat/screenHeatFlux do mesmo protocolo e a identificação de uma função de área com inducedArea da mesma tela, incluindo os parâmetros físicos e as convenções de orientação.

Não é permitido escolher mass, η ou ε para ajustar os coeficientes e apresentar o ajuste como lei derivada. O resultado não demonstra H3, não decide uma nova métrica por decreto e não autoriza iniciar um lote054. É um controle analítico que explicita qual fator de frequência uma eventual ponte ainda deverá justificar.

## Fontes locais consultadas

- [LocalPolarizerWitness.lean](<C:/IALD/Central de Patentes/Chatgpt/LocalPolarizerWitness.lean>): pares brutos, ação do polarizador, produtos do estado, normas e respostas efetivas.
- [QuantumOrbitArea.lean](<C:/IALD/Central de Patentes/Chatgpt/QuantumOrbitArea.lean>): convenção de Ω, quarto de volta orientado e calibração no primeiro plano.
- [UnitaryStateDerivative.lean](<C:/IALD/Central de Patentes/Chatgpt/UnitaryStateDerivative.lean>): convenção U=exp(+itA) e leitura ω(U*BU).
- [MicroscopicClausiusBridge.lean](<C:/IALD/Central de Patentes/Chatgpt/MicroscopicClausiusBridge.lean>): microscopicAreaError, microscopicHeatError e a decomposição com relativo clássico.
- [OpticalConstructedHeat.lean](<C:/IALD/Central de Patentes/Chatgpt/OpticalConstructedHeat.lean>) e [OpticalHeatClausius.lean](<C:/IALD/Central de Patentes/Chatgpt/OpticalHeatClausius.lean>): germe do calor construído, coeficiente quadrático e casamento explícito.

Nenhuma compilação foi executada para esta nota. Não se reproduzem hashes de fontes de memória. Escrita restrita a este documento novo em Chatgpt; fontes053 e memórias canônicas permanecem intocados.
