# Revisão independente087 — aciclicidade CE do setor linear de Weyl

10/09/2026. Revisor: /root/finish_gibbs_realization. [DERIVED — revisão matemática escrita]. [KNOWN — importação primária finita conferida]. [REAL — custódia documental no recibo]. Nenhum cálculo matemático, CAS, Lean ou um.py foi executado nesta revisão.

**Parecer:** não identifiquei erro material no alcance declarado. A nota demonstra que todas as formas horizontais naturais LINEARES de Weyl/EOM são zero e, com uma etapa adicional válida, que todo o complexo CE invariante pela isotropia com coeficientes N₁ é acíclico. A aplicação ao primeiro diferencial BRST conserva m=E−gh=1. Isso não afirma que as cocadeias ou H(s₀) sejam zero, nem calcula o BRST completo.

Li integralmente [ACICLICIDADE_CE_LINEAR_E_PRIMEIRO_DIFERENCIAL.md](<C:/IALD/Central de Patentes/Chatgpt/CE_LINEAR_WEYL_TODOS_GRAUS_087_20260910/ACICLICIDADE_CE_LINEAR_E_PRIMEIRO_DIFERENCIAL.md>) e o [manifesto de origem](<C:/IALD/Central de Patentes/Chatgpt/CE_LINEAR_WEYL_TODOS_GRAUS_087_20260910/MANIFESTO_CE_LINEAR_087.json>). A fonte final possui14.905 bytes, conforme o pin novamente medido no recibo. O exame abaixo é da nova prova de Herschel para N₁; minha investigação quadrática N₂ não é utilizada para demonstrá-la.

## 1. O contrato efetivamente necessário

Conserve a referência espaço-forma orientada Lorentziana de dimensão quatro, K>0 e κ≠0 reais já fixados, sigma constante projetado ao setor métrico e anel Rher real unital não nulo inerte. Todos os produtos são algébricos; cada expressão usa finitos jatos. Não há coeficientes tensoriais externos, dependência coordenada arbitrária ou ghosts adicionais em Rher.

Mcal=kerγ/E é o módulo linear efetivo de jatos métricos gauge-fechados pelas EOM e seus prolongamentos. N₁=Rher⊗Mcal. O resultado não depende de Mcal ser livre nem de se poder prescrever arbitrariamente jatos de Weyl curvos. É uma afirmação no próprio quociente linear efetivo.

A [estriteza086](<C:/IALD/Central de Patentes/Chatgpt/SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md>) fornece a injeção graduada de ordem r+2 no módulo plano maior (r+4,r)⊕(r,r+4), em pesos inteiros2j, e a nulidade dos graus inferiores a dois. O uso dessa injeção na presente nota é suficiente; ela não foi promovida a uma sobrejeção ou a uma identificação de todas as relações curvas.

Minha revisão específica086 desse antecedente foi consumida como registro anterior. O presente parecer não se apresenta como nova revisão independente de si mesmo. Ele verifica como a nova prova linear utiliza aquele resultado.

## 2. Ausência de Bᵖ linear: a contagem realmente passa ao quociente curvo

Os tipos de ΛᵖV* para p=0,…,4 são, respectivamente, (0,0), (1,1), (2,0)⊕(0,2), (1,1), (0,0). A tabela da fonte está correta para a dimensão e orientação fixadas. A autodualidade das representações finitas de sl₂⊕sl₂ transforma a pergunta por um invariante em M⊗ΛᵖV* na pergunta pela presença do respectivo tipo em M.

Os tipos de Weyl e de seus jatos principais têm diferença absoluta de pesos igual a quatro. Todos os tipos de formas exteriores nessa tabela têm diferença zero ou dois. Portanto nenhum deles pode fornecer um invariante, para qualquer r≥0 e qualquer p permitido.

Conferi o passo que impede usar apenas uma contagem formal plana. Um elemento curvo não nulo e finito possui um menor grau de filtragem que o contém. Seu símbolo nesse grau é não nulo. Se o elemento é h-invariante, o símbolo também é. Tensorizar a injeção086 por ΛᵖV*, finito-dimensional, injeta esse símbolo no espaço plano sem invariantes. Isso é uma contradição. A complexificação é fiel e a conclusão retorna aos reais.

Assim Bᵖ=(Mcal⊗ΛᵖV*)^h=0 para todos p=0,…,4. Não foi necessário que a operação de tomar invariantes produzisse uma sobrejeção de graduados; para esse argumento basta que um símbolo invariante não nulo permaneça não nulo na injeção.

