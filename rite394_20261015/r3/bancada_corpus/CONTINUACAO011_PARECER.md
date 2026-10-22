[REAL / INPUT / OPEN] Continuação 011 — entropia da torre e purificação de corte
Data: 05/09/2026. Bancada ChatGPT; entrega espontânea posterior à ordem 007 e à continuação 010.

## Resultado que muda o próximo passo

[REAL — Lean] A torre efetiva tem entropia diagonal S_N=Σ_{n=0}^N h(P.w_n). Para perfil constante p∈(0,1), S_N=(N+1)h(p), com h(p)>0. O cálculo usa os pesos canônicos towerW, e sua expectativa do gerador diagonal −log p coincide com S_N.

[REAL — Lean] Foi construída uma purificação bipartida explícita desses mesmos pesos. As duas marginais são calculadas por traço parcial, e a expectativa de todo observável esquerdo coincide com tState(P,N). Há coerência entre andares para esses observáveis.

[REAL — Lean] A entropia reduzida dessa purificação é a mesma S_N. Ela pode ser escrita como ηA_N com A_N=a(N+1) e η=h(p)/a para qualquer a≠0. A construção não escolhe a unidade a. Duas escolhas positivas, a=1 e a=2, foram verificadas sobre o mesmo estado; produzem áreas distintas e coeficientes recíprocos.

[OPEN] A igualdade por contagem ainda não identifica uma área geométrica transversal. O próximo dado necessário é um mapa explícito entre fatores/pares e regiões ou vínculos de corte, com área geométrica definida independentemente da entropia. A purificação não paga H3 nem a existência dos horizontes físicos da continuação 010.

## Objetos e demonstrações

### 1. Entropia finita e primeira lei

[REAL] FiniteEntropyAlgebra.lean define S(p)=−Σ_i p_i log p_i e prova aditividade para pesos produto normalizados, marginais e informação mútua diagonal nula. A igualdade de primeira variação usa o teorema canônico first_law_diagonal, com p_i>0 e Σq_i=0.

O funcional é definido para todos os pesos reais, porque Real.log é total. Sua interpretação como entropia exige pesos não negativos e normalizados. Nas instâncias towerW essas condições vêm de towerW_pos e towerW_sum. Não se generalizou esse estatuto físico para pesos negativos.

[REAL] A expectativa do gerador diagonal H_p=diag(−log p_i) é a entropia. Esse H_p é o operador do logaritmo da densidade finita; o resultado não o identifica com −log Δ do operador modular de Tomita, que atua na representação GNS.

### 2. Escala da torre

[REAL] TowerEntropyScaling.lean prova a fórmula para perfil geral e o crescimento linear para perfil constante. A mesma entropia é ligada à expectativa do objeto de contagem normalizedVolumeObject construído na ordem 003.

[REAL — implicação delimitada] Se uma sequência proposta de áreas satisfaz A_N/(N+1)→0, não existe η real constante com S_N=ηA_N para todos N no perfil constante admissível. A prova compara limites, sem aproximação numérica.

Esse resultado não exclui uma lei de área para toda interpretação possível. Se N+1 conta vínculos que atravessam um corte, essa contagem pode vir a representar área; se conta graus de liberdade de volume, é necessária outra construção. O teorema também não estende a obstrução a todos os perfis não constantes, cujo crescimento depende dos pesos.

### 3. Purificação calculada

[REAL] SchmidtCutPurification.lean define Ψ(i,j)=δ_ij√p_i e ρ=|Ψ⟩⟨Ψ|. Prova positividade, traço unitário e idempotência para pesos normalizados não negativos. Calcula ambas as marginais como diag(p); prova a identidade do traço parcial para observáveis esquerdos.

[REAL] BoundaryEntropyBridge.lean instancia p=towerW(P,N) e obtém:

- ρ_N positivo, normalizado e idempotente;
- Tr_R ρ_N=Tr_L ρ_N=diag(towerW(P,N));
- Tr[ρ_N(a⊗I)]=tState(P,N,a), para toda matriz a;
- compatibilidade dessa expectativa com towerStep;
- entropia da marginal calculada igual à entropia da torre;
- expectativa do gerador diagonal igual à entropia reduzida;
- fidelidade da restrição esquerda;
- falha da fidelidade na álgebra bipartida completa, em todo andar.

A falha de fidelidade não é só uma observação sobre posto: o teorema produz a≠0 com Tr[ρ_N(a†a)]=0. A testemunha é a projeção sobre (i,j), i≠j.

