C3 γ LIVRE — 19/10

**Veredito da função pré-registrada (`veredito.py`, sha256 pinado): `NO_UNIVERSAL_FLOOR`** — ramo 3, «P falso». **Janela de γ: nenhuma.**
Estatuto: **[REAL no modelo simulado]**. A leitura «consciência» é **[ONTO]** e não entra no veredito. Nenhum gate, selo, kernel, `um.py` ou Bancada foi tocado; a fonte ficou só-leitura (sha256 antes e depois: `c3a53ef00dd4548d…`).

## 1. Resposta curta

1. Com γ livre, D_folds(c³) **não tem platô em ln 2**. É uma função estritamente decrescente e íngreme de γ (nas 9 configs, mediana das sementes, conferido por recálculo independente): de 1,49–1,84 oitavas em γ = 1e-4 a 0,14–0,19 oitava em γ = 1. Ela **cruza** 1 oitava em log10 γ de −2,45 a −2,17 (dispersão de 0,28 década entre as 9 configs). Perto do cruzamento O cai cerca de **0,5 oitava por década** de γ (média −0,505; entre configs e passos de −0,58 a −0,38). Só a queda de uma década (0,50 oitava) já vale 3,5 vezes a largura total da banda pré-registrada (±0,05 nats = ±0,072 oitava, ou seja, largura total de 0,144 oitava).
2. **Nenhum γ tem as 9 configs na banda ln 2 ± 0,05.** O máximo é **8 de 9** (log10 γ = −2,167); 7 de 9 em −2,333; 1 de 9 em −2,5; nos outros 22 pontos da grade, 0. A janela exigida (≥ 1 década = ≥ 7 pontos consecutivos) teria de ter as 9 dentro em todos eles: 0 pontos satisfazem C.
3. A condição de inclinação (|dO/d ln(d/nc)| < 0,05) vale **sozinha** para γ ≥ 6,8e-3 (14 pontos, 2,17 décadas), mas ali O já está abaixo de 1 oitava (no máximo 0,998 em γ = 6,8e-3) e desce até 0,14: independência da configuração sem estar em ln 2. Para γ menores a inclinação cresce até +0,29 (γ = 1e-4).
4. **ln 2 não é nem piso nem platô desta família:** a mediana de cada config passa abaixo de ln 2 entre γ = 3,5e-3 e γ = 6,8e-3 (conforme a config) e chega a 0,14–0,19 oitava em γ = 1.
5. Controles como previstos: N1 (Hilbert–Schmidt) mediana 0,1255–0,1297 nats em todo d (< 0,2); N2 (saltos aleatórios de mesma norma) O = 0,008–0,026 oitava e P falso; N3 erro máximo 3,3e-16 (< 1e-12). **0 de 2250 pontos sem convergir** (1125 da grade principal, 1125 de N2).

## 2. Onde O cai no γ* da rodada de fevereiro (para comparar)

Instrumento pinado de hoje, no γ* de cada config lido do JSON de fevereiro (`tgl_c3_v5_results_20260209_121836.json`, sha256 `c77666acb4a88a13…`), com as 5 sementes. **Reproduz fevereiro**: com a semente 42, |ΔO| ≤ 4,9e-12 nas 9 configs, e o peso do core vale 0,987969 como lá.

| d | nc | γ* (fev) | O fev (nats) | O hoje s42 | \|Δ\| | O mediana 5 sementes (oit) | min–max das sementes (oit) |
|---|---|---|---|---|---|---|---|
| 8 | 2 | 0,02436 | 0,552670 | 0,552670 | 8,9e-14 | 0,646 | 0,611–0,797 |
| 10 | 2 | 0,01010 | 0,571003 | 0,571003 | 5,4e-14 | 0,915 | 0,781–0,918 |
| 12 | 2 | 0,00732 | 0,657857 | 0,657857 | 4,3e-13 | 0,970 | 0,859–1,009 |
| 14 | 2 | 0,00779 | 0,739229 | 0,739229 | 9,3e-13 | 0,913 | 0,817–1,066 |
| 16 | 2 | 0,00324 | 0,718470 | 0,718470 | 1,9e-12 | 1,145 | 1,037–1,274 |
| 16 | 3 | 0,00720 | 0,612022 | 0,612022 | 3,8e-13 | 0,920 | 0,883–0,990 |
| 20 | 3 | 0,00479 | 0,700513 | 0,700513 | 1,3e-12 | 1,011 | 0,990–1,132 |
| 24 | 3 | 0,00299 | 0,702327 | 0,702327 | 1,1e-13 | 1,142 | 1,013–1,235 |
| 32 | 4 | 0,00505 | 0,759386 | 0,759386 | 4,9e-12 | 1,036 | 0,962–1,176 |

