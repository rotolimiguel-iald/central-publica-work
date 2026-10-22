from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert not p.exists() and p.is_relative_to(R)
    t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
specs=[('TGLExt/V350RegularDualAction.lean',23,24),('TGLExt/V350L2CharacterMultiplier.lean',94,96),('TGLExt/V350StrongOperatorField.lean',68,69),('TGLExt/V350DualWeightCuts.lean',14,24),('TGLExt/V350ReducingStarRepresentation.lean',13,17),('TGLExt/V350ScalarGNSRepresentation.lean',14,19),('TGLExt/V350ScalarGNSCompletion.lean',48,53),('TGLExt/V351RegularPositiveGraph.lean',98,110),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unique.lean',486,490),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/Classes.lean',50,54)]
rows=[]
for name,a,b in specs:
    p=K/name;s=p.read_text(encoding='utf8').splitlines();rows.append(dict(source=pin(p),line=a,excerpt='\n'.join(s[a-1:b]),decision='REUSAR'))
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='OPEN__CONCRETE_ADAPTERS_BEFORE_CODE',providers=rows,prior_fiche=pin(R/'REAPROVEITAMENTO_A1B_BALANCO_DOS_CORTES.json'),spectral_adendum=pin(R/'ADENDO_PRE_CODIGO_BALANCO_ESPECTRAL.json'),private_calculation_dev_only=pin(R/'dev_double_cut_balance/20260915_015018_169063/run.json'))
text='[OPEN] Adaptadores concretos para consumir o balanço limitado\n\n'+d['timestamp']+'\n\nA consulta independente localizou a via pontual: injetividade de a.val passa às conjugações unitárias dualAmbient, ao operatorFieldLift por duas igualdades a.e. para cada par de vetores, e à restrição no GNS original por Subtype.ext. Não usar fidelidade da representação como substituta de injetividade vetorial. O cálculo funcional deve ser transportado pela inclusão da álgebra normativamente fechada e pela mesma pi contínua, usando map_cfc existente. A identidade de fases concreta e as comutações necessárias continuam abertas. Os três adaptadores privados já escritos passaram apenas DEV; não são uma entrega33 nem a tracialidade. Balanço de cortes reais e Q permanecem OPEN.\n\n'
for q in rows:text+=q['source']['path']+':'+str(q['line'])+'\n```lean\n'+q['excerpt']+'\n```\n\n'
put(R/'ADENDO_PRE_ADAPTADORES_CONCRETOS_BALANCO.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'ADENDO_PRE_ADAPTADORES_CONCRETOS_BALANCO.md',text.encode('utf8'))
print(json.dumps(d,ensure_ascii=False))
