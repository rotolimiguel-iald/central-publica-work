# Parecer independente: geração natural de H³(s0) em E4

10/09/2026. Revisor: /root/selected_geometry_design. Frente080, separada da entrega079.

**Parecer matemático: favorável no alcance expressamente fixado; não identifiquei erro material.** Li integralmente a fonte080 e seu manifesto, confrontei as importações primárias pertinentes e conferi os argumentos de transporte, sem substituir a prova por caracteres. A conclusão aceita é a geração por P e P*, a injetividade do primeiro diferencial sobre esse módulo e a remoção do termo E4 de uma correção completável, na categoria da fonte. A classificação restante de E5 e a decisão sobre δ(K) continuam abertas.

[DERIVED + KNOWN] Este parecer analisa uma demonstração escrita com completude Calabi importada. Não é compilação Lean, prova por CAS ou validação física. O controle documental abaixo é separado do juízo matemático.

## 1. Objeto, leitura e custódia

Fonte integral: [GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md](<C:/IALD/Central de Patentes/Chatgpt/GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md>).

Manifesto: [MANIFESTO_GERACAO_WEYL_080.json](<C:/IALD/Central de Patentes/Chatgpt/GERACAO_WEYL_H3_E4_080_20260910/MANIFESTO_GERACAO_WEYL_080.json>).

A fonte tem **22293 bytes**, SHA-256 **29e113b6ba63f684a5e832a7db080b6116491d2b0d0d5a9ec84ae2f32024c8dc**. O manifesto tem **7450 bytes**, SHA-256 **665d49dc50823ecf35608ce8c020e7541d16cc79940374dd6694ec9824db2b6f**. Valores medidos dos bytes nesta revisão.

Os sete antecedentes foram relidos em bytes para conferir seus pins. Os enunciados078/079 usados no detector já haviam recebido minha revisão matemática separada; os recibos daquela revisão não são reclassificados como prova nova080. O creator da nota foi apenas lido em bytes para custódia, sem execução. Não recapturei canônicos, nem executei um.py, Lean, scripts dos autores ou CAS.

## 2. Complexo linear, sinais e cortes finitos

As equações(3) usam o adendo KT077 correto: s0h=R0C, s0h*=+H0h e s0C*=R0†h*. O fato de H0R0=R0†H0=0 é o que torna essa sequência um complexo. Não se infere sua exatidão a partir dessas duas identidades.

Conferi os cortes(4). Um jato de h de ordem r tem peso r+1 e sua imagem usa jato de C de ordem r+1. Um jato de h* de ordem r tem peso r+3 e sua imagem usa h até ordem r+2. Para C*, a imagem usa h* até ordem r+1, com o mesmo peso r+4. Curvatura e comutadores só diminuem esses pesos. Os cortes são finitos e estáveis; sua união contém todo polinômio de ordem finita.

Sobre o corpo real, uma cisão linear em cohomologia e pares contráteis dá {s0,ρ}=N_pares na álgebra simétrica graduada. A divisão é pelo inteiro positivo que conta fatores de pares. Conserva E e cada elemento envolve somente número finito de pares. Isso prova H(S⁴L)=S⁴H(L); alternativamente, cortes estáveis e limite direto exato dão a mesma conclusão.

Como o grau máximo de H(L) é 1, os quatro fatores que somam ghost3 têm, necessariamente, graus(1,1,1,0). Um grau negativo reduziria a soma máxima a dois. Assim H³(S⁴L)=H⁰(L)⊗Λ³H¹(L). Isso não requer a nulidade de H⁻¹ ou H⁻². As fronteiras com antifields permanecem no quociente H⁰(L) e nas primitivas de S⁴L. A referência a pares contráteis em BBH é compatível com a prova linear explicitada; nenhum teorema de Yang–Mills é transportado por analogia.

## 3. Killing e geração Calabi: a ponte é efetiva

O quociente H¹(L) elimina o jato simétrico ∇C. O prolongamento de Killing reduz ordens superiores a C e m quando ∇Rbar=0. A conexão de transporte é plana no espaço-forma; a realização pela quádrica garante todos os dez dados iniciais. Portanto G=V⊕Λ²V é efetivamente o quociente linear, e o diferencial CE só aparece em s1.

