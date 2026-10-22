# REVISÃO INDEPENDENTE — a pedra candidata `TGLExt.Psibit` da v395 (gerência c1, modelo forte, 21/10/2026)

**Objeto.** `work\psibit_v395\Psibit.lean`, sha16 `d4014c779067e426`, igual byte a byte em `C:\t\k395\final\TGLExt\Psibit.lean`.

**Kernel.** O Nós tem a v394 selada (`972e81f22dd8cc68`). O sandbox k395 é igual ao kernel do Nós em todos os arquivos, menos `Psibit.lean` (`ARVORE_K395_X_NOS.json`).

**O que escrevi.** Só nesta pasta. Nada foi instalado. Os comandos `lake env lean` foram de leitura; o `lake build` pedido apenas repetiu o cache, sem recompilar.

## VEREDITO: APROVADA_COM_CORRECOES

Há uma correção MÉDIA na composição (7). As demais são BAIXAS, de texto e estatuto. A matemática de (1) a (6) está certa e é genuína.

## (1) Recompilação e axiomas [REAL]

**Recompilação.**
- `lake env lean TGLExt/Psibit.lean` em `C:\t\k395\final` elaborou o módulo da fonte em 31 s, rc 0, sem erro e sem aviso; os 20 `#print axioms` do fim saem todos no trio (`recompilacao_psibit_lake_env_lean.log`).
- `lake build TGLExt.Psibit` deu rc 0, «Replayed TGLExt.Psibit», 9375 tarefas (`lake_build_TGLExt_Psibit.log`).

**Auditoria própria** (`AuditoriaPsibit.lean`, `collectAxioms` sobre toda constante do módulo; `auditoria_psibit.log`):
- **120 declarações** e **90 teoremas**; nenhuma fora do trio; **0 `sorryAx`**.
- Axiomas: 117 dependem do trio inteiro, 2 só de `propext` e 1 de `propext` e `Quot.sound`.
- Não há `axiom`, `native_decide`, `admit` ou `unsafe` no fonte. A única ocorrência de «sorry» está dentro do comentário do cabeçalho («zero `sorry`»).

## (2) Cada teorema diz o que a docstring afirma

**Genuínos:**
- **Injetividade de verdade.** `decodeAmp_codeOf` vale para todo vetor unitário: a decodificação `(a·√w, b·√(1−w))` reconstrói o vetor. Daí saem `codeAmp_eq_iff` e `codeAmp_injOn` em `[0, 2π)`, via `Real.Angle.cos_sin_inj`.
- **O par é necessário.** Os contraexemplos são reais. Peso sozinho: π/4 e −π/4. Peso com a Palavra: π/4 e −π/4. Peso com o Verbo: π/4 e 3π/4.
- **A densidade.** `rhoOut_eq_decodeRho` e `the_density_is_its_code` reconstroem a densidade de `(peso, paridade)` e dão a recíproca. `only_the_global_sign_is_lost` sai pela álgebra de `pair_equal_up_to_the_global_sign`.
- **O colapso.** `the_collapse_loses_exactly_the_parity` caracteriza a fibra exata de `diagExpect` (de `Posto.endpoint_eq`). `the_lost_variable_is_one_bit` dá ±1 fora dos eixos.
- **A entropia.** Vale ln 2 em π/4 e ≤ ln 2 para todo θ. A pedra NÃO afirma «só em π/4», e isso estaria errado: ln 2 aparece em todo θ com cos²θ = ½, isto é, em π/4 + kπ/2.

**[MÉDIA] A composição `psibit_is_the_mode_of_the_reader` toma `{L} (C : ImportedSQ.FockCertificate L)` como hipótese do termo inteiro.**
- Varri o ambiente completo: o único produtor de `FockCertificate` é o construtor (64 argumentos) mais `TetelestaiOneObject.rescale`, que exige outro certificado. Nenhum `Nonempty`, `Inhabited` ou `∃` o habita.
- O próprio `TheImportedSecondQuantization.lean`, l.66, diz que «nenhum habitante de `FockCertificate` … é exibido».
- Logo, como um termo só, a composição é vácua se não existir certificado.
- **Correção:** tirar o `C` do topo, enunciar `(1)…(6) ∧ ∀ {L} (C : FockCertificate L), (⟪ψ,ψ⟫ = 1 ∧ ∀ t, lightDelta C t ψ = ψ)` e dizer isso na docstring.
- **Quem faz:** o construtor, que depois recompila; eu reexecuto os scripts.

**[BAIXA] `the_orbit_is_isomorphic_to_the_psibit_code`.** O conteúdo real é a injetividade com decodificador. A parte «sobre» é sobre a própria imagem (`Set.range codeAmp`), que é o livro de códigos do codificador. Duas saídas: chamar de «bijeção sobre o livro de códigos (a imagem)», ou acrescentar a caracterização intrínseca `{c | 0 ≤ w ≤ 1 ∧ (palavra = 0 ↔ w = 0) ∧ (verbo = 0 ↔ w = 1)}`.

