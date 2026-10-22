"""Adapt the reviewer's own isolated runner for exactly three generic auxiliaries."""
from pathlib import Path
R=Path(__file__).resolve().parent
code=(R/'run_scalar_tomita_adjoint_review.py').read_text(encoding='utf-8')
changes=[
 ('closed_tomita_batch_latest_run.txt','scalar_tomita_adjoint_latest_run.txt'),
 ("RUN=REV/('scalar_tomita_adjoint_independent_'", "RUN=REV/('resolvent_aux_independent_'"),
 ("NAMES={'AntilinearAdjointGraph':'20260912_103611_347285','ScalarTomitaAdjoint':'20260912_104146_918776'}", "NAMES={'AntilinearComposition':'20260912_104911_690291','ClosedAntilinearResolvent':'20260912_105618_331202','PositiveSurjectiveResolvent':'20260912_105619_781262'}"),
 ('len(targets)==len(set(targets))==23','len(targets)==len(set(targets))==12'),
 ('INDEPENDENT_TWO_DEV_MODULES_23_TYPES_AXIOMS','INDEPENDENT_THREE_GENERIC_AUXILIARIES_12_TYPES_AXIOMS'),
 ("write(REV/'scalar_tomita_adjoint_latest_run.txt'", "write(REV/'resolvent_aux_latest_run.txt'"),
 ('ScalarTomitaAdjointAudit','ResolventAuxAudit'),
 ('len(records)==3','len(records)==4'),
 ('exact_23_targets','exact_12_targets'),
 ('two_binaries_equal_author','three_binaries_equal_author')]
for old,new in changes:
    assert old in code,old
    code=code.replace(old,new)
p=R/'run_resolvent_aux_review.py';assert not p.exists()
raw=code.encode();tmp=p.with_suffix('.py.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(p)
print(str(p))
