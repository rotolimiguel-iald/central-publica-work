# Parecer independente — setor quadrático sem derivadas 082

[DERIVED — revisão matemática delimitada]. [REAL — leitura integral da nota e dos scripts, conferência estática e pins medidos]. Não identifiquei erro material no teorema do setor especificado. A fonte examinada é [IMAGEM_DO_DETECTOR_NO_SETOR_FINITO.md](<C:/IALD/Central de Patentes/Chatgpt/SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779/IMAGEM_DO_DETECTOR_NO_SETOR_FINITO.md>), com seu manifesto, script aritmético, recibo e proveniência.

Esta revisão é separada da entrega 081. Não executei os scripts examinados, o cálculo aritmético, Lean ou um.py; não recapturei arquivos canônicos. O novo código desta revisão somente lê bytes, analisa AST, compara registros e grava estes arquivos novos.

## 1. Domínio e exaustividade realmente demonstrada

O setor tem dois fatores de Weyl linearizado SEM derivadas e três fatores do módulo residual G = V ⊕ Λ²V. A referência é fixada: quatro dimensões, assinatura (+---), orientação escolhida, K = 1/ℓ², z0 = ℓ, κ real fixado não nulo e φ0 constante. Rher consiste nos escalares inertes herdados; os coeficientes das cocadeias são os mesmos quando k varia. Não são permitidos coeficientes tensoriais externos nem dependência do parâmetro da perturbação como nova entrada.

Refiz a contagem que sustenta os dez emparelhamentos. Sobre a complexificação, se W+ = (4,0) e W− = (0,4), então Sym²W+ = (8,0) ⊕ (4,0) ⊕ (0,0), e analogamente para W−; o produto cruzado é (4,4). Em Λ³G, somente as quatro cópias do escalar e as cópias únicas (4,0), (0,4) se sobrepõem. Logo a dimensão do espaço de invariantes é 2×4 + 1 + 1 = 10. Os outros tipos não produzem escalares. Aqui os números são pesos inteiros 2j.

A lista explícita realiza essa contagem, em vez de usar a representação como substituto de uma construção. Em Λ²V ⊗ Λ²V há os dois escalares βe e βo. Em Λ³(Λ²V), as duas cúbicas independentes são γe e γo: após decompor a álgebra Lorentz complexificada nos dois fatores de dimensão três, são as duas formas de volume de Cartan; traço e traço com estrela dão combinações reais independentes. Não há escalares nos setores C³ ou C m². As duas distribuições de graus C²m e m³ separam os pares.

Os oito produtos escalares são portanto independentes no espaço de contrações. A projeção quadrática de tipo Weyl é não nula: para o Weyl elétrico diagonal (1,−1,0), a parte sem traço do quadrado é proporcional a (1,1,−2). A projeção e seu dual realizam as duas combinações reais correspondentes. As identidades algébricas adicionais do complexo podem reduzir a imagem cohomológica, mas não acrescentam candidatos a este setor. Não se conclui que esses dez sejam uma base de H³(s0)E5.

## 2. Sinais das cúbicas e da avaliação

A fonte fixa M^a_b = g0^{ac}m_cb e m_ab = ∇bar_[a C_b], com fator 1/2. Para Killing, M = −A, onde A^a_b = ∇bar_b C^a. Mantive esse sinal; não se deve transportar a notação M de outra fonte que a defina como A.

Na avaliação especificada, m^{i3} = −θi/z0 e m^{3i} = +θi/z0. O Hodge aplicado ao tensor covariante, seguido da elevação de índice, satisfaz *² = −1. Refiz os três termos que contribuem para tr((*M)M²): cada um vale +2 θ012/z0³. Assim γo = +6 θ012/z0³, enquanto βo = −6 θ012/z0. βe e γe se anulam nessa avaliação, não universalmente.

Os quatro Killing fecham e induzem dθ θi = θi θ3/z0, i = 0,1,2, com dθ θ3 = 0. Pela regra graduada, dθ(θ012) = 3 θ0123/z0. Resultam precisamente −18 θ0123/z0² para s1βo e +18 θ0123/z0⁴ para s1γo. A relação γo = −K βo, e sua derivada, é uma relação nesta avaliação; não identifica as cocadeias universais.

## 3. Transporte dos invariantes escalares

Para X = I ou J, a identidade usada é s1X + s0X3 = C·∂X. O termo s0X3 é conservado até a avaliação Killing, onde desaparece. Isso evita confundir a variação do Weyl linearizado com uma covariância off-shell que só pertence ao tensor ativo completo.

Se ev(T) = bT θ012, a regra de Leibniz dá bT(3X/z0 − ∂zX) θ0123. O sinal negativo vem de θ3 θ012 = −θ0123; não é uma mudança de convenção do detector.

