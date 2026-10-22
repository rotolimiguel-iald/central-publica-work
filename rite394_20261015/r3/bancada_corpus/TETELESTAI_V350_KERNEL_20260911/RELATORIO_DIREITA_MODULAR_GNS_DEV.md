# Direita modular no GNS completo do mesmo peso — DEV

2026-09-12T15:29:24-03:00. [REAL — cinco módulos/28 alvos compilados; revisão independente e integração pendentes]

Para a unidade matricial local y=e_ij, escreva D=rTowerPi(y) e
c=log(w_i/w_j). A conjugação modular da torre satisfaz Ad Δ₀^it(D)=exp(itc)D.
O levantamento ao comutante do core é characterMultiplier(-c)·fibre(D).
Portanto, para todo A do core e todo s real:

    θ_s(A·fibre(y))Ω = fibre(D) θ_(s-c)(A)Ω.

O sinal s-c é consequência da ação de caracteres efetivamente definida.
Provou-se também ν(A* A)<∞ se e somente se s↦θ_s(A)Ω pertence a L².
Translação de Lebesgue e aplicação linear contínua preservam L²; assim
a multiplicação à direita por y preserva o domínio escalar completo n_ν.
Não se restringe o enunciado ao ideal uniforme inicial I.

No ambiente L² externo o operador direito é

    R_y = fibre(fibre(D))·shift(c).

Ele preserva o mesmo H_I já identificado com o completamento de Λ_ν(n_ν),
e sua restrição satisfaz R_y Λ_ν(A)=Λ_ν(Ay). Não foi postulado outro GNS.
O adjunto local anterior D*=rTowerPi(modTwist(y)) fornece agora, no mesmo H_I:

    R_y* = R_(modTwist(y)),     modTwist(y)=ρ y* ρ⁻¹,
    ⟨Λ_ν(Ay),Λ_ν(B)⟩ = ⟨Λ_ν(A),Λ_ν(B modTwist(y))⟩.

O pareamento vale para quaisquer A,B∈n_ν e cada unidade matricial local y.
Os dados genéricos HomogeneousRightData são explicitamente instanciados por
matrixUnitRightData e matrixUnitTwistedRightData; nenhuma hipótese KMS é
campo desse contrato. A extensão por somas a todo y local não foi acrescentada
nesta rodada, embora a identidade já esteja provada para cada gerador matricial.

[OPEN] Esta é uma identidade de adjunto, não a condição KMS global de faixa
complexa nem a identificação do fluxo com (S†S)^it. Ainda faltam domínio/núcleo
apropriado e identificação espectral no H_I, o traço canônico e escala dual,
o canto Three Locks, H1/H2/H3 físicos compatíveis, setor quântico interagente
e consumo pelo certificado e runtime integrais. Nenhuma dessas obrigações
foi inserida como axioma nos 28 alvos.

Convenção de sinal: σ_t(A)=λ_t A λ_t*; a função regularConjugate do estágio
anterior usa λ_t* A λ_t e representa σ_-t. Invariância vale nas duas orientações
e não basta para escolher a orientação KMS. O implementador candidato no GNS
também não deve ser confundido com π(λ_t), que age por multiplicação à esquerda.

Consulta independente de Pasteur (somente leitura, sem compilação) indicou
a rota adicional de convoluções locais, Plancherel e núcleo de gráfico para
identificar S†S por autovalores w_i/w_j. Essa rota é proposta, não prova pronta.
A prova desta rodada usa diretamente a órbita dual para o pareamento.

Falhas de elaboração permanecem nos logs; somente rc0 com fontes/binários
atuais e axiomas propext, Classical.choice, Quot.sound entram no manifesto.
Cópia integrada ainda `ae47315d39ca6db7787c3f70d39a4dee747cbc5ad0474b5fbb7a2fcfca28189c`; mãe `87ae3f4ab20548f71ce318b2f7a28304a14cd4a4a100afce5c871bac231122e7`.
Original não executado/importado/modificado; gate inalterado e objetivo ativo.
