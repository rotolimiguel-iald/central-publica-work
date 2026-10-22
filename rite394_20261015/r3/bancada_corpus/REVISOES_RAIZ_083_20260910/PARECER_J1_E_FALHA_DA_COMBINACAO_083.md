# Revisão da raiz083 — derivada covariante e falha da combinação

10/09/2026. [DERIVED — revisão matemática escrita] [REAL — fontes lidas e medidas]. A raiz leu integralmente as duas notas083, o script/recibo de J1 e os dois pareceres independentes. Não detectou erro material no domínio declarado. Esta revisão não reexecuta os dez predicados nem se apresenta como compilação Lean.

Na equação de onda, refiz a contração g0^{ef}[∇f,∇c]Wabde. As parcelas dos índices a,b são K(Wcbda+Wacdb); as dos índices d,e somam −2KWabcd. Os traços desaparecem e Bianchi dá Wcbda+Wacdb=−Wabcd, total −3KW. A segunda dupla fornece o mesmo valor. Assim □W=6KW no shell Einstein linear, com a convenção +--- e z espacial. Isso não é a identidade off-shell usada para s0: o fechamento s0W1=0 vem separadamente da naturalidade e W0=0.

O J1 é g0^{ef}tr(∇eW1∧∇fW1)/vol_g0, igual a metade da contração com o dual de Hodge. A derivada atua nos quatro slots. Conferi a conexão conforme e o peso W_abcd=a²Wtilde_abcd: N_e contém ∂eWtilde, 2w_eWtilde e quatro parcelas −Γ. A contração final tem fator a^-6. A derivada temporal do Weyl é conservada pela rotação em todos os índices; somente o pseudoscalar fica independente de τ, pelo pullback helicoidal que preserva g0 e h. As conexões e=1,2 continuam no código, mesmo quando as derivadas ordinárias são zero.

Li o script: aritmética Fraction/Laurent nova, sem importação das fontes antigas, derivada Dz=∂z+p∂f+(2p/z−k²f)∂p a ℓ,k fixos. A comparação covariante direta versus □J/2−6KJ é exata antes dos dados pontuais. As duas rotas compartilham o Weyl e a EDO de entrada; não reconstroem independentemente toda a solução Einstein. Os dez predicados são os do recibo, não uma contagem de cada componente percorrido.

J1(p0)=80k/z0³−28k³/z0 e J1′(p0)=560k/z0⁴−352k³/z0²+8k⁵. Substituir em 6J1′/z0−18J1/z0² dá R1=48k⁵/z0−1608k³/z0³+1920k/z0⁵, e R1(2/z0)=−7488/z0⁶. O termo s0J1,3 da naturalidade é mantido até a avaliação por Killing. J1 tem paridade Grassmann par, embora seu valor nessa família seja ímpar em k; são duas classificações distintas. O fator κ² garante engenharia zero nesse candidato, sem decidir admissibilidade causal.

Na combinação Q=−Jβo/(12K)−q_grad/(28K), conferi a igualdade para todos os k:
−R/(12K)−(112k/z0³−56k³/z0)/(28K)=4k/z0,
usando K=1/z0² fixo. Nenhum coeficiente depende de k. A corrente horizontal tem a realização finita082 com s0q6, que se anula na avaliação adequada.

Refiz a parte invisível ao detector original. Com Mghost=antisym∇C e βo=−εppMghost/2, a invariância de ε e a ciclicidade graduada dão dβo=−εppMghost²/2−12Kν. No ponto, p=θ0e0+θ1e1 e Mghost=θ2J02+θ3J03, com boosts de entradas +1, resultam Mghost²=−θ23J23, (Mghost²)^23=−θ23 e εppMghost²=−4θ0123. Portanto ev(dβo)=+2θ0123.

Como verificação escrita independente do agrupamento covariante, as duas parcelas que diferenciam p contribuem +2θ0123 cada; a que diferencia M contribui −2θ0123. A soma é +2. As parcelas p³ e p⁴ se anulam nessa escolha, deixando ev(dQ+a)=−J/(6K)=2k/(3Kz0), que vale +4/3 em k=2/z0. A normalização do volume é a mesma: g0(p0)=η.

Os dados (valor, primeira derivada antissimétrica) são realizáveis por Killing locais na espaço-forma; seus jatos superiores não são livres. Não se supôs que os quatro escolhidos formassem subálgebra fechada: o diferencial CE é aplicado ANTES da restrição. Com o mesmo h TT on-shell numa vizinhança e antifields zero, a avaliação anula todas as fronteiras s0. A falha não pode ser reparada por Q→Q+s0χ ou por uma primitiva s0 do defeito.

O uso de 1/K é de um real fixo não nulo; não é uma conclusão em anel variável polinomial em K. O resultado exclui essa combinação, não toda a imagem CE. O detector original foi demonstrado insuficiente por um defeito explícito em sua anulação; isso não altera falsificadores físicos, H3 interno ou o gate.

Pareceres externos: [J1](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md>) e [combinação](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_COMBINACAO_ISOTROPIA_083_20260910_054522_9585399/PARECER_COMBINACAO_E_RESIDUO_ISOTROPIA_083.md>). A identidade de corrente082 da raiz possui seu parecer próprio, sem autoaprovação por esta revisão. Investigação084 excluída. Zero matemática reexecutada, Lean, um.py ou alteração de originais.
