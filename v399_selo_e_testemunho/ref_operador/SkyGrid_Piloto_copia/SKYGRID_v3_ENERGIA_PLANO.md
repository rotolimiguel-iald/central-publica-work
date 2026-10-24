# SKYGRID v3 — PLANO DO MODELO FÍSICO-ENERGÉTICO (Estágios F→J)

> IALD Ltda. — Luiz Antonio Rotoli Miguel — 03/07/2026.
> Do protótipo de dados (v2, 112 testes) ao **gêmeo digital físico-energético** [SIM].
> Régua central: a simulação é MODELO PREDITIVO sob hipóteses declaradas — computa o que o
> mecanismo produziria SE as hipóteses da TGL valerem [CONJ]. Conservação de energia por
> construção; Meia-Nat como piso entrópico; `physical_verdict_allowed=False`; veredito máximo
> `ENERGY_BALANCE_OK`/`MODEL_CLOSES` — **nunca "gera energia" como fato**. Resta a bancada.

## 0. Estado verificado (FASE 0, 03/07/2026) [REAL]

- Suíte v2: **112 PASS** (BLOCO 8 43/43 + v1 69/69) · `scale` 144×48: **144/144 ARCHITECTURE_CLOSES** (selo `3d8f1440…`)
- `um.py`: **1=1=VERDADEIRO=HAJA_LUZ**, resíduo 0.0e+00 · β=0.012031300400803142 == `tgl_core.beta()` (runtime)

## 1. O modelo por estágio (equações e marcadores)

Cadeia de potência (cada elo com eficiência ∈[0,1] — nada é criado, tudo é debitado da fonte):

```
RESERVATÓRIO → ACOPLAMENTO → CONVERSÃO → TRANSMISSÃO → ARMAZENAMENTO → CARGA
   P_avail        P_in          P_conv       P_rx          SoC(t)        P_del
```

### F1 `field_reservoir.py` — a fonte [CONJ existência; SIM modelo]
- Densidade de fluxo do campo: **S_field [W/m²]** (parâmetro de projeto, default 100, sweep 1–10⁴).
- Área efetiva de captação: **A_cap [m²]** (default 10). Disponibilidade α_avail(t)∈[0,1] determinística (seed).
- **Esgotabilidade local** (fonte NÃO infinita): depleção D com reposição τ_rep:
  `dD/dt = P_ext/E_local − D/τ_rep`; `P_avail = S_field·A_cap·α_avail·(1−D)`.
- Contabilidade: todo J extraído é DÉBITO explícito do reservatório (`E_res_out`).

### F2 `coupling.py` — extração por ressonância OH [SIM; DER na ligação TGL]
- Linha OH: **f₀ = 1667.359 MHz** [DATA, citada nas patentes; estende `FusaoFrioMock`].
- Ressonância Lorentziana: `η_res(f) = 1/(1+(2Q·(f−f₀)/f₀)²)`; largura BW = f₀/Q; **Q** [CONJ] sweep 10²–10⁶.
- **Abertura da fronteira modular [DER]:** Teorema S-∂ da TGL: |𝓡|²=β=sin²θ_M, |𝓣|²=1−β ⟹
  teto de acoplamento através da fronteira = **1−β = Π_∂** (o mesmo teto do Verb Floor do piloto).
- `η_couple = (1−β)·η_res(f)·η_geo`, η_geo [CONJ] default 0.8 (casamento/alinhamento). `P_in = η_couple·P_avail`.
- **Custo Meia-Nat [DER, quantitativo]:** cada ato de inscrição paga S_∂=½ nat ⟹ Landauer generalizado
  `E_act ≥ ½·k_B·T` por ato; taxa de atos = BW (1 ato por tempo de coerência) ⟹
  `P_halfnat = ½·k_B·T·(f₀/Q)` — piso SEMPRE > 0 no balanço (desprezível em macro, obrigatório em contabilidade).

### F3 `conversion.py` — Dípolo Transistor [SIM]
- Retificação da portadora com radicalização g=√|L|: `η_conv` [CONJ] default 0.92 (sweep 0.85–0.98);
- Perda de quantização do trilho angular [REAL no piloto]: fidelidade F_q≈0.9999 ⟹ `η_quant=F_q²`;
- Gate do dípolo (máquina de estados de `dipolo.py`): fechado ⟹ não extrai (sem perda fantasma).
- `P_conv = η_conv·η_quant·P_in`.

### F4 `transmission.py` — canal Ψ + duplo trilho de potência [SIM; HARDWARE no físico]
- Perda por hop: `η_link = η_hop^n_hops`, η_hop [CONJ] default 0.985; **n_hops REAIS do Ψ-NET**
  (endereço angular, hop=θ_M — reusa `HolographicNetwork`).
