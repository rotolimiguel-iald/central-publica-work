# Reexame de suficiência086 — o cancelamento quadrático foi decidido no teste fixado

10/09/2026. [DERIVED — resultados matemáticos escritos, com revisões distinguidas abaixo]. [REAL — estado documental e canônico conforme snapshot086]. A etapa086 resolve uma pendência concreta da085: **não existe corrente natural quadrática de Weyl/EOM, com finitos jatos, cuja divergência seja J_W, no fundo e na classe de coeficientes fixados.** Isso decide negativamente essa rota de cancelamento; o fechamento do objetivo físico geral ainda requer outros resultados.

O que falta agora se divide em quatro tarefas:

1. **Reconstrução física geral pelos mesmos dados selecionados:** realizar matéria, conservação, área e calor no mesmo registro e em um atlas físico compatível, com as hipóteses de correspondência explicitadas. A fase/ramo e H3 interno já reconhecidos no modelo não são reabertos.
2. **Teoria interagente no complexo físico pertinente:** calcular os setores, graus e diferenciais restantes, estabelecer contratermos causalmente admissíveis e a equação mestra quântica; construir a carga BRST e justificar a positividade interagente sob esses contratos. A teoria linear e os resultados condicionais anteriores não pagam automaticamente essa passagem.
3. **Integração e verificação no programa canônico:** o snapshot086 continua em v338, com 77 dos98 módulos acompanhados e21 ausentes. As demonstrações escritas086 não são novas folhas Lean compiladas nem resultados já executados pelo um.py.
4. **Regime UV:** justificar uma rota com alcance declarado além da expansão perturbativa/EFT, sem usar finitude de outro objeto como resposta automática à renormalização gravitacional.

## O resultado que deixa de estar aberto

O contrato comum fixa dimensão quatro, orientação, referência Lorentziana espaço-forma, K>0 real fixado, κ real não nulo, sigma constante projetado ao setor métrico e escalares herdados Rher inertes. As expressões são naturais e contêm finitos jatos por coeficiente. Não entram tensores espectadores, dependência coordenada ativa ou séries de derivadas ilimitadas.

[DERIVED — demonstração escrita com revisão independente] A [prova de todas as ordens finitas](<C:/IALD/Central de Patentes/Chatgpt/SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md>) demonstra a estriteza das relações Einstein, injeta o graduado curvo no módulo plano e conserva a derivada principal. Todos os vetores quadráticos principais vêm de Wᵣ⁺Wᵣ₊₁⁺ ou da quiralidade negativa. A divergência é injetiva nessas cópias, como mostram duas ondas métricas planas puramente quirais.

Assim, um vetor efetivo não nulo tem ordem total d≥5 em h e sua divergência tem ordem exatamente d+1≥6. J_W tem ordem quatro e símbolo não nulo. Portanto **div₀V=J_W é impossível**, e também div₀V=0 força V=0 nessa categoria. A extensão escalar real cobre coeficientes nilpotentes sem tentar separá-los por números. O [parecer independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684/PARECER_ESTRITEZA_E_DIVERGENCIA_086.md>) não identificou erro material nesse alcance.

Não é preciso afirmar que os jatos curvos de Weyl sejam livres. A injeção do graduado, com a filtragem pela SOMA das ordens dos fatores e com a derivada, basta. A prova não é um limite de uma busca finita por candidatos.

## Duas demonstrações complementares086

[DERIVED — demonstração escrita, revisão independente existente] A [análise de transgressão e cohomologia característica](<C:/IALD/Central de Patentes/Chatgpt/PONTRYAGIN_CARACTERISTICO_E_LIMITE_BBH_086_20260910_062514_4956488/NAO_EXATIDAO_INVARIANTE_E_LIMITE_DA_IMPORTACAO_BBH.md>) constrói a primitiva ordinária tr(L∧Dbar L) de tr(W₁∧W₁). Seu defeito de gauge permanece no shell. Portanto ela não pertence à classe de correntes invariantes de Weyl/EOM. A existência dessa primitiva ordinária e a inexistência da corrente invariante são compatíveis. O [parecer específico](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_PONTRYAGIN_CARACTERISTICO_086_20260910/PARECER_TRANSGRESSAO_GL_E_CONTRATO_CARACTERISTICO_086.md>) conferiu a fórmula e o defeito, sem importar automaticamente um teorema não linear de grau máximo.

