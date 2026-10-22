# Revisão da composição Hadamard física Einstein–sigma

09/09/2026. **[DERIVED — análise matemática própria; REAL somente para leituras, contagens e hashes.]** Esta é uma revisão da composição e da nota TT, confrontadas com a redução S/V que deduzi anteriormente. Não constitui uma segunda autoria independente daquela redução, nem atribui aprovação ao operador ou a outra tarefa.

**Conclusão delimitada:** não encontrei uma falha concreta que invalide o enunciado tal como foi definido: estado quase livre positivo no quociente de observáveis lineares invariantes, neste fundo Einstein–sigma e neste grupo de calibre, com representante bisolução do Jacobi e frente de onda de orientação nula positiva. O documento não afirma a matriz BRST completa nem o contrato de CCR sobre todos os testes de treze componentes. A distinção é necessária e está presente.

## 1. Documentos examinados

- [Estado físico Hadamard e contratos](../HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912/ESTADO_FISICO_HADAMARD_E_CONTRATOS.md), leitura integral.
- [Ação TT e modos exatos](../MODOS_TENSORIAIS_EXATOS_20260909/ACAO_TT_E_MODOS_EXATOS.md), leitura integral.
- [Redução S/V](../REDUCAO_ESCALAR_VETOR_SIGMA_20260909_212531/REDUCAO_ADM_MODOS_FISICOS.md) e [Jacobi/Green](../QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md), fontes da derivação anterior.
- Recibos CAS TT e S/V: respectivamente 12 e 17 controles com resíduos zero, conforme leitura dos JSON. Não reexecutei CAS nem compilei Lean nesta revisão.

Os hashes medidos das versões examinadas constam do manifesto desta pasta. Nenhum documento examinado foi alterado.

## 2. Testes de falha nos modos físicos e na normalização TT

**Escalar ℓ=0.** Não existe gradiente sigma correspondente. Com H≠0, a variação homogênea do traço espacial é calibre temporal e o lapse remanescente obedece à restrição α₀=0. Esse argumento mantém c e Λ fixados como parâmetros da ação. Não permite tratar uma variação desses parâmetros como um modo físico descartado.

**Escalar ℓ=1.** Para λ=3, `Hess Y=−Yγ`, o vetor `v=x∇Y/√3 + [xY/(√3H)]∂r` preserva o corte espacial e reproduz exatamente o lapse e o shift da restrição. O cancelamento da ação reduzida é, portanto, calibre residual. Não há inversão indevida de `K_S=0`.

**Vetorial ℓ=1.** D=0 caracteriza Killing espaciais. `v=x(r)V` fornece ξ=xV e b=dot x V, mantendo a métrica espacial inalterada. Com o grupo de calibre declarado — difeomorfias suaves espacialmente compactas em Cauchy S³ — esses vetores são admissíveis. Um grupo de calibre com condições adicionais de bordo teria outro problema, que a nota não afirma resolver.

**Completude.** Em ℓ≥2, a decomposição SVT permite remover E/F e depois o traço por transformação temporal, pois H≠0. A ausência de 1-formas harmônicas em S³ exclui outro setor vetorial topológico. Os núcleos dos operadores de York nos baixos graus foram tratados, em vez de confundidos com modos físicos de cinética nula. O argumento é válido em `I×S³`, I⊂(0,π), e não transporta automaticamente a decomposição espectral para uma carta com bordo.

**TT.** Recalculei a cadeia de fatores: na curva espacial `q=γe^{εt}`, a segunda derivada de `∫√qR` em TT é `−½∫(|Dt|²+2|t|²)`. O coeficiente de ε² é metade disso. A ação gravitacional recebe `−a/(8κ)(|Dt|²+2|t|²)`. A matéria possui tensor de referência espacial γ fixo e fornece `−ca|t|²/4`, logo o termo espacial é `2+2κc=10`. A cinética é `a³|dot t|²/(8κ)`; portanto o campo canônico é `u_TT=at/(2√κ)`, e não `at/√(2κ)`. O espectro resultante é `p_TT²=(ℓ+1)²+6`. Não encontrei perda de fator dois ou substituição indevida da equação do vácuo.

O teste covariante TT também confere: `h_ij=−a²t_ij`, a medida é `dr a³`, `dr=a dη` e `t=2√κu/a`; logo `j_TT=−2√κ a⁵∫f^{ij}T_ij`. Em S/V, os dois termos simétricos de shift produzem o fator dois já incluído nos mapas.

## 3. Uma complementação explícita: corte temporal e a imagem da álgebra de testes

A nota usa corretamente a identidade de Green e a correspondência simplética. O argumento a seguir torna explícito por que os testes invariantes compactos alcançam todas as soluções físicas suaves do problema global considerado; evita deixar essa passagem dependente apenas da expressão “bijeção simplética”.

Use a notação do documento Jacobi: `H` é a Hessiana variacional, `C` o calibre de Donder, `K` o gerador de difeomorfismos, `Q=CK`, e

\[
H_{gf}=H+\frac1{2\kappa}C^*C,
\quad HK=0,\quad K^*H=0,\quad
E_{gf}C^*=2\kappa K E_Q.
\]

Se v é uma solução física suave, resolva `Qw=−Cv` com dados de Cauchy suaves; `v+Kw` representa a mesma classe e satisfaz C=0. Renomeie esse representante como v, de modo que `Hv=H_gf v=0`.

