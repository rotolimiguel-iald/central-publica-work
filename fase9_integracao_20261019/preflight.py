"""Read/check current delegated lease; this does not mutate the mission."""
from setup_mission import call,REF,ACTOR
import sys,uuid
if __name__=='__main__':
 task=sys.argv[1];suffix=uuid.uuid4().hex[:8]
 p=call('SYNC_'+task+'_'+suffix+'.json',{'operation':'project','reference':REF})
 t=next(t for t in p['projection']['active'] if t['id']==task)
 c=call('CHECK_'+task+'_'+suffix+'.json',{'operation':'check','reference':REF,'actor':ACTOR,'task_id':task,'expected_revision':p['receipt']['revision'],'projection_sha256':p['projection_sha256'],'lease_id':t['lease']['id']})
 print(c)
