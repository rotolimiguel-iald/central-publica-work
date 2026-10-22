from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_085_20260910'
DOC = (ROOT / sys.argv[1]).resolve()
assert DOC.is_relative_to(ROOT) and DOC.is_dir()

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def emit(path, text):
    raw = text.encode('utf-8')
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    temp = path.with_name(path.name + '.tmp_new')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

def link(label, path):
    return '['+label+'](<'+path.as_posix()+'>)'

qreview = ROOT / 'REVISAO_INVARIANTES_KILLING_085_20260910_061730_221515/PARECER_KT_LINEAR_E_INVARIANTES_085.md'
greview = ROOT / 'REVISAO_PRIMEIRA_PAGINA_085_20260910_062843_679705/PARECER_TODAS_VALENCIAS_E_INVARIANTES_085.md'
rreview = ROOT / 'REVISOES_RAIZ_085_20260910/PARECER_NULIDADE_INVARIANTES_QUADRATICOS_085.md'
doc_notes = sorted(DOC.glob('*.md'))
assert doc_notes
sources = [qreview,greview,rreview,OUT/'REEXAME_SUFICIENCIA.md',OUT/'ESTADO_CANONICO_085.json',
           ROOT/'REEXAME_SUFICIENCIA_084_20260910/RESULTADO_ENTREGA_084.json']+doc_notes
before = [pin(p) for p in sources]
previous = json.loads((ROOT/'REEXAME_SUFICIENCIA_084_20260910/RESULTADO_ENTREGA_084.json').read_bytes())

adendum = '''# Adendo final — revisões e custódia085

10/09/2026. [DERIVED — revisões matemáticas escritas; REAL — proveniência documental]. As duas demonstrações085 têm pareceres independentes específicos. As fontes originalmente emitidas como pendentes permanecem intactas; este adendo liga os momentos sem sobrescrever o histórico.

A prova quadrática, de Turing, foi revisada por Herschel e conferida pela raiz. A generalização a todas as valências, da raiz, recebeu revisão própria de Herschel. Sua revisão anterior da entrada quadrática não foi usada como aprovação automática da generalização. Os pareceres não identificaram erro material no domínio delimitado.

'''
adendum += '\n'.join([link('Revisão quadrática085',qreview),link('Revisão das generalizações085',greview),link('Conferência da raiz sobre a prova quadrática',rreview)])+'\n\n'
adendum += 'Revisão documental específica do relatório, memória e desenho:\n\n'+'\n'.join(link(p.stem,p) for p in doc_notes)+'\n\n'
adendum += '''Precisão matemática de linguagem: “primeira cohomologia” na nota geral designa a cohomologia de s0, ou primeira página da análise filtrada, para todos os números de ghost q indicados. Não designa apenas H¹ e não é a cohomologia total de s0+s1+s2+.... As identidades do primeiro diferencial são CE por Leibniz em cada m=E−q. Os invariantes positivos são nulos; m=0 conserva os escalares e a exceção Euler.

A aplicação primária de BBH2000 está limitada ao sistema irreducível estritamente linear, depois de pagar a KT local. A generalização usa a mesma entrada com homogeneidade m>0. A passagem auxiliar a C∞(x) retorna por especialização ao mesmo ideal das EOM; não fornece uma primitiva natural de grau quatro. A equação divV=J_W continua aberta nesta entrega.

Precisão temporal preservada ao lado: o parecer quadrático de Herschel escreveu “entrega084 encerrada” antes de sua finalização documental. O parecer posterior da generalização registra essa precisão, sem alterar o anterior. O resultado084 registra sua emissão em @PREVIOUS_TIME@. Esse instante é lido do arquivo, e não inferido do uso anterior da palavra “encerrada”.

Proveniência da revisão quadrática: uma tentativa de leitura usou nome de manifesto inexistente; a falha foi visível e o nome efetivo foi descoberto antes da leitura. Nenhum sucesso foi atribuído à tentativa que falhou. Os helpers de fontes são artefatos pinados; sua mera presença não é execução matemática auditada.

Contabilidade085: zero nova execução matemática, CAS, Lean, teste de natureza ou controle de integridade ligado a execução matemática. As contas são provas escritas. Hashes, caminhos e comparação de snapshots são controles documentais. A revisão documental tem seu alcance próprio declarado; a emissão final do adendo, túnel e manifesto é ato posterior da raiz.

O snapshot085 confirma quatro artefatos canônicos idênticos a084. A fonte do um.py, seus registros e o plano acompanhado foram apenas lidos;77/98 é presença AST de módulos, não compilação nova. Não se presume ausência de trabalho em outra cópia. A memória e o desenho foram registrados em arquivos novos de Chatgpt; o Atlas, índice, memórias canônicas e originais continuam intactos.

Consultas e investigações086 sobre correntes de uma derivada, transgressão ordinária e símbolos gerais permaneceram preparatórias e separadas. Nenhum resultado086 é contado, aprovado ou incorporado por este manifesto085.

O objetivo geral segue aberto: corrente natural completa, levantamentos/anomalias/QME, admissibilidade causal, reconstrução geral dos mesmos dados e UV. A fase/ramo e H3 da tela não são reabertas. Nenhum gate foi alterado e não há afirmação de confirmação física.
'''
adendum = adendum.replace('@PREVIOUS_TIME@',previous['created_utc'])
emit(OUT/'ADENDO_REVISOES_085.md',adendum)

