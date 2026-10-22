### inverse_parity

Fonte: `resultado_publicado_integral`, `/core/inverse_parity`. [DERIVED — proposta semântica não integrada, NÃO APROVADA.] Estatutos/resultados são reportados na fonte, não reexecutados aqui; OPEN histórico não apaga construção posterior de outro tipo.

**polarization**

Princípio do operador: 0_abs não é estado normal em M_*, não tem suporte observável nem pode ser ocupado; a imagem retorna normalizada, suporte preservado e assimétrica. `rho_B=(P1+P0)/2→rho_ret=p1P1+p0P0`, `p0>p1>0`; `chi=log(p0/p1)`, `q=p0-p1=tanh(chi/2)`, `alpha=2sqrt(p0p1)=sech(chi/2)`, `p0,p1=e^(±chi/2)/(2cosh(chi/2))`, `q²+alpha²=1`. `beta=2sqrt(e)sqrt(p0p1)` é lido como trava mínima contra colapso em zero. Vacuidade/direção, proibição/retorno e paridade/polarização são leitura do princípio, não confirmação física.

**form**

`rho_ret^(chi)=exp(-chi Z_d/2)/(2cosh(chi/2))=FP_(eps→0) M_eps rho_B M_eps†`, `M_eps=exp[-(C_eps+chi)Z_d/4]`. Paridade unitária/antiunitária pura preserva `rho_B=I/2`; lente precisa de renormalização não trivial. Para chi finito, suportes iguais; distorção angular theta_M não destrói a fonte. A fonte escreve aqui `chi=0=0_abs proibido`; isso conflita com a distinção Bell nu/zero de contraste em `contour_theory`. Preservar como leitura local histórica, com compatibilização pendente, sem identificar os zeros globalmente. Forma/gap/q/alpha verificados nesse registro.

**value**

`gap(-log Delta_(ret|Bell))=chi` é tautologia da parametrização, não derivação do valor. Chi observado entra por CODATA: `chi_obs=2 artanh(sqrt(1-alpha²))`. FP depende do esquema: qualquer chi pode ser parte finita de outra subtração. OPEN: condição canônica alpha-livre que fixe chi. Controle negativo: Meia-Nat dá `tau(P1)=tau(P0)=1/2` para TODO chi, fixa peso, não polarização. Painel mantém os quatro passos (chi genérico, VALIDACAO_QED, negativo e populações), números e flags; beta numérico é retrato do registro, não constante substituída no runtime.

**Dados e controles reportados** — números/flags copiados da fonte, não parâmetros novos. Chaves e posições de listas seguem a fonte; null no painel indica texto descrito acima, não dado ausente.

```json
{"steps":[{"ok":true,"chi_test":5.0,"gap":5.0,"q":0.9866142981514303,"alpha":0.1630712319299778,"conservation":1.0},{"ok":true,"chi_obs":11.226755051602328,"p1_Um":1.33130158665451e-05,"p0_zero_mod":0.9999866869841335,"ratio_e_chi":75113.46016623077,"alpha":0.0072973525692962464,"beta":0.012031300400796953},{"ok":true,"tau_P1":0.5,"tau_P0":0.5},{"ok":true,"p0":0.993307149075715,"p1":0.0066928509242848554,"q_pop":0.9866142981514302,"alpha_coh":0.1630712319299778,"beta_pop":0.26885900872222834}]}
```

Veredito literal reportado: `POLARIZATION_PRINCIPLE_FORM_CLOSED__ALPHA_VALUE_QED_SECTOR_FALSIFICATION_CHALLENGE`. `all_verified=true`. Detalhes e custódia: fonte-base acima + chave original; recuperação operacional não validada.
