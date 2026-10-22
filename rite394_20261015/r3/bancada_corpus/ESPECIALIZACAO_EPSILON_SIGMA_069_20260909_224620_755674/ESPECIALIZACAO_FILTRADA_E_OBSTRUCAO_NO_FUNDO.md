# Especialização ε=1, contagem de valência e o fundo físico — arco 069

09/09/2026. [DERIVED — demonstrações escritas] [KNOWN — referências primárias delimitadas]. Nota nova; a fonte BV 068 e todas as fontes anteriores permanecem congeladas.

**Resultado:** a contagem de pernas e laços fornece um limite finito de grau ε para diagramas da expansão no vácuo escalar constante. Uma propriedade adicional de exatidão filtrada permite aplicar esse limite às primitivas e especializar ε=1 como série formal nos campos em torno desse vácuo. Demonstra-se também que esse mecanismo não autoriza recentrar tais primitivas no fundo físico φ̄=id: a substituição formal pode ser indefinida e a tentativa analítica pode divergir, mesmo com aumento de grau e homotopia preservando a filtração. No sigma físico, os jatos de fundo geram ainda vértices quadráticos dependentes de ε. Isso não é uma anomalia calculada; é uma obstrução ao argumento de transporte proposto.

**Encaminhamento:** construir a expansão quântica diretamente em torno de (ḡ,φ̄=id), no parâmetro de flutuações λ, é matematicamente compatível com coeficientes locais finitos. A nulidade de H¹ do sigma deve ser demonstrada no complexo correspondente ou obtida por uma homotopia regular no fundo físico; não é herdada da prova ε-ádica por mera contagem de valência.

## 1. O resultado formal que já existe

A [nota BV 068](<C:/IALD/Central de Patentes/Chatgpt/BV_ANOMALIAS_SIGMA_FORMAL_20260909_215557/BV_LOCAL_SIGMA_E_RENORMALIZACAO_CONDICIONAL.md>) define

\[
h_{AB}(\varepsilon,y)=\delta_{AB}+
 \frac{\varepsilon y_Ay_B}{1-\varepsilon q},\qquad q=|y|^2<1,
\]
\[
S_m=\frac c2\int\mu_g\,q^{m-1}g^{\mu\nu}
 (y\cdot\partial_\mu y)(y\cdot\partial_\nu y),\quad m\ge1,
\]

e prova a recorrência cohomológica em ε, condicionada à referência C0. O coeficiente S_m tem precisamente 2m+2 ocorrências escalares, contando derivadas de y como ocorrências de y. A série formal completa pode ter primitivas de ordem de jato e valência crescentes; a própria nota não a especializa automaticamente.

