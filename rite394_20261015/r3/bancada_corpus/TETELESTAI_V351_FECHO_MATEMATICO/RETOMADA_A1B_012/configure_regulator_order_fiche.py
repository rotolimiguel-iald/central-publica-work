from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_perturbed_norm_fiche.py').read_text(encoding='utf8')
s=s.replace("pat='scalarRightAction_weight_norm|scalarPerturbedWeight|inverseCutoffPerturbedWeight|scalarWeight.*sandwich.*norm'", "pat='regularInverseGeneratorCutoff_(antitone|resolvent_identity)|inverseCutoff.{0,25}(weight.*mono|mono.*weight)|regulador.{0,25}(antit|monot)'")
s=s.replace('search_perturbed_weight_norm','search_regulator_order')
a=s.index('specs=[');b=s.index('\nproviders=[]',a)
s=s[:a]+"""specs=[('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_graph'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_graph_iff'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_nonneg'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_cfc'),('TGLExt/V351AllPositiveWeightOrder.lean','scalarWeight_right_perturbed_mono_all_positive'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_sqrt_right'),('TGLExt/V351CutoffAverageCommutation.lean','regularInverseCutoffSqrt_commutes_average'),('TGLExt/V350AntiunitaryPositiveConjugation.lean','hilbertPositiveSqrt')]
"""+s[b:]
a=s.index("target='");b=s.index('\nstamp=',a)
target='For epsilon,eta>0 derive the resolvent identity B_epsilon-B_eta=(eta-epsilon) smul (B_eta*B_epsilon) directly from the SAME graph and inverse equation. CFC of the same R proves the cuts commute, so their positive product is nonnegative. If epsilon<=eta, obtain B_eta<=B_epsilon. Then discharge membership, square-root norm products and original-average commutation to instantiate the already constructed all-positive weight comparison for sqrt(B_eta) and sqrt(B_epsilon), for EVERY X in PositiveCoreInput P. No finite-weight premise, new resolvent, spectral coordinates, trace definition or physics coupling. The regulator epsilon is mathematical, not beta_TGL. Consumer: define monotone cutoff weights and their supremum on the same cone. Trace and semifinitude of its limit remain obligations.'
s=s[:a]+'target='+repr(target)+'\n'+s[b:]
s=s.replace('OPEN__FICHE_BEFORE_PERTURBED_WEIGHT_NORM','OPEN__FICHE_BEFORE_REGULATOR_ORDER').replace('REAPROVEITAMENTO_A1B_PESO_PERTURBADO_NORMA','REAPROVEITAMENTO_A1B_ORDEM_REGULADORES')
a=s.index("s='[OPEN —");b=s.index('for q in providers:',a)
s=s[:a]+"""s='[OPEN — ficha anterior à ordem dos reguladores]\\n\\n# A1(b): os cortes originais crescem quando o regulador diminui\\n\\n'+stamp+'\\n\\n'+target+'\\n\\nADAPTAR: consumir graph_iff e positividade já provadas. Mathlib cfc_commute_cfc e Commute.mul_nonneg foram lidos nas fontes pinadas; adendo anterior ao alvo. Não redefinir o inverso ou instalar hipótese de ordem como resultado.\\n\\n'
"""+s[b:]
p=R/'prepare_regulator_order_fiche.py';assert not p.exists();b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
