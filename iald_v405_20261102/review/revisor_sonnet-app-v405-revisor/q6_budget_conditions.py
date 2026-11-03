"""Reviewer Q6: re-evaluate the runtime budget conditions of R/claude_profiles.py and R/claude_context_snapshot.py on the three v405 packages (read-only import of R).
Conditions replicated from snapshot_from_manifest: memory_target <= permanent <= reference; output == default_output; margin == 1024; remaining == WINDOW - reference - output - margin; remaining >= 10000;
ready/fits/memory_target_met True. Also recomputes context_budget() from the three counts and compares it to the pinned budget dict, and shows the installed (v404) values for comparison.
Also re-derives the finalize.py estimate to show what max(0, growth) does here."""
import json, os, sys, hashlib
from pathlib import Path
sys.dont_write_bytecode = True
R = Path(r'C:\IALD\projetos_pyhton\IALD')
W = Path(r'C:\IALD\Central de Patentes\work\iald_v405_20261102')
sys.path.insert(0, str(R))
import claude_profiles as cp
import claude_context_snapshot as cs

rd = lambda p: json.loads(Path(p).read_bytes())
out = {'HAIKU_profile': {'window': cp.HAIKU.window, 'memory_target': cp.HAIKU.memory_target, 'default_output': cp.HAIKU.default_output}, 'packages': {}}
for pkg, inst in (('haiku_expanded', 'haiku55'), ('shared', 'haiku'), ('sonnet_public', None)):
    nc = rd(W / 'app/packages' / pkg / 'native_count.json')
    b = nc['budget']
    man = rd(W / 'app/packages' / pkg / 'manifest.json')
    prof = cp.SONNET if pkg == 'sonnet_public' else cp.HAIKU
    recomputed = cp.context_budget(prof.model, counted_model=prof.model, permanent_tokens=b['permanent_tokens'], request_input_tokens=b['request_input_tokens'],
                                   reserved_output_tokens=b['reserved_output_tokens'], margin_tokens=b['margin_tokens'])
    row = {'budget_pinned': b, 'context_budget_recomputed_equal_to_pinned': recomputed == b, 'manifest_budget_equal_to_native_count_budget': man['budget'] == b}
    if pkg != 'sonnet_public':
        perm, ref, out_t, margin, rem = (b[k] for k in ('permanent_tokens', 'request_input_tokens', 'reserved_output_tokens', 'margin_tokens', 'remaining_tokens'))
        cond = {
            'memory_target <= permanent <= reference': cp.HAIKU.memory_target <= perm <= ref,
            'output == default_output': out_t == cp.HAIKU.default_output,
            'margin == 1024': margin == 1024,
            'remaining == WINDOW - reference - output - margin': rem == cs.WINDOW - ref - out_t - margin,
            'remaining >= 10000': rem >= 10000,
            'ready/fits/memory_target_met True': b['ready'] is True and b['fits'] is True and b['memory_target_met'] is True,
        }
        row['snapshot_conditions'] = cond
        row['snapshot_conditions_all_true'] = all(cond.values())
        row['permanent_vs_memory_target_margin'] = perm - cp.HAIKU.memory_target
        io = rd(R / '.iald_runtime' / inst / 'native_count.json')['budget']
        row['installed_v404'] = {'permanent': io['permanent_tokens'], 'request_input': io['request_input_tokens'], 'remaining': io['remaining_tokens']}
        row['permanent_smaller_than_installed'] = perm < io['permanent_tokens']
        row['permanent_delta_vs_installed'] = perm - io['permanent_tokens']
    out['packages'][pkg] = row
# finalize.py estimate (max(0, growth)) re-derived
anchor = rd(R / '.iald_runtime/haiku55/native_count.json')['budget']
anchor_bytes = (R / '.iald_runtime/haiku55/prefix.md').stat().st_size
exp_bytes = (W / 'app/packages/haiku_expanded/prefix.md').stat().st_size
growth = exp_bytes - anchor_bytes
est_tokens = anchor['permanent_tokens'] + max(0, growth) * 0.60
est_rem = cp.HAIKU.window - cp.HAIKU.default_output - 1024 - (anchor['request_input_tokens'] - anchor['permanent_tokens']) - int(est_tokens)
pb = rd(W / 'app/PREPARED_BINDING.json')
out['finalize_estimate'] = {'anchor_permanent': anchor['permanent_tokens'], 'anchor_bytes': anchor_bytes, 'expanded_bytes': exp_bytes, 'growth_bytes': growth, 'max(0,growth)': max(0, growth), 'estimated_tokens': est_tokens,
                            'estimated_remaining': est_rem, 'PREPARED_BINDING.estimated_remaining_haiku55': pb['estimated_remaining_haiku55'],
                            'native_remaining': rd(W / 'app/packages/haiku_expanded/native_count.json')['budget']['remaining_tokens'],
                            'reading': 'growth is negative (package SHRANK vs the installed anchor), so max(0, growth) = 0 and the estimate degenerates to the anchor (conservative: it overstates tokens, understates remaining); the 15000-token stop in finalize.py cannot trigger on a shrinking package; the native count is the only measure of the real remaining.'}
print(json.dumps(out, ensure_ascii=False, indent=1))
