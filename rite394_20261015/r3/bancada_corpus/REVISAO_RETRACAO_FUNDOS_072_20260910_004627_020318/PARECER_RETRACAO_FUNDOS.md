# Parecer independente: retração BRST relativa dos fundos

10/09/2026, arco 072. [DERIVED — revisão matemática interna por agente distinto do autor] [REAL — leitura integral e pins medidos]. Este parecer examina a nota RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md e a precisão PRECISAO_FONTES_CONJUGADAS_E_REFERENCIA.md, ambas da tarefa principal. Os caminhos, tamanhos e hashes efetivamente lidos constam no recibo desta pasta. Não atribuo a esta revisão uma prova formal, execução causal ou validação externa.

**Resultado:** não identifiquei erro material nos enunciados e identidades dentro do domínio explicitado pela nota e por sua precisão aditiva. A restrição da conjugação à subálgebra sem antifields dos fundos externos é essencial e foi registrada pelo autor sem alterar a fonte principal.

## Pares relativos e globalidade no alvo

Para a métrica, u = B - g e v = Omega - sg obedecem Du = v, Dv = 0. A seção p envia B a g e Omega a sg. Avaliar simultaneamente B = g e Omega = 0 não é um mapa de complexos em geral; a nota não usa essa seção incorreta.

No setor sigma, u = Log_phi(B_phi) e v = Du fornecem coordenadas na vizinhança da diagonal do par de mapas. A recuperação de Omega em (3.4) mantém tanto a derivada da exponencial em sua base phi como a derivada vertical em u. Sob u' = J(phi)u, temos v' = Jv + (sJ)u. O termo afim não é suprimido.

A derivação h anula os campos completos e u e envia v a u. Consequentemente, h(v') = Ju = u'; o termo (sJ)u não contribui. O operador de contagem N também respeita essa transformação, inclusive após prolongamento aos jatos. A construção é global sobre uma vizinhança da diagonal em S3. Não afirma a existência de um logaritmo de pares arbitrariamente separados, nem uma carta global de valores da esfera.

## Retração e sinais da descida

A identidade Dh + hD = N vale nos geradores e se prolonga por Leibniz. A divisão por grau positivo produz DK + KD = 1 - ip. A projeção pD = sp e a inclusão Di = is são compatíveis com a seção acima.

A homotopia evolutiva comuta com as derivadas totais nos coeficientes; sua extensão às formas, com o grau total, satisfaz K d_H + d_H K = 0. Para Da + d_H b = 0, segue KDa = d_H Kb. Por isso o sinal positivo de d_H(Kb) em (5.1) é correto, e a fórmula (5.3) transporta efetivamente uma primitiva da projeção.

A avaliação e_0 em Omega = 0, mantendo B como fundo independente, é diferente de p. O uso de e_0 pressupõe uma quebra estendida a_ext com a restrição desejada. A retração não constrói esse levantamento a partir de qualquer cociclo do esquema causal com fundos inertes.

## Conjugação BV e precisão necessária

A nota introduz B* e Omega* para apresentar a ação forte ampliada, mas h e K foram inicialmente definidos apenas na subálgebra A[B,Omega], sem esses antifields externos. A precisão aditiva mantém explicitamente a conjugação nesse domínio.

A férmion Psi(fields,B), sem dependência de B* ou Omega*, preserva essa subálgebra: deixa B e Omega e desloca os antifields dinâmicos por funções dos campos e de B. O diferencial ampliado também a preserva. Nesse domínio, o transporte por conjugação de D,K,i,p é legítimo. O deslocamento de B* na apresentação forte continua necessário para gerar o termo correto de fonte Omega; isso não torna B* um argumento das inserções restritas.

Se fossem incluídas inserções dependentes de B* ou Omega*, seria necessária uma extensão da contração ao par conjugado e o correspondente dicionário causal. Essa conclusão maior não foi usada nem declarada.

## Admissibilidade e fronteira causal

A contração é local e finita por coeficiente na expansão formal em diferenças e parceiros. Não presume avaliação convergente de uma série, nem uma cota uniforme de ordem de jatos para qualquer série. As substituições podem introduzir os jatos já contidos em sg e sphi; a nota pede que eles sejam contabilizados. A analiticidade é preservada se presente na entrada e não é deduzida de mera suavidade.

O domínio é off-shell nos fundos independentes. Restringir previamente E(B) = 0 imporia vínculos aos parceiros e destruiria a apresentação por pares livres empregada. A nota distingue a CME completa da invariância do operador quadrático isolado fora de soluções.

A ressalva sobre o produto quântico está correta: d_B diferencia o propagador, e uma mudança de ordenação simétrica não corrige a variação da parte antissimétrica causal. Transporte de Moller, acordo perturbativo e Ward estendida continuam necessários. Se uma realização fixa um segundo fundo B0, a projeção pode continuar dependente desse espectador; a precisão não confunde isso com o complexo dos campos completos sem fundos externos.

Portanto o resultado revisado é uma retração clássica e o transporte condicionado de primitivas. Não é uma construção da quebra causal estendida, uma integração completa dos contatos D_n, uma prova da QME, da independência quântica do fundo ou de completude ultravioleta.

## Custódia e método

Li integralmente a fonte e sua precisão; conferi as identidades acima por cálculo algébrico escrito. Não reexecutei CAS, Lean, um.py ou produtos temporais. Não revisei de novo os resultados 069/071 como um todo, nem assumi sua admissibilidade numa classe mais estreita. Nenhum arquivo de entrada foi escrito. O recibo mede sua preservação antes e depois da gravação deste parecer.
