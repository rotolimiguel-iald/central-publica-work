# PROPOSTA ORDEM KIMI H0DN-03A (10/11/2026) — Estudo de desenho CONDICIONAL corrigido, cego e assistente: medir capacidade sem sufocá-la

**De:** Kimi K3 Pro, por autorização do operador para redigir a correção, sem executar o estudo.  
**Para:** gerência c1 da Central; depois Kimi K3 Pro, somente após conferência da gerência.  
**Tipo:** ESTUDO DE DESENHO, não certificado. **Esta proposta não foi executada.**  
**Estatuto:** `[DECLARADO pelo Kimi]` até a gerência conferir.  
**Estado:** `PROPOSTA_03A__AGUARDA_CONFERENCIA_DA_GERENCIA__NAO_EXECUTADA`.

**Documento original preservado ao lado:** `ORDEM_KIMI_H0DN_03_10nov.md`, SHA-256 `17e788be9dfaa8ad5cf2a2bfd7afc49a3924a96830626806deece811c553193f`. Esta 03-A não sobrescreve nem apaga a 03; corrige seus três pontos problemáticos e conserva sua parte útil.

## §0 O que permanece decidido e não será refeito

1. A entrega da ORDEM 02 vale como está: `COVARIANCE_NOT_CLOSABLE_FROM_PUBLIC_SOURCES`; nenhuma variante física completa admitida; D conservador nulo; poder não avaliável. **POWER_NOT_EVALUABLE não é UNDERPOWERED.**
2. A1 está algebricamente fechado: 37 tripletes de hospedeira R22, 111 linhas, posto 39, nulidade 72; 183 medidas distintas na rede. A redução/pseudoinversa preserva a informação pública; a HMS completa continua inadmitida.
3. A2/A3 são condicionais; A4 e A6 permanecem abertos; os 13 continuam `OPEN_NO_TRANSPLANT`.
4. A v410 segue sem o teste; qualquer possível abertura futura fica para outra versão, após covariância física admitida, poder certificado e revisão independente.
5. Nenhum D novo foi calculado para esta 03-A. A tabela futura serve para decidir **como e se vale a pena fechar**, não para declarar o poder do teste nem para selecionar o cenário mais agradável.

## §1 As três correções obrigatórias à ORDEM 03

### 1.1 Correção matemática das 72 identidades

**Está corrigida a frase segundo a qual as linhas de cada tripleto teriam de coincidir no vetor observado.** Elas não precisam ser iguais: podem diferir pelos fatores MAS e pelas calibrações de âncora.

Com `N = N4258`, `L = LMC`, `M = MW`, e o hospedeiro `0 = N7250` como referência, as 72 restrições são:

\[
(y_{k,N}-y_{k,L})-(y_{0,N}-y_{0,L})=0,
\qquad k=1,\ldots,36;
\]

\[
(y_{k,N}-y_{k,M})-(y_{0,N}-y_{0,M})=0,
\qquad k=1,\ldots,36.
\]

Uma diferença isolada entre âncoras do mesmo hospedeiro **não** é, em geral, uma direção nula, pois ainda contém os fatores MAS/âncora. São as segundas diferenças entre hospedeiros que têm variância zero.

Nenhuma futura montagem pode forçar igualdade dentro dos tripletes, projetar o vetor para satisfazer as restrições ou rejeitar dados válidos por essa diferença esperada.

### 1.2 Inclusão de S0 para separar efeitos

A ORDEM 03 alterava simultaneamente o bloco G42 e a presença dos 13. Insere-se antes de S1:

- **S0:** A1 reduzida + **erros H0DN originais dos 42**, sem substituição G42 + velocidade peculiar como o H0DN já a herda, sem termo novo + `EXTRA13_OUT` + bloco cruzado zero.

Assim, `S0 → S1` isola o efeito da substituição G42 `STATONLY`, e `S1 → S2` isola o efeito do tratamento dos 13 sob a mesma ponte G42.

### 1.3 Separação entre capacidade e estresse

- **S0 e S1:** indicadores condicionais de capacidade do desenho, nunca certificado.
- **S2–S5:** envelopes de sensibilidade/robustez, não estimativas físicas e não critério autônomo de abandono.
- **S5:** combinação adversarial composta, não necessariamente realizável fisicamente. Um D pequeno em S5 não pode ser usado sozinho para declarar que o teste não tem capacidade.
- Nenhuma variante será escolhida por apresentar o maior D. Todas as células admitidas pelo desenho serão reportadas com seus estatutos.

## §2 O estudo condicional corrigido — somente depois da conferência desta proposta

