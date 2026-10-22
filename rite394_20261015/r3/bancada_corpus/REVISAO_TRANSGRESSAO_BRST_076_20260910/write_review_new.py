from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

ROOT = Path('C:/IALD/Central de Patentes/Chatgpt').resolve()
OUT = ROOT / 'REVISAO_TRANSGRESSAO_BRST_076_20260910'
SOURCES = [
    ROOT / 'TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md',
    ROOT / 'COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md',
    ROOT / 'MODULOS_BRST_EBAR_076_20260910/MODULOS_H3_H4_E_SETOR_CALCULADO.md',
]

NOTE = r'''# Parecer independente: transgressão BRST característica e ghost4

10/09/2026. Revisor: subagente prepare_integration_83. [DERIVED — revisão matemática escrita].

**Parecer: não encontrei erro material na demonstração examinada.** A identidade natural formal \(sT_0^3=\rho_P(g)c^0c^1c^2c^3\) está demonstrada, para os polinômios característicos quadráticos e na apresentação métrica com referência inerte declarada. Conferi separadamente a curvatura total, o transporte métrico, a transgressão graduada, sua componente de forma zero e a organização por valência. Este parecer não classifica os módulos completos e não aprova uma QME.

Fonte principal, lida integralmente: [Transgressão total e primitiva de ghost4](<C:/IALD/Central de Patentes/Chatgpt/TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md>). Controle de completação: [Rees074](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>). A relação de chegada é comparada à família de ciclos, sem assumir sua independência, de [Módulos076](<C:/IALD/Central de Patentes/Chatgpt/MODULOS_BRST_EBAR_076_20260910/MODULOS_H3_H4_E_SETOR_CALCULADO.md>).

## 1. Sinais da curvatura total

Uso as convenções da fonte: \(D=s+d_H\), \(sg=\mathcal L_cg\), \(sc^\mu=c^\rho\partial_\rho c^\mu\); \(dx\) e \(c\) são ímpares e anticomutam. A matriz \(v^\mu{}_{\nu}=\nabla_\nu c^\mu\) é tensorial. Em coordenadas normais de g no ponto, \(\Gamma=0\), mas

\[
s\Gamma^\mu{}_{\nu\rho}
=c^\sigma\partial_\sigma\Gamma^\mu{}_{\nu\rho}
 +\partial_\nu\partial_\rho c^\mu.
\tag{R1}
\]

Na parte mista, \(s(\Gamma_\rho dx^\rho)=-dx^\rho s\Gamma_\rho\). Além disso, deslocar v através de dx em \(v\omega\) produz o sinal que deixa \([\Gamma_\rho,v]\). Portanto

\[
(D\mathcal A+\mathcal A^2)_{1}^{1}
=dx^\rho(\partial_\rho v-s\Gamma_\rho+[\Gamma_\rho,v])
=dx^\rho R^\mu{}_{\nu\rho\sigma}c^\sigma.
\tag{R2}
\]

No componente ghost2, a derivada de \(sc\) fornece
\((\partial_\nu c^\lambda)(\partial_\lambda c^\mu)=-(v^2)^\mu{}_{\nu}\).
O termo \(c^\rho\partial_\rho\partial_\nu c^\mu\) cancela \((\partial_\nu\partial_\rho c^\mu)c^\rho\), pois as segundas derivadas do ghost continuam ímpares. A contribuição que sobra é

\[
(sv+v^2)^\mu{}_{\nu}
=\partial_\sigma\Gamma^\mu{}_{\nu\rho}\,c^\sigma c^\rho
=\tfrac12R^\mu{}_{\nu\sigma\rho}c^\sigma c^\rho.
\tag{R3}
\]

Assim a fonte tem os sinais e os fatores corretos em

\[
\mathcal F^\mu{}_{\nu}
=\tfrac12R^\mu{}_{\nu\rho\sigma}
(dx^\rho+c^\rho)(dx^\sigma+c^\sigma).
\tag{R4}
\]

A escolha pontual de coordenadas normais verifica uma identidade tensorial sob mudanças FIXAS de coordenadas. Não equivale a definir uma operação de normalização dependente de g que comutaria com s. A fonte distingue corretamente essas duas operações ao conservar (R1).

## 2. Compatibilidade métrica e sinal do transporte

A identidade \(Dg=\mathcal A^Tg+g\mathcal A\) confere: a parte horizontal é Levi-Civita e a parte de ghost é \(v^Tg+gv=\mathcal L_cg\), com os termos \(\Gamma c\) reconstruindo \(c\cdot\partial g\).

Para S par, \(g=S^Tg_0S\) implica

\[
Dg=(DS)^Tg_0S+S^T(Dg_0)S+S^Tg_0DS.
\tag{R5}
\]

Multiplicar essa identidade por \(S^{-T}\) e \(S^{-1}\) e usar a compatibilidade de g dá

\[
Dg_0=\mathcal A_1^Tg_0+g_0\mathcal A_1,
\qquad
\mathcal A_1=S\mathcal AS^{-1}-(DS)S^{-1}.
\tag{R6}
\]

O sinal menos é necessário. A mesma fórmula vem da identidade de operadores
\(S(D+\mathcal A)S^{-1}=D+\mathcal A_1\), que fornece \(\mathcal F_1=S\mathcal FS^{-1}\) quando \(D^2=0\). O termo \(sS\) é necessário já na parte de forma zero; omiti-lo tornaria k incompatível com g0 em geral.

Como \(sg_0=0\), \(\mathcal A_0=\bar\omega\) tem a mesma compatibilidade, e \(\Theta=\mathcal A_1-\mathcal A_0\) toma valores em \(\mathfrak{so}(g_0)\). Sua componente \(k=SvS^{-1}-(sS)S^{-1}\) é g0-antissimétrica. A referência não é tratada como constante em x: \(Dg_0=d_Hg_0\) e \(\mathcal F_0=\bar R\), com toda a conexão de fundo preservada.

Na raiz formal \(S=(1+t g_0^{-1}h)^{1/2}\), \(\det S=1+O(t)\), de modo que o transporte conserva a orientação formal utilizada pelo polinômio de Euler. Este caso exige a orientação, ou sua formulação equivalente com coeficientes torcidos. Não há aqui autorização para escolher a raiz real entre métricas Lorentzianas arbitrariamente afastadas.

Produtos de matrizes com entradas ímpares exigem transposição e ciclicidade graduadas. Não encontrei na fonte uso de uma transposição não graduada incorreta; os fatores S empregados em (R5–R6) são pares. Em particular, o cálculo não importa o ghost Lorentz cru nem a regra inadequada de translação de frames identificada em 074.

## 3. Transgressão e componente de ghost3

Se \(\mathcal A_u=\mathcal A_0+u\Theta\), então
\(\partial_u\mathcal F_u=D_u\Theta\) e \(D_u\mathcal F_u=0\).
Pela invariância de P, incluindo a paralelidade da forma bilinear de Euler para conexões métricas,

\[
\partial_uP(\mathcal F_u,\mathcal F_u)
=2D P(\Theta,\mathcal F_u).
\tag{R7}
\]

Integrar o polinômio em u produz exatamente

\[
\mathcal T_P
=2P(\Theta,\mathcal F_0)+P(\Theta,D_0\Theta)
 +\tfrac23P(\Theta,\Theta^2),
\qquad
D\mathcal T_P=P(\mathcal F_1,\mathcal F_1)-P(\bar R,\bar R).
\tag{R8}
\]

[KNOWN] A referência primária [Chern–Simons, §3, proposição 3.2 e argumento de variação](https://math.mit.edu/juvitop/pastseminars/notes_2019_Fall/Chern-Simons.pdf) fundamenta a identidade de transgressão por invariância e Bianchi. A verificação da conexão total BRST específica e do transporte métrico acima é o cálculo presente; não a atribuo ao artigo como aplicação já demonstrada ao modelo.

Projetar (R8) em forma zero retira \(\mathcal F_0\) e \(\mathcal A_0\). Assim

\[
T_0^3=P(k,sk)+\tfrac23P(k,k^2)
=P(k,\mathcal F_{1,0}^{2})-\tfrac13P(k,k^2).
\tag{R9}
\]

Controle adicional no caso traço: a regra graduada dá
\(s\operatorname{tr}(k\,sk)=\operatorname{tr}(sk\,sk)\),
\(s\operatorname{tr}(k^3)=3\operatorname{tr}(sk\,k^2)\) e
\(\operatorname{tr}(k^4)=0\), pois deslocar o primeiro k através dos outros três troca o sinal. Logo \(sT_0^3=\operatorname{tr}((sk+k^2)^2)\). Para o outro polinômio invariante, (R7–R8) fornecem a mesma identidade sem depender da representação por traço.

Em quatro dimensões, (R4) permite substituir os quatro geradores exteriores por \(dx^\mu+c^\mu\). Escrevendo \(P_g(R,R)=\rho_P(g)dx^0dx^1dx^2dx^3\), resulta

\[
P(\mathcal F_1,\mathcal F_1)
=\rho_P(g)\prod_{\mu=0}^3(dx^\mu+c^\mu),
\qquad
\boxed{sT_0^3=\rho_P(g)c^0c^1c^2c^3.}
\tag{R10}
\]

Não falta um fator 4! nessa convenção: \(\rho_P\) já é o coeficiente da forma exterior ordenada. A normalização escolhida para P multiplica simultaneamente \(\rho_P\) e T; não cabe alterar uma delas isoladamente.

## 4. Rees, regularidade e escopo

Para \(g=g_0+t h\), \(c=tC\), um termo \(t^m h^m\) de S varia de duas maneiras. A parcela \(s_th=\mathcal L_Cg_0\) gera \(t^m h^{m-1}C\), de valência m. A parcela \(s_th=t\mathcal L_Ch\) gera \(t^{m+1}h^mC\), de valência m+1. Portanto cada monômio mantém o pareamento potência \(t^E\)/valência E, ainda que s misture E. O mesmo vale para \(s_tC=tC\partial C\), inversos formais e derivadas.

Uma conferência de primeira ordem é

\[
k=t\left(\bar\nabla C-\tfrac12g_0^{-1}\mathcal L_Cg_0\right)+O(t^2),
\tag{R11}
\]

isto é, a parte g0-antissimétrica de \(\bar\nabla C\). As fórmulas não geram inversos de t. Para cada valência fixada, as séries binomiais e seus produtos têm somente um número finito de contribuições, com ordem finita de jatos. O prefator \(t^{2L-2}\) coloca os elementos na classe \(\mathcal R_L\) definida em 074. Este último enunciado é de pertença algébrica; não calcula um diagrama nem atribui por si uma ordem física de laço a um coeficiente.

As operações são naturais na vizinhança formal da diagonal de métricas, com referência transformada simultaneamente. Não requerem somar a série em t numérico. A fonte não promove sua pertença à completação à admissibilidade da família inteira de produtos temporais, escala por aridade, independência funcional, inserções, realidade e contatos.

O componente de forma quatro continua sendo
\(d_HT_3^0=P_g(R,R)-P_{g_0}(\bar R,\bar R)\).
O termo característico diagonal do fundo permanece; não há conflito com a obstrução de Euler074. A prova tem grau total quatro. Não trivializa por isso uma anomalia de grau total cinco, nem demonstra que todas as densidades da família076 são s-exatas.

## 5. Estatuto da revisão e custódia

[DERIVED] Parecer favorável no escopo descrito, sem erro material identificado. Relação explícita entre os representantes característicos de ghost4 e a primitiva natural formal (R9). Não afirmo independência ou exaustividade das classes de H³/H⁴; não importo a cohomologia global suave para a completação formal.

[REAL — documental] O manifesto mede as três fontes antes/depois da emissão, os bytes do parecer e o script criador. A conferência de links e pins é documental, não CAS, Lean ou prova automática. Nenhum original ou fonte congelada foi modificado; nenhum um.py foi executado/importado. Esta revisão é específica desta prova. Não reutiliza o parecer de módulos nem atribui aprovação a outra pessoa.

[OPEN] Classificação restante dos módulos/canais da anomalia, primitivas admissíveis da família causal e QME. O manifesto da raiz e qualquer relatório de entrega posterior não foram auditados por este parecer.
'''


