# Revisão independente — unicidade e aplicação de Araki

[REAL — leitura semântica, 09/09/2026] Parecer favorável à fonte UnitaryCocycleUniqueness.lean, seis teoremas. A prova diferencia u(t)v(t)*, cancela A+A*=0, usa constância em ℝ e multiplica por v(t). Somente v precisa de certificado unitário; não há hipótese circular de unicidade. A especialização mantém a ação canônica modularConjugation e deriva sua antiauto-adjunticidade de V=V*.

A leitura inclui a correção de prova com convert! hd using 1, sem mudança dos enunciados. O primeiro recibo BUILD_20260909_165658_410521 é FAIL_VISIBLE e refere-se à fonte anterior. Este parecer não declara compilação PASS da fonte corrigida. A compilação pertence à raiz.

**Regularidade:** HasDerivAt no módulo significa derivada na norma dos operadores. O expansional de Araki existe em contexto fortemente contínuo mais amplo. Para a interação XX e para a nova classe local somável, a continuidade em norma de t↦α_t(V) foi provada. Esta propriedade justifica promover a identidade diferencial do expansional à derivada em norma requerida aqui. Em particular, escrevendo M=‖V‖, a série ordenada fornece o controle

‖u(t)−1−itV‖ ≤ |t| sup_{|s|≤|t|} ‖α_s(V)−V‖ + exp(|t|M)−1−|t|M.

Dividir por |t| e usar a continuidade em zero dá u'(0)=iV em norma; a lei de cociclo e CanonicalCocycleDerivative propagam a derivada. O controle é argumento matemático aplicado, não novo teorema Lean desta revisão. Não estender a exigência de derivada em norma a todo V limitado do fator sem sua hipótese de órbita em norma.

**Fonte primária conferida:** H. Araki, Relative Hamiltonian for Faithful Normal States of a von Neumann Algebra, Publ. RIMS 9 (1973), 165–209. PDF local Araki_1973_Relative_Hamiltonian.pdf, baixado pela raiz; páginas impressas 174,177–178,181,185,190 conferidas visualmente nos PNGs do PDF, e a continuação 191/nota209 foi lida por extração.

- Prop4.1, p174: define Ψ(V) pela série convergente e o coloca no cone natural.
- Cor4.4, p181: Ψ(V) é cíclico e separante; o expansional direito usa +iα_s(V). A prova herda a propriedade KMS analítica da demonstração de Prop4.3.
- Prop4.12, pp190–191: Ω pertence ao domínio de exp(z(logΔ+V)) para 0≤Re z≤1/2. Em z=1/2 resulta ΦV=exp((logΔ+V)/2)Ω. Não se trata da exponencial Banach de um operador limitado: logΔ pode ser não limitado.
- Def4.2, p177: o Hamiltoniano relativo físico é −V para esse vetor não normalizado.
- Prop4.8, p185: o operador modular COMPLETO satisfaz logΔ_V=logΔ+V−JVJ, na convenção canônica já identificada. exp(logΔ+V) é o operador relativo/preparador, não Δ_V.
- A nota final p209 corrige Props4.13/4.14 e passagens posteriores. Não atinge as proposições e o corolário usados acima.

**Normalização:** Z=‖ΦV‖²>0 pela separação/ciclicidade e ΦV≠0. O estado é ωV(A)=⟨ΦV,AΦV⟩/Z. Na convenção matemática α_t=Δ^{it}(·)Δ^{−it}, o cociclo normalizado é Z^{−it}u(t), e sua derivada na origem é i(V−logZ·1). O Hamiltoniano relativo físico normalizado é −V+logZ·1. A fase central preserva Ad(u), e a normalização escalar do vetor não muda o operador modular completo.

**Alcance:** A existência e a normalidade/fidelidade do estado resultam de aplicação de matemática KNOWN aos dados concretos já provados; não constituem hipótese física nova. A identidade KMS vem do teorema analítico de Araki e da identificação do cociclo com β, não da escolha de chamar um funcional de estado perturbado. Este parecer não afirma novos resultados sobre UV ou anomalias relativísticas.

Nenhuma fonte foi alterada nem recompilada por este revisor. Nenhum um.py foi executado/importado.
