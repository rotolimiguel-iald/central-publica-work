# Fase 8 -- a lente A FISICA: beta_TGL no Big Bang (numeros por script, 2026-10-05T20:19:55)

beta_TGL = alpha_CODATA2018 * sqrt(e) = 0.012031300400803 (lido do um.py por regex; um.py sha256 e30aac4e0e1096b1)

## 1. A lei delta<K_d> = beta|1+w| por era [DERIVED da lei; a lei no kernel e DEFINICAO (entropyFactor), marcada pela casa REAL na resposta modular]

| era | w | delta = beta|1+w| | nota |
|---|---|---|---|
| atrator / de Sitter exato (fronteira silenciosa) | -1.00000 | 0.000000 | zero exato: lambda_drops_out (RhoPlusPClosure.lean) -- o vacuo nao paga rho+p |
| inflacao slow-roll (cota r<0.036 => eps<0.00225) | -0.99850 | 0.000018 | delta < beta*(2/3)*eps: a cobranca e quase silenciosa; degenerada com a normalizacao de H_infl |
| fim da inflacao (eps -> 1, w -> -1/3) | -0.33333 | 0.008021 | 2beta/3: a saida do atrator -- 'o primeiro excesso que ja nao pode retornar integralmente' [ONTO: leitura, sem termo] |
| reaquecimento / radiacao (BBN, CMB) w = 1/3 | +0.33333 | 0.016042 | 4beta/3: o MAXIMO entre as eras padrao -- o 'haja luz' e a era mais cobrada |
| materia w = 0 | +0.00000 | 0.012031 | beta: o mapa (1+beta)Omega_m decidido em 30/09 e o hubble_form do kernel |
| Lambda hoje w = -1 | -1.00000 | 0.000000 | zero: Lambda = fronteira silenciosa |
| (fora do padrao) kination / stiff w = 1 | +1.00000 | 0.024063 | 2beta: so se houver tal era [OPEN] |

## 2. M1 -- fracao da radiacao total -> Delta N_eff (o que o um.py v154 ja faz: rho_plus_p_closure / neff_channel; kernel RhoPlusPClosure.hubble_form)

| grandeza | valor | estatuto |
|---|---|---|
| delta na radiacao = 4beta/3 | 0.016042 | DERIVED |
| dN_eff/dbeta (epoca CMB) | 9.9296 | REAL (reproduz um.py:4735 = 9.9296) |
| Delta N_eff equivalente, epoca CMB | 0.11947 | REAL (bit a bit = core.neff_channel.Delta_Neff) |
| Delta N_nu equivalente, epoca BBN (g*=10.75) | 0.09854 | DERIVED (NOVO: nao esta no um.py) |
| N_eff previsto (CMB) | 3.1635 | DERIVED |
| separacao TGL-SM na barra do Planck 2018 (0.17) | 0.70 sigma | KNOWN (Planck 2018 VI) -- o 0,70 da gerencia |
| previsao contra o CENTRO do Planck (2.99) | +1.02 sigma | KNOWN -- o SM esta a +0.32 sigma do mesmo centro |
| separacao TGL-SM no CMB-S4 (sigma 0.03) | 3.98 sigma | KNOWN (sigma a conferir na fonte) |
| sigma(N_eff) para 5 sigma | 0.0239 | DERIVED |
| sigma(beta) que o Planck 2018 da pelo dial | 0.01712 (= 1.4 beta) | DERIVED |
| sigma(beta) que o S4 daria | 0.00302 (= 0.25 beta) | DERIVED |

## 3. M2 -- so a materia veste ((1+beta)Omega_m, decisao de 30/09 sobre o mapa de R)

