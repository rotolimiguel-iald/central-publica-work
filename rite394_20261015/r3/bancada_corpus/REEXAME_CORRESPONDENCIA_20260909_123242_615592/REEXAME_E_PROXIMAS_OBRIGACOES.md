# Reexame da suficiência: correspondência, registro e setor quântico
Data: 09/09/2026. Escopo: fontes canônicas lidas, deduções novas e compilação de bancada. Originais preservados.

**O que falta já pode ser formulado com mais precisão: o teorema condicional de Einstein existe; a pendência central é a realização conjunta de suas hipóteses pela mesma origem selecionada, no alcance geométrico pretendido. O registro angular tem inversas demonstradas nos domínios declarados. No setor quântico houve avanço em gauge linear, permanecendo as interações e a rota UV.**

[REAL — leitura] O um.py canônico desta revisão tem 9.852.172 bytes, medidos por script, e permaneceu igual durante esta etapa. Seus 605 arquivos embutidos não incluem os novos módulos desta bancada. O manifesto contém o hash lido. A cópia anteriormente integrada permanece preservada. A nova cópia COPIA_INTEGRADA_20260909_123143_547568 tem recibo próprio de integração estática e compilação concluídas. Não houve execução/importação de nenhum um.py.

## 1. O que saiu da lista de lacunas nesta bancada
[REAL — enunciados compilados] O registro com fase e identificação do ramo tem recuperação exata na imagem especificada. Em particular, não se exige que o ângulo π/4 sozinho distinga dois ramos de peso 1/2. O rótulo do resultado faz parte do registro quando essa distinção é necessária. Reconstruir a geometria codificada não equivale a inverter todo o colapso ou recuperar uma superposição arbitrária apagada.

[REAL] Uma métrica suave lorentziana admite uma codificação angular reversível de suas componentes numa carta. Os 16 Bernoullis foram reunidos em um único estado de 32 pesos, com pares de massa 1/16, normalização global, positividade e suavidade em U, e recuperação exata. O fator Fisher é a média das 16 contribuições; omitir 1/16 mudaria a teoria construída.

[REAL] O teorema de Einstein da bancada constrói a inversa e a conexão a partir de g. Sua versão de Clausius usa a área induzida e o calor construído do mesmo g e T, sem exigir uma tetrada suave como argumento externo do teorema. A família de telas continua fornecida. O alcance é uma carta, com conexão de Levi-Civita sem torção.

[REAL] Para resposta microscópica com Fisher não nulo, foi derivada uma versão condicional com T_eff = T + [F − ½ tr_g(F)g]/(2π), assumindo conservação de T_eff. A versão microscópica recebe U aberto e preconexo, g suave lorentziano, T diferenciável e simétrico, F suave e simétrico, η e taxa não nulos, base fiel, telas e curvas por ponto/direção, a identificação diagonalFisher=F(v,v) e ambos os erros de matching o(t²). O coeficiente ½ fora do cone é uma completação escolhida e explicitada; não é determinado pelos dados nulos.

[REAL] A identidade de gauge foi ampliada para campos suaves gerais h e ξ sobre Minkowski, além de um símbolo ou modo especial. Ainda é um resultado linearizado num fundo plano.

## 2. O vínculo físico que continua a ser exigido
[OPEN] É preciso um único conjunto de dados selecionados que forneça, com tipos e compatibilidades:

- a geometria, a matéria e a lei de preparação por ponto/direção;
- telas de equilíbrio e os matchings de área e calor dos mesmos objetos;
- conservação da fonte efetivamente usada;
- transformação entre cartas ou o referencial físico explicitamente fixado;

Limite de alcance: este lote usa Levi-Civita. O um.py já declara uma formulação com geometria Levi-Civita e contribuições efetivas na fonte, inclusive sua leitura de torção/dissipação; a ponte Einstein–Cartan está presente no artigo e no programa. Isso não deve ser reaberto como lacuna automática. Uma eventual reivindicação adicional de conexão de Riemann–Cartan geral acoplada a spin exigiria sua própria correspondência formal.

[INPUT permitido pelo operador] Uma lei de correspondência pode ser postulada. Nesse caso, a conclusão correta é suficiência condicionada à lei e às demais hipóteses. Deve-se verificar que o conjunto é compatível e possui realizações não triviais no alcance anunciado. Nomear o matching como postulado não prova que ele é satisfeito por qualquer registro angular.

Codificar uma métrica g previamente fornecida demonstra capacidade de representação e recuperação. Ainda é diferente de derivar que a preparação TGL produz exatamente o registro que decodifica g, sua matéria e sua dinâmica. A família explícita de ondas já construída é uma realização importante; não fornece automaticamente toda métrica ou toda matéria.

