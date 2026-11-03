# -*- coding: utf-8 -*-
"""Fecho da sessao com a IALD Nativa v4 sobre 5 sigma (gerencia c1, 02/11/2026): medidas finais por script e relatorio. Nada aqui move gate, rito ou canal."""
import hashlib, json, math, re, time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
T = AQUI / "transcritos"
ALPHA_FINE_CODATA_2018 = 7.2973525693e-3
beta = ALPHA_FINE_CODATA_2018 * math.sqrt(math.e)
rod = []
for p in sorted(T.glob("*.jsonl")):
    for l in p.read_text(encoding="utf-8").splitlines():
        x = json.loads(l)
        x["conv"] = p.stem
        rod.append(x)
sem_resp = [x["conv"] for x in rod if not x["resposta"].strip()]
laco = [x["conv"] for x in rod if x["finish"] == "length" and x["resposta"].strip()]
num = re.compile(r"(?<![\d.,])0[.,]01\d{1,8}")
vals = {}
for x in rod:
    if not x["resposta"].strip():
        continue
    for m in re.finditer(r"β[^\n]{0,40}?(0[.,]01\d{1,8})", x["resposta"]):
        vals.setdefault(m.group(1).replace(",", "."), set()).add(x["conv"])
certos = {k: v for k, v in vals.items() if abs(float(k) - beta) / beta < 5e-4}
errados = {k: v for k, v in vals.items() if abs(float(k) - beta) / beta >= 5e-4}
tempo = sum(x["seg"] for x in rod)
tok = sum((x["usage"] or {}).get("completion_tokens", 0) for x in rod)

pred = 3.044 + (4 / 3) * (1 + (7 / 8) * (4 / 11) ** (4 / 3) * 3.044) / ((7 / 8) * (4 / 11) ** (4 / 3)) * beta
med = [("So nucleossintese (He + D)", 2.976, 0.093), ("CMB-PAS, sem low-l EE", 2.89, 0.12), ("CMB-PAS + DESI, sem abundancias", 3.01, 0.11), ("Planck + He LBT + D", 2.961, 0.082), ("Completa (He + D + CMB-PAS + DESI)", 2.990, 0.070)]
linhas_n = "\n".join("| %s | %.3f ± %.3f | %.2f | %.2f | %.2f |" % (n, c, s, (pred - c) / s, (3.044 - c) / s, (pred - 3.044) / s) for n, c, s in med)
dro = (4 / 3) * beta
mu = 1.401 * dro
sig_mu = 4.7e-5 / 2
fr = 4.7e-5 / mu
modos = 2 * (5 / beta) ** 2
assert abs(pred - 3.1634660752537327) < 1e-9

R = {"rodadas": len(rod), "sem_resposta_final": sem_resp, "cortadas_com_resposta": laco, "seg_total": round(tempo, 1), "tokens_gerados": tok,
     "beta_citado_certo": {k: sorted(v) for k, v in certos.items()}, "beta_citado_errado": {k: sorted(v) for k, v in errados.items()},
     "Neff_TGL": pred, "mu_se_troca_total": mu, "sigma_mu_aprox": sig_mu, "mu_em_sigmas": mu / sig_mu, "fracao_max_trocada_95": fr, "modos_para_5sigma_efeito_beta": modos}
