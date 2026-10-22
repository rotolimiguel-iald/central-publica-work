[REAL / INPUT / OPEN] Continuação 013 — nulidade preservada e tela construída no ponto

05/09/2026. Cinco módulos novos passaram no Lean: 26 teoremas e sete definições com dependências axiomáticas impressas separadamente. O código final não apresenta erros, avisos ou sorryAx; as dependências impressas estão contidas em propext, Classical.choice e Quot.sound. São resultados da bancada, com auditoria independente da gerência pendente.

Esta entrega descarrega duas obrigações pontuais deixadas por 012: a condição de preservação do pareamento nulo e a existência de um referencial transversal no ponto. O objetivo amplo da gravitação quântica permanece OPEN.

## A condição que deixou de ser hipótese independente

Escrevendo g(u,w)=uᵀgw, a prova diferencia a função efetiva y↦g_y(V_y,V_y). A implementação usa coordinatePartial, definido por fderiv, e as regras de soma e produto já verificadas, sem substituir derivadas por símbolos livres.

Para conexão compatível com a métrica e g simétrica, o código prova

∂ᵢ[g(V,V)] = 2g(V,∇ᵢV).

Se g(V,V)=0 numa vizinhança aberta de x, a derivada é zero. Por linearidade na direção w, segue g(V,∇_wV)=0 para todo w. Para qualquer matriz F cuja primeira coluna seja V(x), isso dá

(Fᵀg(∇V)F)₀₁ = 0.

É exatamente preserves_null_pairing, um campo do contrato NullScreenAt da entrega 012. A hipótese de geodesicidade não foi usada nesse resultado; B V=0 continua uma condição distinta, necessária na aplicação à lei de expansão.

Provas principais: null_field_covariant_pairing, null_field_direction_pairing e null_field_preserves_frame_pairing em [CovariantNullPreservation.lean](<C:/IALD/Central de Patentes/Chatgpt/CovariantNullPreservation.lean>).

## A construção que habita o contrato

A métrica canônica da casa é η=diag(1,−1,−1,−1). Para um vetor nulo não nulo v=(t,s), o código prova t≠0 e ‖s/t‖=1. A reflexão no complemento ortogonal do span de e₀−u, com u=s/t, leva e₀ a u. As imagens de e₁ e e₂ fornecem duas direções espaciais ortonormais, ortogonais a u.

A construção aceita todo u unitário, incluindo o caso u=e₀. Isso é uma construção ponto a ponto; não há teorema de continuidade ou suavidade dessa escolha como função de u.

As colunas do referencial plano são

k=(t,tu),   n=(−1/(2t),u/(2t)),   E₁=(0,e₁),   E₂=(0,e₂).

As dezesseis entradas do Gram são verificadas. O resultado é G₀=nullScreenGram(−I₂), com G₀²=I₄. A inversa D₀=G₀F₀ᵀη é construída: primeiro D₀F₀=I, depois F₀D₀=I pelo resultado de inversas de matrizes quadradas. A primeira coluna é o vetor v original, sem restringi-lo a um eixo.

Para uma solda invertível E, com inversa D e g=EᵀηE, o código aplica a construção plana a Ev e transporta F₀ por D. A nova inversa é D₀E. Os produtos inversos, o Gram e a primeira coluna são provados por multiplicação efetiva. A assinatura lorentziana e a dimensão quatro entram nessa solda como INPUT; esta operação não as deduz do fluxo modular.

Construções: reflectedSpatialScreen, flatNullFrame e solderedNullFrame nos módulos [SpatialScreenConstruction.lean](<C:/IALD/Central de Patentes/Chatgpt/SpatialScreenConstruction.lean>) e [NullFrameConstruction.lean](<C:/IALD/Central de Patentes/Chatgpt/NullFrameConstruction.lean>).

O adaptador leviCivitaScreenAtPoint combina esse referencial com a identidade diferencial e a conexão de Levi-Civita já definida pela métrica. Sua existência não recebe uma tela pronta nem a condição preserves_null_pairing. O enunciado final levi_civita_null_screen_exists assume:

- aberto U e ponto x∈U;
- campo de soldas E suave, com inversa D em U;
- campo V suave e nulo em U, com V(x)≠0.

