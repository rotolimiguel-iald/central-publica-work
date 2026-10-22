# A1 — leis consumidoras da avaliação funcional

2026-09-14T09:29:36.330444-03:00

[OPEN — ficha anterior ao código] A1(b): avaliacao concreta da media dual para compor nu=m_A(omega); RegularCoreTraceData continua consumidor final via perturbacao, nao preenchido por estas leis.

Para psi:M->L[C]C representado por HasSum vetorial, m_A(psi) conserva zero/soma/escala/ordem no input A; normalidade para supremos positivos dirigidos arbitrarios; identidade com integral da mesma acao dual apos soma; bimodulo e valores limitados. Nenhum teorema presume que todo funcional normal admite tal serie.

ADAPTAR ligacao a leis existentes. NOVO somente troca supremo de rede/serie ENNReal, nao fornecida pela troca sequencial anterior. Nao refazer formas, peso, Moreau ou GNS.

| Declaração | Fonte | Decisão | SHA256 lido |
|---|---|---|---|
| structure RegularCoreTraceData | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351RegularCoreTraceContract.lean:43 | CONSUMIDOR FINAL | `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0` |
| theorem baseDualEvaluation_eq_hasSum_series | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351BaseFunctionalEvaluation.lean:154 | REUSAR descida na mesma M | `364032cb9a1d87eee59474e5c5fc548fb540916fc81779134e9410a16bd2b35f` |
| theorem baseDualWeight_add | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ExtendedBaseDualWeight.lean:58 | REUSAR zero/soma/escala/ordem/fidelidade/bimodulo | `1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87` |
| theorem baseDualWeight_bounded_value | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ExtendedBaseDualWeight.lean:117 | REUSAR controle limitado | `1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87` |
| theorem regularDualForm_preserves_internal_isLUB | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualFormNormality.lean:80 | ADAPTAR supremo de redes, sem impor enumerabilidade | `feace23e31954e69de8103646211acd6d59a1b859e3b9ec109c142b1c994fdaa` |
| def dualQuadraticIntegral | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualWeightForm.lean:62 | REUSAR mesma acao dual e Haar | `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4` |
| theorem dualQuadraticIntegrand_measurable | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualWeightForm.lean:47 | REUSAR Tonelli | `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4` |
| lemma iSup_add_iSup_of_monotone | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\Data\ENNReal\Operations.lean:686 | ADAPTAR somas finitas e serie para rede arbitraria | `ef1b535b89d2f3ff0f710bec2a74a7943a09cfebe9ea4dbd7dc8d67b10873e46` |
| protected theorem tsum_eq_iSup_nat | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\Topology\Algebra\InfiniteSum\ENNReal.lean:134 | REUSAR | `467564faec2b6c357565afaeebed87b6dbd3de21c225189f4041907c6cf2fe38` |
| theorem lintegral_tsum | C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911\r\tgl_kernel\.lake\packages\mathlib\Mathlib\MeasureTheory\Integral\Lebesgue\Add.lean:360 | REUSAR | `e330b98eb9686290a3257802c38ad756150b110deb39fe32c66da46cf1211e4f` |

Buscas exatas, saídas e seis modalidades herdadas no JSON acompanhante. A consulta independente recomenda a descida somente após média: o levantamento vetorial ao core antes dela pode depender da representação. O domínio desta entrega mantém HasSum explícito; não afirma cobertura de todo predual.
