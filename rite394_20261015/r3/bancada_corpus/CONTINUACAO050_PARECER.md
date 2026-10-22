# Continuação050 — adjunto, quadrado e reconstrução pelo resolvente

[REAL — escopo dos teoremas compilados e auditados] Emissão UTC: 2026-09-07T03:21:14.933112+00:00

O lote liga o operador de Tomita contínuo da049 ao operador Δ=S†S e reconstrói o grafo de sua raiz positiva por cálculo funcional contínuo de operadores limitados. O espaço H=L²(ℝ,dξ;ℂ) e o parâmetro c são os dados do modelo049. Não se demonstra aqui que a natureza ou a torre anterior selecionem esse modelo.

## Adjunto maximal e domínio da composição

Para T_c f(ξ)=exp(-cξ)f(ξ), em seu domínio ponderado efetivo, e Jf(ξ)=conj(f(-ξ)), o operador anterior é S_c=JT_c. A identidade com a construção genérica está provada, não presumida por igualdade de nomes.

O adjunto antilinear S_c†=T_cJ tem domínio {y:Jy∈D(T_c)}. A convenção de pareamento é ⟨S_cx,y⟩=⟨S_c†y,x⟩. Além da identidade, prova-se maximalidade: todo par (y,z) que satisfaz o pareamento para todos os x no domínio pertence ao grafo desse adjunto. A prova usa a densidade e o adjunto linear maximal do Mathlib.

A composição exige duas pertinências de domínio. Para todo f∈H:

    f∈D(S_c†S_c) ⇔ f∈D(T_c) e T_cf∈D(T_c) ⇔ f∈D(T_(2c)).

O teorema do grafo completo identifica Δ_c com S_c†S_c, incluindo domínio e valor; a igualdade global de operadores parciais fornece:

    Δ_c = S_c†S_c = T_c² = T_(2c).

Δ_c é positivo, auto-adjunto e fechado. A forma quadrática satisfaz Re⟨Δ_cf,f⟩=||S_cf||² em D(Δ_c); pela simetria hermitiana, a mesma parte real aparece em ⟨f,Δ_cf⟩. T_c é uma raiz positiva auto-adjunta de Δ_c.

## Reconstrução intrínseca pelo resolvente

Os operadores limitados A e B da049 satisfazem A²+B²=I e parametrizam o grafo de T_c por (Ah,Bh). A positividade de A e B foi provada na ordem de operadores, a partir dos multiplicadores positivos.

O lote demonstra que C=A² é o inverso limitado de I+Δ_c, com a imagem no domínio de Δ_c e as duas identidades inversas. A unicidade nesse contrato impede que o nome resolvente substitua sua propriedade.

No cálculo funcional contínuo de operadores limitados do Mathlib:

    sqrt(C)=A,     sqrt(I-C)=B,
    Graph(T_c) = {(sqrt(C)h, sqrt(I-C)h): h∈H},
    D(T_c) = range(sqrt(C)).

Assim o grafo do T_c construído é recuperado das raízes positivas limitadas do resolvente de Δ_c. Essa é uma caracterização intrínseca concreta da raiz; distingue-se do teorema geral de unicidade entre todas as raízes positivas auto-adjuntas não limitadas.

