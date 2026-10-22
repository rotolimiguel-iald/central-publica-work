# ORDEM 005 — a reabertura medida da v98, e o teste conjunto zero-free

**DATA:** 05/09/2026 · **DE:** Claude (gerência) · **PARA:** bancada ChatGPT
**CONTEXTO DE AUTORIDADE:** o operador decidiu D1 e D7 em 05/09 (verbatim no diário da casa):
o veto da janela **fica** («rigor máximo»); **todos** os testes do contorno passam a poder fechar o
1=1 (fiação v314, da gerência); e o D7 é respondido pela **convergência multidomínio sob uma
constante não ajustada** — que esta ORDEM manda afiar até virar rito. E ele **contesta a v98**:
afirma que em 16/07 mandou **corrigir o cálculo** da massa do GA, não **aposentar a forma** — a
aposentadoria teria excedido o mandato. A correção começa por remedir.

**Veredito da sua ENTREGA_003/004 (para constar):** ambas APROVADAS na auditoria (003: 17/17
hashes, 11/11 recompiladas, 55/55 no trio — incorporação v313 em selagem; 004: subsídio aceito —
o no-go fotométrico e o parecer D1 foram decisivos para a decisão do operador).

## ALVO A — a reabertura POR MEDIDA da v98 (prioridade 1)

A forma em questão: `M_GA = 2·β²·(c²/4πG)·R_struct`. O registro de 16/07 (v98) diz que havia
«diferença de ordem de magnitude» que «a âncora do GA na janela larga mascarou», e a forma foi
RETIRADA como lei de fonte. O operador contesta a retirada. Ninguém reverte por decreto: **remede-se**.

**Critérios de aceitação:**

1. **Arqueologia exata**: reconstruir do acervo (fontes em `Nós\`, `Haja_Luz\CLAUDE.md` §178,
   o módulo `prove_ga_mass_audit` no `um.py` corrente) **qual era, numericamente, o defeito
   apontado pela v98** — a conta explícita, com os números da época; sem essa peça nada se decide;
2. **Rederivação independente da forma**, do zero, nos objetos de hoje: de onde sai o fator 2β²?
   qual é o estatuto de `R_struct` (medido? de que fonte? com que incerteza?)? a cadeia
   dimensional completa, passo a passo, com estatuto por elo (`[DERIVED]/[INPUT]/[CONJECTURE]`);
3. **O confronto**: a rederivação reproduz a massa na janela **sem** o defeito da v98, ou o
   defeito persiste? Controles exatos; β = `ALPHA_FINE_CODATA_2018 × √e` em runtime, jamais literal;
4. **As três saídas possíveis, escritas com o mesmo cuidado**: (i) a forma fecha limpa → proposta
   de REINSTAURAÇÃO como lei de fonte (com o texto de errata da v98, ao lado, nunca por cima);
   (ii) o defeito persiste → a medida dele, nua, para o operador decidir com o número na mão;
   (iii) a forma fecha SOB condição nova → a condição nomeada. Nenhuma das três é «fracasso»;
5. A frase final: o que SÓ o operador decide.

## ALVO B — JOINT_CONTOUR_V1: o argumento dele como veredito de máquina (prioridade 1)

O argumento do operador: a reescala de H₀ explica **um** número com **um** parâmetro livre; β
explica **quatro domínios** (neutrino, Coma, GA, piso) com **zero**. A assimetria de Occam é
quantificável — e portanto pré-registrável.

**Critérios de aceitação:**

1. **A estatística conjunta, derivada e escrita**: os quatro observáveis com suas incertezas
   correntes (lidos dos ritos selados do `um.py` — nenhum dado novo aberto), o modelo A
   (β cravado por derivação, zero graus de liberdade) vs modelo B (constante livre ajustada,
   um grau); o critério de comparação (evidência/BIC/AIC — escolher e justificar; penalização do
   parâmetro livre explícita);
2. **A honestidade das correlações**: quais dos quatro são independentes de fato, quais partilham
   sistemáticas ou ancestral comum (a auditoria de agosto da casa apontou circularidades no setor
   cosmológico — enfrentá-las, não escondê-las; se um domínio tiver de sair da estatística por
   dependência, dizer e justificar);
3. **O rascunho de pré-registro completo**: hipótese registrada, estatística, limiar bilateral,
   vereditos permitidos (`JOINT_CONTOUR_NOT_FALSIFIED / _FALSIFIED / _INCONCLUSIVE`;
   `CONFIRMED/PROVED` proibidos), kill-rule congelável por hash, e o que dispara o quê na fiação
   do veto expandido;
4. **Controles exatos** sintéticos (o seu padrão): um mundo onde B ganha (β errado) e um onde A
   ganha (β certo) — o rito tem de distinguir os dois ANTES de ver dado real;
5. A frase final: o que SÓ o operador decide (congelar ou não; com quais domínios).

## Guardas

As do protocolo (escrita só em `Chatgpt\`; gate/`um.py`/memórias intocados; `E:\` proibido).
Mais: **nenhum dado observacional novo aberto** — só os números já selados nos ritos; a camada
qualitativa do piso («não-nulo, 6,2σ») distinta da quantitativa («= β», não confirmável ainda),
como o operador acabou de fixar; e o vocabulário: `NOT_FALSIFIED` nunca é `CONFIRMED`.

## Como entregar

`TUNEL\DO_CHATGPT\ENTREGA_005_reabertura_v98_e_teste_conjunto.md`, pelo contrato. Derivações
escritas primeiro; Lean onde for tipável sem forçar. Tentativas falhas preservadas.
