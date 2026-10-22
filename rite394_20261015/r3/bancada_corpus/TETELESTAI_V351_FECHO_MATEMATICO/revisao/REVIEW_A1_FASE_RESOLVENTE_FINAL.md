# Parecer final — fase do resolvente no mesmo GNS

Data: 2026-09-14T10:21:21.678785-03:00. **[REAL — revisão DEV independente encerrada, cinco módulos/39 declarações].**

**P0=0; P1=0; P2=0; findings=[]**. Aceito o delta delimitado: construção unitária pelo resolvente efetivo, grupo, continuidade forte e caracterização única no mesmo `ScalarGNSHilbert P`. A1(b), identificação da ação com AdΛ, gerador h e traço continuam **[OPEN]**. Nenhuma pendência de revisão dos cinco fontes permanece.

O parecer parcial de 19 alvos continua byte a byte preservado. Ele registra a leitura anterior sem compilação própria; este parecer acrescenta a reprodução agora expressamente solicitada. Não é aceite de integração no monólito nem de custódia futura.

## Evidência própria e pins

Executei **cinco recompilações e um auditor Lean separado**, todos rc0 e sem warnings. Os cinco `.olean` próprios são byte a byte idênticos aos autorais. O auditor contém `#check @nome` com universos e `#print axioms` de **exatamente 39 nomes: seis definições e 33 teoremas**. Todos usam somente `propext`, `Classical.choice`, `Quot.sound`; sem `sorry`, `axiom`, `native_decide` ou `trustCompiler` nos candidatos. Tipos elaborados, fontes, comandos, streams e hashes estão no JSON final e na árvore independente.

