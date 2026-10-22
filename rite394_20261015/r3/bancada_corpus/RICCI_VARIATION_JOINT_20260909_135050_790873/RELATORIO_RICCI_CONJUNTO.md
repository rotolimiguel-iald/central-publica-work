# Ricci de uma família conjuntamente suave
[REAL — prova Lean e revisão independente; INPUT — regularidade conjunta explícita]

O módulo prova a derivada do Ricci canônico de Gamma(t,x), para uma família de conexões conjuntamente C∞ em um aberto W de R×Coordinate4, no ponto (t,x) de W. A família não precisa ser afim no parâmetro.

connectionTimeDerivative é definida pelo fderiv conjunto na direção (1,0). time_slice_derivative e connection_parameter_derivative demonstram que esse valor é a derivada temporal real da conexão. space_slice_partial identifica o jet espacial canônico com a derivada conjunta na direção (0,e_i).

A derivada de jointPartial é calculada pelo fderiv da primeira derivada. A simetria da segunda derivada decorre da regularidade C∞ pela biblioteca; nenhuma comutação é hipótese. time_derivative_of_space_partial usa essa simetria e a continuidade da inclusão s↦(s,x) para transportar a igualdade local no aberto à função temporal por igualdade eventual. O resultado é HasDerivAt do próprio jet espacial.

As regras de produto aplicadas às duas multiplicações da curvatura canônica produzem curvatureVariation. A soma finita da contração canônica de coordinateCurvature produz ricciVariation. O teorema ricci_of_joint_family_derivative refere-se ao coordinateRicci real da família, e não a uma operação de mesmo nome definida independentemente.

## Alcance e revisão

A regularidade conjunta C∞, a abertura de W e a pertença do ponto a W são hipóteses explícitas; a otimização para C² não foi tentada. A identidade temporal/espacial e a primeira variação são conclusões, não dados fornecidos. O módulo não exige nem afirma que Gamma seja Levi-Civita. Sua aplicação à família métrica real é tratada em um módulo seguinte, sem alterar este núcleo congelado.

A identidade é de primeira ordem para uma família arbitrária. Ela não identifica a expansão de segunda ordem de uma família não afim com o termo quadrático calculado para Gamma+tC no lote anterior. Não é Ward sob difeomorfismos nem demonstração de ausência de anomalias quânticas.

O root realizou revisão semântica integral e a considerou favorável: confirmou a troca efetivamente derivada por Schwarz e igualdade eventual no aberto, a contração real de Ricci e a inexistência de hipótese hjet escondida. A fonte permaneceu congelada após o PASS.

## Custódia

Pasta nova; dedução registrada antes do código; backups de bytes em cada correção; builds anteriores preservadas. Nenhum original/um.py foi alterado, executado ou importado. A folha e o agregador foram compilados contra cópias verificadas dos módulos locais PASS e binários canônicos/Mathlib preexistentes. Não se declara recompilação de toda a árvore transitiva.

[REAL — medidas finais]

10 teoremas +4 outros termos =14 auditorias; dois exits0, nenhum warning, trio de axiomas. Fonte: 7283bytes; SHA-256 f3cdf9bfd0f165ebcfce25b303a188b345161a0743f72fdb6055d0dc03e6cb3b. Build: BUILD_20260909_135701_498129/BUILD_RESULT.json.

- ParameterSpace: linha11
- jointPartial: linha13
- JointSmoothConnectionOn: linha16
- connectionTimeDerivative: linha19
- joint_partial_smooth: linha22
- joint_partial_second: linha27
- joint_partials_commute: linha38
- time_slice_derivative: linha46
- space_slice_partial: linha53
- time_derivative_of_space_partial: linha64
- connection_parameter_derivative: linha89
- connection_first_jet_parameter_derivative: linha97
- curvature_of_joint_family_derivative: linha106
- ricci_of_joint_family_derivative: linha122
