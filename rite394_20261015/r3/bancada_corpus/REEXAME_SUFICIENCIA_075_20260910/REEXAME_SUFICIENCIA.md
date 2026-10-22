# Reexame de suficiência — entrega075

10/09/2026. [REAL — arquivos conferidos] [DERIVED — demonstrações escritas] [KNOWN — importações delimitadas].

**A pendência encolheu: a descida da anomalia pode ser construída dentro da classe natural do esquema causal declarado. Ainda falta construir a primitiva que permitiria removê-la.** O canônico continua na versão v338 encontrada na última entrega; os avanços desta etapa estão documentados na bancada Chatgpt.

A [captura atual](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_075_20260910/ESTADO_CANONICO_075.json>) comparou quatro artefatos canônicos com a entrega074: todos conservaram seus bytes. O um.py tem 11,048,796 bytes, 683 arquivos embutidos e selo correspondente. No conjunto de 98 módulos do integrador anterior, 77 estão presentes e 21 continuam ausentes. Essa contagem mede aquele conjunto delimitado; não mede toda a prova.

O programa não foi executado ou importado. A evidência de rodada anterior foi lida. Não houve Lean, CAS, cálculo de diagramas ou novos testes de natureza nesta etapa. Nenhum arquivo original, Atlas, índice, memória canônica ou gate foi alterado.

## O que ficou demonstrado nesta etapa

Na apresentação métrica e nos fibrados graduados declarados, os ghosts e antifields de ghost não zero têm jatos livres. Linearizar uma forma fechada em variações independentes permite resolver seu símbolo principal por uma identidade algébrica de Koszul. A quantização covariante desse símbolo reduz a ordem do operador; derivadas dos coeficientes e curvaturas permanecem no resíduo. Ao final, a identidade de Euler fornece a primitiva natural nos graus de forma menores que quatro.

O primeiro passo, que envolve uma topforma, usa outro antecedente: a consistência da anomalia implica a nulidade dos operadores Euler dessa topforma. Integração por partes covariante fornece então o primeiro descendente. Com os passos restantes obtemos

\[
\Omega=a_4^1+a_3^2+a_2^3+a_1^4+a_0^5,
\qquad (s+d_H)\Omega=0.
\]

A demonstração está na [nota de operadores](<C:/IALD/Central de Patentes/Chatgpt/DESCIDA_NATURAL_SIMBOLOS_075_20260910/DESCIDA_NATURAL_POR_OPERADORES.md>), completada pelo [adendo do primeiro descendente](<C:/IALD/Central de Patentes/Chatgpt/DESCIDA_NATURAL_SIMBOLOS_075_20260910/ADENDO_PRIMEIRO_DESCENDENTE_E_COMPOSICAO_075.md>) e pelo [parecer independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_DESCIDA_E_REES_075_20260910/PARECER_INDEPENDENTE_DESCIDA_E_REES.md>). Os operadores horizontais preservam laço, valência e o peso de Rees por componente quando suas conexões são as dos fibrados fixados por B0. Intercalar s pode misturar valências; a classe completa deve continuar preservada.

A aplicação ao modelo causal foi conferida separadamente. A consistência vale antes de impor as equações aos argumentos dinâmicos. O fundo B0 pode continuar restrito às referências admitidas: a descida preserva um ideal diferencial que contenha relações apenas desses coeficientes. Os jatos de ghosts e antifields precisam permanecer livres. Fontes centrais positivas como ω devem entrar entre esses geradores, ou ser retiradas por uma projeção compatível.

A [auditoria de aplicação](<C:/IALD/Central de Patentes/Chatgpt/APLICACAO_DESCIDA_OFFSHELL_075_20260910_022420_157704/APLICACAO_OFFSHELL_E_FONTES_CENTRAIS.md>) e a [revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_075_20260910/PARECER_APLICACAO_RELATIVA_075.md>) explicitam essa conclusão relativa. A consistência off-shell usada na importação está no [teorema7 de Fröb](https://arxiv.org/pdf/1803.10235v3). Isso não estende automaticamente a identidade a fundos arbitrários nem resolve a cohomologia total.

## O que ainda falta

| Obrigação | Estado após esta etapa |
|---|---|
| Remover a anomalia na classe admissível | [OPEN] Construir a primitiva total de Ω. A descida fornece um cociclo fechado; sua exatidão continua por demonstrar. |
| Completar o cálculo cohomológico necessário | [OPEN] Controlar H¹(s), H²(s), H⁵(s) e os canais H¹(Ebar_N;H⁴(s)), H²(Ebar_N;H³(s)) na mesma classe natural formal e na categoria de B0 realmente usada. São condições suficientes da rota074; não se declarou uma anomalia não nula. H³ aqui é cohomologia BRST, não a antiga hipótese H3 de horizonte. |
| Transformar a primitiva em normalização causal | [OPEN] Preservar regularidade, escala por aridade, realidade, independência funcional, inserções e contatos em toda a família de contratermos. Uma corrente ou densidade isolada não fornece essa família. |
| Fechar o setor quântico interagente | [OPEN] Construir corrente/carga renormalizadas, implementação do diferencial, nilpotência e QME no domínio comum; depois consumir o resultado condicional de positividade. P0 no setor livre declarado permanece preservado. |
| Compatibilidade entre referências | [OPEN] Acordo perturbativo e identificação dos esquemas, estados e cutoffs no alcance pretendido. A descida relativa não paga independência quântica geral de fundo. |
| Reconstrução gravitacional geral | [OPEN] Fornecer pelos mesmos dados TGL selecionados os objetos e relações exigidos pelo teorema geral, ou assumir explicitamente uma lei de correspondência e manter a suficiência condicionada a ela. As construções particulares permanecem válidas no alcance já demonstrado. |
| Altas energias | [OPEN] Justificar a rota UV escolhida. O próprio selo canônico mantém aberta a parede de renormalização; finitude de Breuer não foi aceita como resposta automática. |
| Integração verificável | [OPEN] Incorporar e verificar no um.py os materiais aprovados e módulos ainda ausentes. Nota escrita e presença no código não equivalem a compilação auditada. |

Fase complexa e distinção de ramo, H3 interno e falsificadores já existentes não são reabertos. A suficiência pretendida pode usar resultados importados com hipóteses verificadas; não exige refazer a literatura. Exige, porém, demonstrar que as importações e construções pertencem à mesma classe do modelo que as consome.

## Encaminhamento para a sessão que codifica

Incorporar o teorema de descida junto com o complemento de topforma, a precisão de graus e a aplicação relativa. O estatuto é [DERIVED — demonstração escrita revisada], até a verificação formal pertinente. Não criar uma bandeira de remoção da anomalia ou QME com base apenas em (s+d_H)Ω=0.

O próximo alvo matemático é a primitiva total na categoria correta. Investigações posteriores sobre representantes de H³/H⁴ pertencem à etapa076 e não integram o resultado certificado desta entrega.

As revisões matemáticas estão em [parecer de descida](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_075_20260910/PARECER_DESCIDA_NATURAL_075.md>) e no parecer de aplicação já ligado acima. A [entrega074](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_074_20260910/REEXAME_SUFICIENCIA.md>) conserva o histórico do termo de curvatura e do critério total. O objetivo geral permanece em aberto; a entrega075 não declara gravidade quântica resolvida ou confirmada.
