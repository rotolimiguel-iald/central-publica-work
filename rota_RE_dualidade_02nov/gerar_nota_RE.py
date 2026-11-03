# -*- coding: utf-8 -*-
"""Gera a nota da derivacao da R-E e as contas de Landauer (gerencia c1, 02/11/2026). Hashes lidos dos arquivos; numeros lidos de CONTAS_RE.json ou calculados aqui."""
import hashlib, json, math
from pathlib import Path

AQUI = Path(__file__).resolve().parent
K = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
C = json.loads((AQUI / "CONTAS_RE.json").read_text(encoding="utf-8"))
ORD = Path("C:/IALD/Central de Patentes/work/cunhagens_13out/OPERADOR_02nov_qubit_mqc_e_derivar_re_verbatim.txt")

ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
kB_J, e_C = 1.380649e-23, 1.602176634e-19
piso_J = beta * e_C
Tstar = piso_J / (kB_J * math.log(2))
erg_meV = 1e-7 / e_C * 1e3
W, sW = 1.1828e-16 * erg_meV, 0.3322e-16 * erg_meV
z_piso = (beta * 1e3 - W) / sW
razao_gap = math.log(2) / beta
L = {"beta": beta, "piso_literal_meV": beta * 1e3, "T_estrela_K": Tstar, "Gaudenzi_W_meV": W, "Gaudenzi_sigma_meV": sW, "Gaudenzi_T_K": 1.0, "sigmas_abaixo_do_piso": z_piso,
     "gap_sobre_kT_para_o_piso_superar_Landauer": razao_gap, "fonte": "Gaudenzi et al., Nature Physics 14, 565 (2018), arXiv:1703.04607, lido em ar5iv pela gerencia"}
