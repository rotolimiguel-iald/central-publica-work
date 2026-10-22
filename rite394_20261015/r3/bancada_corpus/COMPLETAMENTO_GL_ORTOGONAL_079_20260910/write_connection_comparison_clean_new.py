from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

ROOT = Path('C:/IALD/Central de Patentes/Chatgpt').resolve()
OUT = ROOT / 'COMPLETAMENTO_GL_ORTOGONAL_079_20260910'
SOURCES = [
    ROOT / 'LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md',
    ROOT / 'LIBERDADE_DE_LEVANTAMENTO_079_20260910/ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md',
    ROOT / 'TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md',
    ROOT / 'SOBREVIVENTE_PONTRYAGIN_077_20260910/PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md',
    ROOT / 'PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md',
    ROOT / 'RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md',
]
NOTE = r'''# Corrente quadrática e comparação explícita das conexões GL e ortogonal

10/09/2026. Investigação079 em pasta nova, fora da entrega078. [DERIVED — demonstração escrita, aguardando revisão independente]. Nenhum original, fonte congelada ou um.py alterado/executado/importado. Zero CAS e Lean.

**Resultado calculado.** A corrente J2=tr(L∧Dbar L) admite uma correção quadrática explícita F(−HL) que satisfaz

\[
\boxed{s_0\bigl(I_CJ_2+F(-HL)\bigr)=-s_1F(L).}
\tag{1}
\]

A definição natural de F está em (7). Esta identidade paga a equação da quinta valência para esse pacote particular, sem usar EOM ou antifields. Mas F(L) não satisfaz, em geral, a equação anterior s0F(L)=0; seu defeito é calculado em (11–12). Portanto o pacote não foi demonstrado pertencente ao núcleo K de079.

Além disso, a transgressão GL e a transgressão transportada para g0 são s-cohomólogas por uma primitiva natural formal explícita. A mudança de conexão sozinha não produz uma classe alternativa em H³(C5): conserva a classe específica já examinada078. Não se conclui daí que toda outra correção com o mesmo líder esteja excluída.

## 1. Objetos distintos e domínio comum

Mantemos g=g0+t h, c=tC, com φ0 constante, g0 espaço forma K=Λ/3>0 e B0 inerte. A apresentação é mínima, sem fontes θ/ω. t é formal. As convenções são sg=Lie_cg, sc=c·∂c, dx e c ímpares em grau total, e R=dΓ+Γ². Usa-se P(X,Y)=tr(XY), sem confundi-lo com o polinômio de Euler.

As fontes são a [transgressão076](<C:/IALD/Central de Patentes/Chatgpt/TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md>), a [expansão077](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md>), o [sistema079](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md>) e o seu [adendo de completação/coeficientes](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md>).

São usados dois objetos ligados por uma fórmula, não por homonímia:

- Na apresentação GL, v=∇^g c é uma zeroforma de ghost1, tensor de tipo (1,1), e Ω_GL=½R(g)^a_bμν cμcν.
- Na apresentação ortogonal transportada, S=(g0⁻¹g)^(1/2), k=S v S⁻¹−(sS)S⁻¹ e Ω_ort=S Ω_GL S⁻¹. k é g0-antissimétrica.

Não há ghost Lorentz independente nessas definições. A matriz S é a raiz formal junto à identidade, construída dos próprios g0 e h. As conexões GL e ortogonal não são identificadas sem transportar sua curvatura e o termo sS.

## 2. A transgressão de traço pode ser escrita antes do transporte métrico

A identidade076 para a conexão total A=Γ(g)dx+v fornece

\[
sv+v^2=\Omega_{\rm GL}.
\tag{2}
\]

O polinômio traço é invariante em GL, de modo que não é necessário transportar primeiro para so(g0) para escrever sua componente de ghost3:

\[
\tau_{\rm GL}=\operatorname{tr}(v\Omega_{\rm GL})
-\tfrac13\operatorname{tr}(v^3),
\qquad
s\tau_{\rm GL}=\operatorname{tr}(\Omega_{\rm GL}^2)=A_P.
\tag{3}
\]

Essa é a mesma densidade de Pontryagin A_P=ρ_P(g)c0c1c2c3 de077. A igualdade sτ_GL=A_P é também a identidade graduada de Chern–Simons aplicada à conexão de forma zero, com diferencial s. O cálculo é puramente algébrico; a transgressão ordinária por invariância/Bianchi está em [Chern–Simons, §3](https://math.mit.edu/juvitop/pastseminars/notes_2019_Fall/Chern-Simons.pdf).

Uma conexão GL arbitrária não é introduzida: v e Ω_GL são especificamente os derivados de g. O uso do traço aqui não fornece por si a mesma afirmação para Euler sem o transporte métrico da fonte076.

## 3. Coeficientes naturais nas valências quatro e cinco

Ponha H=g0⁻¹h. A diferença torsion-free das conexões é

\[
\Gamma(g)-\bar\Gamma=tL+t^2L_2+O(t^3),
\quad
L^a{}_{b\mu}=\tfrac12g_0^{ad}
(\bar\nabla_bh_{d\mu}+\bar\nabla_\mu h_{db}-\bar\nabla_dh_{b\mu}),
\quad L_2=-HL.
\tag{4}
\]

O produto HL atua no primeiro índice da conexão, não no índice da 1-forma. A relação L2=−HL vem diretamente da expansão de g⁻¹ na fórmula da diferença de Levi-Civita; L2 não é um tensor independente.

Para uma 1-forma End(TM) X de ghost zero, defina

\[
a(X)=I_CX=X_\mu C^\mu,
\qquad r(X)=I_C(\bar D X),
\qquad B=\bar\nabla C,
\qquad \Omega_0=\tfrac12\bar R^a{}_{b\mu\nu}C^\mu C^\nu
=K C^aC_b.
\tag{5}
\]

I_C substitui os geradores exteriores dx por C com a ordem exterior usual, incluindo o fator 1/p! quando se usam componentes totalmente antissimétricas. Não é declarado que I_C comute com d_H. Temos

\[
\begin{aligned}
v&=tB+t^2a(L)+t^3a(L_2)+O(t^4),\\
\Omega_{\rm GL}
&=t^2\Omega_0+t^3r(L)
 +t^4\bigl(r(L_2)+a(L)^2\bigr)+O(t^5).
\end{aligned}
\tag{6}
\]

Defina o operador linear em X

\[
\boxed{F(X)=\operatorname{tr}\bigl(B r(X)+a(X)\Omega_0-B^2a(X)\bigr).}
\tag{7}
\]

Ele é natural, de ghost3, linear nos jatos de X. Ao usar X=L tem valência4; com X=L2 tem valência5. As matrizes B,a(X) são ímpares; r(X),Ω0 são pares. Usar a ciclicidade GRADUADA do traço na expansão de (3) dá

\[
\begin{aligned}
\tau_3&=\operatorname{tr}(B\Omega_0)-\tfrac13\operatorname{tr}(B^3),\\
\tau_4&=F(L),\\
\tau_5&=\operatorname{tr}\bigl(a(L)r(L)\bigr)+F(L_2)
=I_CJ_2+F(-HL),\qquad J_2=\operatorname{tr}(L\wedge\bar D L).
\end{aligned}
\tag{8}
\]

Aqui τ_E é o coeficiente de t^E, não um grau de forma. Um cancelamento que importa em τ5 é tr(B a(L)²): ele aparece com sinal positivo em vΩ_GL e com sinal negativo no cubo de v. Os três termos cíclicos de cada composição ímpar têm o mesmo sinal. Esse cancelamento deixa exatamente F(L2) e I_CJ2 em (8).

## 4. Identidade de completamento e a primeira equação que ainda falha

No fundo W(g0)=0, a identidade tr(R∧R)=tr(W∧W) faz A_P começar em valência seis. Nas expressões sem antifields da apresentação com φ0 constante, s=s0+t s1 nos campos/ghosts. Comparar os coeficientes quatro e cinco de (3) fornece

\[
s_0F(L)=-s_1\tau_3,
\qquad
\boxed{s_0\bigl(I_CJ_2+F(-HL)\bigr)=-s_1F(L).}
\tag{9}
\]

Em particular, para a corrente original isolada, a identidade calculada é

\[
\boxed{s_0(I_CJ_2)
=-s_1F(L)-s_0F(-HL).}
\tag{10}
\]

O segundo termo do lado direito é uma correção quadrática local explícita, não uma EOM omitida. Esta é uma redução direta da tarefa de completar J2. Não foi necessário escrever um termo H0u·R(C4): esse termo é zero no pacote particular (8–10), pois nenhum antifield foi usado. Isso não significa que os antifields possam ser removidos da busca geral079.

Para que b4=F(L) e b5=I_CJ2+F(−HL) fossem um elemento do núcleo K, faltaria a primeira identidade s0b4=0. Pelo primeiro membro de (9), ela equivale a s1τ3=0 como identidade UNIVERSAL de jatos, e não somente após impor Killing. Ela é falsa em geral.

Um controle explícito usa coordenadas normais de g0 no ponto. Ponha somente C0(p)=θ não nulo entre os valores do ghost; escolha o bloco espacial de B como matriz antissimétrica

\[
B_{\rm esp}=\begin{pmatrix}0&x&-z\\-x&0&y\\z&-y&0\end{pmatrix},
\quad B^a{}_0=B^0{}_a=0,
\quad\partial_0x=\zeta,\quad\partial_0y=\partial_0z=0.
\tag{11}
\]

x,y,z,θ,ζ são jatos ímpares livres; z nesta equação é um nome de gerador, não a coordenada espacial do certificado078. Os segundos jatos correspondentes podem ser escolhidos compatíveis com a simetria de derivadas parciais. Como há somente um valor não nulo de C, os produtos CμCν e as contribuições Ω0 se anulam no teste. O termo tr(B³)=6xyz fornece τ3=−2xyz. De s1B=−B²+C·∂B nessa especialização, da nulidade tr(B⁴)=0 e da regra graduada, segue

\[
s_1\tau_3=-2\theta\zeta yz\ne0,
\qquad s_0F(L)=+2\theta\zeta yz\ne0.
\tag{12}
\]

Termos de curvatura de fundo contêm dois valores C e se anulam aqui. O teste é off-shell e não impõe que o ghost seja Killing; essa liberdade é necessária para verificar a equação universal de fechamento. Assim (9) completa a corrente dentro da transgressão que já possui o líder τ3, mas não a transforma automaticamente numa correção que começa em valência quatro e pertence a K.

## 5. A diferença GL–ortogonal é s-exata por fórmula explícita

Esta comparação pode ser feita sem adivinhar uma conexão Lorentz. Defina

\[
u=S^{-1}sS,\quad su=-u^2,
\quad k=S(v-u)S^{-1},\quad
\Omega_{\rm ort}=S\Omega_{\rm GL}S^{-1}.
\tag{13}
\]

u e v têm ghost1 e são matrizes ímpares. Para a transgressão ortogonal de077,
τ_ort=tr(kΩ_ort)−tr(k³)/3. Expandir o cubo e usar tr((v−u)³)=tr(v³)−3tr(v²u)+3tr(vu²)−tr(u³) dá

\[
\boxed{\tau_{\rm ort}-\tau_{\rm GL}
=s\operatorname{tr}(uv)+\tfrac13\operatorname{tr}(u^3).}
\tag{14}
\]

O sinal pode ser conferido diretamente: os termos com u v² cancelam e
s tr(uv)=−tr(u²v)−tr(u sv). Se v=0, k=−S u S⁻¹ e a diferença se reduz a +tr(u³)/3, de acordo com (14).

O termo final é também s-exato na vizinhança FORMAL usada aqui. Tome a família auxiliar

\[
S_\rho=(1+\rho tH)^{1/2},\quad
u_\rho=S_\rho^{-1}sS_\rho,\quad
a_\rho=S_\rho^{-1}\partial_\rho S_\rho,
\qquad 0\le\rho\le1.
\tag{15}
\]

O diferencial s permanece o do campo g=g0+t h, fixo ao variar ρ. Não se presume que g0+ρt h tenha a transformação BRST do campo final; (15) é somente uma homotopia de matrizes formais naturais. Dela seguem

\[
\partial_\rho u_\rho=s a_\rho+[u_\rho,a_\rho],
\quad s u_\rho=-u_\rho^2,
\quad s(u_\rho^2)=0.
\tag{16}
\]

aρ é par e tem ghost zero. O traço do termo comutador em ∂ρ tr(uρ³) se anula. Portanto

\[
\partial_\rho\operatorname{tr}(u_\rho^3)
=3s\operatorname{tr}(a_\rho u_\rho^2).
\]

Como u0=0, temos a primitiva explícita

\[
\boxed{\tau_{\rm ort}-\tau_{\rm GL}=s\mathcal B,
\qquad
\mathcal B=\operatorname{tr}(uv)
 +\int_0^1\operatorname{tr}(a_\rho u_\rho^2)\,d\rho.}
\tag{17}
\]

Não é uma integral em espaço-tempo nem uma hipótese de exatidão cohomológica importada. Cada coeficiente formal é um polinômio finito em ρ, e a integração produz números racionais bem definidos. A soma não é avaliada para t numérico. 

## 6. Naturalidade, completação e consequência para C₅

Todos os objetos da comparação têm origem especificada: L é a variação de Levi-Civita, H=g0⁻¹h, v=∇^g c, S a raiz formal correspondente, e k o transporte (13). Sob mudanças de coordenadas ou de apresentação tensorial escolhidas independentemente dos campos ativos, H,S,u,aρ,v transformam por conjugação e os traços são escalares. As derivadas de conexão aparecem como diferenças ou derivadas covariantes de fundo. Nenhuma escolha de frame fica no resultado (17), nem se identifica o ghost Lorentz cru com v ou k.

Cada monômio tem seu fator t^E pareado à valência; o integral finito por coeficiente em (17) conserva essa propriedade e a ordem finita de jatos. Para um rótulo de laço Lloop, o mesmo prefator t^(2Lloop−2) pode ser conservado. A comparação usa o anel de coeficientes HERDADO e o domínio formal do adendo079; não reduz esse anel nem prova admissibilidade da hierarquia causal completa.

Até C5, ambas as transgressões são ciclos. Truncar (17), usando que s não diminui valência, mostra

\[
\boxed{[\tau_{\rm ort,\le5}]=[\tau_{\rm GL,\le5}]
\quad\text{em }H^3(C_5).}
\tag{18}
\]

Essa identidade inclui a diferença dos termos líderes por uma fronteira do mesmo complexo; não supõe igualdade literal entre B=∇bar C e sua parte antissimétrica M. A linha inicial se mantém, mas o representante não é tratado como igual antes da transformação calculada.

Pelo [certificado078](<C:/IALD/Central de Patentes/Chatgpt/RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md>), a classe particular do lado esquerdo não se levanta a C6. Logo a versão GL obtida apenas mudando a conexão tem a mesma limitação. A diferença (17) tem classe zero e, portanto, não fornece um elemento de K com δ igual a −[A6].

## 7. Onde permanecem os antifields e o problema aberto

A identidade (10) é uma fórmula calculada para s0(I_CJ2). Ela mostra uma correção quadrática explícita e um termo s1 conhecido. O pacote satisfaz a segunda equação de079, mas não a primeira, como (12) demonstra. Não foi obtida uma decomposição alternativa que restaure essa primeira equação por um b4 s0-fechado e, simultaneamente, pague as condições de valência cinco/seis com antifields.

Se se acrescentar u*R(C4), seu s0 continua sendo +H0u·R(C4), com o [sinal KT corrigido](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>). Seu s1 contém E2[u,u]R, além dos termos lineares em antifields. Nenhuma dessas contribuições foi declarada nula por (17). Elas pertencem à busca de classes diferentes, não a uma troca de apresentação da mesma transgressão.

[DERIVED — aguardando revisão] (7–10) completam explicitamente a corrente na equação da quinta valência; (12) detecta o defeito anterior; (17–18) provam que a comparação GL–ortogonal não muda a classe particular em C5.

[OPEN] Continua sem decisão se −[A6] pertence a δ(K) para OUTRAS correções admissíveis. A decomposição Weyl de possíveis b4, as EOM quadráticas e a liberdade de antifields ainda precisam ser analisadas. Não se afirma obstrução de toda a linha, classificação completa, lim¹, QME ou UV.

[REAL — documental] Fontes e arquivos novos medidos no manifesto antes/depois. Nenhum original, arquivo078 ou memória canônica foi modificado. Não houve CAS/Lean e nenhuma revisão anterior foi reaproveitada como aprovação desta nova comparação.
'''.replace('\x00', '')


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
note_path = OUT / 'CORRENTE_QUADRATICA_E_EQUIVALENCIA_DAS_CONEXOES.md'
emit(note_path, NOTE.encode('utf-8'))
after = [pin(path) for path in SOURCES]
if before != after:
    raise RuntimeError('SOURCE_CHANGED')
