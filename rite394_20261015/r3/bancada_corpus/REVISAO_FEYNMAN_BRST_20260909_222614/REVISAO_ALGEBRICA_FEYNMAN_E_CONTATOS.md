# Revisão algébrica do inverso Feynman BRST e dos contatos

09/09/2026. [DERIVED — análise escrita desta sessão]. Leitura do adendo `ADENDO_FEYNMAN_PARIDADE_E_CONTATOS.md` e das definições da nota principal `EXTENSAO_BRST_E_CORRECOES_SUAVES.md`. Não houve nova execução CAS/Lean ou alteração de fontes. Esta revisão verifica a composição algébrica tomando a existência e as propriedades das covariâncias W_D± e W_Q± da nota principal como entradas; não repete aqui a demonstração analítica de construção dessas covariâncias.

## 1. Normalização e sinal

Com P_u=−(∂²+ω²), E=G_ret−G_adv=−sin(ωτ)/ω e W⁺=ħ exp(−iωτ)/(2ω), temos W⁺−W⁻=iħE. A definição G_F=G_ret−iW⁻/ħ dá explicitamente

\[
G_F(\tau)=-\frac{i}{2\omega}e^{-i\omega|\tau|}.
\]

Sua derivada tem salto −1 em τ=0; como P_u começa por −∂², segue P_uG_F=δ. Portanto ε=iħ, o sinal −i/ħ na correção do Green e T=iħG_F são mutuamente consistentes. A verificação não depende de trocar informalmente convenções de outra referência.

## 2. Paridade e inversão matricial

Na ordem (u,b,c,bar c), a matriz Z=diag(+,+,−,−) comuta com L e anticomuta com γ. Nas covariâncias do adendo, as únicas entradas ghost ligam graus opostos; nesse suporte matricial Z implementa a paridade de troca. A relação correta é Λ⁺−ZΛ⁻=iħE_L.

Como γΛ⁻=−Λ⁻γ*, temos γ(ZΛ⁻)=ZΛ⁻γ*. Isso preserva a Ward na combinação

\[
G_L^F=G_L^{\rm ret}-\frac{i}{\hbar}Z\Lambda_L^-
=G_L^{\rm adv}-\frac{i}{\hbar}\Lambda_L^+.
\]

As duas apresentações coincidem porque Λ⁺−ZΛ⁻=iħ(G_ret−G_adv). A parcela de covariância é bisolução, logo a inversão de L é preservada em ambas as entradas. Nos blocos explícitos,

\[
G_L^F=\begin{pmatrix}
G_D^F&KG_Q^F&0&0\\
G_Q^FK^*&0&0&0\\
0&0&0&G_Q^F\\
0&0&G_Q^F&0
\end{pmatrix}.
\]

Conferi diretamente os blocos não triviais: H G_D^F+C*G_Q^FK*=I; C G_D^F−ℓ⁻¹G_Q^FK*=0; CKG_Q^F=I; HKG_Q^F=0. As identidades pela direita seguem das Ward na outra entrada. Nos ghosts, QG_Q^F=G_Q^FQ=I. Assim L G_L^F=G_L^F L=I. A multiplicação por γ e γ* produz nas duas ordens somente os blocos (1,4)=KG_Q^F e (4,1)=G_Q^FK*: γG_L^F=G_L^Fγ*.

## 3. Ordenação temporal e derivadas mistas

Fora de tempos coincidentes, T=Θ(τ)Λ⁺+Θ(−τ)ZΛ⁻=iħG_L^F. A definição pelo inverso em distribuições é necessária para fixar os contatos, e foi fornecida pelo adendo.

Há uma justificativa adicional para ΘE_L=G_L^ret nos blocos exibidos. Os propagadores causais de D e Q são de segunda ordem de onda, portanto sua restrição a tempos iguais vale zero. Para um operador de primeira ordem K, os termos de fronteira de K(ΘE_Q) são proporcionais a δ(τ)E_Q|_{τ=0}=0. O mesmo vale na outra entrada. Isso cobre os blocos mistos KG_Q e G_QK*. A condição característica de frente de onda permite a multiplicação por Θ(τ): sua conormal é temporal, enquanto a frente causal é nula. A diferenciação repetida, porém, não pode ignorar o primeiro salto de derivada.

**Contato misto exato a destacar.** As Ward fornecidas implicam

\[
\ell C G_D^F=G_Q^FK^*,\qquad K^*C^*=Q,
\qquad \ell^2 C G_D^F C^*=\ell I.
\tag{1}
\]

Já para as bisoluções, ℓ² C W_D± C*=0, pois W_Q±Q=0. Assim o bloco auxiliar b–b das covariâncias e de G_L^F é zero, mas a aplicação de C nas duas entradas do propagador u–u contém o contato

\[
\ell^2 C(i\hbar G_D^F)C^*=i\hbar\ell I.
\tag{2}
\]

O complemento de Schur é precisamente ℓ² C G_D^F C*−ℓI=0: o contato é subtraído ao formar o bloco b–b. Isso confere que a entrada zero não foi obtida omitindo a contribuição na diagonal.

Um controle escalar mostra o mesmo fenômeno: T_u=ħ exp(−iω|t−t′|)/(2ω) satisfaz

\[
\partial_t\partial_{t'}T_u=\omega^2T_u+i\hbar\delta(t-t').
\]

A ordenação temporal das duas derivadas de campo, calculada separadamente em tempos distintos, daria somente ω²T_u; o contato surge quando as derivadas atingem a ordenação. Uma extensão que identificasse essas operações sem o termo delta seria incorreta. As fórmulas do adendo, particularmente suas Ward e o complemento de Schur da nota principal, já contêm a correção necessária.

## 4. Frente de onda e alcance

A relação nula fora da diagonal, com covariável temporal negativa na primeira entrada para t>t′ e positiva para t<t′, coincide com a fase exp(−ipη) usada no estado físico. A conormal da diagonal é necessária ao inverso, pois L G_F=I. Diferenciações locais por K ou K* não criam relações canônicas adicionais. Isso confere a inclusão microlocal afirmada, sob o contrato Hadamard da nota principal.

**Resultado desta revisão:** não encontrei erro material nos sinais, paridade, inversão, contatos ou Ward do adendo. Ele fornece um inverso Feynman livre do sistema completo, tomando os pares Hadamard construídos na nota principal como entrada. O resultado não constrói produtos temporais superiores nas diagonais e não paga a QME interagente, as anomalias de renormalização ou a conclusão UV. Essas limitações estão corretamente expostas na fonte.
