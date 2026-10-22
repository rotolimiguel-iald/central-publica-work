[REAL — A1 PARCIAL: contrato e recusas compilados; construção do traço canônico ABERTA]

# Entrega 011 · A1 — contrato forte e distinção entre peso dual e traço

Responde à ORDEM_011. A ficha de aproveitamento foi escrita antes do módulo Lean.
Este marco não encerra A1(b), não inicia A2–A7 e não move o gate canônico.

## Resultado exato

`TGLV351.RegularCoreTraceData P` exige, no cone positivo da MESMA
`regularCoreAlgebra P`, valor ENNReal, zero, adição, homogeneidade positiva,
monotonia, fidelidade, normalidade por IsLUB, semifinitude por minorantes positivos
finitos, τ(a*a)=τ(aa*) e escala pela MESMA `regularDualAction P`.

- `legacy_zero_trace_cannot_supply`: qualquer transporte do traço zero legado
  falha nesse contrato. Não supõe identificação inexistente entre álgebras.
- `scalarDualWeight_not_trace_provider`: o peso dual ν não pode fornecer
  diretamente τ. A lei existente ν(θ_s A)=ν(A), aplicada à média quadrática cujo
  valor é exatamente 1, contradiz a escala exigida τ(θ_1 A)=e⁻¹τ(A).
- Os fornecedores do cone, da álgebra, da ação dual, da fidelidade, da
  normalidade, da densidade e da integral da média foram reutilizados.

As recusas são paredes contra dois fornecedores incorretos; não são uma parede
contra a existência do traço canônico. O novo contrato não afirma canonicalidade
pela mera escala: falta construir a perturbação do peso fixado pelo inverso do
gerador e demonstrar suas propriedades.

## Aceitação da ordem

| Critério | Estado | Evidência/limite |
|---|---|---|
| A1(a) contrato fortalecido que recusa o zero legado | PAGO | termo e recusa compilados |
| A1(b) habitante para todo SiteProfile ou impossibilidade tipada | NÃO PAGO | nenhuma das duas alternativas demonstrada |
| A1(c) #print axioms restrito ao trio | PAGO neste módulo | 11 declarações; rc0 sem avisos; auditoria estrita |

`LACUNAS_A1.md` nomeia os antecedentes, tipos matemáticos e conclusões das pontes
restantes: identificação geral do peso dual; sua implementação modular;
gerador positivo afiliado; perturbação de Pedersen–Takesaki com escala dual.
A igualdade do fecho do grafo de Tomita do peso completo já está paga e foi
relocalizada; não voltará a ser cobrada. Os módulos DEV de energia não fornecem
por si esse traço e não foram incorporados.

A ponte posterior a `ThreeLocksCoreData` também deve tratar a diferença entre
o traço no cone positivo e o campo legado `Core → ENNReal`. Não foi fabricado
um adaptador para produtos arbitrários.

## Verificação e falhas preservadas

Lean 4.31.0, pin de mathlib do lake-manifest; 375 pares fonte/objeto importados
conferidos e copiados. Auditoria do módulo: oito controles aprovados. A prova
numérica adulterada 1→2 falhou no Lean, e o auditor a recusou. Relatórios sem
declaração, duplicados, com axioma extra ou rc não zero também são recusados.

Tentativas anteriores foram preservadas: import não localizado; erro de
parênteses com emissão de sorryAx; compilação válida com avisos; primeira sonda
negativa fora da raiz do Lean. Esta última é falha de ambiente e não foi contada
como recusa matemática. A execução aceita e a sonda negativa correta estão
individualizadas em AUDITORIA_A1.json.

O programa copiado permanece byte a byte igual à v351 de entrada. Não se alterou
Python do um.py, nenhum arquivo canônico, experimento, selo, Atlas ou memória
central. A rodada integral anterior não é apresentada como rodada deste módulo;
esta entrega não fez novo runtime integral do monólito.

## Reprodução na bancada existente

