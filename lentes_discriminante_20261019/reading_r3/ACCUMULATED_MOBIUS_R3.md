# Ao lado: degenerescência recíproca das distâncias de atraso — R3

19/10/2026 · [DERIVED analítico, sem nova execução]. Complemento de ACCUMULATED_MAP_R3.md; mesma hipótese adicional de geometria FLRW óptica plana, χ crescente, 0<zl<zs. Identidade sugerida pela coordenação e derivada abaixo. Não é transformação da folha de massa, nem prova de que a D1b seja exatamente fracionária-linear.

## 1. Identidade exata e domínio

D_Δt=χlχs/(χs−χl) implica **1/D_Δt=1/χl−1/χs**.

Considere constantes a>0 e b com a+bχ(z)>0 em todo o intervalo analisado, e

χ̃(z)=χ(z)/(a+bχ(z)).

A transformação preserva χ̃(0)=0 e a ordem, pois dχ̃/dχ=a/(a+bχ)²>0. Como 1/χ̃=a/χ+b,

1/D̃_Δt=a(1/χl−1/χs), portanto **D̃_Δt=D_Δt/a**, para TODOS os pares de redshifts no domínio.

O parâmetro b desaparece exatamente; a é escala comum degenerada com H0 quando livre. Para a=1, todos os D_Δt são idênticos apesar de χ̃≠χ. Isto é uma não unicidade da geometria quando o dado é **somente a distância de atraso**; não é invariância automaticamente de uma likelihood de lente completa, que também reconstrói o potencial. As distâncias angulares individuais, cinemática, réguas externas e outras observações podem responder à transformação.

Se χ'=c/H(z), a curva transformada corresponde matematicamente a H̃(z)=H(z)(a+bχ(z))²/a>0. Isso a torna uma geometria óptica plana candidata, mas não demonstra que pertença à família cosmológica TGL/ΛCDM ou que satisfaça suas equações de campo. Restringir H a uma família física pode quebrar essa liberdade; é preciso verificar a restrição, não supor que qualquer b seja permitido.

## 2. Por que a primeira correção acumulada pode sumir nos atrasos

Após absorver K* em H0_tilde, use L=c/H0_tilde, χbg=L I(z), χA=L J(z), E(0)=1 e e1=E'(0), com E suficientemente suave. A expansão local dá

I(z)=z−e1 z²/2+O(z³),
J(z)=z+(ν−1)e1 z²/2+O(z³),
J−I=(ν e1/2)I²+O(I³).

Logo χA=χbg+kχbg²+O(χbg³), k=ν e1/(2L). A transformação recíproca com a=1,b=−k tem precisamente χ/(1−kχ)=χ+kχ²+O(χ³). Assim o termo quadrático inicial da leitura acumulada pertence à direção invisível dos D_Δt. De modo equivalente, 1/χA=1/χbg−k+O(χbg), e a constante −k cancela entre lente e fonte.

Isto não exige tratar ν como infinitesimal para identificar o coeficiente de z²; a expansão é em redshift/distância. Alternativamente, uma variação infinitesimal δχ=kχ² satisfaz δ(1/D_Δt)=−δχl/χl²+δχs/χs²=−k+k=0 em primeira ordem. Termos superiores ou desvios da forma recíproca podem sobreviver.

**Limite importante:** a coincidência de um termo de Taylor não prova χA=χbg/(a+bχbg) no intervalo inteiro. Não prova residual zero da D1b em redshifts finitos e não autoriza reduzir covariância/erro para obter significância. Explica por que endpoint ou diferença de distância isolada não mede diretamente a resposta do atraso. O cálculo novo da coordenação deve integrar J_ls e perfilar H0/Ωm, como já previsto; este complemento não executa ou antecipa seus resultados.
