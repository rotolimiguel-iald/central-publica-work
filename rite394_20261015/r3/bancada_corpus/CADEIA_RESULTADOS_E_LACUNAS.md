[REAL] Adendo de verificação à demonstração escrita `CADEIA_LOCALIZACAO_VOLUME.md`, 05/09/2026. Não substitui os estatutos históricos daquele texto.

## O que o kernel verificou

Foram compilados dez módulos, com 55 declarações `theorem`. Uma sonda separada imprime as dependências axiomáticas de todas as 55: somente `propext`, `Classical.choice`, `Quot.sound`. São axiomas fundacionais usuais do ambiente Lean, não axiomas físicos acrescentados.

1. **Localização fiel:** `chain_order_faithful` prova A(I)≤A(J) ↔ I⊆J, inclusive para conjuntos não finitos. A álgebra definida é o adjoin algébrico estrelado dos geradores. Para conjuntos infinitos, não se deve chamá-la automaticamente de álgebra de von Neumann; o bicomutante é construído separadamente. `chain_locality` prova comutação para suportes disjuntos. `site_noncommutation` fornece a testemunha que distingue um sítio ausente: E₀₀ e E₀₁ não comutam no mesmo sítio, pela injetividade da representação.
2. **Prefixos:** `chain_prefix_eq_level` prova A({0,…,N})=M_N, e `prefix_expectation_into` situa E_N na rede. O andar N contém N+1 sítios. Não foi validada a igualdade literalmente escrita A([0,N))=M_N, que tem erro de índice nessa convenção.
3. **Cauda completa:** `chainTailClosure P N` é o duplo centralizador de A({N,N+1,…}). `chain_tail_mem_factor` prova T_N⊆M; `chain_tail_antitone` prova a diminuição; `chain_tail_exact` prova, sem hipótese adicional de pertinência a M, que (∀N,x∈T_N) ↔ (∃c,x=c1). Assim, a restrição intermediária x∈M em `ChainTail.lean` foi eliminada no módulo posterior.
4. **Fluxo:** a ação modular sobre cada gerador está calculada em `modularConjugation_site`. `shifted_generator_intertwining` usa explicitamente o perfil P⁺(n)=P(n+1). `uniform_generator_intertwining` usa a hipótese P(n+1)=P(n). Esses enunciados não contêm um termo global ρ:M→M; não substituem essa construção.
5. **Volume:** q_I=Σe_i é local, positivo e aditivo em conjuntos disjuntos. ω(q_I)=ΣP(i); para P constante igual a p, ω(q_I)=p|I|. A calibração com constante única para todos os conjuntos finitos implica P constante. O objeto normalizado Σe_i/P(i) tem avaliação |I| para qualquer perfil fiel. Essa última normalização escolhe uma unidade e não determina comprimento físico.

## O que ainda não se pode incorporar como teorema Lean

**Esperanças localizadas gerais — [OPEN].** A demonstração anterior descreve a construção por traço parcial ponderado e compressão GNS. Nesta entrega, somente as esperanças de prefixos estão conectadas à nova rede. Falta um termo para I finito arbitrário com os oito campos verificados. O caminho concreto é construir o tensor sobre I, provar a inclusão fiel e a redução pelas ações esquerda/direita, identificar a projeção p_I e refazer a prova de compressão. A igualdade E_I E_J=E_(I∩J), normalidade e completa positividade não receberam provas Lean novas nesta ordem. A escrita anterior é uma derivação/esboço analítico, não um certificado desses campos.

**Shift global — [OPEN sob hipóteses adequadas].** Falta construir em Lean a isomorfia GNS H(P)≅H(P₀)⊗H(P⁺) e o homomorfismo normal correspondente M(P⁺)→T₁(P). Para um perfil estacionário, a identificação P⁺=P dá a rota para o endomorfismo pretendido. Unitalidade, injetividade, imagem própria e covariância do homomorfismo global ainda não estão formalizadas. A cauda decrescente e sua interseção estão formalizadas, mas não sua identificação com potências de um ρ ainda não construído.

**Pedido universal de shift normal — [DERIVED, obstrução analítica].** O perfil alternado 1/3,2/3 da demonstração anterior impede uma extensão normal que desloque todos os geradores prescritos. A prova usa médias locais limitadas com limites fortes escalares diferentes antes/depois do shift. Os controles exatos enumeram distribuições produto finitas e confirmam média p e variância p(1−p)/n para n=1,…,8. Não transformam essa enumeração em prova do limite infinito. A prova analítica do limite usa densidade da órbita local e a estimativa do comutador; ela ainda não foi formalizada.

**Inclusão meio-lateral contínua — [OPEN].** O shift estacionário preserva a inclusão modular para todos os tempos, mas a cauda sobre Ω não é cíclica no Hilbert total. Faltam as hipóteses de standardness e a ação contínua com gerador positivo e lei de dilatação. A localização fiel na cadeia não é uma rede de cunhas de espaço-tempo reconstruído.

**Ponte de volume contínua — [OPEN].** ω(q_I) é avaliação de um estado produto em objetos positivos. Não é o traço semifinito do core em projeções geométricas. Faltam a correspondência região↔objeto, o limite contínuo, a unidade física e a identificação do peso apropriado. Nenhuma métrica foi reconstruída por esses resultados. A obstrução conforme anterior permanece.

## Escopo de preservação e auditoria

Todos os novos arquivos, compilações e controles desta bancada foram escritos sob `C:\IALD\Central de Patentes\Chatgpt`. O programa copiado foi analisado como texto na ordem 004; não foi importado ou executado. As fontes canônicas não foram editadas por esta bancada. A sessão irmã pode alterá-las simultaneamente; a preservação medida aqui é a das cópias contra seu manifesto, e não uma alegação de imutabilidade global do computador.

Os 55 teoremas passaram no compilador local. A auditoria independente e a decisão de incorporação pertencem à gerência; nenhum gate é alterado por esta entrega.