```powershell
Set-Location -LiteralPath 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO'
& 'C:\Python314\python.exe' -X utf8 -B .\compile_a1.py
& 'C:\Python314\python.exe' -X utf8 -B .\compile_a1.py .\probes\A1FalseValue.lean
# A segunda compilação deve retornar código 1 por erro matemático deliberado.
& 'C:\Python314\python.exe' -X utf8 -B .\audit_a1.py
```

## Artefatos e custódia

- [REAPROVEITAMENTO_A1.md](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\REAPROVEITAMENTO_A1.md>) — SHA256 `ed59d7894c910785084f717abe7a44753cbd93bd31af665dddf00791e3092cc8`.
- [REAPROVEITAMENTO_A1.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\REAPROVEITAMENTO_A1.json>) — SHA256 `17013f19d849b5db20dd96e7bf61fb490ba5d2db8c758041a5c036acde3cd327`.
- [ADENDO_REAPROVEITAMENTO_A1.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\ADENDO_REAPROVEITAMENTO_A1.json>) — SHA256 `c1e79521a1fd5f646064f5456813f565eee2561b15d37bebac1a7a4358da084e`.
- [LACUNAS_A1.md](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\LACUNAS_A1.md>) — SHA256 `cf0ef3264d91c8033a399851407ca8b5f08deef63b850a2fcf62b2fc56ab581c`.
- [AUDITORIA_A1.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\AUDITORIA_A1.json>) — SHA256 `4ac68cd343edd3aa1d27cefff660c9e8fb37ba5a9c0894fa09a9dc465f8acd3c`.
- [BASE_E_FONTES.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\BASE_E_FONTES.json>) — SHA256 `778d47b54599caef3be54dc0e798f34c6408f53a065193f7be3075d522a5769b`.
- [DEPENDENCIAS_A1.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\DEPENDENCIAS_A1.json>) — SHA256 `05cb828fef6b96f431f1c7bc426092a6de930b65c77aae358dd9abc51f09e7c9`.
- [BUSCAS_A1.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\BUSCAS_A1.json>) — SHA256 `d5b5ade4450c3df73ca9efcdda1ae005862f5f0debb39802cfb494e8beea7475`.
- [OUTRAS_BANCADAS_HASHES.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\OUTRAS_BANCADAS_HASHES.json>) — SHA256 `5b826d9f8cfe3a92e34a1e6d83476617c3d5c3138937039526b90444d1c1fca2`.
- [compile_a1.py](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\compile_a1.py>) — SHA256 `781b91f62c789b3db624b945375f7703cfae98ff406d53722908a86f96e10570`.
- [copy_dependency_objects.py](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\copy_dependency_objects.py>) — SHA256 `4c2a2bf12a9d22c95ee4ddec738b3cc8e782febe4367632016d957ce0ddba443`.
- [audit_a1.py](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\audit_a1.py>) — SHA256 `9d43c2b9c708d5ba03f25aacbbe5c51cd95fc0c09908fa0d11b05d6b0e9ec4ea`.
- [V351RegularCoreTraceContract.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351RegularCoreTraceContract.lean>) — SHA256 `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0`.
- [REVIEW_A1_CONTRATO_FINAL.md](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\REVIEW_A1_CONTRATO_FINAL.md>) — SHA256 `b95220a6440e36aa40cff2557a264449fc5f3f167cf5fba6069876d4f26c525a`.
- [run.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\attempts\20260914_081118_098129\run.json>) — SHA256 `7e6b67262ca7a424fb046e22cbd93eacefb6425cd5aab0e3f2f2375c22806ec2`.
- [stdout.txt](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\attempts\20260914_081118_098129\stdout.txt>) — SHA256 `a5b9992c2d4662d54511e958fc3213d2e061faf5771d86c83123213112b008d1`.
- [run.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\attempts\20260914_081310_479904\run.json>) — SHA256 `80dbd16a219c6ea6a61913a386b098398ef61997e3fc38fd5220c36ce4d8c9bd`.
- [stdout.txt](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\attempts\20260914_081310_479904\stdout.txt>) — SHA256 `e81c4b2c8cfd9dbbdc6a57453d633bffe2fd2149f2654a613c9e122c80335ef2`.
- [A1FalseValue.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\probes\A1FalseValue.lean>) — SHA256 `12053ed67718333e9f66a382b312b0e2975e0b0454c40f4fa1e926ab474bb1d3`.
- [lean-toolchain](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\lean-toolchain>) — SHA256 `efac0b94923b2d8b6840cd35be9177ad0fc5ab2332f4f4311c98712cee92fdee`.
- [lake-manifest.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\lake-manifest.json>) — SHA256 `31a94eb76a8370ae8d75999ccec510f1ef7b994e369beebee2a3ea0088eee235`.
- [search_acervo.txt](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\search_acervo.txt>) — SHA256 `1c8e2848608da28946f9f901174cbccd87a6669507f848c5ce06c6580877b856`.
- [search_acervo_refined.txt](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\search_acervo_refined.txt>) — SHA256 `ed2254853f2a49b39156b1e81cd9cd9c40ca4de3037d19a9da760b9062b88b75`.
- [search_deliveries.txt](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\search_deliveries.txt>) — SHA256 `449ade206974e78cdb2a3f68caed8c264a317e351ff046e4c3179159ecded6b8`.
- [search_embedded.txt](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\search_embedded.txt>) — SHA256 `043d20f234a1f6edeab766686a45726fc6e105e430f1fb6a0269b7e7d64fb28f`.
- [search_mathlib.txt](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\search_mathlib.txt>) — SHA256 `4178b5ee623c4d676b5199f95cfa9cb854eb0bed3e3e5f2d9edff805b7988856`.
- [search_mathlib_full_named_bridges.txt](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\search_mathlib_full_named_bridges.txt>) — SHA256 `e5ab2805c588a2315a80dc04fbe06a7df5aea13b4a0f2a7a3da781267997556e`.
- [search_notes.txt](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\search_notes.txt>) — SHA256 `564e1d7f090c5f331d6a6553a7c532606bad1c63f8bb42aa8f03ef760978bc77`.
- [search_other_workshops.txt](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\search_other_workshops.txt>) — SHA256 `e01d62c0a152baab2af0818daee26f3fb980fb29ea3b8e885d041086744919c4`.
- [A_PROVA_DA_QG_TGL_arvore.md](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\base_v351\A_PROVA_DA_QG_TGL_arvore.md>) — SHA256 `e820f614ca904191e18ccf5c2d14a70a7d248caee21f6bcab191f25b6c304b77`.
- [HANDOFF_v351_A_OITAVA_CLAUSULA.md](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\base_v351\HANDOFF_v351_A_OITAVA_CLAUSULA.md>) — SHA256 `4ac06e634b0513f6d8f67320a7d57854536e53b11147fb74146284c16f1f7c3f`.
- [tgl_kernel_proof_manifest.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\base_v351\tgl_kernel_proof_manifest.json>) — SHA256 `79ffa986c76bb43fd093aa14d6f3b32709946c75c09cc42374c825922ac997f8`.
- [um_absoluto.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\base_v351\um_absoluto.json>) — SHA256 `575e911c50ea8427084f72fcedbe43bf7f41ff16844e829655e3fe4c100a7050`.
- [um_absoluto_selo.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\base_v351\um_absoluto_selo.json>) — SHA256 `3b8e3d42dc170f68215eaa73eb3f44fe4c4cf6f783b2cb72cc30f66eb161140b`.
- [audit_20260914_082410_187996.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\audits\audit_20260914_082410_187996.json>) — SHA256 `6b92fc56fd8b5fa004332062615bf7daf690e01ecbda7ad5c10cc793967ba5c5`.
- [verification.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\a1_independent_20260914_081736_089694\verification.json>) — SHA256 `a2b1d7a177a05d49e8693dbb0fc3a682467c83117a1373e5fae4c0499f01bdd8`.
- [compilation.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\a1_independent_20260914_081700_584120\compilation.json>) — SHA256 `618386f627ec5d746da8f9e89499f6f62a122e486c28c46a128628908b1cd8ee`.
- [compilation.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\a1_independent_20260914_081736_089694\compilation.json>) — SHA256 `2dcf853e8f0d0f0cb766338878f3ba56a16db4a7e99c1dff5cc8507bbc8fd592`.
- [V351RegularCoreTraceContract.olean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\build\TGLExt\V351RegularCoreTraceContract.olean>) — SHA256 `057225cc3d7aace6ff789cb7dce81b0209b054bcc938584b0763250e6aeecb56`.

