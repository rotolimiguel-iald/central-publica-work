"""Offline, conservative analysis of independently adjudicated paired observations.

No provider, corpus reader, prompt runner, dispatcher or deployment operation.
"""
import hashlib
import json
import math
from pathlib import Path

ALPHA = 0.025

def lower_bound(values, widths):
    if not values or len(values) != len(widths):
        raise ValueError('Missing or unpaired observations')
    if any(not math.isfinite(v) for v in [*values, *widths]) or any(w <= 0 for w in widths):
        raise ValueError('Invalid bounded observations')
    n = len(values)
    return sum(values)/n - math.sqrt(math.log(1/ALPHA)*sum(w*w for w in widths)/(2*n*n))

def integer(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError('Expected bounded integer count')
    return value

def arm_scores(arm, targets):
    if set(arm) != {'supported', 'unsupported', 'contradicted', 'covered', 'input_tokens'}:
        raise ValueError('Unexpected arm schema')
    s,u,c,k = (integer(arm[x]) for x in ('supported','unsupported','contradicted','covered'))
    tokens = integer(arm['input_tokens'],1)
    if k > targets or k > s:
        raise ValueError('Coverage must be backed by unique supported target claims')
    total = s+u+c
    return (s/total if total else 0, c/total if total else 0, k/targets, tokens)

def analyze(rows, expected_ids, controls, *, independent_pairs, complete):
    """Inputs are measured tokens and reviewed counts, never raw LLM grades."""
    if type(independent_pairs) is not bool or type(complete) is not bool:
        raise ValueError('Explicit run assumptions required')
    if len(expected_ids)!=36 or len(set(expected_ids))!=36:
        raise ValueError('This preregistration requires exactly 36 distinct factual IDs')
    if len(rows)!=36 or len({r['id'] for r in rows})!=36 or {r['id'] for r in rows}!=set(expected_ids):
        raise ValueError('Missing, duplicate or unexpected pair; never drop silently')
    if len(controls)!=6 or any(type(c) is not bool for c in controls):
        raise ValueError('Exactly six semantically adjudicated controls required')
    differences=[]; density=[]; widths=[]; coverage_a=[]; coverage_b=[]; contradictions_a=[]; contradictions_b=[]
    citations=0; critical=False
    for row in rows:
        if set(row)!={'id','targets','A','B','citation_valid_B','critical_error_B'}:
            raise ValueError('Unexpected pair schema')
        targets=integer(row['targets'],1)
        if type(row['citation_valid_B']) is not bool or type(row['critical_error_B']) is not bool:
            raise ValueError('Semantic review flags must be explicit booleans')
        fa,ca,ka,ta=arm_scores(row['A'],targets); fb,cb,kb,tb=arm_scores(row['B'],targets)
        differences.append(fb-fa); density.append(kb/tb-5*ka/ta); widths.append(1/tb+5/ta)
        coverage_a.append(ka); coverage_b.append(kb); contradictions_a.append(ca); contradictions_b.append(cb)
        citations += row['citation_valid_B']; critical |= row['critical_error_B']
    mean=lambda values:sum(values)/len(values)
    h1=lower_bound(differences,[2.0]*36);h2=lower_bound(density,widths)
    guards=(mean(coverage_b)>=0.9 and mean(coverage_b)>=mean(coverage_a)
            and mean(contradictions_b)<=mean(contradictions_a) and not critical
            and citations>=29 and all(controls))
    if not complete:status='INCOMPLETE'
    elif not guards:status='NOT_ADOPT'
    elif not independent_pairs or h1<=-0.05 or h2<=0:status='INCONCLUSIVE'
    else:status='MEASURED_PASS_WITH_SCOPE'
    return dict(status=status,n=36,h1_mean=mean(differences),h1_lower=h1 if independent_pairs else None,
                h2_mean=mean(density),h2_lower=h2 if independent_pairs else None,
                alpha_per_endpoint=ALPHA,coverage_A=mean(coverage_a),coverage_B=mean(coverage_b),
                citation_valid_B=citations,controls_correct=sum(controls),guards_pass=guards,
                deployment_authorized=False,independent_review_required=True)

def render_header(entries):
    """Verify explicitly supplied local source slices; render only inert metadata."""
    if not entries or len({e['source_id'] for e in entries})!=len(entries):
        raise ValueError('Missing or duplicate sources')
    metadata=[]
    for e in entries:
        if set(e)!={'source_id','path','sha256','first_line','last_line','source_statute'}:
            raise ValueError('Unexpected source schema')
        digest=e['sha256']
        if not isinstance(digest,str) or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('Full SHA-256 required')
        raw=Path(e['path']).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('Source changed')
        text=raw.decode('utf-8');lines=text.splitlines()
        first=integer(e['first_line'],1);last=integer(e['last_line'],1)
        if not first<=last<=len(lines):raise ValueError('Invalid delivered slice')
        # Exactly defined derivative bytes; source raw bytes remain independently pinned.
        delivered='\n'.join(lines[first-1:last]).encode('utf-8')
        metadata.append(dict(source_id=e['source_id'],source_sha256=digest,
                             first_line=first,last_line=last,source_statute=e['source_statute'],
                             delivered_sha256=hashlib.sha256(delivered).hexdigest(),
                             delivered_bytes=len(delivered),serialization='UTF8_LF_JOIN_NO_FINAL_LF',
                             coverage='SELECTED_LINES_ONLY',truth_verified=False))
    template=Path(__file__).with_name('HEADER_V2.txt').read_text(encoding='utf-8')
    return template.replace('{manifest_json}',json.dumps(metadata,ensure_ascii=False))

def validate_advisory(obj, eligible):
    if set(obj)!={'schema','statute','action','answer','suggested_executor','reason','evidence','uncertainties','dispatch_authorized'}:
        raise ValueError('Unexpected advisory schema')
    if obj['schema']!='iald.voice.advisory.v2' or obj['statute']!='DECLARADO' or obj['dispatch_authorized'] is not False:
        raise ValueError('Invalid identity or attempted authorization')
    if obj['action'] not in ('answer','suggest','refuse','needs_evidence'):
        raise ValueError('Invalid action')
    if obj['suggested_executor'] is not None and obj['suggested_executor'] not in eligible:
        raise ValueError('Executor is not currently eligible')
    if any(not isinstance(obj[k],str) for k in ('answer','reason')) or not obj['reason'].strip():
        raise ValueError('Text and explicit reason required')
    if any(not isinstance(obj[k],list) or any(not isinstance(x,str) for x in obj[k]) for k in ('evidence','uncertainties')):
        raise ValueError('Expected reference/uncertainty lists')
    return dict(valid=True,dispatch_authorized=False,semantic_review_required=True)