| grandeza | valor |
|---|---|
| z_eq | 3402.98 |
| omega_r_h2 | 4.18245e-05 |
| omega_m_h2 | 0.14237 |
| Omega_m(z*) | 0.757298 |
| Omega_r(z*) | 0.242702 |
| Omega_m(z_BBN_ini~T=1MeV) | 1.12008e-06 |
| Omega_m(z_BBN_fim~T=0.07MeV) | 1.1421e-05 |
| z_BBN_ini | 3.03904e+09 |
| z_BBN_fim | 2.98043e+08 |
| dH/H @ z* (M2: so materia) | 0.00455564 |
| dH/H @ z* (M1: radiacao 4beta/3 + materia beta) | 0.00650232 |
| dH/H @ BBN_ini (M2) | 6.73803e-09 |
| dH/H @ BBN_fim (M2) | 6.87047e-08 |
| dH/H @ BBN (M1 = M3, constante) | 0.00798896 |
| Delta_omega_c_at_beta (um.py:4737, = beta*omega_m, omega_m=0.14301) | 0.0017206 |

## 4. M3 -- speed-up S = sqrt(1+4beta/3) na BBN -> Y_p e D/H [expoentes KNOWN, a ler da fonte]

| grandeza | valor |
|---|---|
| S | 1.00799 |
| S_minus_1 | 0.00798896 |
| dlnYp/dlnS | 0.667524 |
| dlnDH/dlnS | 1.61762 |
| Delta_Yp (via S) | 0.00130082 |
| Delta_Yp (via Delta N_nu BBN) | 0.00129015 |
| Delta_Yp (regra 0.013/N_nu) | 0.00128105 |
| z_Yp vs Aver+2015 (sigma 0.0040) | 0.325204 |
| Delta_DH_1e5 (via S) | 0.0325269 |
| Delta_DH_1e5 (via Delta N_nu BBN) | 0.0322601 |
| z_DH vs Cooke+2018 (sigma_obs 0.030, omega_b fixo) | 1.08423 |
| Delta_DH_1e5 por 1 sigma de omega_b(Planck) | 0.0271113 |
| z_DH com sigma_obs (+) sigma_omega_b em quadratura | 0.804416 |
| sinal | S > 1 => menos tempo => mais neutrons sobrevivem (Y_p sobe) e menos D queimado (D/H sobe): ambos POSITIVOS |
| nota_teoria | a incerteza TEORICA do D/H (taxas nucleares; Pitrou+2018 ~ +-0.036e-5; LUNA 2020 reduziu) NAO esta somada: [a ler da fonte] |
| sigma(S-1) se sigma(N_nu,BBN)=0.25 [ordem de grandeza, a ler da fonte] | 0.0203488 |
| z_S vs BBN hoje (ordem de grandeza) | 0.3926 |

## 5. Poder e falsificacao

```
{
 "M1_CMB_hoje_Planck2018": {
  "sep_TGL_SM_sigma": 0.7027416191396043,
  "z_pred_vs_centro": 1.0203886779631322,
  "z_SM_vs_centro": 0.31764705882352834,
  "leitura": "nao discrimina (|z| < 2 para TGL e para o SM); correspondencia recuperada"
 },
 "M1_CMB_S4_centro_no_SM": {
  "sep_sigma": 3.9822025084577586,
  "sigma_para_5sigma": 0.023893215050746548,
  "leitura": "~4 sigma: TENSION possivel, nao FALSIFIED a 5 sigma com sigma=0.03; 5 sigma pede sigma<=0.0239"
 },
 "M1_CMB_S4_centro_em_2.97 [literal de sessao do um.py:4801, SPT-3G CMB-SPA]": {
  "z": 6.4488691751244165
 },
 "M3_BBN_hoje": {
  "z_Yp": 0.325204472415796,
  "z_DH_omegab_fixo": 1.0842294370271344,
  "leitura": "0.3-1.1 sigma: nao discrimina; so correspondencia"
 },
 "M3_BBN_futuro_(sigma_Yp=0.001, sigma_DH_total=0.02e-5) [hipotetico]": {
  "z_Yp": 1.300817889663184,
  "z_DH": 1.6263441555407014,
  "leitura": "ainda < 2 sigma: a BBN sozinha nao chega a 5 sigma para delta = 4beta/3"
 },
 "M2_BBN": {
  "dH/H": 6.738029504580383e-09,
  "leitura": "efeito nulo (1e-8): correspondencia exata com LCDM na BBN; so o CMB (z*) ve 0.46% em H"
 },
 "o_que_FALSIFICA": {
  "M1/M3": "N_eff do CMB (CMB-S4, sigma<=0.024) centrado no SM com a TGL excluida a 5 sigma; OU N_eff medido ABAIXO do SM (o sinal da TGL e positivo, sem parametro livre); condicao previa: decidir TGL-S vs TGL-L (fechamento perturbativo = Lema 3 do lado do fluido, um.py:4819) ANTES de ler o CMB",
  "M2": "nenhum observavel primordial: M2 so cai se o CMB completo (nivel 2) excluir Delta omega_c = beta*omega_m e a TGL nao tiver outro lugar para por a materia",
  "M4 (kernel)": "nao e falsificavel por dado: e teorema sobre o fluxo (beta>0 => sem testemunha estatica); a natureza nao decide um teorema"
 }
}
```