[Manifesto completo](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\MANIFESTO_A1.json>) — SHA256 `f8ba57dc9e9b219db302e819b06e5e859a287f430e99c4104a5f0c61b0d8f29c`.

## Ficha de aproveitamento anexada

[REAL — ficha de reaproveitamento por leitura; nenhuma nova prova declarada]

# A1 — traço no core regular da mesma torre

Para todo P:SiteProfile, τ:PositiveCoreInput P→ENNReal com zero, adição, homogeneidade NNReal, monotonia, fidelidade, normalidade IsLUB, semifinitude por supremo de minorantes positivos finitos, τ(a*a)=τ(aa*) e τ(regularDualAction P s A)=ofReal(exp(-s))*τ(A). Canonicalidade exige adicionalmente τ=(ν)_(h^-1), h^(it)=regularUnitary P t, não apenas escolher uma normalização arbitrária.

NOVO: contrato forte e suas recusas; REUSAR: cone, álgebra, ação, normalidade/ideal/peso existentes. ADAPTAR: ponte modular/perturbação do peso para τ. Não construir nova teoria genérica sem necessidade.

## Fornecedores e tipos

### structure ContinuousCoreData — ADAPTAR

[ModularRealization.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGL\ModularRealization.lean:68>) · SHA256 `17e344c8b7b40ae8f2ed4910c3b5e4712cc8ba84dd53e05d10a94f0009295348`

