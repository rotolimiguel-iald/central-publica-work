"""Reviewer: write receipts/v404-review-findings.json (exclusive create). Numbers read from the reviewer's own output files; hashes computed here."""
import json,hashlib,datetime
from pathlib import Path
W=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029');RV=W/'review/revisor_sonnet-app-v404-revisor'
sh=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
rd=lambda p:json.loads(Path(p).read_bytes())
r1=rd(RV/'r1_out.json');r3=rd(RV/'r3_out.json');r3o=rd(RV/'r3_out_v402.json');r5=rd(RV/'r5_out.json');r4=rd(RV/'r4_out.json');r3d=rd(RV/'r3d_out_v404.json')
dry=rd(RV/'review_app_dryrun_output.json');ver=rd(RV/'r2_verify_sources_shim_output.json');bld=rd(W/'sources_verified.json')
ver2={k:v for k,v in ver.items() if k!='checked_at'};bld2={k:v for k,v in bld.items() if k!='checked_at'}
files=sorted(p for p in RV.iterdir() if p.is_file() and p.suffix in('.py','.json','.txt'))
evid={p.name:sh(p)[:16] for p in files}
def pk(name):
    v=r3['packages'][name]
    return {'bytes':v['bytes'],'topics_present':v['present'],'lost':v['lost'],'topics_restoring_exactly_own_decoder':v['topics_restoring_exactly'],'n_mismatch':v['n_mismatch']}
packages={k:pk(k) for k in('shared','haiku_expanded','haiku55','sonnet_public')}
old={}
for p,s in r4.items():
    old[p]={'strict_hits_raw':len(s['RAW_old0']),'where':[(('sealed v392 record estatuto_da_prova_ressalva_v392' if h[0]=='estatuto_da_prova_ressalva_v392' else 'literal dictionary entry (v403 erratum quoting the old wording as true on its date and superseded)' if h[2] else 'sealed canonical-form index line (exposition) carrying the v392 verdict token'),h[1][:60],'supersession marker in context' if h[2] else 'no local marker') for h in s['RAW_old0']],
            'bandeiras_do_gate_v403_present':s['has_bandeiras_do_gate_v403']}
