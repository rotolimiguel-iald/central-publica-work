[REAL / INPUT / OPEN] CONTINUAÇÃO 017 — suavidade conjunta do fluxo no domínio local

06/09/2026. Continuação espontânea de 016. O turno anterior e esta etapa produziram progresso formal. Permanecem somente as ordens gerenciais 001–007 no túnel. A auditoria independente segue a cargo da gerência; nenhuma declaração de gate.

## Resultado central

O teorema flow_smooth_on_domain prova, para um campo C∞ num aberto Q de um espaço de Banach real e um objeto LipschitzLocalFlow F desse campo:

\[
\Phi\in C^\infty\bigl(B(p,r)\times(-r,r),E\bigr),
\qquad r=F.radius.
\]

O raio é o do fluxo recebido. A conclusão vale para a mesma função e para todo o domínio aberto original; não é somente uma família de afirmações com raios decrescentes conforme a ordem da derivada.

O enunciado recebe as propriedades explícitas de LipschitzLocalFlow: condições iniciais, solução da ODE, permanência no domínio, continuidade conjunta e limite uniforme de Lipschitz nos dados. A construção desse objeto já foi provada em 016 para um campo suave. Não se recebe a suavidade do fluxo como hipótese.

A aplicação c1_geodesic_flow_smooth fortalece a regularidade da própria função c1GeodesicFlow definida em 016. O nome histórico da função foi preservado; o arquivo entregue anteriormente não foi editado.

## Prova e quantificadores

1. **Unicidade de escolhas locais.** flow_germ_eq_at_initial compara famílias que resolvem a mesma ODE e partem do mesmo dado. A suavidade de f fornece uma vizinhança de Lipschitz; a continuidade conjunta conserva as trajetórias nela por um intervalo comum. A unicidade da ODE dá igualdade das famílias numa vizinhança do dado e do tempo zero. Centros e domínios das duas construções podem ser diferentes.

2. **Indução por prolongamento variacional.** exists_finite_regular_flow é provado por indução em n, uniformemente quanto ao espaço de Banach. No passo sucessor, a hipótese indutiva é aplicada ao campo ampliado (f,Df∘J). As projeções Φ e J são Cn perto do dado inicial. A derivada efetiva demonstrada em 016,
   DΦ[h,τ]=Jh+τf(Φ), é então Cn. O critério contDiffAt_succ_iff_hasFDerivAt dá C(n+1). O caso n=0 usa continuidade numa vizinhança, não apenas continuidade no ponto.

3. **Uma única função em todas as ordens.** flow_finite_regular_at_initial transfere cada prova finita para qualquer fluxo recebido por igualdade local. flow_smooth_at_initial reúne todas as ordens. Até aqui, a conclusão é C∞ no ponto inicial no sentido preciso da mathlib; as vizinhanças podem depender de n.

4. **Propagação temporal.** flow_finite_regular_nearby_transfer constrói um fluxo Ψ centrado em Φ(q,T). Pela unicidade, para dados e tempos próximos,
   Φ(q′,s)=Ψ(Φ(q′,t₀),s−t₀).
   Essa identidade transporta regularidade de um tempo t₀ próximo para T. Para cada n finito, o conjunto dos tempos regulares é aberto. A identidade também mostra que todo ponto de seu fecho situado no intervalo original é regular. Como o intervalo é conexo e contém o tempo zero, todos os seus tempos são regulares.

5. **Domínio fixo.** flow_finite_regular_on_domain vale em todo B(p,r)×(-r,r) para cada n; flow_smooth_on_domain reúne essas afirmações no mesmo domínio. Não foi usada a interseção de bolas com raios decrescentes para fabricar um raio positivo.

O símbolo J nesta cadeia é o operador variacional flowVariation de 016. Não é uma identificação com a conjugação modular de Tomita.

## Arquivos e contagens medidas

