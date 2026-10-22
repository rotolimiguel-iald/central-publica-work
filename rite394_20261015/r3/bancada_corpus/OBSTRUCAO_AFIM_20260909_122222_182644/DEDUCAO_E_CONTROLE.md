# Controle adversarial da amostragem espacial afim

[REAL — compilado] AffineSamplingObstruction.lean foi congelado no build BUILD_20260909_122513_427198.
A fonte nova tem 11 teoremas e 2 definições. O build conjunto recompilou também a cópia
byte a byte intacta de FisherInformationTensor: total 33 teoremas, 7 definições,
40 linhas auditadas e três processos Lean com exit 0.
Zero warnings ou saída residual. Axiomas somente propext, Classical.choice e Quot.sound.
Hash SHA-256 lido da fonte nova: d4fb9d35f05cf9033877b07ce203106ccd6d71f8f076619fa6952102db81de8f.

## Problema precisamente testado

[INPUT — proposta sob teste] O MESMO campo de probabilidades P(x) é amostrado por
X_(x,v)(t)=P(x+t•v), e o matching de entropia–área de segunda ordem é exigido em TODO
ponto x de U e em TODA direção não nula v que seja nula para g(x).

A probabilidade de referência é estritamente positiva em U; P é suave em U e normalizada
globalmente, como exige probabilityFieldCurve/DiagonalStateCurve.
A região U é aberta, g é lorentziana ponto a ponto, g e Γ são suaves e Γ é sem torção.
Cada tela é EquilibriumScreenData: sua expansão inicial é zero, sua área inicial é um
e o foco quadrático é dado por Ricci. Nenhuma condição de Einstein está nesse contrato.

O objetivo deste controle é testar a suficiência e a compatibilidade dessa proposta
de correspondência. Ele não afirma uma lei TGL nem uma refutação da TGL.

## Cadeia provada

1. [linear_map_zero_of_eta_null](C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_AFIM_20260909_122222_182644/AffineSamplingObstruction.lean:12) e [linear_map_zero_of_lorentz_null](C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_AFIM_20260909_122222_182644/AffineSamplingObstruction.lean:41):
um covetor linear que se anula no cone nulo lorentziano é zero.
A prova usa geradores nulos e uma congruência apenas no ponto; não pede tetrada suave.
A variação de g e de seu cone de ponto a ponto não invalida esse passo.

2. [affine_area_matching_entropy_quadratic_limit](C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_AFIM_20260909_122222_182644/AffineSamplingObstruction.lean:91):
o matching de área força
(S(P(x+t v))−S(P(x)))/t² → eta·(−Ricci_Γ(v,v)/2), pelo lado t<0.
O coeficiente é finito. [quadratic_limit_forces_zero_derivative](C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_AFIM_20260909_122222_182644/AffineSamplingObstruction.lean:61) então força
a derivada de S(P(x+t v)) em t=0 a ser zero.
[affine_area_matching_entropy_derivative_zero](C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_AFIM_20260909_122222_182644/AffineSamplingObstruction.lean:118) identifica essa derivada com dS_x(v).

3. [UniversalAffineAreaMatching](C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_AFIM_20260909_122222_182644/AffineSamplingObstruction.lean:141) explicita a quantificação universal em x e v.
[universal_affine_area_matching_entropy_fderiv_zero](C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_AFIM_20260909_122222_182644/AffineSamplingObstruction.lean:152) prova dS_x=0 em U.
[universal_affine_area_matching_entropy_constant](C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_AFIM_20260909_122222_182644/AffineSamplingObstruction.lean:174) prova S(P) constante quando
U também é preconexa. Não há requisito de calor, de conservação de T ou de energia positiva
nessa conclusão.

4. Para eta≠0, [constant_entropy_affine_area_matching_ricci_null_zero](C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_AFIM_20260909_122222_182644/AffineSamplingObstruction.lean:191) e
[universal_affine_area_matching_ricci_null_zero](C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_AFIM_20260909_122222_182644/AffineSamplingObstruction.lean:219) demonstram
Ricci_Γ(v,v)=0 em todas as direções nulas.
A reta x+t v não precisa permanecer nula: ela serve para amostrar o campo de estados.
A existência local dentro de U decorre da abertura, e sua tangente inicial é v.

5. O controle algébrico [zero_ricci_nonnegative_matter_forces_zero_variation](C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_AFIM_20260909_122222_182644/AffineSamplingObstruction.lean:241)
mostra que Ricci(v,v)=0, o balanço eta Ricci(v,v)=2π matter+F(v,v),
matter≥0 e P_i>0 obrigam matter=0 e dp(v)=0.
Não se supõe nem se conclui conservação do tensor de Fisher.
[DERIVED — composição ainda não embalada em um único teorema aqui] Com o matching de calor
do FisherInformationTensor em todas as direções nulas e T(v,v)≥0, essa conclusão se aplica
a dp_i=dP_i; o lema do cone fornece então dP_i=0.
A constância de P e a constância de uma métrica decodificada da MESMA P requerem essa
composição e o respectivo contrato do codec; não são conclusões declaradas do lema de Ricci sozinho.

## Limites que o resultado preserva

- Ricci(v,v)=0 nos nulos não significa Riemann=0 e não significa espaço plano.
A entrega não contém nem utiliza a implicação incorreta Ricci-flat ⇒ flat.
- Sem matéria nulo-positiva, o termo de Fisher pode ser compensado por T(v,v)<0;
o último controle exige explicitamente matter≥0.
- Um matching direcional em um único ponto não implica que S(P) seja constante na região.
A obstrução exige a mesma P com o contrato universal indicado.
- Os parâmetros podem continuar sendo codificados e recuperados: o controle restringe
a correspondência termodinâmica universal proposta para esses parâmetros.
- O termo de Fisher positivo é informação, não a assinatura lorentziana da métrica.

## Dois tipos de variação

[REAL — leitura de tipos] A resposta de preparação usada em UnitaryClausiusBridge fornece
uma curva X_(x,v)(t) para cada tela; ela não identifica seus pesos com P(x+t v) para
um único campo de entropia espacial.
Uma resposta local pode ter primeira derivada nula e resposta quadrática não nula
sem impor dS(P)_x=0 como derivada espacial.

[INPUT / OPEN] Uma lei que ligue a preparação local, os dados selecionados, o parâmetro
microscópico e a geometria continua a precisar de especificação independente.
Distinguir os dois tipos evita aplicar a obstrução a uma hipótese que o modelo não fez;
também evita apresentar a amostragem afim como lei validada apenas porque seu tipo compila.

## Custódia

Nenhum original ou um.py foi alterado, executado ou importado.
FisherInformationTensor congelado não foi alterado: a nova pasta recebeu uma cópia integral
de seus bytes e os comparou novamente depois da compilação.
O primeiro build falhou no uso do extensor de LinearMap; logs e recibo foram preservados.
A correção foi precedida de backup imediato de bytes na mesma pasta.
O segundo build passou. A fronteira de imports diretos permaneceu igual antes/depois;
dependências transitivas pré-compiladas não foram todas reexecutadas nem individualmente medidas.
Revisão semântica independente foi solicitada; seu resultado será registrado separadamente.
