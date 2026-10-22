"""Deliver the independently checked functional bridge; preserve prior milestones."""
from pathlib import Path
import datetime, hashlib, json, os, re
ROOT=Path(__file__).absolute().parent
OUT=ROOT.parent/'TUNEL/DO_CHATGPT'
ALLOWED={'propext','Classical.choice','Quot.sound'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,data):
    assert not p.exists(),p
    if isinstance(data,str):data=data.encode('utf-8')
    assert data
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(data)
    assert t.read_bytes()==data
    os.replace(t,p)
def jsnew(p,obj):new(p,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
spec=[
 ('V351BaseFunctionalEvaluation','20260914_092635_416376','AVALIACAO_FUNCIONAL',21),
 ('V351BaseFunctionalWeightLaws','20260914_093341_530178','LEIS_FUNCIONAIS',12),
 ('V351BaseSeriesNormality','20260914_093715_947928','NORMALIDADE_SERIES',4)]
files=[];modules=[];failed=[]
for stem,attempt,label,count in spec:
    src=ROOT/'kernel/TGLExt'/(stem+'.lean');obj=ROOT/'build/TGLExt'/(stem+'.olean')
    d=ROOT/'attempts'/attempt;run=json.loads((d/'run.json').read_bytes())
    source=src.read_text(encoding='utf-8');stdout=(d/'stdout.txt').read_text(encoding='utf-8')
    names=re.findall(r'^#print axioms (\w+)$',source,re.M)
    rows=re.findall(r"'TGLV351\.(\w+)' depends on axioms: \[([^\]]*)\]",stdout)
    assert len(names)==len(rows)==count and set(names)=={n for n,a in rows}
    assert all(set(map(str.strip,a.split(',')))<=ALLOWED for n,a in rows)
    assert run['returncode']==0 and run['source_sha256']==sha(src)
    assert not re.search(r'\b(error|warning):',stdout) and (d/'stderr.txt').stat().st_size==0
    assert not re.search(r'\b(?:sorry|native_decide|trustCompiler)\b|^\s*axiom\s',source,re.M)
    review=ROOT/'revisao'/('REVIEW_A1_'+label+'_FINAL.json')
    rr=json.loads(review.read_bytes())
    assert rr['P0']==rr['P1']==rr['P2']==0 and rr['findings']==[]
    assert rr['source']['sha256']==sha(src) and rr['author_object_sha256']==sha(obj)
    ir=rr['independent_compilation']
    assert all(ir[k] for k in ['all_exit_zero','exact_targets','trio_only','binary_byte_equal_to_author','pins_preserved'])
    report=Path(rr['report']['path']);assert sha(report)==rr['report']['sha256']
    for p,h in rr['evidence_files'].items():assert sha(Path(p))==h,p
    if label!='NORMALIDADE_SERIES':
        audit=ROOT/('AUDITORIA_A1_'+label+'.json');ar=json.loads(audit.read_bytes())
        assert ar['source_sha256']==sha(src) and ar['object_sha256']==sha(obj)
        assert ar['negative']['returncode']!=0 and ar['negative']['real_elaboration_error']
        files.append(audit)
    else:
        normal_audit=dict(status='PASS_AUTHOR_AND_INDEPENDENT__A1B_OPEN',source=str(src),
          source_sha256=sha(src),object_sha256=sha(obj),positive_attempt=str(d),
          checked_declarations=names,allowed_axioms=sorted(ALLOWED),no_warning=True,
          independent_review=str(review),independent_review_sha256=sha(review),
          additional_negative='Nao repetido: cadeia ja tem dois controles matematicos de adulteracao recusados; esta ponte foi recompilada e auditada independentemente.')
    modules.append(dict(module=stem,source=str(src),source_sha256=sha(src),object_sha256=sha(obj),
      declarations=names,theorem_count=len(re.findall(r'^theorem ',source,re.M)),definition_count=len(re.findall(r'^def ',source,re.M)),
      attempt=str(d),review=str(review),review_sha256=sha(review),report=str(report)))
    files += [src,obj,review,report,d/'run.json',d/'stdout.txt',d/'stderr.txt',d/src.name]
    files += [Path(p) for p in rr['evidence_files']]
    for part in ['module','auditor']:
        for token in ir[part]['command']:
            p=Path(token)
            if p.suffix in ('.lean','.olean') and p.is_file():files.append(p)
    stems={stem,stem+'Tampered'}
    for a in sorted((ROOT/'attempts').iterdir()):
        snap=[p for p in a.glob('*.lean') if p.stem in stems]
        if not snap or not (a/'run.json').exists():continue
        q=json.loads((a/'run.json').read_bytes())
        files+=snap+[a/'run.json',a/'stdout.txt',a/'stderr.txt']
        if q['returncode']:
            failed.append(dict(attempt=str(a),returncode=q['returncode'],source_sha256=q['source_sha256'],
              classification='ELABORATION_REJECTED' if 'object file' not in (a/'stdout.txt').read_text(encoding='utf-8') else 'ENVIRONMENT_FAILURE'))
assert sum(len(m['declarations']) for m in modules)==37
assert sum(m['theorem_count'] for m in modules)==34
previous=[]
for mn in ['MANIFESTO_A1.json','MANIFESTO_A1_BASE_SEMIFINITUDE_APROXIMANTES.json']:
    p=ROOT/mn;r=json.loads(p.read_bytes())
    for f in r['files']:
        q=Path(f['path']);assert sha(q)==f['sha256'] and q.stat().st_size==f['bytes'],q
    previous.append(dict(path=str(p),sha256=sha(p),verified_files=len(r['files'])))
    files.append(p)
driftp=ROOT/'CUSTODIA_A1_FUNCIONAIS_CANONICO_ATUAL.json';drift=json.loads(driftp.read_bytes())
assert sha(ROOT/'um.py')==drift['local']['sha256']
assert drift['embedded']['all_identical'] and drift['embedded']['local_count']==922
dp=ROOT/'DEPENDENCIAS_A1_MARCO_BASE.json';dep=json.loads(dp.read_bytes())
entries=dep['entries'][:]
for e in entries:
    assert sha(Path(e['source']))==e['source_sha256'] and sha(Path(e['object']))==e['object_sha256']
    if e.get('inherited'):
        assert sha(Path(e['source_origin']))==e['source_sha256']
        assert sha(Path(e['object_origin']))==e['object_sha256']
for m in modules:
    entries.append(dict(module='TGLExt.'+m['module'],source=m['source'],source_sha256=m['source_sha256'],
      object=str(ROOT/'build/TGLExt'/(m['module']+'.olean')),object_sha256=m['object_sha256'],inherited=False))
assert len(entries)==len({e['module'] for e in entries})==387
stamp=datetime.datetime.now().astimezone().isoformat()
note='''[REAL — avaliação e leis no cone representado verificadas; OPEN — existência do traço de A1(b)]

# A1 — avaliação funcional, leis do peso e normalidade das séries

Este é adendo ao marco anterior, sem reescrever suas fontes, memórias ou lacunas. Os três módulos novos são fornecedores Lean em bancada, ainda não embutidos no programa. A1(a) permanece pago; A1(c) está pago nestas 37 declarações; A1(b) não tem habitante de RegularCoreTraceData nem impossibilidade tipada.

## Reutilizar, sem reconstruir

Fixe M=theFactorObject P e N=regularCoreAlgebra P. A sequência D_n(A) positiva e crescente na mesma M já existia. Agora:

    m_A(ψ) = sup_n ofReal Re ψ(D_n(A)).

O domínio da definição é o dual contínuo complexo de M. Positividade, normalidade e representação não são inferidas desse nome: as hipóteses e teoremas abaixo determinam quando cada lei vale.

1. baseVectorFunctional é um funcional contínuo na própria M; sua norma é ≤‖v‖². exists_base_series_functional constrói ψ por uma série vetorial quadrado-somável, prova HasSum complexo em todo D∈M e positividade complexa. Não recebe ψ como testemunha pronta. No sentido inverso elementar, avaliar uma representação HasSum na unidade recupera a soma dos quadrados das normas.
2. baseDualEvaluation_vector identifica m_A(ω_v)=q_A(testVector v); baseDualEvaluation_vacuum identifica m_A(ω_Ω)=ν(A), incluindo infinito. São ligações de objetos, não novos pesos de mesmo nome.
3. Adição em ψ exige funcionais positivos; homogeneidade NNReal cobre 0·∞. A semicontinuidade inferior demonstrada é na norma do dual contínuo. Não é uma identificação de preduais de Banach.
4. Para uma representação HasSum, m_A(ψ)=Σ_k q_A(testVector v_k). A soma ENNReal pode ser infinita. Duas decomposições do mesmo ψ dão o mesmo resultado após média. Não foi afirmada independência do levantamento vetorial ao core antes da média.
5. O segundo módulo transfere zero/soma/escala/ordem, normalidade em A para supremos positivos internos de REDES DIRIGIDAS ARBITRÁRIAS, bimódulo e outputs limitados. ennreal_tsum_iSup_directed fornece exatamente a troca de supremo/série necessária; não impõe enumerabilidade ao índice da rede.
6. baseDualEvaluation_eq_dual_integral prova a identidade com a integral da soma dos dualQuadraticIntegrand, usando a mesma dualAmbient e dualHaarFactor=(2π)⁻¹. Tonelli foi aplicado a termos mensuráveis não negativos, permitindo infinito. O bimódulo mantém χ explicitamente representado por Bv_k; ainda não define um transporte canônico de funcionais por B.
7. baseSeriesFunctional_normal prova normalidade por ordem do próprio ψ na BASE, a partir de HasSum. baseVectorFunctional_normal reutiliza o limite forte existente de vonNeumann_exists_positive_isLUB. A igualdade é ofReal Re ψ(S)=sup_i ofReal Re ψ(A_i) para A_i≥0; positividade complexa está provada separadamente. Esta normalidade de ψ em M é distinta da normalidade de A↦m_A(ψ) em N.
8. A fidelidade é da família de avaliações, suficiente para recusar A≠0 com todas as leituras zero. O controle da média normalizada vale 1; o input unidade tem saída infinita em cada vetor não zero. Não se afirma que cada funcional ψ seja fiel.

## O endereço da obrigação seguinte

A direção **série vetorial ⇒ funcional positivo normal** está provada no mesmo M, e a avaliação média independe da decomposição. A direção inversa permanece nomeada:

    ψ : M→L[ℂ]ℂ positivo; para todo índice dirigido não vazio ι,
    A_i∈M positivos e crescentes, IsLUB(range A) S ⇒
    ofReal Re ψ(S)=sup_i ofReal Re ψ(A_i)
      ⟹ ∃v:ℕ→TowerHilbert P,
           Summable (‖v_k‖²) ∧
           ∀D∈M, HasSum (⟨v_k,Dv_k⟩) (ψ(D)).

Esse é o lema de cobertura, não uma alegação de impossibilidade. [KNOWN] O Teorema 2.41 de Bryder, pp. 50–51, enuncia e demonstra a equivalência na álgebra de von Neumann concreta, sem hipótese de Hilbert separável. A fonte foi aberta e o enunciado/prova relidos; não foi convertido em axiom Lean: https://web.math.ku.dk/~musat/Injective_and_semidiscrete_von_Neumann_algebras_final.pdf#page=67.

A construção do predual abstrato inteiro não deve virar uma nova camada obrigatória por conveniência de nome. O próximo CONSUMIDOR é regular_dual_weight_modular_implementation de LACUNAS_A1: identificar σ^ν_t=Ad Λ_t no GNS do mesmo ν. Se a prova consumir diretamente a construção escalar e as formas concretas existentes, reutilizá-las; se consumir o cone predual padrão inteiro, pagar antes a cobertura/tipagem efetivamente exigida. Não reabrir GNS, fechamento da estrela ou Moreau já construídos.

Depois permanecem regular_unitary_positive_generator e pedersen_takesaki_inverse_generator_trace: h positivo afiliado, h^{it}=Λ_t; perturbação pelo inverso de h produzindo τ fiel normal semifinito, tracial e τ∘θ_s=e^{-s}τ. A invariância do peso ν não substitui essa escala do traço. Nenhuma dessas etapas finais foi promovida por este marco.

## Validação e alcance

São três módulos, 34 teoremas e três definições: 37 declarações. Compilação autora e reprodução independente com Lean 4.31.0, sem avisos, somente propext/Classical.choice/Quot.sound, objetos idênticos. Dois controles matemáticos adulterados foram recusados: m_A(0)=0→1 e média=1→2. Tentativas rc1 e seus sorryAx de elaboração permanecem no histórico e foram excluídas. Não houve nova rodada integral de um.py: seu Python não foi modificado nem executado.

Todos os arquivos dos dois manifestos anteriores foram reconferidos. A cópia v351 continua intacta. Durante o marco o canônico mudou: a comparação está em CUSTODIA_A1_FUNCIONAIS_CANONICO_ATUAL.json; os monólitos diferem, mas os 922 fontes formais embutidos eram exatamente idênticos na leitura. Essa medição não declara o canônico congelado para sempre. A gerência deve aplicar os fornecedores sobre sua versão corrente.

Nenhuma bandeira de fronteira foi alterada, nenhum gate foi movido por esta entrega, A2–A7 não foram iniciados e nenhum resultado físico foi examinado. O objetivo A1 permanece ativo.
'''
note=note.replace('# A1 — avaliação funcional, leis do peso e normalidade das séries','# A1 — avaliação funcional, leis do peso e normalidade das séries\n\nData: '+stamp)

# Everything above is validation. Only now create this milestone's records.
jsnew(ROOT/'AUDITORIA_A1_NORMALIDADE_SERIES.json',normal_audit)
dm=ROOT/'DEPENDENCIAS_A1_MARCO_FUNCIONAL.json'
jsnew(dm,dict(timestamp=stamp,status='HASH_VERIFIED__INHERITED_NOT_REBUILT',
 previous_manifest=str(dp),previous_sha256=sha(dp),entries=entries))
adendo=ROOT/'ADENDO_A1_AVALIACAO_LEIS_NORMALIDADE.md';new(adendo,note)
files += [ROOT/'AUDITORIA_A1_NORMALIDADE_SERIES.json',dm,dp,adendo,driftp]
for n in [
 'REAPROVEITAMENTO_A1_AVALIACAO_FUNCIONAL.md','REAPROVEITAMENTO_A1_AVALIACAO_FUNCIONAL.json',
 'REAPROVEITAMENTO_A1_LEIS_FUNCIONAIS.md','REAPROVEITAMENTO_A1_LEIS_FUNCIONAIS.json',
 'REAPROVEITAMENTO_A1_NORMALIDADE_SERIES.md','REAPROVEITAMENTO_A1_NORMALIDADE_SERIES.json',
 'prepare_series_laws.py','prepare_series_normality.py','compile_a1.py','audit_functional_module.py',
 'check_canonical_drift_functional.py','search_A1_funcionais_kernel.txt','search_A1_funcionais_mathlib.txt',
 'search_A1_series_laws_0.txt','search_A1_series_laws_1.txt','search_A1_series_normality.txt',
 'revisao/CONSULTA_A1_PREDUAL_CONCRETO_QUOCIENTE.md',
 'revisao/write_consulta_predual_concreto.py']:
    p=ROOT/n;assert p.exists(),p;files.append(p)
files.append(Path(__file__).absolute())
files += list((ROOT/'probes/TGLExt').glob('V351BaseFunctional*Tampered.lean'))
for folder in (ROOT/'audits').glob('functional_*'):
    files += [p for p in folder.iterdir() if p.is_file()]
for folder in (ROOT/'revisao').glob('functional_*_independent_*'):
    files += [p for p in folder.iterdir() if p.is_file()]
for folder in (ROOT/'revisao').glob('base_series_normality_independent_*'):
    files += [p for p in folder.iterdir() if p.is_file()]
unique={str(p):p for p in files}
manifest=dict(timestamp=stamp,status='A1_FUNCTIONAL_BRIDGE_VERIFIED__A1B_OPEN',
 acceptance={'a':'PAGO_ANTERIOR_PRESERVADO','b':'NAO_PAGO','c':'PAGO_NESTAS_37_DECLARACOES'},goal='ACTIVE',
 program_sha256=sha(ROOT/'um.py'),canonical_at_read=drift['canonical'],canonical_equals_local=False,
 previous_manifests_verified=previous,dependency_entries=len(entries),modules=modules,failed_attempts=failed,
 files=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for _,p in sorted(unique.items())])
