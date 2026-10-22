# Revisão independente079: completamento da corrente e equivalência GL–ortogonal

10/09/2026. Autor: /root/finish_gibbs_realization. [DERIVED — conferência matemática escrita própria]. [REAL — verificações de bytes, AST e proveniência especificadas no recibo]. Nenhum CAS, Lean ou um.py executado/importado; nenhuma fonte ou memória existente alterada.

**Conclusão delimitada.** Não identifiquei erro material na [nota examinada](<C:/IALD/Central de Patentes/Chatgpt/COMPLETAMENTO_GL_ORTOGONAL_079_20260910/CORRENTE_QUADRATICA_E_EQUIVALENCIA_DAS_CONEXOES.md>). Recalculei a expansão de τGL nas valências quatro e cinco, o contraexemplo local de fechamento, a transformação entre as duas transgressões e a primitiva pela homotopia formal. As fórmulas sustentam os resultados anunciados: o pacote satisfaz a equação da quinta valência, mas falha a anterior; as apresentações GL e ortogonal representam a mesma classe específica em C5. Não sustentam a exclusão de todas as outras correções no núcleo 𝒦.

O primeiro writer inválido permanece preservado. O arquivo limpo difere dele exatamente pela retirada de um byte NUL. A falha não foi tratada como execução bem-sucedida. Abaixo distingo o que os bytes permitem conferir da história de execução declarada no registro.

## 1. Entradas e alcance da revisão

Li integralmente a nota principal, seu [manifesto](<C:/IALD/Central de Patentes/Chatgpt/COMPLETAMENTO_GL_ORTOGONAL_079_20260910/MANIFESTO_COMPARACAO_CONEXOES_079.json>), a [proveniência da cópia limpa](<C:/IALD/Central de Patentes/Chatgpt/COMPLETAMENTO_GL_ORTOGONAL_079_20260910/PROVENIENCIA_WRITER_LIMPO_079.json>) e o helper responsável por essa cópia. Examinei o AST do writer limpo sem executar nenhuma instrução sua, incluindo a correspondência entre sua constante NOTE e os bytes da nota produzida.

O [sistema079](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md>) e o [adendo de ideal fechado e coeficientes herdados](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md>) delimitam o consumo: apresentação métrica mínima, B0 inerte espaço-forma, φ0 constante, campos ativos off-shell, completação por valência e ordem de jatos finita em cada coeficiente. Antifields são admitidos na busca geral; a comparação concreta não os usa.

