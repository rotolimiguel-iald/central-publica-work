MOTOR R3 — 13/10

# Pedra `TGLExt.IALD` («o motor único», nome provisório), rodada 3: só docstrings e comentários

Construtor da rodada 3, gerência c1, programa IALD. O pedido vem da reauditoria c1 `a4a8fb5f`
(`C:\IALD\PROGRAMA_IALD\auditorias\F1.MOTOR\AUDITORIA_F1_MOTOR_C1_a4a8fb5f.md`), que aprovou a r2 com ressalvas.
Nada foi instalado e o gate não se move. Todos os números abaixo foram lidos dos artefatos por script (`RECIBOS_R3.json`).

## 1. Fontes e binários [REAL]

| | sha256 |
|---|---|
| fonte r2 (base, conferida antes de copiar) | `9b0e9260b208beef05342a04cadc8a8812dca3b620dcdbc5b8fbd4dd9708d268` |
| fonte r3 `fonte\TGLExt\IALD.lean` (786 linhas) | `d7c1f1d3b03e6095b661db1efe0c8ebecdf5624c47d0ea8deccaeafaaec2fc80` |
| `.olean` r3 `olean\IALD.olean` (1.090.096 bytes) | `5856f7f6ea78dcc6d16343c879c78ef32b29ad54ed89e57831d2ecb1463bfdee` |
| `.olean` r2 recompilado no mesmo sandbox | `d37804a344beb186…`, igual bit a bit ao da r2 |

O `.olean` mudou porque docstrings e posições de declaração entram nele. Tipos e termos não mudaram (§3).
As quatro candidatas pinadas pela r2 foram compiladas no sandbox antes da pedra. Os `.olean` delas saíram iguais bit a
bit aos da r2: PALAVRA `d52ebd0943e96192`, ADENDO1 `8cf8b1726c588cac`, `TheUnitIsTheRank` r3 `6364ea0b0c43e512`,
`TheTimeIsNotAPost` R2 `3e591a5b494ed315`. As quatro compilaram com EXIT 0, 0 erros e 0 sorry.

## 2. O que mudou: só texto

| achado da reauditoria | onde na r3 | o que diz agora |
|---|---|---|
| **M-1** (MÉDIA), docstring de T2 | `motor_idempotent_under_anchor` | A hipótese é o binder `hU : U a = a`, e não existe constante `Anchor`. `anchoring_preserves` (`F(t)·P = P`) é a ancoragem do FLUXO, outro objeto, e o termo não a usa. Na luz, `hU` vem de `Γ_vac` (SONDA 2). |
| T3′ não prova traço | `the_name_has_rank_one` | Saiu «Tr Π = 1 = ω(I)» do título. Ficou só imagem = ℂ∙a de dimensão 1. A leitura do posto 1 como ω(I) = 1 está marcada [ONTO]. Por termo, traço só aparece na face matricial (B8(ii), ρ*). |
| T4 sem motor no enunciado | `the_name_reads_one` | O título passa a «a memória do Nome no próprio Nome é 1». O motor não aparece no enunciado. «O motor lê o Um» fica marcado [ONTO], com apoio em T3. |
| título da seção 4 | módulo-doc da seção 4 | S1 é concreta (ℓ²), S2 é condicional ao certificado C (sem habitante no kernel) e S3 é universal em `c : TGLCoupling`. |
| homônimo `reading` | cabeçalho (novo item R3), `memory`, PONTE 3, B4, B5 | (a) `reading P ψ = ⟪ψ, Pψ⟫` é escalar (`TheVerbSelectsTheAction.lean:182`). (b) `TheSingularityReadsTheAttractor.reading T` é o operador projeção do espaço fixo. Nenhum lema iguala os dois. |
| «único» sem termo de unicidade | título do cabeçalho | Marcado [ONTO] como parte do nome provisório. Nenhum termo prova unicidade. |
| cabeçalho do ensaio diz «unitario U» | `numerico\ensaio_motor_r3.py` | Agora diz «transporte U (qualquer operador linear; a pedra NÃO exige U unitário)» e lista os U ensaiados. |
| observação do auditor (U unitário × isométrico) | NOTA R3 (`/-! … -/`, comentário) após `phase_is_unitary`, e remissão no item C1 do cabeçalho | Com U sobrejetivo e isométrico e ‖a‖ = 1, a idempotência força `U a = a` (sonda do auditor `c1_unitary_forces_strong_anchor`). Com U só isométrico, não força: a imagem pode ser ⊥ a, como no deslocamento unilateral de ℓ² [KNOWN, não construído]. A decisão é do operador. **Não é teorema da pedra.** |

Também foi corrigida a remissão do comentário de B8, que dizia «o motor devolve posto 1».
O cabeçalho ganhou o parágrafo R3. O parágrafo R2 ficou como registro.
Nenhuma citação nova foi atribuída ao operador. As aspas «…» novas citam o texto da r2 ou da auditoria.

## 3. Prova de invariância lida do kernel [REAL]

Método: r2 e r3 foram compiladas no **mesmo** sandbox `C:\t\mo3`, com o lean v4.31.0 copiado e conferido e o LEAN_PATH
apontando primeiro para a cópia verificada do `.lake/build` do Nós e depois para os pacotes, só leitura. O `.olean` r2
foi afastado antes de compilar a r3. Para cada constante do módulo, lida de `env.header.moduleData[idx].constNames`,
`scripts\Meta_TEMPLATE.lean` grava:
- espécie, parâmetros de universo, `isInternal`, hints/safety e axiomas (`collectAxioms`);
- TIPO e VALOR serializados de dois modos: SA, em De Bruijn sem nomes de binder, e SN, com nome e info de cada binder;
- o hash da docstring.

