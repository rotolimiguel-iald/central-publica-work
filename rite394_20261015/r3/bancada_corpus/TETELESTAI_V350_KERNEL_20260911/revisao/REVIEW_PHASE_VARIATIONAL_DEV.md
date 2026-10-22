# Revisão DEV parcial — seleção variacional de fase

2026-09-13T03:38:02-03:00. [REAL — leitura integral e recompilação independente de **RealPhaseVariational.lean, 12 declarações**.] **Sem P0, P1 ou P2 neste módulo congelado.** O exame dos12 está concluído; o estágio permanece parcial, sem manifesto cumulativo e sem módulo concreto aceito neste parecer.

**Semântica/tipos conferidos:**

- **Linhas16–33:** `phaseRealMap` multiplica por conj(z) antes da restrição de escalares. Como o produto interno complexo é conjugado-linear no primeiro argumento, a compressão real produz exatamente **Re(z⟨x,y⟩)**, sem troca de sinal. K é submódulo **real**, e a projeção mantém o contradomínio K mesmo quando K não é estável por escalares complexos.
- **Linhas35–48:** B_z(x,x)=Re(z)‖x‖² prova coercividade com constante Re(z)>0. Nenhuma simetria, positividade complexa de B_z ou novo produto interno foi pressuposto. O caso não real de z está abrangido.
- **Linhas51–82:** a solução é a inversa da equivalência Lax–Milgram aplicada à projeção ortogonal de x. Equação vale para todo x∈H e todo teste v∈K; unicidade é provada entre todos os u∈K que satisfazem essa equação. A hipótese `hu` é a condição de candidato à solução, não uma hipótese residual de existência. Foi relida a implementação Mathlib `IsCoercive.continuousLinearEquivOfBilin`, que não exige simetria.
- **Linhas85–119:** Re(z)‖η‖≤‖x‖ resulta da equação testada em η e Cauchy–Schwarz, incluindo η=0. Re(z)=1 dá contração; **z=1** dá a própria projeção ortogonal. A fonte não afirma que toda fase com Re(z)=1 produza a projeção.

Os tipos do auditor usam H:`Type` (universo0), estrutura de Hilbert complexo e K:`Submodule ℝ H` com `CompleteSpace K`; a completude de H permanece nos teoremas impressos. Não há densidade, standardness ou não trivialidade de K pressuposta. K=0 é caso legítimo. Nenhum SiteProfile, F/S/J, peso ou álgebra concreta entra nestes enunciados.

Precisão sobre o alcance: **o mapa de solução x↦η é de fato um operador limitado real-linear H→K**, já construído como CLM. A cota é desse mapa e de seu vetor de saída. Ela **não** constrói nem limita o multiplicador de álgebra associado a η. Também não prova a identidade complexificada, (V)/(P), invertibilidade do bloco de gráfico ou pertinência a Fix S concreto.

| Nome, namespace TGLV350.Regular | Axiomas próprios |
|---|---|
| `phaseRealMap` | trio |
| `phaseCompression` | trio |
| `phaseVariationalForm` | trio |
| `phaseVariationalForm_apply` | trio |
| `phaseVariationalForm_diagonal` | trio |
| `phaseVariationalForm_coercive` | trio |
| `phaseVariationalSolution` | trio |
| `phaseVariationalSolution_equation` | trio |
| `phaseVariationalSolution_unique` | trio |
| `phaseVariationalSolution_bound` | trio |
| `phaseVariationalSolution_unit_real_bound` | trio |
| `phaseVariationalSolution_one` | trio |

“trio” = `propext`, `Classical.choice`, `Quot.sound`, conferido transitivamente nos12 prints. Foram lidos os12 tipos completos com universos. Quatro definições e oito teoremas; nenhum axiom/sorry/admit/unsafe novo ou atributo de redutibilidade introduzido na fonte.