O contrato legado recebe Core→ENNReal sem cone positivo, fidelidade, normalidade ou semifinitude. O novo tipo restringirá o peso a PositiveCoreInput P; não se afirmará conversão automática ao legado.

```lean
structure ContinuousCoreData (W : TGLSpecificAQFTWitness) (D : WedgeModularData W) where
```

### structure ThreeLocksCoreData — CONSUMIDOR

[ModularRealization.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGL\ModularRealization.lean:100>) · SHA256 `17e344c8b7b40ae8f2ed4910c3b5e4712cc8ba84dd53e05d10a94f0009295348`

Consumidor posterior A2: PF_trace_pos e PF_trace_finite precisam do mesmo traço.

```lean
structure ThreeLocksCoreData (W : TGLSpecificAQFTWitness) (D : WedgeModularData W)
    (C : ContinuousCoreData W D) where
```

### def zeroTraceLegacyCore — REUSAR

[V350CoreContractCounterexample.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350CoreContractCounterexample.lean:12>) · SHA256 `1aaa11d4c572c2ad3c0c80a54322247233b64e6e16e28710cd4ccc0d3524de0e`

Sonda negativa: refutar a restrição zero no novo contrato. A prova antiga só refuta ThreeLocks, não fortalece o core.

```lean
def zeroTraceLegacyCore (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness)
    (D : WedgeModularData W) : ContinuousCoreData W D where
```

### def regularCoreAlgebra — REUSAR

[V350RegularGeneratedAlgebra.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularGeneratedAlgebra.lean:50>) · SHA256 `252b0fa3d5e37c42827efccfc26a555db80ac5c20a6f94269060ce2b3dcb5f71`

Mesma álgebra concreta; não reconstruir produto gerado.

```lean
def regularCoreAlgebra (P : SiteProfile) : VonNeumannAlgebra (RegularHilbert (TowerHilbert P)) :=
```

### def regularDualAction — REUSAR

[V350RegularDualAction.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularDualAction.lean:76>) · SHA256 `e7c3628d969c0dae2a971c156200acb88f6bf4286a9c648a2ad3da08c468040c`

Mesma ação dual concreta; a operação no cone usa regularDualAction_apply e dualAmbient_nonneg.

```lean
def regularDualAction (P : SiteProfile) (s : ℝ) :
    (regularCoreAlgebra P).toStarSubalgebra ≃⋆ₐ[ℂ] (regularCoreAlgebra P).toStarSubalgebra :=
```

