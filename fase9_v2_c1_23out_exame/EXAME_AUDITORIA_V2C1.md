# AUDITORIA INDEPENDENTE (C08) antes do congelamento — Fase 9 V2-c1 «O Teste da Única Palavra» (gerência c1, modelo forte, 23/10/2026)

**Objeto.** `C:\IALD\Central de Patentes\work\fase9_v2_c1_23out`:
- spec `46b329d8c86e96b3`, cuja forma canônica é `c9f9fec83d10dd4f`;
- função `383961aa796d68b5`;
- registro D-H `3e25ac3431c62887`;
- runner E1–E5, S5, calibração de cauda e trava;
- fontes L1b `302b0a42572723e7` e L6 `1b728822339026c4`.

A base de comparação é a R5.2-E1 `81a970926345832a`, no túnel (`ORDEM_019\F3.1`), que só foi lida.

**O que NÃO fiz.** Não abri o dado observado. Não calculei o composto observado da V2, não rodei o modo observado com recibos e não emiti recibo nenhum.

**Onde escrevi.** Só nesta pasta. Os testes rodaram numa cópia byte a byte do pacote (`copia_pacote\`). O original segue intocado: `diff -rq` só aponta o `RESULTADO_TESTES.json` da cópia, regravado pelos testes. O `conferir_consistencia.py` do original dá 10 de 10 OK. Não foi escrito nenhum `__pycache__` no pacote nem na Bancada.

## VEREDITO: PODE_CONGELAR

Não há achado ALTO nem MÉDIO; há 6 BAIXAS (§8).
- B1 e B6 se corrigem sem tocar nenhum byte pinado.
- As outras ficam opcionais, para esta ou para a próxima versão.

## (1) A spec e a função contra a R5.2 [REAL; `cmp_spec_funcao.py`, `CMP_SPEC_FUNCAO.json`, `diff_campos.py`, `DIFF_CAMPOS_R52_V2C1.json`]

**A spec.** Comparei as seções em JSON canônico:
- 7 novas, 3 removidas e 17 alteradas, exatamente as do `DIFF_R52_PARA_V2C1.md`, cada uma atribuída;
- 19 iguais, entre elas `lei` (K congelado), `covariancia`, `fundos`, `gate`, `beta`, `poder_previo` e `hipoteses`;
- os 8 leitores têm o mesmo H0 e o mesmo σ da R5.2.

**As folhas numéricas que mudaram** são só estas: `n_alvos` passa de 2 a 0, e entram as tolerâncias novas do `runner_contract` (BG1 0,01, que já existia, σ 0,005, quadratura 1e-6, extração 1e-9, recibo 1%, poder 0,002).

**A função.** O AST é idêntico, salvo o nome, a docstring e a base do token. As constantes numéricas são iguais: {0, 0,01, 1, 2, 3, 5}. A ordem de precedência não muda.

**A única mudança de semântica** é que z_δ e z_disc entram CALIBRADOS (`entrada_calibrada`, C1-CAL, G01). Está declarada.

## (2) A extração dos 8 leitores [REAL; `verificar_extracao.py`, `VERIFICACAO_EXTRACAO.json`]

- Os 8 sha256 e os tamanhos em bytes conferem nos três lugares: disco, registro D-H e spec.
- Cada regra pinada casa uma única vez e devolve o declarado a 1e-9; o declarado é igual na V2 e na R5.2.

**As fontes baixadas são as certas:**
- **L1b** = arXiv:2509.01667, Riess, Li, Anand +8, 01/09/2025, «The Perfect Host…», com 73,49 ± 0,93.
- **L6** = arXiv:2509.04348 (LVK, GWTC-4.0), v1 de 04/09/2025, com 76,6 (+13,0/−9,5) e σ médio 11,25. A v3, que dá 75,4, fica ao lado e não é admitida (G04).

## (3) E1–E2 [REAL; `reproduzir_fundo_bg1.py`, `REPRODUCAO_FUNDO_BG1.json`]

Rodei de novo o fornecedor REAL (`BANCADA_REAL`: Planck comprimido + DESI DR2, nenhum H0 local), pelo módulo pinado:
- H0 = 68,53106 e σ = 0,30140 (Δ = 6,4e-05 e 4,0e-04), em 4,9 s;
- o resultado é bit a bit igual ao da qualificação;
- os 7 pinos da Bancada são iguais aos do pedido.

**A divergência interrompe** (`BackgroundError`, sem calibrar) nos três casos: H0 + 0,011, σ + 0,006 e NaN.

## (4) A calibração de cauda `sup_caixa` [REAL; `verificar_calibracao.py`, `VERIFICACAO_CALIBRACAO.json`]

- **O recibo.** Os limiares vivos são iguais aos do recibo: 3,7986 e 6,3705 para z_δ; 1,3032 e 4,9833 para z_disc.
- **Não há vazamento de centro.** Com os H0 dos leitores trocados por NaN, por 1000 ou por 0, limiares e τ ficam idênticos. A calibração só usa σ, a caixa e o fundo.
- **τ_f_sup recomputado à mão** pelos 4 cantos da caixa (a variância é linear em λ) mais V_T = g'Cθg dá 1,09645, igual ao recibo. O pior caso é (1,1); o ponto de análise é (0,0).
- **O mapa z_δ(u) é monótono.** Por isso p_cal_sup é uma cota superior válida, e conservadora, para toda covariância da caixa.
- **O mapeamento confere.** O bruto 6,3705 dá p = 5,7329e-07, igual a 2Φ(−5) = 5,7330e-07, e corresponde a z_cal 5,000004. O bruto 5 corresponde a 3,942.
- **MC próprio.** São 20.000 sorteios pelo pipeline completo, com outra semente, sob a nula TGL e covariância verdadeira (1,1). Nos limiares brutos 2, 3, 3,8 e 5 deram 2273/2282, 371/356, 48/54 e 2/1,6 contra o analítico (z de Poisson −0,2, +0,8, −0,8 e +0,3).

## (5) A trava [REAL; leitura do código, mais `SONDAS_TRAVA.json` sobre pacotes SINTÉTICOS]

**Ordem do código.** `check_freeze` e `check_opening_act` vêm antes de tudo:
- antes de qualquer número, do fundo e de qualquer saída;
- `ALVOS_FASE9_LIDOS.json` em qualquer lugar da árvore recusa;
- o cofre retira os H0 antes do PODER, e `CAL.primary_thresholds` só lê σ.

**Minhas 6 sondas recusam todas, sem calcular o fundo nem gravar nada:**
- ato de auditoria falso: `FREEZE_ACT_MISSING`;
- `quem` vazio: `OPENING_ACT_INVALID`;
- sem abertura: `OPENING_ACT_MISSING`;
- sem congelamento: `FREEZE_RECEIPT_MISSING`;
- ALVOS numa subpasta das fontes: `MANUAL_TARGET_LEDGER`;
- congelamento trocado depois da abertura: `OPENING_ACT_INVALID`.

**Pacote válido.** Contei os `open` por caminho: cada fonte é aberta uma vez, e o PODER é gravado antes de `CENTERS_UNSEALED`. No REAL, o PDF compartilhado por L4_5 e L4_6 é lido duas vezes, ambas no `check_freeze` e ambas conferidas.

## (6) Os 48 testes e os controles negativos [REAL; `testes_na_copia.out`]

Na cópia deu **48/48 em 35,8 s**, incluindo o E20: o modo observado na cópia, sem recibos, recusa sem ler nada.

O harness é sólido:
- `refuses` exige o código exato;
- o `ExplodingProvider` prova que o fundo não foi chamado antes da recusa;
- nenhuma saída sobra depois de uma recusa.

**Exceção (B1).** Em `run_tests.py:448` (D5), a asserção da palavra proibida termina em `or True` e não morde. O token vem da função pinada, cujas strings não contêm a palavra; por isso o risco real é nulo.

## (7) β, palavra proibida, escritas [REAL; varreduras por script]

- **β e α.** Não há literal de β, α ou √e no código. A spec traz `alpha_read` e `beta_runtime` herdados da R5.2 (seção `beta` inalterada), só como pino de conferência. O β do runner é `ALPHA_FINE_CODATA_2018 × √e`, com o α lido do um.py instalado.
- **A palavra proibida** não aparece em nenhum token de veredito. Aparece só na frase da régua, «NOT_FALSIFIED nunca é CONFIRMED»: nas docstrings, no AVISO e na `leitura` do resultado, e no texto da spec (B2).
- **Escritas.** Todas são relativas à raiz do pacote ou a `testes/_tmp`; os caminhos absolutos são só de leitura (R5.2, fala do operador, um.py, Bancada).

## (8) Achados BAIXOS

- **B1.** Tirar o `or True` de `run_tests.py:448`, ou aplicar a guarda do um.py a todo campo «veredito». Não toca byte pinado.
- **B2.** Se a casa preferir não escrever a palavra nem no texto (como fez a v396), trocar por «NOT_FALSIFIED nunca é creditação».
- **B3.** `mapa_z_delta_monotono` é só gravado. Sugiro recusar se for False (fail-closed); hoje é True.
- **B4.** Recusa depois da abertura (E3, `ExtractionError`, `VerdictLoadError`) não grava registro, e as duas últimas não viram código REFUSE no `main`. Não há guarda de abertura única (rodar duas vezes gera dois resultados determinísticos). Sugiro um registro de recusa e recusar se já existir `saidas/RESULTADO_*`.
- **B5.** `constantes_E_conferem_com_um_py` (S5) é só gravado, sem cobrança; o efeito do S5 é desprezível.
- **B6.** Os pinos cobrem os `.py`, mas não o `__pycache__`, e `emitir_recibo_*` sem `-B` grava `.pyc` em `runner/`. É benigno, mas convém pôr `-B` nos comandos do pedido. Não toca byte pinado.

**Custos já declarados** (G01/G02, decisão da gerência; não são defeito): com `sup_caixa`, P(FALSIFIED | ΛCDM) fica em 43–47%, e P(FALSIFIED | TGL) em 0%. A regra de dispersão dá 9–20% de INCONCLUSIVE com dados consistentes.