**Reprodução própria:** fonte rc0 em **14.88s** e auditor separado12 rc0 em **13.581s**, sem warnings/stderr. Binário próprio **byte a byte igual** ao autoral. SHA fonte `fe34c27260bd05593679bf2e03b06ab7c7f92993aeed8c657616075c4b00b265`; .olean `d0b971a22b746d8392ff5eba125068b249dfa8a58b6f08e4fab85d55a72acffb`. Log autoral final `RealPhaseVariational_20260913_032929_894153.json`, SHA `793532d142256d63962db549df0aa29eb7132ee52140b120615842e670fcf048`. Mãe `adjoint_polar_graph_custody.json`, SHA `727e919fc181c271a50b004b37fcb3ec8aeb95b9cec36e4917b1049cfc7e7dee`, conferida por pin/verificação existente, sem reauditoria ampla da custódia.

O módulo importa somente quatro Mathlib: **zero dependências de projeto precisaram ser copiadas/recompiladas**. Reutilizados os oito caminhos de pacotes readonly da árvore própria anterior `adjoint_polar_graph_final_independent_20260913_025725_898901`; 11 pins externos diretos/herdados relidos antes e depois. LEAN_PATH contém somente build próprio e pacotes externos, sem build autoral de projeto. A cadeia interna inteira dos pacotes não foi reconstruída nem integralmente re-hasheada; sua proveniência é herdada, com os imports diretos pinados e axiomas transitivos auditados.

**Duas tentativas autorais rc1 rejeitadas e preservadas:** `_032257_168445` (coerção `starRingEnd`, argumento de `inner_self_im` e rewrite dependente da prova de positividade) e `_032843_186947` (falha de `linarith` no caso Re(z)=1). Seus prints com `sorryAx`, e também os prints verdes parciais, não serviram de evidência de aceite. Apenas os bytes/log final rc0 e a reprodução própria foram aceitos.

[Compilação própria](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/phase_variational_independent_20260913_033307_003262/compilation.json>) — SHA `62ea5d5eb90e3d0bfaaeabb0306801c56012099f5c8d3414e1c9f6a63ca87a1a`; [manifesto próprio/pins/pacotes](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/phase_variational_independent_20260913_033307_003262/manifest.json>); [12 tipos e axiomas](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/phase_variational_independent_20260913_033307_003262/logs/PhaseVariationalAudit.stdout.txt>); [verificação e histórico excluído](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/phase_variational_independent_20260913_033307_003262/verification.json>) — SHA `32de83d886aa5a076007026f7537b2291832e993875f59d66db8353c009ef154`.

[OPEN] Aplicação a Fix S original, passagem à identidade complexa e prova do teste ponderado, multiplicador limitado com adjunto, inclusão inversa, KMS/traço/gate. Não há integração deste módulo certificada aqui. Fontes/binários autorais, mãe, monólito e gate permaneceram iguais aos pins; nenhuma memória ou helper autoral foi executado/alterado. Escritas exclusivamente revisao. **Parecer parcial12 pronto para futura ampliação por adendo, sem antecipar o módulo concreto.**


---

## Adendo DEV final cumulativo — 21 alvos

2026-09-13T03:51:26-03:00. **PHASE_VARIATIONAL_DEV_REVIEW**

[REAL — leitura integral, reprodução própria e auditoria de tipos/axiomas.] **Sem P0–P2 nos dois módulos congelados (12+9). Escopo DEV encerrado.** Este adendo preserva o estrato parcial acima e o amplia com ScalarPhaseVariational; a falta de aplicação concreta que constava naquele estrato foi superada somente no alcance descrito abaixo. Nenhuma integração é aprovada neste parecer.

**Pontos substantivos conferidos em ScalarPhaseVariational.lean:**

