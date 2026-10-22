# Fase central de normalização — entrega

[REAL — prova compilada] CentralScalarPhase.lean está congelado: 18 teoremas, 3 definições, 21 auditorias e 2 processos aprovados, sem warnings. Recibo: C:/IALD/Central de Patentes/Chatgpt/FASE_CENTRAL_20260909_165421_701211/BUILD_20260909_165920_305303/BUILD_RESULT.json. Fonte medida em 2026-09-09T20:02:05.153505+00:00: 6400 bytes; SHA-256 1eb554d7a3e7aa75f0b5955ab385f823761890ef6e2f1d63b7ce2417822e0ec5.

[DERIVED — definição e efeito] Para a real, scalarPhase(a,t)=exp(−ita) e shifted(u,a,t)=scalarPhase(a,t)•u(t), no espaço de operadores do Hilbert canônico. A fase é um caráter temporal unitário. Portanto shifted preserva unitariedade, continuidade, u(0)=I e a lei torcida de cociclo para a ação modular canônica complexa-linear.

O teorema shifted_adjoint_action, linha 75, prova para qualquer operador A:

shifted(u,a,t) A shifted(u,a,t)* = u(t) A u(t)*.

Essa identidade nem exige u(t) unitário; depende do módulo unitário da fase. shifted_modular_action aplica a identidade a α_t(A), mostrando que β_t permanece exatamente igual.

[REAL — gerador e evolução] shifted_generator, linha 87, usa u(0)=I e HasDerivAt u (i•V) 0 e fornece:

HasDerivAt (shifted u a) (i•(V−aI)) 0.

shifted_generator_equation, linha 100, combina o gerador com a lei torcida e demonstra em todo t a ODE à direita:

shifted′(t) = shifted(t) · i α_t(V−aI).

Não há hipótese de que V comute com a dinâmica de base, nem construção de um estado no argumento. Os operadores e a ação são os canônicos.

[REAL — Z positivo] scalar_phase_log_cpow, linha 109, prova para Z>0 a identidade exp(−it log Z)=Z^(−it), usando a potência complexa principal. normalizedShift u Z é definido por shifted u (Real.log Z). normalized_shift_formula faz a identificação positiva; normalized_shift_generator desloca V para V−log Z·I; normalized_shift_modular_action preserva β.

A definição Real.log é total em Lean, de modo que os lemas algébricos de normalizedShift não precisam de positividade. A interpretação como normalização por Z^(−it) neste módulo é ligada ao lema que exige Z>0. Não se interpreta Z≤0 como peso de um estado.

[OPEN — ligação ao estado perturbado] Se um teorema separado fornece Φ(V) não nulo e Z=‖Φ(V)‖², este módulo permite efetuar a correção central Z^(−it). Ele não produz Φ(V), não prova sua norma nem identifica o cociclo como Connes–Radon–Nikodym de um estado normalizado. Não contém uma conclusão KMS escondida como premissa. Construção/positividade/normalidade/identificação modular do estado pertencem à etapa Araki separada.

[REAL — revisão e preservação] A raiz /root leu integralmente os mesmos enunciados na versão de 6411 bytes e emitiu revisão semântica favorável, destacando a distinção entre Ad inalterada e gerador deslocado e o uso correto de Z>0. As mudanças posteriores comunicadas corrigiram somente convert!/simp nas provas de derivada, sem alterar qualquer enunciado. A fonte final passou no Lean.

Tudo foi escrito nesta pasta nova Chatgpt; originais e fontes congeladas anteriores permaneceram somente leitura. Cada alteração própria tem backup imediato de bytes. Nenhum um.py foi executado, importado ou integrado. A folha e seu importador foram compilados usando a biblioteca63 aprovada, com fronteira de fontes/binários explicitamente medida antes/depois. Não se fez recompilação nem hash de toda dependência transitiva do kernel/Mathlib. Tentativas falhas e seus logs foram preservados.
