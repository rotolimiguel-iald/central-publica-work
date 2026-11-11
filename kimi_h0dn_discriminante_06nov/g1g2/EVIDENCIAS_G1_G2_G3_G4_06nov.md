# Evidências G1–G4 — agregação, identificadores, covariância e prova de afixação

**Data:** 06/11/2026  
**Estado:** `G1_DERIVED_STRONG_CANDIDATE` · `G2_CLOSED_IDENTITY_AND_PROVENANCE` · `G3_OPEN` · `G4_OPEN` · `AFIXACAO_TEMPORAL_R1_COMPILED`

## 1. Resposta executiva

- A agregação SH0ES encontrada é a **média aritmética das curvas de cada SN**, não uma média inversa da variância.
- Os dois aliases foram validados por identificador canônico, coordenadas e redshift: `2008fv_comb = 2008fv` e `1994DRichmond = 1994D`.
- Os demais objetos foram separados por proveniência; nenhum ID foi adivinhado por semelhança nominal.
- A pedra `AfixacaoTemporalR1` compilou com **13 teoremas**, todos no trio `{propext, Classical.choice, Quot.sound}`, sem `sorryAx`.
- A decomposição física da covariância e a abertura observada continuam bloqueadas. As novas sensibilidades mostram que o poder pode cair muito se a ponte G42 for aplicada sem separar Cepheid, dispersão intrínseca e PV.

## 2. G1 — agregação aritmética

Foram testados GLS completo, GLS estatístico, pesos diagonais e erros brutos. Nenhum reproduziu as incertezas publicadas. Em seguida, a comparação direta com o vetor SH0ES mostrou que

\[
m_{0,i}=\frac1{m_i}\sum_{j=1}^{m_i}y_{ij},
\]

para cada SN com \(m_i\) curvas.

Resultados:

- 42 calibradores R22: 25 com múltiplas curvas e 17 com uma;
- as 25 agregações R22 com múltiplas curvas reproduzem `m0_Bi` dentro de **0,0005 mag**;
- a 26ª combinação, `2007on`, não pertence a `IS_CALIBRATOR=1` e não foi admitida na ponte;
- os pesos são constantes por SN, \(w_{ij}=1/m_i\), e não foram escolhidos para melhorar poder;
- a normalização é agora teorema Lean: `arithmeticAggregate_one` e `arithmeticAggregate_const`.

A matriz `G` foi construída com 42 linhas e pesos \(1/m_i\). Todas as 42 entradas têm `IS_CALIBRATOR=1`.

**Limite:** a confirmação documental da regra e a revisão independente da sequência continuam necessárias antes de marcar G1 como fechado no freeze. A força do resultado é numérica e reproduzível, não licença para ignorar a proveniência.

Evidências:

- `G1_ARITHMETIC_CANDIDATE.json` — SHA-256 `1f5f0b5da10533a73823ba8af862049b020397f81c59001018564731734ef40e`;
- `g42_aggregation_covariance.npz` — matriz G, covariâncias agregadas e cruzamentos;
- `G1_G42_COVARIANCE_SCENARIOS.json` — SHA-256 `2a70a91fce557ba2eccc2f3c87de4ff55d3203cc961604be32cdbc5f1e2916fd`.

## 3. G2 — identidade e proveniência

### Alias fechados

- `2008fv_comb`: linha 123 do release, `IS_CALIBRATOR=1`; o catálogo canônico `all_redshifts_PVs.csv` registra `2008fv` em NGC 3147 com as mesmas coordenadas e redshifts dentro da precisão publicada.
- `1994DRichmond`: linha 4 do release; o catálogo canônico registra `1994D` em NGC 4526 com coordenadas e redshifts coincidentes. A proveniência fotométrica é Richmond et al. 1995.

### Proveniência separada

- `2011iv`, `2007on`, `1980N`, `1981D`, `2006dd` e `1992A` têm linhas no release, mas `IS_CALIBRATOR=0`; não pertencem ao conjunto R22.
- `1989B` e `1998bu` estão no catálogo de redshifts, mas foram consideradas excessivamente avermelhadas para a amostra Cepheid de 2022.
- `2021rhu`, `ASASSN-14lp`, `2021J` e `2020nvb` não aparecem no arquivo de distâncias nem no catálogo de redshifts consultado; têm fontes observacionais independentes e não podem receber covariância de objetos semelhantes.

