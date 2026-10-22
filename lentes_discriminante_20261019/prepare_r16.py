"""Pin bounded source retrieval and a sigma tracker without recomposing observations."""
from setup import ROOT,save
from record_trajectory_r2 import pin
import json,datetime,re
d=ROOT/'calibration_r16'
save('calibration_r16/OPERADOR.txt','Prossiga, procure no que já escrevi como determinar a amplitude do campo e ligar f0 ao G medido, sem ajustar aos atrasos, para avançarmos na comparação entre dinâmica estelar e lentes.\n\nNão obtivemos um sinal de 5 sigma, mas estamos alcançando quanto, precisamos acompanhar isso?\n\ntalvez eu deva trabalahr com Os 4,28σ históricos da Fase 9, esse já é suficiente como prova de betatgl, bvc não acha?')
sources={}
for n in ['SOURCE_AMPLITUDE_R16.json','SOURCE_G_R16.json']:
    j=json.loads((d/n).read_text(encoding='utf-8'))
    for a in j['sources']:
        now=pin(a['path']);assert now['sha256']==a['sha256'],a['path'];sources[now['path']]=now
prior=json.loads((ROOT/'full_source_r14/PINS_RELEASE_R14.json').read_text(encoding='utf-8'))
for a in prior['artifacts']:
    now=pin(a['path']);assert now['sha256']==a['sha256'],a['path'];sources[now['path']]=now
save('calibration_r16/PINS_RELEASE_R16.json',{'sources':list(sources.values()),'artifacts':[],'seal_version':prior['seal_version'],'seal_timestamp':prior['seal_timestamp'],'unchanged_canonical':True})
p=ROOT/'v394_r12/v394_source.py.snapshot';lines=p.read_text(encoding='utf-8').splitlines()
intervals=[(209371,209399),(209494,209504)]
anchors=[{'first':a,'last':b,'text':'\n'.join(lines[a-1:b])} for a,b in intervals]
values=[float(re.search(r"'valor': ([0-9.]+)",lines[i-1]).group(1)) for i in [209376,209383]]
z=sum(values)/2
save('calibration_r16/PROGRESSO_SIGMA_R16.json',{'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'lenses':{'law':'R15 restricted static timelike covector/spinless Cartan; R16 calibration','predicted_q':None,'covariance':None,'forecast_Z':None,'observed_Z':None,'status':'NO_NUMERIC_SIGMA__AMPLITUDE_AND_COVARIANCE_OPEN','not_zero':True,'formula':'abs(log(1+q_TGL))/sqrt(vL+vD-2cLD)','required_for_nominal_5':'sigma_logcontrast <= abs(log(1+q_TGL))/5','optical_only':'No distinct radial correction in R15; mass degeneracy remains'},
 'fase9':{'status':'HISTORICAL_V1_READ_FROM_V394__NOT_REEXECUTED','z_disc_bounds_in_source':values,'z_disc_reference':z,'verdict':'INCONCLUSIVE_SYSTEMATICS','new_V2_result':None,'source':pin(p),'anchors':anchors,
 'conditional_planning_only':{'assumption':'same fixed contrast and statistical model, sigma_total can be reduced; independent statistical dominance only for information scaling','target':5,'required_sigma_ratio':z/5,'relative_sigma_reduction':1-z/5,'equivalent_information_factor':(5/z)**2,'not_a_forecast_or_new_measurement':True}},
 'cannot_add_significances':True,'probability_theory_true':None,'gate_changed':False})
print(json.dumps({'source_count':len(sources),'fase9_reference':z,'sigma_reduction':1-z/5,'information_factor':(5/z)**2}))
