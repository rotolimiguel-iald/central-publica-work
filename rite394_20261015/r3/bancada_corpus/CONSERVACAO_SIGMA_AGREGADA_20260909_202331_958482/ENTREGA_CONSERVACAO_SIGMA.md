# Conservação sigma agregada — entrega local congelada

[REAL — compilação Lean] SigmaMatterConservation.lean passou no Lean 4.31.0: 12 teoremas, 2 definições e 14 auditorias de axiomas. Os dois processos (fonte e importador) terminaram com código 0, sem warnings. Todos os termos auditados usam somente propext, Classical.choice e Quot.sound. O namespace é ChatgptAudit.SigmaMatter.

Fonte: [SigmaMatterConservation.lean](<C:/IALD/Central de Patentes/Chatgpt/CONSERVACAO_SIGMA_AGREGADA_20260909_202331_958482/SigmaMatterConservation.lean>), 13.844 bytes, SHA-256 4e66a8bc3a35ffe9616e04805feffb5563e1f58229ba9d8676f3f486ebe2543e.

Recibo: [BUILD_RESULT.json](<C:/IALD/Central de Patentes/Chatgpt/CONSERVACAO_SIGMA_AGREGADA_20260909_202331_958482/BUILD_20260909_202859_186257/BUILD_RESULT.json>). A compilação usa a biblioteca transposta 83 aprovada; a fonte, os módulos cobertos pela fronteira do builder e os pins permaneceram estáveis. Isto não declara recompilação ou hashing de toda a árvore transitiva canônica/Mathlib. Nenhum um.py foi executado ou importado, nenhum original ou módulo previamente congelado foi alterado. Este relatório é a análise do próprio autor da folha; não constitui atestado de revisão atribuído a terceiro.

## O que a folha demonstra

[REAL — Lean] Para uma família finita de covetores fechados e coeficientes constantes, a divergência do tensor total é a soma das forças:

div T_total = Σ_q weight_q coupling_q (div w_q) w_q.

Assim, finite_stress_conserved_of_aggregate (linha 41) aceita o cancelamento dessa soma, sem exigir que cada div w_q seja zero. A versão metric_finite_conserved_of_aggregate (linha 130) constrói a inversa e a conexão de Levi-Civita a partir da métrica lorentziana suave.

[REAL — Lean] Para w_q=dφ_q, suavidade e fechamento são derivados. A igualdade Σ_q φ_q²=1 no aberto U implica Σ_q φ_q dφ_q=0, em sphere_constraint_tangent (linha 76). Se Box_g φ_q=λ(x)φ_q para o mesmo λ e o mesmo coeficiente c, segue:

Σ_q c (Box_g φ_q) dφ_q = c λ(x) Σ_q φ_q dφ_q = 0.

Não é necessário λ=0; tampouco é necessária regularidade independente de λ, pois a demonstração não o diferencia. metric_sigma_stress_conserved (linha 147) entrega a conservação resultante. A identidade genérica agregada é mais ampla que essa especialização esférica.

[REAL — Lean] sigmaGibbsRecord (linha 160) usa os mesmos potenciais e um k comum. Para k>0, sigma_gibbs_source (linha 169) identifica a fonte com a soma dos stresses de dφ_q, de coeficiente c=k/(π cosh² k). sigma_gibbs_conserved (linha 177) fornece a conservação sigma dessa fonte.

[REAL — Lean, condicional] sigma_gibbs_einstein_from_area (linha 191) compõe essa conservação com o registro e a transferência de área da resposta Gibbs. Em aberto preconexo, obtém uma constante Λ com G+Λg=(2π/η)T. Permanecem explícitos o registro métrico lorentziano, os potenciais suaves, a restrição esférica, a equação com λ comum, k>0, η≠0, as telas de equilíbrio e o limite (incremento entrópico Gibbs−η incremento de área)/t²→0 em cada direção nula não zero.

## Controle Minkowski

[DERIVED — demonstração escrita, não formalizada nesta folha] Tome g=diag(1,−1,−1,−1), Γ=0, φ_0=cos x⁰ e φ_1=sin x⁰. Temos φ_0²+φ_1²=1 e Box_g φ_q=−φ_q: o autovalor comum é λ=−1 e as ondas individuais não são identicamente nulas. Entretanto,

dφ_0=−sin x⁰ dx⁰,   dφ_1=cos x⁰ dx⁰,
Σ_q dφ_q⊗dφ_q=dx⁰⊗dx⁰,
T_total=c(dx⁰⊗dx⁰−g/2)=(c/2)diag(1,1,1,1).

O tensor total é constante e conservado, embora a conservação individual não seja garantida. Este é um exemplo concreto da utilidade do cancelamento agregado.

[DERIVED — controle da condição restante] Para Gibbs com k>0, c=k/(π cosh² k)>0. Na direção nula v=(1,1,0,0), T_total(v,v)=c e o coeficiente quadrático entrópico/modular do protocolo é −πc<0. Uma tela plana paralela tem área constante, logo coeficiente de área zero. O quociente do erro de área tende então a −πc, e não a zero, independentemente de η. Portanto o exemplo paga a conservação agregada e falha no matching dessa área plana. Não é um habitante do pacote gravitacional completo; tampouco é uma refutação da TGL.

## Limites e próxima composição

[INPUT] A folha recebe um registro métrico admissível e potenciais. Não recebe Einstein como hipótese, mas ainda recebe a correspondência de área. A fonte material é derivada dos potenciais do protocolo Gibbs escolhido.

[OPEN nesta folha] A composição concreta com g[P] e φ(P), o cálculo completo do exemplo curvo categórico/FLRW e a realização de um pacote simultaneamente compatível não são formalizados aqui. O exemplo motivador da derivação prévia é separado do recibo Lean. Outros artefatos da tarefa principal podem tratar essas obrigações.

[OPEN nesta folha] Não há identificação dos campos sigma com campos CCR livres; não há dedução da ação variando P quando g[P] também varia. A conexão é Levi-Civita sem torção. Nada nesta entrega declara confirmação física, cobertura de todas as métricas lorentzianas ou fechamento da gravidade quântica.

Fonte congelada após o PASS; backups em bytes e a primeira tentativa de compilação foram preservados. Nenhuma folha adicional foi aberta para o controle escrito.