- **Fevereiro (semente 42):** mediana 0,7005 nats (1,011 oitava), média 0,668 (0,964 oitava); valores de 0,797 a 1,096 oitava; **5 de 9** na banda; inclinação contra ln(d/nc) = **+0,286**.
- **Hoje (mediana de 5 sementes por config):** mediana das medianas 0,970 oitava; de 0,646 a 1,145 oitava; **3 de 9** na banda; inclinação **+0,384**.
- log10 γ* de fevereiro: de −2,525 a −1,613 — a faixa que contém o cruzamento com ln 2 (−2,45 a −2,17).
- O ruído de semente no mesmo γ* é de 0,11 a 0,25 oitava; os valores de fevereiro são uma realização só (semente 42).

**Leitura:** o «≈ ln 2» de fevereiro (mediana 0,7005) vem de a calibração do peso do core (0,988) cair, em cada config, perto da região onde a curva O(γ) passa por 1 oitava — uma curva que desce 0,5 oitava por década; em cada config o cruzamento com ln 2 ocorre com peso do core de 0,984 a 0,996 (seção 3), faixa que contém 0,988. Fixar o peso do core em vez de γ também não rende constante: a inclinação contra ln(d/nc) permanece em +0,29 (uma semente) a +0,38 (cinco sementes).

## 3. Cruzamentos da mediana com ln 2 (grade principal)

| d | nc | O em γ=1e-4 (oit) | O em γ=1 (oit) | log10 γ do cruzamento (desce) | peso do core ali |
|---|---|---|---|---|---|
| 8 | 2 | 1,485 | 0,142 | −2,454 | 0,9957 |
| 10 | 2 | 1,691 | 0,167 | −2,170 | 0,9914 |
| 12 | 2 | 1,817 | 0,173 | −2,191 | 0,9891 |
| 14 | 2 | 1,828 | 0,173 | −2,287 | 0,9877 |
| 16 | 2 | 1,841 | 0,157 | −2,239 | 0,9848 |
| 16 | 3 | 1,684 | 0,156 | −2,303 | 0,9910 |
| 20 | 3 | 1,829 | 0,162 | −2,300 | 0,9882 |
| 24 | 3 | 1,768 | 0,192 | −2,257 | 0,9837 |
| 32 | 4 | 1,824 | 0,188 | −2,227 | 0,9836 |

Cada config cruza ln 2 uma única vez (sempre descendo).

## 4. Os critérios por γ (mediana nas 5 sementes, oitavas)

