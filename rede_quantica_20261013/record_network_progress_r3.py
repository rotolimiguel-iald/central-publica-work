"""Custody of actual exponential/Weyl construction; additive progress, not completion."""
import datetime as dt,json,re
from pathlib import Path
from diary_r1 import ROOT,WORK,CLI,WHO,new,pin,append_bytes
import register_rule_tetelestai as reg
OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
reg.DEST=OUT
MARKER='fecho_exponential_weyl_progress_20261015_r3'

def main():
    if (OUT/'PROGRESS_R3.json').exists(): raise FileExistsError('Recover registration; do not repeat memory')
    claim=reg.call([CLI,'ver','F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem']==WHO and dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    for x in ('DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md','AVISO_GERENCIA.md'): assert x in claim['nota']
    wiring=OUT/'weyl_net_wiring'
    builds=[]
    for name in ('WeylCoefficientsR4','WeylOperatorsGenericR2','WeylCovarianceR1','ConcreteWeylR1','ConcreteWeylContinuityR2','FieldWeylR3'):
        source=pin(wiring/(name+'.lean')); choices=[]
        for r in (wiring/'attempts').glob('*/RECEIPT.json'):
            d=json.loads(r.read_bytes())
            if d['source']['sha256']==source['sha256'] and d['exit_code']==0: choices.append((r,d))
        assert choices,name
        r,d=sorted(choices)[-1]
        for a in d['artifacts']: assert pin(a['path'])==a
        raw=(r.parent/'AXIOMS.txt').read_text(encoding='utf-8')
        assert 'sorryAx' not in raw
        assert not re.search(r'(?m)^\s*(?:axiom|sorry)\b',Path(source['path']).read_text(encoding='utf-8'))
        builds.append({'source':source,'receipt':pin(r),'exit':0,'seconds':d['seconds'],'artifacts':d['artifacts']})
    artifacts=[OUT/'network_exponential/FINAL_EXPONENTIAL_RECEIPT_R1.json',OUT/'exponential_review/REVISAO_EXPONENCIAIS_R1.json',
      OUT/'weyl_extension/REVIEW_ROOT_R1.json',OUT/'weyl_review/REVISAO_WEYL_R1.json',
      OUT/'weyl_review/continuity/RECEIPT_R1.json',OUT/'takesaki_reuse/TAKESAKI_INVENTARIO_R7.json',
      OUT/'physical_clock_reuse/RESULTADO_OH_SECTOR_R2.json',OUT/'physical_clock_reuse/review/REVISAO_OH_R1.json']
    progress={'unit':'F1.FECHO_20261015','claim_event':845,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
      'status':'EM_CURSO_PARTIAL_VERIFIED_CONSTRUCTION_FULL_R1_R10_PRESERVED','requirements':pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'),
      'builds':builds,'artifacts':[pin(a) for a in artifacts],
      'constructed':'Exponential vectors and totality on the SAME Fock; Gram extension; actual displacement D, CCR, adjoint, covariance, R(K); strong continuity. Field convention W(f)=D(i f) compiled, correct sign for the intended Tomita link.',
      'independent_review':'Exponential/totality, Gram extension, four Weyl modules and continuity reviewed independently. FieldWeylR3 independent recompilation still running at this snapshot.',
      'takesaki_correction':'V354 already supplies regularLegacyCore and cyclicTraceCandidate matching V351 on all positives. The remainder is the Fock wedge/core representation and modular/trace identification, not a missing total trace adapter.',
      'physical_clock':'Configured OH sector checked independently 30/30. gamma_phi=beta*omega_OH/4 is INPUT; no experimental rate inferred. Energy-origin shift changes root dissipation and is refused as an invariant replacement.',
      'rite':'Actual main R3 still running. Formal build/audit succeeded in partial output; Windows long-path containment bug refused internal corpus paths; DNS blocked. No full-rite PASS or seal claimed. Guard correction/test is a separate next attempt.',
      'remaining':['Restricted exp(K) density and actual wedge vacuum standardness; Tomita/modular identification',
        'Global localization/device realization; Takesaki on the same Fock and trace/weight identification',
        'Joint physical Maxwell/stress realization; all-directions H3 scope',
        'Actual full rite completion and final joint review'],
      'no_new_provider_or_production_change':True}
    new(OUT/'PROGRESS_R3.json',progress)
    addition=f"""\n\n## 15/10/2026 — Exponenciais, Weyl e continuidade na mesma realização Fock
<!-- {MARKER} -->
Em nome de {WHO}, F1.FECHO_20261015, reivindicação845 conferida.
[REAL — termos em sandbox] Vetores exponenciais e sua totalidade foram construídos
no Fock existente. A extensão de Gram fornece D(f), CCR, adjunto, covariância e
R(K) pelo bicomutante. A continuidade forte foi compilada e recompilada
independentemente. Exponenciais/totalidade e os quatro módulos iniciais de Weyl
foram revistos; W(f)=D(if) compila e sua revisão independente segue em curso.
Essa convenção corrige a orientação para Γ(J); a identificação Tomita do par
não é afirmada só pela convenção. Ciclicidade/separância na cunha estão em construção.
[REAL — reaproveitamento corrigido] V354 já contém regularLegacyCore e
cyclicTraceCandidate, coincidente com o traço V351 em todo positivo. Não falta
um adaptador total desse traço; falta a identificação na representação da cunha
Fock pretendida. O inventário específico é evidência desta correção ao lado.
[REAL — teste sintético configurado] OH:30/30 conferências independentes.
γφ=βωOH/4 é INPUT da configuração, não taxa observada. O controle de mudança do
zero de energia altera a dissipação da raiz; não se remove essa constante por
ela desaparecer apenas do comutador.
[EM_CURSO] Main real R3: parte formal passou; a guarda recusou caminhos internos
no formato Windows longo e bloqueou DNS. Sem PASS integral ou selo novo. A
correção da guarda é preparação separada; esta tentativa permanece preservada.
Os requisitos R1–R10 continuam vigentes. Nenhum provedor, original científico,
Bancada de produção ou gate foi alterado nesta etapa.
Evidência: `{OUT/'PROGRESS_R3.json'}`, SHA256`{pin(OUT/'PROGRESS_R3.json')['sha256']}`.
"""
    new(OUT/'MEMORY_ADDITION_R3.txt',addition)
    surfaces=[ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',ROOT/'memory/TGL_ATLAS.md',ROOT/'memory/TGL_INDICE_VIVO.md',ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    memories=[append_bytes(p,addition,MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R3.json',{'unit':'F1.FECHO_20261015','claim':claim,'surfaces':memories,'evidence':pin(OUT/'PROGRESS_R3.json')})
    new(OUT/'MAP_ENTRY_PROGRESS_R3.json',{'tipo':'ANOTACAO','rota_id':'formal.f1_rede.concrete_bosonic_kinematics','dominio':'FORMAL',
      'titulo':'Exponenciais, Weyl e continuidade construídos no Fock existente','resultado':progress['constructed'],
      'estatuto':'REAL — componentes; EM_CURSO — conjunto','status':'EM_CURSO','veredito':'PARTIAL_VERIFIED_PROGRESS_FULL_SCOPE_PRESERVED',
      'defeito':'Tomita/KMS, realização conjunta e rito integral ainda pendentes. V354 já fornece o adaptador total do traço.',
      'proximo_passo':'Pagar ciclicidade/separância, identificar modularidade, construir core Fock e terminar rito corrigido.',
      'onde':str(OUT),'artefatos':[str(OUT/'PROGRESS_R3.json'),str(OUT/'MEMORY_PROGRESS_R3.json')],'olhou_dados':False})
    new(OUT/'ACOM_PROGRESS_REQUEST_R3.json',{'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),
      'expected_revision':31,'event_id':MARKER,'actor':{'id':WHO,'kind':'agent'},'changes':{
      'records':[{'id':MARKER,'kind':'fact','statute':'REAL','text':progress['constructed']+' '+progress['takesaki_correction']+' '+progress['rite'],
        'sources':[{'kind':'artifact','ref':str(OUT/'PROGRESS_R3.json'),'sha256':pin(OUT/'PROGRESS_R3.json')['sha256']}]}],
      'flow':{'phase':'actual_weyl_exponential_completed_wedge_modularity_in_progress','next_action':'Finish wedge standardness and modular/trace identification on same Fock; preserve full-rite attempt and run corrected guard only after terminal. Keep full R1-R10.'}}})
    print(json.dumps({'progress':pin(OUT/'PROGRESS_R3.json'),'memories':len(memories)},ensure_ascii=False))
if __name__=='__main__':main()
