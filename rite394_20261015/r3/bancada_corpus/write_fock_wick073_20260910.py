from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'FOCK_HADAMARD_QUARTETOS_073_20260910'
POL = ROOT / 'POLARIZACAO_BRST_HADAMARD_073_20260910/POLARIZACAO_ADAPTADA_E_MAJORANTE.md'
paths = [POL,
 ROOT / 'RADICAL_GNS_BRST_073_20260910/RADICAL_DA_PSEUDOCOVARIANCIA_E_P0.md',
 ROOT / 'RADICAL_GNS_BRST_073_20260910/REPARO_DO_BLOCO_E_LIMITE_HADAMARD.md',
 ROOT / 'POSITIVIDADE_BRST_FORMAL_072_20260910/ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md',
 ROOT / 'POSITIVIDADE_BRST_FORMAL_072_20260910/PRECISAO_COMUTADOR_GRADUADO_E_R0.md',
 ROOT / 'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md']

def pin(p):
    raw = p.read_bytes()
    return {'path': p.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

pins = [pin(p) for p in paths]
OUT.mkdir(exist_ok=False)

def write_new(path, value):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    raw = value.encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

note = r'''# Representação Fock, domínio Wick e positividade BRST livre

10/09/2026, arco073. [DERIVED — demonstração escrita] [KNOWN — ferramentas microlocais indicadas]. Esta nota compõe a polarização adaptada073 com a representação de estados. Não executa um.py, Lean ou CAS e não altera fontes congeladas. O estatuto final depende da revisão conjunta das duas construções; os recibos documentais não substituem essa revisão.

**Resultado.** Dadas as propriedades explicitadas da polarização adaptada073, a sua pseudocovariância possui uma representação Fock–Krein com domínio denso comum de funções de onda suaves, preservado pela carga livre, pela homotopia e pelos operadores Wick polinomiais compactos microcausais. Nesse domínio, ker Q0 é positivo e todo vetor fechado nulo é Q0-exato. Isso realiza P0 no modelo e domínio indicados. Também realiza a parte representacional de P1 para os coeficientes compactos polinomiais da construção causal069. A existência da carga interagente renormalizada com todas as identidades de P2, a QME, a remoção da anomalia e o estado físico interagente continuam obrigações.

## 1. Dados consumidos: a mesma covariância, não outra representação escolhida por nome

A [polarização adaptada](<C:/IALD/Central de Patentes/Chatgpt/POLARIZACAO_BRST_HADAMARD_073_20260910/POLARIZACAO_ADAPTADA_E_MAJORANTE.md>) fornece projetores complementares puros Pi_D e Pi_Q, compatíveis com a conjugação, auto-adjuntos para as formas de Cauchy e com orientação Hadamard. Fornece ainda mapas reais de ordem pseudodiferencial espacial finita q,c,k,r,p,s0,R, que preservam C-infinito, com

\[
u=R s_0u+kqu+rcu,\quad s_0R=1,\quad R s_0=p,
\qquad qk=cr=1,\quad qr=ck=0.
\tag{1}
\]

Os projetores novos entrelaçam exatamente k,c e são obtidos dos iniciais por mudanças suavizantes. O bloco físico é o estado067, não uma covariância física ajustada para melhorar os sinais. Em uma partícula, a forma bosônica é

\[
B(u,v)=A_{067}(s_0u,s_0v)
       +\ell G(qu,cv)+\ell G(cu,qv),\qquad \ell>0.
\tag{2}
\]

G é a forma ghost da frequência escolhida; pode ser indefinida. O bloco de vínculos e o bloco físico–vínculos são zero. Consequentemente, antes de passar à frequência positiva, o radical é N_A ⊕ k N_G ⊕ r N_G. As condições S1 e S2 da [análise do radical](<C:/IALD/Central de Patentes/Chatgpt/RADICAL_GNS_BRST_073_20260910/RADICAL_DA_PSEUDOCOVARIANCIA_E_P0.md>) são satisfeitas. Não se usa a pseudocovariância arbitrária068 como se essa propriedade já estivesse garantida.

A pureza permite realizar o quociente por cada radical como a imagem do respectivo projetor. No setor físico, isso dá H_phys, com norma positiva determinada pelos modos S/V/TT067. No setor ghost, dá o espaço Krein K. O lema de majorante da polarização fornece um produto Hilbert positivo ( , )_K e uma simetria fundamental eta_K, com eta_K²=1,

\[
G(v,w)=(v,\eta_Kw)_K.
\tag{3}
\]

Eta_K e as identificações preservam os dados suaves. A propriedade decorre do cálculo funcional de um operador Hilbert auto-adjunto elíptico de ordem zero com gap; não se toma o sinal de uma matriz Krein arbitrária. A norma total será puxada da soma dos blocos de (2). Não é afirmado que k,c sejam limitados no Sobolev padrão dos campos originais.

## 2. Normalização dos quartetos e Fock

A graduação e as fases constantes dos vetores ghost são as da seção 2 da análise do radical073, compatíveis com a involução cbar*=-cbar e s cbar=-b do dicionário069. Elas dão o complexo de uma partícula a→k a, u→ell c u. Reescale o levantamento dos vínculos por ell^{-1}; ambos os mapas passam a ter coeficiente um e os dois pareamentos cruzados ficam iguais a G.

Chame de b† e c† os criadores bosônicos das duas parcelas auxiliares, e a† e d† os criadores fermionicos, com ghost -1 e +1. Substituir simultaneamente c†(v) e d†(v) por c†(eta_K v) e d†(eta_K v) transforma os dois pareamentos cruzados em ( , )_K e conserva as setas do complexo. Essa é uma mudança explícita de coordenadas na forma (2), não uma troca de sua função de dois pontos.

Obtemos a Fock Hilbert subjacente

\[
\mathscr F=\Gamma_s(H_{\rm phys}\oplus K_b\oplus K_c)
            \widehat\otimes\Gamma_a(K_a\oplus K_d).
\tag{4}
\]

O produto indefinido é [Psi,Phi]=(Psi,eta_F Phi), onde eta_F é a segunda quantização das trocas b↔c, a↔d e da identidade física. É uma involução Hilbert limitada, de modo que a forma é contínua e não degenerada. Seu adjunto de criadores produz

\[
[b(v),c^\dagger(w)]=[c(v),b^\dagger(w)]=(v,w)_K,
\quad
\{a(v),d^\dagger(w)\}=\{d(v),a^\dagger(w)\}=(v,w)_K,
\tag{5}
\]

com as demais contrações auxiliares iguais a zero. Os campos físicos têm suas CCR positivas usuais. O asterisco/adjunto aqui é o de Krein quando aplicado aos campos; os operadores de criação na apresentação Hilbert são transportados pela forma indicada.

Os campos do modelo são reconstruídos pelos mapas de (1), pelos projetores e pelas fases acima. As contrações de vácuo reproduzem (2) e a matriz completa de covariâncias BRST. Pela regra de Wick, reproduzem todos os funcionais gaussianos polinomiais. A evolução hiperbólica e a propriedade de faixa temporal fornecem os testes compactos que geram dados suaves de Cauchy; logo esse vácuo é cíclico num subdomínio denso. Não foi aplicada uma construção GNS positiva à álgebra auxiliar indefinida.

## 3. Um domínio maior que os tensores algébricos simples

Seja E_+ o espaço nuclear dos dados suaves nas imagens positivas física e ghost, com as quatro cópias auxiliares. Use a topologia induzida por todas as normas Sobolev; os projetores e eta_K preservam esse espaço. Defina

\[
\mathscr D=\bigoplus_{N\ge0}^{\rm alg}
              \operatorname{Sym}_{\rm gr}^{N}
                     (E_+^{\widehat\otimes N}).
\tag{6}
\]

O produto tensorial dentro de cada grau é o **completado nuclear**: funções de onda suaves em produtos de superfícies de Cauchy, com a simetria/antissimetria apropriada. Só a soma dos graus de partícula é algébrica. Uma função de onda suave de duas partículas não precisa ser uma soma finita de tensores simples. Essa distinção remove a insuficiência do domínio puramente polinomial apontada na análise073.

E_+ é denso na respectiva Hilbert e C-infinito em S3 está contido em todos os Sobolev. Portanto D é denso em F. Todos os mapas de uma partícula que são contínuos nos dados suaves, e suas somas finitas nos slots de cada N, preservam D. A projeção P sobre Fock física com vácuo auxiliar também o preserva.

## 4. Carga e homotopia no mesmo domínio

No espaço de uma partícula defina d a†=b†, d c†=d†, d b†=d d†=0; o símbolo d† nessa expressão é o criador do ghost positivo, não o adjunto do diferencial. Defina j b†=a†, j d†=c†, j a†=j c†=0. Ambos anulam as partículas físicas. Então d²=j²=0 e dj+jd é a projeção auxiliar.

Prolongue d e j como derivação graduada nos slots, obtendo Q0 e h. Equivalentemente, para uma base Hilbert de K,

\[
Q_0=\sum_i(b_i^\dagger d_i+d_i^\dagger b_i),\qquad
h=\sum_i(a_i^\dagger c_i+c_i^\dagger a_i).
\tag{7}
\]

As somas significam os operadores de segunda quantização: em grau N cada operador é a soma de N mapas de um slot. Não são somas de criadores de pares sobre o vácuo. A definição é independente da base e contínua no espaço suave de cada grau. Não há divisão por uma frequência possivelmente nula.

Os termos em slots distintos cancelam no anticomutador pelas regras graduadas. Os termos no mesmo slot dão a identidade auxiliar. Assim, em D,

\[
Q_0^2=0,\qquad Q_0h+hQ_0=N_{\rm aux},\qquad
Q_0P=PQ_0=hP=Ph=0.
\tag{8}
\]

A forma cruzada (5) torna Q0 e h simétricos para [ , ]; também se confere isso diretamente nos quatro geradores e depois por tensorização. No núcleo suave estamos afirmando simetria no domínio, não uma auto-adjunticidade Hilbert inexistente de um operador nilpotente não nulo.

Defina N_aux^{-1} como 1/m no setor de m>0 partículas auxiliares e zero em m=0, e R0=N_aux^{-1}h. Como h conserva m, todos esses mapas preservam D e

\[
Q_0R_0+R_0Q_0=1-P.
\tag{9}
\]

Logo, para Psi fechado,

\[
\Psi=P\Psi+Q_0R_0\Psi,\qquad
[\Psi,\Psi]=\|P\Psi\|_{\rm phys}^{2}\ge0.
\tag{10}
\]

A segunda igualdade usa a simetria e nilpotência para anular os termos que contêm Q0. Se a norma é zero, P Psi=0 na Hilbert física positiva e Psi=Q0 R0 Psi. A recíproca vale pela mesma simetria/nilpotência. Portanto

\[
\{\Psi\in\ker Q_0\cap\mathscr D:[\Psi,\Psi]=0\}
       =Q_0\mathscr D,
\quad
H^0(\mathscr D,Q_0)\cong P\mathscr D.
\tag{11}
\]

É igualdade de imagem efetiva no domínio indicado, não apenas de seu fecho. Em outros ghosts a cohomologia é zero. O vácuo físico normalizado com vácuo auxiliar é fechado e induz o estado067. Isso prova P0 no domínio (6), consumindo a polarização e sua majorante.

## 5. Por que Wick local preserva o domínio suave

Precisamos verificar que D não é apenas um domínio conveniente para (7). Os mapas de amplitudes de criação são kernels de meia onda, seguidos pelos projetores e mapas pseudodiferenciais espaciais de ordem finita da polarização. Na covariável do espaço-tempo, cada parcela criadora tem a mesma orientação causal. A composição com a simetria fundamental/majorante preserva essa orientação, porque os operadores atuam dentro do ramo projetado e preservam C-infinito. A evolução é usada só em compactos interiores de I×S3.

Considere primeiro :Phi^m:(f), com f suave e compacto. No termo que cria m partículas a partir do vácuo, integram-se m desses kernels na mesma variável x contra f. Uma singularidade nas variáveis de Cauchy de saída exigiria que a soma das covariáveis em x fosse zero. Todos os termos não nulos dessa soma têm a mesma orientação causal; a soma não pode ser zero. O critério de composição/pushforward de frentes de onda implica que a função de onda criada é suave. Derivadas dos campos alteram a ordem, não essa orientação.

Para um termo com aniquiladores, a função de onda inicial em (6) é suave conjuntamente em todos os seus argumentos. A contração de um kernel de aniquilação com esses dados dá uma solução suave no argumento integrado e nos argumentos restantes. Depois dessa contração, aplica-se o argumento anterior às variáveis criadas. O número de partículas de saída continua finito e a aplicação é contínua entre os espaços suaves de cada grau, com seminormas que dependem de f, do grau e da ordem diferencial. Não se afirma uma cota uniforme em todos os graus ou uma extensão limitada em toda a Fock.

O mesmo argumento vale para um polinômio Wick com kernel compacto microcausal t_m(x1,...,xm): sua frente de onda exclui as configurações nas quais todas as covariáveis não nulas são futuras ou todas são passadas, incluindo zeros nas demais entradas. Após as contrações com as entradas suaves, uma possível singularidade de saída exigiria precisamente uma dessas configurações excluídas. Logo cada operador Wick polinomial compacto microcausal leva D em D.

[KNOWN] O uso de produtos e pushforwards sob essa condição de frente de onda é o cálculo microlocal padrão. [Hollands–Wald, seção 2.2, equações (9)–(11), Teorema 2.1](https://arxiv.org/html/gr-qc/0103074) constroem a álgebra Wick estendida por esses kernels e a involução/produto correspondentes. [Brunetti–Fredenhagen, seção 2, equação (11)](https://arxiv.org/pdf/math-ph/9903028) apresentam um domínio microlocal invariante. Aqui não se identifica D por nome com o domínio dessas fontes: o argumento anterior verifica diretamente a preservação das funções de onda suaves completadas. As formas indefinidas entram através de uma majorante Hilbert e mapas contínuos de uma partícula; as contrações de paridade ímpar acrescentam sinais, sem modificar as condições de frente de onda.

O produto e o adjunto dos operadores são os da álgebra graduada, pelo Wick finito, com [A,Q]_gr=-(-1)^|A|[Q,A]_gr quando Q é ímpar. As fases da realidade dos ghosts são mantidas. Não se representa uma série não polinomial inteira por somar infinitos operadores sem prova de convergência.

## 6. Compatibilidade BRST e representação dos coeficientes interagentes

A polarização entrelaça o complexo, então Q0 não mistura criadores e aniquiladores e anula o vácuo. Seu comutador graduado com um campo linear é a ação livre do dicionário, com o fator fixado i/hbar. A identidade vale nos produtos normais por Leibniz e pela invariância das contrações. As identidades (8)–(11) e a representação Wick vivem, portanto, no mesmo domínio D.

A [construção causal069](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md>) fornece, a cada ordem/truncagem e para inserções compactas, coeficientes Wick polinomiais com kernels microcausais renormalizados. A mudança suave da covariância auxiliar é transportada pela isomorfia de Wick finita coeficiente a coeficiente. Não exige refazer as distribuições renormalizadas nem muda a ação física.

Somas, produtos e os coeficientes da inversa formal da matriz S são operações finitas em cada grau da filtração pertinente. Por isso cada coeficiente de Bogoliubov R_V(F) atua em D e sua involução é representada pelo adjunto de Krein no mesmo domínio. Isso paga a existência representacional dos coeficientes compactos polinomiais e seu domínio comum, na classe já construída por069. Para fontes formais da referência072, a mesma conclusão é por grau externo, conservando a organização Laurent declarada; fontes centrais não ganham operadores propagantes.

Essa conclusão não prova que uma corrente renormalizada específica seja conservada, que a carga interagente implemente toda a Ward, ou que seu quadrado seja zero. Representar os coeficientes de uma expressão candidata não paga as identidades que essa expressão deve satisfazer. P2 continua sendo uma obrigação efetiva da interação e dos contatos. Tampouco se promove a simetria no núcleo a uma auto-adjunticidade não perturbativa de cada operador interagente.

## 7. Consequência para a recorrência072 e fronteira

Na [prova formal072](<C:/IALD/Central de Patentes/Chatgpt/POSITIVIDADE_BRST_FORMAL_072_20260910/ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md>), R0 deixa de ser uma escolha algébrica sem domínio: a fórmula (9) o realiza no domínio Wick comum. Uma vez construída a carga Q(z)=Q0+sum z^n Qn com as propriedades renormalizadas de P2 e coeficientes nesse domínio, a recorrência

\[
\psi_n=-R_0\sum_{j=1}^{n}Q_j\psi_{n-j}
\tag{12}
\]

permanece em D coeficiente a coeficiente. A prova de positividade e radical072 pode então ser consumida sem recolocar P0 como hipótese abstrata. Ela continua formal em z e não afirma convergência.

O avanço vale para a ação ambiente Einstein–sigma adotada, no fundo interior I×S3 e na representação construída. Não é um teorema de Hadamard/P0 para todos os fundos selecionados. Permanecem a anomalia geral/QME, a carga renormalizada, a comparação de fundos, a compatibilidade global/adiabática dos estados, a correspondência física de alcance geral e UV. A fase e o ramo já integrados não são reabertos.
'''
out_pin = write_new(OUT / 'FOCK_DOMINIO_WICK_E_P0.md', note)
for p, item in zip(paths, pins):
    assert pin(p) == item, 'Changed source: ' + str(p)
manifest = {'status': 'WRITTEN_FOCK_WICK_AND_P0_PROOF__COMPOSITION_REVIEW_PENDING',
            'created_utc': datetime.now(timezone.utc).isoformat(),
            'source_pins': pins, 'output': out_pin,
            'source_files_unchanged': True,
            'new_cas_controls': 0, 'new_lean_compilations': 0,
            'originals_written': False, 'um_executed_or_imported': False,
            'limits': 'Consumes adapted pure Hadamard polarization073 and its majorant. P0 on the smooth finite-particle Wick domain and compact polynomial coefficient representation; interacting P2/QME and general objective remain open.'}
mp = write_new(OUT / 'MANIFESTO_FOCK_WICK_073.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': manifest['status'], 'note': out_pin, 'manifest': mp}, ensure_ascii=True))
