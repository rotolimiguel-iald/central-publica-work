from pathlib import Path
import hashlib,json,datetime
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'TETELESTAI_V350_KERNEL_20260911'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
specs=[('kernel/TGLExt/V350ScalarWeightTomitaIdentification.lean','scalarClosedTomita_graph_eq_weight','REUSAR: a igualdade com o fecho do grafo do peso completo já existe; não cobrá-la novamente.'),
 ('kernel/TGLV350/ScalarProjectionGap.lean','scalarPhaseVariational_projection_lower_bound','DEV: cota do bloco de projeção, escrita anteriormente, sem compilação aceita própria; não entrega KMS nem traço.'),
 ('kernel/TGLV350/ScalarWeightedEnergy.lean','scalarPhaseVariational_rightPair_energy','DEV: energia variacional para pares direitos; não fornece τ:PositiveCoreInput→ENNReal.'),
 ('kernel/TGLV350/ProjectionGapEnergy.lean','projectionGapPart_energy_annihilates','DEV: aniquilação de bloco condicionada à energia; não constrói o traço do core.')]
records=[]
for rel,name,decision in specs:
 p=(ROOT if rel.startswith('kernel/TGLExt') else OLD)/rel
 lines=p.read_text(encoding='utf-8').splitlines()
 line=next(i+1 for i,l in enumerate(lines) if l.startswith('theorem '+name))
 records.append(dict(file=str(p),line=line,sha256=sha(p),declaration=name,decision=decision))
flags=['gpf_H1_internal_susy_relative_gap_discharged','gpf_H2_smooth_modular_four_frame_discharged','gpf_H3_local_horizon_equilibrium_discharged','gpi_H3_horizon_data_produced','qgf_continuous_modular_realization_constructed','qgf_full_TGL_witness_constructed','qgf_unconditional_continuous_corner_proved','full_static_witness_exists']
values=[]
def walk(x,path):
 if isinstance(x,dict):
  for k,v in x.items():
   if k in flags:values.append(dict(path=path+[k],value=v))
   walk(v,path+[k])
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,path+[i])
walk(json.loads((ROOT/'base_v351/um_absoluto.json').read_text(encoding='utf-8')),[])
data=dict(time=datetime.datetime.now().isoformat(),providers=records,flags=values,old_workshop_matches_all_equal_embedded=True,source_program_sha256=sha(ROOT/'um.py'),notes=['A ficha inicial permanece intacta como registro anterior ao código.','Busca refinada de acervo confirma registros históricos de pilares externos; truncada em 35, não é prova de ausência.','Árvore v351 §6 contém a expressão semifinita III1; não é usada aqui como tipo: A1 refere-se ao core semifinito, não chama III1 semifinito.'])
p=ROOT/'ADENDO_REAPROVEITAMENTO_A1.json';assert not p.exists();t=p.with_suffix('.json.tmp');t.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
print(json.dumps(dict(new_providers=len(records),flag_occurrences=len(values),values=[v['value'] for v in values]),indent=2))
