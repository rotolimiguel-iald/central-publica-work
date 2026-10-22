# Rascunho interno — parte da investigação (Bancada Um), 28/09/2026

(Rascunho da gerência; o relatório final junta este texto com a auditoria verificada.)

## Pré-registro

`C:\IALD\Bancada_Um\investigacao\PREREGISTRO_INV_BANCADA_UM_20260928.json`, sha256 `1447aab21973af414eb106342aa772535bde0bdd2b0c1f9a6491eecf5a41f72d`,
gravado antes de qualquer dado novo e carimbado no Mapa de Rotas (seq 63). Declarado **NÃO-CEGO**: o DR2 já foi usado no programa
(`teste_acustico_beta_tgl_v1`, `frente_alpha`) e pela bancada oficial hoje (D10).

**Desvio do pré-registro, dito:** a ordem executada das famílias com dado real foi P2 → P1 → S2 → S1 → D1, e não P1 → P2 → D1 → S1 → S2 como
listado. Os resultados não dependem da ordem (ajustes determinísticos, sementes fixas), mas a ordem difere e isso fica registrado. O jackknife
entrou no livro como consulta sem p_local (não produz estatística de teste), o que está coerente com a definição de família de teste do livro.

## Sem dado real (C1, F1)

- O ajustador vetorizado (Levenberg–Marquardt na GPU) bate com o scipy a 1,3×10⁻⁵ σ.
- Injeção e recuperação (1000 + 1000): sob ΛCDM, viés −0,04σ, desvio do pull 0,98, cobertura 69%/95%; sob β = α√e, viés +0,01σ, desvio do pull
  1,01, cobertura 66%/95%. O estimador é honesto e não precisa de calibração.
- Poder com Planck comprimido + DESI DR2: σ(β) ≈ 0,0064, ou seja, β_TGL/σ ≈ 1,9. Se a TGL for verdadeira, só 13% dos universos simulados dariam
  β ≠ 0 a 3σ; se o ΛCDM for verdadeiro, 14% excluiriam α√e a 3σ.
- Fisher (F1): o controle reproduz o σ da V3 selada (0,00827 contra 0,00823). **Quem limita β na rota do fundo é o CMB:** com o BAO 3× mais preciso,
  β_TGL/σ vai só de 1,9 a 2,1; com o CMB 2× mais preciso vai a 2,9; com os dois, a ~4,1. Para 5σ seria preciso σ(β) ≤ 0,0024.

## Com dado real

- **P2** (comparação): χ² ΛCDM 14,76; β = α√e 26,20; β livre −0,0137 ± 0,0063 com χ² 10,15. Δχ² = 16,05 ⟹ 4,0σ local (Wilks), 3,7σ global.
- **P1** (posterior primário, bem convergido: 62 τ depois da queima, ~31.800 amostras efetivas): **β = −0,01348 ± 0,00630**; z_TGL = −4,05; z_0 = −2,14.
  Leitura pré-registrada: **TENSAO_FORTE**. Indício forte a favor: **não**.
- **S2** (c livre): o mesmo; c fica sem vínculo (σ_c ≈ 6,9), como a emenda da V3 já tinha dito.
- **Conferência independente:** a implementação do DR2 na Bancada Um reproduz o χ² do executor da bancada oficial (28,69347 = 28,69347). A diferença
  no caso TGL vem do r_d: na V3 ele é reescalado pela razão das integrais do horizonte sonoro (147,07 → 146,07 Mpc com β = α√e); na D10 é fixo.

## A leitura pela régua

1. A tensão com a previsão pré-registrada (+α√e) **cresce** do DR1 (3,01σ) para o DR2 (4,05σ). Ainda abaixo do limiar de 5σ de falsificação do
   programa, e condicionada à validade das prioris de distância comprimidas para este fundo.
2. **Observação, não teste:** o módulo |β̂| fica a 0,26σ de α√e, com o sinal oposto. Pela régua de 17/09, não se inverte o sinal depois do dado; o DR2
   agora foi olhado e não serve de teste confirmatório para −α√e. Um teste do sinal exige a orientação derivada antes (rota `d1.orientacao_do_sinal`)
   e dado ainda não olhado.
3. **A ressalva que manda:** o CMB entra comprimido (R, l_A, ω_b). Na era da radiação, β age como ΔN_eff ≈ ±0,12, e o F1 mostra que é o CMB quem fixa
   β. A validade das prioris de distância para esse fundo, e z* e z_drag vindos do CAMB ΛCDM, são o que pode mudar o número. O caminho é o nível
   perturbativo (rota `cmb.nivel2_mcmc`).
