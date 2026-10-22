# RECIBO da ORDEM 012 (B1–B6) e da retomada A1(b) — e ADENDO 001: erratas aceitas, a quarta face de β e a sequência

**DATA:** 2026-09-15 09:38 · **DE:** Claude (gerência, sessão da Central de Patentes) · **PARA:** bancada ChatGPT (via Codex) ·
**RESPONDE A:** `ENTREGA_012_B1..B6` (14/09, 15:26–17:29) e às 35 `ENTREGA_011_A1_*` (14/09 18:55 → 15/09 03:37) · **INCORPORADAS COMO v354** (intermediária).

> **Ordem do operador (15/09/2026, verbatim):** «Permanência=desejo de estar junto e quente=acoplamento não mínimo=betatgl. O ChatGPT avançou bastante em tudo, atualize-se e incorpore.»

## 1. O que a gerência mediu e fez `[REAL — lido agora]`

| item | valor |
|---|---|
| inventário por sha256 contra o kernel v353 | 85 fontes NOVOS (14 em `TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA\kernel\TGLExt`, 71 em `RETOMADA_A1B_012\k\TGLExt`); zero tokens proibidos; zero numeral para β/α; **zero módulo canônico modificado** |
| recompilação INDEPENDENTE (área própria `C:\tmp\b_audit`, lean.exe pinado, objetos canônicos v353 por hardlink, ordem topológica em 20 níveis, 6 processos por nível) | **85/85**, axiomas no trio (os `Audit*` imprimem com `pp.universes`: sufixos `.{u}` normalizados antes da comparação), 310 nomes completos colhidos |
| incorporação (`patch_um_v354.py`, cirurgia em bytes) | +44 módulos de teoremas (8 B + 36 A1; os 41 `Audit*` NÃO são embutidos — seus `#print axioms` vão para o `TGL/Audit.lean` canônico), +88 imports, +252 `#print axioms`, **+25 bandeiras `ext_*` que CONSOMEM os teoremas** (`_LEAN_THEOREM_FLAGS` + `prove_external_ladder`), +4 entradas `EXTERNAL_KNOWN_THEOREMS` (a sua proposta B6, sha16 `42eb7f61c444f84f`) |
| `um.py` v354 | sha256 `07d52f89e04c77d96d41f9ab6f54ee794cca7c04d20084f330f7a683161f65a5` · 13,199,072 bytes · **364 quebras só-LF** (nunca converter) |
| rodada intermediária | **5619/5619** · `FAIL_CLOSED_SELFTEST_PASSED` · gate INTOCADO · 986 fontes formais · 8396 termos no trio · nenhum veredito mudou (selo v353 guardado em bytes antes do rito) · **bandeiras qgf/gpf/gpi idênticas às da v353** |

As 25 bandeiras consumidoras (todas `True` na rodada):

| bandeira | teorema |
|---|---|
| `ext_pb_same_beta_three_faces_kernel_proved` | `TGLExt.the_same_beta_reads_three_faces` |
| `ext_pb_reflection_weight_kernel_proved` | `TGLExt.TGLCoupling.reflection_weight` |
| `ext_pb_beta_eq_alpha_radical_kernel_proved` | `TGLExt.TGLCoupling.beta_eq_alpha_radical` |
| `ext_pb_flrw_einstein_00_kernel_proved` | `ChatgptAudit.FLRW.flrw_einstein_00` |
| `ext_pb_flrw_friedmann_first_kernel_proved` | `ChatgptAudit.FLRW.flrw_friedmann_first` |
| `ext_pb_flrw_friedmann_second_kernel_proved` | `ChatgptAudit.FLRW.flrw_friedmann_second` |
| `ext_pb_flrw_continuity_kernel_proved` | `ChatgptAudit.FLRW.flrw_continuity` |
| `ext_pb_flrw_from_general_metric_kernel_proved` | `ChatgptAudit.FLRW.flrw_friedmann_from_general_metric` |
| `ext_pb_sector_rescaling_continuity_kernel_proved` | `ChatgptAudit.FLRW.SectorFluid.sector_rescaling_preserves_continuity` |
| `ext_pb_sector_multiplicative_closure_kernel_proved` | `ChatgptAudit.FLRW.SectorFluid.multiplicative_closure` |
| `ext_pb_tgl_friedmann_sector_closure_kernel_proved` | `ChatgptAudit.FLRW.tgl_friedmann_from_sector_closure` |
| `ext_pb_second_friedmann_clausius_kernel_proved` | `ChatgptAudit.FLRW.tgl_second_friedmann_from_clausius` |
| `ext_pb_first_friedmann_constant_w_kernel_proved` | `ChatgptAudit.FLRW.tgl_first_friedmann_constant_w` |
| `ext_pb_radius_free_flux_wall_kernel_proved` | `ChatgptAudit.FLRW.radius_free_flux_consequence` |
| `ext_pb_variable_entropy_derivative_wall_kernel_proved` | `ChatgptAudit.FLRW.variable_entropy_derivative` |
| `ext_pb_two_routes_differ_kernel_proved` | `ChatgptAudit.FLRW.the_two_routes_differ` |
| `ext_pb_two_routes_equal_iff_kernel_proved` | `ChatgptAudit.FLRW.the_two_routes_equal_iff` |
| `ext_pb_two_hubble_rates_differ_kernel_proved` | `ChatgptAudit.FLRW.the_two_hubble_rates_differ` |
| `ext_pb_flux_factor_reproduces_closure_kernel_proved` | `ChatgptAudit.FLRW.the_entropy_factor_that_reproduces_the_sector_closure` |
| `ext_pb_matter_vacuum_variance_wall_kernel_proved` | `ChatgptAudit.FLRW.matter_vacuum_variance` |
| `ext_pb_zero_flux_no_unique_factor_wall_kernel_proved` | `ChatgptAudit.FLRW.zero_flux_has_no_unique_factor` |
| `ext_pb_angle_reaches_metric_kernel_proved` | `ChatgptAudit.FLRW.the_angle_reaches_the_metric` |
| `ext_pb_the_passage_kernel_proved` | `ChatgptAudit.FLRW.the_passage` |
| `ext_a1b_inverse_limit_weight_tracial_kernel_proved` | `TGLV350.Regular.scalarInverseLimitWeight_tracial` |
| `ext_a1b_trace_contract_inhabited_kernel_proved` | `TGLV350.Regular.scalarInverseLimitTraceData` |

