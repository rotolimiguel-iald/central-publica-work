# KIMI E0-01 — Inventário e derivação independente da unidade da nota fundamental

**Data:** 31/10/2026  
**Estatuto geral:** **[DECLARADO pelo Kimi]**, até conferência da gerência na fonte e por código próprio.  
**Escopo:** derivação sem dados de oscilação, sem ajuste, sem download de dados de neutrino e sem escolher lei pela proximidade de 1 eV.

## Resumo — 12 linhas

1. **Resultado:** `U_E_NOT_DERIVED`.
2. As escalas físicas fechadas encontradas são \(m_ec^2\), Hartree \(E_h=\alpha^2m_ec^2\) e Rydberg \(E_h/2\), não a unidade da nota fundamental.
3. A energia de Coulomb em \(a_0\) reproduz Hartree; no raio clássico do elétron reproduz \(m_ec^2\).
4. As regiões \(27.2114\,a_0\) e \(1.43996\,\mathrm{nm}\), e a temperatura de Unruh fornecida, foram classificadas como **escolhidas pelo alvo**.
5. A conversão \(U_E=1\,\mathrm{eV}\) é metrologicamente legítima, mas não deriva a escala física.
6. O volume \(\sqrt e\) é adimensional; \(E_{\rm pent}=\sqrt e\,U_E\) só fecha algebricamente depois que \(U_E\) é posto.
7. A leitura modular do vácuo tem energia zero no relógio de Killing; a tônica precisa ser gap, excitação ou normalização independente.
8. Fluxo e monopolo fornecem identidades, não a carga: falta \(\mathcal F\), \(q\), \(\tau^\star\) ou \(R_{\rm mod}(x)\) com procedência independente.
9. Unruh fornece \(U=\hbar\kappa/(2\pi)\), mas não seleciona \(\kappa\).
10. Quatro identidades algébricas foram compiladas em Lean com código `0`, no trio e sem `sorryAx`.
11. A regra do posto permanece: dado \(U\), \(m_2=U\alpha e^{1/2}\sen45^\circ\); nenhum dado foi usado nesta análise.
12. A parede medida é uma única entrada dimensional independente: gap, região, \(\kappa\), \(\tau^\star\) ou carga, com unidade e sem ajuste.

## A. Inventário das leis candidatas

As entradas usadas são CODATA 2018 e SI 2019, sem qualquer determinação de oscilação. A fórmula \(m_2=U\alpha e^{1/2}\sen45^\circ\) é apenas transporte algébrico, não comparação com experimento. Valores podem diferir nos últimos dígitos por arredondamento independente das constantes; os valores tabulados permanecem preferidos quando disponíveis.

