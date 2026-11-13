"""Operational staging adapter. Installed configuration is an operator artifact.

No production defaults: final path/hash configuration must receive independent
review. Commands are fixed pinned local Python tools, never source-file content.
"""
import json
from pathlib import Path
import subprocess
import sys
from continuous_source_prepare import discover,prepare_sources,immutable,dump,digest


class Adapter:
    def __init__(self, config):
        self.cfg=json.loads(Path(config).read_bytes())
        self.root=Path(self.cfg['state_root']).resolve()
        self.cached_probe=None;self.cached_candidate=None

    def command(self, name, args=(), payload=None):
        tool=self.cfg['tools'][name];path=Path(tool['path']).resolve(strict=True)
        if path.name=='um.py' or digest(path.read_bytes())!=tool['sha256']:
            raise ValueError('Trusted tool pin mismatch')
        p=subprocess.run([self.cfg['python'],'-B','-X','utf8',str(path),*map(str,args)],
                         input=None if payload is None else dump(payload),capture_output=True)
        if p.returncode: raise RuntimeError('Local tool failed: '+name)
        return p.stdout

    def detect(self):
        root=Path(self.cfg['vault_root'])
        dirs=sorted((p for p in root.glob('um_unificado_v*') if p.name.removeprefix('um_unificado_v').isdigit()),
                    key=lambda p:int(p.name.removeprefix('um_unificado_v')))
        if not dirs: return None
        # Full source hashing and public Git check happen only after this small
        # seal/custody byte probe changes (or a process restart).
        p=dirs[-1];seal=p/'um_absoluto_selo.json';custody=p/'CUSTODY_MANIFEST.json'
        probe=(str(p),digest(seal.read_bytes()),digest(custody.read_bytes()))
        if probe!=self.cached_probe:
            candidate=discover(root,self.cfg['repository'],self.cfg['installed_catalog'])
            self.cached_candidate=candidate;self.cached_probe=probe
        return self.cached_candidate

    def active(self):
        d=json.loads(Path(self.cfg['installed_catalog']).read_bytes())
        c=d['operational_core']
        return {'release':c['current_release'],'source_sha256':c['release_source_sha256']}

    def prepare(self,candidate,directory):
        runtime=Path(self.cfg['runtime']).resolve()
        sys.path.insert(0,str(runtime))
        import iald_kernel,iald_jev_control
        source=prepare_sources(candidate,directory/'source',iald_kernel.extract_sources,iald_jev_control)
        descriptor=dict(candidate,**source)
        descriptor_path=directory/'candidate.json';immutable(descriptor_path,dump(descriptor))
        self.command('prepare',['--descriptor',descriptor_path,'--output',directory/'package'])
        # The reviewer consumes these immutable artifacts; no model is called,
        # no reviewer actor is invented, and no acceptance is written here.
        immutable(directory/'REVIEW_REQUEST.json',dump({'status':'REVIEW_PENDING',
                  'candidate':candidate['identity'],'manifest':str(directory/'package'/'release.json'),
                  'required':'Actual distinct ACOM review pinned to package, install plan, runtime and source policy'}))

    def verify_package(self,directory):
        root=(directory/'package').resolve();path=root/'release.json';raw=path.read_bytes();m=json.loads(raw)
        rows=m['artifacts']
        if not rows: raise ValueError('Empty package')
        for row in rows:
            p=(root/row['path']).resolve(strict=True)
            if not p.is_relative_to(root): raise ValueError('Artifact path escape')
            b=p.read_bytes()
            if digest(b)!=row['sha256'] or len(b)!=row['bytes']: raise ValueError('Package artifact mismatch')
        return {'identity':{'release':m['release'],'source_sha256':m['source_sha256']},
                'manifest_sha256':digest(raw)}

    def review(self,directory,package_sha):
        # REVIEW_BINDING is produced by the real reviewer, not by this worker.
        p=directory/'REVIEW_BINDING.json'
        if not p.exists(): return False
        binding=json.loads(p.read_bytes())
        if binding['manifest_sha256']!=package_sha: raise ValueError('Review package changed')
        ref=Path(binding['reference']).resolve(strict=True)
        if not ref.is_relative_to(self.root): raise ValueError('Review reference outside updater scope')
        result=json.loads(self.command('mission',payload={'operation':'project','reference':str(ref),'max_chars':100000}))
        if result.get('ok') is not True: raise ValueError('ACOM project failed')
        projection=result['result']['projection']
        if projection['hold']: return False
        tasks=projection['active']+projection['settled']
        task=next(t for t in tasks if t['id']==binding['requirement'])
        if task['status']!='satisfied': return False
        if not task.get('reviewed_by') or task['reviewed_by']==task.get('submitted_by'):
            raise ValueError('Independent reviewer missing')
        expected=(directory/'package'/'release.json').resolve()
        if not any(Path(e['path']).resolve()==expected and e['sha256']==package_sha for e in task['evidence']):
            raise ValueError('Accepted evidence does not pin package')
        for row in binding['final_pins']:
            path=Path(row['path']).resolve(strict=True)
            if not path.is_relative_to(directory.resolve()): raise ValueError('Final pin scope mismatch')
            if digest(path.read_bytes())!=row['sha256']: raise ValueError('Reviewed final pin changed')
        return True

    def authorize(self,candidate):
        policy=self.cfg['standing_authorization']
        for row in policy['sources']:
            if digest(Path(row['path']).read_bytes())!=row['sha256']: return False
        return (policy['scope']=='app_science_transactional_updates' and
                policy['restart_ports']==[8082] and policy['independent_review_required'] is True)

    def quiet(self):
        return json.loads(self.command('quiet'))['quiet'] is True

    def deploy(self,directory,expected_active):
        # Wrapper is independently reviewed and pins its own imported modules.
        # It must recheck authorization/review/quiet/CAS while admission is frozen.
        expected=directory/'expected_active.json';immutable(expected,dump(expected_active))
        self.command('deploy',['--candidate',directory,'--expected-active',expected])

    def reconcile(self,directory):
        # A dedicated read-only verifier checks installed bytes, identity, rollback
        # and durable deployment receipt. Status text alone is never sufficient.
        result=json.loads(self.command('reconcile',['--candidate',directory]))
        if result.get('verified') is True and result.get('status') in ('ACTIVE','ROLLED_BACK'):
            return result['status']
        return None


def main():
    import argparse,threading
    from continuous_update_hook import acquire_mutex
    from continuous_update_worker import Worker
    parser=argparse.ArgumentParser();parser.add_argument('--config',required=True)
    args=parser.parse_args();handle=acquire_mutex()
    if handle is None: return
    adapter=Adapter(args.config)
    Worker(adapter.root,adapter).run(threading.Event(),interval=60)

if __name__=='__main__': main()
