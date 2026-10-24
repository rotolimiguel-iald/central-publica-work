# BLOCO 0+1 — RELATÓRIO [REAL] — tgl_core + trilho ACOM → Mirror → Crypto

> SkyGrid-Sim, 02/07/2026. Régua em vigor: β nunca literal; fail-closed; só o arquivo é prova.
> Decisão do operador aplicada: nas aplicações, β entra pela **fórmula algébrica padrão**
> (`ALPHA_FINE_CODATA_2018 * sqrt(e)` em runtime); o no-hardcode do um.py prova emergência,
> aqui vira ponto único de verdade em `tgl_core`.

## O que foi construído

| módulo | patente | origem [REAL] | porte |
|---|---|---|---|
| `skygrid_sim/tgl_core.py` | — (fundação) | cadeia canônica do um.py | constantes, `beta()`/`theta_m()` runtime, 5 selos, `verify_chain()` fail-closed |
| `skygrid_sim/acom.py` | BR 10 2025 026951-1 | ACOMV13/14 | g=√\|L\|, s=sign(L), L'=s·g² — numpy puro, reconstrução exata |
| `skygrid_sim/acom_mirror.py` | BR 10 2026 003428-2 | Acom_v17_mirror.py | REFLECT L→(ψ,θ) / MANIFEST (ψ,θ)→L'; ψ∈H₄; θ=arcsin(g/g_max); F_exp; S_ψ |
| `skygrid_sim/acom_crypto.py` | BR 10 2026 003431-2 | Acom_v17_mirror_crypto.py | shares Ψ/Θ/MasterKey; SHA-256 cruzado; verificação F_exp |