O resultado não anula Mcal: Weyl com seus quatro índices livres continua sendo um tensor não nulo. Tampouco anula cocadeias completas, pois os ghosts de isotropia acrescentam tipos de representação. O exemplo W_abcd pᵃpᵇθᶜᵈ, discutido na linhagem080, pertence à cocadeia com grau horizontal dois e vertical um. Sua existência não contradiz Bᵖ=0. A nota distingue esses objetos expressamente.

## 3. Chevalley–Eilenberg: importação finita e aplicação à isotropia

Conferi diretamente o texto original de [Chevalley–Eilenberg1948, §23 e Teorema24.1, pp.115–119](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/chev-eilen.pdf). A definição de coeficientes do §23 exige dimensão finita. O Teorema24.1 prova nulidade em todos os graus para uma representação irredutível não trivial de álgebra semissimples em característica zero. A prova algébrica produz uma primitiva mediante um operador invertível associado à representação.

A nota aplica esse resultado a h=so(1,3), não à álgebra g inteira com seu módulo infinito de jatos. Para p fixo, E_p=Mcal⊗ΛᵖV* é uma união de cortes finitos estáveis sob h. A ação de isotropia preserva a ordem dos jatos. Qualquer corte é um submódulo de E_p; como E_p^h=0 pelo §2, nenhum corte contém representação trivial. A completa redutibilidade finita de h permite aplicar o teorema a cada somando irredutível não trivial.

Os fatores de normalização das cocadeias no texto histórico não são utilizados para reescrever os sinais da ação082. Reescalar as identificações das cocadeias por constantes reais não nulas ou usar a apresentação consistentemente oposta da álgebra não muda a nulidade da cohomologia. O diferencial concreto usado na nota continua sendo o da ação082/084, com seus shuffles e termo de curvatura.

Há um segundo requisito: a primitiva deve continuar h-invariante. Num corte finito, d₀ é h-equivariante. A sobrejeção de cocadeias sobre sua imagem admite cisão h-equivariante por completa redutibilidade. Aplicar essa cisão a um ciclo invariante dá uma primitiva invariante dentro do mesmo corte. Esse argumento está explicitado e é suficiente. Não há média sobre o grupo Lorentz não compacto nem necessidade de escolher uma primitiva g-invariante.

Como Λʳh* é finito-dimensional, toda cocadeia tem finitamente muitos coeficientes, todos contidos em algum corte. A primitiva vertical obtida nesse corte é uma combinação finita. Isso paga a aciclicidade de cada coluna vertical no limite DIRETO algébrico. Não envolve inverso limite ou uma hipótese de Mittag–Leffler.

A cohomologia H³(h,R), com suas duas classes de Cartan, não foi declarada zero. Para os coeficientes desta coluna, a componente trivial que poderia multiplicá-la está ausente. A diferença entre esses dois enunciados é mantida na fonte.

## 4. A eliminação horizontal conserva o diferencial completo

O CE da referência simétrica se escreve d=d₀+d_hor+d_curv, com bidegraus (0,1),(1,0),(2,−1). Essa decomposição é a da [identificação082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>) e da [redução084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>). O termo de curvatura que troca θ por Kpp é mantido. A prova usa d²=0, sem afirmar d_hor²=0 sobre toda cocadeia não horizontal.

Se Q é ciclo e p é seu menor grau horizontal presente, a componente inicial da equação dQ=0 é d₀Q_(p,q−p)=0, porque todos os termos que poderiam chegar de graus horizontais inferiores são zero. Se o grau vertical r=q−p é positivo, a aciclicidade da coluna fornece R_(p,r−1) com d₀R=Q_(p,r).

Subtrair dR com o diferencial COMPLETO elimina precisamente a componente de grau horizontal p. As demais parcelas da subtração ficam em p+1 ou p+2. O novo elemento é ciclo por d²=0 e não adquire termos de grau menor que p. Os sinais adicionais ficam nos próprios d_horR e d_curvR; não são zerados por uma decisão externa.

O caso r=0 foi tratado corretamente: H⁰ da coluna é zero e não tem fronteiras provenientes de grau−1. Logo a componente inicialmente fechada já é zero. Não se tenta construir uma primitiva de ghost vertical negativo. Isso inclui o grau total zero.

Repetir esse procedimento percorre no máximo os cinco valores horizontais0,1,2,3,4. A soma das primitivas escolhidas satisfaz Q=dR_total. Se p+1 ou p+2 ultrapassa quatro, a parcela desaparece pela álgebra exterior dos quatro ghosts de translação. Não resta uma cauda não controlada de correções por curvatura.

Cada etapa vertical é realizada em corte finito; as aplicações horizontais acrescentam apenas finitos jatos. Um número finito de etapas conserva essa propriedade. Não se exige uma cota uniforme de ordem para todos os ciclos. Essa demonstração direta paga a convergência que, na linguagem de sequência espectral, aparece como E₁=0 numa filtração finita de comprimento cinco.

