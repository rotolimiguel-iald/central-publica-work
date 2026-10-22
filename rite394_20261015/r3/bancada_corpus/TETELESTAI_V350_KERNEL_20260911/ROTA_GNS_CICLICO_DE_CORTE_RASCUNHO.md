# GNS cíclico dos funcionais de corte — DEV posterior

[REAL — compilado na cópia; não revisado independentemente nem integrado]
Quatro módulos, 26 declarações auditadas pelo trio de axiomas padrão:
ScalarCutVacuum (4), ScalarCutCyclicSpace (13),
ScalarCutVectorFunctional (2), ScalarCutGNSProperties (7).
Pins e logs finais são lidos pelo registro de desenvolvimento.

No mesmo ambiente L²(ℝ,K), construiu-se Ω_R=√c·1_(-R,R]η,
com c=(2π)⁻¹. É vetor de medida finita, não uma função constante
não nula sobre toda a reta. Não foi normalizado como estado.
Para R≥0 e todo A em B(K), ⟨Ω_R,ρ(A)Ω_R⟩=ψ_R(A).
A integral orientada só é identificada com (-R,R] quando R≥0.

Γ_R(B)=ρ(B)Ω_R é complexo-linear em B∈N. Seu fecho de imagem
é o Hilbert H_R. A representação π_R é a restrição da mesma ρ
a esse subespaço redutor; Ω_R tem representante em H_R, e
π_R(N)Ω_R tem imagem densa ali. Para B∈N e R≥0,
‖Γ_R(B)‖²=Re ψ_R(B*B). Isso identifica a seminorma GNS de ψ_R
no espaço construído, incluindo a possibilidade de núcleo.

Os mapas anteriormente construídos chegam agora a H_R:
T_R:H_I→H_R, contrações com T_RΛ(A)=Γ_R(A) para A∈I e
T_Rπ_I(B)=π_R(B)T_R. T_n v=0 para todo natural n implica v=0.
Cada T_R tem imagem densa em H_R; não se afirma sobrejetividade,
injetividade individual ou fidelidade de ψ_R.

A densidade é provada usando B X_h, X_h a mesma média regular
contrativa que converge fortemente para 1. Para h>0, B X_h∈I.
O limite forte uniformemente limitado passa para ρ e então
para o subtipo H_R; a norma Hilbert fecha a imagem. Não se
troca densidade forte em N por densidade Hilbert sem essa ponte.
Ω_R também foi colocado no fecho da imagem ambiente de T_R.

R arbitrário é permitido nas construções de espaços/mapas.
Para R≤0 o intervalo pode ser vazio e o espaço pode ser zero;
não se exige vetor não nulo nem fidelidade nesses casos.
As identidades positivas do funcional são afirmadas com R≥0.

[OPEN] Ciclicidade não implica a propriedade separante. Não foram
provadas fidelidade ou normalidade de π_R, a propriedade separante
de Ω_R, ou fechabilidade de sua involução. Não se conclui
(0,y)∈fecho(G_Tomita)⇒T_n y=0. Essa estimativa de separação
continua necessária antes de usar a injetividade conjunta.

[REAL — tentativas corrigidas] ScalarCutVacuum exigiu explicitar
o ponto 0 em nhdsGT_le_nhdsNE. ScalarCutCyclicSpace exigiu uma
função explícita para evitar timeout de coerção e a preimagem
de isClosed_closure. ScalarCutGNSProperties teve correção de
sintaxe na estimativa de norma. Logs rc1 foram preservados;
só os rc0 das fontes finais entram no registro aceito.

A ponte com o domínio escalar máximo não exige presumir I=n_ν.
[Precisão e pesquisa externa](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/PESQUISA_FECHABILIDADE_PESOS_20260912.md>)
registra essa distinção. A leitura bibliográfica não gerou axioma
ou quitação de Tomita/KMS/traço. O parecer anterior sobre mapas
ambientes não cobre estes quatro módulos ou estas 26 declarações.
Gate, H1–H3, setor interagente e runtime seguem abertos.
