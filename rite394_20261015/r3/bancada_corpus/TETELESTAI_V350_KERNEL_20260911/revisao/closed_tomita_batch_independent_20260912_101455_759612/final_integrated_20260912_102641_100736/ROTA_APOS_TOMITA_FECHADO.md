# Próxima obrigação: ligar o operador fechado ao peso e ao traço

[DERIVED — roteiro de implementação; nenhuma prova nova é declarada aqui]

Os objetos a preservar são N=regularCoreAlgebra P, ν=scalarDualWeight P,
I=finiteDualLeftIdeal P, H_I=ScalarGNSHilbert P e o S construído do
fecho de {(Λ(A),Λ(A*)) : A∈I∩I*}. A nova fechabilidade não autoriza
substituir S pelo operador da torre ou de um outro estado.

1. Empacotar um adjunto antilinear máximo do S efetivo. Sua convenção,
   com produto interno complexo linear na segunda entrada, é
   ⟨Sx,y⟩ = ⟨S†y,x⟩. O domínio deve conter exatamente os y para os
   quais existe o vetor representativo desse pareamento, com unicidade
   deduzida da densidade de D(S). Uma identidade em um subdomínio
   arbitrário não demonstra maximalidade do adjunto.
2. Construir Δ=S†S com domínio da composição explícito. Positividade
   e simetria não substituem auto-adjunticidade. A identidade de formas
   ⟨x,Δx⟩=‖Sx‖² requer que x e Sx pertençam aos domínios corretos.
   O cálculo funcional/raiz e a decomposição polar precisam ser
   ligados a esse operador, e não apenas receber o nome Δ.
3. Identificar a ação modular do peso. ScalarModularInvariance já
   prova invariância de ν pela conjugação regular candidata. Seu
   comentário delimita expressamente que isso não é identificação
   KMS. O certificado ampliado deve demonstrar KMS ou uma ponte
   formal equivalente com os mesmos ν, representação e domínios.
4. Construir o gerador positivo afiliado h cuja potência imaginária
   realiza o grupo interno correspondente e a perturbação que produz
   τ no cone positivo do mesmo N. Reutilizar a convenção registrada em
   CONVENCOES_DO_TRACO.md. Provar normalidade, fidelidade, semifinitude
   e τ∘θ_s=e^(-s)τ; só então alimentar o certificado de core/Three Locks.

**Não transformar I=n_ν em objetivo obrigatório.** I foi definido por
finitude uniforme da forma em todos os vetores; n_ν pede finitude de
uma avaliação escalar. Os domínios podem ser diferentes. A obrigação
é construir a ponte de densidade/núcleo e a identificação efetivamente
necessária ao teorema utilizado, ou provar KMS diretamente no domínio
adequado. Igualar dois nomes não fornece essa ponte.

[REAL — interfaces locais lidas]

- TGLExt/TomitaAdjoint.lean fornece adjunto máximo e S†S=Δ para
  TowerHilbert P, mas usa explicitamente towerJ e a parte positiva
  closedModulatorCandidate. Não fornece o adjunto para o novo H_I.
- TGLExt/RelativeModularOperator.lean transporta a construção da
  referência thirdThermalReference por filtros limitados invertíveis.
  Essa mudança relativa não identifica o GNS do peso ν aqui.
- Mathlib/Analysis/InnerProductSpace/LinearPMap.lean define adjoint
  para operadores parciais lineares sobre RCLike e prova fechamento
  e maximalidade. Sua definição usa valor padrão fora do caso de
  domínio denso; essa condição deve ser fornecida em cada aplicação.
  O tipo lido não é um adjunto genérico de mapas complexo-antilineares.

[DERIVED — alternativa técnica a investigar] Tratar S primeiro como
operador real-linear no domínio com escala real permitiria reutilizar
o adjunto real. Depois é preciso provar que seu domínio é complexo,
que o valor é antilinear e que a identidade real implica a identidade
complexa acima, usando também ix. Essa rota não está compilada; não
se presume densidade do domínio do adjunto, nem se introduz um J
auxiliar e o chama de conjugação modular física.

O produto de dois operadores antilineares é complexo-linear, mas
esse fato isolado não constrói a decomposição polar nem KMS. O
subespaço padrão Fix(S) não entrega uma escala entrópica ou física.
Gate, H1–H3, setor interagente e execução integral permanecem fora
do alcance desta nota. As provas já revisadas não são modificadas.
