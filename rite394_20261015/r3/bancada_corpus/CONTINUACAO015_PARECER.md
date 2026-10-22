[REAL / INPUT / OPEN] Continuação 015 — fluxo geodésico local e preservação da nulidade

06/09/2026. Trabalho espontâneo posterior à entrega 014, sob o objetivo amplo iniciado na ordem 007. A entrega 014 foi reconferida no início da sessão. O turno anterior foi progresso, e o objetivo amplo permanece ativo.

## Resultado

[REAL] Foi construído um fluxo local de geodésicas no espaço de fases, com dados iniciais variáveis, continuidade conjunta e suavidade no tempo de cada solução. O fluxo conserva exatamente \(g(v,v)\). Portanto todo dado inicialmente nulo, dentro do domínio local, permanece nulo.

O resultado `local_levi_civita_null_geodesics` recebe uma solda suave invertível \(g=E^T\eta E\), um ponto x no aberto U e uma velocidade v≠0. Ele produz uma família F num produto de bola de dados iniciais e intervalo aberto de tempo. Para cada dado q nessa bola:
\[
F(q,0)=q,\qquad
\frac{d}{dt}F(q,t)=\mathcal G_\Gamma(F(q,t)),
\]
onde
\[
\mathcal G_\Gamma(x,v)=\bigl(v,-\Gamma_x(v,v)\bigr).
\]
A posição permanece em U e a velocidade permanece não nula. Se \(g_{q_x}(q_v,q_v)=0\), então a energia é zero durante todo o intervalo construído. O resultado não recebe um campo espacial V nem uma curva geodésica previamente escolhida.

[INPUT] Suavidade da solda, inversas E,D, aberto U e dimensão/assinatura \((1,3)\) continuam nos dados. A família é local. Não se deduz a métrica de um estado quântico.

## Como a construção fecha

`geodesic_spray_smooth` prova a suavidade do campo de fase por somas finitas e produtos das componentes da conexão e da velocidade. `geodesic_spray_c1` permite obter os parâmetros locais de Picard–Lindelöf.

`localPhaseFlow` aplica o teorema da mathlib que fornece um fluxo conjuntamente contínuo. Um argumento de vizinhanças restringe a solução a um produto de bola aberta nos dados iniciais e intervalo aberto em torno de zero. A mesma restrição mantém a solução dentro de qualquer aberto Q que contenha o dado inicial. Para `localGeodesicFlow`, escolhemos \(Q=\{(x,v):x\in U,\ v\ne0\}\).

O contrato `LocalPhaseFlow` contém explicitamente raio positivo, mapa de fluxo, condição inicial, derivada efetiva, permanência em Q e continuidade conjunta. As duas projeções da derivada dão \(x'=v\) e \(v'=-\Gamma(v,v)\). Essas equações são conclusões da construção de ODE, não campos recebidos sem testemunho.