Escolha uma função suave temporal θ, igual a zero antes de uma seção de Cauchy e igual a um depois de outra, ambas interiores a I. Como S³ é compacta,

\[
F=H(\theta v)
\]

é um teste de suporte compacto: somente derivadas de θ sobrevivem, pois Hv=0. Além disso `K*F=0` pela identidade de Noether. A seção θv não tem suporte temporal compacto, logo isso não torna F automaticamente zero no quociente `ker K*/HΓ_c`.

Temos `C(θv)=[C,θ]v`, também compacto. Pela unicidade dos Green avançado/retardado, escolhendo `E_gf=G_gf^ret−G_gf^adv`,

\[
E_{gf}H_{gf}(\theta v)=v.
\]

Com efeito, θv é a solução que zera no passado, enquanto `(θ−1)v` é a que zera no futuro. Substituindo `H=H_gf−C*C/(2κ)`, segue

\[
\boxed{E_{gf}F=v-K E_Q C(\theta v).}
\]

Portanto a imagem de F é precisamente a classe física de v. Esse argumento usa compacidade espacial, a equação do fundo e as identidades de Green já demonstradas. Combinado à forma simplética reduzida não degenerada nos modos físicos, ele paga a passagem entre o quociente de testes e as soluções reduzidas, incluindo a possibilidade de uma apresentação pré-simplética com radical.

A igualdade de CCR é então efetiva: a forma de Green transportada coincide com a forma canônica S/V/TT, e o Wronskiano fornece a parte antissimétrica. Uma convenção de sinal que torna a correspondência transparente é a seguinte: a ação canônica `½∫(u'²−Ω²u²)` tem Hessiana `−P`, `P=∂η²+Ω²`; seu causal `G_{−P}^ret−G_{−P}^adv` é `G_P^adv−G_P^ret`. Para o modo `e^{-ipη}`, a diferença das covariâncias é `iℏ` vezes esse causal. Isso coincide com a convenção física da Hessiana usada nas notas. Não encontrei uma troca efetiva de sinal; a orientação já é declarada conjunta na composição.

## 4. Frente de onda dos operadores espaciais: o risco real foi tratado

Um projetor espacial não local, estendido por `δ(η−η')`, não pode ser tratado indiscriminadamente como um operador pseudodiferencial clássico em todas as covariáveis do espaço-tempo. Isso seria uma lacuna concreta se fosse o argumento usado. A nota, porém, distingue esse ponto expressamente.

Na distribuição de meia onda, as covariáveis características satisfazem `|τ|≈|ξ|` e ξ≠0. Nessa região, a parte diagonal do núcleo espacial tem a relação conormal que mantém o covetor espacial; a composição FIO preserva a relação nula orientada. A parte espacial suavizante, inclusive fora da diagonal, só poderia compor com uma covariável espacial de entrada zero, que não pertence à frente de onda da meia onda. Ela produz um termo suave nessa composição. Isso também se verifica pela expansão harmônica: um operador espacial suavizante amortiza todas as potências espectrais, inclusive as introduzidas por derivadas temporais dos modos.

Os projetores transversais/TT e os inversos elípticos em S/V têm a ordem espacial finita exigida. A esfera de curvatura constante garante invariância dos subespaços pelo laplaciano usado. A retirada de um número finito de baixos autovalores é suavizante. Não encontrei uma nova covariável temporal espúria que sobreviva a essa composição.

A inclusão de frente de onda é a afirmação adequada para a matriz de polarizações físicas reconstruída. Ela não obriga a parte singular a ser a identidade de treze componentes. A positividade resulta separadamente da forma de Gram explícita, e os CCR resultam do Wronskiano mais a redução simplética; nenhum dos três fatos foi indevidamente usado como sinônimo dos outros.

## 5. Alcance mantido, sem exigir um teorema que não foi afirmado

O representante `ΣR_AW_AR_A*` é bisolução de H porque cada reconstrução é solução do sistema linearizado; por integração por partes ele anula `HΓ_c`. Para testes invariantes, mudanças por K(v) são invisíveis. Isso dá o estado físico linear anunciado. Não é necessário impor CCR sobre testes arbitrários para validar esse enunciado delimitado.

Continuam separados:

- A matriz de covariâncias de gauge/ghost com os requisitos BRST fortes para funcionais não lineares.
- Interações, equação mestra quântica, anomalias, contra-termos e qualquer limite UV.
- Integrabilidade não linear das perturbações globais em Cauchy compacta com simetrias.
- Controle uniforme nos extremos H=0/a=0; crescimento de variáveis geométricas na contração não foi excluído pelo Hamiltoniano quadrático positivo.
- Derivação dos graus de liberdade ambiente a partir da família mínima de cinco probabilidades. O resultado de puro calibre dessa família permanece vigente.
- Identificação da álgebra global construída com uma álgebra definida sob outro grupo de calibre ou condições de bordo. A nota afirma somente a restrição à álgebra local induzida no diamante positivo.

Essas limitações já aparecem na composição examinada. Minha análise não requer que elas sejam resolvidas antes de registrar o avanço físico linear mais restrito. A conclusão honesta é uma construção escrita específica de estado físico positivo e microlocal neste modelo linearizado, não uma prova de uma teoria quântica completa.
