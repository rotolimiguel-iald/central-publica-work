# ORDEM KIMI H0DN-02 (10/11/2026) — O que falta para o teste H0DN × BG1 ter poder preditivo discriminante REAL: fechar a covariância física e certificar o poder às cegas

**De:** gerência c1 da Central (Claude Code), por ordem do operador Luiz Antonio Rotoli Miguel (IALD/TGL), verbatim sha256 `122e85b43994d6c0a186d63f0a65f54b786c1f6bcbb9b72387b3afaa1f613a96` (arquivo `work\cunhagens_13out\OPERADOR_10nov_teste_sem_poder_preditivo_nao_se_roda_comando_ao_kimi_o_que_falta_verbatim.txt`): «Quanto ao teste, se ele não tiver poder preditivo não vamos roda-lo dê o comando ao Kimi sobre o que falta ele resolver para que tenhamos um teste com poder preditivo discriminante real.»
**Para:** Kimi K3 Pro. **Tipo:** FECHO DE COVARIÂNCIA + CERTIFICADO DE PODER. Nenhuma abertura, nenhum Z, nenhuma publicação.
**Estatuto do que você devolver:** `[DECLARADO pelo Kimi]` até a gerência conferir na fonte e por código próprio.

## §0 O que está decidido (não refazer)

1. O teste é o H0DN × BG1 (razão H_local/H_fundo), congelado em `FREEZE_R2` e PRÉ-REGISTRADO na v410 do `um.py` com a função de veredito pinada por sha256. Nulo: razão = 1. Alternativa: K = E(z*)^(2β/3) = 1,0838071748529643, β = α√e, zero parâmetro livre. Regra conjunta: z_nulo ≥ 5 e |z_TGL| ≤ 1,959963984540054.
2. A sua entrega de 09/11 foi lida e VALE como está: `y_obs` de 255 linhas montado; G1 candidato forte; G2 fechado; **G3/G4 obstrução exata** (covariância publicada com posto 183 e nulidade 72; o vetor observado tem projeção de 0,0931 mag nas 72 direções de variância zero; a HMS completa dá posto 255 mas DUPLICA a variância já contida em `mu_error` e não é admitida); 18 fontes primárias dos 13 calibradores fora do R22, com fatores parciais; `opening_allowed = false`. A v410 embute só o recibo documental. Se aberto hoje, o veredito seria `INCONCLUSIVE_SYSTEMATICS`.
3. **REGRA NOVA DO OPERADOR (10/11): teste sem poder preditivo discriminante não se abre.** A função congelada só chama «subpotente» quando o D esperado é menor que 5; isso é 50 % de chance de alcançar 5σ se a TGL for verdadeira. Não basta. O poder tem de ser CERTIFICADO, às cegas, sob a covariância FÍSICA, antes de qualquer abertura.
4. O que se sabe do poder hoje, e por que não serve: no `FREEZE_R2` (covariância publicada) D = 6,823355 no modelo publicado (poder 96,6 %) e D = 5,316944 com o viés diferencial das Cefeidas livre (poder 62,4 %). Essa covariância é a que NÃO aceita o vetor real. Sob a covariância física o poder é desconhecido. Relação que vale: poder = Φ(D − 5); 80 % pede D ≥ 5,842; 90 % pede D ≥ 6,282; 95 % pede D ≥ 6,645.

## §1 O que falta, em ordem

### A. Fechar a covariância física (sem ela não há teste)

A1. **Equações de hospedeira (166 linhas; o nó da obstrução).** Decida PELA FONTE o que são as 72 direções de variância zero: (i) restrições exatas (a mesma medida repetida em linhas de âncoras diferentes), e então o vetor observado TEM de satisfazê-las e a sua montagem do `y_obs` é que muda; ou (ii) variância independente ausente (cada linha âncora-específica é uma medida distinta com erro próprio que o `mu_error` publicado não separa), e então você a fornece a partir dos orçamentos de erro originais. Entregue, por linha: σ independente, fatores compartilhados F_âncora, F_MAS, F_HMS, a fonte (arquivo e linhas) e a prova de que nenhuma variância entra duas vezes. É o seu próprio `required_decomposition` de 09/11.
A2. **SN-only:** o G42 STATONLY com a reconciliação da dispersão intrínseca.
A3. **Hospedeira-Cefeida:** separada, sem duplicar a informação Cefeida que já está na rede.
A4. **Velocidade peculiar:** separada, sem duplicar a variância de velocidade que o H0DN já soma.
A5. **Os 13 calibradores fora do R22:** para cada um, covariância com fonte, ou `OPEN_NO_TRANSPLANT`. Para os que ficarem abertos, DUAS variantes decididas às cegas e declaradas antes de qualquer número: (V13-dentro) com inflação conservadora justificada pela fonte; (V13-fora) excluindo as linhas dos 13. As duas servem só para o poder; nenhuma é escolhida olhando o dado.
A6. **Bloco cruzado H0DN–BG1:** a independência condicional justificada, ou cenários com cota.
**Aceite de A:** matriz simétrica, PSD, de posto completo no suporte usado; duplicação de variância excluída por demonstração; o estimador reconstruído para a nova matriz aceita vetores SINTÉTICOS. O teste de suporte com o vetor observado é permitido UMA vez por variante admitida, só passa/falha, e entra na contabilidade de rotas (é olhar o dado).

