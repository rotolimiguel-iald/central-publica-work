# Handoff — o diamante na rede efetivamente construída

16/09/2026. Adendo às entregas V2 e Centralizador. Originais preservados; execução e arquivos novos somente em Chatgpt.

**Resultado novo [REAL]: na `wedgeNet` canônica, todo diamante redondo finito de Minkowski recebe `scalarAlg`. A álgebra do diamante é diferente da álgebra não abeliana da cunha.** Sete teoremas foram elaborados pelo Lean, sem `sorry`, novos axiomas ou advertências. Os objetos compilados das dependências existentes foram reutilizados; não houve reconstrução integral do kernel canônico nem revisão independente.

Isso localiza uma dificuldade anterior à determinação do coeficiente físico de R. A centralidade da ação no diamante dessa rede é automática para qualquer candidato limitado a R. Portanto esse teste, nessa rede, não distingue uma carga geométrica correta de uma carga arbitrária.

## Fontes e alcance

O acesso de leitura ao canônico foi obtido nesta continuação. Isso supera a restrição de acesso relatada no adendo anterior. Os hashes e a busca delimitada estão em `CANONICAL_DIAMOND_SOURCE_AUDIT.json`.

- `TGLExt/WedgeNet.lean`: `hasRW`, `hasLW`, `wedgeNet`, `scalarAlg`, `theSpecificAQFTWitness`.
- `TGL/SpecificAQFTWitness.lean`: exige não abelianidade e ciclicidade/separação na **cunha**. Não exige esses predicados em diamantes limitados. O habitante satisfaz o contrato escrito; este resultado não refuta suas provas.
- `TGLExt/V350WedgeModularData.lean`: `towerWedgeData` fornece dados modulares da cunha. O próprio comentário limita o alcance a essa camada.
- `TGLExt/V350GateContract.lean` e `V350ModularCertificate.lean`: o certificado usado no fechamento é a dualidade do fator da torre, incluindo as duas inclusões de JMJ=M′. Este adendo não reabre essa dualidade.
- `TGLExt/TheSameBetaReadsFourFaces.lean`: a EOM é hipótese explícita; `boxOperator` não é construído da métrica e `K_boundary` não é identificado ali com o gerador da torre ou com a carga de tensão-energia.

A busca em TGL/TGLExt localizou também redes `PhysicalNetData`, como `theWideNet`, `theFusedNet` e `thePoincareNet`. Seus contratos são de fibras e transportes; seus nomes não substituem uma identificação com a rede de álgebras regionais da pergunta. O levantamento registrado é dessa árvore de fontes, não uma declaração de inexistência em todo o computador ou em toda teoria possível.

O SHA256 de WedgeNet canônico é igual ao da fonte da dependência local usada na elaboração. O relatório guarda os valores lidos, sem hashes transcritos de memória.

## Prova aplicada à construção existente

Pela definição, `hasRW O` significa que O contém uma cunha direita inteira transladada. Uma cunha dessas contém pontos com x¹ arbitrariamente grande: `deep_right_mem` já fornece os pontos. Logo uma região com x¹ limitado superiormente não pode contê-la. O argumento espelhado, usando `deep_left_mem`, exclui a cunha esquerda quando x¹ tem limite inferior.

Portanto, se lo ≤ x¹ ≤ hi em O, os dois predicados são falsos. A própria ramificação de `wedgeNet` devolve `scalarAlg`.

Para o diamante aberto

    D(c,ℓ) = {x : |x⁰−c⁰| + sqrt((x¹−c¹)²+(x²−c²)²+(x³−c³)²) < ℓ},

temos c¹−ℓ ≤ x¹ ≤ c¹+ℓ. A aplicação ao habitante existente é direta:

    theSpecificAQFTWitness.net D(c,ℓ) = scalarAlg.

O enunciado Lean vale para todo ℓ real; quando ℓ≤0 a região é vazia. O caso físico considerado tem ℓ>0. A região formalizada é de Minkowski; não se presume que esse resultado prove algo sobre toda rede em espaço-tempo curvo.

`scalarAlg` é definida como o comutante de todos os operadores limitados em WH. A identificação usual desse conjunto com ℂI pode ser demonstrada diretamente: se T comuta com todos os operadores de posto um, escolha um vetor unitário e. Comutar com a projeção em e dá Te=ce; comutar com |v⟩⟨e| dá Tv=cv para todo v. Essa última identificação está demonstrada neste texto; a nova fonte Lean usa a definição exata de `scalarAlg` e o lema existente de comutação, sem alegar formalização adicional de Schur.

A não abelianidade da cunha, já presente no habitante, fornece A e B que não comutam. Assim a álgebra de D não pode ser a álgebra da cunha. O sétimo teorema formaliza esse contraste; ele impede substituir D por W na cadeia por simples mudança de nome.

