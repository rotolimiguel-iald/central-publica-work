# Progresso nas três frentes — 09/09/2026

[REAL — fontes e recibos lidos nesta sessão] O trabalho parte do um.py canônico reexaminado como v336. Este lote contém 115 teoremas em sete módulos, dos quais sete vieram da bancada angular anterior e 108 foram construídos nesta etapa. São 40 outras declarações; 155 declarações auditadas no total. Contagem de teoremas não mede, sozinha, alcance físico.

| Frente | Teoremas | Outras declarações | Recibo |
|---|---:|---:|---|
| Registro e fase | 54 | 21 | [PASS](<C:/IALD/Central de Patentes/Chatgpt/REGISTRO_ANGULAR_20260909_110257_318312/BUILD_20260909_112251_810885/BUILD_RESULT.json>) |
| Seleção e família gravitacional | 17 | 10 | [PASS](<C:/IALD/Central de Patentes/Chatgpt/SELECAO_GEOMETRIA_20260909_110405_1043089/BUILD_20260909_111235_577496/BUILD_RESULT.json>) |
| Consistência óptica | 17 | 4 | [PASS](<C:/IALD/Central de Patentes/Chatgpt/SMATRIX_OPTICAL_20260909_110514_326918/BUILD_20260909_110839_321122/BUILD_RESULT.json>) |
| Cone e volume | 12 | 3 | [PASS](<C:/IALD/Central de Patentes/Chatgpt/CONE_VOLUME_20260909_112343_982192/BUILD_20260909_112537_639293/BUILD_RESULT.json>) |
| Einstein pela métrica | 15 | 2 | [PASS](<C:/IALD/Central de Patentes/Chatgpt/METRICA_GERAL_20260909_113535_425341/BUILD_20260909_113901_352028/BUILD_RESULT.json>) |

Todos os módulos passaram em builds novas, com as dependências canônicas usadas para leitura. Não há resultado aceito com erro, aviso ou dependência de axioma fora de propext, Classical.choice e Quot.sound. As tentativas fracassadas e os backups foram preservados. Há revisão semântica independente dos registros, da geometria e da inversa construída; a compilação não equivale à reconstrução integral das dependências de Lean/Mathlib.

## 1. O que o registro reconstrói

[REAL] Na família angular A(theta), a fase complexa de uma face selecionada determina a forma angular completa. A ligação com a matriz de fronteira e com thetaMiguel está demonstrada na base [SelectionAngleReconstruction.lean](<C:/IALD/Central de Patentes/Chatgpt/REGISTRO_ANGULAR_20260909_110257_318312/SelectionAngleReconstruction.lean>). Portanto seria incorreto repetir que a seleção nunca permite reconstruir a forma inteira: isso depende do domínio da aplicação.

[REAL] A forma angular comum e o resultado do ramo são dados distintos. Para p=1/2, os dois ramos têm o mesmo ângulo e a mesma fase da forma preparada, mas rótulos diferentes. O registro tipado conserva fase e rótulo, e seu decodificador tem retorno exato e injetividade na imagem admissível. Isso identifica matematicamente o ramo registrado; não exige inverter a redução que apagou informação.

[REAL] O módulo [ScatteringOutcomeRecord.lean](<C:/IALD/Central de Patentes/Chatgpt/REGISTRO_ANGULAR_20260909_110257_318312/ScatteringOutcomeRecord.lean>) conecta o registro à densidade canônica de espalhamento para 0≤p≤1. Usa o peso do ramo efetivamente escolhido: 1-p na transmissão e p na reflexão. Pelo rótulo, recupera p; na família principal, p determina arcsin(sqrt(p)) e a mesma Smat que o decodificador de fase. Os leitores com as duas convenções de peso têm domínios e nomes distintos. Há controle explícito mostrando que não podem ser intercambiados em transmissão pura.

Os ramos não normalizados são reconstruídos inclusive nas extremidades p=0 e p=1. Normalização exige peso não nulo; peso zero produz ramo zero. O rótulo é dado conservado pelo registro, não uma amostragem estocástica derivada. Os tipos brutos podem descrever um ramo de peso zero; isso não o transforma em ocorrência física observada. A reconstrução vale na família declarada, não para estados arbitrários após apagar suas coerências.

**Estado da frente 2:** o contrato de conteúdo e decodificação está demonstrado para os domínios formalizados. A instrumentação que entrega o registro físico permanece uma correspondência a especificar no modelo de observação.

