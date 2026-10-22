# SÍNTESE — Caça da Âncora de Massa de Coma (4 frentes auditadas)

**Para decisão do OPERADOR. Nada abaixo está aprovado; `approved_for_primary_blind_test=false` em tudo.**

---

## 1. Tabela de candidatas (consolidada, deduplicada entre as 4 frentes)

| Fonte | Método | Massa (M_sun) | Dependências (motor) | M ∝ D^n | Veredito |
|---|---|---|---|---|---|
| **Mirakhor & Walker 2020** (MNRAS 497,3204) | HSE híbrido: P do SZ Planck + n_e do XMM; T=P/n | **M_200 = (8,50±0,55)e14** (h=0,7 travado) | z=0,0231 + H0=70 + ΛCDM em θ→r; abertura r500=47' herdada de Planck Int X | **n = +0,5** (P∝D⁻¹, n_e∝D^(−1/2)) | **WEAKLY_DEPENDENT_DECLARED — RECOMENDADA** |
| Okabe+2014 (ApJ 784,90) | WL Subaru, LSS modelada, r_vir angular publicado (96,67') | M_200 = 6,23 (+2,53/−1,58)e14 h⁻¹ | z + H0 + ΛCDM em Σ_crit e θ→r; ⟨D_ls/D_s⟩=0,9554 declarado | n=1 (modo h); n≈0,08–0,24 (distância-pura) | DEPENDENT (melhor WL; reconstrutível para qualquer D) |
| HyeongHan+2026 (arXiv:2606.12523) | WL HSC ~12 deg², maior S/N existente | M_200c = (8,2±0,7)e14 (H0=70 embutido, sem h⁻¹) | z + H0 + ΛCDM **+ prior c-M de simulação** (dupla injeção) | n=1 (h); ~0,27 (dist.-pura); prior c-M não fatorável | DEPENDENT (preprint não aceito) |
| Kubo+2007 (ApJ 671,1466) | WL SDSS | M_200 = 1,88 (+0,65/−0,56)e15 h⁻¹ | z + H0 + ΛCDM | n=1 (h) | DEPENDENT — **DESCARTAR** (viés +3x por LSS não modelada, per Okabe+2014) |
| Gavazzi+2009 (A&A 498,L33) | WL CFHT (campo pequeno) | M_200c = 5,1 (+4,3/−2,1)e14 h70⁻¹ | z + H0 + ΛCDM; dominada por priors | n=1 (h) | DEPENDENT — só consistência |
| Planck Int X 2013 (A&A 554,A140) | Y_X–M (calibração Arnaud+2010) | M500≈6e14 implícito; **r500=47' — origem da abertura de todos** | z + H0 duplo (direto + herdado da calibração externa) | n ≈ 1,4 | DEPENDENT (cadeia longa; circularidade de abertura) |
| PSZ2 2016 | Y_SZ–M de catálogo | M500≈6e14 | calibração entrelaçada; Coma flagado extenso demais pelo próprio Planck | n ≈ 1,2 (não auditável ponta a ponta) | DEPENDENT — não usar |
| Simionescu 2013 (ApJ 775,4) | Suzaku, perfis T/n até 2 Mpc (sem massa própria) | — (abertura herdada de Planck) | z + H0 nos perfis físicos | n=1 se re-derivada HSE pura | DEPENDENT — fornecedora de perfis brutos |
| Churazov+2021 (eROSITA) | Imageamento; massa 100% herdada | M500~6e14 (citação de Planck) | herança integral | n herdado (~1,4) | DEPENDENT — não usar como âncora |
| Hughes 1989 (ApJ 337,21) | HSE X puro + óptico | M(<5 h50⁻¹ Mpc) = (1,85±0,24)e15 h50⁻¹ | z + H0, **exemplarmente declarado** (h50⁻¹) | **n=1 exato** | DEPENDENT — padrão de auditabilidade; M/R invariante de D |
| The & White 1986 | Virial generalizado | M(<2,7 h⁻¹ Mpc) = 0,95e15 h⁻¹ | z + H0 (cz/H0) | n=1 exato | DEPENDENT |
| Geller, Diaferio & Kurtz 1999 | Cáustica (infall, até 10 h⁻¹ Mpc) | M(<10 h⁻¹ Mpc) = (1,65±0,41)e15 h⁻¹ | z + H0; F_β de simulações | n=1 exato | DEPENDENT — útil para testar a FORMA M(r) (livre de D) |
| Rines+2003 CAIRNS | Cáustica + virial + projetada | M_200 = 7,85e14 h⁻¹; M_vir=(9,32±0,43)e14 h⁻¹ | z + H0; F_β | n=1 (h); ~0,7 (dist.-pura, sobredensidade) | DEPENDENT — tripla checagem interna, tabelas verificadas no PDF |
| Łokas & Mamon 2003 | Jeans (dispersão + curtose) | M_vir = 1,4e15 h70⁻¹ (±30%) | cadeia mais transparente da literatura: cz→7093 km/s→H0=70→D=101,3 Mpc | n=1 | DEPENDENT — âncora secundária didática |
| Sohn+2017 / Kang+2025 | Cáustica moderna (12.989 z) | M_200 = (1,18±0,20)e15 h⁻¹ | z + H0; F_β=0,7 | n=1 (h); ~0,7 (dist.-pura) | DEPENDENT — banda sistemática do método cáustico ~50% vs CAIRNS |
| Pedratti+2026 (DESI espectroscopia) | Jeans MG-MAMPOSSt | M_200 = 1,04 (+0,07/−0,08 ±0,09)e15 | z + H0 + ΛCDM (NÃO usa FP-DESI; livre da circularidade FP) | n=1 | DEPENDENT |
| Falco+2014 | Infall vs fluxo de Hubble | M_vir = (9,2±2,4)e14 | **H0 entra na própria equação do sinal** | n não fatorável | DEPENDENT — **EXCLUÍDA** (motor proibido) |
| Ho+2022 | CNN em espaço de fase | M_200 = 1,26 (+0,52/−0,37)e15 h⁻¹ | cosmologia de treino opaca (caixa-preta) | n≈1 nominal, não verificável | **UNCLEAR** — inutilizável em pré-registro |
| M_gas (X) — perfil em MW20 | Massa de gás do brilho X | ~1,2–1,4e14 [INPUT pendente — extrair do perfil] | z + H0; ponte gás→total exige f_b cósmico | **n = 2,5** (maior alavanca) | DEPENDENT — só com ponte declarada |

---

## 2. A VERDADE ESTRUTURAL: não existe âncora INDEPENDENT

**Resultado da caça (4 frentes, ~20 candidatas): zero INDEPENDENT.** E não é acidente bibliográfico — é estrutural:

- Os observáveis brutos de um aglomerado são **ângulos** (adimensionais), **velocidades e temperaturas espectroscópicas** (livres de D) e **fluxos** (∝D⁻²). Toda massa exige um comprimento físico, e o único conversor ângulo→comprimento é a distância assumida: `r = θ·D_A(z_Coma, H0, ΛCDM)`. Dinâmica pura mede `GM/D` (n=1); fótons medem `M·D^(−2)` a `M·D^(−5/2)`; lensing mede `M/(D_l·D_s/D_ls)`.
- A prova definitiva: a combinação X+SZ **não produz massa com n=0 — produz a própria distância** (método clássico de D_A, Birkinshaw 1999). Se existisse massa livre de D, esse método não funcionaria.
- **Agravante específico do teste:** a lei de previsão M=K·R também escala como D¹. Toda âncora com n=1 (TODA a Frente 3 dinâmica, HSE X puro, WL em unidades h⁻¹) é **exatamente degenerada**: a distância cancela identicamente e o confronto vira um teste da constante K (≡ σ²/G), não de D.

**Significado para o teste primário cego:** o veredito honesto é **NOT_IDENTIFIABLE** — a distância de Coma não é identificável por confronto massa-primária vs lei M=K·R usando a literatura existente, porque nenhuma massa publicada é independente de distância e as de cadeia mais limpa são degeneradas (n=1). Pela régua do programa (negativos honestos são resultados), **NOT_IDENTIFIABLE é RESULTADO científico**, deve ser pré-registrado como desfecho possível e publicado como tal se ocorrer. Não é fracasso do teste; é a anatomia da literatura de Coma, agora auditada elo a elo.

---

## 3. RECOMENDAÇÃO — modo secundário declarado

**Âncora: Mirakhor & Walker 2020.** Única com n≠1 de cadeia curta e 100% auditável (dados XMM e Planck públicos; expoente n=+0,5 derivável analiticamente; f_gas(r200)≈cósmica sugere viés HSE pequeno). M/R ∝ D^(−1/2) quebra a degenerescência com M=K·R. Ressalvas obrigatórias: (i) o n=0,5 vale onde T=P_SZ/n_X — verificar seção a seção se o núcleo usa T espectroscópica (ali n→1); (ii) viés hidrostático 10–20% (merger NGC 4839, excluir setor SW) não escala com D; (iii) abertura r500=47' herdada de Planck Int X — circularidade de abertura a declarar; (iv) o expoente foi derivado pelo auditor, não pelos autores — **pré-registrar a derivação**.

Apoios: Okabe+2014 (WL, raio angular publicado, reconstrutível para qualquer D) como âncora WL secundária; M_gas (n=2,5) como alavanca máxima SE a ponte gás→total for declarada; âncoras n=1 (Kang 2025, Łokas & Mamon, Hughes) apenas para teste de K e da forma do perfil.

`coma_mass_anchor.json` proposto (a aprovação é do OPERADOR):

```json
{
  "anchor_id": "coma_mass_anchor_v1",
  "mass_Msun": 8.50e14,
  "sigma_stat_Msun": 0.55e14,
  "sigma_sys_Msun": 1.3e14,
  "sigma_sys_note": "vies hidrostatico 10-20% (merger NGC 4839; nao escala com D) — adotado 15%; f_gas(r200) ~ cosmica sugere vies pequeno nas direcoes calmas",
  "definition": "M_200c (sobredensidade 200x rho_crit(z))",
  "aperture_definition": "r200 = 70 arcmin = 2.0 Mpc na distancia assumida (1' = 28 kpc); abertura herdada de r500 = 47 arcmin de Planck Int. X 2013 (circularidade de abertura declarada)",
  "source": "Mirakhor, M. S. & Walker, S. A. 2020, MNRAS 497, 3204; arXiv:2007.12194; DOI 10.1093/mnras/staa2203",
  "method": "Massa hidrostatica hibrida: pressao eletronica do perfil y do Planck SZ + densidade eletronica da deprojecao do mosaico XMM-Newton; T = P/n (derivada, nao espectroscopica); M_HSE de dP/dr ate ~r200, cobertura azimutal quase completa",
  "uses_H0": true,
  "uses_cluster_redshift": true,
  "uses_assumed_distance": true,
  "uses_cosmological_model": true,
  "assumed_cosmology": "flat LCDM, Omega_m = 0.3, Omega_L = 0.7, H0 = 70 km/s/Mpc, z_Coma = 0.0231 (Struble & Rood); numero publicado TRAVADO em h = 0.7, nao declarado em h^-1 pelos autores",
  "independence_verdict": "WEAKLY_DEPENDENT_DECLARED",
  "dependency_notes": "M ∝ D^n com n = +0.5 (DERIVADO PELO AUDITOR, nao pelos autores — derivacao a pre-registrar): y_SZ adimensional => P ∝ y/l ∝ D^-1; S_X => n_e ∝ D^-1/2; M_HSE ∝ r^2 (dP/dr)/n_e ∝ D^{1/2}. Menor |n| entre todos os metodos publicados para Coma; M/R ∝ D^-1/2 quebra a degenerescencia com a lei M = K*R (ancoras n=1 sao exatamente degeneradas). Validade condicional: n = 0.5 apenas onde T = P_SZ/n_X; se o nucleo usar T espectroscopica XMM, ali n -> 1 — verificar secao a secao antes do uso. Amplificacao de erro na inversao para D: dD/D = (dM/M)/(1-n) = 2x.",
  "excluded_alternatives": {
    "Kubo2007": "vies +3x por LSS nao modelada (per Okabe+2014)",
    "Falco2014": "H0 entra na propria equacao do sinal — motor proibido",
    "PSZ2": "pipeline inadequado para objeto extenso (flag do proprio Planck) + calibracao Y-M nao separavel",
    "FP_DESI": "zero-point calibrado em Coma — circular",
    "Ho2022": "caixa-preta ML, expoente nao verificavel"
  },
  "approved_for_primary_blind_test": false,
  "approval_pending": "OPERADOR"
}
```

---

## 4. NOTA — autoconsistência (ponto fixo em D): modo terciário legítimo ou vazamento?

A equação `D = M(D)/(2 β² K tanθ)` com `M(D) = M₀·(D/D₀)^n` tem solução fechada:

**D* = D₀ · [M₀/(2 β² K tanθ · D₀)]^{1/(1−n)}**

- **n = 1:** não há ponto fixo — D cancela identicamente; a equação vira ou identidade ou contradição sobre K. Confirma que âncoras n=1 são estruturalmente inúteis para D.
- **n = 0,5 (MW20):** ponto fixo único, e a iteração é contração (|n|<1 ⟹ converge de qualquer chute inicial). Matematicamente bem-posto.

**Parecer: legítimo como MODO TERCIÁRIO DECLARADO, sob quatro condições duras; vazamento se qualquer uma faltar:**

1. **n pré-registrado com derivação analítica** (não ajustado a posteriori) — senão n vira parâmetro livre que absorve o desvio, e o "ponto fixo" é curve-fitting disfarçado.
2. **Declarar que M₀ carrega o resíduo não-potência:** a cosmologia assumida entra também por vias que NÃO são lei de potência em D (abertura r500 herdada, E(z), prior c-M no caso WL). O ponto fixo só remove a dependência em lei de potência; o resto é vazamento residual a quantificar.
3. **Declarar a amplificação de erro:** dD/D = (dM/M)/(1−n). Para n=0,5, fator 2 (erro de massa de ~8% estat + 15% sys ⟹ ~35% em D). Para n→1 a amplificação diverge — mais uma face da degenerescência.
4. **Rotular o resultado como AUTOCONSISTÊNCIA, nunca como confirmação independente:** o ponto fixo responde "existe um D em que âncora e lei coexistem?", não "a lei prevê o D correto". É teste de coerência interna (pode FALSIFICAR se D* sair absurdo — ex.: incompatível com z_Coma por fator grande — mas não confirma).

Em síntese: o modo terciário é o análogo honesto do método de distância X+SZ de Birkinshaw — usa a diferença de expoentes para extrair D. É ciência legítima **porque declara a dependência em vez de escondê-la**; vira vazamento no instante em que for apresentado como teste primário independente. A hierarquia proposta ao OPERADOR: **primário = NOT_IDENTIFIABLE (resultado); secundário = MW20 com n=0,5 declarado; terciário = ponto fixo como autoconsistência falsificadora.** Aprovação de todos os três é decisão do OPERADOR.