from pathlib import Path
import ast, datetime, difflib, hashlib, json, os

root = Path(__file__).resolve().parent
def put(name, value):
    p = root/name; assert not p.exists()
    b = value.encode('utf8') if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2).encode('utf8')
    t = p.with_name(p.name+'.tmp'); t.write_bytes(b); assert t.read_bytes()==b; os.replace(t,p)
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

before = (root/'CANONICAL_READERS_SNAPSHOT.py').read_text(encoding='utf8')
tree = ast.parse(before)
prefix = 'TGLV354.TraceCompletion.'
frontier = {
    'unconditional_continuous_corner_proved': prefix+'regularLegacyThreeLocks',
    'continuous_modular_realization_constructed': prefix+'regularModularRealization',
    'full_TGL_witness_constructed': prefix+'regularFullWitness'}
price = {'H1_internal_susy_relative_gap_discharged': 'TGLV354.regularSusyData'}
contracts = {
    'qgf_unconditional_continuous_corner_proved': (
        prefix+'regularLegacyCore', prefix+'regularLegacyThreeLocks',
        prefix+'cyclicTraceCandidate_positive', prefix+'regularLegacyThreeLocks_concrete'),
    'qgf_continuous_modular_realization_constructed': (
        prefix+'regularModularRealization', prefix+'regularLegacyCore',
        prefix+'regularLegacyThreeLocks', prefix+'cyclicTraceCandidate_positive'),
    'qgf_full_TGL_witness_constructed': (
        prefix+'regularFullWitness', prefix+'regularModularRealization',
        prefix+'regularLegacyThreeLocks_concrete'),
    'gpf_H1_internal_susy_relative_gap_discharged': (
        'TGLV354.regularSusyData', 'TGLV354.regularSusy_gives_breuer',
        'TGLV354.regularSusy_operator_identifications',
        'TGLV354.coreProjectionTraceSubadditive')}
replacements = {}
for node in tree.body:
    if isinstance(node,ast.Assign) and isinstance(node.targets[0],ast.Name):
        name=node.targets[0].id
        update={'_QG_FRONTIER_FLAGS':frontier,'_GRAVITY_PRICE_FLAGS':price,'_V350_MODULAR_CONTRACTS':contracts}.get(name)
        if update:
            values=ast.literal_eval(node.value); values.update(update)
            # Direct references to the exact existing terms: no new Lean aliases.
            replacements[name]=name+' = '+repr(values)
    if isinstance(node,ast.FunctionDef):
        body=ast.get_source_segment(before,node)
        if node.name=='verify_v350_modular_provenance':
            body=body.replace('Require a successful build/audit and BOTH the term and its exact-type bridge.',
                'Require successful build/audit and every named supplier. Audit also checks the exact A2 types.')
        if node.name=='finalize_v350_modular_frontier':
            body=body.replace('A name alone cannot light any of the three newly constructed targets.',
                'Read the typed modular and minimal continuous contracts; missing proof stays false.')
            body=body.replace('"PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT"',
                '"PRODUCT_TOWER__JMJ__REGULAR_CORE_MINIMAL_LOCK"')
        if node.name=='evaluate_v350_kernel_frontier':
            body='''def evaluate_v350_kernel_frontier(kernel):
    """Keep modular, minimal continuous and SUSY scopes separately measured."""
    proofs = verify_v350_modular_provenance(kernel)
    modular = all(proofs.get(k) is True for k in (
        "red_clause_JMJ_contains", "qgf_modular_realization_constructed",
        "gpf_tower_act_III_inhabitant_constructed"))
    continuous = all(proofs.get(k) is True for k in (
        "qgf_unconditional_continuous_corner_proved",
        "qgf_continuous_modular_realization_constructed",
        "qgf_full_TGL_witness_constructed"))
    susy = proofs.get("gpf_H1_internal_susy_relative_gap_discharged") is True
    remaining = [
        "H2_smooth_modular_four_frame_and_geometric_identification",
        "H3_area_heat_equilibrium_on_the_same_physical_horizon",
        "interacting_quantum_state_BRST_QME_anomalies_and_UV_scope"]
    if not continuous:
        remaining.insert(0, "continuous_core_and_finite_Three_Locks_corner_on_same_realization")
    if not susy:
        remaining.insert(0, "H1_relative_gap_beyond_finite_face")
    return {
        "verification": "LEAN_EXACT_TYPE_CHECKS_AND_AXIOM_WHITELIST",
        "modular_duality_constructed": modular,
        "continuous_minimal_realization_constructed": continuous,
        "susy_minimal_representative_constructed": susy,
        "proofs": proofs,
        "scope": "PRODUCT_TOWER__JMJ__REGULAR_CORE_MINIMAL_LOCK",
        "remaining": remaining,
        "physical_identifications_open": [
            "microscopic_origin_of_Hmin_and_standard_bounded_transform",
            "geometric_BW_identification_for_legacy_wedge_data_U_equals_one"],
        "verdict": (
            "CONTINUOUS_MINIMAL_REALIZATION_AND_SUSY_CONSTRUCTED__PHYSICAL_IDENTIFICATIONS_OPEN"
            if modular and continuous and susy else
            "MODULAR_DUALITY_CONSTRUCTED__REMAINING_SCOPES_REPORTED"
            if modular else "MODULAR_DUALITY_OPEN"),
        "legacy_gate_changed": False,
        "full_plan_complete": False,
    }
'''
        replacements[node.name]=body
