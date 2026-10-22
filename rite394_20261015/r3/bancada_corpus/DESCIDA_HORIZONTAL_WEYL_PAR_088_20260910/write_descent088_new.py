from pathlib import Path
import datetime as dt
import hashlib
import json
import os

BASE = Path("C:/IALD/Central de Patentes/Chatgpt")
OUT = Path(__file__).resolve().parent
SOURCES = {
    "TRANSLACAO": BASE / "HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/TRANSLACAO_NORMAL_E_CURVATURA_BRST.md",
    "FRAME": BASE / "HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/PRECISAO_FRAME_LOCAL_074.md",
    "REES": BASE / "COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md",
    "TRANSGRESSAO": BASE / "TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md",
    "CLASSE": BASE / "CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md",
    "PARECER_CLASSE": BASE / "REVISAO_CLASSE_PAR_BRST_087_20260910/PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md",
    "ADENDO_CLASSE": BASE / "REVISAO_CLASSE_PAR_BRST_087_20260910/ADENDO_CONSUMO_REVISAO_N2_087.md",
    "CRITERIO": BASE / "CONTRATO_CRITERIO_ANOMALIAS_087_20260910/CRITERIO_074_GRUPOS_EXATOS_E_MAPA_085_086.md",
}
def pin(p):
    raw = p.read_bytes()
    st = p.stat()
    return {"path": p.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "mtime_ns": st.st_mtime_ns,
            "mtime_utc": dt.datetime.fromtimestamp(st.st_mtime, dt.timezone.utc).isoformat()}
def emit(name, raw):
    p = OUT / name
    tmp = OUT / (name + ".pending_new")
    if p.exists() or tmp.exists():
        raise FileExistsError(str(p))
    with tmp.open("xb") as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    if tmp.read_bytes() != raw:
        raise RuntimeError("Temporary verification failed: " + name)
    os.rename(tmp, p)
    if p.read_bytes() != raw:
        raise RuntimeError("Final verification failed: " + name)
    return pin(p)
