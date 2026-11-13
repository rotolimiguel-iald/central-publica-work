# H0DN × BG1 — a conferência independente da tabela de poder (11/11/2026; registro da gerência c1, AO LADO do desenho)

**Estado:** `CONFERENCIA_DE_DESENHO__ARITMETICA_CONFERE__NAO_VALIDA_A_FISICA`. Fica ao lado de `DESENHO_RATIFICADO_H0DN_11nov.md` (sha256 `c62858c238efea54fdbabe38e3983a8ac4415bf3070d5238b48223996bf1f6d4`), que não foi tocado.

**Quem fez:** um agente distinto do Kimi e da gerência, com código próprio (numpy), sem executar o código do Kimi. `[DECLARADO pelo agente]` quanto ao método; `[REAL]` quanto aos números abaixo, que a gerência leu do resultado dele por script e comparou com o estudo do Kimi (`ESTUDO_CONDICIONAL_R3B.json`, sha256 `24d42026500d864d85685de6cb2825e873a4826bc7cd26c4d5e8128e635ed8e3`).

## 1. Os quatro números

| o quê | recalculado | no estudo do Kimi | diferença |
|---|---|---|---|
| D do congelamento, modelo publicado | 6,823355474280 | 6,823355474280 | 1e-14 |
| D do congelamento, Cefeidas livres | 5,316943561403 | 5,316943561403 | 7e-15 |
| D do S0, modelo publicado | 6,710150598579 | 6,710150598579 | 5e-15 |
| D do S0, Cefeidas livres | 5,191312010024 | 5,191312010024 | 2e-14 |

Os quatro conferem dentro de 1e-6. O S0 é o desenho com os 13 calibradores fora, que é o desenho ratificado.

## 2. O que o agente relatou (`[DECLARADO pelo agente]`)

- **Fórmula:** mínimos quadrados generalizados na pseudoinversa da covariância, no suporte (posto 183 de 255 linhas no congelamento; posto 170 de 242 no S0); D = log10 K dividido pela raiz da soma da variância do estimador local com a do fundo.
- **Dupla contagem: não há no desenho.** A covariância local é exatamente a publicada, sem termo somado por cima, mais o bloco do fundo, com o bloco cruzado zero. Ressalva dele: se o erro por linha do próprio pacote publicado já embute o erro de âncora, a duplicação seria da colaboração; o desenho não decide isso.
- **O fundo BG1:** ΛCDM, Planck comprimido mais BAO do DESI DR2, 16 resíduos; sem supernovas, sem cronômetros, sem SH0ES.
- **log10 K = 0,034952021735181**, lido dos arquivos do congelamento; vem do pré-registro da Fase 9 V2, com zero parâmetro livre.

## 3. O que a conferência NÃO faz

- Não recalculou a covariância do fundo (pede o motor e os dados de Planck e DESI; só leu o recibo).
- A independência entre o local e o fundo e a gaussianidade são hipóteses do desenho, não medidas. K entra fixo, sem incerteza.
- É aritmética de desenho: não valida a física nem o orçamento de erros publicado.

## 4. Cegueira

O agente declarou não ter aberto `y_obs.npz` nem nenhum vetor observado, e a gerência conferiu que os scripts dele não os carregam. **Um incidente, dito:** ao ler o código do Kimi ele viu de passagem o agregado local PUBLICADO pela colaboração, que está escrito ali para uma derivada. É número público do artigo; o composto da casa (a razão, o Z) não foi calculado por ninguém.

## 5. Arquivos do agente (cópia de bytes em `conferencia_independente_11nov\`)

| arquivo | bytes | sha256 |
|---|---|---|
| `cmp_full.py` | 1118 | `5e913a6e3f9148cc76c524837a2c7fb87a37ce3afffa1aa5987967336a0e5f0b` |
| `conferir_D.py` | 5315 | `6533ffa3be0b6573b503b1265727b0b792c5f34c945b5596f7aa1e211af84030` |
| `conferir_estrutura_C.py` | 2183 | `ee6f2e0f77da477a99921492d9d7b1bd992062ddfd181bd77f7e3adfd06f983a` |
| `hms_diag.py` | 868 | `d0aa10d489632917f00d782496732adcf3cb543490b4dd61337e4755f30997d6` |
| `keys.py` | 292 | `41f24e917f25bcd88b7585455150cecfa624938374b0f6c34378c67f011d5d9e` |
| `resultado_D.json` | 1197 | `d3d85050853a75191da1c803940163f2c0acd63f225a5459b6ea7c2cbefe5637` |
| `rows_probe.py` | 548 | `2c5939f16de6857c346bd2beccf7c0b8ccc924b364e7fcd4d717ec45669180e4` |