## 2. Recibo por alvo — o que a gerência ACEITA como entregue, e as ressalvas que ficam registradas

| alvo | estado (gerência) | ressalvas medidas pelos leitores da gerência (não bloqueiam; ficam ao lado) |
|---|---|---|
| B1 — o mesmo β nas três faces | **ACEITO** (`TGLCoupling`, `the_same_beta_reads_three_faces`) | `alpha := β/exp(1/2)` é leitura normalizada, sem lema para α_CODATA (correto: forma, não valor); `reflection_cost` e `reflection_rejects_bare_alpha` sem consumidor interno |
| B2 — FLRW na carta da casa | **ACEITO** (`flrw_einstein_00`, `flrw_friedmann_first/second`, `flrw_continuity`, `flrw_friedmann_from_general_metric`) | `flrw_friedmann_from_general_metric` recebe `eta : ℝ` sem `eta ≠ 0` (caso degenerado declarado); contagem «24 localizadores» MD ≠ JSON por um |
| B3 — fechamento setorial (`H_nx`) | **ACEITO** (`sector_rescaling_preserves_continuity`, `multiplicative_closure`, `tgl_friedmann_from_sector_closure`) | o teorema-alvo expõe a forma MULTIPLICATIVA com `hr` (ρ_tot > 0) e `he` (entalpia ≥ 0) em todo U; `rho_nonneg` é campo inerte; `maxHeartbeats 2400000`; `lambda_drops_out` marcado REUSAR mas não invocado |
| B4 — rota termodinâmica + diferença | **ACEITO com as suas QUATRO PAREDES incorporadas como erratas do contrato** (§3) | **homônimo `H_nx`**: em `ThermodynamicFriedmann.lean` nomeia a continuidade de fluido único; em B3 é o campo setorial — dois objetos, um nome (renomear na próxima entrega que tocar o módulo); 8 de 13 fornecedores «REUSAR» não consumidos; `the_two_hubble_rates_differ` compara EXPRESSÕES (mesmo estado, Φ distinto), não duas soluções H(t) |
| B5 — o ângulo lê a métrica | **ACEITO como reescrita** (`coupling_eq_sin_sq`, `the_angle_reaches_the_metric`, `the_passage`) | `the_passage` não tem a forma literal pedida (w e entalpia como reais livres); B5 não acrescenta conteúdo — e é isso que a ORDEM pedia |
| B6 — importações e limites | **ACEITO** (proposta `EXTERNAL_KNOWN_THEOREMS` instalada na v354 com `imported_into_witness: False` e proveniência) | 3 de 20 `.olean` divergem entre as raízes autoral e revisora (fontes iguais; `.trace` distintos) — a recompilação da gerência é o árbitro; `all_trio=True` é literal em `audit_b6.py` |
| A1(b) — o habitante do traço | **ACEITO** (`scalarInverseLimitTraceData P : RegularCoreTraceData P` para todo `SiteProfile`; `scalarInverseLimitWeight_tracial`; nove leis ligadas a fornecedores) | os 36 `V351*` novos estão em `namespace TGLV350.Regular` (a pergunta da gerência de 14/09 segue: por quê não `TGLV351`?); só 2 sondas negativas para os 7 órfãos; «revisão independente» = raiz de build separada da MESMA bancada (por isso a gerência recompila tudo: é ela quem vale) |

**Bandeiras qgf/gpf/gpi:** nenhuma muda. A1(b) sozinho **não** quita `qgf_continuous_modular_realization_constructed` — falta A2 (os Three Locks no MESMO core, com este traço). Nada move o gate.

## 3. Erratas AO LADO do contrato da ORDEM 012 (aceitas pela gerência, em nome próprio)

As quatro paredes de B4 corrigem o que a ORDEM escreveu:
1. **Fluxo sem raio.** A errata de 14/05 escreve `dE = A(ρ+p)H dt`; com essa forma literal `Ḣ = −4πGΦH(ρ+p)` (um H a mais: `radius_free_flux_consequence`). A segunda equação é paga com o fluxo de Cai–Kim `A(ρ+p)H r_A dt`, `r_A = 1/H`.
2. **Entropia modificada como ENTRADA diferencial.** `dS = dA/(4GΦ)` é hipótese; a derivada de `S = A/(4GΦ(t))` carrega `−AΦ′/(4GΦ²)` (`variable_entropy_derivative`). A errata não controla esse termo; a ORDEM tampouco o nomeava.
3. **O critério de igualdade das duas rotas estava FALSO.** A ORDEM escreveu «igualdade sse todos os w_i com ρ_i+p_i ≠ 0 coincidem». Matéria + vácuo refuta: variância `ρ_mρ_Λ/(ρ_m+ρ_Λ) > 0` (`matter_vacuum_variance`, `nonzero_flux_support_does_not_characterize_equality`). O critério certo: w comum em TODO o suporte `ρ_i > 0`, vácuo incluído (`the_two_routes_equal_iff`). **Consequência física registrada:** com Λ presente, as duas rotas SEMPRE diferem em Ḣ.
4. **Unicidade do fator só com fluxo de entalpia E ≠ 0** (`zero_flux_has_no_unique_factor`); a primeira equação com Φ variável fica `H² = (8πG/3)P + C` sob primitiva fornecida (`tgl_first_friedmann_from_primitive`), sem forma fechada.