| Módulo | Teoremas declarados | Definições impressas |
|---|---:|---:|
| FlowGermUniqueness | 1 | 0 |
| FlowRegularityInduction | 3 | 1 |
| FlowSmoothGerm | 3 | 0 |
| FlowTimePropagation | 4 | 0 |
| SmoothGeodesicFlow | 4 | 0 |
| SmoothFlowControls | 3 | 0 |
| Total | 18 | 1 |

As contagens são de declarações. A existência usa Picard/mathlib e a identificação do diferencial de 016; a nulidade, a solução plana e o fundo curvo reutilizam resultados de 014–016. Não se apresentam essas contagens como número de descobertas matemáticas novas.

Os seis módulos finais compilaram sem erros ou avisos. Todas as declarações impressas dependem apenas de propext, Classical.choice e Quot.sound, sem sorryAx. Hashes dos bytes, metadados, logs finais, backups e tentativas rejeitadas são fixados por audit_continuation017.py no manifesto.

## Consequência geométrica e controles

local_smooth_metric_null_geodesics produz um LocalPhaseFlow suave para uma conexão suave compatível com a métrica. local_smooth_levi_civita_null_geodesics instancia a construção para uma solda suave invertível e sua conexão de Levi-Civita. Para cada dado inicialmente nulo da bola, a nulidade persiste. A posição permanece no aberto e a velocidade permanece diferente de zero pelos campos do objeto construído.

Os controles foram recompilados conjuntamente:

- Campo nulo: existe um fluxo suave que permanece no dado inicial.
- Conexão nula: qualquer LocalPhaseFlow dessa conexão coincide, no seu domínio, com (x+t v,v). A suavidade foi conferida diretamente pela expressão polinomial, independentemente da indução variacional.
- Fundo conformal curvo de 014–015: o fluxo é conjuntamente C∞, preserva a nulidade da trajetória de controle e mantém a aceleração inicial já calculada, −2(1,1,0,0).

O caso curvo não supõe que o fundo seja plano nem transforma a aceleração num teste observacional.

## Obrigações restantes para a reconstrução

A dívida de regularidade C∞ nos dados iniciais e no tempo está paga para o fluxo local construído. Isso ainda não produz um campo de velocidades único no espaço-tempo: o fluxo vive no espaço de fases, cujos dados incluem posição e velocidade.

A próxima obrigação é escolher uma seção transversal de dados iniciais nulos, demonstrar que o mapa de posição dessa família tem diferencial invertível e construir sua inversa local suave. Só então a velocidade transportada define um campo espacial SmoothVectorOn apto a alimentar 014. O primeiro jato de equilíbrio também precisa ser imposto por uma construção demonstrada.

Continuam OPEN a congruência espacial, o horizonte imerso e sua área integrada, a identificação microscópica região–álgebra e entropia–área, o coeficiente físico, o fluxo de calor e Clausius/H3, a ponte modular–geométrica e a globalização. A dimensão e assinatura lorentziana e a solda invertível continuam INPUT nos enunciados geométricos.

O objetivo amplo de gravidade quântica não está concluído. Esta entrega prova regularidade de fluxos e suas consequências locais sob hipóteses explícitas.

## Custódia e reprodução

Conferência somente leitura:

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation017.py'
```

A ordem de compilação nova é a da tabela; SmoothFlowControls importa toda a árvore 017 e a entrega 016. A gerência deve recompilar em cópia independente, mantendo a bancada entregue imutável. Os binários e fontes locais são fixados pelo manifesto; Lean 4.31.0 e mathlib são dependências externas resolvidas pelo wrapper, não um pacote portátil integral.

As falhas intermediárias de coerção da ordem de diferenciabilidade, da representação de vizinhanças e da composição de funções, além dos avisos de variáveis, estão preservadas. A conferência local verifica evidências e custódia; não constitui a auditoria adversarial independente.

A entrega 016 foi reconferida sem alterações: 538 hashes. Todas as escritas desta etapa ficaram em Chatgpt. Nenhum um.py foi executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate não foram tocados pela bancada.
