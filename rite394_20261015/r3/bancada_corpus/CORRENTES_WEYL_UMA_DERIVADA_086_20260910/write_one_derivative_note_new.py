from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
SOURCES = [
"GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md",
"COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md",
"DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md",
"CANDIDATO_DERIVADA_WEYL_083_20260910/CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md",
"REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md",
"REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md",
"CORRENTE_NECESSARIA_E_LIMITE_GRADIENTE_084_20260910/EULER_SOZINHO_E_GRADIENTE_ESCALAR_NAO_BASTAM.md",
"INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md",
]
def pin(path):
    p = Path(path); raw = p.read_bytes()
    return {"path": p.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
def new(name, raw):
    p = OUT / name
    assert p.resolve().is_relative_to(ROOT) and not p.exists() and raw
    tmp = p.with_name(p.name + ".tmp_" + datetime.now().strftime("%H%M%S_%f"))
    with tmp.open("xb") as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(p)
    assert p.read_bytes() == raw
    return pin(p)
before = [pin(ROOT / rel) for rel in SOURCES]
script_before = pin(Path(__file__))
note = r"""# Correntes quadráticas de Weyl com uma derivada: classificação e imagem de divergência

10/09/2026. Investigação086 NOVA, separada da consolidação085. [DERIVED — demonstração escrita, a submeter a revisão independente integral]. [REAL — apenas medição documental de arquivos; zero novo CAS, Lean ou execução/importação de um.py].

**Resultado delimitado.** No fundo Einstein espaço-forma Lorentziano orientado de dimensão quatro, com K>0 real fixado e coeficientes escalares herdados constantes/inertes, todas as correntes naturais quadráticas da forma W·∇bar W, tomadas no quociente pelas equações Einstein LINEARES e seus prolongamentos, são

\[
\boxed{V^a=A\,\bar\nabla^a I+B\,\bar\nabla^a J,\qquad
I=\tfrac12W_{bcde}W^{bcde},\quad
J=\tfrac12W_{bcde}(*W)^{bcde}=J_W,\quad A,B\in R_{\rm her}.}
\tag{1}
\]

Os dois geradores são independentes no próprio quociente. A imagem da divergência é o módulo livre

\[
\boxed{\operatorname{div}\mathscr V_{W\nabla W}
=R_{\rm her}\bar\Box I\oplus R_{\rm her}\bar\Box J.}
\tag{2}
\]

Nenhuma corrente desse setor produz J. Mais fortemente, não existem V nesse setor e f invariante sob TODA a álgebra de Killing tais que

\[
\boxed{J=\operatorname{div}V+K^2 f.}
\tag{3}
\]

O resultado amplia a exclusão084, que tratava somente B grad J: agora foi provado que grad I e grad J esgotam as contrações com exatamente UMA derivada. Não se classifica W∇³W, ∇W∇²W, os demais jatos, primitivas causais, QME ou o modelo físico geral.

## 1. Categoria e convenções

Conservamos a [categoria080](<C:/IALD/Central de Patentes/Chatgpt/GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md>) e o [quociente linear081](<C:/IALD/Central de Patentes/Chatgpt/COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md>). W=W[1][h] é a variação do tensor de Weyl; g0 é inerte, conformemente plano e satisfaz Ric(g0)=3K g0. A matéria foi projetada para φ0 constante no teste métrico mínimo; não se está substituindo o fundo físico φ=id.

Rher é a álgebra real unital não nula dos escalares herdados, conservados ou fixados como na origem. Eles são constantes no espaço-tempo e inertes para os diferenciais. K e a normalização não nula κ do operador Einstein são reais fixados. Nada exige que Rher seja reduzida ou domínio. Não se apagam acoplamentos herdados, não se permite um coeficiente dependente do k da solução de teste e não se faz localização oculta num anel restrito de K variável.

Uma corrente desta investigação é uma combinação finita de contrações de UM W e UMA derivada covariante de W usando g0, sua inversa e ε0. Fatores de curvatura do fundo só acrescentam potências do K fixado; ∇bar Rbar=0. Nenhum vetor, tensor ou jato escalar externo não constante está disponível. Ambos os fatores podem ser escritos em ordem contrária; como W é bosônico, ∇W·W não é uma espécie adicional. A igualdade é no quociente linear prolongado de EOM, não módulo divergências.

A assinatura é η=diag(1,−1,−1,−1), com coordenadas (τ,x,y,z), z espacial e orientação dτ∧dx∧dy∧dz. Usamos

\[
R^a{}_{bcd}=\partial_c\Gamma^a{}_{bd}-\partial_d\Gamma^a{}_{bc}
+\Gamma^a{}_{uc}\Gamma^u{}_{bd}-\Gamma^a{}_{ud}\Gamma^u{}_{bc},
\quad
\bar R^a{}_{bcd}=K(\delta^a_c g_{0,bd}-\delta^a_d g_{0,bc}).
\tag{4}
\]

A estrela atua na última dupla de W. Nesta assinatura *²=−1 em duas-formas, ε^{0123}=−1/√|det g0|; métrica, volume e estrela são paralelos. A normalização J=½W·*W coincide com tr(W∧W)/vol da [nota083](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATO_DERIVADA_WEYL_083_20260910/CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md>).

W e seus jatos são s0-fechados off-shell por W(g0)=0 e naturalidade. Já as identidades usadas para REDUZIR correntes abaixo valem no shell linear. Seus restos off-shell são EOM/prolongamentos, isto é, imagens KT na comparação081. Não descartamos antifields do complexo nem identificamos essas duas afirmações.

## 2. Primeiro jato: a Bianchi elimina exatamente a parte contraída necessária à classificação

W tem simetrias de Riemann, Bianchi algébrica e traço zero. No shell Einstein linear,

\[
\bar\nabla^a W_{abcd}=0,\qquad
\bar\nabla_{[e}W_{ab]cd}=0.
\tag{5}
\]

São as identidades de Cotton/Bianchi linearizadas: o Schouten da família Einstein é Kg/2 até primeira ordem; sua derivada é zero nessa ordem, e W(g0)=0 elimina variações da conexão multiplicando Weyl de fundo. As mesmas relações valem para *W. Isso já foi justificado080/083; aqui só usamos a primeira ordem de derivada.

Complexificar a representação TENSORIAL no ponto é um meio de cálculo. Escreva V_C=S⊗S', com S,S' bidimensionais, e

\[
W_\mathbb C=\operatorname{Sym}^4S\oplus\operatorname{Sym}^4S'
=(2,0)\oplus(0,2).
\tag{6}
\]

Os pares (j,j') são spins, portanto dim(j,j')=(2j+1)(2j'+1). Em uma das quiralidades, ∇bar_{AA'}Ψ_{BCDE} decompõe-se como

\[
S\otimes\operatorname{Sym}^4S
=\operatorname{Sym}^5S\oplus\operatorname{Sym}^3S.
\]

O segundo termo é precisamente a contração ε^{AB}∇bar_{AA'}Ψ_{BCDE}; (5) o anula. Resta o espinor χ_{ABCDE A'} totalmente simétrico nos cinco índices não pontuados. O conjugado fornece a outra quiralidade. Assim o primeiro jato admissível é um submódulo, ou pode ser tratado para o limite superior como um quociente, de

\[
\mathcal W_1=(5/2,1/2)\oplus(1/2,5/2).
\tag{7}
\]

Nesta ordem a afirmação é exata, não apenas sobre o símbolo graduado: não se comutaram DUAS derivadas e não há um termo K·W inferior faltando em (7). Eventuais relações adicionais do quociente completo só podem DIMINUIR o espaço de correntes. Não precisamos presumir liberdade de toda a torre nem realizabilidade arbitrária de todos os jatos para obter o limite superior.

[KNOWN — controle primário delimitado] [Vasiliev, hep-th/9611024v2, §9, equações87–89](https://arxiv.org/pdf/hep-th/9611024) escreve a Bianchi de Weyl exatamente como o espinor com cinco índices de uma quiralidade e um da outra. As equações90–91 distinguem os termos inferiores de curvatura nas ordens seguintes. Essa remissão apoia a organização do primeiro jato; não importamos a equivalência não linear inteira ou o sinal de λ² dessa fonte. A [parametrização de Torre, equação8](https://arxiv.org/pdf/gr-qc/9508005) é uma referência sobre a linguagem de jatos, mas seu domínio Ricci-flat não é usado para substituir K>0 por K=0.

## 3. Contagem de todas as contrações e sua forma explícita

Um vetor W·∇W é um intertwiner da isotropia entre \(\mathcal W_0\otimes\mathcal W_1\) e V. O uso de ε permite ambos os setores de paridade; produtos de duas ε reduzem-se a deltas/métricas. A complexificação não muda a pergunta de existência de contrações tensoriais.

Na mesma quiralidade,

\[
(2,0)\otimes(5/2,1/2)
=\bigoplus_{j=1/2,3/2,5/2,7/2,9/2}(j,1/2),
\tag{8}
\]

portanto V=(1/2,1/2) aparece UMA vez. A quiralidade conjugada contribui outra. Nos produtos cruzados,

\[
(2,0)\otimes(1/2,5/2),\qquad
(0,2)\otimes(5/2,1/2),
\]

um dos spins é fixamente 5/2; V não aparece. A multiplicidade complexa total é dois. A conjugação da forma real Lorentziana troca esses dois somandos, dando dimensão real dois, não quatro.

A única contração de uma quiralidade, a menos de fator, é

\[
T_{AA'}=\Psi^{BCDE}\chi_{ABCDE A'}
=\tfrac12\,\bar\nabla_{AA'}(\Psi^{BCDE}\Psi_{BCDE}).
\tag{9}
\]

O sinal é o usual de Leibniz: são campos bosônicos e a forma bilinear em Sym⁴S é simétrica. O conjugado fornece o outro gradiente. Com \(W_\pm=(W\mp i*W)/2\),

\[
W_\pm\cdot W_\pm
=\tfrac12(W\cdot W\mp iW\cdot *W)=I\mp iJ.
\tag{10}
\]

Assim os dois intertwiners reais são precisamente grad I e grad J, até normalizações reais constantes absorvidas em A,B. Esta conta dá um limite superior para as correntes no quociente efetivo; §5 prova que os dois sobrevivem independentemente.

**Por que isso cobre contrações, e não somente uma contagem formal.** O espaço em questão envolve só W e seu primeiro jato; é finito dimensional antes das relações. As Bianchi/traços/divergências são mapas equivariantes de módulos tensoriais finitos. A isotropia tem álgebra semissimples, logo seus módulos finitos são completamente redutíveis; tomar invariantes/intertwiners é exato. Uma corrente natural no quociente não ganha novos intertwiners que não existam antes. Pode-se complexificar, usar SU(2)×SU(2) para projetar em um corte FINITO, e tomar a parte real; não se faz média sobre o grupo Lorentz não compacto.

Os intertwiners (9–10) já foram realizados por contrações com g0 e ε. O resultado é, portanto, independente do frame ou da apresentação espinorial auxiliar. Não se escolheu um frame físico, uma conexão diferente de ∇bar ou um spinor externo. Não se invoca local finitude sob toda a álgebra de Killing: a conta é somente de isotropia finita.

Como controles de normalização, seguem identidades tensoriais no shell:

\[
\begin{aligned}
W^{cdef}\bar\nabla_bW_{cdef}&=\bar\nabla_b I,\\
W^{cdef}\bar\nabla_b(*W)_{cdef}&=\bar\nabla_b J,\\
W_{acde}\bar\nabla^aW_b{}^{cde}&=\tfrac12\bar\nabla_b I,\\
W_{acde}\bar\nabla^a(*W)_b{}^{cde}&=\tfrac12\bar\nabla_b J.
\end{aligned}
\tag{11}
\]

As duas últimas seguem, usando div W=0, das identidades quadráticas quatro-dimensionais

\[
W_{acde}W_b{}^{cde}=\tfrac14g_{0,ab}W^2,\qquad
W_{acde}(*W)_b{}^{cde}=\tfrac14g_{0,ab}(W\cdot *W).
\tag{12}
\]

Uma demonstração finita de(12): Sym²\(\mathcal W_0\) tem tipos (0,0) duas vezes, (2,0),(0,2),(4,0),(0,4),(2,2), e não contém os tipos de um tensor de posto dois sem traço, (1,1),(1,0),(0,1). A parte quadrática dos tensores do lado esquerdo só pode ser proporcional a g0; tomar o traço fixa 1/4. Isso também cobre o tensor misto com estrela, por ser polinomial quadrático no MESMO W. Já W_b cde ∇bar_a W^{acde}=0 e sua versão dual são diretamente (5).

## 4. A imagem de divergência: termo de curvatura conservado

A conexão atua em todos os quatro slots covariantes de W. No shell linear, a Bianchi diferenciada e a divergência nula dão

\[
\bar\Box W_{abcd}
=-g_0^{ef}[\bar\nabla_f,\bar\nabla_c]W_{abde}
-g_0^{ef}[\bar\nabla_f,\bar\nabla_d]W_{abec}.
\]

Na convenção(4), cada índice covariante contribui −R e a primeira contração é

\[
K(W_{cbda}+W_{acdb}-2W_{abcd})=-3K W_{abcd}.
\]

A segunda também é −3KW. Logo

\[
\bar\Box W=6KW,\qquad \bar\Box(*W)=6K(*W).
\tag{13}
\]

É o cálculo covariante083, com [revisão independente específica](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md>). Não se substituiu ∇bar por derivada plana.

Defina

\[
I_1=\tfrac12(\bar\nabla_eW_{abcd})(\bar\nabla^eW^{abcd}),\qquad
J_1=\tfrac12(\bar\nabla_eW_{abcd})(\bar\nabla^e(*W)^{abcd}).
\]

Leibniz, paralelismo das contrações e (13) fornecem

\[
\boxed{\bar\Box I=12KI+2I_1,\qquad
\bar\Box J=12KJ+2J_1.}
\tag{14}
\]

Portanto a imagem procurada é

\[
A(12KI+2I_1)+B(12KJ+2J_1),
\tag{15}
\]

equivalentemente(2). Não se pode remover o termo J1 por decreto para resolver J mediante B=1/(12K): os termos de primeira derivada são parte do MESMO operador. O teste a seguir prova a independência e a impossibilidade, em vez de pressupor que todos os invariantes dos jatos são livres.

## 5. Independência no quociente por soluções Einstein completas na vizinhança

Usamos somente a [família TT078, retomada081](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md>):

\[
g_0=(\ell/z)^2\eta,\quad a=\ell/z,\quad
h=a^2\gamma,\quad
\gamma_{11}=f\cos(k\tau),\quad
\gamma_{22}=-\gamma_{11},\quad
\gamma_{12}=f\sin(k\tau),
\]
\[
f''-2f'/z+k^2f=0,\qquad f(z_0)=0,\quad f'(z_0)=1,\quad z_0=\ell.
\tag{16}
\]

Ela satisfaz H0h=0 em toda uma vizinhança, incluindo TODOS os prolongamentos. Assim as avaliações descem ao quociente, não apenas a um conjunto de equações no ponto. O k varia entre soluções no mesmo fundo. Nenhum elemento de Rher é avaliado numericamente: tensorizamos o funcional real com a identidade de Rher.

Nas formas Weyl081 com índices internos abaixo, E=(k²f−f'/z)/2 e B=kf'/2,

\[
\widetilde W_{01}=E e^{01}+B e^{23},\quad
\widetilde W_{02}=-E e^{02}+B e^{13},\quad
\widetilde W_{13}=B e^{02}+E e^{13},\quad
\widetilde W_{23}=B e^{01}-E e^{23}.
\]

Somar os quatro pares com os sinais ηaaηbbηccηdd e os quatro representantes de cada dupla antissimétrica dá

\[
\widetilde W_{abcd}\widetilde W^{abcd}=16(E^2-B^2),\qquad
I=8a^{-4}(E^2-B^2).
\tag{17}
\]

O tensor Weyl covariante físico é a² vezes o tilde; suas quatro elevações dão o fator a^-4 final em(17). Para J, a conta081 já fornece tr(W∧W)=16EB vezes o volume coordenado, antes da divisão por a⁴.

Na solução k=0, p=f' satisfaz p'=2p/z, p(z0)=1, de modo que p=(z/z0)². Então

\[
J=0,\qquad I=\frac{2z^6}{\ell^4 z_0^4}.
\]

Para um escalar dessa solução dependente apenas de z,

\[
\bar\Box F=\frac{z^2}{\ell^2}(-F''+2F'/z).
\tag{18}
\]

Antes de avaliar, \(\bar\Box I=-18I/\ell^2\). Em p0, depois de impor ell=z0,

\[
I'(p_0)=12/z_0^3,\qquad \bar\Box I(p_0)=-36/z_0^4.
\tag{19}
\]

São contas escritas de(16–18), não execução nova de CAS.

Na solução k=1/z0, os perfis081/083 fornecem

\[
J'(p_0)=-24/z_0^3,\qquad
\bar\Box J(p_0)=56/z_0^4.
\tag{20}
\]

Se A grad I+B grad J=0, a componente covariante z em k=0 dá A=0 por(19), e k=1/z0 dá B=0 por(20). Para a igualdade A□I+B□J=0, a mesma sequência com os outros dois valores dá A=B=0. Todos os fatores cancelados são reais não nulos, portanto unidades em QUALQUER álgebra real unital, inclusive com nilpotentes.

Isso paga as duas independências usadas em(1–2). Em particular, nesse setor não há corrente de divergência nula não zero como classe on-shell. Termos que já são zero modulo EOM não são contados como correntes novas.

## 6. J não pertence à imagem; mesmo o canal Euler invariante não ajuda

Na família(16), f depende de k². O invariante I é par em k e J é ímpar. Geometricamente, a reflexão de y leva h(k) a h(−k) e preserva g0; I não contém ε, enquanto J contém uma ε. Essa afirmação só compara soluções com a orientação previamente fixada; não restringe o anel Rher a coeficientes de paridade particular.

A simetria helicoidal de083, translação em τ compensada por rotação no plano xy, garante que I e J são independentes de τ em toda a vizinhança; x,y já estão ausentes. Portanto □I também é par e □J ímpar. Não foi omitida uma derivada temporal de um perfil conhecido apenas em τ=0.

Primeiro, suponha J=A□I+B□J. Tome a diferença das avaliações k e −k e divida por2. Resta J=B□J. Os valores

\[
J(p_0)=-4k/z_0,\qquad
\bar\Box J(p_0)=112k/z_0^3-56k^3/z_0
\tag{21}
\]

dão, para k=1/z0 e k=2/z0 respectivamente,

\[
-4/z_0^2=(56/z_0^4)B,\qquad
-8/z_0^2=(-224/z_0^4)B.
\]

A primeira força B=−z0²/14; a segunda força B=z0²/28. A diferença é um real não nulo vezes a unidade de Rher. Assim J não está na imagem(2).

Para permitir o canal Euler, use o [critério084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>):
\(J=\operatorname{div}V+K^2f\), com f∈N^g. A invariância sob as transvecções impõe ∇bar f=0 no quociente. Derive em z e tome a parte ímpar k↔−k. O termo de A□I desaparece por paridade e f desaparece por invariância, sem exigir sua paridade nem sua nulidade. Fica

\[
J'(p_0)=B(\bar\Box J)'(p_0).
\tag{22}
\]

A [conta covariante084](<C:/IALD/Central de Patentes/Chatgpt/CORRENTE_NECESSARIA_E_LIMITE_GRADIENTE_084_20260910/EULER_SOZINHO_E_GRADIENTE_ESCALAR_NAO_BASTAM.md>) deriva mantendo K=ell^-2 fixo, e só DEPOIS põe ell=z0:

\[
J'=4k^3-28k/z_0^2,\qquad
(\bar\Box J)'=16k^5-656k^3/z_0^2+784k/z_0^4.
\]

Em k=1/z0 e k=2/z0, respectivamente,

\[
-24/z_0^3=(144/z_0^5)B,\qquad
-24/z_0^3=(-3168/z_0^5)B.
\tag{23}
\]

Subtrair força (3312/z0⁵)B=0, logo B=0; qualquer equação então contradiz a não nulidade de −24/z0³. Isso prova(3), para qualquer A e qualquer f admissível invariante.

A nova [investigação085 de N^g](<C:/IALD/Central de Patentes/Chatgpt/INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md>) trata a nulidade desse módulo por outro argumento. A presente exclusão NÃO depende de aceitar sua conclusão: mantém f arbitrário invariante até a derivação(22). Não há autovalidação cruzada de085.

## 7. Alcance operacional e limites

[DERIVED] A corrente horizontal q_V associada a V tem dCE q_V=(div V)ν pela identificação082/084. Assim a exclusão não se limita a uma escolha de cúbica de ghosts: dentro da forma normal084, todo o setor horizontal W·∇W falha na equação-alvo, inclusive com o canal Euler permitido. Não se confundiu s0 com dH; as relações lineares de EOM foram mantidas no módulo, e as avaliações anulam seus prolongamentos.

[DERIVED] A classificação é de jatos covariantes com exatamente uma derivada total entre dois Weyl lineares. Vetores sem derivada não aparecem em Sym²W por representação/paridade de índices. Fatores constantes K ou κ só mudam os coeficientes A,B. A valência de campo continua dois; acrescida dos três ghosts horizontais, continua E5. Não se criou série infinita de jatos nem mudou o número de pernas por esse cálculo.

[OPEN] Não foram classificados vetores com três, cinco ou mais derivadas totais, como W∇³W e ∇W∇²W, nem somas arbitrárias finitas dessas ordens. A filtração dessas ordens pode misturar termos inferiores por curvatura; (7) não foi estendido sem prova. A corrente de energia com um Killing externo também pertence a outra categoria, pois aqui nenhum vetor externo está disponível.

[OPEN] Não se conclui a impossibilidade de toda primitiva do alvo, a presença de uma anomalia efetiva, QME, contratermos admissíveis T5/T9/T11, transporte entre fundos ou solução UV. O fundo físico sigma não constante, espectadores tensoriais e um anel universal restrito em K variável continuam fora do teorema. I,J têm dimensão de engenharia quatro, seus gradientes cinco e divergências seis; coeficientes podem compensar unidades, mas essa observação dimensional não verifica as condições causais de renormalização.

[REAL — custódia] Somente arquivos novos nesta pasta086. O manifesto mede oito fontes e o emissor antes/depois da gravação documental; essa janela não é apresentada como auditoria de cada minuto anterior da investigação. Não foi executado nenhum código matemático fonte, programa canônico, Lean ou CAS. A conferência representacional curta recebida de Turing cobriu(8) e a dimensão real; não é aprovação independente integral desta nota.
"""
links = re.findall(r"\]\(<(C:/[^>]+)>\)", note)
assert all(Path(p).is_file() for p in links)
note_pin = new("CLASSIFICACAO_CORRENTES_W_NABLA_W_E_DIVERGENCIA.md", note.encode("utf-8"))
after = [pin(ROOT / rel) for rel in SOURCES]
assert before == after and script_before == pin(Path(__file__))
record = {
    "status": "WRITTEN_DERIVATION_AWAITING_INDEPENDENT_FULL_REVIEW",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "W times one covariant derivative of linear Weyl, Einstein spaceform4D, fixed K and inert scalar coefficient ring",
    "sources_before": before, "sources_after": after, "all_sources_unchanged": True,
    "script_before": script_before, "script_after": pin(Path(__file__)), "note": note_pin,
    "local_links_checked": len(links), "new_math_executions": 0, "new_lean_executions": 0,
    "um_executed_or_imported": False, "originals_written": False,
    "primary_sources_consulted": [
      {"url": "https://arxiv.org/pdf/hep-th/9611024", "part": "v2 section9 equations87-91", "role": "first covariant Weyl jet; no nonlinear theorem imported"},
      {"url": "https://arxiv.org/pdf/gr-qc/9508005", "part": "equation8", "role": "spinor jet language only; not used to replace K>0 by Ricci-flat"}
    ],
    "claims": ["two independent currents gradI,gradJ", "image freely spanned by boxI,boxJ",
               "J outside that image even modulo K^2 invariant Euler coefficient"],
    "not_claimed": ["classification of all derivative orders", "nonexistence of every primitive", "QME", "UV", "physical sigma background closure"]
}
receipt_pin = new("MANIFESTO_CORRENTES_UMA_DERIVADA_086.json", (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"note": note_pin, "manifest": receipt_pin, "sources_preserved": len(before),
                  "links": len(links), "new_math_runs": 0}, ensure_ascii=False))

