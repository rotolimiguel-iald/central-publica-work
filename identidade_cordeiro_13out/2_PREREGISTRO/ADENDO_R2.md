ADENDO R2 AO PRÉ-REGISTRO — F1.IDENTIDADE — 13/10/2026 (construtor da rodada 2, gerência c1, em nome próprio)

Arquivo NOVO, ao lado. `PREREGISTRO.json` (sha256 207aa703…) e `FREEZE.json` (sha256 582cfbe8…) da r1 ficam intocados.
O texto normativo deste adendo é `ADENDO_R2.json`; o congelamento é `FREEZE_ADENDO_R2.json`, gravado ANTES de a pedra r2
existir. Havendo divergência, vale o .json. Entre aspas angulares só trechos do operador, conferidos nos bytes.

Pedido de origem: auditoria cética c1 a414e21b (`C:\IALD\PROGRAMA_IALD\auditorias\F1.IDENTIDADE\`), achados R1–R10.

## Ao lado da FALHA I6.b da r1

A FALHA I6.b fica registrada como resultado da r1. ERRATA AO LADO do motivo: o pré-registro r1 disse que "faltaria uma
esperança condicional / semigrupo dissipativo em B(H_φ)". Isso foi dito sem consultar o kernel e era FIAÇÃO, não FALTA.
O kernel instalado do Nós já tem `ChatgptAudit.Aperiodic046.aperiodicExpectationInput` (AperiodicCentralizerExpectation.lean
l.129), `ChatgptAudit.Orbit052.aperiodic_pauli_x_zero` (LocalHorizontalPauli.lean l.98) e `TGLExt.towerIALD`
(TheSelectionIsTheBallast.lean l.86, v335). O posto LITERAL de P_v em B(H_φ) segue [OPEN].

## Afirmações novas

* **I6.b′** — a negativa de I1 NA TORRE pela esperança aperiódica: A = q·1 + α·σ_x ∈ M, AΩ = qΩ + αξ; para w(0) ≠ 1/2,
  E_aper(A) = q·1 (o eixo interior é apagado), ω(E_aper A) = ω(A), ⟨ξ, AΩ⟩ = α e ⟨ξ, E_aper(A)Ω⟩ = 0, e E_aper(A) ≠ A
  para α ≠ 0. O mesmo pela `towerIALD` (recognize). Ler isto como "o posto 1 não permanece na torre" é [INPUT da gerência].
* **I6.c** — a mesma identidade também na `towerIALD` (ω(I) = 1 lido; 1 reconhecido como 1; o reconhecimento recursivo
  devolve a leitura; a inscrição tem vetor unitário e ω lê q antes e depois do reconhecimento), MANTENDO I6.a em
  `TowerHilbert`. A pedra oferece as duas; qual é a Torre da ordem («dentro da Torre») é decisão do operador.
  `NamedIdentity` ganha o campo `in_the_IALD_tower`.
* **I3.c′** — `rereading_reads_the_same`: a forma do motor r3 (a LEITURA não muda), da idempotência mais a auto-adjunção.

## Controles novos

* **C2′** `dephasing_fixes_the_poles` — o termo que faltava para "nos polos a defasagem não muda P".
* **C6** `the_inner_reading_is_by_construction`, `the_inner_reading_at_five_is_not_an_identity` — a leitura interior é
  α·α para todo real; em α = 5 (TESTE) dá 25 com traço ≠ 1.
* **C7** `probe_IALD_tower` — não-vacuidade de I6.b′/I6.c num perfil não tracial de TESTE (w ≡ 1/3), α = 1/2 de TESTE.

## Renomeações (R2, R3) e critério de manutenção

`inscription → quadInscription`, `towerInner → towerInnerAxis` e os lemas que carregam esses nomes;
`rereading_adds_nothing → post_is_idempotent_on_the_vector`. Qualquer outra colisão medida é renomeada e declarada.
Toda declaração da r1 fora das mudanças previstas mantém o tipo (Expr.eqv e Expr.equal, depois do mapa de nomes; para
definições, também o valor). Mudanças de tipo previstas: só `NamedIdentity.mk` e os geradores da estrutura (campo novo);
`ofName` muda de valor.

## Docstrings (R5, R6, R7, R9, R10)

R5: a leitura interior é [REAL, por construção]; o traço 1 exige q² + α² = 1; "medido por dentro" é [ONTO] (leitura do
operador). R6: identidade = TRAÇO (I1; não fixa α) × PROJEÇÃO (I2/I3; determina α). R7: a frase "α fora de (0,1) quebra a
forma" é da gerência (C3), não do verbatim. R9: [ONTO]/[POSTO]/[INPUT] em linha. R10: Nome da casa (post v / ω) ×
`NamedIdentity.name : String`.

Critérios: EXIT 0; 0 "declaration uses `sorry`" com controle positivo; collectAxioms de todas as constantes no trio;
impressão digital do tgl_kernel antes = depois; homônimos zero; tabela r1→r2; parametricidade do Nome; citações nos bytes.
Nada move o gate; validade no kernel não é creditação.
