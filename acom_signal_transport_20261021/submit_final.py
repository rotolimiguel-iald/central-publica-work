"""Record applied operational updates and submit deployment for distinct review."""
import hashlib,json
from pathlib import Path
import task
names=['delivery.json','live_validation.json','availability.json','FINAL_RUNTIME_PINS.json','MEMORY_APPLIED_FINAL.json','admin_deadlines37stage/DELIVERY_APPLIED_R2.json']
evidence=[{'path':str(task.W/n),'sha256':hashlib.sha256((task.W/n).read_bytes()).hexdigest()} for n in names]
task.check('deployment')
p=task.project();t=next(t for t in p['projection']['active'] if t['id']=='deployment')
result=task.act('submit',task_id='deployment',lease_id=t['lease']['id'],evidence=evidence,event_id='transport-final-deployment-submit')
task.new('DEPLOYMENT_SUBMITTED_FINAL.json',result)
print('SUBMITTED')
