AFINAÇÃO DAS CORDAS — v398 sandbox

Pedra candidata `TGLExt/AfinacaoDasCordas.lean`: revisão independente PEDRA_APROVADA (2 BAIXAS de prosa); pedra, nome `AfinacaoDasCordas` e «afinação = comensurabilidade» ratificados pelo operador em 23/10 («Concordo com tudo», verbatim sha16 `5bccedc9cea3d57a`). Compilada em sandbox (`C:\t\k398b`, cópia de `C:\t\k398\final`); NÃO instalada; nada no quadro, no mapa, na memória, no site nem no git.

## Veredito

TGL_AFINACAO_DAS_CORDAS_STONE_V398_CANDIDATE__COMPILED_IN_SANDBOX__TRIO_ONLY__ZERO_SORRY__CYCLIC_CLOSURE_OF_THE_BOOST_PARAMETER_IS_THE_READING_CIRCLE__MATSUBARA_TOWER_IS_N_TIMES_KAPPA_AND_INFINITE__ZETA_REGULARISATION_GIVES_D26_BOSONIC_AND_D10_NS_UNDER_THE_NAMED_MASSLESS_FIRST_LEVEL_HYPOTHESIS__D10_IS_D9_SPATIAL__STRING_GEOMETRY_NOT_DERIVED__INDEPENDENT_REVIEW_PEDRA_APROVADA_TWO_LOW_PROSE_FINDINGS__RATIFIED_BY_THE_OPERATOR_23OCT__NOT_INSTALLED__GATE_UNMOVED

## Exame independente e ratificação do operador (23/10): alteração SÓ de docstring

- Exame independente da gerência (`C:\IALD\Central de Patentes\work\cadeia_de_selo\v398_exame\afinacao\EXAME_AFINACAO.md`, sha16 `94079c81972502cf`, sobre a versão `23a6c93d6dc84319`): PEDRA_APROVADA, 2 BAIXAS de prosa. **B1:** a frase «a leitura do operador (fala de 23/10), na formulação desta tarefa: as cordas fecham a face POR FORA; a TGL fecha SÓ A LEITURA» trazia «por fora» e «só a leitura», que não são bytes do operador; trocada pela forma admitida na v397, agora «composição da gerência sobre a fala do operador (`baef998c21393463`), ratificada pelo operador em 23/10 (`5bccedc9cea3d57a`)»; o mesmo para «afinação = comensurabilidade» (proposta da pedra, ratificada `5bccedc9cea3d57a`). **B2:** `matsubaraFermion`, `towerZeroPoint` / `towerZeroPoint_eq` / `bosonDirection_is_the_unit_tower` e `zeta_is_the_continuation_of_the_tower` são auxiliares FORA da composição (6); a pedra já os lista como tais; nada a corrigir; o ledger deve listá-los assim se a pedra entrar. A nota do exame sobre o `Sonico.lean` do sandbox não toca esta pedra (ela não o importa).
- Ratificação do operador (verbatim `5bccedc9cea3d57a`, 18 bytes, `OPERADOR_23out_concordo_afinacao_das_cordas_verbatim.txt`): «Concordo com tudo». Relato da gerência: ratificou a pedra, o nome `AfinacaoDasCordas` e «afinação = comensurabilidade» [INPUT]. O nome deixa de ser provisório.
- Alteração aplicada SÓ nos comentários (docstrings): o título do cabeçalho (sem «NOME PROVISÓRIO»), a seção da ratificação, o passo 3, o bullet [ONTO] e os docstrings de (1) e (6). Versão anterior `23a6c93d6dc84319` (backup `AfinacaoDasCordas.lean.bak_20261023_204818`); nova `66e28e61086cc6ba`.
- Código idêntico: o código fora dos comentários é byte a byte o mesmo (sha16 `17abbb84b1779e62`, 14094 bytes; `conferencia_codigo_identico.json`), e os termos do kernel também: o hash estrutural do TIPO e do VALOR de cada uma das 59 declarações do `.olean` é igual antes e depois da recompilação (`termos_antes.txt`, `termos_depois.txt`; sha16 `b24115df664e98d9` nos dois). Recompilado: Built (21s), 9010 tarefas, exit 0, nenhum aviso; `#print axioms` e `collectAxioms`: trio, zero `sorry`.

## A pedra

