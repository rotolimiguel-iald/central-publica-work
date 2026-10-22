from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, sys

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_084_20260910'
DOC = (ROOT / sys.argv[1]).resolve()
INSPECTION = (ROOT / sys.argv[2]).resolve()
assert DOC.is_relative_to(ROOT) and INSPECTION.is_relative_to(ROOT)
assert DOC.is_dir() and INSPECTION.is_dir()

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
    return '[' + label + '](<' + path.as_posix() + '>)'

doc_notes = sorted(DOC.glob('*.md'))
inspection_notes = sorted(INSPECTION.glob('*.md'))
assert doc_notes and inspection_notes
reduction_review = ROOT / 'REVISAO_REDUCAO_ISOTROPIA_084_20260910/PARECER_ELIMINACAO_FINITA_E_CANAL_EULER_084.md'
current_review = ROOT / 'REVISAO_CORRENTE_NECESSARIA_084_20260910_061100_677142/PARECER_EULER_E_GRADIENTE_084.md'
root_review = ROOT / 'REVISOES_RAIZ_084_20260910/PARECER_FORMA_NORMAL_E_CANAL_EULER_084.md'
sources = [reduction_review, current_review, root_review, OUT / 'REEXAME_SUFICIENCIA.md',
           OUT / 'ESTADO_CANONICO_084.json'] + doc_notes + inspection_notes
before = [pin(p) for p in sources]

adendum = '''# Adendo final de revisões e proveniência084

10/09/2026. [REAL — documental; DERIVED — revisões matemáticas escritas]. Este arquivo novo conecta as revisões concluídas aos documentos emitidos antes delas. Nenhuma fonte histórica foi reescrita para mudar um estatuto pendente.

A redução por isotropia, de Herschel, recebeu parecer independente de Singer e conferência da raiz. A nota de exclusões, da raiz, recebeu parecer independente de Herschel. Os pareceres não identificaram erro material nos respectivos alcances. Os autores não aprovam como independentes suas próprias entradas antecedentes: essas dependências e revisões anteriores estão identificadas.

'''
adendum += '\n'.join([
    link('Revisão independente da redução084', reduction_review),
    link('Revisão independente das duas exclusões084', current_review),
    link('Conferência da raiz sobre a forma normal', root_review)]) + '\n\n'
adendum += 'Revisão documental específica do relatório, memória e desenho:\n\n' + '\n'.join(link(p.stem, p) for p in doc_notes) + '\n\n'
adendum += 'Inspeção complementar do estado canônico e sinais de preparação, com seu alcance próprio:\n\n' + '\n'.join(link(p.stem, p) for p in inspection_notes) + '\n\n'
adendum += '''A leitura canônica principal mede quatro arquivos idênticos a083. A presença de módulos por AST não é contagem de compilação. A inspeção complementar não atesta a inexistência de trabalho em qualquer lugar do computador: limita-se aos caminhos registrados. Os21 módulos ausentes são do conjunto acompanhado de98, não uma contagem de todas as pendências da teoria.

Contabilidade084: zero nova execução matemática/CAS, zero novos controles algébricos executados, zero controles de integridade ligados a uma execução matemática, zero Lean e zero rito de natureza. Hashes e links conferidos são controles documentais. As derivadas e substituições da prova084 usam identidades083 já revisadas, sem reexecução ou dupla contagem. Houve releitura de Chevalley–Eilenberg para o uso finito sob h. Consultas preparatórias à investigação085 não são resultados ou fontes matemáticas da entrega084.

Proveniência do parecer de Singer: sua pasta conserva um emissor documental original não executado e uma adaptação nova de separadores de caminho; essa adaptação está documentada pelo próprio recibo. Não houve execução matemática falha ocultada nessa ocorrência. Nesta retomada, tentativas de ler AGENTS.md na raiz IALD e na Central retornaram inexistência visível; as instruções globais fornecidas pelo operador e a skill tgl-atlas foram lidas. Isso não foi contado como uma leitura bem-sucedida dos arquivos ausentes.

Memória e desenho: adendos novos somente em Chatgpt, conforme a ordem de não tocar o acervo. O Atlas e o índice canônicos foram consultados, permanecendo intactos. Nenhuma alegação de atualização dos pesos do modelo ou da memória do ChatGPT online é feita nesta entrega.

O fechamento do manifesto verifica artefatos e ligações; não aprova QME, UV, reconstrução geral ou confirmação física. Investigação085 fica excluída, com sua avaliação independente própria. O objetivo geral permanece aberto.
'''
emit(OUT / 'ADENDO_REVISOES_084.md', adendum)

source_directories = [
    'REDUCAO_ISOTROPIA_CE_084_20260910',
    'REVISAO_REDUCAO_ISOTROPIA_084_20260910',
    'CORRENTE_NECESSARIA_E_LIMITE_GRADIENTE_084_20260910',
    'REVISAO_CORRENTE_NECESSARIA_084_20260910_061100_677142',
    'REVISOES_RAIZ_084_20260910', DOC.relative_to(ROOT).as_posix(), INSPECTION.relative_to(ROOT).as_posix()]
