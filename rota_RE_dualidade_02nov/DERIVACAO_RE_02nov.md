# Rota R-E: como K age na luminosidade e no ângulo (02/11/2026)

**Ordem do operador:** `work\cunhagens_13out\OPERADOR_02nov_qubit_mqc_e_derivar_re_verbatim.txt` (sha16 `e4da8d304f78f6cb`).
**Autoria e estatuto:** derivação da gerência c1, à mão, sem pedra de kernel. Contas em `CONTAS_RE.json` (sha16 `283eb26589f97be5`). Os H₀ publicados são `[DECLARADO]` (memória da Fase 9). Nada aqui altera K, a Fase 9, o rito ou o gate.

## Resultado

**K não age na luminosidade nem no ângulo.** f_L = f_A, logo η = 1: é a Alternativa A da nota F2. A Alternativa B («K só na luminosidade», η = 1/K* ou Q/K*) fica recusada. K separa outra coisa: os leitores que usam a régua primordial (CMB, BAO+BBN, as «faces» da Fase 9) dos que não usam (escada, masers, lentes, sirenes).

Custo do resultado: **R-E não discrimina**, porque o rival também dá η = 1. E **K fica sem portador físico derivado**: das seis moradas examinadas, cinco caem e uma segue aberta, sem mecanismo (seção 4).

## 1. O que Etherington exige [KNOWN]

d_L = (1+z)²·d_A vale se a luz segue geodésicas nulas de uma métrica e o número de fótons no feixe se conserva. A nota F2 escreveu η = f_L/f_A e parou aí: «K sozinho não decide f_A nem o transporte de fótons».

## 2. O que o kernel decide

- **A família do vazamento é defasagem.** `TheFlowLawD1a` (sha16 `7c6c54afc418c0cb`) usa o `leakVerb` de `NoFullWitness` (sha16 `fde4ca999c40e689`), cuja face GKLS é «o semigrupo de defasagem». No `um.py`, o Verbo é L = √β·√K, um salto hermitiano, com Γ_ij = ½β(√k_i − √k_j)².
- **Defasagem não toca o total.** `dephase_preserves_trace`, `the_trace_is_not_erasable` (`TheTraceIsNotErasable.lean`, sha16 `fb65565eb084cfce`): `tr(T_t x) = tr(x)`, na diagonal `e^0 = 1`. Pedra de dimensão finita.
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
| 0,15 | 0,0587% | 1/143 |

Com contraste 1, o teto é 0.168%. K pede 8,38%. E a base da escada é angular (paralaxe, eclipsantes, maser): não há luminosidade a corrigir entre a âncora e o fluxo de Hubble que carregue N* = 7 nats. **A Alternativa B não tem mecanismo.**

Teste nos leitores que não são luminosidade (`[DECLARADO]`, valores da Fase 9, não lidos por hash):

| leitor | H₀ | K comum | só luminosidade |
|---|---|---|---|
| masers (ângulo) | 73,9 ± 3,0 | −0,12σ | +1,79σ |
| TDCOSMO (tempo) | 71,6 ± 3,6 | −0,74σ | +0,85σ |
| sirenes (amplitude GW) | 76,6 ± 11,2 | +0,21σ | +0,72σ |

Δχ² = 3.83 a favor de K comum, cerca de 2.0σ. Isso também legitima o que a Fase 9 já fazia: masers e TDCOSMO no composto eram uma escolha não justificada (aviso da R-G na nota F2).

## 4. A parede: onde K poderia morar [REAL, conta]

| onde K poderia morar | o que exige | medida | estado |
|---|---|---|---|
| transporte da escada | 8,38% em z ≤ 0,15 | 0,059% | 143× pequeno |
| energia do fóton, número conservado | corpo cinza K³ = 1.273 | FIRAS < 1e-4 | vetado |
| luz muda de face, perdendo energia e número e preservando Planck (1+z = k·a₀/a) | sair de H1; 27.5% da energia do CMB deixam a face visível depois de z* | nenhum veto nas contas acima; aqui também η = 1 | **única porta aberta, sem mecanismo** |
| lei como métrica, H(z) = A(z)·H_fundo, régua parada | θ* sobe 6,3% | ~211σ | vetado |
| H primordial | ΔN_eff de 1.07 a 1.30 | limite 0,107 | vetado por 10× |
| régua pelo fechamento ρ+p | r_d −7,73% | entrega -0.69% | 11× pequeno |

