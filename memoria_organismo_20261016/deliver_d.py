"""Measured deployment matrix, including unavailable surfaces and scope variance."""
import json
from datetime import datetime,timezone
from mission_io import WORK,pin,save,check
from advance import action

check('D')
def read(n):return json.loads((WORK/n).read_bytes())
arch=read('mobile_build/ARCHIVE_REVIEW_R1.json')
jev=read('live_validation/jev_long/RESULT_R1.json')
mcp=read('live_validation/MCP_INSTALLED_R1.json')
inst=read('live_validation/INSTALLED_R1.json')
restart=read('deployment_r2/runs/activation_r1/RESTART.json')
assert arch['status']=='PASS_ARCHIVES_WITH_SCOPE' and jev['status']==mcp['status']==inst['status']=='PASS'
files=['deployment_r2/ACTIVATION_R1.json','deployment_r2/INSTALL_PLAN_R1.json',
    'deployment_r2/REVIEW_R1.json','review_deployment_r2/INSTALLED_PRECHECK_R1.json',
    'live_validation/INSTALLED_R1.json','live_validation/jev_long/RESULT_R1.json',
    'live_validation/jev_long/REQUEST_R1.json','live_validation/jev_long/RETURN_R1.json',
    'live_validation/MCP_INSTALLED_R1.json','live_validation/BENCH_GET_R1.json',
    'live_validation/BENCH_CONNECTIVITY_R1.json','live_validation/MOBILE_SOURCE_PUBLISH_R1.json',
    'mobile_build/ROOT_REVIEW_R1.json','mobile_build/ARCHIVE_REVIEW_R1.json',
    'tests_app/BROWSER_ACCESS_R1.json','validation_final/V_ROOT_REVIEW_R1.json',
    'tests_core_r2/GROWTH_RESULTS_FINAL_R1.json']
matrix=[
 {'surface':'web/backend app','state':'INSTALLED_RUNNING','evidence':restart,
  'limit':'HTTP/login and new PID verified. Authenticated chat/review UI await operator login; no live logged-in chat claim.'},
 {'surface':'native/holographic memory','state':'INSTALLED_TESTED_IN_ISOLATION',
  'limit':'Installed source/imports and20integration tests. Same algorithm, partitioned checkpoints. Resident llama unchanged; no native-model inference in this delivery.'},
 {'surface':'JEV','state':'REAL_LONG_HEADER_TRANSPORT_PASS','http_status':jev['http_status'],
  'seconds':jev['seconds'],'usage':jev['usage'],'bytes':jev['admission']['request_bytes'],
  'limit':'One public/synthetic call,12764input tokens. Long header accepted; not a262k-token stress test or authenticated chat.'},
 {'surface':'scientific queue/CLI','state':'INSTALLED_NEW_PROCESS_IMPORTS',
  'limit':'Generation, provider constraints and uncertain IDs preserved. No legacy migration, scientific job or provider dispatch through production queue.'},
 {'surface':'MCP','state':'NEW_INSTALLED_PROCESS_PASS','tools':mcp['tool_count'],'new_tools':mcp['new_tools'],
  'limit':'Existing clients/processes were not reloaded; use absolute CLI or a newly loaded MCP client.'},
 {'surface':'Bancada caller','state':'WRAPPER_INSTALLED_SERVICE_UNAVAILABLE','tcp_connect_ex':10061,
  'limit':'One GET failed/uncertain, not repeated. Later TCP probe confirmed port18777closed. Production Bancada files/processes unchanged; numerical live test unavailable.'},
 {'surface':'Android','state':'SIGNED_4_1_28_BUILT_ARCHIVE_VERIFIED',
  'apk':arch['apk']['artifact'],'aab':arch['aab']['artifact'],
  'limit':'Local APK/AAB; same public signing certificate as27. No Play/download publication or device installation.'},
 {'surface':'iOS internal/external','state':'RESOURCES_UPDATED_PRIVATE_SOURCE_PUSHED',
  'limit':'App Store Connect login required. New Xcode Cloud build and both tester groups not verified; no claim of availability on device.'}
]
report={'status':'DELIVERED_WITH_VERIFIED_LIMITS','author':'codex-gerente-tgl','requirement':'D',
 'unit':'F9.MEMORIA_ORGANISMO_20261016','time_utc':datetime.now(timezone.utc).isoformat(),
 'reference':pin(WORK/'SESSION_REFERENCE.json'),'installed_files':31,'byte_backups':20,
 'integration_tests':170,'mcp_integration_checks':7,'availability':matrix,
 'evidence':[pin(WORK/f) for f in files],
 'scientific_memory_scope':'Existing installed app sciencev392 preserved (public JEV source confirms it); scientific queue generation remains independent. This delivery updates activity memory, not scientific release packages.',
 'scope_variance':{'declared_unit_text':'NOVA_UNIDADE.json includes the broad phrase "ou publicar".',
  'performed':'Two accepted JavaScript resources committed/pushed to the existing private mobile repo under the permanent coordinated-app-update instruction; no store publication.',
  'receipt':pin(WORK/'live_validation/MOBILE_SOURCE_PUBLISH_R1.json'),
  'disposition':'Recorded explicitly; no deletion/rewrite of prior scope or remote history; APK/AAB retained locally. Source push alone proves neither CI execution nor iOS distribution.'},
 'open_checks':['Authenticated app interaction after operator login','App Store Connect build and IALD Equipe/Piloto availability',
  'Bancada live wrapper after service becomes available; preserve failed request ID','Existing MCP clients load new tools when explicitly reloaded'],
 'physical_device_mission':'F1.FECHO is separate. The device/model/clock linkage of that scientific mission is not supplied by activity-memory deployment.'}
path=WORK/'DELIVERY_D_R1.json';save(path,report)
r,p=action('submit','D',{'evidence':[pin(path)]})
save(WORK/'D_SUBMITTED_R1.json',{'evidence':pin(path),'receipt':pin(p),'revision':r['receipt']['revision']})
print(json.dumps({'report':pin(path),'revision':r['receipt']['revision']}))