[DERIVED — fonte escrita; revisão independente específica ainda pendente no corte deste relatório] A [classificação com uma derivada](<C:/IALD/Central de Patentes/Chatgpt/CORRENTES_WEYL_UMA_DERIVADA_086_20260910/CLASSIFICACAO_CORRENTES_W_NABLA_W_E_DIVERGENCIA.md>) obtém V=A grad I+B grad J_W, com I=½W², e imagem livre gerada por □I e □J_W. Ela conserva □W=6KW e, portanto, □J_W=12KJ_W+2J₁. Esse setor não produz J_W, mesmo com o canal Euler invariante permitido. É uma prova delimitada própria; sua revisão posterior deve ser ligada no adendo final. A prova geral acima já possui seu parecer específico e não depende de promover essa revisão pendente.

## Consequências CE e dos líderes cúbicos

[DERIVED — dedução escrita da raiz; revisão independente específica pendente no corte deste relatório] Os [corolários086](<C:/IALD/Central de Patentes/Chatgpt/COROLARIOS_CE_E_LIDER_CUBICO_086_20260910/COHOMOLOGIA_CE3_E_IMAGEM_CUBICA_ZERO_APOS_C6.md>) combinam a forma normal084, N₂^g=0 da085, a injetividade da divergência086 e os mapas077/080/082. No MESMO contrato, dão:

- H³(C(g,N₂)^h,dCE)=0, com N₂=Rher⊗Sym²Mcal;
- a linha λ↦λ[J_Wν] injeta Rher em H⁴ CE;
- im[H³(C_N,s)→H³(C₃,s)]=0 para todo N≥6.

O terceiro enunciado exclui todos os líderes cúbicos não nulos desse teste, incluindo as correções admissíveis da linha que sobrevivia até C₅. Não afirma H³(C_N)=0: classes que começam em valência posterior continuam possíveis. A projeção do complexo formal também se fatora por C₆, mas isso não calcula lim¹ nem estabelece Mittag–Leffler para todos os alvos. A revisão dos corolários, quando concluída, será registrada ao lado; não é antecipada aqui.

O resíduo é de ghost quatro. Ele não é um coeficiente de anomalia física de ghost um nem uma violação calculada da QME interagente. H³ desses complexos tampouco é o H3 interno da tela. A decisão de uma rota cohomológica não exclui as soluções físicas do modelo nem fornece um veredito da TGL inteira.

## Estado atual do um.py e custódia

[REAL — leitura estática registrada às09:54:42UTC de10/09/2026] A [inspeção canônica086](<C:/IALD/Central de Patentes/Chatgpt/INSPECAO_CANONICO_NAVEGACAO_086_20260910/PARECER_INSPECAO_CANONICA_086.md>) e seu [snapshot](<C:/IALD/Central de Patentes/Chatgpt/INSPECAO_CANONICO_NAVEGACAO_086_20260910/ESTADO_CANONICO_INSPECAO_086.json>) mediram os mesmos quatro artefatos de085: um.py, selo, manifesto Lean e stdout v338. O programa continua com11.048.796 bytes,683 arquivos embutidos e77/98 módulos presentes;21 estão ausentes. O hash do programa coincide com o selo. Não foi observado stdout sucessor naquele diretório; isso não nega trabalho em outra cópia ou em preparação.

O cabeçalho canônico conserva área e conservação como condições da reconstrução; R e sua origem física permanecem INPUT, e a correspondência física, os mesmos dados de matéria/área, anomalias e UV permanecem OPEN. O gate e o selftest são vereditos lidos do programa, não reexecutados nesta etapa. Presença AST não equivale a compilação086.

A navegação Atlas/índice aponta para v338. A divergência histórica entre “última COMPLETA” v336 no append do Atlas e v320 no índice permanece registrada, sem resolver a custódia por inferência. Nenhum desses números é evidência de versão posterior à v338. Não houve cópia nem bifurcação do Atlas.

Zero novas execuções matemáticas, CAS, Lean ou ritos de natureza em086. Os recibos contam verificações documentais, não novos teoremas compilados. Somente novos arquivos em Chatgpt; originais, memórias canônicas, selo e gate preservados. A [memória086](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_086_20260910/MEMORIA_DE_TRABALHO_086.md>) e o [adendo ao desenho](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_086_20260910/DESENHO_DO_FECHAMENTO_ADENDO_086.md>) registram a passagem para a sessão codificadora. Resultados posteriores à086 não são consumidos neste relatório.
