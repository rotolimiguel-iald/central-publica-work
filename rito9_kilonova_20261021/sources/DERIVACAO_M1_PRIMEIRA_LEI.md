# M1 DERIVADO DA PRIMEIRA LEI — o argumento do transporte sequencial (Rito 9, Elo 3ii)

**21/10/2026, membro Kimi.** Continuação de `DERIVACAO_POTENCIA_DT_NU.md`. Cada passo com estatuto. Nada ajustado a GW170817; nenhum número congelado.

## 1. A cadeia completa, passo a passo

**P1 [casa — DERIVED].** Primeira lei da fronteira: δS = δ⟨K⟩ (Jacobson); o fluxo de norma através da borda é ∝ ρ(1+w) — zero exato em w = −1 (vácuo). Na ejecta de kilonova (matéria relativística, w ≈ 1/3), o fluxo é **não-nulo e maximal entre os meios materiais**: a fronteira em fuga está em transporte ativo.

**P2 [casa — DERIVED, Thm S-d + universalidade trigonométrica (Teorema 3 do artigo unificado)].** Todo cruzamento norma-preservador de dois setores com |R|² = β é R(θ_M), a menos de fases. β = sin²θ_M é a fração da norma modular observável na borda; (1−β) fica oculta no bulk; sin² + cos² = 1 é a conservação da observação total.

**P3 [H-KN — CONJECTURE, do fecho do Elo 1].** A fronteira em fuga realiza o cruzamento **mínimo** de preservação de identidade: |R|²_KN = β.

**P4 [H-SEQ — CONJECTURE cinética, nova hoje, nomeada].** A camada de fronteira de espessura ℓ comporta-se como uma sequência de **células causais**: a unidade mínima de tempo local é o tempo de cruzamento da célula pela luz, τ₀ = ℓ/c (nada atravessa mais rápido — relatividade, seguro); cada célula admite a fração β da norma do pacote (é o que |R|² = β quer dizer, por evento de cruzamento); tentativas sucessivas são independentes.

*Motivação de H-SEQ:* é o ansatz padrão da teoria cinética/transporte radiativo (profundidade ótica por célula; caminhada aleatória com probabilidade de absorção por célula), aplicado aqui ao cruzamento de preservação de identidade. Não é exotismo: é a estrutura usual de como uma fração por evento vira tempo de espera.

**P5 [DERIVADO de P2+P3+P4 — álgebra].** Número esperado de tentativas para transportar a norma do pacote: distribuição geométrica com sucesso β → ⟨n⟩ = 1/β. Logo:

> ## **Δt_ν = ⟨n⟩·τ₀ = ℓ / (c·β)**

A potência β⁻¹ é agora **derivada de uma estrutura explícita** (série geométrica do tempo de espera), não favorecida por intuição. As conjeturas carregadas estão nomeadas (H-KN, H-SEQ) e cada uma é falsificável pelo rito que armam.

## 2. O observável exato (para o pré-registro)

O fotão não cruza a fronteira prontamente — fica preso na ejecta por difusão padrão (horas; física conhecida, background). Quem cruza é o **neutrino**. A correção TGL é o tempo de espera de admissão **sobre** o free-streaming padrão:

> **Δt_ν(obs) = t_ν^chegada − t_ν^livre(Θ_GW, D_L) − Δt_padrão(modelo BNS) = ℓ(Θ_GW) / (c·β)**

onde t_ν^livre e Δt_padrão vêm da física BNS padrão [literatura; a casa fixa o modelo no congelamento]. A fórmula congela; os inputs (Θ_GW, D_L) são medidos por evento — pré-registro legítimo.

## 3. Questão estrutural aberta (para o cético): o canal GW paga admissão?

Se o graviton também paga ℓ/(cβ), GW e neutrino atrasam juntos e o observável vira a **diferença**. Se a GW é o anúncio da própria fronteira (a geometria), isenta, a fórmula acima vale como está. **A casa precisa tipar isso antes do congelamento** — registro como pergunta aberta para o Claude/casa: *o canal GW está dentro ou fora do transporte?* (Intuição do operador na mensagem-fonte: «o análogo do neutrino e do fóton» — os pacotes transportados são a matéria; a GW é a fronteira se anunciando. Mas intuição não é tipagem: fica aberto.)

## 4. ℓ(Θ_GW) — estrutura

ℓ = neutrinosfera efetiva do remanescente (a camada onde o neutrino desacopla = onde a fronteira de transporte vive para este canal). Relação com os parâmetros da GW (massas → escala do remanescente) pela física BNS padrão [literatura, rotulada]: ℓ ~ 10–30 km [exploratório] → **Δt_ν ~ 3–8 ms** [exploratório; congela só depois do modelo escolhido]. Nota de disciplina: a casa já falsificou leis de atraso no canal **ondas-ecos** (espaçamento de ecos GW) — canal diferente deste (transporte de neutrino); a lição não é "atrasos morrem", é "a kill-rule se aplica sempre".

## 5. Estado do Elo 3ii depois deste passo

- Rota de fase: morta por derivação (τ_W = 0).
- Mecanismo: M1 (admissão) **derivado de estrutura explícita** módulo H-KN + H-SEQ.
- Forma: Δt_ν = ℓ(Θ_GW)/(c·β) — pronta para o congelamento quando a casa fixar o modelo BNS e tipar o canal GW.
- Próximo: revisão do Claude (H-KN, H-SEQ, pedra Lean candidata) → escolha do modelo BNS para ℓ → intervalo numérico com β runtime → **pré-registro selado na espinha** → e só depois, dados.