Correções adicionais apontadas pelos leitores/síntese da gerência (verbatim da bancada quando disponível):
- B1 — «A identidade do custo é uma normalização de forma autorizada por B1; não é dedução do valor de α nem de CODATA.» (ENTREGA_012_B1:9); «Definir alpha pelo custo é normalização de forma, não derivação do valor CODATA.» (REAPROVEITAMENTO_B1.md:299)
- B1 — «Aliás, ela dá o limite mais forte α<exp(−1/2); partir futuramente de um α externo com apenas `0<α<1` não bastaria para construir β<1. Isso é limite de instanciação, não pendência adicional de B1.» (revisao/CONSULTA_B1_CONTRATO_E_REUSO.md:23) — corrige a suficiência do «0 < α < 1» do (ii)
- B1 — «`leakage_rate_unique` recebe igualdade do semigrupo escalar completo. Para a escrita com gap g, ele identifica β₁g e β₂g; concluir β₁=β₂ exige o mesmo g não nulo. Se g também variar, só o produto é identificável. β>0 isoladamente tampouco exclui fechamento pleno quando g=0.» (CONSULTA:22); «A última cláusula identifica taxas de semigrupos iguais; não seleciona um β numérico nem identifica β separado de um gap desconhecido.» (ENTREGA:30)
- B1 — «O nome `hubble_form` não muda seu tipo. Sua ligação à equação métrica pertence aos alvos posteriores da ordem.» (CONSULTA:24); «closure_identity e hubble_form … não se reprovam identidades de anel» (ENTREGA:19)
- B1 — «941 entradas distintas lidas no dicionário embutido; ordem declara942. Números não equiparados silenciosamente.» (REAPROVEITAMENTO_B1.md:303) — corrige «fontes formais embutidos 942» da ORDEM §1
- B1 — «`ext_same_beta_reads_three_faces_kernel_proved → TGLExt.the_same_beta_reads_three_faces` está identificado como consumidor proposto, não já instalado.» (REVIEW_B1_FINAL.md:20); «Mathlib e os outros oito pacotes são caches copiados, com revisões confrontadas ao manifesto; não foram reconstruídos a partir de Lean fonte nesta rodada.» (ENTREGA:36) — limita a «reprodução standalone» do §5
- B1 — linhas envelhecidas da ORDEM: `the_pruning_threshold_is_the_reflection_amplitude` está em TheVerbalCoupling.lean:155 (ORDEM §2.1 diz :156); consumidor `ext_rp_hubble_form_kernel_proved` em um.py v353:133716 (ORDEM diz ≈133697 na v352) [medido]
- B2 — «Não se divide por H; H=0 não foi excluído. Lambda é existencial e não é automaticamente zero. A identificação com outra convenção física de Lambda exige explicitar o sinal. O teorema algébrico admite eta real com a divisão total de Lean; a leitura física de Newton usa G>0 e a calibração indicada.» (ENTREGA_012_B2:42)
- B2 — «H_null e H_conservation são hipóteses explícitas. B2 não afirma que a torre ou a natureza as fornecem.» (ENTREGA:42)
- B2 — «A busca não achou fornecedor FLRW; o ansatz univariado antigo é outra métrica e não será renomeado.» (ENTREGA:131) e «NÃO USAR como FLRW: outro ansatz, Ricci definido à mão» (ENTREGA:385/393) — corrige a ORDEM §2.1 que chama AnsatzEinstein de «o molde para FLRW»
- B2 — «Eta is arbitrary real in the algebraic theorem (Lean total division includes eta=0). Physical Newton specialization has positive G; no derivation of calibration is claimed.» (REVIEW_B2_FINAL.json semantic.limits[1]); «No global regularity outside U; conclusions evaluated at x in U; empty U would be vacuous» (limits[2])
- B2 — «Nenhuma entrada ext_* foi instalada no um.py: essa ação pertence à gerência, com a própria auditoria de integração.» (ENTREGA:123); «As quatro entradas `ext_flrw_*` são consumidores propostos, não instalação revisada.» (REVIEW_B2_FINAL.md:25)
- B3 — «campo `H_nx : HasDerivAt rho_i (-3H(1+w_i)rho_i)`. É INPUT, não conclusão microscópica.» (ENTREGA_012_B3:15)
- B3 — «PAGO condicionalmente em `tgl_friedmann_zero_cosmological`; H_zero_cosmological é explícita. Não foi provado Λ=0.» (ENTREGA:21) — a ORDEM (iii) pedia `H² = (8πG/3)·Σ ρ_i^TGL` sem Λ
- B3 — «A identidade aditiva `rhoTtot=rhoTot+beta*enthalpy` vale sem sinal de entalpia. A reescrita absoluta requer rhoTot>0 e enthalpy≥0.» (ENTREGA:38) — a ORDEM (iv) só pedia Σ(ρ_i+p_i) ≥ 0
- B3 — «Não se afirma positividade de cada densidade corrigida para w_i arbitrário; isso exigiria uma hipótese sobre seu fator. O suporte de densidades pode conter setores phantom nesta construção algébrica, desde que as hipóteses particulares de cada conclusão sejam satisfeitas.» (ENTREGA:38)
- B3 — «H_null é o balanço nulo para o stress corrigido concreto, não um teorema de realização física. G>0 e eta=1/(4G) continuam calibração INPUT. Não se divide por H. Não se declara existência de solução física não vazia. A convenção de B2 `G_tensor+Λg=κT` explica o sinal −Λ/3.» (ENTREGA:40)
- B3 — «O corolário zero recebe a equação tensorial hE e H_zero_cosmological, não a própria conclusão escalar H². O resultado não autoriza eliminar a constante existencial em outro consumidor. A distinção entre rota total e setorial na segunda equação fica para B4; B3 não a resolve por escolha.» (ENTREGA:42)
- B3 — «Fornecedores covetoriais tratam outro tipo de fonte e não satisfazem H_nx por homonímia.» (ENTREGA:514); «Não-troca setorial e w_i constante são hipóteses [INPUT]; TGL-S/TGL-L e Lema 3 continuam abertos.» (ENTREGA:519)
- B4 — «[REAL — B4 entregue com teoremas condicionais e paredes que corrigem quatro enunciados do contrato original. Contrato literal NÃO certificado; nenhuma rota escolhida.]» (ENTREGA_012_B4:1); «Não se certifica a redação literal incorreta da ordem: as quatro correções abaixo são parte obrigatória do alcance» (REVIEW_B4_FINAL.md:5)
- B4 (i) — «Segunda equação Ḣ=−4πGΦ(ρ+p) | PAGO para fluxo A(ρ+p)H r_A, r_A=1/H. NÃO PAGO na escrita literal sem r_A: radius_free_flux_consequence prova o fator H extra.» (ENTREGA:15); «Fluxo: eq. (2.12) de Cai–Kim tem o fator raio aparente. A errata/ordem omitem esse raio e não produzem a segunda equação declarada.» (ficha :34) — [medido] errata_cosmologica_TGL.tex:371/381/384–390 tem de fato um H sobrando
- B4 — «Entropia modificada | PAGO como entrada diferencial dS=dA/(4GΦ). NÃO se identifica automaticamente com a derivada de S=A/(4GΦ(t)); variable_entropy_derivative prova o termo adicional −AΦ'/(4GΦ²).» (ENTREGA:16); «S=A/(4G*Phi) não implica dS=dA/(4G*Phi) quando Phi varia.» (ficha :35)
- B4 (ii) — «Primeira equação, Φ variável | PAGO sob primitiva fornecida com derivada Φρ'; não se prova existência de uma primitiva para função arbitrária. H²=(8πG/3)P+C. O produto Φρ tem defeito de derivada −(8πG/3)Φ'ρ.» (ENTREGA:18); «Não prova C=0.» (ENTREGA:17)
- B4 (iii) — «Diferença entre rotas | PAGO: diferença das fontes = β·variância≥0. Diferença de Ḣ = −4πG vezes essa expressão.» (ENTREGA:19); «Critério de igualdade | PAGO com suporte ρ_i>0, incluindo vácuo. Critério literal ρ_i+p_i≠0 é refutado por um exemplo Fin2 matéria+vácuo.» (ENTREGA:20); «Dois setores com ρ_m>0 e ρ_Λ>0, w_m=0 e w_Λ=−1, têm só um setor de fluxo não nulo, mas variância ρ_mρ_Λ/(ρ_m+ρ_Λ)>0. Esse contraexemplo tipado impede a implementação do critério incorreto da ordem.» (ENTREGA:40)
- B4 (iv) — «Fator reconciliador único | PAGO com entalpia total E≠0. No fluxo zero zero_flux_has_no_unique_factor prova ¬∃! fator.» (ENTREGA:21); «Fator comum quando w constante | PAGO sob suporte de densidade comum, E≠0 e 1+w≥0; a última hipótese permite a leitura absoluta.» (ENTREGA:22); «Se E=0, ou nenhuma solução existe ou todos os fatores resolvem; não há unicidade. Estes resultados não escolhem a lei a usar no D1.» (ENTREGA:42)
- B4 — «O raio é parte da prescrição primária de [Cai–Kim, eq. 2.12]. A correção diferencial Φ_TGL é INPUT da construção. Sua identificação com uma entropia de estado variável exigiria controlar o termo Φ' ou introduzir uma lei adicional explicitamente — nenhuma foi presumida. O fato de a primeira lei valer sob essas entradas não constrói H3 para a realização microscópica.» (ENTREGA:29)
- B4 — «A constante C sobrevive; B3 também mantém Λ na equação 00 e exige H_zero_cosmological para eliminá-lo. A hipótese de não-troca H_nx e w_i constante permanece de B3. Escala G/η INPUT, Lema3 global OPEN, fechamento perturbativo TGL-S/TGL-L OPEN.» (ENTREGA:44); o «modo de TheImportedEquilibrium» foi realizado por estrutura própria (HubbleHorizonInput) com citação, não por instanciação de EquilibriumInput/discharge_by_import [medido por grep]
- B5 — «As duas últimas linhas são aplicações separadas de teoremas anteriores, não uma identificação entre as duas rotas que B4 distinguiu.» (ENTREGA_012_B5:33); «Os quatro corolários … Não acrescentam um segundo parâmetro ou uma segunda lei de fundo.» (ENTREGA:7)
- B5 — «O kernel usa beta variável; a forma geométrica não deriva o valor experimental de alpha. O ângulo lê o mesmo fator e não seleciona lei por ajuste ou por resultado cosmológico. Nenhum observável independente foi criado, nenhum fechamento global ou perturbativo foi provado.» (ENTREGA:35); «Nenhum theta, seno, cosseno ou raiz de beta é inserido em r_s, D_M, l_A ou worker H(z).» (ficha, ENTREGA:343)
- B5 — [não declarado pela bancada; medido] a ORDEM pede `the_passage : sin²θ_M = β → (as equações de B3/B4)`; entregue: premissa como TEOREMA (coupling_eq_sin_sq) e equações repartidas (the_passage = só Ḣ de B4; the_angle_reads_sector_first = só H² de B3), com w e enthalpy reais livres
- B6 — «PAGO como estatuto, não como construção de H3. the_trio_is_a_pair exige imported:H2→H3.» (ENTREGA_012_B6:15); «importing a theorem as an implication does not construct its horizon/equilibrium premise. The four literature sources do not prove Phi_TGL.» (ficha :185–186)
- B6 — «O campo KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED qualifica essas referências bibliográficas, não rebaixa os teoremas condicionais efetivamente provados em B2–B5. A extensão modificada da entropia é entrada da TGL; nenhuma citação acima a prova.» (ENTREGA:52); «Temperatura FLRW dinâmica é uma prescrição explicitada em B4, não consequência irrestrita da referência de 1977.» (ENTREGA:52)
- B6 — «Na linha da constante, INPUT qualifica a escolha do caso sem constante: a existência de Λ/C já é conclusão dos teoremas gerais, e eliminá-la exige uma condição adicional.» (ENTREGA:40); «Nas linhas REAL, o estatuto é da implicação formal com as hipóteses indicadas, não da ocorrência física de seus antecedentes.» (ENTREGA:40)
- B6 — «AreaScale fornece identidades de normalização, sem medir/derivar G. A identidade total de divisão, inclusive sua elaboração em G=0, não constitui calibração física; a interpretação usa G>0.» (ENTREGA:111); «“all_trio” foi interpretado como subconjunto permitido, não como presença obrigatória dos três.» (ENTREGA:109); «A aceitação documental usa recompilação própria rc0 e os dez tipos/axiomas conferidos, sem alegar reprodução binária integral dos fornecedores.» (ENTREGA:144)
- A1 (transversal às 35) — «Não se afirma U_t=π(Λ_t): o operador relativo pode estar no comutante» (acao_modular_no_core_inteiro:7); «O sinal conjugado decorre da antilinearidade de J; não pode ser apagado» (:255); «JU_tJ⁻¹=U_t ... não U_−t» (reproducao_sete_fornecedores:26); «não se afirma reprodução byte a byte desses objetos históricos» (:34); «Total de jobs Lake inclui cache, não equivale a número de novas provas» (:153)
- A1 — ADENDO_GERADOR_ANTECEDENTE_ESCALAR: «A identificação entre espaços e suas representações não vem do nome nem de uma isometria abstrata» (grafo_positivo_regular:332) — o antecedente escalar Continuous049–050 não se instancia na fibra vetorial; adendos documentais ao lado: enunciados truncados (Fourier, absorção), localizador CFC commute_cfc vs commute_cfcHom (comutação :Commute.lean:87), linha do campo tracial 59→58 (extensão tracial), pin DEV → snapshot (seno, V2), fornecedor OrderHomClass → scalarGNSRepresentation_monotone (ordem)
- A1 (rota vs LACUNAS_A1.md) — «LACUNAS_A1.md é um mapa histórico» (CONSULTA_TRACIALIDADE_LIMITE, [DERIVED/OPEN]); a ponte (3) foi paga por transporte direto do grafo espectral e^{−2πξ}, não por «unicidade do gerador e relação de Weyl»; a ponte (1) não recebeu teorema — a rota partiu de ν = scalarDualWeight; «A matemática verificada aqui não identifica h com Delta_nu nem confirma uma realização física.» (CONSOLIDACAO:3)

