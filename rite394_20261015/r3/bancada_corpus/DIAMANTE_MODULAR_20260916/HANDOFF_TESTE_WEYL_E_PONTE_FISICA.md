# Handoff — teste físico da ação geométrica após a ponte dephasing–torre

16/09/2026. Destino: sessão responsável pelo um.py. Complementa a [V2](HANDOFF_TECNICO_V2.md) e a [realização modular regional](HANDOFF_PONTE_REGIONAL_EINSTEIN_SIGMA.md). Este documento é uma entrega de provas e critérios para os leitores existentes; não altera o motor canônico.

## Resultado e escopo

**A identificação vácuo–dephasing já recebeu uma ponte construtiva na torre.** O [recibo v358](../TUNEL/PARA_CHATGPT/RECIBO_DIAMANTE_MODULAR_v358.md) deve ser lido antes de voltar a pedir essa prova. A distinção entre a leitura espectral completa e a leitura parcial de último sítio permanece essencial. A primeira preserva todo K e é estacionária na imagem; a segunda admite uma igualdade não trivial dos fluxos na família produto especificada. Não reabrir PRODUCT_TOWER/JMJ.

O novo trabalho usa a ação e o estado linear Einstein–sigma já disponíveis. A realização modular regional foi construída na entrega anterior. Agora testamos uma proposta concreta para a ação geométrica: o pullback tensorial ordinário do Weyl linear C(1,3), sem peso adicional. **Essa proposta falha no estado 067**, para os diamantes e hipóteses da [demonstração](TESTE_GEOMETRICO_WEYL_ESTADO_067.md).

Estatuto: [DERIVED — prova escrita condicional, não Lean]. A revisão independente e seus limites são registrados em arquivo próprio no manifesto desta entrega. Não converter o teste em exclusão de toda ação geométrica modificada, nem em conclusão sobre a teoria interagente UV completa.

## A cadeia que foi realmente testada

1. O Weyl linear é um observável local de gauge no fundo conformemente plano.
2. Os modos TT existentes dão uma leitura harmônica b_n com correlação exata:

\[
\omega(b_n(\eta)b_n(\eta'))
=\frac{\hbar\kappa(p_n^2+1)}{2p_n}
\cosh\eta\cosh\eta' e^{-ip_n(\eta-\eta')},
\qquad p_n^2=(n+1)^2+6.
\]

3. A modularidade da ação proposta exigiria invariância dessa referência. A estimativa analítica da entrega anterior permite estender uma eventual identidade de Ward local para todo o interior do espaço-tempo.
4. SO(4) e a soma dos vetores conformes de centros antipodais, ξ_n+ξ_−n=−2 cot(L)∂η, obrigariam estacionariedade em tempo conforme para L≠π/2.
5. A correlação calculada a contradiz: d log ω(b_n²)/dη=2 tanh η≠0.

O smearing harmônico é global e só é usado depois do passo de continuação analítica. Não foi declarado observável de suporte no diamante. O raio excepcional π/2 está explicitamente fora desta prova.

**Controle da interpretação:** a leitura reescalada a b_n tem correlação estacionária. Isso demonstra por que a hipótese de transformação não pode ficar implícita. Um peso adicional pode remover esta obstrução específica; ainda seria necessário provar preservação das equações, covariância conforme inteira, condição KMS e identificação modular. Escolher um peso apenas para obter estacionariedade não cumpre essas obrigações.

## O que significa para R e para o dephasing

Se Kξ implementar exatamente a ação testada na mesma realização, Kω−Kξ não pode ser somente uma constante na álgebra inteira. A prova não localiza o observável que detecta a diferença dentro do centralizador.

O dephasing espectral de Kω preserva o estado e o próprio gerador. Ele não corrige uma transformação externa que não preserve a covariância desse estado. Portanto, o lugar em que a ponte precisa ser verificada é a ação geométrica nos mesmos observáveis físicos, não outra definição de pinching.

Para a esperança centralizante existe ainda o [critério espectral](CENTRALIZADOR_FOCK_E_ESPECTRO.md): se log δD não tem espectro pontual, então o centralizador Fock é ℂI. Nesse caso a ação de qualquer resto no centralizador é trivial automaticamente; esse resultado não atestaria geometricidade fora dele. **A hipótese espectral não foi estabelecida para a 067.** Não a preencher com a mera existência de δD.

## Integração solicitada à gerência

- Preservar os leitores existentes `prove_cocycle_to_einstein` e `prove_decision_commutation`; usar os modos de leitura já aceitos. Não acrescentar outra torre, outro cociclo ou uma série de funções de fechamento.
- Vincular esta prova como evidência DERIVED, incluindo estado 067, observável C(1,3), ação sem peso, restrição de raio e revisão. Ela não tem certificado Lean e não deve acender uma bandeira KERNEL.
- Se o fornecedor geométrico do motor pretender a ação pura testada, registrar incompatibilidade nesse escopo. Se adotar outra ação, apontar o termo que a define e suas hipóteses; este no-go não decide o novo caso por homonímia.
- Manter o contrato físico que já existe no handoff anterior: k T_t f=δD^(it) kf. A preservação da covariância é uma condição necessária prévia, não um substituto desse contrato.
- Não usar 2 tanh η como R1, taxa de Lindblad, coeficiente universal ou medida experimental. É uma derivada logarítmica de uma correlação especificada.
- Incorporar a correção de contexto no Atlas, índice vivo, diário e desenho pela gerência, com backups imediatos: ação e estado LINEAR existem; geometricidade simples foi agora testada; estado físico interagente e controle UV continuam distintos. Esta bancada só atualiza suas memórias locais e a proposta para o Atlas.

## Verificação e limites

[REAL — execução] `verify_weyl_ward.py` passou em nove combinações modo/tempo e quatro raios: diferença finita com convergência quadrática, correlação em tempos desiguais, rejeição da estacionariedade sem peso, preservação da estacionariedade após reescala e exclusão do raio excepcional. Esses testes conferem identidades; não substituem suporte, analiticidade ou prova de gauge. Resultado: [WEYL_WARD_CHECKS.json](WEYL_WARD_CHECKS.json).

O [manifesto](WEYL_BRIDGE_MANIFEST.json) registra os bytes das fontes, evidências e memórias desta rodada. Os manifests anteriores são retratos históricos: as memórias que recebem append passam a ter novos hashes, com a versão anterior preservada no backup imediato. Sem mudança no um.py original ou no gate.

**O próximo cálculo tem endereço preciso:** obter da mesma ação física a transformação de observáveis gerada pela carga renormalizada Kξ, incluindo eventual peso/mistura e termos de fronteira, e confrontá-la com δD. A ponte algébrica dephasing–torre não precisa ser refeita para isso.