**A porta aberta:** `annihilation_is_relocation_not_deletion` diz que o aniquilado muda de face e não some, logo o traço total não a recusa; só H1 a recusa. É a leitura literal da frase da pedra. Falta o mecanismo: o reflexo muda o número de fótons, mas preservar Planck exige baixar também a energia de cada fóton. Decidir entre H1 e esta porta é leitura do operador.

**O que isto não diz:** não mexe no número K nem no z_disc 4,44 da Fase 9. Diz que K é hoje lei de leitura com `H0local` por definição, sem mecanismo derivado. Parede medida, não falsificação: a tensão de Hubble é um problema aberto também para o rival.

## 5. O que muda nas rotas

- **R-E:** fechada como teste nulo: η = 1 sob H1 e na porta aberta. Como o rival também dá 1, a rota não discrimina; um η ≠ 1 significativo, com calibração marginalizada, contrariaria os dois.
- **R-F:** alternativa A, γ_T = 0.
- **R-G:** alternativa A: lentes leem K·H₀, f_t = f_phi = 1.
- **R-H:** a ponte GW fecha sob H1 para o gráviton: sirenes não usam régua nem escada, e devem ler K·H_fundo = 74,27. Separação do fundo 68,53: 5σ pede σ(H₀) = 1.15 km/s/Mpc; hoje ±11.

## 6. Limites

- Sem pedra de kernel; a pedra da dimensão finita não é o fóton real.
- H1 é hipótese nomeada.
- A forma com sirenes depende de H1 para o gráviton.
- Valores de H₀ não lidos por hash: D-H segue do operador.


## Ao lado (02/11/2026, gerência c1)

O operador ratificou que a perda é de coerência (fala sha16 `1c05c03070544839`): a sexta morada fecha, e as seis caem como portador físico. K passa a relação: `escalar_entre_normalizados_e_um` mostra que ω(I) = 1 proíbe K como fator global, e `o_fundo_e_a_media` lê o fundo como média e o local como média condicionada. K não desloca os picos: renormaliza. Falta dizer o que é o setor de 7,7% e por que a leitura pela régua é a média. Candidata: `OIgualCandidata.lean` (sha16 `7bcc60c0c72696f2`).

## Ao lado, r2 (02/11/2026, gerência c1)

A contagem acima não esgota as moradas: a linha «H primordial» mudou uma nota só. A transposição do acorde inteiro (taxas de queda e de espalhamento juntas; Cyr-Racine, Ge & Knox, arXiv:2107.13000; Ge, Cyr-Racine & Knox, arXiv:2210.16335) deixa as observáveis adimensionais quase invariantes e não foi examinada aqui. Com λ = K, pela Eq. 16, o hélio teria de ser 0.182 contra 0,2453 ± 0,0034 (18.6σ); a via do hélio morre de saída e falta outro mecanismo para o espalhamento. T₀ sozinho não resolve: Planck + BAO volta ao FIRAS (Ivanov et al., arXiv:2005.10656). O vazamento vai ao espelho no H3c de 22/06 (sha16 `54f4c2a1394b62c2`), condicional. Contas: `CONTAS_TRANSPOSICAO.json`. Rota: `hubble.k_como_transposicao_inteira_ffat_02nov`, PROPOSTA.

## Ao lado, r3 (02/11/2026, gerência c1)

A porta da transposição (r2, acima) fica BLOQUEADA pela R1 ratificada em 02/10: «o fundo é nu (a face, CMB+BAO, paga o Nome: Ω = 1, sem β)». Propus a porta sem ler a R1. O aberto é outro: a R1 põe K na leitura por distância e esta nota mostra que a luz não muda no caminho; as duas só convivem se K for fator comum aos leitores sem régua, o que não foi examinado. Rota: `conceitual.k_chave_da_guarda_da_travessia_02nov`.
