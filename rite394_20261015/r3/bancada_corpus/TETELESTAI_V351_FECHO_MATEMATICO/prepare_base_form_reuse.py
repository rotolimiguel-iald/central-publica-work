"""Record the A1 extended-base bridge reuse before writing formal code."""
from pathlib import Path
import datetime, hashlib, json, re, subprocess, os

ROOT = Path(__file__).absolute().parent
KERNEL = ROOT / 'kernel'
stamp = datetime.datetime.now().isoformat()
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(p, data):
    assert not p.exists(), p
    raw = data.encode('utf-8') if isinstance(data, str) else data
    temp = p.with_name(p.name + '.tmp')
    with temp.open('xb') as f:
        f.write(raw)
    assert temp.read_bytes() == raw and len(raw) > 0
    os.replace(temp, p)

specs = [
 ('V351RegularCoreTraceContract.lean', 'structure RegularCoreTraceData', 'CONSUMIDOR', 'A1(b): o traço neste cone e nesta ação. A ponte de base integra a identificação do peso usado para a perturbação; não fornece ainda o traço.'),
 ('V350DualClosedForm.lean', 'structure AffiliatedPositiveForm', 'REUSAR', 'Forma positiva fechada estendida com invariância sob o comutante unitário; mesma tipagem, agora na base.'),
 ('V350DualFixedWeightLaws.lean', 'def dualFixedWeight', 'ADAPTAR', 'Fornecedor retorna AffiliatedPositiveForm(dualFixedCore P); exigimos saída em AffiliatedPositiveForm(theFactorObject P).'),
 ('V350DualFixedWeightLaws.lean', 'theorem dualFixedWeight_bimodule', 'REUSAR', 'Transportar pela equivalência e pela isometria já construídas.'),
 ('V350DualFixedWeightLaws.lean', 'theorem dualFixedWeight_preserves_internal_isLUB', 'REUSAR', 'Normalidade do mesmo integral, aplicada aos vetores da base.'),
 ('V350FixedBaseEquivalence.lean', 'def fixedBaseEquiv', 'REUSAR', 'Equivalência concreta entre M e F, não hipótese abstrata.'),
 ('V350FixedCoreBaseIdentification.lean', 'theorem dualFixedCore_eq_amplified_base', 'REUSAR', 'Identificação de cada operador fixo com fibre de um elemento da base.'),
 ('V350L2Order.lean', 'def testVectorIsometry', 'REUSAR', 'H →ₗᵢ[ℂ] L²(R,H); fornece continuidade e linearidade para restrição da forma.'),
 ('V350L2OperatorLift.lean', 'def fibreRepresentation', 'REUSAR', 'Amplifica o unitário de M′ para provar afiliação da forma restrita.'),
 ('V350ScalarDualWeight.lean', 'theorem scalarDualWeight_bounded_base_value', 'ADAPTAR', 'A hipótese exige output limitado; o novo caso cobrirá ENNReal inclusive infinito.'),
 ('V350ScalarDualWeight.lean', 'theorem scalarDualWeight_square_finite_strong_density', 'REUSAR', 'Não substituir a semifinitude de peso por exigência mais forte de minorantes finitos de cada positivo.'),
]
providers=[]
for fname, declaration, decision, reason in specs:
    p=KERNEL/'TGLExt'/fname
    lines=p.read_text(encoding='utf-8').splitlines()
    hits=[i for i,l in enumerate(lines) if l.startswith(declaration)]
    assert len(hits)==1,(fname,declaration,hits)
    i=hits[0]; snippet=[]
    for line in lines[i:i+25]:
        snippet.append(line)
        if ':=' in line or line.endswith(' where'):
            break
    providers.append(dict(file=str(p),line=i+1,sha256=digest(p),declaration=declaration,statement='\n'.join(snippet),decision=decision,reason=reason))

searches=[]
for name,args in [
 ('base_forms',['rg','-n','AffiliatedPositiveForm|baseForm|extendedPositive|predual',str(KERNEL/'TGLExt'),'-g','V350*.lean']),
 ('existing_notes',['rg','-n','extended.positive|predual|forma.*base|base.*forma|semifinit',str(ROOT.parent/'TETELESTAI_V350_KERNEL_20260911'/'TRACO_PROXIMAS_OBRIGACOES.md')]),
]:
    r=subprocess.run(args,capture_output=True)
    assert r.returncode in (0,1),r.stderr
    out=ROOT/('search_A1_'+name+'.txt')
    write_new(out,r.stdout)
    searches.append(dict(command=args,returncode=r.returncode,lines=len(r.stdout.splitlines()),output=str(out),sha256=digest(out)))

record=dict(timestamp=stamp,status='FICHA_ANTES_DO_CODIGO_FORMAL',target='A1(b), ponte regular_scalar_weight_is_dual_weight: forma na base',
 exact_target='(P : SiteProfile) → AffiliatedPositiveForm (dualFixedCore P) → AffiliatedPositiveForm (theFactorObject P), value(v)=Q.value(testVector v)',
 actual_consumer='RegularCoreTraceData P; LACUNAS_A1.md item 1, entrada para item 4. Não há nova bandeira/gate.',
 acceptance=['afiliacao na base provada','avaliacao no mesmo Omega igual a scalarDualWeight, incluindo infinito','leis transportadas por fornecedores existentes','nao declarar isomorfismo geral do cone/predual sem prova'],
 providers=providers,searches=searches,
 inherited_searches={str(ROOT/n):digest(ROOT/n) for n in ['REAPROVEITAMENTO_A1.json','ADENDO_REAPROVEITAMENTO_A1.json','BUSCAS_A1.json','OUTRAS_BANCADAS_HASHES.json']},
 decision='ADAPTAR: mudar o espaço de representação por isometria e provar afiliação; nenhuma rederivação do integral, do GNS ou da álgebra fixa.',
 not_paid=['identificacao geral do cone estendido com funcionais do predual','implementacao modular do peso','gerador positivo afiliado','perturbacao inversa produzindo traco fiel normal semifinito'])
write_new(ROOT/'REAPROVEITAMENTO_A1_BASE_ESTENDIDA.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
md='[REAPROVEITAMENTO — ANTES DO CÓDIGO FORMAL]\n\n# A1: forma dual na base\n\n'+stamp+'\n\n'
md+='Consumidor: `RegularCoreTraceData P`, via a ponte 1 de `LACUNAS_A1.md` e a perturbação do peso. O alvo local é transportar `AffiliatedPositiveForm (dualFixedCore P)` para `AffiliatedPositiveForm (theFactorObject P)`, usando `testVectorIsometry` e provando afiliação. A avaliação no mesmo Ω deve ser igual ao peso escalar em ENNReal, sem hipótese de finitude.\n\n'
for p in providers:
    md+=f"- **{p['decision']}** `{p['declaration']}`, `{p['file']}:{p['line']}`; SHA256 `{p['sha256']}`. {p['reason']}\n\n```lean\n{p['statement']}\n```\n\n"
md+='As seis modalidades de busca de A1 constam da ficha original e de seus adendos, cujos hashes são referidos no JSON. As duas buscas adicionais estão registradas integralmente. Não se afirma ausência universal de fornecedor.\n\nEste marco não paga A1(b): a identificação abstrata do cone/predual e as pontes modulares/gerador/traço continuam explícitas. Não se cria nova camada Python nem se altera o gate.\n'
write_new(ROOT/'REAPROVEITAMENTO_A1_BASE_ESTENDIDA.md',md)
print(json.dumps({'providers':len(providers),'searches':searches,'formal_code_written':False},ensure_ascii=False,indent=2))