- **Linhas13–28:** a instância local de completude vem do fechamento do submódulo real Fix S já existente, obtido do gráfico fechado original. Não cria norma, hipótese sobre P ou novo operador. `scalarPhaseVariational` especializa exatamente o CLM real anterior; sua pertinência prova η∈D(S) e Sη=η no mesmo ScalarGNSHilbert P.
- **Linhas30–56:** equação real, unicidade, cota Re(z)‖η‖≤‖ξ‖ e caso z=1 são aplicações diretas dos lemas genéricos. A seleção vale para qualquer ξ do Hilbert e Re(z)>0. Re(z)=1 dá contração; z=1 dá projeção. Não é suposta simetria de B_z.
- **Linhas58–109:** a promoção do pareamento real para complexo exige explicitamente ξ∈D(F) e Fξ=ξ. Para v∈Fix S, o pareamento do adjunto máximo original dá ⟨v,ξ⟩=⟨ξ,v⟩, logo parte imaginária zero. A equação real produz 2⟨ξ,v⟩=z⟨η,v⟩+conj(z)⟨v,η⟩. `fixedComplexFromPairing` recebe hipóteses genéricas, mas a aplicação concreta descarrega-as com v.property, scalarTomitaAdjoint_pairing e a equação variacional; nenhuma ficou como premissa residual.
- **Linhas111–135:** para TODO u∈D(S) original, scalarClosedTomita_fixed_decomposition fornece u=h+ik e Su=h−ik com h,k∈Fix S. A combinação das duas identidades é hh−i·hk, respeitando a conjugação no primeiro argumento. Assim:

  **2⟨ξ,Su⟩ = z⟨η,Su⟩ + conj(z)⟨u,η⟩**, η=scalarPhaseVariational P z hz ξ.

Os tipos/universos foram lidos no auditor. O módulo concreto recebe P:SiteProfile e os objetos originais; os auxiliares privados usam H:Type. A identidade final mantém `hz : 0 < z.re`, `ξ : scalarTomitaAdjointDomain P`, `Fξ=ξ` e `u : scalarClosedTomitaDomain P`. Não exige continuidade de S/F, domínio total em H, hipótese KMS ou pertinência de pares ponderados. Foram lidos os cinco auxiliares privados e auditados transitivamente: fixedPairReal, realPairComplexIdentity, fixedComplexFromPairing, complexRelationFromDecomposition e graphEquationFromFixed. Limites de elaboração da fonte permanecem 200000; fonte final sem sorry/axiom/unsafe ou alteração de redutibilidade.

| Novo alvo — namespace TGLV350.Regular | Auditor próprio |
|---|---|
| `scalarPhaseVariational` | trio |
| `scalarPhaseVariational_fixed` | trio |
| `scalarPhaseVariational_equation` | trio |
| `scalarPhaseVariational_unique` | trio |
| `scalarPhaseVariational_bound` | trio |
| `scalarPhaseVariational_unit_real_bound` | trio |
| `scalarPhaseVariational_one` | trio |
| `scalarPhaseVariational_fixed_complex_equation` | trio |
| `scalarPhaseVariational_graph_equation` | trio |

Trio = propext/Classical.choice/Quot.sound, sem outros axiomas. O auditor cumulativo confere **exatamente21 nomes e mapas de axiomas**, iguais ao manifesto e aos streams autorais finais. Os12 nomes anteriores permanecem no estrato preservado.

**Evidência própria:** ScalarPhaseVariational rc0 em **103.514s**; auditor21 separado rc0 em **24.433s**, ambos sem warnings/stderr. Binário concreto próprio byte a byte igual ao autoral. RealPhaseVariational reutilizado da reprodução própria verde anterior, com fonte/binário relidos; não recompilado redundantemente.

