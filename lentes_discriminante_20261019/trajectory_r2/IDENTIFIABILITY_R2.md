# Identificabilidade do atraso e da trajetória — R2

19/10/2026 · F8.LENTES_5SIGMA_20261019 · claim 1009 · referência própria SESSION_REFERENCE.json, revisão 2. Autor: agente codex da coordenação, derivação para revisão. [DERIVED], não prova Lean nem resultado observado. Reuso: LENTES_VIABILIDADE_R1.md:7–19 e TDCOSMO2026 §II, equações (1)–(6); pinos/âncoras em SOURCE_PINS_IDENTIFIABILITY_R2.json. A notação **y** é a posição angular da fonte, para não confundir com β_TGL.

## 1. Objeto e convenções

Uma lente fina, estática, um plano e uma fonte; ângulos em radianos na normalização comum. Potencial projetado ψ(θ;p), parâmetros físicos compartilhados p. Seja

φ(θ,y;p)=|θ−y|²/2−ψ(θ;p),  t(θ)=Dφ/c,  D=(1+z_l)D_l D_s/D_ls>0.

As imagens são pontos estacionários ∇θφ=0, incluindo selas. Atraso orientado Δt_ij=t_i−t_j; não impor sinal positivo a cada par. Esta descrição é geométrica/escalar; efeitos dispersivos, birefringentes ou de óptica ondulatória exigem sua lei própria. Nenhuma q abaixo é atribuída à TGL. [INPUT] q é um potencial adicional suficientemente regular, com εq nas mesmas unidades angulares de φ; sua normalização precisa ser fixada independentemente para ε ser identificável.

## 2. Deslocamento consistente, sem congelar imagens

Defina φε=φ+εq(θ). A deflexão efetiva é αε=∇ψ−ε∇q. Para uma imagem não crítica θ_i, A_i=I−Hessψ(θ_i) invertível, o teorema da função implícita dá

θ_i'(0)=−A_i⁻¹∇q(θ_i).

A derivada do tempo avaliado na imagem móvel satisfaz a regra de envelope:

d/dε φε(θ_i(ε))|0 = ∇φ(θ_i)·θ_i'(0)+q(θ_i)=q(θ_i),

portanto ∂εΔt_ij=(D/c)(q_i−q_j) para D,y,p fixos. O deslocamento não desaparece do modelo: ele é necessário para as posições, magnificação e ordens seguintes; apenas seu termo linear no tempo é nulo por estacionariedade. Com nuisances variando,

δΔt_ij = (δD/c)Δφ_ij +(D/c)[εΔq_ij−(θ_i−θ_j)·δy−Δ(∂pψ)_ij·δp].

A equação de posições simultânea é A_i δθ_i=δy+(∂p∇ψ)_i δp−ε∇q_i. Isso obriga usar os mesmos p em imagem e atraso. Para magnificação μ=1/det A, δA inclui εHessq **e** −D³ψ[δθ], além das variações de p; omitir o deslocamento também ali é incorreto. Próximo de cáusticas A⁻¹ diverge: esta expansão regular não vale, e é necessário tratar a ramificação/óptica pertinente.

## 3. Multiplicador universal e folha de massa: degenerescências exatas

(a) Se o modelo fosse tε=D C(ε)φ/c, C>0 independente de θ e da polarização, as imagens não mudariam. Todos os atrasos são idênticos aos do modelo sem ε com D_fit=C D. Um parâmetro de distância livre absorve o efeito **exatamente**, com qualquer precisão instrumental. Razões de atrasos cancelam C. Isso não vale automaticamente para multiplicar só ψ: nesse caso a equação de lente e as imagens mudam.

(b) Transformação de folha de massa (MST): ψλ=λψ+(1−λ)|θ|²/2, yλ=λy, λ>0. Então

φλ(θ,yλ)=λφ(θ,y)+λ(λ−1)|y|²/2,

∇φλ=λ∇φ, Δφλ=λΔφ, Aλ=λA, μλ=μ/λ².