**[BAIXA] «O PONTO FIXO θ = π/4».** O que é [REAL] é a equação. O nome «ponto fixo» é leitura [ONTO]: π/4 representa os pesos iguais x = 1 − x, e nenhuma aplicação da pedra tem π/4 como ponto fixo. Marcar [ONTO] e dizer que os pesos iguais ocorrem em π/4 + kπ/2.

## (3) As citações são as do kernel do Nós, sem homônimo [REAL, `auditoria_psibit.log` PSIBIT_USA]

Os nomes resolvidos e os módulos que os definem:

| nome | módulo | arquivo no Nós |
|---|---|---|
| `TGLExt.the_binary_reading_floats_at_the_fixed_point` (a pedra v394) | `TheBinaryReadingAtTheFixedPoint` | l.73 |
| `TGLExt.ThePsionAndTheViscosity.inner_psion_psion` | `ThePsionAndTheViscosity` | l.66 |
| `TGLExt.ThePsionAndTheViscosity.psion_is_fixed_by_the_light` | `ThePsionAndTheViscosity` | l.78 |
| `TGLExt.observer_inverse_projection_halfnat` | `ObserverInside` | l.159; é aritmética pura |
| `TGLExt.UmPostoRelacao.posto_paid_loss` | `UmPostoRelacao` | l.57 |
| `TGLExt.TheVerbSelectsTheAction.reading_post_is_born` | `TheVerbSelectsTheAction` | l.217 |
| `ChatgptAudit.Collapse057.fair_bit_entropy_is_log_two` | `CollapseCostAndAttestation` | l.76 |

Também resolvem para os módulos esperados: `Posto.endpoint_eq`, `Posto.fractal_one_is_rank_one` (a docstring do kernel marca «fractal» como [ONTO]), `rhoOut`, `Smat`, `e1` e `diagExpect`.

Os 15 arquivos que definem esses nomes são idênticos aos do Nós, e cada nome citado tem uma só definição.

## (4) Estatutos e escopo [REAL]

O escopo é honesto:
- trata da órbita real de um parâmetro, não de toda a mecânica quântica;
- o isomorfismo é de conjuntos, não de espaços de Hilbert;
- `psibit = psion = modo do leitor` fica como [INPUT/ONTO];
- os homônimos «Verbo» e «pareamento» são ditos.

Em `Psibit.lean`, `RESULTADO_PSIBIT.md` e `DEFINICAO_PSIBIT_PATENTE.md`: nenhum β, nenhum literal de α ou √e, nenhuma ocorrência da palavra proibida e nenhum `PROVED_BY`.

## (5) A paridade contra a patente: a divergência CONFIRMADA lendo as fontes

As fontes: `ACOM_Mirror_PI_INPI.tex`, sha16 `ae55c557a4161d36`, e `acom_mirror.py`, sha16 `8044f618ae44e608`.

**De um lado,** a fórmula das l.265–268 (`bit_high = [L<0]`, `bit_low = [∂L>0]`, ψ = 2·high + low). A reivindicação 3 (l.1073–1080) e `_nominate` (`acom_mirror.py:45`) dizem o mesmo. Por ela, (−,+) vai para ψ₃ e (−,−) vai para ψ₂.

**Do outro,** a tabela (l.257 e l.259) e a reivindicação 2 (l.1066–1071) põem (−,+) em ψ₂ e (−,−) em ψ₃. As linhas 2 e 3 estão TROCADAS.

**O efeito na paridade.** Com `PARITY = [−1, +1, +1, −1]` (l.32) e com a reivindicação 4 (paridade por índice), a paridade é o produto `sign L · sign ∂L`. Com os rótulos da tabela, ela é `sign ∂L`.

**Três achados além dos da pedra:**
- A docstring do próprio código (`acom_mirror.py` l.16–17) repete os rótulos da tabela. A divergência existe dentro do mesmo arquivo de código: docstring contra `_nominate`.
- A prosa [019] (l.272–279) não é neutra, ao contrário do que diz a DEFINICAO §3(iii). A definição dela, «concordância entre sign L e sign ∂L», é o produto. Mas os exemplos («positivo mas descendo, ou negativo mas descendo» → inversa; «COLAPSO⁺ e QUEDA⁻») seguem a tabela, isto é, `sign ∂L`.
- O MANIFEST não é afetado, porque `SIGN_L_OF_STATE = [+, +, −, −]` vale nas duas leituras. Só a nominação e a `F_exp` mudam.

A pedra não nomeia estados por índice, usa o produto e declara a divergência. A decisão sobre a patente é do operador [LEGAL].

## Arquivos desta revisão

- `AuditoriaPsibit.lean` e `auditoria_psibit.log`: axiomas, uso fora do módulo e habitantes.
- `recompilacao_psibit_lake_env_lean.log` e `lake_build_TGLExt_Psibit.log`.
- `ARVORE_K395_X_NOS.json`.