mp=ROOT/'MANIFESTO_A1_AVALIACAO_LEIS_NORMALIDADE.json';jsnew(mp,manifest)
delivery='''[REAL — ponte funcional e normalidade de séries verificadas; OPEN — A1(b), traço canônico, não quitado]

# Entrega 011 · A1 — avaliação da média dual no cone representado

Responde à ORDEM_011. Fornecedores de A1 preparados em bancada; incorporar apenas após auditoria da gerência. Não acender qgf_continuous_modular_realization_constructed com este delta.

| Critério | Estado | Evidência |
|---|---|---|
| A1(a), contrato forte e recusa do zero | PAGO, preservado | manifesto anterior reconferido |
| A1(b), habitante ou impossibilidade tipada | NÃO PAGO | faltam implementação modular, gerador e traço |
| A1(c), axiomas | PAGO no delta | 37 declarações no trio; compilação autora e reprodução independente por fonte |

'''+note+'\n\n## Fontes e reprodução\n\n'
for m in modules:
    delivery+=f"- `{m['source']}` — SHA256 `{m['source_sha256']}`; objeto `{m['object_sha256']}`; {len(m['declarations'])} declarações. Parecer `{m['report']}`.\n"
delivery+=f"\nManifesto: `{mp}` — SHA256 `{sha(mp)}`. Dependências: `{dm}` — {len(entries)} entradas, SHA256 `{sha(dm)}`. O manifesto cobre fontes, objetos, fichas, auditorias, histórico e revisões; pacotes e binários antigos não foram recompilados.\n"
delivery+='\n```powershell\n'
for m in modules:
    delivery+=f"& C:\\Python314\\python.exe -X utf8 -B '{ROOT/'compile_a1.py'}' kernel/TGLExt/{m['module']}.lean\n"
