# Parecer independente: equivalência BV formal métrica–vielbein

09/09/2026, continuidade 070. [DERIVED — revisão matemática escrita, sem CAS ou Lean]. Li integralmente [EQUIVALENCIA_FORMAL_E_PARES_LORENTZ.md](../EQUIVALENCIA_BV_METRICA_VIELBEIN_070_20260909/EQUIVALENCIA_FORMAL_E_PARES_LORENTZ.md). **Não identifiquei erro material no escopo local formal e de naturalidade em dados de fundo transportados conjuntamente.** O pin efetivamente lido está no manifesto novo. Nada na fonte foi alterado.

## 1. Decomposição com assinatura indefinida

A construção usa séries em uma matriz A com termo constante zero. Não importa uma decomposição polar Euclidiana: S²=I+A e SS⁻¹=I são identidades formais no subanel gerado por A. A autoadjunção relativa a gbar é preservada pelas potências, portanto SᵀgbarS=g vale também para assinatura (+---). O bloco constante gbar é invertível por hipótese. Não se exige que um operador indefinido tenha raiz quadrada positiva global.

L=e(e_sigma)⁻¹ satisfaz LᵀηL=η. Como seu termo constante é I, a identidade formal log(L⁻¹)=−log L implica que chi=log L está em so(1,3). A exponencial reconstrói e a partir de g e chi. Assim a contagem 16=10+6 corresponde a uma transformação formal inversível, no componente da identidade e com a orientação fixada.

## 2. Ghost e compensação

Os sinais de (5) conferem pela regra graduada. Em s²e, a contribuição restante de Lorentz é

    (s c_L−Lie_C c_L−c_L²)e,

que se anula na convenção adotada; Lie_(sC)−Lie_C² também se anula. Por antissimetria de c_L, sg=Lie_C g. O setor métrico não recebe dependência no ghost Lorentz.

Para delta L=c_L L, a trivialização direita da derivada da exponencial dá delta L L⁻¹=[(exp(ad chi)−1)/(ad chi)] delta chi, com o sinal de ad chi utilizado na nota. A inversa tem termo constante identidade; não é uma divisão por chi. A parcela F de difeomorfismos deve permanecer, e permanece na fórmula (7). A mudança (c_L,C)↔(upsilon,C) é triangular: resolve c_L por substituição local, sem inverter uma EDP. Definir upsilon=s chi dá supsilon=0 por nilpotência, em vez de impor essa igualdade adicionalmente.

## 3. Antifields e contração relativa

A transformação de campos/ghosts é uma substituição local com inversa local, embora contenha primeiros jatos. Seu diferencial de Fréchet e o da inversa são inversos como substituições prolongadas. O levantamento cotangente usa os adjuntos formais dessas matrizes diferenciais; a integração por partes preserva a forma BV no quociente por d. Essa construção explica por que não surge uma hipótese independente de inversão de operador diferencial nos antifields.

Como a mudança não depende de antifields, a ação mínima linear neles continua sendo o pareamento com o vetor BRST transformado. O setor clássico depende somente de g e phi. Segue S_new=S_metric+∫chi* upsilon, incluindo o deslocamento do antifield de C causado por F. A definição p=s upsilon* absorve apenas um sinal unitário de convenção e fornece o segundo par; não elimina antifields prematuramente.

A homotopia rho tem ghost −1 em ambos os pares. Prolongada aos jatos, satisfaz {s,rho}=N e rho d+d rho=0. De sa_k=−dm_k, a identidade resulta com o sinal exibido:

    a_k = s(rho a_k/k)+d(rho m_k/k),   k>0.

A projeção dos pares a zero é um morfismo para s e d. Ela prova também a injetividade, não apenas que todo representante pode perder os pares. A divisão por k opera coeficiente a coeficiente e mantém a ordem de jato finita em cada coeficiente formal. O apoio bibliográfico é exatamente o mecanismo de pares e seus antifields, inclusive para sa+dm=0, de [BBH 2000, §2.7, equações (2.48)–(2.51)](https://arxiv.org/pdf/hep-th/0002245v3); a transformação específica desta nota foi conferida separadamente acima.

## 4. Precisão explícita sobre mudanças de referencial

A naturalidade afirmada na seção 6 está correta, mas convém registrar a transformação implícita do **ghost antigo**. Com e'=Omega e, ebar'=Omega ebar e sOmega=0, a manutenção da forma se'=Lie_C e'+c_L'e' exige

    c_L' = Omega c_L Omega⁻¹ − (Lie_C Omega) Omega⁻¹.

O último termo é necessário quando Omega depende de x. Ele decorre diretamente de s(Omega e)=Omega se. Não se deve substituir c_L' por somente Ad_Omega c_L nessa convenção que mantém o fundo fixo sob s.

A nota não faz essa substituição incorreta: ela afirma a transformação adjunta de **chi e upsilon**, que de fato vale. De L'=Omega L Omega⁻¹ e sOmega=0 seguem chi'=Ad_Omega chi e upsilon'=Ad_Omega upsilon. A compensação F e a transformação local do ghost antigo tornam as duas descrições compatíveis. Os antifields novos seguem na representação dual densitizada. Essa precisão explicita a colagem sem exigir uma correção da fonte.

Rho identifica dois exemplares do mesmo fibrado e comuta com essa mudança externa e seus prolongamentos. O resultado permite trabalhar em cartas de referenciais sobre o fundo fixo; não implica independência da escolha de gbar, ausência de setores globais de Lorentz ou admissibilidade de primitivas em uma classe que proíba toda dependência de fundo.

## 5. Veredito e fronteira

A equivalência H_formal(s_vielbein|d)≅H_formal(s_metric|d) está sustentada no espaço declarado. Ela permite transportar uma classificação já demonstrada **na mesma classe formal admissível**. Não implica que H^{1,4} do sigma seja nulo, não elimina por si um contrato de cohomologia característica e não prova admissibilidade causal/renormalizatória de toda primitiva produzida. O tratamento de matéria Lorentz-escalar e ação sem conexão de spin independente é uma hipótese real, satisfeita pela ação examinada, e não pode ser removido por generalização verbal.

[REAL] Revisão somente de leitura. Fonte conferida antes/depois, inalterada. Nenhum CAS, Lean, programa canônico, integrador ou finalizador foi executado. Parecer interno delimitado; não se atribui aprovação externa ou confirmação do operador.