config = {
    'source_directories':[
        'INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957',
        'REVISAO_INVARIANTES_KILLING_085_20260910_061730_221515',
        'PRIMEIRA_PAGINA_TODOS_GRAUS_085_20260910',
        'REVISAO_PRIMEIRA_PAGINA_085_20260910_062843_679705',
        'REVISOES_RAIZ_085_20260910', DOC.relative_to(ROOT).as_posix()],
    'new_exact_arithmetic_controls':0,'new_source_integrity_controls':0,'new_lean_compilations':0,
    'status':'POSITIVE_KILLING_INVARIANTS_ZERO__LINEAR_FIRST_PAGE_ALL_FINITE_VALENCES__HORIZONTAL_TARGET_REDUCED_TO_NATURAL_DIVERGENCE__INTERACTING_GOAL_OPEN',
    'written_results':[
        'The complete local linear KT chain is acyclic in positive antifield degree by finite Bianchi factorization and absence of identities among divergence identities.',
        'The quadratic Killing-invariant module is zero via injection into the original linear on-shell jet algebra, ordinary characteristic degree-zero cohomology, and homogeneity.',
        'The target J_W nu is CE exact precisely when J_W is the divergence of a finite natural quadratic current; positive-degree Cartan coefficients vanish.',
        'All finite-valence s0 cohomology is Rher tensor [Sym^(E-q)M tensor exterior^q G]^h, for 0<=q<=min(E,10); the first differential is CE in each m=E-q.',
        'The invariant module vanishes in every positive symmetric degree; the algebraic polynomial invariant algebra retains only inherited degree-zero scalars. Horizontal positive-degree exactness is precisely natural divergence.',
        'Independent written reviews and read-only canonical snapshot; no new mathematical execution or Lean.'],
    'remaining':[
        'Construct or exclude a finite natural quadratic current with divergence J_W in the complete admissible jet module.',
        'If possible, realize the corresponding finite BRST primitive and subsequent lifts; otherwise delimit the obstructed branch.',
        'Higher differentials, remaining anomaly cohomology, causal counterterms, interacting charge/current and QME with compatible backgrounds and states.',
        'General gravitational reconstruction from the same selected data and justification of the ultraviolet route.',
        'Canonical integration and appropriate verification of new constructions and the21 absent tracked modules.'],
    'limits':'Fixed oriented four-dimensional space-form K>0 and nonzero real kappa, constant sigma projection, inert inherited real algebra, finite jets per element. First linear cohomology and first CE differential, not full interacting BRST. Positive symmetric degree only for invariant vanishing; degree zero retains scalars/Euler. Natural divergence of J_W remains open. Zero new mathematical execution, CAS, Lean or nature tests; no original or gate changes. Investigation086 excluded.'}
emit(OUT/'CONFIG_ENTREGA_085.json',json.dumps(config,ensure_ascii=False,indent=2)+'\n')

tunnel = '''# ENTREGA085 — invariantes nulos e corrente natural

10/09/2026. [DERIVED — demonstrações escritas com revisões independentes]. Entrega para a sessão que integra o um.py. Nenhum código canônico foi alterado ou executado.

O módulo quadrático N=Rher⊗Sym²M não tem invariantes sob toda a álgebra de Killing no domínio fixado. A prova paga a KT linear completa, injeta no quociente polinomial das EOM, aplica a cohomologia característica de grau zero e usa homogeneidade. Não assume liberdade da torre Weyl, separação por testes TT ou ausência de nilpotentes.

O critério084 perde os coeficientes quadráticos das Cartan: J_Wν é CE-exato se e somente se existe corrente natural quadrática finita V com divV=J_W. A corrente continua aberta; c gradJ_W já foi excluída084.

A generalização da raiz descreve a primeira página em toda valência E: H^q(s0)_E=Rher⊗[Sym^(E−q)M⊗Λ^qG]^h para 0≤q≤min(E,10), demais zero. O primeiro diferencial é CE para todo m=E−q; invariantes são zero para todo m>0. Alvos horizontais positivos são exatos exatamente quando são divergências naturais. m=0 preserva escalares e Euler.

Ao integrar, conservar os tipos: K eκ reais fixos, referência espaço-forma, projeção métrica comφ0 constante, escalares herdados inertes, jatos finitos por elemento e relações Weyl/EOM. Não promover a primeira página a BRST total ou a condição de divergência a uma solução realizada. Investigação086 é separada.

O snapshot canônico continua v338, com77/98 módulos acompanhados presentes e21 ausentes. Presença AST não é uma compilação nova. Zero execução matemática/CAS/Lean ou rito nesta entrega. Fase/ramo eH3 da tela permanecem pagos; reconstrução geral dos mesmos dados eQME/UV seguem abertos.

'''
tunnel += '\n'.join([
    link('Relatório085',OUT/'REEXAME_SUFICIENCIA.md'),
    link('Revisões e proveniência',OUT/'ADENDO_REVISOES_085.md'),
    link('Memória de trabalho',OUT/'MEMORIA_DE_TRABALHO_085.md'),
    link('Desenho do fechamento',OUT/'DESENHO_DO_FECHAMENTO_ADENDO_085.md'),
    link('Manifesto final',OUT/'MANIFESTO_ENTREGA_085.json')])+'\n'
emit(ROOT/'TUNEL/DO_CHATGPT/ENTREGA_085_ESPONTANEA_invariantes_nulos_e_corrente_natural.md',tunnel)
assert before == [pin(p) for p in sources]
print(json.dumps({'adendum':pin(OUT/'ADENDO_REVISOES_085.md'),'sources':config['source_directories']},ensure_ascii=True))
