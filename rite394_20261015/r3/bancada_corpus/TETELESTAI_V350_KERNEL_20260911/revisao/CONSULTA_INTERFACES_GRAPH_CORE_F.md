# Consulta — interfaces para graph-core do F original

2026-09-13T01:26:37-03:00. **Consulta de fontes, sem compilação e sem revisão dos novos rascunhos.** Não certifica a prova por blocos ainda em construção. Mãe `scalar_vna_custody.json`, SHA lido `f9f3fc9f6e6592c679daad828b688bc2419d242f7b3b0c8ee6b132ac4520a4ff`; contagens herdadas da custódia 201/101/6982, não reexecutadas.

A costura final pode reutilizar diretamente a decomposição em pontos fixos de uma involução antilinear fechada. A nova obrigação substancial permanece provar densidade **real em Fix F** dos vetores de operadores direitos auto-adjuntos por meio da identidade positiva dos blocos. A densidade complexa de j já existente não dá essa conclusão.

Interfaces exatas lidas:

| Uso | Nome e alcance |
|---|---|
| Fix real, fechado | `ChatgptAudit.Continuous049.fixedRealSubmodule`, `mem_fixedRealSubmodule_iff`, `fixedRealSubmodule_closed`, `fixedClosedSubmodule` |
| Decomposição simultânea | `ChatgptAudit.Continuous049.domain_fixed_decomposition`: para x∈D, fornece h,k∈Fix, x=h+i k e F x=h−i k |
| Domínio e ação | `ChatgptAudit.Continuous049.mem_domain_iff_fixed_sum`, `fixed_sum_tomita`; a primeira isoladamente não fornece o valor de F |
| Estrutura padrão, se útil | `ChatgptAudit.Continuous049.closedAntilinearStandardSubspace` recebe fechamento, invariância do domínio, involução e densidade; não é necessária para a última passagem ao fecho do gráfico |
| F concreto | `TGLV350.Regular.scalarTomitaAdjointDomain`, `scalarTomitaAdjoint`, `scalarTomitaAdjoint_isClosed`, `scalarTomitaAdjoint_maps_domain`, `scalarTomitaAdjoint_involutive`, `scalarTomitaAdjoint_domain_dense` |
| j e estrela | `TGLV350.Regular.scalarRightPairVector` é ℂ-linear; `scalarRightPairVector_original_adjoint` fornece pertinência em D(F) e F(j a)=j(a*); `scalarRightPairVector_injective` permite refletir estrela a partir da igualdade dos vetores |
| Vetor do novo par | `TGLV350.Regular.scalarRightPairVector_of_pair` identifica j do operador tipado com o vetor efetivamente construído, independentemente da escolha |
| Inclusão já fechada | `TGLV350.Regular.scalarRightPairGraph_closure_subset_original` já prova closure(graph j)⊆graph F; basta construir a inclusão oposta |

Fontes: [genéricos de Fix](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/ClosedAntilinearStandardSubspace.lean:48>), [F original](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarTomitaAdjoint.lean:13>), [j e ligação a F](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarRightPairVector.lean:57>), [gráfico existente](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarRightHilbertCore.lean:53>).

Instanciação sugerida, **esquema não recompilado nesta consulta**: `D := scalarTomitaAdjointDomain P`, mapa semilinear `F := (scalarTomitaAdjoint P).toFun`. Aplicar os genéricos acima com `scalarTomitaAdjoint_isClosed P`, `scalarTomitaAdjoint_maps_domain P` e `scalarTomitaAdjoint_involutive P`. O wrapper existente `scalarTomitaStandardSubspace P` e `scalarClosedTomita_fixed_decomposition` usam S, não F: não reutilizá-los como se seus pontos fixos fossem os do adjunto.

Para a densidade real, tomar K=Fix F fechado e E_sa={j(a) | a*=a} como submódulo **ℝ de K** (ou provar a formulação equivalente com inclusões no ambiente). Fechamento sob soma/escala real vem da linearidade de j e das leis da estrela; `scalarRightPairVector_original_adjoint` coloca esses vetores em K. `Submodule.topologicalClosure_eq_top_iff` aplicado em K reduz a densidade a E_saᗮ=⊥. Não o aplicar como se E_sa fosse complexo ou como se sua clausura devesse ser todo H.

A instanciação real canônica é a scoped instance de `ClosedSubmodule`: o próprio comentário Mathlib recomenda `open ClosedSubmodule`, sem criar outra estrutura de produto interno. `ClosedSubmodule.inner_real_eq_re_inner` identifica ⟨x,y⟩ℝ=Re⟨x,y⟩ℂ. A identidade dos blocos deve produzir, para η∈K não nulo, um R=R* pareado e v=j(R) com

