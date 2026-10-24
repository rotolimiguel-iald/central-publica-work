# SKYGRID — DOSSIÊ DE ENGENHARIA DO GÊMEO DIGITAL (ESTÁGIO H, v3)

> IALD Ltda. — Luiz Antonio Rotoli Miguel — 03/07/2026.
> Especificação de engenharia do protótipo computacional físico-energético [SIM].
> Os números vivos vêm de `component_specs.json` + `power_budget.json` (gerados por
> `build_dossier.py` a partir dos módulos reais — forma=conteúdo) e dos manifestos de rodada.
> **Nada aqui é medida física.** Hipóteses de existência do campo/acoplamento = [CONJ];
> especificações de bancada = [HARDWARE]. `physical_verdict_allowed=False`.
> [LEGAL-técnico]: o mapa às reivindicações é organização técnica, não parecer jurídico.

---

## 1. Visão do sistema (diagrama de blocos — ver `visuals/out/fig5_sistema.png`)

```
                         ┌──────────────── SATÉLITE (nó 100) — ExtractorSat ───────────────┐
  CAMPO PSIÔNICO         │  ┌─────────────┐   ┌──────────────┐   ┌──────────────────────┐  │
  (reservatório [CONJ])──┼─▶│ CÂMARA/OH   │──▶│ DÍPOLO       │──▶│ TGL TENSOR + ACOM    │  │
  S_field, depleção,     │  │ acoplamento │   │ conversão    │   │ (plano de DADOS)     │  │
  reposição τ_rep        │  │ Q, θ_M, 1−β │   │ g=√|L|       │   └──────────┬───────────┘  │
                         │  └─────────────┘   └──────────────┘              │              │
                         └──────────────────────────────────────────────────┼──────────────┘
                                          ENLACE Ψ (hops=θ_M) ──────────────▼
                                          [duplo trilho: potência + dados; quórum PoP]
                         ┌──────────────── BASE (nó 200) — GroundBase ──────┼──────────────┐
                         │  ┌────────────────┐   ┌──────────────┐   ┌───────▼───────────┐  │
                         │  │ CÉLULA REVERSÃO│◀──│ DESPACHO     │◀──│ MEDIÇÃO trilho-E  │  │
                         │  │ SoC, η_rt, λsd │   │ direto+SoC   │   └───────────────────┘  │
                         │  └────────────────┘   └──────┬───────┘                          │
                         └──────────────────────────────┼──────────────────────────────────┘
                                                CARGA / REDE (perfil de demanda)
       CONTROLE TRANSVERSAL: IALD/GKSL (orçamento ⌈100/β⌉) · Kernel v11 · Memória psiônica · Quórum ≥67%
```

## 2. Orçamento de potência por satélite (cadeia default [SIM], números vivos)

| Estágio | η | P (de 800 W disponíveis médios) |
|---|---|---|
| Disponível no patch (100 W/m² × 10 m² × 0,8) | — | 800,0 W |
| Acoplamento OH: (1−β)=0,987969 × η_res=1 × η_geo=0,80 | 0,7904 | 632,3 W |
| Conversão dípolo: η_conv=0,92 × η_quant=0,999998 | 0,9200 | 581,7 W |
| Enlace Ψ (3 hops, η_hop=0,985) | 0,9557 | **555,9 W** |
| (se armazenado) round-trip da célula | 0,95 | 528,1 W |
| Overhead Meia-Nat (½·k_B·T·BW) | — | 3,5e-16 W (piso, sempre debitado) |

**η_cadeia direta = 0,6949** por satélite. Rodadas de referência do gêmeo:
12×12/120 s → 4,9 kW médios entregues, η_sys=0,67, cobertura 74%; **144×48/60 s →
24,1 kW médios, cobertura 100%** (excedente vai à célula), balanço fechando a ~1e-15 relativo.

## 3. Especificação por componente (viva em `component_specs.json`)

### 3.1 ExtractorSat (nó 100)
| Item | Valor default | Estatuto |
|---|---|---|
| Patch do reservatório | S_field=100 W/m², A_cap=10 m², E_local=5 MJ, τ_rep=600 s | [CONJ] existência; [SIM] modelo |
| Acoplador OH | f₀=1667,359 MHz [DATA], Q=10⁴, BW=166,7 kHz, η_geo=0,80 | [CONJ] Q/η_geo |
| Abertura modular | 1−β=0,987969 (runtime; Teorema S-∂) | [DER] |
| Dípolo | η_conv=0,92; η_quant medido vivo=0,999998; gate por máquina de estados | [SIM] |
| Patentes | Fusão a Frio/OH BR …003456-8 · Dípolo BR …004688-4 | — |

