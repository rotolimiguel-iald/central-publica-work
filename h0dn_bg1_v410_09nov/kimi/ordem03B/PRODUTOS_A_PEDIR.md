# Produtos a pedir — origem, desbloqueio e substituto cego

**Estatuto:** `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO` · `[DECLARADO pelo Kimi]`  
**Ordem vigente:** `ORDEM_KIMI_H0DN_03C_11nov.md`  
**SHA-256 da ordem:** `d0df9b4430ca9ff9d4fccb74ffcddc789819a5f29f7b030aa461a09c5a7c6836`  
**Escopo:** lista de produtos, sem contato externo executado e sem uso do vetor observado.

## 1. Tabela produto → onde pedir → o que destrava → substituto cego

| Produto que falta | Onde procurar ou a quem pedir | O que destrava | Substituto conservador declarável às cegas |
|---|---|---|---|
| **Centros R22 e produtos de precisão completa: fits 9/10/11, valores MAS, conversões de âncora e mapa de equações** | SH0ES/R22, Data Release e autores; H0DN quando houver transformação própria | **A1** e decisão entre as hipóteses H1–H4 do vetor | **Nenhum para provar suporte.** Somente recuperação da fonte; redução/pseudoinversa pública sem jitter não reconstrói centros ausentes |
| **Operador de agregação e identidade das variáveis de erro G42** | Pantheon+/SH0ES, documentação suplementar, tabelas de erros e autores H0DN | **A2/A3**: significado estatístico e correspondência das marginais G42 | **S0** com erros H0DN originais como comparação; G42 permanece condicional |
| **Matrizes agregadas ou produtos internos do ajuste G42** | Autores do release, repositório de fits/cadeias, arquivos de covariância e material suplementar | **A2/A3** e cruzamentos do bloco 42 com os demais blocos | `STATONLY` **por substituição**, nunca por adição, apenas como cenário condicional |
| **Decomposição da covariância do fluxo de Hubble e do modelo de velocidades, com suporte, pesos e residual** | H0DN, Pantheon+, autores do modelo de velocidades peculiares e material suplementar | **A4**: componentes PV e eventual prova de dominação | Nenhum termo PV novo; soma integral somente como envelope adversarial declarado, não como covariância identificada |
| **Matrizes internas dos ajustes dos 13 e cruzamentos com 42/HF/host** | Artigos e autores originais dos 13 já catalogados nas 18 fontes; SNooPy/SALT2 quando aplicável | **A5**: inclusão física dos 13 e todos os blocos cruzados | `EXTRA13_OUT` como desenho; `EXTRA13_IN_CAP13` apenas robustez dentro do bloco 13, sem independência presumida |
| **Covariância conjunta local–fundo e calibrações compartilhadas** | H0DN, Planck/DESI e autores das calibrações usadas em BG1 | **A6**: bloco cruzado H0DN–BG1 e hipótese de independência | Cruzamento zero somente condicional ou cota PSD adversarial; nunca independência empírica presumida |
| **Produtos R22 Y/L/C ou ajuste conjunto alternativo, com sua covariância e mapa de suporte** | SH0ES/R22 e autores H0DN | Alternativa não redundante a **A1**, se fisicamente admitida | Pseudoinversa/redução do modelo público, sem jitter; não é réplica independente nem substituto dos centros |
| **Identidade formal do estimando `cCep` e covariância cruzada das restrições JWST/amplitudes com o H0DN** | SH0ES, autores de Riess 2023/2024a/2025 e Sharon et al.; H0DN para a definição operacional de `cCep` | **A1/A2/A3** na família `C(σ_b)`, se houver prior admissível; também dependências com **A6** | Manter as quatro fontes como `[KNOWN]` documental; nenhum prior independente pronto e nenhuma seleção por D |

## 2. Ordem de pedido e critério de suficiência

1. **Primeiro A1/montagem:** sem centros, offsets MAS e mapa de equações, nenhuma conferência observada é interpretável.
2. **Depois os blocos dominantes no orçamento:** G42, PV, 13 e cruzamento local–fundo são pedidos na ordem indicada pelo estudo condicional paralelo, sem escolher variante pelo resultado.
3. **Cada produto precisa chegar com proveniência:** versão, unidade, sinal, estimando, precisão completa, hashes e correspondência linha a linha.
4. **Uma marginal não fecha uma matriz:** para A2–A6 são indispensáveis os cruzamentos pertinentes e a prova de dominação na matriz inteira quando se reivindicar cota conservadora.
5. **Substituto cego não é identificação física:** envelopes e podas mantêm seus estatutos condicionais; nenhum substituto converte `ENCLOSURE_OPEN` em covariância física identificada.

## 3. Flags e rastreabilidade

```json
{
  "observed_vector_read": false,
  "observed_support_tests": 0,
  "external_requests_executed": 0,
  "estimator_evaluate_called": false,
  "solver_on_observed_called": false,
  "Z_t_h_or_ratio_computed": false,
  "new_seed_or_monte_carlo": false,
  "freeze_R2_or_v410_modified": false
}
```