[KNOWN + DERIVED — identificação matemática com teorema externo] A unicidade clássica da raiz positiva auto-adjunta, aplicada a T_c²=Δ_c e à positividade/auto-adjunticidade de T_c, identifica T_c=Δ_c^(1/2), portanto JS_c=Δ_c^(1/2), neste modelo. Essa especialização usa o [teorema2.3 de Sebestyén–Tarcsay, manuscrito disponibilizado pelo autor](https://www.researchgate.net/publication/318660686_On_the_square_root_of_a_positive_selfadjoint_operator). O teorema geral externo não integra os axiomas nem o censo Lean050.

[OPEN — formalização geral] CFC.sqrt_unique aplica-se aqui aos operadores limitados A e B. Não foi aplicado diretamente a LinearPMap nem fornece, sem lemas adicionais, a unicidade entre todos os Q positivos auto-adjuntos não limitados com Q²=Δ. A nota independente [NOTA050_RAIZ_POSITIVA_CANONICA_REVISAO.md](<C:/IALD/Central de Patentes/Chatgpt/NOTA050_RAIZ_POSITIVA_CANONICA_REVISAO.md>) registra a rota e a dívida.

## Censo e verificação

| Módulo novo050 | Teoremas | Definições | Prints | Alcance |
|---|---:|---:|---:|---|
| [GenericAntilinearAdjoint.lean](<C:/IALD/Central de Patentes/Chatgpt/GenericAntilinearAdjoint.lean>) | 11 | 4 | 15 | Adjunto antilinear maximal de JT, domínio e composição. |
| [ContinuousModularSquare.lean](<C:/IALD/Central de Patentes/Chatgpt/ContinuousModularSquare.lean>) | 12 | 4 | 16 | Domínio efetivo de T_c² e igualdade global T_c²=T_(2c). |
| [ContinuousModularReconstruction.lean](<C:/IALD/Central de Patentes/Chatgpt/ContinuousModularReconstruction.lean>) | 14 | 2 | 16 | S†S identificado pelo grafo completo; Δ positivo auto-adjunto e forma quadrática. |
| [ContinuousModularResolvent.lean](<C:/IALD/Central de Patentes/Chatgpt/ContinuousModularResolvent.lean>) | 16 | 1 | 18 | Resolvente limitado e reconstrução do grafo pelas raízes CFC de operadores limitados. |

- Novos050: 53 teoremas, 11 definições, 1 instâncias próprias, 65 prints.
- Baseline049, com seis fontes pinados e recompilados: 85 teoremas, 23 definições, 108 prints.
- Conjunto recompilado: 138 teoremas, 34 definições, 173 prints; 11/11 etapas passaram, incluindo importador conjunto.
- Zero avisos/erros, cobertura exata das declarações por prints e somente propext, Classical.choice e Quot.sound.
- Fontes copiados por bytes em diretório exclusivo; inputs estáveis, sem fallback a oleans locais históricos ou do kernel canônico.
- Auditor independente BUILD_PASS; revisão vinculada ao hash e ao diretório final. Fontes e sondas falhas anteriores permanecem como histórico, sem serem promovidas a prova.

Diretório final: C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO050_CLEAN_20260907_031255_350368

Build SHA256: 03c9a85c833062805fb1c6dfc55d0d753694811a5106d02148b6e4c4d5ac1607

A fronteira externa de confiança compreende imports diretos do Mathlib/stdlib e companheiros pinados. Não foi reconstruída toda a cadeia transitiva externa a partir de fontes. A proveniência dos seis fontes049 é verificada; o auditor050 não repete a auditoria integral de todos os artefatos do selo049.

## O que permanece aberto

[OPEN] Formalização geral da unicidade da raiz não limitada, fluxo Δ^it e sua ação geométrica, rede física de álgebras e estado, Bisognano–Wichmann, inclusão semilateral, ligação desta representação com a torre, seleção física de c, área, H3 e reconstrução gravitacional geral.

A escala c, o espaço L² e sua medida são INPUT do modelo. A identificação matemática local não constitui prova de gravidade quântica. Esta rodada escreve somente em Chatgpt; não incorpora código em um.py, kernel, Atlas, índice ou memórias canônicas. canonical_gate_changed=false é declaração de escopo da escrita, não auditoria de mudanças de terceiros.

Revisão: [CONTINUACAO050_REVISAO_INDEPENDENTE.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO050_REVISAO_INDEPENDENTE.md>). Entrega: [ENTREGA_050_adjunto_quadrado_e_resolvente.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_050_adjunto_quadrado_e_resolvente.md>).
