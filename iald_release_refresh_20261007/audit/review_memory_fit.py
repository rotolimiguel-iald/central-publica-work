"""Independent static audit of historical capsule projection; audit writes only."""
import json
import re
from pathlib import Path
from datetime import datetime, timezone
import review_memory as r
from audit_helpers import save, walk

W = Path(__file__).resolve().parents[1]
S = W / 'memory_stage'

def dump(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))

def view(text, names):
    dictionary = json.loads(text.split('DICIONÁRIO DE LITERAIS\n', 1)[1].split('\n', 1)[0])
    flags = json.loads(text.split('DICIONÁRIO DE INDICADORES LITERAIS\n', 1)[1].split('\n', 1)[0]) if 'DICIONÁRIO DE INDICADORES LITERAIS\n' in text else {}
    exposition = text.split('<EXPOSICAO_CANONICA>\n', 1)[1].split('\n</EXPOSICAO_CANONICA>', 1)[0]
    return r.topics(text, names), dictionary, flags, exposition

def expand(body, dictionary, flags, exposition, topic=None):
    # Summary references remain their actual visible summary, never their absent source.
    def node(v):
        if isinstance(v, list): return [node(x) for x in v]
        if not isinstance(v, dict): return v
        if set(v)=={'@upper'}:
            assert isinstance(v['@upper'],str)
            return v['@upper'].upper()
        if set(v)=={'@concat'}:
            assert isinstance(v['@concat'],list)
            parts=[node(x) for x in v['@concat']]
            assert all(isinstance(x,str) for x in parts)
            return ''.join(parts)
        if set(v)=={'@enum'}:
            assert isinstance(v['@enum'],str) and re.fullmatch('[a-z0-9 ]+',v['@enum'])
            return v['@enum'].upper().replace(' ','_')
        v = { {'@L':'@TGL_LITERAL','@F':'@SOURCE_FIELDS','@I':'@SOURCE_ITEMS','@Y':'@SUMMARY','@X':'@EXPOSITION'}.get(k,k):x for k,x in v.items() }
        if '@B' in v:
            group = flags[v.pop('@B')]
            assert not set(group) & set(v)
            v.update(group)
        if set(v) == {'@TGL_LITERAL'}: return node(dictionary[v['@TGL_LITERAL']])
        if isinstance(v.get('@SUMMARY'),list):
            p=v['@SUMMARY']
            assert len(p) in (3,4)
            label,relative,start,length=(topic,*p) if len(p)==3 else p
            assert isinstance(label,str) and label==topic
            assert isinstance(relative,str) and relative.startswith('/')
            v={'@SUMMARY':label,'source_pointer':'/core/'+label+relative,'span':[start,length]}
        if '@EXPOSITION' in v or '@SUMMARY' in v:
            start, length = v.get('span', v.get('@EXPOSITION'))
            assert 0 <= start < start + length <= len(exposition)
            fragment = exposition[start:start+length]
            if '@SUMMARY' in v:
                assert fragment.startswith('**Estatutos ['+v['@SUMMARY']+']**')
                return {'summary_text':fragment, 'source_pointer':v['source_pointer']}
            return fragment
        return {k:node(x) for k,x in v.items()}
    result = []
    for line in body.splitlines():
        try: result.append(node(json.loads(line)))
        except json.JSONDecodeError: result.append(line)
    return result