### theorem regularCoreEmbedding_preserves_positive_directed_isLUB — REUSAR

[V350RegularNormality.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularNormality.lean:127>) · SHA256 `bcd49e92800bf99d7770bb9969879be02a9768f129ce842ae2f39cefaca3cc0a`

Normalidade da inclusão já paga; não é a normalidade do traço.

```lean
theorem regularCoreEmbedding_preserves_positive_directed_isLUB (P : SiteProfile)
    (S : Set (theFactorObject P).toStarSubalgebra)
    (B : (theFactorObject P).toStarSubalgebra)
    (hne : S.Nonempty) (hdir : DirectedOn (· ≤ ·) S)
    (hpos : ∀ A ∈ S, 0 ≤ A) (hB : IsLUB S B) :
    IsLUB (regularCoreEmbedding P '' S) (regularCoreEmbedding P B) := by
```

### abbrev PositiveCoreInput — REUSAR

[V350DualFixedWeightLaws.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualFixedWeightLaws.lean:15>) · SHA256 `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`

Cone positivo exato, adição e escala já definidos neste arquivo.

```lean
abbrev PositiveCoreInput (P : TGLExt.SiteProfile) :=
```

### def scalarDualWeight — REUSAR

[V350ScalarDualWeight.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:15>) · SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

Peso ν concreto de partida. Não casa com traço: invariância dual não é escala e^-s.

```lean
def scalarDualWeight (P : SiteProfile) (A : PositiveCoreInput P) : ℝ≥0∞ :=
```

### theorem scalarDualWeight_normal — REUSAR

[V350ScalarDualWeight.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:46>) · SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

Normalidade por IsLUB interno já provada para ν; preservação na perturbação ainda exigida.

```lean
theorem scalarDualWeight_normal (P : SiteProfile)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    scalarDualWeight P ⟨S.val,S.property,positive_internal_isLUB_nonneg P A S hpos hS⟩ =
      ⨆ i, scalarDualWeight P ⟨(A i).val,(A i).property,hpos i⟩ :=
```

### theorem scalarDualWeight_faithful — REUSAR

[V350ScalarDualWeight.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:36>) · SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

Fidelidade já provada para ν.

```lean
theorem scalarDualWeight_faithful (P : SiteProfile) (A : PositiveCoreInput P) :
    scalarDualWeight P A = 0 ↔ A = PositiveCoreInput.zero P := by
```

### theorem scalarDualWeight_square_finite_strong_density — REUSAR

[V350ScalarDualWeight.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:66>) · SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

Ideal finito fortemente denso de ν. Não identificar isso por rfl com semifinitude por minorantes positivos de τ.

```lean
theorem scalarDualWeight_square_finite_strong_density (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → dualQuadraticIntegral
      (star (A.val * regularAverage P h) * (A.val * regularAverage P h)) (regularVacuum P) < ⊤) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 (A.val v))) := by
```

### theorem regularScalarWeightCertificate — REUSAR

[V350RegularScalarWeightCertificate.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularScalarWeightCertificate.lean:58>) · SHA256 `f7c1786097ce619e7cbe7f35269147b8bde95793de9b0b5a09bf98627a2db6c0`

Agrega leis já provadas. Explicitamente não fornece KMS nem traço.

```lean
theorem regularScalarWeightCertificate (P : SiteProfile) :
    RegularScalarWeightCertificate.{u} P where
```

### theorem dualQuadraticIntegral_dual_invariant — REUSAR

[V350DualWeightForm.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualWeightForm.lean:87>) · SHA256 `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`

Ponte para demonstrar que renomear ν como τ falha na escala dual.

```lean
theorem dualQuadraticIntegral_dual_invariant (r : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral (dualAmbient r A) v = dualQuadraticIntegral A v := by
```

### theorem regularAverage_dualQuadraticIntegral — REUSAR

[V350RegularFiniteWeight.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularFiniteWeight.lean:108>) · SHA256 `39e417e41adf90a2d575b6a93f8a35ccd2d816a445097745fd3c540ab240baf6`

