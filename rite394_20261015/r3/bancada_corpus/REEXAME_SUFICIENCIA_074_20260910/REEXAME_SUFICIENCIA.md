# Continuidade da suficiência — entrega074

10/09/2026. [DERIVED — matemática escrita] [KNOWN — importações delimitadas] [REAL — documentação medida]. A entrega073 anterior representou progresso: realizou P0 no modelo declarado e deixou construções revisadas. Esta etapa prossegue pela classe natural dos contratermos, preservando o objetivo geral.

**Avanço desta entrega:** construímos a substituição natural da translação dos ghosts na apresentação métrica e calculamos seu termo de curvatura. Demonstramos que essa translação preserva a completação por laços e valência pertinente. Também delimitamos, com um contraexemplo e um transporte positivo, o que pode passar da cohomologia coordenada para a natural.

O resultado não é a remoção das anomalias. Ele fornece operadores e critérios para essa demonstração e exclui uma passagem incorreta que apagaria a curvatura ou ampliaria indevidamente o alcance aos ghosts Lorentz convencionais.

## 1. Estado canônico e evidência

A [captura canônica074](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_074_20260910/ESTADO_CANONICO_074.json>) encontrou os quatro artefatos canônicos com os mesmos bytes da entrega073. O programa consultado continua v338, com 683 arquivos embutidos; o comparador encontra 77 dos 98 módulos anteriores e mantém 21 ausentes. O selo corresponde ao um.py lido. A captura usa AST e leitura de bytes; não executa/importa o programa.

As demonstrações novas são escritas, com revisões internas por leitores distintos de seus autores nas frentes indicadas. Não houve Lean, CAS, cálculo de diagramas ou testes de natureza. Controles de hashes e links medem integridade documental. Nenhum original, Atlas, índice, memória canônica, selo ou gate foi alterado. Todas as escritas ficam em Chatgpt.

## 2. A translação natural conserva a curvatura

A nota de [translação natural e curvatura](<C:/IALD/Central de Patentes/Chatgpt/HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/TRANSLACAO_NORMAL_E_CURVATURA_BRST.md>) define b_N pela inserção dos jatos de campos constantes empurrados pela exponencial geodésica de B0, centrada a cada ponto. Isso produz um operador natural sem coordenadas normais globais. A derivada horizontal diferencia também a dependência no centro.

O cálculo fornece C_N=[d_H,b_N], C_N(∇̄c)=−R̄ e a conjugação exata e⁻ᵇᴺ(s+d_H)eᵇᴺ=s+E_N+C_N. As relações incluem E_N²=−{s,C_N}, {s,E_N}=0 e {E_N,C_N}=C_N²=0. Portanto E_N induz um diferencial em H(s), mas não é um diferencial independente na álgebra completa. Não pode ser identificado sem prova com d_ext da entrega073.

No fundo g0=dr²−a²γ, a=2cos(r/2), a componente C_N(∇̄_i c^r)=a²γij dr∧dy^j/4 é não nula no interior. Ela não é uma anomalia física: é o termo geométrico que a conjugação precisa conservar.

A recorrência correta para uma primitiva total é sT_q+E_NT_(q−1)+C_NT_(q−2)=Ω_q, para q=0,…,4. Depois de resolver as etapas anteriores, a próxima obstrução é s-fechada. Encontrar sua primitiva natural continua uma obrigação; a recorrência não a presume. O [parecer da raiz sobre a translação](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_074_20260910/PARECER_TRANSLACAO_NORMAL_E_FRAME_074.md>) confere a construção e seus limites.

## 3. Correção de alcance: métrica e vielbein

A revisão encontrou uma ampliação indevida na alternativa inicial “métrica ou vielbein”. Na convenção se=L_c e+λe, uma mudança local de frame A(x) exige λ'=AλA⁻¹−(c·∂A)A⁻¹. Consequentemente b_Nλ=0 produz b_Nλ'=−dA A⁻¹. A mesma receita não cola sob frames locais arbitrários. A [correção de alcance para frames locais](<C:/IALD/Central de Patentes/Chatgpt/HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/PRECISAO_FRAME_LOCAL_074.md>) retira expressamente essa extensão, preservando a fonte e a correção ao lado.

O teorema permanece válido na apresentação MÉTRICA mínima efetivamente usada por Q2. Uma formulação com ghost Lorentz covariantizado exigiria outro operador e a conferência de seus comutadores. A equivalência formal anterior entre apresentações é uma rota separada; não identifica automaticamente os dois operadores.

## 4. A completação da translação está controlada

