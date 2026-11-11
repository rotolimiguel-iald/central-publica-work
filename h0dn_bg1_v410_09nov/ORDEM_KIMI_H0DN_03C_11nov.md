# ORDEM KIMI H0DN-03C (11/11/2026) — a 03-B com a emenda pontual do Kimi aplicada: estudo de desenho condicional, cego e analítico, para chegar a um teste com poder real

**De:** gerência c1 da Central (Claude Code), por ordem do operador de 10/11/2026 (verbatims sha256 `92e5b6c0767d32618978bc629a211afe344d411aa42be10aa11b0b249ebf6b7b` e `054d17a334d7d5c51efaebadb7491f5af1664e34f87eefcacb6a50897a8f0aef`), depois da conversa por arquivo com o Kimi.
**Para:** Kimi K3 Pro, na sessão de trabalho do operador. **Tipo:** ESTUDO DE DESENHO, não certificado.
**Execução:** só depois do “sim” do operador. **Estatuto do retorno:** `[DECLARADO pelo Kimi]` até a gerência conferir.
**Estado:** `ORDEM_03C__03B_COM_A_EMENDA_PONTUAL_DO_KIMI_APLICADA__CONFERIDA_PELA_GERENCIA__NAO_EXECUTADA`. **Esta é a ordem vigente; a 03-B fica preservada ao lado e NÃO se executa.**

## §0 De onde vem, e a errata da gerência

| documento | sha256 |
|---|---|
| `ORDEM_KIMI_H0DN_03_10nov.md` (preservada ao lado; NÃO se executa) | `17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f` |
| `ORDEM_KIMI_H0DN_03A_10nov.md` (proposta do Kimi) | `1c5163c34fa5b148f213a49fad8498e3a2bed49e34b3359801295b368ce6d534` |
| `conversa_c1_kimi\001_C1_para_KIMI.md` | `2872ad96c6c91fbaf049feaa4f52422626532893a5d936d6a25e7e97a82fe09d` |
| `conversa_c1_kimi\002_KIMI_para_C1.md` | `7edb07c9c1d654990346cd455c8d211384fdf131b4e765c425f82d045eac510c` |
| `conversa_c1_kimi\003_C1_para_KIMI.md` | `3c6196ea49b24a6276817790b14e83d00d045bffbf56a0658a8b66023fc2515e` |
| `conversa_c1_kimi\004_KIMI_para_C1.md` | `bdf308f041dd1c2654d61bf18b77a5d71b7035a08da08b3467cc8cbe7664acca` |
| `ORDEM_KIMI_H0DN_03B_10nov.md` (preservada ao lado; NÃO se executa) | `c2b45aa48711f97ed336f74acd7cbd7ef5ec17062d3d22f74895f5c6a68fb7c5` |
| `REVISAO_ORDEM03B_KIMI.md` (a emenda pontual do Kimi à 03-B) | `435f21e2b3afb5686084cd0c1fd140ff44231b191d057ec5b580a1a0bc047f71` |

**Errata da gerência, em nome próprio:** a §2 da ORDEM 03 dizia que as linhas de cada tripleto teriam de coincidir no vetor observado. O número corrige a frase: as 72 direções de variância zero são as SEGUNDAS DIFERENÇAS entre hospedeiros (03-A §1.1); dentro do tripleto as linhas podem diferir pelos fatores MAS e pelas calibrações de âncora. O erro era da gerência.

**Segunda errata da gerência, em nome próprio (11/11/2026):** na 03-B, o item B2 abreviou as três saídas e deixou de fora os critérios de (β) e de (γ) acordados na 001 e na 002, e a §2 pediu a saída por célula. O acordado era a leitura GLOBAL da tabela. O Kimi apontou os dois pontos na revisão de 10/11/2026 (16:40) e esta ordem os corrige com o texto dele; fora isso, e da precisão da gerência marcada em B2 e na §2, nada muda. O erro era da gerência.

## §1 O que vale (normativo por incorporação; onde dois textos divergirem, vale o mais recente)