- ScalarPhaseVariational fonte SHA `907e5b1b9a87e946e3086bbf395209783f70179efa7befe08fdef40fb0a809bb`; .olean próprio/autoral `13380e004607b28af63c4b1f08ca26f879a5b0b1f7fe9a4db8928c0b460760df`.
- Log final autoral ScalarPhaseVariational_20260913_034056_185241.json SHA `c58a9714ff11ab27fe26fbe1d00f90381c2937cfa3db470291e6847334c3c462`; stdout SHA `2137689d5e83fb7d8639bad320e0f593b5d8368da0fac25bc489a88d388c2b03`. As quatro rc1 `_033206_169218`, `_033422_188089`, `_033608_904818` e `_033838_745756` foram lidas/preservadas e integralmente excluídas, inclusive prints “sem axiomas” e prints verdes parciais. Falhas: coerções/CompleteSpace, nomes derivados ausentes e timeouts whnf/isDefEq. Somadas às duas rc1 do genérico, **seis tentativas autorais rejeitadas**.
- Manifesto autoral phase_variational_draft_status.json SHA `958f74b45913bd808fe32f8961cabd7b6dd7bd95933375cb47b7fde3456e0e0d`; relatório autoral lido integralmente SHA `297bcca96200f322dd85f35380fdf5d34d672d8a208c36ad0d6c24e27438090a`. Texto distingue seleção, identidade em D(S), obrigação dos pares ponderados e multiplicador ainda aberto; sem achado documental.
- Mãe adjoint_polar_graph_custody.json SHA `727e919fc181c271a50b004b37fcb3ec8aeb95b9cec36e4917b1049cfc7e7dee`, conferida com sua verificação e os pins atuais de um.py/gate. Os números209/103/7056 e as seis flags falsas são o estrato integrado da mãe; não constituem integração nem testes destes21. Não houve nova execução de gate, monólito, recorder ou reauditoria das34 memórias.

**Dependências:** 403 módulos de projeto congelados a partir de árvores próprias, com fontes/binários e arquivos acompanhantes conferidos antes/depois; nenhum build autoral de projeto no LEAN_PATH. Origem principal `adjoint_polar_graph_final_independent_20260913_025725_898901`; ScalarTomitaStandardSubspace recuperado da árvore própria `closed_scalar_tomita_independent_20260912_100020_793911`, cujos manifestos/compilação também foram pinados. RealPhaseVariational vem de `phase_variational_independent_20260913_033307_003262`. O catálogo inicial não continha ScalarTomitaStandardSubspace e parou antes de executar Lean; esse erro de preparação está preservado, resolvido sem aceitar binário autoral ou reconstruir dependências. Oito caminhos de pacotes externos readonly, 11 pins externos diretos/herdados; seus interiores não foram integralmente reconstruídos/re-hasheados. Axiomas transitivos dos21 foram efetivamente auditados nesta execução.

[Compilação própria](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/phase_variational_final_independent_20260913_034807_811147/compilation.json>) — SHA `a74186a2eeb01ea8befcddf258c31c07cd0fc284543ac3d250760ae82a8adc16`; [manifesto/pins](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/phase_variational_final_independent_20260913_034807_811147/manifest.json>); [21 tipos e axiomas](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/phase_variational_final_independent_20260913_034807_811147/logs/PhaseVariationalAudit21.stdout.txt>); [verificação](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/phase_variational_final_independent_20260913_034807_811147/verification.json>) — SHA `ee2d6d5a498d37de419f64ec94a53f4fce9f30169abed1c149a25c1338b33380`; [histórico excluído](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/phase_variational_final_independent_20260913_034807_811147/author_history.json>).

[OPEN] O mapa ξ↦η é um operador limitado REAL-linear para Fix S; isso não constrói o multiplicador associado a η. A identidade complexa não demonstra que os pares ponderados pertençam a D(S), nem resolve (V)/(P), invertibilidade do bloco A ou inclusão inversa. A consulta por CFC/quadrados permanece DERIVED e fora destes21. KMS, identificação do fluxo Δ^it, traço/gate/runtime não são promovidos. **Nenhuma análise DEV necessária destes dois módulos permanece pendente; integração futura exige escopo próprio.**
