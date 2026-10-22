from pathlib import Path
import difflib, hashlib, json

ROOT = Path(__file__).resolve().parent

def replace(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)

policy = (ROOT/'baseline/iald_task_policy.py').read_text(encoding='utf-8')
policy = replace(policy, "'Arquitetura e revisão pelo Sonnet quando permitido; implementação delegada e execução verificada.'", "'Kimi primeiro para rascunhos de código; MiMo gere ferramentas e execução verificada.'")
insert = '''# Temporary operator policy, 2026-10-14. This orders only host-admitted
# candidates; it cannot grant consent, budget, availability or tools.
AUTOMATIC_PREFERENCE_VERSION = 'preserve_claude_20261014'
AUTOMATIC_ORDER = ('kimi', 'mimo', 'openai', 'deepseek', 'nativa')


def automatic_candidates(candidates):
    """Claude is manual-only during preservation; never add a destination."""
    model_identities(list(candidates))  # Reject unknown names, not silently allow.
    return [key for key in AUTOMATIC_ORDER if key in candidates]


def preferred_executor(candidates):
    ordered = automatic_candidates(candidates)
    if not ordered:
        raise ValueError('No authorized capable non-Claude executor')
    return ordered[0]


'''
policy = replace(policy, 'def tool_managers(candidates):', insert + 'def tool_managers(candidates):')
policy = replace(policy, "Operator preference: code architect/reviewer. Prefer as manager for nontrivial code; delegate bulk implementation to a cheaper eligible worker. This is a preference, not measured superiority.", "Manual operator selection only during Claude preservation; never an automatic executor.")
policy = replace(policy, 'nem chame todos os modelos. Sonnet como gestor é preferência do operador, não benchmark.', 'nem chame todos os modelos. Priorize Kimi para rascunhos de código quando elegível;\nMiMo gere ferramentas. Claude fica reservado à escolha manual do operador.')
policy = replace(policy, "'policy_version':3", "'policy_version':4")
policy = replace(policy, "'claude-sonnet':'code architecture/review, owner only'", "'claude-sonnet':'manual operator choice only during preservation'")
router = (ROOT/'baseline/iald_auto_router.py').read_text(encoding='utf-8')
router = replace(router, "('mimo' if 'mimo' in candidates else 'openai' if 'openai' in candidates else None)", "task_policy.preferred_executor(candidates)")
router = replace(router, "    mod=backend()\n    if mod.availability()", "    candidates=task_policy.automatic_candidates(candidates)\n    if not candidates:raise ValueError('No authorized capable non-Claude executor')\n    mod=backend()\n    if mod.availability()")
router = replace(router, 'Consider Haiku 5.5 for full-memory TGL answers and economical tool workflows, MiMo for detailed derivations and implementation, and Sonnet only for operator-authorized complex review.', 'The host enforces Kimi then MiMo among capable authorized candidates; Kimi is preferred for text/code drafts, MiMo for tool workflows. Claude is excluded from automatic routing during preservation.')
router = replace(router, "        current=jev_control.contract_state(jev_control.load_contract(root))", """        # Apply the operator order AFTER capability projection. A JEV answer
        # never overrides consent/budget, adds a candidate or causes a retry.
        preferred_pool=(task_policy.tool_managers(candidates)
            if not worker and decision['work_path']!='answer' else candidates)
        preferred=task_policy.preferred_executor(preferred_pool)
        record['operator_preference']={'version':task_policy.AUTOMATIC_PREFERENCE_VERSION,
            'before':chosen,'selected':preferred,'eligible':preferred_pool,
            'basis':'operator_order_not_quality_benchmark'}
        chosen=preferred
        details['jev_decision_rule']=details['decision_rule']
        details['decision_rule']='operator_preference_before_dispatch'
        current=jev_control.contract_state(jev_control.load_contract(root))""")
guide = (ROOT/'baseline/iald_execution_guide.py').read_text(encoding='utf-8')
guide = replace(guide, "VERSION = '2026-10-07.1'", "VERSION = '2026-10-14.routing'")
guide = replace(guide, 'Use the authorized Claude manager for architecture/review when appropriate.', 'Prefer Kimi for authorized text/code drafts; MiMo manages required tools. Claude is manual operator choice only during preservation.')
guide = replace(guide, 'Default candidate for coherent TGL exposition, normal code and tool workflows. Preserve complete fixed public memory.', 'Manual operator choice only during preservation. Preserve complete fixed public memory.')
guide = replace(guide, 'When luiz has access and complex code merits it, specify interfaces and tests; delegate bounded implementation and review the complete draft.', 'Only when luiz manually selects this model; specify interfaces and tests, then review bounded drafts.')
outputs = [('iald_task_policy.py',policy),('iald_auto_router.py',router),('iald_execution_guide.py',guide)]
for name, text in outputs:
    original = (ROOT/'baseline'/name).read_bytes()
    data = text.replace('\n','\r\n').encode('utf-8') if b'\r\n' in original else text.encode('utf-8')
    (ROOT/'patched'/name).write_bytes(data)
    compile(data, name, 'exec')
diff = ''.join(''.join(difflib.unified_diff((ROOT/'baseline'/n).read_text(encoding='utf-8').splitlines(True),
    (ROOT/'patched'/n).read_text(encoding='utf-8').splitlines(True),fromfile='a/'+n,tofile='b/'+n))
    for n, _ in outputs)
(ROOT/'routing.patch').write_text(diff,encoding='utf-8')
print('Built three modules; syntax valid; baseline preserved.')
