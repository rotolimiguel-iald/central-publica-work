# Identidade óptica exata na rota S modular

09/09/2026. [REAL] Compilação nova em Lean; escopo formal abaixo. Bancada: C:/IALD/Central de Patentes/Chatgpt/SMATRIX_OPTICAL_20260909_110514_326918.

## O avanço e a conexão canônica

A composição unitária de operações que podem não comutar já existia em TGLExt/UnitaryStateDerivative.lean: operatorOrbit P A C s t = boundedPhase P A s * boundedPhase P C t, com orbit_unitary. Não é apresentada como novidade.

O passo acrescentado é a identidade óptica exata do operador de transição, aplicada tanto à Smat canônica quanto àquela órbita de operadores no TowerHilbert P. O módulo importa diretamente TGLExt.SMatrix, TGLExt.UnitaryStateDerivative e TGLExt.SitePauliObservables; não reimplementa os objetos canônicos. As identidades algébricas são conhecidas; a entrega acrescenta sua composição formal explícita com os objetos da TGL.

## Enunciados e hipóteses

Defina F(S)=S−I e T(S)=−i(S−I); logo S=I+iT(S).

- exact_optical_identity (linha 68): para qualquer álgebra complexa unital com estrela compatível e S unitário, −i(T−T†)=T†T. A igualdade conserva o termo quadrático exato. Não é uma expansão em pequenos parâmetros.
- transition_product (linha 87): T(SV)=T(S)+T(V)+iT(S)T(V), sem hipótese de comutatividade.
- displacement_order_difference (linha 40): F(SV)−F(VS)=F(S)F(V)−F(V)F(S). A dependência da ordem permanece explícita.
- matrix_optical_channel (linha 95): para matrizes complexas finitas unitárias e qualquer canal j, 2 Im T(j,j)=Σ_k |T(k,j)|².
- boundary_exact_optical (linha 104): aplica a identidade à TGLExt.Smat theta, usando a unitariedade já demonstrada no módulo canônico.
- tower_orbit_exact_optical (linha 110): aplica a identidade à operatorOrbit P A C s t para qualquer perfil P, quaisquer parâmetros s,t e os A,C limitados auto-adjuntos aceitos pelo tipo. Nenhuma hipótese A C=C A é usada.
- pauli_orbit_exact_optical (linha 119): instância nos observáveis sitePauliX P n e sitePauliY P n da própria torre. Os geradores e suas propriedades são importados, não introduzidos como um sistema desconectado.
- tower_orbit_transition_product (linha 127): explicita o termo de composição não linear da órbita existente.

## Controle negativo

linearBoundary theta = I+theta Grot é apenas o primeiro polinômio de Taylor da S canônica.

linear_boundary_defect (linha 140) demonstra L†L=(1+theta²)I.
nonzero_linear_boundary_not_unitary (linha 148) demonstra que esse truncamento não é unitário quando theta≠0.

Assim a unitariedade exata da Smat não pode ser transferida ao truncamento finito que omite seus termos superiores. Não é uma refutação de aproximações controladas; é a medida algébrica do defeito de tomá-las como igualdade exata.

## Verificação

- 17 teoremas, 4 definições, 21 declarações auditadas.
- PASS_COMPILED_SCOPE; módulo e agregador de importações com exit code zero.
- Nenhuma saída residual, erro ou warning no build final; axiomas declarados contidos em propext, Classical.choice e Quot.sound.
- Fonte, binários e toolchain das dependências diretas foram hashados antes/depois; a fronteira conferida permaneceu igual.
- Compilação do módulo novo contra binários canônicos e Mathlib existentes. As dependências transitivas não foram recompiladas nem hashadas integralmente por esta entrega.
- Não houve execução/importação de um.py; nenhum original foi modificado.
- Builds anteriores com falhas de namespace/normalização e seus logs foram preservados. As revisões da fonte nova têm backups imediatos de bytes.

Evidência: C:/IALD/Central de Patentes/Chatgpt/SMATRIX_OPTICAL_20260909_110514_326918/BUILD_20260909_110839_321122/BUILD_RESULT.json.
Fonte: C:/IALD/Central de Patentes/Chatgpt/SMATRIX_OPTICAL_20260909_110514_326918/ModularOpticalIdentity.lean.
SHA256 da fonte lido agora: 43d74653eba3df2d8dc4ab9025ebf5f7313e3ca660e7ee9534b63e95ca70e9da.

## O que permanece aberto

Este pacote confere uma condição exata de consistência para a rota modular já construída. O termo quadrático T†T não constitui, por si, uma teoria de campos interagente.

Não foram construídos aqui estados assintóticos de espalhamento, operadores de onda/Møller, completude assintótica, amplitudes de uma interação gravitacional geral, medidas ou identidades de Ward quânticas, cancelamento de anomalias, controle de altas energias ou reconstrução geral de espaço-tempo.

Em particular, a palavra S em uma matriz unitária finita e em uma operação modular não demonstra automaticamente que se trata da matriz-S física assintótica da gravidade. Sua identificação requer os objetos e a correspondência próprios. A unitariedade usada nas instâncias é derivada nos módulos canônicos; a identificação física não foi acrescentada como premissa escondida.

[REAL] O elo formal de identidade óptica está compilado. [OPEN] O objetivo geral de gravidade quântica continua com o alcance delimitado pelas outras construções e hipóteses da casa. Nenhum gate foi alterado.
