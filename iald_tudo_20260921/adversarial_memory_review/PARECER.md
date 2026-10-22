# Revisão adversarial do candidato Haiku — 22/09/2026

**Parecer ao responsável pela tarefa principal: não aprovo ainda a adequação ao orçamento nem a cobertura semântica dos 325 tópicos.** Há uma redução estrutural concreta de **8.410 tokens o200k**, medida localmente, que preserva os textos dos conceitos do candidato e externaliza metadados de auditoria identificados. Ela não demonstra o corte de aproximadamente 40 mil tokens Anthropic necessário. Não encontrei base para prometer que apenas remover metadados alcance a meta.

## Base conferida

[REAL — leitura e medição local] Candidato SHA256 `70344cd27bca5f733b52a1d5bfce121ee99abf5deb41fc5ed208c4cdf42fcbc5`, com **178.804 o200k_base** recalculados. O recibo `haiku_count.json`, conferido contra esse SHA, registra **220.651 input_tokens Anthropic**, baseline **9**, modelo `claude-haiku-4-5-20251001`. A chamada Anthropic não foi refeita nesta revisão.

[DERIVED — subtração do baseline do recibo] A diferença é **220.642**, não uma nova contagem isolada de memória feita aqui. Para atingir 180.000 nessa convenção, cortar **40.642**. A razão observada é cerca de 1,234 Anthropic/o200k; não é um conversor válido para as variantes, pois sua composição muda. Os cerca de 32–33 mil o200k são uma orientação inicial, não critério de aceitação.

[REAL] Kernel de instrução **v5** e Memory Core **v1** foram lidos pelos caminhos do manifesto, seus hashes conferidos e seu texto integral localizado no candidato. Isso não é auditoria de compilação do kernel Lean. Foram identificados **325 blocos de tópicos**, não certificadas 325 coberturas semânticas. Os cinco arquivos revisados mantiveram seus hashes durante a primeira medição; o candidato também foi reconferido ao final da segunda.

## Proposta quantitativa reproduzível

Os scripts só constroem variantes em memória. Não gravam nem substituem candidato ou builder. Os números abaixo já incluem as pequenas instruções adicionais necessárias para explicar a representação.

| Alternativa isolada ou combinada | Total o200k | Economia o200k |
|---|---:|---:|
| Abreviar 11 chaves repetidas, com dicionário literal | 177.650 | 1.154 |
| Dicionário reversível de 57 identificadores nos JSONs | 177.253 | 1.551 |
| Chaves e 28 valores repetidos compartilhados | 175.945 | 2.859 |
| Referências internas exatas à exposição por offset e extensão | 178.235 | 569 |
| Caminho implícito apenas em objetos que hoje contêm somente `@` | 177.202 | 1.602 |
| Metadados auxiliares recuperáveis e indicadores individuais da escada | 172.594 | 6.210 |
| **Combinação das três últimas alternativas** | **170.394** | **8.410** |

**Não somar as alternativas entre si:** há sobreposição. A combinação indicada foi efetivamente tokenizada. Tokens Anthropic das variantes: **[OPEN — não medidos]**. A igualdade por expansão dos dicionários de chaves/identificadores foi verificada; isso não mede a capacidade do modelo de usar a codificação.

Aplicação concreta recomendada ao pai:

