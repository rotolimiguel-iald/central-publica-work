# Derivada do cociclo limite por erro linear — 09/09/2026

[REAL — fontes compiladas e revisadas] Duas folhas congeladas passaram com **8 teoremas, 1 definição e 9 declarações auditadas**, quatro processos Lean com código zero, sem avisos e axiomas restritos a propext, Classical.choice e Quot.sound. O agente raiz leu integralmente as duas fontes finais e registrou parecer semântico favorável, inclusive aos ajustes de representação linear e instâncias de escalares.

## Derivar o limite sem supor convergência local de derivadas

[hasDerivAt_of_linear_cutoff_error](<C:/IALD/Central de Patentes/Chatgpt/DERIVADA_LIMITE_COCICLO_20260909_155045_687120/DerivativeFromLinearCutoffError.lean:27>) recebe funções f_N,f:ℝ→E, derivadas d_N em zero, d_N→d, erros e_N≥0 com e_N→0 e o controle ‖f(t)−f_N(t)‖≤|t|e_N. A conclusão é HasDerivAt f d 0.

A prova tem dois passos efetivos. [slope_norm_error_le](<C:/IALD/Central de Patentes/Chatgpt/DERIVADA_LIMITE_COCICLO_20260909_155045_687120/DerivativeFromLinearCutoffError.lean:12>) divide o erro pelo incremento e obtém erro entre slopes menor ou igual a e_N. Para t≠0, a norma do inverso cancela |t|; em t=0, ambos os slopes são zero. Depois, ε/3 escolhe um corte N pelos dois limites e usa somente a derivada desse corte para controlar seu slope perto de zero. A desigualdade triangular e hasDerivAt_iff_tendsto_slope concluem a derivada de f.

A hipótese de mesmos valores em zero também decorre do controle de erro. [cutoff_base_value_eq](<C:/IALD/Central de Patentes/Chatgpt/DERIVADA_LIMITE_COCICLO_20260909_155045_687120/DerivativeFromLinearCutoffError.lean:52>) prova essa igualdade; [hasDerivAt_of_linear_cutoff_error_auto_base](<C:/IALD/Central de Patentes/Chatgpt/DERIVADA_LIMITE_COCICLO_20260909_155045_687120/DerivativeFromLinearCutoffError.lean:59>) oferece a interface sem a hipótese redundante.

[INPUT — escopo explícito] E é um espaço normado real; completude não é necessária nesta passagem, pois f e d já são dados. O resultado **não recebe convergência das derivadas em uma vizinhança** e não supõe a derivabilidade da função limite. A existência do próprio limite f pertence ao módulo de completude/cociclo anterior ou à instanciação que o fornece.

## Propagar a derivada pelo cociclo canônico

[canonicalConjugationRealLinear](<C:/IALD/Central de Patentes/Chatgpt/DERIVADA_LIMITE_COCICLO_20260909_155045_687120/CanonicalCocycleDerivative.lean:11>) é a aplicação linear contínua real formada do modularConjugation canônico por restrição de escalares. Sua continuidade é o teorema canônico existente; não se define um novo fluxo.

[canonical_cocycle_hasDerivAt](<C:/IALD/Central de Patentes/Chatgpt/DERIVADA_LIMITE_COCICLO_20260909_155045_687120/CanonicalCocycleDerivative.lean:24>) usa a lei u(t+r)=u(t) alpha_t(u(r)) e HasDerivAt u d 0 para concluir:

u′(t) = u(t) alpha_t(d).

A regra da cadeia aplica alpha_t para t fixo, o produto multiplica à esquerda por u(t), e a translação r=x−t devolve a função u em torno de t. Não se exige derivabilidade temporal de alpha_t em todos os operadores.

[canonical_cocycle_generator_equation](<C:/IALD/Central de Patentes/Chatgpt/DERIVADA_LIMITE_COCICLO_20260909_155045_687120/CanonicalCocycleDerivative.lean:52>) especializa d=iV:

u′(t) = u(t) · i alpha_t(V).

O gerador está **à direita**, conforme a convenção de cociclo usada. [canonical_cocycle_differentiable](<C:/IALD/Central de Patentes/Chatgpt/DERIVADA_LIMITE_COCICLO_20260909_155045_687120/CanonicalCocycleDerivative.lean:60>) conclui diferenciabilidade em todo tempo, sem afirmar regularidade superior.

## Aplicação e limites

[DERIVED — interface para composição] Nos cortes concretos, a sessão raiz pode usar d_N=iV_N, a convergência dos V_N e o erro linear aprovado dos cociclos para obter u′(0)=iV. A segunda folha então fornece a equação em todo tempo. A identidade do cociclo e a estimativa de corte devem ser descarregadas pelos módulos concretos; não são campos acrescentados ao construtor para fingir essa identificação.

Estas duas fontes são as ferramentas analíticas dessa composição. O presente recibo não inclui uma nova recompilação da aplicação completa a pauliCocycle, um estado modular perturbado, ligação à fonte gravitacional, ausência de anomalias ou limite UV.

## Evidência

| Fonte | Teoremas | Outras declarações | Recibo |
|---|---:|---:|---|
| DerivativeFromLinearCutoffError | 4 | 0 | [PASS](<C:/IALD/Central de Patentes/Chatgpt/DERIVADA_LIMITE_COCICLO_20260909_155045_687120/BUILD_20260909_155459_329222/BUILD_RESULT.json>) |
| CanonicalCocycleDerivative | 4 | 1 | [PASS](<C:/IALD/Central de Patentes/Chatgpt/DERIVADA_LIMITE_COCICLO_20260909_155045_687120/BUILD_20260909_155649_636626/BUILD_RESULT.json>) |

Primeira fonte: 3152 bytes; SHA-256 `0864931af0535af15439939c2f1e767ff04ca3c5159e965426a7efc6bbc69049`.

Segunda fonte: 3225 bytes; SHA-256 `a2d4a6fc451cb76a04274324a95fd9d12d51ceb39fff479f4d76e7f5f331a2da`.

O primeiro build da primeira folha preserva o aviso de variável de seção desnecessária; a revisão removeu essa hipótese apenas do lema que não usa escalares. O primeiro build da segunda folha preserva os erros de API/diamantes de instâncias corrigidos por toAlgEquiv e convert!. Nenhuma conclusão matemática foi substituída por postulado. Todas as tentativas e backups imediatos em bytes permanecem na pasta.

Cada build recompila uma fonte nova e um importador em diretório isolado, usando os binários canônicos/Mathlib existentes. Fontes/binários diretamente importados são medidos antes e depois; não houve rebuild transitivo integral. Nenhum um.py foi executado/importado, nenhum original foi alterado e nenhuma memória canônica, Atlas, selo ou gate foi tocado.