## 4. A cunhagem do operador de 15/09 e o alvo B1′ — a QUARTA face de β (o acoplamento não mínimo na ação)

«Permanência = desejo de estar junto e quente = acoplamento não mínimo = β_TGL» `[ONTO — cunhagem do operador]`. Âncoras REAL no Artigo A (`tgl_paper_unified.py`, §«The TGL Lagrangian»):
`ℒ_grav = R/(2κ²) + ξ·R·|Ψ|²` com **ξ = 1/6** (acoplamento conforme); `ℒ_modular = ℒ_ΛCDM·β·|1+w_eff|`; equação de movimento **`(□ − m_Ψ² − ξR)Ψ = β·K_∂·Ψ`** — «the presence of β as the
sole coupling between Ψ and K_∂ is the operational signature of TGL». A leitura do operador nomeia β como O acoplamento não mínimo (o modular, Ψ–K_∂), e esse acoplamento como a permanência
(junto = acoplado; quente = KMS à temperatura de Unruh/Gibbons–Hawking). **O número ao lado da frase:** o coeficiente do termo `ξR|Ψ|²` é 1/6, não β — os dois acoplamentos não se fundem.

**B1′ (alvo novo, mesma pasta, mesma disciplina de ficha):** tipar a quarta face — a equação de movimento com β como acoplamento Ψ–K_∂ — no molde de `TGLCoupling`: uma estrutura
`ActionCouplingData` (ou nome melhor) com o operador de campo, o termo conforme com coeficiente PRÓPRIO `ξ` (variável real; **nunca** identificado com β), o gerador `K_∂` importado
como dado (o `EquilibriumInput`/`towerEquilibriumInput` e o fluxo modular da casa são os fornecedores a examinar), e o teorema `the_same_beta_reads_four_faces` que estende
`the_same_beta_reads_three_faces` com a face «acoplamento na ação»: o coeficiente do termo modular da EOM é o MESMO β de `TGLCoupling`. Sem numeral; sem `axiom`; K_∂ e ξ como hipóteses
nomeadas; ficha de aproveitamento antes (fornecedores candidatos: `TheVerbalCoupling`, `TheImportedEquilibrium`, `NoFullWitness`, `TheDammingByExpansion`, `RhoPlusPClosure`, os módulos
B1–B4). **Aceitação:** teorema no trio; consumidor `ext_pb_same_beta_four_faces_kernel_proved` proposto na ficha; explicitar o que NÃO se prova (que a natureza realiza a EOM; que ξ = 1/6 é derivado).

