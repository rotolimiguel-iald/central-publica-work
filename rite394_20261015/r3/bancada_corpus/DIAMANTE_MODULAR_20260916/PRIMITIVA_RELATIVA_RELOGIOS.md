# Primitiva relativa no domínio dos relógios físicos

16/09/2026. [DERIVED — demonstração escrita; revisão independente em documento separado]. Não é uma compilação Lean, uma normalização causal executada ou uma demonstração de completude UV.

## 1. Recuperação do antecedente, sem inventar uma entrega

O arquivo [write_bv_clock088_new.py](../write_bv_clock088_new.py) contém, na variável `body`, uma demonstração intitulada “Homotopia BV por relógios no fundo físico — 088”. A pasta de saída anunciada pelo script, `HOMOTOPIA_BV_RELOGIOS_088_20260910`, não foi encontrada nesta leitura. O script não foi executado. Portanto o antecedente é um **rascunho matemático recuperado**, não uma entrega emitida ou aprovada em 10/09.

Seu mecanismo reaproveita o extrator F de [BRST068, §3](../EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md), a [ação BV069](../CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md) e os [relógios relacionais088](../RELOGIOS_RELACIONAIS_FUNDO_FISICO_088_20260910/RELOGIOS_X_SIGMA_E_RETRACAO_DE_JATOS.md). Aqui explicitamos sua consequência diretamente para a cohomologia relativa. Não precisamos impor uma descida completa como hipótese adicional.

