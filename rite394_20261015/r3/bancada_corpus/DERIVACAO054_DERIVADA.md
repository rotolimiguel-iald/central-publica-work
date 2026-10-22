# Derivação054 — adendo anterior ao módulo da derivada efetiva
[DERIVED — registrado antes de implementar o quarto módulo]
O plano054 ganha ModularCostDerivative.lean, após os três módulos inicialmente listados. A identidade série/log não basta para chamar o custo de resposta de uma curva; este módulo visa ligar os mesmos coeficientes à curva unitária efetiva.

Para A autoadjunto limitado, U(t)=exp(itA), f_B(t)=Re ω(U(t)* B U(t)).
A derivada no zero é Re iω(BA−AB). A segunda derivada é
    f_B''(0)=Re ω(−A²B+2ABA−BA²).
Isso segue diferenciando a exponencial e os produtos, não de uma definição escolhida para a derivada.

No prefixo finito fiel, B=K_N=diag(−log wi) e A=towerPi(a), a=a*. A primeira derivada é zero porque ρ_N comuta com K_N. A soma matricial fornece
    f_K''(0)=Σij(wi−wj)(log wi−log wj)|aij|²=2 C_D(aΩ).
O cálculo usa a conjugação de entradas da autoadjunção e a troca i↔j no somatório finito. A resposta quadrática é do mesmo D global e da mesma curva U.

Alvo: derivadas efetivas e igualdade com o custo local. Se um limite dividido por t² for afirmado, será provado pelo Taylor/limite pertinente; não trocar segunda derivada por coeficiente sem fator2. A identificação com entropia relativa quântica continua distinguida da expressão energética finita, caso a primeira não seja objeto formalizado no módulo.

A inclusão não deriva H3: B é o observável modular do corte, não constructedHeat. Não se postula uma matriz densidade trace-class global, um logΔ global nem área física. As guardas da derivação principal continuam.

Registro UTC: 2026-09-07T06:15:11.675682+00:00