config = {
    'source_directories': source_directories,
    'new_exact_arithmetic_controls': 0, 'new_source_integrity_controls': 0, 'new_lean_compilations': 0,
    'status': 'FINITE_ISOTROPY_NORMAL_FORM__EXACT_CURRENT_PLUS_INVARIANT_EULER_CRITERION__EULER_ONLY_AND_SCALAR_GRADIENT_EXCLUDED__FULL_TARGET_OPEN',
    'written_results': [
        'Finite h-isotropy normal form for ghost-three cochains with horizontal differential: Q=qV+ftr CStr+fE CSE+dR, with coefficients in the full Killing-invariant quadratic module.',
        'The target is CE exact if and only if J_W=div V+K^2 fE, retaining the Euler curvature channel and finite jets per element.',
        'No nonzero inherited scalar multiple of J_W is Killing invariant; an Euler-only cancellation is excluded.',
        'No solution with V=c grad J_W, even allowing arbitrary invariant fE, by two derivative evaluations and a real unit; nilpotent coefficients retained.',
        'Canonical snapshot unchanged from083; separate read-only inspection of current source and preparation indicators linked.'],
    'remaining': [
        'Determine the full invariant quadratic module and the image of divergence, or construct V,f satisfying the exact target criterion.',
        'Construct an admissible finite BRST lift if the criterion is met; settle later lifts and remaining anomaly/cohomology channels.',
        'Causal counterterm admissibility, interacting charge/current, QME and compatible backgrounds, states and cutoffs.',
        'General gravitational reconstruction from the same selected data and justification of the ultraviolet route.',
        'Canonical integration and appropriate verification of new constructions and the21 absent tracked modules.'],
    'limits': 'Fixed oriented 4D space-form K>0 and nonzero real kappa, constant sigma projection, inert inherited real algebra and finite jets per element. Written reviewed derivations; no new mathematical execution, CAS, Lean or nature test. Full invariant module and divergence problem remain open in delivery084. No um execution/import, original or canonical memory mutation, gate change, or physical confirmation. Investigation085 excluded.'}
emit(OUT / 'CONFIG_ENTREGA_084.json', json.dumps(config, ensure_ascii=False, indent=2)+'\n')

tunnel = '''# ENTREGA084 — critério da corrente e canal Euler

10/09/2026. Entrega para a sessão que integra o um.py. [DERIVED — demonstrações escritas revisadas; integração Lean não realizada aqui].

O pedido de reexame após avanço motivou nova comparação: nos quatro artefatos canônicos lidos, continua a v338, sem mudança de bytes desde083. Há21 módulos ausentes dos98 acompanhados. A inspeção complementar registra o que encontrou sobre preparação, sem atribuir versão inexistente ao arquivo canônico.

A novidade matemática é a forma normal finita do CE natural para um diferencial horizontal: Q=qV+ftr CStr+fE CSE+dR, com ftr,fE invariantes por toda a álgebra de Killing. As primitivas verticais usam finitude sob isotropia; não presumem local finitude sob a álgebra inteira. Conservados dCStr=0 e dCSE=K²ν.

O resíduo é exato precisamente quando J_W=divV+K²fE. Não foi demonstrada a existência desse par, nem a nulidade do módulo de invariantes nesta entrega084. Foram excluídos o canal Euler sozinho e V=c gradJ_W mesmo com fE invariante arbitrário. Outras correntes continuam abertas.

Para eventual integração, preservar o domínio de referência fixa, as relações Weyl/EOM, os jatos finitos, a extensão escalar inerte e as condições de invariância. A condição necessária e suficiente não deve virar uma afirmação de cancelamento realizado. A etapa085 tem análise separada e não deve ser imputada a esta entrega.

Zero nova execução matemática/CAS/Lean ou rito. Pareceres e integridade documentais não são testes de natureza nem prova de QME/UV. Fase/ramo e H3 da tela não reabertos. Nenhum original foi alterado.

'''
tunnel += '\n'.join([
    link('Relatório084', OUT / 'REEXAME_SUFICIENCIA.md'),
    link('Revisões e proveniência', OUT / 'ADENDO_REVISOES_084.md'),
    link('Memória de trabalho', OUT / 'MEMORIA_DE_TRABALHO_084.md'),
    link('Desenho do fechamento', OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_084.md'),
    link('Manifesto final', OUT / 'MANIFESTO_ENTREGA_084.json')]) + '\n'
emit(ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_084_ESPONTANEA_criterio_da_corrente_e_canal_Euler.md', tunnel)
assert before == [pin(p) for p in sources]
print(json.dumps({'source_directories': source_directories, 'adendum': pin(OUT / 'ADENDO_REVISOES_084.md')}, ensure_ascii=True))
