# Suficiência082 — exclusão do setor sem derivadas e identificação do próximo diferencial

10/09/2026. [DERIVED — demonstrações escritas revisadas] [REAL — controles algébricos e custódia documental].

**Todos os dez candidatos quadráticos sem derivadas de Weyl foram excluídos como solução do cancelamento.** Para investigar os candidatos com derivadas, identificamos o diferencial completo com o de Chevalley–Eilenberg, atuando nos jatos de Weyl com suas relações. O alvo é um cociclo nesse complexo. Uma corrente gradiente fornece uma imagem explícita, mas a nulidade da classe alvo continua aberta.

## 1. Estado canônico e domínio conservado

A [captura082](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_082_20260910/ESTADO_CANONICO_082.json>) confirma os mesmos quatro arquivos canônicos da081: v338, 683 arquivos embutidos e 77 dos 98 módulos acompanhados presentes; 21 permanecem ausentes. O selo corresponde aos bytes de um.py. Foi leitura por bytes e AST, sem executar/importar o programa ou repetir sua rodada. A parede UV continua aberta na própria fonte. H3 interno, fase/ramo e falsificadores já reconhecidos permanecem preservados.

As provas usam o complexo métrico mínimo de zeroformas naturais orientadas, referência espaço-forma fixa em quatro dimensões, K>0, κ real não nulo fixado, φ0 constante projetada e escalares inertes herdados. Cada elemento tem ordem finita de jatos. Não se afirma comparação pronta com φ=id, outros fundos, tensores espectadores ou um anel restrito com K variável.

## 2. O setor sem derivadas não fornece o cancelamento

Sym²W tem dois escalares, dois tipos Weyl e outros tipos sem emparelhamento com Λ³G. Assim o setor sem derivadas tem dez contrações: oito produtos dos dois escalares I,J_W com as quatro cúbicas de ghosts e duas contrações de tipo Weyl quadrático com CCm.

Na avaliação Killing/TT já usada079–081, as cúbicas ímpares têm valores

βo=−6θ012/z0,   γo=+6θ012/z0³,
ev(s1γo)=−K ev(s1βo),   K=1/z0².

Essa proporcionalidade vale na avaliação; não identifica as cocadeias universais. Os produtos com I são pares em k, e os dois tipos Weyl são invisíveis por Bianchi. Para qualquer combinação do setor,

Lk(s1Q)=A R(k),
R(k)=24k³/z0−96k/z0³,
A∈Rher independente de k.

Em k=2/z0, R(k)=0; o cancelamento exigiria +8/z0². Logo nenhuma combinação desse setor resolve. A conclusão conserva os coeficientes herdados, inclusive nilpotentes, e a possibilidade de somar fronteiras s0. A contribuição direta de antifields h*C⁴ continua invisível pelo detector079. A exclusão não alcança todos os termos com derivadas.

[Prova do setor](<C:/IALD/Central de Patentes/Chatgpt/SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779/IMAGEM_DO_DETECTOR_NO_SETOR_FINITO.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_SETOR_FINITO_082_20260910_052417_739397/PARECER_SETOR_FINITO_SEM_DERIVADAS_082.md>).

## 3. O diferencial sobre todos os jatos foi identificado

Se Mcal é o módulo linear de Weyl modulo EOM e N=Sym²Mcal, a diagonal E=q+2 torna-se

(H^q(s0)_(E=q+2),d1) ≅ Rher ⊗ (C^q(g,N)^h,dCE),
h=so(1,3), g=álgebra matricial de Killing.

O lado direito é o subcomplexo invariante pela isotropia, não o CE relativo. As fórmulas sobre os geradores são

d1p=−Mghost p,
d1Mghost=−Mghost²+Kpp♭,
d1W_r=p^a∇bar_aW_r+𝔯(Mghost)W_r.

Aqui Mghost=antisym(∇C)=−g0⁻¹m. A matriz chamada M na nota do setor finito é g0⁻¹m, com o sinal oposto. Mcal é um terceiro objeto: o módulo de coeficientes. J_W é o pseudoscalar quadrático local, e βo uma cúbica de ghosts; não se confundem com a involução J=Luz ou a constante β_TGL.

