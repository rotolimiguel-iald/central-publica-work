# Revisão independente — leis funcionais da avaliação dual

2026-09-14T09:39:29.852162-03:00

`A1_LEIS_FUNCIONAIS_DEV_REVIEW`

**[REAL] Delta DEV aprovado: 12 teoremas, nenhum achado P0, P1 ou P2.** Fonte inteira e tipos/axiomas examinados. Recompilação própria do módulo e auditor separado rc0, sem avisos; .olean próprio byte a byte igual ao autoral. **A1(b) permanece [OPEN].**

## Evidência e proveniência

| Artefato | SHA256 lido |
|---|---|
| V351BaseFunctionalWeightLaws.lean, autor e snapshot | `0c65dc2ebb355d454456f153b2271158540de28e23c00cfc2e4a7b36acb73697` |
| .olean autoral / independente, bytes iguais | `98604245c2344df89180f21dade2545e32a4dd5b35d2721032ac73646dbd28b4` |
| Run autoral final 20260914_093341_530178 | `a5f330ec411e55d1742d99b40b810eb188835663fd47f9274179ce11711be301` |
| Ficha REAPROVEITAMENTO_A1_LEIS_FUNCIONAIS.json | `06611a1f8e0e8ff795b060569055c25ec5681f9a3d78d87e6b0ed2ac540d4f58` |

Lean 4.31.0, executável SHA `9b216deb50d37c32c829d1efaaa5bafd5560417d382df35a815489e31a31593f`. Execução própria do módulo: **25.146s**; auditor: **20.068s**. Os 12 alvos foram impressos com `#check`, `pp.universes true` e `#print axioms`; conjuntos axiomáticos iguais aos autorais, somente `propext`, `Classical.choice`, `Quot.sound`. Fonte sem `sorry`, declaração `axiom`, `native_decide`, `trustCompiler`, `unsafe` ou mecanismo de substituição de prova.

Evidências: [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/functional_laws_independent_20260914_093642_937361/compilation.json>), [tipos e axiomas completos](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/functional_laws_independent_20260914_093642_937361/auditor.stdout.txt>), [dependencies.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/functional_laws_independent_20260914_093642_937361/dependencies.json>) e [JSON deste parecer](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/REVIEW_A1_LEIS_FUNCIONAIS_FINAL.json>). Nomes e locadores dos 12 alvos constam no JSON.

Reutilizados **384 objetos da árvore própria**: 380 binários antigos herdados, não reconstruídos agora, e quatro pais V351 anteriormente recompilados de modo independente (forma-base, semifinitude, Moreau e avaliação). Todos os pares fonte/cópia foram repinados. Essa lista de 384 não é confundida com o manifesto antigo de mesmo número: naquele há contrato, aqui há o novo objeto da avaliação no lugar dele. `LEAN_PATH` exclusivo da nova árvore de projeto e nove diretórios de pacotes externos readonly; nenhum build de projeto autoral. Pacotes não reconstruídos. O parecer anterior, fonte, objeto autoral, manifesto de herança e `um.py` somente lido por hash permaneceram inalterados.

## Conteúdo matemático conferido