before = {key: pin(p) for key, p in SOURCES.items()}
script_before = pin(Path(__file__).resolve())
note = r"""# Descida da classe par de Weyl e sua imagem horizontal natural

10/09/2026, investigação088. Autor: /root/prepare_integration_83. [DERIVED — demonstração escrita, oferecida à revisão independente]. O cálculo usa o teste métrico mínimo de sigma constante087. Não executa fontes matemáticas, CAS, Lean ou um.py, nem modifica qualquer fonte congelada.

**Resultado:** para a densidade completa ρ_I(g) de ½W(g)²vol_g,

\[
A_I=\rho_I(g)c^0c^1c^2c^3,\qquad
\boldsymbol\Omega_I=\rho_I(g)\prod_{\mu=0}^3(dx^\mu+c^\mu)
                  =e^{b_N}A_I,
\]

a descida usual satisfaz (s+d_H)Ω_I=0. A conjugação074 fornece algo mais preciso que uma fronteira horizontal abstrata:

\[
\boxed{Q_N A_I=0,\qquad E_NA_I=0,\qquad C_NA_I=0.}
\tag{1}
\]

Na equação E_NA_I=−sB₁ é possível escolher B₁=0; na etapa seguinte C_NA_I+E_NB₁=0, com B₂=0. Todos os componentes positivos de forma do representante conjugado podem ser zero. A própria classe de ghost quatro é, assim, horizontalmente fechada em forma ZERO. Isso não demonstra H¹(Ebar_N;H⁴(s))=0.

## 1. Domínio, entradas e graus

A [classe par087](@CLASSE) fixa dimensão quatro, orientação, referência espaço-forma g₀ com K>0 real fixado, κ≠0 e sigma constante projetado ao complexo métrico mínimo. Rher é o mesmo anel real unital herdado, inerte para os operadores do teste. Não acrescentamos tensores espectadores, coordenadas como campos, inversas de novos invariantes ou séries de infinitos jatos por coeficiente.

O diferencial s é o BV–BRST CLÁSSICO completo por valência, incluindo antifields. Não é uma carga quântica renormalizada. A [revisão independente087](@PARECER_CLASSE), com seu [adendo de consumo da entrada](@ADENDO_CLASSE), delimita a linha livre Rher[A_I] em H⁴(s). Consumo esse resultado para a consequência de não exatidão do §7; não refaço nem reaprovo sua cadeia de antecedentes.

A presente identidade de descida usa apenas o setor antifield-free e as regras

\[
sg=\mathcal L_cg,\qquad sc^\mu=c^\nu\partial_\nu c^\mu,\qquad
sB_0=0.
\tag{2}
\]

As convenções são as da [transgressão076, §1](@TRANSGRESSAO) e da [translação normal074, §§2–5](@TRANSLACAO). Os dx ficam à esquerda, anticommuntam com c e têm grau total ímpar. A paridade total é ghost+forma. Os operadores s e d_H são ímpares, com s²=d_H²={s,d_H}=0, e s(dx^\mu f)=−dx^\mu sf. Ponha D=s+d_H.

b_N tem bidegrau (ghost−1, forma+1), paridade total PAR e anula os campos métricos e todos os seus jatos, B₀ e dx. Nos ghosts,

\[
b_Nc^\mu=dx^\mu,\qquad
b_N(\partial_\nu c^\mu)
=-\bar\Gamma^\mu_{\nu\sigma}dx^\sigma.
\tag{3}
\]

Defina D_N=[b_N,s], E_N=d_H−D_N e C_N=[d_H,b_N]. O resultado074 é

\[
Q_N=e^{-b_N}De^{b_N}=s+E_N+C_N,
\quad
\operatorname{bideg}(s,E_N,C_N)=(1,0),(0,1),(-1,2).
\tag{4}
\]

C_N aqui é o operador de CURVATURA da074; não é o truncamento por valência chamado C_N na087. Quando necessário, os truncamentos serão escritos \(\mathfrak C_n\).

A [precisão de frame074](@FRAME) conserva este teorema na apresentação MÉTRICA. Não inserimos um ghost Lorentz cru nem herdamos naturalidade sob mudanças locais de frame a partir da regra b_Nλ=0.

## 2. A densidade completa e a lei de transformação ativa

Use a métrica DINÂMICA em todas as contrações e no volume:

\[
I(g)=\tfrac12W_{abcd}(g)W^{abcd}(g),\qquad
I(g)\operatorname{vol}_g=\rho_I(g)dx^0dx^1dx^2dx^3.
\tag{5}
\]

ρ_I é um coeficiente de densidade de peso um, não um escalar. Sua lei ativa é

\[
s\rho_I=c^\mu\partial_\mu\rho_I
             +(\partial_\mu c^\mu)\rho_I.
\tag{6}
\]

Ela decorre da naturalidade da quatro-forma de (5). Não se fixa vol₀ durante essa transformação. A expressão é formal regular perto de g₀: não se divide por ρ_I ou W, que se anulam na referência.

Introduza quatro geradores totais ímpares

\[
z^\mu=dx^\mu+c^\mu,\qquad
Z=z^0z^1z^2z^3,\qquad
\vartheta=\partial_\mu c^\mu.
\]

Como d_Hc^\mu=dx^\nu\partial_\nu c^\mu e Ddx=0, seguem

\[
Dz^\mu=z^\nu\partial_\nu c^\mu,\qquad
D\rho_I=z^\mu\partial_\mu\rho_I+\vartheta\rho_I.
\tag{7}
\]

Essas fórmulas não congelam d_HB₀ e não substituem derivadas covariantes de ghosts por derivadas planas. São fórmulas coordenadas da transformação da densidade completa.

## 3. Prova graduada de DΩ_I=0

Aplicar a regra de Leibniz ímpar a Z dá

\[
DZ=\sum_{\mu=0}^3(-1)^\mu
 z^0\cdots z^{\mu-1}
 z^\nu(\partial_\nu c^\mu)
 z^{\mu+1}\cdots z^3.
\]

Mover o ghost derivado \(\partial_\nu c^\mu\) pelos 3−μ fatores à direita produz sinal (−1)^(3−μ). Assim o sinal combinado é sempre −1. Para ν≠μ há um z repetido e a parcela é zero. Portanto

\[
DZ=-Z\,\partial_\mu c^\mu=-\vartheta Z.
\tag{8}
\]

Z tem paridade total par; a segunda igualdade não acrescenta sinal. Não se tratam os ghosts derivados como números comutativos.

Defina \(\boldsymbol\Omega_I=\rho_I Z\). Por (7–8),

\[
D\boldsymbol\Omega_I
=(z^\mu\partial_\mu\rho_I)Z+\vartheta\rho_I Z
 -\rho_I\vartheta Z=0.
\tag{9}
\]

O primeiro termo contém cinco fatores entre apenas quatro z e é zero. A prova é off-shell, sem EOM, integração por partes ou antifields. Tampouco requer que a densidade seja uma forma característica de Chern–Weil: basta a lei de densidade natural (6). Essa é a razão pela qual o cálculo vale para Weyl² sem transformá-la em Pontryagin.

## 4. Todos os descendentes usuais, com sinais

Escreva
\(\boldsymbol\Omega_I=\sum_{q=0}^4\omega_q^{\,4-q}\),
onde q é forma e 4−q é ghost. Com ε₀₁₂₃=+1,

\[
\omega_q^{\,4-q}
=\frac{\rho_I}{q!(4-q)!}
 \epsilon_{\mu_1\cdots\mu_q\nu_1\cdots\nu_{4-q}}
 dx^{\mu_1}\cdots dx^{\mu_q}
 c^{\nu_1}\cdots c^{\nu_{4-q}}.
\tag{10}
\]

Produtos ordenados são abreviados por dx^{01}=dx⁰dx¹ e c^{123}=c¹c²c³. Explicitamente:

\[
\begin{aligned}
\omega_0^4={}&\rho_I c^{0123}=A_I,\\
\omega_1^3={}&\rho_I(
 dx^0c^{123}-dx^1c^{023}
 +dx^2c^{013}-dx^3c^{012}),\\
\omega_2^2={}&\rho_I(
 dx^{01}c^{23}-dx^{02}c^{13}+dx^{03}c^{12}
 +dx^{12}c^{03}-dx^{13}c^{02}+dx^{23}c^{01}),\\
\omega_3^1={}&\rho_I(
 dx^{012}c^3-dx^{013}c^2
 +dx^{023}c^1-dx^{123}c^0),\\
\omega_4^0={}&\rho_I dx^{0123}.
\end{aligned}
\tag{11}
\]

A separação por formas de (9) fornece exatamente

\[
\begin{array}{rcl}
s\omega_0^4&=&0,\\
s\omega_1^3+d_H\omega_0^4&=&0,\\
s\omega_2^2+d_H\omega_1^3&=&0,\\
s\omega_3^1+d_H\omega_2^2&=&0,\\
s\omega_4^0+d_H\omega_3^1&=&0.
\end{array}
\tag{12}
\]

d_Hω₄⁰=0 por grau de forma. Para conferir o último sinal diretamente,
\(d_H\omega_3^1=-[(\partial_\mu\rho_I)c^\mu+
\rho_I\partial_\mu c^\mu]dx^{0123}\),
na escrita com dx à esquerda, e esse termo cancela sω₄⁰. Nenhum termo de contato foi descartado.

Esses são descendentes do MESMO ciclo de grau total quatro. Não são uma primitiva de anomalia de grau total cinco.

## 5. Conjugação natural: os componentes positivos cancelam

b_Nρ_I=0 porque ρ_I contém apenas a métrica dinâmica e seus jatos. Como b_N é derivação par, b_Nc=dx e b_Ndx=0,

\[
e^{u b_N}A_I=\rho_I\prod_{\mu=0}^3(c^\mu+u\,dx^\mu),
\quad
\omega_q^{\,4-q}=\frac{b_N^q}{q!}A_I.
\tag{13}
\]

Não há derivadas de ghosts em A_I; portanto os termos de curvatura da inserção normal nos jatos superiores não entram em (13). Sua ausência neste representante não os anula no complexo inteiro.

Agora defina os componentes conjugados

\[
\boldsymbol B=e^{-b_N}\boldsymbol\Omega_I
             =\sum_{q=0}^4 B_q^{\,4-q}.
\]

A componente de forma q é a soma finita

\[
B_q^{\,4-q}
=\sum_{j=0}^q\frac{(-b_N)^j}{j!}\omega_{q-j}^{\,4-q+j}
=b_N^qA_I\sum_{j=0}^q\frac{(-1)^j}{j!(q-j)!}.
\tag{14}
\]

A soma é 1 para q=0 e (1−1)^q/q!=0 para q>0. Logo

\[
B_0^4=A_I,\qquad B_1^3=B_2^2=B_3^1=B_4^0=0,
\qquad \boldsymbol B=A_I.
\tag{15}
\]

Em particular, o descendente usual ω₁³ não deve ser confundido com B₁³:
\(B_1^3=\omega_1^3-b_NA_I=0\).
Também
\(B_2^2=\omega_2^2-b_N\omega_1^3+
\tfrac12b_N^2A_I=0\).

De (9), (4) e (15) resulta Q_NA_I=0. As equações pedidas, com seus graus, são

\[
\boxed{
E_NA_I=-sB_1^3=0,\qquad
C_NA_I+E_NB_1^3=-sB_2^2=0.
}
\tag{16}
\]

O primeiro termo tem bidegrau(4,1); o segundo,(3,2). As próximas equações também têm representantes zero. Não surgiu uma obstrução de forma dois oculta sob uma fronteira s não calculada: o próprio representante é zero.

## 6. Controle direto de E_N e C_N em uma carta qualquer

Há uma conferência de (16) que não usa apenas a conjugação. Escreva

\[
\gamma_0=\bar\Gamma^\mu_{\mu\sigma}dx^\sigma
         =d_H\log\sqrt{|\det g_0|}.
\]

γ₀ é a conexão de densidades escrita nessa carta; não a declaramos uma 1-forma tensorial isolada. A combinação final será tensorial.

Aplicar b_N a (6), usando (3), dá

\[
D_N\rho_I=d_H\rho_I-\gamma_0\rho_I,
\qquad E_N\rho_I=\gamma_0\rho_I.
\tag{17}
\]

Do mesmo modo, a partir de sc e da simetria dos índices inferiores de \(\bar\Gamma\),

\[
D_Nc^\mu
=dx^\sigma\partial_\sigma c^\mu
 +\bar\Gamma^\mu_{\nu\sigma}dx^\sigma c^\nu,
\qquad
E_Nc^\mu=-\bar\Gamma^\mu_{\nu\sigma}dx^\sigma c^\nu.
\tag{18}
\]

Ponha G=c^{0123}. No Leibniz total de E_NG, mover dx para a esquerda cancela o sinal da posição diferenciada. Somente o índice diagonal ν=μ sobrevive. Assim

\[
E_NG=-\gamma_0G,\qquad
E_N(\rho_IG)=\gamma_0\rho_IG-\rho_I\gamma_0G=0.
\tag{19}
\]

A conexão do coeficiente de densidade cancela a do produto dos ghosts. Não se supôs que ρ_I fosse escalar ou que a conexão de fundo fosse zero numa vizinhança.

Por definição C_N anula todos os jatos métricos, e C_Nc=0 pela torsão nula. Daí C_Nρ_I=C_NG=0 e

\[
C_NA_I=0.
\tag{20}
\]

A identidade074 \(C_N(\bar\nabla c)=-\bar R\) continua válida e em geral não nula. Ela é compatível com (20): A_I não contém esses geradores. Também permanecem \(E_NB_0=d_HB_0\) e \(E_N^2=-\{s,C_N\}\). Nenhum desses operadores foi globalmente substituído por zero ou por uma derivada exterior ingênua.

## 7. Imagem horizontal permitida e o que não se conclui

O [contrato do critério087, §§2–3](@CRITERIO) distingue a filtração por FORMAS da filtração por valência. Aqui usamos somente a primeira, cuja primeira página é H_s^{g,q}, e cujo primeiro diferencial é Ebar_N.

As identidades (16) demonstram, no mesmo domínio,

\[
\overline E_N[A_I]=0
 \quad\text{em }H_s^{4,1}.
\tag{21}
\]

O segundo diferencial por formas é representado por C_NA_I+E_NB₁ e também é zero. Há levantamento completo para Q_N, fornecido já pelo próprio A_I, sem componentes adicionais. Consequentemente, a classe não tem diferencial de saída em nenhuma página por formas.

No MESMO teste087, sua não exatidão em H_s^{4,0} implica ainda uma linha livre de Rher em H⁰(Ebar_N;H_s^{4,*}): não há formas de grau −1 que pudessem fornecer fronteiras de Ebar para essa posição. Essa é uma afirmação de forma ZERO.

Pode-se verificar diretamente a persistência no complexo total de grau quatro. Se \(\lambda A_I=Q_NT\) com T de grau total três, a parcela de forma zero seria \(\lambda A_I=sT_0^3\), contradizendo a injeção087 salvo λ=0. Portanto, consumindo aquela injeção na MESMA categoria,

\[
R_{\rm her}\hookrightarrow H^4(Q_N),\qquad
\lambda\longmapsto[\lambda A_I].
\tag{22}
\]

Por conjugação, o mesmo vale para \([\lambda\boldsymbol\Omega_I]\) em H⁴(s+d_H). Não foi preciso intercambiar cohomologia e limites inversos. A prova usa uma projeção em forma zero; não usa Mittag–Leffler. A naturalidade e a completação de todas as operações são as do §8.

Nada em (21–22) identifica ou anula o grupo de forma UM exigido pelo critério:

\[
H^1(\overline E_N;H_s^{4,*})
=
\frac{\ker(\overline E_N:H_s^{4,1}\to H_s^{4,2})}
{\operatorname{im}(\overline E_N:H_s^{4,0}\to H_s^{4,1})}.
\tag{23}
\]

A imagem horizontal da linha construída é zero. Isso não significa que todos os elementos do numerador de (23) pertençam à imagem, nem que todo elemento de H_s^{4,1} seja uma 1-forma multiplicada por [A_I]. Não foi demonstrada uma decomposição tensorial por formas arbitrárias, uma exaustão de H⁴(s) ou uma homotopia para (23).

A hipótese de Rher inerte para E_N também importa. Em outra categoria que admita um coeficiente f(B₀) com sf=0 mas d_Hf≠0, a derivação daria
\(Q_N(fA_I)=d_Hf\,A_I\).
Essa fórmula é somente um alerta tipado sobre a mudança de coeficientes, não uma inclusão automática desses f no teste087 ou um cálculo da cohomologia dessa categoria maior.

O fechamento (9) não utiliza as EOM, mas a NÃO EXATIDÃO consumida em (22) permanece a do teste087 de sigma constante. Não a transportamos por nome ao fundo físico sigma não constante, a uma categoria com espectadores adicionais ou a um domínio que localize novos invariantes.

## 8. Valência, Rees, regularidade e contatos

Com g=g₀+t h, c=tC e W(g₀)=0, escreva a densidade formal

\[
\rho_I(g_0+t h)=\sum_{r\ge2}t^r\rho_{[r]}(h).
\]

Cada ρ_[r] tem r pernas métricas e usa jatos de h até ordem dois. A componente ω_q contém 4−q ghosts normalizados e, portanto,

\[
\omega_q
=\sum_{r\ge2}t^{\,r+4-q}
 \rho_{[r]}(h)\,(\text{q fatores dx e 4−q fatores C}),
\qquad E=r+4-q.
\tag{24}
\]

Seu primeiro grau de valência é 6−q. Para q=4, começa em E=2; para q=0, em E=6. A perda de q potências de t corresponde precisamente à remoção de q pernas ghosts por b_N=t⁻¹\(\mathcal B_N\). Não se afirma preservação de cada corte ordinário por valência: uma projeção antes de conjugar deve conservar também as valências superiores que podem alimentar a forma escolhida.

A [completação Rees074, §§2–5](@REES) é
\(\mathcal R_L^q=\prod_Et^{E+2L-2}P_E^q\).
Multiplicar toda esta cadeia por t^(2L−2) a coloca em R_L; para L≥1 os expoentes são não negativos. Cada componente conjugada recebe no máximo cinco contribuições, e aqui elas cancelam explicitamente como em (14). Isso prova continuidade coeficiente a coeficiente no domínio declarado. Não existe ressoma a t numérico.

As expressões finais de (11) não aumentam a ordem dois dos jatos métricos de ρ_I. As derivadas de ordem superior que aparecem ao verificar DΩ cancelam pela identidade de densidade. Inversas métricas e volume são séries regulares junto à métrica não degenerada de referência. Coeficientes reais permanecem reais; não há divisão por K, por uma curvatura variável, por ρ_I ou por qualquer relógio.

Na graduação de engenharia usada em074, [∂]=1, [g]=0 e [c]=[dx]=−1, a densidade de Weyl² tem peso quatro e cada componente de (11) tem peso total zero. Esse controle algébrico e a naturalidade não constroem a hierarquia multilinear de normalizações Q2, nem seus limites de escala por aridade, independência funcional, inserções e contatos. Não afirmamos QME.

As equações foram escritas como identidades de jatos locais, sem descartar divergências por integração. Por exemplo, se uma função externa f de teste for s-inerte, a regra total mantém
\(D(f\boldsymbol\Omega_I)=d_Hf\,\boldsymbol\Omega_I\).
A cadeia sem cutoff não elimina o termo de derivada do cutoff quando ele é inserido.

## 9. Estatuto e custódia

[DERIVED] Descida usual completa(10–12); conjugação natural exata(13–16); controle direto das conexões de densidade e ghosts(17–20); imagem horizontal zero do representante A_I em forma zero. A relação pedida admite B₁=B₂=…=0.

[DERIVED — consumo delimitado de087] A linha não nula de ghost quatro persiste como ciclo total de grau quatro(22), no MESMO teste métrico de referência e no MESMO anel. Isso não calcula (23), ghost um/forma quatro, nem o operador quântico.

[OPEN] O grupo horizontal inteiro do critério, os demais grupos, admissibilidade da primitiva de anomalia causal, QME, UV e reconstrução gravitacional geral pelos mesmos dados permanecem fora deste cálculo. Weyl² não foi confundida com Pontryagin. H⁴/H³ cohomológicos não designam H3 interno do um.py; nenhum resultado de fase, ramo ou gate foi alterado.

[REAL — custódia] O manifesto mede as fontes locais e o helper documental antes/depois da emissão. Nenhuma execução matemática, CAS, Lean, teste de natureza ou execução/importação de um.py foi realizada. Houve um controle algébrico curto por mensagem de /root/selected_geometry_design sobre (7–9) e sua conjugação; não é parecer integral desta nota e não é contado como aprovação futura. Esta nota é nova e aguarda revisão específica.
"""
for token in sorted(SOURCES, key=len, reverse=True):
    note = note.replace("@" + token, "<" + SOURCES[token].as_posix() + ">")
