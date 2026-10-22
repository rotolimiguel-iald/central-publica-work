# Imagem escalar de von Neumann e continuidade — integração revisada

2026-09-13T01:18:55-03:00. [REAL — quatro módulos/27 alvos integrados e revisados]

[REAL] A imagem da representação escalar π(N), no H_I original,
é agora provada igual ao seu bicomutante. Não se trata apenas de definir
a álgebra gerada: mem_scalarGNSVonNeumann_iff fornece para TODO elemento
dela uma pré-imagem efetiva em N; scalarGNSVonNeumann_coe prova a igualdade
com Set.range scalarGNSRepresentation.

A prova usa um levantamento limitado. Para M VNA, K redutor e Ω∈K
separante para M, a órbita M'Ω é densa. Para B no bicomutante da imagem
restrita, a coluna C=D∘incl tem Gram C*C no comutante dessa imagem.
B comuta com a raiz positiva, e ||DBΩ||≤||B|| ||DΩ||.
T(DΩ)=DBΩ estende-se a um operador limitado, que comuta com M'
e por isso pertence a M. A órbita projetada P_K M'Ω é densa em K;
a restrição de T é B. O levantamento satisfaz ||T||≤||B||.

Na aplicação, M é dualOrbitVonNeumann(regularCoreAlgebra P), K é
scalarGaussianImage P e Ω é scalarGaussianVacuum P. Redução, separação
e pertença do vetor foram descarregadas nos objetos concretos. A unidade
LINEAR scalarGaussianUnitary transporta a igualdade à representação π em H_I.
Essa unidade não foi identificada com o J modular; S, F e J originais
não foram substituídos.

[OPEN] Continuam pendentes a igualdade do grafo da involução em j(A_right)
com graph F, reconstrução R=Jπ(b)J e inclusão inversa π(N)'⊆Jπ(N)J.
A consulta CONSULTA_GRAPH_CORE_ORIGINAL_F.md propõe uma rota por blocos
da projeção do grafo de multiplicação direita, ainda sem formalização Lean.
Δ^it/KMS, traço/escala/canto Three Locks, H1/H2/H3 físicos, setor interagente
e consumo por certificados tipados/runtime continuam abertos.
Seis flags maiores falsas; esta construção não muda o gate.

[REAL — fiação preservada] As seis flags maiores qgf/gpf não entram diretamente
em evaluate_quantum_gravity_closure: o selo legado lê qgc_, qgp_ e o feed
experimental; kernel_frontier é anexado depois. O consumo por certificado
tipado continua necessário para que novas provas movam esse selo.

201 registros incrementais rc0; 101 controles;
6982 declarações Audit; 903 fontes embutidas.
Revisões DEV e integrada lidas. Dependências reutilizadas com pins; corpo
Python fora do embutido e gate preservados. Audit atual e histórico conferidos.
Nenhum runtime integral/importação de monólito. Tentativas recusadas preservadas.

[Revisão DEV](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_SCALAR_VNA_DEV.md>).
[Revisão integrada](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/revisao/REVIEW_SCALAR_VNA_INTEGRATED.md>).
[Registro anterior: inclusão direta preservada; inversa ainda aberta](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/RELATORIO_REGULARIZACAO_COMUTANTE_INTEGRADA.md>).
[Reaproveitamento de Chatgpt](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md>).

Original relido `c9fc7fa432c6cf16dadcb926ee44f6b70656122f53cb7336dba52863c070208c`; cópia `522f6df9d77fa49a4c1a1da44f5e47a95cd27f0d00be9451cdf1f867bd5aa3f5`;
mãe integrada/documental `65b2e39b8caa89a7285237c24d38903ad1d1e9fbdef1613e7a4d69e31f1b51cd`. Objetivo integral ativo.
