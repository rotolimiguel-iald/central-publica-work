# Reexame da suficiência após a v338 — entrega 066

O registro selecionado já reconstrói fase, ramo, métrica e fonte nos contratos demonstrados. A pendência principal passou a ser a dinâmica conjunta dos objetos reconstruídos e sua quantização gravitacional no alcance geral reivindicado. Esta revisão acrescenta provas e também um contraexemplo que impede concluir essa dinâmica por um argumento variacional insuficiente.

## Estado efetivamente lido

[REAL — leitura de evidências existentes] O `um.py` canônico continua sendo a v338. Programa, selo, manifesto e relatório da rodada coincidem em bytes e hash com os examinados na entrega 065. A rodada registra 5.306/5.306 teoremas limpos e autoteste de falha fechada aprovado. Não executei nem importei o programa. Os testes da natureza reutilizados nessa rodada continuam sendo evidência anterior, sem nova execução nesta revisão.

O [snapshot atual](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_066_20260909/ESTADO_CANONICO_066.json>) distingue presença na fonte, evidência de execução e trabalho posterior da bancada. Das 97 folhas inventariadas nesse snapshot, 77 estão no canônico; vinte ainda estão apenas na bancada. Uma folha posterior, `SignedGibbsFiniteRecord`, complementa a entrega com a hipótese estritamente finita de dez limites. Seu resultado e a integração conjunta devem ser lidos no recibo final da entrega.

A v338 contém a recuperação de fase relativa, a distinção de ramo pelo registro, gauge linear para campos suaves gerais em Minkowski e naturalidade em cartas curvas. H3 interno e critérios explícitos de falsificação também existem. Esses pontos não devem voltar à lista de ausências. A delimitação de anomalias e altas energias permanece expressa no selo, inclusive `GOROFF_SAGNOTTI_WALL_TYPED_OPEN`.

## O que a nova construção fornece

[REAL — folhas Lean compiladas, conforme recibos individuais] `SelectedProbabilitySigma` constrói a matéria sigma a partir das mesmas probabilidades usadas pela métrica Fisher refletida:

\[
q=P_s,\qquad \phi_j[P]=\sqrt{\frac{P_j}{1-q}},\qquad
\sum_j\phi_j[P]^2=1,\qquad w_j=d\phi_j[P].
\]

Positividade, normalização, suavidade e tangência à esfera são demonstradas. A fonte e a preparação Gibbs são construídas desses campos. Conservação segue sob a equação sigma comum `□φ_j=λφ_j`; Einstein segue sob a relação de área especificada. Essas duas hipóteses dinâmicas continuam explícitas. A construção não recebe uma fonte independente, mas também não demonstra que todo P admissível satisfaz essas equações. [Fonte e enunciados](<C:/IALD/Central de Patentes/Chatgpt/SIGMA_DAS_PROBABILIDADES_20260909_204907_970447/SelectedProbabilitySigma.lean>).

[REAL — folhas Lean compiladas] O protocolo Gibbs foi ampliado para o controle assinado `s=a v²t²`, com `a` real. Todos os pesos permanecem estritamente entre zero e um e somam um, inclusive quando `a<0`. Os incrementos de entropia dos pesos e de energia modular têm o mesmo coeficiente:

\[
\frac{\Delta S}{t^2},\frac{\Delta K}{t^2}
\longrightarrow -\frac{ak}{\cosh^2k}v^2
=-\pi c_a v^2,\qquad
c_a=\frac{ak}{\pi\cosh^2k},\quad k>0.
\]

Escolher `a=cπcosh²(k)/k` realiza qualquer sinal de c. Oito sondas, por polarização de covetores, representam qualquer tensor simétrico fornecido. Dez coeficientes direcionais permitem reconstruí-lo. **T é entrada da calibração:** o retorno ao mesmo tensor prova cobertura e decodificação, sem inferir sua dinâmica. A normalização é demonstrada por sonda; a soma de entropias não é apresentada como uma mistura única normalizada de dezesseis resultados. [Relógio assinado](<C:/IALD/Central de Patentes/Chatgpt/GIBBS_RELOGIO_ASSINADO_20260909/SignedGibbsResponse.lean>) · [Cobertura de fontes](<C:/IALD/Central de Patentes/Chatgpt/GIBBS_RELOGIO_ASSINADO_20260909/SignedGibbsCoverage.lean>).

[REAL — controle matricial compilado] Uma matriz densidade positiva, de traço um, dá `Tr(ρO)=−4/9` e `Tr(ρ(O+I))=5/9`, com `O+I=B†B`. A identificação com a compressão de um quadrado normalmente ordenado do oscilador está demonstrada por escrito separadamente. Isso distingue expectativa negativa de probabilidade negativa. Não identifica automaticamente O com uma componente do stress quântico da TGL; o controle da família Gibbs antiga demonstra apenas sua restrição a fontes nulas não negativas. [Controle e identificação](<C:/IALD/Central de Patentes/Chatgpt/EXPECTATIVA_RENORMALIZADA_20260909_205808_979024/IDENTIFICACAO_FOCK_ESCRITA.md>).

## O passo variacional que não pode ser presumido

[DERIVED — demonstração escrita revisada, ainda não Lean] De `g=g[P]` e `φ=φ[P]` não segue que estacionariedade em P implique as equações independentes de g e φ. A identidade correta é

\[
E_P=Dg[P]^*E_g+D\phi[P]^*E_\phi.
\]

