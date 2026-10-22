2026-09-15T00:36:52.822755-03:00

**A1_AVERAGE_POLAR_RIGHT_REVIEW_ACCEPTED__FIXED_VECTORS_TRACE_OPEN**

[REAL] **Sem achados P0/P1/P2.** Módulo e auditor próprios rc0; dois tipos completos com universos, axiomas do trio. Controle negativo próprio rc1 por Type mismatch.

[REAL — tipos e objetos] regularAverage_polar_approximants recebe o mesmo P e δ>0, constrói b_n na álgebra direita existente E, norma≤1 e limites fortes b_n→eδ e b_n*→eδ*. regularAverage_mem_scalarPolarRightAlgebra conclui a pertença de eδ a E. A definição de E inclui as identidades direitas para b e b* em TODO o ideal escalar nν, com o J/GNS originais. A família aproximante exigida no fornecedor de fechamento é construída, não recebida como campo.

[REAL — partição exata] O helper average_partition traduz cada integral em [0,h] por k h usando a lei de grupo e integral_comp_add_right. sum_integral_adjacent_intervals, com μ=volume explicitado, soma os intervalos adjacentes e fornece b_N e_h=e_(N h), com normalização N⁻¹h⁻¹=(Nh)⁻¹. É uma identidade finita da integral vetorial existente, não uma afirmação assintótica de Riemann. O helper admite N=0 ou h=0 pela convenção de inverso zero; o consumidor usa N=n+1>0 e h=d_n>0.

[REAL — construção e convergência forte] b_n é a combinação finita (n+1)⁻¹Σ_{k<n+1}λ_(k d_n), d_n=δ/(n+1). Pertence a E por soma e escala dos geradores já existentes. A cota≤1 vem das normas das λ e da cardinalidade da soma. d_n tende a zero no filtro perfurado, pois δ>0. A identidade b_n e_(d_n)=eδ e a cota dão ‖b_n v−eδ v‖≤‖v−e_(d_n)v‖→0. O bound_limit local é um argumento de contração no corpo da prova, não uma quarta declaração privada/global.

[REAL — adjunto, ponto crítico] average_commutes_regular demonstra comutação da média com cada λ por transporte da integral vetorial e abelianidade da lei regular. Da soma resulta b_n e_(d_n)=e_(d_n)b_n. A prova estrelará e_(d_n)b_n=eδ, e não somente a identidade na ordem anterior: assim obtém b_n* e_(d_n)*=eδ*. Reaplica bound_limit usando ‖b_n*‖≤1 e regularAverage_star_tendsto_identity, já provado para contrações. Não usa continuidade geral de star para SOT e não afirma eδ=eδ*.

[REAL — fechamento e domínio] O primeiro uso de scalarRightAction_closed_of_bounded_strongStar recebe b_n, as duas convergências e a primeira componente da pertença b_n∈E. O segundo recebe b_n*, com o limite adjunto e star_star, além da segunda componente dessa pertença. Produz a ação para eδ e eδ* em todos A∈nν. A passagem da inscrição GNS é responsabilidade do fornecedor já aceito; não se presume continuidade forte irrestrita de Λ nem se constrói outro GNS.

[REAL — auxiliares, ficha e histórico] Três helpers privados globais: average_commutes_regular, average_partition e finite_regular_average_norm, auditados transitivamente pelos dois alvos. Nove fornecedores da ficha relidos por linha e pin. O excerto operatorIntegral_commutes está truncado no binder; o tipo completo foi relido, e o adendo explica o adaptador concreto via integral vetorial. A ficha antecede o código; o adendo declara posterioridade ao DEV. Dois DEV rc1 preservados e excluídos: timeouts/coerções/ext/rewrite e depois medida/filtro/metavariáveis. As três versões usam os mesmos limites 2200000/200000; o final rc0 está limpo.

