"""Resume only the reviewed receipt-projection tail after local hard-link refusal."""
from context import *
import ast,runpy

def main():
 check();stable_seal();review=read(H/'INTEGRATION_REVIEW.json');script=H/'integrate_v404.py'
 assert review['status']=='PASS_WITH_SCOPE' and review['installer_sha256']==sha(script)
 plan=read(H/'INTEGRATION_PLAN.json');assert review['plan_sha256']==sha(H/'INTEGRATION_PLAN.json')
 installed=read(H/'INTEGRATION.json');assert installed['status']=='PASS'
 ns=runpy.run_path(str(script))
 for row in installed['files']:
  ns['verify'](row['installed']);assert row['installed']['sha256']==row['candidate']['sha256']
 dep={k:json.loads(ns['checked_bytes'](p)) for k,p in plan['dependencies'].items()}
 for row in plan['derived_destinations']:
  path=V/row['relative'];assert (pin(path) if path.exists() else None)==row['before'],'Unexpected projection state'
 negatives=list((V/'audit').glob('DELIVERY_D_V404.json.new_*'));assert len(negatives)==1
 create(H/'INTEGRATION_PROJECTION_INTERRUPTED.json',{'status':'LOCAL_HARDLINK_REFUSED_AFTER_VERIFIED_FILE_COPY','error':'WinError5','installed_data':pin(H/'INTEGRATION.json'),'uncommitted_receipt_bytes':pin(negatives[0]),'source':'v404','source_sha256':plan['source_sha256'],'scope':'97 copied files verified; three derived public/audit receipts not yet committed. No capture, TTS retry or publication.'})
 # Execute the exact reviewed tail, not another installation or a rewritten fallback.
 tree=ast.parse(script.read_text('utf-8'));fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='apply')
 indexes=[i for i,node in enumerate(fn.body) if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='d' for t in node.targets)]
 assert len(indexes)==1
 tail=ast.FunctionDef(name='finish_projections',args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=n) for n in ['plan','dep','out']],kwonlyargs=[],kw_defaults=[],defaults=[]),body=fn.body[indexes[0]:],decorator_list=[])
 module=ast.fix_missing_locations(ast.Module(body=[tail],type_ignores=[]));exec(compile(module,str(script),'exec'),ns)
 ns['finish_projections'](plan,dep,installed['files'])
 stable_seal();create(H/'INTEGRATION_PROJECTIONS_COMPLETED.json',{'status':'PASS','source':'v404','source_sha256':plan['source_sha256'],'reviewed_installer':pin(script),'projection_files':[pin(V/x['relative']) for x in plan['derived_destinations']],'media_audio_ready':pin(H/'MEDIA_AUDIO_READY.json'),'initial_refusal':pin(H/'INTEGRATION_PROJECTION_INTERRUPTED.json'),'scope':'Exact reviewed receipt tail completed with OS hard-link permission; data/audio files not installed again.'})

if __name__=='__main__':main()
