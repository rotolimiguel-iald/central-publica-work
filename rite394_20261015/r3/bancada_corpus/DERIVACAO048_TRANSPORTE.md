# Derivação048 — obstrução de Borchers após transporte de perfil

Data: 07/09/2026. Autor: agente de revisão global/cociclo. Documento registrado antes da fonte nova `TransportedBorchersObstruction.lean`.

## Escopo e estatutos

[REAL — fontes anteriores lidas] A etapa007 fornece `ChatgptAudit.product_borchers_trivial`; a etapa027 fornece `ChatgptAudit.Transport027.profileGNSUnitary`, `profileFactorConjugation`, `profileModularFlow` e `profile_flow_conjugation_eq`. Esta nota não recompila nem altera esses artefatos.

[DERIVED — alvo da nova formalização, ainda sem compilação neste registro] A obstrução transporta-se para qualquer par de perfis produto P,Q com `0 < profileAffinityLimit P Q`. A conclusão é negativa para o fluxo produto transportado. Não é uma impossibilidade de Bisognano–Wichmann em geral.

## Dados concretos

Escreva H_P = `TowerHilbert P`, H_Q = `TowerHilbert Q` e

- e = `profileGNSUnitary P Q hpos : H_Q ≃ₗᵢ[ℂ] H_P`;
- C = `profileFactorConjugation P Q hpos`, isto é, C(A)=e A e⁻¹;
- α_t = `profileFlowConjugation P Q hpos t`.

O teorema027 dá exatamente α_t(A)=C(σ_t^Q(C⁻¹(A))). Não se identifica esse automorfismo com a congruência pelo filtro positivo039, que em geral não é unital.

Considere V : ℝ → B(H_P), com:

1. para todo vetor v, a ↦ V(a)v é contínua em zero;
2. V(0)=I;
3. ‖V(a)v‖=‖v‖ para todos a,v;
4. α_t(V(a)) = V(exp(−2πt) a) para todos t,a.

O alvo é `∀ a, V a = 1`.

## Prova antes do código

Defina W(a)=C⁻¹(V(a)). Em vetores, W(a)v=e⁻¹(V(a)(ev)). A continuidade de e⁻¹ transporta (1), a preservação da identidade por C⁻¹ transporta (2), e a isometria de e e e⁻¹ transporta (3).

Aplicando C⁻¹ à hipótese (4), e usando a igualdade027, obtemos

σ_t^Q(W(a)) = W(exp(−2πt) a).

Portanto `product_borchers_trivial (P := Q)` dá W(a)=I. Aplicar C fornece V(a)=I.

A prova007 usada aqui explora a família total de autovetores modulares locais. Ela não pressupõe um período comum, nem um retículo de logaritmos. Na diagonal de cada autovetor, a conjugação modular cancela a fase; a relação de Borchers impõe invariância por uma contração real; a continuidade em zero fixa a diagonal; a norma preservada fixa o vetor; a totalidade conclui a identidade.

## Hipóteses ausentes e limite da interpretação

Não se exige V(a)∈M, lei de grupo para V, sobrejetividade de V(a), gerador positivo, estacionariedade de Q ou periodização do fluxo. A preservação da norma de cada V(a) continua sendo hipótese essencial do teorema utilizado e não será removida.

A relação de Borchers é uma hipótese explícita sobre os operadores concretos. O módulo não deriva essa relação de uma inclusão modular semilateral e não constrói uma rede de regiões. Uma futura aplicação a tal inclusão precisa pagar separadamente esses requisitos. Trocar o perfil produto dentro do transporte027 preserva a obstrução; disso não segue uma obstrução para todo estado não produto ou para toda representação modular.

[OPEN] Permanecem a construção de uma localização geométrica efetiva com suas propriedades modulares e a seleção de dados físicos suficientes para essa localização. A tétrade, a assinatura física geral, H3 e a meta ampla não são conclusões deste módulo.
