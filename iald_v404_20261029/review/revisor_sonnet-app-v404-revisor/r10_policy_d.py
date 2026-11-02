"""Reviewer: Policy D (EXPAND_OVERRIDE=()) implemented as stated? Rebuild haiku_expanded from haiku55 base independently (no codec import, no execution of um.py: ast.parse only)."""
import json,re,ast,hashlib,sys
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029')
sha=lambda b:hashlib.sha256(b).hexdigest()
cfg_src=(W/'release_cfg.py').read_text('utf-8')
m=re.search(r'(?m)^EXPAND_OVERRIDE\s*=\s*(\(\))',cfg_src);print('EXPAND_OVERRIDE literal in release_cfg.py:',m.group(0)[:60] if m else None)
ns={}
# evaluate expand_suffixes() semantics without importing release_cfg (which reads vault): replicate trivial rule
print("''.endswith(()) semantics:",'caminho_v403'.endswith(()),'(False means no suffix-selected topic)')
res=json.loads((W/'app/science/memory_stage/release/Um (absoluto) — Grande Atrator/um_absoluto.json').read_bytes());core=res['core']
rx=re.compile('lagrang|hamilton|lindblad|dephas|bootstrap|breuer|horizon|master|three_locks|continuous_modular_zero|light_eigen|the_imported|price_of_the_gravity')
selected=[n for n in core if rx.search(n)]
fp=json.loads((W/'app/packages/haiku_expanded/FINAL_PREPARATION.json').read_bytes())
print('regex-selected topics:',len(selected),'| FINAL_PREPARATION.expanded_topics:',len(fp['expanded_topics']),'| equal as sets:',set(selected)==set(fp['expanded_topics']),'| any version-suffixed:',[n for n in fp['expanded_topics'] if re.search(r'_v\d{3}$',n)])
dump=lambda v:json.dumps(v,ensure_ascii=False,separators=(',',':'),allow_nan=False)
base=(W/'app/packages/haiku55/prefix.md').read_text('utf-8');exp=base
for n in selected:
    pat=r'(?m)^### '+re.escape(n)+r'\nFonte: [^\n]+\n[^\n]+(?=\n)'
    exp,k=re.subn(pat,lambda _:'### '+n+'\nFonte: resultado_publicado_integral /core/'+n+'\n'+dump(core[n]),exp)
    assert k==1,(n,k)
prog=(W/'app/science/memory_stage/release/Um (absoluto) — Grande Atrator/um.py').read_bytes()
lines=prog.decode('utf-8-sig').splitlines(keepends=True)
node=next(x for x in ast.parse(prog).body if isinstance(x,ast.FunctionDef) and x.name=='prove_the_bootstrap')
chunk=''.join(lines[node.lineno-1:node.end_lineno])
exp+='\n<BOOTSTRAP_SOURCE_DOCUMENTARY_NOT_EXECUTED>\n'+dump({'source_sha256':sha(prog),'symbol':node.name,'lines':[node.lineno,node.end_lineno],'chunk_sha256':sha(chunk.encode()),'statute':'SOURCE_DEFINITION_NOT_NEW_EXECUTION'})+'\n```python\n'+chunk+'```\n</BOOTSTRAP_SOURCE_DOCUMENTARY_NOT_EXECUTED>\n'
built=(W/'app/packages/haiku_expanded/prefix.md').read_bytes()
print('haiku_expanded rebuilt from haiku55 base == built bytes:',exp.encode()==built,len(exp.encode()),len(built))
# haiku55 base vs shared: no private atlas marker; exposition identical in the haiku packages
print('private atlas marker in packages:',{f:('<ATLAS_CANONICO' in (W/'app/packages'/f/'prefix.md').read_text('utf-8')) for f in('shared','haiku_expanded','haiku55','sonnet_public')})
# estimated vs native haiku remaining
b=json.loads((W/'app/PREPARED_BINDING.json').read_bytes());nc=json.loads((W/'app/packages/haiku_expanded/native_count.json').read_bytes())['budget']
print('estimated remaining (pre-count):',b['estimated_remaining_haiku55'],'native remaining:',nc['remaining_tokens'])