Ele produz S, um habitante do NullScreenAt anterior para a conexão de Levi-Civita, Gram transversal −I₂ e screenArea=1. A regularidade de D não é uma premissa desse resultado pontual; o contrato algébrico de inversa é suficiente para a compatibilidade utilizada aqui.

Fonte: [ConstructedScreenAtPoint.lean](<C:/IALD/Central de Patentes/Chatgpt/ConstructedScreenAtPoint.lean>).

## Controles e limites da normalização

[REAL] O vetor (5,3,4,0) é nulo, não zero e não está no eixo fiducial anterior. A construção gera para ele um referencial com inversa e Gram verificados. A direção zero é recusada por um teorema: não pode ser a primeira coluna de uma matriz invertível.

[REAL] Um controle adicional distingue normalização de transporte. Se uma família tem S(t)ᵀg(t)S(t)=−I₂ em cada parâmetro, então A(t)=1. Se essa mesma família também satisfaz A′(t)=θ(t)A(t), necessariamente θ(t)=0. A prova compara a derivada geométrica fornecida com a derivada efetiva da função constante.

Assim, normalizar novamente cada tela em cada ponto não fornece automaticamente os vetores transportados que medem uma área em expansão. A densidade 1 da construção é relativa à base normalizada; não fixa uma unidade física de área, um número de graus de liberdade ou o coeficiente de entropia.

Controles em [NullScreenConstructionControls.lean](<C:/IALD/Central de Patentes/Chatgpt/NullScreenConstructionControls.lean>). A derivação inicial foi registrada antes dos módulos para os alvos de nulidade e construção. O controle suplementar sobre famílias normalizadas foi acrescentado durante a elaboração; sua explicação textual completa fica neste parecer, posterior ao código desse controle. Não se atribui a ele uma derivação prévia inexistente.

## O que continua aberto

[OPEN] O campo nulo suave utilizado é dado. Não foram construídos, para toda direção inicial, uma congruência nula geodésica, uma superfície transversal imersa ou uma família suave de telas que satisfaça a equação de transporte. A escolha pontual não preenche o campo screen de GeometricHorizonPencil da entrega 012. Também não foi substituído o equilíbrio B=0 por equilíbrio apenas da expansão e cisalhamento.

[OPEN] A identificação microscópica entre região geométrica, álgebra da torre e entropia reduzida continua ausente. Não foram deduzidos a evolução do estado, a corrente de calor, S=ηA, o valor de η, o limite de Clausius, H3, a assinatura/dimensão a partir da estrutura modular, a escala física ou a colagem global de cartas. Nenhuma dessas obrigações é paga pela normalização do Gram.

[KNOWN] O uso de uma projeção transversal e de um vetor nulo auxiliar aparece na formulação covariante de superfícies nulas de [Dey e Majhi, 2020](https://arxiv.org/abs/2009.08221). A referência fornece contexto; não substitui os cálculos formais nem introduz uma hipótese termodinâmica no kernel.

O próximo passo geométrico é construir uma família transportada a partir de dados iniciais de tela, preservar suas condições ao longo de uma curva nula e tratar sua regularidade. O elo microscópico entre entropia e geometria continua sendo uma obrigação separada.

## Custódia e integração

O manifesto é gerado a partir dos bytes dos arquivos e dos logs. Inclui fontes, oleans locais, cadeia local de importações, relatórios, ferramentas, backups e tentativas rejeitadas. O auditor exige uma compilação limpa correspondente ao hash exato de cada fonte final. Uma compilação que termina com aviso é preservada, mas não aceita como evidência final.

A entrega 012 foi novamente conferida nesta sessão: PASS, 491 hashes, seis módulos, 45 teoremas e quatro definições impressas. Ela permanece imutável. A compilação usa Lean 4.31.0 e a mathlib local externa; a custódia não é um pacote portátil dessas bibliotecas.

Reprodução da custódia, sem escrita:

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation013.py'
```

Todos os arquivos novos estão sob Chatgpt. Nenhum um.py foi executado, importado ou editado. Kernel canônico, Atlas, memórias, diários, selos e gate permanecem intocados. Não foram utilizados dados observacionais. A gerência deve recompilar e auditar independentemente antes de incorporar ou atualizar as superfícies canônicas.