[KNOWN] Em [BBH 2000, §§4.7 e 5.3](https://arxiv.org/pdf/hep-th/0002245), a igualdade das séries formais é coeficiente a coeficiente; o resultado de Koszul–Tate formal não afirma convergência. O §6.4.3 distingue também a resolução formal do controle adicional de localidade. Esses resultados justificam o tipo de álgebra empregado, sem decidir a especialização física em discussão.

## 2. Lema exato de contagem de valência

Considere um grafo conectado, com V vértices, I arestas internas e E pernas externas. Seja v_i o número total de pernas no vértice i. Tadpoles internos e linhas fantasmas obedecem à mesma contagem combinatória. Para o número de laços topológico L=I−V+1,

\[
\sum_i v_i=2I+E,\qquad
\boxed{\sum_i(v_i-2)=E+2L-2.}\tag{2.1}
\]

Isso segue diretamente de contar as extremidades de cada aresta; não depende de uma hipótese de renormalizabilidade.

No vácuo ȳ=0 constante, um vértice originário de ε^m S_m e de grau k no gráviton tem v_i=2m+2+k, logo 2m≤v_i−2. Os vértices de referência têm m=0. Após absorver a parte quadrática no propagador e expandir em torno de um fundo on-shell, os demais vértices gravitacionais e de calibre têm valência ao menos três. A gravidade não linear acrescenta pernas; não reduz a valência escalar mínima dos vértices S_m. Portanto, quando todos os vértices satisfazem essa atribuição,

\[
\boxed{M:=\sum_i m_i\le L+\frac E2-1.}\tag{2.2}
\]

Assim o grau ε dos diagramas com L e E fixos é finito. Para E=4,L=0, por exemplo, só M≤1 pode contribuir. Para E=2,L=1, só M≤1. Não se conclui um número máximo de pernas a todos os processos ou em toda a ação efetiva.

Há uma versão útil para vértices que já contêm contra-termos. Atribua a cada vértice o peso quântico ℓ_i≥0 e suponha

\[
2m_i\le v_i+2\ell_i-2.
\]

O peso total em ħ é L_tot=I−V+1+Σℓ_i. Somar as desigualdades dá 2M≤E+2L_tot−2. Logo a condição é preservada ao contrair subgrafos e representá-los por vértices de contra-termo com o peso correto. Isso fornece um critério concreto para uma prescrição de renormalização preservar o limite.

**Limite desta aplicação:** a contagem não demonstra que uma renormalização finita escolhida para remover uma anomalia preserve tal desigualdade. Inserções marcadas de Ward, antifields e observáveis devem receber seus próprios pesos e limites; não se presume que a fórmula de um grafo sem inserção seja automaticamente a fórmula de toda quebra BV. Constantes da ação e termos lineares de um fundo off-shell também não devem ser tratados como vértices de interação de valência ≥3.

## 3. Teorema de especialização diagonal, com hipótese filtrada explícita

Trabalhe no complexo de formas locais modulo d, completado pelo grau total de campos, ghosts e antifields em torno de um fundo fixado. Denote por F^p os elementos sem componentes de grau menor que p; para p≤0 ponha F^p=\mathcal A. Pressupõe-se completude, separação e continuidade dos diferenciais nessa filtração, com localidade finita em cada coeficiente.

Suponha:

1. s_ref preserva F^p, e s_m F^p⊆F^{p+2m} para m≥1;
2. cada cociclo de ghost 1 em F^p que ocorre na recorrência admite uma primitiva de ghost 0 ainda em F^p, na mesma classe admissível e modulo d;
3. a=Σ ε^n a_n é um cociclo de s_ε e a_n∈F^{2n+w}, para um inteiro w fixado.

A condição 2 é exatidão com controle da filtração. Uma homotopia local preservando F é um certificado suficiente. H¹(s_ref)=0 sem controle de grau não a fornece por definição.

**[DERIVED] Teorema.** Sob essas hipóteses, a recorrência pode escolher b_n∈F^{2n+w}, com a=s_εΣ ε^n b_n. Logo ε=1 pode ser avaliado coeficiente a coeficiente na conclusão formal em campos, e

\[
\sum_n a_n=s_\sigma\left(\sum_n b_n\right),\qquad
s_\sigma=s_{\rm ref}+\sum_{m\ge1}s_m.
\tag{3.1}
\]

**Prova.** Admitindo os b_j anteriores, o resto de ordem n é

\[
r_n=a_n-\sum_{m=1}^n s_m b_{n-m}.
\]

Cada parcela pertence a F^{2n+w}. Pela nilpotência, s_ref r_n=0; a condição 2 fornece b_n no mesmo F^{2n+w}. A indução começa em n=0. No quociente de graus ≤D, somente n≤⌊(D−w)/2⌋ podem contribuir. Todas as somas e produtos necessários para (3.1) são, portanto, finitos nesse quociente. Completude e separação dão a identidade em toda a conclusão formal. □

O cone de valência de ghost zero sugerido por (2.2), a ordem quântica L fixa, é w=2−2L. Para uma anomalia ou inserção deve-se conferir a correspondente escolha de w. O teorema paga a operação de especialização para cociclos compatíveis que possuam esse levantamento ε-ádico; não afirma que qualquer cociclo de s_σ admita automaticamente um levantamento a(ε).

No fundo escalar constante ȳ=0, a substituição de y† por δS_m/δy tem ao menos 2m+1 campos e aumenta o grau total em ao menos 2m. A substituição de g† por δS_m/δg tem ao menos 2m+2 escalares e aumenta o grau em ao menos 2m+1. Os geradores de gauge não são deformados. Esse cálculo verifica a primeira parte da condição 1 relativa aos s_m. Para s_ref preservar o grau, o fundo de referência deve ser on-shell; para pagar a condição 2 ainda é necessária a construção filtrada da referência. Essa homotopia Einstein–escalar não foi construída nesta nota.

[KNOWN] O requisito adicional é compatível com o lema de perturbação homológica: a inversibilidade de 1−δh é uma hipótese concreta, e versões topológicas precisam de controle da homotopia. Veja [Crainic, §§2.2, 3.7 e 3.8](https://arxiv.org/pdf/math/0403266). O teorema acima usa a finitude por grau para demonstrar a operação pertinente; não usa uma norma pequena presumida em ε=1.

## 4. Por que o fundo φ̄=id não satisfaz essa contagem automaticamente

O fundo físico é o da [construção global 068](<C:/IALD/Central de Patentes/Chatgpt/GLOBALIZACAO_PROBABILIDADES_S3_20260909_220238_785086/PROVA_GLOBAL_S3_ASSINADA_E_LIVRE.md>): M=(0,π)×S³, ḡ=dr²−a²γ e φ̄(r,z)=z. Em uma carta hemisférica escreva y=ȳ+η. Os valores de ȳ e seus jatos têm grau zero na expansão em η.

Escolha um ponto da carta onde ȳ=(b,0,0), 0<|b|<1. O coeficiente da parte principal quadrática (∂η¹)² contém

\[
h_{11}(\varepsilon,\bar y)=\frac1{1-\varepsilon b^2}
 =\sum_{m\ge0}\varepsilon^m b^{2m}.
\tag{4.1}
\]

Portanto todos os m ocorrem já com duas pernas de flutuação. Esse coeficiente pode ser isolado no jato da flutuação tomando η=0 no ponto e variando ∂η. A presença de outros jatos de fundo não cancela essa identificação da parte principal. A antiga afirmação v≥2m+2 deixou de valer para a valência em η.

Mesmo centralizar uma coordenada normal no valor φ̄ de um ponto não apaga os jatos dφ̄. Diretamente no vértice S₁, quando ȳ=0 nesse ponto e d ȳ≠0, surge o termo quadrático

\[
\varepsilon\,g^{\mu\nu}
 (\eta\cdot\partial_\mu\bar y)(\eta\cdot\partial_\nu\bar y).
\tag{4.2}
\]

Na expansão covariante, o mesmo fenômeno aparece no termo de Jacobi com curvatura do alvo e dφ̄. Uma inserção quadrática dependente de ε pode repetir-se arbitrariamente em uma cadeia de propagadores com E e L fixos. Absorver esse termo no propagador completo é permitido, mas passa a usar um sistema livre dependente de ε; não demonstra o limite de grau das primitivas construídas a partir da referência ε=0.

Além disso, o mesmo par (ḡ,φ̄=id) não é presumido on-shell na referência plana. No habitante, em coordenadas projetadas y^A=z^A, vale Box_ḡ y^A=3y^A/a², enquanto a equação do alvo plano é Box y=0. Assim o termo constante de s_ref y† não desaparece em geral nesse fundo e pode baixar a filtração de flutuações. A coerência on-shell em ε=1 não soluciona esse problema em ε=0.

## 5. Obstrução explícita à mudança do centro formal

Este controle é um complexo linear abstrato; não é apresentado como o complexo BV do sigma ou como uma anomalia física.

Tome \(\mathcal C^0=\mathbb R[[x]]u\), \(\mathcal C^1=\mathbb R[[x]]v\), e zero nos demais graus. Defina

\[
D_\varepsilon(fu)=(f-\varepsilon x^3\partial_x f)v,
\qquad D_\varepsilon|_{\mathcal C^1}=0.
\tag{5.1}
\]

D_ε²=0 por construção; D₀=Id entre os dois termos e H¹(D₀)=0. A homotopia referência é Id de grau 1 a 0, preservando o grau em x. A perturbação x³∂_x aumenta o grau em dois. Todas as condições de finitude formal relevantes do teorema anterior se verificam para o cociclo a=xv.

A equação D_ε B=xv dá b₀=x e b_m=x³∂_x b_{m−1}, logo

\[
B(\varepsilon,x)=\sum_{m\ge0}(2m-1)!!\,
 \varepsilon^m x^{2m+1}u,\qquad (-1)!!=1.
\tag{5.2}
\]

A recorrência determina essa solução formal em ε univocamente. Cada coeficiente é um polinômio local de ordem zero em jatos, e o grau 2m+1 cresce exatamente como requerido. Portanto B(1,x) existe em R[[x]] e D₁ B(1,x)=xv é uma identidade formal válida.

Agora tente deslocar o centro: x=b+η, b real não nulo. Tal substituição não define, em geral, um morfismo contínuo R[[x]]→R[[η]]: a imagem de x não pertence ao ideal maximal (η). Aqui o coeficiente de η⁰ exigiria explicitamente

\[
\sum_{m\ge0}(2m-1)!!\,b^{2m+1}.
\]

A razão absoluta entre termos consecutivos é (2m+1)b² e tende a infinito; os termos não tendem a zero. A tentativa de soma analítica diverge para todo b≠0. Mesmo uma homotopia preservando a filtração e um diferencial polinomial no parâmetro não garantem que a primitiva formal possa ser recentrada num valor de campo não nulo.

Isso prova a insuficiência do argumento, sem provar inexistência de alguma solução suave obtida por outro método no novo centro. Não há uma afirmação de salto de H¹ do sigma. O controle foi conferido independentemente por outro agente desta mesma tarefa, com concordância limitada a (5.1)–(5.2) e à impossibilidade da substituição formal; não se atribui aprovação externa.

## 6. O que converge classicamente e o que ainda precisa de controle

Na família clássica, a série pode ser somada explicitamente. Para h^(N)=I+Σ_{m=1}^N q^{m−1}yyᵀ, em ε=1,

\[
h_1-h^{(N)}=\frac{q^N}{1-q}yy^T,
\qquad \|h_1-h^{(N)}\|_{\mathrm{op}}=
 \frac{q^{N+1}}{1-q}\le\frac{\rho^{N+1}}{1-\rho}
\tag{6.1}
\]

quando 0≤q≤ρ<1. Essa é uma estimativa uniforme concreta no compacto da carta. Não há, nas fontes revistas, estimativa análoga para os b_m da recorrência cohomológica. A regularidade explícita de h_ε não limita o crescimento dos coeficientes da homotopia nem preserva automaticamente naturalidade, ordem de jato, normalidade ou compatibilidade entre cartas.

Uma rota analítica suficiente teria de construir primitivas com estimativas somáveis, juntamente com as derivadas de campo/jato exigidas na classe de contra-termos e com as transições de carta. Uma rota algébrica alternativa seria uma homotopia direta nos germes do sigma físico, mantendo coeficientes admissíveis regulares em torno dos jatos de φ̄=id. Ambas são resultados adicionais mensuráveis; nenhuma é inferida de (6.1).

## 7. Expansão direta no fundo físico: resultado positivo independente de ε

Há uma construção clássica global da série de flutuações que evita trocar o centro de uma primitiva formal. Ponha ξ∈Γ(φ̄*TS³), isto é, ξ·φ̄=0, e r_ξ²=ξ·ξ. A exponencial da esfera unitária é

\[
\phi_\lambda=\operatorname{Exp}_{\bar\phi}(\lambda\xi)
 =\cos(\lambda r_\xi)\bar\phi+
 \frac{\sin(\lambda r_\xi)}{r_\xi}\xi.
\tag{7.1}
\]

A razão sin(λr)/r é tomada por sua extensão regular em r=0. Os coeficientes são globais e polinomiais em ξ:

\[
\phi_\lambda=
\sum_{n\ge0}\frac{(-1)^n\lambda^{2n}}{(2n)!}
 (\xi\cdot\xi)^n\bar\phi+
\sum_{n\ge0}\frac{(-1)^n\lambda^{2n+1}}{(2n+1)!}
 (\xi\cdot\xi)^n\xi.
\tag{7.2}
\]

Não é preciso escolher uma carta positiva única nem um frame global para o fibrado tangente. A derivação em espaço-tempo produz, em cada grau λ, um número finito de contrações em ξ, ∂ξ e nos dados suaves φ̄,∂φ̄. Com g_λ=ḡ+λh, a inversa formal da métrica é uma série geométrica em λḡ⁻¹h e o volume tem expansão formal regular em torno da métrica não degenerada. Cada coeficiente da ação Einstein–sigma é local de ordem finita de jato. No fundo on-shell, a primeira variação da ação se anula para perturbações compactas, modulo borda, e a parte quadrática é o sistema livre do fundo físico.

[KNOWN] A organização de gravidade perturbativa em um parâmetro formal de flutuações e a exigência on-shell para o sistema livre são explicitadas em [Brunetti–Fredenhagen–Rejzner, §3.2](https://arxiv.org/html/1306.1058v4). A fórmula sigma global acima é uma construção direta para o fundo em questão; não importa da gravidade pura um teorema de anomalias para matéria acoplada.

Essa rota paga a existência dos coeficientes clássicos dos vértices no fundo φ̄=id e permite formular Q2 diretamente ali. Ela não é ainda a construção de todos os produtos temporais renormalizados nem fornece uma homotopia de H¹. λ, ε e ħ têm papéis distintos; colocar ε=1 na geometria clássica antes de construir a expansão λ não demonstra a especialização das primitivas ε-ádicas anteriores.

A comparação quântica entre fundos também continua separada: [Taslimi Tehrani–Zahn, §4](https://arxiv.org/html/1804.07640) identificam condições adicionais de fundo na gravidade perturbativa. Aqui não se presume que o transporte entre dois centros formais seja automático.

## 8. Resultado operacional e limite final

Para a sessão que codifica:

- [DERIVED] Conservar a identidade de valência (2.1), o limite (2.2) e sua versão com pesos de contra-termos como lemas combinatórios, com as hipóteses de vértices tipadas.
- [DERIVED condicional] O teorema da seção 3 autoriza especialização ε=1 na conclusão formal em torno do mesmo vácuo, se a homotopia/exatidão filtrada for fornecida. Essa hipótese ainda não foi paga para Einstein–escalar nesta nota.
- [DERIVED] No fundo φ̄=id, as condições de valência e de preservação da filtração pela referência não seguem das do vácuo. O controle da seção 5 impede promover a prova formal por simples mudança de centro.
- [DERIVED] A expansão covariante direta (7.1)–(7.2) existe globalmente sobre o fundo físico e tem coeficientes locais finitos. É uma base apropriada para formular a construção perturbativa nesse fundo.
- [OPEN] Demonstrar H^{1,4}(s_σ|d) na classe física admissível, ou produzir uma homotopia/somatória regular que realmente transporte as primitivas e seus contratos. A contagem de valência isolada não fecha essa obrigação.

A decisão sustentada é abandonar o atalho ε→1 como prova do caso φ̄=id, preservando o resultado formal condicionado no vácuo e trabalhando diretamente no sigma físico. Não se apresenta anomalia sigma efetiva, refutação do modelo, confirmação observacional ou conclusão sobre UV.

## 9. Custódia

Somente esta pasta nova recebeu o texto e o manifesto. Nenhum arquivo existente, memória canônica, Atlas ou gate foi alterado. Nenhum um.py foi importado/executado; nenhum Lean, CAS ou cálculo de diagramas foi executado nesta frente. As demonstrações combinatórias, formais e a estimativa (6.1) são escritas. Os pins abaixo foram lidos do disco, nunca reconstruídos de memória.

- `C:/IALD/Central de Patentes/Chatgpt/BV_ANOMALIAS_SIGMA_FORMAL_20260909_215557/BV_LOCAL_SIGMA_E_RENORMALIZACAO_CONDICIONAL.md` — 25611 bytes; SHA-256 `14f18119239fe1bd9971a6860dc094efb9fd4c201b43eb5211532373bf7b4da8`.

- `C:/IALD/Central de Patentes/Chatgpt/GLOBALIZACAO_PROBABILIDADES_S3_20260909_220238_785086/PROVA_GLOBAL_S3_ASSINADA_E_LIVRE.md` — 19874 bytes; SHA-256 `628b9e031d42094e0cdf3486a960530e38400a21fe82923eefca0bcbc2286d19`.