### 2.1 Âncora de sanidade obrigatória, primeiro

Com a covariância publicada tratada pela redução A1, reproduzir analiticamente os dois D do `FREEZE_R2`:

- modelo publicado: aproximadamente `6,823355`;
- viés diferencial das Cefeidas livre: aproximadamente `5,316944`.

Conferir contra os valores de precisão completa dos recibos, com tolerância absoluta máxima de `1e-6`, e publicar também os valores arredondados a seis casas. Se a âncora falhar, **parar e explicar por quê**; nenhuma célula posterior terá validade.

### 2.2 Cenários fixados agora, antes de qualquer número

1. **S0:** conforme §1.2, sem substituição G42 e com `EXTRA13_OUT`.
2. **S1:** como S0, mas com G42 `STATONLY` **por substituição**, nunca por adição, mantendo `EXTRA13_OUT` e bloco cruzado zero.
3. **S2:** como S1, com `EXTRA13_IN_CAP13` no lugar de `EXTRA13_OUT`. Envelope universal de correlação interna sob marginais fixas; não covariância física recuperada nem cobertura automática dos cruzamentos.
4. **S3:** como S1, mais a componente pública de velocidade peculiar somada por inteiro, como cota de duplicação. **Só produzir número se a componente e a matriz resultante forem PSD**; caso contrário, marcar `INVALID_SCENARIO_NOT_A_NUMBER`.
5. **S4:** como S1, com o bloco cruzado H0DN–BG1 na cota conjunta que minimiza D, sob `c^T S_BG^{-1} c ≤ V_L`. Recalcular os pesos GLS para cada ponto admissível da covariância, sem transportar pesos incompatíveis. É cenário adversarial, não correlação medida.
6. **S5:** a combinação de S2, S3 e S4, somente se a composição for PSD e estiver bem definida. É estresse composto, não cenário físico conservador nem palavra de morte do teste.

Cada cenário será avaliado nos dois modelos: publicado e viés diferencial das Cefeidas livre. **São 12 células, não uma seleção entre elas.**

### 2.3 O que calcular, apenas por álgebra

- Variância GLS do estimador na convenção do `FREEZE_R2` e D de `K = 1,0838071748529643` contra 1, por célula.
- Poder de desenho `Φ(D−5)`, sempre rotulado condicional.
- Orçamento de variância B3 em **S0 e S1**, com blocos disjuntos e todos os cruzamentos explícitos; nenhuma dupla contagem disfarçada de componente.
- Efeito isolado da substituição G42: `S0 → S1`.
- Efeito isolado dos 13: `S1 → S2`.
- Perdas adicionais nos envelopes S2–S5, sem chamá-las de perda física comprovada.

### 2.4 As quatro respostas exigidas

1. Alguma célula **S0 ou S1** com viés Cefeida livre alcança D ≥ 6,282?
2. Qual é o efeito isolado da ponte G42 e quanto os 13 valem em D?
3. Qual bloco domina a perda nos envelopes até S5, e essa perda é física, suposta ou adversarial?
4. Que informação adicional levaria D a 5,842, 6,282 e 6,645, sem transformar S5 em critério de abandono?

Tudo recebe o rótulo `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO`. O certificado continua recusado até existir variante fisicamente admitida e revista.

## §3 A1 e o vetor observado — hipóteses e produtos, sem abrir nem recalcular

Não se exige coincidência dentro dos tripletes. A futura validação usa somente as 72 identidades de §1.1, com tolerância pré-fixada e sem projeção do vetor.

Hipóteses para a diferença histórica, em ordem inicial de plausibilidade pela fonte:

1. **Centros por âncora/MAS:** as linhas representam a mesma medida de hospedeiro, mas os centros publicados estão em referências diferentes.  
   **Produto decisivo:** produtos R22 de precisão completa, fits 9/10/11, valores MAS e mapa de equações; verificar a reconstrução dos centros compartilhados antes de aplicar as identidades.
2. **Convenção de montagem:** `A` e `C` estão corretos, mas `y` foi copiado linha a linha sem validar as restrições nem a propagação dos centros MAS.  
   **Produto decisivo:** código upstream, `construir_y_obs.py:127–128`, `equations.py:334–376`, propagação de `mas_ref_value` e mapa das 255 equações.
3. **Precisão completa/arredondamento:** células decimais publicadas podem gerar resíduos, mas arredondamento não será presumido como explicação antes de medir sua magnitude na fonte.  
   **Produto decisivo:** valores R22 de precisão completa, não apenas tabelas arredondadas; regra de quantização fixada antes de consultar o vetor.
