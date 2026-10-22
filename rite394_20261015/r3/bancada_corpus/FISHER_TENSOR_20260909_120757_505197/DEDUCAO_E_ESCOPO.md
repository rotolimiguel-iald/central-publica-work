# Tensor de informação e correspondência termodinâmica geral

[REAL — compilado nesta bancada] Fonte congelada: FisherInformationTensor.lean.
Namespace: ChatgptAudit.FisherField. Build: BUILD_20260909_121149_390313.
Foram medidos 22 teoremas, 5 definições e 27 declarações auditadas.
Os dois processos Lean concluíram com exit 0; zero saída residual ou warnings.
Todos os axiomas impressos pertencem a propext, Classical.choice e Quot.sound.
SHA-256 lido do arquivo: 9b3bb75b946578ceb0580ad132f93544795190e401ebd067ea8b8d2b7825336e.

## Dedução e objetos

Para um conjunto finito de resultados i, valores positivos p_i e covetores dp_i, definimos
F_ab = Σ_i (dp_i)_a (dp_i)_b / p_i.
A definição usa a soma de produtos externos, e [fisher_tensor_entries](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:26) prova essa fórmula por componentes.

[fisher_tensor_symmetric](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:34) prova Fᵀ=F; [fisher_tensor_directional](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:38) prova
F(v,v)=Σ_i (dp_i(v))²/p_i=diagonalFisher(p,dp(v)).
A positividade dos p_i implica F(v,v)≥0; [fisher_tensor_null_iff](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:55) e [fisher_tensor_positive_iff](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:62)
caracterizam exatamente a degenerescência pela variação direcional nula.
A normalização Σp_i=1 não é necessária para essa álgebra. Ela entra na realização por estados.

Para um campo P:Coordinate4→ι→ℝ, probabilityDifferential usa o potentialCovector canônico:
dp_i=coordinatePartial(P_i), sem covetores livres inseridos à mão.
[directional_variation_fderiv](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:90) identifica sua leitura em v com fderiv(P_i)(v).
[fisher_field_smooth](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:100) deriva a suavidade de F em um aberto U de P suave e P_i>0 em U.

[DERIVED — consequência dos enunciados] F é um tensor de informação positivo semidefinido e pode ser degenerado.
Essa assinatura não é identificada com a métrica lorentziana g. Tampouco se identifica uma área de parâmetros com área espacial.

## Curva determinada pelo mesmo campo

[probabilityFieldCurve](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:149) constrói X.weights(t)=P(x+t•v) e
X.tangent(t)=directionalVariation(P,x+t•v,v).
A construção exige U aberto, x∈U, cada P_i suave em U e Σ_i P(y)_i=1 para todo y.
A normalização global atende ao tipo canônico DiagonalStateCurve; não se exige suavidade ou positividade global.
A positividade da referência P(x) garante positividade local por continuidade.
As identidades [probability_field_curve_tangent](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:166) e [probability_field_curve_fisher](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:173)
eliminam a escolha de uma curva microscópica independente.

[INPUT — interpretação] t parametriza a reta na carta espacial. Nenhum enunciado o identifica com tempo físico ou fluxo modular.

## Correspondência geral com Ricci

[probability_field_geometric_compatibility](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:232) compõe com geometric_microscopic_compatibility canônico.
Dados uma tela EquilibriumScreenData construída para g, Γ, x e v, a área é inducedArea e
o calor é constructedHeat, primitiva do fluxo −rate·t·T(V,V)·area.

As hipóteses materiais de correspondência são explicitamente:

- erro calor–incremento modular dividido por t² tende a zero no passado;
- erro entropia–eta·variação de área dividido por t² tende a zero no passado.

Exigem-se g e Γ suaves, T diferenciável, Γ sem torção no ponto, referência P(x) estritamente positiva,
rate≠0, a curva determinada acima e as propriedades geométricas da tela.
A conclusão é η Ricci_Γ(v,v)=2π T(v,v)+F_P(v,v).
Não se assume Ricci-balance, Einstein ou tangente nula nesse contrato.

