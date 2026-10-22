from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

ROOT = Path('C:/IALD/Central de Patentes/Chatgpt').resolve()
OUT = ROOT / 'LIBERDADE_DE_LEVANTAMENTO_079_20260910'
SOURCES = [
    ROOT / 'RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md',
    ROOT / 'SOBREVIVENTE_PONTRYAGIN_077_20260910/PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md',
    ROOT / 'PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md',
    ROOT / 'CME_DIMENSIONAL_EINSTEIN_SIGMA_071_20260910/CME_DIMENSIONAL_E_CONTRATO_DE_TRANSFERENCIA.md',
    ROOT / 'COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md',
]
NOTE = r'''# Outras classes com o mesmo líder: redução gravitacional e equações dos coeficientes

10/09/2026. Investigação079, separada das entregas077/078. [DERIVED — resultados escritos, aguardando revisão independente]. Somente novos arquivos em Chatgpt. Zero CAS, Lean ou execução/importação de um.py; fontes congeladas preservadas.

**Avanço efetivo.** Classifico todas as espécies de correção que podem entrar em ghost3 nas valências quatro, cinco e seis, conservando antifields. Escrevo o sistema explícito de identidades locais necessário e suficiente para cancelar o defeito da classe077. Demonstro que o setor sigma constante admite uma projeção de complexos para Einstein puro; todo cancelamento do modelo completo teria um cancelamento gravitacional como imagem. Construo ainda uma correção quadrática natural cuja variação s1 tem avaliação exatamente A6, mas mostro por um jato explícito que ela falha a condição anterior s0-fechada. A divergência de Pontryagin, sozinha, não resolve o problema.

**Não resolvido aqui:** se −[A6] pertence à imagem δ(K). Não anulo δ(K) por hipótese nem afirmo que a linha cúbica inteira esteja obstruída.

## 1. Qual liberdade restou

Na categoria mínima sem fontes, com B0=(g0,φ0) inerte, curvatura constante K=Λ/3>0 e φ0 constante, a [nota077](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md>) construiu um ciclo T≤5 de ghost3 em C5. O [certificado078](<C:/IALD/Central de Patentes/Chatgpt/RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md>) detecta seu defeito de valência seis por uma solução TT e ghosts de Killing:

\[
r_6=(sT_{\le5})_{[6]}=A_6-s_0\alpha_6,
\qquad [A_6]\ne0\text{ em }H^4(s_0)_{E=6}.
\tag{1}
\]

Seja

\[
\mathcal K=\ker[H^3(C_5)\to H^3(C_3)],
\qquad
\delta:H^3(C_5)\to H^4(F^6/F^7,s_0).
\tag{2}
\]

Outra classe com o mesmo líder pode diferir por β∈K. Para ela levantar a C6, precisamos δβ=−[A6]. A anotação K da curvatura e a notação caligráfica K do núcleo têm papéis distintos nesta nota.

Um representante de β pode ser escolhido com componentes de valência no máximo três iguais a zero: a sua restrição a C3 é uma fronteira, que se retira subtraindo s de qualquer prolongamento finito do representante correspondente. Essa mudança não decide o problema, mas permite procurar β=b4+b5 sem perder nenhuma classe do núcleo. Os fatores t⁴ e t⁵ ficam implícitos quando se indicam as valências.

## 2. A lista completa de espécies nesses três graus

Escreva u=(h,ξ) para os campos pares normalizados, C para o ghost ímpar, u* para antifields físicos ímpares e C* para o antifield do ghost, par. Seus graus de ghost são 0,1,−1,−2; cada jato de qualquer gerador conta uma perna. Os coeficientes dependem de jatos de B0, dos acoplamentos e dos tensores permitidos pela naturalidade, sem fontes extras de ghost positivo.

Um monômio com nC ghosts, nu campos, na antifields físicos e nb antifields de ghost satisfaz

\[
n_C-n_a-2n_b=3,\qquad
E=n_C+n_u+n_a+n_b=3+n_u+2n_a+3n_b.
\tag{3}
\]

Portanto não há espécies ocultas na lista:

| Valência | Espécies de ghost3 |
|---|---|
| 4 | u C³ |
| 5 | u² C³ ; u* C⁴ |
| 6 | u³ C³ ; u* u C⁴ ; C* C⁵ |

Cada fator admite jatos arbitrários, mas FINITOS em um coeficiente, inclusive jatos de ghosts e antifields. A lista classifica espécies, não as classes cohomológicas ou as contrações tensoriais independentes. Não pressupõe um corte uniforme de ordem de derivadas.

Em particular, C* só aparece a partir da valência seis. Os antifields físicos já aparecem em b5 e podem alterar δβ. A orientação admitida e suas possíveis contrações epsilon não mudam (3); nenhuma projeção de paridade espaço-temporal é presumida.

## 3. Diferenciais que realmente entram

Use o [sinal KT corrigido](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>):

\[
s_0u=R_0C,\quad s_0C=0,\quad
s_0u^*=+H_0u,\quad s_0C^*=R_0^\dagger u^*.
\tag{4}
\]

Como φ0 é constante em x, a coordenada local normalizada φ=Exp_φ0(tξ) se comporta como escalar de espaço-tempo. A regra da cadeia e a inversa formal do diferencial de Exp dão exatamente s_tξ=t Lie_Cξ. Não surgem termos superiores nessa transformação dos CAMPOS, embora a ação sigma e suas equações tenham coeficientes superiores. Assim

\[
s_t=s_0+t s_1+t^2s_2+\cdots,
\qquad
s_1h=\mathcal L_Ch,\quad s_1\xi=\mathcal L_C\xi,
\quad s_1C=C\cdot\partial C,
\quad s_j(u)=s_j(C)=0\ (j\ge2).
\tag{5}
\]

Por isso s2b4=0: b4 não contém antifields. Não se conclui que s2 ou os termos seguintes desapareçam do complexo completo.

Se E2,A[u,u] denota o coeficiente quadrático das equações de movimento normalizadas, então

\[
s_1u_A^*=E_{2,A}[u,u]+(\mathcal L_Cu^*)_A.
\tag{6}
\]

O último termo é a derivada de Lie do tensor/densidade dual apropriado; a ordem dos antifields e as derivadas direitas são as de (4). Nenhum fator ½ é imposto a E2 além da definição de coeficiente da expansão. Em especial, s1h* contém E_g,2(h,h), mesmo quando ξ=ξ*=0. Essa contribuição não é descartada por colocar antifields iguais a zero DEPOIS de aplicar s1.

As regras (4–6) prolongam-se a todos os jatos pela conexão de fundo inerte. Usar jatos covariantes simetrizados como geradores requer conservar os comutadores de curvatura nas ordens inferiores; não os eliminamos. Não integramos por partes módulo d_H, pois as expressões aqui são zeroformas e a questão é exatidão de s.

## 4. Sistema explícito necessário e suficiente

Denote por P[u;C³] um operador local linear finito em u e cúbico nos jatos C. Denote por Q[u,u;C³] um operador simétrico bilinear em u; os símbolos a seguir incluem todas as contrações naturais e todas as somas finitas de índices de jato. Escreva

\[
b_4=P[u;C^3],\qquad
b_5=\tfrac12Q[u,u;C^3]+\langle u^*,R(C^4)\rangle.
\tag{7}
\]

O pareamento em (7) é PONTUAL entre jatos e seus coeficientes. Não denota uma integral ou uma classe módulo divergências. O antifield fica à esquerda; R é par, de ghost4. As duas condições para b4+b5 definir uma classe do núcleo K são precisamente

\[
\boxed{P[R_0C;C^3]=0,}
\tag{8}
\]

\[
\boxed{Q[u,R_0C;C^3]
 +\langle H_0u,R(C^4)\rangle
 +s_1P[u;C^3]=0.}
\tag{9}
\]

São identidades universais de polinômios de jatos, não somente identidades na solução TT de avaliação. Em s1P entram tanto a variação Lie_Cu como a variação de cada jato do ghost. As identidades devem valer em todos os componentes, inclusive os sigma.

Para representar uma possível correção seguinte, a lista (3) dá

\[
b_6=\tfrac16D[u,u,u;C^3]
 +\langle u^*u,E(C^4)\rangle
 +\langle C^*,F(C^5)\rangle.
\tag{10}
\]

D é simétrico trilinear nos campos. O sistema de cancelamento da classe específica mais β é

\[
\boxed{s_0b_6+s_1b_5=-r_6,}
\tag{11}
\]

além de (8–9). Essas condições são NECESSÁRIAS pela comparação de valências e SUFICIENTES para T≤5+b4+b5+b6 ser fechado em C6, porque não há outros termos de ghost3 nesses graus e s2b4=0. A afirmação é sobre a solução desse sistema local; não afirma que os operadores P,Q,R,D,E,F tenham sido encontrados.

A parte sem antifields de (11) contém explicitamente

\[
\tfrac12D[u,u,R_0C;C^3]
 +\langle (H_0u)u,E(C^4)\rangle
 +s_1\!\left(\tfrac12Q[u,u;C^3]\right)
 +\langle E_2[u,u],R(C^4)\rangle=-r_6.
\tag{12}
\]

Há ainda uma condição independente para a parte linear em antifields:

\[
-\langle u^*(R_0C),E(C^4)\rangle
 +\langle R_0^\dagger u^*,F(C^5)\rangle
 +\langle\mathcal L_Cu^*,R(C^4)\rangle
 -\langle u^*,s_1R(C^4)\rangle=0.
\tag{13}
\]

O sinal menos no primeiro e no último termos vem da regra de Leibniz para o antifield ímpar colocado à esquerda. Todas as derivadas e contrações presentes nos pareamentos devem ser conservadas. Não basta satisfazer apenas a avaliação da parte (12); (8), (9) e (13) são obrigações distintas.

## 5. Projeção sigma constante: redução de complexos

Na [ação Einstein–sigma071](<C:/IALD/Central de Patentes/Chatgpt/CME_DIMENSIONAL_EINSTEIN_SIGMA_071_20260910/CME_DIMENSIONAL_E_CONTRATO_DE_TRANSFERENCIA.md>), o setor matéria é somente c/2 vezes g⁻¹h_target(dφ,dφ), sem potencial escalar adicional. Para qualquer métrica, o mapa constante φ=φ0 tem dφ=0, equação sigma zero e tensor de energia sigma zero.

Seja Iσ o ideal diferencial gerado por todos os jatos de ξ e ξ*. Então

\[
s(I_\sigma)\subset I_\sigma.
\tag{14}
\]

De fato, sξ=t Lie_Cξ pertence ao ideal. A equação de ξ* contém a equação sigma, que se anula em ξ=0 para qualquer g, e os termos de fontes sigma, que contêm ξ*. A transformação do antifield métrico perde seu tensor matéria em ξ=0; a fonte sigma da transformação de C* contém ξ* e/ou dξ. O mesmo vale para todos os prolongamentos, e a expansão formal é regular nessa subvariedade.

Portanto existe uma projeção de complexos completos e de seus truncamentos

\[
\pi:\mathcal A_{\mathrm{Einstein-}\sigma}
\longrightarrow\mathcal A_{\mathrm{Einstein}},
\qquad \xi=\xi^*=0,
\tag{15}
\]

com a mesma métrica de fundo e Λ. Ela preserva ghost, valência e naturalidade, e comuta com δ e com a restrição C5→C3. O resíduo A6 e a classe T≤5 são puramente gravitacionais. Consequentemente

\[
-[A_6]\in\delta(\mathcal K_{\mathrm{full}})
\ \Longrightarrow\
-[A_6]\in\delta(\mathcal K_{\mathrm{grav}}).
\tag{16}
\]

A recíproca não foi demonstrada. Um cancelamento em Einstein puro que use h* pode gerar termos sigma quando reinserido no modelo completo, pois s1h* contém também a contribuição quadrática da matéria. A projeção é uma condição necessária útil; não é uma identificação de todas as cohomologias.

Em particular, no funcional TT078, todos os termos com ξ, ξ* e seus jatos desaparecem após aplicar s1: Eσ,2(h,0)=0 e s1ξ=0 nesse teste. Para um candidato (7), a condição necessária de avaliação fica

\[
\operatorname{ev}_p\!\left[
s_1\!\left(\tfrac12Q[h,h;C^3]\right)
 +\langle E_{g,2}[h,h],R_g(C^4)\rangle\right]
=-\operatorname{ev}_p(A_6).
\tag{17}
\]

Essa fórmula conserva as derivadas de E_g,2 que aparecem se R emparelha jatos de h*. Elas não são zero simplesmente porque a solução escolhida satisfaz E_g,1=0. Nenhum passo da redução permite omiti-las.

## 6. Um controle natural com avaliação não nula, que ainda falha a condição anterior

Há uma razão concreta para não tentar provar ev_p s1=0 sobre TODAS as espécies h²C³. Ponha L=δΓ[g0;h], a diferença de conexão linearizada, uma 1-forma End(TM) natural de grau um em h. Considere a 3-forma quadrática

\[
J_2=\operatorname{tr}(L\wedge\bar D L).
\tag{18}
\]

Ela usa somente a conexão relativa e seus jatos; não introduz um frame externo. Para g_t=g0+t h, a diferença exata Θ=Γ(g_t)−Γ(g0) é tensorial e satisfaz Θ^a_b∧dx^b=0 por ausência de torção. Como Rbar^a_b=K dx^a∧dx_b,

\[
\operatorname{tr}(\Theta\wedge\bar R)=0.
\tag{19}
\]

A transgressão ordinária de traço, válida entre essas duas conexões GL, reduz-se portanto a
tr(Θ∧DbarΘ)+(2/3)tr(Θ³). Seu coeficiente quadrático é exatamente J2. A identidade de Weyl077 dá

\[
\boxed{d_HJ_2
=\operatorname{tr}(W_{[1]}\wedge W_{[1]})
=\rho_{[2]}d^4x.}
\tag{20}
\]

Em particular, não é preciso acrescentar um termo envolvendo a segunda variação Γ2: sua contração com Rbar já é zero por (19). Essa é uma identidade local de formas, não uma primitiva s0.

Defina I_CJ2=(1/3!)(J2)_μνρ CμCνCρ, uma zeroforma natural de espécie h²C³ e valência cinco. Na avaliação por ghosts de Killing, s1 atua em h por Lie_C h e a referência é preservada por C. Assim J2 varia pela derivada de Lie e a identidade de avaliação de formas fornece

\[
\boxed{\operatorname{ev}_p(s_1 I_CJ_2)
=\operatorname{ev}_p(I_Cd_HJ_2)
=\operatorname{ev}_p(A_6)\ne0.}
\tag{21}
\]

O sinal em (21) é o da convenção sC=C·∂C e da ordenação I_C das notas076–078. A fórmula inclui a variação dos ghosts; omiti-la quebraria a identidade de Cartan. Portanto as espécies puramente métricas não são eliminadas pela avaliação TT sozinhas.

Contudo, I_CJ2 não é automaticamente um elemento de K. A primeira condição necessária, se b4=0, seria s0(I_CJ2)=0, e ela é falsa. Um controle nos jatos mais altos mostra a falha sem depender de K. Escolha coordenadas normais de g0 em p, h(p)=∇h(p)=0 e o segundo jato h22=(x1)²; isso dá (Dbar L)^1_2(p)=dx1∧dx2. Entre os ghosts, escolha C0(p)=θ0, C1(p)=θ1, C2(p)=θ2, C3(p)=0 e um segundo jato independente ∂0∂1C2(p)=ζ. Todos são geradores ímpares livres; esse ghost NÃO é restringido a Killing para o teste universal de fechamento.

O símbolo de s0L^a_bμ é ∂b∂μC^a. Como L(p)=0, a variação do segundo fator de (18) não contribui ao monômio escolhido. A variação do primeiro fator produz

\[
\bigl[s_0(I_CJ_2)\bigr]_{\zeta\theta^0\theta^1\theta^2}
=1\ne0
\tag{22}
\]

nas normalizações de jatos acima. Os termos de curvatura de fundo dependem dos jatos inferiores do ghost e não podem cancelar o coeficiente do gerador ζ escolhido independentemente. A conexão linearizada é derivada do segundo jato de uma perturbação métrica, de modo que o controle respeita suas simetrias; não foi escolhida uma conexão arbitrária.

Portanto −I_CJ2 satisfaria a condição de avaliação desejada, mas viola (9) quando b4=0 e R=0. Para torná-lo uma correção legítima, seria necessário encontrar b4 e/ou R(C4) e outros termos Q que restaurem (8–9), e depois também (13). Não os presumo disponíveis. Este exemplo paga uma verificação negativa concreta: a identidade de divergência natural e o valor certo na avaliação não bastam para produzir δβ.

## 7. O que foi reduzido e o que ainda exige cálculo

[DERIVED] As espécies (3), o sistema (8–13), a projeção de complexos (14–16), a redução TT (17) e o controle (18–22) são resultados novos delimitados. Eles isolam a obrigação gravitacional sem remover os antifields que podem contribuir. O problema residual já é uma busca por operadores locais finitos P,Q,R,D,E,F satisfazendo identidades explícitas, na mesma classe natural.

[OPEN] Não foi encontrada uma solução desse sistema que realize −[A6], nem um funcional que anule δ(K) inteiro. O contraexemplo (22) exclui somente a correção simples I_CJ2 tomada isoladamente. Não prova que ela não possa ser completada com outros termos.

A classe de coeficientes admite jatos de ordem finita em cada expressão, mas sem uma cota uniforme preestabelecida. Por isso a classificação das espécies não transforma por si o sistema em uma matriz finita. Um corte legítimo de peso de engenharia, ordem de derivadas e acoplamentos, ou uma homotopia com controle nessa classe, ainda precisará ser demonstrado antes de anunciar uma enumeração exaustiva.

Não se promove a obstrução da classe específica078 a uma obstrução de toda a linha CE. Não se decide H³/H⁴ completo, lim¹, Mittag–Leffler, QME ou UV. A nota079 permanece fora da entrega078 e não altera nenhuma fonte anterior.

[REAL — documental] O manifesto mede as cinco fontes antes/depois, nota e script; as verificações de existência e bytes são documentais. Nenhuma revisão de077/078 foi reaproveitada como aprovação desta investigação, e nenhum CAS/Lean foi executado para ela.
'''


