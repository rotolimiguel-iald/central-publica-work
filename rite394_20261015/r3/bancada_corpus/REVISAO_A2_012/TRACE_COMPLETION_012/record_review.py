from pathlib import Path
import datetime, hashlib, json, os, subprocess, uuid

ROOT = Path(__file__).resolve().parent
CHAT = ROOT.parent.parent
FICHE = CHAT/'A2_TRACE_COMPLETION_012'
BASE = CHAT/'TETELESTAI_V351_FECHO_MATEMATICO'/'RETOMADA_A1B_012'/'k'
MATH = BASE/'.lake'/'packages'/'mathlib'/'Mathlib'


def stamp():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S_%f')


def info(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=str(p.resolve()), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())


def write(p, b):
    p = Path(p)
    assert p.resolve().is_relative_to(ROOT)
    if isinstance(b, str):
        b = b.encode('utf-8')
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name+'.bak_'+stamp())
        with backup.open('xb') as f:
            f.write(old)
        assert backup.read_bytes() == old
    tmp = p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f:
        f.write(b)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.stat().st_size == len(b)
    os.replace(tmp, p)
    assert p.read_bytes() == b


def record(p, d):
    write(p, json.dumps(d, ensure_ascii=False, indent=2)+'\n')


def main():
    entries = []
    full = [(FICHE/'REAPROVEITAMENTO.md', 'ficha/REAPROVEITAMENTO.md'),
        (FICHE/'REAPROVEITAMENTO.json', 'ficha/REAPROVEITAMENTO.json'),
        (FICHE/'src/TGLExt/V354TraceShiftEquivalence.lean', 'candidates/V354TraceShiftEquivalence.lean'),
        (FICHE/'src/TGLExt/V354CyclicTraceCompletion.lean', 'candidates/V354CyclicTraceCompletion.lean'),
        (BASE/'TGLExt/V351RegularCoreTraceContract.lean', 'providers/V351RegularCoreTraceContract.lean'),
        (BASE/'TGLExt/V351RegularCoreTraceConstruction.lean', 'providers/V351RegularCoreTraceConstruction.lean'),
        (BASE/'TGLExt/V351InverseLimitTracialExtension.lean', 'providers/V351InverseLimitTracialExtension.lean')]
    for p, relative in full:
        before = info(p)
        q = ROOT/'inputs'/relative
        write(q, p.read_bytes())
        assert info(p) == before
        entries.append(dict(file=before, scope='full_text_read', copy=info(q)))
    parts = [(BASE/'TGL/ModularRealization.lean', 68, 87),
        (BASE/'TGLExt/V351QuadraticTrace.lean', 243, 251),
        (MATH/'Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Commute.lean', 185, 208),
        (MATH/'Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean', 231, 292),
        (MATH/'Analysis/Normed/Operator/Extend.lean', 310, 335)]
    for p, first, last in parts:
        b = p.read_bytes()
        chunk = b''.join(b.splitlines(keepends=True)[first-1:last])
        q = ROOT/'inputs'/'excerpts'/(p.stem+f'_{first}_{last}.txt')
        write(q, chunk)
        entries.append(dict(file=info(p), scope='specified_lines_only', first_line=first, last_line=last,
            read_excerpt_bytes=len(chunk), excerpt_sha256=hashlib.sha256(chunk).hexdigest(), copy=info(q),
            note='Full file bytes read mechanically for hash; only recorded range semantically inspected.'))
    search = subprocess.run(['rg', '-n', '-i', 'polar.?decomp|partial.?isometr|polarDecomp', str(MATH)], capture_output=True)
    write(ROOT/'polar_search_stdout.txt', search.stdout)
    write(ROOT/'polar_search_stderr.txt', search.stderr)
    search_result = dict(command=search.args, returncode=search.returncode,
        stdout=info(ROOT/'polar_search_stdout.txt'), stderr=info(ROOT/'polar_search_stderr.txt'),
        no_matches=search.returncode == 1 and not search.stdout and not search.stderr,
        meaning='Bounded text search, not proof of nonexistence under any name.')
    report = dict(created_utc=stamp(), reviewer_identity=dict(name='Carver',
        agent_id='01a0a5b5-e12d-70c1-a68a-c6f13373e3c0', provenance='INPUT from principal agent', role='independent mathematical reviewer'),
        scope='Route critique before independent code review; no Lean compilation; no reopening the paid 33 names',
        mathematical_status='DERIVED_ARGUMENT_GIVEN__POSITIVE_COMPATIBILITY_TRUE_UNDER_STATED_HYPOTHESES',
        formal_status='OPEN_NOT_INDEPENDENTLY_COMPILED', A2_complete=False, full_adendo_accepted=False,
        hypotheses=['Complex Hilbert space; bounded operators', 'p,q positive in one von Neumann algebra M',
            'r,s in that SAME M', 'n>=1 and the ShiftRelated equations', 'tau(a*a)=tau(aa*) for every a in M'],
        unnecessary_hypotheses=['finite dimension', 'finite trace', 'normality for this equality',
            'semifiniteness for this equality', 'faithfulness for this equality', 'closed range', 'invertibility'],
        key_witness='a = u sqrt(q), with u the canonical polar partial isometry of r inside M',
        alternative_without_polar=dict(status='DERIVED_ON_PAPER_NOT_COMPILED', t='r+s*', R='t*t', T='tt*',
            S_epsilon='sqrt(p) T (T+epsilon I)^-1', K_epsilon='t sqrt(R) (R+epsilon I)^-1 sqrt(q)',
            exact_identities=['K*K <= q', 'KK* = S*S'],
            norm_estimate='||S_epsilon-sqrt(p)|| <= (3/2) epsilon^(1/(2n))',
            paid_limit_supplier='scalarInverseLimitWeight_square_le_of_strong',
            source=str(BASE/'TGLExt/V351InverseLimitTracialExtension.lean'), line=46,
            bound='tau(q), including infinity', conclusion='tau(p)<=tau(q); swap endpoints for equality'),
        positive_sup_inflation=False, reason='Each nonempty set of positive readings in a ShiftRelated class is a singleton.',
        global_additivity=False, global_additivity_counterexample='M=C: F(1)=1, F(-1)=0, F(0)=0',
        counterexamples=['Polar support may be larger: p=q=e11,r=I,s=p,n=1',
            'Witnesses outside M: diagonal M, trace(a,b)=a+2b, p=e11,q=e22,r=e12,s=e21',
            'Nontracial weight inside M2: phi(A)=A11+2A22; same matrix witnesses inflate the supremum'],
        pending=[dict(priority='P1', kind='formal_obligation_not_mathematical_counterexample',
            text='Formalize positive compatibility by the internal polar or the explicit approximation route; then independently review actual interface construction.')],
        sources=entries, polar_search=search_result,
        external_sources=[dict(title='Vaughan F. R. Jones, Von Neumann Algebras (2009)',
            url='https://math.berkeley.edu/~vfr/VonNeumann2009.pdf', accessed_utc=stamp(),
            read_scope='Section 2.3 (PDF index8); Section3.4 EP8 (PDF index21), and surrounding text',
            supplied_fact='Canonical bounded polar exists; its partial isometry belongs to the same von Neumann algebra',
            whole_pdf_read=False, pdf_sha256='NOT_MEASURED_WEB_TEXT_ACCESS'),
            dict(url='https://people.math.harvard.edu/~lurie/261ynotes/lecture9.pdf', status='OPEN_TOOL_INTERNAL_ERROR_NOT_USED')],
        historical_receipts_untouched=True, canonical_integration=False)
    record(ROOT/'LEITURAS_E_PARECER.json', report)
    files = [info(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name != 'SELO_DOCUMENTAL.json']
    assert all(info(r['file']['path']) == r['file'] for r in entries)
    record(ROOT/'SELO_DOCUMENTAL.json', dict(created_utc=stamp(), type='DOCUMENTARY_REVIEW_NOT_LEAN_PROOF',
        files=files, no_Lean_compilation=True, no_A2_acceptance=True))
    assert all(info(r['path']) == r for r in files)
    print(json.dumps(dict(document=info(ROOT/'REVISAO_MATEMATICA.md'), source_count=len(entries),
        polar_search=search_result, seal=info(ROOT/'SELO_DOCUMENTAL.json')), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