1. Em `capsule`, tratar `/core/external_ladder/per_theorem` como indicadores individuais de auditoria, conservando ponteiro e contagens true/false. A projeção atual contém somente booleanos nesse campo: a medição checou isso. Os seus nomes não são enunciados de teoremas. A coleção custa **4.496 o200k** na serialização por campo; a economia líquida é menor e está computada na variante. O veredito e os campos conceituais do tópico permanecem carregados. Atribuir prova individual continua exigindo consulta ao indicador e à fonte.
2. Tirar do texto carregado somente os campos auxiliares explicitamente medidos: `runtime_s`, `protocol_hash`, `frozen_hash`, `result_sha16`, `catalog_sha16`, `result_path`. Preservá-los na fonte e no registro derivado de recuperação. Não retirar o hash de ancoragem do pacote/manifesto. A lista concreta das ocorrências está em `structural_measurements.json`, `audit_removed`.
3. Para objetos exclusivamente `{"@":"/caminho"}`, usar caminho derivado da posição estrutural do objeto. Não aplicar isso indiscriminadamente a objetos com `fields`, índices de listas ou escapes JSON Pointer. A medição representa o ganho; o resolvedor novo precisa de teste independente de ida e volta em **cada** ocorrência antes de adoção.
4. Referências novas à exposição devem identificar intervalo exato por caracteres Unicode e vincular-se ao SHA final. A medição confere a igualdade literal da substring. Não apagar o texto de destino e não remover os estatutos associados.
5. Só então medir o pedido Anthropic completo na tarefa principal e considerar a economia residual. Esta revisão não faz rede, API ou implantação.

`all_verified` aparece 276 vezes; `does_not_gate_core`, 223. São candidatos a tabelas compartilhadas **com associação explícita por tópico e valor**, nunca a um default global que esconda false/ausente. O ganho adicional não foi medido em conjunto e não entra nos 8.410. A repetição desses campos não autoriza transformar flags em prova ou mover gate.

## O que não é metadado descartável

Custos por campo, somados em serializações individuais, servem para localizar volume; não são economias líquidas: `verdict` **12.812**, `theorem` **9.611**, `statuses` **5.500**, `seals` **3.172**, `not_claimed` **2.399**, `selo` **1.716 o200k**. Esses campos podem conter o próprio enunciado, hipótese, fórmula, ressalva ou resultado negativo. Não os descartar pelo nome, por caixa alta ou por aparência de identificador.

Exemplo observado: o campo `status` de `alpha_inversion` contém a distinção entre forma e valor, a identidade `1=q²+α²` e a função de validação externa do CODATA. `seals` também contém proposições; `not_claimed` preserva limites substantivos. Os blocos **Estatutos** da exposição incluem protocolos, resultados quantitativos e limitações. **Não são uma lista de auditoria vazia.**

Divisão medida do candidato: antes dos tópicos **40.919**, região dos tópicos **98.479**, exposição e cauda **39.406 o200k**. O prefixo contém, além de v5/Core, construções formais completas de H1/H2/H3. Não proponho amputar essas construções como atalho para a meta.

Após a combinação estrutural ainda faltariam aproximadamente **24,5 mil o200k**, se a razão inicial fosse usada apenas como estimativa de planejamento. A próxima proposta concreta é fundir cada tópico com sua exposição correspondente numa única cápsula semântica: ideia principal, objetos, hipóteses, enunciado/fórmula, estatuto, limite e recuperação. Orçamento inicial de redução adicional: cerca de **75 o200k por tópico em média**, aplicado por volume e redundância, nunca uniformemente. Essa etapa exige revisão das 325 relações tópico–fonte: **não foi realizada nem está aprovada aqui**. A economia de referências literais foi pequena; uma economia maior exigirá reformulação semântica e não pode ser anunciada como compressão sem perdas já demonstrada.

## Achados adversariais dos verificadores

**[P1] O seletor não acompanha o significado do ancestral.** `protected_fields` decide pela chave imediata. Uma estrutura `hypothesis` ou `assumptions` é percorrida, mas seus filhos com nomes como `amplitude`, `sign` e `delay_INPUT` deixam de herdar proteção. `statement` nem sequer está no regex. A auditoria de essenciais repete a mesma heurística e ainda exclui strings menores que 40 caracteres, números, booleanos e elementos string de listas sem chave correspondente.

Exemplos lidos da fonte publicada indicada pelo manifesto, ausentes literalmente tanto em texto direto quanto escapado no candidato:

