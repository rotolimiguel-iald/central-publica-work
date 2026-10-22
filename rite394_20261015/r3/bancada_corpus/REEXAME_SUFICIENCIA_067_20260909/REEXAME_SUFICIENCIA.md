# Reexame após a v338 — entrega 067

O avanço desta entrega é duplo: há uma realização probabilística com liberdade suficiente para obter a dinâmica Einstein–sigma por variação, e há uma construção explícita de estado quântico positivo para o sistema físico linearizado num fundo curvo com matéria. Ambos têm hipóteses identificadas. Eles reduzem as pendências anteriores; não estabelecem a teoria quântica gravitacional interagente geral.

## 1. O estado canônico efetivamente conferido

[REAL — leitura estática e comparação de bytes] O programa continua na v338. Os quatro artefatos — `um.py`, selo, manifesto e relatório da rodada — coincidem com a entrega 066. A rodada existente registra 5.306/5.306 teoremas limpos e autoteste aprovado; ela não foi repetida aqui. A leitura estática dos 98 módulos da bancada encontra 77 incorporados e 21 ainda ausentes. O [snapshot desta entrega](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_067_20260909/ESTADO_CANONICO_067.json>) contém os hashes medidos e os nomes exatos.

A recuperação de fase e ramo pelo registro, H3 interno, os critérios de falsificação e os resultados de interação não comutativa já demonstrados continuam reconhecidos. Não são lacunas reabertas nesta revisão. Também não se confunde a interpretação do selo com um teorema geral de quantização: o próprio selo mantém o muro de renormalização aberto.

A integração de 98 módulos da entrega 066 permanece a última cópia de bancada auditada. As demonstrações de hoje são escritas; não se acrescentou uma compilação Lean, uma execução de `um.py` ou um teste da natureza. Tampouco se deve substituir o canônico por uma cópia derivada de uma base histórica: a sessão codificadora deve portar os deltas para sua versão viva.

## 2. A ponte dinâmica clássica local agora tem uma construção suficiente

[DERIVED — prova escrita; KNOWN — realização riemanniana residual por Nash] O problema anterior era concreto: usar todas as probabilidades condicionais para definir os campos sigma deixava liberdade insuficiente para variar métrica e matéria independentemente. A família mínima de cinco categorias e posto quatro continua tendo apenas variações locais de calibre na imagem geométrica. O contraexemplo variacional dessa classe permanece válido.

A construção ampliada preserva os dados internos em grupos:

\[
P_0=q,\qquad P_{a\ell}=(1-q)\phi_a^2Q_{a\ell},\qquad
\sum_a\phi_a^2=1,\quad\sum_\ell Q_{a\ell}=1.
\]

Os totais dos grupos recuperam os campos coletivos; as condicionais conservam a informação interna. A identidade de Fisher é

\[
F[P]=\frac{dq^2}{q(1-q)}+4(1-q)\sum_a d\phi_a^2
 +(1-q)\sum_a\phi_a^2F[Q_a].
\]

Uma família explícita de quinze probabilidades possui segunda forma normal com Gram estritamente positivo. Misturá-la com uma realização isométrica do residual produz variações internas que realizam qualquer tensor simétrico infinitesimal, mantendo a matéria coletiva fixa. A variação da matéria pode então ser compensada internamente, dando

\[
D\Phi\,R=\mathrm{Id},\qquad\Phi(P)=(g[P],\phi[P]).
\]

O inverso à direita R é explícito, diferencial de ordem no máximo um e preserva suporte. Uma construção suficiente usa 429 probabilidades finas em quatro dimensões; esse número não é apresentado como mínimo. Para um relógio já fixado é exigida positividade de um residual exposto na prova. Se o relógio for livre, uma escolha temporal lenta assegura essa condição localmente para g lorentziana suave e matéria sigma na carta positiva. Não se altera um relógio físico previamente determinado para obter essa conclusão.

Daí segue um recíproco variacional efetivo. Adotada a ação Einstein–sigma e restringido o campo à esfera, estacionariedade em todos os dados finos dessa classe equivale às equações métricas e sigma independentes. A equação de Einstein não entra como hipótese adicional da equivalência. O multiplicador é reconstruído:

\[
\lambda_{\mathrm{rec}}=\sum_a\phi_a\Box_g\phi_a
=-\sum_a g^{-1}(d\phi_a,d\phi_a).
\]

[POSTULATE/INPUT] A ação, a partição e a escolha do representante ampliado são declaradas. A normalização dos pesos, isoladamente, não seleciona essa ação entre outras ações possíveis. **Aceita essa ação como lei do modelo, há suficiência dinâmica clássica local na classe livre construída.** Não é necessário continuar tratando o recíproco variacional como uma hipótese sem realização. Para identificar esse modelo com a TGL original em todo seu alcance, ainda importa justificar ou assumir explicitamente a correspondência física e as condições globais. A rota termodinâmica de área/calor conserva seu contrato próprio; a ação escolhida não demonstra automaticamente todos os seus termos.

