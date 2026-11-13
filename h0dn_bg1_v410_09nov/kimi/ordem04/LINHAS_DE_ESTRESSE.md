# Linhas de estresse — publicar junto, sem certificado

**Estado:** `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO`  
**Fonte dos D:** `ESTUDO_CONDICIONAL_R3B.json`, SHA-256 `24d42026500d864d85685de6cb2825e873a4826bc7cd26c4d5e8128e635ed8e3`.  
**Escopo:** transcrição do estudo 03-C, sem novo cálculo e sem vetor observado.

## 1. Primário ratificado

O primário ratificado é **S0 publicado + EXTRA13_OUT**: modelo publicado com a covariância tratada por redução às 183 medidas ou pseudoinversa, os 13 fora, independência local–fundo como hipótese nomeada e portão de 90% (`D ≥ 6,282`) no S0 do modelo publicado. A primariedade decorre da **ratificação do operador**, não de uma seleção posterior pelo maior D. O modelo Cefeida livre acompanha o resultado de forma inseparável.

## 2. Linhas a publicar junto

| Linha de estresse | D publicado | D com Cefeida livre | Hipótese, em uma frase | Estatuto |
|---|---:|---:|---|---|
| **Cefeidas livres — S0, EXTRA13_OUT** | `6,710150598579069` | `5,191312010024399` | No S0 com EXTRA13_OUT, o viés diferencial das Cefeidas é deixado livre em vez de fixado no desenho publicado. | `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO` |
| **S1 — G42 STATONLY por substituição** | `5,489824585314922` | `4,7432683914542775` | O S0 é modificado pela substituição da covariância G42 pela STATONLY, nunca por adição. | `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO` |
| **S2 — EXTRA13_IN_CAP13** | `5,527886977528846` | `4,773510143639735` | O S1 passa a incluir os 13 com `C_13 → 13 diag(C_13)`, mantendo as demais entradas. | Condicional; cap interno hipotético, sem dominação demonstrada da matriz inteira. |
| **S4 — envelope analítico local–BG1** | `4,378058410058796` | `3,871969766287` | O S1 é submetido ao mínimo global analítico de D sob `q C_BG⁻¹ qᵀ ⪯ C_L`, com GLS recalculado. | Condicional; envelope adversarial cuja contenção na classe física não está provada. |

## 3. Por que estas linhas não são travas nem certificado

A Ordem 04 determina que Cefeidas livres, S1, S2 e S4 sejam publicadas como linhas de estresse e não como travas adicionais. O fecho da covariância física permanece **ABERTO**, mas deixa de ser usado pela gerência como barreira de abertura; a montagem A1, a conferência da variante, a revisão e o pré-registro continuam necessários.

Esses D medem desenho condicional, não resultado observado nem certificado conservador da regra conjunta. Não há dominação completa de Loewner, covariância física admitida e revisada ou prova de poder conservador. S2 estabelece apenas cap interno hipotético, e S4 é adversarial sem contenção física demonstrada; nenhum deles estabelece perda física.

S3 foi recusado porque a componente PV não é PSD, e S5 não foi calculado. **S3/S5 não aparecem como possibilidades de abertura nem como critério de abandono.**

## 4. Regime da ordem e flags

- O campo `opening_allowed=false` do estudo 03-C pertence ao regime anterior e não é apagado.
- A Ordem 04 retira o fecho físico como trava, mas **não autoriza a Etapa 2**: a conferência do vetor ainda exige manifesto completo, revisão e autorização explícita do operador.
- `observed_vector_read=false`; `observed_support_tests=0`; `D_H0_or_ratio_computed=false` nesta preparação; `new_seed_or_monte_carlo=false`; `freeze_R2_v410_or_gate_modified=false`.
