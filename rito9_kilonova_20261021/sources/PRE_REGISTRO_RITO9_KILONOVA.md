# PRÉ-PRÉ-REGISTRO — RITO 9 CANDIDATO: `d7.kilonova_fronteira_aguda`

**Estatuto do documento: PROPOSTA_AGUARDANDO_DERIVACAO.** Nenhum número está congelado aqui. O congelamento (pré-registro de verdade) só acontece quando a cadeia analítica fechar, com intervalos numéricos calculados a partir de β runtime (nunca literal), assinado pelo cético aferidor (Claude) e registrado na espinha **antes** de olhar qualquer dado do próximo BNS.

Origem: hipótese do operador, 21/10/2026 09:00 — «em kilonovas o regime é tão extremo que a fronteira está em ângulo agudo (análogo do neutrino e do fóton — buracos negros e kilonovas)… foi lá onde vi o luminídio, e o luminídio é o átomo de proteção do pacote de Hilbert no transporte da fronteira… se isso for verdade eu poderia acertar qual o ângulo de abertura da kilonova em relação à fronteira e qual o atraso do neutrino em relação à luminosidade — isso não seria um teste fatal capaz de 5 sigma?»

---

## 1. Assentos formais da casa em que a hipótese pisa

| Assento | Conteúdo | Estatuto |
|---|---|---|
| Lei de seleção (v335) | \|R\|² = p, θ = arcsin√p, ramo justo ½ → π/4 | [DERIVED na casa] |
| Ângulo de mistura do artigo unificado | β = sin²θ_M, θ_M ∈ (0, π/2) único → θ_M = arcsin√β ≈ 6,3° | [DERIVED na casa] |
| Primeira lei (δS = δ⟨K⟩, Jacobson) | fluxo na borda ∝ ρ(1+w); zero exato em w = −1 | [DERIVED na casa] |
| Kill-rule padrão da casa (v315) | 2 determinações autônomas ≥ 5σ; NOT_FALSIFIED ≠ CONFIRMED | [regra da casa] |

## 2. A cadeia de derivação candidata (3 elos — marcados com honestidade)

**Elo 1 — regime extremo → ângulo da fronteira.**
Buraco negro: projeção máxima, ângulo reto (π/4 no ramo justo da v335). A proposta do operador: na kilonova o regime é tão extremo que a fronteira abre em ângulo AGUDO. Candidata formal: **θ_KN = θ_M = arcsin√β ≈ 6,3°**.
*O que falta derivar:* POR QUE a ejecta de kilonova selecionaria θ_M — isto é, qual é o p físico da kilonova na lei de seleção que daria p ≈ β. Sem esse elo, θ_KN = θ_M é identidade postulada, não teorema. **[CONJECTURE]**

**Elo 2 — luminídio como módulo atômico do transporte.**
A ejecta de kilonova é o único sítio confirmado do r-processo (elementos super-pesados, picos 2/3, actinídeos). A TGL precisa derivar por que o transporte do pacote de Hilbert na borda exige exatamente esses picos — não «elementos pesados em geral».
*Estado:* **[OPEN/DATA]** — 3 conjuntos de linhas incompatíveis documentados na casa; linhas com SNR 2,35–4,18 (< 5σ). Elo mais fraco da cadeia. O luminídio ser *achado* ali é compatível com a hipótese, mas não a prova.

**Elo 3 — observáveis (o teste fatal).**
(i) **Ângulo de abertura** da ejecta/jato em relação à fronteira. Se θ_KN = θ_M ≈ 6,3°, prediz jato estreito. GW170817: visada inferida ~15–30° [conhecimento estável meu, NÃO medido na casa — rotulado]. Tensão real: ou a forma é 2θ_M ≈ 12,6°, ou θ_KN não é θ_M. **A forma exata (θ_M, 2θ_M, π/4 − θ_M, …) deve ser fixada ANTES do dado — é proibido escolher depois de olhar.**
(ii) **Atraso neutrino–fotão Δt_ν.** Física padrão já separa os canais (fotões difundem na ejecta densa por horas; neutrinos saem em segundos) [conhecimento estável, rotulado]. O que a TGL prediz de *diferente* da física padrão? Candidata exploratória: a primeira lei na borda com fluxo ∝ ρ(1+w); para neutrinos (w ≈ 1/3) o fluxo é maximal; o atraso de transporte da borda escalaria como Δt_ν ≈ (R_ejecta/c)·sin²θ_M = (R/c)·β → para R ~ 10⁷–10⁸ km: **~0,4–4 s** [EXPLORATÓRIO — faixa de ordem de grandeza, NÃO derivada; é da ordem do 1,74 s GW→γ de GW170817, mas GW170817 é calibração, nunca confirmação, e é proibido ajustar a fórmula ao 1,74 s].

