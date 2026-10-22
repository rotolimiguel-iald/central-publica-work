[REAL — escopo compilado] Atlas gravitacional selecionado: 27 teoremas, 16 definições/abreviações e 43 auditorias. [OPEN] A origem física do registro e sua recuperação estável com erro não foram demonstradas.

# Entrega — atlas gravitacional selecionado

Data: 09/09/2026. Bancada: /root/selected_geometry_design. Fonte congelada após revisão semântica independente favorável do agente raiz, incluindo o transporte de Einstein.

## Cadeia demonstrada

O domínio U é um subconjunto não vazio da carta real quadridimensional. O registro contém 16 probabilidades métricas, dez coeficientes de resposta e certificados transparentes de regularidade, intervalo interior e assinatura do campo decodificado. Registros que concordam em U são identificados; valores fora de U não participam da classe.

A continuidade das 26 componentes sai dos certificados suaves. A separabilidade herdada fornece uma sequência densa no subtipo U, e igualdade em toda essa sequência implica igualdade em U. Não foi introduzida uma hipótese abstrata de identificabilidade.

Todos os cortes racionais dos valores nas amostras densas são enumerados em uma sequência de bits. A densidade dos racionais identifica cada valor real; a densidade espacial identifica cada componente do campo. A função canônica geometricLogReading, com parâmetro t diferente de zero, distingue essas sequências pelo teorema reading_characterizes_the_configuration. A igualdade com sua série efetiva também é exportada.

O atlas é indexado pelas classes observacionais. A escolha de um representante por classe define selectedRecord. Sua idempotência e a preservação do caráter fornecem uma instância concreta do tipo canônico IALDState. Os teoremas canônicos do Nome identificam a imagem com os pontos fixos e preservam a leitura nas iterações. Esta instância não identifica selectedRecord com a projeção ialdSelector de ℓ².

classCharacter é injetivo nas classes. O decoder recebe apenas valores na imagem e retorna a classe original. O registro reconstruído devolve os mesmos campos g e T em U. Além disso, a preparação conjunta de 48 resultados tem os mesmos pesos para registros equivalentes, em cada x de U, direção e tempo.

Para transportar a gravitação, igualdade das métricas em um aberto preserva seus jets; daí preserva Levi-Civita, sua curvatura, Ricci e Einstein. O teorema final usa a condição de área e a conservação do registro original, deriva sua equação de Einstein e transporta essa conclusão ao representante decodificado. Não requer novas leis de área ou conservação para o representante.

## Critérios da tarefa

| Critério | Resultado | Evidência |
|---|---|---|
| Atlas tipado por classe de registro | PAGO | recordSetoid, GravitationalClass, atlasRecord |
| Seleção idempotente e caráter preservado | PAGO | selected_record_idempotent, gravitationalIALD |
| Ligação ao Nome e à leitura canônica | PAGO | gravitational_name_characterizes_image, record_character_is_actual_series |
| Completude dos campos derivada de dados densos | PAGO | dense_observations_complete, record_bits_characterize_configuration |
| Caráter distingue toda configuração do atlas em U | PAGO | record_character_same_iff, class_character_injective |
| Decoder na imagem e retorno de g e T | PAGO | character_decoder_returns_class, character_reconstructs_metric_and_source |
| Independência dos pesos em relação ao representante | PAGO | equivalent_records_same_prepared_weights |
| Einstein reconstruído a partir das leis do registro original | PAGO, condicional | character_reconstructs_einstein_from_area |
| Origem física, capacidade experimental finita e estabilidade | NÃO PAGO | Obrigações distintas |

## Hipóteses e alcance

