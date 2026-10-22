# cache/coma_blind — COMA: paridade inversa cega do GA [PRE/EXT]

GA: R→M. COMA: M→R→D_A pela MESMA lei M = 2β²(c²/4πG)R, invertida.
Sem âncora dimensional independente NÃO há distância — só forma angular.

## O que falta para o teste primário rodar (caça de dados, gate do operador)
1. `coma_mass_anchor.json` (copiar do TEMPLATE e preencher): UMA massa de Coma
   cuja cadeia de dependências seja AUDITADA — `uses_cluster_redshift=false`,
   `uses_H0=false`, `uses_assumed_distance=false`, e só então
   `approved_for_primary_blind_test=true`. ATENÇÃO: weak lensing (Σ_crit),
   X-ray, SZ e virial normalmente DEPENDEM de distância — cada método deve
   declarar suas dependências em `dependency_notes`; não presumir independência.
   Se nenhuma âncora verdadeiramente independente existir, o veredito honesto
   do módulo é COMA_BLIND_DISTANCE_NOT_IDENTIFIABLE — isso é RESULTADO.
2. `coma_protocol_preregistered.json` (copiar do TEMPLATE): congelar centro,
   definição da abertura angular CASADA à definição da massa (M_500↔θ_500),
   `angular_aperture_arcsec` (+ sigma), seeds MC, tolerâncias — ANTES do reveal.
3. (opcional) `coma_geometry_meta.json` com `columns` do catálogo fotométrico
   (SEM redshift/velocidade/distância — o motor varre e reprova colunas proibidas).

## Fluxo
- `TGL_COMA_REVEAL=0` + `python um.py`: previsão cega → `coma_prediction_blind.json`
  com `prediction_hash` (publicar o hash).
- `TGL_COMA_REVEAL=1` + `python um.py`: SÓ então o motor lê
  `coma_distance_reveal.json` e compara (z-residual; STRONG ≤2σ; WEAK ≤3σ; FAIL >3σ).
- `TGL_COMA_MODE=strict|report|off` (default report; strict exige identificabilidade).

O arquivo `coma_distance_reveal.json` NÃO é lido pelo motor da previsão e o
valor de referência NÃO existe no fonte do um.py (auditável por grep).