`scripts\comparar_r2_r3.py` compara as **strings inteiras**.

Resultado (`TIPOS_R2_VS_R3.json`):
- 69 constantes nas duas rodadas, na mesma ordem: 62 públicas, 6 internas (`dephase._proof_1..4`, dois `_abel_1_1`) e
  o lema de equação `TGLExt.IALDJones.jonesReading.eq_1`.
- **69/69 idênticas em tipo e termo no modo SA, e 69/69 também no modo SN.** Mesmo os nomes de binder, inclusive os
  higiênicos, são iguais. A ressalva «módulo nomes higiênicos» não precisou ser usada.
- Espécie, universos, hints e axiomas também são iguais. Veredito do script: `INVARIANTE_100_POR_CENTO`, 0 falhas.
- A docstring mudou em exatamente 7 constantes, as 7 editadas: `memory`, `motor_idempotent_under_anchor`,
  `motor_is_the_reading_of_the_attractor`, `reader_eq_reading`, `the_name_has_rank_one`, `the_name_reads_one` e
  `the_singularity_reads_the_name`. As outras mudanças estão em módulo-docs (`/-! -/`), que não são constantes.
- Diff textual (`DIFF_R2_R3.diff`, Lean +66/−13). Com todos os comentários removidos, inclusive os blocos aninhados,
  `/--` e `/-!`, o código r2 e o r3 são idênticos (`medidas\DIFF_SO_COMENTARIOS.json`, sha do resto
  `fec42771f853006e…` nos dois).
- Os 10 avisos de compilação (deprecações) são os mesmos nas duas rodadas, salvo o número da linha.
- Os dumps do kernel ficaram comprimidos em `meta\meta_r2.txt.gz` e `meta\meta_r3.txt.gz`. Os 123 MB descomprimidos
  não foram mantidos.

`#print axioms` das 69 constantes da r3 (`scripts\PrintAxiomsR3.lean`, recibo `logs\printax_r3_RECIBO.json`):
69 impressos e 0 fora do trio {propext, Classical.choice, Quot.sound}. Só `jonesReading.eq_1` não depende de axioma
nenhum. Houve 4 avisos do linter `auxLemma` por citar `_proof_n`, sem efeito no resultado.

## 4. Ensaio numérico [REAL; sanidade matemática, nenhum dado observado]

O cabeçalho mudou, então o ensaio foi refeito: `numerico\ensaio_motor_r3.py`. O diff contra o r2 está só no docstring
e no nome do arquivo de saída. Resultado: **112/112 PASSA**, 242 folhas, e só `quando_utc` difere da r2
(`medidas\ENSAIO_R2_VS_R3.json`). β = 0.012031300400803142 = α·√e, com α lido nos bytes da l.5557 do `um.py`
(sha256 `8e7b9927ceae64b8…`). O `um.py` não foi executado.

## 5. Higiene [REAL]

- Impressão digital do `tgl_kernel` do Nós antes e depois, por receita que **não segue junções** (`scripts\digital.py`;
  a junção `.lake/packages` é listada e não é atravessada; 11.049 arquivos). Tudo igual: metadados `42953f27bcd15ba2…`,
  fontes `22557eadef61ef50…`, `.olean` de TGLExt `aef5f8dcd469aa79…`.
- Sandbox: `toolchain/` e `ov/` foram apagados ao final, e não há `.lake` em `C:\t\mo3`. Restam só as fontes curtas e
  os `.lean` de leitura (368 KB).
- Não escrevi nada no Nós, no `um.py`, no quadro, no mapa, na memória, no túnel, na Bancada, no site ou no git.
- A palavra proibida da régua não aparece em nenhum dos arquivos de texto desta pasta (varredura em `RECIBOS_R3.json`).

## 6. O que NÃO fiz

- Não registrei no mapa. Só deixei a proposta `registro_mapa_F1.MOTOR_R3.json`.
- Não inscrevi esta tarefa na memória ACOM (`session_memory.py`), porque a unidade proíbe escrever na memória.
- Não corrigi os relatórios: C6 no relatório, «Q16/Q17 resolvidas», «EU SOU = IALD como termo», a frase sobre isometria
  e a premissa da pergunta 3. Essas correções são da gerência, ao lado.
- Não reaudito a mim mesmo: a r3 ainda não foi conferida por terceiro.
- Não refiz a coexistência com o `TGLExt` inteiro nem o fecho transitivo de usos (C3). Pela invariância de termo, os
  usos são os mesmos da r2, mas isso não foi remedido aqui.
- Não construí o deslocamento de ℓ² em Lean nem promovi a NOTA R3 a teorema.
- Não decidi P2 (Π_N := `post a`), P3 (U unitário por tipo), P4 (`DualScalingData`) nem P6 (nome e entrada na v392).
  Essas decisões são do operador.

## 7. Estatuto

A pedra r3 é a r2 com o texto corrigido. É [REAL] como termo no trio, contra o kernel v391 só leitura, e segue
**não instalada**. É validade (fecho lógico na face do posto), não prova distintiva: a saída do motor não depende de β.
A creditação é do observador humano. O único elo pendente da QG segue sendo β_TGL na natureza a 5σ.
