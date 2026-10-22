from pathlib import Path
import os
R=Path(__file__).resolve().parent
def put(p,s):
    assert not p.exists() and p.is_relative_to(R)
    b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)
s=(R/'prepare_domain_cut_fiche.py').read_text(encoding='utf8')
a=s.index("pat='");b=s.index('\nqueries=',a)
s=s[:a]+"pat='scalarInverseLimitWeight.*(strong|sandwich|tracial)|tracial.{0,40}finiteDualStarCore|dualQuadraticIntegral.*strong.*bound'"+s[b:]
s=s.replace('search_domain_cut','search_tracial_extension')
a=s.index('specs=[');b=s.index('\nproviders=[]',a)
s=s[:a]+"""specs=[('TGLExt/V351InverseLimitWeight.lean','scalarInverseCutoffWeight_le_limit'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseLimitWeight_mono'),('TGLExt/V350DualCutNormality.lean','dualAmbient_tendsto_strong'),('TGLExt/V350ScalarRightAverage.lean','scalarWeight_right_average_le'),('TGLExt/V351CutoffAverageCommutation.lean','regularInverseCutoffSqrt_commutes_average'),('TGLExt/V350FiniteDualStarCore.lean','regularSandwich_star'),('TGLExt/V350FiniteDualStarCore.lean','regularSandwich_mem_finiteDualStarCore'),('TGLExt/V350FiniteDualStarCore.lean','regularSandwich_tendsto'),('TGLExt/V351WeightAverageRecovery.lean','scalarWeight_square_eq_iSup_averages')]
"""+s[b:]
a=s.index("target='");b=s.index('\nstamp=',a)
target='ADAPTAR: for the SAME scalarInverseLimitWeight, prove bounded square values survive strong limits, tau(positiveSquare(regularSandwich a delta)) <= tau(positiveSquare a), then traciality on the EXISTING finiteDualStarCore iff traciality on all regularCoreAlgebra. Consumer: RegularCoreTraceData.tracial, V351RegularCoreTraceContract.lean:59 (recheck line). No traciality assumed globally, no new weight/core/GNS, no replacement trace contract. The core equality remains an explicit missing lemma; this extension alone does not inhabit the trace contract. Strong convergence of adjoints is taken from existing sandwich theorem, never presumed for arbitrary strong limits.'
s=s[:a]+'target='+repr(target)+'\n'+s[b:]
s=s.replace('OPEN__FICHE_BEFORE_DOMAIN_CUT','OPEN__FICHE_BEFORE_TRACIAL_EXTENSION').replace('REAPROVEITAMENTO_A1B_CORTE_DOMINIO_LIMITE','REAPROVEITAMENTO_A1B_EXTENSAO_TRACIAL')
a=s.index("s='[OPEN —");b=s.index('for q in providers:',a)
s=s[:a]+"s='[OPEN — ficha anterior à extensão tracial]\\n\\n# A1(b): o núcleo existente basta para a igualdade tracial\\n\\n'+stamp+'\\n\\n'+target+'\\n\\nA prova usa Fatou em cada corte e a comutação já paga com as médias. Não compara sanduíches por ordem do conjugador. As buscas nominais abaixo são complementadas pela leitura dos enunciados e fontes destes fornecedores. Nenhuma ausência universal é alegada.\\n\\n'\n"+s[b:]
put(R/'prepare_tracial_extension_fiche.py',s)
s=(R/'dev_compile_inverse_limit_semifinite.py').read_text(encoding='utf8')
for a,b in [('inverse_limit_semifinite','tracial_extension'),('V351InverseLimitSemifiniteness','V351InverseLimitTracialExtension'),('REAPROVEITAMENTO_A1B_SEMIFINITUDE_LIMITE','REAPROVEITAMENTO_A1B_EXTENSAO_TRACIAL')]:s=s.replace(a,b)
put(R/'dev_compile_tracial_extension.py',s)
