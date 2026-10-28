# ORDEM KIMI 5σ-01 (27/10/2026) — Levantamento e desenho: onde β_TGL aparece SEM supressão de Planck fora da cosmologia, e o custo de levar cada rota a 5σ

**De:** gerência c1 da Central (Claude Code), por ordem do operador Luiz Antonio Rotoli Miguel (IALD/TGL).
**Para:** Kimi.
**Tipo:** LEVANTAMENTO + DESENHO. Sem execução sobre dados, sem download, sem ajuste de parâmetro, sem publicação.
**Estatuto de tudo que você devolver:** `[DECLARADO pelo Kimi]` até a gerência conferir na fonte. Nada do que você escrever autoriza execução, move o gate da TGL ou cria selo.

## §0 Por que esta ordem existe (medido pela gerência em 27/10/2026)

A lei de dephasing da TGL é Γ_ω = ½·β·τ★·ω², com β = α·√e calculado em runtime (0,0120313…; nunca literal) e, no ramo canônico, τ★ = t_Planck. Com isso, o tamanho do efeito em cada canal de laboratório, partícula ou onda gravitacional é:

| canal | ω (rad/s) | Γ_TGL (s⁻¹) | sensibilidade atual (s⁻¹) [KNOWN, ordem de grandeza — você confirma com fonte] | ordens que faltam |
|---|---|---|---|---|
| neutrino DUNE, E = 1 GeV, n = −2 (ω = Δm²/2E) | 1,9e3 | 1,2e-39 | ~15 (cota de decoerência ~1e-23 GeV) | 40 |
| neutrino JUNO, E = 3 MeV | 1,9e4 | 1,2e-37 | ~15 | 38 |
| ringdown LIGO, f = 250 Hz | 1,6e3 | 8,0e-40 | ~50 (1/τ_QNM a ~20%) | 41 |
| NANOGrav, f = 1e-8 Hz | 6,3e-8 | 1,3e-60 | ~1e-9 | 51 |
| relógio óptico Sr, 429 THz | 2,7e15 | 2,4e-15 | ~1e-2 (coerência ~100 s) | 13 |
| relógio nuclear Th-229, 2,02 PHz | 1,3e16 | 5,2e-14 | ~1e-3 (aspiração mHz em íon) | 10 |
| Mössbauer Fe-57, 14,4 keV | 2,2e19 | 1,6e-7 | ~7e6 (largura natural) | 14 |

**Leitura:** no laboratório β vem multiplicado por t_Planck e fica de 10 a 51 ordens de grandeza abaixo de qualquer instrumento. Não é falta de estatística: é supressão de Planck. Na cosmologia β entra como FRAÇÃO ou EXPOENTE de ordem 1 (piso dos vazios ρ/ρ̄ ≥ β = 0,012; razão de Hubble com expoente 2β/3 = 0,008). O que separa os dois casos é se o SISTEMA tem horizonte próprio cujo tempo substitui t_Planck. O buraco negro tem: o ramo B do ringdown (τ★ = k·GM/c³, pré-registrado na v386, `PREREG_RAMO_B_RINGDOWN_20261005_V1`, sha16 `86f98fcc124dd9ca`) dá Γ_TGL ≈ 0,014·k de 1/τ_QNM, independente da massa — efeito de ordem 1. Isso já existe na casa e NÃO se refaz.

**Nota do operador (27/10/2026, ratificação verbatim, `work/cunhagens_13out/OPERADOR_27out_e_isso_prossiga_pre_registro_ja_fizemos_verbatim.txt`):** «É isso, prossiga, as outras formas foram indicações de pré-registro para dados futuros e eu desprezei porque já fizemos isso». Logo: NÃO responda com «pré-registre e espere os dados». A casa já fez isso (piso dos vazios V11, Fase 9 da razão de Hubble, ramo B v386). A pergunta é onde β aparece em ordem 1 fora da cosmologia e o que falta, em número, para 5σ.

## §1 A pergunta que você responde

**Fora do horizonte cosmológico, em que sistemas físicos a TGL faz β aparecer sem o fator t_Planck — e quanto custa (dado, N, σ) levar cada um a um teste de 5σ pré-registrado, com zero parâmetro ajustado ao dado?**

## §2 Fontes permitidas

1. As portas públicas da TGL: `https://teoriadagravitacaoluminodinamica.com` → `llms.txt` na raiz → `PORTA.md` / `PORTA.json` de cada pasta (URL raw direta de cada arquivo; nunca adivinhe caminho). Espelho: GitHub `rotolimiguel-iald/the_boundary`, branch `main`.
2. A Central pública (`/central/` no site e os três repositórios públicos ligados ali).
3. Literatura: só com DOI ou arXiv e data de acesso.
Nada do que não esteja numa porta ou numa referência se presume. Se não achou, escreva «não localizado na fonte X», nunca «não existe».

