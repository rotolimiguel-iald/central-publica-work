"""Adapt the audited budget-accounted single-call evaluator to this staged context."""
from pathlib import Path
WORK=Path(__file__).resolve().parent
text=(WORK.parent/'iald_tgl_cluster_20260919/probe_cluster.py').read_text(encoding='utf-8')
text=text.replace('"""Prepared one-call evaluation. Requires a recorded explicit user approval."""',
                  '"""Single-call regression evaluation within the existing app budget."""')
text=text.replace("approval = {'max_test_usd': 0.50}","test_limit = {'max_test_usd': 0.50}")
text=text.replace("approval['max_test_usd']","test_limit['max_test_usd']")
old="""    manifest = json.loads((WORK/'manifest_staged.json').read_bytes())
    prep = json.loads((WORK/'prepared.json').read_bytes())
    catalog = kernel.KernelCatalog(prep['kernel'])"""
new="""    manifest = json.loads((ROOT/'iald_nucleo_fixo.json').read_bytes())
    cluster=manifest['active_cluster']
    catalog = kernel.KernelCatalog(cluster['kernel_bundle'],cluster['kernel_verification'])"""
assert old in text;text=text.replace(old,new)
text=text.replace("nucleus_manifest=WORK/'manifest_staged.json'","nucleus_manifest=ROOT/'iald_nucleo_fixo.json'")
start=text.index('    question = (');end=text.index('    messages, _',start)
text=text[:start]+'''    question = ('O índice de trabalho menciona v369. Qual versão do um.py está efetivamente carregada em você? '
        'Depois resolva o problema da gravidade quântica pela TGL: quero a articulação matemática da solução, '
        'não um pedido de confirmação experimental. Em até 700 palavras, ligue os objetos/hipóteses, '
        'lagrangiana, equação mestra, dephasing, Hamiltoniano limitado inferiormente e as testemunhas H1/H2/H3 '
        'à reconstrução geométrica. Preserve o alcance exato das provas e localize alguma lacuna específica '
        'se realmente existir. Use a memória ativa, sem ferramentas; não invente fórmulas nem provas.')
'''+text[end:]
text=text.replace('iald-v368-cluster-evaluation','iald-solution-contract-evaluation')
with (WORK/'probe.py').open('xb') as out:out.write(text.encode())
print('Single-call probe prepared with budget reservation; no private Atlas is sent.')