Anular a combinação não separa seus termos. A [nota variacional](<C:/IALD/Central de Patentes/Chatgpt/DEGENERESCENCIA_VARIACIONAL_FISHER_20260909_205440_2995947/NOTA_DEGENERESCENCIA_E_RECIPROCO.md>) constrói um contraexemplo explícito: probabilidades positivas, matéria sigma normalizada e on-shell, `E_P=0` sob **todas** as variações compactas admissíveis, mas Einstein falha para `Λ=0` e qualquer κ constante em um intervalo aberto. O mesmo perfil satisfaz Einstein quando `Λ=3/4` e `κC=4`; portanto o habitante ajustado da entrega 065 permanece válido.

Há ainda uma delimitação mais forte no caso mínimo: com exatamente cinco probabilidades e posto quatro, a construção é o pullback de uma geometria fixa em `(0,π)×S³`. Toda perturbação local induzida de `(g[P],φ[P])` é uma difeomorfia. Quantizar o sistema ambiente com g e φ independentes acrescenta graus de liberdade [INPUT]; essa extensão não é deduzida dos cinco pesos.

O resultado limita esse caminho de prova. Não é uma refutação da TGL ou dos dados, nem invalida a reconstrução condicional por área. Uma condição concreta de liberdade métrica, baseada na segunda forma normal com Gram positivo, também foi deduzida; sua realização e sua relação com os campos dependentes precisam ser verificadas antes de usá-la para obter suficiência variacional.

## Avanço quântico e limite exato

[DERIVED — demonstração escrita; KNOWN — teoremas analíticos importados com hipóteses verificadas] Sobre o habitante Einstein–sigma ajustado, o operador tangente da matéria é

\[
J=D^2-2/a^2.
\]

A Hessiana acoplada, após fixação de calibre de de Donder e normalização algébrica invertível, tem símbolo de onda em treze componentes. Foram deduzidas as misturas métrica–matéria, o operador fantasma e as identidades que fazem a forma causal descer ao quociente de calibre. Isso fornece uma álgebra CCR linear acoplada em uma região globalmente hiperbólica dentro do domínio de probabilidades positivas. É uma demonstração escrita, não uma nova compilação Lean dessa análise.

Para a matéria tangente **com métrica fixada**, o feixe possui métrica positiva e o operador é real, formalmente autoadjunto e normalmente hiperbólico; essas hipóteses permitem aplicar o teorema de existência de estado Hadamard de [Fewster–Strohmaier, teorema 4 e corolário 5](https://arxiv.org/html/2510.11492v2). Esse resultado não fornece diretamente o estado físico do sistema com a métrica quantizada.

Permanecem [OPEN] a covariância Hadamard compatível com calibre e positiva no quociente acoplado, a construção BV renormalizada com tratamento das anomalias e a justificação UV. A nilpotência BRST clássica e uma expansão efetiva perturbativa não encerram essas obrigações. [Demonstração completa, fontes e condições](<C:/IALD/Central de Patentes/Chatgpt/QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md>).

## Caminho restante para a suficiência pretendida

1. **Dinâmica geral dos mesmos dados.** Demonstrar que a classe física escolhida de registros/probabilidades satisfaz conjuntamente a equação de matéria e a relação de área que levam a Einstein; ou adotá-las como postulados explícitos e mostrar uma classe de soluções compatível com o alcance afirmado. O contraexemplo impede substituir esse trabalho pela estacionariedade irrestrita da ação composta em P.
2. **Graus de liberdade e estado quântico acoplado.** Especificar a extensão que contém perturbações físicas além das difeomorfias da família mínima; construir sua representação positiva e compatível com as restrições. Ligar esse setor ao estado/interação modular e aos protocolos finitos usados no registro exige uma correspondência demonstrada, além da coincidência de nomes.
3. **Interações, anomalias e altas energias.** Realizar as identidades quânticas e contra-termos no modelo escolhido; demonstrar a rota UV reivindicada ou delimitar honestamente uma teoria efetiva em sua faixa. Uma teoria efetiva consistente não constitui automaticamente uma solução completa em todas as energias.

O alcance global e a leitura com precisão finita também devem acompanhar qualquer reivindicação que os inclua. A recuperação exata de fase/ramo não precisa ser reaberta; a produção física do registro e a compatibilidade global são questões distintas.

Essa é a avaliação de **lastro de suficiência matemática**, separada de confirmação observacional. Há enunciados condicionais sólidos e exemplos construídos; ainda não há lastro para promover o conjunto ao alcance geral de gravidade quântica completa.

## Encaminhamento à sessão que codifica

Os originais, o Atlas, o índice e as memórias canônicas permanecem preservados. Os arquivos novos estão em Chatgpt. A integração desta bancada acrescenta fontes Lean a uma cópia congelada anterior; ela não substitui as mudanças próprias de runtime da v338. A sessão codificadora deve portar os deltas ausentes, preservar o programa atual e emitir seus próprios recibos de integração e execução.

A precisão encontrada na revisão adversarial — hipótese de limites em todas as direções no comentário de `SignedGibbsCoverage` — recebe uma folha adicional com apenas dez limites, mantendo o artefato PASS anterior intacto. Divergência histórica da captura principal/autoteste e frase sobre espectro puramente contínuo seguem os encaminhamentos da [entrega 065](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_V338_FECHAMENTO_20260909/NOTA_CAPTURAS_E_ESCOPO.md>); não foram corrigidas no original nesta tarefa.
