# Motor: reconhecimento e dephasing

[INPUT] Ordem do operador: “isso precisa entrar no nosso motor, no código, porque a meu ver é a ligação que vc me pediu já tem algum tempo”.

[REAL — implementado em cópia] A função existente `prove_decision_commutation`, em `um.py:3533`, agora computa o pinching E, seu complemento Q e a evolução T_t=E+exp(-Gamma t)Q. O resultado é consumido pela chamada que já existia em `run_um` e retorna no mesmo bloco `core["decision_commutation"]`, acrescido de `recognition_dephasing`. Nenhuma função nova no nível superior do programa, nenhum segundo motor, nenhum módulo Lean novo.

O domínio testado é uma face finita com dois blocos de dimensão dois. A lei temporal L=Gamma(E-id) é declarada como INPUT; o nome “igualdade” é leitura ONTO do predicado E(rho)=rho. Gradiente na métrica Hilbert–Schmidt, não métrica gravitacional. Beta vem de SEALED_CODATA_ALPHA*ONE*sqrt(e); Gamma usa tau/omega de referência declarados, sem predição física nova.

A evolução é aplicada ao estado completo com coerência entre setores. A saída selecionada de V=C_-G C_+ aparece como controle: E(rho_tr)=rho_tr, Q(rho_tr)=0 e o dephasing posterior é zero. Código não relata essa ausência de efeito como dissipação positiva.

[REAL — validação] 57 verificações passaram, incluindo comparação com gerador GKSL montado independentemente nas 16 unidades matriciais e exponenciado por diagonalização hermitiana. Resíduo contra o estado calculado pelo consumidor: 0.0. Quatro adulterações da dinâmica foram recusadas; ausência de cada uma das dez evidências herdadas também recusa o selo do módulo. Entrada ONE inválida é recusada. Valores e veredito anteriores foram preservados no caso válido. Todos os demais nós AST, incluindo kernel embutido, chamada principal e leitores do gate, permaneceram iguais. O programa completo passa por compile() sem execução.

[ESCOPO] A rodada completa de um.py não foi executada; nenhuma recompilação Lean nesta mudança. O teste executou a função real extraída por AST, com o relatório de axiomas previamente registrado e hash conferido do fonte Lean embutido correspondente. Não se importou o programa nem se materializou seu kernel. Isso não é uma nova rodada canônica, confirmação física ou mudança de gate.

Arquivos de revisão: `recognition_in_existing_consumer.diff`, `TEST_RESULTS.json`, `RESULTADO_MOTOR_RECONHECIMENTO.json`, `DELIVERY_MANIFEST.json`. Fonte original copiada preservada: `um_ORIGINAL_SNAPSHOT.py`.

Executar os testes com o Python que contém NumPy indicado em `TEST_RESULTS.json`. O script não substitui resultados preexistentes: preserve-os e use uma cópia da bancada se precisar repetir. Não executar `implement_recognition.py` por cima da cópia já produzida; ele também recusa sobrescrita.
