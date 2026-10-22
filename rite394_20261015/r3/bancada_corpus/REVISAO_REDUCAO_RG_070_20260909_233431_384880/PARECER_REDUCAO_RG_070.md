# Parecer independente delimitado — redução on-shell e RG 070

[DERIVED — revisão matemática escrita] **FAVORÁVEL no escopo solicitado; nenhum erro material identificado.** Li integralmente REDUCAO_EFT_E_FLUXO_LOGARITMICO.md e confrontei suas equações com o coeficiente C4 de 069 e a fonte quartica anterior. A nota de redução foi construída por outro agente; sou autor da nota de calor de entrada. Este parecer revisa independentemente a redução nova e seus sinais, sem apresentar uma revisão independente adicional da minha própria derivação de calor.

## Conferências matemáticas

1. **Redução Euler/Einstein.** A troca Riem²=E4+4Ric²−R² dá os coeficientes 15/8 de Ric² e −13/16 de R². Com Ric=Λg+sW e R=4Λ+sQ, obtêm-se os cinco termos da equação (1), inclusive A1=−13s²/16+7s/6+1/6 e A2=27s²/8−s+1/3. Em s=4, A1=−49/6, A2=151/3 e 3A1+A2=155/6.

2. **Certificado do resto.** Para e=tr E, Ric=Λg+sW+E−eg/2 e (E−eg/2)²=E:E em dimensão quatro. Expandir (3) dá exatamente M da equação (8). Bochner fora das soluções acrescenta 〈u,Dτ〉; sua eliminação fornece −(s/6)div〈u,τ〉+(s/6)|τ|². A derivada de R=4Λ+sQ−e fornece +(1/6)□e. Esses termos fecham a corrente J e o certificado (7), com os sinais exibidos.

3. **Redefinição de campos.** A variação de árvore é E:δg/(2κ)−c〈τ,δφ〉. Portanto δg=2κχM e δφ=−χsτ/(6c) geram o resto da equação (7). O argumento é válido a primeira ordem em χ, incluindo o contrato de bordo. A nota corretamente identifica C42_poly como extensão escolhida de um polinômio on-shell, sem chamá-la de verdadeira Hessiana off-shell calculada.

4. **As duas divergências.** No fundo original, a redução dá
   C_red=(7440x²+1544x−211)/96.
   A corrente residual (1−s)□Q/6 vale 3x/4; somá-la recupera (7440x²+1616x−211)/96. Em 069, retirar somente a divergência explícita 5x/4 de (4.2) deixava (7440x²+1496x−211)/96. Os representantes sem divergência diferem por x/2; a troca de Bochner desloca precisamente essa contribuição. Não se detectou contradição entre 3x/4 e 5x/4.

5. **RG e pesos.** Da relação g_B^E=g^E(μ)+K A log(ρ²/μ²), derivar a bare fixo dá β_E=+2KA na primeira ordem. Pela convenção formal t_L=−iτ_E, g_L^W=−g_E e S_E=−iS_L^W, a densidade transforma com −i e L_E=−L_L^W. Assim Λ_E=−Λ_L, c_E=c_L, κ_E=κ_L e os quarticos satisfazem g_Q²^E=−b1 e g_W²^E=−b2. Logo β_b=−2KA, conforme (15). Não há fator ghost ou 1/2 adicional a inserir: já integra o C4 de entrada.

6. **Fonte FRW.** β_B=−155K/3 para B=3b1+b2. Com ρ4=−3B/a⁴ e p4=ρ4/3, a derivada a geometria fixa é +155K/a⁴ e +155K/(3a⁴), respectivamente. A nota preserva que essa é a parcela local escolhida, cuja dependência de μ não é a de uma observável física total. Não fixa o sinal do acoplamento finito nem a escolha μ(r).

## Alcance preservado

A tabela constitui fluxo de acoplamentos dimensionais num representante on-shell e numa convenção declarada. Não separa unicamente β_κ, β_c e β_Λ; não inclui escala canônica de variáveis adimensionais. O uso de parâmetros de árvore nos A_i é coerente a primeira ordem em ℏ. A continuação é uma regra local de coeficientes/ação, não prova de uma seção Euclidiana global ou de um determinante Lorentziano completo.

As limitações sobre medida ultralocal, contorno conforme, condições de bordo, informação off-shell ausente, estado e termos não locais estão explícitas. A solução da ação quartica truncada não é promovida a solução semiclassica única. A ausência de Pontryagin no C4 não é usada como prova de H¹ ou de QME.

[REAL — leitura documental] O recibo existente registra 16 controles CAS aprovados com resíduo zero e seus pins conferem. **Não reexecutei esses 16 controles, os 31 de calor, Lean, um.py ou qualquer finalizador.** A revisão acima foi feita por leitura e recombinação algébrica. Nenhuma fonte existente foi alterada.


Fonte revisada: C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ON_SHELL_RG_070_20260909_232623_681687/REDUCAO_EFT_E_FLUXO_LOGARITMICO.md
Tamanho medido: 14835 bytes.
SHA-256 medido: 6c438cc20de6a1b4f6faf4ad8f53b0a7540d00fc5a83eb0bf5efc6954dfc37b7.
