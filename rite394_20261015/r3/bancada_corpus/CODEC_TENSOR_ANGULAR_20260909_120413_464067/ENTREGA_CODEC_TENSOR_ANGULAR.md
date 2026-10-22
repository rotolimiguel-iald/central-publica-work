# Entrega — codec angular geral de tensores

[REAL — compilado em escopo isolado] GeneralAngularTensorCodec.lean está congelado. O módulo novo e o importador ImportsRealization compilaram com saída 0 e sem avisos. Há 32 teoremas e 12 definições/estruturas; todas as 44 declarações foram auditadas e usam apenas propext, Classical.choice e Quot.sound. A fronteira direta de dependências permaneceu inalterada.

Fonte: C:/IALD/Central de Patentes/Chatgpt/CODEC_TENSOR_ANGULAR_20260909_120413_464067/GeneralAngularTensorCodec.lean
SHA-256 medido: 1b85b13d2bd4edef11016dabb975a73526828232d59b4f7c812dacb886d3f4c4
Bytes medidos: 12520
Recibo: C:/IALD/Central de Patentes/Chatgpt/CODEC_TENSOR_ANGULAR_20260909_120413_464067/BUILD_20260909_120629_281814/BUILD_RESULT.json

## Resultado e API

Namespace: ChatgptAudit.AngularTensorCodec.

Para qualquer real x:
θ(x)=(arctan x+π/2)/2; encodeScalar(x)=sin²θ(x);
decodeScalar(p)=tan(2·TGLExt.selectionAngle(p)−π/2).

A codificação leva todos os reais ao intervalo aberto (0,1). A seleção canônica recupera exatamente θ. As duas composições são identidades, a primeira para todo x real e a segunda para 0<p<1. A codificação é suave em ℝ; a decodificação é suave em (0,1).

encodeMatrix/decodeMatrix funcionam para índices arbitrários m,n, sem restringir as entradas a uma família física. A simetria da matriz é preservada e refletida pela codificação. encodeTensorField/decodeTensorField aplicam o codec em cada ponto e componente do TensorField4 canônico. A ida e volta é igualdade de campos; a volta de probabilidades é igualdade em U, onde a interioridade foi certificada.

ProbabilityFieldRecord U armazena:
- probabilities : TensorField4;
- interior : cada componente pertence a (0,1) em U;
- smooth : SmoothMatrixOn U probabilities.

decodeRecord R é o campo tensorial construído dessas probabilidades; decoded_record_smooth R demonstra sua suavidade. Nenhuma métrica adicional é armazenada.

LorentzProbabilityRecord U contém esse registro e lorentz, certificado explícito de LorentzByCongruence para decodeRecord data em U. O teorema lorentz_record_decodes_smooth_metric entrega as duas hipóteses geométricas que a dinâmica métrica geral exige. every_smooth_lorentz_field_is_representable demonstra que todo campo suave lorentziano da carta admite um registro com decodificação exatamente igual ao campo original.

## Alcance exato

[DERIVED] Completude da representação para campos reais de duas entradas tensoriais na carta: não se restringe a ondas planas ou a uma classe especial de métricas. A extensão matricial cobre tamanhos arbitrários. Não se construiu uma transformação tensorial do registro entre cartas.

[INPUT] As componentes são probabilidades Bernoulli separadas: em quatro dimensões, até 16 probabilidades por ponto, cada uma com complemento 1−p. A matriz de probabilidades inteira NÃO é apresentada como uma única distribuição normalizada nem como uma matriz de densidade. Não se afirma que um único resultado binário contenha todas essas probabilidades reais exatas.

[INPUT] Interioridade, suavidade e assinatura são certificados transparentes. Probabilidades interiores arbitrárias decodificam um campo real suave quando são suaves; não necessariamente um campo simétrico ou lorentziano. A assinatura pertence ao tensor decodificado, não ao Fisher positivo.

[OPEN] Codificar g já dado não demonstra que a natureza produz p(g), que p(g) é extraído de um estado/cociclo comum, nem que um resultado selecionado fornece a lei de probabilidades inteira. O módulo demonstra capacidade e unicidade informacional de uma representação escolhida. A lei física de produção, compatibilidade do registro completo e vínculo com dinâmica continuam separados.

[OPEN] A regularidade é local em probabilidades estritamente interiores. Não há separação uniforme dos extremos exigida, nem estimativa uniforme de erro para decodificação. p=0 e p=1 estão fora da parte invertível do codec de reais finitos.

[OPEN] Equações dinâmicas, energia-momento, conservação, telas físicas, consistência global e torção não são resultados deste módulo. A composição com o teorema métrico geral deve preservar essas hipóteses visíveis. O módulo não move o gate nem declara QG resolvida.

## Verificação e preservação

A primeira build falhou visivelmente no uso de fun_prop para arco-tangente e no fechamento da seção. Os logs e recibo falhos foram preservados. A revisão local foi precedida de backup byte a byte; substituiu-se a automação pelo lema explícito Real.contDiff_arctan e fechou-se a seção. A build final acima passou. O arquivo de backup permanece na mesma pasta.

O builder, copiado em bytes de uma entrega anterior, criou uma pasta BUILD nova e compilou apenas este módulo e seu importador. As dependências canônicas foram utilizadas somente para leitura e tiveram suas fontes/binários DIRETAMENTE importados medidos antes e depois. Não foram recompiladas todas as dependências transitivas nem calculados hashes de todas elas. Nenhum um.py foi importado/executado e nenhum original ou Atlas foi alterado.

[INPUT] Revisão independente de escopo solicitada à sessão principal; este recibo não marca aprovação independente já concluída.
