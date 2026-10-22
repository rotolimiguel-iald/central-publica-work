from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'COMPLETACAO_REES_BRST_074_20260910'
SOURCES = [
    'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md',
    'COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md',
    'COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md',
    'COHOMOLOGIA_ESPECTADOR_B0_073_20260910/PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md'
]


def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}


def create(path, content):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    raw = content.encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert raw and temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)


before = [pin(ROOT / relative) for relative in SOURCES]
assert not OUT.exists()
OUT.mkdir()
note = r'''# Completação por laços e valência para a translação BRST

10/09/2026, entrega074. [DERIVED — demonstração escrita]. Somente arquivo novo na bancada. Nenhum cálculo de diagrama, CAS ou Lean foi executado.

## 1. O problema que este resultado resolve

A translação de ghosts completos b c=dx não age da mesma maneira sobre o ghost normalizado C=c/t da teoria causal. Nessa variável, b C=t⁻¹dx. Portanto a finitude da exponencial eᵇ não basta para afirmar que ela preserva séries arbitrárias com potências não negativas de t.

Existe, porém, uma classe mais precisa já identificada em Q2: a ordem em t acompanha simultaneamente o número de pernas e o número de laços. Provamos que qualquer translação do tipo b=t⁻¹B, com B linear em derivadas de ghosts e coeficientes somente no fundo, preserva essa classe. A operação é contínua coeficiente a coeficiente e não gera potências negativas no setor de laços positivos.

O enunciado aplica-se a b_N quando a construção natural separada fornece suas propriedades de derivação e de coeficientes de fundo. Não usa a aciclicidade do complexo natural, não constrói uma primitiva e não certifica a família inteira de mapas de renormalização.

Entradas locais:

- [Q2_069, §§2–3 e 5](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md>): escala simultânea dos campos/ghosts/anticampos, vértices t^(v−2) e peso conectado t^(E+2L−2).
- [Contrato072, §§3–5](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md>): diferença entre finitude, escala, regularidade e hierarquia multilinear.
- [Ward072, §7](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md>): fontes externas, tadpoles e séries Laurent.
- [Cohomologia073, §9](<C:/IALD/Central de Patentes/Chatgpt/COHOMOLOGIA_ESPECTADOR_B0_073_20260910/PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md>): a completação da primitiva geral continuava sendo uma obrigação.

## 2. Convenções e classe formal

t é o parâmetro formal de organização da interação, não uma coordenada temporal. ħ conta laços. B0 é a referência inerte para o diferencial BRST mínimo. Denote por X todos os campos de flutuação, ghosts e anticampos normalizados; cada jato de X conta uma perna. Anticampos contam nessa graduação mesmo sem terem propagadores. Formas dx e coeficientes feitos somente de B0 não contam pernas.

A escala dos campos completos é g=B0_g+t h, c=t C, e analogamente nos setores lineares. No alvo, φ=Exp_(B0_φ)(tξ). O anticampo sigma é transportado pelo cotangente inverso para que a forma de Liouville completa p dφ se puxe a t² ξ* dξ, com B0 fixo no antibracket. Isso explicita a transformação canônica da escala; uma troca de carta no alvo não acrescenta uma potência independente de t.

Se P_E^q é o espaço de polinômios homogêneos de grau E nos jatos normalizados, com forma q, defina

\[
\mathcal R_L^q
=\prod_{E\ge0}t^{E+2L-2}P_E^q,
\qquad 0\le q\le4.
\tag{1}
\]

Cada elemento de P_E é finito em jatos e em monômios, com coeficientes suaves de jatos finitos de B0. Pode-se impor uma subclasse analítica ou de peso de engenharia, se os operadores a conservarem. A ordem de jatos não precisa ser uniformemente limitada em todos os E. O produto em (1) permite uma série infinita de valências; não avalia essa série para t numérico.

Ghost e paridade são graduações adicionais e independentes de E. Fontes centrais adicionais podem entrar como coeficientes de um multigrau externo fixado, contanto que o operador considerado não as diferencie e respeite esse multigrau. A conclusão abaixo conserva a classe (1), quando essa é a classe da entrada; não identifica toda a expansão Laurent072 com (1) por mera nomenclatura.

Para L≥1, E+2L−2≥0. Assim R_L não contém potências negativas de t. Para L=0, são possíveis t⁻² e t⁻¹ nos graus E=0/1. Isso é compatível com termos centrais e tadpoles na expansão clássica estendida.

## 3. A graduação vem dos vértices, não de uma escolha posterior

Considere um grafo conectado com V vértices, I linhas internas, E pernas externas e número topológico de laços l=I−V+1. Se o vértice v tem valência n_v e já representa uma inserção de ordem de laço L_v, seu peso é t^(n_v+2L_v−2). A igualdade de contagem é Σ n_v=E+2I. Logo

\[
\sum_v(n_v+2L_v-2)
=E+2\bigl(l+\sum_vL_v\bigr)-2.
\tag{2}
\]

Com L=l+ΣL_v, obtém-se exatamente o expoente de (1). Isso inclui vértices de contratermo já construídos que respeitem a graduação e pernas de anticampo que nunca são contraídas. A prova é combinatória; não calcula coeficientes de diagramas nem prova que algum invariante tenha coeficiente não nulo.

As operações locais de extensão que não misturam a organização formal de t mantêm esse rótulo. Trata-se de uma organização disponível na construção Q2. Uma normalização arbitrária acrescida sem respeitar esse rótulo não está automaticamente coberta pelo teorema.

## 4. Teorema da translação e sua continuidade

Suponha que B seja uma derivação par em grau total, de bidegrau (ghost −1, forma +1), com as seguintes propriedades:

1. Age apenas nos jatos do ghost normalizado C, substituindo cada um por uma 1-forma cujo coeficiente depende somente de jatos de B0.
2. Anula dx, B0 e os demais geradores normalizados.
3. Tem ação local de ordem finita sobre cada jato individual e conserva a classe de regularidade de seus coeficientes.

Então B:P_E^q→P_(E−1)^(q+1), com resultado zero quando E=0. Seja

\[
b=t^{-1}B.
\tag{3}
\]

Para um termo de (1),

\[
b\left(t^{E+2L-2}F_E^q\right)
=t^{(E-1)+2L-2}BF_E^q.
\tag{4}
\]

Portanto b preserva R_L, embora reduza o expoente isolado de t. Como ele eleva forma e há quatro dimensões, b⁵=0. Assim

\[
e^{\pm b}=\sum_{j=0}^{4}\frac{(\pm b)^j}{j!}
\tag{5}
\]

são automorfismos inversos da soma dos R_L^q. Mais precisamente, o coeficiente de grau E e forma q de eᵇF é

\[
(e^bF)_E^q
=\sum_{j=0}^{q}\frac{B^jF_{E+j}^{q-j}}{j!}.
\tag{6}
\]

O fator t^(E+2L−2) foi retirado em ambos os lados de (6). Só entram cinco coeficientes, no máximo. Cada um possui ordem de jatos finita; o resultado também. Isso prova continuidade na topologia de produto por valência e continuidade t-ádica com perda limitada de até quatro ordens. Não afirma preservação da ordem t-ádica isolada de cada entrada.

Se L≥1, todos os termos de saída continuam tendo potência de t não negativa. A perda de t por (3) acompanha exatamente a retirada de uma perna ghost. Não há uma passagem a t≠0 numérico e não é necessária uma ressoma em amplitudes finitas.

**Por que a hipótese de classe é necessária:** C^μ f(B0), escrito com potência t⁰, pertence ao espaço genérico de séries não negativas, mas não ao componente E=1 de R_1. Aplicar b produz t⁻¹dx^μ f(B0). Já a entrada permitida t C^μ f(B0) em R_1 produz dx^μ f(B0), que pertence ao componente E=0 da mesma R_1. A primeira expressão não refuta (4); mostra por que não se deve substituir R_L por todas as séries positivas.

## 5. Compatibilidade com os diferenciais

A derivada horizontal d_H conserva E: derivar um coeficiente de B0 não cria flutuação; derivar um jato de X troca esse jato por outro, mantendo uma perna. Logo d_H preserva R_L.

O antibracket nos campos normalizados retira uma perna de cada argumento. Derivadas totais nos operadores de Euler não alteram essa contagem. Se F∈R_L e G∈R_M, um par de graus E1/E2 gera E=E1+E2−2 e expoente

\[
(E1+2L-2)+(E2+2M-2)
=E+2(L+M)-2.
\tag{7}
\]

Portanto

\[
(\mathcal R_L,\mathcal R_M)\subset\mathcal R_{L+M}.
\tag{8}
\]

A cada E há somente os pares 1≤E1,E2≤E+1 com E1+E2=E+2: a operação sobre as séries é coeficiente a coeficiente finita. Termos sem campos possuem antibracket zero. Se a ação clássica normalizada S_t pertence a R_0, seu diferencial s_t=(S_t,·) preserva R_L. A existência da CME continua uma hipótese separada da contagem; no modelo, é fornecida pelas construções clássicas anteriores.

Consequentemente, a conjugação finita por eᵇ é uma equivalência de complexos na classe R_L quando s_t+d_H é o diferencial em questão e b satisfaz as hipóteses. Os comutadores d_H−[b,s_t] e [d_H,b] também preservam R_L. Uma identidade natural s_t+E_N+C_N, quando demonstrada na nota de geometria dos jatos, pode ser transportada a essa completação sem perder esse controle.

Essa equivalência não afirma que o complexo transformado seja acíclico. Também não afirma que uma homotopia posterior de s_t ou de E_N preserve (1). Cada operador adicional precisa de seu próprio controle de graus e continuidade.

## 6. Peso de engenharia e termos de curvatura

Na apresentação geométrica, escolha [g]=[φ]=0, [∇]=1, [c]=−1 e [dx]=−1, de modo que s e d_H tenham peso total zero. t tem peso zero. Isso é uma graduação de engenharia; não é uma dimensão de norma Hilbert nem uma potência de ħ.

Para a translação construída com coordenadas normais de B0, a substituição do jato ∇^r c tem a forma dx vezes um tensor de fundo de peso r. Em r=0 é dx; em r=1 o termo é zero; em r=2 surge curvatura de peso dois, e nas ordens seguintes aparecem seus jatos e produtos de peso total r. Portanto a imagem tem peso r−1, igual ao do jato original. Em uma apresentação coordenada intermediária, os coeficientes de conexão e suas derivadas possuem a mesma graduação; a expressão final deve satisfazer a naturalidade demonstrada separadamente.

Sob essa hipótese explicitada sobre os coeficientes, B e b têm peso total zero, e eᵇ preserva componentes homogêneas e cadeias finitas de logaritmos de escala já presentes na entrada. As operações são finitas, sem partição suave adicional nem integração sobre valores de campos; coeficientes analíticos permanecem analíticos se os coeficientes de B o forem.

Preservar esse peso não é provar todos os limites de extensão às diagonais para cada aridade. O número de inserções e as relações com seus submonômios continuam dados adicionais. A liberdade de renormalização inclui essas condições: [Hollands, Teorema2, equações256–259](https://arxiv.org/pdf/0705.3340v4) exige independência funcional dos campos, escala, realidade e ação por partes da aplicação multilinear inteira. Essa entrada é usada somente para delimitar o que o presente cálculo não fornece.

## 7. Resultado utilizável e obrigações que permanecem

[DERIVED] A translação finita dos ghosts, inclusive a versão natural quando suas hipóteses geométricas são satisfeitas, é bem definida e contínua na completação por laços/valência já motivada por Q2. Em laços positivos não produz potências negativas de t. A derivada horizontal e o antibracket preservam a organização, e o peso total de engenharia também é preservado sob a hipótese de homogeneidade dos coeficientes normais.

[OPEN] Falta construir uma primitiva do cociclo efetivo no complexo NATURAL com curvatura e demonstrar que os demais homotópicos conservam essa mesma classe, sua regularidade e a hierarquia de renormalização. A consistência do cociclo precisa valer na álgebra universal efetivamente utilizada. Nenhuma dessas condições foi deduzida de (6).

A nota estreita a obrigação de completação: ela deixa de recair no operador eᵇ deste teorema, para entradas de R_L, e passa a recair na construção restante da primitiva e em seu consumo por Q2. Fontes externas e inserções de pesos diferentes exigem sua própria graduação; o enunciado não as recategoriza silenciosamente.

Não se alteram P0 da entrega073, o estado físico067, os originais, o Atlas ou o gate. Não há aqui uma carga interagente construída, uma QME ou um fechamento UV.
'''
output = create(OUT / 'COMPLETACAO_POR_LACOS_E_VALENCIA.md', note)
after = [pin(ROOT / relative) for relative in SOURCES]
assert before == after
record = {
    'status': 'WRITTEN_REES_COMPLETION_TRANSLATION_THEOREM__INDEPENDENT_REVIEW_PENDING',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'sources': before,
    'outputs': [output],
    'source_bytes_unchanged': True,
    'new_cas_controls': 0,
    'new_lean_compilations': 0,
    'scope': 'Conditional operator theorem for the stated Rees module; not natural BRST acyclicity or a Q2 renormalization family.'
}
receipt = create(OUT / 'MANIFESTO_REES_074.json', json.dumps(record, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'note': output, 'manifest': receipt}, ensure_ascii=True))