## Consequência para R e para a identificação vácuo/dephasing

Para A nessa álgebra regional, o kernel prova

    Commute R A

para **todo** R limitado em WH. Não há dependência de β, ℓ, curvatura ou constantes de interação nesse resultado. Isso não identifica um primeiro coeficiente físico igual a zero: a leitura disponível não tem observáveis não escalares capazes de distingui-lo.

Comutar com a álgebra não demonstra pertencer a ela. Portanto não substituir “ação trivial” por “R pertence ao centro” sem a hipótese de pertença/afiliação apropriada. Tampouco substituir R físico ilimitado por um operador limitado sem regularização e domínio explicitados.

Todo canal complexo-linear unital fixa cI. Todo estado normalizado tem a mesma restrição ω(cI)=c. Assim, nessa álgebra regional, a invariância sob dephasing não distingue qual estado global é o vácuo. Esse é um resultado sobre a informação disponível na realização, não uma rejeição da nomenclatura ontológica do operador.

A ponte parcial da V2 continua válida na torre: igualdade de fluxos em uma subálgebra especificada, com resto central nesse setor. Ela não identifica automaticamente esse setor com 𝒜(D), pois acabamos de verificar qual 𝒜(D) o habitante regional existente de fato atribui.

## Uma razão estrutural que impede a correção por mero religamento

[DERIVED — prova textual] Na rede canônica, U(a)=I. Em qualquer rede local covariante por translação com essa mesma propriedade, A(O+a)=A(O). Se O é um diamante limitado de Minkowski, escolha uma translação espacial suficientemente grande para tornar O e O+a separados tipo-espaço. Pela localidade, todos os pares de elementos de A(O) comutam: o segundo elemento também pertence a A(O+a). Logo a álgebra regional é abeliana.

Portanto manter simultaneamente localidade, covariância e U≡I impede obter uma álgebra não abeliana nesse diamante apenas mudando a seleção de setores. Não se corrige isso trocando um pin, somando uma função de dephasing ou transportando o selo JMJ=M′. Uma realização física regional precisa de dados e provas adicionais de localização/translação. Esta observação textual não foi adicionada como nova condição ao gate.

## O que a sessão do um.py deve fazer com esta entrega

1. Preservar o fechamento algébrico já verificado e as provas incorporadas na v358. Não duplicar pinching, cociclo, logaritmos ou geradores.
2. No índice/relatório existente que associa “torre/cunha/diamante”, distinguir os objetos: dualidade da torre provada; álgebra do diamante na `wedgeNet` escalar; identificação regional física ainda aberta.
3. Recompilar a fonte de auditoria se for incorporá-la. Consumir seus enunciados como delimitação de alcance; nenhum resultado experimental move o gate e nenhum “zero” dessa leitura deve virar coeficiente físico.
4. Para calcular o coeficiente pedido, fornecer uma realização regional com observáveis locais não escalares e uma referência de vácuo especificada, a construção de Tμν e Kξ e uma regra de comparação quando o estado/diamante variar. Então reutilizar R₁=−Dlog(ρ₀)[ρ₁]−Q₁ e [R₁,A₀]+[R₀,A₁], já entregues. As fórmulas de densidade são da regularização finita; a passagem ao contínuo tem suas próprias hipóteses.

Não foi implementada uma nova teoria de campos interagente UV completa. Não foi calculado um coeficiente físico para ela. A meta de gravidade quântica permanece aberta. O progresso desta rodada é eliminar uma ambiguidade concreta de localização na realização efetivamente existente.

## Proposta de memória canônica — append pela gerência

[REAL/DERIVED, 16/09/2026] `WedgeNetFiniteDiamond.lean` prova que regiões limitadas na coordenada x¹, incluindo diamantes redondos finitos de Minkowski, recebem `scalarAlg` na `wedgeNet` existente. Qualquer resto limitado tem ação trivial ali; isso não determina R nem seu coeficiente físico. A não abelianidade da cunha prova que a álgebra do diamante é diferente da dela. O contrato do habitante exige ciclicidade/separação e não abelianidade na cunha; suas provas permanecem válidas. U≡I e localidade/covariância impõem abelianidade em regiões separáveis por translação espacial. [OPEN] realização regional física não trivial e identificação com a carga T·ξ. Sem alteração do gate. Ler auditorias e manifesto da bancada antes de incorporar.

Aplicar a regra de backup de bytes e append às memórias canônicas quando a gerência incorporar: Atlas, índice vivo, memória/diário da linhagem e desenho do fechamento. Nesta bancada as atualizações ficam em Chatgpt, respeitando a restrição do operador.