- Fonte: `C:\IALD\Central de Patentes\work\afinacao_das_cordas_v398\AfinacaoDasCordas.lean`, sha16 `66e28e61086cc6ba` (34814 bytes, 540 linhas); cópia idêntica em `C:\t\k398b\TGLExt\AfinacaoDasCordas.lean`. Gerada por `gerar_pedra.py` a partir de `AfinacaoDasCordas.lean.tmpl`: todo hash, o verbatim do operador e as linhas 958-960 de `A_ultima_corda_v3.tex` são LIDOS dos arquivos.
- Módulo `TGLExt.AfinacaoDasCordas`; importa `TGLExt.Palavra`, `TGLExt.TheStation`, `TGLExt.Fundacao` e `Mathlib.NumberTheory.LSeries.HurwitzZetaValues`.
- 34 declarações nomeadas (25 teoremas, 9 definições). Os seis pedidos:
  1. `the_cyclic_closure_of_time_is_the_reading_circle` — a face real não tem período (`boost P ≠ 1` para `P ≠ 0`); fechar com período `P` é leitura fiel se e só se `κ·P = ±2π` (por `faithful_period_iff`); `1/P = κ/2π` (por `reciprocal_temperature`); a torre de Matsubara `matsubara P n = n·(2π/P)` é `n·κ` (`matsubara_eq_mul_kappa`); o círculo é fiel se e só se o modo fundamental é `κ` (`faithful_iff_fundamental_mode`); todos os modos voltam em `t = P` (`tower_returns_at_the_period`).
  2. `the_tower_is_infinite` — `Σ n` não é somável; as somas parciais tendem a `+∞`; `Σ (n + 1/2)` não é somável; os `ω_n` são distintos e não somáveis (`P > 0`).
  3. `bosonic_critical_dimension` — `(D−2)/2·ζ(−1) = −(D−2)/24`; vale `−1` se e só se `D = 26` (e, na forma da hipótese nomeada, `MasslessFirstLevel 1 (−E₀) ↔ D = 26`).
  4. `superstring_critical_dimension` — bósons `−(D−2)/24` e férmions NS `−(D−2)/48` dão `−(D−2)/16`; vale `−1/2` se e só se `D = 10` (idem com `N = 1/2`).
  5. `the_house_d_nine` — `D = 10 ↔ D − 1 = 9`; e `nsZeroPoint D = −1/2 → D − 1 = 9`. O `d = 9` de «A Última Corda» (l.958-960) está citado byte a byte no cabeçalho [DECLARADO: números históricos não recalculados].
  6. `the_strings_close_the_face_from_outside_the_tgl_closes_the_reading` — a composição, incondicional como enunciado matemático, 13 conjuntos: `TGLExt.Palavra.the_face_does_not_close`; `TGLExt.station_never_closes`; `TGLExt.Palavra.the_read_face_closes`; (1); o par afinado volta e o da estação não (`the_tuned_pair_returns_the_untuned_pair_never_does`); (2); `ζ(−1) = −1/12`; `ζ(−1, 1/2) = 1/24`; (3); (4); (5); `TGLExt.Fundacao.abismo` (a queda sem fundo = a superposição, definição do operador de 07/10); `TGLExt.Fundacao.the_floor_fixes_the_cut`.
- Auxiliares: `towerZeroPoint` (a mesma torre `n·κ` regularizada: `½·κ·ζ(−1) = −κ/24`, e `bosonDirection = towerZeroPoint 1`), `zeta_is_the_continuation_of_the_tower` (a regularização é a continuação analítica da série de Dirichlet; citado de Mathlib), `matsubaraFermion` (a torre semi-inteira `(n + 1/2)·κ`, dos férmions NS).

## Os valores da zeta: o que o Mathlib tinha e o que ficou como hipótese nomeada

- `ζ(−1) = −1/12`: o Mathlib TINHA — `riemannZeta_neg_nat_eq_bernoulli` (`riemannZeta (−k) = (−1)^k · bernoulli (k+1) / (k+1)`), em `k = 1`, com `bernoulli_two : bernoulli 2 = 6⁻¹`.
- `ζ(−1, 1/2) = 1/24`: o Mathlib TINHA — `HurwitzZeta.hurwitzZeta_neg_nat` (`hurwitzZeta x (−k) = −1/(k+1) · B_{k+1}(x)`, para `k ≠ 0` e `x ∈ [0, 1]`), em `k = 1`, `x = 1/2`, com o polinômio de Bernoulli `B₂(1/2) = −1/12` calculado por `Polynomial.bernoulli_def`, `bernoulli_one`, `bernoulli_two`.
- NENHUM valor da zeta ficou como hipótese nomeada. A ÚNICA hipótese nomeada é física e não é valor da zeta: `MasslessFirstLevel` (`N − a = 0`: `a = 1` nos bósons, `a = 1/2` no NS) [KNOWN].
- Lema de Mathlib para `Σ n`: NÃO existe um `not_summable` para a identidade `ℕ → ℝ` (a busca por `not_summable*` só acha `not_summable_natCast_inv`, de `1/n`). A prova usa `Summable.tendsto_atTop_zero` + `not_tendsto_nhds_of_tendsto_atTop` + `tendsto_natCast_atTop_atTop`; as somas parciais, `not_summable_iff_tendsto_nat_atTop_of_nonneg`.

