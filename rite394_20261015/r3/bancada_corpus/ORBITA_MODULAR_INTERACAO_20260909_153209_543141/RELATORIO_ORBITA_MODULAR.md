[REAL] Órbita modular do potencial XX somável construída pela ação canônica: α_t(V) = modularConjugation P t (certifiedInteraction P c). O módulo novo está congelado, com 24 teoremas e 3 definições, 27 auditorias, dois processos Lean exit 0, zero avisos e apenas propext, Classical.choice e Quot.sound. [Recibo de compilação](./BUILD_20260909_153346_145753/BUILD_RESULT.json).

[REAL — v322 localizado e lido] LikelihoodCocycle.lean:32 define exp(i·s·likelihoodGenerator b t) no perfil thirdThermalReference. O teorema da linha 98 prova fixidez modular; a identidade torcida da linha 104 usa essa fixidez para reduzir a lei torcida à lei de grupo. SummableLikelihoodGenerator.lean:138 já prova que o gerador é fixo. Os termos também estão no centralizador (linha 60), cujo fechamento em norma está na linha 46. O Atlas, adendo v322, linhas 11932–11935, delimita a família comutante; o índice vivo lista seus seis módulos. Assim, esse construtor específico não fornece, por instanciação direta, o novo potencial XX exterior ao centralizador. Isso preserva integralmente o resultado v322 em sua classe.

[DERIVED] A construção nova usa a ação modular já existente em ModularFlowAlgebra.lean:63, obtida de modularFlowUnitary. Não postula uma ação substituta. As propriedades demonstradas são:
- Linhas 20–54: lei de grupo, identidade temporal, preservação exata da norma e isometria da conjugação canônica nos operadores.
- Linhas 57–81: continuidade em norma das órbitas locais, dos sítios, dos produtos XX e dos prefixos finitos. A passagem usa modularConjugation_local, flowLevel_continuous e towerPiLinear contínua por dimensão finita.
- Linhas 83–108: α_0(V)=V, covariância α_s(α_t(V))=α_(s+t)(V), auto-adjunticidade, pertencimento ao fator e norma exatamente igual a ‖V‖≤Σ|c_j|.
- Linhas 110–119: ‖α_t(V)−α_t(V_N)‖=‖V−V_N‖≤Σ_(j≥N)|c_j|, com a mesma cauda para todo t.
- Linhas 121–156: continuidade em norma da órbita limite por aproximação ε/3; para cada ε>0 há N que funciona para todos os cortes n≥N e todos os tempos reais.
- Linhas 158–179: o coeficiente B(t)=i·α_t(V) é contínuo, anti-auto-adjunto, pertence ao fator, tem norma constante e obedece à mesma covariância.

[INPUT] A interface exige P:SiteProfile e c:SummableCouplingData, incluindo prova efetiva de Σ|c_j|<∞. A norma totalizada de tsum fora desse domínio não serve como certificado. Não há hipótese de limite uniforme das frequências logarítmicas dos sítios. A derivabilidade da órbita em t não foi afirmada; apenas sua continuidade em norma, suficiente para servir como coeficiente da ODE na composição seguinte.

[DERIVED — convenção da ODE] O coeficiente entregue é B(t)=i·α_t(V)=α_t(iV). Para u(t)=exp(it(H₀+V))exp(−itH₀), a convenção correspondente é u′(t)=u(t)·B(t), com o coeficiente à direita, e a lei torcida alvo é u(s+t)=u(s)α_s(u(t)). Este módulo não resolve essa ODE nem assume sua solução em uma estrutura. A construção do cociclo é outra folha.

[OPEN] Não se construiu aqui o estado perturbado, uma derivada de Radon–Nikodym modular para todos os pares de estados, a identificação de um gerador quântico gravitacional ou um limite UV relativista. Os acoplamentos XX entre si comutam; sua interação bipartida e sua possível exclusão do centralizador são propriedades distintas. A continuidade em norma foi provada para esta classe somável de operadores, não para toda órbita de todo operador do fator.

[REAL — revisão independente] A raiz leu a fonte integral congelada e aprovou: conjugação canônica real, norma nos dois sentidos, continuidade local finita seguida de ε/3, cauda uniforme em todo t e coeficiente i·α(V), sem exigir derivabilidade não demonstrada. A revisão é de enunciados e provas, separada da compilação do construtor.

[REAL — custódia] Fonte com 9851 bytes, SHA-256 medido cbe89365a504e4590a6ada7a4fb3963dfc140f652ef4944c58a5d540bea9d31c, idêntica à cópia da build PASS. A primeira falha e o backup imediato de bytes estão preservados. A rodada recompilou a folha nova e um agregador; as três dependências locais de interação foram copiadas de builds PASS, verificadas por bytes e recibos. Binários canônicos/Mathlib existentes foram lidos; dependências transitivas não foram recompiladas integralmente. Nenhum original alterado e nenhum um.py executado/importado.

Integração futura: preservar namespace ChatgptAudit.InteractionOrbit; transpor somente o import local AdmissiblePauliInteraction para TGLExt.AdmissiblePauliInteraction e auditar os nomes completos. Nenhuma flag/gate quântico é alterado por esta entrega.