As igualdades acima são sobre classes: as fórmulas completas conservam s0p2, s0k2 e s0(T_r,2−𝔯(H/2)W_r). O tensor T_r=(∇g)^rWg completa naturalmente cada jato. O comutador de transvecções mantém a curvatura e todos os índices adicionais dos jatos. As relações de EOM/Bianchi são preservadas.

Não foi provada local finitude sob g: transvecções podem aumentar a ordem indefinidamente. A dimensão dez de g não torna N finito nem autoriza Whitehead. O operador foi identificado; sua imagem completa ainda precisa ser calculada.

[Demonstração CE](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CE_QUADRATICO_082_20260910_053047_6990258/PARECER_IDENTIFICACAO_CE_082.md>).

## 4. A obrigação agora é a classe seguinte; uma corrente explícita

Defina ν(p)=ε_abcd p^ap^bp^cp^d/4!. O alvo a=[A6] corresponde a J_Wν(p), incluindo o fator volume da referência. Ele é fechado por dCE: a ação de isotropia tem traço zero e o termo de transporte teria cinco p em dimensão quatro.

Pela transferência080,

−[A6]∈im d1E5  ⇔  [J_Wν(p)]_CE=0 em H⁴(Cnat,dCE).

A não nulidade de [A6] em H⁴(s0) não decide a classe na cohomologia seguinte. A imagem não nula encontrada081 tampouco decide sua nulidade.

Uma família horizontal, permitida sem retirar os demais cochains, é

q_V=ε_abcd V^a p^bp^cp^d/3!,
dCE q_V=(div_bar V)ν(p).

Para V=∇bar J_W, a corrente gradiente q_grad satisfaz dCE q_grad=(□bar J_W)ν(p). Há realização finita antes da cohomologia:

s1q_grad+s0q6=(□bar J_W)ν(C),
q6=[t⁶]{ι_(grad_g 𝒥(g))vol_g evaluated on (tC)³/3!},
g=g0+t h,  𝒥(g)=tr(W(g)∧W(g))/vol_g.

q6 é da espécie h³C³ e tem ordem finita de jatos. Para engenharia zero, multiplicar a identidade inteira por κ. Essa imagem é □bar J_W, ainda não −J_W: nenhum cancelamento foi declarado. A nota não calcula seu perfil TT.

[Cociclo e corrente](<C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_OBSTRUCAO_CE_CORRENTE_082_20260910_053437_900535/PARECER_CLASSE_CE_E_CORRENTE_GRADIENTE_082.md>).

## 5. Evidência e pendências

O [recibo finito082](<C:/IALD/Central de Patentes/Chatgpt/SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779/CONTROLES_SETOR_SEM_DERIVADAS_082.json>) registra 18 controles algébricos exatos e um de integridade de fontes, numa execução de Python com biblioteca padrão. Aritmética e proveniência tiveram revisão estática; zero rerun e zero Lean novo. A completude tensorial, a identificação CE e a corrente gradiente são demonstrações escritas revisadas, não resultados de uma amostragem numérica.

A [revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_082_20260910/PARECER_SETOR_FINITO_E_CE_082.md>) separa esses alcances. A aprovação da corrente construída pela raiz está em parecer externo próprio. As notas de origem que registravam revisão pendente devem ser lidas junto dos pareceres posteriores, preservando a história.

[OPEN] Calcular a imagem CE no módulo completo com derivadas, decidir a classe alvo e construir uma primitiva finita admissível, ou provar uma exclusão geral. Passar num detector é necessário, mas não prova a identidade universal. A investigação083 fica excluída desta entrega.

Continuam também a torre real e demais canais de anomalia, contratermos causais e QME, corrente/carga interagentes, compatibilidade entre fundos/estados/cortes, reconstrução gravitacional geral pelos mesmos dados selecionados, justificação UV e integração formal das construções aprovadas. A fase/ramo já paga não é reaberta.

Somente arquivos novos sob Chatgpt foram escritos. Originais, Atlas, índice, memórias canônicas, selo e gate continuam intactos. Nenhum teste de natureza foi realizado.
