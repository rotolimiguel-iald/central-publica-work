from pathlib import Path
import datetime
import hashlib
import json
import os

BASE = Path('C:/IALD/Central de Patentes/Chatgpt')
OUT = Path(__file__).resolve().parent
assert OUT.parent == BASE and OUT.name == 'HOMOTOPIA_NORMAL_COVARIANTE_074_20260910'
SOURCES = [
    'COHOMOLOGIA_ESPECTADOR_B0_073_20260910/PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md',
    'COVARIANTIZACAO_SUAVE_071_20260910_001058_826723/COROLARIO_H5_E_ANOMALIA_LOCAL.md',
    'RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md',
    'COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md',
    'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md',
]

def pin(path):
    data = path.read_bytes()
    st = path.stat()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'mtime_ns': st.st_mtime_ns}

def new_file(name, content):
    path = OUT / name
    assert not path.exists(), f'Existing destination: {path}'
    data = content.encode('utf-8')
    tmp = OUT / (name + '.tmp_new')
    with tmp.open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    assert tmp.read_bytes() == data and len(data) > 0
    tmp.rename(path)
    assert path.read_bytes() == data
    return pin(path)

before = [pin(BASE / name) for name in SOURCES]
note = r'''# Translação normal, curvatura e classe natural BRST

10/09/2026, arco074. [DERIVED — demonstração escrita]. Somente arquivos novos nesta pasta. Nenhum original ou artefato congelado alterado; nenhum um.py executado/importado; zero CAS e zero Lean novos.

## 1. Resultado e comparação com073

A substituição coordenada c→c+dx possui uma substituição natural, construída com os jatos da exponencial geodésica da métrica de referência g0. Ela não comuta com a derivada horizontal. O defeito é calculável e, no primeiro jato covariante do ghost, é exatamente a curvatura:

\[
\boxed{C_N(\bar\nabla_\mu c^\nu)=-\bar R^\nu{}_\mu,\qquad
C_N=[d_H,b_N].}
\tag{1}
\]

Definindo D_N=[b_N,s] e E_N=d_H−D_N, obtemos a identidade natural exata

\[
\boxed{e^{-b_N}(s+d_H)e^{b_N}=s+E_N+C_N.}
\tag{2}
\]

E_N não é um diferencial separado na álgebra completa: E_N²=−{s,C_N}. Em particular, não se pode trocar E_N por d_ext da prova073 e reutilizar a sequência espectral daquela prova sem novo cálculo. O resultado paga uma conjugação natural e fornece a correção explícita que esse novo cálculo deve conservar; não paga sozinho a trivialidade da cohomologia natural ou a QME.

A [nota073](<C:/IALD/Central de Patentes/Chatgpt/COHOMOLOGIA_ESPECTADOR_B0_073_20260910/PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md>) provou um resultado ordinário coordenado e expôs a falta de naturalidade do seu b. A [retração072](<C:/IALD/Central de Patentes/Chatgpt/RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md>) e a [Ward de referência072](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md>) conservam B0 como espectador. Aqui sB0=0 permanece verdadeiro e d_HB0 permanece presente.

## 2. Álgebra e convenções

Trabalhamos inicialmente com os campos COMPLETOS no complexo BV mínimo Einstein–sigma, em apresentação métrica ou vielbein. Como em073, primeiro desfazemos o gauge por transformação canônica e contraímos os pares não mínimos. Isso evita aplicar a identidade de translação diretamente à regra s c̄=−b, que não é uma transformação por derivada de Lie.

B0=(g0,φ0) tem ghost zero e é inerte sob s, inclusive todos os seus jatos. A conexão \(\bar\nabla\) é a de Levi-Civita de g0, com

\[
[\bar\nabla_\mu,\bar\nabla_\nu]v^\rho
 =\bar R^\rho{}_{\sigma\mu\nu}v^\sigma,
\qquad sc^\mu=c^\nu\partial_\nu c^\mu
               =c^\nu\bar\nabla_\nu c^\mu.
\tag{3}
\]

O último sinal fixa nossa convenção BRST. O grau total é ghost+forma. s e d_H são ímpares, s²=d_H²={s,d_H}=0; dx anticommuta com c. b_N terá bidegrau (−1,+1) e será uma derivação PAR de grau total zero. Colchetes indicam comutadores graduados pelo grau total; chaves entre dois operadores ímpares indicam anticomutadores.

A classe considerada contém funções suaves conjuntas nos valores dos campos e de B0, com dependência finita/polinomial nos jatos diferenciados, ghosts e antifields. Formas naturais são formas horizontais que transformam conjuntamente sob mudanças de coordenadas de todos os dados. Essa naturalidade externa é compatível com sB0=0: transformação passiva/conjunta e diferencial quântico são operações distintas.

O cálculo também faz sentido coeficiente a coeficiente numa classe formal de flutuações, mas o transporte dessa completação precisa da contagem explícita da seção9. Não se usa uma métrica Euclidiana auxiliar para definir b_N.

## 3. Construção centrada e natural em todos os jatos

Fixe x e considere a exponencial de \(\bar\nabla\), como germe em zero:

\[
\psi_x=\operatorname{Exp}^{\bar\nabla}_x:T_xM\supset V\longrightarrow M.
\]

Para w∈T_xM, seja \(w_{\rm const}\) o campo constante no espaço vetorial T_xM e defina

\[
\xi_{x,w}=(\psi_x)_*w_{\rm const},\qquad
I_x(w)=j_x^\infty\xi_{x,w}.
\tag{4}
\]

É o pushforward de um campo de componentes constantes em coordenadas normais; não é transporte paralelo radial. Esta diferença importa já nos segundos jatos.

Contraia w com a identidade \(\mathrm{Id}_{TM}\in TM\otimes T^*M\), representada por dx. Defina b_N nos jatos do ghost pela inserção I_x(dx), e estenda por Leibniz par. Nos demais geradores — campos, antifields, ghosts Lorentz, B0 e seus jatos, x e dx — b_N vale zero. Assim, numa carta qualquer,

\[
b_N(\partial_Ic^\mu)=T_I{}^\mu{}_\nu(jB0)\,dx^\nu.
\tag{5}
\]

Cada T_I depende de um número finito de jatos de g0. Não se exige uma carta normal global nem uma série convergente: a equação geodésica determina recursivamente cada Taylor finito, e a parte linear da exponencial é a identidade. A inversão da série formal e a diferenciação de (4) requerem apenas operações finitas a cada ordem.

Se f transporta todos os dados, a naturalidade da exponencial dá f∘ψ_x=ψ'_{f(x)}∘df_x. Logo f_*I_x(w)=I'_{f(x)}(df_xw). Essa igualdade demonstra a naturalidade da inserção. Duas bases de T_xM mudam as coordenadas normais por transformação linear, sem mudar I_x. Não escolhemos um centro global: construímos o operador em CADA x e conservamos a derivada da dependência nesse centro.

[KNOWN] A reconstrução universal finita dos jatos normais pseudo-Riemannianos e sua equivariância são explicitadas por [Jentsch, teoremas1–3, versão arXiv1509.08269v1](https://arxiv.org/pdf/1509.08269v1). Importamos apenas o controle dos jatos normais; os comutadores BRST abaixo são demonstrados aqui.

Em coordenadas normais centradas em x, o campo (4) tem componentes constantes em toda a carta usada para esse centro. Portanto seus jatos parciais positivos se anulam nesse x. Mas b_N NÃO é o prolongamento evolutivo da regra c↦dx: ao mover x, muda a carta que define a inserção. Fazer d_Hb_N=0 por considerar a carta de um único centro como fixa eliminaria precisamente o termo de curvatura de (1).

## 4. Primeiros jatos e o defeito de curvatura

Da definição seguem

\[
b_Nc^\nu=dx^\nu,\quad
b_N(\partial_\mu c^\nu)=-\bar\Gamma^\nu_{\mu\sigma}dx^\sigma,
\quad b_N(\bar\nabla_\mu c^\nu)=0.
\tag{6}
\]

Em coordenadas normais centradas em x, escreva

\[
A^\rho{}_{\mu\nu|\sigma}
 :=\partial_\sigma\bar\Gamma^\rho_{\mu\nu}(x)
 =-\frac13\left(\bar R^\rho{}_{\mu\nu\sigma}
                 +\bar R^\rho{}_{\nu\mu\sigma}\right).
\tag{7}
\]

A fórmula vem da identidade de curvatura no centro, da simetria dos dois índices inferiores de Γ e da condição normal Γ^ρ_(μν,σ)=0. Como os jatos parciais positivos inseridos são zero no centro,

\[
b_N(\bar\nabla_\rho\bar\nabla_\mu c^\nu)
 = A^\nu{}_{\mu\sigma|\rho}dx^\sigma
 =-\frac13(\bar R^\nu{}_{\mu\sigma\rho}
            +\bar R^\nu{}_{\sigma\mu\rho})dx^\sigma.
\tag{8}
\]

Em particular,

\[
b_N(\bar\nabla_{(\mu}\bar\nabla_{\nu)}c^\rho)
 =-\frac16(\bar R^\rho{}_{\nu\sigma\mu}
            +\bar R^\rho{}_{\mu\sigma\nu})dx^\sigma.
\tag{9}
\]

Logo não é correto zerar todos os jatos covariantes simetrizados na definição de b_N.

Agora ponha Z_μ^ν=\(\bar\nabla_\mu c^\nu\). Por (6), b_N Z=0 como identidade em todo centro. Assim d_H(b_NZ)=0. No centro normal, onde Γ=0,

\[
b_N(d_HZ_\mu{}^\nu)
 =dx^\rho(\partial_\rho\bar\Gamma^\nu_{\mu\sigma})dx^\sigma
 =\frac12\bar R^\nu{}_{\mu\rho\sigma}
                 dx^\rho\wedge dx^\sigma.
\tag{10}
\]

A última igualdade também se vê diretamente usando a simetria Γ^ν_μσ=Γ^ν_σμ e antissimetrizando ρ,σ. Portanto (1) segue com sinal negativo. C_Nc=0, pois a possível contribuição de Γ tem dois índices simétricos contra dx∧dx.

Um controle útil: para Levi-Civita, tr R̄=0, portanto C_N(tr Z)=0. Isso não anula o defeito matricial: o setor de divergência/traço não mede as componentes de curvatura presentes nos demais componentes de Z.

## 5. Comutadores exatos, sem truncamento em curvatura

Defina D_N=[b_N,s] e C_N=[d_H,b_N]. Então

\[
[b_N,D_N]=0,\qquad [b_N,C_N]=0,\qquad C_N^2=0.
\tag{11}
\]

Prova do primeiro comutador. Os coeficientes T_I dependem só de B0, e sB0=0. As regras BRST mínimas dos campos e antifields contêm no máximo um ghost difeomórfico em cada termo, exceto a regra quadrática sc; as partes KT sem ghosts não contribuem a uma segunda inserção. Os ghosts Lorentz têm no máximo um c nos termos de transporte; b_N não insere no ghost Lorentz. No caso sc e todos os seus jatos, duas inserções são os jatos do colchete dos campos ξ_{x,w} de (4). Fixando x, todos esses campos são pushforwards dos campos constantes na MESMA carta e comutam como campos perto de x. Seus colchetes e todos os seus jatos são zero. Isso paga a identidade em todas as ordens, não apenas em c(x).

Prova das demais. C_N é uma derivação ímpar que insere apenas nos jatos de c, com coeficientes de duas-formas construídos de B0. Aniquila os demais geradores. b_N e C_N aniquilam os coeficientes de ambas as inserções, que não contêm ghosts. Logo [b_N,C_N]=0 e C_N²=0 em cada gerador, portanto na álgebra toda.

Como b_N eleva o grau de forma, b_N⁵=0 em dimensão4. O BCH e (11) dão exatamente

\[
e^{-b_N}s e^{b_N}=s-D_N,
\qquad e^{-b_N}d_H e^{b_N}=d_H+C_N.
\tag{12}
\]

A primeira identidade e s²=0 implicam {s,D_N}=0 e D_N²=0; o primeiro também segue diretamente de Jacobi. Somar (12) prova (2). Definindo E_N=d_H−D_N, separar os bidegraus de (s+E_N+C_N)²=0 fornece

\[
\{s,E_N\}=0,\qquad E_N^2+\{s,C_N\}=0,
\qquad\{E_N,C_N\}=0,\qquad C_N^2=0.
\tag{13}
\]

Não houve aproximação em R̄. Estes são os comutadores corretos da translação natural.

## 6. O que E_N deriva e o controle no fundo físico

Nos jatos do espectador,

\[
D_N B_{0,I}=0,\quad C_N B_{0,I}=0,
\qquad \boxed{E_N B_{0,I}=d_H B_{0,I}.}
\tag{14}
\]

Portanto os jatos de φ0 e de g0 não foram congelados horizontalmente. Conexão e curvatura variam como funções desses jatos. Nos campos dinâmicos não diferenciados, D_Ng=dx^ρ\(\bar\nabla_\rho g\) e D_Nφ=d_Hφ. Porém D_N não é a derivada exterior covariante ingênua em todos os jatos.

Por exemplo, no centro normal, calculando sZ pela regra sc de (3),

\[
D_NZ_\mu{}^\nu=dx^\rho\partial_\rho\partial_\mu c^\nu,
\quad
(D_N-\bar D)Z_\mu{}^\nu
 =-dx^\rho A^\nu{}_{\mu\sigma|\rho}c^\sigma
 =\frac13dx^\rho(\bar R^\nu{}_{\mu\sigma\rho}
                 +\bar R^\nu{}_{\sigma\mu\rho})c^\sigma.
\tag{15}
\]

Aqui \(\bar D\) é a derivada exterior covariante no tensor Z. D_N²=0 não contradiz \(\bar D^2=\bar R\): os operadores diferem, já em (15). Quando se usam componentes com índices livres, d_H deve ser distinguido de \(\bar D\); as identidades de conjugação são identidades intrínsecas na álgebra de funções de jatos e formas horizontais naturais.

Há um defeito não nulo exatamente no fundo usado pela construção Q2:

\[
g0=dr^2-a(r)^2\gamma,\qquad a(r)=2\cos(r/2),\quad 0<r<\pi.
\]

As conexões Γ̄^r_ij=a a′γij e Γ̄^i_rj=(a′/a)δij dão, pela convenção (3),

\[
\bar R^r{}_{i r j}=a a''\gamma_{ij}
                  =-\frac{a^2}{4}\gamma_{ij}.
\]

As componentes \(\bar R^r{}_{i k l}\) puramente espaciais são zero. Portanto

\[
\boxed{C_N(\bar\nabla_i c^r)
 =\frac{a^2}{4}\gamma_{ij}\,dr\wedge dy^j\ne0.}
\tag{16}
\]

O controle é uma derivação escrita das conexões; não foi apresentado como CAS. (16) obstrui omitir C_N no transporte da prova. Não é uma anomalia física não removível e não refuta o modelo.

## 7. Filtração natural correta para procurar a primitiva

b_N é natural, e s,d_H são naturais conjuntamente. Logo (2) é um isomorfismo do complexo total no subcomplexo natural efetivamente escolhido, não apenas na classe coordenada. O problema restante é calcular a cohomologia do lado direito NA MESMA classe. Naturalidade de um isomorfismo não prova que sua cohomologia seja zero.

Filtre pelo grau de forma q, com 0≤q≤4. Os operadores s,E_N,C_N elevam esse grau em0,1,2, respectivamente. A primeira página é H(s) da classe natural com B0; o primeiro diferencial é induzido por E_N. Ele quadratura a zero em H(s) por (13). A partir do segundo passo, a curvatura C_N participa explicitamente.

Isso não é a sequência de073 com d_ext simplesmente renomeado. Em particular, o [corolário H5_071](<C:/IALD/Central de Patentes/Chatgpt/COVARIANTIZACAO_SUAVE_071_20260910_001058_826723/COROLARIO_H5_E_ANOMALIA_LOCAL.md>) e a exatidão coordenada073 não identificam automaticamente H(s) do novo subcomplexo natural com espectadores e sua cohomologia de E_N.

Há uma receita finita para verificar uma primitiva candidata. Se Ω=ΣΩ_q é um cociclo de Q_N=s+E_N+C_N e T=ΣT_q tem grau total um a menos, suas equações são

\[
sT_q+E_NT_{q-1}+C_NT_{q-2}=\Omega_q,
\qquad T_{-1}=T_{-2}=0,\quad 0\le q\le4.
\tag{17}
\]

Defina U_q=Ω_q−E_NT_{q−1}−C_NT_{q−2}. Se as equações anteriores valem, então sU_q=0. Prova: use a equação de cociclo no grau q e (13); os termos com E_N² cancelam os de {s,C_N}, e os restantes cancelam por {E_N,C_N}=C_N²=0. Assim, a cada etapa, a obstrução é uma classe de s de um cociclo natural CONCRETO. Se essa classe admite primitiva natural no grau em questão, escolhe-se T_q e avança-se. Esta é uma regra verificável; não constitui uma hipótese de exatidão já paga.

O termo C_NT_{q−2} é obrigatório desde q=2. O exemplo (16) mostra que apagá-lo altera o problema no fundo físico. Se uma análise independente demonstrar a nulidade das entradas relevantes da sequência espectral na classe natural, a filtração é finita e os passos posteriores só tomam subquocientes; nenhuma classe pode ser criada a partir de entradas já nulas. A demonstração dessas entradas e a admissibilidade dos T_q continuam separadas desta nota.

Obtido T natural, (2) dá (s+d_H)(e^{b_N}T)=e^{b_N}Ω. O componente de forma4 fornece o contratermo e o componente de forma3 a divergência. Isso é transporte explícito de uma primitiva já construída na classe correta. Uma primitiva coordenada arbitrária de073 não se torna natural apenas por aplicar e^{b_N}.

## 8. Propriedades locais pagas pelo operador e limites T5

Cada aplicação em um jato de ordem r usa um número finito de jatos de Γ̄; a receita normal é universal e sua expressão covariante é polinomial em curvatura e suas derivadas, com contrações por g0 e sua inversa. C_N aumenta no máximo em uma unidade a ordem de jatos de fundo necessária. Nenhum valor de B0 distante de x entra.

Essa construção preserva a dependência analítica em famílias já analíticas de métricas não degeneradas: os coeficientes finitos usam derivação, soma, produto e inversão de g0. Uma entrada apenas C∞ continua C∞; ela não é convertida em analítica. A exponencial geodésica é usada como germe de jatos finitos, sem exigir sua convergência em uma expansão formal de campos.

A conexão Levi-Civita é invariante sob multiplicação CONSTANTE de g0 por um fator não nulo compatível com a assinatura. Assim b_N não introduz por si uma escala métrica absoluta. Na convenção auxiliar dim∂=1, dimc=dimdx=−1 e dimg0=0, a substituição de um jato de ghost de ordem r conserva o peso r−1: seu coeficiente geométrico tem peso r e é multiplicado por dx. Isso é uma verificação do peso deste operador, não uma identificação automática com todos os axiomas de escala Q2.

b_N usa somente g0 e o ghost de espaço-tempo e, portanto, comuta com a simetria rígida O(4) atuando nos dados do alvo. Preserva suporte local e não realiza média de produtos temporais. Derivadas de testes/cutoffs geradas por d_H permanecem nas equações: não foram descartadas para obter (2).

[OPEN] A existência de uma primitiva com a condição T5, os limites de escala por setor, a hierarquia causal completa de contatos, a realidade apropriada e a normalização Ward não segue somente dessas propriedades de b_N. A construção tampouco implementa independência quântica de fundo ou transporte renormalizado entre parametrizes.

## 9. Campos completos, t e continuidade limitada

Até aqui c é o ghost dos campos completos. Na expansão usual c=tC, o mesmo operador age por b_NC=t⁻¹dx, e analogamente nos jatos. Logo finitude em grau de forma, isoladamente, permite perda de até quatro potências de t: não basta alegar que a exponencial preserva qualquer série não negativa arbitrária.

Existe um controle mais preciso para o peso conectado da [construção Q2_069, seção2](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md>). Se \(\mathcal P_E\) denota expressões homogêneas de grau E nos campos perturbativos e seus jatos, e os coeficientes de b_N dependem de B0, escreva b_N=t⁻¹\(\mathcal B_N\). Então

\[
\mathcal B_N:\mathcal P_E\longrightarrow\mathcal P_{E-1},
\qquad
b_N\left(t^{E+2L-2}P_E\right)
 =t^{(E-1)+2L-2}\mathcal B_NP_E.
\tag{18}
\]

Portanto b_N preserva a completação equilibrada

\[
\mathcal R_L=\prod_{E\ge0}t^{E+2L-2}\mathcal P_E
\tag{19}
\]

sempre que o objeto efetivo possui esse peso e esses graus. Para e^{±b_N}, cada coeficiente de grau E recebe apenas contribuições dos graus E,…,E+4. A transformação é contínua coeficiente a coeficiente em (19). Para L≥1 os pesos de (19) são não negativos. Esta conclusão é sobre a conjugação b_N na completação tipada (19); não prova que as homotopias que resolveriam (17) preservem (19), nem que toda anomalia com inserções externas tenha esse peso sem verificar seus graus e normalizações. Desvios de fundo, tadpoles e antifields devem permanecer na contagem da Ward072.

Não precisamos completar todos os jatos a uma série convergente. Precisamos, sim, provar a finitude/continuidade das operações usadas em cada categoria formal real antes de transportar uma primitiva. Esta nota paga a parte de b_N que (18) efetivamente cobre; a resolução cohomológica e os contatos Q2 não foram identificados com essa única operação.

## 10. Estatuto final desta contribuição

[DERIVED] Foram construídos b_N natural de jatos, sua conjugação total exata, o termo C_N(∇̄c)=−R̄ e o defeito não nulo no FRW de Q2. d_HB0 foi conservado. A naturalidade é conjunta e local em jatos, sem uma carta normal global.

[DERIVED] A filtração correta tem s+E_N+C_N, com E_N²=−{s,C_N}; a recorrência (17) explicita onde procurar obstruções e onde a curvatura entra. A conjugação preserva a completação equilibrada (19) no escopo e com os graus ditos.

[OPEN] Esta nota não dá por concluída a cohomologia relativa natural com espectadores, a primitiva na classe causal completa, a QME ou a independência quântica de fundo. O resultado corrige uma passagem concreta da prova e disponibiliza operadores naturais para o próximo cálculo, sem transformar naturalidade de um operador em exatidão de todo o complexo.

O manifesto anexo registra os pins das cinco fontes locais lidas antes e depois da escrita. A revisão algébrica independente recebida nesta tarefa conferiu (8)–(13), incluindo o sinal de (1), a dependência do centro e o limite de escopo; não foi um novo teste Lean nem uma aprovação da QME.
'''
written = new_file('TRANSLACAO_NORMAL_E_CURVATURA_BRST.md', note)
after = [pin(BASE / name) for name in SOURCES]
assert before == after, 'Source changed during note creation'
manifest = {
    'created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope': '074 natural normal ghost-jet insertion and exact curvature commutators; no claim of natural cohomological exactness or QME',
    'source_pins_before': before, 'source_pins_after': after, 'sources_unchanged': before == after,
    'outputs': [written], 'writer': pin(Path(__file__)),
    'external_primary_sources': [
        {'url': 'https://arxiv.org/pdf/1509.08269v1', 'read': 'Theorems 1-3; finite universal equivariant pseudo-Riemannian normal jets', 'import_limit': 'normal-jet construction only, not the derived BRST identities'}
    ],
    'verification': {'kind': 'documentary source/output byte checks', 'new_cas': 0, 'new_lean': 0,
                     'um_executed_or_imported': False, 'original_or_frozen_file_modified': False,
                     'independent_algebra_review': 'Agent selected_geometry_design reported checks of second covariant jets, curvature sign, commutators and BCH in task messages; not an independent QME approval'},
    'open': ['natural relative cohomology in actual admissible class', 'T5/causal contacts for a constructed primitive', 'full homotopy continuity in actual perturbative completion', 'QME', 'quantum background independence']
}
mp = new_file('MANIFESTO_HOMOTOPIA_NORMAL_074.json', json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'note': written, 'manifest': mp, 'sources_unchanged': True, 'source_count': len(before), 'new_cas': 0, 'new_lean': 0}, ensure_ascii=False))
