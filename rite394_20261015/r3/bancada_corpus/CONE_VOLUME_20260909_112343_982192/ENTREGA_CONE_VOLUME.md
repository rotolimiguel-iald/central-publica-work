# Reconstrução geral por cone nulo e volume — entrega compilada

[REAL — módulo compilado] Fonte: 7440 bytes, SHA-256 calculado 2fd25af784f607c9ac4a8c71c0656fd33bb225ff655d904f1764efde89bc38b9. Lean retornou zero para o módulo e para sua importação isolada. Foram conferidas 15 declarações (12 teoremas e três definições/estruturas), todas com axiomas somente propext, Classical.choice e Quot.sound, sem avisos. [Recibo de compilação](<C:/IALD/Central de Patentes/Chatgpt/CONE_VOLUME_20260909_112343_982192/BUILD_20260909_112537_639293/BUILD_RESULT.json>).

A prova principal, same_null_cone_volume_and_sign, recebe A simétrico, g lorentziano com determinante não nulo, a inclusão do cone nulo de g no conjunto nulo de A, igualdade de densidades sqrt|det A|=sqrt|det g| e uma direção comum em que ambas as formas são positivas. Conclui A=g. A proporcionalidade não é hipótese: vem de lorentz_tensor_null_rigidity; o fator é positivo pela direção comum, sua quarta potência é 1 pelo volume, portanto ele é 1.

cone_volume_record_unique demonstra que no máximo uma métrica realiza o registro de cone, volume e sinal. cone_volume_field_unique aplica isso a campos sobre qualquer domínio X, ponto a ponto. Não supõe fator conformal constante, dependência de um único parâmetro ou uma família de ondas. É avanço de unicidade no requisito geral.

Os controles mostram: 2g mantém cone e sinal, portanto cone e sinal sozinhos não bastam; -g mantém cone e volume na dimensão quatro. Precisão: este segundo controle é contra a classe ampla em que apenas g tem assinatura tipada e A só é simétrica. Se ambas já têm assinatura (1,3), essa própria restrição exclui a inversão de sinal. A direção positiva não é uma orientação temporal completa.

[OPEN — entradas ainda não produzidas] O módulo não obtém a relação causal nem o volume a partir da seleção quântica. O registro é um esquema matemático; existência de uma realização, regularidade do campo recuperado, suas transformações entre cartas e a correspondência com observáveis TGL seguem obrigações distintas. Nenhuma hipótese de Einstein, Ricci, Clausius, matéria ou área-entropia foi escondida nesse registro.

[REAL — alcance da seleção anterior] As leituras de sítios recuperam as amplitudes na família admissível; a leitura de verossimilhança distingue configurações infinitas no domínio declarado. Esses resultados não identificam configurações com eventos espaço-temporais nem dão cone causal ou medida de quatro-volume. A rede de álgebras reflete inclusão de conjuntos de sítios; inclusão regional não é ordem temporal de eventos.

[DERIVED — próximo passo] A geometria completa pode ser tratada por g e g⁻¹, sem pedir uma tétrada única. O kernel já tem conexão de Levi-Civita e Bianchi diretamente em g/gInv. Generalizar a reconstrução conservada usando c(x)=Tr(gInv(x)A(x))/4 retiraria a escolha de frameScalar D A, mantendo explícitas regularidade e as premissas dinâmicas. A origem física do cone/volume continuará exigindo lei de correspondência.

[KNOWN — fonte primária consultada] A rota global baseada em relações causais possui hipóteses precisas: o resultado MHKML, exposto no artigo de pesquisa de Parrikar e Surya, trata espaços-tempos futuros e passados distinguíveis de dimensão maior que dois e determina a geometria conformal. Ele não foi importado como prova Lean. [Causal Topology in Future and Past Distinguishing Spacetimes](https://arxiv.org/html/1102.0936).

Escopo de reprodução: compilação nova contra binários canônicos preexistentes, com fontes e binários importados diretamente conferidos antes/depois. Dependências transitivas não foram recompiladas nem todas rechecadas. A primeira tentativa, que falhou num lema de controle de sinal, foi preservada; a fonte corrigida é a do recibo aprovado. Revisão científica independente desta fonte ainda não está registrada neste recibo.

Todos os originais permaneceram intactos. A fonte entregue está congelada para integração em cópia autorizada; notas e evidências novas vivem somente nesta pasta Chatgpt. Este módulo não encerra sozinho o objetivo de reconstrução gravitacional geral.