A função reducedDiagonalEntropy toma a entropia da diagonal da marginal. Neste pacote a marginal foi provada diagonal; a função não é uma implementação de entropia de von Neumann para matrizes arbitrárias.

A compatibilidade provada é da família de expectativas esquerdas. Não se construiu aqui um limite de Hilbert bipartido com dinâmica, rede local, representação modular contínua ou evolução geométrica. Não é uma substituição já concluída da torre canônica.

### 4. Controles de correlação e unidade

[REAL] EntropyGeometryControls.lean prova que a densidade pura não é o produto de suas marginais quando há dois pesos positivos. O controle usa uma entrada fora da diagonal, sem inferir correlação apenas do nome “purificação”.

Para siteW(1/2), a densidade global é positiva, normalizada e idempotente; a entropia reduzida é log 2. A informação mútua diagonal nula é provada para a distribuição PRODUTO comparativa. Não foi atribuída à densidade pura correlacionada. A entropia é invariante sob p↦1−p.

[REAL] A troca a↦ca é acompanhada por η↦η/c. O coeficiente 2π/η usado na reconstrução condicional de 010 escala por c. Esta é uma identidade algébrica; a aplicação física exige η não nulo e a>0. Não fixa G nem uma unidade de área.

## Relação com a rota gravitacional

[KNOWN] A referência de Jacobson recebe proporcionalidade entre entropia e área e o balanço de Clausius como premissas da derivação termodinâmica. Fonte primária: [Jacobson, 1995](https://arxiv.org/abs/gr-qc/9504004).

[REAL / INPUT] A entrega 010 formalizou uma implicação para dados locais de horizonte. A entrega 011 determina a entropia do estado finito e uma realização bipartida com essa marginal. A composição física entre os dois pacotes ainda requer identificar a função A dos dados de horizonte com uma área transversal derivada da geometria e justificar a dinâmica do calor e o balanço.

[OPEN] A purificação mantém o mesmo estado esquerdo. Portanto não oferece, por si, uma evasão da obstrução de Borchers provada em 007 para a torre-produto sob suas hipóteses. Para prosseguir nessa rota é necessário mudar ou justificar explicitamente a estrutura relevante: estado limite, álgebra, inclusão, representação ou relação de covariância. Renomear fatores como “corte” não basta.

## Verificação, tentativas e custódia

[REAL] Os cinco módulos novos receberam compilação limpa de suas versões finais. Todos os teoremas têm #print axioms, com dependências contidas em {propext, Classical.choice, Quot.sound}. O manifesto mede contagens, bytes, hashes e identifica os logs de cada versão. Definições auxiliares são listadas; não são contadas como teoremas.

[REAL] A conferência somente de leitura da entrega 010 passou novamente antes de fechar este pacote. Ela confere a preservação daquele inventário, não substitui recompilação independente.

As tentativas falhas permanecem em logs e backups de bytes. Houve falhas de inferência, normalização, ordem em ℂ e notação; nenhum log com erro, aviso ou sorryAx conta como prova final. Uma tentativa de revisão por nome ambíguo foi recusada pelo helper antes de escrever: schmidt_amplitude_norm também era prefixo de schmidt_amplitude_normalized. O comando seguinte recompilou a versão antiga; seu log de falha permanece no histórico. O registro desse incidente é retrospectivo, não um log de execução inventado.

A biblioteca externa Lean 4.31.0/mathlib é a instalada nesta máquina. O pacote fixa fontes locais, cópias binárias TGL/TGLExt e evidências de compilação; não é distribuição portátil nem auditoria independente. A gerência ainda precisa recompilar e examinar os enunciados antes de incorporar.

Escritas desta bancada somente em Chatgpt. Nenhuma execução/importação de um.py, nenhuma edição no kernel canônico, Atlas, memórias, selos ou gate. Nenhum dado observacional utilizado. Nenhuma afirmação de solução geral ou confirmação de gravitação quântica.

## Próximo alvo preciso

[OPEN] Construir, ou refutar sob hipóteses explícitas, um vínculo geométrico independente entre a família de marginais e áreas de cortes. A entrada mínima deve incluir a escolha de regiões, a correspondência algébrica e uma medida de área que não seja definida por S/η. Depois, demonstrar sua variação e a relação com o calor no mesmo estado. É esse vínculo, junto à dinâmica e às demais folhas abertas, que falta para aplicar a reconstrução condicional já formalizada.