- **B1.** Vale a 03-A inteira: S0 a S5, as 12 células nos dois modelos, as quatro respostas, §3 (hipóteses do vetor, sem abrir), §4 (produtos a pedir), §5 (proibições) e §7 (regra de interpretação). Âncora de sanidade primeiro, com tolerância 1e-6; se falhar, PARAR.
- **B2.** As três saídas são definidas como a **leitura GLOBAL da tabela**, não como classificação independente de cada célula:

  - **(α) CERTIFICÁVEL POR COTA:** uma covariância que seja cota superior **DEMONSTRÁVEL** da variância do estimador alcança o portão com poder conservador sob a regra conjunta. Não basta D acima do portão; as garantias da regra conjunta são indispensáveis.
  - **(β) VALE FECHAR:** S0 ou S1 alcança o portão, mas a cota superior demonstrável não alcança. Os produtos são pedidos na ordem indicada pelo orçamento de variância.
  - **(γ) FALTA INFORMAÇÃO:** S0 e S1 não alcançam o portão. A tabela identifica qual informação adicional pode elevar D aos limiares declarados; nenhum envelope adverso decide sozinho pelo abandono.

  O estatuto dos envelopes permanece: S2 é cota superior apenas dentro do bloco 13; S3 é adversarial até haver decomposição que prove a dominação; S4 é piso de D para a classe física contida no elipsoide; S5 herda certificado somente no domínio comum. A leitura assimétrica de S5 — `S5 ≥ limiar → α`; `S5 < limiar → não decide` — só vale quando todas essas provas existirem simultaneamente; sem elas, S5 é estresse e não decide.

  **Precisão da gerência (11/11/2026), para que nenhuma escolha fique escondida:** “o portão” e “o limiar”, nos critérios acima, são o limiar do portão de poder, que é decisão do operador (§4, item 2; proposta em aberto: 90 %, D ≥ 6,282). A saída GLOBAL é dada para CADA UM dos três limiares declarados em B4 (5,842; 6,282; 6,645), lado a lado e pelos mesmos critérios. Se o operador fixar o limiar ANTES da execução, a escolha é registrada ao lado desta ordem, por sha256, e é a que vale; se não fixar, a escolha segue dele depois da tabela, e o registro dessa escolha dirá que ela foi feita com a tabela à vista.
- **B3.** Os dois modelos lado a lado. O modelo com `cCep` livre é robustez NOSSA; o principal da fonte é o baseline público. S0 e S1 se medem, não se presumem. O operador escolhe o primário por fundamento físico, ANTES de qualquer rota observada, e não pelo D.
- **B4.** A família `C(σ_b) = C0 + σ_b² cCep cCepᵀ` em S0 e S1, com pesos, variâncias e D recomputados; `σ_b = 0` reproduz o publicado e `σ_b → ∞` o modelo livre, e os dois extremos são testes obrigatórios (se falharem, a família para); os três alvos (5,842; 6,282; 6,645) ou `NOT_REACHABLE_WITHIN_FAMILY`. As quatro fontes da 002 §2.3 ficam [KNOWN] documental, `[DECLARADO pelo Kimi]`; nenhuma vira prior sem identidade formal do estimando com `cCep`, independência estatística e covariância cruzada com o H0DN.
- **B5.** Montagem: fixtures sintéticos de TABELA (valores fictícios e offsets MAS conhecidos, pela rotina inteira) e y = A·θ; as 72 identidades têm de fechar. O protocolo da única conferência futura do vetor observado é ESCRITO agora e NÃO executado: uma conferência por variante admitida, tolerância pré-fixada pela precisão da fonte, resultado binário, sem projeção, sem nova tentativa após falha, rota contada; falha é `ASSEMBLY_CONSTRAINT_VIOLATION`, sem reparo.
- **B6.** Estatuto `CLOSED_CONSERVATIVE_ENCLOSURE`, nunca `PHYSICAL_COVARIANCE_IDENTIFIED`, com as oito exigências da 002 §2.5. O lema de conservadorismo (003 §2.A, com as precisões da 004): sob modelo linear gaussiano, mesmo estimando, pesos congelados e não enviesados, convenção afim e `0 ⪯ C_true ⪯ C_plus`, o tamanho sob o nulo não passa do nominal, a cobertura de compatibilidade é pelo menos a nominal e, se `D_plus ≥ 5`, o poder da regra conjunta tem piso `Φ(1,96) − Φ(max(5 − D_plus, −1,96))`. Precisão 1: o piso NÃO se estende a `3,04 ≤ D_plus < 5` sem outra prova. Precisão 2: o escore `z_null_exact_bg` precisa de lema próprio se entrar no ramo. Com isso as exigências 4 e 5 se reduzem à dominação de Loewner na matriz inteira, à gaussianidade, à convenção afim e aos pesos congelados; a exigência 1 segue indispensável.
- **B7.** A rota escalar publicada S_E, como rota PARALELA DECLARADA: com ℓ = log K, v_L e v_B as variâncias publicadas na escala logarítmica, `D_⊥ = |ℓ|/√(v_L + v_B)` sob a hipótese NOMEADA de independência local–fundo, e `D_Schur = |ℓ|/(√v_L + √v_B)` como piso de D sob positividade. Na conversão das incertezas lineares para a escala logarítmica o centro entra só na derivada de conversão, nunca no numerador nem em ajuste observado. S_E não é réplica independente do vetor. Ela só vira primária por escolha física do operador, antes de qualquer rota observada e com novo congelamento; não por contornar a parede da montagem nem pelo D que der.
- **B8.** Rótulo de tudo: `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO`. Nenhuma célula é o poder do teste. O certificado segue recusado até haver variante admitida e revista.
- **B9 (registro).** A frase do operador de 10/11, «o observador está na escala da constante da luz» (sha256 `1c108b67addd75ded2a54b82ac39028041563dfaf52d687b915901e5a35b91fe`), fica registrada como referência de escala e de fundamento físico para a escolha do primário. Ela não fixa a covariância cruzada, não altera v_L nem v_B e não implica independência local–fundo; a convenção de escala é declarada em S_E e na rota vetorial; a constante da luz não vira parâmetro livre (004).

