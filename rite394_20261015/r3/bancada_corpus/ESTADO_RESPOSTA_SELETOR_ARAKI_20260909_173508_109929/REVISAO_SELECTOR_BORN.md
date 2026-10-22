# Revisão independente: CanonicalSelectorBorn

Data: 09/09/2026. Parecer FAVORÁVEL no alcance dos enunciados. Fonte: [CanonicalSelectorBorn.lean](<C:/IALD/Central de Patentes/Chatgpt/SELETOR_BORN_REGISTRO_20260909/CanonicalSelectorBorn.lean>). Recibo: [BUILD_RESULT.json](<C:/IALD/Central de Patentes/Chatgpt/SELETOR_BORN_REGISTRO_20260909/BUILD_20260909_172830_186727/BUILD_RESULT.json>). Medidas atuais de bytes/hashes, declarações, logs e binários estão em EVIDENCIA_E_REVISAO.json deste lote.

[REAL — fonte e recibo conferidos] São 15 teoremas e 3 definições, 18 auditorias com apenas propext, Classical.choice e Quot.sound, dois exits 0 e nenhum aviso/erro nos logs conferidos. A fonte atual coincide em bytes e hash com a fonte registrada no PASS. Esta revisão não recompilou a folha nem toda a cadeia transitiva.

[REAL — sentido dos enunciados] O módulo usa o ialdSelector canônico em ellTwo, e não um projetor homônimo. As inscrições e₀ e e₁ são ortonormais, P e₀=e₀ e P e₁=0. Para a∈ℝ, constrói ψ(a)=sin(encodeAngle a)e₀+cos(encodeAngle a)e₁, prova ‖ψ(a)‖=1 e obtém:

- Pψ(a)=sin(encodeAngle a)e₀;
- p(a)=‖Pψ(a)‖²=encodeScalar a, com 0<p(a)<1;
- decodeScalar(p(a))=a e p(a)=p(b) se, e somente se, a=b;
- Pψ(a)/‖Pψ(a)‖=e₀ para todo a.

O argumento de normalização usa ortogonalidade e sin²+cos²=1. A positividade estrita de sin no intervalo codificado justifica o cancelamento. O pós-vetor normalizado realmente esquece a, como o último teorema declara. A informação recuperável está no peso registrado antes da normalização, e não num ângulo escondido do vetor e₀.

[DERIVED — leitura operacional] Isso realiza um registro de Born exato para o dado a fornecido à preparação. A prova não infere a probabilidade de um único resultado físico. Para usar o decoder é preciso dispor do peso p — por preparação conhecida, registro matemático ou estimação justificada por um protocolo adicional. Uma seleção isolada, com resultado e₀, não diferencia os valores de a.

## Precisões de zero, fidelidade e objeto

A definição normalizedSelected é total. Se Px=0, a convenção de inversa de zero produz o vetor zero. Os teoremas sobre scalarPreparation evitam esse caso por p(a)>0; não proclamam normalização de toda entrada arbitrária.

A fórmula bornWeight é definida para qualquer x, mas a garantia probabilística aqui é aplicada a ψ(a) normalizada. Não se deve tomar bornWeight(x)≤1 para um x arbitrário sem a hipótese correspondente.

As probabilidades p e 1−p são estritamente positivas na leitura binária. Isso dá suporte completo na álgebra comutativa dessa medição. O vetor ψ(a), porém, define um estado puro em B(ellTwo), e sua restrição à álgebra matricial completa gerada por e₀,e₁ continua pura; não é fiel nessas álgebras. “Fidelidade” do codec pode designar sua injetividade, mas não deve ser confundida com fidelidade de estado de Araki.

O módulo não identifica ellTwo, ψ(a) ou sua distribuição com TowerHilbert P, Ω_V ou ω_V. Tampouco determina a resposta de matéria R a partir da interação. Esses limites preservam o valor do resultado: há um elo explícito entre o seletor canônico e a codificação de um escalar por peso de Born.