A [completação por laços e valência](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>) usa o peso já presente em Q2: um termo conectado de laço L com E pernas possui t^(E+2L−2). Anticampos contam como pernas mesmo sem propagador. Com c=tC e b_N=t⁻¹B_N, a aplicação de B_N retira uma perna, exatamente compensando a potência t⁻¹.

Assim e^±b_N preserva R_L=∏E≥0 t^(E+2L−2)P_E. Cada coeficiente recebe no máximo cinco entradas, pois o grau de forma é no máximo quatro. Para L≥1 não surgem expoentes negativos. Para uma saída truncada em t^N podem ser necessários dados até t^(N+4); preservar a série completa não significa poder truncar antes sem margem.

O [parecer independente da completação](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_COMPLETACAO_REES_074_20260910_015708_288616/PARECER_COMPLETACAO_REES_074.md>) confirma a escala simplética e o lift cotangente do sigma: o antibracket canônico normalizado não recebe um segundo fator t⁻² além da ação já normalizada. R_L é um espaço homogêneo, não uma álgebra individual sob produto ordinário. O peso de engenharia é conservado sob a homogeneidade declarada dos coeficientes.

Esse resultado paga a continuidade desta translação na classe indicada. Não demonstra que uma homotopia cohomológica posterior conserve essa classe, nem os mapas de contratermos com relações entre inserções e contatos.

## 5. Transporte positivo e contraexemplo

A nota [normalização para s e obstrução de Euler](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_E_CURVATURA_B0_074_20260910/NORMALIZACAO_S_E_OBSTRUCAO_EULER.md>), junto com a [precisão métrica e frame de referência](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_E_CURVATURA_B0_074_20260910/PRECISAO_METRICA_E_FRAME_DE_REFERENCIA.md>), demonstra um transporte condicionado: avaliar em jatos normais de B0 comuta com s porque sB0=0. Na classe formal em que cada coeficiente é tensorial e polinomial finito, a projeção algébrica no tipo trivial de Lorentz também comuta com s. Se α natural já possui primitiva coordenada β nessa MESMA completação, α=sβ implica α=sR_Nβ com primitiva natural.

Isso é um resultado para H(s). Não é uma retração para d_H. A forma de Euler do espectador E(g0) possui primitiva Chern–Simons coordenada, mas não primitiva natural universal no complexo relativo da classe regular declarada. A prova avalia em uma solução de curvatura constante, mapas sigma constantes e ghosts/antifields nulos: o termo s desaparece e uma 3-forma natural teria de ser invariante por Lorentz, portanto zero; entretanto E(g0)=24(Λ/3)²dV é não nula.

O contraexemplo pertence a ghost zero e forma quatro. Não demonstra uma anomalia de ghost um da teoria nem contradiz o resultado ordinário073. Demonstra por que normalizar e projetar uma primitiva arbitrária não fornece prova geral de exatidão natural.

Há também uma transgressão natural positiva: na vizinhança formal g=g0+h, transportar as duas conexões ao mesmo fibrado métrico dá dT=E(g)−E(g0). A diferença é removida, enquanto a classe diagonal de g0 permanece. O [parecer da raiz sobre normalização e Euler](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_074_20260910/PARECER_NORMALIZACAO_E_EULER_074.md>) confere esses resultados e o critério espectral condicionado.

## 6. Próximas obrigações

Na classe natural formal correta, precisam-se das primitivas dos graus H¹(s), H²(s), H⁵(s) e dos dois grupos com coeficientes H¹(Ebar_N;H⁴(s)) e H²(Ebar_N;H³(s)). Se os cinco canais forem nulos, a filtração finita elimina o grau total cinco. O transporte desta entrega trata primitivas de s já existentes na mesma completação; não calcula automaticamente os dois grupos horizontais com coeficientes.

A descida da anomalia também precisa permanecer natural. Trabalho exploratório posterior sobre essa descida não integra as conclusões desta entrega. Para consumir a primitiva na teoria causal, permanecem regularidade/analiticidade efetivamente exigida, cotas de escala por aridade, independência funcional dos campos, inserções marcadas, realidade e contatos. Exatidão de uma densidade não fornece toda a família de normalizações.

Depois continuam a corrente e a carga interagentes, as identidades renormalizadas/QME, acordo perturbativo e compatibilidade entre fundos/estados. A reconstrução gravitacional geral pelos mesmos dados selecionados e a rota UV continuam parte do objetivo. P0, o critério condicional da comutante e os limites da [entrega073](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_073_20260910/ADENDO_REVISOES_073.md>) são preservados. Fase, ramo, H3 interno e falsificadores existentes não são reabertos.

Os materiais devem ser integrados com seus adendos e hipóteses. A presença de nota ou índice não equivale a compilação formal ou confirmação física. O objetivo geral permanece ativo.
