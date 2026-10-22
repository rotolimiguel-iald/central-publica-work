# Continuação 042 — completamento conservado da resposta nula

06/09/2026. [REAL / DERIVED / INPUT / OPEN]. Complemento à ordem009. Compilação final e auditoria independente do build concluídas; o manifesto final reúne a evidência desta entrega.

A contribuição desta etapa é permitir toda a liberdade tensorial que as leituras nulas deixam invisível e decidir quando ela pode restaurar conservação. O teste anterior do representante canônico não bastava para excluir outro representante com traço variável. Encontramos tanto uma correção possível quanto uma obstrução que nenhuma correção desse tipo remove.

## A precisão do operador sobre a área

O operador propõe distinguir L, interpretado como cauda/poço, de sua inscrição angular quadrática, candidata a geometria. [ONTO] Essa interpretação de L e do retorno da luz não é uma identificação física demonstrada.

[DERIVED — cálculo analítico, fora dos módulos042] Para um gerador autoadjunto limitado L e Uθ=exp(iθL), o módulo quadrático da própria fase é Uθ*Uθ=I. A diferença relativa à identidade fornece
Fθ=(Uθ−I)*(Uθ−I)=4 sin²(θL/2).
Para θ pequeno, Fθ=θ²L²+O(θ⁴), em norma para L limitado. Isso mede uma diferença quadrática de fase; não seleciona sozinho uma área. Pode ser diferente de zero mesmo para L=cI, quando apenas a fase global do vetor muda.

[KNOWN] Para uma família suave de vetores normalizados ξ(q), a variação horizontal é D_aξ=(I−|ξ〉〈ξ|)∂_aξ. O tensor Q_ab=〈D_aξ,D_bξ〉 fornece a métrica G_ab=Re Q_ab. Na órbita de um único L, Dθξ=i(L−〈L〉ξ I)ξ e Gθθ=Varξ(L). Com duas direções reais independentes, a densidade de área é sqrt(G11 G22−G12²). Uma única direção repetida tem determinante zero. A convenção aqui não inclui o fator4 às vezes usado na métrica de Fisher. Referência primária: Kolodrubetz, Sels, Mehta e Polkovnikov, “Geometry and non-adiabatic response in quantum and classical systems”, https://arxiv.org/abs/1602.01062.

[REAL — fontes locais consultados] AngularScreenMetric.lean define precisamente um Gram de direções GNS centradas, prova positividade para sítios distintos e área zero para o sítio repetido. AngularAreaObservability.lean demonstra que, na família centralizante estudada, a área dos raios GNS pode ser positiva enquanto todas as leituras no fator permanecem constantes. Assim, uma geometria de vetores não identifica automaticamente a geometria operacional do estado restrito, muito menos a área do espaço-tempo.

[OPEN] Não há nesta etapa uma ponte que identifique L=log H da030 com L_phi do Atlas. A distinção canônica entre face hiperbólica e leitura angular é preservada; a formalização de uma derivada de uma família suave de fases não afirma que o kernel canônico tenha demonstrado essa derivada para qualquer família homônima. Fθ=F−θ perde a orientação. U(−θ)=U(θ)* fornece reversibilidade, não uma lei de atração. “Luz que dobra e retorna como estabilização” precisa de transporte/curvatura e de uma evolução cujo equilíbrio seja demonstrado. Positividade, conservação e estabilidade são propriedades diferentes.

## Todos os representantes com a mesma resposta nula

[INPUT] Fixamos o fundo plano g=eta4, assinatura +--- e conexão zero. U é aberto, w é um covetor suave e fechado, e c é uma constante real. Os candidatos T são tensores simétricos e suaves no mesmo U. A resposta é exigida para TODOS os vetores d com g(d,d)=0, em TODOS os pontos de U:
T(d,d)=c[w(d)]².

Defina S=c(w⊗w−g⁻¹(w,w)g/2). A contração g⁻¹(w,w) tem assinatura indefinida e não é uma norma positiva. A rigidez quadrática no cone nulo implica
T=S+f g.
Não se supõe conservação de S nessa classificação. Uma escolha explícita e suave é f=(T−S)00, pois g00=1.

A divergência do tensor completo é
div T=c(div w)w+df.
Logo a realização conservada existe se, e somente se, a força J=c(div w)w admite um potencial negativo suave em U:
df=−J.

Isso é um critério de EXATIDÃO. Fechamento dJ=0 é necessário; esta etapa não prova que fechamento sozinho implique uma primitiva global. A topologia e os períodos não são apagados. Para w=dφ, a condição é df=−c(□φ)dφ e a obstrução local é c d(□φ)∧dφ≠0.

Se houver uma lei adicional □φ=F(φ) e uma função escalar W com W'=F, a escolha f=−cW(φ) resolve a equação. [DERIVED — analítico] Essa construção condicional não deduz F nem a ação de campo a partir do estado.