## 2. Seleção, amplitude e uma geometria curva construída

[REAL] [SelectedAmplitudeGeometry.lean](<C:/IALD/Central de Patentes/Chatgpt/SELECAO_GEOMETRIA_20260909_110405_1043089/SelectedAmplitudeGeometry.lean>) demonstra, usando os estados já existentes no kernel:

p_n = 1/3 - b_n r(t), com r(t)=t²/(1+t²).

Para t conhecido e não nulo, theta_n=arcsin(sqrt(p_n)) permite recuperar

b_n = (1/3 - sin²(theta_n))/r(t).

O registro admissível inclui a preparação e os ângulos, além dos certificados de não negatividade, limite e somabilidade das amplitudes recuperadas. Não recebe métrica, tensor de Einstein nem matching de área/calor como campos. A codificação/decodificação recupera a sequência original; toda leitura admissível também é realizada por suas probabilidades decodificadas. A massa total é reconstruída por soma convergente, com convergência dos prefixos.

Usando essa mesma amplitude decodificada, o módulo constrói os campos da família de ondas já disponível e obtém sua matéria, matching de área e equação de Einstein. A fonte é proporcional à massa reconstruída pelo fator ln(2)/pi, nos termos exatos do modelo. Esta é uma aplicação efetiva dos mesmos dados a uma família curva.

[INPUT] A preparação t, eta não nulo e shear continuam explícitos. Trata-se de probabilidades esperadas e de uma sequência completa ou limite de prefixos com convergência demonstrada; um único resultado binário não fornece essa sequência inteira. O t de preparação não é o fluxo modular do estado fixo. Os theta_n são ângulos de probabilidades locais, sem identificação adicional com o thetaMiguel canônico. A prova opera em carta e frame fixados.

[REAL — controle] A mesma massa com o mesmo eta e shear dá a mesma solda; omitir shear permite mudar uma componente de curvatura na carta fixada. Isso registra concretamente qual informação ainda importa à família.

## 3. Critério geral de reconstrução pelo registro

[REAL] O módulo da geometria selecionada também prova, para tipos arbitrários, que existe um decodificador geométrico na imagem de uma leitura se, e somente se, a geometria é constante em cada conjunto de entradas com a mesma leitura:

read(x)=read(y) implica geom(x)=geom(y).

O decodificador é único nessa imagem. Não é necessário recuperar todas as características do estado microscópico quando elas não mudam a geometria pretendida. A existência abstrata usa escolha clássica; não fornece algoritmo, continuidade, estabilidade numérica nem instrumento físico.

[REAL] [ConeVolumeReconstruction.lean](<C:/IALD/Central de Patentes/Chatgpt/CONE_VOLUME_20260909_112343_982192/ConeVolumeReconstruction.lean>) fornece um conteúdo suficiente concreto para a unicidade métrica: mesmo cone nulo, mesma densidade de volume na mesma carta, sqrt(abs(det(g))) e sinal comum numa direção positiva implicam a mesma métrica. A proporcionalidade conforme vem da rigidez do cone; o volume fixa seu módulo e o sinal fixa o sinal. Há também unicidade ponto a ponto para campos.

Os controles 2g e -g exibem o que pode ser perdido ao omitir volume ou sinal no domínio de comparação usado. A direção positiva fixa convenção de sinal, não orientação temporal. Se ambos os candidatos já forem tipados com a mesma inércia, essa tipagem já exclui certas reversões de sinal.

[OPEN] Esse resultado é de unicidade: não fabrica um campo métrico suave que realize um registro causal arbitrário. É preciso fornecer, a partir dos mesmos dados TGL, o cone causal e a densidade, demonstrar ou postular explicitamente sua realização/regularidade e compatibilidade entre cartas.

## 4. Dinâmica geral sem tetrada nem inversa independentes

[REAL] [GeneralMetricEinstein.lean](<C:/IALD/Central de Patentes/Chatgpt/METRICA_GERAL_20260909_113535_425341/GeneralMetricEinstein.lean>) remove uma exigência desnecessária da interface anterior. O teorema final recebe uma única métrica g suave lorentziana; constrói sua inversa suave pela adjugada e determinante e usa a conexão de Levi-Civita da própria g. A prova não escolhe uma tetrada suave escondida.

