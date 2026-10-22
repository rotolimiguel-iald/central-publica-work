"""Read-only analysis of the validated program; write only new handoff artifacts."""
from pathlib import Path
import ast
import collections
import difflib
import hashlib
import json
import math
from datetime import datetime
from statistics import NormalDist

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'HANDOFF_SESSAO_UM_20260913'
OUT.mkdir(exist_ok=True)

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def write_new(name, content):
    target = OUT / name
    assert not target.exists(), target
    payload = content.encode('utf-8')
    temporary = target.with_name(target.name + '.tmp')
    with temporary.open('xb') as stream:
        stream.write(payload)
    assert temporary.stat().st_size == len(payload) > 0
    temporary.replace(target)
    assert target.read_bytes() == payload

def load_program(path):
    source = path.read_text(encoding='utf-8-sig')
    tree = ast.parse(source)
    assignments = {}
    functions = collections.defaultdict(list)
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignments[target.id] = node
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            functions[node.name].append(node)
    embedded = ast.literal_eval(assignments['_EMBEDDED_KERNEL_FILES'].value)
    return source, tree, assignments, functions, embedded

base_path = ROOT / 'fontes/um_v350_original.py'
final_path = ROOT / 'r/um.py'
base, bt, ba, bf, be = load_program(base_path)
final, ft, fa, ff, fe = load_program(final_path)
base_result = json.loads((ROOT/'fontes/um_absoluto.json').read_bytes())
final_result = json.loads((ROOT/'r/um_absoluto.json').read_bytes())
seal = json.loads((ROOT/'r/um_absoluto_selo.json').read_bytes())
proof = json.loads((ROOT/'r/tgl_kernel_proof_manifest.json').read_bytes())
integration = json.loads((ROOT/'integration.json').read_bytes())

files=[]
for name in sorted(set(be)|set(fe)):
    old, new = be.get(name), fe.get(name)
    status = 'added' if old is None else 'removed' if new is None else 'modified' if old != new else 'unchanged'
    path = ROOT/'r/tgl_kernel'/name
    if new is not None:
        actual_hash = sha(path)
        assert actual_hash == proof['formal_files_sha256'][name]
        assert path.read_text(encoding='utf-8-sig').replace('\r\n','\n') == new.replace('\r\n','\n')
    else:
        actual_hash = None
    if status != 'unchanged':
        import re
        declarations = [dict(kind=m.group(1),name=m.group(2)) for m in re.finditer(
            r'^\s*(?:noncomputable\s+)?(?:private\s+)?(theorem|lemma|def|structure|class|abbrev)\s+(\S+)',new or '', re.M)]
        files.append(dict(name=name,status=status,materialized_path=str(path),sha256=actual_hash,
                          embedded_text_sha256=hashlib.sha256((new or '').encode()).hexdigest(),
                          declarations=declarations))
assert {x['name'] for x in files if x['status']=='added'} == set(integration['added_kernel_files'])
assert {x['name'] for x in files if x['status']=='modified'} == set(integration['updated_kernel_files'])

def signature(nodes):
    return [ast.dump(n, include_attributes=False) for n in nodes]

function_changes=[]
patch=[]
for name in sorted(set(bf)|set(ff)):
    old, new = bf.get(name,[]), ff.get(name,[])
    if signature(old) == signature(new):
        continue
    status = 'added' if not old else 'removed' if not new else 'modified'
    old_text='\n\n'.join(ast.get_source_segment(base,n) for n in old)
    new_text='\n\n'.join(ast.get_source_segment(final,n) for n in new)
    function_changes.append(dict(name=name,status=status,base_lines=[n.lineno for n in old],final_lines=[n.lineno for n in new],
                                 final_ast_sha256=hashlib.sha256(repr(signature(new)).encode()).hexdigest()))
    patch.extend(difflib.unified_diff(old_text.splitlines(True),new_text.splitlines(True),
        fromfile=f'base::{name}',tofile=f'final::{name}',n=4))
    patch.append('\n')
write_new('FUNCOES_PYTHON.diff',''.join(patch))

assignment_changes=[]
for name in sorted(set(ba)|set(fa)):
    old,new=ba.get(name),fa.get(name)
    if old and new and ast.dump(old,include_attributes=False)==ast.dump(new,include_attributes=False):
        continue
    assignment_changes.append(dict(name=name,status='added' if old is None else 'removed' if new is None else 'modified',
                                   base_line=old.lineno if old else None,final_line=new.lineno if new else None))

excluded=(ast.Assign,ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)
other_base=[n for n in bt.body if not isinstance(n,excluded)]
other_final=[n for n in ft.body if not isinstance(n,excluded)]
other_changes=[]
matcher=difflib.SequenceMatcher(a=signature(other_base),b=signature(other_final),autojunk=False)
for tag,i,j,k,l in matcher.get_opcodes():
    if tag != 'equal':
        other_changes.append(dict(operation=tag,
            before=[dict(line=n.lineno,source=ast.get_source_segment(base,n)) for n in other_base[i:j]],
            after=[dict(line=n.lineno,source=ast.get_source_segment(final,n)) for n in other_final[k:l]]))

bc=base_result['core']; fc=final_result['core']; bk=bc['kernel_formalization']; fk=fc['kernel_formalization']
flags={k:dict(before=bk.get(k),after=fk.get(k)) for k in fk if k.startswith(('qgc_','qgp_'))}
modular={k:dict(before=bk.get(k),after=fk.get(k)) for k in ['red_clause_JMJ_contains','qgf_modular_realization_constructed','gpf_tower_act_III_inhabitant_constructed']}
assert len(flags)==11 and all(v=={'before':True,'after':True} for v in flags.values())
assert all(v=={'before':False,'after':True} for v in modular.values())
assert sha(final_path)==seal['sha256']['um.py']
records=[]
for p in sorted(ROOT.glob('*.md')):
    if '.bak_' not in p.name:
        records.append(dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)))

