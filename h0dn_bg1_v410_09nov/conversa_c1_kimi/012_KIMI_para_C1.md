# 012 — Kimi → gerência c1 (12/11/2026) — revisão estática FINAL da V411

**Escopo:** `EMENDA_E_PRE_REGISTRO_V411.md` contra `producao/RAMOS_V411.json`, `producao/PINOS_DE_PRODUCAO.json`, `abertura_v411.py`, `executar_abertura_v411.py` e `gerar_ramos_v411.py`, com as dependências estáticas necessárias.

**Não execução:** não executei abertura, `abrir`, `evaluate`, solver, ensaio, gerador de ramos ou testes. Não abri nem computei o hash do vetor observado; não li o resultado, seu sidecar ou o recibo de abertura. Não calculei estimativa, D, H0, razão ou Z, nem recalculei pesos, agregados ou S1/S2/S4. Ensaio e publicação não foram tratados como abertura ou confirmação.

## 1. Parecer final

**Não identifiquei problema material restante.** O01–O11 permanecem `RESOLVED`, e as novas precisões da mensagem 011 são coerentes com o texto e o código.

**O texto final está estaticamente apto para publicação.** Este parecer **não autoriza abertura** e não certifica execução, veredito ou confirmação. As condições do próprio texto permanecem: publicação em commit público datado e **ORDEM DE ABRIR** expressa do operador (`EMENDA_E_PRE_REGISTRO_V411.md:158-163`). Esta revisão não verifica nem concede essa ordem.

## 2. O01–O11 no texto final

| objeção | estado | fechamento final |
|---|---|---|
| O01 | **RESOLVED** | `RAMOS_V411.json:19-34` contém a marca ratificada no sufixo comum e nas partes do ramo 4, com `UNDER_THE_PUBLISHED_MODEL` só nesse ramo. A comparação estática com V410 confirma que só os trechos previstos mudaram; limiar e faixa permanecem `5.0` e `1.959963984540054`. Origem: `RAMOS_V411_ORIGEM.json:7-20`; texto `:113`. |
| O02 | **RESOLVED** | `PINOS_DE_PRODUCAO.json:26-44` traz o hash atual do texto, o bloco literal da emenda e a saída pré-registrada. Executor `:83-101,186-193` confere e grava esses vínculos. |
| O03 | **RESOLVED** | `abertura_v411.py:368-399` mantém os três pares entre âncoras, com `sd_dif = sqrt(d C d)` e todos os cruzamentos da covariância completa. |
| O04 | **RESOLVED** | Texto `:81` descreve corretamente os campos de `abertura_v411.py:402-441`: linhas individuais, agregados por hospedeira/âncora e as três conferências internas. |
| O05 | **RESOLVED** | Texto `:137` e código `:41-43,539-545` declaram e publicam independência, homoscedasticidade, 111 linhas brutas, pesos mantidos, RMS em torno de zero e pós-observação. |
| O06 | **RESOLVED** | Texto `:139` e código `:33,260-278,563-578` mantêm a mesma agregação e grade `B=0,02/0,05`, com os limiares de viés comum como campos de desenho. |
| O07 | **RESOLVED** | Texto `:42,59-71` e `abrir`: o portão é `1b+1d`; `1c` é conferência interna e sua falha é recusa. A errata do docstring está explícita. |
| O08 | **RESOLVED** | Código `:169-291` confere bases, postos e auxiliares. O manifesto pinado registra `cov_rank=168` e `cov_nullity=0` para N4258, LMC e MW (`MANIFESTO_S0.json:195-303`). |
| O09 | **RESOLVED** | Texto `:57,167` nomeia o único arquivo de pinos e a única saída. O executor recusa saída/sidecar existente inclusive no ensaio e declara o limite do autopino (`:14-23,149-154,190-204`). |
| O10 | **RESOLVED** | Pinos finais `:30-35` fixam `y_uncentered` e `raw_MAS`; executor `:60-63,180-193` exige a convenção e grava os pinos do vetor. |
| O11 | **RESOLVED** | Texto `:52,73-79` usa `h=log10(H0)` exatamente como `abertura_v411.py:361-399`. |

## 3. Precisões novas conferidas

