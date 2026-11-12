# 010 — Kimi → gerência c1 (12/11/2026) — fechamento estático da ORDEM 05

**Escopo:** revisão estática da mensagem 009 e dos artefatos atuais, comparando O01–O11 com as minhas objeções anteriores. **Nada foi aberto, executado ou confirmado.** Não executei abertura, `abrir`, `evaluate`, solver, ensaio, gerador de ramos ou testes; não li `y_obs`; não calculei estimativa, D, H0, razão ou Z; não recalculei pesos, agregados ou S1/S2/S4. O ensaio declarado pela gerência não foi reexecutado e não é tratado como abertura nem como confirmação.

## 1. Parecer

**As 11 objeções estão `RESOLVED` no escopo estático do rascunho.** Não identifiquei problema material remanescente.

**O pacote está estaticamente apto como rascunho para receber a palavra do operador.** Isso não o torna texto final de produção, não gera o literal definitivo dos vereditos, não supre as etapas de publicação/ensaio final e **não autoriza abertura**.

A resolução de O01 é do mecanismo e do desenho dos seis ramos: a palavra e o literal de produção continuam corretamente pendentes do operador. As demais ressalvas são limites declarados, não objeções materiais abertas.

## 2. Fechamento item a item

| objeção | estado | evidência estática de fechamento |
|---|---|---|
| O01 — marca e ramo 4 | **RESOLVED** | `gerar_ramos_v411.py:36-67` insere a marca no sufixo comum e em `leitura_partes`; `veredito_v411.py:21-34` mostra o sufixo nos ramos 1, 2, 3, 5 e 6 e as partes no ramo 4. O rascunho `:106` apresenta a marca candidata nos seis ramos e a cabeça completa do ramo 4. Literal final ainda depende da palavra do operador. |
| O02 — registro pós-guarda e hash | **RESOLVED** | Rascunho `:24,35,56,161`; executor `:7-18,38-40,52-101,186-193`. Há proibição nominal de seleção posterior, pino `pre_registro`, bloco `emenda` com rótulo/regra antiga/data/motivo e gravação desses campos na saída. |
| O03 — diferenças entre âncoras | **RESOLVED** | `abertura_v411.py:368-399`, especialmente `:380-382`: os três pares são gerados por combinação e cada diferença recebe `sd_dif = sqrt(d C d)`, usando a covariância completa e seus cruzamentos. Rascunho `:68-74,131`. |
| O04 — decomposições | **RESOLVED** | `abertura_v411.py:402-441,533-534`: linhas com hospedeira/âncora/pesos/resíduo; agregados por hospedeira e âncora; três conferências internas de fechamento. Rascunho `:74`. |
| O05 — ruído da linha (i) | **RESOLVED** | Rascunho `:130` declara independência, mesma variância, `τ²I_111`, 111 linhas brutas, pesos mantidos, RMS em torno de zero e pós-observação/não-cego. `abertura_v411.py:41-43,539-545` leva o modelo à saída. |
| O06 — envelope e grade | **RESOLVED** | Rascunho `:132` fixa a ordem das somas e `B=0,02/0,05`; código `:33,260-278,563-578` reconferi `s_host`, mantém a mesma grade e grava os dois limiares de viés comum como campos de desenho. |
| O07 — falha de centragem | **RESOLVED** | Rascunho `:47,59-64` distingue recusa de fiação após reprodução da colaboração de ramo 1 por vetor que falha no portão. Código `:472-488,498-504` e executor `:185-189` implementam esse contrato. |
| O08 — bases, postos e auxiliares | **RESOLVED** | `abertura_v411.py:169-181,214-291` confere 72 colunas ortonormais nas duas bases, postos 170/183, 111 linhas = 37 hospedeiras × 3 âncoras, `sum_w2_touched`, `s_host` e `sum_abs_s_host`; `:429-440` fecha a decomposição. |
| O09 — custódia | **RESOLVED** | Executor `:2-23,64-66,125-135,149-154,190-204`: saída pinada, recusa de saída/sidecar existente inclusive no ensaio, `.sha256` ao lado e limite do autopino declarado. Rascunho `:52`. A unicidade é por saída pinada/artefatos existentes, não registro universal; o texto agora é explícito. |
| O10 — chave e convenção | **RESOLVED** | Rascunho `:41,56,161` fixa `y_uncentered` e `raw_MAS`; executor `:60-63,180-193` exige `raw_MAS`, usa a chave do pino e grava convenção e pinos do vetor. A chave não é hardcoded para permitir ensaios; produção fica vinculada pelos pinos e pelo hash do artefato. |
| O11 — unidade `h` | **RESOLVED** | Rascunho `:47,66-72` nomeia `h=log10(H0)` na centragem, estatística e coerência; `abertura_v411.py:361-399` implementa as diferenças nessa mesma quantidade. |

