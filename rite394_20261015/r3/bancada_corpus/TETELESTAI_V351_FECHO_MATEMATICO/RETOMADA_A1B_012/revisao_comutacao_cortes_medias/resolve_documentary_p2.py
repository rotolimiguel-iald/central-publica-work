from review_helpers import *
from copy import deepcopy

def main():
    original_comp_path=OUT/'compilation.json'
    original_report_path=OUT/(NAME+'.json')
    originals=[pin(p) for p in OUT.iterdir() if p.is_file() and (p.name.startswith('REVIEW_') or p.name in ['compilation.json','documentary_finding.json','pin_verification.json'])]
    old=load(original_comp_path);oldreport=load(original_report_path)
    assert old['mathematical_review_passed'] and not old['unqualified_delivery_accepted']
    assert len(old['P2'])==1 and old['P2'][0]['id']=='P2-CFC-PROVIDER-LOCATOR'
    checked=[];validate_pin_tree(old,checked);validate_pin_tree(oldreport,checked)
    cp=R/'ADENDO_FICHA_COMUTACAO_CFC_CORRECAO.json';mp=R/'ADENDO_FICHA_COMUTACAO_CFC_CORRECAO.md'
    correction=load(cp);validate_pin_tree(correction,checked)
    original_finding=load(OUT/'documentary_finding.json')
    assert correction['supersedes_provider_zero_of']==original_finding['documents'][0]
    assert correction['historical_md']==original_finding['documents'][1]
    assert len(correction['providers'])==1
    provider=correction['providers'][0]
    source=Path(correction['source']['path']);text0=source.read_text(encoding='utf8')
    m=re.search(r'^protected theorem IsSelfAdjoint\.commute_cfc \{a b : A\}[\s\S]*? :=',text0,re.M);assert m
    actual=dict(name='IsSelfAdjoint.commute_cfc',line=text0[:m.start()].count('\n')+1,statement=m[0][:-3].rstrip())
    assert actual==provider and actual['line']==87
    own_source=Path(original_finding['finding']['actual']['source']['path'])
    assert own_source.read_bytes()==source.read_bytes()
    md=mp.read_text(encoding='utf8')
    assert provider['statement'] in md and str(source)+':87' in md
    assert 'Esta correção não é uma alegação de ficha anterior ao código' in md
    assert 'Commute.cfcₙ_nnreal' in md
    assert correction['timestamp']>oldreport['timestamp']
    assert load(Path(old['run']['path']))['returncode']==0
    assert load(Path(old['type_axiom_audit']['path']))['all_axioms_allowed']
    resolution=dict(timestamp=now(),id='P2-CFC-PROVIDER-LOCATOR',status='RESOLVED_BY_ADDITIVE_DOCUMENTARY_CORRECTION',source_statement_exact=True,own_author_mathlib_sources_byte_equal=True,previous_documents_unchanged=True,correction_posterior_to_code=True,correction_json=pin(cp),correction_markdown=pin(mp),corrected_provider=actual,source=pin(source),own_source=pin(own_source),author_correction_script_read_only=pin(R/'correct_cutoff_cfc_reference.py'),original_finding=pin(OUT/'documentary_finding.json'),previous_artifacts=originals,no_lean_recompilation=True,no_author_script_executed=True)
    save(OUT/'documentary_resolution_v2.json',resolution)
    comp=deepcopy(old)
    comp.update(timestamp=now(),status=STATUS,revision=2,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],resolved_findings=[dict(id=resolution['id'],status='RESOLVED',resolution=pin(OUT/'documentary_resolution_v2.json'))],previous_compilation=pin(original_comp_path),previous_reports=[pin(original_report_path),pin(OUT/(NAME+'.md'))],documentary_resolution=pin(OUT/'documentary_resolution_v2.json'),correction_documents=[pin(cp),pin(mp)],lean_runs_reused_without_recompilation=True,source_and_objects_unchanged=True,version2_helper=pin(Path(__file__)))
    comp['historical_documentary_finding']=comp.pop('documentary_finding')
    validate_pin_tree(comp,checked)
    save(OUT/'compilation_v2.json',comp)
    report=deepcopy(oldreport)
    report.update(timestamp=now(),status=STATUS,revision=2,mathematical_review_passed=True,unqualified_delivery_accepted=True,P0=[],P1=[],P2=[],findings=[],resolved_findings=comp['resolved_findings'],compilation=pin(OUT/'compilation_v2.json'),previous_reports=comp['previous_reports'],documentary_resolution=comp['documentary_resolution'],lean_runs_reused_without_recompilation=True)
    report['limits']=[v for v in report['limits'] if 'P2 documental' not in v]
    report['semantic_review'].append('[REAL — P2 encerrado] A correção MD/JSON foi lida integralmente e confrontada com Commute.lean nas árvores K e V, byte a byte iguais: IsSelfAdjoint.commute_cfc, linha 87, enunciado exato. O adendo histórico permanece intacto e a correção declara ser posterior ao código. O fornecedor Commute.cfcₙ_nnreal permanece inalterado. Nenhuma fonte, objeto ou run Lean foi alterado; esta V2 apenas encerra o achado documental e inclui sua evidência.')
    validate_pin_tree(report,checked)
    v2name=NAME+'_V2';save(OUT/(v2name+'.json'),report)
    target=next(x for x in comp['objects'] if x['module']=='TGLExt.V351CutoffAverageCommutation')
    run=load(Path(comp['run']['path']))
    result='# Revisão independente V2 — comutação de cortes e médias\n\n'+now()+'\n\n**'+STATUS+'**\n\n[REAL] **Sem P0, P1 ou P2 pendente. P2-CFC-PROVIDER-LOCATOR encerrado.** Três teoremas públicos + um helper privado, zero definições. Esta V2 preserva integralmente o parecer/compilation anteriores e reaproveita o Lake e auditor próprios rc0; nenhuma recompilação foi executada para a correção documental.\n\n'
    result+='\n\n'.join(report['semantic_review'])+'\n\n'
    result+='[REAL — reprodução herdada] '+str(comp['own_previous_project_object_count'])+' objetos próprios anteriores preservados; somente módulo e auditor acrescentados (total '+str(comp['own_project_object_count_after'])+'). Nenhum objeto autoral/DEV herdado, nenhum fornecedor antigo reconstruído. Pacotes externos: cache pinado da reprodução anterior. O run próprio original concluiu rc0 em '+str(round(run['elapsed_seconds'],3))+' s, zero avisos do alvo/auditor, trio propext/Classical.choice/Quot.sound com #check de universos. As '+str(len(comp['supplierwarnings']))+' mensagens históricas de fornecedores e stderr permanecem no compilation.\n\n'
    result+='| Artefato | SHA256 lido |\n|---|---|\n| Fonte final inalterada | `'+target['source']['sha256']+'` |\n| .olean próprio inalterado | `'+target['own']['sha256']+'` |\n| .olean cold autoral, comparação somente | `'+target['author_cold']['sha256']+'` |\n\nIgualdade binária medida: '+str(target['equal_author_cold'])+'.\n\n'
    result+='[OPEN — limites] '+' '.join(report['limits'])+'\n\nArtefatos desta V2:\n\n'
    for label,p in [('compilation V2',report['compilation']),('resolução documental',comp['documentary_resolution']),('correção MD',pin(mp)),('correção JSON',pin(cp)),('run próprio preservado',comp['run']),('tipos/axiomas preservados',comp['type_axiom_audit'])]:result+='- ['+label+'](<'+p['path']+'>) — SHA256 `'+p['sha256']+'`.\n'
    fresh(OUT/(v2name+'.md'),result.encode())
    for p in originals:ck(p)
    save(OUT/'pin_verification_v2.json',dict(timestamp=now(),all_active_pins_match=True,checked_pin_occurrences=len(checked),old_artifacts_unchanged=True,old_artifacts=originals,report=pin(OUT/(v2name+'.md')),report_json=pin(OUT/(v2name+'.json')),compilation=report['compilation'],no_lean_execution=True))
    print(json.dumps(dict(report=pin(OUT/(v2name+'.md')),json=pin(OUT/(v2name+'.json')),compilation=report['compilation'],status=STATUS,P0=[],P1=[],P2=[]),ensure_ascii=False))

if __name__=='__main__':main()
