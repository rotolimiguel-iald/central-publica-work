# Consulta — gráfico dos pares, Fix S e blocos

2026-09-13T06:28:49-03:00. **[DERIVED — consulta matemática e leitura de interfaces; zero compilação, zero novo alvo aceito]**.
Mãe lida: `square_resolvent_custody.json`, SHA256 `52a83cf4d0f6b3927ab8ef706153f325005ce97e0f11400d7ac3b583d4ca04c5`. A verificação autoral existente aponta esse mesmo pin; não foi reexecutada. Pareceres/memórias/fontes permanecem intocados.

A rota proposta é válida. Fixe H=H_I original, E=scalarPairedRightAlgebra P, j=scalarRightPairVector P, η∈D(S) com Sη=η, e fη(a)=a.val η. O gráfico novo é G=complexGraphClosure j fη; não é o gráfico antigo sobre o ideal esquerdo do peso e Fix F.

**Simetria: produto e ordem corretos.** Com produto interno antilinear na primeira variável:

    ⟨aη,j(b)⟩ = ⟨η,a* j(b)⟩ = ⟨η,j(a* b)⟩
                = ⟨j(b* a),η⟩ = ⟨b* j(a),η⟩ = ⟨j(a),bη⟩.

A passagem central usa F j(a* b)=j((a* b)*)=j(b* a) e ⟨F x,η⟩=⟨η,x⟩ para TODO x∈D(F), fornecido por Sη=η. Interfaces reais: [scalarRightPairVector_mul](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarRightPairVector.lean:79>), [scalarRightPairVector_original_adjoint](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarRightPairVector.lean:89>) e a direção `.mp` de [scalarClosedTomita_bidual_graph_iff](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarTomitaBidual.lean:63>). Basta a identidade de pareamento já existente; não há hipótese KMS, identificação de J auxiliar ou novo domínio máximo.

**As três ações estão certas.** A definição lida fixa B como bloco superior direito: Π=G.starProjection=[A B; B* D]. Ponha x=j(a), y=aη. Pertinência ao gráfico dá Π(x,y)=(x,y); a simetria dá Π(y,−x)=0. Lendo as coordenadas:

    Bx=Ay,       By=(I−A)x,       B*y=Dx.

Logo B j(a)=A(aη), B(aη)=(I−A)j(a), B*(aη)=D j(a), SEM [A,B]=0. A quarta relação útil é B* j(a)=(I−D)(aη). A primeira já tem o genérico [hilbertBlockB_from_rotated](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/HilbertProjectionBlocks.lean:88>); a quarta, [hilbertBlockBadjoint_from_fixed](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/HilbertProjectionBlocks.lean:97>). As duas outras exigem apenas os análogos de coordenada: aplicar inl.adjoint à equação fixa e inr.adjoint à equação rotacionada. `complexGraphEmbedding_mem`, `Submodule.starProjection_eq_self_iff`, `complexGraphClosure_projection_rotated`, `hilbertPairInl_adjoint_apply` e `hilbertPairInr_adjoint_apply` dão as interfaces necessárias. Não trocar B por B*.

**Ordem e identidades: rota genérica econômica.**

- `Submodule.isIdempotentElem_starProjection`, `starProjection_isSymmetric` e `LinearMap.IsSymmetric.clm_adjoint_eq` fornecem Π²=Π=Π*. `ContinuousLinearMap.IsIdempotentElem.isPositive_iff_isSelfAdjoint` dá positividade de Π; repetir em Gᗮ dá a de I−Π por `Submodule.starProjection_orthogonal`.
- `ContinuousLinearMap.IsPositive.adjoint_conj`, aplicado à inserção i₁, dá A=i₁*Πi₁≥0 e I−A=i₁*(I−Π)i₁≥0; `nonneg_iff_isPositive` e `le_def` convertem à ordem real de operadores. Idem D. Reduzir i₁*i₁=I pelas fórmulas de adjunto existentes. Esta rota dispensa calcular uma desigualdade de números complexos; se usar energia real, a interface correta é `ContinuousLinearMap.isPositive_def'`, mantendo IsSelfAdjoint explícito.
- Das coordenadas de Π²=Π: A²+BB*=A e AB+BD=B. Reorganizar dá BB*=A(I−A), BD=(I−A)B. É álgebra não comutativa; `ring` com hipótese tácita de comutatividade seria incorreto. A aplicação/extensão vetorial e distributividade bastam.
- Injetividade de A vem de Re⟨v,Av⟩=‖Π i₁v‖² e [complexGraph_projection_inl_ne_zero](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/HilbertProjectionBlocks.lean:153>) com `scalarRightPairVector_denseRange`. A fórmula de energia pode ser extraída do argumento já existente de `hilbertProjectionWitness_energy`. **Injetividade não fornece uma cota inferior uniforme**: A≥c⁻¹I continua uma obrigação posterior.

**Por que os blocos pertencem à MESMA π(N).** Para t∈E, use b=t*a na hipótese de `complexGraphClosure_projection_commutes`; j(t*a)=t j(a) e fη(t*a)=t fη(a). A segunda hipótese usa star t∈E e o adjunto concreto do operador t.val. Não exige unidade em E. Assim `hilbertBlockA_commutes`, `hilbertBlockB_commutes`, `hilbertBlockD_commutes` colocam os blocos em E′.

A ponte E′=π(N) pode ser um pequeno lema novo, sem TT:

    generatedAlgebra E = E′′ = scalarGNSCommutant = M′,
    E′ = E′′′ = (M′)′ = M,
    M := scalarGNSVonNeumann P = range(scalarGNSRepresentation P).

As igualdades não são nominais: usar [scalarPairedRightAlgebra_generated_eq_commutant](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarPairedRightAlgebra.lean:124>), definição de `scalarGNSCommutant`, [scalarGNSVonNeumann_coe](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarGNSVonNeumann.lean:148>) e `VonNeumannAlgebra.centralizer_centralizer`. Atenção: `generatedAlgebra` usa **StarSubalgebra.centralizer**; `StarSubalgebra.coe_centralizer_centralizer` produz (E∪star E)′′. Simplificar primeiro por `StarMemClass.star_coe_eq`/`Set.union_self` (E é fechado por estrela), e só então aplicar `Set.centralizer_centralizer_centralizer`. Para extrair o operador-base representado, usar [mem_scalarGNSVonNeumann_iff](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/ScalarGNSVonNeumann.lean:139>). Nada disso usa ou resolve Jπ(N)J=π(N)′.

**Próximos enunciados delimitados:** simetria do novo fη; pacote genérico de ordem/identidades e das duas ações ainda não encapsuladas; lema E′=M; aplicação dos blocos em M. A cota inferior, os dois vetores ponderados no grafo de S, o multiplicador limitado e a inclusão inversa por J permanecem fora desta consulta. Nenhuma fonte nova ainda em autoria foi certificada.

Pins e arquivos efetivamente consultados: `CONSULTA_BLOCOS_PARES_FIXS.pins.json`. Uma busca inicial por `TGLExt/GeneratedAlgebra.lean` falhou; a definição real foi localizada em `TGLV350/RegularGeneratedAlgebra.lean`. Nomes citados acima provêm dos arquivos lidos, não de um novo #check/compile.
