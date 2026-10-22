# Série de comutadores e evolução unitária finita

[REAL] A folha FiniteCommutatorEvolution.lean foi compilada isoladamente: 16 teoremas + 10 demais declarações (incluindo instâncias locais nomeadas), 26 auditorias de axiomas. O recibo PASS_COMPILED_SCOPE está na build181547; nenhum um.py foi executado ou importado e nenhuma fonte canônica foi alterada.

[REAL] finite_evolution_hasSum iguala a série Σk (it)^k/k! ad(H_N)^k(A) à evolução efetiva exp(itH_N) A exp(−itH_N), no MESMO TowerHilbert P e com cutoffHamiltonian da folha BondLocalityEstimates. Vale para todo t real e todo observável limitado A. Não exige [H_N,A]=0 nem comutação dos termos da interação. finite_evolution_isometry prova a conservação da norma.

[DERIVED] A prova constrói operadores contínuos de multiplicação à esquerda e à direita no espaço dos operadores. Estes dois superoperadores comutam por associatividade, mesmo quando H e A não comutam. A série exponencial de cada um é transportada pela avaliação contínua. Isso identifica a exponencial do comutador com a conjugação efetiva, e depois identifica suas potências com os comutadores iterados já certificados.

[REAL] Revisão semântica independente do root favorável, por leitura integral. As correções posteriores foram apenas de elaboração: ordem associativa, instâncias explícitas de escalares/topologia e parâmetro explícito do tipo na exponencial. A topologia usada é a canônica de norma do operador, compatível com a convergência limitada da biblioteca, sem axioma adicional.

[OPEN] Este arquivo sozinho não constrói o limite N→∞, dinâmica extensiva, estimativa de Lieb–Robinson, extensão normal ao fator ou estado KMS. A próxima folha usará o majorante uniforme da localidade e convergência dominada de séries para construir o limite local em tempo pequeno. O fundo modular não foi acrescentado a esta evolução pura da interação.

Todas as tentativas anteriores e backups de bytes foram preservados.