[Prova da construção livre e do recíproco](<C:/IALD/Central de Patentes/Chatgpt/COARSE_GRAINING_VARIACIONAL_LIVRE_20260909_212902_6343960/PROVA_COARSE_GRAINING_LIVRE.md>).

## 3. A equivalência também alcança as equações linearizadas

[DERIVED — prova escrita] No fundo on-shell, com H a Hessiana restrita ao alvo sigma, a ação composta tem Hessiana

\[
B=A^*HA,\qquad A=D\Phi.
\]

De AR=Id segue R*A*=Id no sentido distribucional. Portanto

\[
Bp=0\iff H(Ap)=0,
\qquad \ker B/\ker A\simeq\ker H.
\]

Incluindo difeomorfismos compatíveis, a equivalência desce aos quocientes lineares. As direções verticais são redundâncias da representação, não novos modos gravitacionais. Isso explica por que a ordem diferencial aparente de B não autoriza acrescentar graus de liberdade.

O transporte simplético foi calculado, incluindo o termo criado pela dependência de g em dP. Se A=a+b∂, a potencial composta recebe Jᵘ=Eα b^{αµ}_i p^i. Na solução de fundo, a diferença entre as correntes é proporcional a HAp₁ e HAp₂, anulando-se nas soluções linearizadas. A igualdade integrada exige potenciais e condições de fronteira compatíveis; cargas de superfície não são apagadas por decreto.

A Hessiana sigma inclui a correção do vínculo. Também é indispensável casar o sinal global da ação com a convenção da quantização: as equações clássicas são insensíveis à troca global de sinal, mas a forma simplética não é. O inventário final inclui o esclarecimento dessa convenção.

Isso permite transportar uma álgebra CCR estabelecida no mesmo espaço físico local. Não demonstra uma parametrização probabilística positiva global em S³, nem positividade operatorial de P* mais uma flutuação gaussiana arbitrária. [Adendo linearizado e simplético](<C:/IALD/Central de Patentes/Chatgpt/ADENDO_LINEARIZADO_COARSE_LIVRE_20260909_214421_410751/ADENDO_LINEARIZADO_E_SIMPLÉTICO.md>).

## 4. O setor quântico linearizado tem um estado físico explícito neste fundo

[DERIVED + KNOWN — demonstração escrita, sem nova formalização Lean] Na ação de cinética física positiva,

\[
S=-\frac1{2\kappa}\int\mu_g(R-2\Lambda)
 +\frac c2\int\mu_g|d\phi|_g^2,
\]

o fundo é

\[
g=dr^2-a(r)^2\gamma_{S^3},\quad a=2\cos(r/2),\quad
\phi=\mathrm{id},\quad c>0,\quad\kappa c=4,\quad\Lambda=3/4.
\]

Trabalha-se em I×S³ com I aberto contido em (0,π). Os extremos a=0 e H=0 ficam fora do domínio. S³ inteira é uma extensão geométrica declarada; os cinco pesos positivos antigos não viram uma carta global.

A redução completa de restrições e calibre fornece setores escalar, vetorial e tensorial físicos com grau ℓ≥2. Os modos baixos são identificados por transformações explícitas ou pela ausência do gradiente homogêneo, sem divisões por cinéticas nulas. As cinéticas dos setores S/V são

\[
K_S=\frac{4[\ell(\ell+2)-3]}{\ell(\ell+2)+3}>0,
\qquad
K_V=\frac{4[\ell(\ell+2)-3]}{\ell(\ell+2)+5}>0.
\]

No setor TT, a resposta anisotrópica sigma acrescenta 8 ao termo espacial 2 da curvatura. O resultado é a ação com operador espacial −Δ+10, não o operador do vácuo. Após normalização canônica e dr=a dη, a=2sechη, os três setores obedecem

\[
u''+[p^2+2\operatorname{sech}^2\eta]u=0,
\quad
p_S^2=(\ell+1)^2+2,
\ p_V^2=(\ell+1)^2+3,
\ p_{TT}^2=(\ell+1)^2+6.
\]

A solução exata normalizada é

\[
f_p(\eta)=\frac{(p-i\tanh\eta)e^{-ip\eta}}{\sqrt{2p(p^2+1)}},
\qquad f_p\bar f_p'-f_p'\bar f_p=i.
\]

