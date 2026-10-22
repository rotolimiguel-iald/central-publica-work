# Suficiência081 — representantes quadráticos e uma imagem não nula distinta do resíduo

10/09/2026. [DERIVED — demonstrações escritas revisadas] [REAL — controles exatos e custódia documental].

**A liberdade restante foi reduzida a quadráticos de Weyl e sua imagem comprovadamente não é zero.** Toda classe E5 admite representante sem antifields, fechado por s0, enquanto os antifields continuam nas relações entre classes. Construímos um candidato explícito com imagem não nula; duas avaliações mostram que essa imagem e [A6] são independentes. Portanto esse candidato sozinho não cancela o resíduo. O problema de outros candidatos permanece aberto.

## 1. Estado canônico e domínio

A [captura081](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_081_20260910/ESTADO_CANONICO_081.json>) relê por bytes e AST, sem executar/importar um.py. Os quatro canônicos permanecem iguais080: v338, 683 arquivos embutidos, 77 dos98 módulos acompanhados presentes,21 ausentes; selo correspondente e parede UV aberta. Não houve nova rodada canônica. H3 interno, fase/ramo e falsificadores já reconhecidos permanecem preservados.

As provas desta entrega usam o mesmo complexo métrico mínimo de zeroformas naturais orientadas: dimensão quatro, referência espaço-forma K>0 FIXADA, κ real não nulo fixado, φ0 constante projetada e escalares inertes herdados. A ordem de jatos é finita por elemento. Não se afirma extensão a K variável num anel restrito, tensores espectadores, φ=id ou uma categoria causal com condições adicionais ainda não pagas.

## 2. Todas as classes E5 têm representantes quadráticos fechados

Se L é o complexo linear de jatos, a fatoração das identidades de Einstein por Bianchi dá

H⁻¹(L,s0)=0.

O argumento vale também para um ciclo dado apenas no ponto: escrever coeficientes à esquerda permite reduzir a ordem por P→P−B div, conservando PH=0. A primitiva termina em ordem finita e não divide por p².

Em Sym⁵L, ghost3 só admite(1,1,1,0,0) e(1,1,1,1,−1). Eliminado o segundo padrão,

H³(s0)_(E5,nat) ≅ Rher⊗[Sym²M⊗Λ³G]^Lorentz,

com M=H⁰(L,s0) gerado por jatos de Weyl modulo suas relações e G=V⊕Λ²V, os dados de Killing. M não foi declarado livre nem o módulo quadrático finito.

Consequentemente, qualquer ciclo b5 pode ser escrito

b5=Q(W1,∇bar W1,…;C,m)+s0χ5,   s0Q=0,

com Q quadrático nos jatos de Weyl e cúbico nos ghosts. O fechamento de Q vale antes das equações de movimento. As relações entre classes continuam usando as EOM e as primitivas com antifields h³C², h*hC³ e C*C⁴. A conclusão trata também ciclos mistos; não supõe que seu pedaço antifield feche sozinho.

[Demonstração E5](<C:/IALD/Central de Patentes/Chatgpt/COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md>) · [Revisão independente da aplicação](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_REDUCAO_QUADRATICA_081_20260910_050052_914909/PARECER_H3_E5_E_REPRESENTANTES_QUADRATICOS_081.md>).

## 3. Uma classe admitida tem imagem não nula

Para manter os tipos explícitos, chamamos aqui J_W o pseudoscalar tr(W1∧W1)/vol_g0, e Bgh a cúbica ε_abcd C^aC^b m^cd/2. São os símbolos J e β definidos localmente na nota do candidato. Tome

b5=κ J_W Bgh.

Ele tem ghost3, valência5, engenharia zero e s0b5=0 universalmente no fundo declarado. Nenhum coeficiente depende de k. Na família TT078, com z0=ℓ,

Lk(s1b5)=κ(24k³/z0−96k/z0³).

Em k=1/z0 o valor é−72κ/z0⁴≠0. Como Lk anula todas as fronteiras de s0, isso prova [s1b5]≠0. Em C5, b5 é ciclo e projeta a zero em C3; sua imagem pela conexão é [s1b5]. Logo

δ(Kcal)≠0.

Essa conclusão refuta a hipótese de que o detector ímpar anulasse a imagem de TODOS os quadráticos fechados. Ela não estabelece −[A6]∈δ(Kcal).