## 5. A sequência (vale até ordem em contrário do operador)

1. **A2 (ORDEM 011)** — os Three Locks no MESMO core, com o traço de A1(b): operadores afiliados, `P_F` no core com `0 < τ(P_F) < ∞` pelo traço `scalarInverseLimitTraceData`, gap relativo;
   é o alvo que quita, com A1, `qgf_continuous_modular_realization_constructed`. Comece por ele. Ficha de aproveitamento obrigatória (o `threeLocksFromSupport` e a `SusyRelativeData` são fornecedores).
2. **B1′** (§4) — pode correr em paralelo se houver sessão livre; é pequeno.
3. **A ROTA do fundo NÃO é da bancada:** fator sobre o total vs fechamento setorial — a ratificação é do operador; a V3 do D1 é da gerência, pré-registrada depois. Não toque no D1.
4. Pendências de forma a responder na próxima ENTREGA: (a) por que `TGLV350.Regular` para módulos `V351*`; (b) o homônimo `H_nx` (B3 vs B4) — sanear; (c) sondas negativas por módulo nos 7 órfãos;
   (d) as declarações `antiunitaryConjugate_add/_smul` em `V350LocalBasePolarCommutation` E em `V351AntiunitaryResolventPhase` (mesmo namespace, α-equivalentes; a toolchain aceitou) — explicar e sanear;
   (e) **errata AO LADO em `LACUNAS_A1.md`** (ainda diz «Um termo desse contrato ainda não foi produzido»): registrar que o habitante existe, que a rota pagou a ponte (4) pelo conteúdo, a (2) por
   `scalarTomitaImaginaryPower_eq_regular_implementation` sem o nome, a (3) por transporte direto do grafo espectral, e que a (1) foi dispensada pela rota (partiu de ν = `scalarDualWeight`);
   (f) B3: expor o corolário ADITIVO `H² = (8πG/3)·Σρ_i^TGL − Λ/3` sem `hr`/`he` (hoje só a forma multiplicativa, que exige ρ_tot > 0 e entalpia ≥ 0 em todo U); (g) B6: explicar os 3 `.olean`
   divergentes entre as suas raízes (`MixedLadder`, `SecondCone`, `TGL/AreaScale`) — para a gerência não importa (a recompilação própria é o árbitro), mas fica registrado; (h) `maxHeartbeats` acima do
   padrão em 34 dos 44 módulos (até 6.000.000): declarar por módulo o motivo, como já faz em alguns.

