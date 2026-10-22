"""Custody only: read selected existing text sources; never import scientific code."""
from pathlib import Path
import hashlib, json, datetime

BASE = Path(__file__).resolve().parent
CENTRAL = Path(r'C:\IALD\Central de Patentes')
KERNEL = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
TUNNEL = CENTRAL / 'Chatgpt/TUNEL/DO_CHATGPT'
LENS = CENTRAL / 'work/lentes_discriminante_20261019'

def pin(path):
    data = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

def new(name, obj):
    with (BASE/name).open('x', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')

specs = [
 ('S01', TUNNEL/'ORDEM_019/F3.1/EXAME_MAPA_TGL_H0_R2_20261008.md', [(5,27)]),
 ('S02', KERNEL/'TheFlowLawContrast.lean', [(40,54),(141,170)]),
 ('S03', KERNEL/'SectorFriedmann.lean', [(8,11),(22,55),(70,88)]),
 ('S04', Path(r'C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py'), [(3266,3344),(3358,3404),(3622,3656),(3746,3758)]),
 ('S05', Path(r'C:\IALD\Bancada_Um\bancada\motor.py'), [(29,41),(250,285)]),
 ('S06', Path(r'C:\IALD\Bancada_Um\bancada\fundo_gpu.py'), [(141,149)]),
 ('S07', TUNNEL/'ORDEM_018/derivacoes/poder_forma/NOTA_PODER_FORMA.md', [(19,32)]),
 ('S08', TUNNEL/'ORDEM_018/f9_maser_anchor_alternative/sources/page_4.txt', [(90,130)]),
 ('S09', TUNNEL/'ORDEM_018/f9_maser_anchor_alternative/sources/page_5.txt', [(49,104)]),
 ('S10', LENS/'trajectory_r2/DISTANCE_REPARAMETRIZATION_R2.md', [(1,100)]),
]
if __name__ == '__main__':
    for name in ('SOURCE_MAPS_R3.json', 'DELIVERY_MAPS_R3.json'):
        if (BASE/name).exists():
            raise FileExistsError(name)
    sources=[]
    for sid,path,ranges in specs:
        lines=path.read_text(encoding='utf-8-sig').splitlines()
        fragments=[]
        for first,last in ranges:
            last=min(last,len(lines))
            if first>last:
                raise ValueError((path, first, last))
            fragments.append({'first_line':first,'last_line':last,'text':'\n'.join(lines[first-1:last])})
        sources.append({'id':sid,**pin(path),'statute':'REAL_DOCUMENTARY_READ_NOT_NEW_EXECUTION', 'fragments':fragments})
    seal=LENS/'v394_r12/SEAL_SNAPSHOT.json'
    data=json.loads(seal.read_text(encoding='utf-8-sig'))
    sources.append({'id':'S11',**pin(seal),'fields':{k:data.get(k) for k in ('um_version','timestamp','result_hash')},
                    'statute':'SNAPSHOT_METADATA_NOT_CURRENT_DEPLOYMENT'})
    new('SOURCE_MAPS_R3.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':sources,
                            'scientific_sources_imported_or_executed':False,'new_observed_composite':False})
    new('DELIVERY_MAPS_R3.json',{'scope':'R1_PHYSICAL_MAPS_CONDITIONAL_DERIVATION','task':'R1',
      'mission_reference':str(BASE.parent/'SESSION_REFERENCE.json'),'mission_revision_checked':8,
      'result':'MAP_CONSUMER_EXPLICIT_PHYSICAL_ADMISSION_OPEN',
      'existing_reused':['D1b_scalar_factor','sector_Friedmann','effective_background_distances','accumulated_luminosity_map'],
      'derived_here':['single_object_distance_to_H0_conversion','conditional_accumulated_angular_conversion','positive_weight_ratio_bound','low_z_expansion_with_unbounded_remainder_explicit'],
      'remaining':['instrument_distance_clock_identification','disk_likelihood_and_priors_transport_or_invariance_proof','joint_flow_likelihood_preserving_selection_and_peculiar_velocities'],
      'evidence':[pin(BASE/n) for n in ('DERIVACAO_MAPAS_R3.txt','SOURCE_MAPS_R3.json','custody_r3.py')],
      'no_new_scientific_execution':True,'no_observed_significance':True,'production_changed':False,'gate_changed':False})
    print(json.dumps(pin(BASE/'DELIVERY_MAPS_R3.json'),ensure_ascii=False))
