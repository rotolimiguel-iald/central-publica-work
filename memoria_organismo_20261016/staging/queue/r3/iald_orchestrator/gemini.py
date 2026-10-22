"""Official Gemini CLI with personal OAuth, bounded attempts and no model tools."""
from pathlib import Path
import hashlib,json,os,subprocess,re
from .profiles import BASE,PROFILES,client_environment

SETTINGS=Path(__file__).with_name('gemini_text_settings.json')
POLICY=Path(__file__).with_name('gemini_text_policy.toml')
RECEIPT=BASE/'validation/gemini_connection.json'

def selected_auth():
    settings=PROFILES/'gemini/.gemini/settings.json'
    if not settings.is_file():return None
    return json.loads(settings.read_bytes()).get('security',{}).get('auth',{}).get('selectedType')

def signature():
    files=[Path(__file__),SETTINGS,POLICY,BASE/'clients/node_modules/@google/gemini-cli/package.json']
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}

def connection_status():
    if not (PROFILES/'gemini/.gemini/oauth_creds.json').is_file():return 'installed_needs_login'
    if selected_auth()!='oauth-personal':return 'api_billing_not_enabled'
    if not RECEIPT.is_file():return 'installed_pending_auth_validation'
    record=json.loads(RECEIPT.read_bytes())
    if record.get('status')=='ready' and record.get('signature')==signature():return 'ready'
    return 'installed_pending_auth_validation'

def prepare_launch(command,workspace):
    if selected_auth()!='oauth-personal':raise RuntimeError('Gemini exige o login pessoal Google neste perfil.')
    if not (PROFILES/'gemini/.gemini/oauth_creds.json').is_file():raise RuntimeError('Login Gemini ausente.')
    workspace=Path(workspace);workspace.mkdir(parents=True,exist_ok=True)
    (workspace/'.git').mkdir(exist_ok=True)
    env=client_environment('gemini')
    for key in list(env):
        if key.startswith(('GEMINI_SYSTEM','GEMINI_CLI_SYSTEM_','GEMINI_CLI_IDE_','GOOGLE_GENAI_')) or key in ('GOOGLE_APPLICATION_CREDENTIALS','GOOGLE_CLOUD_PROJECT','GOOGLE_CLOUD_LOCATION','GOOGLE_CLOUD_QUOTA_PROJECT'):
            env.pop(key,None)
    env['GEMINI_CLI_SYSTEM_SETTINGS_PATH']=str(SETTINGS)
    args=command+['--output-format','json','--admin-policy',str(POLICY),'--extensions','none','--approval-mode','default','--prompt','Responda à tarefa recebida pela entrada padrão.']
    return args,env

def parse_output(output):
    try:data=json.loads(output)
    except (ValueError,TypeError):raise RuntimeError('Gemini não devolveu JSON final válido.') from None
    if data.get('error') or not isinstance(data.get('response'),str) or not data['response'].strip():
        raise RuntimeError('Gemini não concluiu a resposta.')
    stats=data.get('stats')
    if not isinstance(stats,dict) or stats.get('tools',{}).get('totalCalls')!=0:
        raise RuntimeError('Gemini não comprovou ausência de chamadas de ferramentas no conector textual.')
    return {'text':data['response'],'usage':{'models':stats.get('models',{}),'tools':stats.get('tools',{}),'scope':'OFFICIAL_CLI_REPORTED'},'verification':'PROVIDER_COMPLETED_NOT_FACT_CHECKED'}

def execute(command,prompt,workspace,*,process_callback=None):
    # Preserve the client trust check and use only the folder the operator trusted during login.
    workspace=BASE/"state/login/gemini"
    args,env=prepare_launch(command,workspace)
    proc=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',errors='replace',cwd=workspace,env=env,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    if process_callback:process_callback(proc)
    try:
        output,diagnostic=proc.communicate(prompt,timeout=150)
    except subprocess.TimeoutExpired:
        proc.kill();proc.communicate();raise RuntimeError('Gemini excedeu o tempo de execução; nenhuma repetição iniciada pelo orquestrador.') from None
    finally:
        if process_callback:process_callback(None)
    if proc.returncode:
        safe_diagnostic=re.sub(r'https?://\S+|[\w.+-]+@[\w.-]+|[A-Za-z0-9_=-]{35,}', '[REDACTED]', diagnostic)[-2500:]
        report={'exit_code':proc.returncode,'diagnostic':safe_diagnostic}
        p=BASE/'validation'/('gemini_failure_'+str(os.getpid())+'.json')
        p.write_bytes(json.dumps(report,ensure_ascii=False,indent=2).encode())
        combined=(output+'\n'+diagnostic).lower()
        if any(x in combined for x in ('quota','resource_exhausted','rate limit','429')):
            from .providers import ProviderLimitError
            raise ProviderLimitError('Gemini informou limite de consumo; conferir no cliente oficial.')
        raise RuntimeError(f'Cliente Gemini encerrou com código {proc.returncode}; verificar acesso no cliente oficial.')
    return parse_output(output)
