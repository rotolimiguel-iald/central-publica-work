# Imagem escalar de von Neumann — DEV

2026-09-13T01:01:58-03:00. [REAL — quatro módulos/27 alvos compilados; revisão e integração pendentes]

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

Integração anterior: 197 registros,
100 controles, 6955 declarações Audit.
Este DEV não altera um.py nem as 34 memórias; atualização pendente de revisão
nesta sessão. Cópia `76265b7ebb0c298e07f467697e93b8304619e939789079458c251386b5d3e795`, mãe `65b2e39b8caa89a7285237c24d38903ad1d1e9fbdef1613e7a4d69e31f1b51cd`.
Tentativas Lean recusadas e fontes anteriores foram preservadas; somente
logs rc0 dos bytes atuais são aceitos. Nenhum monólito executado/importado.