Conferi a dependência usada no script: I = 16(z/ℓ)^4(E²−B²), J = 16(z/ℓ)^4 EB, com E = (k²f−f'/z)/2 e B = kf'/2. A paridade de I e ∂zI é par, pois f−k = fk. A derivada de J é tomada a ℓ fixo antes da especialização, resultando J(p0) = −4k/z0 e J'(p0) = 4k³−28k/z0².

As únicas respostas escalares visíveis são

Lk(s1(Jβo)) = R(k),    Lk(s1(Jγo)) = −K R(k),
R(k) = 24k³/z0 − 96k/z0³.

Os fatores de engenharia κ e κ² não mudam a direção desse perfil no anel da referência fixada. Uma exigência diferente de polinomialidade no acoplamento, sem tratá-lo como escalar real fixado, precisaria de outra declaração do módulo; a exclusão em k = 2/z0 continuaria válida, mas não se deve importar automaticamente a afirmação de igualdade de módulos para essa outra categoria.

## 4. Anulação das duas projeções Weyl e de suas variações

A identidade decisiva é anterior à escolha de h TT:

T_abcd C^a C^b m^{cd}
= −(2/z0) T_abcd C^a C^b C^c n^d
= 0

para qualquer tensor algébrico de Weyl T. O produto de três ghosts seleciona T_[abc]d, eliminado por Bianchi. O dual de um Weyl também é Weyl em quatro dimensões; esta última propriedade não seria automática para uma curvatura geral com traço.

Isso vale para a projeção S[W[h],W[h]] e seu dual para todo h. Ao variar h na direção s1h, a derivada de S continua no espaço linear dos tensores algébricos de Weyl, de modo que a parte da variação em h se anula. Ao variar os ghosts, a substituição C = ΣθA vA entrelaça s1C e dθC, incluindo os primeiros jatos, porque a subálgebra dos quatro Killing fecha. Aplicar dθ à identidade em θ dá zero. Não se inferiu a nulidade da variação a partir apenas de uma função que se anula em uma solução particular.

O argumento prova a invisibilidade de ambas as contrações e de s1 aplicado a elas. O detector diferente de 079, que tinha valores e primeiros jatos Killing independentes, não satisfazia m = n∧C/z0; sua resposta não contradiz esta identidade.

## 5. Imagem e exclusão delimitada

A imagem do setor é Rher·R(k): a inclusão vem das oito respostas e das duas nulidades, e a direção R(k) é realizada por Jβo; se o peso zero for imposto, κ é uma unidade real fixada. Em k = 2/z0, toda a imagem é zero, enquanto a resposta necessária para compensar −[A6] é +8/z0².

O raciocínio vale sobre a extensão escalar inerte, inclusive com nilpotentes, pois utiliza unidades reais. Acrescentar a contribuição direta h*C⁴, com jatos, não altera esse teste pelo resultado 079; tampouco acrescentar s0V altera Lk(s1z5). Isso não elimina por decreto os termos mistos da equação de fechamento.

Portanto este setor não fornece o levantamento procurado. δ(𝒦) continua não nulo, e −[A6] pertencer ou não à imagem COMPLETA permanece aberto. Derivadas de Weyl, coeficientes tensoriais, outros fundos, admissibilidade causal, QME e UV não foram classificados aqui.

## 6. Revisão estática do cálculo e da custódia

Li integralmente compute_zero_derivative_sector082.py, prepare_exact_copy082.py e finalize_finite_sector082.py. Aritmética Laurent usa Fraction; o produto exterior elimina índices repetidos e conta inversões. A derivada total é suficiente para I e J, que só envolvem f e f'; a especialização impõe f = 0, f' = 1, f'' = 2/z e ℓ = z depois da derivação. A projeção ímpar e o teste k = 2/z operam sobre os polinômios resultantes, sem amostragem numérica.

A base de dez Weyl é construída de cinco matrizes elétricas e cinco magnéticas simétricas sem traço. A injetividade dos respectivos blocos E e B mostra que é uma base, além dos controles explícitos de Bianchi e traço. O último controle aplica dghost a contrações já nulas: é um controle aritmético coerente, mas a justificativa da variação para todos os h pertence ao argumento escrito do item 4, não a esse teste isolado.

Comparei, sem executar as funções, os 17 segmentos de definição copiados por AST com o script 081. Reconstruí documentalmente a concatenação declarada pelo preparador; seus bytes coincidem integralmente com o script 082. Nenhum import ou execução da fonte 081 é necessário para essa verificação.

O recibo histórico contém exatamente 19 itens correspondentes às chamadas literais de check: 18 algébricos e um de preservação das quatro fontes. Todos estão registrados como passados. O pin próprio do script consta ao final da execução; a proveniência do preparador fornece também seu pin anterior, e ambos coincidem com o arquivo presente. Não atribuo a este parecer uma segunda execução nem uma prova Lean.

Os pins do manifesto, do recibo e da proveniência foram relidos, e os seis vínculos locais existem. As fontes lidas permaneceram byte a byte iguais durante esta revisão. As contagens documentais desta conferência estão separadas dos 18 controles algébricos históricos no recibo novo.

Conclusão delimitada: parecer favorável ao teorema do setor finito e à coerência do script/recibo, sem erro material identificado. Os limites acima fazem parte do parecer.
