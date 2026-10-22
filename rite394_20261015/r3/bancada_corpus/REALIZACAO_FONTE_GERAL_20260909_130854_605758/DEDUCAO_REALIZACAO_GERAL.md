# Realização unitária de fonte simétrica geral — 09/09/2026

[REAL] GeneralSourceUnitaryRealization.lean, namespace ChatgptAudit.GeneralSourceUnitary: **19 teoremas + 5 definições**, 24 termos auditados, dois processos Lean com saída zero, zero warnings/erros. SHA-256 lido: 3c3107a03a7b1e40f289bed1ef1a423c9497ef0c5bb255fbbeb45b3da0353b8e. Recibo final: BUILD_20260909_132346_182654/BUILD_RESULT.json. A fonte está congelada; os axiomas observados ficam em propext, Classical.choice e Quot.sound.

[REAL] A primeira tentativa atingiu timeout de 240 s no módulo novo. A segunda, com auditorias intercaladas, isolou três custos de inferência em chamadas que deixavam a frequência implícita. A terceira forneceu explicitamente a frequência w_j(d) e passou. Enunciados não mudaram. O timeout, o build FAIL_VISIBLE e os backups de bytes anteriores foram preservados; termos incompletos do build falho não são evidência de prova.

## O que foi realizado

[DERIVED] Se g é uma métrica lorentziana na carta e T é um tensor simétrico fornecido, a construção usa sua completação de traço F=T−(tr(g⁻¹T)/2)g. Para cada índice i de 0 a 3, a polarização fornece covetores p_i=(row_i(F)+e_i)/2 e m_i=(row_i(F)−e_i)/2. A soma de p_i⊗p_i−m_i⊗m_i é F. A completação de traço aplicada duas vezes em dimensão quatro devolve T.

[DERIVED] A calibração usa dois acoplamentos efetivos reais, κ+>0 e κ−<0, provenientes das preparações canônicas com eixos (−3/5,4/5) e (0,1), ambas com amplitudes iniciais (3/5,4/5). As escalas reais r+=√(8/κ+) e r−=√(8/(−κ−)) satisfazem

(1/8)κ+ r+² = +1 e (1/8)κ− r−² = −1.

Portanto os pesos dos oito rótulos continuam positivos e somam um; os sinais da cobertura são carregados pelos acoplamentos. positive_scale_identity, negative_scale_identity, positive_calibration e negative_calibration fazem essa ligação na fonte UnitarySourceCalibration importada.

[REAL] calibrationLabelData (linha 16) reúne os oito rótulos, peso 1/8, eixos normalizados e amplitudes iniciais positivas normalizadas. calibrationSourceCovectors (linha 31) aplica os covetores calibrados a F(x), usando metricInverse construída de g. realized_source_eq (linha 80) prova que a finiteCoherentStressField correspondente é exatamente T(x), para g(x) lorentziana e T(x) simétrica. realized_source_eq_on (linha 90) estende a igualdade ao domínio admissível.

[REAL] Os covetores e o tensor realizado são suaves quando g e T são suaves no aberto e g é lorentziana nele (linhas 72 e 106). A fonte é simétrica pela simetria de g (linha 98). A igualdade é algébrica e pontual; a suavidade é uma conclusão separada, não uma hipótese escondida na igualdade.

[REAL] realized_source_divergence_eq (linha 116) transporta a divergência por igualdade de campos num aberto. realized_source_conserved (linha 128) recebe conservação TOTAL de T e conclui conservação da representação. Não supõe que cada covetor polarizado seja fechado ou satisfaça uma equação de onda. Essas leis setoriais pertencem a outra rota suficiente, comprovada no módulo FiniteCoherentSources.

## Estado, evolução e resposta

[REAL] A curva atua em oito rótulos vezes duas componentes: 16 resultados diagonais. A base é positiva e normalizada (linhas 55 e 61); os pesos da curva são não negativos e normalizados para todo parâmetro t (linhas 140 e 146). Há um fluxo unitário por blocos (linha 211), e os módulos quadrados das amplitudes evoluídas coincidem com os pesos diagonais (linha 219).

[DERIVED] A frequência do bloco j é w_j(x)(d). A base inicial jointBase calibrationLabelData é fixa, independente de T; T entra nos covetores, frequências e resposta da evolução. Assim a presente construção não demonstra identificação de T arbitrário por um único ângulo da base inicial. É uma realização explícita da fonte fornecida por uma família de preparações.

[REAL] A tangente diagonal inicial é zero (linha 152), mas a resposta quadrática pode ser não nula. Os limites entrópico e modular foram provados nas linhas 158 e 166. Para d nulo em g,

calibrationSourceResponse(g,T,x,d) = −π T_x(d,d)

(linha 174), e os limites correspondentes possuem esse coeficiente (linhas 189 e 200). A entropia aqui é a entropia dos pesos diagonais; não se identifica com a entropia de von Neumann do vetor puro global. Respostas medidas apenas no cone nulo também não distinguem T de T+c g por si; a cobertura completa usa os covetores fornecidos.

## Alcance e próximo elo

[INPUT] T é fornecido e sua conservação total é uma hipótese na rota geral. A calibração realiza matematicamente T; ela não é uma lei de produção física de T. Acoplamentos dos dois sinais não implicam a condição de energia nula positiva por setor. Nenhuma inversão irreversível do colapso é reivindicada.

[INPUT] O módulo GeneralSourceEinsteinBridge, desenvolvido separadamente na mesma pasta, compõe a realização com a ponte de calor e área. Seu estatuto de compilação será registrado em recibo próprio. A lei de área permanece explícita e equivale ao balanço nulo de Ricci; não é obtida automaticamente da existência da representação unitária.

[DERIVED] O módulo JointPreparationCovariance, revisado separadamente, transporta a família escolhida sob mudança de base pontual. Isso não afirma que regenerar a polarização dos oito covetores em outra carta produz o mesmo estado. A globalização por cartas e o controle das transformações da conexão são assuntos distintos.

[REAL — revisão independente nesta sessão] /root/review_remaining_hypotheses leu os enunciados e a calibração importada e deu parecer favorável no alcance acima. Verificou a separação entre base fixa e frequências dependentes de T, a calibração assinada, a igualdade da fonte e o transporte da conservação total. A revisão não recompilou a fonte. A correção posterior somente explicitou argumentos de frequência, reduziu o limite de heartbeats e intercalou auditorias.

[REAL] A compilação final reutilizou cópias de cinco módulos locais com recibos PASS, igualdade de suas fontes e hashes verificados antes/depois. O novo módulo e seu agregador de imports foram compilados novamente. Dependências transitivas canônicas e Mathlib não foram integralmente recompiladas nem individualmente medidas. Nenhum original foi modificado, nenhum um.py foi executado ou importado e nenhum gate foi alterado.

[INPUT — integração] A transposição deve manter namespace e enunciados, convertendo apenas os três imports locais para TGLExt.UnitarySourceCalibration, TGLExt.FiniteCoherentSources e TGLExt.JointUnitaryPreparation. Acrescentar os 19 teoremas únicos ao Audit numa NOVA cópia do programa, preservando as anteriores.