links = re.findall(r'\]\(<(C:/[^>]+)>\)', NOTE)
if not all(Path(p).is_file() for p in links):
    raise RuntimeError('MISSING_LOCAL_LINK')
manifest = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'kind': 'explicit_GL_orthogonal_transgression_comparison',
    'author': '/root/prepare_integration_83',
    'status': 'DERIVED_WRITTEN_AWAITING_INDEPENDENT_REVIEW',
    'results': ['s0(I_CJ2+F(-HL))=-s1F(L)', 'explicit failure of s0 closure of F(L)', 'natural formal s primitive for orthogonal minus GL transgression', 'same C5 class for the two connection presentations'],
    'source_pins_before': before,
    'source_pins_after': after,
    'sources_unchanged': True,
    'note': pin(note_path),
    'creator': pin(Path(__file__).resolve()),
    'local_links': [{'path': p, 'exists': True} for p in links],
    'executions': {'CAS': 0, 'Lean': 0, 'um_py_execution_or_import': 0},
    'remaining': ['closed b4 completion with possible H0u R contribution', 'membership -[A6] in delta(K) for other classes'],
    'not_claimed': ['all possible lifts obstructed', 'antifields irrelevant', 'QME', 'universal anomaly verdict', 'independent approval already received'],
}
manifest_path = OUT / 'MANIFESTO_COMPARACAO_CONEXOES_079.json'
emit(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'note': pin(note_path), 'manifest': pin(manifest_path),
                  'source_count': len(before), 'sources_unchanged': True,
                  'local_links_existing': len(links)}, ensure_ascii=False))
