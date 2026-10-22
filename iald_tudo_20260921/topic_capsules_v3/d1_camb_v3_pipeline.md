### d1_camb_v3_pipeline

Fonte: `resultado_publicado_integral`, `/core/d1_camb_v3_pipeline`. [DERIVED — proposta semântica não integrada, NÃO APROVADA.] Estatutos/resultados são reportados na fonte, não reexecutados aqui; OPEN histórico não apaga construção posterior de outro tipo.

**route**

Rota INPUT ratificada em 17/09/2026: `Phi_total=1+beta|1+w_eff|`, fluido total inclui vácuo. Emenda pré-dado: `P=rho+beta J`, `J(a)=∫_a^inf 3(rho+p)²/(rho a') da'`, `P(inf)=rho_Lambda`, `C=0` preserva de Sitter/Phi(-1)=1; limites radiação `(1+4beta/3)rho`, matéria `(1+beta)rho`. Fecho `H(a=1)=H0` por raiz Omega_Lambda; V2 usava `H(0)=H0 sqrt(Phi(0))`. Gate GOF `chi²_LCDM<=3n` (45 primário sem SH0ES,48 com). Ajuste escalado com limites, Fisher J^T J, emcee 24×2000/queima400; priors no painel. Fiducial (67.5,0.02237,0.1200) sintético, mesmas sementes entre injeções; tranca exige confirmação do operador e hashes. Não confundir a recusa inicial com estado posterior: errata v366 reporta execução real única fases1–3 autorizada e resultado lido por `prove_d1_camb_v3_real_v366`.

**negative**

Autocheck CAMB beta=0, segunda Friedmann/limites w; injeção em três betas e SH0ES; MCMC Asimov. Negativo preservado: C livre falhou, 24/24 realizações na borda do prior. C é absorvido em rho_Lambda pelo fecho: efeito 2.220446049250313e-16 em beta=0 e 5.246358724497746e-5 em beta_TGL. Sem refazer/afrouxar teste: passa a diagnóstico de degenerescência, fora da matriz de vereditos, V1 preservada. Sigma primário≈0.00835 excede beta/2≈0.00602 exigido POWERED; projeção fiducial antes do dado permitiria no máximo D1_BETA_INCONCLUSIVE. MCMC≈0.00852 versus Fisher≈0.00836 é validação sintética, não resultado real. Textos PT/EN duplicam essa narrativa; valores exatos no painel. Gate inalterado; `in_contour_roster_v314=false`.

**Dados e controles reportados** — números/flags copiados da fonte, não parâmetros novos. Chaves e posições de listas seguem a fonte; null no painel indica texto descrito acima, não dado ausente.

```json
{"amendment":{"declared_before_any_real_data":true,"priors":{"H0":[50,90],"ombh2":[0.015,0.03],"omch2":[0.08,0.18],"beta":[-0.05,0.05],"c_sensibilidade":[-0.05,0.05]}},"sigma_beta":{"primary":0.008354863425114496,"sh0es":0.008366116697853298},"c_free_degeneracy":{"beta_0":2.220446049250313e-16,"beta_TGL":5.246358724497746e-05,"realizations_at_prior_edge":1.0},"mcmc_asimov":{"sigma_mcmc":0.008517780105559982,"sigma_fisher":0.008359770114225784,"desvio_mediana_em_sigma":0.022467538955489814},"does_not_gate_core":true,"in_contour_roster_v314":false,"checks_reported":{"true":9,"false":0}}
```

Veredito literal reportado: `TGL_D1_CAMB_V3__PIPELINE_BUILT_BLIND__AMENDMENT_BESIDE_420a25dd11fe4786__PRIMARY_AND_SH0ES_INJECTION_PASSED__C_FREE_DEGENERATE_WITH_VACUUM_AMENDMENT_faec13742bfab745__MCMC_VALIDATED_ON_ASIMOV__REAL_DATA_UNLOCKED_BY_OPERATOR_LINE__RESULT_READ_BY_V366__GATE_UNTOUCHED`. `all_verified=true`. Detalhes e custódia: fonte-base acima + chave original; recuperação operacional não validada.