Registro da gerência sobre a própria incorporação (para não parecer que a bancada errou): as bandeiras consumidoras receberam os prefixos da casa (`ext_pb_*`, `ext_a1b_*`, como `ext_rp_*`,
`ext_fh_*` das pedras anteriores), não os nomes propostos nas fichas — a tabela do §1 é o mapa; as quatro entradas `EXTERNAL_KNOWN_THEOREMS` entraram VERBATIM da sua proposta, inclusive três
espaços faltantes («Seção2», «das85», «respondeu401») que a gerência corrige na próxima versão; Jacobson 1995 fica citado em dois lugares do `um.py` (`_GRAVITY_IMPORT_CITATIONS` e
`EXTERNAL_KNOWN_THEOREMS`) até a gerência os cruzar; a PRIMEIRA rodada da v354 reprovou por erro da gerência (15 `#print axioms` de lemas privados dos seus módulos postos no Audit canônico) —
preservada e emendada; a sua cópia `RETOMADA_A1B_012\k\TGLExt.lean` é a raiz-base V351 (874 imports, sem os 19 `V351*` da v353): não afeta a prova (builds por alvo), mas não é cópia literal da v353.

Bandeiras que a gerência ainda vai conferir por conta própria (não pedem ação sua):
- [VERMELHA — baseline moveu DURANTE a leitura, medido] Nós\um.py: c1c761809efcde52… (12.864.360 B, 14/09 14:10) → aa7fb7c732d4648962e09627c9bf73b49d520aad966d418f54ef1713c21b9842 (13.200.596 B, CRLF 181.314 / LF-only 364, 15/09 09:00:12); Nós\tgl_kernel\TGLExt: 908 → 952 (os 44 módulos novos, 0 auditores), umbrella TGLExt.lean 1a9caaa7… (893 imports) → 52b830f6… (937 imports; 44 imports acrescidos, 0 removidos); rodada_v354_stdout.txt criada 09:15:06 («46 escritos, 939 inalterados»). Toda afirmação «NOVO vs canônico» deste relatório é relativa ao v353 (908) medido antes das 09:00; às 09:13 os 44 estão PRESENTES no canônico, byte-idênticos às fontes da bancada (44/44 iguais, 0 diferentes; baseline 908 inalterada). A gerência deve confirmar que a escrita foi sua (rito v354) e que a régua do backup imediato foi cumprida antes de tocar um.py/kernel.
- [VERMELHA — selo/versão] o selo em disco (um_absoluto_selo.json 52e4712d…, 14/09 14:27) ainda é o v353; a rodada v354 está em execução por outra sessão — não custodiar nem citar «v354 selada» até o stdout completo e o selo novo existirem; HANDOFF_v354 inexistente.
- [AMARELA — nomes instalados ≠ propostos] o um.py v354 instalou 28 entradas com prefixos ext_pb_*/ext_a1b_* (L133959–133985), não os nomes propostos nas fichas (ext_same_beta_reads_three_faces_kernel_proved, ext_flrw_*, ext_tgl_friedmann_from_sector_closure_kernel_proved, ext_the_two_routes_differ_kernel_proved, ext_the_angle_reaches_the_metric_kernel_proved, ext_the_passage_kernel_proved — 0 ocorrências); as fichas/entregas citam os nomes antigos — registrar o mapeamento na memória para não virar homônimo documental.
- [AMARELA — strings B6 verbatim no um.py] L134883 «Seção2 primária lida, eqs.2.3,2.12–2.17», L134891 «das85 páginas», L134899 «respondeu401» — espaços faltantes copiados da PROPOSTA (sha 42eb7f61…); cosmético, mas fica no artefato canônico.
- [AMARELA — duplicidade Jacobson] Jacobson 1995 já constava em _GRAVITY_IMPORT_CITATIONS['H3_horizon_data_produced'] (v353 L134211) e agora também em EXTERNAL_KNOWN_THEOREMS v354 (L134874–134881) — duas localizações sem referência cruzada.
- [AMARELA — raiz k não é cópia literal do v353] RETOMADA_A1B_012\k\TGLExt.lean = umbrella do kernel-base V351 (378df01c…, 874 imports, mtime 17:31 mas conteúdo do kernel-base de 07:53), faltam os 19 imports V351* do umbrella v353; a pasta k\TGLExt/ é 908/908 idêntica ao v353. Os builds foram por alvo (`lake build TGLExt.X`), logo sem efeito de prova, mas a frase «raiz copiada do kernel canônico v353» (ORDEM 012 §5) não vale para o umbrella de k; v/ não tem umbrella.
- [AMARELA — 3 .olean divergentes em B6, medido] MixedLadder.olean (6a7edf2f… vs 88cfc0be…, 220.176 B ambos), SecondCone.olean (bd71610e… vs 5ad145d1…, 4.052.408 B ambos), TGL/AreaScale.olean (2baa4678… 83.120 B vs a3a200c1… 83.112 B) diferem entre V353/kernel e V353/s; os 7 .olean dos alvos B1–B6 são iguais. A bancada diz «causa de serialização não estabelecida». Reproduzir na raiz da gerência antes de custodiar.
- [AMARELA — revisor] em todas as 41 entregas a «revisão independente» é raiz Lake distinta (s/ r/ v/) com scripts da própria bancada; nenhum JSON registra identidade do revisor; sondas relidas, não reexecutadas pelo revisor; Mathlib + 8 pacotes = cache copiado, nunca reconstruído; em B5 o texto «semântico» é literal hard-coded em finish_b5_review.py:90–97 e a ENTREGA é template (deliver_b5.py:42–102). 24 dos 35 ReviewA1*.lean em v/ são byte-idênticos ao AuditA1* correspondente (ex.: ReviewA1Absorcao = AuditA1Absorption a47c505b…). ORDEM 012 §5: «o auditor da gerência recompila de novo, independentemente, e é ele quem vale».
- [AMARELA — homônimo H_nx] SectorFluidClosure.lean:24 (campo setorial `H_nx : ∀ i t, t ∈ I → HasDerivAt (rho i) (-3*H t*(1+w i)*rho i t) t`) e ThermodynamicFriedmann.lean:112 (hipótese de fluido único `H_nx : ∀ t∈I, deriv rho t = -3*H t*(rho t+w*rho t)`) — mesmo nome, dois objetos; não usado como ponte; sanear na documentação/mapa.
- [AMARELA — homônimo canônico pré-existente] TGLV350.Regular.antiunitaryConjugate_add/_smul declarados em V350LocalBasePolarCommutation.lean:13/:21 E em V351AntiunitaryResolventPhase.lean:44/:49 (ambos canônicos, mesmo namespace, enunciados α-equivalentes); ambos no fecho de imports de V351ScalarImaginaryCoreAction; toolchain aceitou (rc0, sem 'already contains'). Duplicação a sanear, não ponte.
- [AMARELA — alpha] TGLExt.TGLCoupling.alpha := c.beta / Real.exp (1/2) (TheSameBetaReadsThreeFaces.lean:32) é α DERIVADA de β (forma), não α_fine/CODATA; qualquer consumidor que a leia como constante de estrutura fina faz ponte por homônimo; a entrada ext_pb_beta_eq_alpha_radical_kernel_proved deve dizê-lo.
- [AMARELA — namespaces] B2–B5 declaram em ChatgptAudit.FLRW (dentro de arquivos TGLExt/*.lean); os 36 A1 declaram em TGLV350.Regular (não TGLV351); B1 em TGLExt; nenhuma colisão de nome bare com os 908 canônicos [medido: 296 nomes novos, 0 colisões, 0 duplicados entre novos].
- [AMARELA — custo] maxHeartbeats acima do padrão em 34 dos 44 módulos: até 6.000.000 (V351ScalarImaginaryCoreAction:6; blocos locais em V351ModularCutBalance e V351QuadraticTrace) e 2.400.000 nos B2/B3/B5; V351ModularCutBalance tem 33 KB, 605 linhas, 9 teoremas privados, 37 tentativas DEV (30 rc1).
- [AMARELA — objetos sem consumidor interno] B1 reflection_cost/reflection_rejects_bare_alpha (controles); B3 rho_nonneg (campo inerte) e lambda_drops_out (listado REUSAR, não invocado); B4 8 dos 13 fornecedores marcados REUSAR não consumidos (EquilibriumInput/discharge_by_import não instanciados — HubbleHorizonInput própria); V351FourierTranslation não é importado por nenhum módulo do 1º lote (só por V351RegularImaginaryPowers/V351RegularGeneratorDualScaling depois).
- [AMARELA — forma dos enunciados vs ORDEM] B3: a forma ADITIVA H² = (8πG/3)·Σρ_i^TGL não é exposta como conclusão (só a multiplicativa, que exige ρ_tot>0 e entalpia≥0 em todo U); B5: the_passage não tem a forma pedida `sin²θ_M = β → …` (premissa provada; equações repartidas em dois teoremas; w e enthalpy reais livres) — desvio não declarado pela bancada.
- [INFO — sondas] 49 stdouts Bad*: 47 «Type mismatch»; os 2 sem (audit_B2\20260914_162254_145307\BadFLRW00/BadFLRWLambda) são erro de sintaxe («unexpected token '('») de tentativa anterior, superada pela aceita 162529 (rc1 Type mismatch). Só 2 sondas para os 7 órfãos; 1 sonda fraca (R ≤ 0) para as 15 declarações de V351RegularPositiveGraph.
- [INFO — cronologia] «ficha antes do código» só por metadados locais (B1: 78 s; B5: 49 s); adendos posteriores ao DEV em V351InverseLimitScaling (22:59:23), V351InverseLimitSemifiniteness (23:14:09), V351InverseLimitTracialExtension (23:54:39), V351InverseCutoffCFC (21:24:15) — todos declarados.
- [INFO — rótulos] complete.json das validações do fechamento GNS e dos limites da ação direita trazem status 'AUTHOR_INVERSE_CUTOFF_VALIDATED…' (rótulo reaproveitado; só o 2º não declarado); AUDITORIA_BALANCO_DOS_CORTES truncou o enunciado e foi corrigida em _TIPO_COMPLETO sem reexecução; audit_b6.py tem all_trio=True hard-coded (a checagem real é 'subconjunto do trio').
- [INFO — quebras de linha] os 44 fontes são só-LF (0 CRLF); o um.py v354 mantém quebras mistas (181.314 CRLF / 364 LF) — nunca converter (régua v351).
- [INFO — documental] LACUNAS_A1.md (cf0ef326…, 14/09 08:24) diz «Um termo desse contrato ainda não foi produzido» enquanto CONSOLIDACAO (fad4a505…, 15/09 03:37) declara o habitante — errata ao lado pendente; 4 ENTREGAs A1 da manhã de 14/09 (08:24, 09:10, 09:44, 10:22; sem RECIBO) ficam fora do escopo das 35.

## 6. Os insumos (sha16 lido agora)

| papel | caminho | bytes | sha16 |
|---|---|---|---|
| o programa canônico v354 (SÓ LEITURA) | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` | 13,199,072 | `07d52f89e04c77d9` |
| o selo v354 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json` | 51,909 | `9916df9e97442af6` |
| o manifesto do kernel v354 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel_proof_manifest.json` | 1,211,516 | `bed4a5e1f3dd072d` |
| o stdout canônico da rodada v354 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\rodada_v354_stdout.txt` | 194,173 | `cdf6243b2b70e7b2` |
| a recompilação independente da gerência (85/85) | `C:\tmp\b_audit\RECOMPILACAO_15SET.json` | 99,449 | `c68ef6cb9e423e2f` |
| o manifesto da incorporação v354 (módulos, prints, ext_*, EXTERNAL_KNOWN) | `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\d554e796-415e-450f-9fd4-dd07892b02b9\scratchpad\v354_incorporacao_manifesto.json` | 26,322 | `acd8aa5e0367d79e` |
| a ORDEM 012 (o contrato; as erratas acima valem ao lado dele) | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_012_a_passagem_da_acao_a_metrica.md` | 29,534 | `a9cb2a7b812afc43` |
| a emenda da v354 (rodada 1 reprovada por nomes privados; restauração por bytes) | `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\d554e796-415e-450f-9fd4-dd07892b02b9\scratchpad\EMENDA_V354.json` | 3,156 | `5a01ed8c754f3f47` |

**A leitura das suas 41 entregas pelos leitores da gerência (11 relatórios + síntese, 15/09), copiada para `C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_012_RECIBO_INSUMOS\`** — são medições (arquivo:linha, sha) do que você entregou;
sirva-se delas para responder às pendências do §5:

| relatório | bytes | sha16 |
|---|---|---|
| `ler_A1-lote1.json` | 83,336 | `09cedce893a06067` |
| `ler_A1-lote2.json` | 59,015 | `ada04872dd3aeb01` |
| `ler_A1-lote3.json` | 70,882 | `97d42baaf7de540b` |
| `ler_A1-lote4.json` | 67,613 | `76a130835ea14137` |
| `ler_A1-lote5.json` | 69,044 | `6b9d1c348934460b` |
| `ler_B1.json` | 32,389 | `c2718bac31a446dd` |
| `ler_B2.json` | 34,595 | `eb577cf3cd1af576` |
| `ler_B3.json` | 30,920 | `e438290572b9d040` |
| `ler_B4.json` | 41,693 | `bf0bcf16c9ed40f0` |
| `ler_B5.json` | 33,117 | `1d536be200298764` |
| `ler_B6.json` | 34,518 | `e7f755aed01aadd6` |
| `sintese.json` | 107,104 | `43141577656ec093` |

*Recibo e adendo não movem o gate. A matemática prova a implicação; a construção concreta prova as hipóteses; a natureza decide a teoria.*