### B. O certificado de poder, às cegas (sem `y_obs`)

B1. Para cada variante admitida de covariância × modelo (publicado; viés Cefeida livre; e qualquer sistemático novo que a decomposição revelar): o D esperado de K contra 1, com os pesos refeitos para a nova matriz, só em sintéticos.
B2. Poder por Monte Carlo com sementes NOVAS, gravadas em arquivo ANTES de rodar (as da R2 não se tocam): P(z_nulo ≥ 5 e |z_TGL| ≤ 1,96 | TGL verdadeira); P(z_nulo ≥ 5 | ΛCDM) (falso positivo); P(|z_TGL| ≥ 5 | ΛCDM) (o poder de FALSIFICAR a lei K se ela for falsa: discriminante real é dos dois lados); e a robustez à covariância mal especificada (analisar com a variante i quando a verdadeira é a j).
B3. O orçamento de variância de ln(razão), em frações: âncoras; relações PL e indicadores (Cefeidas, TRGB, JAGB, SBF, masers); calibradores SN (os 42 e os 13); fluxo de Hubble; velocidade peculiar; BG1.
B4. **O que falta para o poder:** no cenário CONSERVADOR (o menor D entre as variantes e modelos admitidos), a tabela do que levaria D a ≥ 5,842, ≥ 6,282 e ≥ 6,645: qual bloco reduzir, ou qual conjunto PÚBLICO adicional (nome, fonte, o que acrescenta), com o ΔD estimado; e se depende de dado ainda não público.
B5. **Veredito do certificado**, um de: `POWER_CERTIFIED_REAL` (D conservador ≥ 6,282); `POWER_MARGINAL` (5 ≤ D conservador < 6,282); `UNDERPOWERED` (D conservador < 5); `COVARIANCE_NOT_CLOSABLE_FROM_PUBLIC_SOURCES` (com o que seria preciso). O limiar de 90 % é PROPOSTA da gerência; o operador o fixa antes de qualquer abertura; devolva os D para que qualquer limiar se aplique.

### C. Se o H0DN sozinho não alcançar poder real

Proponha (sem executar) o melhor teste discriminante de zero parâmetro com dado público: por exemplo a combinação do H0DN com medidas locais que não compartilham calibradores (com a covariância entre elas), ou outro observável em que K e ΛCDM diferem. Consulte antes o Mapa de Rotas (`rotas.py consultar "discriminante"`, `"hubble"`, `"fase9"`): a Fase 9 V2 (z_disc 4,44) e as rotas mortas não se refazem.

### D. Revisão independente e contabilidade de rotas

Cada vez que o dado observado foi tocado (a montagem do `y_obs`; cada teste de suporte) é uma rota contada; a abertura usará UMA rota pré-registrada. Prepare o pacote para um revisor que não seja você conferir A e B.

## §2 O que você NÃO faz

Não calcula Z, t, ĥ nem razão com dado observado; não roda `estimator.evaluate` nem solver no vetor observado; não compara `y_obs` com a direção do sinal; não gera semente da R2; não altera `FREEZE_R2` nem nada da pasta `work\cadeia_de_selo\v410`; não adota a HMS completa para forçar o suporte; não transplanta `STAT+SYS` por atacado; não escolhe variante de covariância olhando o dado; não escreve «5σ», «confirmado» ou «detectado»; não publica.

## §3 Entrega, em `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\ordem02\`

`SEEDS_R3_REGISTRADAS.json` (antes das rodadas); `C_fisica_R3_<variante>.npz`; `DECOMPOSICAO_FISICA_R3.json` (por bloco: método, fonte com linhas, prova de não duplicação); `CERTIFICADO_DE_PODER_R3.json` (B1 a B5); `PACOTE_REVISAO_R3\`; `ENTREGA_ORDEM02.json` com sha256 e bytes de tudo. Depósito na fila da memória em `...\memory\fila\depositos\kimi\` com o campo `quem: kimi` no frontmatter, IGUAL ao nome da pasta: os seus quatro depósitos de 09/11 foram recusados pelo guarda porque diziam `quem: kimi-k3pro`; redeposite-os com o campo certo. Anotação na rota `estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov` do Mapa.

## §4 Retorno

Até 15 linhas: o veredito do certificado; os D por variante e modelo; o que fechou e o que não fechou em A, com a razão; a tabela B4 resumida; os sha256; e as perguntas que pedem decisão do operador, nas quatro línguas dele (TGL, teológica, linguística, jurídica). Uma obstrução demonstrada também é resultado: «não é fechável com fonte pública, e falta X» é resposta válida e útil.

## §5 O que a gerência fará com a entrega

Confere na fonte e por código próprio. Só com `POWER_CERTIFIED_REAL` e a revisão independente aceita se pré-registra o novo congelamento e o portão de poder numa versão futura do `um.py`, e só então o teste se abre, uma vez, pela função de veredito.

— gerência c1, 10/11/2026. Correções AO LADO, nunca por cima.
