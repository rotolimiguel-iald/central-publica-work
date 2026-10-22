from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_075_20260910'
review_dir = Path(sys.argv[1]).resolve()
assert review_dir.is_relative_to(ROOT) and review_dir.is_dir()
assert review_dir.name.startswith('REVISAO_DOCUMENTAL_RELATORIO_075')
review_notes = list(review_dir.glob('PARECER*.md'))
assert len(review_notes) == 1
review = review_notes[0]
assert review.stat().st_size > 0
created = []

def new(path, text):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    data = text.encode('utf-8')
    assert data
    temporary = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temporary.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == data
    temporary.rename(path)
    assert path.read_bytes() == data
    created.append({'path':path.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})

def link(path, label):
    return '[' + label + '](<' + path.as_posix() + '>)'

new(OUT / 'ADENDO_REVISOES_075.md', """# Adendo de revisões075

10/09/2026. [DERIVED — demonstrações e revisões escritas] [REAL — integridade documental].

A prova por símbolos de Singer, o complemento de topforma de Turing e sua composição foram lidos integralmente pela raiz. O parecer independente de Turing sobre a composição foi favorável com hipóteses explícitas. A auditoria de Herschel sobre a aplicação causal relativa foi lida integralmente e recebeu revisão favorável separada da raiz.

A revisão preserva quatro distinções: (i) v é independente de Z até a avaliação final; (ii) a topforma requer operadores Euler nulos, não basta ser fechada; (iii) a homotopia horizontal preserva E,N, mas intercalar s pode misturá-los; (iv) liberdade de jatos dinâmicos não exige liberdade de todos os jatos de B0. O argumento desce por ideais diferenciais exclusivamente dos coeficientes B0.

A nota de aplicação consome o esquema causal069/072. Fontes positivas centrais entram com seus jatos livres em Z ou saem por projeção compatível. A extensão com tadpoles Laurent mantém sua filtração própria. Não se impuseram EOM dinâmicas, não se acrescentaram conjugados de fundo à álgebra de inserções e não foram omitidos contatos de cutoff.

O resultado escrito aceito é Ω natural fechado. A primitiva total, sua admissibilidade como família de contratermos e QME permanecem abertas. A comparação entre a classe cohomológica global, a completação formal e a categoria efetiva de referência continua obrigação da etapa seguinte. Resultados076 não integram esta custódia.

""" + link(review, 'Parecer documental independente') + """

A conferência final de hashes e links é documental; não conta teoremas. Nenhum original foi alterado, nenhum um.py executado/importado, nenhum novo CAS/Lean/diagrama/teste de natureza realizado. O gate e o objetivo geral não foram declarados concluídos.
""")
new(ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_075_ESPONTANEA_descida_natural_relativa_e_obrigacoes_restantes.md', """# Entrega075 — descida natural relativa

10/09/2026. Destinada à sessão que codifica o um.py. [DERIVED — matemática escrita revisada]. Não é ordem para mover o gate.

O canônico foi relido por bytes e AST: conserva a v338 da captura074, com selo correspondente. O conjunto anterior de 98 módulos segue com 77 presentes e 21 ausentes. O programa não foi executado ou importado.

**Material a incorporar com suas hipóteses:** lema horizontal natural por símbolos em jatos livres de ghost não zero; complemento de topforma via primeira variação e Euler; composição da descida inteira; controle por valência/Rees; aplicação relativa ao esquema causal de referência.

De uma quebra natural com consistência off-shell obtém-se Ω natural com (s+d_H)Ω=0. Relações diferenciais somente de B0 são compatíveis com a construção; relações que atinjam os jatos Z não são. Fontes positivas como ω precisam ser contabilizadas ou retiradas por mapas de complexos. A apresentação é a métrica efetiva; não estender automaticamente ao ghost Lorentz cru.

**Não registrar como concluído:** primitiva total de Ω, nulidade da classe de anomalia, família admissível de contratermos, carga interagente ou QME. A construção da descida é um passo da rota, com revisão escrita, sem nova compilação Lean.

Continuam a correspondência gravitacional geral pelos mesmos dados selecionados, compatibilidade de referências e rota UV. Preservar fase/ramo, H3 interno e os falsificadores existentes.

""" + link(OUT / 'REEXAME_SUFICIENCIA.md', 'Relatório e tabela de pendências') + '\n\n' +
link(OUT / 'ADENDO_REVISOES_075.md', 'Revisões e precisões de consumo') + '\n\n' +
link(OUT / 'MEMORIA_DE_TRABALHO_075.md', 'Memória da etapa') + '\n\n' +
link(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_075.md', 'Adendo do caminho crítico') + '\n\n' +
link(OUT / 'MANIFESTO_ENTREGA_075.json', 'Manifesto de integridade') + """

Todas as escritas desta entrega são novas e estão em Chatgpt. Originais, Atlas, índice, memórias canônicas e selos permanecem intactos.
""")
new(OUT / 'CONFIG_ENTREGA_075.json', json.dumps({
    'source_directories':[
        'DESCIDA_NATURAL_SIMBOLOS_075_20260910',
        'AUDITORIA_DESCIDA_NATURAL_075_20260910',
        'REVISAO_DESCIDA_E_REES_075_20260910',
        'APLICACAO_DESCIDA_OFFSHELL_075_20260910_022420_157704',
        'REVISOES_RAIZ_075_20260910',
        review_dir.name
    ],
    'new_cas_controls':0,
    'new_lean_compilations':0,
    'status':'WRITTEN_NATURAL_DESCENT_AND_RELATIVE_OFFSHELL_APPLICATION__TOTAL_ANOMALY_PRIMITIVE_OPEN',
    'written_results':[
        'Natural horizontal primitives by free-variation principal symbols in positive ghost degree and form degree below four.',
        'Natural first descendant from vanishing Euler operators of the consistent topform, and complete natural closed descent.',
        'Horizontal primitives preserve loop/valence Rees components with connections on fixed background bundles.',
        'Relative application to the off-shell causal insertion algebra, stable under differential relations solely on background coefficients.',
        'Explicit central-source routes and limits of reference universality and causal admissibility.'
    ],
    'remaining':[
        'Total primitive and actual natural formal BRST cohomology with background-coefficient E2 groups.',
        'Admissible all-order causal counterterms, insertion/contact identities, current/charge implementation and QME.',
        'Perturbative agreement and compatible background/state/cutoff families.',
        'General gravitational correspondence from the same selected TGL data and justified UV route.',
        'Canonical integration and appropriate formal verification of written constructions and absent modules.'
    ],
    'limits':'Written reviewed mathematics under the declared causal and free-jet hypotheses. Natural descent is not total exactness or anomaly removal. No new CAS, Lean, diagrams or nature tests; originals and canonical memories read-only. No gate modification or full-goal completion. Stage076 excluded.'
},ensure_ascii=False,indent=2) + '\n')
print(json.dumps(created,ensure_ascii=True))
