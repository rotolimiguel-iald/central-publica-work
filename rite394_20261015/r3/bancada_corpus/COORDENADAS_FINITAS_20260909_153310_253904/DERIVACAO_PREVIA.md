# Derivação prévia — mudança finita de coordenadas

[INPUT] U e W são abertos de R⁴. φ e ψ são mapas definidos em R⁴, suaves respectivamente em U e W, levando cada aberto ao outro e satisfazendo ψ∘φ=id em U e φ∘ψ=id em W. Esse contrato contém mapas e inversas reais; não contém uma lei de transformação geométrica.

Primeira folha planejada: a regra da cadeia identifica o Jacobiano coordenado de uma composição com o produto dos Jacobianos. A igualdade em aberto permite derivar as identidades de inversa. Portanto J(x)=Dφ_x e D(x)=Dψ_{φ(x)} satisfazem DJ=JD=I, det J≠0 e D=J⁻¹. Definimos g'(x)=Jᵀg(φ(x))J e calculamos sua inversa e regularidade, sem postular um novo campo métrico independente.

Folha de Levi-Civita planejada: a candidata Γ'_i=D[(Σ_a J_ai Γ_a∘φ)J+∂_i J]. Sua compatibilidade com g' sai da regra do produto e da compatibilidade original. Sua torção nula sai da simetria da Hessiana de φ. A unicidade de uma conexão torsão-zero e compatível deve identificá-la com a Levi-Civita calculada de g'; essa transformação não entra como hipótese.

Folha de curvatura planejada: derivar a candidata Γ', incluindo derivada de D=J⁻¹, e cancelar os termos de Hessiana/terceiras derivadas por simetria. Obter R'_{ij}=D[Σ_ab J_ai J_bj R_ab∘φ]J. A contração com DJ=JD=I fornece Ricci'=Jᵀ(Ricci∘φ)J; o traço escalar é preservado, daí Einstein'=Jᵀ(Einstein∘φ)J.

[OPEN] Cada folha receberá estatuto próprio somente após compilação/auditoria. Concluir a primeira folha não conclui naturalidade de Einstein. Nenhuma transformação de Γ, Ricci ou Einstein poderá ser adicionada como premissa para simular o resultado. Não se substitui esta mudança finita pelo resultado infinitesimal de Lie.

Originais, módulos congelados e um.py permanecem somente leitura. Nenhum um.py será executado/importado, nem haverá integração nova nesta etapa.