def pin(path):
    data = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def emit(path, data):
    if path.exists():
        raise FileExistsError(path)
    tmp = path.with_name(path.name + '.tmp_new')
    with tmp.open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if tmp.read_bytes() != data:
        raise RuntimeError('TEMP_BYTE_MISMATCH')
    if path.exists():
        raise FileExistsError(path)
    tmp.rename(path)
    if path.read_bytes() != data:
        raise RuntimeError('FINAL_BYTE_MISMATCH')


before = [pin(path) for path in SOURCES]
OUT.mkdir(exist_ok=True)
note_path = OUT / 'CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md'
emit(note_path, NOTE.encode('utf-8'))
after = [pin(path) for path in SOURCES]
if before != after:
    raise RuntimeError('SOURCE_CHANGED')
links = re.findall(r'\]\(<(C:/[^>]+)>\)', NOTE)
if not all(Path(p).is_file() for p in links):
    raise RuntimeError('MISSING_LOCAL_LINK')
manifest = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'kind': 'written_lift_freedom_reduction',
    'author': '/root/prepare_integration_83',
    'status': 'DERIVED_WRITTEN_AWAITING_INDEPENDENT_REVIEW',
    'results': ['complete monomial species at ghost3 valences4-6', 'explicit necessary and sufficient local coefficient system through C6', 'BRST quotient to pure Einstein at constant sigma map', 'nonzero evaluation of quadratic connection current and explicit failure of its s0 closure'],
    'remaining_question': 'whether -[A6] belongs to delta(kernel(H3(C5)->H3(C3)))',
    'source_pins_before': before,
    'source_pins_after': after,
    'sources_unchanged': True,
    'note': pin(note_path),
    'creator': pin(Path(__file__).resolve()),
    'local_links': [{'path': p, 'exists': True} for p in links],
    'executions': {'CAS': 0, 'Lean': 0, 'um_py_execution_or_import': 0},
    'not_claimed': ['solution of cancellation system', 'vanishing of delta(K) under TT evaluation', 'obstruction of every class with same cubic leader', 'finite exhaustive tensor basis without derivative bound', 'QME or UV verdict', 'canonical integration', 'independent approval already received'],
}
manifest_path = OUT / 'MANIFESTO_LIBERDADE_LEVANTAMENTO_079.json'
emit(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'note': pin(note_path), 'manifest': pin(manifest_path),
                  'source_count': len(before), 'sources_unchanged': True,
                  'local_links_existing': len(links)}, ensure_ascii=False))