## Controle reparável e contraexemplo

[REAL — teoremas042 compilados] Para φ=t²/2, w=t dt e div w=1, temos J=c t dt. O representante S sozinho não é conservado para c≠0, mas f=−c t²/2 o corrige. O tensor resultante é diag(0,ct²,ct²,ct²). As leituras nulas são preservadas e a divergência é zero. Não se demonstram condições de energia, mínimo energético nem estabilidade dinâmica por essa correção.

Para φ=t²x, w=(2tx,t²,0,0) e div w=2x, temos
J=(4ctx²,2ct²x,0,0),
∂1 J0−∂0 J1=4ctx.
Em p=(1,1,0,0), a diferença vale4c. Para c≠0, não há potencial negativo suave de J em QUALQUER aberto que contenha p. Portanto não existe qualquer T suave simétrico conservado com essas mesmas leituras em todos os vetores nulos nesse aberto. O resultado inclui todo traço variável, e não só a falha de S.

A igualdade da resposta apenas num ponto não bastaria: as derivadas exigem as igualdades no aberto. O caso c=0 admite o tensor zero. A família de onda029, que satisfaz condições adicionais, não é refutada por este contraexemplo.

## Ligação aos estados somáveis efetivamente construídos

[REAL — resultados028 existentes] amplitudeResponse b z=−log(2) B z², com B=amplitudeMass b. O módulo SummableGravityBridge fornece c_b=log(2)B/π e a igualdade amplitudeResponse b (w·d)=−π S_b(d,d) para d nulo. Os limites quadráticos entrópico e modular da028 certificam esse mesmo coeficiente.

A042 aplica o critério diretamente a essa resposta. A existência de T conservado com amplitudeResponse=−π T(d,d) equivale à realização anterior com c=c_b. Para B>0, c_b>0 e o campo misto não admite tal T. A hipótese escrita diretamente como limite do incremento entrópico dividido por t² é convertida à igualdade do coeficiente por unicidade do limite, sem definir a entropia a partir do tensor.

O controle temporal crescente admite a realização conservada com a correção de traço acima. zeroAmplitude admite T=0. [INPUT] O campo direcional w(x), a identificação da frequência com w·d e o fundo plano são escolhas da extensão espaço-temporal; não são selecionados pela família de estados nesta etapa.

O incremento entrópico é relativo à referência: não se declara entropia absoluta finita de um fator. As leituras finitas da028 são ligadas aos pesos de amplitudeState; a passagem ao valor B requer cutoff→∞. Um cutoff fixo mede B_N. O contraexemplo não invalida os estados: exclui a realização conservada da extensão direcional escolhida.

## Verificação e alcance

[REAL — compilação final e auditoria independente] Em CONTINUACAO042_CLEAN_20260906_211041_859289, os quatro módulos e Imports042All passaram: 52 teoremas, 12 definições, 64 impressões de axiomas e zero instâncias. Os cinco passos retornaram exit0/PASS, sem erros ou advertências, com cobertura exata e apenas propext, Classical.choice e Quot.sound. As fontes de trabalho e as cópias compiladas são idênticas; os snapshots de entrada permaneceram estáveis. O auditor independente --build-only retornou BUILD_PASS/exit0, conferindo 1.987 arquivos do build e 163 registros históricos. O revisor também conferiu separadamente os logs, metadados, snapshots, importador e adaptação integral do auditor041. As tentativas anteriores e backups foram preservados. O manifesto final é produzido depois do parecer e da entrega, e sua auditoria somente leitura confere a custódia completa.

Os módulos são NullStressCompletion, ConservativeNullResponse, NonintegrablePotential e SummableNullIntegrability, namespace Completion042. O construtor cria diretório inédito, usa a fronteira histórica pinada e compila em série; depois compila o importador conjunto. Toda definição/teorema tem #print axioms. Erros, advertências, sorryAx, axiomas fora da base admitida e instâncias anônimas impedem PASS.

Os binários históricos são conferidos por hash, mas não recompilados nesta etapa. Fontes canônicos sem pin histórico de fonte só servem à descoberta dos imports, sem provar proveniência até o binário. A resolução das dependências externas diretas é conferida; o fechamento transitivo inteiro de Mathlib/toolchain não é hashado. A auditoria de custódia não substitui interpretação física.

Originais, um.py, kernel canônico, Atlas, memórias e entregas seladas anteriores permanecem somente em leitura. As novas escritas e backups ficam em Chatgpt. A entrega pelo túnel disponibiliza os resultados à sessão irmã; não incorpora mudanças ao canônico.

H3: OPEN. Reconstrução gravitacional geral a partir do estado: OPEN. Meta ampla de gravidade quântica: OPEN. Nenhum gate canônico foi alterado.