| Lei e fórmula | Entradas e procedência | Número em eV e transporte para m₂ | Estatuto | Escolhida pelo alvo? | O que falta para ser lei |
|---|---|---|---|---|---|
| **Repouso do elétron:** \(U=m_ec^2\) | \(m_e,c\), CODATA | \(U=510998.95000\); \(m_2=4.3472797\times10^6\) meV | `[KNOWN]` | Não | Escala de repouso, não nota da fronteira. |
| **Hartree:** \(U=\alpha^2m_ec^2=m_ee^4/[(4\pi\varepsilon_0)^2\hbar^2]\) | \(e,\hbar,c,\varepsilon_0,m_e\) | \(U=27.211386245988\); \(m_2=231.4985\) meV | `[DERIVED]` | Não | Unidade atômica fechada, não unidade da nota. |
| **Rydberg:** \(U=hcR_\infty=\tfrac12\alpha^2m_ec^2=E_h/2\) | Rydberg CODATA e relação com Hartree | \(U=13.605693122994\); \(m_2=115.7493\) meV | `[DERIVED]` | Não | É metade do Hartree; nenhuma ponte à nota. |
| **Dirac 1s:** \(U=m_ec^2(1-\sqrt{1-\alpha^2})\) | Hamiltoniano de Dirac, núcleo pontual/massa infinita | \(U=13.6058742583\); \(m_2=115.7508\) meV | `[DERIVED]` | Não | Modelo específico; recuo e QED ficam fora. |
| **Coulomb no raio de Bohr:** \(U=\alpha\hbar c/a_0\), \(a_0=\hbar/(\alpha m_ec)\) | \(e,\hbar,c,m_e\) | \(U=27.2113862\); \(m_2=231.4985\) meV | `[DERIVED]` | Não | Repete Hartree; não nova unidade. |
| **Coulomb no raio clássico do elétron:** \(U=\alpha\hbar c/r_e\), \(r_e=e^2/(4\pi\varepsilon_0m_ec^2)\) | \(e,\hbar,c,\varepsilon_0,m_e\) | \(U=510998.95000\); \(m_2=4.3472797\times10^6\) meV | `[DERIVED]` | Não | Identidade circular para nova escala. |
| **Potência isolada:** \(U=\alpha^3m_ec^2\) | α e repouso do elétron | \(U=0.1985710793\); \(m_2=1.6893264\) meV | `[OPEN]` | Expoente não derivado | Falta lei selecionando \(n=3\). |
| **Potência isolada:** \(U=\alpha^4m_ec^2\) | α e repouso do elétron | \(U=0.0014490432\); \(m_2=0.0123276\) meV | `[OPEN]` | Expoente não derivado | Falta lei selecionando \(n=4\). |
| **Coulomb na região:** \(U=\alpha\hbar c/(27.2114a_0)\) | \(r_0=27.2114a_0\) | \(U\simeq0.9999995\); \(m_2\simeq8.50741\) meV | `DESCARTADA` | **Sim** | \(27.2114\) reproduz Hartree em eV; região escolhida pela normalização. |
| **Coulomb na região:** \(U=\alpha\hbar c/r_0\), \(r_0=1.43996\) nm | Raio fornecido | \(U\simeq1.0000032\); \(m_2\simeq8.50744\) meV | `DESCARTADA` | **Sim** | \(r_0=\alpha\hbar c/U_E\); falta região independente. |
| **Térmica:** \(U=k_BT_U\), \(T_U=11604.5181\) K | \(k_B\), temperatura fornecida | \(U\simeq0.9999999981\); \(m_2\simeq8.5074141\) meV | `DESCARTADA` | **Sim** | \(T_U=U_E/k_B\); falta temperatura independente. |
| **CMB:** \(U=k_BT_{\rm CMB}\), \(T=2.72548\) K | Temperatura observacional externa | \(U=2.3486369\times10^{-4}\); \(m_2=0.0019981\) meV | `[OPEN]` | Não | Falta lei identificando CMB ao banho da fronteira. |
| **Landauer/CMB:** \(U=k_BT_{\rm CMB}\ln2\) | Temperatura e processo de apagamento | \(U=1.6279511\times10^{-4}\); \(m_2=0.0013850\) meV | `[OPEN]` | Não | Exige protocolo, reservatório e ΔS; não volume→energia. |
| **Ramo nativo planckiano:** \(U=E_P/(4\pi)\) | \(t_P,\hbar,c,G\) | \(U\simeq9.71553\times10^{26}\); \(m_2\simeq8.2654\times10^{27}\) meV | `[OPEN]/CONDICIONAL` | Não, mas não responde | Não é 1 eV; não pode ser usado como atalho. |
| **Fluxo:** \(U=c^4\mathcal F/(4\pi G)\) | \(R_{\rm mod},B_\partial,\partial_nu\) | Não calculável sem fluxo | `[DERIVED condicional]` | Não | Falta fluxo com unidade e independência. |
| **Monopolo:** \(U=c^5\tau^\star/(4\pi G)\) | \(\tau^\star\) | Nativo: acima; alvo: abaixo | `[DERIVED condicional]` | Depende de τ★ | Falta escala temporal independente. |
| **Unruh:** \(U=\hbar\kappa/(2\pi)\) | κ do horizonte | Não calculável sem κ | `[KNOWN]/[OPEN]` | Não | Falta κ ou aceleração independente. |
| **Coulomb genérico:** \(U=\alpha\hbar c/r_0\) | \(e,\hbar,c\), região \(r_0\) | Não calculável sem região | `[OPEN]` | Depende da região | Falta \(B_\partial=r_0\) independente. |

### Leis que não foram escolhidas pelo alvo

Hartree, Rydberg, Dirac e as identidades de Coulomb são leis físicas reais. Elas foram incluídas justamente porque **não** fornecem a unidade pedida. A expressão Rydberg/27.2114 vale cerca de **0,5 eV**, não 1 eV; a expressão Hartree/27.2114 é aproximadamente 1 eV porque o denominador é o próprio Hartree expresso em eV. Essa distinção evita a falsa derivação por numerologia.

## B. Derivação — parede medida

### B1. O que as constantes realmente determinam

As constantes \(e,\hbar,c,\varepsilon_0,m_e\) fornecem

\[
m_ec^2,
\qquad
\alpha=\frac{e^2}{4\pi\varepsilon_0\hbar c},
\qquad
E_h=\alpha^2m_ec^2,
\qquad
\mathrm{Ry}=E_h/2 .
\]

Toda nova energia fechada por essa via tem a forma \(C(\alpha)m_ec^2\), com \(C(\alpha)\) fixado por uma lei física. Nenhuma das estruturas examinadas — inscrição \((q,\alpha)\), meio-tom, volume, PsiBit, pentada ou fluxo — fornece independentemente \(C(\alpha)\). A simples conversão \(1\,\mathrm{eV}=1.602176634\times10^{-19}\,\mathrm J\) não seleciona \(C(\alpha)\).

### B2. O que cada rota exige ainda

- **Fluxo:** \(U=c^4\mathcal F/(4\pi G)\). É necessário fornecer \(\mathcal F=-\oint\partial_n\log(R_{\rm mod}/\theta_M)\,dA\), com região e campo local independentes.
- **Monopolo:** \(U=c^5\tau^\star/(4\pi G)\). É necessário derivar \(\tau^\star\) sem usar \(U\). O horizonte da própria energia é tautológico quanto à escala.
- **Unruh:** \(U=\hbar\kappa/(2\pi)\). É necessário derivar \(\kappa\), ou a aceleração, sem usar \(U\).
- **Coulomb:** \(U=\alpha\hbar c/r_0\). É necessário derivar \(r_0\), sem usar \(U\).
- **Hamiltoniano:** é necessário um gap com unidade, regulador, região, condições de contorno e prescrição de vácuo. A energia modular do vácuo é zero; portanto, a tônica não pode ser simplesmente a energia fundamental.