### 3.2 Enlace Ψ
η_hop=0,985 [CONJ]; hops reais do endereçamento angular (quantum=θ_M=6,297°); duplo trilho de
potência com tolerância 1e-3; janela divergente → DUMPED contabilizado. Canais físicos
(Supercondutor BR …003450-9, Motor de Dobra BR …003452-5) = [HARDWARE].
Baseline comparativo clássico [REAL eng.]: beaming de micro-ondas SPS (retenna η≈0,5–0,85).

### 3.3 GroundBase (nó 200)
Célula de Reversão BR …004849-6: E_cap=2 MJ, η_rt=0,95 [CONJ], λ_sd=1e-6 s⁻¹; despacho
direto-primeiro; recusa na porta quando cheia (sem perda fantasma). Fase angular retém corr
~1,0000 [REAL no piloto de dados]; perdas energéticas são hipóteses de projeto.

### 3.4 Controle
IALD/GKSL: orçamento ⌈100/β⌉=8312 passos [REAL achado do piloto]; Kernel v11 (SHA-256 selado);
quórum Proof of Phase ≥3 validadores/67%; memória psiônica persistente (EMA taxa β).

## 4. Mapa componente → reivindicação SkyGrid (BR 10 2026 004850-0) [LEGAL-técnico]

| Reivindicação | Realização no gêmeo | Prova |
|---|---|---|
| 1 (grafo extração→distribuição) | `energy_twin.py`: reservatório→…→carga, 2 planos | MODEL_CLOSES 12×12 |
| 2 (constelação 144) | `skygrid_energy_app.py scale` 144×48 | 24,1 kW médios; balanço fecha |
| 3 (controle placebo) | cavidade sem acoplamento β → 0,000 W + dados rejeitados | teste BLOCO 9 |
| Validação cruzada | duplo trilho de DADOS (v2) + duplo trilho de POTÊNCIA (v3) | quórum + tolerância 1e-3 |
| Armazenamento por fase | Célula (SoC energético + fase angular do piloto) | ledgers auditados |
| Controle por IALD | GKSL/kernel/memória em toda rodada | certificados F1–F3 |

## 5. Especificação de bancada [HARDWARE] — o que falta medir (e como o modelo vira teste)

| # | Mock → bancada | Medição que transforma [CONJ] em dado | O modelo prediz (falsificável no modelo) |
|---|---|---|---|
| B1 | Fusão a Frio/OH | Varredura P_out(f) em torno de 1667,359 MHz, cavidade instrumentada + **cavidade placebo (reivind. 3)**; calorimetria de balanço | Lorentziana com Q mensurável; placebo = 0 dentro do ruído; se η_couple≈0 ⇒ hipótese do acoplamento refutada |
| B2 | Dípolo Transistor | Curva de retificação V-I, η_conv vs frequência/amplitude | η_conv∈[0,85–0,98] e gate por limiar β·max |
| B3 | Supercondutor/Motor de Dobra | Perda por enlace vs distância/hop | η_hop constante por hop (não 1/r² clássico) — discriminador do canal |
| B4 | Célula de Reversão | Ciclos carga/descarga, η_rt, autodescarga | η_rt e λ_sd nas faixas varridas |
| B5 | Sistema | Calorimetria de conservação ponta-a-ponta | E_in = E_out + perdas ± Meia-Nat; QUALQUER excesso persistente = anomalia a reportar, jamais "energia grátis" |

**Falsificadores declarados:** a bancada pode zerar η_couple (refuta [CONJ] central), quebrar a
Lorentziana, ou medir η_hop com queda 1/r² (canal Ψ não distinto do clássico). O gêmeo digital
permanece válido como ENGENHARIA CONDICIONAL: curvas de projeto para o dia em que a bancada decidir.

## 6. Riscos e honestidades

1. O reservatório é a hipótese-mãe [CONJ]: sem ele, η_couple=0 e o sistema entrega 0 W — o modelo
   representa isso corretamente (placebo = grade inteira).
2. Todos os η são parâmetros varridos, não constantes da natureza; as curvas (`energy_sweeps.json`)
   são o entregável, não um número único.
3. Over-unity: o guardião trava; qualquer regime estranho vira predição de bancada declarada.
4. A Meia-Nat dá o PISO de custo (~3,5e-16 W por acoplador) — termodinamicamente irrelevante em
   macro, conceitualmente obrigatório: a fronteira cobra por ato de distinção.