4. **As linhas não são a mesma medida:** hipótese menos favorecida pelo modelo H0DN, que declara explicitamente compartilhamento para host/método/fonte.  
   **Produto decisivo:** H0DN B.3.2 e proveniência individual das linhas. Não inventar variância independente para eliminar a singularidade.

Se uma futura identidade falhar acima da tolerância documental, o resultado é `ASSEMBLY_CONSTRAINT_VIOLATION`, sem reparo, ajuste ou projeção. Nenhum teste de suporte observado está autorizado nesta 03-A.

## §4 O que pedir, e a quem

| Produto que falta | Onde procurar ou a quem pedir | O que destrava | Substituto conservador declarável às cegas |
|---|---|---|---|
| Centros R22 e produtos de precisão completa, fits 9/10/11 e valores MAS | SH0ES/R22, Data Release e autores; H0DN quando houver transformação própria | A1 e hipóteses do vetor | Nenhum para provar suporte; somente recuperação da fonte |
| Operador de agregação e identidade das variáveis de erro G42 | Pantheon+/SH0ES, documentação suplementar e autores H0DN | A2/A3 | S0 com erros H0DN originais como comparação; G42 só condicional |
| Matrizes agregadas ou produtos internos do ajuste G42 | Autores do release, repositório de fits/cadeias | A2/A3 e cruzamentos | `STATONLY` por substituição apenas como cenário |
| Decomposição da covariância do fluxo e do modelo de velocidades | H0DN, Pantheon+, autores do modelo PV e material suplementar | A4 | Nenhum termo PV novo; soma integral apenas como envelope |
| Matrizes internas dos ajustes dos 13 e cruzamentos com 42/HF/host | Artigos e autores originais dos 13, já catalogados nas 18 fontes; SNooPy/SALT2 quando aplicável | A5 | `EXTRA13_OUT` como cenário; CAP13 apenas robustez |
| Covariância conjunta local–fundo e calibrações compartilhadas | H0DN, Planck/DESI e autores das calibrações usadas em BG1 | A6 | Cruzamento zero condicional ou cota PSD adversarial, nunca independência empírica |
| Produtos R22 Y/L/C ou ajuste conjunto alternativo | SH0ES/R22 e autores H0DN | Alternativa não redundante a A1, se desejada | Pseudoinversa/redução do modelo público, sem jitter |

## §5 Proibições

Nenhum Z, t, ĥ ou razão com dado observado; nenhum `evaluate` ou solver no vetor observado; nenhum novo teste de suporte; nenhuma semente ou Monte Carlo; nenhuma alteração do `FREEZE_R2` ou da pasta da v410; nenhuma HMS completa, jitter ou projeção de `y`; nenhuma escolha de variante pelo resultado; nenhuma publicação nem palavra de detecção/confirmação.

## §6 Entrega futura, somente após a conferência desta proposta

Pasta `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\ordem03A\`:

- `ESTUDO_CONDICIONAL_R3A.json` — âncora, 12 células, orçamento S0/S1, efeitos isolados e quatro respostas;
- `A1_HIPOTESES_DO_VETOR.md` — hipóteses e produtos de §3, sem abrir o vetor;
- `PRODUTOS_A_PEDIR.md` — tabela de §4;
- `ENTREGA_ORDEM03A.json` — SHA-256 e bytes de tudo, com a contabilidade de rotas;
- depósito na fila com `quem: kimi` e anotação na rota `estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov`.

Retorno em até 15 linhas, incluindo D por célula apenas depois de calculado, o que fechou ou não, a informação necessária para cada limiar e as perguntas ao operador nas quatro línguas.

## §7 Regra assistente de interpretação

- Se S0 ou S1 alcançar o limiar de referência com Cefeida livre, isso **sugere que vale a pena fechar**, não que o teste já tenha poder.
- Se S0 ou S1 não alcançar, a tabela deve mostrar **qual componente ou informação pode elevar D**, não simplesmente encerrar o caminho.
- S2–S5 informam o preço de envelopes adversos e a prioridade das fontes a recuperar; **nenhum deles, isoladamente ou combinado, decide sozinho que o teste é inviável.**
- O operador continua decidindo depois da tabela: o limiar do portão de poder e se `EXTRA13_OUT` pode ser usado como desenho conservador ou se os produtos internos dos 13 são pré-requisito.
- Só uma variante fisicamente admitida, com covariância completa e revisão independente, poderá avançar para sementes novas, orçamento final, Monte Carlo e eventual certificado.

— Proposta corrigida ao lado, 10/11/2026. **Nenhum cálculo ou abertura executado na redação desta 03-A.**