if any("@" + token in note for token in SOURCES):
    raise RuntimeError("Unresolved source link")
note_pin = emit("DESCIDA_POR_FORMAS_E_IMAGEM_HORIZONTAL_WEYL_PAR.md", note.encode("utf-8"))
after = {key: pin(p) for key, p in SOURCES.items()}
script_after = pin(Path(__file__).resolve())
if before != after or script_before != script_after:
    raise RuntimeError("Input changed during emission; keep emitted note but do not issue stable manifest")
manifest = {
    "status": "WRITTEN_DERIVATION_PENDING_SPECIFIC_INDEPENDENT_REVIEW",
    "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    "scope": "Classical metric BV-BRST constant-sigma test087; explicit form descent of the complete Weyl-squared density",
    "note": note_pin,
    "source_pins_before": before,
    "source_pins_after": after,
    "all_eight_sources_preserved": before == after,
    "documentary_helper_before": script_before,
    "documentary_helper_after": script_after,
    "helper_preserved": script_before == script_after,
    "source_roles": {
        "TRANSLACAO": "Read: b_N, C_N, E_N, conjugation and algebra",
        "FRAME": "Read: metric-only naturality precision",
        "REES": "Read: balanced completion and bounded loss of valence",
        "TRANSGRESSAO": "Read: total parity conventions; not imported as a Weyl-squared primitive",
        "CLASSE": "Read: A_I, full-density transformation and non-exactness in the fixed test",
        "PARECER_CLASSE": "Read: independent review of the root's composition087",
        "ADENDO_CLASSE": "Read: effective consumption of the independent N2 review",
        "CRITERIO": "Read: actual horizontal groups and distinction of filtrations"
    },
    "claims": {
        "D_total_density_closed": "Written off-shell proof with total signs",
        "normal_conjugated_representative": "A_I only; positive-form components are zero",
        "E_N_A_I": "Exactly zero",
        "C_N_A_I": "Exactly zero",
        "B1_and_next_obstruction": "B1=0; C_N A_I + E_N B1=0; B2=0",
        "entire_H1_horizontal_group_zero": False,
        "arbitrary_form_tensor_factorization": False,
        "QME_or_UV_completed": False
    },
    "short_message_check": {
        "agent": "/root/selected_geometry_design",
        "scope": "D rho, D z, D product, e^b A, and zero E_N/C_N on this representative",
        "entire_note_independently_approved": False
    },
    "mathematical_execution_count": 0,
    "cas_execution_count": 0,
    "lean_execution_count": 0,
    "um_executed_or_imported": False,
    "canonical_or_memory_written": False,
    "writes_only_new_Chatgpt_files": True,
    "discovery_note": "An initially guessed Rees filename was absent; the actual existing filename was obtained from the directory listing and read. No source was invented or replaced."
}
manifest_pin = emit("MANIFESTO_DESCIDA_HORIZONTAL_WEYL_PAR_088.json",
                    (json.dumps(manifest, ensure_ascii=False, indent=2)+"\n").encode("utf-8"))
print(json.dumps({"status": manifest["status"], "note": note_pin, "manifest": manifest_pin,
                  "preserved_sources": len(SOURCES), "mathematical_executions": 0}, ensure_ascii=False))

