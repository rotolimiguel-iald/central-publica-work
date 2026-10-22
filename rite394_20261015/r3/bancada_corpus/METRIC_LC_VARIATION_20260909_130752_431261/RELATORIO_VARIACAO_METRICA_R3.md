# Variação métrica da conexão canônica — entrega R3
[REAL — fonte e compilação medidas abaixo; DERIVED — dedução matemática; OPEN — elos delimitados]

Foi provada a primeira variação da própria `leviCivitaField` canônica, calculada com o campo métrico g+t h e a inversa matricial real desse campo. O resultado não introduz uma conexão de nome semelhante sem vínculo com o kernel.

Para g e h suaves em U aberto, x em U e g(x) invertível:
δ(g⁻¹) = −g⁻¹ h g⁻¹;
δΓᵢ = −g⁻¹ h g⁻¹ Lᵢ(dg) + g⁻¹ Lᵢ(dh)
     = −g⁻¹ h Γᵢ + g⁻¹ Lᵢ(dh),
onde L é exatamente `lowerChristoffelJet` e dg é exatamente `tensorFieldJet`.

## Encadeamento formal

- `matrix_inverse_first_variation`, linha 32: HasDerivAt da função t ↦ (g+t•h)⁻¹, com hipótese IsUnit g. Aplica o resultado matemático `hasFDerivAt_ringInverse` de Mathlib, identificando a inversa usual por `Matrix.nonsing_inv_eq_ringInverse`. A norma matricial de operador fornece a álgebra normada exigida; o transporte às instâncias topológicas canônicas é verificado pelo Lean.
- `metric_perturbation_jet`, linha 56: deriva a linearidade do jet espacial REAL de g+t h a partir da suavidade de g e h. Não recebe os jets como símbolos independentes.
- `perturbed_levi_civita_jet_formula`, linha 68: igualdade exata, para todo parâmetro real t, entre a conexão canônica do campo perturbado e (g+t h)⁻¹[L(dg)+t L(dh)].
- `levi_civita_metric_first_variation`, linha 79: HasDerivAt da conexão canônica perturbada em t=0, com derivada `metricConnectionVariation`. A regra de produto e a regra da cadeia descarregam a derivada; nenhuma hipótese identifica previamente δΓ.
- `metric_connection_variation_formula`, linha 97: reescrita equivalente −g⁻¹ h Γ + g⁻¹ L(dh), com a conexão canônica do campo de fundo.
- `matrix_perturbation_eventually_invertible`, linha 111: IsUnit g implica IsUnit(g+t h) para t suficientemente próximo de zero. É uma afirmação por matriz/ponto, não um raio uniforme em toda uma região não compacta.
- `perturbed_levi_civita_torsion_free`, linha 120, e `perturbed_levi_civita_metric_compatible`, linha 130: os certificados canônicos acompanham a mesma família. A ausência de torção usa simetria de g e h no aberto; a compatibilidade métrica usa também a não degenerescência do campo perturbado na região considerada.
- `constant_metric_jet`, linha 141, e `constant_background_metric_variation`, linha 146: um fundo constante tem jet zero, e δΓ reduz a G⁻¹L(dh). A igualdade algébrica aceita qualquer matriz G; para interpretar a derivada de uma métrica, aplica-se o resultado anterior com G invertível e simétrico.

## Aplicabilidade e limites

A fórmula de derivação matricial, tomada isoladamente, também vale para matrizes não simétricas. Sua interpretação como Levi-Civita de uma métrica não degenerada acrescenta a simetria e a invertibilidade, com certificados formais separados. Não se afirma neste lote preservação da assinatura Lorentziana por toda a família, nem um raio uniforme de não degenerescência sobre U.

Esta etapa reduz concretamente a lacuna do lote CurvatureNonlinearVariation: a direção de conexão já pode ser produzida como derivada de uma métrica real. O lote anterior provava a expansão de curvatura para Γ+tC. A família Levi-Civita(g+t h) geralmente NÃO é afim em t; sua primeira derivada é C, mas seus termos de ordem superior não são os da linha afim Γ+tC.

[OPEN] Ainda se deve provar, com regularidade conjunta e troca justificada de derivadas temporal/espacial, que a derivada de `coordinateRicci (perturbedLeviCivita g h t)` é exatamente a `ricciVariation` anterior aplicada a Γ e `metricConnectionVariation g h`. A ligação do limite plano ao operador `linRicci` canônico é consequência pretendida desse elo, não um teorema já incluído aqui.

[OPEN] Para a Ward métrica em fundo curvo, escolher h como a derivada de Lie da métrica e provar a naturalidade: a variação de Ricci acompanha a derivada de Lie de Ricci. Em fundo curvo genérico ela não é automaticamente zero. O anulamento gauge de um operador linearizado requer especificar o tensor de equação e um fundo que satisfaça essa equação. A mudança de referencial da conexão GL do lote anterior é um controle distinto.

Este é avanço clássico de geometria diferencial, sem conclusão sobre anomalias quânticas interagentes, dinâmica UV ou resolução geral da gravidade quântica. Não altera gate, selos, Atlas ou o programa canônico.

## Custódia e reprodução

A pasta é nova sob Chatgpt; cada edição local manteve backup imediato dos bytes anteriores. As versões intermediárias e builds malsucedidas foram preservadas. Nenhum um.py foi executado ou importado. Os imports são canônicos, sem transposição local adicional. A build compila novamente o módulo novo e seu agregador, usando binários preexistentes de TGLExt e Mathlib; mede antes/depois as fontes e binários das dependências diretas e a ferramenta. Não se declara recompilação nem hash de toda a árvore transitiva.

Os números, hashes e resultados efetivamente medidos constam em MANIFESTO_ENTREGA.json e no BUILD_RESULT.json indicado ali. A aprovação semântica independente cabe ao revisor, separada do passe do Lean.

[REAL — medição final]

- Build: BUILD_20260909_132230_999137/BUILD_RESULT.json; PASS_COMPILED_SCOPE.
- 14 teoremas + 4 definições = 18 termos auditados; dois exits 0, sem warnings.
- Fonte: 8112 bytes; SHA-256 224b7ddb8d7165bb502268958ab7510db82467b54a6391c53cdf9a945ba36abc.
