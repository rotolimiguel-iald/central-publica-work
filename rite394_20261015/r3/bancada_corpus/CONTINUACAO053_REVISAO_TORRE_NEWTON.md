# Revisão matemática independente053 — polarizador e torre

[REAL — revisão de fontes e evidências de desenvolvimento; não é aprovação do build final conjunto]

Revisor: Newton (/root/relative_operator_domains). Autoria dos módulos revisados: SymplecticPolarizer por Beauvoir; TowerStatePolarizer pela raiz, com trecho de derivada em coautoria de Beauvoir, conforme coordenação da equipe. O revisor não é autor desses dois módulos. HorizonGNSImplementation, de autoria do revisor, é uma dependência e NÃO recebe aprovação matemática independente nesta nota.

## Fontes e evidências medidas

| Fonte | Bytes | SHA256 | T | D | Prints |
|---|---:|---|---:|---:|---:|
| SymplecticPolarizer.lean | 9193 | ef5c76b0d4451fa4a615b85c0c8567e503e052b9f91187e4fb58ffb5fa929eff | 19 | 3 | 22 |
| TowerStatePolarizer.lean | 15156 | 53631dbd465b60fe0d9b8a713a94b44e85a898492d191add1e254cf8542a9b9a | 20 | 4 | 24 |

- SymplecticPolarizer: [02_SymplecticPolarizer.json](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_DEVELOPMENT_20260907_052653_964997/02_SymplecticPolarizer.json>); log [02_SymplecticPolarizer.log](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_DEVELOPMENT_20260907_052653_964997/02_SymplecticPolarizer.log>), SHA256 b9c109e7fb713851d9cfea7b95f254b81dcb1fed4121ae1c706162e27a309140.
- TowerStatePolarizer: [03_TowerStatePolarizer.json](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_DEVELOPMENT_20260907_052653_964997/03_TowerStatePolarizer.json>); log [03_TowerStatePolarizer.log](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_DEVELOPMENT_20260907_052653_964997/03_TowerStatePolarizer.log>), SHA256 bbd6b62f612c8931ee2aa249c540dbadd06bdfe46740b94598bfb8ac9765f75c.

Os fontes atuais coincidem byte a byte com as cópias das compilações individuais indicadas. Foram conferidos os hashes dos logs e oleans ligados aos metadados, exit 0, flags de estabilidade, ausência de issues, cobertura dos prints e uso exclusivo de propext, Classical.choice e Quot.sound. Não foi iniciada compilação nem executado auditor integral nesta revisão. Os diretórios citados são de desenvolvimento; esta nota não os promove a evidência final conjunta.

## Revisão de SymplecticPolarizer

A definição é literalmente a composição real D=P_R∘(−i)∘P_R. R é um submódulo REAL completo; a projeção ortogonal é a da Mathlib, não um operador cuja propriedade foi postulada no arquivo. A instância real usada pelo escopo ClosedSubmodule conserva o produto real como Re do produto complexo.

A fórmula ambiental comprime as duas entradas: ⟨x,Dy⟩_ℝ=Im⟨P_Rx,P_Ry⟩. Somente para x,y∈R é removida essa compressão. O sinal negativo em −i está correto para a convenção do produto complexo, linear na segunda entrada: Re(−i⟨x,y⟩)=Im⟨x,y⟩. A antissimetria e a cota ‖D‖≤1 seguem da conjugação do pareamento e da contração das duas projeções.

A unicidade pelo pareamento exige explicitamente os vetores no subespaço e testa a diferença contra ela mesma. A equivalência do núcleo também mantém y∈R. Não se afirma que a parte imaginária seja positiva ou que o Hilbert real inteiro tenha radical classificado pelo centralizador.

polarizerFormBilin é REAL bilinear. Para ε≥0, sua diagonal é ‖Dx‖²+ε‖D²x‖²; os dois termos são não negativos. O primeiro termo já força Dx=0 quando a diagonal zera, inclusive em ε=0. Para ε negativo não se afirma essa equivalência nem positividade.

