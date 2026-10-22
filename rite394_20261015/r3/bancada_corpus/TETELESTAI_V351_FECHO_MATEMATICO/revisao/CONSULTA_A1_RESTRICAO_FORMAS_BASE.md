# A1 — restrição de formas à base e semifinitude

2026-09-14T08:42:26.825229-03:00

[DERIVED — consulta matemática por leitura; nenhum candidato implementado ou compilado.] A rota proposta é válida e, se formalizada, pagará uma parte real da identificação do peso dual **no modelo de formas**. Não entrega ainda A1(b), nem uma equivalência genérica com o cone positivo estendido/predual. ORDEM_011 e LACUNAS_A1 foram relidas; o adendo desta última mantém a/c pagos e b aberto.

**Construção e prova econômica.** Ponha H=TowerHilbert P, N=regularCoreAlgebra P, M=theFactorObject P, F=dualFixedCore P, e=testEmbeddingCLM e ι(b)=fibre(b). Para Q afiliada a F, defina matematicamente Res(Q)(v)=Q.value(e v).

1. Zero, homogeneidade complexa, paralelogramo e semicontinuidade inferior transportam pela linearidade e continuidade de e. O fornecedor é [V350UnitIntervalProjection.lean:16](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350UnitIntervalProjection.lean:16>). A isometria fixa a normalização e será usada na compatibilidade com valores limitados; mera continuidade linear já basta para transportar as quatro leis. Atenção de tipo: `ClosedPositiveForm.precompose`, em [V350PositiveFormCone.lean:49](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350PositiveFormCone.lean:49>), recebe um **endomorfismo** H→L H. Não aceita diretamente e:H→L RegularHilbert H; aqui cabe construir a estrutura com esses campos ou um transporte heterogêneo, sem hipótese nova.
2. Para todo U unitário no comutante de M, ι(U) é unitário por `fibreRepresentation` (mapa unital e estrela, [V350L2OperatorLift.lean:53](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350L2OperatorLift.lean:53>)). Para B∈F, `dualFixedCore_eq_amplified_base` escreve B=ι(b), b∈M; `fibre_mul` transporta U b=b U e prova que ι(U) comuta com B. Finalmente `fibre_testVector` dá e(Uv)=ι(U)e(v), logo Q(e(Uv))=Q(e(v)). Isso fornece a afiliação à **mesma base M**, por todos os unitários de M′; não usa o J da torre nem o J do peso.
3. `testVector` é a função constante sobre (0,1] e zero fora, **não** uma constante sobre toda a reta. O intervalo tem medida 1. Não aparece outro fator de Haar ou suposição de valores pontuais comuns de representantes L².

**Aplicação ao peso existente.** Defina prospectivamente baseDualWeight(A)=Res(dualFixedWeight(A)), para todo A∈N₊. Pelo valor de `dualFixedWeight` ([V350DualFixedWeightLaws.lean:50](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350DualFixedWeightLaws.lean:50>)),

    baseDualWeight(A)(v) = dualQuadraticIntegral(A, testVector(v)).
    baseDualWeight(A)(hOmega P) = scalarDualWeight(P,A).

A segunda igualdade decorre das definições, inclusive quando o valor é ∞, pois `regularVacuum P = testVector(hOmega P)` ([V350ScalarDualWeightFaithfulness.lean:15](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350ScalarDualWeightFaithfulness.lean:15>)). **O ganho não está nessa igualdade isolada**: está em remover a hipótese de output limitado e produzir uma forma fechada afiliada a M para cada A positivo. Já o caso limitado deve continuar dando `ofReal(Re⟨v,Dv⟩)` para o mesmo D∈M fornecido por `exists_boundedDualValue_in_base`; `fibre_testVector` e a isometria resolvem essa compatibilidade. Não usar `toReal` para transportar o caso infinito.

As leis necessárias têm caminhos diretos:

- Zero, soma, escala NNReal e ordem: aplicar a restrição às igualdades/pontos do arquivo `V350DualFixedWeightLaws`; ENNReal mantém 0·∞=0. O resultado é preservação de ordem, sem alegar reflexão de ordem para toda forma Q.
- Bimódulo: para b∈M, usar `dualFixedWeight_bimodule` com ι(b)∈F e e(bv)=ι(b)e(v). A fórmula exata é baseDualWeight(ι(b)† A ι(b))(v)=baseDualWeight(A)(bv). Não substituir b pela ação de outra representação GNS.
- Normalidade: reutilizar `regularDualForm_preserves_internal_isLUB` ([V350DualFormNormality.lean:80](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350DualFormNormality.lean:80>)) em **e(v)**. Isso dá q_S(v)=sup_i q_Ai(v) em ENNReal para cada v, com positividade, monotonia, índice dirigido não vazio e supremo interno a N. Dessa igualdade pontual segue o IsLUB no cone de formas da base. Não concluir preservação de todos os supremos de uma aplicação monótona apenas por monotonia, nem transportar cegamente um IsLUB abstrato de F para M.
- Fidelidade desta família pode vir de avaliação em hOmega e `scalarDualWeight_faithful`: se a forma de saída é zero, ν(A)=0 e A=0. Não precisa primeiro provar injetividade genérica de Res.
- O output de A=1 conserva ∞ em todo v≠0, por `dualQuadraticIntegral_one` e injetividade de e; seu domínio finito é {0}. Isso não contradiz semifinitude do peso e não autoriza eliminar o setor infinito.