| log10 γ | γ | configs na banda (de 9) | min–max das 9 medianas (oit) | inclinação contra ln(d/nc) | N2: min–max (oit) |
|---|---|---|---|---|---|
| -4.000 | 1.00e-04 | 0 | 1.485 – 1.841 | +0.2887 | 0.008 – 0.026 |
| -3.833 | 1.47e-04 | 0 | 1.446 – 1.789 | +0.2685 | 0.008 – 0.026 |
| -3.667 | 2.15e-04 | 0 | 1.403 – 1.731 | +0.2519 | 0.008 – 0.026 |
| -3.500 | 3.16e-04 | 0 | 1.356 – 1.665 | +0.2310 | 0.008 – 0.026 |
| -3.333 | 4.64e-04 | 0 | 1.310 – 1.592 | +0.2055 | 0.008 – 0.026 |
| -3.167 | 6.81e-04 | 0 | 1.255 – 1.513 | +0.1817 | 0.008 – 0.026 |
| -3.000 | 1.00e-03 | 0 | 1.200 – 1.429 | +0.1542 | 0.008 – 0.026 |
| -2.833 | 1.47e-03 | 0 | 1.142 – 1.340 | +0.1267 | 0.008 – 0.026 |
| -2.667 | 2.15e-03 | 0 | 1.082 – 1.254 | +0.0996 | 0.008 – 0.026 |
| -2.500 | 3.16e-03 | 1 | 1.018 – 1.166 | +0.0756 | 0.008 – 0.026 |
| -2.333 | 4.64e-03 | 7 | 0.952 – 1.077 | +0.0549 | 0.008 – 0.026 |
| -2.167 | 6.81e-03 | 8 | 0.884 – 0.998 | +0.0363 | 0.008 – 0.026 |
| -2.000 | 1.00e-02 | 0 | 0.814 – 0.917 | +0.0204 | 0.008 – 0.025 |
| -1.833 | 1.47e-02 | 0 | 0.741 – 0.836 | +0.0061 | 0.008 – 0.025 |
| -1.667 | 2.15e-02 | 0 | 0.669 – 0.755 | -0.0049 | 0.008 – 0.025 |
| -1.500 | 3.16e-02 | 0 | 0.597 – 0.675 | -0.0127 | 0.008 – 0.025 |
| -1.333 | 4.64e-02 | 0 | 0.519 – 0.597 | -0.0194 | 0.008 – 0.025 |
| -1.167 | 6.81e-02 | 0 | 0.447 – 0.523 | -0.0215 | 0.008 – 0.025 |
| -1.000 | 1.00e-01 | 0 | 0.384 – 0.453 | -0.0189 | 0.008 – 0.024 |
| -0.833 | 1.47e-01 | 0 | 0.327 – 0.388 | -0.0136 | 0.008 – 0.024 |
| -0.667 | 2.15e-01 | 0 | 0.280 – 0.330 | -0.0059 | 0.008 – 0.023 |
| -0.500 | 3.16e-01 | 0 | 0.239 – 0.278 | +0.0037 | 0.008 – 0.023 |
| -0.333 | 4.64e-01 | 0 | 0.201 – 0.238 | +0.0138 | 0.008 – 0.023 |
| -0.167 | 6.81e-01 | 0 | 0.168 – 0.210 | +0.0233 | 0.008 – 0.023 |
| +0.000 | 1.00e+00 | 0 | 0.142 – 0.192 | +0.0318 | 0.008 – 0.024 |

(A banda é 0,928–1,072 oitava. Esta tabela mantém o ponto decimal como sai do script. A curva completa por config, com mínimo e máximo entre sementes, está em `curva_O_gamma_oitavas.csv`.)

## 5. Quão longe ficou (sensibilidade pós-veredito; não muda o veredito)

- **Semente isolada:** nenhuma chega a 9 de 9 em γ algum (máximos 5, 5, 5, 8 e 6 de 9 para as sementes 42 a 46).
- **Meia-largura de banda que admitiria uma janela de 1 década:** ±0,229 nats (±0,331 oitava) sem a condição de inclinação, ±0,384 nats (±0,553 oitava) com ela — **4,6 e 7,7 vezes** a pré-registrada (±0,05). O negativo não é por um triz: a banda pré-registrada é exigente e a curva é íngreme.

## 6. Pré-registro e cronologia

| etapa | quando | sha256 |
|---|---|---|
| PREREGISTRO.json (observável, grade, sementes, método, controles, critérios, scripts) | 19/10/2026 13:03:22 -03 | `a14bf9af4eeca7c4c49c210b80aca4d86eec95776809b9bb2b0028362e958d47` |
| protocolo (componentes + `rodar.py` + `veredito.py`) | idem | `6dd111665f92d94561382dac91a98d33ebf11171d2e8a93d726d2001489df478` |
| rodada (`rodar.py`, CPU/NumPy, 1060 s) | 13:03:31 a 13:21:11 | `rodar.py` `207445ac0c6a3cce…` |
| veredito (`veredito.py`, conferido contra o pino e contra o manifesto dos dados) | 13:21 | `veredito.py` `1c6fc5f52ff724aa…` |