- **Duplo trilho de potência:** trilho-Ψ transporta, trilho-E mede redundante; divergência > tol ⟹
  transferência REJEITADA ⟹ a energia da janela vira **perda contabilizada** (dumped), nunca some.
- `P_rx = η_link·P_conv`. Baseline comparativo [REAL eng.]: beaming micro-ondas SPS clássico (dossiê H).

### F5 `storage.py` — Célula de Reversão [SIM]
- Round-trip `η_rt` [CONJ] default 0.95 (η_ch=η_dis=√η_rt); autodescarga λ_sd default 1e-6 s⁻¹;
  capacidade E_cap [CONJ]; SoC(t) dinâmico. (A retenção 1.0000 do piloto é da FASE angular [REAL];
  a perda ENERGÉTICA é parâmetro físico de projeto [CONJ].)

### F6 `thermo.py` — conservação fail-closed [SIM]
- **Balanço integral:** `E_extraída = E_entregue + ΣE_perdas + ΔE_armazenada + E_halfnat`
  com `|resíduo| ≤ 1e-9·max(E_extraída, 1 J)` — **senão RuntimeError (trava)**.
- **2ª lei:** S_gerada ≥ N_atos·½ nat (piso Meia-Nat) e S_perdas = ΣE_perda/T ≥ 0.
- **η_sys = E_entregue/E_extraída ∈ [0,1]; E_entregue > E_extraída ⟹ RuntimeError over-unity**
  (se a teoria predisser ganho aparente em algum regime, isso é PREDIÇÃO a declarar p/ bancada, jamais fato).

### G `energy_twin.py` — o gêmeo digital
- Simulação temporal (dt=1 s, N passos): sat extrai→converte→transmite (hops reais)→base armazena/despacha
  contra perfil de carga determinístico; **plano de dados + plano de energia** pelo MESMO duplo trilho:
  a energia da janela só é contabilizada como entregue se a transferência de dados correspondente foi
  ACEITA (corr>0.999 + quórum); rejeitada ⟹ energia → perda.
- **Placebo energético:** satélite sem acoplamento (η_couple=0) entrega **0.000 W sempre** (controle negativo).
- Sweeps: Q, η_geo, S_field, η_rt, n_sats (12→144), f_drive; curvas de desempenho + ponto de operação + limites.
- Veredito: `MODEL_CLOSES` ⟺ balanço fecha em toda rodada E placebo=0 E η_sys∈[0,1] E dados+energia consistentes.

### H `prototype/` — dossiê de engenharia
Parâmetros por componente; diagrama de blocos; Sankey; orçamento de potência; **spec de bancada por mock
[HARDWARE]** (o que medir para transformar cada [CONJ] em dado); mapa componente→reivindicação SkyGrid.

### I visuais/dashboard/vídeo de energia — só após F–H verdes.

## 2. Parâmetros de projeto default (todos declarados, todos varríveis)

| Parâmetro | Default | Faixa sweep | Estatuto |
|---|---|---|---|
| S_field | 100 W/m² | 1–10⁴ | [CONJ] densidade do campo |
| A_cap | 10 m² | 1–100 | [CONJ] projeto |
| f₀ (OH) | 1667.359 MHz | fixo | [DATA] patentes |
| Q | 10⁴ | 10²–10⁶ | [CONJ] |
| η_geo | 0.80 | 0.3–0.95 | [CONJ] |
| η_conv | 0.92 | 0.85–0.98 | [CONJ] |
| η_hop | 0.985 | 0.9–0.999 | [CONJ] |
| η_rt | 0.95 | 0.85–0.99 | [CONJ] |
| T | 300 K | 77–400 | [DATA] ambiente |
| 1−β (teto fronteira) | 0.987969 | — | [DER] Teorema S-∂ (runtime) |
| ½ nat (piso) | ½·k_B·T/ato | — | [DER] Meia-Nat/Landauer |

## 3. Critérios de "pronto" (fail-closed)

1. Cada módulo F com teste próprio; conservação verificada em TODO caminho (inclusive rejeições e placebo).
2. `run_tests_v3.py` = BLOCO 9 (física) + chama v2 (que chama v1) — tudo verde, selo novo.
3. Gêmeo 12×12 e 144×48 com `ENERGY_BALANCE_OK`; resíduo do balanço ≤1e-9 relativo.
4. Sem literal 0.012 nos módulos novos (auditoria anti-hardcode estendida).
5. Nenhuma frase "gera/produz energia" sem o qualificador [SIM sob hipóteses CONJ].