Para um tensor A simétrico que se anula no cone, a rigidez dá A=c(x)g. O traço recupera c(x)=Tr(g⁻¹ A)/4 e prova sua regularidade. A conservação torna c constante em um aberto pré-conexo. Aplicando a G(g)-kT e usando a identidade de Bianchi derivada, resulta:

G(g) + Lambda g = k T, com Lambda constante.

[INPUT] Assinatura (1,3), suavidade, domínio aberto pré-conexo, T diferenciável e simétrico, conservação de T, acoplamento constante e balanço nulo de Ricci. O resultado tem alcance geral em carta no setor métrico de Levi-Civita; não faz nova afirmação sobre o setor de Cartan com torção e spin.

**Estado da frente 1:** a reconstrução explícita por seleção fecha em uma família curva; o critério de unicidade métrica e a etapa dinâmica geral foram reforçados. Falta a correspondência geral que produz cone, volume, matéria e balanço dinâmico a partir dos mesmos dados selecionados. Uma lei de correspondência pode ser declarada como postulado; a suficiência resultante deve nomear exatamente esse postulado.

## 5. Setor quântico e identidade óptica

[REAL] [ModularOpticalIdentity.lean](<C:/IALD/Central de Patentes/Chatgpt/SMATRIX_OPTICAL_20260909_110514_326918/ModularOpticalIdentity.lean>) prova, para a convenção S=I+iT, a identidade exata -i(T-T†)=T†T e a relação de composição T(SV)=T(S)+T(V)+iT(S)T(V), preservando a ordem não comutativa. Há versões para os canais matriciais, a matriz de fronteira e órbitas unitárias já construídas na torre, incluindo geradores Pauli.

[REAL — controle] O truncamento linear da matriz de fronteira falha em ser unitário para parâmetro não nulo; o defeito quadrático é exposto no enunciado. O teste opticalBalance=0 corresponde a S†S=I; sozinho não garante sobrejetividade em dimensão infinita. As aplicações do módulo recebem unitariedade bilateral.

**Estado da frente 3:** há nova consistência algébrica exata, mas o teorema não constrói o espalhamento de uma teoria gravitacional interagente, não calcula anomalias quânticas e não demonstra uma rota UV. O setor linear, as direções nulas gerais e os certificados TT/gauge existentes permanecem resultados, não voltam à lista de ausências.

## 6. Alcance da entrega e memória de trabalho

[REAL] O original foi apenas lido. Todas as novas fontes, cópias, logs, backups e recibos estão em Chatgpt. Nenhum um.py foi executado ou importado nesta etapa. A primeira cópia integrada de seis módulos já passou com seu TGLExt e TGL/Audit efetivamente extraídos; a sucessora com sete módulos também passou, com dez processos Lean, 115/115 teoremas na auditoria dedicada e seu próprio recibo final. Não há novo selo ou rodada completa de runtime.

As novas fontes recebem nomes completos em namespaces ChatgptAudit. O nome curto phaseReading já existe em outro namespace; o índice IALD marca a ambiguidade. Use os nomes completos e preserve o diagnóstico.

Este documento registra progresso e pendências para a sessão codificadora. Não é cópia nem substituto do Atlas canônico. O Atlas, as memórias e o desenho canônicos não foram alterados, respeitando o regime de leitura do acervo; o handoff permite incorporar o adendo na casa responsável.

O objetivo amplo permanece ativo. Nenhuma conclusão de gravidade quântica geral demonstrada ou confirmação física é emitida por esta entrega.

[REAL — revisão semântica do relatório] selected_geometry_design confirmou a distinção entre família construída, unicidade cone-volume e dinâmica geral, recomendando explicitar a carta da densidade e não atribuir à convergência uma cota universal de erro. As duas precisões foram incorporadas com backup imediato.

[REAL — integração final] [Cópia congelada de sete módulos](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_114310_143963/um.py>) · [Recibo de compilação e limites](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_114310_143963/RECIBO_INTEGRACAO_E_COMPILACAO.md>) · [Obrigações quânticas detalhadas](<C:/IALD/Central de Patentes/Chatgpt/AVANCO_TRES_FRENTES_20260909_114458_261086/OBRIGACOES_QUANTICAS.md>). A revisão independente também confirmou AST e bytes fora da tabela preservados na sucessora. O Audit completo desta compilação tem 4601 relatórios e 4594 nomes distintos; esses números não são a contagem do manifesto histórico de uma rodada integral do programa.
