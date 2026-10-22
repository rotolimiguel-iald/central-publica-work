"""Publish a bounded A1 milestone after independent review. No canonical edits."""
from pathlib import Path
import datetime, hashlib, json, os, re

ROOT = Path(__file__).absolute().parent
OUT = ROOT.parent / 'TUNEL/DO_CHATGPT'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def new(p, text):
    assert not p.exists(), p
    raw = text.encode('utf-8') if isinstance(text, str) else text
    tmp = p.with_name(p.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
    assert len(raw) > 0 and tmp.read_bytes() == raw
    os.replace(tmp, p)

spec = [
    ('V351ExtendedBaseDualWeight', '20260914_084253_409522', 'AUDITORIA_A1_BASE_ESTENDIDA.json', 'REVIEW_A1_BASE_ESTENDIDA_FINAL.md'),
    ('V351ScalarWeightSemifiniteness', '20260914_084729_714501', 'AUDITORIA_A1_SEMIFINITUDE.json', 'REVIEW_A1_SEMIFINITUDE_FINAL.md'),
    ('V351BaseMoreauApproximants', '20260914_090140_683505', 'AUDITORIA_A1_APROXIMANTES_BASE.json', 'REVIEW_A1_APROXIMANTES_BASE_FINAL.md'),
]
files = []
modules = []
for stem, attempt, audit, review in spec:
    src = ROOT / 'kernel/TGLExt' / (stem + '.lean')
    obj = ROOT / 'build/TGLExt' / (stem + '.olean')
    adir = ROOT / 'attempts' / attempt
    run = json.loads((adir / 'run.json').read_bytes())
    au = json.loads((ROOT / audit).read_bytes())
    rev = ROOT / 'revisao' / review
    assert rev.exists(), rev
    assert 'Aceito' in rev.read_text(encoding='utf-8') or 'aceito' in rev.read_text(encoding='utf-8')
    assert run['returncode'] == 0
    assert run['source_sha256'] == au['source_sha256'] == sha(src)
    assert au['object_sha256'] == sha(obj)
    stdout = (adir / 'stdout.txt').read_text(encoding='utf-8')
    assert not re.search(r'\b(?:warning|error):', stdout)
    assert (adir / 'stderr.txt').stat().st_size == 0
    source = src.read_text(encoding='utf-8')
    names = re.findall(r'^#print axioms (\w+)$', source, re.M)
    printed = re.findall(r"'TGLV351\.(\w+)' depends on axioms: \[([^\]]*)\]", stdout)
    assert set(names) == {n for n, _ in printed}
    assert all(set(map(str.strip, a.split(','))) <= {'propext', 'Classical.choice', 'Quot.sound'} for _, a in printed)
    assert not re.search(r'\b(?:sorry|native_decide|trustCompiler)\b|^\s*axiom\s', source, re.M)
    modules.append(dict(module=stem, source=str(src), source_sha256=sha(src), object_sha256=sha(obj),
        declarations=names, theorem_count=len(re.findall(r'^theorem ',source,re.M)),
        definition_count=len(re.findall(r'^def ',source,re.M)), attempt=str(adir), review=str(rev)))
    files += [src, obj, ROOT/audit, rev, adir/'run.json', adir/'stdout.txt', adir/'stderr.txt', adir/src.name]

old = json.loads((ROOT/'MANIFESTO_A1.json').read_bytes())
for row in old['files']:
    p = Path(row['path'])
    assert sha(p) == row['sha256'] and p.stat().st_size == row['bytes'], p
program = ROOT/'um.py'
canonical = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
assert sha(program) == sha(canonical) == old['program_sha256']
assert sum(len(x['declarations']) for x in modules) == 19
assert sum(x['theorem_count'] for x in modules) == 17

for name in [
 'REAPROVEITAMENTO_A1_BASE_ESTENDIDA.md','REAPROVEITAMENTO_A1_BASE_ESTENDIDA.json',
 'REAPROVEITAMENTO_A1_SEMIFINITUDE.md','REAPROVEITAMENTO_A1_SEMIFINITUDE.json',
 'REAPROVEITAMENTO_A1_APROXIMANTES_BASE.md','REAPROVEITAMENTO_A1_APROXIMANTES_BASE.json',
 'ADENDO_REAPROVEITAMENTO_A1_APROXIMANTES_BASE.json',
 'DEPENDENCIAS_A1_BASE_ESTENDIDA.json','DEPENDENCIAS_A1_SEMIFINITUDE.json','DEPENDENCIAS_A1_MARCO_BASE.json',
 'VERIFICACAO_MARCO_A1_ANTERIOR_E_BUSCA_PREDUAL.json',
 'search_A1_base_forms.txt','search_A1_existing_notes.txt','search_A1_moreau.txt',
 'search_A1_predual_analysis.txt','search_A1_predual_kernel.txt',
 'prepare_base_form_reuse.py','compile_a1.py','audit_base_form.py','audit_moreau.py',
 'revisao/CONSULTA_A1_RESTRICAO_FORMAS_BASE.md','revisao/CONSULTA_A1_MOREAU_PREDUAL.md',
 'revisao/CONSULTA_A1_MOREAU_PREDUAL_pins.json',
]:
    p=ROOT/name
    assert p.exists(),p
    files.append(p)
files += [Path(__file__).absolute()]
failed=[]
stems={s[0] for s in spec} | {'V351ExtendedBaseDualWeightTampered','V351BaseMoreauApproximantsTampered'}
for folder in sorted((ROOT/'attempts').iterdir()):
    snapshots=[p for p in folder.glob('*.lean') if p.stem in stems]
    if not snapshots or not (folder/'run.json').exists():
        continue
    run=json.loads((folder/'run.json').read_bytes())
    files += snapshots + [folder/'run.json',folder/'stdout.txt',folder/'stderr.txt']
    if run['returncode']:
        output=(folder/'stdout.txt').read_text(encoding='utf-8')
        failed.append(dict(attempt=str(folder),returncode=run['returncode'],
            classification='ENVIRONMENT_MISSING_OBJECT' if 'object file' in output else 'ELABORATION_REJECTED'))
for stem in ['V351ExtendedBaseDualWeightTampered','V351BaseMoreauApproximantsTampered']:
    files.append(ROOT/'probes/TGLExt'/(stem+'.lean'))
for pattern in ['base_form_*','moreau_*']:
    for folder in (ROOT/'audits').glob(pattern):
        files += [p for p in folder.iterdir() if p.is_file()]
for pattern in ['extended_base_independent_*','scalar_semifiniteness_independent_*','base_moreau_independent_*']:
    for folder in (ROOT/'revisao').glob(pattern):
        files += [p for p in folder.iterdir() if p.is_file()]

stamp=datetime.datetime.now().astimezone().isoformat()
note='''[REAL — três pontes auxiliares verificadas; OPEN — A1(b), existência do traço, permanece aberta]

# A1: forma dual na base, domínio semifinito e recuperação por aproximantes

Este adendo preserva `LACUNAS_A1.md` e o manifesto anterior byte a byte. A1(a) e A1(c) já pagos permanecem pagos. A1(b) ainda não tem habitante concreto de `RegularCoreTraceData P`, nem parede contra sua existência.

## O que passa a ser fornecedor, para não ser refeito

1. `fixedFormOnBase` transporta uma forma afiliada ao fixo F para uma forma afiliada à própria base M. A afiliação é demonstrada pelos unitários de M′, amplificados por `fibre`, e pela identificação F=fibre(M). O transporte não pressupõe output limitado.
2. `baseDualWeight` é essa forma para o integral dual existente. Zero, soma, escala, ordem, fidelidade, bimódulo e normalidade por supremos internos estão provados. Avaliar no mesmo Ω dá exatamente `scalarDualWeight`, inclusive no infinito. Unidade tem valor infinito em todo vetor não zero; a média quadrática de comprimento 1 tem valor escalar 1.
3. `scalarWeight_square_finite_wot_closure` prova que nν={a∈N:ν(a*a)<∞} é WOT-denso no mesmo core N, reutilizando a aproximação forte anterior. `scalarWeight_unit_not_square_finite` recusa a unidade nesse domínio. O enunciado Lean não identifica topologias preduais arbitrárias.
4. `exists_base_moreau_approximant` produz, para c>0, D_c∈M, 0≤D_c≤cI, tal que a forma limitada de fibre(D_c) é o mínimo de q_A(w)+c‖w−v‖². Usa o resolvente já construído de A/c e c(I−R_c), sem refazer a representação do operador.
5. `exists_monotone_base_dual_approximation` produz D_n∈M positivo, crescente na ordem de operadores, e para TODO vetor da representação regular:

    q_A(v) = sup_n ofReal Re⟨v,fibre(D_n)v⟩.

A recuperação inclui q_A(v)=∞. Quando o supremo é finito, o bound de energia dá w_n→v, e o subnível fechado da mesma forma conclui a igualdade. Não foi presumida densidade do domínio finito da forma individual.

O novo delta tem três módulos, 17 teoremas e duas definições, totalizando 19 declarações auditadas no trio. São fornecedores formais de A1; não são funções novas no Python e não foram embutidos no monólito.

## A obrigação imediata, sem reiniciar o que já foi pago

Ponham-se M=theFactorObject P, N=regularCoreAlgebra P, ι=fibre e ψ∈M_*^+.
Os aproximantes agora EXISTEM em kernel. A próxima construção é

    m_A(ψ) := sup_n ofReal Re ψ(D_n(A)).

Ela deve usar funcionais normais positivos da MESMA M. Faltam tipar essa interface e provar aditividade/homogeneidade/semicontinuidade em ψ, a avaliação m_A(ω_v)=baseDualWeight(A)(v), e a extensionalidade necessária para transportar as leis em A.

Um fornecedor suficiente, precisamente delimitado, é: para cada funcional normal positivo ψ sobre esta M existe uma família v_k na Hilbert da base, com soma_k ‖v_k‖²<∞, tal que ψ(D)=soma_k ⟨v_k,Dv_k⟩ para todo D∈M. Convergência monótona dá então m_A(ψ)=soma_k baseDualWeight(A)(v_k). Alternativamente, uma extensão normal positiva ambiente com a mesma propriedade serve. Não presumir que todo ψ seja um único estado vetorial nem tratar um funcional positivo arbitrário como normal.

As buscas dirigidas no kernel e na Analysis da mathlib estão preservadas. A mathlib declara WStarAlgebra com existência abstrata de predual; isso não fornece por si só a interface concreta, sua identificação com esta representação ou o lema de decomposição. `GNSBridge` é um fornecedor de funcional finito em matrizes, não essa ponte infinita. O nome correto `exists_dualFormRepresentation` foi conferido e registrado no adendo da ficha; uma busca pelo nome com sublinhados foi negativa apenas por grafia.

## O que permanece depois dessa obrigação

As pontes 2–4 de `LACUNAS_A1.md` continuam: implementação modular do mesmo peso, gerador positivo afiliado h com h^{it}=Λ_t e perturbação por h^{-1} produzindo o traço fiel normal semifinito, tracial e com τ∘θ_s=e^{-s}τ. A invariância ν∘θ_s=ν não é essa escala; o peso ν não fornece τ diretamente. Não há parede contra a existência de τ neste marco.

Correção de exigência, ao lado do texto anterior: para o peso não tracial ν, usar o domínio nν fracamente denso como critério de semifinitude; não cobrar o campo de todos os minorantes positivos finitos de cada A, que pertence aqui ao contrato final do TRAÇO. Esse campo final não foi enfraquecido. A consulta independente registra um contraexemplo analítico de peso não tracial, explicitamente não Lean. Referência primária: Hiai, definições 7.1 e 8.1/8.5, https://arxiv.org/pdf/2004.02383.

Os três marcos não alteram o gate, não produzem dados físicos e não autorizam iniciar A2 antes de resolver A1. Canonicalidade/normalização não é inferida da mera lei de escala.
'''
note=note.replace('Este adendo preserva', 'Data: '+stamp+'\n\nEste adendo preserva')
adendo=ROOT/'ADENDO_A1_BASE_SEMIFINITUDE_APROXIMANTES.md'
new(adendo,note)
files.append(adendo)
unique={str(p):p for p in files}
manifest=dict(status='A1_MARCO_BASE_VERIFICADO__A1B_OPEN',timestamp=stamp,
    acceptance={'a':'PAGO_ANTERIOR_PRESERVADO','b':'NAO_PAGO','c':'PAGO_NOS_TRES_MODULOS'},
    goal='ACTIVE',program_sha256=sha(program),old_manifest_sha256=sha(ROOT/'MANIFESTO_A1.json'),
    previous_manifest_verified_files=len(old['files']),modules=modules,failed_attempts=failed,
    files=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for _,p in sorted(unique.items())])