- `/core/area_scale_newton_equivalence/no_go/statement`: invariância dos dados modulares adimensionais sob `A -> lambda A`, enquanto eta e o acoplamento gravitacional mudam.
- `/core/right_angle_mirror/c3_register_theorem/statement`: contém `Theta_perp=pi/2`, `P²=P`, `J²=I` e a interpretação do registro. O estatuto do registro deve ser recuperado no contexto; ausência lexical não autoriza atribuir prova nova.
- `/core/gw_echo_kms_rite/record/hypothesis/amplitude`: fórmula `A_echo/A_wave = |R| = sin(theta_Miguel) = sqrt(beta)` com referências nominais ao kernel na fonte.
- No mesmo objeto, `sign`, `delay_INPUT`, `beta_source`, `retired`: sinal, lei de atraso e seus estatutos KNOWN/ONTO/INPUT, fórmula de beta e hipótese aposentada.

Isso demonstra uma **lacuna do teste**, não prova que cada ideia esteja semanticamente ausente da exposição. É necessário mapear sua representação equivalente, com hipóteses e estatuto, antes de aceitar a omissão. Foram encontrados **5 campos `statement`** ausentes literalmente. A lista ampla de **4.783 strings** ausentes também inclui detalhes e evidências legitimamente recuperáveis; não deve ser tratada como 4.783 perdas essenciais.

**[P2] Falsos positivos do regex.** As **32 strings ausentes** cuja chave bate no filtro original são hashes de 64 caracteres sob `formal_files_sha256`, porque o nome do arquivo contém termos como `commut`/`theorem`. Não é correto reinserir esses hashes como se fossem fórmulas restauradas. A lista concreta está no relatório de strings ausentes.

**[P1] Verificador compartilha o mecanismo de seleção do construtor.** `verify_haiku_candidate.py` importa `capsule` e `compact_references` do próprio builder. Pode aprovar que o candidato seja exatamente a projeção defeituosa. Isso é teste de equivalência da implementação, não revisão independente da suficiência da projeção.

**[P2] Referência `@EXPOSITION` não é resolvida até o intervalo efetivo.** A função `compare` testa a presença do valor esperado na exposição original e o prefixo, mas não testa que a dupla seção/prefixo seja uma identificação única no texto carregado. O verificador compara linhas da exposição separadamente, o que reduz alguns riscos de ausência, mas não garante ordem, multiplicidade ou resolução inequívoca. Proposta: `id`/intervalo determinístico e resolução contra o texto final; teste independente de equivalência no campo de origem.

**[P2] Recuperação operacional permanece aberta nesta revisão.** Resolubilidade de ponteiro JSON em disco não equivale a uma ferramenta `fetch_tgl` implantada que aceite esse ponteiro e devolva o trecho exato. Não executei `prepare_pointer_fetch.py`; não testei produção. Preservar a remissão é necessário, mas não basta para declarar recuperação operacional verificada.

## Critério de aceitação recomendado

Manter v5/Core integrais por comparação de fonte, comparar enunciados/hipóteses/estatutos por localização de origem e destino, conservar negativos e ressalvas, e testar cada referência nova. Contar **o pedido completo**, com ferramentas, demais instruções, histórico e reserva de saída dentro dos 200.000. O alvo do operador é núcleo **>=180.000 tokens Haiku**: atingir 179 mil não satisfaz automaticamente esse piso, e 180 mil de memória não demonstra sozinho que o pedido completo caiba. Não usar enchimento para cumprir o piso; calibrar o conteúdo substantivo depois da contagem efetiva.

## Limites e entrega

Sem rede, API paga, leitura de `.env`, leitura de arquivos privados proibidos, execução/importação de `um.py`, execução do builder/verificador original ou alteração de candidato, fontes, memórias e produção. O acesso elevado foi usado apenas para a biblioteca Python instalada no perfil e os scripts locais autorizados. Não consultei nem alterei Cloud18/Sonnet. A consulta ao Atlas foi restrita à régua; as fontes técnicas vieram do manifesto. Nenhum gate foi movido.

Artefatos: `measure_local.py`, `measure_structure.py`, `measurements.json`, `structural_measurements.json`, `missing_source_strings.json`, `reversible_dictionaries.json`. Os scripts recusam sobrescrever seus relatórios; nova execução deve usar nomes novos ou uma nova subpasta de revisão. O parecer é independente do construtor, mas não constitui aprovação semântica integral nem afirma “toda a TGL completa”.