Valor finito explícito sobre quadrado de média: testemunha contra troca de ν por τ.

```lean
theorem regularAverage_dualQuadraticIntegral (P : TGLExt.SiteProfile) (h : ℝ) (hh : 0 < h)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    dualQuadraticIntegral (star (regularAverage P h) * regularAverage P h) v =
      ENNReal.ofReal (h⁻¹ * ‖v‖ ^ 2) := by
```

### theorem matrix_trace_is_faithful_weight — NAO_CASA

[SemifiniteSeed.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\SemifiniteSeed.lean:115>) · SHA256 `9e91547595c6fdfa37c5d9b786bf3b1e5b774fa90fa4ff0a01a463a775e77dc5`

Matrizes reais finitas; não fornece N(P)+→ENNReal nem escala dual.

```lean
theorem matrix_trace_is_faithful_weight :
    (∀ A : Matrix n n ℝ, A.PosSemidef → 0 ≤ A.trace) ∧
      (∀ A : Matrix n n ℝ, A.PosSemidef → (A.trace = 0 ↔ A = 0)) ∧
      (∀ A B : Matrix n n ℝ, (B - A).PosSemidef → A.trace ≤ B.trace) :=
```

### def dimTraceData — NAO_CASA

[DimensionTrace.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\DimensionTrace.lean:51>) · SHA256 `cdadc9fdf8ed641c7c260e0a5450577b4e190b102a055dc0d2c49e71f49338ea`

Reticulado de subespaços reais finitos; tipo distinto do cone positivo de N(P).

```lean
def dimTraceData (n : Type) [Fintype n] :
    SemifiniteTraceData (Submodule ℝ (n → ℝ)) where
```

### theorem opWeight_star_mul_self_comm — NAO_CASA

[BreuerTrace.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\BreuerTrace.lean:104>) · SHA256 `4a667f41d3b7bb1d6a3a02fa46f43372c2a3e4bef30c98acde05294f5c46b496`

Traço padrão de B(ellTwo), não o traço semifinito de N(P) com ação dual prescrita.

```lean
theorem opWeight_star_mul_self_comm (a : ellTwo →L[ℂ] ellTwo) :
    opWeight (ContinuousLinearMap.adjoint a * a)
      = opWeight (a * ContinuousLinearMap.adjoint a) := by
```

### structure SemifiniteTraceData — NAO_CASA

[LocalBreuerGap.lean](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\LocalBreuerGap.lean:72>) · SHA256 `8ec73c7d9e703d6c775f53351a784ab98b27ad2dd3d253b79a3d34992e0d5d3d`

Peso fiel/monótono em reticulado: nome não fornece normalidade e semifinitude no core.

```lean
structure SemifiniteTraceData (L : Type) [Lattice L] [BoundedOrder L] where
```

## Consumidor e alcance

A1 fornece o traço para A2, que fornece o core/ThreeLocks compatíveis a A5. A bandeira qgf_continuous_modular_realization_constructed não vira True por esta ficha. Localizadores exatos de todas as ocorrências estão no JSON. O gate principal pago permanece intacto.

## Busca e limites

922 arquivos embutidos (918 Lean), buscas registradas em BUSCAS_A1.json; 625 caminhos correspondentes em outras bancadas, 7 hashes distintos.

- A busca inicial do acervo foi truncada em 50 ocorrências históricas; exige refinamento Pedersen-Takesaki, não prova ausência.

- Bancada TOE: único arquivo por padrão foi FrontierCertificate.lean, contrato não construtor de traço.

- Mathlib Analysis: busca dos nomes dá subespaços padrão e homônimos; não identifica implementação do teorema de perturbação.

- DEV não reativado: nenhum módulo suspenso fornece τ no cone positivo com escala dual.


Contrato compilado não é habitante. Falha de provedor não é impossibilidade matemática. Registrar precisamente o lema faltante e manter b NÃO PAGO se não houver construção nem parede contra sua existência.


Convenção: Λ_t=h^(it), L=log h desloca L−s; K=−log h desloca K+s. O traço é a perturbação ν_(h^-1); não trocar sinais nem inferir normalização da lei de escala.