[REAL — controle] BadAverageMembershipIsSelfAdjoint foi reproduzido em V/ReviewControls com cópia de bytes e objetos próprios. A tentativa de usar pertença em E como prova de eδ*=eδ retorna rc1 por Type mismatch, com imports funcionais. O controle autoral também foi relido/pinado. Essa recusa prova apenas a inadequação do termo adulterado, não uma classificação de todas as médias por auto-adjunção.

[REAL — proveniência] 699 objetos próprios preservados; 2 novos (alvo+auditor), total 701. Nenhum fornecedor antigo recompilado, nenhum objeto K/DEV herdado. Run 41.531 s; negativo 21.701 s. Zero avisos do alvo/auditor; 178 mensagens de fornecedores herdadas discriminadas. all_accepted_builds_exit_zero=True; all_attempts_exit_zero=False inclui o negativo esperado. LEAN_PATH dos traces restrito a V/pacotes.

| Artefato | SHA256 lido |
|---|---|
| Fonte K=snapshot=V | 9a982e09a318e7c306c20a9c5baf0d07a6354b34d3cf2e6cc3cf168968f334cc |
| .olean próprio | c8e2ec1647c3a69fd5e9586dbee4363a072e30c2a1b6bbc97cd064607dff7572 |
| .olean autoral, só comparação | c8e2ec1647c3a69fd5e9586dbee4363a072e30c2a1b6bbc97cd064607dff7572 |

Igualdade binária medida: True.

[OPEN] Aceite29: dois teoremas públicos, três helpers privados globais e zero defs; bound_limit é prova local incluída transitivamente. Pertença da média e da sua estrela na álgebra direita original. Não declara auto-adjunção da média, vetor fixo S/F, igualdade dos implementadores, Q ou tracialidade. 19 V351 são subconjunto das 940 entradas da base (937 Lean e três configurações), não 959 arquivos; pins relidos. Somente esta pasta e novas saídas em V. Fontes K/OLD/V353, memórias, monólito, writers e pareceres anteriores preservados.

Tipos lidos:

~~~lean
theorem regularAverage_polar_approximants (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    ∃ b : ℕ → (regularCoreAlgebra P).toStarSubalgebra,
      (∀ n, b n ∈ scalarPolarRightAlgebra P) ∧
      (∀ n, ‖(b n).val‖ ≤ 1) ∧
      (∀ v, Tendsto (fun n => (b n).val v) atTop (𝓝 (regularAverage P δ v))) ∧
      (∀ v, Tendsto (fun n => (star (b n)).val v) atTop
        (𝓝 (star (regularAverage P δ) v)))
~~~

Axiomas próprios: propext, Classical.choice, Quot.sound.

~~~lean
theorem regularAverage_mem_scalarPolarRightAlgebra (P : SiteProfile)
    (δ : ℝ) (hδ : 0 < δ) :
    (⟨regularAverage P δ,regularAverage_mem P δ⟩ :
      (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
~~~

Axiomas próprios: propext, Classical.choice, Quot.sound.

Evidências:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\compilation.json>) — SHA256 84479368c983b2e712d52c71dd15157bfda87b1005426c88eaa494f3ef0bcace.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\independent_20260915_003308_093413\run.json>) — SHA256 a5de8e79ce0fce0bd20c5eaf4591af8235455c3350318025b5f966ba269776b0.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\independent_20260915_003308_093413\type_axiom_audit.json>) — SHA256 e6c3d69fb64320cc340e296fa3c4d7fe11860d6e8f7bcd9282bad4cde82cf121.
- [negativo próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\negative_20260915_003500_293603\run.json>) — SHA256 3a38cfb3185539120692c9d51efb5c61e5e93dd0aa793ac4ae84634d24a7bed0.
- [preservação19/940](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\preservation_19_940.json>) — SHA256 76f0a8e413b80773fca360c4a5acb7dbd211302a46b3fa2d42b745b672db0929.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\history_read.json>) — SHA256 faf46fa257a2088f9bb2dd441be697089eb3d65f316b61e50a276258a6d17d3f.