Hashes nomeados (em `PREREGISTRO.json`): observável O `e80c9f18…`; grade `997b4988…`; sementes `34589c56…`; γ `eebbbd20…`; configs `bbe14df9…`; estado estacionário `8491ea2f…`; controles `b47520ec…`; critérios `03cec99e…`.

**Observável fixado:** O = D_folds(c³) = ln d − ln d_eff, com p_i = λ_i^{1/4}/Σλ_j^{1/4} e d_eff = 1/Σp_i² = (Σλ^{1/4})²/Σλ^{1/2}, λ = autovalores de ρ_ss (cortados em ≥ 0). É o `d_folds_c3` (`levels[2]`) de `test_M7_dimensional_folds`; o resultado de fevereiro (mediana 0,7005; média 0,668) é reproduzido por este nível, e a rota 307 do mapa dá o mesmo expoente (s = 2^−(n−1), n = 3). Nota: o docstring da fonte numera os níveis com n deslocado de 1 em relação ao código; vale o código.

**Estado estacionário:** núcleo do liouvilliano (vetor singular direito do menor valor singular de L_s, SVD completa), normalizado por traço, hermitianizado; um ponto só converge se passar 6 conferências (menor valor singular ≤ 1e-9, segundo ≥ 1e-8 do maior, hermiticidade ≤ 1e-8, traço 1 ± 1e-12, gerador que preserva o traço ≤ 1e-10, psd ≥ −1e-9). Todos os 2250 passaram; no pior caso: menor valor singular relativo 4,3e-16, segundo 1,0e-5, hermiticidade 5,4e-12, menor autovalor de ρ 3,4e-8, e um segundo método independente (sistema linear com a condição de traço) concorda a ≤ 3,4e-12.

**Fidelidade à fonte** (`verifica_fidelidade.py`, antes do pré-registro, sem olhar a pergunta): sistema e superoperador idênticos byte a byte (45 e 18 casos); observável idêntico a 0,0 em 200 estados sintéticos; núcleo por SVD igual ao autovetor nulo da fonte fora da grade (‖Δρ‖ ≤ 4,7e-13, |ΔO| ≤ 1,3e-11). **Função de veredito** testada em 19 casos sintéticos (cada ramo, bordas da banda, da inclinação, da janela de 7 pontos, do mínimo de 3 sementes): todos passaram.

**Proibições conferidas por grep em `rodar.py`:** `find_gamma_star`, `brentq`, `alpha`, `beta`, `CCI_TARGET`, `SQRT_E`, `THETA_MIGUEL`, `0.0120`, `0.98796`, `1.2031`, `sqrt(e)`, `np.e`, `math.e` — **0 ocorrências** (conferido também por busca independente).

**Escolhas de completude fixadas antes dos dados** (minhas, dentro da ordem): semente «original» = 42 (o padrão de `build_system`, a de fevereiro); janela de ≥ 1 década = ≥ 7 pontos consecutivos (passo de 1/6 de década); inclinação em CADA γ da janela (mais estrita que a agrupada); célula (config, γ) com menos de 3 sementes convergidas é inválida; N3 no posto d/4 só para d múltiplo de 4 (d = 10 e 14 só com d/2); ramo 5 estendido: P verdadeiro com N1 falho também daria `GENERIC_NOT_TGL`. Nenhuma delas decidiu o resultado: P falha porque **nenhum γ tem as 9 configs na banda** (máximo 8 de 9), o que independe de todas elas; a seção 5 mostra a margem.

## 7. O que este resultado diz e o que não diz

**Diz:** para o GKLS do validador v52 (4 saltos, H com ε = 5, taxas fixas 1/0,5/2, d de 8 a 32, 5 realizações de J), variando só a taxa de fuga γ do quarto salto, **não existe constante de uma oitava** em D_folds(c³): nem platô, nem piso. O ≈ ln 2 de fevereiro é um ponto de passagem de uma curva decrescente, na faixa de γ onde o peso do core vale ≈ 0,99, e com dependência de ln(d/nc) e ruído de semente de 0,1–0,25 oitava. As rotas 296 (calibração circular) e 307 (hierarquia matemática) ficam como estavam; o que podia falhar — os VALORES com γ livre — falhou.