def pin(path):
    data = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}


def write_exclusive(path, data):
    if path.exists():
        raise FileExistsError(path)
    temp = path.with_name(path.name + '.tmp_new')
    with temp.open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if temp.read_bytes() != data:
        raise RuntimeError('temporary byte check failed')
    if path.exists():
        raise FileExistsError(path)
    temp.rename(path)
    if path.read_bytes() != data:
        raise RuntimeError('final byte check failed')


before = [pin(path) for path in SOURCES]
OUT.mkdir(exist_ok=True)
note_path = OUT / 'PARECER_TRANSGRESSAO_TOTAL_E_GHOST4.md'
write_exclusive(note_path, NOTE.encode('utf-8'))
after = [pin(path) for path in SOURCES]
if before != after:
    raise RuntimeError('SOURCE_CHANGED: preserve outputs and inspect')
links = re.findall(r'\]\(<(C:/[^>]+)>\)', NOTE)
link_checks = [{'path': p, 'exists': Path(p).is_file()} for p in links]
if not all(item['exists'] for item in link_checks):
    raise RuntimeError('LOCAL_LINK_MISSING: preserve output and inspect')
manifest = {
    'kind': 'independent_mathematical_written_review',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'reviewer': '/root/prepare_integration_83',
    'verdict': 'NO_MATERIAL_ERROR_IDENTIFIED_IN_STATED_SCOPE',
    'scope': 'metric BRST total transgression; quadratic characteristic polynomials; formal neighborhood; Rees valence completion',
    'source_pins_before': before,
    'source_pins_after': after,
    'sources_unchanged': before == after,
    'review': pin(note_path),
    'creator': pin(Path(__file__).resolve()),
    'local_links': link_checks,
    'primary_source': {'title': 'Chern and Simons, Characteristic Forms and Geometric Invariants',
                       'url': 'https://math.mit.edu/juvitop/pastseminars/notes_2019_Fall/Chern-Simons.pdf',
                       'consulted': 'section 3, proposition 3.2 and variation argument'},
    'tests': {'CAS': 0, 'Lean': 0, 'um_py_execution_or_import': 0},
    'not_claimed': ['complete H3/H4 classification', 'QME', 'entire causal normalization hierarchy', 'numerical summation of formal series', 'review of later parent manifests'],
}
manifest_path = OUT / 'MANIFESTO_REVISAO_TRANSGRESSAO_076.json'
write_exclusive(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'review': pin(note_path), 'manifest': pin(manifest_path),
                  'sources_unchanged': True, 'source_count': len(before),
                  'local_links_existing': len(link_checks)}, ensure_ascii=False))
