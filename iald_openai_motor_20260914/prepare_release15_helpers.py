from pathlib import Path
WORK=Path(__file__).parent
for source,target in [('record_android14.py','record_android15.py'),('deliver_android14.py','deliver_android15.py')]:
    data=(WORK/source).read_bytes().replace(b'4.1-14',b'4.1-15').replace(b"'build': 14",b"'build': 15")
    data=data.replace(b'android14_',b'android15_')
    p=WORK/target
    assert not p.exists()
    p.write_bytes(data)
data=(WORK/'restart_web.ps1').read_text(encoding='utf-8')
data=data.replace('$expectedWebPid = 44296','$expectedWebPid = 37140')
data=data.replace("'2026-09-13T18:41:17'","'2026-09-14T17:29:48'")
needle='$receipt = Get-Content -LiteralPath $receiptFile.FullName -Raw | ConvertFrom-Json'
extra='''
$betaReceipt = Get-Content -LiteralPath (Join-Path $taskRoot 'beta_assets_installation.json') -Raw | ConvertFrom-Json
$serverFile = Join-Path $serverRoot 'iald_web_server.py'
$receipt.files.'iald_web_server.py' = $betaReceipt.PSObject.Properties[$serverFile].Value.sha256
'''
assert needle in data
data=data.replace(needle,needle+extra)
path=WORK/'restart_web_beta.ps1'
assert not path.exists()
path.write_bytes(data.encode('utf-8'))
print('NEW_BUILD_HELPERS_READY')