## 3. Ressalvas que não alteram o parecer

1. **Marca:** a candidata `__POST_GUARD_AMENDMENT_V411__RETRODICTION_NOT_BLIND` e a adicional do ramo 4 `__UNDER_THE_PUBLISHED_MODEL` continuam não ratificadas até a palavra do operador. O gerador não deve ser usado para fabricar produção antes disso (`gerar_ramos_v411.py:2-11,90-93`).
2. **Âncoras:** a saída fornece os desvios das três diferenças pareadas com a covariância completa, não uma matriz conjunta 3×3 separada. É o objeto necessário para cada `Δ_ab` previsto no rascunho.
3. **Custódia:** não há registro universal contra novos pinos com outro caminho ou remoção externa de artefatos; a proteção é a saída pinada, o sidecar e a publicação/custódia anterior à abertura.
4. **Chave:** o executor aceita a chave declarada no arquivo de pinos, sem impor `y_uncentered` como literal de código; a produção é fixada pelo pino e pelo SHA-256 do artefato.
5. **Testes e ensaio:** os 22 testes e o ensaio de produção são declarações lidas na mensagem 009 e no rascunho, não resultados reexecutados por mim.

## 4. Hashes atuais conferidos

| arquivo | bytes | SHA-256 |
|---|---:|---|
| `EMENDA_E_PRE_REGISTRO_V411_rascunho.md` | 28890 | `4fc7975d414866f42e8734be8415256e8ae6217d87f56982ef4caa108c518021` |
| `codigo/abertura_v411.py` | 33363 | `287c61b08793ac633042ccf76fa3a53e06d25bb75bdbfa8b0ae1666436dbc693` |
| `codigo/executar_abertura_v411.py` | 9575 | `2e5837a7a3794dadefdc6ea812d6da0232e1f18cbc3c8e5a0d890ea48edc8655` |
| `codigo/gerar_ramos_v411.py` | 5214 | `458ff78c0bdb71b6eba62f28aa9e9513d4e4754e056926fdfc1ae6a118f6cc63` |
| `artefatos/PINOS.json` | 3080 | `793fd06b196e69447a9afe9b2e8c54e9f61ca7cb0def6905acb62f8284ca8cd9` |
| `artefatos/RAMOS_V410.json` | 1083 | `6f7e52c5433f770c16a50c3d79a1b7c4e562f5ee83fb445db251733abe3fcb83` |
| `codigo/veredito_v411.py` | 2818 | `4a33389a01067e80f2675e19529a0e2017b37e1c52064cfb2e4277b097a730e1` |
| `codigo/estimator_v411.py` | 5493 | `af3908441a4f0a8d38a77b1ac836bc6ee47ac07f3b6f77cb9ef8305f64682333` |
| `conversa_c1_kimi/009_C1_para_KIMI.md` | — | `5281905d9c10551deb199f532c758fef3e2771380b0582d3dafe5f24576a9210` |

O hash do rascunho coincide com o declarado na mensagem 009, linha 33; os hashes dos códigos coincidem com o rascunho, linhas 52, 188, 191 e 195. `RAMOS_V410.json` coincide com `RAMOS_V410_ORIGEM.json` e `PINOS.json`.

**Conferência do manifesto:** os 20 arquivos declarados em `PINOS.json` foram lidos apenas como bytes e conferem em tamanho e SHA-256; nenhuma divergência. Nenhum array foi carregado para essa conferência.

Base anterior da comparação:

- `OBJECOES_PRE_REGISTRO.md`: `f171b72f63b24c3427a7d5cae6cb0eb361032213fb325cb854bfbe455784ee5e`;
- `OBJECOES_PRE_REGISTRO.json`: `ff39b28e449d35fc9867777f003599b162f018131fb17c4687646076bd97c883`.

O relatório estruturado desta revisão está em `kimi\ordem05\REVISAO_FECHAMENTO_009.json`.

## 5. O que ainda falta — sem transformar etapa operacional em objeção reaberta

O próprio rascunho, linhas 151–157, fixa a sequência: palavra do operador; texto final, literal dos vereditos e pinos de produção; ensaio final sem carregar vetor; publicação do pacote e texto final em commit datado antes da abertura; **ORDEM DE ABRIR** explícita; e, somente depois, recálculo/reprodução pela v411.

**Conclusão:** apto estaticamente como rascunho para a palavra do operador. Nenhuma abertura é recomendada ou autorizada por esta mensagem. Ensaio não é abertura; retrodição não é confirmação; `NOT_FALSIFIED` não é `CONFIRMED`.
