from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

ROOT = Path('C:/IALD/Central de Patentes/Chatgpt').resolve()
OUT = ROOT / 'SOBREVIVENTE_PONTRYAGIN_077_20260910'
SOURCES = [
    ROOT / 'PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/S0_KILLING_E_PRIMEIRA_TRANSICAO.md',
    ROOT / 'TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md',
    ROOT / 'REVISAO_TRANSGRESSAO_BRST_076_20260910/PARECER_TRANSGRESSAO_TOTAL_E_GHOST4.md',
    ROOT / 'COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md',
]

NOTE = r'''# Sobrevivente de Pontryagin e levantamento natural até C₅

10/09/2026, contribuição077. [DERIVED — demonstração escrita, aguardando revisão independente específica]. Novos arquivos somente em Chatgpt; fontes congeladas preservadas. Zero CAS, Lean ou execução/importação de um.py.

**Resultado.** Na referência métrica de curvatura constante não nula, com sigma de fundo constante, a transgressão natural de Pontryagin076 tem um termo líder cúbico não nulo no setor CE residual. Seu truncamento até valência cinco é um ciclo BRST natural em C₅. O líder pertence, portanto, à imagem H³(C₅)→H³(C₃). Na categoria restrita em que a primeira transição077 tem imagem unidimensional, esse líder gera precisamente a linha sobrevivente. O resíduo da transgressão completa começa em valência pelo menos seis; sua eventual removibilidade cohomológica não foi decidida aqui.

## 1. Categoria, fontes e convenções

Usamos a apresentação métrica mínima, sem fontes externas θ/ω, sem o setor não mínimo de gauge fixing, com B0=(g0,φ0) inerte e on-shell. A referência satisfaz Ric(g0)=Λg0, K=Λ/3≠0, φ0 constante, e

\[
\bar R^a{}_{bcd}=K(\delta^a_c(g_0)_{bd}-\delta^a_d(g_0)_{bc}).
\tag{1}
\]

As perturbações dinâmicas permanecem off-shell, incluindo as perturbações sigma. A identidade de Pontryagin abaixo não exige suas EOM. A condição on-shell de B0 é usada para a filtração do complexo mínimo: não há termo KT constante que abaixe valência.

As fontes locais são: [primeira transição077](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/S0_KILLING_E_PRIMEIRA_TRANSICAO.md>), [transgressão076](<C:/IALD/Central de Patentes/Chatgpt/TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md>), seu [parecer independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_TRANSGRESSAO_BRST_076_20260910/PARECER_TRANSGRESSAO_TOTAL_E_GHOST4.md>) e a [classe Rees074](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>).

A fonte077 está em revisão; o sinal de seu bloco KT no §1 necessita uma precisão separada. A presente construção não usa aquele sinal nem conta classes com antifields. Usa sg=Lie_c g, sc=c·∂c e a ação desses operadores sobre expressões sem antifields. O resultado de unicidade da linha é explicitamente condicionado à contagem natural da primeira transição077; o ciclo construído e sua não nulidade no primeiro corte são verificados abaixo.

Fixe P(X,Y)=tr(XY). O polinômio convencional p₁=−tr(R∧R)/(8π²) multiplica todas as fórmulas por esse fator não nulo, sem mudar a linha cohomológica. A assinatura no controle de componentes será (+---), com orientação 0123. Defina g=g0+t h, c=tC, D=s+d_H. t é somente formal; cada jato de h, C, ξ ou antifield normalizado conta uma perna. C_N é o quociente por valências maiores que N, não um corte de ordem de derivadas.

## 2. Por que a densidade começa quadraticamente: prova por Weyl

Em um coframe ortonormal apenas usado para a identidade tensorial pontual, escreva a decomposição de curvatura

\[
R^a{}_b=W^a{}_b+B^a{}_b,
\qquad
B^a{}_b=e^a\wedge P_b-e_b\wedge P^a,
\tag{2}
\]

onde P_ab=½(Ric_ab−R g_ab/6) é o Schouten em dimensão quatro e P_a=P_ab e^b. Ele é simétrico. A curvatura de Weyl satisfaz a primeira Bianchi W^a{}_b∧e^b=0 e é antissimétrica nos índices métricos. Logo os dois termos de tr(W∧B) se anulam por Bianchi, um deles após trocar os índices antissimétricos.

Expandir tr(B∧B) produz quatro termos. Dois contêm a contração P_a∧e^a, zero pela simetria de P_ab; os outros contêm e^a∧e_a ou e_a∧e^a, zero pela simetria da métrica. Portanto

\[
\operatorname{tr}(W\wedge B)=0,
\quad \operatorname{tr}(B\wedge B)=0,
\quad
\boxed{\operatorname{tr}(R\wedge R)=\operatorname{tr}(W\wedge W).}
\tag{3}
\]

Não se trata de igualdade módulo divergência ou EOM; é uma identidade algébrica pontual. O coframe auxiliar usado para calculá-la não integra os dados da teoria nem introduz ghost de frame. O resultado é tensorial e vale também na assinatura Lorentziana.

[KNOWN] A expressão das formas de Pontryagin somente pelo Weyl é o resultado primário de [Avez, Characteristic Classes and Weyl Tensor: Applications to General Relativity (1970)](https://pmc.ncbi.nlm.nih.gov/articles/PMC283038/?page=3). O argumento explícito (2–3) verifica aqui o polinômio quadrático necessário; não depende de uma hipótese de conformalidade das perturbações. A transgressão característica é a de [Chern–Simons, §§3–4](https://math.mit.edu/juvitop/pastseminars/notes_2019_Fall/Chern-Simons.pdf).

Como g0 tem curvatura constante, W(g0)=0. A expansão formal regular tem a forma

\[
W(g_0+t h)=tW_{[1]}[h]+t^2W_{[2]}[h,h]+\cdots,
\quad
\operatorname{tr}(R(g)\wedge R(g))
=t^2\operatorname{tr}(W_{[1]}\wedge W_{[1]})+O(t^3).
\tag{4}
\]

Cada coeficiente tem exatamente a valência indicada em h; derivar h só troca seu jato. Assim os termos de ordens zero e um da densidade são identicamente nulos para quaisquer perturbações off-shell. Não basta somente Pontryagin(g0)=0: a informação adicional W(g0)=0 é o que anula também a primeira variação.

## 3. A transgressão exata e a ordem do resíduo

A fonte076 construiu, na vizinhança formal g=g0+t h,

\[
S=(g_0^{-1}g)^{1/2},\qquad
k=S(\nabla c)S^{-1}-(sS)S^{-1},
\qquad
\Omega=S\left(\tfrac12R^a{}_{bcd}(g)c^cc^d\right)S^{-1}.
\tag{5}
\]

k é g0-antissimétrica, tem ghost1 e forma zero; Ω tem ghost2. A identidade Ω=sk+k² e a transgressão dão

\[
T=\operatorname{tr}(k\Omega)-\tfrac13\operatorname{tr}(k^3),
\qquad
sT=A_P=\rho_P(g)c^0c^1c^2c^3,
\tag{6}
\]

onde tr(R∧R)=ρ_P(g)dx⁰dx¹dx²dx³. Mantém-se o termo sS; ele é necessário ao transporte métrico. Pela substituição c=tC e por (4),

\[
\boxed{A_P\in F^6,\qquad
(A_P)_{[6]}=\rho_{[2]}[h,h],C^0C^1C^2C^3,}
\quad
\rho_{[2]}dx^0dx^1dx^2dx^3
=\operatorname{tr}(W_{[1]}\wedge W_{[1]}).
\tag{7}
\]

A equação (7) é uma cota inferior de valência e uma expressão do primeiro coeficiente possível. Não afirma que ele seja diferente de zero em cada perturbação; setores especiais podem anulá-lo. Tampouco afirma que, quando não nulo como polinômio, ele represente uma classe cohomológica não trivial.

## 4. Líder cúbico e a linha CE

Ponha p^a=C^a e

\[
M^a{}_b=\tfrac12(\bar\nabla_bC^a-\bar\nabla^a C_b),
\qquad
\widehat R_0{}^a{}_b=Kp^ap_b.
\tag{8}
\]

O primeiro termo de (5) é

\[
k=tM+O(t^2),\qquad \Omega=t^2\widehat R_0+O(t^3).
\tag{9}
\]

De fato, S=1+½t g0⁻¹h+O(t²) e s0h=Lie_Cg0. Portanto a contribuição −sS retira exatamente a parte simétrica de ∇C. Resulta

\[
T=t^3\alpha_3+O(t^4),
\qquad
\boxed{\alpha_3=\operatorname{tr}(M\widehat R_0)
-\tfrac13\operatorname{tr}(M^3).}
\tag{10}
\]

A notação da077 usa m_ab=∇_[a C_b]. Os sinais não podem ser transportados pelo nome: M_ab=−m_ab. Como tr(M R̂0)=−K M_ab p^ap^b, a mesma expressão na notação077 é

\[
\boxed{\alpha_3=K m_{ab}p^ap^b
+\tfrac13\operatorname{tr}((m^a{}_b)^3).}
\tag{11}
\]

Trata-se da combinação par espaço-temporal feita com a métrica, sem epsilon; não é a combinação de Euler com a forma volume. Os dois termos têm ghost3, valência3 e peso de engenharia zero: [m]=0, [K]=2, [p]=−1. Não há divisão por K.

Há um controle de não nulidade sem cálculo computacional. Ponha p=0, anule os boosts e deixe somente m12=x, m23=y, m31=z, três geradores ímpares independentes. Com assinatura (+---), a matriz espacial de m elevado é

\[
\begin{pmatrix}0&-x&z\\x&0&-y\\-z&y&0\end{pmatrix}.
\]

Os seis caminhos cíclicos da diagonal do cubo valem −xyz cada um, usando a anticomutação. Assim

\[
\operatorname{tr}(m^3)=-6xyz,
\qquad \alpha_3|_{p=0,\,\mathrm{rot}}=-2xyz\ne0.
\tag{12}
\]

A condição de fechamento CE do líder segue também da expansão de (6): em valência quatro, s1α3+s0α4=0. No quociente dos jatos ghosts pelos prolongamentos de R0C, o segundo termo é zero, de modo que d_CE[α3]=0. Esse argumento usa somente a transgressão e os sinais já verificados; não precisa escolher o sinal do colchete das isometrias ambiente.

No teste077, W=V⊕Λ²V é o espaço dos dez dados Killing e o denominador natural de ghost3 em C3 contém d_CE(Λ²W)^G. Esse espaço de invariantes de grau dois é zero: Λ²V é adjunto, V⊗Λ²V não contém escalar, e a potência exterior segunda do adjunto Lorentz não contém bilinear alternada invariante. Os invariantes quadráticos de cada fator simples complexo são simétricos. Logo a cúbica natural não nula (12) não é uma fronteira nesse primeiro corte.

Se se consome a contagem077 de que a imagem de H³(C4)→H³(C3) tem dimensão um, (10–12) identificam seu gerador: é a linha de Pontryagin representada por α3. Não importo essa dimensão para a cohomologia universal sobre todos os fundos nem para H³ do complexo completo.

## 5. Levantamento finito explícito até C₅

A expressão exata (6) permite obter as correções sem resolver outra equação. Escreva

\[
k=\sum_{j\ge1}t^j k_j,\qquad
\Omega=\sum_{j\ge2}t^j\Omega_j.
\tag{13}
\]

Os primeiros coeficientes da transgressão são os seguintes polinômios finitos, com ciclicidade graduada do traço:

\[
\begin{aligned}
\alpha_3&=\operatorname{tr}(k_1\Omega_2)-\tfrac13\operatorname{tr}(k_1^3),\\
\alpha_4&=\operatorname{tr}(k_1\Omega_3+k_2\Omega_2)
 -\operatorname{tr}(k_1^2k_2),\\
\alpha_5&=\operatorname{tr}(k_1\Omega_4+k_2\Omega_3+k_3\Omega_2)
 -\operatorname{tr}(k_1^2k_3+k_1k_2^2).
\end{aligned}
\tag{14}
\]

Para determinar esses coeficientes, bastam (5), a conexão/curvatura métricas até as ordens indicadas e

\[
S=1+\tfrac12tA-\tfrac18t^2A^2+\tfrac1{16}t^3A^3+O(t^4),
\quad
S^{-1}=1-\tfrac12tA+\tfrac38t^2A^2-\tfrac5{16}t^3A^3+O(t^4),
\quad A=g_0^{-1}h.
\tag{15}
\]

As regras s_th=Lie_Cg0+tLie_Ch e s_tC=tC·∂C determinam os coeficientes de sS; portanto (14–15) são uma prescrição algébrica explícita, com número finito de derivadas e sem escolher preimagem de um operador. Só são necessárias k1,k2,k3 e Ω2,Ω3,Ω4. Nenhum coeficiente posterior entra em (14).

Defina

\[
T_{\le5}=t^3\alpha_3+t^4\alpha_4+t^5\alpha_5.
\tag{16}
\]

Como s não diminui valência no complexo mínimo sobre essa referência e sT∈F6, temos

\[
\boxed{sT_{\le5}=0\quad\text{em }C_5.}
\tag{17}
\]

Sua imagem em C3 é a classe não nula (12). Logo [T≤5] não pode ser uma fronteira em C5, pois sua restrição seria então uma fronteira em C3. Isto fornece um levantamento efetivo, sem antifields, da linha de Pontryagin até C5; não depende de excluir antifields da categoria completa para afirmar sua não nulidade, pois eles não podem produzir uma fronteira de ghost3/valência≤3.

Na categoria restrita com a dimensão077 da primeira imagem, a fatorização H³(C5)→H³(C4)→H³(C3) implica

\[
\dim\operatorname{im}[H^3(C_5)\to H^3(C_3)]=1.
\tag{18}
\]

A desigualdade superior vem da primeira transição; a inferior vem de (17) e (12). Não se afirma que H³(C5) inteiro seja unidimensional. A prova não usa a contagem de qualquer outro setor.

## 6. Por que a valência seis ainda é outra obrigação

O primeiro coeficiente possível A6 em (7) é o resíduo da TRANSGRESSÃO COMPLETA, não automaticamente o resíduo do truncamento (16). Escrevendo T=T≤5+t6α6+…, o grau seis obedece

\[
(sT_{\le5})_{[6]}=(A_P)_{[6]}-s_0\alpha_6.
\tag{19}
\]

Portanto um levantamento posterior pode modificar esse representante por uma correção. Por exemplo, uma primitiva s0 de A6, se existir na mesma categoria, poderá ser subtraída da correção α6. Antifields e as EOM lineares passam a participar dessas questões; não se pode julgar a exatidão apenas olhando o escalar de Weyl em (7).

W[1] é invariante sob s0 no fundo W0=0, pois sua variação linearizada por uma difeomorfia é Lie_C W0=0. Assim o coeficiente A6 é s0-fechado, como também decorre de s²T=0. Fechamento não decide exatidão. Esta nota não demonstra que A6 seja uma obstrução, nem que possa ser cancelado, nem que a classe se levante a todos os C_N.

Não há afirmação de estabilização de imagens em todos os cortes, de lim¹ nulo ou não nulo, de classe BRST formal completa, de anomalia efetiva não nula ou de QME. Também não se usa o fundo φ=id físico para este teste: a categoria aqui é a referência simétrica permitida com φ0 constante. A transgressão (5–6) é natural mais geralmente, mas a cota (7) utiliza W0=0 e a identificação da linha CE utiliza o teste077.

## 7. Rees e estatuto

Cada αn em (14) é homogêneo de valência n, com coeficientes naturais de B0 e jatos finitos. O fator tⁿ corresponde exatamente a essa valência, conforme a verificação076. Multiplicar (16) por t^(2L−2) dá um elemento da classe R_L; para L≥1 não há potências negativas. O índice L é aqui um rótulo algébrico de organização, não um laço calculado.

Não há ressoma em t numérico, inversão de gradiente sigma, conexão escolhida extra, fontes externas, mudança de assinatura ou especialização de uma homotopia ε-ádica. A raiz S é formal junto à identidade. A pertença à classe por valência não certifica a hierarquia de normalização causal, escala por aridade ou contatos.

[DERIVED] Pontryagin dá uma linha natural explicitamente levantada até C5 no teste077. Seu primeiro resíduo possível na transgressão completa está em valência seis, com expressão de Weyl em (7). A identidade de Weyl foi demonstrada aqui e o líder cúbico foi controlado por (12).

[INPUT — resultado077 em revisão] A contagem da primeira transição identifica essa linha construída com a única dimensão sobrevivente. Nenhuma aprovação da fonte077 ou desta nota foi atribuída a outro revisor.

[REAL — documental] O manifesto mede fontes antes/depois, nota, script e links. Zero CAS/Lean/um.py. Essas conferências documentais não são provas formais automáticas.

[OPEN] Exatidão admissível do resíduo e levantamento posterior, grupos completos e imagens estabilizadas, primitiva de anomalia e QME. Preservam-se os limites de076 e todos os originais.
'''


