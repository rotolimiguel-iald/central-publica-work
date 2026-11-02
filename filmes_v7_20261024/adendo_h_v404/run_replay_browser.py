from context import *
module=Path(r'C:\Users\rotol\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules\playwright')
assert module.is_dir()
check();stable_seal()
assert not (H/'REPLAY_BROWSER_RUN_R4.json').exists(),'Recover existing browser result'
assert read(H/'REPLAY_BROWSER_FAILURE_R3.json')['returncode']!=0
env=os.environ.copy();env['PLAYWRIGHT_MODULE']=str(module)
env['CHROMIUM_EXECUTABLE']=r'C:\Users\rotol\AppData\Local\ms-playwright\chromium_headless_shell-1228\chrome-headless-shell-win64\chrome-headless-shell.exe'
assert Path(env['CHROMIUM_EXECUTABLE']).is_file()
r=subprocess.run([r'C:\Program Files\nodejs\node.exe',str(S/'replay/test_browser.cjs')],cwd=S,env=env,capture_output=True,text=True,encoding='utf-8')
create(H/'REPLAY_BROWSER_RUN_R4.json',{'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'script':pin(S/'replay/test_browser.cjs'),'browser_executable':env['CHROMIUM_EXECUTABLE'],'network_scope':'Harness refuses all requests except its own ephemeral loopback origin.'})
print(r.stdout);print(r.stderr);assert r.returncode==0
report=read(S/'replay/TEST_BROWSER.json');assert report['status']=='PASS' and not report['external_requests']
stable_seal()
