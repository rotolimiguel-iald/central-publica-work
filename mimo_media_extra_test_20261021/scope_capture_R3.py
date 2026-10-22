from pathlib import Path
W=Path(__file__).resolve().parent
s=(W/'capture_extra_audio.py').read_text(encoding='utf-8')
old="'SELECT context_id,revision,changes_json FROM events WHERE changes_json LIKE ?'"
query="SELECT e.context_id,e.revision,e.changes_json FROM events e JOIN contexts c ON c.context_id=e.context_id WHERE json_extract(c.scope_json,'$.house')='IALD_APP' AND e.changes_json LIKE ?"
assert s.count(old)==1
s=s.replace(old,repr(query));compile(s,'capture','exec')
(W/'capture_extra_audio_R3.py').open('x',encoding='utf-8').write(s)