Com Dλ=D/λ, os atrasos também são iguais. Posições, formas relativas e razões de fluxo permanecem iguais sob a correspondente reescala da fonte. Magnificação absoluta não permanece igual. A MST ideal é uma simetria matemática; a admissibilidade física de um perfil/sheet finito e as informações externas limitam a sua realização. A diferença de atrasos entre várias imagens **não quebra por si a MST**. [KNOWN] Schneider, arXiv:1409.0015, mostra a mesma limitação para razões no contexto multi-plano; aqui a identidade de plano único foi derivada explicitamente.

(c) Além da MST, se a família admitida de potenciais puder absorver ψ_eff=ψ−εq, todos os observáveis escalares de lente deste modelo são os de ψ_eff. A presença de uma forma espacial em q não garante identificabilidade: é preciso informação que distinga massa gravitante de propagação, ou uma restrição independente da família de massa. Positividade, regularidade e fronteira podem restringir essa absorção; não são assumidas como resolvidas.

## 4. Ponto-massa: dois casos de não identificabilidade demonstrados

Para ψ=b ln|θ|, b=θ_E²>0, fonte alinhada y>0, as duas imagens axiais são x±=(y±√(y²+4b))/2. Escrevendo u=y/√b>0,

Δφ_−+=b F(u), F(u)=u√(u²+4)/2+ln[(√(u²+4)+u)/(√(u²+4)−u)],
Δt_−+=(D b/c)F(u)=4GM(1+z_l)F(u)/c³.

**Só um atraso:** há uma única restrição no produto D b F(u); para qualquer b,u admissíveis com F≠0 escolhe-se D=cΔt/[bF(u)]. Se b for convertido para M por distâncias consistentes, D b=4GM(1+z_l)/c²: não contar M e b como informações independentes. O atraso sozinho continua degenerado com M e u. Isso não é corrigido por minimizar apenas massa e manter imagens arbitrárias.

**Mesmo duas posições + um atraso:** há uma família exata local para q radial (ou axial compatível), sem afirmar o mesmo para uma q 2D arbitrária. Fixe posições observadas x+>0>x−, distintas de zero. Para o modelo φε= (x−yε)²/2−bε ln|x|+εq(x), defina

bε=[(x+−x−)+ε(q'(x+)−q'(x−))]/(1/x+−1/x−),
yε=x+−bε/x++εq'(x+).

As DUAS equações de lente são satisfeitas exatamente nas mesmas posições. Para ε suficientemente pequeno, bε>0 e Δφε_−+ mantém o sinal não nulo. Defina então Dε=D0 Δφ0_−+/Δφε_−+. O atraso é idêntico. Um H0 livre, com a forma da expansão fixa, permite reescalar D; a massa física é ajustada consistentemente por bε Dε, não mantida independentemente sem dados. Razões de fluxo, imagens extensas e informação dinâmica não foram impostas nesta família; podem restringi-la. No alinhamento y=0, o atraso par é zero e não fornece esta divisão; é ainda menos informativo.

[REAL — controle racional pré-registrado] x+=2, x−=−1/2, b0=1,y0=3/2. Para q=x²/2 a fonte/massa fixas: x+'=−8/5, x−'=1/10, ∂εΔφ_−+=−15/8. Para q=x⁴/4 e ε=−1/100, o perfil exato acima dá bε=387/400,yε=1149/800 e Δφε_−+=2247/1280+(387/400)ln4. Ambos os gradientes são zero. Manter b0,y0 e congelar as imagens produz gradientes não nulos. 23 verificações racionais aprovadas; a compensação Dε é identidade analítica por substituição, sem medição ou ajuste numérico. q é exemplo genérico, não uma lei TGL nem um perfil global real validado.

## 5. Critério operacional para um discriminante

Para um vetor conjunto d=(posições/arcos, atrasos, fluxos admitidos, cinemática...), prediga m(ε,η) com a mesma massa, distâncias e instrumentação; η inclui fonte, perfil, convergência externa, anisotropia etc. Com covariância positiva definida Σ, defina W=Σ⁻¹, s=∂εm, N=∂ηm. No modelo linear local sem priors:

Iε,perfil = sᵀWs − sᵀWN(NᵀWN)^+NᵀWs ≥0.

