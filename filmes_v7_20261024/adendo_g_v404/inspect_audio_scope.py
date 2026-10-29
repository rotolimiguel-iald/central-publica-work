"""Offline inventory of v404 speech changes; does not import um or synthesize."""
import ast
import copy
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys

G = Path(__file__).resolve().parent
W = G.parent
sys.path[:0] = [str(W), str(W / 'adendo_e_v402')]
from record_operator_acceptance import create, pin, read
from bootstrap import ACTOR, REF
import mission

ORDER = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_022_ADENDO_G_render_v404_e_frases_do_gate.md')
T = ORDER.parent.parent / 'DO_CHATGPT/ORDEM_022/ADENDO_G'
V = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
N = V.parent.parent / 'Nós'
REQUEST = 'ordem022-adendo-g-v404-20261028'


def current():
    p = mission.call({'operation': 'project', 'max_chars': 350000})
    return {'actor': ACTOR, 'expected_revision': p['receipt']['revision'], 'projection_sha256': p['projection_sha256']}


def main():
    assert not (G / 'AUDIO_SCOPE_CHECK.json').exists(), 'Recover existing inventory; do not repeat'
    assert pin(ORDER)['sha256'] == '8d71e12cc87d510fa32ee893e370681f79faa0fffb458281ba6876010c4c09e0'
    src = [{'path': str(ORDER), 'sha256': pin(ORDER)['sha256']}]
    requirement = {'id': 'ADENDO_G_V404', 'criterion': 'Adendo G: preparar V7 v404, substituir somente duas falas do gate verbatim em quatro línguas e números autorizados. TTS somente horizon/PT/EN e einstein/PT/EN; parar e informar segmentos/custo antes de qualquer outro TTS. Parar por outra divergência numérica ou avanço do selo. Um render v404, nenhum v403, sem publicação; revisão real distinta.', 'depends_on': []}
    if not (G / 'MISSION_EXTEND.json').exists():
        create(G / 'MISSION_EXTEND.json', mission.call({'operation': 'extend', **current(), 'event_id': REQUEST + '-extend', 'requirements': [requirement], 'reason': 'Adendo G decide as duas frases do F e autoriza v404 sob restrição explícita de quatro novas unidades TTS.', 'sources': src}))
    if not (G / 'MISSION_CLAIM.json').exists():
        create(G / 'MISSION_CLAIM.json', mission.call({'operation': 'claim', **current(), 'event_id': REQUEST + '-claim', 'task_id': requirement['id'], 'lease_seconds': 43200}))
    p = mission.call({'operation': 'project', 'max_chars': 350000})
    task = next(t for t in p['projection']['active'] if t['id'] == requirement['id'])
    preflight = mission.call({'operation': 'check', **current(), 'task_id': task['id'], 'lease_id': task['lease']['id'], 'max_chars': 350000})
    assert preflight['ready']
    if not (G / 'PREFLIGHT.json').exists():create(G / 'PREFLIGHT.json', preflight)
    else:create(G / 'PREFLIGHT_RECHECK_R2.json', preflight)

    seal = read(N / 'um_absoluto_selo.json')
    core = read(N / 'um_absoluto.json')['core']
    program = pin(N / 'um.py')
    assert seal['um_version'] == 'v404' and program['sha256'] == seal['sha256']['um.py']
    proof = core['estatuto_da_prova_v391']['prova_1_kernel']
    flags = core['bandeiras_do_gate_v403']['values']
    counts = {'proof_ladder_clean': proof['n_theorems_clean'], 'proof_ladder_total': proof['n_theorems_expected'], 'formal_count': len(core['kernel_formalization']['formal_files_sha256']), 'declaration_count': len(core['kernel_formalization']['axiom_report']), 'flags': flags['n_flags'], 'flags_computed': flags['n_calculated'], 'flags_literal': flags['n_literal']}
    assert counts == {'proof_ladder_clean':9698,'proof_ladder_total':9698,'formal_count':1438,'declaration_count':29484,'flags':18,'flags_computed':18,'flags_literal':0}, 'STOP: source/order counts differ'
    assert proof['no_trio'] == counts['declaration_count'] == proof['declaracoes_auditadas']
    assert flags['n_read_by_the_verdict'] == 15 and flags['gate_verdict_equals_v402'] is True
    create(G / 'SOURCE_INTAKE.json', {'order':pin(ORDER),'program':program,'seal':pin(N/'um_absoluto_selo.json'),'core':pin(N/'um_absoluto.json'),'version':seal['um_version'],'timestamp':seal['timestamp'],'counts':counts,'gate_values':flags,'source_executed_or_imported':False})

    baseline_path = V / 'audio/NARRATION_PLAN_v402_formula_final.json'
    baseline = read(baseline_path)
    templates_path = V / 'audio/script_templates.json'
    templates = read(templates_path)
    builder_path = V / 'audio/build_narration.py'
    assert pin(builder_path)['sha256'] == baseline['pins']['builder_sha256']
    assert pin(templates_path)['sha256'] == baseline['pins']['template_sha256']
    # Execute only these original read-only/pure helpers, not module initialization or transport.
    selected = {'require','sha','encoded','io_path','read_json','safe_text','fill','hud_values','cache_key','cache_status','completed_cached_audio'}
    tree = ast.parse(builder_path.read_text(encoding='utf-8'))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in selected]
    assert {n.name for n in nodes} == selected
    namespace = {'hashlib':hashlib,'json':json,'Path':Path,'os':os,'re':re,'math':math,'RATE':baseline['rate'],'FORMAT':baseline['format']}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(builder_path),'exec'),namespace)
    oldvalues = namespace['hud_values'](read(V / 'data/hud.json'))
    values = {**oldvalues,**counts,'theorems':counts['proof_ladder_clean'],'n_formal':counts['formal_count'],'seal_version':seal['um_version'],'seal_pin':program['sha256'],'seal_timestamp':seal['timestamp'],'um_sha16':program['sha256'][:16]}

    # Obtain the eight complete replacement strings from the authoritative order itself.
    text = ORDER.read_text(encoding='utf-8')
    gate_text = {}
    for film, segment, marker in [('film1','horizon','- Filme 1, segmento'),('film2','einstein','- Filme 2, segmento')]:
        section = text.split(marker,1)[1].split('\n- Filme ',1)[0]
        rows = re.findall(r'  - (PT|EN|FR \(legenda\)|zh-Hans \(legenda\)): «([^»]+)»',section)
        assert len(rows)==4
        for lang, sentence in rows:
            lang={'PT':'pt-BR','EN':'en','FR (legenda)':'fr','zh-Hans (legenda)':'zh-Hans'}[lang]
            assert str(counts['flags']) in sentence
            if film=='film2':assert str(counts['proof_ladder_clean']) in sentence
            gate_text[(film,segment,1,lang)]=sentence

    changes=[]; units={}; occurrences=0
    for film, data in baseline['films'].items():
        ts={s['key']:s for s in templates['films'][film]['segments']}
        for seg in data['segments']:
            for index,cue in enumerate(seg['cues']):
                for lang, oldtext in cue.items():
                    template=ts[seg['key']]['text'][lang][index]
                    assert namespace['fill'](template,oldvalues,lang,templates['formats'])==oldtext
                    newtext=gate_text.get((film,seg['key'],index,lang))
                    if newtext is None:newtext=namespace['fill'](template,values,lang,templates['formats'])
                    if newtext!=oldtext:changes.append({'film':film,'segment':seg['key'],'cue_index':index,'language':lang,'before':oldtext,'after':newtext,'segment_start':seg['start'],'segment_end':seg['end']})
                    if lang not in baseline['voices']:continue
                    occurrences+=1
                    voice=baseline['voices'][lang];key=namespace['cache_key'](voice,newtext)
                    if key not in units:
                        hit=namespace['completed_cached_audio'](namespace['io_path'](V/'audio/cache'),key)
                        units[key]={'key':key,'language':lang,'voice':voice,'text':newtext,'text_sha256':hashlib.sha256(newtext.encode()).hexdigest(),'characters':len(newtext),'cache_hit':None if hit is None else pin(hit),'cache_receipt':None if hit is None else pin(hit.with_suffix('.json')),'occurrences':[]}
                    units[key]['occurrences'].append({'film':film,'segment':seg['key'],'cue_index':index})
    allowed={('film1','horizon',1),('film2','einstein',1)}
    missing=[u for u in units.values() if u['cache_hit'] is None]
    extra=[u for u in missing if any((x['film'],x['segment'],x['cue_index']) not in allowed for x in u['occurrences'])]
    authorized=[u for u in missing if u not in extra]
    result={'schema':'iald.audio-scope-preflight.v404/v1','status':'STOP_ADDITIONAL_TTS_REQUIRES_AUTHORIZATION' if extra else 'AUDIO_SCOPE_WITHIN_AUTHORIZED_FOUR','request_id':REQUEST,'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actor':ACTOR,'mission_reference':str(REF),'order':pin(ORDER),'source':pin(G/'SOURCE_INTAKE.json'),'existing_plan':pin(baseline_path),'templates':pin(templates_path),'builder':pin(builder_path),'read_only_builder_helpers':sorted(selected),'voices':baseline['voices'],'rate':baseline['rate'],'format':baseline['format'],'changes':changes,'unit_counts':{'total_unique':len(units),'occurrences':occurrences,'reusable':len(units)-len(missing),'new_authorized':len(authorized),'new_outside_authorization':len(extra)},'authorized_new_units':authorized,'additional_new_units':extra,'all_units':list(units.values()),'cost':{'currency':'USD','estimated_direct_tts_charge_per_unit':0,'estimated_direct_tts_charge_extra_units':0,'estimated_direct_tts_charge_all_new_units':0,'statute':'DERIVED_ESTIMATE_NOT_PROVIDER_QUOTE','basis':'Installed MsEdgeTTS Read Aloud transport uses no user Azure billing credential or metered paid API. Upstream project identifies the library as free-tts. Zero is an incremental direct-charge estimate, not a provider invoice or guarantee of availability.','sources':['https://github.com/Migushthe2nd/MsEdgeTTS','https://support.microsoft.com/en-us/edge/use-immersive-reader-in-microsoft-edge'],'official_automation_tariff_found':False,'local_compute_energy_subscription_cost':'NOT_MEASURED','actual_new_tts_requests':0,'actual_new_tts_charge':0},'um_imported_or_executed':False,'render_started':False,'tts_started':False,'production_modified':False,'public_pointer':pin(V.parent/'PUBLIC_DELIVERY_V7.json'),'public_manifest':pin(V/'PUBLIC_DELIVERY_V7.json'),'other_numeric_comparison':'NOT_COMPLETED_AFTER_AUDIO_SCOPE_STOP'}
    create(G/'AUDIO_SCOPE_CHECK.json',result)
    print(json.dumps({'status':result['status'],'unit_counts':result['unit_counts'],'additional':extra,'changes':len(changes),'cost':result['cost']},ensure_ascii=False))


if __name__=='__main__':main()
