# Parecer independente — aproximantes positivos na base

2026-09-14T09:09:20.326558-03:00

**[REAL] DEV aceito no escopo de um módulo/três teoremas, sem achados P0–P2.** Fonte final lida integralmente, hipóteses e tipos conferidos, recompilação própria e auditor separado rc0, sem avisos. O binário produzido coincide byte a byte com o autoral. Não resta análise necessária deste delta.

| Declaração (`TGLV351`) | Tipos e alcance conferidos |
|---|---|
| `dualResolvent_minimum_energy_value` (linha 15) | Hilbert complexa completa genérica; A≥0 e R dado como limite forte dos resolventes de cortes. Identifica a energia no minimizador com `ofReal(Re⟨v,(I−R)v⟩)`. |
| `exists_base_moreau_approximant` (linha 47) | Para todo P, input positivo A do mesmo core e c>0, existe D na base original, 0≤D≤cI, que representa o mínimo atingido para todo vetor regular e todos os competidores. |
| `exists_monotone_base_dual_approximation` (linha 115) | Existe uma sequência D:ℕ→B(Hbase), escolhida antes dos vetores, positiva, pertencente à base e crescente na ordem dos operadores, recuperando q_A por supremo em ENNReal para **todo** vetor regular. |

No primeiro lema, `toReal` é usado após provar finitude de q_A(Rv). A orientação do produto interno é reconciliada pela simetria da parte real; não se supõe que os valores de q_A em vetores arbitrários sejam finitos.

No segundo, A/c mantém pertinência e positividade. O fornecedor existente produz R positivo, contrativo e fixo, com seu limite forte; essas premissas não ficam a cargo do consumidor final. B=c(I−R) pertence a F e satisfaz 0≤B≤cI. A identificação concreta F=amplificação de M e `fibre_nonneg_iff`/`fibre_le_iff` transportam a pertinência e a **mesma ordem** até D∈M. A escala é cancelada em ENNReal usando c>0; a normalização da integral dual permanece herdada, sem redefinir Haar.

No terceiro, c=n+1 evita a escala zero. A comparação de mínimos dá monotonicidade das avaliações. Positividade e auto-adjunção, mais teste em `testVector v`, devolvem monotonicidade real dos CLM: não é apenas ordem de valores truncados por `ofReal`. Para s=sup das avaliações, a prova separa s=∞ de s<∞. No caso finito, minimizadores w_n satisfazem q_A(w_n)≤s e (n+1)‖w_n−v‖²≤s.toReal; daí w_n→v e o subnível fechado da forma dá q_A(v)≤s. A desigualdade inversa usa o competidor v. Não há densidade do domínio finito presumida, troca ∞→0 por `toReal`, circularidade com o predual ou hipótese de cota uniforme da forma.

A cota D≤cI está explicitamente exportada pelo segundo teorema. O último exporta positividade, pertinência, monotonicidade e supremo; não exporta a cota D_n≤(n+1)I nem os minimizadores como campos adicionais. Isso basta para a ponte por supremos de avaliações de operadores limitados planejada.

## Reuso, errata documental e limites

[REAL] Ficha MD/JSON e `ADENDO_REAPROVEITAMENTO_A1_APROXIMANTES_BASE.json` lidos. A grafia correta `exists_dualFormRepresentation`, linha 137 de V350DualFormRepresentation, foi conferida com seu hash e enunciado. A busca antiga com sublinhados foi negativa por grafia; **não demonstra ausência da representação completa**. O fornecedor já constrói representação/raiz no suporte; o novo delta fornece especificamente aproximantes limitados crescentes na base. Os registros antigos e a correção ao lado foram preservados.

[REAL] Este resultado é um avanço concreto para a ponte predual de A1(b): oferece os D_n positivos da mesma base, com recuperação da mesma integral em toda a representação regular. Não define ainda m_A em todos os funcionais normais positivos nem prova suas compatibilidades preduais. Isso permanece a próxima ligação delimitada descrita na [consulta Moreau/predual](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/CONSULTA_A1_MOREAU_PREDUAL.md>). Não se exige isomorfismo geral de cones para aceitar estes três teoremas.

