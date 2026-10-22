# Adendo ao handoff v358 — centralizador e primeira obstrução

16/09/2026. Complemento da entrega V2; não a substitui nem pede nova camada do motor.

O operador perguntou se R=K_ω−K_ξ é central na imagem da esperança centralizante e qual o primeiro coeficiente não central, para diamantes finitos em teoria interagente UV completa. A resposta física numérica não está fixada pelos dados gerais: a construção de Q_ξ e da família de estados continua necessária. Não preencher o coeficiente com β por identificação de nomes.

## Reutilização, antes de incorporar

O Atlas declara que as seis pedras V2 foram incorporadas na v358. Usar os termos canônicos `stationary_generator_balance`, `generator_bridge_iff`, `existing_tower_dephasing_is_stationary` e `erased_remainder_counterexample`; não os duplicar. O acesso direto da bancada ao manifesto/kernel canônico não foi possível nesta rodada; a declaração de incorporação não foi elevada a nova verificação canônica.

A nova fonte `CentralizerRemainderPerturbation.lean` acrescenta apenas:

1. Caracterização finita da comutação com TODA a imagem de `specExpect`: matriz diagonal e constante em cada bloco de autovalor igual. Mais forte que comutar com a densidade.
2. Nessa realização matricial completa, o operador que comuta com a imagem pertence a ela, logo ao centro. Não extrapolar essa pertença para representação geral/operador ilimitado.
3. Controle de degenerescência: densidade tracial não torna qualquer operador central.
4. Balanço algébrico do primeiro coeficiente com observável transportado: [R₁,A₀]+[R₀,A₁], e não apenas [R₁,A₀].
5. Transporte exato de comutadores por conjugação.
6. Família finita cuja obstrução tem amplitude c e ordem ε^m arbitrárias; não é um contraexemplo QFT interagente.

O arquivo `AUDIT_CENTRALIZADOR.json` identifica a compilação aceita e os axiomas. As tentativas anteriores ficam preservadas e não integram a evidência positiva. Os 23 controles de `REMAINDER_RESPONSE_CHECKS.json` verificam respostas resolventes/espectrais, diferenças finitas, degenerescências e transporte. Não são dados da natureza.

## Como consumir sem encadear funções redundantes

No consumidor existente de cociclo/resto, manter R=−h_ab. Se vier uma carga candidata Q e uma densidade finita, avaliar os blocos espectrais e a ação em todas as unidades matriciais do setor indicado. A tolerância espectral em dados numéricos deve ser declarada: não converter quase degenerescência em uma hipótese exata do Lean.

Se houver uma família física explicitamente fornecida, a primeira variação é

    R₁=−Dlog(ρ₀)[ρ₁]−Q₁.

A fórmula integral e a segunda ordem estão demonstradas no texto `RESPOSTA_CENTRALIZADOR_COEFICIENTE.md`, mas NÃO formalizadas como integrais em Lean. Marcar DERIVED, não KERNEL. Não acrescentar uma API concorrente de logaritmos/cociclo. O script numérico é uma verificação de bancada, não módulo obrigatório de runtime.

Ao variar o estado, exigir a regra de comparação dos setores; se o centralizador muda de dimensão, não pressupor um isomorfismo. Se a pergunta for sobre o setor centralizante completo, usar a identidade [R,A]=−[Q,A]. Não trocar pelo modo parcial do último sítio apenas porque o último admite um fluxo não trivial.

Nenhuma nova condição ao gate principal. Nenhuma conclusão sobre geometricidade física, valor de G, UV completo, massa inercial ou dissipação é promovida pelos seis termos. A meta ampla de resolver gravidade quântica permanece OPEN, sem redução a um sucesso da bancada finita.

## Memória canônica — proposta para a gerência

[DERIVED/REAL] A centralização do vácuo implica [R,A]=−[K_ξ,A]; não fornece comutação de K_ξ com o setor. Em matrizes, a condição exata é K_ξ escalar por bloco espectral. Na comparação de estados, o primeiro coeficiente observável inclui [R₀,A₁]. Uma variação unitária conjunta pode tornar [R₁,A₀] não nulo mantendo a obstrução total zero. A regra de Fréchet do logaritmo é universal; seus dados não são. [OPEN] identificação regional física e coeficiente na teoria interagente UV completa.

Append com backup de bytes nas superfícies canônicas só pela gerência autorizada. A bancada atualiza sua memória e entrega o adendo no túnel; não escreve nos originais de outras pastas.