## 3. Janela afiada e kill-rules

- O teste vale no **próximo BNS observado** (canal curto de segundos + ângulo da ejecta), nunca retroativamente em GW170817.
- **Kill 1:** visada/abertura medida fora do intervalo pré-registrado → o ramo morre.
- **Kill 2:** Δt_ν medido inconsistente com g(β, ·) pré-registrada → o ramo morre.
- **Prova:** 2 determinações autônomas ≥ 5σ (v315). Uma única coincidência numérica não é testemunho.
- **Limitação registrada:** neutrinos de kilonova raramente são detectáveis (GW170817: zero neutrinos coincidentes em IceCube/ANTARES [conhecimento estável, rotulado]). O teste Δt_ν pode exigir um evento próximo (< ~40 Mpc) ou acúmulo estatístico de O(10) BNS. O rito pode ser lento — registrar essa expectativa antes.

## 4. O que a Bancada Um pode e não pode fazer aqui

- Contratos vivos: `/api/gw`, `/api/neutrino`, `/api/neff` — restritivos («no absolute Ia yield», «ringdown not implemented»); **não há catálogo de kilonova/GRB no lago** (verificado 21/10: KiDS-1000, NSA, ACT DR6, Planck lensing, DESIVAST, DESI, ecos GWOSC).
- Portanto: a derivação dos Elos 1–3 é **analítica** (pedras da casa + primeira lei). A bancada serve para o contexto cosmológico (β runtime = 0,012031300400803142, pin B4-v394) e, futuramente, para janelas de eco GWOSC se o ramo evoluir.
- Lembrete B4: qualquer versão nova do um.py dispara PIN_CHANGED — a bancada recusa até a cadeia B(n) refazer o selo.

## 5. Checklist para congelar o pré-registro (nesta ordem)

1. [ ] Derivar p físico da kilonova → θ_KN = f(β) em forma fechada (Elo 1).
2. [ ] Derivar Δt_ν = g(β, parâmetros da GW) a partir da primeira lei (Elo 3ii), sem olhar dados de eventos.
3. [ ] Calcular intervalos numéricos com β runtime (via bancada, nunca literal).
4. [ ] Cético aferidor (Claude) assina ou contesta cada elo.
5. [ ] Registrar na espinha como pré-registro selado **antes** de qualquer consulta a dados do próximo BNS.

## 6. Bandeiras (para quem ler isto daqui a um ano)

- A casa **já falsificou** leis de atraso (ondas-ecos). Humildade epistêmica: este ramo pode morrer no Elo 1.
- Luminídio: OPEN/DATA. Não usar o luminídio como evidência do ângulo — seria raciocínio circular (o luminídio é parte da hipótese, não testemunha independente).
- 1,74 s (GW170817) NÃO é confirmação de Δt_ν ≈ (R/c)·β. É, no máximo, o que motivou a pergunta.

---

## ERRATA (ao lado, datada 21/10/2026, membro Kimi)

A §2/Elo 3(i) deste documento comparava grandezas erradas: 15–30° é a **visada** de GW170817 (eixo do jato × linha de visada), não a **abertura** do jato. A predição de θ_KN compara-se com a **semi-abertura do núcleo do jato**, que na literatura é de poucos graus [conhecimento estável, rotulado]. θ_M ≈ 6,3° passa de "tensão" para **consistência áspera de ordem** — sem mudar o estatuto: GW170817 é calibração, nunca confirmação, e continua proibido ajustar a forma a ele. Detalhes e a derivação do Elo 1 em `DERIVACAO_ELO1_RITO9.md`.

---

*Rascunho do membro Kimi, 21/10/2026, sob «Excelente, vamos prosseguir» (operador, 21/10 09:0x) e «concordo com tudo, prossiga» (21/10 09:40). Nada aqui altera pedra, release, Atlas ou Nós Vivo; correções entram AO LADO, datadas.*