**[OPEN] A1(b), existência/perturbação do traço escalado, não está pago por este módulo.** Nenhum KMS, traço, gate, runtime ou custódia nova é afirmado. Os pareceres [base estendida](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/REVIEW_A1_BASE_ESTENDIDA_FINAL.md>) e [semifinitude escalar](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/REVIEW_A1_SEMIFINITUDE_FINAL.md>) permanecem íntegros e sustentam seus próprios escopos; esta revisão conclui somente o delta dos aproximantes.

## Evidência e proveniência

Lean 4.31.0. Execução própria final: módulo rc0 em 26.350s; auditor rc0 em 18.558s. `#check` com universos e `#print axioms` exatamente dos três alvos: somente **propext, Classical.choice, Quot.sound**, inclusive transitivamente.

| Artefato | SHA256 lido por script |
|---|---|
| Fonte final | `45d47db69249a1873c8059b0a9e85f74c0af6920e31ce48b787a4c33e4fde49d` |
| Binário próprio = autoral | `8d9403a721b132f34c97780a46288b1beb9287c9a1b00e8beb9c632490382176` |
| stdout próprio do módulo | `9c853a4f9e4a982d887ee809b4e1ed8dac590d17c5d84e8f5a4b023faa2a7e60` |
| stdout próprio do auditor | `69657bfb5d3b394262e8ae1d14b84c672e7fc514f4338d2a33ece2296af1e11a` |
| Adendo de reuso | `462c1d6cf5691d0c935e420f57ef4311f16b4fdc0b0d7f8e19a592082a672a37` |
| Manifesto conjunto de dependências | `5aecabbd03d2b3ea74bf0e63df8f98a40071b1d41fdefc83caa116b75a7ef618` |

Foram relidos os 384 pares fonte/binário do manifesto conjunto: 380 herdados e quatro V351. Isso é verificação de pins, não 384 recompilações. Nesta árvore foram reutilizados por cópia 382 objetos da árvore própria de semifinitude: os 380 antigos são binários herdados, e dois pais V351 já tinham recompilação própria. Os pacotes externos são somente leitura e não foram reconstruídos. O LEAN_PATH final contém o build próprio e os pacotes, sem build autoral de projeto.

A primeira tentativa própria `base_moreau_independent_20260914_090448_645300` rc1 é preservada: o novo prefixo TGLExt ocultou a resolução do objeto pai existente na árvore anterior. A preparação foi corrigida copiando os objetos pinados ao novo build, sem alterar nenhuma fonte Lean nem recompilar dependências. A execução final ocorreu em `base_moreau_independent_20260914_090556_274602`.

Histórico autoral relido: quatro rc1 excluídos e um rc0 intermediário com aviso/snapshot anterior, não utilizado para aceitar a fonte final; somente `attempts/20260914_090140_683505` é o run final aceito. O negativo +1 em `090247_321102` foi **relido, não reexecutado**: rc1 por elaboração matemática e `sorryAx`, sem falha de ambiente. `AUDITORIA_A1_APROXIMANTES_BASE.json` é evidência autoral; os seis controles ali nomeados não são apresentados como seis testes executados pelo revisor.

Evidências próprias: [compilation.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/base_moreau_independent_20260914_090556_274602/compilation.json>), [auditor.stdout.txt](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/base_moreau_independent_20260914_090556_274602/auditor.stdout.txt>), [preflight.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/base_moreau_independent_20260914_090556_274602/preflight.json>), [author_history.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/base_moreau_independent_20260914_090556_274602/author_history.json>), [verification.json](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/revisao/base_moreau_independent_20260914_090556_274602/verification.json>).

[REAL] Pins das fontes, binário final, fichas, `um.py` e pareceres anteriores reconferidos sem alteração. Todas as escritas ficaram em revisao/. Nenhum programa autoral, integrador, recorder ou monólito foi executado; memórias e originais intocados.
