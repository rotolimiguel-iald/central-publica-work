# Adendo anterior ao código da compatibilidade positiva

[DERIVED] O parecer independente de Carver, em `REVISAO_A2_012/TRACE_COMPLETION_012/REVISAO_MATEMATICA.md`, demonstra a compatibilidade matemática: o polar de r transporta os dois positivos e a tracialidade quadrática de A1 dá a igualdade. A pertença do polar ao mesmo core é indispensável. Não se presume que os suportes do polar sejam iguais aos suportes dos positivos; bastam as inclusões.

[OPEN] Formalização: Poincare constrói `V354BoundedPolar` em `A2_SUSY_012`; esta bancada consome sua futura fonte compilada, sem duplicá-la. Aqui serão provados apenas o núcleo das potências de um auto-adjunto, as inclusões de suporte que seguem de ShiftRelated e o entrelaçamento do polar para os dois positivos. Fornecedores já lidos: `ContinuousLinearMap.ker_adjoint_comp_self` (Mathlib/Analysis/InnerProductSpace/Adjoint.lean:211), `real_cfc_intertwines`/`positive_sqrt_intertwines` (V350PositiveRootIntertwining), e a lei `scalarInverseLimitWeight_tracial` (V351QuadraticTrace).

A primeira busca trouxe lemas de estabilização de núcleos em dimensão finita; eles não serão usados para o core infinito. A implementação do núcleo reutilizará o lema geral do adjunto e composição. Nenhuma mudança na relação algébrica, em A1 ou nos 33 lemas de A2 é necessária.

O parecer e as definições não substituem uma compilação: não se declara aqui a compatibilidade formal concluída nem se instancia o testemunho legado.
