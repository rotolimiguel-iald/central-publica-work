from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_finite_minorants_fiche.py').read_text(encoding='utf8')
s=s.replace("pat='scalarInverseLimitWeight_finite_contractions|scalarInverseLimitWeight_finite_minorants|finite.{0,12}minorants.{0,12}tracial'","pat='scalarPolarRight.{0,40}average|regularAverage.{0,40}(partition|sum|polar)|average_mem_polar_right'")
s=s.replace('search_finite_minorants','search_average_polar_right')
a=s.index('specs=[');b=s.index('\nproviders=[]',a)
s=s[:a]+"""specs=[('TGLExt/V351ScalarRightActionAlgebra.lean','scalarPolarRightAlgebra_regular_mem'),('TGLExt/V351ScalarRightActionLimits.lean','scalarRightAction_closed_of_bounded_strongStar'),('TGLExt/V350RegularApproximation.lean','regularAverage_apply'),('TGLExt/V350RegularApproximation.lean','regularAverage_tendsto_identity'),('TGLExt/V350ContractionAdjointLimit.lean','regularAverage_star_tendsto_identity'),('TGLExt/V350StrongOperatorIntegral.lean','operatorIntegral_commutes'),('TGLExt/V350RegularTowerRepresentation.lean','regular_mul'),('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean','sum_integral_adjacent_intervals'),('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean','integral_comp_add_right')]
"""+s[b:]
a=s.index("cp=K/");b=s.index('\nd=dict(',a)
s=s[:a]+"""cp=K/'TGLExt/V350ScalarRightAdjointPair.lean';ls=cp.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(ls) if s.startswith('structure ScalarRightAdjointPair'))
target='ADAPTAR: prove the EXISTING regularAverage delta (delta>0) belongs to the EXISTING scalarPolarRightAlgebra, supplying the right action for z=e*e needed by ScalarRightAdjointPair with the same weight/GNS/S/F. Construct bounded finite sums of the existing regular unitaries b_n=(n+1)^(-1) sum_{k<n+1} lambda_(delta*k/(n+1)). Exact interval partition gives e_delta=b_n e_(delta/(n+1)), so contraction bounds and existing small-average convergence give strong convergence; commuting factors and the existing adjoint convergence give strong-star. Apply already proved bounded strong-star closure twice. This avoids a new generic Riemann-integral framework, operator-norm continuity, Bochner integration in B(H), alternate average, GNS or trace. The fixed S/F vector, modular implementator identity, Q and traciality remain later obligations. No claim average is selfadjoint; use e*e for later fixed vector.'
"""+s[b:]
s=s.replace('OPEN__FICHE_BEFORE_FINITE_MINORANTS','OPEN__FICHE_BEFORE_AVERAGE_POLAR_RIGHT').replace('REAPROVEITAMENTO_A1B_MINORANTES_FINITOS','REAPROVEITAMENTO_A1B_MEDIA_ACAO_DIREITA')
a=s.index("s='[OPEN —");b=s.index('for q in providers:',a)
s=s[:a]+"s='[OPEN — ficha anterior à pertença da média à álgebra direita]\\n\\n'+d['timestamp']+'\\n\\n'+target+'\\n\\n'\n"+s[b:]
a=s.index("s+='Buscas:");b=s.index("\nput(R/",a)
s=s[:a]+"s+='Buscas: '+str(A/'searches.json')+'. Ausência nominal não é ausência universal. Consulta2 corrigida V2 já lida; rota reduzida à partição exata da integral e limites existentes.\\n'"+s[b:]
def put(p,s):
    assert not p.exists();b=s.encode();t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
put(R/'prepare_average_polar_right_fiche.py',s)
s=(R/'dev_compile_finite_minorants.py').read_text(encoding='utf8')
s=s.replace('finite_minorants','average_polar_right').replace('V351InverseLimitFiniteMinorants','V351AveragePolarRight').replace('REAPROVEITAMENTO_A1B_MINORANTES_FINITOS','REAPROVEITAMENTO_A1B_MEDIA_ACAO_DIREITA')
put(R/'dev_compile_average_polar_right.py',s)