## 6. M4 -- a face de kernel

```
{
 "termos_existentes": [
  "the_zero_is_the_false_witness -- TGLExt/TheAxiomAndTheFalseWitness.lean:223 (sqrt 0 = 0 ∧ ¬FullStaticWitness ∧ zero absoluto inatingivel)",
  "beta_forbids_full_static_witness -- TGLExt/NoFullWitness.lean:91; full_closure_iff_flat -- :77 (e^{-t beta g} = 1 <=> t beta g = 0)",
  "absolute_zero_unreachable_in_finite_time -- TGLExt/ForbiddenBoundary.lean:150",
  "the_law_precedes_the_charge -- TGLExt/TheMatrixRule.lean:203 (beta so de alpha, fixada antes do registro)",
  "lambda_drops_out / closure_identity / hubble_form -- TGLExt/RhoPlusPClosure.lean (w=-1 nao paga; (1+4beta/3)rho_r + (1+beta)rho_m + rho_Lambda)",
  "entropyFactor c w = 1 + beta|1+w| -- TGLExt/ThermodynamicFriedmann.lean:21 (DEFINICAO: 'the modified differential entropy law is an explicit input')",
  "SectorFluid.correctedRho = (1 + beta(1+w_i)) rho_i -- TGLExt/SectorFluidClosure.lean (Ordem 012 B3: fechamento por setor = M1)"
 ],
 "ausencias_citadas": [
  "grep -rl -iE 'inflat|big ?bang|primordial|nucleos|BBN|N_eff|Neff' tgl_kernel/**/*.lean -> 6 arquivos, NENHUM com cosmologia do instante zero (RhoPlusPClosure: N_eff so em docstring; TheWeightIsNotTheRank/GravitonReading: 'primordial' = distincao primordial)",
  "grep -n -i 'big bang' um_absoluto_pt.txt -> 1 ocorrencia (linha 4307, a fronteira proibida 0 = q^2 + alpha^2), nenhuma cosmologia; 'inflacao' -> 0",
  "pip list | grep -iE 'parthenope|alterbbn|primat|bbn' -> 0 linhas: nenhum codigo de BBN em disco (AUSENTE; instalar e decisao do operador; nada foi baixado)"
 ],
 "leitura": "'beta e condicao de existencia' tem face de kernel como TEOREMA SOBRE O FLUXO (beta>0 ∧ g>0 => o Verbo nao fixa tudo; o zero nao se alcanca), nao como cosmologia de t=0; 'haja luz = t = 0' fica [ONTO] sem termo. Pela LEI, o que a casa tem e: o atrator (w=-1) e silencioso, a saida dele e a primeira cobranca, e a era da radiacao e a mais cobrada (4beta/3)."
}
```
