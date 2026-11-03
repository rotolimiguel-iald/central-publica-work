"""Reviewer Q6b: would the runtime loader REFUSE the new packages? Re-apply, read-only and against the STAGED active manifest, the checks of R/claude_memory_package.load_package
(schema/model/prefix_file, prefix sha, reserved output/margin policy, context_budget equality, remaining >= 10000, tool identity format) and R/iald_release_binding.check_package_binding.
The staged manifest points at W paths (the install manifest points at not-yet-existing R paths), so the release identity is computed from the staged one. Audit hook: no sockets, no subprocess, no writes."""
import hashlib, json, os, sys
from pathlib import Path

sys.dont_write_bytecode = True
R = Path(r'C:\IALD\projetos_pyhton\IALD')
W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
SCR = (W / 'review/revisor_sonnet-app-v405-revisor').resolve()
ST = W / 'app/science/memory_stage'


def guard(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
        raise RuntimeError('blocked ' + event)
    if event == 'open':
        path, mode, flags = args
        if isinstance(path, int):
            return
        p = Path(os.fsdecode(path)).resolve()
        if p.name in ('.env', 'iald_stack_v7.py', 'iald_psion_state.json'):
            raise RuntimeError('private input forbidden')
        writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
        if writing and not p.is_relative_to(SCR):
            raise RuntimeError('write outside reviewer folder: ' + str(p))


sys.addaudithook(guard)
sys.path.insert(0, str(R))
import claude_profiles as cp
import iald_release_binding as irb

out = {}
release = irb.load_release(ST / 'manifest_staged.json')
out['release_identity_from_staged_manifest'] = release.identity
for pkg in ('haiku_expanded', 'shared'):
    root = W / 'app/packages' / pkg
    man = json.loads((root / 'manifest_install.json').read_bytes())
    raw = (root / 'prefix.md').read_bytes()
    b = man['budget']
    checks = {
        'schema': man.get('schema') == 'iald.claude.memory.v1',
        'model': man.get('model') == cp.HAIKU.model,
        'prefix_file': man.get('prefix_file') == 'prefix.md',
        'prefix_sha': hashlib.sha256(raw).hexdigest() == man.get('prefix_sha256'),
        'reserved_output_and_margin': b.get('reserved_output_tokens') == cp.HAIKU.default_output and b.get('margin_tokens') == 1024,
        'context_budget_equal': cp.context_budget(cp.HAIKU.model, counted_model=cp.HAIKU.model, permanent_tokens=b['permanent_tokens'], request_input_tokens=b['request_input_tokens'],
                                                   reserved_output_tokens=b['reserved_output_tokens'], margin_tokens=b['margin_tokens']) == b,
        'ready_and_remaining_ge_10000': b['ready'] is True and b['remaining_tokens'] >= 10000,
        'tools_sha256_format': isinstance(man.get('tools_sha256'), str) and len(man['tools_sha256']) == 64,
    }
    try:
        irb.check_package_binding(man, release)
        checks['check_package_binding'] = True
    except Exception as e:
        checks['check_package_binding'] = 'REFUSED: ' + type(e).__name__ + ': ' + str(e)[:200]
    inst = json.loads((R / '.iald_runtime' / ('haiku55' if pkg == 'haiku_expanded' else 'haiku') / 'manifest.json').read_bytes())
    out[pkg] = {'checks': checks, 'all_pass': all(v is True for v in checks.values()),
                'tools_sha256_same_as_installed_v404': man['tools_sha256'] == inst['tools_sha256'], 'counted_scoped_tools_sha256_same_as_installed_v404': man.get('counted_scoped_tools_sha256') == inst.get('counted_scoped_tools_sha256'),
                'manifest_keys_new_vs_installed_equal': sorted(man) == sorted(inst)}
print(json.dumps(out, ensure_ascii=False, indent=1))