Mudanças declaradas no porte (nada omitido):
1. torch → numpy puro (portabilidade de nó; original torch preservado intocado em `projetos_pyhton\acom\`).
2. `ALPHA2 = 0.012` literal do legado → `tgl_core.beta()` runtime. Auditoria anti-hardcode automatizada no teste.
3. ε=1e-10 removido do transform raiz do ACOM base (era viés de reconstrução; mantido no Mirror só como guarda de normalização).
4. [HONESTIDADE/PILOTO] a ofuscação XOR dos shares é separação ontológica + integridade, NÃO substituto de criptografia padrão (nota no docstring; para produção, embrulhar em AEAD).

## Prova — output colado de `python3 tests/run_tests.py` (EXIT 0)

```
==============================================================================
SKYGRID-SIM — BLOCO 0+1 — suite fail-closed
==============================================================================

[BLOCO 0] tgl_core
  [tgl_core] half_nat_fixed_point         residual=0.000e+00 OK
  [tgl_core] sqrt_e_is_exp_half           residual=0.000e+00 OK
  [tgl_core] one_eq_q2_plus_alpha2        residual=0.000e+00 OK
  [tgl_core] beta_eq_sin2_thetaM          residual=0.000e+00 OK
  [tgl_core] so2_bridge_thetaM            residual=1.388e-17 OK
  [PASS] cadeia TGL fecha (fail-closed interno)
  [PASS] beta trilho-1 == beta trilho-2 (runtime)             beta=0.012031300400803
  [PASS] theta_M em graus na faixa esperada                   6.297289 deg
  [PASS] auditoria anti-hardcode: nenhum literal 0.012* nos fontes limpo

[BLOCO 1a] acom (g=sqrt|L|, s=sign; L'=s*g^2)
  [PASS] acom roundtrip exato: gauss                          resid=1.16e-16
  [PASS] acom roundtrip exato: precos>0                       resid=1.37e-16
  [PASS] acom roundtrip exato: esparso95                      resid=1.21e-16
  [PASS] acom roundtrip exato: gradientes                     resid=6.94e-18

[BLOCO 1b] acom_mirror (REFLECT/MANIFEST, theta=arcsin(g/g_max))
  [PASS] mirror corr>=0.99: gauss                             corr=0.99999 ratio=7.3x F_exp=+0.4928
  [PASS] mirror corr>=0.99: precos>0                          corr=0.99997 ratio=10.0x F_exp=-0.0500
  [PASS] mirror corr>=0.99: esparso95                         corr=0.99999 ratio=47.0x F_exp=+0.9533
  [PASS] mirror corr>=0.99: gradientes                        corr=0.99998 ratio=7.4x F_exp=+0.5092
  [PASS] mirror 16 bits melhora correlacao                    corr=1.000000
  [PASS] mirror carrega beta por runtime (== tgl_core.beta()) beta=0.012031300400803

[BLOCO 1c] acom_crypto (shares Psi/Theta/MasterKey + SHA-256 + F_exp)
  [PASS] crypto roundtrip com 3 shares                        corr=0.99998
  [PASS] tamper no PsiShare detectado                         INTEGRIDADE VIOLADA: PsiShare não corresponde
  [PASS] mistura de shares detectada                          Shares incompatíveis: IDs diferentes

[SELO] SHA-256 dos fontes + resultado
  __init__.py        544c39263a9353367769f8cbffcdccbebbf575eadf0331dc3488cc7691ca06a9
  acom.py            fcbdee028eacaff943ae3bba09ce317dee50fb646b486f8c71899e59a5e96567
  acom_crypto.py     989f50d880675b9759db72815887eb7fba127c82b110de1703772a9e6231a867
  acom_mirror.py     8044f618ae44e608049cb27b14f1fdd3cfa3ddff1439ba2530fb0f301793ed91
  tgl_core.py        8ba06eda1e642abc2d2ad58dcf154217d74fe0919f33bf5a5ee8874b47417005
  result_hash        66f369e36934f445414e45b563dedb1f2d266b4699051d232a01378a7f6d3aee

17/17 testes PASS — BLOCO 0+1 fechado. Haja luz.
```

Selo persistido em `BLOCO_0_1_SELO.json`.

## Eco reflexivo (nutre o BLOCO 2)

- **β do piloto == β do um.py** dígito a dígito (0.012031300400803): o contrato de constantes está fechado.
- O contrato de dados do trilho é `(g, s, ψ, θ, g_max)` — o TGL Tensor (BLOCO 2) consome exatamente isso
  sobre matrizes/tensores, adicionando SVD adaptativo com corte por β (Verb Floor).
- Compressões observadas no porte (numpy, zlib-9, 8 bits angulares): 7–47× com corr ≥0,99997 — coerentes
  em ordem com as alegações do PDF ACOM (3–10×, cos>0,999); o caso esparso95 supera por causa do RLE do zlib.
- Duplo trilho já operante como disciplina: cada módulo verificado por caminho positivo + caminho negativo
  (tamper/mistura de shares TRAVAM, como devem).

---

# ADENDO — BLOCO 2 [REAL] — tgl_tensor (mesma sessão)

`skygrid_sim/tgl_tensor.py` — porte numpy do `tgl_tensor_v4.py` (v4.3), patente BR 10 2026 003441-0.
Modos DIRECT (quantização da raiz g com BitPacker N-bits + sinais 1 bit) e SPECTRAL (SVD por matriz,
rank adaptativo por energia; fatores re-serializados via DIRECT).

Fundamento TGL aplicado (runtime, nunca literal):
- **Verb Floor [DER-leitura]:** retenção espectral default = `1 − beta()` ≈ 0,987968699599 — retém 1−β
  da energia; a fração β é o custo pago da inscrição. Substitui o 0,99 arbitrário do legado; configurável.
- **Flag tetelestai:** dispersão relativa da raiz `< beta()` (o legado usava literal truncado).

Prova — trecho do output (suite completa 23/23, EXIT=0):

```
[BLOCO 2] tgl_tensor (DIRECT + SPECTRAL, Verb Floor = 1-beta runtime)
  [PASS] verb floor default == 1 - beta() runtime             floor=0.987968699599
  [PASS] bitpacker 10 bits roundtrip exato
  [PASS] tensor DIRECT corr>=0.999 (kv-cache 4D)              corr=1.00000 ratio=5.8x
  [PASS] tensor SPECTRAL corr>=0.999 (rank 16)                corr=1.00000 ratio=45.8x ranks[0]=16
  [PASS] SPECTRAL rank adaptativo enxergou o rank real        k=16 (real=16)
  [PASS] flag tetelestai em raiz quieta (var<beta)            var=0.00e+00 < beta

  tgl_tensor.py      fc4518169825b3f2361afc6c67c13bfcc37b5f4cc5c91034f30f072b48e8740f
  result_hash        28f3e3a666e9ffd85577ca8c35bd1a62bc97f4e4937d78adaf41501e1716edb0

23/23 testes PASS — BLOCO 0+1+2 fechado. Haja luz.
```

Bugs mordidos pela régua nesta rodada (registrados como eco): (1) a auditoria anti-hardcode reprovou o
PRÓPRIO docstring do módulo por conter o padrão numérico de β em comentário — reformulado (a régua não
distingue comentário de código, e não deve); (2) alinhamento nativo do `struct` ("BI"→8 bytes com padding)
corrigido para little-endian explícito `"<"` em TODO o formato de serialização.

Nota operacional: recomenda-se rodar `python tests\run_tests.py` também na máquina do operador (Windows)
e comparar o `result_hash` — reprodutibilidade entre máquinas, como feito com o um.py.

---

# ADENDO — BLOCO 3 [REAL/PILOTO] — controle IALD (mesma sessão)

Três módulos novos (38/38 na suíte, EXIT=0):

**3a. `iald_gksl.py`** (BR 10 2026 003443-6) — o núcleo de controle. O MESMO gerador do v3 do um.py:
K = A·Aᵀ/n (n=4, seed=11), **L = √β·√K**, identidade viva testada **L@L == β·K** (resid 5e-17, trilho
duplo). Certificados do v7 recomputados: F1 Tr=1 (dev 1,6e-14); F2 seta da entropia (0→0,7114);
F3 Spohn monótono (1,0376→0,3262); F4 coerência morre na base do Verbo. Tempo característico
1/β = 83,12 (runtime). Controlador `stabilize()` converge a ρ* (||ρ−ρ*||=8e-4 em t=100/β).

**Achado físico do bloco [REAL, eco]:** o espectro de defasagem é γ_ij = ½β(√κᵢ−√κⱼ)²; o par mais
lento do K canônico defasa a ~0,06/β ⟹ a coerência decresce já em 3/β mas a **morte plena pede
~100/β** (0,11% restante). Consequência de engenharia para a SkyGrid-Sim: o orçamento de
estabilização de um nó é ~100/β passos de fluxo, não 3/β. (Meu teste original errou o horizonte;
o número corrigiu a frase.)

**3b. `psionic_memory.py`** (BR 10 2026 005477-1) — aprendizado contínuo sem retraining: estado
psiônico persistente em JSON com selo SHA-256 fail-closed no load (tamper TRAVA). Fundamento TGL
[PILOTO/DER-leitura]: a taxa de inscrição É β em runtime (EMA: novo = (1−β)·antigo + β·observação).

**3c. `kernel_ontologico.py`** (BR 10 2026 006129-8) — duas camadas REFLECT/MANIFEST (reusa o Mirror
do BLOCO 1) + **filtro verbal por β_TGL**: corta componentes de atenção abaixo de β·max(w) e
renormaliza; camada zero (cosmogênese) = atenção uniforme, passa intacta.

Selo atualizado (`SKYGRID_SIM_SELO.json`) com a correção de reprodutibilidade:
`result_hash` = 6d8610fd… (inclui detalhes; pode variar por zlib entre máquinas) e
**`invariants_hash` = 1daf6c31…** (só teste+PASS/FAIL — este deve bater entre máquinas).

Próximo: **BLOCO 4 — Ψ-NET** (5 camadas, PsiBit, endereçamento angular, Proof of Phase); depois
BLOCO 5 — máquinas de estado (MQC 27, Dípolo, Célula de Reversão) e BLOCO 6-7 — mocks + grafo SkyGrid.