## §3 Entregáveis

**A. Inventário:** onde β é de ordem 1 na TGL pública. Pelo menos: a matriz-S da fronteira (|R|² = β, |T|² = 1−β, θ_M = arcsin√β); o piso dos vazios ρ/ρ̄ ≥ β; a razão de Hubble K = E(z*)^{2β/3}; S_∂ = ½ nat; Vol_∂^min = √e; a inscrição 1 = q² + α²; Δn_Q = −β (sombra numérica, não natureza); Chandrasekhar ~0,35% (negativo honesto). Para cada item: URL da fonte e o estatuto COMO ESTÁ na fonte.

**B. Candidatos fora da cosmologia** (mínimo):
- B1 buracos negros — ringdown, ramo B: NÃO rederivar; citar o pré-registro v386; só atualizar sensibilidade e N com catálogos públicos O4/O5.
- B2 ecos de ondas gravitacionais: reclassificados na casa (o observável é o dephasing, não o eco). Não reviver; registrar em uma linha por que não.
- B3 horizontes análogos: condensado de Bose-Einstein (Steinhauer), fibra óptica (Philbin/Leonhardt), água (Weinfurtner/Rousseaux).
- B4 detectores acelerados / efeito Unruh; a temperatura κ/2π e o balanço de Clausius.
- B5 Casimir dinâmico e contornos de cavidade (circuitos supercondutores).
- B6 relógios ópticos e nucleares, interferometria atômica de grande base: confirmar as ordens da tabela acima, com fonte.
- B7 Mössbauer e linhas γ.
- B8 neutrinos (n = −2): só o número com fonte; o canal F7.2 da casa existe.
- B9 informação/engenharia — ACOM: classificar como ENGENHARIA (ver C2).

Para cada candidato, nove colunas: (1) sistema; (2) onde está o contorno/horizonte do sistema e qual tempo substitui t_Planck; (3) observável que a TGL prediz — DERIVADO (cite a fonte pública) ou NÃO DERIVADO (escreva «[OPEN] não derivado»; não invente derivação); (4) tamanho previsto com ZERO parâmetro ajustado (β = α√e); (5) melhor sensibilidade atual, com referência; (6) ordens de grandeza que faltam; (7) N de eventos ou tempo de integração para 5σ; (8) dado PÚBLICO já existente — retrodição sem ajuste é evidência de pleno direito (precedente: o periélio de Mercúrio); (9) estatuto.

**C. Exclusões obrigatórias** (escreva-as no relatório, para não voltarem):
- C1 «identidade CODATA»: β é DEFINIDO como α√e; α = β/√e é tautologia; «infinitos sigmas» é zero evidência; qualquer «resíduo de 1e-15» é arredondamento de ponto flutuante. A casa já descircularizou o BBN pelo mesmo motivo (28/09/2026).
- C2 benchmark de compressão (ACOM contra zstd/LZMA): mede codec contra codec, não a natureza. Pode entrar no dossiê de engenharia da patente BR 10 2025 026951-1; jamais como «σ da TGL».
- C3 qualquer teste com parâmetro ajustado ao dado.
- C4 qualquer frase com «confirmado» ou «CONFIRMED»: a confirmação é creditação (ato do observador humano). O que se mede devolve NOT_FALSIFIED, FALSIFIED, INCONCLUSIVE ou UNDERPOWERED.
- C5 β literal: sempre α√e.

**D. Rascunho de pré-registro** para TODA rota com gap ≤ 1 ordem de grandeza, se houver: função de veredito, alvos, covariância, vereditos permitidos, controles nulos, cegamento, critério de poder. A gerência fixa por hash ANTES de qualquer dado ser aberto. Se nenhuma rota chega a gap ≤ 1, escreva isso: negativo honesto é resultado.

**E. Formato:** resumo de até 15 linhas no topo; a tabela; referências com URL/DOI e data de acesso; estatuto em cada linha. Nenhuma execução sobre dados, nenhum download, nenhum ajuste. Não tocar as rotas cosmológicas (a Fase 9 corre na Central).

## §4 A régua (vale para você como para qualquer IA da casa)

O número corrige a frase. NOT_FALSIFIED nunca é CONFIRMED. Prova é validade (kernel); confirmação é creditação (observador). A evidência vale pela novidade de uso (nenhum parâmetro ajustado ao dado), não pela data do dado: «pós-dição» nunca é demérito. Hash nunca de memória. Correção ao lado, nunca por cima.

## §5 Devolução

O operador cola a sua resposta à gerência (texto ou arquivo .md). A gerência confere cada linha na fonte, consulta o Mapa de Rotas para cada candidato (rota já examinada não se refaz), registra as rotas novas e decide o próximo passo com o operador.