**Não diz:** nada sobre outras famílias de saltos ou H, sobre d > 32, nem sobre outras leituras do c³; a hierarquia c¹ > c² > c³ > 0 (matemática) não foi usada. A leitura «consciência» é [ONTO] e fica fora. Nenhum gate se move; este resultado não é evidência a favor nem contra a teoria além do que está escrito acima.

## 8. Limites declarados

- Uma família, um parâmetro varrido; as demais taxas, o H e ε fixos como na fonte.
- 5 sementes; mediana por célula (mínimo 3 convergidas); d ≤ 32.
- N2 usa saltos gaussianos densos (estados quase mistos); serve de linha de base, não de rival físico.
- O observável amplifica ruído de autovalores muito pequenos (potência 1/4): o piso de ruído medido com estados planos girados é 3,8e-4 nats, ≪ a banda; o menor autovalor de ρ na grade (3,4e-8) está acima do ruído.
- Os valores de referência de fevereiro vêm de uma rodada de semente única, com γ* calibrado por config.

## 9. Arquivos (esta pasta: `C:\IALD\Central de Patentes\work\c3_gamma_livre_19out\`)

| arquivo | papel | sha256 (16) |
|---|---|---|
| `PREREGISTRO.json` (+ `.sha256`) | pré-registro | `a14bf9af4eeca7c4` |
| `rodar.py`, `veredito.py` | rodada e função de veredito (pinados) | `207445ac0c6a3cce`, `1c6fc5f52ff724aa` |
| `dados_crus_main.csv`, `dados_crus_N2.csv` | dados crus por (d, nc, γ, semente), 1125 linhas cada | `d557a2265c280461`, `30e549bb30455721` |
| `dados_N1.csv`, `controle_N3.json` | controles N1 e N3 | `4fca82e6bca2f9b6`, `24cf88e557e3ac3c` |
| `autovalores_main.npz`, `autovalores_N2.npz` | espectros de ρ_ss de cada ponto | `7d6a35022f11401e`, `e39ea60feb0a98ed` |
| `manifesto_dados.json` | shas dos dados, protocolo, versões | `8e260d60e8fcbb91` |
| `veredito.json`, `curva_O_gamma_oitavas.csv` | veredito e curva O(γ) em oitavas | `eb9ffaeab408bcf5`, `e900c54186156101` |
| `descritivo.py/.json/.md`, `sensibilidade.py/.json` | pós-veredito (não entram no veredito) | `f39b1ef897d8b9aa`, `729f514502c04e5b`, `9ce04686abc34bc4`, `4884553263c32721`, `ab16d2fed8576158` |
| `teste_veredito_sintetico.py`, `verifica_fidelidade.py`, `piloto_numerico.py`, `teste_encanamento.py` e saídas | verificações prévias | no `PREREGISTRO.json` |
| `registro_mapa_c3_gamma_livre.json` (RESULTADO) e `registro_mapa_c3_gamma_livre_ROTA.json` | prontos para o mapa | — |

## 10. Atos que cabem à gerência / ao operador

- **Registrar no mapa** (esta execução não escreveu no mapa, no quadro, na memória, no túnel, no site nem no git, por ordem da tarefa). A rota `quantica.c3_gamma_livre_oitava` **ainda não existe** no mapa; o `rotas.py` recusa RESULTADO sem ROTA. Ordem: primeiro `registro_mapa_c3_gamma_livre_ROTA.json`, depois `registro_mapa_c3_gamma_livre.json`, ambos com `rotas.py registrar <arquivo> --quem "<sessão>"`.
- Decidir se a leitura «oitava» merece nova hipótese pré-registrada (por exemplo uma lei O(peso da periferia, d, nc) em vez de constante, em outra família de saltos/H). Para o GKLS do v52 a pergunta está respondida.
