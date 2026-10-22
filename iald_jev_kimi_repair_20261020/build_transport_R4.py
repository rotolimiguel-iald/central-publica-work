"""Single-file R4 patch against installed sources. Never modifies runtime."""
from pathlib import Path
import hashlib,json,difflib
W=Path(__file__).resolve().parent;S=W/'admission_R4_stage';S.mkdir(exist_ok=False)
source=Path(r'C:\IALD\projetos_pyhton\IALD\iald_activity_operations.py')
raw=source.read_bytes();text=source.read_text(encoding='utf-8')
old='''        saw_terminal = False
        representation ='''
new='''        saw_terminal = False
        archived_sha = None
        representation ='''
assert text.count(old)==1;text=text.replace(old,new)
old='''        def terminal(line):'''
new='''        def finish_received():
            nonlocal archived_sha
            raw = (b'\\n' if lines else b'').join(raw_parts)
            sha = hashlib.sha256(raw).hexdigest()
            if sha == archived_sha:
                return
            receipt = archive_wire(self.op.lifecycle.binding, raw, representation, 'RECEIVED')
            if not self.op.done:
                self.op.complete({'http_status': self.response.status_code, 'response': receipt})
            else:
                # Terminal was already acknowledged. Preserve later received bytes
                # without a second result identity or a repeated operation.
                self.op.lifecycle.binding.checkpoint('transport_tail.' + self.op.id,
                    {'status': 'RECEIVED', 'transport': receipt})
            archived_sha = sha

        def terminal(line):'''
assert text.count(old)==1;text=text.replace(old,new)
old='''                    if terminal(line):
                        saw_terminal = True
                yield part'''
new='''                    if terminal(line):
                        saw_terminal = True
                if saw_terminal:
                    # The caller may break/close as soon as it receives this part.
                    # Custody of all bytes already received MUST precede that yield.
                    finish_received()
                yield part'''
assert text.count(old)==1;text=text.replace(old,new)
old='''            self._finish({'stream': text, 'representation': representation})
        finally:
            if not self.op.done:
                partial = (b'\\n' if lines else b'').join(raw_parts)
                self._custody_raw(partial, representation)'''
new='''            if saw_terminal:
                finish_received()
            else:
                self._finish({'stream': text, 'representation': representation})
        finally:
            if not self.op.done:
                partial = (b'\\n' if lines else b'').join(raw_parts)
                self._custody_raw(partial, representation)'''
assert text.count(old)==1;text=text.replace(old,new)
staged=text.encode();compile(staged,str(S/source.name),'exec')
with (S/source.name).open('xb') as f:f.write(staged)
with (S/'PATCH.diff').open('x',encoding='utf-8') as f:f.write(''.join(difflib.unified_diff(raw.decode().splitlines(True),text.splitlines(True),fromfile=str(source),tofile=str(S/source.name))))
with (S/'SOURCE_PIN.json').open('x',encoding='utf-8') as f:json.dump({'source':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),'stage':str(S/source.name),'stage_sha256':hashlib.sha256(staged).hexdigest()},f,indent=2)
print(json.dumps({'stage':str(S),'source_sha256':hashlib.sha256(raw).hexdigest()}))