[DERIVED — forma de composição] Para eta≠0, a equação pode ser reescrita usando fonte efetiva
T_eff=T+F/(2π) e acoplamento 2π/eta.
[OPEN nesta entrega] A conservação de T_eff não foi derivada. A conservação de T, isoladamente,
não fornece a conservação de F. ScalarStressConservation possui um teorema de conservação
para a tensão completada de covetores fechados que satisfazem equação de onda; isso não permite
atribuir conservação automática a F, cujos coeficientes 1/P_i variam.
As leis de matching continuam hipóteses independentes na apresentação, não são inferidas do codec ou da seleção.

## Controle Bernoulli angular

[bernoulli_tensor](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:183) prova, para p≠0 e 1−p≠0,
F(![1−p,p],![-w,w])=(p(1−p))⁻¹ w⊗w.
[angular_bernoulli_tensor](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:194) usa explicitamente os valores
![cos²θ,sin²θ] e diferenciais ![−2sinθcosθ·w,2sinθcosθ·w],
obtendo F=4w⊗w quando sinθ e cosθ são não nulos.
[angular_bernoulli_directional](C:/IALD/Central de Patentes/Chatgpt/FISHER_TENSOR_20260909_120757_505197/FisherInformationTensor.lean:218) fornece F(v,v)=4(w(v))².
O controle é uma identidade de dados diferenciais no ponto: não contém um teorema separado
de derivação de um campo angular θ(x). Se w=dθ, os dados exibidos são precisamente os
diferenciais de cos²θ e sin²θ. Os endpoints com probabilidade zero não entram na identidade.

## Alcance e não duplicação

A consulta às declarações canônicas encontrou diagonalFisher, Fisher radial/temporal infinito e
PauliMeasurementFisher 2×2 de parâmetros. Não localizou um campo 4D geral com o contrato desta entrega.
Foram reutilizados outer_tensor_symmetric, outer_tensor_quad, potentialCovector,
coordinatePartial_smooth, scalarAlong_eq_fderiv e geometric_microscopic_compatibility.

O setor permanece finito e diagonal; não é uma construção de entropia quântica não comutativa geral.
Dados estritamente positivos não podem ser substituídos diretamente pelos pesos de um projetor puro.
Uma matriz de parâmetros Bernoulli do codec angular não é automaticamente um vetor normalizado:
a integração com DiagonalStateCurve precisa de uma realização normalizada explícita.

OpticalHeatClausius prova defeito quártico positivo na família óptica sob hipóteses positivas;
por isso os matchings e Clausius aqui são de segunda ordem, não igualdade finita exata.
Sua hipótese óptica η(a+c)=2π·mass já representa o balanço específico daquela família e não foi usada
como premissa oculta para a conclusão geral acima.

## Custódia e verificação

Nenhum original ou um.py foi alterado, executado ou importado.
Apenas esta pasta nova recebeu fontes, backups imediatos de bytes, scripts e builds.
Os dois primeiros builds falharam visivelmente em inferência de continuidade e avisos de estilo;
seus logs e resultados foram preservados. O terceiro build passou.
Dependências canônicas diretamente importadas, suas fontes/binários e a ferramenta foram medidos
antes/depois pelo builder; permaneceram inalterados. Dependências transitivas precompiladas
não foram todas reexecutadas nem todas individualmente medidas.
Revisão independente foi solicitada; o seu resultado não é presumido neste documento.

## Fontes relacionadas

- [PauliMeasurementFisher.lean](C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/PauliMeasurementFisher.lean:38).
- [DiagonalRelativeEntropy.lean](C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/DiagonalRelativeEntropy.lean:30).
- [InfiniteFisherGeometry.lean](C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/InfiniteFisherGeometry.lean:41).
- [ScalarStressConservation.lean](C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/ScalarStressConservation.lean:126).
- [MicroscopicClausiusBridge.lean](C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/MicroscopicClausiusBridge.lean:85).
- [UnitaryClausiusBridge.lean](C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/UnitaryClausiusBridge.lean:96).
- [ScreenClausiusCoefficient.lean](C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/ScreenClausiusCoefficient.lean:104).
- [OpticalHeatClausius.lean](C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt/OpticalHeatClausius.lean:92).