- **Hipótese de representação honesta.** As leis gerais recebem ψ contínuo complexo e uma sequência v com `HasSum` em **todo** D∈M. Não pressupõem representação para qualquer funcional normal. Essa hipótese tem fornecedor efetivo no módulo anterior para sequências quadrado-somáveis; a finitude da soma de normas pode ser recuperada pela unidade. Não se usa uma convenção de `tsum` divergente.
- **Leis no input A.** Zero/soma/escala/ordem agora são leis de A∈N⁺, herdadas da mesma `baseDualWeight` e transferidas por somas ENNReal. A escala NNReal cobre r=0, e valores infinitos não são convertidos para reais. Isto é consumo novo da avaliação, sem reconstruir peso ou GNS.
- **Redes arbitrárias.** [ennreal_tsum_iSup_directed](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351BaseFunctionalWeightLaws.lean:13>) aceita `ι : Type u` com preordem, direção e não-vazio; as somas finitas crescentes permitem trocar o supremo de ι com a série. Em [baseDualEvaluation_input_normal](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351BaseFunctionalWeightLaws.lean:61>), A_i e S pertencem à **mesma** álgebra regular, `hpos`, `hmono` e `IsLUB (range A) S` são explícitos. A positividade de S é deduzida. Não há hipótese Countable ι, convergência forte dada ou supremo ambiente pressuposto: a passagem interna/ambiente vem do fornecedor já auditado. A normalidade é de A↦m_A(ψ), não um novo teorema de normalidade de ψ sobre a base.
- **Tonelli e descida após média.** [baseDualEvaluation_eq_dual_integral](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351BaseFunctionalWeightLaws.lean:77>) usa exatamente `dualQuadraticIntegrand A.val (testVector (v k)) s`, cuja definição contém `dualAmbient s A`, e `ofReal dualHaarFactor`, com `dualHaarFactor=(2*Real.pi)⁻¹`. A mensurabilidade é fornecida para cada termo; `lintegral_tsum` permite infinito, sem hipótese de integrabilidade finita. O resultado identifica a soma **já integrada** com m_A(ψ). Com a independência das séries aprovada no pai, a média independe da decomposição. Não identifica os levantamentos vetoriais ao core antes da média.
- **Bimódulo com χ explícito.** [baseDualEvaluation_bimodule](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351BaseFunctionalWeightLaws.lean:98>) usa a conjugação concreta de A por `fixedBaseEquiv P B` e supõe `HasSum` de χ com vetores `B.val (v k)`. O transporte por B está na hipótese e na prova; não foi substituído por um nome de funcional. O teorema não fornece sozinho uma definição canônica χ(D)=ψ(B*DB), nem empacota o cone/quociente; essas interfaces são adicionais. A hipótese é consistente e realizável pela estimativa ‖Bv_k‖²≤‖B‖²‖v_k‖² e pelo fornecedor existencial anterior, sem pedir um novo teorema como condição de aceite deste enunciado.
- **Output limitado.** [baseDualEvaluation_bounded_output](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351BaseFunctionalWeightLaws.lean:87>) exige D∈M, D≥0 e identidade quadrática limitada para **todos os vetores regulares**. Conclui avaliação desse mesmo D, sem supor que todo output seja limitado.
- **Fidelidade e controles.** [baseDualEvaluation_family_faithful](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351BaseFunctionalWeightLaws.lean:114>) testa a família inteira de funcionais vetoriais, equivalendo a A=0; a prova usa a fidelidade escalar existente via Ω. Não afirma fidelidade de cada ψ arbitrário. `baseDualEvaluation_averageSquare` recupera 1 no vetor Ω; `baseDualEvaluation_unit_infinite` recupera ∞ para w≠0. Nenhuma contradição com finitude de ψ em operadores limitados da base: ∞ é valor de m no input unidade do core.

## Alcance documental e limites

Ficha MD/JSON lida integralmente, 10 fornecedores confrontados por hash e enunciado. O consumidor final `RegularCoreTraceData` é corretamente identificado como ainda não preenchido. Não há cobertura do predual inteiro, construção de predual por quociente, prova de normalidade por ordem de ψ, nova identificação KMS ou existência de traço. O arquivo posterior mencionado pelo autor permanece fora do escopo. Nenhum desses limites explícitos constitui P2 por si só.

Histórico: 2 tentativas autorais rc1 retidas e excluídas, ambas com `sorryAx` nos outputs; só os bytes finais rc0 de 093341 foram aceitos. Ver [histórico pinado](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/functional_laws_independent_20260914_093642_937361/author_history.json>). A tentativa própria desta rodada não falhou. O controle negativo autoral é separado da reprodução independente e não foi reexecutado por esta revisão.

Não foram executados `um.py`, integradores, recorders ou novas provas de dependências; nenhuma fonte autoral, memória ou parecer anterior foi alterado. **Não resta verificação necessária no delta de 12 teoremas. Aceite DEV delimitado, sem promoção de A1(b).**