Compilação: [resolvent_phase39_independent_20260914_101512_721055/compilation.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\resolvent_phase39_independent_20260914_101512_721055\compilation.json>), SHA256 `7942155540ed0e866e3f1fe89a0ccc7a8723bf991e9cca56079d9f583a128de9`. Toolchain: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`; executável pinado. `LEAN_PATH` contém apenas a árvore própria e pacotes externos readonly, sem caminho de build autoral de projeto.

Foram congelados e reconferidos **448 pares fonte/objeto** do manifesto: **378** objetos vêm de snapshots prévios de revisão, **70** são herdados dos objetos autorais pinados, copiados para a árvore isolada após comparação de hashes. Essas 448 dependências **não foram recompiladas aqui**; ter bytes iguais ao manifesto não equivale a uma nova reprodução independente delas. A proveniência individual está em `dependencies.json`. Nenhum dos cinco módulos novos usou seu próprio binário autoral como importação.

| Módulo | Alvos | SHA256 fonte | SHA256 olean autoral = próprio |
|---|---:|---|---|
| `V351ResolventPhaseFunctions` | 9 | `8eb2f7fb43b753d739c276b9e98655529860084586e311d94c8984cde361aea5` | `4ea76e6e501af3a9b56d9f02d2263c210ab68806e287ab74c001380eb059eebd` |
| `V351ResolventPhaseCalculus` | 10 | `cd207e3a21c50f65fe3b199e201b2b148a0d98fc2e3a3cf7e40a80e61ba4f818` | `774314761aedd48f91114349db843d8d23c674cbb73b741915c258d20790aff6` |
| `V351ResolventImaginaryPowers` | 9 | `0cfc297376410ff6bd259eeaf921a9d6e6ca47829b5d389c6b5c30bf4c5accf5` | `f7784e9cec15f3bd5661743a5f920a99c70cf8b633e72bee77b1133d7d120e48` |
| `V351ResolventImaginaryContinuity` | 3 | `8dd7a20376d00763bd8717227fa6bf7436f9eb11cbf4433caabb762d7719fdd4` | `867a0a83324248a2cb18994e4d4afb7f35fef601675d3548c3b145faed546c3c` |
| `V351ScalarTomitaImaginaryPowers` | 8 | `b8871f05b5b9605a8b193a8ed25346d79eac72d025d3ad95c8f9c884f28b4e52` | `001ddbe8096f6f85f418e761297dbb8cc2ab4f2edd87ff4d292ec9dc15374737` |

Execuções autorais aceitas e streams próprios correspondentes:

- `V351ResolventPhaseFunctions`: `20260914_095907_662952`; próprio `V351ResolventPhaseFunctions.stdout.txt`, rc0, 23.90s.
- `V351ResolventPhaseCalculus`: `20260914_100402_294282`; próprio `V351ResolventPhaseCalculus.stdout.txt`, rc0, 24.12s.
- `V351ResolventImaginaryPowers`: `20260914_100649_329613`; próprio `V351ResolventImaginaryPowers.stdout.txt`, rc0, 22.78s.
- `V351ResolventImaginaryContinuity`: `20260914_101045_813310`; próprio `V351ResolventImaginaryContinuity.stdout.txt`, rc0, 23.76s.
- `V351ScalarTomitaImaginaryPowers`: `20260914_101128_096848`; próprio `V351ScalarTomitaImaginaryPowers.stdout.txt`, rc0, 34.06s.

O auditor próprio durou 22.95s. Seu rc0 foi obtido na primeira execução. O pós-processador Python inicialmente recusou os nomes decorados `Classical.choice.{u}`/`Quot.sound.{u}` impressos com universos; corrigiu-se somente essa normalização, preservando o JSON inicial e o stream bruto. Não houve nova execução de Lean nem alteração de prova para esse ajuste; `AuditResolventPhase39.verified.json` registra a leitura corrigida.

## Hipóteses e conteúdo efetivo

**1. Funções (9).** `b(x)=x(1−x)` e `g_t(x)=b(x)exp(it·Real.log((1−x)/x))` têm as identidades de norma, estrela e produto declaradas. A continuidade conjunta é global em ℝ×ℝ. Fora de 0 e 1, o argumento do log é não nulo — Mathlib permite log de negativo como log do módulo. Nas duas pontas, `||g_t(x)||=||b(x)||→0` controla conjuntamente t e x. Não se usa continuidade da fase não amortecida nas pontas, nem extensão por zero fora de [0,1]. No interior do espectro positivo contrativo, o sinal é **+it log((1−x)/x)**.

**2. Cálculo funcional (10).** O Hilbert genérico está em `Type` (universo 0), complexo e completo para o CFC; os tipos efetivamente elaborados constam do auditor. A definição elementar `resolventDampingOperator` dispensa completude, como mostra seu tipo. T é limitado; as identidades de CFC/produto/Gram recebem auto-adjunticidade, e positividade do amortecimento/módulo/norma recebem `0≤T≤1`. O teorema da estrela é válido para todo T conforme o CFC total da biblioteca, mas isso não torna os outros teoremas incondicionais. Não há hipótese espectral escondida ou uso de cálculo holomorfo: usa-se a função contínua `z↦g_t(z.re)`. Aqui C₀=B e C_s C_t=B C_(s+t), não a lei unitária sem amortecimento.

**3. Extensão unitária e grupo (9).** Agora são recebidas explicitamente as injetividades de T e I−T. B=T(I−T) é positivo e injetivo, logo tem imagem densa; a injetividade de B usa a composição dessas duas aplicações. `Ran(B²)⊆Ran(C_t)` vem de **C_t C_−t=B²**, e Ran(B²) é densa. Assim `denseLinearEquiv` recebe as duas densidades e a igualdade `||C_t x||=||Bx||`; sua sobrejetividade está paga, não presumida. Define U_t como equivalência linear isométrica e prova U_t B=C_t. A lei do grupo é demonstrada em Ran(B²) e estendida por continuidade. Nenhuma inversa limitada de B, gap ou PVM é exigida.

**4. Continuidade (3).** Para T auto-adjunto, t↦C_t é contínua na **norma de operadores**, pelo CFC sobre o espectro compacto. Com `0≤T≤1` e ambas injetividades, a continuidade das órbitas em Ran(B), junto da constante Lipschitz 1 de cada U_t, dá continuidade conjunta `(x,t)↦U_t x` e continuidade forte. Não se afirma continuidade de t↦U_t em norma de operadores. A retipagem `t↦(x,t)` no corolário mantém exatamente essa topologia.

**5. Mesmo objeto concreto (8).** Os alvos recebem apenas `P : SiteProfile` e os parâmetros/vetores indicados; não há nova hipótese de modularidade. `scalarTomitaResolvent_complement_injective` transforma a igualdade (I−T)x=(I−T)y pelo J original, usa JT=(I−T)J e a injetividade de T/J. As condições do grupo são então descarregadas com os fornecedores concretos, sem trocar de GNS. A cadeia relida é `scalarClosedTomita_graph_eq_weight` → S do peso completo; `scalarTomitaSquare_apply` → Δ=S†S com domínio de composição; `scalarTomitaResolvent_graph` → T=(I+Δ)⁻¹ como igualdade de mapas parciais. Nenhuma identificação por homônimo é usada.

`scalarTomitaImaginaryPower_unique` afirma unicidade **entre mapas complexos limitados que satisfazem U·b(T)=g_t(T)**, ponto a ponto para todo vetor. Esta é uma caracterização densa efetiva da potência imaginária definida por resolvente. É correto chamar o grupo de Δ_ν^it **nessa construção concreta**; não foi provada nem alegada igualdade com uma API abstrata anterior de potências de `LinearPMap`. Grupo, inversa e continuidade forte estão especializados ao mesmo T e H_I.

## Documentação, históricos e limites

Li a ficha MD/JSON anterior ao código, seus oito fornecedores pinados e o `ADENDO_A1_POTENCIAS_IMAGINARIAS.md`. A ficha foi preservada; sua data/status são antecedentes e não aprovação antecipada. O adendo separa corretamente o pagamento deste subpasso das pontes de escala funcional, conjugação por J e ação nos geradores, ainda abertas. Essas pontes futuras não foram incluídas no aceite.

As **oito tentativas autorais rc1 anteriores** (2+3+2+1+0) foram localizadas e excluídas; nomes, logs e hashes constam da evidência. Prints parciais e `sorryAx` dessas tentativas não contam como prova. As cinco fontes finais correspondem aos snapshots rc0.

Também reli a auditoria autora e os dois controles negativos: multiplicar por 2 a norma da fase e trocar s+t por s−t. Ambos têm rc1, erros reais de elaboração e `sorryAx`, sem falha de acesso/importação. Os controles foram **executados pelo autor**, não repetidos por esta revisão; os logs e pins foram conferidos independentemente. Nenhum controle adicional foi necessário.

**Fronteira:** a igualdade U_t π(a) U_−t=π(Λ_t a Λ_−t), a identificação literal com um implementador esquerda/direita, o gerador h, sua perturbação e um habitante do contrato do traço não pertencem aos 39 alvos. Não se infere KMS por invariância, nem fechamento de A1(b). Nenhum monólito, integrador, recorder, memória ou gate foi executado/alterado pela revisão. Os únicos escritos desta rodada estão em `revisao/`.
