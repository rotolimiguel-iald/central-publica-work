from pathlib import Path
import hashlib
import json
import os
import datetime
import re

ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=Path(__file__).resolve().parent
assert OUT.is_relative_to(ROOT)
COPY=ROOT/'COPIA_INTEGRADA_20260909_192248_937671/um.py'
OVERLAY=ROOT/'INTEGRADOR_GIBBS_DINAMICA_20260909_191901_8768394/BUILD_SUCCESSOR_20260909_192313_320129/TGLExt'
CANON=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')

def pin(path):
    p=Path(path); b=p.read_bytes()
    return {'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

names=['MetricEinsteinVariation.lean','ScalarEinsteinLieNaturality.lean',
       'GeneralLinearizedGauge.lean','FiniteEinsteinNaturality.lean',
       'MixedGibbsGravitationalBridge.lean','FiniteCoherentSources.lean',
       'ConeVolumeReconstruction.lean','LeviCivitaMetricVariation.lean']
canonical=['ScalarStressConservation.lean','CoherentScalarStress.lean',
           'PhysicsCertificates.lean','ContinuumTT.lean']
sources=[OVERLAY/n for n in names]+[CANON/n for n in canonical]
source_pins=[pin(p) for p in sources]
source_anchors=[]
for p in sources:
    lines=p.read_text(encoding='utf-8').splitlines()
    source_anchors.append({'path':p.as_posix(),'declarations':[
        {'line':i,'text':line.strip()} for i,line in enumerate(lines,1)
        if re.match(r'^(?:def|theorem) ',line)]})
copy_pin=pin(COPY)
copy_text=COPY.read_text(encoding='utf-8')
terms=['EinsteinJetWard','TheSpectrum','BRST','Batalin','antifield','master equation','quantum master']
counts={t:len(list(re.finditer(re.escape(t),copy_text,re.I))) for t in terms}
primary=[
 {'authors':'Barnich, Brandt, Henneaux','title':'Local BRST cohomology in Einstein--Yang--Mills theory','year':1995,'url':'https://arxiv.org/pdf/hep-th/9505173','scope':'Classificacao local incluindo materia; seccoes 2, 9 e 10.4; nao e compilacao Lean.'},
 {'authors':'Hollands, Wald','title':'Conservation of the stress tensor in perturbative interacting quantum field theory in curved spacetimes','year':2005,'url':'https://arxiv.org/abs/gr-qc/0404074','scope':'Wick/time-order renormalizados e conservacao escalar; nao quantiza a metrica.'},
 {'authors':'Fredenhagen, Rejzner','title':'Batalin-Vilkovisky formalism in perturbative algebraic quantum field theory','year':2013,'url':'https://arxiv.org/abs/1110.5232','scope':'BV e equacao mestra renormalizados; exige verificacao dos contratos do modelo.'},
 {'authors':'Brunetti, Fredenhagen, Rejzner','title':'Quantum gravity from the point of view of locally covariant quantum field theory','year':2016,'url':'https://arxiv.org/html/1306.1058v4','scope':'Gravidade pura; secao6 diz que extensao a materia e esperada. Nao importada como prova pronta Einstein-escalares.'},
 {'authors':'Alvarez-Gaume, Witten','title':'Gravitational anomalies','year':1984,'url':'https://collaborate.princeton.edu/en/publications/gravitational-anomalies/','doi':'10.1016/0550-3213(84)90066-X','scope':'Anomalias gravitacionais quirais e distincao dimensional; nao universalidade sem anomalias.'},
 {'authors':'Donoghue','title':'General relativity as an effective field theory: The leading quantum corrections','year':1994,'url':'https://arxiv.org/abs/gr-qc/9405057','scope':'Expansao de baixa energia; nao completamento UV.'},
 {'authors':'Gomis, Weinberg','title':'Are Nonrenormalizable Gauge Theories Renormalizable?','year':1996,'url':'https://arxiv.org/abs/hep-th/9510087','scope':'Renormalizacao moderna com infinitos operadores sujeitos a cohomologia BRST; nao finitos parametros.'},
]
manifest={'status':'WRITTEN_EINSTEIN_SCALAR_BV_EFT_ROUTE_AND_SOURCE_REVIEW',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'authorship':'Analise propria finish_gibbs_realization; sem aprovacao atribuida a terceiros.',
 'note':pin(OUT/'ACAO_ESCALAR_QUANTIZACAO_E_LIMITES.md'),'script':pin(__file__),
 'copy_read_only':copy_pin,'local_sources':source_pins,'source_declaration_anchors':source_anchors,
 'bounded_text_search':{'path':COPY.as_posix(),'case_insensitive_occurrences':counts,
    'claim':'Resultados apenas da copia identificada e fontes indicadas; nao ausencia em todo acervo.'},
 'primary_references':primary,
 'recommended_leaf':'ScalarMatterDensityVariation.lean',
 'new_lean_compilations':0,'um_executed_or_imported':False,'originals_written':False,
 'action_status':'INPUT_POSTULATE','written_variation_status':'DERIVED',
 'coherent_quantum_stress_difference_status':'DERIVED_CONDITIONAL_ON_GLOBALLY_HYPERBOLIC_BACKGROUND_HADAMARD_REFERENCE_AND_GLOBAL_SCALAR_SOLUTIONS',
 'interacting_gravity_quantization_status':'OPEN_IMPLEMENTATION_WITH_EXPLICIT_PERTURBATIVE_EFT_CONTRACTS',
 'uv_completion_status':'OPEN'}
assert pin(COPY)==copy_pin
assert [pin(p) for p in sources]==source_pins
dest=OUT/'MANIFESTO_EFT_ESCALAR.json'; tmp=OUT/'MANIFESTO_EFT_ESCALAR.json.tmp'
assert not dest.exists() and not tmp.exists()
b=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
with tmp.open('xb') as f:
    f.write(b); f.flush(); os.fsync(f.fileno())
assert tmp.read_bytes()==b
tmp.rename(dest)
assert dest.read_bytes()==b
print(json.dumps({'status':manifest['status'],'note':manifest['note'],
                  'manifest':pin(dest),'search_counts':counts},ensure_ascii=False))
