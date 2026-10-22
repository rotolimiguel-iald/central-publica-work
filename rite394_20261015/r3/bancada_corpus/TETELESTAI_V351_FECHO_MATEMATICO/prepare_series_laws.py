"""Record reuse before the consumer laws, without changing any prior artifact."""
from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
ROOT=Path(__file__).absolute().parent
K=ROOT/'kernel/TGLExt'
M=ROOT.parent/'TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,data):
    if isinstance(data,str): data=data.encode('utf-8')
    assert not p.exists(),p
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f: f.write(data)
    assert t.read_bytes()==data
    os.replace(t,p)
spec=[
 (K/'V351RegularCoreTraceContract.lean','structure RegularCoreTraceData','CONSUMIDOR FINAL'),
 (K/'V351BaseFunctionalEvaluation.lean','theorem baseDualEvaluation_eq_hasSum_series','REUSAR descida na mesma M'),
 (K/'V351ExtendedBaseDualWeight.lean','theorem baseDualWeight_add','REUSAR zero/soma/escala/ordem/fidelidade/bimodulo'),
 (K/'V351ExtendedBaseDualWeight.lean','theorem baseDualWeight_bounded_value','REUSAR controle limitado'),
 (K/'V350DualFormNormality.lean','theorem regularDualForm_preserves_internal_isLUB','ADAPTAR supremo de redes, sem impor enumerabilidade'),
 (K/'V350DualWeightForm.lean','def dualQuadraticIntegral','REUSAR mesma acao dual e Haar'),
 (K/'V350DualWeightForm.lean','theorem dualQuadraticIntegrand_measurable','REUSAR Tonelli'),
 (M/'Data/ENNReal/Operations.lean','lemma iSup_add_iSup_of_monotone','ADAPTAR somas finitas e serie para rede arbitraria'),
 (M/'Topology/Algebra/InfiniteSum/ENNReal.lean','protected theorem tsum_eq_iSup_nat','REUSAR'),
 (M/'MeasureTheory/Integral/Lebesgue/Add.lean','theorem lintegral_tsum','REUSAR')]
providers=[]
for p,name,decision in spec:
    lines=p.read_text(encoding='utf-8').splitlines()
    hits=[i for i,l in enumerate(lines) if re.match(re.escape(name)+r'(?=\s|\{|\(|:|$)',l)]
    assert len(hits)==1,(p,name,hits)
    i=hits[0];statement=[]
    for l in lines[i:]:
        statement.append(l)
        if ':=' in l or ' where' in l: break
    providers.append(dict(file=str(p),line=i+1,sha256=sha(p),declaration=name,statement='\n'.join(statement),decision=decision))
queries=[['rg','-n','baseDualEvaluation|series.*normal|tsum.*iSup|iSup.*tsum',str(K),'-g','*.lean'],
 ['rg','-n','sum_iSup|iSup_add_iSup_of_monotone|lintegral_tsum',str(M/'Data/ENNReal'),str(M/'Topology/Algebra/InfiniteSum/ENNReal.lean'),str(M/'MeasureTheory/Integral/Lebesgue/Add.lean')]]
searches=[]
for n,args in enumerate(queries):
    r=subprocess.run(args,capture_output=True)
    assert r.returncode in (0,1) and not r.stderr,(args,r.stderr)
    p=ROOT/f'search_A1_series_laws_{n}.txt';new(p,r.stdout)
    searches.append(dict(command=args,output=str(p),sha256=sha(p),lines=len(r.stdout.splitlines())))
record=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHA_ANTES_DO_CODIGO',
 consumer='A1(b): avaliacao concreta da media dual para compor nu=m_A(omega); RegularCoreTraceData continua consumidor final via perturbacao, nao preenchido por estas leis.',
 exact_target='Para psi:M->L[C]C representado por HasSum vetorial, m_A(psi) conserva zero/soma/escala/ordem no input A; normalidade para supremos positivos dirigidos arbitrarios; identidade com integral da mesma acao dual apos soma; bimodulo e valores limitados. Nenhum teorema presume que todo funcional normal admite tal serie.',
 decision='ADAPTAR ligacao a leis existentes. NOVO somente troca supremo de rede/serie ENNReal, nao fornecida pela troca sequencial anterior. Nao refazer formas, peso, Moreau ou GNS.',
 providers=providers,searches=searches,
 inherited_six_modalities={n:sha(ROOT/n) for n in ['REAPROVEITAMENTO_A1.json','BUSCAS_A1.json','OUTRAS_BANCADAS_HASHES.json','ADENDO_REAPROVEITAMENTO_A1.json']},
 consultation=dict(path=str(ROOT/'revisao/CONSULTA_A1_PREDUAL_CONCRETO_QUOCIENTE.md'),sha256=sha(ROOT/'revisao/CONSULTA_A1_PREDUAL_CONCRETO_QUOCIENTE.md')),
 limits=['normal_positivo_implica_serie_vetorial_nao_provado','sem_predual_completo_por_renomeacao','sem_traco_ou_movimento_de_gate'])
new(ROOT/'REAPROVEITAMENTO_A1_LEIS_FUNCIONAIS.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
rows='\n'.join(f"| {x['declaration']} | {x['file']}:{x['line']} | {x['decision']} | `{x['sha256']}` |" for x in providers)
new(ROOT/'REAPROVEITAMENTO_A1_LEIS_FUNCIONAIS.md',f"# A1 — leis consumidoras da avaliação funcional\n\n{record['timestamp']}\n\n[OPEN — ficha anterior ao código] {record['consumer']}\n\n{record['exact_target']}\n\n{record['decision']}\n\n| Declaração | Fonte | Decisão | SHA256 lido |\n|---|---|---|---|\n{rows}\n\nBuscas exatas, saídas e seis modalidades herdadas no JSON acompanhante. A consulta independente recomenda a descida somente após média: o levantamento vetorial ao core antes dela pode depender da representação. O domínio desta entrega mantém HasSum explícito; não afirma cobertura de todo predual.\n")
print(json.dumps(dict(providers=len(providers),searches=len(searches),sha256=sha(ROOT/'REAPROVEITAMENTO_A1_LEIS_FUNCIONAIS.json')),indent=2))
