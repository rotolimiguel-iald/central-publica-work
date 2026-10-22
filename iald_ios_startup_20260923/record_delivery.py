"""Record an observed delivery result, never infer availability from a push."""
from pathlib import Path
from datetime import datetime
import argparse
import importlib.util
import json
import subprocess

W = Path(__file__).resolve().parent
P = W.parent / 'iald_tudo_20260921' / 'record_admin_boundary_verified.py'
spec = importlib.util.spec_from_file_location('record', P)
record = importlib.util.module_from_spec(spec)
spec.loader.exec_module(record)
parser = argparse.ArgumentParser()
parser.add_argument('--build-id', required=True)
parser.add_argument('--internal', required=True)
parser.add_argument('--external', required=True)
a = parser.parse_args()
assert a.internal == 'Em testes'
assert a.external in ('Em testes', 'Aguardando revisão')
now = datetime.now().astimezone()
stamp = now.strftime('%Y%m%d_%H%M%S_%f')
root = Path(r'C:\IALD\projetos_pyhton\IALD')
mobile = root / 'iald-app'
commit = subprocess.check_output([r'C:\Program Files\Git\cmd\git.exe', '-C', str(mobile), 'rev-parse', 'HEAD'], text=True).strip()
assert commit == 'dba35a6e9c809026134d793745e0aa93bbbe6f32'
tests = json.loads((W / 'installed_verified_receipt.json').read_text())
assert tests['success'] and tests['tests'] == 8
note = f'''[INPUT] O operador relatou que a mãe não consegue abrir a IALD4.1(21), mesmo após apagar/reinstalar: fecha sozinho ao abrir. O próprio operador havia usado21 e exportado os três formatos. Não tratar como erro de servidor, memória ou senha.

[REAL — observação na Apple] Feedback de23/09/2026 10:39, build4.1(21), iPhone16ProMax, iOS27.0, anônimo: “Falhou não consigo baixar esse app”. Também há relato20/09 build16 no mesmo modelo/OS. IDs e identidade não demonstram que seja a mãe; compatível com a descrição do operador. Relatório ZIP foi solicitado pelo navegador, mas seu stack trace não ficou acessível localmente. Não inventar exceção nem assinatura de crash.

[REAL/DERIVED] Info.plist antigo não tinha UIApplicationSceneManifest e AppDelegate usava o ciclo legado. Apple exige UIScene em apps SDK27/iOS27; XcodeCloud mostra Xcode27(27A266a), macOS27. Incompatibilidade verificável e causa provável do encerramento; atribuição do crash específico ainda depende do aparelho/stack trace. Fonte: https://developer.apple.com/documentation/uikit/transitioning-to-the-uikit-scene-based-life-cycle .

[REAL — correção] Somente3arquivos do repo mobile alterados: Info.plist declara cena única/Main; AppDelegate.swift acrescenta SceneDelegate e encaminha cold/warmURL/UniversalLinks ao SceneDelegateProxy do Capacitor8.5.2; pbxproj21→22. Storyboard cria janela/bridge, sem segundaWebView e sem duplicar notificações. Preservados demais ajustes, permissões, login, webassets, Selo, kernel e exports. Backups imediatos debytes; manifesto local e instalado em {W}. Commit privado lido: {commit}. Nenhum servidor/chave/.env enviado.

[REAL — validação] Revisor independente sem bloqueantes estáticos;8/8checks deplist/classes/storyboard/target/forwarding/preservação passaram no stage e instalado; controleantigo falha como esperado. Validador deassets passou. XcodeCloud22 concluiuarchive comsucesso; run b12c43db-b7f2-4d39-834d-989e22972434. Compilação não é execução em iPhone. OAuth/retorno e abertura física pós22 aguardam teste.

[REAL — matriz] iOS4.1(22), build{a.build_id}: IALDEquipe={a.internal}; IALDPiloto={a.external}, observado após vinculação. Link do grupo já existente https://testflight.apple.com/join/A5XEdy1H. Web e Android4.1(20) preservados porque correção só iOS; GooglePlay continua cadastro/DUNS pendente. Não anunciar instalação física. Prazos operacionais atualizados apenas registroadministrativo, não app. Não executadas mensagens pagas, nemalterados modelos/cânone/gate. CorreçãoHaiku da etapa anterior preservada; reteste físicoHaiku ainda não confirmado.

[OPEN] Confirmar que a mãe atualizou22, abre semfechar, fazlogin e inicia conversa; testar no aparelho dooperador regressão deabertura/OAuth/export. Se persistir, obter .ips/stacktrace e confirmar modelo/OS da pessoa antes deatribuir os relatóriosanônimos. Não encerrarbug como curado somente porcompile. Manter entrega coordenada dos grupos semrepetir autorização.
'''
targets = [p.with_name('MEMORY_2.md') if p.name == 'MEMORY.md' else p for p in record.helper.TARGETS]
rows = [record.append(p, 'IALD_IOS22_SCENE_STARTUP_FIX_20260923', 'iOS22: migração UIScene e correção de inicialização iOS27', note, stamp, now) for p in targets]
deadline = root / 'iald_deadlines.json'
before = deadline.read_bytes()
data = json.loads(before)
data['checked_at'] = now.isoformat()
for key, group, state in [('testflight_internal', 'IALD Equipe', a.internal), ('testflight_external', 'IALD Piloto', a.external)]:
    data['items'][key].update(label=f'IALD 4.1 (22) — {group}', build='4.1 (22)', status=state,
        expires_at=None, source=f'App Store Connect, {now.isoformat()}: {state}; data exata de expiração não exibida.')
record.helper.create(deadline.with_name(deadline.name + '.bak_' + stamp), before)
after = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf8')
temp = deadline.with_name(deadline.name + '.tmp_' + stamp)
record.helper.create(temp, after)
assert deadline.read_bytes() == before
temp.replace(deadline)
assert deadline.read_bytes() == after
receipt = {'at': now.isoformat(), 'commit': commit, 'ios_build_id': a.build_id,
           'internal': a.internal, 'external': a.external, 'physical_test': 'pending',
           'web_android': 'unchanged, iOS-only fix', 'memory': rows}
record.helper.create(W / ('delivery_' + stamp + '.json'), json.dumps(receipt, ensure_ascii=False, indent=2).encode('utf8'))
print(json.dumps({'recorded': len(rows), 'ios': '4.1 (22)', 'physical_test': 'pending'}))