delivery+='```\n\nA ordem acima é a ordem de dependências; cada execução cria uma tentativa nova. As sondas adulteradas podem ser passadas ao mesmo compilador, esperando rc1. Os scripts de registro são de execução única e recusam sobrescrita.\n\n### Axiomas conferidos\n\n'
for m in modules:
    delivery+='\n'.join('- `TGLV351.'+n+'`: `propext`, `Classical.choice`, `Quot.sound`.' for n in m['declarations'])+'\n'
delivery+=f"\n### Custódia para integrar na versão corrente\n\nCópia v351: `{drift['local']['sha256']}` ({drift['local']['bytes']} bytes). Canônico observado em {drift['timestamp']}: `{drift['canonical']['sha256']}` ({drift['canonical']['bytes']} bytes). Os 922 fontes embutidos coincidem integralmente; nenhuma atualização desta bancada substituiu o canônico. A presença de comentários v352 foi localizada na fonte, mas sua rodada/selagem não foi auditada neste trabalho A1.\n"
delivery+='\n### Fichas de aproveitamento anexas\n\n'
for label in ['AVALIACAO_FUNCIONAL','LEIS_FUNCIONAIS','NORMALIDADE_SERIES']:
    delivery+='\n---\n\n'+(ROOT/('REAPROVEITAMENTO_A1_'+label+'.md')).read_text(encoding='utf-8')
    delivery+='\n\nFicha máquina, com tipos/fornecedores/hashes/buscas:\n\n```json\n'+(ROOT/('REAPROVEITAMENTO_A1_'+label+'.json')).read_text(encoding='utf-8')+'```\n'
dest=OUT/'ENTREGA_011_A1_avaliacao_funcional_leis_normalidade.md';new(dest,delivery)
for f in manifest['files']:
    assert sha(Path(f['path']))==f['sha256'] and Path(f['path']).stat().st_size==f['bytes'],f['path']
receipt=dict(timestamp=stamp,status='DELIVERED_PARTIAL__GOAL_ACTIVE',delivery=str(dest),delivery_sha256=sha(dest),
 manifest=str(mp),manifest_sha256=sha(mp),verified_files=len(manifest['files']),adendo_sha256=sha(adendo),
 declarations=37,theorems=34,definitions=3,acceptance=manifest['acceptance'])
jsnew(ROOT/'RECIBO_A1_AVALIACAO_LEIS_NORMALIDADE.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