(AQUI / "CONTAS_LANDAUER.json").write_text(json.dumps(L, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(L, ensure_ascii=False)[:420])

t = f"""# Rota R-E: como K age na luminosidade e no ângulo (02/11/2026)

**Ordem do operador:** `work\\cunhagens_13out\\{ORD.name}` (sha16 `{sha(ORD)}`).
**Autoria e estatuto:** derivação da gerência c1, à mão, sem pedra de kernel. Contas em `CONTAS_RE.json` (sha16 `{sha(AQUI / "CONTAS_RE.json")}`). Os H₀ publicados são `[DECLARADO]` (memória da Fase 9). Nada aqui altera K, a Fase 9, o rito ou o gate.

## Resultado

**K não age na luminosidade nem no ângulo.** f_L = f_A, logo η = 1: é a Alternativa A da nota F2. A Alternativa B («K só na luminosidade», η = 1/K* ou Q/K*) fica recusada. K separa outra coisa: os leitores que usam a régua primordial (CMB, BAO+BBN, as «faces» da Fase 9) dos que não usam (escada, masers, lentes, sirenes).

Custo do resultado: **R-E não discrimina**, porque o rival também dá η = 1. E **K fica sem portador físico derivado**: das seis moradas examinadas, cinco caem e uma segue aberta, sem mecanismo (seção 4).

## 1. O que Etherington exige [KNOWN]

d_L = (1+z)²·d_A vale se a luz segue geodésicas nulas de uma métrica e o número de fótons no feixe se conserva. A nota F2 escreveu η = f_L/f_A e parou aí: «K sozinho não decide f_A nem o transporte de fótons».

## 2. O que o kernel decide

- **A família do vazamento é defasagem.** `TheFlowLawD1a` (sha16 `{sha(K / "TheFlowLawD1a.lean")}`) usa o `leakVerb` de `NoFullWitness` (sha16 `{sha(K / "NoFullWitness.lean")}`), cuja face GKLS é «o semigrupo de defasagem». No `um.py`, o Verbo é L = √β·√K, um salto hermitiano, com Γ_ij = ½β(√k_i − √k_j)².
- **Defasagem não toca o total.** `dephase_preserves_trace`, `the_trace_is_not_erasable` (`TheTraceIsNotErasable.lean`, sha16 `{sha(K / "TheTraceIsNotErasable.lean")}`): `tr(T_t x) = tr(x)`, na diagonal `e^0 = 1`. Pedra de dimensão finita.
- **Hipótese nomeada H1:** a luz sofre esse vazamento na base de K, e K comuta com o momento do fóton. Razão `[KNOWN]`: a simetria de um estado comuta com o seu fluxo modular (Tomita–Takesaki), e o fundo FRW é homogêneo e isotrópico. Um salto único hermitiano simétrico comuta com as isometrias. Se K não agir na luz, a conclusão é a mesma.

**Sob H1 [DERIVED]:** populações em momento não mudam, logo número, energia e direção do fóton se conservam. A premissa de Etherington deixa de ser hipótese externa e vem de ω(I) = 1. Portanto:

- η(z) = 1 para toda z;
- T(z) = T₀(1+z), γ_T = 0 (fecha a R-F na alternativa A);
- μ = 0 na janela do FIRAS;
- registro = expansão para o fóton: 1+z = a₀/a.

Consequência que pede leitura do operador: a frase da pedra, «o fundo atribui o registro inteiro à expansão», não pode significar que parte do desvio do fóton não é expansão.

## 3. Conferência sem H1: o transporte não alcança K [REAL, conta]

Mesmo com o vazamento agindo com força total na luz, a escada só atravessa z ≤ 0,15.

| z | k(z) − 1 | fração do que K pede |
|---|---|---|
| 0,05 | 0,0187% | 1/449 |
| 0,15 | 0,0587% | 1/{C["fator_que_falta_escada"]:.0f} |

Com contraste 1, o teto é {100 * C["custo_maximo_escada_g_le_1"]:.3f}%. K pede 8,38%. E a base da escada é angular (paralaxe, eclipsantes, maser): não há luminosidade a corrigir entre a âncora e o fluxo de Hubble que carregue N* = 7 nats. **A Alternativa B não tem mecanismo.**

Teste nos leitores que não são luminosidade (`[DECLARADO]`, valores da Fase 9, não lidos por hash):

| leitor | H₀ | K comum | só luminosidade |
|---|---|---|---|
| masers (ângulo) | 73,9 ± 3,0 | −0,12σ | +1,79σ |
| TDCOSMO (tempo) | 71,6 ± 3,6 | −0,74σ | +0,85σ |
| sirenes (amplitude GW) | 76,6 ± 11,2 | +0,21σ | +0,72σ |

Δχ² = {C["delta_chi2_K_comum_contra_so_luminosidade"]:.2f} a favor de K comum, cerca de {C["sigma_equiv"]:.1f}σ. Isso também legitima o que a Fase 9 já fazia: masers e TDCOSMO no composto eram uma escolha não justificada (aviso da R-G na nota F2).

## 4. A parede: onde K poderia morar [REAL, conta]

| onde K poderia morar | o que exige | medida | estado |
|---|---|---|---|
| transporte da escada | 8,38% em z ≤ 0,15 | 0,059% | 143× pequeno |
| energia do fóton, número conservado | corpo cinza K³ = {C["fator_de_diluicao_corpo_cinza"]:.3f} | FIRAS < 1e-4 | vetado |
| luz muda de face, perdendo energia e número e preservando Planck (1+z = k·a₀/a) | sair de H1; {100 * (1 - C["K_fase9"]**-4):.1f}% da energia do CMB deixam a face visível depois de z* | nenhum veto nas contas acima; aqui também η = 1 | **única porta aberta, sem mecanismo** |
| lei como métrica, H(z) = A(z)·H_fundo, régua parada | θ* sobe 6,3% | ~{C["sigmas_theta"]:.0f}σ | vetado |
| H primordial | ΔN_eff de {C["dNeff_BBN_se_H_primordial"]:.2f} a {C["dNeff_CMB_se_H_primordial"]:.2f} | limite 0,107 | vetado por 10× |
| régua pelo fechamento ρ+p | r_d −7,73% | entrega {100 * C["regua_fechamento"]:.2f}% | 11× pequeno |

**A porta aberta:** `annihilation_is_relocation_not_deletion` diz que o aniquilado muda de face e não some, logo o traço total não a recusa; só H1 a recusa. É a leitura literal da frase da pedra. Falta o mecanismo: o reflexo muda o número de fótons, mas preservar Planck exige baixar também a energia de cada fóton. Decidir entre H1 e esta porta é leitura do operador.

**O que isto não diz:** não mexe no número K nem no z_disc 4,44 da Fase 9. Diz que K é hoje lei de leitura com `H0local` por definição, sem mecanismo derivado. Parede medida, não falsificação: a tensão de Hubble é um problema aberto também para o rival.

## 5. O que muda nas rotas

- **R-E:** fechada como teste nulo: η = 1 sob H1 e na porta aberta. Como o rival também dá 1, a rota não discrimina; um η ≠ 1 significativo, com calibração marginalizada, contrariaria os dois.
- **R-F:** alternativa A, γ_T = 0.
- **R-G:** alternativa A: lentes leem K·H₀, f_t = f_phi = 1.
- **R-H:** a ponte GW fecha sob H1 para o gráviton: sirenes não usam régua nem escada, e devem ler K·H_fundo = 74,27. Separação do fundo 68,53: 5σ pede σ(H₀) = {C["sigma_sirenes_para_5s"]:.2f} km/s/Mpc; hoje ±11.

## 6. Limites

- Sem pedra de kernel; a pedra da dimensão finita não é o fóton real.
- H1 é hipótese nomeada.
- A forma com sirenes depende de H1 para o gráviton.
- Valores de H₀ não lidos por hash: D-H segue do operador.
"""
(AQUI / "DERIVACAO_RE_02nov.md").write_text(t, encoding="utf-8")
print("nota", len(t.encode("utf-8")), sha(AQUI / "DERIVACAO_RE_02nov.md"))