A conservação é provada por diferenciação:
\[
\frac d{dt}g(v,v)
=g(v',v)+(\partial_vg)(v,v)+g(v,v').
\]
Com \(L=\sum_i v^i\Gamma_i\), a compatibilidade métrica fornece \(\partial_vg=L^Tg+gL\), e a ODE fornece \(v'=-Lv\). `geodesic_energy_algebra` verifica o cancelamento dos termos. `geodesic_energy_derivative` liga esse cálculo às derivadas efetivas. A derivada zero num intervalo conexo implica a conservação em `geodesic_flow_energy_conserved`, seguida de `geodesic_flow_null_preserved`.

A especialização a Levi-Civita usa as provas anteriores de suavidade da conexão e compatibilidade da métrica soldada. `leviCivitaGeodesicFlow` escolhe o fluxo; o teorema final reúne a preservação da nulidade para todos os dados inicialmente nulos próximos.

## Regularidade provada e regularidade ainda faltante

[REAL] `geodesic_flow_smooth_Icc` aplica a regularidade de soluções da mathlib a cada intervalo fechado interno ao domínio. `geodesic_flow_smooth_time` passa à suavidade \(C^\infty\) no intervalo aberto inteiro. Posição e velocidade são suaves no tempo. `phase_flow_jointly_continuous_at` fornece continuidade conjunta em todo o produto aberto construído.

[OPEN] Isso ainda não prova suavidade em relação aos dados iniciais. A busca nos diretórios locais Analysis e Geometry não localizou um teorema pronto de suavidade conjunta do fluxo; essa observação não afirma inexistência absoluta de tal resultado na biblioteca.

Para alimentar diretamente a tela da entrega 014, ainda é preciso construir:
1. uma hipersuperfície transversal e uma escolha suave de velocidades nulas iniciais;
2. suavidade conjunta da família de geodésicas;
3. invertibilidade local da projeção \((s,t)\mapsto x_s(t)\);
4. o campo \(V(x_s(t))=v_s(t)\), com suavidade, nulidade e geodesicidade;
5. controle do primeiro jato inicial para a condição de equilíbrio exigida no contrato de horizonte.

A prova desta etapa não produz `GeometricScreenAlong` ou `GeometricHorizonPencil` adicionais. Ela constrói a família geodésica que antecede essa passagem.

## Controles e negativo exato

[REAL] No caso Γ=0, `zero_connection_velocity_constant` e `zero_connection_position_affine` provam, para o fluxo efetivamente construído:
\[
F((x,v),t)=(x+tv,v).
\]
`flat_geodesic_flow_control` fornece o habitante correspondente para qualquer velocidade inicial não nula.

No caso curvo de 014, \(g=e^{2x^0}\eta\), a conexão explícita e o dado inicial \((0,k)\), com \(k=(1,1,0,0)\), dão
\[
v'(0)=-2k\ne0.
\]
`curved_null_geodesic_flow_control` constrói o fluxo e prova a preservação da nulidade e essa derivada inicial. `curved_flow_background_nonzero` reutiliza a componente de curvatura igual a 1 já verificada em 014. Essa última declaração é uma reutilização explícita, não uma nova descoberta de curvatura.

`phase_flow_cannot_assign_one_field` prova um limite da identificação de tipos: nenhum único campo V pode representar as velocidades iniciais da família completa de fase sobre uma bola aberta. Há dados iniciais com a mesma posição e velocidades distintas. O controle constrói uma perturbação da componente zero da velocidade, de tamanho raio/2, e aplica a condição inicial do fluxo.

Esse negativo não proíbe congruências geodésicas. Ele mostra por que a seleção transversal dos dados iniciais é necessária. Também não afirma que a família inteira usada nesse controle é nula; o fluxo está definido numa bola de fase, e a preservação da nulidade vale no subconjunto de dados inicialmente nulos.

## Evidência e custódia

[REAL] Contagem lida dos fontes: cinco módulos, 29 declarações de teoremas e três definições com axiomas impressos separadamente. Uma das 29 declarações reutiliza a componente de curvatura de 014, conforme indicado acima. Definições auxiliares também constam no inventário. Todos os teoremas têm `#print axioms`.

As cinco compilações finais estão limpas, com dependências impressas restritas a `propext`, `Classical.choice` e `Quot.sound`. O auditor recusa manifesto se faltar uma compilação limpa da fonte exata, se houver erro/aviso ou `sorryAx`, se faltar cobertura de impressão ou se os bytes históricos não estiverem preservados. O último módulo importa a árvore nova inteira e os controles da entrega 014.

A entrega no túnel inclui os resultados medidos desse auditor, os caminhos absolutos, os hashes dos bytes e os comandos de reprodução. Logs de tentativas com defeitos são conservados, inclusive erros de elaboração de somas, intervalos e instâncias de derivação. Revisões próprias têm backups imediatos dos bytes. Fontes e binários locais importados são fixados; Lean 4.31.0/mathlib permanecem dependências externas locais. Isto não é uma recompilação independente integral nem um pacote portátil.

Conferência de custódia, somente leitura após o manifesto:

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation015.py'
```

## Reconstrução gravitacional geral

[KNOWN] A construção de Jacobson usa horizontes locais de equilíbrio e assume a proporcionalidade entre entropia e área e a relação de Clausius. Ela não fornece, por si só, a identificação microscópica desses dados: [Thermodynamics of Spacetime, 1995](https://arxiv.org/html/gr-qc/9504004).

[OPEN] O fluxo geodésico preservando nulidade é um avanço geométrico. Congruência suave no espaço-tempo, superfície/horizonte imerso, equilíbrio, entropia–área microscópica, coeficiente físico, corrente de calor, Clausius/H3, ponte modular, seleção de assinatura/dimensão e globalização permanecem no objetivo. Não há prova da gravidade quântica geral nesta entrega.

Toda escrita ocorreu em `C:\IALD\Central de Patentes\Chatgpt`. `um.py` não foi executado, importado nem alterado. Acervo original, kernel canônico, Atlas, memórias, selos e gate continuam intocados. Auditoria adversarial da gerência permanece pendente.
