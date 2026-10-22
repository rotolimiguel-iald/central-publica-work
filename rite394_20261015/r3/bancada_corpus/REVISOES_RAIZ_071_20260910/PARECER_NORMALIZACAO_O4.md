# Revisão da normalização causal O(4)

10/09/2026. [DERIVED — revisão escrita da raiz]. Li integralmente a nota `NORMALIZACAO_O4_CAUSAL_071_20260910_000602_682931/PROVA_NORMALIZACAO_O4_E_ANOMALIA.md`. Não identifiquei erro material no alcance declarado. Esta revisão usa a construção Q2 e sua liberdade de renormalização já delimitadas; não repete a prova de existência analítica de Q2.

O ponto central confere: quando as aridades inferiores já são equivariantes, as prescrições transportadas têm exatamente a mesma distribuição fora da diagonal na aridade corrente. A diferença tem suporte na diagonal e pertence à liberdade local dessa primeira aridade. A média atua nesse espaço afim, mantendo os produtos inferiores fixos. A recíproca do teorema de renormalização fornece os produtos superiores compatíveis; estes não são obtidos por uma média simples de famílias completas.

Na convenção S(F)=sum (i/hbar)^n T_n(F^n)/n!, um Z que começa em aridade n produz Delta T_n=(hbar/i)^(n−1)T_1 Z_n. O fator da nota está correto. A normalização é realizada para todas as inserções, de modo que a diferenciação funcional e a identidade de ação por partes possam ser transportadas conjuntamente.

A equação de unitariedade tem uma única parcela com T_n; as demais usam aridades inferiores. Com estas fixas, a restrição é afim real. A média por transformações que preservam a involução conserva essa equação. O(4) age realmente no slot material e em seu dual, mantendo o slot dos antighosts e sua convenção de realidade. Uma reflexão interna não inverte a orientação temporal e não é uma operação antiunitária.

A relação R Exp_z(v)=Exp_Rz(Rv) vale inclusive em v=0 e coeficiente a coeficiente na expansão formal. Ela exige transportar o centro z. Isso confirma a limitação da nota: a família inteira é equivariante, enquanto uma única expansão com fundo fixo admite diretamente apenas o estabilizador desse fundo. O uso de parametrices locais e isomorfismos entre realizações de Hadamard não exige um estado global preferido invariante.

A extração recorrente da quebra a partir da identidade de Ward transportada é compatível com a normalização equivariante. O resultado é uma quebra no setor invariante diagonal da família de fundos. O exemplo com o produto interno entre phi e phi_bar mostra corretamente por que isso não implica ausência de dependência de fundo. Também não implica exatidão cohomológica ou QME satisfeita.

Aceito o resultado delimitado: existe uma normalização Q2 com essa simetria rígida exata, sob a classe de extensões e as hipóteses Q2 indicadas. Permanecem próprios a primitiva da quebra, a comparação com a álgebra de campos completos, o transporte entre esquemas e as condições do setor físico. Nenhum CAS, Lean ou um.py foi executado nesta revisão; a fonte não foi alterada.