A ponte entre BRST e a derivada de Lie foi mantida inteira: s1J_W+s0J3=C·∂J_W, obtida da série do pseudoscalar da métrica ativa. O termo s0J3 só desaparece na avaliação por Killing. O cálculo de J'_W também mantém o fator conforme e deriva antes de impor os dados iniciais.

[Candidato e prova](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_DETECTOR_WEYL_QUADRATICO_081_20260910/PARECER_DETECTOR_IMPAR_E_CLASSE_E5_081.md>) · [Revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_081_20260910/PARECER_REDUCAO_E5_E_DETECTOR_081.md>).

## 4. A imagem construída e o resíduo são independentes

Ponha a=[A6] e b=[s1b5]. Aplique os funcionais nas frequências1/z0 e2/z0, mantendo o MESMO fundo e coeficientes:

| Avaliação | a | b |
|---|---|---|
| ℓ_(1/z0) | −4/z0² | −72κ/z0⁴ |
| ℓ_(2/z0) | −8/z0² | 0 |

A matriz tem determinante−576κ/z0⁶, uma unidade em Rher. Portanto a,b são independentes sobre o próprio anel herdado, inclusive com nilpotentes. A nota dá uma retração explícita; eles geram um submódulo livre cindido Rher² de H⁴(A6,s0), para Rher não nulo. O restante desse grupo não foi calculado.

Isso prova −a∉Rher b: nenhum múltiplo escalar do candidato exibido, acrescido de fronteiras, cancela o resíduo. Não prova −a∉δ(Kcal), pois outras classes de E5 ainda podem contribuir.

Qualquer candidato a cancelamento precisa ter

ℓ_(2/z0)(d1[z5])=+8/z0².

O candidato κJ_W Bgh contribui zero nesse teste. A nova condição é um filtro para outros candidatos; não foi estendida a uma anulação de toda a imagem.

[Prova das duas avaliações](<C:/IALD/Central de Patentes/Chatgpt/INDEPENDENCIA_RESIDUO_E_IMAGEM_081_20260910/DUAS_AVALIACOES_E_SUBMODULO_LIVRE_E6.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_INDEPENDENCIA_RESIDUO_081_20260910_050818_526290/PARECER_DUAS_AVALIACOES_E_RETRACAO_081.md>).

## 5. Verificação executada e seus limites

O [recibo081](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTROLES_DETECTOR_WEYL_QUADRATICO_081.json>) contém14 registros:13 controles algébricos exatos e1 de integridade das cinco fontes, em uma execução Python puro. Houve revisão estática independente; nenhum rerun e zero Lean novo.

O script recebe as formas Weyl E/B. Sua derivação a partir de Riemann/Ricci/Schouten é demonstração escrita revisada, não um cálculo completo de geometria feito pelo script. As cinco fontes têm pins antes/depois; o próprio script possui somente pin final da execução matemática. A conferência atual não inventa um pin inicial.

A contagem Sym²W, dimensão55, produz dez emparelhamentos tensoriais sem derivadas com Λ³G. Isso não é a dimensão da cohomologia E5 nem classificação de todos os jatos. As duas avaliações do item4 são consequência algébrica escrita; não foram contadas como nova execução desse recibo.

## 6. Próxima obrigação e objetivo completo

Pela080, δ(Kcal)=im d1E5. Pela081, podemos escolher representantes Q quadráticos de Weyl, e sabemos que essa imagem tem uma direção não nula independente de [A6]. Falta decidir se OUTRAS classes fornecem a direção necessária: construir Q admissível e a6 finito com r6+s1Q=s0a6, ou provar exclusão de −[A6] para toda a imagem pertinente.

A redução E4 por cotas de representação não exclui automaticamente jatos altos nos produtos quadráticos: produtos de tipos grandes podem conter tipos pequenos. A investigação082 sobre famílias sem derivadas e a ação do diferencial fica EXCLUÍDA desta entrega081.

Continuam também a torre real e os demais canais de anomalia, contratermos causais, corrente/carga interagentes e QME, compatibilidade entre fundos/estados/cortes, reconstrução gravitacional geral pelos mesmos dados selecionados e justificação UV. A incorporação dos21 módulos pendentes é uma obrigação distinta.

Somente arquivos novos sob Chatgpt foram escritos. Originais, Atlas, índice, memórias canônicas, selo e gate permanecem intactos; nenhum um.py executado/importado e nenhum teste de natureza. As memórias novas registram o progresso com seus limites, sem substituir documentos anteriores.
