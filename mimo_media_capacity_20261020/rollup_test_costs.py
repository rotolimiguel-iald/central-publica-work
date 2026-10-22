"""Recount exact receipt values. Estimates remain estimates, never invoices."""
from pathlib import Path
from decimal import Decimal
import json,hashlib
W=Path(__file__).resolve().parent
paths=dict(previous=W.parent/'mimo26_upgrade_20261020/live_stage/FOUR_CALLS_COST.json',
           refused_route=W/'host_followup/DIAGNOSIS_FIX_RECEIPT.json',
           manual_audio=W/'live_stage/MANUAL_AUDIO_RESULT.json',
           manual_video=W/'live_stage/MANUAL_VIDEO_RESULT.json')
d={k:json.loads(p.read_bytes(),parse_float=Decimal) for k,p in paths.items()}
amounts=dict(previous=Decimal(d['previous']['known_cost_estimate_usd']),
 refused_route=d['refused_route']['actual_dispatch_evidence']['estimated_JEV_cost_usd'],
 manual_audio=d['manual_audio']['known_cost_estimate_usd'],
 manual_video=Decimal(d['manual_video']['video_debit_usd']))
total=sum(amounts.values(),Decimal(0))
value=dict(status='RECOUNTED_KNOWN_AND_PESSIMISTIC_ESTIMATES',
 values_usd={k:str(v) for k,v in amounts.items()},
 combined_total_estimate_usd=str(total),current_mission_estimate_usd=str(total-amounts['previous']),
 internal_combined_ceiling_usd='1.00',remaining_combined_estimate_usd=str(Decimal(1)-total),
 scope='Prior4 test receipts plus current3 jobs; video debit is pessimistic reserved cap, not measured vendor usage. No invoice or moderation overhead reconciliation.',
 additional_test_authorization='PENDING_USER_REPLY_NO_NEW_PAID_TEST',
 sources={k:dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for k,p in paths.items()})
with (W/'live_stage/TEST_COST_ROLLUP_R1.json').open('xb') as f:
    f.write(json.dumps(value,ensure_ascii=False,indent=2).encode())
print(str(total))
