"""Embed the tested v394 composition into a copy; preserve every baseline artifact."""
import ast
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
from diary_r1 import ROOT,new,pin

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394'
BASE=OUT/'baseline/um.py'
DEST=OUT/'candidate/um.py'

ARTICLE=r'''
def _v394_article_tex(text, core, lang):
    """Append the actual current-run result and scoped mathematics in both languages."""
    out = core.get('tempo_frequencia_v394') or {}
    pt = lang == 'pt'
    title = 'Tempo, frequencia e leitura gravitacional: composicao v394' if pt else 'Time, frequency and gravitational reading: v394 composition'
    def esc(value):
        replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
        return ''.join(replacements.get(ch, ch) for ch in str(value))
    block = '\n\\section*{' + title + '}\n'
    block += ('Resultado desta rodada: ' if pt else 'Result of this run: ') + esc(out.get('verdict', 'NOT_RUN')) + '.\n\n'
    block += (r'No modelo $M_2$, a conjugacao $C=\mathrm{diag}(1,i)$ realiza a ponte espectral: $H_g=CH_{lig}C^\dagger=iV_0K$, $\Omega=V_0/\hbar$. O fluxo continuo e seu relogio sao derivados para estes objetos. ' if pt else
              r'In the $M_2$ model, conjugation $C=\mathrm{diag}(1,i)$ realizes the spectral bridge: $H_g=CH_{lig}C^\dagger=iV_0K$, $\Omega=V_0/\hbar$. The continuous flow and its clock are derived for these objects. ')
    block += r'\[T_t(X)=U_t\{E_g(X)+e^{-\gamma t}[X-E_g(X)]\}U_t^\dagger,\qquad E_gT_t=E_g.\]' + '\n'
    block += r'\[c(t)=e^{(-\gamma+2i\Omega)t}c(0),\qquad\Delta t=\frac{\Delta\phi}{2\Omega}=-\frac{\log|c(t_2)/c(t_1)|}{\gamma}.\]' + '\n'
    block += ('As duas leituras de tempo exigem coerencia nao nula, gamma positivo e fase levantada. O espaco fixo tem dimensao complexa dois. A fase isolada admite alias; leitura preservada nao e preservacao de todo produto.\n\n' if pt else
              'The two clock readings require nonzero coherence, positive gamma and a lifted phase. The fixed space has complex dimension two. A single phase admits aliases; preserved reading does not preserve every product.\n\n')
    block += r'\[H_{pos}=E_{ref}I+H_g,\quad E_{ref}\ge V_0,\quad\gamma=\frac{\beta}{2\hbar}\left(\sqrt{E_{ref}+V_0}-\sqrt{E_{ref}-V_0}\right)^2.\]' + '\n'
    block += ('A referencia energetica e parte do contrato fisico. O caso Eref=V0 e uma instancia matematica, nao uma nova identificacao atomica universal. Os calculos sao sinteticos; nao acreditam a natureza e nao alteram o gate.\n\n' if pt else
              'The energy reference is part of the physical contract. Eref=V0 is a mathematical instance, not a new universal atomic identification. Calculations are synthetic; they neither credit nature nor change the gate.\n\n')
    block += ('Cunhagens do operador, preservadas na lingua original [INPUT/ONTO]:\n' if pt else 'Operator inscriptions, preserved in their original language [INPUT/ONTO]:\n')
    for record in _V394_INSCRIPTIONS.values():
        block += '\\begin{quote}\n' + esc(record['text']) + '\n\\end{quote}\n'
    assert text.count(r'\end{document}') == 1, 'article boundary missing or ambiguous'
    return text.replace(r'\end{document}', block + '\n' + r'\end{document}')
'''