parts=[]
for node in tree.body:
    name=node.name if isinstance(node,ast.FunctionDef) else node.targets[0].id
    parts.append(replacements.get(name,ast.get_source_segment(before,node)))
after='\n\n'.join(parts)+'\n'
new_tree=ast.parse(after)
old_funcs={n.name for n in tree.body if isinstance(n,ast.FunctionDef)}
new_funcs={n.name for n in new_tree.body if isinstance(n,ast.FunctionDef)}
assert old_funcs==new_funcs
candidate=put('PROPOSTA_LEITORES_EXISTENTES.py',after)
diff=put('PROPOSTA_LEITORES_EXISTENTES.diff',''.join(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='CANONICAL_READERS_SNAPSHOT.py',tofile='PROPOSTA_LEITORES_EXISTENTES.py')))
put('PROPOSTA_MAPA_CONSUMIDORES.json',{
    'timestamp':datetime.datetime.now().astimezone().isoformat(),
    'status':'PROPOSAL_IN_COPY_NOT_CANONICALLY_INTEGRATED',
    'frontier_updates':frontier,'price_updates':price,'typed_contracts':contracts,
    'no_new_python_function_names':old_funcs==new_funcs,
    'new_lean_aliases':0,
    'required_audit':'Add the checked type ascriptions in AuditReaderContracts012.lean to the existing canonical audit; retain source/hash verification.',
    'candidate':candidate,'diff':diff,
    'existing_checks_replacements':[
        {'canonical_line':160146,'old':'and not kf.get("qgf_full_TGL_witness_constructed")',
         'new':'and v350_frontier_flag_has_proof(kf, "qgf_full_TGL_witness_constructed")',
         'text':'The finite Bell identification remains absent; any independent FullTGLWitness flag requires its own checked proof.'},
        {'canonical_line':160198,'old':'bool(not kf.get("qgf_continuous_modular_realization_constructed"))',
         'new':'bool(v350_frontier_flag_has_proof(kf, "qgf_continuous_modular_realization_constructed"))',
         'text':'The continuous flag requires the same-core A1/A2 typed realization; this finite-level module alone does not supply it.'}],
    'limits':['Parser tests are integration unit tests, not a full um.py run.',
              'H1 means concrete bounded minimal SusyRelativeData, not microscopic H1.',
              'Preserve FullStaticWitness obstruction, H2/H3/physical gates and experiment separation.']})
print(json.dumps({'proposal':candidate,'new_functions':len(new_funcs-old_funcs)}))