`Re⟨η,v⟩ = ‖Pη(η,0)‖² + ‖(1−Pη)(0,η)‖² > 0`.

O primeiro termo é estritamente positivo: se Pη(η,0)=0, a ortogonalidade a todos (Λa,π(a)η) dá ⟨η,Λa⟩=0; `scalarWeightGNSEmbedding_denseRange` elimina η. Isso contradiz η∈E_saᗮ e fornece a densidade real desejada. Esta passagem é uma obrigação nova efetiva, não consequência de `scalarRightPairVector_denseRange` ou `scalarRightPairVector_products_dense`.

Para converter densidade real em graph-core, sugiro um lema genérico separado sobre j, estrela e F, sem expandir a álgebra concreta:

1. Para x∈D(F), `domain_fixed_decomposition` dá h,k∈K com (x,Fx)=(h+i k,h−i k).
2. Pela densidade, (h,k)∈closure(E_sa×E_sa); usar `closure_prod_eq`.
3. O mapa contínuo Φ(u,v)=(u+i v,u−i v) envia (j(a),j(b)), a*=a e b*=b, ao par (j(a+i b),j((a+i b)*)), por linearidade e conjugação do escalar i.
4. Como `closure (scalarRightPairGraph P)` é fechado, sua pré-imagem por Φ é fechada. `closure_minimal` transporta (h,k) ao fecho do gráfico. Combinar com a inclusão existente.

Assim não é necessário escolher sequências, exigir continuidade de j na norma operatorial, nem aplicar continuidade a F não limitado. A continuidade usada é apenas a de Φ entre produtos de Hilbert.

Armadilhas de tipagem e alcance:

- **Gη é complexo; graph F é real.** Gη é o fecho da imagem da aplicação complexa a↦(Λa,π(a)η). Sua projeção deve ser ℂ-linear para gerar blocos em B(H) e um `ScalarRightAdjointPair`. `antilinearL2Graph`/`realL2Graph` são gráficos reais de mapas antilineares e não devem substituir esse Gη. O gráfico final de j(a),j(a*) não é, em geral, submódulo complexo.
- Fazer a geometria ortogonal e a soma dos quadrados em `WithLp 2 (H × H)`. `WithLp.prod_inner_apply` é a identidade de produto interno pertinente. O gráfico público `scalarRightPairGraph` está no produto usual: `WithLp.prodContinuousLinearEquiv 2 ℂ H H` transporta a topologia para ele. Essa equivalência topológica não autoriza chamar a norma usual do produto de norma euclidiana.
- A nova construção deve entregar **ambas** identidades sobre todo `scalarWeightLeftIdeal P` para o mesmo R. `ScalarRightAdjointPair` não exige Fη=ζ como campo; `scalarRightAdjointPair_maximal` prova-o. Para R=R*, pode-se construir o par com vetor e adjointVector iguais e então usar `scalarRightPairVector_of_pair`.
- A simetria usa a*b e b*a no domínio algébrico completo da estrela: ambos pertencem a nν porque nν é ideal esquerdo. `scalarWeightStar_mem_closedTomitaDomain`, `scalarClosedTomita_extends_weight_star` e `scalarTomitaAdjoint_pairing` são as pontes existentes para Fη=η. Não trocar nν pelo ideal uniforme I nem supor que a↦π(a)η seja limitado em ‖Λa‖.
- Não presumir que a densidade gaussiana em H seja graph-core de F, que K_h preserve E em todo D(F), ou que exista inversa limitada de transporte. A última costura topológica acima tampouco precisa identificar J do vetor/J do peso ou usar KMS.
- Para evitar os timeouts históricos, formular o lema de densidade⇒fecho genericamente e especializar com H,D,F,j e o ponto do gráfico explícitos. Preferir igualdade de pares e `congrArg` às reescritas que forçam expansão de `Classical.choose` nos operadores concretos.

Próximos enunciados sugeridos, **nomes de proposta, ainda sem alegação de existência Lean**: `fixed_right_pair_vectors_dense` (densidade real provada pelos blocos), `antilinear_graph_closure_of_fixed_dense` (costura genérica acima) e `scalarRightPairGraph_closure_eq_original` (igualdade final no mesmo F). Não é necessário introduzir graph-core como campo.

Consulta encerrada. Zero builds, zero revisão de arquivos novos não congelados, nenhuma alteração de fonte, memória ou parecer selado. Esta nota não move flags nem afirma inclusão inversa, KMS ou traço. Pins das interfaces lidas no artefato [source_pins.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/consulta_interfaces_graph_core_f_20260913_012637_289146/source_pins.json>).
