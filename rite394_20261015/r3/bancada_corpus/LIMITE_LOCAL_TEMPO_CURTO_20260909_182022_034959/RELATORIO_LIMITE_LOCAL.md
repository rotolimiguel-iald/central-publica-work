# Limite local da evolução efetiva em tempo pequeno

[REAL] SmallTimeLocalDynamics.lean está congelada com PASS_COMPILED_SCOPE: 12 teoremas + 4 definições, 16 auditorias; dois processos Lean terminaram com código zero, sem avisos. Fonte: 7480 bytes; SHA-256 medido 5c60897d0ddc3cead0f2b0f2c83cf893a64ecb67ee0e8e937cc3002be26d8e3b.

[REAL] O teorema finite_evolution_tendsto_local_series (linha 109) demonstra convergência EM NORMA da evolução efetiva exp(itH_N) A exp(−itH_N) ao candidato construído pela série estabilizada. Não recebe a existência do limite como hipótese. Recebe A na álgebra local do prefixo [0,R] e 2J|t|<1. J=0 inclui todo tempo real. Os termos da interação têm suporte {j,j+1}, são auto-adjuntos e têm norma uniformemente limitada; não há hipótese de soma global finita nem comutação entre termos.

[DERIVED] A cota previamente demonstrada para o comutador iterado transforma-se, após a divisão por k!, no majorante q^k·choose(k+R,R)·‖A‖, q=2J|t|. A série binomial é somável para q<1. Cada coeficiente do corte coincide com o coeficiente estabilizado quando N≥R+k. O teorema de convergência dominada de séries de Mathlib (Tannery) dá o limite da mesma evolução finita identificada na folha FiniteCommutatorEvolution.

[REAL] finite_evolution_cauchy_local (linha 121) fornece a sequência de Cauchy dos cortes. local_series_evolution_norm (linha 128) preserva a norma, e local_series_evolution_independent_prefix (linha 137) prova que dois prefixos admissíveis dão o mesmo limite. O número R é uma escolha de suporte, não um parâmetro físico da evolução.

[REAL] O root leu integralmente as duas folhas desta continuação e aprovou semanticamente a cadeia, suas hipóteses e limites. A última correção foi somente substituir uma conversão de igualdade de funções por Summable.congr. Todos os axiomas auditados pertencem a propext, Classical.choice e Quot.sound. Fontes compiladas e fontes entregues foram comparadas em bytes; limites do ambiente de leitura permanecem no recibo.

[OPEN] A convergência formalizada nesta folha é pontual no tempo. Não se afirma aqui uniformidade em intervalos compactos, extensão a todo tempo por composição, automorfismo do fecho quase local, extensão normal ao fator, fundo modular ou estado KMS. O símbolo tsum continua totalizado pela biblioteca fora do domínio; somente os enunciados com hA e q<1 atestam a convergência e a interpretação dinâmica. Este avanço extensivo local não é uma afirmação de conclusão UV relativista.

O lote de duas folhas acrescenta 28 teoremas e 14 outras declarações, todos compilados e auditados. Integração em um.py é uma etapa posterior por cópia. Nenhum um.py foi executado ou importado; nenhum original foi alterado. Os dois fracassos anteriores desta folha e os backups de bytes foram preservados.