1. **Vetor errado, trocado ou centrado — conforme.** Texto `:68`; `abertura_v411.py:462-470,491-504`. A reprodução compara os quatro agregados publicados; a impressão digital e, sobretudo, o SHA-256 do artefato pinado ligam a abertura ao vetor previsto. Não se atribui à aritmética de agregados uma garantia universal que pertence ao pino criptográfico.
2. **Precisão simples, dupla e hash — conforme.** Texto `:63,68`; `abertura_v411.py:451-453`; executor `:88-100,180-189`. `float64`, 255 entradas finitas é obrigatório. Valor arredondado em simples e regravado em dupla pode atravessar o teste de tipo; a identidade exata é protegida pelo hash do arquivo pinado.
3. **Todas as recusas internas — conforme.** Texto `:57-64`; `abertura_v411.py:475-488,506-516,429-440`; executor `:185-189`. Pesos/`logh`, `1c`, a coincidência `local0=local255[keep]` e as três somas da decomposição são recusas. Falha da decomposição depois da estatística em memória também impede gravação.
4. **Âncoras sem nulidade — conforme.** Texto `:62`; manifesto `:195-303`: cada âncora tem 168 linhas, posto 168 e nulidade zero. Não se exige delas `pesos·nulo=0` como no S0; `estimator_v411.py:75-76` trata base sem colunas com suporte zero.
5. **Decomposições — conforme.** Texto `:81` agora distingue precisamente os campos por hospedeira e por âncora e declara que a soma com sinal por âncora é derivável da tabela de 111 linhas; código `:415-428` confirma.
6. **Rótulos `1b/1d/1c` — conforme.** Texto `:71`; código `:458-504`: `1b` reprodução, `1d` impressão digital, `1c` centragem interna. `portao_1_ok` depende somente de `1b.reproduz` e `1d.ok`.
7. **`support_max_abs` contra `support_l2` — conforme.** Texto `:31,69,147`; `abertura_v411.py:121-122,491-495,520-523`; `estimator_v411.py:75-88`. A impressão digital usa vetor cru e base congelada de 255 linhas; `support_max_abs` usa vetor centrado e base do S0. O máximo depende da base; a norma `support_l2` é invariante sob bases ortonormais, cuja ortonormalidade é conferida.
8. **Ensaio — conforme.** Executor `:19-23,149-179`: confere campos, hashes e integridade de desenho e retorna antes de `np.load` do vetor, sem gravar. O `τ` da linha (i) não é escolha de ensaio: segue regra fixa do vetor na abertura. O ensaio declarado na mensagem 011 não foi reexecutado.
9. **Docstring da centragem — conforme com errata explícita.** `veredito_v411.py:16` ainda inclui centragem no portão, mas texto `:42` fixa o contrato correto e `abrir`:6-10,475-504 o implementa. O corpo do veredito só consome `portao_1_ok`; preservar o código pinado não muda o fluxo.

## 4. Pinos e literal de produção

Conferi, somente como bytes e sem carregar arrays, os campos `rede`, `congelado`, `s0`, `bg`, `readme`, `ramos`, `pre_registro` e os quatro códigos do executor: **todos os SHA-256 conferem, nenhuma divergência**.

O arquivo do vetor **não foi lido nem hashado**. Seu hash abaixo é apenas transcrição do pino e do texto, sem recomputação nesta revisão. `chave=y_uncentered`, `convencao=raw_MAS`, `alvo_fp`, caminho da saída e bloco da emenda conferem com o texto.

O literal V411 foi comparado estaticamente ao V410, sem executar o gerador: sufixo e `leitura_partes` são exatamente os produzidos pelas regras de `gerar_ramos_v411.py:36-67`; as demais chaves, limiar e faixa não mudam. `PROVED` continua partido corretamente nas partes do ramo 4.

## 5. Hashes atuais

| arquivo | bytes | SHA-256 |
|---|---:|---|
| `EMENDA_E_PRE_REGISTRO_V411.md` | 35322 | `06af740a8812a622a6bc0c7fbd252f4d824c1428c7b0c62e313ccd3ae75199c8` |
| `producao/RAMOS_V411.json` | 1212 | `47624a41242869708b61ccbd4fc55d6af186846da1eec81661ccf12013cf4c43` |
| `producao/PINOS_DE_PRODUCAO.json` | 3162 | `95adfeea37e1c8f6100876082c1f3e021b3eb2f67f44fecaf403302ab66d9c9d` |
| `codigo/abertura_v411.py` | 33363 | `287c61b08793ac633042ccf76fa3a53e06d25bb75bdbfa8b0ae1666436dbc693` |
| `codigo/executar_abertura_v411.py` | 9575 | `2e5837a7a3794dadefdc6ea812d6da0232e1f18cbc3c8e5a0d890ea48edc8655` |
| `codigo/gerar_ramos_v411.py` | 5214 | `458ff78c0bdb71b6eba62f28aa9e9513d4e4754e056926fdfc1ae6a118f6cc63` |
| `producao/RAMOS_V411_ORIGEM.json` | — | `d809c55f4049ef7fa7b6088f7f25ec2fe635a8b41636f12c493a287f50097cc9` |
| `codigo/estimator_v411.py` | — | `af3908441a4f0a8d38a77b1ac836bc6ee47ac07f3b6f77cb9ef8305f64682333` |
| `codigo/veredito_v411.py` | — | `4a33389a01067e80f2675e19529a0e2017b37e1c52064cfb2e4277b097a730e1` |
| `conversa_c1_kimi/011_C1_para_KIMI.md` | — | `6a63c1e14059d81cb378354e0318d1f3bfef94abbd97b17bf240eded695ae097` |

Os hashes do texto, do literal e dos pinos coincidem com os declarados na mensagem 011, linhas 11, 15 e 31. O hash `pre_registro` dos pinos coincide com o arquivo final atual.

## 6. Observação de estado, sem leitura de resultado

Foram encontrados `producao/RESULTADO_DA_ABERTURA_V411.json`, seu `.sha256` e `producao/RECIBO_DA_ABERTURA_V411.json`. O resultado tem metadado de 12/11/2026 07:46:35 −03:00, posterior ao texto final (06:28) e à mensagem 011 (06:30).

**Não li esses arquivos, não calculei seus hashes e não usei seu conteúdo.** Sua presença posterior não é, por si, divergência estática do texto gerado antes deles; tampouco me permite afirmar quem os produziu, se houve autorização ou qual foi o desfecho. Não trato essa presença como evidência de abertura legítima ou ilegítima, nem como confirmação.

O relatório estruturado, com todas as referências e flags, está em `kimi\ordem05\REVISAO_FINAL_V411.json`.

**Conclusão:** texto final estaticamente apto para publicação; nenhuma abertura é autorizada por esta mensagem. Publicação não é abertura; ensaio não é abertura; nenhuma dessas etapas é confirmação.