Conferi a importação na Definição2 e no §3.1/eq32 de [Khavkine1805.03751v2](https://arxiv.org/pdf/1805.03751), com o tratamento detalhado em [Khavkine1409.7212](https://arxiv.org/pdf/1409.7212). Trata-se de compatibilidade completa por operadores diferenciais finitos, com os tipos de simetria dos fibrados preservados. Não é apenas a identidade R1R0=0.

Uma precisão útil para a leitura por jatos é a seguinte. Um ciclo linear em um ponto pode ser transportado por uma seção local suave das isometrias que leva esse ponto aos vizinhos. Assim ele se estende a um operador diferencial local cujos coeficientes são suaves e cuja composição com R0 é zero em toda a vizinhança. A completude aplica-se a esse operador; avaliar sua fatorização de volta no ponto fornece a geração dos ciclos por jatos de R1. Esse argumento usa a homogeneidade do espaço-forma e evita confundir uma igualdade pontual com uma identidade diferencial ainda não demonstrada.

A contração da curvatura corrigida(9) está correta:
g0^ac δR_abcd=δRic_bd+K[(trh)g0_bd−h_bd],
enquanto a contração da variação de Kgg é K[(trh)g0+2h].
Logo tr R1=δRic−3Kh=E. A linearização de G+Λg é E−g0 trE/2. O traço reverso em dimensão quatro, a densitização e κ≠0 são isomorfismos algébricos. Incluindo todos os jatos, as EOM eliminam precisamente o traço necessário para substituir R1 por W[1]. Relações adicionais podem reduzir o espaço; não invalidam o limite superior usado depois.

## 4. Conferência da redução de TODOS os jatos de Weyl

O ponto central dos §§5–6 foi conferido independentemente. Escrevo seu mecanismo para explicitar por que a decomposição de representações não está fazendo o trabalho da geração.

No graduado da ordem de derivadas, estas comutam. A divergência
∇^{AA'}Ψ_ABCD=0, válida modulo os jatos das EOM, elimina toda contração entre um índice de derivada e um índice de Ψ. Para ver também o traço de duas derivadas, diferencie a divergência e contraia o índice pontuado. A identidade spinorial
p_EA' p^{AA'}=(δ_E^A/2)p²
fornece p²Ψ_EBCD=0 no graduado. Não há divisão por p²: ele é uma relação obtida da divergência prolongada.

A antissimetrização de dois índices de spinor em dimensão dois é uma contração por ε. Entre dois índices de derivadas, essa contração reduz-se a ε vezes p². Entre derivada e Ψ, já é um prolongamento da divergência. Entre índices de Ψ, é zero pela própria simetria. Assim todos os índices não pontuados remanescentes podem ser simetrizados. A simetria dos pares de derivadas, combinada com a simetria não pontuada, força a simetria pontuada.

Para as derivadas efetivas, cada troca introduz [∇,∇]=Rbar·, isto é, K vezes ordem duas unidades menor. Ao prolongar, ∇Rbar=0 evita novos coeficientes de ordem maior. A redução termina na ordem finita do elemento. O resultado é uma sobrejeção do tipo
Sym^(r+4)S⊗Sym^r S'
e de seu conjugado para o graduado correspondente; não se precisa provar que esses dados sejam todos independentes ou simultaneamente realizáveis.

Li diretamente as eqs87–91 e o contexto Einstein do §9 de [Vasiliev9611024v2](https://arxiv.org/pdf/hep-th/9611024). A recorrência linear confirma a próxima parte simétrica e um termo de curvatura inferior. O argumento acima usa a convenção do fundo em exame e não transfere o sinal AdS da fonte. A eq8 de [Torre9508005](https://arxiv.org/pdf/gr-qc/9508005) foi usada apenas como conferência do símbolo Ricci-flat, não como prova para K>0.

## 5. Naturalidade, invariantes e a cota de dimensão

Nos cortes finitos, os geradores e seus quocientes são representações tensoriais finitas da isotropia. A complexificação tem álgebra sl2⊕sl2; uma projeção pela forma compacta dá a exatidão dos invariantes, e a parte real devolve um mapa real. Não se faz média sobre o grupo Lorentz não compacto.

Esse procedimento também naturaliza uma primitiva coordenada finita: escolha um corte estável que a contenha, projete nesse espaço finito e use a equivariância de s0. A identidade de fronteira é mantida. Para uma fatorização Calabi, o mesmo argumento atua no espaço finito dos coeficientes do operador. Um intertwiner tensorial é realizado por contrações com a métrica/inversa e, no setor orientado, ε, com derivadas covariantes. A homogeneidade transporta a identidade. O argumento vale na fibra fixada da nota; não é um teorema geral de naturalização do BRST não linear.

Conferi à mão a decomposição(15), expandindo Λ³(V⊕A⊕B). Λ²V=A⊕B, Λ²A=A, Λ²B=B e as duas terceiras potências adjuntas são escalares. As parcelas resultam em quatro escalares, os dois adjuntos, os dois Weyl, quatro(1,1), quatro vetores, duas cópias de cada(3/2,1/2) conjugado e uma(3/2,3/2). A dimensão é120. Esse controle não é uma reexecução de caracteres por CAS.

Os tipos W_r para r≥1 têm um spin pelo menos5/2, inexistente em Λ³G. Como o graduado V_r/V_(r−1) é quociente de W_r, a exatidão dos invariantes força toda classe natural de ordem r a vir de ordem menor. A indução finita reduz a W0, com multiplicidade escalar total dois. Não se ignoram extensões entre ordens: elas são justamente tratadas pela sequência exata finita. A linguagem spinorial é apenas a complexificação de representações tensoriais locais e não exige um campo espinorial ou spin global no modelo.

## 6. Coeficientes, detector079 e remoção de b4

A nota fixa K e κ antes de tomar a extensão R_her⊗R A_R. Isso é matematicamente essencial: s0 é então 1⊗s0,R, e todo R-módulo é plano. Não são apagados os escalares herdados. O argumento abrange essa extensão algébrica explicitada, inclusive coeficientes com nilpotentes; não demonstra automaticamente um módulo uniforme sobre K variável, uma completação adicional de coeficientes ou coeficientes tensoriais espectadores.

As duas avaliações079 foram objeto da revisão independente anterior: −2/z0 para s1P e +2k para s1P*. Elas usam soluções lineares e Killing em uma vizinhança, portanto anulam s0 inclusive sobre todos os jatos de antifields. Se uma combinação fosse s0-exata, sua imagem por s1 também seria; k e −k no mesmo fundo a anulariam. As duas equações dão λ=μ=0. O raciocínio também prova diretamente a injetividade de d1; sobre R_her, os divisores são números reais não nulos, portanto unidades, sem hipótese de separação numérica de nilpotentes.

De s0b4=0 e s0b5+s1b4=0 resulta d1[b4]=0. A geração e a injetividade fornecem b4=s0v4 com v4 natural, finito, ghost2/E4. Subtrair s(v4) elimina b4 e deixa b5'=b5−s1v4, com s0b5'=0. O sinal decorre de s0s1=−s1s0. Trata-se de alteração por fronteira do complexo truncado, não da imposição arbitrária de b4=0.

## 7. Limites que devem acompanhar a utilização

Aprovo esse argumento para o complexo métrico mínimo, em referência Lorentziana espaço-forma FIXADA, K>0, φ0 constante, dimensão quatro, κ não nulo, orientação e apenas coeficientes escalares inertes da classe declarada. Não há inferência para o fundo material físico φ=id.

Não foram pagos por esta nota:
- a classificação de H³(s0) em E5 ou a ação de s1 sobre esse módulo;
- o cancelamento ou a impossibilidade de cancelamento universal de −[A6] por δ(K);
- coeficientes tensoriais de referência, espectadores com jatos não constantes ou um anel universal restrito em K;
- preservação de uma cota causal adicional de scaling degree, contatos de inserção, T9/T11, QME ou UV.

As operações preservam E e deixam ordem finita por elemento. Isso é o que basta para a comparação Rees indicada; não garante uma cota uniforme de derivadas em todas as aridades. Nenhum resultado080 deve ser retroinserido na entrega079 congelada.

**Conclusão:** a exaustividade declarada para E4 não é sustentada apenas por representações. Ela usa a geração Calabi, o quociente efetivo pelas EOM, a redução triangular da torre, a exatidão finita dos invariantes e os detectores independentes079. Não encontrei necessidade de errata material no enunciado delimitado.