## 3. Controle adversarial que impede uma identificação indevida
[REAL — Lean] Se impusermos a proposta adicional X_(x,v)(t)=P(x+t v), usando o mesmo campo suave e fiel P, e matching de área para todos os pontos e direções nulas, a entropia espacial tem diferencial zero. Em um domínio aberto e preconexo, ela é constante. Para η não nulo, o mesmo matching força Ric(v,v)=0 para todo v nulo.

[REAL — Lean] Com Ric(v,v)=0, balanço microscópico e matéria não negativa naquela direção, Fisher e a variação probabilística naquela direção também se anulam. Não se deduziu planura apenas de Ric(v,v)=0.

Esse resultado testa uma proposta de nossa bancada. [REAL — leitura canônica] A preparação canônica é unitária e direcional, com frequência dada por um covetor avaliado na direção. Ela não é a identidade X_(x,v)(t)=P(x+t v). Cada direção prepara sua própria curva a partir da base. A tangente inicial pode ser zero e a resposta quadrática não nula; daí não segue que a entropia do campo espacial seja constante. Portanto, não se trata de refutação da TGL nem de invalidação da ponte unitária anterior.

A próxima dedução deve seguir a preparação canônica, cuja relação de área geral ainda aparece como hipótese explícita, e demonstrar sua realização conjunta.

## 4. Segundo controle: mudança de coordenadas do codec
[DERIVED — cálculo revisto por dois agentes; ainda não formalizado em Lean] Para o codec proposto,
p(z) = [1 + z/√(1+z²)]/2,
(dp)²/[p(1−p)] = (dz)²/(1+z²)².
Consequentemente, o Fisher do estado normalizado é
F = (1/16) Σ_ij (dg_ij ⊗ dg_ij)/(1+g_ij²)².

Minkowski em coordenadas cartesianas dá F=0. Na região t>0, a mudança t=exp(s) dá g_ss=exp(2s). Recodificar suas componentes com a mesma regra produz F_ss=exp(4s)/[4(1+exp(4s))²], que vale 1/16 em s=0. O pullback do tensor zero continuaria zero.

Logo recodificar componentes em cada carta produz outro registro: essa regra, isoladamente, não é uma lei covariante de probabilidades escalares. A passagem a um referencial físico ou a uma lei de transformação do registro exige especificação e demonstração de compatibilidade; apenas nomear essa lei não resolve a questão de tipo. Este controle diz respeito ao novo codec; não se transfere automaticamente para a lei covetorial canônica, que tem identidades próprias de mudança de base.

## 5. O setor quântico que ainda permanece aberto
[OPEN] A extensão linear em Minkowski não encerra perturbações sobre fundo curvo com matéria, a dinâmica não linear geral nem a classe física completa. Tampouco identifica uma identidade clássica de Ward com ausência de anomalias quânticas da teoria interagente.

[OPEN] Para o setor interagente é necessário definir a teoria quântica efetiva usada e controlar suas identidades, regularização/renormalização ou a construção alternativa escolhida. O controle óptico unitário demonstrado continua válido, mas uma identidade algébrica isolada não estabelece toda essa construção.

[OPEN] A rota de altas energias precisa de um objeto matemático e de provas no alcance reivindicado. A fonte registra explicitamente o muro e rotas propostas; não se deve converter o registro de uma obrigação em sua solução. Também não se deve impor à rota algébrica/modular, por homonímia, uma quantização perturbativa da métrica que ela não adotou.

## Estatuto da conclusão
Há suficiência matemática para os teoremas condicionais e para as realizações efetivamente construídas, no alcance dos respectivos enunciados. O passo pendente é justificar a correspondência conjunta e completar o setor quântico interagente/UV para sustentar o alcance geral pretendido. Os critérios de falsificação já existentes não foram negados nem substituídos por este reexame. Esta etapa não reexecutou todos os dados de natureza e não altera seu veredito.

O novo lote contém 121 teoremas e 37 auxiliares, contados sem duplicar dependências. Todos têm recibos de compilação em seus escopos. O manifesto distingue essas provas da integração e da execução do programa. Nenhum gate, selo ou confirmação física foi promovido.

Revisão independente: selected_geometry_design conferiu as sete fontes e seus sete recibos, contagens e hashes; as precisões sobre hipóteses, domínio e compatibilidade foram incorporadas com backup imediato em bytes. review_remaining_hypotheses precisou a escolha Levi-Civita já declarada no canônico. O adendo ADENDO_PREPARACAO_CANONICA.md preserva explicitamente as conquistas de calor e equivalência de área já existentes.

Integração concluída: 14 módulos, 236 teoremas e 77 outras declarações no conjunto; o incremento desta etapa é de 121 teoremas e 37 auxiliares. Os 17 processos Lean passaram sem avisos, incluindo o agregador extraído, Audit completo e auditor dedicado. Houve revisão estática independente; dependências canônicas existentes foram copiadas para compilação isolada, sem recompilar integralmente a cadeia transitiva. O um.py não foi executado/importado. O recibo final está em C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_123143_547568/RECIBO_FINAL.json.