É a norma quadrada da componente de Σ⁻¹/²s fora da imagem de Σ⁻¹/²N. Se s pertence ao espaço de nuisances, I=0: não há poder local, nem acumulando cópias que preservem a mesma degenerescência livre. I>0 não elimina degenerescências globais, não linearidades, fronteiras ou vieses. Informação externa acrescenta likelihood/precisão com origem explícita; nunca chamar massa inferida assumindo a própria lente GR de massa independente.

Uma meta gaussiana mediana local de separação cinco exige |ε_alvo|√Iε,perfil≥5, além de validade e controle de sistemáticas. Não foi avaliada aqui: não há q_TGL normalizada, amplitude prevista, dados conjuntos ou covariância admissível nesta entrega. Uma diferença temporal dividida só por erro de relógio ignora o perfilamento necessário.

## 6. Observáveis candidatos e limites

| Informação adicional | O que pode separar | O que não garante |
|---|---|---|
| Três ou mais imagens: razões de atrasos | Remove D; testa padrão de Δq não proporcional ao vetor Δφ, depois do perfilamento da massa | Não quebra C universal/MST; mais imagens não fixam automaticamente ψ |
| Cinemática estelar resolvida + luminosidade, com massa e anisotropia compartilhadas | Restringe potencial dinâmico e família interna de massa se a teoria explicitar a relação luz–dinâmica | Não elimina automaticamente convergência externa ou degenerescência massa–anisotropia; a dinâmica TGL não pode ser presumida GR sem contrato |
| Distâncias externas/cosmologia independente e ambiente | Restringe reescala D e linha de visada | Um prior escolhido para favorecer o efeito não é dado independente |
| Magnificação absoluta de fonte calibrada (SN Ia) | Sensível ao fator μ/λ² | Exige padronização, distância/luminosidade, poeira, microlentes e seleção consistentes |
| Atraso diferencial de polarização ou frequência | Pode cancelar uma contribuição gravitacional comum se q_s difere e o modelo prevê esse contraste | q escalar comum não cria discriminação polarimétrica; dispersão do meio, relógio, emissão e transporte de polarização precisam ser modelados |
| Imagens extensas/fluxos e fontes adicionais | Acrescentam derivadas/estrutura do potencial e podem restringir q genérica | Degenerescências generalizadas e geometria multi-plano precisam ser tratadas; não presumir ruptura universal |

Para um contraste polarizado entre as MESMAS duas imagens, compare (t_i,s−t_j,s)−(t_i,r−t_j,r), que cancela o tempo de emissão por canal se a variável observada foi identificada corretamente; deslocamentos específicos e propagação/instrumentação permanecem. Sem lei q_s não há amplitude polarizada previsível. Para três imagens, δ(Δt_ij/Δt_ik)=(Δq_ij Δφ_ik−Δφ_ij Δq_ik)/(Δφ_ik)² a p,y fixos; o perfilamento deve incluir a resposta destes parâmetros.

## 7. Entrega e próxima ligação

O resultado útil é um teste de **identificabilidade conjunta**, antes do poder: recuperar q_TGL/lei de raios, calcular trajetórias e atrasos pela mesma ação e só depois projetar contra nuisances com informações independentes. Não escolher uma q conveniente ou fixar cosmologia/massa para produzir cinco sigma. Se o acervo fornecer apenas multiplicador universal, o atraso isolado não é o canal discriminante, mesmo que o atraso seja precisamente previsto. Se fornecer uma assinatura dependente da trajetória/polarização, esta nota dá o consumidor e os controles necessários.

Referências primárias: TDCOSMO2026, https://arxiv.org/html/2610.14781v1, §II.1–II.3 (bytes previamente custodiados, equações 1–6); Peter Schneider, https://arxiv.org/abs/1409.0015, abstract consultado em19/10/2026 (web; sem alegar custódia local de seus bytes). Fórmulas de perturbação, exemplo ponto-massa e projeção de nuisance são as derivações desta nota, auditáveis independentemente. Nenhum dado observado, provedor, arquivo canônico, memória ou gate alterado.
