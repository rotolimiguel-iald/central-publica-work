[REAL] O módulo ScalarEinsteinLieNaturality.lean está congelado e compilado: 15 teoremas e 1 definição, 16 termos auditados. Os dois processos Lean encerraram com código zero; os logs não contêm avisos. Todos os termos usam apenas propext, Classical.choice e Quot.sound. Recibo: [BUILD_RESULT.json](./BUILD_20260909_145854_177250/BUILD_RESULT.json). Revisão semântica independente da raiz favorável à fonte integral e ao delta final.

[DERIVED] Fechamento obtido nesta carta: para a família métrica efetiva g_t=g+t·L_Vg, com inversa matricial efetiva e conexão de Levi-Civita efetiva, dR(g_t)/dt em zero é V∂R(g), e dG(g_t)/dt em zero é L_VG(g). Esses são enunciados HasDerivAt, não operadores de variação apenas nomeados. A naturalidade de Ricci usada é a folha RicciLieNaturality previamente compilada; a variação geral real do escalar/Einstein é MetricEinsteinVariation.

[INPUT] Os teoremas finais recebem U aberto, g e V suaves em U, g simétrica e invertível em U, e um ponto x∈U. Nenhuma equação de Einstein, assinatura lorentziana, condição de energia, escolha de fonte, dinâmica quântica ou seleção de resultado é acrescentada como hipótese. Não se afirma que essa regularidade seja mínima.

A cadeia demonstrada usa a contração canônica Σij gInv_ij Ric_ij sem trocar silenciosamente por outra contração:
- Linha 14: tensorPair é exatamente a soma dupla canônica.
- Linhas 28 e 33: duas identidades de produto com transposta, provadas por álgebra finita.
- Linha 38: transporte da contração vem da regra de produto das derivadas espaciais efetivas de ambos os fatores.
- Linha 70: −gInv·(L_Vg)·gInv = V∂gInv − P·gInv − gInv·Pᵀ, com P a Jacobiana efetiva de V.
- Linha 86: igualdade do operador Ricci pela unicidade de duas derivadas da mesma família.
- Linhas 99 e 127: cancelamento dos termos P e naturalidade escalar da família efetiva.
- Linhas 142, 163 e 178: divisão por dois, diferença e produto escalar da derivada de Lie.
- Linhas 190 e 215: todas as parcelas de G=Ric−(R/2)g produzem a naturalidade de Einstein da família efetiva.

[REAL — revisão independente] A raiz leu o núcleo e depois a fonte completa, confirmando a contração efetiva, os jets da inversa/curvatura, a unicidade de Ricci e todas as parcelas de Leibniz em Einstein. Essa revisão foi registrada sobre o hash medido abaixo; o construtor não se apresentou como revisor independente.

[OPEN — limite de alcance] O resultado é naturalidade infinitesimal local na carta. Não constrói um difeomorfismo global, não prova por si a colagem entre cartas e não demonstra identidade de Ward de uma teoria quântica nem ausência de anomalias. Não escolhe a métrica física nem deriva as leis de área ou de produção de registros. Não é nova afirmação de resolução/confirmacão da gravidade quântica.

[REAL — custódia] Fonte com 11729 bytes; SHA-256 medido: abba0e104b39bb5020ffc4e5f116b632ba8a38f9f70ee545e81e613fbe5271a4. A fonte é idêntica à copiada na build PASS. As duas tentativas anteriores, diagnósticos e backups imediatos de bytes permanecem disponíveis. As dependências locais foram copiadas de recibos PASS, com hashes verificados; esta rodada recompilou apenas a folha nova e o agregador de importação, lendo os binários canônicos e Mathlib existentes. Não houve rebuild integral das dependências, alteração de original ou execução/importação de um.py.

Integração mecânica futura: transpor somente os imports locais MetricEinsteinVariation e RicciLieNaturality para os respectivos TGLExt., preservar namespace ChatgptAudit.EinsteinLie e acrescentar auditorias pelos nomes completos. Não criar flags de fechamento quântico a partir deste suplemento.