Os graus negativos e maiores que dez são zero por definição do complexo CE de uma álgebra de dimensão dez. Nos graus restantes, a eliminação prova aciclicidade; não é uma suposição baseada apenas na dimensão dos ghosts.

## 5. Rher e naturalidade das primitivas

O argumento de extensão escalar está correto. Um elemento do produto tensorial ALGÉBRICO contém somente finitos coeficientes herdados. Escolher uma base real do subespaço por eles gerado separa a identidade em finitíssimas identidades reais. Como a ação e o diferencial são inertes nesses coeficientes, as primitivas reais se recompõem numa primitiva sobre Rher.

Essa separação linear não é uma avaliação numérica por homomorfismos do anel. Não apaga nilpotentes nem usa que Rher seja domínio. Equivalentemente, a exatidão dos mapas reais é preservada ao tensorizar sobre o corpo R.

As cisões verticais são equivariantes sob h e ocorrem nos módulos tensoriais finitos da referência fixa. Nesse domínio homogêneo, continuam na classe natural. Não foi afirmado que a mesma escolha resolveria naturalidade em um catálogo universal de fundos, com tensores espectadores ou coeficientes espaciais ativos.

A restrição a elementos finitos também é essencial. A prova não calcula o complexo completado em que uma única cocadeia tenha infinitos jatos. Tampouco mostra, apenas por esse argumento, que as primitivas satisfaçam todas as condições adicionais de uma classe causal de contratermos. A nota deixa essas obrigações abertas.

## 6. O que efetivamente desaparece na primeira página BRST

Reli a [generalização085](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIRA_PAGINA_TODOS_GRAUS_085_20260910/COHOMOLOGIA_S0_GERAL_E_INVARIANTES_POSITIVOS.md>), em especial sua fórmula(1) e a identificação por derivação nos geradores. Para m=E−q=1, ela identifica a cadeia Hᵠ(s₀)|_(E=q+1), com o primeiro diferencial induzido por s₁, ao CE da nota.

Esse d₁ aumenta ghost e valência de um e conserva m=1. Ele é o CE COMPLETO, não somente d_hor. Portanto sua aciclicidade significa que todo ciclo de d₁ nessa diagonal é imagem de d₁ do grau precedente. A fonte escreve o domínio da primitiva com E=q e ghost q−1, o que preserva m=1.

Não se segue que Hᵠ(s₀)|_(E=q+1) seja zero como espaço. Suas cocadeias e candidatos podem ser não nulos e deixar de sobreviver ao primeiro diferencial. Não se segue também que todas as classes de m=0 ou m=2 desapareçam. A nota declara explicitamente essas diferenças.

Escolher representantes e correções s₀-exatas no BRST utiliza a comparação085 já existente; o cálculo CE não é uma autorização para descartar s₂,s₃,… na álgebra inteira. A conclusão é sobre a cohomologia do primeiro diferencial, não sobre H(s₀+s₁+s₂+⋯).

## 7. Parecer, independência e custódia

[DERIVED] Parecer favorável delimitado: a cadeia “injeção graduada → ausência de formas lineares → colunas verticais acíclicas → eliminação horizontal finita” é coerente. A referência primária foi utilizada com suas hipóteses finitas efetivamente satisfeitas. Não há exigência disfarçada de ausência de Killing, liberdade da torre curva ou local finitude sob g.

Esta revisão trata a nova prova de N₁, de autoria de Herschel. A prova086 de estriteza e meu parecer anterior são antecedentes; minha nota087 de N₂ não foi usada para validar o resultado linear. Nenhuma aprovação é atribuída ao operador ou a outro agente por este texto.

[REAL — documental] O recibo mede a nota, o manifesto, sete antecedentes e os dois arquivos auxiliares pinados pela origem. O emissor da origem não foi executado; sua medição de bytes não é apresentada como auditoria integral de código. Os paths com separadores Windows duplicados registrados no JSON são resolvidos como paths locais antes da comparação; os hashes e tamanhos são comparados efetivamente, sem inferir igualdade por nome.

Os17 controles do manifesto de origem são documentais. A contagem desta revisão, igualmente documental, está no recibo próprio e não é somada a testes matemáticos. Os pins apontam para caminhos finais existentes. A primária web não recebeu um hash de PDF local inexistente.

Zero matemática executada, CAS, Lean, programa canônico ou ritos de natureza. Nenhum original, fonte congelada, Atlas, memória canônica, selo ou gate foi alterado. Permanecem fora do parecer: outros fundos, setores superiores, contratermos causalmente admissíveis, QME, anomalia física, reconstrução geral e UV.