out={
 'status':'NOT_ACCEPTED__PENDING_MANAGEMENT_DECISION','release':'v404','reviewer':'sonnet-app-v404-revisor','builder':'sonnet-app-v404-construtor',
 'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'steps':{'app':'NOT_ACCEPTED (review_pending kept; no mission accept sent)','sources':'NOT_ACCEPTED (review_pending kept; all source checks PASS -- held together with `app` so the pair is decided at once; sources is not itself defective)'},
 'validation/review_final.json':'NOT WRITTEN (deploy_controlled.py asserts it; the PASS from review_app.py logic is in review_app_dryrun_output.json, a differently named file that gates nothing)',
 'ls_remote_origin_main':'1d3c4cbe3f3ce5182e1d8e123d76bad5a7ac15ad\trefs/heads/main (the only network call; equals RELEASE.espelho_commit, local HEAD and origin/main)',
 'passed_checks':{
   'C1_release_and_commit_binding':{'run':r1['n'],'passed':r1['passed'],'note':'ls-remote == pin; um.py blob at pinned commit == selo cofre == selo Nos == RELEASE pin; 3ae6f43f is ancestor; identical bytes at both commits for um.py, selo, core, proof manifest, canonical form, um_absoluto_pt.txt, both .tex; README.md and read-brief.md differ ONLY by the 29/10 gate-flag correction + regeneration date/size (word-level diff in r1_out.json)'},
   'C2_review_app_logic':{'run':dry['status'],'checks':len(dry['checks']),'note':'review_app.py (copy with only B and the output path changed, so the deploy-gating file is not created): all PASS incl. 1464 plan pins/baselines, 1438 formal sources, 458 roundtrips, qualifiers, runtime preserved'},
   'C2_verify_sources_with_shim':{'equal_to_builder_sources_verified_except_checked_at':ver2==bld2,'offline':True},
   'C3_topics_and_capsules':{'core_topics':r3['core_topics'],'packages':packages,'top_level_compact_capsules_shared':r3d['shared']['top_level_capsules'],'restore_exactly':r3d['shared']['restore_exactly'],'v402_for_comparison':{'capsules':r3o['packages']['shared']['form']['top_level_capsule']},
      'note':'0 topics lost in all four packages. haiku55 and haiku_expanded restore 458/458 exactly with the reviewer decoder. In shared/sonnet_public 34 historical JSON topics omit audit keys (runtime_s, protocol_hash, frozen_hash, result_sha16, catalog_sha16, result_path, ext_*_kernel_proved booleans) by the inherited projection: a SUBSET of the 35 the accepted v402 had; none is a statute/verdict/hypothesis key. 0 status/statute/verdict leaves regressed from literal to pointer-only among 385 unchanged-source topics (r11_out.txt).'},
   'C3_windows':{'builder_equals_reviewer':True,'kimi':r5['executor_windows']['kimi'],'mimo':r5['executor_windows']['mimo'],'deepseek':r5['executor_windows']['deepseek'],'haiku_expanded_remaining_tokens':r5['native']['haiku_expanded']['remaining_recomputed'],'floor':10000,
      'shared_remaining_tokens':r5['native']['shared']['remaining_recomputed'],'sonnet_public_remaining_tokens':r5['native']['sonnet_public']['remaining_recomputed'],'jev':r5['jev'],'native_count_chain_and_zero_generations':True},
   'C3_plan':{'files':1464,'runtime_python_changes':0,'only_new_vs_v402':'5 kernel .lean (Caminho, Jo8v32, ProjecaoTransversalDaMeiaNat, VerdadeAdendo, Vida)','active_manifest_last':True},
   'C3_scripts_vs_v402':'release_cfg.py differs in BUILDER and EXPAND_OVERRIDE only; task.py in comments + unit text only; builder_measurements.py in version labels + 2 new keys; prepare/finalize/count_final_public/preflight_offline/validate_plan/codec/fit_* byte-identical; transaction/maintenance/deploy_controlled/verify_installed/verify_sources/mission_step byte-identical; native_prefix.md differs only by version parameters + the appended v404 paragraph; 3 new builder scripts (expand_candidates_dryrun.py, expand_candidates_windows.py, grep_superseded_check.py) read-only.',
   'C5_forbidden_wording':'0 unqualified new CONFIRMED/confirmada hits vs the accepted v402 (r6_out.txt); qualifiers CONDITIONAL, UNINHABITED, BIJECTION, HILBERT, CREDITATION and the gate qualifier present in shared, haiku_expanded, sonnet_public',
   'C6_secrets':'0 secret-pattern hits in 1552 files; confidential names appear only as names/paths in pipeline code and baselines (as in v402); no .env, no .pyc, no stack/psion/web_server file',
   'Policy_D_as_stated':'EXPAND_OVERRIDE=() verified; haiku_expanded rebuilt independently from the haiku55 base + the 17 regex topics + bootstrap block == built bytes; no version-suffixed topic expanded; A/B/C each exceed the Haiku55 floor with the measured ratio (r7_out.txt, builder table)',
   'Pin_to_origin_main_as_stated':'verified (C1): the 11 custody-vs-pinned differences are limited to README.md and read-brief.md',
   'v402_immutable':'0 files newer than its last accept; 22 pinned evidence hashes unchanged; production still v402 (f13abb8f4b47d194)'},
 'findings':[
  {'id':'F1','severity':'BLOCKING_BY_BRIEF','title':'bandeiras_do_gate_v403 is NOT present in full in haiku55 / haiku_expanded',
   'evidence':'Same 5.388-byte block in both: 65 of 244 source leaves inline, 6 pointer references (mechanics, values, flags, gv03, and two item-count references decisoes_da_gerencia, probe_novo). Inline in full: estatuto, scope ("18 bandeiras ... todas CALCULADAS (0 literais) ... le 15 (6+5+4)"), limites, diz, nao_diz, literais_que_viraram_calculadas, feed_v11, assinatura; verdict is an @EXPOSITION reference to the carried exposition. decoded block == sealed topic (restores exactly), so nothing is wrong or lost -- but it is not "in full".',
   'cause':'Policy D (EXPAND_OVERRIDE=()) expands no _v403/_v404 topic; bandeiras_do_gate_v403 is not among the 17 regex-expanded topics.',
   'files':['r4c_out.txt','r3e_out.txt']},
  {'id':'F2','severity':'NEEDS_MANAGEMENT_AWARENESS','title':'Policy D also collapses the P2 literal-protection window of the SHARED prefix (prepare.py l.77 ties it to the same override)',
   'evidence':'The brief describes D as affecting haiku55 only. In shared and sonnet_public the 11 topics new in v404 (caminho/vida/verdade_adendo/bandeiras/cunhagens/kh_n1_cobertura _v403; projecao_transversal/jo8v32/f2b_errata/cunhagens/kh_n1_cobertura _v404) are top-level capsules and the 8 former-window topics (_v401/_v402) lost literal carriage: limites, diz, nao_diz (and formal_theorems/mechanics/support_theorems in Haiku55) are pointer-only. estatuto/scope/verdict/hypothesis-status leaves stay literal (0 regressions). The v402 reviewer check 18 (new topics carry every qualifier literal in shared) would FAIL for v404. Kimi has no tools (ferramentas=[] in iald_app_providers), so for Kimi pointer-only means unreachable.',
   'files':['r3e_out.txt','r11_out.txt','r3d_out_v404.json','r3d_out_v402.json']},
  {'id':'F3','severity':'INFORMATIONAL_EXPECTED_ZERO_NOT_MET','title':'Old wording "15 calculadas e 3 literais" is not 0 in the four prefixes',
   'evidence':old,
   'reading':'All hits are (a) the sealed v392 record estatuto_da_prova_ressalva_v392 (verdict token; in haiku also the diz line), (b) in haiku the sealed canonical-form index line carrying that verdict token inside the exposition, (c) one literal-dictionary entry (NL8 in shared/sonnet_public, L7 in haiku) that is the v403 erratum QUOTING the old wording as true on its date, kept as record, superseded in v403 ("18 de 18 calculadas, 0 literais, 15 no veredito (6+5+4)"). No other topic, no operational core, kernel v5, native prefix, Jev contract/packet asserts it; README.md and read-brief.md at the pinned commit have 0. Outside the prefixes it remains only in sealed sources (um.py, um_absoluto.json, um_absoluto_pt.txt: 4 strict hits, 2 with a supersession marker and 2 unmarked -- the v392 chapter sentence and the verdict-token index line, forma canonica, selo). The correction is present in every prefix: bandeiras_do_gate_v403 + the dictionary entry; shared header says "correcoes atuais prevalecem". The v392 record block itself carries no local correction mark (cannot be added without altering a sealed record). Strictly an improvement on v402, which had the old wording and no correction.',
   'corrected_wording_counts_raw':{p:r4c for p,r4c in {}.items()},
   'files':['r4_out.json','r4b_out.txt','r4c_out.txt','r4d_out.txt']},
  {'id':'F4','severity':'INFORMATIONAL','title':'Margins trending down',
   'evidence':'DeepSeek full-output reserve 281.865 tok = 71.7% of the 393.216 provider max (v402: 295.217 = 75%); declared-policy slack 133.315 B (v402 146.667 B). Haiku55 remaining 28.640 tok (v402 27.136) only because nothing was expanded; the compact base grows ~63 KB per two releases (builder note) -> redesign before v406.'}],
 'decision_menu_for_management_not_a_decision_of_the_reviewer':[
   'A. Management states in writing that F1 is satisfied by "all correcting statements inline" and acknowledges F2 and F3; the reviewer then runs the original review_app.py (writes validation/review_final.json) and accepts app + sources. Every other check already PASSES.',
   'B. Rebuild with bandeiras_do_gate_v403 in full in haiku55: measured +10.615 B (~5.7k-6.4k tokens; remaining would stay ~22k-23k > floor 10.000). _v403 as a whole (+44.8 KB, ~24k tokens) and all 11 new topics (+86.1 KB, ~46k tokens) do NOT fit. Needs a selection that EXPAND_OVERRIDE (suffix-based) cannot express: a pipeline edit in finalize.py/prepare.py.',
   'C. Decouple the shared P2 window from the Haiku55 override so the 11 new topics stay literal in shared: +109.417 B in shared. Arithmetic only: Kimi slack 154.288 -> 44.871 B, MiMo 150.916 -> 41.499 B, DeepSeek declared-policy 133.315 -> 23.898 B; i.e. below the >100.000 B margin the v402 reviewer recorded for Kimi/MiMo.'],
 'reviewer_scripts_and_outputs_sha16':evid,
 'reviewer_folder':str(RV),
 'not_done':['No deploy, no maintenance, no verify_installed, no service touched, no lease claimed, no mission accept sent.','Native token counts are custody of the builder receipts (6 public count-only calls, 0 generations); the reviewer recomputed arithmetic and the intent->result->prefix chain, made no paid call.','No Lean and no um.py executed (ast.parse only in the independent haiku_expanded rebuild).']}
out['findings'][2].pop('corrected_wording_counts_raw')
with (W/'receipts/v404-review-findings.json').open('xb') as f:f.write(json.dumps(out,ensure_ascii=False,indent=2).encode())
print(hashlib.sha256((W/'receipts/v404-review-findings.json').read_bytes()).hexdigest())