### B3. Veredito da derivação

**`U_E_NOT_DERIVED`.** A parede não é aritmética nem falta de candidatos. É uma única entrada dimensional independente, com unidade e procedência: **gap, região, \(\kappa\), \(\tau^\star\), carga ou fluxo**, acompanhada da prova de que \(E_{\rm fluxo}=E_0\) e de que a tônica pertence ao mesmo sistema. Atribuir qualquer uma delas pela proximidade de 1 eV seria ajuste, não derivação.

## C. Lean — identidades verificadas

Arquivo: [E0ScaleAudit.lean](lean/TGLExt/E0ScaleAudit.lean)

Compilação: `lake env lean`, **código de saída `0`**. `#print axioms` mostra apenas `propext`, `Classical.choice` e `Quot.sound`; sem `sorryAx`.

Foram provadas quatro identidades, nenhuma derivando 1 eV:

1. `hartree_eq_two_mul_rydberg`: \(E_h=2\mathrm{Ry}\);
2. `coulomb_at_a0_eq_alpha_sq_mec2`: energia Coulombiana em \(a_0=\alpha^2m_ec^2\);
3. `semitone_exp_roundtrip`: \(e^{-1/2}(e^{1/2}U)=U\);
4. `monopole_time_eq_two_pi_rs_div_c`: \(\tau=2\pi r_s/c\), condicionada a \(r_s=2q\) e \(q=c\tau/(4\pi)\).

A auditoria numérica e o inventário estão em [inventario_unidades_e0.py](inventario_unidades_e0.py) e [inventario_unidades_e0.json](inventario_unidades_e0.json).

## D. Regra do posto

Dada qualquer unidade \(U\) derivada independentemente, a transformação é

\[
\boxed{m_2=U\,\alpha\,e^{1/2}\sen45^\circ} .
\]

Com \(U=1\,\mathrm{eV}\), a fórmula devolve \(m_2=8.5074140999\) meV, sem que isso constitua comparação ou avaliação experimental nesta entrega. O teste do neutrino decidiria apenas sobre uma unidade previamente congelada por lei e hash; não decidiria sobre uma unidade escolhida pelo resultado. `U_E_NOT_DERIVED` é o estado desta derivação. Se, depois de congelada por lei e hash, uma unidade candidata for negada pelo experimento, o resultado **falsifica essa unidade ou sua identificação com E₀**, não necessariamente a forma geral da TGL.

## E. Fontes, acesso e hashes

### Fontes externas — acesso em 31/10/2026

- NIST/CODATA 2018, ajuste completo: https://physics.nist.gov/cuu/Constants/ArchiveASCII/allascii_2018.txt
- CODATA 2018, artigo: https://doi.org/10.1103/RevModPhys.93.025010
- NIST, elétron-volt em joules: https://physics.nist.gov/cgi-bin/cuu/Value?evj
- NIST, constante de Boltzmann: https://physics.nist.gov/cgi-bin/cuu/Value?k
- NIST, constante de Planck reduzida: https://physics.nist.gov/cgi-bin/cuu/Value?hbar
- NIST, constante de Planck em eV/Hz: https://physics.nist.gov/cgi-bin/cuu/Value?hev
- Unruh 1976: https://the-center-of-gravity.com/documents/33/Unruh_Notes-on-Black-Hole-evaporation.pdf
- Landauer 1961: https://www.pitt.edu/~jdnorton/lectures/Rotman_Summer_School_2013/thermo_computing_docs/Landauer_1961.pdf
- Fixsen 2009, temperatura CMB: https://arxiv.org/abs/0911.1955

### Fontes locais principais

- `ORDEM_KIMI_E0_01_31out.md`;
- `CONFERENCIA_E0_KIMI_E_CADEIA_31out.md`;
- `LeiDoMeioTom.lean`;
- `E0LiberdadeDeEscala.lean`;
- `PROVA_TONICA_SQRT_E_31out.md`;
- `PROVA_CONDENSACAO_E0_31out.md`;
- `PROVA_FLUXO_VOLUMETRICO_E0_31out.md`;
- `PROVA_CARGA_MONOPOLO_NATIVA_31out.md`;
- `HANDOFF_CLAUDE_E0_M2_31out.md`;
- `boundary_flux_mass_theorem.py`;
- `tgl_modular_clock_source.py`;
- `ga_rb_causal_dissipation_form.py`;
- `ga_gamma_blind_dissipation_rate.py`;
- `TriadMaster.lean`.

**Manifesto SHA-256 completo das fontes locais lidas e dos artefatos devolvidos:** [MANIFESTO_SHA256_E0_01.json](MANIFESTO_SHA256_E0_01.json)

O manifesto é gerado por script, nunca de memória, e inclui este relatório, o inventário, os programas e os módulos Lean.
