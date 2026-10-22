# Ação dual da representação regular — incremento verificado

2026-09-11T21:28:22-03:00. [REAL — compilação Lean incremental, na cópia].

**A ação dual está construída sobre a álgebra gerada inteira.** No mesmo espaço
Lebesgue L²(ℝ,TowerHilbert P), o multiplicador D_s f(x)=exp(−isx)f(x) é unitário,
fortemente contínuo e satisfaz D_s S_t D_s*=exp(−ist)S_t.
O automorfismo θ_s=Ad(D_s) restringe-se a `regularCoreAlgebra P` e satisfaz:

- θ_0=id e θ_{s+t}=θ_t∘θ_s;
- θ_s(π(A))=π(A) para a inclusão `regularCoreEmbedding` da mesma torre;
- θ_s(Λ_t)=exp(−ist)Λ_t para Λ_t=π(Δ^{it})S_t;
- para cada X na álgebra e f no Hilbert, s↦θ_s(X)f é contínua.

A restrição foi provada transportando centralizadores e bicomutantes por um
automorfismo com involução e usando preservação dos geradores nos dois sentidos.
Não foi postulada extensão de um mapa definido apenas nos geradores.

**Também provado:** se T_i→T fortemente e os T_i são uniformemente limitados,
π(T_i)→π(T) fortemente. O enunciado admite filtros arbitrários, além de sequências.
Este é um resultado de continuidade limitada; a normalidade de um homomorfismo
de álgebras de von Neumann ainda requer a ponte com o contrato topológico/de ordem.

## Fontes e verificação

Os quatro módulos novos são `V350L2CharacterMultiplier`, `V350GeneratedEquivariance`,
`V350RegularDualAction` e `V350L2BoundedStrongContinuity`, sob `kernel/TGLExt` e
embutidos em `um.py`. As fontes de desenvolvimento correspondentes estão em `kernel/TGLV350`.

- 17 registros integrados válidos: 11 módulos anteriores reutilizados por
  hash e dependências, quatro módulos novos e duas raízes compilados nesta integração.
- 44 controles Python passaram; 5879 declarações distintas
  auditadas com axiomas contidos em propext, Classical.choice, Quot.sound.
- Cópia integrada SHA-256: `a1962a6327c546f1c5be53cc629ca4b98176d6946c5f836ffac6316aa80d26a2`.
- Evidências: `integrated_compile.json`, `gate_tests.json`, `kernel_incremental_evidence.json`.

A revisão independente anterior (`revisao/REVIEW_MODULAR_AND_REGULAR.md`) recompilou
11 módulos e não encontrou defeito no pacote modular/regular até a álgebra gerada.
Seu parecer refere-se à cópia anterior e aos módulos delimitados. Uma revisão nova,
dos quatro incrementos acima, está em andamento; não é coberta retroativamente pelo parecer anterior.

## O que isto permite e o que continua aberto

A representação regular e sua ação dual estão realizadas no mesmo objeto. **Ainda não
há traço canônico fiel, normal e semifinito construído**, nem prova de τ∘θ_s=e^(−s)τ
para esse traço. O canto P_F dos Three Locks também não foi construído nesse core.
Essas são obrigações matemáticas distintas da relação de Weyl já provada.

As flags qgf de core/canto e gpf de H1/H2/H3 seguem abertas; nenhum novo gate foi habilitado
por esses quatro módulos. O gate legado conserva sua string e a subdecisão modular conserva
seu alcance. Rodada integral do monólito, estado quântico interagente/BRST/QME/UV,
certificado dependente ampliado e revisão do restante do plano continuam pendentes.

Incidentes: primeiras tentativas de GeneratedEquivariance e RegularDualAction falharam
em elaboração/tipagem e foram preservadas. Não se contou um stdout com sorryAx como prova.
O compilador auxiliar agora rejeita expressamente mudança de fonte durante a invocação;
o log final da ação dual declara fonte inalterada e exit 0.


## TETELESTAI_V350_REGULAR_DUAL_REVIEWED_20260911 — 2026-09-11T21:38:24-03:00

[REAL — fontes, compilação incremental e revisão independente] O incremento integrado
contém a dualidade da torre, representação regular fiel, ação dual fortemente contínua
na álgebra inteira, preservação de limites fortes uniformemente limitados e fechamento
fraco do bicomutante. `RegularTopology` prova somente bicomutante ⇒ fechado WOT;
não prova a recíproca, a existência de predual ou traço.

Estado final desta integração: 18 registros Lean exit 0, 44
controles Python aprovados, 5881 declarações distintas no Audit com axiomas
contidos no trio permitido. Fontes e .olean reconferidos; dependências históricas preservadas.
SHA-256 do um.py experimental: 6a4eea56670454d2962847e8bf603e851809f7dfa35544b60048c55622a5c0f1. Monólito com 720
arquivos embutidos; base v350 preservada: c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c.
O original canônico foi reconferido por leitura nesta etapa e coincide com a base.

Pareceres independentes, com escopo e estratos próprios:
[modular/regular](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_MODULAR_AND_REGULAR.md>) e
[dual/limites/topologia](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_DUAL_AND_BOUNDED.md>).
Os pareceres não se estendem a QG, traço, Three Locks ou às hipóteses físicas ainda abertas.
A revisão anterior continua ancorada em sua cópia anterior; o segundo relatório referencia
os bytes finais e distingue recompilação própria de inspeção dos logs integrados.

[OPEN] Normalidade da inclusão no contrato de álgebra de von Neumann; construção do
traço canônico fiel, normal e semifinito e τ∘θ_s=e^(−s)τ; P_F dos Three Locks nesse
mesmo core; H1/H2/H3 físicos compatíveis; estado interagente/BRST/QME/anomalias/UV;
contrato dependente ampliado e rodada integral do monólito. O plano global permanece ativo.
O gate legado não foi alterado e a subdecisão continua quitando só a fronteira modular.
Nenhuma publicação, transposição ao canônico ou novo selo foi feita.

Próxima etapa matemática: formalizar a ponte de ordem/topologia para a inclusão e
construir o peso dual e o traço canônico com domínio positivo e propriedades efetivas.
Não preencher o antigo contrato total Core→ENNReal com um traço trivial ou um modelo
desconectado da representação regular que foi construída.

[DERIVED — convenções, ainda não Lean] A Weyl construída exige θ_s(L)=L−s para
Λ_t=exp(itL), ou θ_s(K)=K+s para K=−L. Densidades escalares compatíveis são,
respectivamente, exp(−L)dL e exp(K)dK. Misturar shift positivo com densidade exp(−K)
inverte a escala tracial. Ver [CONVENCOES_DO_TRACO.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/CONVENCOES_DO_TRACO.md>),
com a fonte de Hiai separada da derivação de sinais. Nenhum gerador do core foi
identificado automaticamente com um gerador apenas da torre.