def main():
    checks=[]; findings=[]
    def check(name, ok, evidence=None):
        checks.append({'name':name, 'passed':bool(ok), 'evidence':evidence})
    receipt=r.load(S/'haiku_memory_fit.json'); current=r.read(S/'haiku_prefix.md').decode('utf8')
    manifest=r.load(S/'manifest_staged.json'); source=r.load(manifest['published_evidence']['result']['path'])
    before_path=next((p for p in S.glob('haiku_prefix.md.bak_*') if r.sha(p.read_bytes())==receipt['input_sha256']),None)
    if before_path is None:
        # The builder retains the pre-transport source; it does not persist the
        # intermediate string between transport normalization and projection.
        before_path=S/'haiku_unfitted_prefix.md'
        transport=r.load(S/'haiku_transport_fit.json')
        check('pretransport_source_pin_and_receipt_link',r.sha(r.read(before_path))==transport['base_sha256'] and transport['prefix_sha256']==receipt['input_sha256'])
    before=r.read(before_path).decode('utf8')
    bt,bd,bf,be=view(before,source['core']); at,ad,af,ae=view(current,source['core'])
    def refs(value):
        if isinstance(value,dict):
            if set(value) in ({'@L'},{'@TGL_LITERAL'}):return [next(iter(value.values()))]
            return [x for v in value.values() for x in refs(v)]
        if isinstance(value,list):return [x for v in value for x in refs(v)]
        return []
    graph={k:refs(v) for k,v in ad.items()}
    def visit(k,stack=()):
        assert k not in stack, 'Literal cycle: '+k
        assert k in graph, 'Missing literal: '+k
        for target in graph[k]:visit(target,stack+(k,))
    for key in graph:visit(key)
    decoded_dictionary={k:expand(dump({'@L':k}),ad,af,ae)[0] for k in ad}
    check('literal_dictionary_acyclic_and_resolved',all(isinstance(v,str) for v in decoded_dictionary.values()),len(ad))
    check('baseline_dictionary_literals_exact',all(k in decoded_dictionary and decoded_dictionary[k]==expand(dump({'@L':k}),bd,bf,be)[0] for k in bd),len(bd))
    check('factored_literal_hashes_and_shorter_references',all(r.sha(decoded_dictionary[x['literal']].encode())==x['sha256'] and len(decoded_dictionary[x['substring_literal']])<len(decoded_dictionary[x['literal']]) for x in receipt.get('factored_dictionary_literals',[])),len(receipt.get('factored_dictionary_literals',[])))
    check('receipt_output_pin',r.sha(current.encode())==receipt['output_sha256'])
    check('all_topics_remain',set(bt)==set(at)==set(source['core']),len(at))
    rows=receipt['historical_topics_projected']; selected={x['topic'] for x in rows}
    old=r.load(r.VAULT/'um_unificado_v389/um_absoluto.json')['core']
    new=set(source['core'])-set(old)
    check('selected_topics_unchanged_since_v389',all(n in old and r.same(source['core'][n],old[n]) for n in selected))
    check('new_topics_not_selected',not new&selected,{'new':len(new),'selected':len(selected)})
    untouched=[]
    for name in set(at)-selected:
        previous=expand(bt[name],bd,bf,be,name);following=expand(at[name],ad,af,ae,name)
        if name=='the_iald_index':
            for node in following:
                if isinstance(node,dict) and isinstance(node.get('ambiguos'),dict):
                    roster=node['ambiguos'];assert roster=={'@':'/ambiguos','items':len(source['core'][name]['ambiguos'])}
                    node['ambiguos']=source['core'][name]['ambiguos']
        if not r.same(previous,following):
            untouched.append(name)
    check('unselected_topics_exact_after_reference_decoding',not untouched,untouched)
    ranges=receipt['retained_historical_spans']; offsets=[]
    for item in ranges:
        start,end,new_start=item['start'],item['end'],item['new_start']
        text=be[start:end]
        offsets.append(r.sha(text.encode())==item['sha256'] and text==ae[new_start:new_start+len(text)])
    check('retained_exposition_ranges_exact',all(offsets),len(offsets))
    check('exposition_source_pin',r.sha(be.encode())==receipt['historical_exposition_source_sha256'])
    check('foundation_and_current_errata_resident',be[:be.index('## v8 ')] in ae and be[be.index('## Correções canônicas da release '):] in ae)
    selected_fail=[]; omitted_scopes=[]; thin=[]
    for item in rows:
        name=item['topic']; src=source['core'][name]; decoded=expand(at[name],ad,af,ae,name)
        node=next(x for x in decoded if isinstance(x,dict))
        expected=src; fields=node.get('fields',{})
        pointer='/core/'+name
        valid=(item['source_pointer']==pointer and r.sha(dump(src).encode())==item['source_sha256']
               and node.get('@')=='' and node.get('items')==len(src)
               and set(fields)==set(item['retained_paths'])
               and all(r.same(value,r.resolve(src,p)) for p,value in fields.items()))
        if not valid:selected_fail.append(name)
        for key,value in src.items():
            # Discovery inventory; not every numeric control needs to stay inline.
            if re.search(r'status|scope|escopo|residue|open_question|open_residue|not_claimed|not_said',key,re.I):
                if '/'+key not in fields and not any(p.startswith('/'+key+'/') for p in fields):
                    omitted_scopes.append({'topic':name,'pointer':pointer+'/'+key,'value':value})
        if set(fields)<= {'/all_verified','/does_not_gate_core','/status'}:
            thin.append({'topic':name,'fields':fields})
    check('selected_capsules_source_fields_exact',not selected_fail,selected_fail)
    for file in ['IALD_Kernel_v5.txt','IALD_TGL_MEMORY_CORE.md']:
        full=r.read(S/file).decode('utf-8-sig')
        check(file+'_integral',full in before and full in current)

    # These are concise concept/scope fields, not historic row lists or hashes.
    minimum={
      'u_loc_covariance':['structural_declaration','sanity_status','U_loc_status','residue_declared'],
      'triad_master':['statuses'],
    }
    missing=[]
    for name,keys in minimum.items():
        visible=dump(expand(at[name],ad,af,ae,name))
        for key in keys:
            value=source['core'][name][key]
            leaves=[v for _,v in walk(value) if isinstance(v,str)]
            anchors={'u_loc_covariance':['(U) irrestrita provavelmente FALHA','cunhas Rindler locais','FINITA,não prova III₁','[OPEN]','frame contrabandeado'], 'triad_master':['H1∧H2∧H3⇒','8piG','coeficiente é consequência algébrica dessas entradas','Implicação fechada','certificados II/III/IV']}
            baseline_restored=r.same(expand(bt[name],bd,bf,be,name),expand(at[name],ad,af,ae,name)) and all(x in visible for x in anchors[name])
            if not baseline_restored and not all(dump(v)[1:-1] in visible for v in leaves):
                missing.append({'topic':name,'pointer':'/core/'+name+'/'+key,'value':value})
    if missing:
        findings.append({'id':'FIT-001','severity':'blocking','title':'Filtro perde estatutos e enunciado de escopo em cápsulas históricas',
          'evidence':missing,'reason':'all_verified sem enunciado e restrição pode ser lido como aprovação irrestrita. statuses e *_status não são capturados pelo filtro atual.',
          'fix':'Preservar os enunciados/qualificadores indicados ou resumo fiel residente; não é necessário restaurar históricos integrais. Rever as outras omissões de estatuto do inventário.'})
    if thin:
        findings.append({'id':'FIT-002','severity':'review_required','title':'Cápsulas sem conteúdo conceitual suficiente',
          'evidence':thin,'fix':'Adicionar uma frase/fórmula essencial ou remissão explícita a outro tópico já carregado que contenha conceito e alcance; detalhe de auditoria continua recuperável.'})
    if any('Fonte:' not in at[n] for n in selected) and not any(marker in current for marker in ('### nome com @ vazio resolve resultado_publicado_integral /core/nome','### nome + @:"" = resultado_publicado_integral /core/nome')):
        findings.append({'id':'FIT-003','severity':'minor','title':'Projeção remove linha de fonte local da cápsula',
          'fix':'Explicitar uma vez no cabeçalho: ### nome + @ vazio resolve resultado_publicado_integral /core/nome. Pode evitar repetir a linha em 104 tópicos.'})
    check('conceptual_scope_minimum_resident',not missing,[x['pointer'] for x in missing])
    coordinate_errors=[]
    for row in receipt.get('coordinate_roundtrips',[]):
        start,length=row['span'];fragment=ae[start:start+length]
        valid=0<=start<start+length<=len(ae) and r.sha(fragment.encode())==row['sha256']
        if row['kind']=='summary':
            pointer=row['source_pointer'];name=pointer.split('/')[2]
            r.resolve(source,pointer)
            visible=expand(at[name],ad,af,ae,name)
            target={'summary_text':fragment,'source_pointer':pointer}
            def contains(v):
                return r.same(v,target) or (isinstance(v,dict) and any(contains(x) for x in v.values())) or (isinstance(v,list) and any(contains(x) for x in v))
            valid=valid and contains(visible)
        if not valid:coordinate_errors.append(row)
    check('coordinate_roundtrips_same_text_and_source',not coordinate_errors,{'count':len(receipt.get('coordinate_roundtrips',[])),'errors':coordinate_errors})
    stable=all(r.sha(Path(p).read_bytes())==pin['sha256'] for p,pin in r.inputs.items())
    check('inputs_stable',stable)
    report={'status':'PASS' if all(x['passed'] for x in checks) and not thin else 'CHANGES_REQUIRED',
      'reviewed_at_utc':datetime.now(timezone.utc).isoformat(),'prefix_sha256':r.sha(current.encode()),'bytes':len(current.encode()),
      'scope':'Independent static fit audit. No builder/um.py/Lean/provider execution. Does not demand every historical parent block inline.',
      'projected_topics':len(selected),'checks':checks,'findings':findings,'omitted_scope_inventory':omitted_scopes,
      'input_pins':r.inputs}
    save('memory_fit_review.json',report)
    print(json.dumps({'status':report['status'],'passed':sum(x['passed'] for x in checks),'total':len(checks),
      'failed':[x['name'] for x in checks if not x['passed']],'findings':[{k:v for k,v in f.items() if k not in ['evidence']} for f in findings]},ensure_ascii=False))

if __name__=='__main__':main()