**O que falta para a expressão predual.** A estrutura Lean atual guarda uma função de **vetores** e invariância por unitários do comutante; ainda não uma função aditiva/homogênea semicontínua em M*₊. Hiai distingue esses tipos na definição 8.1 e relaciona formas e operadores positivos estendidos no teorema 8.3/Apêndice A.15; a extensão de pesos é a proposição 8.4. [Fonte primária](https://arxiv.org/pdf/2004.02383).

Para fechar essa parte de `regular_scalar_weight_is_dual_weight`, falta identificar o valor obtido com um elemento m_A do cone estendido da base, de modo que m_A(ω_v)=baseDualWeight(A)(v), preservar as operações e os supremos e compatibilizar sua amplificação com a integral dual original. Então φ̄(m_A)=m_A(ω_hOmega)=ν(A). Definir φ̄ nesta única família por avaliação não demonstra, sozinho, a extensão predual pretendida nem a independência de decomposições de funcionais.

Não é necessário exigir antecipadamente um isomorfismo genérico de cones: uma representação comprovada **destes outputs**, por exemplo por aproximantes positivos limitados crescentes D_n∈M cuja avaliação converge para q_A, já permitiria definir m_A(ψ)=sup_n ψ(D_n) e provar as compatibilidades. Essa aproximação/identificação não está fornecida pela restrição isolada. A existência de `fixedBaseEquiv` para operadores limitados não a implica automaticamente. Não há necessidade de refazer o GNS ou o fecho do S já identificados.

**Semifinitude: a ressalva é correta e substantiva.** Para peso normal não tracial, a definição usual admite n_φ fracamente denso; não exige a fórmula de todos os minorantes finitos de cada A. Conferido em Hiai, definição 7.1; para peso operatorial, definição 8.5. [Fonte primária](https://arxiv.org/pdf/2004.02383).

[DERIVED — contraexemplo analítico, não novo Lean.] Em B(ℓ²(ℕ≥1)), seja φ(X)=Σ_n n²⟨e_n,Xe_n⟩ para X≥0. É normal e fiel; os cortes p_k sobre as primeiras k coordenadas satisfazem φ(p_k)<∞ e p_k↑1, assegurando semifinitude usual. Tome v_n=c/n com ‖v‖=1 e p a projeção sobre ℂv. Temos φ(p)=Σ_n c²=∞. Todo 0≤b≤p é b=t p, 0≤t≤1; se φ(b)<∞, então t=0. Portanto

    sup{φ(b) : 0≤b≤p, φ(b)<∞} = 0 ≠ φ(p).

Logo seria uma exigência indevida impor esse campo do **contrato tracial** ao fornecedor ν antes da perturbação. Para traço normal semifinito a aproximação por minorantes finitos é adequada; não há motivo para enfraquecer o contrato final de τ.

No caso concreto, já há `scalarWeightLeftIdeal = n_ν`, inclusão do ideal uniforme nesse domínio ([V350ScalarWeightDomain.lean:50](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350ScalarWeightDomain.lean:50>)) e `scalarDualWeight_square_finite_strong_density` ([V350ScalarDualWeight.lean:66](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V350ScalarDualWeight.lean:66>)). As médias são contrações (`regularAverage_norm_le_one`), portanto A·average_h é uniformemente limitado e converge fortemente para A. Isso oferece a ponte concreta à densidade fraca/ultrafraca do domínio, conforme a topologia escolhida na futura interface; não requer I=n_ν nem a fórmula de minorantes para ν. O fornecedor `finiteBaseValues_strong_approximation` faz o papel análogo para outputs operatoriais limitados. No Lean, ainda é preciso formular/ligar a noção de semifinitude usada pelo consumidor, não decretar que ela falta matematicamente nem cobrar uma condição tracial extra.

**Próximo pacote delimitado sugerido:** transporte de forma e afiliação; leis de restrição; baseDualWeight e valor no vácuo; compatibilidade com output limitado; bimódulo; igualdade pontual para supremos internos e IsLUB correspondente. Nomes prospectivos, não declarações compiladas. Nenhum obstáculo matemático concreto encontrado nessa proposta. Existência do traço/perturbação e A1(b) permanecem abertas; nenhum gate é alterado por esta consulta.

**Proveniência da leitura (SHA-256, medidos agora):**

- `V350DualClosedForm.lean`: `69a47c01fc1a366a61b871b86e1d7114e43e865b025a04cd57918f09ed7c5be7`.
- `V350PositiveFormCone.lean`: `cee6510b0cd71261988bae68692d52b2a6a6270261ccd3a8e892ca625f49181d`.
- `V350UnitIntervalProjection.lean`: `60b0cf134b9db7b6fbd286dd2b039452a2f7420a2bf2ababbc5240568b6343b2`.
- `V350L2OperatorLift.lean`: `bbdf07f64bc1abdfb50fed8420911c868a11cc6c8036b6f06167f021a1db7465`.
- `V350FixedCoreBaseIdentification.lean`: `0454ce14669be84c8384143a8ace33b7e795bc5b262355afc97284d1a963f4a1`.
- `V350FixedBaseEquivalence.lean`: `6b4cda490d27efc86fdac21e57b91c30778477221d08ff9c90f31a1bf8b8f278`.
- `V350DualFixedWeightLaws.lean`: `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`.
- `V350DualFormNormality.lean`: `feace23e31954e69de8103646211acd6d59a1b859e3b9ec109c142b1c994fdaa`.
- `V350ScalarDualWeight.lean`: `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`.
- `V350ScalarDualWeightFaithfulness.lean`: `3ff3e31e49de71f035a425202ef1796be18da2b46bdb60a7f6c34b8a2e73f61c`.
- `V350BoundedBaseDualValues.lean`: `8ca1418ac31012523b72539d0a734c77edc15caacacd87eec912a23f8e40aa50`.
- `V350ScalarWeightDomain.lean`: `e83ada9b5abbf2c179c28b03d3c020be83861681ba3ae450999c1c64ea8e2f0f`.
- `V350RegularApproximation.lean`: `d8e7830989e0ba3d71f0e8495f54414cedc12a9eac16b1bc0501f15342b8bb44`.
- `V350DualWeightForm.lean`: `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`.
- `LACUNAS_A1.md`: `cf0ef3264d91c8033a399851407ca8b5f08deef63b850a2fcf62b2fc56ab581c`.
- `ORDEM_011`: `2457c9b136025aeb24a3f9131e001d53fdcdbc8cdfa4f377da01c31f7c5304d0`.

Somente esta nota foi criada em revisao/. Nenhuma fonte Lean, memória, parecer anterior, compilação ou monólito foi tocado/executado.
