# Revisão independente — semifinitude escalar A1

Data: 2026-09-14T08:58:29.689839-03:00

**[REAL] Aceito o delta DEV de um módulo/dois teoremas. Nenhum achado P0–P2 no escopo.** Leitura integral da fonte, dos tipos impressos e dos fornecedores pertinentes; recompilação própria e auditor separado concluídos rc0, sem avisos. Não resta análise necessária deste delta.

| Declaração em `TGLV351` | Alcance conferido |
|---|---|
| `scalarWeight_square_finite_wot_closure` | O fecho WOT de `nν` dentro do mesmo core regular é exatamente esse core, para todo `P : SiteProfile`. |
| `scalarWeight_unit_not_square_finite` | A unidade não pertence a `nν`, pois sua avaliação escalar é infinita. |

`HasFiniteScalarSquare P A` significa `q_(A* A)(regularVacuum P) < ∞`. Portanto o primeiro alvo trata o domínio escalar completo, não exige uma cota uniforme da forma em todos os vetores e não identifica esse domínio com o ideal uniforme anterior.

A inclusão do fecho no core usa seu fechamento WOT. A inclusão inversa reaproveita `A regularAverage_h`, pertencente ao core e de quadrado escalar finito quando `h>0`, convergindo fortemente para `A`. O filtro é o concreto `𝓝[>] 0` de reais, não vazio; a pertinência eventual vem de `h>0`. A passagem forte→WOT é explícita. Não há hipótese residual de densidade, continuidade SOT da estrela ou limite forte a fornecer.

O segundo alvo usa o mesmo vetor `hOmega P`: sua não nulidade decorre da norma unitária do `regularVacuum`, transportada pela isometria `testVector`. `baseDualWeight_unit_infinite` dá o valor `∞`, contradizendo estritamente `< ∞`; não ocorre uso indevido de `toReal` no infinito.

**[DERIVED — alcance matemático]** Junto às leis de peso fiel e normal já herdadas, a aproximação de quadrados finitos fornece o critério usual de semifinitude escalar. Os aproximantes herdados também são uniformemente limitados (`‖A regularAverage_h‖ ≤ ‖A‖`); não se infere uma identificação geral WOT/predual de redes arbitrárias. O novo enunciado Lean certifica precisamente o fecho WOT acima, sem construir uma interface geral de pesos no predual. A unidade ter peso infinito é compatível com semifinitude. Referência conceitual já examinada: definição 7.1 de [Hiai, Lectures on Selected Topics in von Neumann Algebras](https://arxiv.org/pdf/2004.02383).

**[OPEN] A1(b) permanece parcial.** Esta etapa paga a ponte de densidade do domínio escalar e reutiliza o transporte real para formas na base aprovado em [REVIEW_A1_BASE_ESTENDIDA_FINAL.md](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/REVIEW_A1_BASE_ESTENDIDA_FINAL.md>). Não fornece a existência do traço fiel normal semifinito com escala dual exigido pelo contrato, nem sua perturbação a partir de ν. Também não acrescenta isomorfismo geral de cones/predual, KMS ou promoção de gate. A fórmula por supremos de minorantes positivos finitos do contrato **tracial** não é imposta aqui como requisito adicional para ν não tracial.

## Evidência própria e proveniência

Lean 4.31.0; módulo rc0 em 22.883s e auditor rc0 em 18.412s. Auditor com `#check` e universos explícitos mais `#print axioms` exatamente dos dois alvos. Ambos dependem apenas de `propext`, `Classical.choice`, `Quot.sound`, inclusive transitivamente.

| Artefato | SHA256 lido por script |
|---|---|
| Fonte final | `f5e7e85b034949be6517286f60c692d3d97d29c341aeba42a1f7172b7e610c2a` |
| `.olean` próprio = autoral, byte a byte | `36361c7abcb29c182d36457c5b69371217e5208936e2c2bec6a82974dbb3689b` |
| stdout próprio do módulo | `1cd2aa772359d88f6705c99566094b8f9f416b66754b2a40d26c3d73d802583c` |
| stdout próprio do auditor | `df2c4d3884e2e6fa79d733b2b0c0f969eb5a937a2f20458d52070acabeff81d2` |

O run autoral aceito é `attempts/20260914_084729_714501/run.json`; sua evidência foi relida e confrontada, sem substituir a reprodução própria. Foram conferidos os 378 registros do manifesto autoral de dependências e os seis fornecedores da ficha. A árvore própria congelada contém 382 objetos de projeto: 380 binários antigos herdados por hashes e dois pais V351 previamente recompilados de forma independente. Quatro dos antigos foram acrescentados agora por cópia pinada: `ContractionAdjointLimit`, `StrongBoundedApplication`, `FiniteDualStarCore` e `ScalarWeightDomain`. Não se afirma recompilação independente desses 380 objetos.

O `LEAN_PATH` usa somente o build próprio para objetos de projeto e pacotes externos somente leitura. Não foi usado build autoral de projeto como caminho de importação; pacotes não foram recompilados. Inventário, origens e hashes completos constam da árvore de evidências.

Evidências: [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/scalar_semifiniteness_independent_20260914_085400_122493/compilation.json>); [preflight.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/scalar_semifiniteness_independent_20260914_085400_122493/preflight.json>); [auditor.stdout.txt](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/scalar_semifiniteness_independent_20260914_085400_122493/auditor.stdout.txt>); [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/scalar_semifiniteness_independent_20260914_085400_122493/verification.json>).

[REAL] Fonte/binário autorais, fichas pinadas, `um.py` e os pareceres anteriores conferidos permanecem byte a byte. Escritas restritas a `revisao/`; nenhum recorder, integrador ou monólito foi executado, nenhuma memória foi atualizada. Esta conclusão é DEV, sem aceite integrado ou nova custódia.