def pin(path):
    data = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}


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
note_path = OUT / 'PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md'
emit(note_path, NOTE.encode('utf-8'))
after = [pin(path) for path in SOURCES]
if before != after:
    raise RuntimeError('SOURCE_CHANGED: preserve output for diagnosis')
links = re.findall(r'\]\(<(C:/[^>]+)>\)', NOTE)
checks = [{'path': path, 'exists': Path(path).is_file()} for path in links]
if not all(item['exists'] for item in checks):
    raise RuntimeError('MISSING_LINK: preserve output for diagnosis')
manifest = {
    'kind': 'written_mathematical_contribution',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'author': '/root/prepare_integration_83',
    'status': 'DERIVED_WRITTEN_AWAITING_INDEPENDENT_REVIEW',
    'result': 'natural Pontryagin ghost3 lift through C5 on constant-curvature reference; full transgression residual in valence at least 6',
    'unique_line_identification': 'conditional on first-transition077 natural cohomology calculation under independent review',
    'source_pins_before': before,
    'source_pins_after': after,
    'sources_unchanged': before == after,
    'note': pin(note_path),
    'creator': pin(Path(__file__).resolve()),
    'local_links': checks,
    'references': [
        {'title': 'Avez 1970, Characteristic Classes and Weyl Tensor: Applications to General Relativity', 'url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC283038/?page=3', 'usage': 'primary bibliographic/abstract confirmation; quadratic identity proven in note'},
        {'title': 'Chern and Simons, Characteristic Forms and Geometric Invariants', 'url': 'https://math.mit.edu/juvitop/pastseminars/notes_2019_Fall/Chern-Simons.pdf', 'usage': 'graded transgression built in local source076; primary sections3-4'},
    ],
    'executions': {'CAS': 0, 'Lean': 0, 'um_py_execution_or_import': 0},
    'not_claimed': ['all-order lift', 'nontrivial cohomological obstruction at valence6', 'lim1 verdict', 'full H3/C5 dimension', 'QME', 'canonical integration', 'approval by other agent'],
}
manifest_path = OUT / 'MANIFESTO_SOBREVIVENTE_PONTRYAGIN_077.json'
emit(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'note': pin(note_path), 'manifest': pin(manifest_path),
                  'source_count': len(before), 'sources_unchanged': True,
                  'local_links_existing': len(checks)}, ensure_ascii=False))