O procedimento abstrato de retirar pares contráteis também vale para cociclos relativos; essa passagem está demonstrada no apêndice 2.B de [Barnich–Brandt–Henneaux](https://arxiv.org/pdf/hep-th/0002245), pp.18–19. Sua aplicação ao fundo, às variáveis e à completação abaixo é uma verificação própria, não um resultado físico importado daquele artigo.

## 2. Domínio e hipóteses que a conclusão conserva

Fundo físico on-shell: M=(0,π)×S³, ḡ=dr²−a²γ, a=2cos(r/2), φ̄=id. Os suportes são compactos no interior. Os coeficientes pertencem ao aberto de jatos no qual

\[
E(v)=(d\bar\phi(v),d\bar X(v)),\qquad
\bar X=\bar g^{-1}\cdot\bar\phi^*\gamma,
\]

é inversível. No fundo, X̄=−3/a² e X̄′=6a′/a³≠0. Essa localização permite inversas de jatos do fundo. Ela NÃO é a classe universal regular074, que inclui mapas sigma constantes. A [auditoria de domínio088](../DOMINIO_RELOGIOS_FISICOS_088_20260910/NOTE.payload.md), §§3–7, explicita naturalidade, regularidade interior e a falha de extensão da receita.

Usamos o complexo BV clássico completo, com antifields e setor não mínimo, e a completação por valência: cada coeficiente é polinomial nas variáveis dinâmicas, tem ordem finita de jatos e coeficientes de fundo na localização. Todos os campos, ghosts, auxiliares e antifields contam com valência um; suas derivadas têm a mesma valência. A_E designa a componente homogênea de valência E. Não há coeficiente externo de ghost positivo. Uma fonte Ω de ghost positivo para comparação de fundos muda este contrato.

As convenções são de grau total ghost+forma:

\[
s^2=d_H^2=0,\quad s d_H+d_Hs=0,\quad
s=s_0+s_+,\quad s_+=\sum_{j\ge1}s_j,
\]

com s_j aumentando a valência em j. O fundo on-shell exclui um termo constante de equações de movimento na transformação dos antifields. Não se afirma convergência da série formal.

## 3. Por que a contração livre inclui antifields

Desfazemos primeiro a fixação de gauge pela inversa da transformação canônica de BV069. Esse passo conserva o complexo, a valência e a ordem finita por coeficiente. Com u=(h,ξ), escrevemos a ação livre não fixada como

\[
S_2=\tfrac12\langle u,\mathscr Hu\rangle
    +\langle u^*,KC\rangle-\langle\bar C^*,b\rangle.
\]

A Hessiana variacional satisfaz Hscr K=0 como identidade diferencial. O extrator existente satisfaz FK=Id. Defina ζ=Fu e H=h−Lie_ζ ḡ; aqui H é o tensor reduzido, não a Hessiana. Então

\[
s_0\zeta=C,\quad s_0C=0,\quad s_0H=0,
\qquad u=(H,0)+K\zeta.
\]

H pertence ao fibrado de posto nove ker τ, com τ(H)=ḡ^{μα}ḡ^{νβ}(φ̄*γ)_{αβ}H_{μν}. Essa restrição remove a redundância que haveria ao tratá-lo como dez componentes livres. A mudança e sua inversa são diferenciais de ordem finita; usam o limite direto dos espaços de jatos, não um mesmo J^k em ambos os lados.

Mantemos os antifields antigos não fixados como coordenadas independentes. Não alegamos que mudar só os campos preserve o antibracket: transportamos o diferencial já definido, o que basta para a cohomologia. As transformações livres dos demais geradores são independentes de ζ,C e seus jatos. Em particular, s₀u* é, com o sinal da convenção BV, Hscr(H,0), e s₀C* é K*u* com seu sinal fixado. Os pares não mínimos tampouco dependem de ζ,C. Os geradores restantes têm ghost não positivo.

Defina κ(C_I)=ζ_I, κ(ζ_I)=0 e κ=0 nos demais geradores e nos fundos, prolongando pelas derivadas totais. Se N conta os fatores ζ,C e seus jatos, então

\[
s_0\kappa+\kappa s_0=N,\qquad
\kappa d_H+d_H\kappa=0,\qquad[N,d_H]=0.
\]

O sinal horizontal resulta da extensão por grau total; as derivadas horizontais continuam derivando os coeficientes de fundo. Seja π a projeção que põe ζ_I=C_I=0 e h₀=κ/N em N>0, zero em N=0. Obtemos

\[
\{s_0,h_0\}=1-\pi,\qquad \{h_0,d_H\}=0.
\tag{1}
\]

Como os geradores residuais e os coeficientes não têm ghost positivo, πa=0 para toda forma de ghost positivo. Isso não afirma que a cohomologia física de ghost zero seja trivial.

## 4. Primitiva relativa livre: basta a primeira consistência

Considere a de ghost g>0 e forma p e b de ghost g+1 e forma p−1, satisfazendo

\[
s_0a+d_Hb=0.
\]

Aplicando (1), sem construir descendentes adicionais,

\[
a=s_0h_0a+h_0s_0a
  =s_0h_0a-h_0d_Hb
  =s_0h_0a+d_Hh_0b.
\tag{2}
\]

Logo H^{g,p}(s₀|d_H)=0 para g>0 nessa classe. Não usamos um lema de Poincaré global nem trocamos a topologia de S³ pela de uma carta.

## 5. Primitiva relativa para todas as valências

Agora suponha sa+d_Hb=0 para o diferencial clássico completo. Construiremos B e C com a=sB+d_HC. Os seus graus são (g−1,p) e (g,p−1).

Partindo de B=C=0, defina

\[
R=a-sB-d_HC,\qquad b_R=b-sC.
\]

Aqui R é somente um **resíduo de construção BRST**, não o resto modular Kω−Kξ. A anticomutação entre s e d_H fornece

\[
sR+d_Hb_R=0.
\tag{3}
\]

Se R já é zero nas valências menores que E, a componente de (3) em E é s₀R_E+d_H(b_R)_E=0: s_+ só receberia parcelas menores de R, já nulas. Por (2),

\[
R_E=s_0h_0R_E+d_Hh_0(b_R)_E.
\]

Acrescente

\[
\Delta B_E=h_0R_E,\qquad
\Delta C_E=h_0(b_R)_E.
\tag{4}
\]

A atualização mata R_E e não altera as valências inferiores. A parte adicional s_+ΔB_E tem valência estritamente maior. Atualizando b_R=b−sC, (3) continua exata. Não é necessário que b_R se anule nas valências inferiores: o controle usado é R_{<E}=0. Não se afirma que a identidade (1) valha ao substituir s₀ por s; o diferencial completo é tratado pela recorrência. A indução em E define B,C coeficiente a coeficiente; em cada ordem ocorrem finitamente muitas operações de ordem finita. Portanto

\[
\boxed{H^{g,p}(\widehat{\mathcal A}_{\rm clk},s\mid d_H)=0
       \quad(g>0),}
\qquad
\boxed{a^1_4=sB^0_4+d_HC^1_3.}
\tag{5}
\]

Aqui 0≤p≤4; para p=0, tomamos as formas de grau negativo como zero, portanto b=C=0. Este é um resultado na completação localizada declarada. Não requer hipótese separada de descida completa de a₄¹ a uma forma zero. Não prova uma cota uniforme de jatos em todas as ordens, nem preservação de qualquer subespaço com cota de escala fixada.

## 6. O que isso paga na cadeia física, e o que ainda deve ser consumido

A consistência local da primeira quebra não removida da Q2 fornece precisamente a entrada sa+d_Hb=0. Quando seus coeficientes são restringidos à classe acima e não há fontes externas de ghost positivo, (4) constrói uma primitiva clássica formal localizada. Essa etapa de cohomologia pode ser consumida, sem exigir novamente uma prova de FK=Id ou da existência do estado livre067.

O [contrato Q2, §3](../COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md) exige mais: as aplicações multilineares de renormalização têm cotas de escala, compatibilidade entre aridades, EOM, contatos, ação por partes, regularidade e condições de realidade. Uma primitiva na localização não constitui por si essa família de normalizações. Multiplicar uma identidade por cutoff conserva os termos de sua derivada. A exigência de comparação de fundos com fontes Ω também fica fora de (5).

Assim, não se infere QME, carga renormalizada P2, estado positivo interagente/UV ou igualdade kT_t f=δ_D^{it}kf a partir de (5). Também não se infere uma anomalia física inevitável: o déficit é de admissibilidade/implementação, não uma prova de impossibilidade.

Quanto à relação solicitada entre vácuo, dephasing e geometria, os fornecedores Lean da [V2](HANDOFF_TECNICO_V2.md) permanecem os corretos. A prova BRST acima ajuda a organizar o fornecedor interagente; ela não troca a referência tracial parcial da torre pela carga regional do tensor de energia. Essa última identificação conserva seu próprio contrato.

Nenhum consumidor Python, gate ou original foi modificado por esta nota. A revisão e o manifesto registram separadamente prova escrita, antecedente recuperado e evidência histórica de compilação da ponte V2.