A covariância usa um W complexo-unitário bijetivo e a equivalência x∈R↔Wx∈R. O uso da inversa garante que W leva R sobre R; apenas inclusão de W(R) em R seria insuficiente. A prova identifica a projeção transportada pela ortogonalidade, depois usa linearidade complexa para passar a multiplicação por −i e entrelaçar D. Essa hipótese é paga pelo implementador da torre no módulo seguinte.

## Revisão de TowerStatePolarizer

real_state_pairing_ext usa o funcional real contínuo definido por u−v. Os testes AΩ autoadjuntos do fator anulam seu núcleo linear; a inclusão estende-se do span ao fecho por fechamento do núcleo. Testar u−v conclui u=v. Não há suposição oculta de que os vetores locais ou os vetores AΩ isolados já sejam todo R.

statePolarizer apenas especializa o polarizador genérico ao único realStateSubspace da torre. A ligação Re⟨AΩ,D(BΩ)⟩=Imω(A*B) é demonstrada com os dois geradores autoadjuntos em M.

A direção não trivial da caracterização do centralizador é paga com DOIS testes autoadjuntos construídos de um B arbitrário do fator:
- C=B+B*;
- F=i(B−B*).

Ambos pertencem a M. A identidade ω(B*A)=conj(ω(AB)), usando A=A*, transforma a nulidade da parte imaginária de ω(CA) na igualdade das partes imaginárias de ω(BA) e ω(AB). O teste F fornece a igualdade das partes reais. Portanto os testes recuperam a condição COMPLEXA inteira para todo B∈M, sem assumir que B seja autoadjunto no resultado final.

A equivalência D(AΩ)=0↔A∈M^ω exige A∈M e A autoadjunto. Ela é combinada com a diagonal positiva para identificar o radical de hε nesse setor e provar positividade estrita fora do centralizador. Nenhuma dessas equivalências é estendida automaticamente a todo B(H) ou a todos os vetores de R.

A aplicação stateCovariantBilinear existe no ambiente dos operadores limitados como forma REAL bilinear. A covariância por cada h:TowerHorizon P usa a fórmula global W_h(AΩ)=adT(h)(A)Ω e a invariância real em ambas as direções; não usa h.UΩ=Ω. O lema mais forte exige apenas A,B∈M, e o wrapper autoadjunto é uma especialização coerente.

A descida é demonstrada por igualdades de valores após adição de C autoadjunto centralizante em cada entrada. Como D(CΩ)=0, os termos com C desaparecem por linearidade. [DERIVED] Isso permite uma forma positiva definida no quociente algébrico do setor autoadjunto pelas direções centralizantes. O arquivo não constrói uma variedade, um espaço tangente global diferenciado ou uma métrica lorentziana.

## Derivada e núcleo das respostas

Foi lida também a API de UnitaryStateDerivative na cópia limpa035 para conferir a convenção. unitaryConjugation é U_A(t)* B U_A(t), e a derivada da expectativa já provada é iω(BA−AB). Para A,B autoadjuntos, ω(AB)=conj(ω(BA)), logo:

    Re[iω(BA−AB)] = −2 Imω(BA).

state_reading_real_hasDerivAt compõe a derivada complexa real-parametrizada com Re, por aplicação contínua real linear; a fórmula não é usada como definição da resposta. realStateResponse é definida pela derivada da curva efetiva. Em seguida, state_response_kernel testa todos os B autoadjuntos em M e recupera exatamente a caracterização do centralizador. O kernel de hε e o kernel de todas essas respostas coincidem no setor A∈M autoadjunto, com ε≥0.

Não se presume uma identificação do parâmetro dessa curva unitária com tempo modular, tempo afim ou relógio físico.

## Conclusão e limites

Não foi identificada falha matemática nos enunciados ou argumentos examinados. Os quantificadores, os sinais, o uso da completude real, a condição ε≥0 e o alcance autoadjunto da classificação do radical estão explícitos e coerentes.

Esta revisão não demonstra seleção de área física, escolha de região/horizonte, compatibilidade geral de inclusões ou H3. Não reaudita o fecho externo da Mathlib nem substitui a futura auditoria do lote final053. Nenhuma fonte, derivação, infraestrutura, memória ou arquivo selado foi alterado; a única escrita é a criação exclusiva desta nota.

Emissão UTC: 2026-09-07T05:29:50.117322+00:00
