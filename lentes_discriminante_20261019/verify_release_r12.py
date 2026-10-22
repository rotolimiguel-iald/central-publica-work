"""Pin current release state and existing sandbox evidence without running a release."""
from pathlib import Path
import json,hashlib,datetime,ast
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'v394_r12'
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 chain=Path(r'C:\IALD\Central de Patentes\work\cadeia_de_selo\v394')
 nos=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
 kr=chain/'kernel/KERNEL_RECIBO_v394.json';d=json.loads(kr.read_text(encoding='utf-8'));checks=[]
 for key in ['build_full_log','audit_log']:
  actual=pin(d[key]['path']);assert actual['sha256']==d[key]['sha256'];checks.append({'kind':key,**actual,'pin_matches':True})
 raw=(chain/'kernel/audit.log').read_text(encoding='utf-8');totals=[x for x in raw.splitlines() if 'TOTAL' in x and ('decl=' in x or 'thm=' in x)]
 source=OUT/'v394_source.py.snapshot';tree=ast.parse(source.read_text(encoding='utf-8-sig'))
 contract=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_V394_NETWORK_CONTRACT' for t in n.targets)))
 files=[nos/'um.py',nos/'um_absoluto_selo.json',nos/'HANDOFF_v393_CUSTODIA.md',chain/'APLICADO_AO_CANONICO_20261019_151122.json',chain/'ESTADO_V394.md',kr,chain/'kernel/POS_BUILD_v394.json',chain/'ensaio_a_seco_v394.json']
 rows=[pin(f) for f in files]
 assert rows[0]['sha256']==pin(source)['sha256']
 seal=json.loads((nos/'um_absoluto_selo.json').read_text(encoding='utf-8'))
 log=nos/'rodada_v394_stdout.txt';b=log.read_bytes()
 with (OUT/'RELEASE_LOG_OBSERVED.txt').open('xb') as f:f.write(b)
 report={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artifacts':rows,'current_program_version':'v394','current_program_sha256':rows[0]['sha256'],'current_seal_version':seal['um_version'],'current_seal_timestamp':seal['timestamp'],'current_seal_sha256':rows[1]['sha256'],'v393_post_release_custody':'PARTIAL per its handoff, distinct from existing v393 scientific seal','v394_state':'APPLIED_TO_CANONICAL_PATH__NO_MATCHING_SEAL_OBSERVED','v394_ritual_log_snapshot':pin(OUT/'RELEASE_LOG_OBSERVED.txt'),'sandbox_evidence':{'receipt_rc':d['rc'],'receipt_sorry':d['sorry'],'receipt_axioms':d['axiomas'],'pinned_logs':checks,'audit_total_lines':totals,'new_build_executed_here':False,'independent_full_log_semantics_reaudited_here':False},'network_components':contract['constructed_components'],'network_open':contract['open_joint_contract'],'whole_certificate_inhabited_in_runtime':False,'no_automatic_active_generation_change':True}
 with (OUT/'RELEASE_STATUS_R12.json').open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2)
 print(json.dumps({'program':report['current_program_version'],'seal':report['current_seal_version'],'sandbox_logs_match':len(checks),'audit_totals':totals},ensure_ascii=False))
if __name__=='__main__':main()
