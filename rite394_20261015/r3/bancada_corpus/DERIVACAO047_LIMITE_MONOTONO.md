# Derivação047 — limite monótono de operadores positivos

[INPUT] Ordem do root: construir o limite forte e IsLUB de uma família crescente positiva de operadores limitados, com índice arbitrário dirigido. Esta derivação precede o fonte MonotoneOperatorLimit.lean. Nenhuma convergência forte é hipótese do teorema principal. Somente a bancada Chatgpt recebe arquivos novos; fontes anteriores permanecem em leitura.

[DERIVED] Para D≥0, seja S=√D. A desigualdade C*-algébrica star(S) D S≤‖D‖ star(S)S, já disponível em CStarAlgebra.star_left_conjugate_le_norm_smul, e S²=D dão D²≤‖D‖D. Testar em v dá ‖Dv‖²≤‖D‖ Re⟨v,Dv⟩. Portanto, se0≤A_i≤A_j e ‖A_j‖≤C, temos0≤A_j−A_i≤A_j, de modo que ‖(A_j−A_i)v‖²≤C(q_j(v)−q_i(v)), com q_i(v)=Re⟨v,A_i v⟩.

Para cada v, q_i(v) é uma rede real crescente limitada acima por C‖v‖². Sua convergência ao supremo real é a API tendsto_atTop_ciSup. A desigualdade anterior e um majorante comum k≥i,j dão Cauchy forte de A_i v. O índice exige apenas Preorder, IsDirectedOrder e Nonempty, não SemilatticeSup nem enumeração por naturais. Usar Metric.cauchy_iff em Filter.map para manter esse escopo.

A completude de H constrói o limite f(v). A cota uniforme e ContinuousLinearMap.ofTendstoOfBoundedRange empacotam f como B contínuo e linear. A positividade é fechada para limites fortes: simetria e leituras quadráticas passam ao limite escalar. Assim B≥0. A mesma passagem aplicada a A_i−A_j eventualmente e a D−A_i para qualquer majorante D prova A_j≤B≤D. Isso dá IsLUB(range A)B e ‖B‖≤C.

Não aplicar tendsto_atTop_isLUB à topologia de NORMA dos operadores: sua hipótese SupConvergenceClass não foi dada e a conclusão seria falsa em geral. O argumento proposto constrói SOT, não convergência em norma. O teorema é de operadores limitados genéricos; pertença do limite a uma subálgebra e preservação de supremos por E são passos posteriores do root. Não antecipa normalidade de E, CP, H3 ou geometria física.
