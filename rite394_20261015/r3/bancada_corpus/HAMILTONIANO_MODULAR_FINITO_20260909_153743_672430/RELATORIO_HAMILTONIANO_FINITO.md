# Hamiltoniano modular finito e extensão espectadora — 09/09/2026

[REAL — compilação auditada] A fonte [finiteModularHamiltonian](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:27>) constrói o operador H0_N=towerPi(diag(log W_N)). Seus 20 teoremas, 5 definições e 2 instâncias locais nomeadas passaram: **27 declarações auditadas**, duas execuções Lean com código zero, sem avisos e somente axiomas padrão propext, Classical.choice e Quot.sound. A fonte está congelada.

## Cadeia efetiva

- [level_hamiltonian_exp](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:57>) identifica exp(it diag(log W_N)) com a matriz diagonal de modularPhase(t,log W_N).
- [finite_modular_unitary_eq_towerPi](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:69>) transporta a igualdade pela representação canônica towerPi. [finite_hamiltonian_selfadjoint](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:43>) prova auto-adjunção do operador no Hilbert canônico; [finite_modular_unitary_unitary](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:74>) prova unitariedade da exponencial.
- [level_modular_action](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:88>) identifica a conjugação matricial com flowLevel, incluindo o sinal e a diferença dos logaritmos nos dois índices.
- [finite_modular_action_eq_canonical](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:108>) conclui a igualdade da ação interna exp(itH0_N) A exp(−itH0_N) com modularConjugation P t A para todo A do andar N. O lado canônico é o objeto existente, não uma nova função homônima.

## Inclusões de andares e espectador

O peso do andar seguinte é produto do peso antigo pelo peso do sítio adicional. A positividade canônica de SiteProfile permite aplicar log(xy)=logx+logy. No comutador com a matriz a⊗I, os logaritmos do sítio adicional cancelam.

[level_commutator_step](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:123>) prova esse cancelamento por entradas; [level_commutator_push](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:141>) o estende por indução para N≤M. Multiplicatividade e compatibilidade de towerPi entregam [finite_commutator_extension](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:163>).

O resultado final [finite_spectator_commutes](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:179>) é Commute(H0_M−H0_N,A) para TODO A∈levelOperatorAlgebra P N. A hipótese de comutação não é recebida; é derivada da inclusão efetiva. [finite_spectator_commutes_base](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:189>) especializa A=H0_N e [finite_spectator_selfadjoint](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteModularHamiltonian.lean:194>) atesta a auto-adjunção da diferença.

Isso fornece os elos espectador/base necessários para comparar cociclos de dois cortes usando um mesmo Hamiltoniano de referência maior. O produto de exponenciais e a estimativa de Duhamel são construídos em folhas separadas.

## Hipóteses e limites

[INPUT — tipos declarados] Um SiteProfile canônico com pesos estritamente positivos e menores que um; N,M naturais e N≤M quando há inclusão. A é um elemento do andar explicitado. O alvo é válido para matrizes locais arbitrárias, sem exigir auto-adjunção de A.

[REAL] Os H0_N são operadores limitados de suporte finito representados no Hilbert canônico. O teorema identifica sua ação modular sobre a álgebra daquele andar. **Não afirma** convergência dos H0_N em norma, existência de Hamiltoniano modular global limitado, identidade desses operadores finitos com o logaritmo global não limitado de Delta, existência do cociclo interagente no limite, ausência de anomalias ou controle UV.

A revisão semântica independente do agente raiz foi favorável ao módulo integral, inclusive ao logaritmo do produto e ao comutador espectador. Depois dela, as duas instâncias locais receberam nomes estáveis e auditoria explícita; os enunciados matemáticos foram preservados e o resultado recompilado.

## Evidência e preservação

[Recibo PASS](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/BUILD_20260909_154117_765191/BUILD_RESULT.json>).

Fonte: 9940 bytes; SHA-256 `7da1de3894d41f14b2822172bdab4820e4810c931aff785f8c4d388d0ad4bf64`.

O primeiro build ficou preservado como FAIL_VISIBLE com dois erros de elaboração; o segundo passou antes da nomeação das instâncias; o terceiro é o recibo final de 27 declarações. Os backups imediatos são cópias em bytes. Nenhum backup, tentativa, original ou fonte canônica foi apagado ou alterado.

O builder compila somente a folha nova e um importador, em diretório novo. Fontes/binários importados diretamente são medidos antes e depois; dependências canônicas e Mathlib transitivas usam binários existentes, sem reconstrução integral. Nenhum um.py foi executado/importado e nenhum Atlas, memória canônica, selo ou gate foi alterado.

Uma segunda folha FiniteLevelExponentials está sendo verificada separadamente; seus resultados não são pressupostos neste recibo.
