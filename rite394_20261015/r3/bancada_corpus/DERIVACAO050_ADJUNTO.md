# Continuação050 — adjunto antilinear maximal de S=JT
[DERIVED — derivação anterior ao código; elaboração Lean pendente]

Autoria: agente review_global_cocycle. Este módulo é genérico e importa apenas Mathlib, sem importar a torre ou alterar qualquer fonte≤049.

Seja H um Hilbert complexo, T um LinearPMap auto-adjunto e J uma antiunitária involutiva. Não se exige positividade de T. Definimos S=JT em D(T), D†={y∈H:Jy∈D(T)} e S†y=T(Jy).

A convenção de produto interno é antilinear no primeiro argumento. A norma e a semilinearidade de J implicam, por polarização, 〈Ju,Jv〉=conj〈u,v〉. Com J²=I, segue 〈Ju,y〉=〈Jy,u〉. A simetria de T fornece então 〈Sx,y〉=〈Jy,Tx〉=〈TJy,x〉 para x∈D(T), y∈D†.

A identificação é maximal: se z satisfaz 〈Sx,y〉=〈z,x〉 para todo x∈D(T), então 〈z,x〉=〈Jy,Tx〉. A API mem_adjoint_domain_of_exists põe Jy em D(T*). Pela igualdade efetiva T*=T, y∈D†. A densidade de D(T), consequência de autoadjunticidade, e a identidade de pareamento mostram que o valor construído S†y é exatamente z. Assim D† coincide com o domínio definido pela existência do representante de Riesz; não é apenas um candidato nomeado adjunto.

A composição não presume D(T) estável por T: para x∈D(T), Sx∈D† se, e somente se, J(Sx)=Tx pertence a D(T). Nesse domínio explicitamente caracterizado, S†(Sx)=T(JJTx)=T(Tx). Portanto D(S†S)={x∈D(T):Tx∈D(T)} e a composição coincide com o quadrado nesse domínio. O módulo não introduzirá uma definição concorrente do quadrado concreto T_c; fornecerá lemas de domínio e valores para a integração pelo coordenador.

[OPEN] A construção geral não identifica uma álgebra/estado, fase espectral, cálculo funcional, BW, inclusão semilateral ou H3. A integração concreta da050 deve aplicar este resultado ao mesmo T e J já construídos, sem trocar os operadores por homônimos.

Custódia: apenas novos arquivos050 em Chatgpt; revisão preserva os bytes anteriores em backup imediato, temporário verificado e substituição. Cada declaração da fonte terá print de axiomas. Estatuto REAL exige compilação medida e revisão independente.