A transgressão convencional foi confrontada com a fonte primária [Chern e Simons, Characteristic Forms and Geometric Invariants, §3, Proposição 3.2](https://math.mit.edu/juvitop/pastseminars/notes_2019_Fall/Chern-Simons.pdf). Ela dá a identidade de derivação da forma transgressiva. O transporte ao diferencial s e a homotopia específica em S são verificados algebricamente aqui; não são atribuídos ao artigo como um teorema pronto sobre a categoria formal de079.

## 2. Expansão de Levi-Civita e coeficientes τ4/τ5

Abrevie H=g0⁻¹h, l=a(L), l2=a(L2), r=r(L), r2=r(L2), O=Ω0. A diferença exata de conexões usa

\[
g^{-1}=(1+tH)^{-1}g_0^{-1}
=(1-tH+t^2H^2-\cdots)g_0^{-1}.
\]

O numerador da diferença de Levi-Civita é t vezes uma expressão linear em ∇bar h. Portanto Γ−Γbar=tL−t²HL+…, com o produto H atuando no índice superior. Isso verifica L2=−HL, sem introduzir conexão independente.

Como c=tC, v=∇g c tem expansão tB+t²l+t³l2+… . A curvatura é Rbar+Dbar(Γ−Γbar)+(Γ−Γbar)², e contrair seus dois índices exteriores com c fornece

\[
\Omega=t^2O+t^3r+t^4(r_2+l^2)+\cdots.
\]

Os fatores 1/2 são os da conversão de componentes antissimétricas em duas-formas. I_C respeita o produto exterior no sentido de substituir os geradores dx por C; essa conta não exige comutação com d_H.

Para τ=tr(vΩ)−tr(v³)/3, o coeficiente de t4 é

\[
\tau_4=\operatorname{tr}(Br+lO-B^2l)=F(L).
\]

Na quinta valência, o produto vΩ dá

\[
\operatorname{tr}(Br_2+B l^2+lr+l_2O).
\]

O cubo dividido por três dá

\[
\operatorname{tr}(B^2l_2+B l^2).
\]

Em cada conjunto de três termos cíclicos, mover um fator ímpar através dos outros dois gera sinal positivo. Logo o termo tr(B l²) se cancela e sobra

\[
\boxed{\tau_5=F(L_2)+\operatorname{tr}(lr)
=F(-HL)+I_C\operatorname{tr}(L\wedge\bar DL).}
\tag{R1}
\]

Não há fator 2 ou 3 restante diante de I_CJ2. A primeira parcela tem dois fatores h e três ghosts, assim como a segunda: ambas têm ghost3 e valência5.

Em W(g0)=0, tr(R²)=tr(W²) começa quadraticamente em h; após as quatro inserções c, A_P começa na valência6. Nos campos e ghosts em questão s=s0+t s1, sem termos sj≥2. Os coeficientes t4 e t5 de sτ=A_P são então precisamente

\[
s_0F(L)=-s_1\tau_3,\qquad
s_0\tau_5=-s_1F(L).
\tag{R2}
\]

O argumento só usa essa ausência de termos superiores no setor SEM antifields. Não autoriza concluir sj≥2=0 na álgebra BV completa.

## 3. Contraexemplo (11–12): segundo jato admissível e sinal

O bloco B espacial usado na nota tem tr(B³)=6xyz. Todas as seis trajetórias de três índices distintos dão +xyz: as permutações dos geradores ímpares compensam os sinais antissimétricos da matriz. Assim τ3=−2xyz quando somente C0=θ tem valor não nulo.

É importante que os jatos não sejam escolhidos como uma matriz de conexão livre. Eles podem ser realizados por um ghost em coordenadas normais Xμ centradas no ponto, por exemplo pelos termos polinomiais

\[
\begin{aligned}
C^0&=\theta,\\
C^1&=xX^2-zX^3+\zeta X^0X^2,\\
C^2&=-xX^1+yX^3-\zeta X^0X^1,\\
C^3&=zX^1-yX^2.
\end{aligned}
\tag{R3}
\]

x,y,z,θ,ζ são os geradores ímpares, e X são coordenadas pares. As derivadas parciais mistas de (R3) comutam. No ponto Γbar=0, seus primeiros jatos dão exatamente B da fonte. O segundo jato realiza ∂0x=ζ, com o correspondente ∂0B21=−ζ. Ao passar a jatos covariantes, ∂Γbar·C acrescenta termos proporcionais a θ; multiplicá-los pelo θ externo no termo de transporte os anula. Termos de curvatura com dois valores C também são zero. Isso basta para o coeficiente θζyz que detecta o defeito.

Na variação de τ3, a parcela tr(BΩ0) não contribui: Ω0=0 nesse teste e s1C(p)=C0B·0=0, logo s1Ω0(p)=0. Para o cubo,

\[
s_1\tau_3=-\operatorname{tr}[(s_1B)B^2]
=\operatorname{tr}(B^4)
-\theta\operatorname{tr}[(\partial_0B)B^2].
\]

O traço B4 é zero: mover o primeiro B ímpar através dos outros três muda o sinal. A derivada PAR de tr(B³)=6xyz dá

\[
3\operatorname{tr}[(\partial_0B)B^2]=6\zeta yz.
\]

Portanto s1τ3=−2θζyz e, por (R2), s0F(L)=+2θζyz. Os sinais da equação (12) conferem. O teste não impõe Killing em todos os jatos; se impusesse, perderia justamente o segundo jato independente necessário para testar o fechamento universal.

Assim o pacote (F(L),τ5) satisfaz a segunda condição do sistema079, mas falha a primeira. A identidade de completamento não produz, por si, um elemento de 𝒦 que comece na valência4.

## 4. Diferença das transgressões e primitiva explícita

Defina u=S⁻¹sS. Por s²=0 e s(S⁻¹)=−S⁻¹(sS)S⁻¹,

\[
su=-u^2.
\]

Com k=S(v−u)S⁻¹ e Ωort=SΩS⁻¹, os fatores S desaparecem dos traços. Expandir as cúbicas dá

\[
\tau_{\rm ort}-\tau_{\rm GL}
=-\operatorname{tr}(u\Omega)
+\operatorname{tr}(v^2u)-\operatorname{tr}(vu^2)
+\tfrac13\operatorname{tr}(u^3).
\]

Substituir Ω=sv+v² cancela tr(uv²) contra tr(v²u). O restante é

\[
-\operatorname{tr}(u,sv)-\operatorname{tr}(u^2v)
+\tfrac13\operatorname{tr}(u^3)
=s\operatorname{tr}(uv)+\tfrac13\operatorname{tr}(u^3).
\tag{R4}
\]

O sinal negativo em s(uv)=(su)v−u(sv) é essencial. A expressão coincide com a equação (14) da fonte.

Para Sρ=(1+ρtH)^(1/2), mantenha s fixo, defina aρ=Sρ⁻¹∂ρSρ e uρ=Sρ⁻¹sSρ. Diferenciar os produtos, usando ∂ρSρ=Sρaρ, fornece

\[
\partial_\rho u_\rho=s a_\rho+u_\rho a_\rho-a_\rho u_\rho,
\qquad s u_\rho=-u_\rho^2.
\]

Como uρ é ímpar, s(uρ²)=−uρ³+uρ³=0. Na derivada par de tr(uρ³), os três termos cíclicos têm sinal positivo. O traço [uρ,aρ]uρ² é zero, pois aρ é par. Segue

\[
\partial_\rho\operatorname{tr}(u_\rho^3)
=3\operatorname{tr}[(s a_\rho)u_\rho^2]
=3s\operatorname{tr}(a_\rho u_\rho^2).
\tag{R5}
\]

S0=1 implica u0=0. Integrar (R5) e inserir em (R4) verifica exatamente a primitiva da equação (17):

\[
\boxed{\tau_{\rm ort}-\tau_{\rm GL}
=s\left[\operatorname{tr}(uv)
+\int_0^1\operatorname{tr}(a_\rho u_\rho^2)\,d\rho\right].}
\tag{R6}
\]

Esta prova não afirma que g0+ρt h tenha para cada ρ a transformação BRST do g final. A fonte distingue isso corretamente: Sρ é uma família auxiliar de matrizes na mesma álgebra diferencial.

## 5. Domínio formal, naturalidade e anéis

A raiz S e sua inversa são séries binomiais junto à identidade. Em uma potência fixa de t só entram finitos termos, cada um polinomial em ρ. Logo a integração de (R6) se faz coeficiente a coeficiente e introduz somente denominadores inteiros não nulos. A classe de coeficientes já é real/racionalizada para essas operações. Nenhuma divisão por curvatura, por gradiente de φ0 ou por símbolo diferencial é necessária.

Cada coeficiente permanece de ordem finita nos jatos; a raiz usa H, e sH introduz derivadas já permitidas do ghost e de h. A formalidade não é completada em valores arbitrários de todos os espectadores nem usada como avaliação em t numérico. A primitiva (R6) não é afirmada global para uma transformação S arbitrária distante da identidade, onde a cúbica de Maurer–Cartan poderia carregar topologia.

Os objetos transformam tensorialmente por conjugação sob mudanças independentes dos campos ativos; s atua trivialmente nas matrizes dessas mudanças. A diferença de Levi-Civita e as derivadas covariantes tornam a expressão natural. Isso não equivale a introduzir um ghost de frame Lorentz cru, nem a usar a homotopia074 sobre ele.

O anel permanece Rher do adendo079. Mesmo quando φ0 é constante, não se apagam seus parâmetros ou os acoplamentos herdados sem outro argumento. A fórmula é construída nesse anel, em vez de importar uma mudança de base cohomológica ou uma hipótese de planura.

Como s não diminui valência no fundo on-shell, truncar (R6) dá uma fronteira válida em C5. Isso sustenta a igualdade das CLASSES das duas transgressões, sem exigir a igualdade literal de B=∇barC com sua parte antissimétrica. Consequentemente a versão GL conserva a limitação da classe específica078. Não modifica o espaço de outras classes que poderiam diferir por um elemento de 𝒦.

## 6. Proveniência da cópia limpa e o que foi medido

O recibo desta revisão lê os bytes dos dois writers e confirma: o histórico contém exatamente um NUL; a cópia limpa contém zero; retirar aquele byte do histórico produz exatamente a cópia, sem qualquer outra diferença. O AST do histórico é recusado com a mensagem de NUL, e o AST da cópia é válido. Nenhum deles é executado nesta revisão.

A expressão NOTE do writer limpo contém um literal de texto seguido da normalização explícita .replace('\\x00',''). O helper desta revisão aceita somente essa forma AST, extrai o literal e os dois argumentos por ast.literal_eval, exige os argumentos byte NUL e string vazia e realiza essa única substituição na string local. Não avalia código arbitrário. O resultado codificado em UTF-8 coincide byte a byte com a nota examinada. Essa verificação não chama funções do writer nem materializa os seus arquivos novamente. Os pins da nota, do writer limpo, do helper e do writer histórico conferem com manifesto/proveniência; os seis pins de fontes registrados também conferem com os arquivos atualmente lidos.

O helper de limpeza cria um destino exclusivo, verifica os bytes, preserva a fonte e escreve uma proveniência separada. O writer limpo usa a mesma política de escrita exclusiva com temporário verificado. Sua leitura de pins antes/depois envolve a emissão da nota. Não altera as fontes que usa.

A afirmação histórica de que o writer inválido não chegou a ser executado é conservada como [DECLARADO — proveniência da criação]. A sua invalidade sintática é [REAL — reproduzida por AST sem execução]. Os bytes sozinhos não reconstituem todo o histórico de processos; por isso não converto a declaração de não execução histórica em uma observação independente minha. Tampouco escondo a falha para chamar a primeira tentativa de sucesso.

Nesta própria revisão, o primeiro helper documental tentou ast.literal_eval diretamente sobre a expressão NOTE completa e parou com ValueError por ela ser uma chamada .replace. A falha ocorreu antes de emitir o parecer final ou o recibo. O helper inicial e o rascunho foram preservados; uma cópia nova estritamente limitada ao padrão AST acima e um novo rascunho corrigem o procedimento. A proveniência dessa correção é registrada separadamente. Não se registra a primeira tentativa como sucesso.

As doze fontes sob revisão são medidas novamente ao fechar o recibo. As verificações são documentais, não testes formais Lean nem novos controles CAS. A consulta à fonte primária é uma verificação de referência, não uma certificação por seus autores da construção079.

## 7. Veredito e obrigações que permanecem

[DERIVED — revisão própria] As equações (7–10), (12), (14–18) da nota são consistentes com a expansão e a álgebra graduada verificadas aqui. O completamento particular de J2 e a equivalência formal GL–ortogonal estão sustentados no domínio declarado.

[OPEN] Permanece a busca por OUTROS b4 s0-fechados, Q e R com antifields que satisfaçam todas as equações do sistema079 e realizem −[A6] em δ(𝒦). A ausência de antifields neste pacote não os elimina da busca geral. Não se decide a cohomologia completada, estabilização de imagens, lim¹, anomalia efetiva, QME ou UV.

Este parecer não reexecuta o certificado078, não incorpora resultados080 e não representa uma aprovação em nome do operador ou de outro agente. Seu objeto é exclusivamente a construção GL–ortogonal079 e a proveniência documental examinada.