inv=dict(timestamp=datetime.now().astimezone().isoformat(),
    scope='Documentation and portability inventory; no program executed or modified',
    baseline=dict(path=str(base_path),bytes=base_path.stat().st_size,sha256=sha(base_path)),
    final=dict(path=str(final_path),bytes=final_path.stat().st_size,sha256=sha(final_path)),
    embedded_counts=dict(before=len(be),after=len(fe),changed=len(files),by_status=dict(collections.Counter(x['status'] for x in files))),
    kernel_files=files,python_symbols=function_changes,python_assignments=assignment_changes,
    other_top_level_changes=other_changes,
    principal_flags=flags,modular_flags=modular,
    gate=dict(before=bc['qg_closure']['gate']['verdict'],after=fc['qg_closure']['gate']['verdict']),
    readers={k:dict(before={n:bc[k].get(n) for n in ['all_verified','clauses_proved','clauses_total','flag_lit','n_atlas','n_indice']},
                    after={n:fc[k].get(n) for n in ['all_verified','clauses_proved','clauses_total','flag_lit','n_atlas','n_indice']})
             for k in ['the_assembly_and_the_single_debt','the_atlas_and_the_index']},
    historical_checks_updated=integration['historical_checks_updated'],
    restored_inputs=json.loads((ROOT/'r/reader_integration_manifest.json').read_bytes()),
    not_sealed=seal['not_sealed_this_run'],reports=records,
    scope_note='AST difference is syntactic, not proof of semantic equivalence. Declaration lists are lexical navigation aids, not audited theorem counts.')
write_new('INVENTARIO_PORTABILIDADE.json',json.dumps(inv,ensure_ascii=False,indent=2)+'\n')

lines=['# Inventário integral dos fontes formais a transportar\n',
       '[REAL — comparação AST dos dicionários embutidos e hashes dos 922 arquivos materializados.]\n',
       f"Base: {len(be)} arquivos; final: {len(fe)}; {len(files)} alterados/acrescentados. A contagem inclui raízes/configurações, não só módulos.\n",
       'Os nomes de declarações abaixo servem para navegação; não substituem os tipos e a auditoria.\n',
       '| Arquivo | Estado | Primeiras declarações | SHA-256 materializado |\n|---|---|---|---|\n']
for item in files:
    names=', '.join(d['name'] for d in item['declarations'][:3])
    lines.append(f"| [{item['name']}](<{Path(item['materialized_path']).as_posix()}>) | {item['status']} | `{names}` | `{item['sha256']}` |\n")
write_new('FONTES_FORMAIS.md','\n'.join(lines))
lines=['# Mudanças Python entre a v350 original e a cópia final\n',
       'Comparação AST sem importação/execução. `FUNCOES_PYTHON.diff` é diff por símbolo para revisão, não patch de aplicação automática.\n',
       '| Símbolo | Estado | Linha na base | Linha final |\n|---|---|---|---|\n']
for item in function_changes:
    lines.append(f"| `{item['name']}` | {item['status']} | {item['base_lines']} | {item['final_lines']} |\n")
lines.append('\n## Atribuições de topo alteradas\n\n')
for item in assignment_changes:
    lines.append(f"- `{item['name']}`: {item['status']}; base {item['base_line']}, final {item['final_line']}.\n")
write_new('MUDANCAS_PYTHON.md','\n'.join(lines))

rd=fc['ringdown_dephasing_result_v2']['stacks']['3.0']
amplitude=abs(rd['delta_pred_B']); sigma=rd['sigma']; sep=amplitude/sigma
projections=dict(source='core.ringdown_dephasing_result_v2.stacks[3.0]',
    delta_observed=rd['delta_tau'],sigma_reported=sigma,delta_branch_B=rd['delta_pred_B'],
    expected_separation=sep,required_sigma_median_5sigma=amplitude/5,
    ideal_information_multiplier=(5/sep)**2,
    required_sigma_90pct_power=amplitude/(5+NormalDist().inv_cdf(.9)),
    ideal_information_multiplier_90pct=((5+NormalDist().inv_cdf(.9))/sep)**2,
    current_bias_relative=rd['mean_bias_rel'],
    interpretation='Gaussian planning approximation, not a new experiment or validated forecast. Assumes fixed branch and signal, unbiased identifiable estimator, known covariance and no systematic floor. Multiply information, not raw detector-series count. Real V2 fails systematics.')
experimental=dict(timestamp=inv['timestamp'],projections=projections,
    local_results={k:fc[k] for k in ['ringdown_dephasing_result_v2','neutrino_m2','void_density_v41','d1_camb_result_v2']},
    source_sha256=sha(ROOT/'r/um_absoluto.json'),
    sources=[
      'https://pdg.lbl.gov/2025/reviews/rpp2025-rev-statistics.pdf',
      'https://arxiv.org/abs/1007.1727',
      'https://gwosc.org/GWTC-5.0/',
      'https://dcc.ligo.org/LIGO-P2500461/public',
      'https://arxiv.org/abs/2511.14593'])
write_new('EVIDENCIA_E_PROJECAO_EXPERIMENTAL.json',json.dumps(experimental,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(out=str(OUT),kernel=inv['embedded_counts'],
    python_counts=dict(collections.Counter(x['status'] for x in function_changes)),
    changed_python=[x['name'] for x in function_changes],assignment_changes=assignment_changes,projections=projections),ensure_ascii=False,indent=2))
