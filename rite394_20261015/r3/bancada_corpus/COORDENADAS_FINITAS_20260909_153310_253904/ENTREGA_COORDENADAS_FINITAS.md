# Mudança finita de coordenadas — entrega

[REAL — Lean e revisão independente] A cadeia de transformação finita foi demonstrada para mapas suaves inversos entre abertos de R⁴ e para a métrica Lorentziana suave do kernel. As seis fontes estão congeladas. Nenhuma transformação de Levi-Civita, curvatura, Ricci ou Einstein foi recebida como hipótese para obter a mesma conclusão.

Medição: 2026-09-09T19:12:51.522477+00:00. São 50 teoremas, 13 definições/estrutura, 63 auditorias de termos e 12 processos de compilação aprovados nas seis folhas e seus importadores. Todos os recibos finais têm PASS_COMPILED_SCOPE, sem warnings nem axiomas fora de propext, Classical.choice e Quot.sound. A biblioteca transposta anterior de 45 módulos foi reutilizada, sem nova integração ou execução de um.py.

| Folha | Teoremas | Definições/estrutura | Auditorias | Recibo final |
|---|---:|---:|---:|---|
| FiniteCoordinateMap | 22 | 5 | 27 | BUILD_20260909_153830_997115 |
| FiniteLeviCivita | 8 | 2 | 10 | BUILD_20260909_154525_107054 |
| FiniteCurvatureAlgebra | 5 | 5 | 10 | BUILD_20260909_155616_767490 |
| FiniteCoordinateCurvature | 6 | 1 | 7 | BUILD_20260909_155846_206162 |
| FiniteRicciContraction | 4 | 0 | 4 | BUILD_20260909_160651_571489 |
| FiniteEinsteinNaturality | 5 | 0 | 5 | BUILD_20260909_160816_702038 |

[DERIVED — conteúdo formal, agora compilado] A cadeia é a seguinte:

1. J(x) é efetivamente Dφ no ponto x, e D(x) é Dψ no ponto φ(x). A regra da cadeia e as identidades locais de inversa fornecem DJ = JD = I, det J ≠ 0 e D = J⁻¹. A métrica puxada é g′ = Jᵀ(g∘φ)J, sua inversa é D(g⁻¹∘φ)Dᵀ, e ambas têm regularidade derivada.
2. A conexão candidata Γ′ᵢ = D[(Σₐ Jₐᵢ Γₐ∘φ)J + ∂ᵢJ] é compatível com g′ e tem torção zero. A fórmula de Christoffel inferior demonstra a unicidade, identificando a candidata com a Levi-Civita calculada de g′.
3. Diferencia-se D pela identidade DJ = I. Os termos Hessianos e de terceira derivada cancelam por simetria das derivadas. Isso fornece a transformação finita R′ᵢⱼ = D[Σₐᵦ Jₐᵢ Jᵦⱼ (Rₐᵦ∘φ)]J, aplicada às derivadas reais da conexão.
4. A contração R(a,j)^a_b fornece Ricci′ = Jᵀ(Ricci∘φ)J. O cancelamento do índice interno usa a identidade de traço trace(DMJ) = trace(M), decorrente de JD = I. A curvatura escalar permanece igual após a transformação.
5. Conclui-se G[g′](x) = J(x)ᵀ G[g](φ(x)) J(x). O teorema einstein_finite_overlap_transformation estende a conclusão a qualquer campo h que coincida com g′ em todo o aberto de origem U.

[INPUT — hipóteses exatas da conclusão final] SmoothCoordinateChange U W fornece dois mapas reais suaves, U e W abertos, MapsTo em ambos os sentidos e identidades de inversa em cada aberto. g é suave e LorentzByCongruence em W. Para a versão em sobreposição, EqOn h (pullbackMetric C g) U é explícita. x pertence a U. Não se exige um campo inverso independente; metricInverse é a inversa matricial construída. A igualdade local em U determina também as derivadas usadas por Einstein, sem exigir novos postulados de naturalidade.

[DERIVED — aplicação à colagem] Para substituir a igualdade independente de Einstein em hmatch, deve-se apresentar uma mudança C real entre subabertos do encontro, identificar φ(y) com a coordenada x do mesmo ponto e fornecer a lei métrica em todo o subaberto. O fator F passa a ser changeJacobian C y, com não degenerescência derivada. A igualdade de Einstein então sai do teorema. Uma matriz arbitrária F e a igualdade de métricas somente no ponto não fornecem esse resultado.

[OPEN — fora desta entrega] A existência e a compatibilidade de um atlas físico concreto, a correspondência física que produz seus registros, a transformação da matéria e as leis de área/conservação permanecem obrigações separadas. Esta prova trata da Levi-Civita sem torção; não fornece a dinâmica de uma conexão independente com torção de Einstein–Cartan. Não constrói por si só uma solução global, não impõe a equação de Einstein e não resolve qualquer condição experimental. Nenhum argumento infinitesimal foi usado como substituto da transformação finita.

[REAL — preservação e escopo] Nenhum um.py foi executado ou importado. Todas as escritas ocorreram nesta pasta nova de Chatgpt. As cópias anteriores e o acervo canônico ficaram somente leitura. As fronteiras explicitamente registradas nos recibos foram medidas antes e depois; isso inclui a biblioteca aprovada de 45 módulos e as dependências diretas. Não foi feita recompilação nem hash de toda dependência transitiva do kernel/Mathlib. As tentativas falhas e os backups imediatos em bytes foram preservados.

O documento DERIVACAO_PREVIA.md permanece intacto como registro anterior à prova. Seus itens então abertos são resolvidos pelo alcance condicional acima, sem mudança retroativa do documento.

Hashes medidos das fontes e de seus recibos:
- FiniteCoordinateMap: 12469 bytes; SHA-256 1377e53e9871f4ad6fbfb0d59fc961164342eb39c9b8c6149a06b5ed1c51c2f1; recibo 3339f9997eacb96e5f227a61e50ff0a7990a2fd274ffa5c35ad6599c723f2731.
- FiniteLeviCivita: 8621 bytes; SHA-256 d52291cde391066d395e5bd1a786cba5a9d09033f21d2d310336d5df71f951f5; recibo 8ecd672a5ed86b880d15013ffb288ef64758dcd2f979d038bae715ef14be4f6d.
- FiniteCurvatureAlgebra: 4500 bytes; SHA-256 b89f04e2f26314fcaeffaa76de5d40b517cc5a1a01546c9172d037d75c785111; recibo ecb0682f18cbc465119192be877a483c1fbf832f85cd5e871c2bc023da7acb9b.
- FiniteCoordinateCurvature: 8101 bytes; SHA-256 2b172bffdcdce7b7abf7da397cbf693de4707b260cf3145f453af0e234e53a65; recibo aaaf16466cb60942e60ddb58b3f07524f8b4d0c13b3f6ef8a92fc179f8e08d62.
- FiniteRicciContraction: 3661 bytes; SHA-256 3a03d216e629850988d6e59e1028d8c1b99fbc8fb8195970d34fd3d896291afd; recibo 757f2c52f58e81a3dc3bb24fe4460518eafd51e0b90828683b9f8d6c81a7112a.
- FiniteEinsteinNaturality: 4809 bytes; SHA-256 d26cf29e648b3d08a7193d139df64008f79a310b03a2f8c8bfb950b62df0548a; recibo 4d6bbdc8fe0920d2c5bd2e9c24e906df4f356e21de4f23da2d19f8492d8431a2.