def main():
    if (OUT/'INTEGRATION_R1.json').exists():
        raise FileExistsError('Integration already has an immutable receipt; inspect it instead of repeating')
    if DEST.read_bytes() != BASE.read_bytes():
        raise RuntimeError('Candidate has already changed; recover the prior attempt explicitly')
    manifest=json.loads((OUT/'formal_verified/FORMAL_MANIFEST.json').read_bytes())
    assert manifest['passed'] is True, 'formal compilation must finish first'
    raw=BASE.read_bytes();assert not raw.startswith(b'\xef\xbb\xbf')
    text=raw.decode('utf-8');tree=ast.parse(text)
    lines=raw.splitlines(keepends=True);starts=[];i=0
    for line in lines:starts.append(i);i+=len(line)
    def span(n):return starts[n.lineno-1]+n.col_offset,starts[n.end_lineno-1]+n.end_col_offset
    assignments={n.targets[0].id:n for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name)}
    edits=[]
    def replace_node(n,value):
        a,b=span(n);edits.append((a,b,value.encode('utf-8')))
    def append_dict(n,entries):
        a,b=span(n);assert raw[b-1:b]==b'}'
        insertion=''.join('    '+repr(k)+': '+repr(v)+',\n' for k,v in entries.items())
        edits.append((b-1,b-1,insertion.encode('utf-8')))
    embnode=assignments['_EMBEDDED_KERNEL_FILES'].value
    embedded=ast.literal_eval(embnode)
    modules=manifest['modules']
    bodies={m['relative']:Path(m['path']).read_text(encoding='utf-8') for m in modules}
    for m in modules:assert pin(m['path'])['sha256']==m['sha256']
    assert not(set(bodies)&set(embedded)), 'new modules already in baseline'
    assert all(not (OUT/'candidate/tgl_kernel'/rel).exists() for rel in bodies), 'Partial integration requires explicit recovery'
    imports=''.join('import '+rel[:-5].replace('/','.')+'\n' for rel in bodies)
    # Every prior source stays byte-identical; only aggregator/audit import glue grows.
    replacements={'TGLExt.lean':embedded['TGLExt.lean']+'\n'+imports,
                  'TGL/Audit.lean':imports+'\n'+embedded['TGL/Audit.lean']}
    for k,v in zip(embnode.keys,embnode.values):
        if isinstance(k,ast.Constant) and k.value in replacements:replace_node(v,repr(replacements[k.value]))
    append_dict(embnode,bodies)
    declarations=sorted(set(x for m in modules for x in m['theorems']))
    assert declarations
    flags={f'ext_tf394_{n:04d}':name for n,name in enumerate(declarations,1)}
    append_dict(assignments['_LEAN_THEOREM_FLAGS'].value,flags)
    ladder_function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='prove_external_ladder')
    ladder_node=next(n.value for n in ladder_function.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ext_flags' for t in n.targets))
    old_ladder=ast.literal_eval(ladder_node)
    assert len(old_ladder)==7045 and len(set(old_ladder))==7045
    _,ladder_end=span(ladder_node)
    assert raw[ladder_end-1:ladder_end]==b']'
    edits.append((ladder_end-1,ladder_end-1,(''.join('        '+repr(flag)+',\n' for flag in flags)).encode('utf-8')))
    replace_node(assignments['UM_VERSION'].value,repr('v394'))
    lineage=[]
    for n in tree.body:
        if isinstance(n,ast.Assign) and isinstance(n.value,ast.List):
            try:values=ast.literal_eval(n.value)
            except Exception:continue
            if any(isinstance(v,tuple) and len(v)>2 and v[0]=='v393' and v[1]=='RuleTruthContract' for v in values):lineage.append(n.value)
    assert len(lineage)==1
    _,end=span(lineage[0]);assert raw[end-1:end]==b']'
    extra=''.join('    '+repr(('v394',Path(rel).stem,rel,None,None))+',\n' for rel in bodies)
    edits.append((end-1,end-1,extra.encode('utf-8')))
    old=b'esc_ok_ = isinstance(n_cl_, int) and n_cl_ == n_ex_ == _V393_ESCADA["esperada"]'
    assert raw.count(old)==1
    pos=raw.index(old)
    edits.append((pos,pos+len(old),b'esc_ok_ = isinstance(n_cl_, int) and n_cl_ == n_ex_ and n_cl_ >= _V393_ESCADA["esperada"]  # v394: preserve historical floor; current exact ladder is checked by v394'))
    functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
    for expr in ast.walk(functions['emit_article']):
        if isinstance(expr,ast.Call) and isinstance(expr.func,ast.Name) and expr.func.id in ['build_pt','build_en']:
            source=ast.get_source_segment(text,expr);language='pt' if expr.func.id=='build_pt' else 'en'
            replace_node(expr,f'_v394_article_tex({source}, core, {language!r})')
    hook=b'    _figs = emit_figures(core)'
    assert raw.count(hook)==1;pos=raw.index(hook)
    edits.append((pos,pos,b'    _v394_result = tempo_frequencia_v394(core)\n    print("   [v394] tempo/frequencia: %s" % _v394_result["verdict"])\n'))
    seal_anchor=b'            "registros_v393": '
    assert raw.count(seal_anchor)==1;pos=raw.index(b'\n',raw.index(seal_anchor))+1
    edits.append((pos,pos,b'            "tempo_frequencia_v394": {k_: (core.get("tempo_frequencia_v394") or {}).get(k_) for k_ in ("verdict", "all_verified", "formal_theorems", "embedded_sources", "inscriptions", "runtime_executed", "scope", "does_not_gate_core")},\n'))
    inscriptions={}
    front=OUT.parent/'F1.TEMPO.LEITURA_20261015'
    for p in [front/'IGUALDADE_RECONHECIMENTO_R8/OPERADOR_IGUALDADE_VERBATIM.txt',front/'FREQUENCIA_E_GRAVITON_R9/OPERADOR_FREQUENCIA_VERBATIM.txt',front/'FREQUENCIA_E_GRAVITON_R9/OPERADOR_PONTE_EXISTENTE_VERBATIM.txt',front/'ENCAMINHAMENTO_V394_20261015/OPERADOR_ENVIO_V394_VERBATIM.txt',OUT/'OPERADOR_NOME_INTELIGENCIA_VERBATIM.txt']:
        info=pin(p);inscriptions[p.stem]={'text':p.read_text(encoding='utf-8'),'sha256':info['sha256'],'source_informative_only':str(p),'statute':'INPUT/ONTO operator verbatim'}
    expected=len(old_ladder)+len(flags)
    contract={'theorems':declarations,'source_sha256':{rel:hashlib.sha256(body.encode('utf-8')).hexdigest() for rel,body in bodies.items()},'expected_ladder':expected,'baseline_version':'v393','baseline_sha256':pin(BASE)['sha256']}
    physical=(OUT/'physical_contract/physical_parameters.py').read_text(encoding='utf-8')
    # This module is definitions only; no test/CLI is silently embedded.
    ptr=ast.parse(physical)
    assert all(isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.ClassDef,ast.Assign,ast.AnnAssign,ast.Expr)) for n in ptr.body)
    kms=(OUT/'physical_contract/kms_root_anchor_r2.py').read_text(encoding='utf-8')
    runtime=(OUT/'runtime/time_runtime_v394_r3.py').read_text(encoding='utf-8')
    chunk='\n\n# v394: isolated candidate composition, operator order 15/10/2026.\n'
    chunk+='_V394_FORMAL_CONTRACT = '+repr(contract)+'\n_V394_INSCRIPTIONS = '+repr(inscriptions)+'\n\n'+physical+'\n'+kms+'\n'+runtime+'\n'+ARTICLE+'\n'
    added_names=[n.name for n in ast.parse(chunk).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
    assert len(added_names)==len(set(added_names)) and not (set(added_names)&set(functions)), 'New definition shadows an existing function'
    pos=starts[functions['main'].lineno-1]
    edits.append((pos,pos,chunk.encode('utf-8')))
    edits.sort(reverse=True)
    last=len(raw)+1
    for a,b,data in edits:
        assert b<=last, 'overlapping edits'
        raw=raw[:a]+data+raw[b:];last=a
    ast.parse(raw.decode('utf-8'))
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S_%fZ')
    old=DEST.read_bytes();backup=DEST.with_name('um.py.bak_'+stamp)
    with backup.open('xb') as f:f.write(old)
    tmp=DEST.with_name('um.py.tmp_'+stamp)
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw and DEST.read_bytes()==old
    os.replace(tmp,DEST)
    # Materialize only changed and new embedded sources, in the copy.
    changed=[]
    for rel,body in {**replacements,**bodies}.items():
        p=OUT/'candidate/tgl_kernel'/rel;p.parent.mkdir(parents=True,exist_ok=True)
        if p.exists():
            bak=p.with_name(p.name+'.bak_'+stamp)
            with bak.open('xb') as f:f.write(p.read_bytes())
        temp=p.with_name(p.name+'.tmp_'+stamp)
        with temp.open('xb') as f:f.write(body.encode('utf-8'))
        os.replace(temp,p);changed.append(pin(p))
    new(OUT/'INTEGRATION_R1.json',{'candidate':pin(DEST),'baseline':pin(BASE),'backup':pin(backup),'edits':len(edits),'new_modules':list(bodies),'new_flags':flags,'expected_ladder':expected,'changed_materialized':changed,'script':pin(__file__),'status':'INTEGRATED_NOT_YET_INDEPENDENTLY_AUDITED','no_canonical_change':True})
    print(json.dumps({'candidate':pin(DEST),'new_theorems':len(declarations),'expected_ladder':expected},ensure_ascii=False))

if __name__=='__main__':main()
