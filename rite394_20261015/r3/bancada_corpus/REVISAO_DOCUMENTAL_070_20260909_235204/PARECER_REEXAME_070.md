# Revisão documental delimitada da entrega 070

09/09/2026. [DERIVED — análise própria de coerência documental] [REAL — leitura e medição dos artefatos]. Esta revisão não recompila Lean, não executa CAS nem um.py e não repete as provas das entregas anteriores. O manifesto registra os bytes exatos examinados.

**Conclusão:** não identifiquei erro material na síntese `REEXAME_SUFICIENCIA_070_20260909/REEXAME_SUFICIENCIA.md` quanto aos pontos solicitados. O texto mantém a diferença entre a completação formal e a classe suave covariante, identifica a primitiva relativa residual e conserva as limitações da redução RG. O parecer expressa minha análise; não é uma aprovação em nome do operador ou de outra tarefa.

## 1. Formalidade e o contrato característico

A abertura, a seção 4 e a seção 7 preservam o ponto central: a eliminação formal de M₂ não fornece automaticamente uma primitiva C∞(U). O transporte em Λ mantém sua hipótese de base na mesma classe e sua terminação é por grau K; não há especialização de uma série infinita.

A equivalência métrica–vielbein é apresentada como local e formal, no setor da identidade e com dados de fundo. O relatório não a transforma em independência quântica de fundo, equivalência topológica global ou anulação de cohomologia.

Também não há identificação indevida de

\[
H^4_2(\delta\mid d_H,\widehat A)
\quad\text{com}\quad
H^2_{\mathrm{char,cov}}(A_{\mathrm{nat}}(U)).
\]

O primeiro é o resultado relativo no espaço formal delimitado pela nota de normalidade; o segundo exige primitivas covariantes na classe suave especificada. A seção 4 não usa a ausência de reducibilidade para apagar o representante M₂, e a seção 7 exige sua covariantização e a comparação/descida na mesma álgebra. A seção 3 mantém condicional a redução do canal de anomalias a esse grupo característico.

O argumento dos quatro covetores foi reproduzido com o mesmo sinal, dQ=−2b dx⁰. A precisão `B=Du=D(dy)` foi acrescentada em arquivo novo junto da nota de normalidade; é um Hessiano simétrico, sem derivada adicional. Nenhuma fonte congelada foi corrigida por cima.

## 2. Controles CAS e estatutos

Li o recibo `VERIFICACAO_REDUCAO_RG.json`: ele se identifica como `PASS_EXACT_ON_SHELL_RG_REDUCTION__NOT_LEAN` e contém 16 entradas com `passed=true` e resíduo `0`. A inspeção estruturada desses campos e a comparação do pin do script são registradas no manifesto desta revisão. Isso verifica o conteúdo e a custódia do recibo; não repete o cálculo simbólico.

A seção 6 do relatório atribui os 16 controles à rodada de RG e declara explicitamente zero compilação ou teorema Lean novo. Os 31 controles 069 são identificados como anteriores e não reexecutados. A linguagem não transforma essas verificações algébricas da redução em prova compilada da Hessiana, da teoria de campos ou da QME.

Os números históricos da auditoria 069 e da captura canônica são atribuídos aos seus recibos. Esta revisão não executou o programa canônico nem repetiu a auditoria 069; o manifesto distingue esse limite de uma revalidação independente de todos os números históricos.

## 3. Coeficientes e sinais RG

O relatório reproduz os polinômios A₁,A₂ e a combinação FRW da fonte de redução. Em s=4,

\[
A_1=-49/6,\quad A_2=151/3,\qquad
3A_1+A_2=(-147+302)/6=155/6.
\]

Com K=ℏ/(4π)², a convenção bare escrita é g_B^E=g^E(μ)+K A log(ρ²/μ²). Derivar em log μ mantendo o bare fixo dá 0=β_E−2KA, portanto β_E=2KA na ordem indicada. A identificação local formal g^E=−b dá β_b=−2KA. Assim

\[
\mu\frac{d(3b_1+b_2)}{d\mu}
=-2K\frac{155}{6}=-\frac{155\hbar}{3(4\pi)^2},
\]

como consta do relatório. Essa verificação escrita confere o sinal e o fator dois; não importa uma convenção Lorentziana não declarada.

A corrente remanescente depois de Bochner vale (1−s)□Q/6. No fundo citado, s=4 e □Q=−3x/2, portanto resulta 3x/4. O relatório distingue corretamente essa parcela dos 5x/4 do representante anterior e não altera o C₄ total. Também preserva a distinção entre o representante polinomial escolhido fora das soluções e o coeficiente da verdadeira Hessiana off-shell, não calculado por essa extensão.

Permanecem explícitos os limites: a relação Euclidiano/Lorentziano é uma regra local formal de ação; os acoplamentos finitos não são determinados pelo logaritmo; não há fluxo único de κ,c,Λ sem esquema adicional, nem backreaction completa ou energia física total inferida da parcela local.

## 4. Pendências que a síntese conserva

O próximo passo permanece a primitiva M₂ suave e covariante, ou uma homotopia direta de H²_char,cov no espaço admissível. A ausência universal de reducibilidade e a equivalência BV formal deixam de ser lacunas integrais, sem suprimir os contratos restantes.

A conclusão do relatório conserva a ligação da classe de contratermos à anomalia efetivamente produzida, a descida/colagem, a remoção por renormalizações finitas em todas as ordens e a QME. Estado e setor físico interagentes, independência de fundo, questões globais, UV e integração das folhas anteriores continuam separados. Não se declara a gravidade quântica resolvida, nem se convertem dados naturais ou o gate histórico em prova adicional.

Não proponho alteração do relatório examinado. O adendo de notação do Hessiano é suficiente para a única precisão solicitada na nota fonte, cujo conteúdo matemático foi preservado.
