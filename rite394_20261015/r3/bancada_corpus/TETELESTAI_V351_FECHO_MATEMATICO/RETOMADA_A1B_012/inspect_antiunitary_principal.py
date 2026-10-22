from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists(),p
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
names=['V351AntiunitaryResolventPhase','V351ScalarTomitaImaginaryConjugation'];suppliers=['V351ResolventPhaseFunctions','V351ResolventImaginaryPowers','V351ScalarTomitaImaginaryPowers','V350ScalarTomitaPolarResolvent','V350AntiunitaryPositiveConjugation']
rows=[]
for n in names:
 p=K/'TGLExt'/f'{n}.lean';s=p.read_text(encoding='utf8');decs=[]
 for m in re.finditer(r'^(theorem|def) (\w+)[\s\S]*?(?= :=| where)',s,re.M):decs.append(dict(name='TGLV350.Regular.'+m[2],kind=m[1],line=s[:m.start()].count('\n')+1,statement=m[0]))
 rows.append(dict(module=n,source=pin(p),declarations=decs))
checks=[
 'The conjugation used throughout is J T J.symm, with J the specified semilinear isometric equivalence. J²=I is not assumed or needed in the generic proof.',
 'The real star-algebra homomorphism conjugates complex scalars. Real CFC transport and real/imaginary decomposition establish the complex CFC formula; no complex-linear automorphism is falsely attributed to J.',
 'The damped phase satisfies star(g_t(1-x))=g_t(x). Reflection of log((1-x)/x) and scalar conjugation cancel. Endpoint values are zero through damping; no undefined endpoint division is used to infer a nonzero limit.',
 'Norm-continuity of bounded antiunitary conjugation justifies CFC transport. Self-adjointness follows by adjoint identities. The CFC composition is supplied with its continuity and star-normality conditions.',
 'T and 1-T are injective positive contractions in the generic imaginary-power theorem. The already proved dense range of T(1-T) permits extension from damped vectors by continuity. No bounded inverse or spectral gap is introduced.',
 'The concrete specialization uses the original scalarTomitaResolvent and scalarTomitaPolarFactor. The actual polar-resolvent flip is a supplier, not an assumed new covariance. The resulting group is scalarTomitaImaginaryPower in the same ScalarGNSHilbert P.',
 'Final pointwise and bounded-operator equalities are JU_tJ^{-1}=U_t. Neither claims JU_tJ^{-1}=U_{-t}, nor a KMS theorem, affiliated regular generator, trace, or complete RegularCoreTraceData inhabitant.',
 'The existing module V350LocalBasePolarCommutation contains same-name add/smul statements. The actual combined import was accepted in a separate DEV check. This inspection does not label the repeated names a demonstrated compilation bug; the standalone delta build remains required.'
]
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='PRINCIPAL_SEMANTIC_INSPECTION_COMPLETE__STANDALONE_REPLAY_PENDING',reviewer='principal',authorship='The sidecar reports prior authorship of these two modules. This semantic review is by the principal; the sidecar replay is computational evidence and is not relabeled independent personal review.',P0=[],P1=[],P2=[],modules=rows,providers=[pin(K/'TGLExt'/f'{n}.lean') for n in suppliers],checks=checks,compilation_required='Author cold Lake replay and sidecar private cold Lake replay with all16 declaration types/axioms; no final acceptance before both return zero.',negative_control='BadAntiunitaryPhase changes the phase identity to twice its RHS. It is a tamper-rejection probe, not a mathematical theorem of impossibility.',full_trace_open=True)
put(R/'INSPECAO_PRINCIPAL_ANTIUNITARIOS.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[REAL — inspeção semântica dos dois fornecedores; reprodução isolada ainda pendente]\n\n# Revisão do principal: camada antiunitária\n\n'+d['timestamp']+'\n\nA revisão do principal é distinta da autoria anterior declarada pelo sidecar. O replay do sidecar continuará identificado como reprodução computacional. Nenhum P0, P1 ou P2 encontrado na leitura dos tipos e provas. Esta nota não antecipa rc0.\n\n'
for c in checks:s+='- '+c+'\n\n'
s+='## Fontes e declarações relidas\n\n'
for row in rows:
 s+=f"`{row['source']['path']}` — `{row['source']['sha256']}`\n\n"
 for q in row['declarations']:s+=f"`{q['name']}` :{q['line']}\n\n```lean\n{q['statement']}\n```\n\n"
put(R/'INSPECAO_PRINCIPAL_ANTIUNITARIOS.md',s.encode('utf8'))
print(json.dumps(dict(modules=2,declarations=sum(len(x['declarations']) for x in rows),P0=[],P1=[],P2=[],compilation_pending=True)))