mp=ROOT/'MANIFESTO_A1_BASE_SEMIFINITUDE_APROXIMANTES.json'
new(mp,json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')

delivery='''[REAL — A1 parcial: forma dual na base, densidade do domínio e aproximantes crescentes verificados; OPEN — traço canônico ainda não construído]

# Entrega 011 · A1 — forma, semifinitude e recuperação na base

Responde à ORDEM_011. A1(a) e A1(c) permanecem pagos; A1(b) NÃO PAGO. O resultado novo é uma construção efetiva de aproximantes positivos NA MESMA BASE, recuperando a forma dual inteira, somada à afiliação da forma na base e à densidade WOT do domínio escalar. Não se entrega habitante de RegularCoreTraceData nem se move gate.

As fichas de aproveitamento antecederam cada módulo e estão anexadas ao final. Nenhuma rederivação do integral, GNS, resolvente ou equivalência F=M foi introduzida.

## Critérios

| Critério | Estado | Evidência |
|---|---|---|
| A1(a), contrato forte e recusa do zero legado | PAGO, preservado | manifesto anterior inteiro reconferido |
| A1(b), habitante para todo SiteProfile ou impossibilidade tipada | NÃO PAGO | peso e aproximação construídos; rota modular/perturbação ainda aberta |
| A1(c), auditoria no trio | PAGO no delta | três módulos: 17 teoremas + 2 definições, todos rc0 sem avisos |

## Resultados e próxima obrigação

'''+note.split('## O que passa a ser fornecedor',1)[1]
delivery+='\n\n## Artefatos e reprodução\n\n'
for m in modules:
    delivery+=f"- `{m['source']}` — SHA256 `{m['source_sha256']}`; objeto `{m['object_sha256']}`; {len(m['declarations'])} declarações. Revisão: `{m['review']}`.\n"
delivery+=f"\nManifesto: `{mp}` — SHA256 `{sha(mp)}`. Contém fontes, objetos, fichas, revisões, auditorias e tentativas por hash. O manifesto anterior tem {len(old['files'])} arquivos, todos reconferidos sem alteração. Monólito local e canônico continuam idênticos: `{sha(program)}`.\n"
delivery+='\nCompilação com Lean 4.31.0 pinado (PowerShell):\n\n```powershell\n'
for m in modules:
    delivery+=f"& C:\\Python314\\python.exe -X utf8 -B '{ROOT / 'compile_a1.py'}' kernel/TGLExt/{m['module']}.lean\n"
delivery+='```\n\nCada comando cria uma tentativa nova e compila apenas o módulo no build isolado. As dependências antigas são binários herdados e verificados por hash, não uma recompilação integral. `DEPENDENCIAS_A1_MARCO_BASE.json` registra 384 entradas: 380 herdadas e quatro V351, contando o contrato anterior. A revisão independente reproduz os módulos em árvore própria. Não executar os scripts autorais de registro/auditoria novamente: eles preservam saídas imutáveis e recusam sobrescrita. As sondas adulteradas podem ser recompiladas pelo mesmo compilador, esperando rc1.\n'
delivery+='\n## Axiomas e controles\n\n'
for m in modules:
    for name in m['declarations']:
        delivery+=f"- `TGLV351.{name}`: `propext`, `Classical.choice`, `Quot.sound`.\n"
delivery+='\nO teste da média 1→2 e o teste da energia mínima acrescida de +1 foram recusados por erros reais de elaboração, não por dependências ausentes. Tentativas com `sorryAx` automático foram recusadas integralmente. A tentativa de semifinitude inicialmente sem objeto de dependência é classificada separadamente como falha de ambiente. Todas as tentativas e snapshots permanecem; o manifesto lista seus códigos. Uma tentativa intermediária Moreau rc0 com aviso de tática redundante foi substituída por uma final sem avisos, preservando o histórico.\n'
delivery+='\n## Escopo de integração\n\nA gerência pode auditar estes três módulos como fornecedores de A1. Eles não devem acender `qgf_continuous_modular_realization_constructed`: não existe ainda o traço exigido. Não houve rodada integral do Python porque nenhum byte do programa foi alterado. A2–A7, natureza, física, memórias, selos e espelho ficaram fora deste marco. A entrega é parcial e o objetivo A1 permanece ativo.\n'
delivery+='\n## Fichas anexas\n\n'
for n in ['REAPROVEITAMENTO_A1_BASE_ESTENDIDA.md','REAPROVEITAMENTO_A1_SEMIFINITUDE.md','REAPROVEITAMENTO_A1_APROXIMANTES_BASE.md']:
    delivery+='\n---\n\n'+(ROOT/n).read_text(encoding='utf-8')
delivery+='\n\nAdendo da ficha dos aproximantes (grafia do fornecedor):\n\n```json\n'+(ROOT/'ADENDO_REAPROVEITAMENTO_A1_APROXIMANTES_BASE.json').read_text(encoding='utf-8')+'```\n'
dp=OUT/'ENTREGA_011_A1_forma_base_semifinitude_aproximantes.md'
new(dp,delivery)
check=dict(timestamp=stamp,manifest_sha256=sha(mp),delivery=str(dp),delivery_sha256=sha(dp),
    adendo_sha256=sha(adendo),files_verified=len(manifest['files']),status='DELIVERED_PARTIAL__GOAL_ACTIVE')
for row in manifest['files']:
    assert sha(Path(row['path'])) == row['sha256']
new(ROOT/'RECIBO_A1_BASE_SEMIFINITUDE_APROXIMANTES.json',json.dumps(check,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(check,ensure_ascii=False,indent=2))
