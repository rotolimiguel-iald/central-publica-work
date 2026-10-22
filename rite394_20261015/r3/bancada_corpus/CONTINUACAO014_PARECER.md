[REAL / INPUT / OPEN] Continuação 014 — tela transportada local e controle curvo

06/09/2026. Trabalho espontâneo posterior à entrega 013, sob o objetivo amplo iniciado na ordem 007. O túnel continua com ordens gerenciais 001–007. Esta entrega é da bancada; a auditoria adversarial da gerência permanece pendente.

## Resultado e alcance

[REAL] `local_levi_civita_transported_screen` constrói uma curva e um habitante de `GeometricScreenAlong` a partir de uma solda suave invertível e de um campo nulo suave, geodésico e não nulo no ponto inicial. O teorema recebe esses dados, mas não recebe uma família de telas pronta. A área é a densidade geométrica efetiva
\[
A(t)=\sqrt{\det(S(t)^T g(x(t)) S(t))},
\]
e a construção satisfaz \(A'=\theta A\), com \(\theta=\operatorname{tr}(\nabla V)\), numa vizinhança à esquerda de zero. O resultado auxiliar `flow_screen_area_derivative_zero` também prova a derivada no próprio parâmetro zero.

[REAL] O controle curvo `expanding_screen_nonconstant` instancia a construção com \(g=e^{2x^0}\eta\) e \(V=e^{-2x^0}(1,1,0,0)\). Produz \(A(0)=1\), \(A'(0)=2\) e prova que A não é constantemente 1 numa vizinhança de zero. `expanding_background_curvature` calcula uma componente não nula do tensor de curvatura: `coordinateCurvature Γ 0 1 2 1 2 = 1`. São igualdades formais, sem dados observacionais.

[INPUT] A dimensão quatro e a assinatura \((+---)\) já estão fixadas pela solda \(g=E^T\eta E\). E e D são suaves e mutuamente inversos no aberto U. O campo V é suave e nulo em U, satisfaz \(\nabla_VV=0\) em U e V(x)≠0 no ponto escolhido. Essas condições aparecem no enunciado principal; a prova não as deduz de dados quânticos.

## Construção verificada

1. Definimos \(B=\nabla V\), \(L=\sum_i V^i\Gamma_i\) e \(K=B-L\). No espaço finito \(\mathbb R^4\times\operatorname{Mat}_4(\mathbb R)\), provamos que o campo \((V(x),K(x)F)\) é C¹. O teorema de existência local de ODE da mathlib fornece x e F com \(x'=V(x)\), \(F'=K(x)F\) e dados iniciais definidos. `localFrameFlow` escolhe esse habitante. É uma construção formal não computável, sem algoritmo numérico ou fórmula fechada para a solução geral.

2. A compatibilidade métrica permite calcular a derivada efetiva de \(g(V,Z)\) para uma coluna Z transportada:
   \[
   \frac{d}{dt}g(V,Z)=g(BV,Z)+g(V,BZ)=0.
   \]
   O primeiro termo se anula pela geodesicidade. O segundo se anula pela derivada do campo nulo, provada em 013. Seguem \(g(V,W)=-1\) e \(g(V,S_i)=0\) em todo o intervalo da solução.

3. As colunas 2 e 3 de F definem S. A normalização inicial dá \(h(0)=-I_2\), onde \(h=S^TgS\). Continuidade garante \(h_{00}<0\) e \(\det h>0\) numa vizinhança menor. Esse Gram simétrico permanece negativo definido, sem ser imposto igual a \(-I_2\) fora do ponto inicial.

4. Para obter o certificado nulo completo preservando S, usamos o Gram da base bruta \((V,W,S_1,S_2)\). Com \(a=g(W,W)\), \(b_i=g(S_i,W)\), \(q=h^{-1}b\) e \(d=a-b^Tq\), definimos
   \[
   N=W-Sq+\frac d2 V.
   \]
   As operações matriciais provam que \((V,N,S_1,S_2)\) tem Gram `nullScreenGram h`. Seu determinante é \(-\det h\ne0\), o que prova a invertibilidade da base. A substituição modifica apenas o vetor auxiliar N; os dois vetores de tela continuam os da ODE.

5. `flowScreenCertificate` produz `NullScreenAt`. `geometricScreenFromFlow` reúne certificados, tangência, continuidade e transporte no contrato `GeometricScreenAlong`. A lei de área da entrega 012 aplica-se então à tela construída. O contrato usa a vizinhança passada de zero; a ODE e a preservação das contrações foram obtidas num intervalo aberto dos dois lados.

[REAL] No controle plano, o gerador zero produz F constante, recuperando a tela plana anterior. No controle curvo, o gradiente covariante é
\[
B=q\begin{pmatrix}-1&1&0&0\\-1&1&0&0\\0&0&1&0\\0&0&0&1\end{pmatrix},
\qquad q=e^{-2x^0}.
\]
Assim BV=0 e \(\theta=2q\). No ponto inicial, \(\theta=2\), e a lei geral fornece \(A'(0)=2\). Esse controle não satisfaz a condição de equilíbrio B(0)=0 usada em outras etapas: não é um habitante do contrato completo de horizonte/Clausius.

## Errata de integração da entrega 013

[REAL] A leitura dos fontes revelou duas declarações com nome completo `ChatgptAudit.flatNullFrame`: a matriz constante do controle 012 e a construção parametrizada de 013. As compilações isoladas de 013 não cobriam a integração conjunta desses dois ramos. Nesta sessão não foi executada uma sonda de importação dos dois ramos originais; portanto não se atribui a essa combinação um log de falha que não foi medido.

A correção foi feita exclusivamente em três cópias novas:
- `NullFrameConstruction.lean` → `Screen013NullFrame.lean`;
- `ConstructedScreenAtPoint.lean` → `Screen013Constructed.lean`;
- `NullScreenConstructionControls.lean` → `Screen013Controls.lean`.

As cópias usam `ChatgptAudit.Screen013` e imports ajustados. O auditor compara os bytes com o resultado dessas substituições mecânicas nos originais. Nenhuma prova matemática foi alterada nessas três cópias. `ScreenImportIntegration.lean` importa o controle 012 e o ramo corrigido simultaneamente, verificando as duas bases e seus produtos inversos. O módulo final de controles importa também esse módulo de integração. Essa compilação conjunta foi observada e passou sem avisos.

## Evidência formal e custódia

[REAL] Contagem lida dos fontes: nove módulos, 62 teoremas e 11 definições com axiomas impressos separadamente. Desse total, 14 teoremas e seis definições são as cópias de 013; um teorema é o controle de integração; 47 teoremas e cinco definições impressas pertencem à nova construção geométrica e seus controles. Definições auxiliares sem impressão separada constam no manifesto.

Os nove módulos têm compilação final limpa da fonte cujo hash é registrado. Os `#print axioms` cobrem todos os teoremas e as 11 construções indicadas; as dependências impressas ficam restritas a `propext`, `Classical.choice` e `Quot.sound`. Não há `sorryAx` nas saídas finais. Tentativas com erros e avisos permanecem nos logs e ganham cópias com sufixos do defeito. Cada revisão preserva backup dos bytes imediatamente anteriores.

O manifesto inclui as fontes locais importadas, os binários locais correspondentes, os registros de compilação, os backups, as versões anteriores fixadas e os originais das três cópias. O auditor confere hashes, tamanhos, cobertura dos axiomas e igualdade entre entrega e inventário. Lean 4.31.0 e a mathlib são dependências externas resolvidas pelo script local; não se alega um pacote portátil nem uma recompilação independente completa da cadeia. A leitura dos manifestos anteriores já reconferiu 012 e 013 nesta sessão.

Reprodução da custódia, somente leitura, depois da criação do manifesto:

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation014.py'
```

A entrega no túnel contém caminhos absolutos, hashes calculados e comandos para recompilar os módulos novos em uma cópia independente.

## O que permanece aberto

[OPEN] Esta etapa paga a existência local de uma tela transportada sob os dados indicados. Permanecem:
- construção de um campo nulo geodésico geral a partir dos dados geométricos de horizonte e com as condições de equilíbrio exigidas;
- existência de uma superfície/horizonte imerso, dependência em parâmetros transversais e área total integrada;
- ligação microscópica entre região, álgebra, estado, entropia e a densidade de área construída;
- coeficiente físico de entropia por área, evolução de estado, corrente de calor e a hipótese Clausius/H3;
- substituição da condição forte B(0)=0 por equilíbrio apenas transversal, quando pertinente;
- seleção física de assinatura/dimensão, escala, colagem de cartas e ponte modular–geométrica.

A normalização \(A(0)=1\) é escolha de base, não fixação de uma unidade física. Nenhuma equação de Einstein nova foi deduzida de entropia microscópica nesta etapa. Não há fechamento nem confirmação da gravidade quântica geral.

Toda escrita ocorreu sob `C:\IALD\Central de Patentes\Chatgpt`. `um.py` não foi executado, importado ou alterado. Acervo original, kernel canônico, Atlas, memórias, selos e gate continuam intocados. A gerência recebe a entrega para auditoria independente e eventual incorporação.