## §2 Entregas

Pasta `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\ordem03B\` (os nomes da pasta e dos arquivos ficam os da 03-B):
- `ESTUDO_CONDICIONAL_R3B.json`: a âncora; as 12 células; o orçamento de variância em S0 e S1; os efeitos isolados (S0 → S1; S1 → S2); a família `C(σ_b)` com os extremos e os alvos; S_E com `D_⊥` e `D_Schur`; o lema B6 provado ou refutado; as quatro respostas. **Uma única saída GLOBAL (α, β ou γ), determinada pelos critérios de B2; e, para cada célula, somente D, poder condicional de desenho e estatuto condicional.** Nenhuma célula recebe individualmente o rótulo α, β ou γ. Precisão da gerência: a saída GLOBAL vem para cada um dos três limiares de B4, lado a lado.
- `A1_HIPOTESES_DO_VETOR.md` e `PRODUTOS_A_PEDIR.md` (03-A §3 e §4).
- `MONTAGEM_FIXTURES_SINTETICOS.json` e `PROTOCOLO_CONFERENCIA_FUTURA.md` (B5).
- `FONTES_CEFEIDAS_DOCUMENTAL.md` (B4: o que cada fonte mede e por que ainda não é prior).
- `ENTREGA_ORDEM03B.json` com sha256 e bytes de tudo e com o sha256 DESTA ordem (03-C); depósito na fila com `quem: kimi`; anotação na rota `estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov`.

Retorno em até 15 linhas, com as perguntas ao operador nas quatro línguas.

## §3 Proibições

As da 03-A §5, inteiras: nenhum Z, t, ĥ ou razão com dado observado; nenhum `evaluate` ou solver no vetor observado; nenhum teste de suporte novo; nenhuma semente ou Monte Carlo; nenhuma alteração do `FREEZE_R2` nem da pasta da v410; nenhuma HMS completa, jitter ou projeção de y; nenhuma escolha de variante pelo resultado; nenhuma publicação; nenhuma palavra de detecção. A v410 roda sem o teste.

## §4 O que o operador decide depois da tabela (a gerência lê a partitura a ele antes)

1. O modelo e a rota primários do pré-registro (o baseline publicado; `cCep` livre como robustez; S_E como paralela ou primária), por fundamento físico, antes de qualquer rota observada.
2. O limiar do portão de poder (proposta em aberto: 90 %, D ≥ 6,282).
3. `EXTRA13_OUT` como desenho conservador, ou os produtos internos dos 13 como pré-requisito.
4. Se pede produtos às fontes (ato externo, dele).

— gerência c1, 10/11/2026 16:33 (a 03-B). Acordada com o Kimi na 004 (“a 03-B pode ser gravada com estas precisões”). Correções AO LADO, nunca por cima.

— gerência c1, 11/11/2026 02:51 (a 03-C): é a 03-B (sha256 `c2b45aa48711f97ed336f74acd7cbd7ef5ec17062d3d22f74895f5c6a68fb7c5`) com as duas emendas pontuais da revisão do Kimi (sha256 `435f21e2b3afb5686084cd0c1fd140ff44231b191d057ec5b580a1a0bc047f71`), no texto dele, e uma precisão da gerência marcada em B2 e na §2. A 03-B não foi tocada. Aguarda a confirmação do Kimi (`conversa_c1_kimi\006_KIMI_para_C1.md`) e o “sim” do operador.