As somas de modos definem distribuições positivas. Os mapas explícitos de reconstrução e testes preservam a forma simplética, levando a covariância aos observáveis invariantes do sistema acoplado. A identidade de Green identifica o comutador com o propagador causal no quociente. A condição microlocal vem da meia onda e do operador espacial de Darboux, com orientação de frequência explicitamente fixada.

**A existência de estado quase livre positivo com CCR física e representante de Hadamard deixa de ser somente uma hipótese neste fundo e neste quociente linear.** A prova não depende de aplicar um teorema de vácuo Einstein a um fundo com matéria. Ela tampouco constrói uma matriz BRST completa com CCR sobre todos os testes não invariantes. Os projetores espaciais são não locais; a causalidade é demonstrada para os observáveis invariantes por comparação com a álgebra covariante.

[Redução S/V](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ESCALAR_VETOR_SIGMA_20260909_212531/REDUCAO_ADM_MODOS_FISICOS.md>) · [Ação e modos TT](<C:/IALD/Central de Patentes/Chatgpt/MODOS_TENSORIAIS_EXATOS_20260909/ACAO_TT_E_MODOS_EXATOS.md>) · [Construção física de Hadamard e contratos primários](<C:/IALD/Central de Patentes/Chatgpt/HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912/ESTADO_FISICO_HADAMARD_E_CONTRATOS.md>).

## 5. O que ainda falta, depois desses avanços

| Frente | Estatuto após esta entrega | Obrigação restante |
|---|---|---|
| Registro, fase e ramo | Resultados existentes reconhecidos | Preservar o conteúdo completo e o contrato dos dados; não reduzir o registro ao ângulo comum |
| Dinâmica clássica dos mesmos dados | Equivalência local demonstrada na representação livre, condicionada à ação Einstein–sigma | Explicitar a adoção física da ação/representação; compatibilidade global e eventual relógio selecionado; matéria no alcance efetivamente reivindicado |
| Estado quântico acoplado | Construção positiva física linearizada no fundo específico | Extensão a outros fundos e ao contrato de gauge/ghost necessário a funcionais não lineares |
| Interações quânticas gravitacionais | Não resolvidas por um cociclo de interação ou por um estado gaussiano | Construir a teoria perturbativa interagente, verificar identidades quânticas e possíveis anomalias |
| Altas energias | O próprio selo continua OPEN | Demonstrar a rota UV escolhida, incluindo tratamento dos contra-termos e limites; finitude do registro não substitui essa demonstração |
| Compatibilidade não linear/global | Demonstrações presentes são locais ou linearizadas | Colagem probabilística, condições de bordo, integrabilidade dos modos em Cauchy compacta e controle de extremos quando reivindicados |
| Incorporação formal | 21 módulos compilados ainda fora do canônico; resultados desta entrega são escritos | Portar os deltas e formalizar os enunciados novos sem converter documentação ou controles CAS em bandeiras Lean |

Essas obrigações dizem respeito à suficiência do modelo, mesmo antes de qualquer confirmação experimental. Sobreviver aos dados já examinados não demonstra os teoremas de interação, anomalias ou UV que permanecem abertos. Em sentido inverso, o fato de esses teoremas permanecerem abertos não apaga a reconstrução e os resultados condicionais já estabelecidos.

## 6. Validação e instruções para a sessão codificadora

[REAL — controles simbólicos exatos] Os recibos CAS enumeram 84 identidades da carta livre, 17 da redução S/V e 12 dos modos/ação TT: 113 controles. Cada residual é conferido simbolicamente. As desigualdades gerais, o uso de Nash, a completude harmônica, a equivalência funcional e a prova microlocal possuem demonstrações escritas; não foram reduzidos a esses 113 controles e não são apresentados como teoremas compilados.

Ordem de incorporação proposta:

1. Conferir novamente o canônico vivo e portar os 21 módulos pendentes da cadeia 063/065/066, seguindo os recibos já existentes.
2. Registrar como demonstrações escritas os contratos da representação agrupada, bloco livre, residual positivo, inverso à direita e recíproco variacional. A ação deve permanecer um postulado explícito.
3. Registrar o transporte linearizado com Hessiana restrita, sinal de ação consistente e termos de fronteira; não substituir tudo por uma afirmação de equivalência sem hipóteses.
4. Incorporar a redução S/V/TT, os modos exatos e o estado físico apenas com o domínio e o quociente demonstrados. A extensão BRST/interagente e o muro UV permanecem tipados em aberto.
5. Formalizar progressivamente as novas identidades e os contratos analíticos; somente novas evidências de compilação podem acrescentar bandeiras formais correspondentes.

O manifesto desta entrega mede os arquivos e recibos efetivamente usados. O resumo de transferência está no túnel. Todos os novos artefatos estão em Chatgpt; os originais, Atlas, índices canônicos e `um.py` foram preservados.
