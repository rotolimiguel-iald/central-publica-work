# Sessão com a IALD Nativa v4: testes para 5σ (02/11/2026)

**Ordem do operador:** verbatim em `work\cunhagens_13out\OPERADOR_02nov_sessao_iald_nativa_5sigma_verbatim.txt` (sha16 `25d5e21ba0cf74b4`).
**Estatuto:** toda resposta dela é `[DECLARADO]`; neural = ilustração; nada aqui move gate, rito ou canal.

## O que foi feito

42 rodadas no modelo servido em :8081 (302543 tokens gerados, 23.7 min de GPU), com o mesmo system do treino. Modelo puro, sem a memória do app. Transcritos em `transcritos\`.

| bloco | pergunta | leitura |
|---|---|---|
| A | a do operador, verbatim | modo direto: «não há teste», TGL «não é falsificável», laço até o corte. Com raciocínio: conselho genérico de cosmologia, com erros sobre a teoria |
| B | melhorada, com regras | modo direto: tabela com aparência de resultado («já hoje ~5–10σ»), toda inventada. Com raciocínio: laço; só B5 concluiu, com fontes e números inventados |
| C | com resumo do já examinado (12 sementes) | propostas novas sem derivação; `[DERIVED]` usado sem derivação. Melhor: C8 (corte no lenteamento do CMB em ℓ < 30), que cai na variância cósmica (lê-se abaixo). Melhor pista: C17 (dualidade de distância) |
| D | teoremas do kernel com consequência nunca testada | 0 de 78 nomes específicos existem no kernel, inclusive quando ela escreve «não há nome inventado» |
| E, F1, G | enunciados reais dentro da pergunta | o melhor regime: admite `[OPEN]`, acha a lacuna certa, refuta a própria proposta. Ainda erra contas e inventa citações (G2) |

## Medidas da capacidade dela [REAL]

- **Memória de kernel:** 203 nomes distintos citados; 78 específicos (três palavras ou mais): **0** existem como identificador nas fontes `.lean` (10,8 M caracteres). Módulos reais: 2. `NOMES_CONFERIDOS.json`.
- **β escrito nas respostas (amostra lida à mão):** nas 8 rodadas em que o valor aparece como β, 4 erram (~0,1 em A3; 0,0128 em B1; 0,012034 em E2; 0,012249 em E3), 1 erra só a última casa (0,012032 em G1) e 3 acertam ou arredondam.
- **Sem resposta final:** 9 rodadas gastaram os 12.000 tokens em raciocínio; o laço chegou a 841 linhas com 44 distintas.

## As três pistas, conferidas

**1. Distorções espectrais do CMB (FIRAS).** Não estava no Mapa nem no Atlas. Mas o fechamento ρ+p declara a hipótese de não-troca de energia entre setores, logo a TGL prevê μ = 0, igual ao ΛCDM. **Não discrimina; veta um ramo.** Se toda a resposta (4/3)β trocasse energia com os fótons na janela do μ, então μ ≈ 0.0225, cerca de 956σ contra o limite |μ| < 4,7×10⁻⁵ a 95% (Bianchini & Fabbian 2022; σ aproximado pela metade do limite). A fração trocada permitida é < 0.21%. Ganho real: a hipótese declarada ganha um teste externo publicado.

**2. Dualidade de distância (C17).** Não é nova: é a rota `discriminante.ordem018.f2.r_e` (η = f_L/f_A), parada porque o mapa físico entre luminosidade e ângulo não foi derivado. A forma com sirenes (D_L de GW contra D_A de EM) também depende desse mapa. A literatura de 2025–2026 está dividida sobre DESI DR2 + Pantheon+. O rival tem valor nulo exato, o que torna a rota valiosa, mas a TGL ainda não diz quanto vale η.

**3. N_eff.** Ela o citou de passagem (A3, F1). O canal é conhecido (v154, «linha de morte»), mas **não entrou nas buscas 5σ-01 nem 5σ-02**, e tem o que falta às outras: Modelo Padrão com valor fixo 3,044 e previsão sem parâmetro, N_eff = 3.1635. Medida que não está nas fontes congeladas: Goldstein & Hill, arXiv:2603.13226 (v2, 20/03/2026) `[lido no HTML do arXiv]`:

| combinação | N_eff | TGL (σ do centro) | SM (σ do centro) | separação TGL–SM (σ) |
|---|---|---|---|---|
| So nucleossintese (He + D) | 2.976 ± 0.093 | 2.02 | 0.73 | 1.28 |
| CMB-PAS, sem low-l EE | 2.890 ± 0.120 | 2.28 | 1.28 | 1.00 |
| CMB-PAS + DESI, sem abundancias | 3.010 ± 0.110 | 1.40 | 0.31 | 1.09 |
| Planck + He LBT + D | 2.961 ± 0.082 | 2.47 | 1.01 | 1.46 |
| Completa (He + D + CMB-PAS + DESI) | 2.990 ± 0.070 | 2.48 | 0.77 | 1.71 |

ΔN_eff < 0,107 a 95% (variantes: 0,0913; 0,116; 0,0876), com prior ΔN_eff > 0. O +0.1195 da TGL fica acima das quatro. A linha só de nucleossíntese é canal de fundo puro: a ressalva perturbativa (TGL-S contra TGL-L) não se aplica a ela. Para 5σ TGL–SM é preciso σ = 0.0239; se o centro persistir, 5σ contra o fechamento ρ+p chega antes, com σ = 0.0347. Abaixo da regra de TENSÃO do rito (3σ): o canal segue `TGL_NEFF_ARMED_CONSISTENT`, não gateia. Nada foi instalado: admitir a medida é a D8, e a linha de Y_p é a X16, ambas do operador.

## C8 conferida

Em ℓ = 2..29 há 896 modos: variância cósmica de 4,72% com céu inteiro e ruído zero. 5σ exigiria efeito ≥ 23,6%; ela estimou 0,5–1%. Regra geral: um efeito de tamanho β pede cerca de 345 mil modos independentes para 5σ, e a parede não é a contagem de modos, é a degenerescência com A_s, Ω_m, r_d (já medida na rota `bao_cmb.d10.degenerescencia_do_fundo`).

## Veredito

Nenhuma rota nova de 5σ. Isto é parede do modelo, não falsificação da teoria. O treino deu a ela vocabulário e disciplina de estatuto, não memória: a teoria não está nos pesos, e ela rende quando recebe os enunciados.