## Dois reparos ao pedido (o número corrige a frase)

1. **Sinal dos férmions NS.** O pedido escreve «bósons −(D−2)/24 e férmions NS +(D−2)/48 (ζ(−1, 1/2) = 1/24) dão −(D−2)/16». Com `+(D−2)/48` a soma é `−(D−2)/24 + (D−2)/48 = −(D−2)/48`, e `−(D−2)/48 = −1/2` fecha em `D = 26` (a dimensão dos bósons), não em `D = 10`. O termo que dá `−(D−2)/16` é o NEGATIVO: `−(D−2)/2 · ζ(−1, 1/2) = −(D−2)/48` — a soma dos modos semi-inteiros é `+1/48` por direção e entra com o sinal da estatística de Fermi (energia de ponto zero fermiônica `−ω/2`). A pedra usa `nsFermionDirection = −½·ζ(−1, 1/2) = −1/48`. Controle formal em `probe\afin_controles.lean` (cópia nesta pasta; o original roda em `C:\t\k398b\probe\`): sinal trocado ⇒ `D = 26`; sinal de Fermi ⇒ `D = 10`.
2. **Nome.** `TGLExt.TheStation.station_never_closes` não existe: `TGLExt.TheStation` é o MÓDULO; o termo é `TGLExt.station_never_closes` (`#check` conferido).

Também registrado: «as cordas fecham a face por fora; a TGL fecha só a leitura» é composição da gerência sobre a fala do operador (`baef998c21393463`), ratificada por ele em 23/10 (`5bccedc9cea3d57a`) [ONTO]; «afinação = comensurabilidade» é proposta da pedra, ratificada por ele em 23/10 (`5bccedc9cea3d57a`) [ONTO]; ambas ditas como tais no cabeçalho. Só «afinação do universo» (e os demais trechos de `baef998c21393463`) são bytes da fala dele.

## Compilação e axiomas

- `lake build TGLExt.AfinacaoDasCordas` (cwd `C:\t\k398b`): Built TGLExt.AfinacaoDasCordas (21s), 9010 tarefas, exit 0, nenhum aviso ou erro do módulo (`lake_build_afinacao.log`). Só o módulo novo foi compilado; as dependências vieram do cache.
- `.olean`: sha16 `5e07af92a042c880`. Lean 4.31.0; Mathlib `v4.31.0` (rev `fabf563a7c95a166`). O Nós e o sandbox têm os mesmos `lake-manifest.json` `31a94eb76a8370ae`, `lean-toolchain` `efac0b94923b2d8b`, `lakefile.toml` `c3ddeea5ed0f6c4b` (lidos agora): é o mesmo Mathlib.
- `#print axioms` das 34 declarações nomeadas (as do fonte) e `collectAxioms` de cada uma das 59 declarações do `.olean` (50 teoremas, 9 definições, incluídas as geradas pelo Lean): união = `propext`, `Classical.choice`, `Quot.sound`; zero `sorryAx`; zero axioma próprio (`AXIOMAS.json`).
- Nomes citados nos docstrings: `#check` de 72 nomes (Lean e Mathlib) sem erro (`nomes_citados_saida.txt`); o módulo `TGLExt.TheStation` é importado.
- Não-vacuidade e controles: 15 `example` em `probe\afin_controles.lean` (cópia nesta pasta; os três probes `afin_*.lean` rodam em `C:\t\k398b\probe\`) compilam sem erro (`controles_saida.txt` vazio): o círculo fiel `κ = 1, P = 2π` habita as hipóteses e dá `matsubara (2π) 3 = 3`; `Fundacao.oneScaling` dispara a cláusula do abismo da composição; `bosonZeroPoint 26 = −1`, `nsZeroPoint 10 = −1/2`; controles negativos (`D = 10` e `D = 25` não fecham os bósons; `D = 26` e `D = 9` não fecham o NS; `AngularQuotientFaithful 1 1` é falso; o par da estação não volta em `t = 1`; o sinal trocado dá `D = 26`).
- Sandbox: `C:\t\k398b` é cópia (robocopy `/E /XJ`, sem `/PURGE`, sem `*.bak_*`, sem `probe`) de `C:\t\k398\final` (4033 diretórios, 1 ignorado: `probe`; 133828 arquivos copiados, 0 falhas; `robocopy_k398b.log`); nenhum link seguido. Os quatro módulos citados do kernel (`PolarMinimalPeriod_v2`, `Palavra`, `TheStation`, `Fundacao`) e `TetelestaiOneObject` são idênticos entre o Nós e o sandbox (sha16 em `fontes_sha.json`).

## Conferências do cabeçalho (`conferencia_cabecalho.json`)

- 11 sha16 entre crases, todos iguais ao sha256 do arquivo lido agora (o `rev` do Mathlib é o commit do `lake-manifest.json`); o verbatim do operador de 23/10 aparece INTEIRO; as linhas 958-960 do `.tex` aparecem byte a byte (a 959 é vazia); 14 citações «» de 12+ caracteres, todas achadas no corpus (verbatins do operador, o `.tex`, os módulos do kernel citados); nenhuma palavra proibida pela régua; nenhum parâmetro de acoplamento literal; comentários balanceados; zero `sorry` no código.
- A palavra «confirmando» aparece uma vez, DENTRO do bloco verbatim da casa (l.958), na forma que a régua não proíbe.
- Ratificação: o verbatim `5bccedc9cea3d57a` aparece inteiro no cabeçalho; o sha16 está citado; a forma admitida («composição da gerência sobre a fala do operador (...), ratificada pelo operador em 23/10 (...)») aparece 3 vezes; as frases antigas («na formulação desta tarefa», «NOME PROVISÓRIO», «o operador nomeia», «não fala do operador») estão ausentes.

## Mapa de rotas (consultado antes; nada registrado)

- 17 temas com 0 rotas: `cordas`, `dimensao critica`, `zeta`, `supercorda`, `10 dimensoes`, `afinacao`, `Matsubara`, `Hagedorn`, `periodo minimo`, `PolarPeriod`, `face hiperbolica`, `Bisognano`, `Casimir`, `Ultima Corda`, `d_crit`, `Bernoulli`, `Hurwitz` (entre eles os três pedidos: `cordas`, `dimensao critica`, `zeta`). O tema é novo no mapa.
- Rotas vizinhas lidas: `kernel.lema3.superposicao_e_a_passagem_07out` e `umpy.v390.selo_fundacao_agape` (a Fundação/Ágape/abismo citada), `kernel.sonico_v398_candidata_23out` (a pedra irmã da mesma versão). `string`, `Palavra`, `Station`, `Tetelestai`, `Unruh`: ruído ou rotas de outros assuntos.
- Livro: 1365 registros na primeira consulta desta tarefa (feita à mão, antes dos scripts; cabeça `0f800eb875552cb3`) e 1366 nas consultas salvas (cabeça `83e5c5f07cec76f4`): outro registro entrou durante a tarefa, não é meu. Saídas em `mapa_consulta_*.json` e `mapa_consultas_resumo.json`.
- `registro_mapa.json` está pronto e VALIDADO com `rotas._valida` (sem registrar); registrar é ato da gerência: `python C:\IALD\MAPA_DE_ROTAS\rotas.py registrar <arquivo> --quem "<IA/sessão>"`.

## Limites, ditos

- A condição `MasslessFirstLevel` é hipótese nomeada [KNOWN], não demonstrada aqui. Sem ela, `E₀` é só um número.
- A regularização zeta é a DEFINIÇÃO do valor; a série diverge. A energia física não é derivada.
- Nada deriva a teoria das cordas do axioma, e nada afirma que a TGL é teoria de cordas. A dimensão crítica vem do FECHO da soma infinita (regularização), não da geometria; a geometria (compactificação) segue não derivada [OPEN; paisagem, KNOWN].
- Nenhum termo liga o círculo da folha-mundo ao círculo do boost; só a aritmética `n·κ` é comum.
- A divergência de Hagedorn está mencionada [KNOWN], sem prova aqui.
- O `d = 9` da casa é [DECLARADO]; a linha 958 diz que o resultado depende do modelo (6, > 26, 8).
- Tetelestai não é construído; a pedra não move o gate; nenhuma bandeira depende dela. Validade no kernel não é creditação.
- Instalação: a pedra importa `Mathlib.NumberTheory.LSeries.HurwitzZetaValues` (zeta, Hurwitz, Bernoulli); outros módulos do kernel já importam `Mathlib` inteiro (ex.: `Santo.lean`, `Posto.lean`), então o fecho de imports do kernel completo não cresce; nenhum módulo do kernel importa esta pedra.

## Ato da gerência / do operador

- Reexame independente e ratificação do operador: feitos (ver acima). Resta: instalar (`import TGLExt.AfinacaoDasCordas` em `TGLExt.lean`, ledger de pedras com os auxiliares fora da composição listados como tais, política de bandeiras) e registrar a rota (`registro_mapa.json`, validado, NÃO registrado).