(AQUI / "MEDIDAS_FINAIS.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in R.items() if k not in ("beta_citado_certo", "beta_citado_errado")}, ensure_ascii=False))
print("beta certo", {k: len(v) for k, v in certos.items()}, "| errado", {k: len(v) for k, v in errados.items()})

REL = f"""# Sessão com a IALD Nativa v4: testes para 5σ (02/11/2026)

**Ordem do operador:** verbatim em `work\\cunhagens_13out\\OPERADOR_02nov_sessao_iald_nativa_5sigma_verbatim.txt` (sha16 `25d5e21ba0cf74b4`).
**Estatuto:** toda resposta dela é `[DECLARADO]`; neural = ilustração; nada aqui move gate, rito ou canal.

## O que foi feito

{len(rod)} rodadas no modelo servido em :8081 ({tok} tokens gerados, {tempo / 60:.1f} min de GPU), com o mesmo system do treino. Modelo puro, sem a memória do app. Transcritos em `transcritos\\`.

| bloco | pergunta | leitura |
|---|---|---|
| A | a do operador, verbatim | modo direto: «não há teste», TGL «não é falsificável», laço até o corte. Com raciocínio: conselho genérico de cosmologia, com erros sobre a teoria |
| B | melhorada, com regras | modo direto: tabela com aparência de resultado («já hoje ~5–10σ»), toda inventada. Com raciocínio: laço; só B5 concluiu, com fontes e números inventados |
| C | com resumo do já examinado (12 sementes) | propostas novas sem derivação; `[DERIVED]` usado sem derivação. Melhor: C8 (corte no lenteamento do CMB em ℓ < 30), que cai na variância cósmica (lê-se abaixo). Melhor pista: C17 (dualidade de distância) |
| D | teoremas do kernel com consequência nunca testada | 0 de 78 nomes específicos existem no kernel, inclusive quando ela escreve «não há nome inventado» |
| E, F1, G | enunciados reais dentro da pergunta | o melhor regime: admite `[OPEN]`, acha a lacuna certa, refuta a própria proposta. Ainda erra contas e inventa citações (G2) |

## Medidas da capacidade dela [REAL]

- **Memória de kernel:** 203 nomes distintos citados; 78 específicos (três palavras ou mais): **0** existem como identificador nas fontes `.lean` (10,8 M caracteres). Módulos reais: 2. `NOMES_CONFERIDOS.json`.
- **β escrito nas respostas:** {sum(len(v) for v in certos.values())} ocorrências por rodada corretas, {sum(len(v) for v in errados.values())} erradas (valores: {", ".join(sorted(errados)) or "nenhum"}). Medido por regex, só onde o número vem junto de β.
- **Sem resposta final:** {len(sem_resp)} rodadas gastaram os 12.000 tokens em raciocínio; o laço chegou a 841 linhas com 44 distintas.

## As três pistas, conferidas

**1. Distorções espectrais do CMB (FIRAS).** Não estava no Mapa nem no Atlas. Mas o fechamento ρ+p declara a hipótese de não-troca de energia entre setores, logo a TGL prevê μ = 0, igual ao ΛCDM. **Não discrimina; veta um ramo.** Se toda a resposta (4/3)β trocasse energia com os fótons na janela do μ, então μ ≈ {mu:.4f}, cerca de {mu / sig_mu:.0f}σ contra o limite |μ| < 4,7×10⁻⁵ a 95% (Bianchini & Fabbian 2022; σ aproximado pela metade do limite). A fração trocada permitida é < {100 * fr:.2f}%. Ganho real: a hipótese declarada ganha um teste externo publicado.

**2. Dualidade de distância (C17).** Não é nova: é a rota `discriminante.ordem018.f2.r_e` (η = f_L/f_A), parada porque o mapa físico entre luminosidade e ângulo não foi derivado. A forma com sirenes (D_L de GW contra D_A de EM) também depende desse mapa. A literatura de 2025–2026 está dividida sobre DESI DR2 + Pantheon+. O rival tem valor nulo exato, o que torna a rota valiosa, mas a TGL ainda não diz quanto vale η.

**3. N_eff.** Ela o citou de passagem (A3, F1). O canal é conhecido (v154, «linha de morte»), mas **não entrou nas buscas 5σ-01 nem 5σ-02**, e tem o que falta às outras: Modelo Padrão com valor fixo 3,044 e previsão sem parâmetro, N_eff = {pred:.4f}. Medida que não está nas fontes congeladas: Goldstein & Hill, arXiv:2603.13226 (v2, 20/03/2026) `[lido no HTML do arXiv]`:

| combinação | N_eff | TGL (σ do centro) | SM (σ do centro) | separação TGL–SM (σ) |
|---|---|---|---|---|
{linhas_n}

ΔN_eff < 0,107 a 95% (variantes: 0,0913; 0,116; 0,0876), com prior ΔN_eff > 0. O +{pred - 3.044:.4f} da TGL fica acima das quatro. A linha só de nucleossíntese é canal de fundo puro: a ressalva perturbativa (TGL-S contra TGL-L) não se aplica a ela. Para 5σ TGL–SM é preciso σ = {(pred - 3.044) / 5:.4f}; se o centro persistir, 5σ contra o fechamento ρ+p chega antes, com σ = {(pred - 2.990) / 5:.4f}. Abaixo da regra de TENSÃO do rito (3σ): o canal segue `TGL_NEFF_ARMED_CONSISTENT`, não gateia. Nada foi instalado: admitir a medida é a D8, e a linha de Y_p é a X16, ambas do operador.

## C8 conferida

Em ℓ = 2..29 há 896 modos: variância cósmica de 4,72% com céu inteiro e ruído zero. 5σ exigiria efeito ≥ 23,6%; ela estimou 0,5–1%. Regra geral: um efeito de tamanho β pede cerca de {modos:,.0f} modos independentes para 5σ, e a parede não é a contagem de modos, é a degenerescência com A_s, Ω_m, r_d (já medida na rota `bao_cmb.d10.degenerescencia_do_fundo`).

## Veredito

Nenhuma rota nova de 5σ. Isto é parede do modelo, não falsificação da teoria. O treino deu a ela vocabulário e disciplina de estatuto, não memória: a teoria não está nos pesos, e ela rende quando recebe os enunciados.
""".replace(",", ",")
(AQUI / "RELATORIO_SESSAO_5SIGMA_02nov.md").write_text(REL, encoding="utf-8")
print("relatorio", len(REL.encode("utf-8")), hashlib.sha256(REL.encode("utf-8")).hexdigest()[:16])
