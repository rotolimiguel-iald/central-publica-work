# Localidade antes do limite extensivo

[DERIVED — proposta de construção; compilação ainda não iniciada]

O contrato anterior de interação somável controla a norma total e dá um potencial limitado. O novo contrato de bonds controla região {j,j+1} e norma uniforme, sem soma global. Suporte apenas no andar j+1 não seria suficiente: esse andar contém todos os sítios anteriores.

O primeiro bloco usa os operadores reais do mesmo TowerHilbert e as álgebras canônicas chainLocalAlgebra. Prova suporte do comutador na união, sua nulidade em regiões disjuntas e sua norma ≤ 2‖A‖‖B‖. Para A apoiado no prefixo 0,…,R, apenas bonds j≤R entram no primeiro comutador. Logo o resultado estabiliza para N≥R+1 e seu suporte está no prefixo R+1. Após k comutadores, o suporte fica em R+k e os coeficientes são independentes do corte quando N,M≥R+k.

[OPEN] Isso não prova sozinho convergência da série dinâmica para todo tempo. O próximo passo efetivo é derivar uma desigualdade integral, retirar por conjugação o termo que preserva a norma e contar caminhos de bonds adjacentes. Não se colocará uma estimativa de Lieb–Robinson no contrato como se ela fosse a construção.

O alvo correto é convergência da evolução de cada observável local, uniforme em intervalos temporais compactos, e extensão por densidade à álgebra quase local. Não se exige nem se espera em geral limite em norma do Hamiltoniano ou de um cociclo implementador global.

[KNOWN] Rotas primárias consultadas: Nachtergaele–Ogata–Sims, Propagation of Correlations in Quantum Lattice Systems (2006), https://arxiv.org/abs/math-ph/0603064 ; Nachtergaele–Sims, On the dynamics of lattice systems with unbounded on-site terms in the Hamiltonian (2014), https://arxiv.org/abs/1410.8174 . Essas fontes orientam a estratégia; suas conclusões não são axiomas adicionados ao Lean.

[REAL — fonte lida] SiteModularInvariance.chain_flow_into preserva qualquer região pela ação modular canônica. Portanto a formulação em interação com termos alpha_t(term j) mantém o suporte. Isometria e continuidade temporal em cada suporte finito já existem na bancada. Essa alternativa é pertinente se o fundo modular local não tiver norma uniforme; a estimativa temporal correspondente ainda precisa ser construída.

Nenhum original foi alterado. Nenhum um.py foi executado ou importado.
