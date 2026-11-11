# ORDEM KIMI H0DN-03 (10/11/2026) — Estudo de desenho CONDICIONAL, às cegas e analítico: o H0DN × BG1 pode alcançar poder real? E a lista do que pedir e a quem

**De:** gerência c1 da Central (Claude Code), pela ordem vigente do operador de 10/11 (verbatim sha256 `122e85b43994d6c0a186d63f0a65f54b786c1f6bcbb9b72387b3afaa1f613a96`: dar ao Kimi o comando do que falta para um teste com poder preditivo discriminante real).
**Para:** Kimi K3 Pro. **Tipo:** ESTUDO DE DESENHO, não certificado. Sem dado observado, sem Monte Carlo, sem semente, sem abertura.
**Estatuto do que você devolver:** `[DECLARADO pelo Kimi]` até a gerência conferir.

## §0 O que a gerência leu da sua entrega da ORDEM 02 (vale como está)

Hashes conferidos. Veredito `COVARIANCE_NOT_CLOSABLE_FROM_PUBLIC_SOURCES`; nenhuma variante admitida; D conservador nulo; poder não avaliável. A1 fechado por álgebra (37 tripletos de hospedeira R22: 111 linhas, posto 39, nulidade 72; 183 medidas distintas). A2/A3 condicionais; A4 e A6 abertos; os 13 em `OPEN_NO_TRANSPLANT`. Decisão do operador: a v410 roda SEM o teste; o teste fica para a v411. A recusa de certificar está certa e fica. O que falta é saber se VALE A PENA fechar: se nem no melhor cenário declarado o desenho alcança poder real, o caminho é outro.

## §1 O estudo condicional (tudo declarado ANTES de qualquer número; nada aqui é covariância física admitida)

1. **Âncora de sanidade (obrigatória, primeiro):** com a covariância publicada tratada pela sua redução de A1 (183 medidas, ou pseudoinversa no suporte), reproduza por conta analítica os dois D do `FREEZE_R2`: 6,823355 (modelo publicado) e 5,316944 (viés diferencial das Cefeidas livre). Se não reproduzir, PARE e diga por quê: sem a âncora a tabela não vale.
2. **Cenários condicionais, fixados agora:**
   - S1: A1 reduzida + G42 STATONLY por substituição + velocidade peculiar como o H0DN já a herda (nenhum termo novo) + EXTRA13_OUT + bloco cruzado zero.
   - S2: como S1, com EXTRA13_IN_CAP13 no lugar de EXTRA13_OUT.
   - S3: como S1, mais a componente pública de velocidade peculiar somada por inteiro (cota superior da duplicação).
   - S4: como S1, com o bloco cruzado H0DN–BG1 na cota conjunta que MINIMIZA D (a sua condição c^T S_BG^{-1} c ≤ V_L).
   - S5: a pior combinação de S2, S3 e S4.
   Cada cenário nos dois modelos (publicado; viés Cefeida livre). Dez células.
3. **O que calcular, só por álgebra:** a variância GLS do estimador na convenção do `FREEZE_R2` e o D de K = 1,0838071748529643 contra 1, por célula; o orçamento de variância (B3 da ORDEM 02) em S1; e para cada célula o poder Φ(D − 5).
4. **As três respostas que a tabela tem de dar:** (a) alguma célula com o viés Cefeida livre alcança D ≥ 6,282? (b) qual bloco domina a perda de S1 para S5? (c) quanto os 13 calibradores valem em D (S1 contra S2)?
5. **Rótulo de tudo:** `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO`. Nenhuma célula é «o poder do teste». O certificado continua recusado até haver variante admitida.

## §2 A1 e o vetor observado, sem executar

Se as 72 direções são redundâncias exatas, as linhas de cada tripleto têm de coincidir no vetor observado. O `y_obs` de 09/11 tinha projeção de até 0,0931 mag nessas direções, muito acima de arredondamento. Entregue, SEM abrir nem recalcular nada sobre o vetor: as hipóteses que explicam a diferença, em ordem de plausibilidade pela fonte (centros por âncora; produtos de precisão completa; convenção de montagem; linhas que não são a mesma medida), e para cada uma o produto público que a decide.

## §3 O que pedir, e a quem

Uma tabela: produto que falta (matrizes internas dos ajustes dos 13; decomposição por componente da covariância do fluxo de Hubble e do modelo de velocidades; identidade das variáveis de erro do G42; produtos R22 de precisão completa; covariância conjunta local–fundo) → onde pode estar publicado ou a quem pedir (grupo, repositório, material suplementar) → o que cada um destrava (A1 a A6) → se há substituto conservador declarável às cegas.

## §4 Proibições e entrega

Como na ORDEM 02: nenhum Z com dado observado, nenhum `evaluate` ou solver no vetor observado, nenhum teste de suporte novo, nenhuma semente, `FREEZE_R2` e a pasta da v410 intocados, nada de «5σ», «confirmado» ou «detectado», nenhuma publicação. Pasta `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\ordem03\`: `ESTUDO_CONDICIONAL_R3.json` (âncora, as dez células, orçamento, as três respostas), `A1_HIPOTESES_DO_VETOR.md`, `PRODUTOS_A_PEDIR.md`, `ENTREGA_ORDEM03.json` com sha256. Depósito na fila com `quem: kimi`; anotação na rota `estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov`. Retorno em até 15 linhas, com as perguntas ao operador nas quatro línguas.

## §5 O que o operador ainda decide (você já perguntou; fica registrado)

O limiar do portão de poder (proposta: 90 %, D conservador ≥ 6,282) e se admite a poda cega EXTRA13_OUT como desenho conservador ou exige primeiro os produtos internos dos 13. A sua tabela é o que ele precisa para decidir.

— gerência c1, 10/11/2026. Correções AO LADO, nunca por cima.
