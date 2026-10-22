# Parecer da raiz — translação normal074 e correção de frame

10/09/2026. [DERIVED — revisão matemática escrita, delimitada]. Li integralmente a nota TRANSLACAO_NORMAL_E_CURVATURA_BRST e seu adendo PRECISAO_FRAME_LOCAL_074, pinados no recibo. Conferi a entrada de jatos normais em Jentsch, Teoremas1–3, no PDF primário https://arxiv.org/pdf/1509.08269v1. Não se trata de compilação Lean nem de uma auditoria de todas as entradas anteriores da teoria.

**Conclusão: favorável para a apresentação métrica mínima após a correção explícita de alcance.** A referência B0 é inerte por s; a naturalidade considerada transporta conjuntamente campos e referência. A leitura antes ampliada aos ghosts Lorentz convencionais sob frames locais foi retirada no adendo e não é aceita neste parecer.

## Cálculo revisto

A inserção pelo pushforward dos campos constantes do espaço tangente via Exp_x usa um centro a cada ponto. Sua naturalidade segue da equivariância da exponencial. Ela é diferente de transporte paralelo radial e de uma derivação evolutiva que prolongasse c→dx com todos os jatos derivados nulos. Essa diferença aparece nos segundos jatos covariantes e quando a derivada horizontal move o centro.

Com [∇̄_μ,∇̄_ν]v^ρ=R̄^ρ_{σμν}v^σ, os coeficientes −1/3 da derivada normal de Γ e −1/6 da parte simetrizada dão a ação escrita sobre ∇̄²c. O defeito C_N=d_Hb_N−b_Nd_H sobre Z=∇̄c é −R̄: b_NZ=0 em todo ponto, mas b_Nd_HZ contém a antissimetrização da derivada da conexão. A curvatura não desaparece com Γ(x)=0.

O segundo comutador com s anula-se porque duas inserções no termo quadrático sc são o colchete dos campos constantes empurrados pela MESMA carta normal do centro escolhido. Esses campos comutam com todos os seus jatos. As outras regras métricas mínimas têm no máximo um ghost difeomórfico. Os coeficientes da inserção são s-inertes.

C_N e b_N só inserem ghosts, e aniquilam os coeficientes de fundo um do outro; daí [b_N,C_N]=0 e C_N²=0. O BCH é finito e fornece s+E_N+C_N. Separar os bidegraus da quadratura confirma {s,E_N}=0, E_N²=−{s,C_N} e {E_N,C_N}=0. Portanto não se pode usar E_N como diferencial na álgebra antes de passar à cohomologia de s.

No fundo g0=dr²−a²γ, a=2cos(r/2), as conexões escritas dão R̄^r_{irj}=aa''γij=−a²γij/4. Assim C_N(∇̄_i c^r)=a²γij dr∧dy^j/4 é não nulo no interior. Isso é um controle escrito do termo que a conjugação tem de conservar, não um coeficiente de anomalia física.

A recorrência sT_q+E_NT_(q−1)+C_NT_(q−2)=Ω_q é consistente: depois de resolver as etapas anteriores, a obstrução U_q é s-fechada pelas relações acima. A existência de sua primitiva natural continua um antecedente. A filtração finita não transforma esse antecedente em conclusão.

## Correção material identificada nesta revisão

Na convenção se=L_c e+λe, a mudança e'=A(x)e com sA=0 força λ'=AλA⁻¹−(c·∂A)A⁻¹. Logo b_Nλ=0 implica b_Nλ'=−dA A⁻¹ e não satisfaz a mesma receita no frame primado. Solicitei que essa ampliação fosse retirada por adendo; o autor o fez sem alterar a nota congelada.

A apresentação métrica efetiva de Q2 não contém esse ghost adicional e conserva o teorema. A combinação tensorial ϑ=λ−ι_cω̄ exigiria bλ=ω̄ para que bϑ=0; isso é outro operador. Seus comutadores não foram aceitos por analogia. A comparação formal métrica–vielbein anterior pode fornecer uma rota separada, com suas próprias hipóteses.

## Limites

A parte de completação da nota é compatível com o teorema Rees e seu parecer independente, lido nesta revisão: preservar R_L não é preservar uma truncagem t≤N sem margem. A construção geométrica conserva jatos finitos e regularidade de suas entradas. Isso não paga os grupos naturais de cohomologia, a descida, os contratermos por aridade, os contatos, a carga interagente ou QME.

Parecer aceito somente junto com o adendo de frame. Fontes preservadas; os controles automáticos do recibo medem integridade, não substituem esta análise.