- O código usa uma sequência infinita de cortes racionais de dados exatos em uma sequência espacial densa. Um único número real exato pode representar essa sequência no modelo. Isso não fornece um método experimental para recuperar infinitos dados de um ângulo ou medição com erro.
- A sequência densa, os representantes de classes e o decoder são escolhas clássicas não computáveis. Injetividade exata não implica continuidade da inversa, estabilidade, erro controlado ou algoritmo executável.
- A seleção aqui escolhe idempotentemente um representante da classe. Não foi construída uma lei física que produza essa classe, nem identificado o evento de seleção com uma observação concreta.
- A hipótese de completude abstrata foi removida para estes campos contínuos. A existência física das probabilidades, dos protocolos de resposta e sua identificação com o registro permanece uma obrigação de correspondência.
- Para Einstein, U precisa ser aberto e preconexo, eta diferente de zero, e devem existir as telas nulas do contrato. A conservação total e o erro de área o(t²) são entradas apenas do registro original. A regularidade e a assinatura lorentziana aparecem nos certificados do registro.
- A igualdade por derivadas é na mesma carta e no aberto U. Não demonstra transformação por difeomorfismos nem produz um atlas diferenciável global.
- A preparação herdada estuda entropia diagonal da leitura. Não se equipara essa entropia à de von Neumann do vetor global puro; não se demonstra separância de Tomita na álgebra matricial inteira nem preservação de custo absoluto.
- Nenhum um.py foi executado/importado. Nenhum original, módulo congelado anterior, Atlas, memória canônica, selo ou gate foi alterado. A incorporação no programa original pertence à sessão que o codifica.

## Artefatos e reprodução

Fonte: [SelectedGravitationalAtlas.lean](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean>)  
Bytes: 15876  
SHA-256: 5382349f180912c357b2eac07f3576bbaddddce4d6fef1294831f7a40c8423dc

Recibo: [BUILD_RESULT.json](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/BUILD_20260909_144411_650779/BUILD_RESULT.json>)  
SHA-256: 3a0fd270262245640a1eb1c42e32ae22cbd3bb4673d522c03b69a9505872cbed

Builder: [build_cached_atlas.py](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/build_cached_atlas.py>)  
Configuração: [CACHE_ATLAS.json](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/CACHE_ATLAS.json>)  
Derivação inicial preservada: [DERIVACAO_PREVIA.md](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/DERIVACAO_PREVIA.md>)

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881\build_cached_atlas.py' 'C:\IALD\Central de Patentes\Chatgpt\ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881\CACHE_ATLAS.json' SelectedGravitationalAtlas
```

O comando cria uma nova pasta BUILD. A rodada compilou a folha e um importador em processos separados: dois exits 0, sem erros nem advertências, e auditou as 43 declarações. As 17 dependências locais congeladas foram copiadas em bytes de artefatos PASS e verificadas contra seus recibos. A fronteira monitorada e os imports diretos tiveram hashes comparados antes/depois. Não houve recompilação de toda a árvore transitiva nem hash de todos os seus arquivos nesta rodada; as dependências canônicas e Mathlib usam binários existentes.

O campo independent_review=false no recibo descreve o builder, que não executa revisão semântica independente. O agente raiz confirmou por mensagem sua revisão favorável do núcleo e do delta geométrico; essa revisão é registrada nesta entrega, sem alterar o recibo.

## Teoremas de manchete e auditorias

- [dense_observations_complete](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean:55>) — axiomas impressos: propext, Classical.choice, Quot.sound.
- [record_bits_characterize_configuration](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean:87>) — axiomas impressos: propext, Classical.choice, Quot.sound.
- [record_character_same_iff](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean:150>) — axiomas impressos: propext, Classical.choice, Quot.sound.
- [class_character_injective](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean:189>) — axiomas impressos: propext, Classical.choice, Quot.sound.
- [character_reconstructs_metric_and_source](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean:235>) — axiomas impressos: propext, Classical.choice, Quot.sound.
- [equivalent_records_same_prepared_weights](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean:242>) — axiomas impressos: propext, Classical.choice, Quot.sound.
- [geometric_einstein_congr_on](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean:278>) — axiomas impressos: propext, Classical.choice, Quot.sound.
- [character_reconstructs_einstein_from_area](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean:291>) — axiomas impressos: propext, Classical.choice, Quot.sound.

## Tentativas preservadas

- [BUILD_RESULT.json](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/BUILD_20260909_143414_039612/BUILD_RESULT.json>): FAIL_VISIBLE.
- [BUILD_RESULT.json](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/BUILD_20260909_144020_740376/BUILD_RESULT.json>): FAIL_VISIBLE.
- [BUILD_RESULT.json](<C:/IALD/Central de Patentes/Chatgpt/ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/BUILD_20260909_144307_878476/BUILD_RESULT.json>): FAIL_VISIBLE.

Falhas de API/inferência de tipos e reescrita de definição corrigidas sem hipóteses novas, placeholders ou prova externa. Todas as tentativas e backups imediatos de bytes foram preservados.