**Resultado:** G2 fica fechado como identidade/proveniência. A covariância dos 13 adicionais permanece fora da ponte R22 e exige suas fontes originais ou sensibilidade pré-registrada.

Artefato: `G2_IDS_PROVENIENCIA_RESOLVIDA.json`  
SHA-256: `725a6f53ebc9754f2347d0a6f486e9c4523bb046d6d49d0c3f970cb56a4fe873`.

## 4. G3 — decomposição física ainda aberta

A ponte G42 permite calcular `G C Gᵀ` e a covariância com o intercepto comprimido do fluxo. Entretanto:

- `STAT+SYS` inclui covariância Cepheid e pode duplicar informação já presente na rede;
- `STATONLY` contém componentes de dispersão intrínseca que também precisam ser reconciliados com o tratamento H0DN;
- os 13 calibradores adicionais continuam com suas incertezas diagonais publicadas, sem ponte física própria;
- a variância de velocidade adicionada pela H0DN precisa ser auditada contra o fluxo já covariante.

Portanto, as figuras abaixo são **sensibilidades, não covariância física admitida nem falsificação**.

### Sensibilidades lineares analíticas, sem novos dados ou sementes

| Componente G42 | Modelo | \(D\) | Rejeição isolada | Evento conjunto |
|---|---|---:|---:|---:|
| `STAT+SYS` | Publicado basal | 5,758612 | 77,5958% | 75,0958% |
| `STAT+SYS` | Cepheid livre | 4,970269 | 48,8141% | 46,3141% |
| `STATONLY` | Publicado basal | 5,818101 | 79,3350% | 76,8350% |
| `STATONLY` | Cepheid livre | 4,995079 | 49,8037% | 47,3037% |
| `VPEC` | Publicado basal | 5,919632 | 82,1117% | 79,6117% |
| `VPEC` | Cepheid livre | 5,030701 | 51,2246% | 48,7246% |

A interpretação correta é que o poder da rota é sensível à ponte de covariância. Não se pode escolher o cenário mais favorável, nem declarar a TGL falsificada pelo mais desfavorável.

## 5. G4 — geometria, sem freeze

Os três cenários passaram pela guarda geométrica da R2:

- posto da covariância 183, nulidade 72;
- desenho e coluna Cepheid no suporte;
- sem diagonalização ou ridge;
- influência e dimensões verificadas.

Isso valida a execução matemática dos cenários, **não a covariância física final**. G4 permanece aberto até a decomposição e a revisão independente.

## 6. Pedra de afixação temporal

Arquivo: `../provas/AfixacaoTemporalR1.lean`.

Os 13 teoremas provam:

1. a informação do sistema não depende da marca clássica;
2. o controle `n=0` devolve a entrada;
3. a travessia devolve exatamente o canal original;
4. os detectores não mudam ao somar a marca temporal;
5. a completeza das Kraus preserva o traço;
6. a marca de travessia preserva peso um sob entrada normalizada;
7. o controle conserva a normalização;
8. a marca lê o próprio setor;
9. o outro setor não é revelado;
10. preparo e travessia são registros distintos antes do detector;
11. \(J^2=I\) não é um contador absoluto;
12. os pesos da média aritmética somam um;
13. a média de uma constante é a própria constante.

**Limites:** a pedra não implementa o aparelho, não mede o rival óptico, não fixa \(P,Q\) na natureza e não prova uma nova CPTP experimental. É um contrato algébrico por setores clássicos, não uma dilatação tensorial nova.

Recibo: `../provas/AfixacaoTemporalR1_receipt.json`  
Fonte SHA-256: `6e0623a8d122e20095a773e76b28a4ec4e1ccb51ca64d558b9d05edb34845dda`  
Log SHA-256: `f0b657d1227ac6aac7ece25850c7ecccb8f3814ba14c93311194b56cb0e0ee9b`.

## 7. Decisão de abertura

`opening_allowed = false`.

G1 é uma candidata forte derivada; G2 está documentalmente resolvido; G3/G4 não estão fechados. A regra R3 não pode abrir dados observados, e nenhum cenário G42 substitui a covariância exigida pelo pré-registro.
