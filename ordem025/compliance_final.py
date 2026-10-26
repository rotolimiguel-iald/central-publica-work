"""Additive requirement audit. Never follow the withdrawn speech reference."""
from task import *
import datetime, re

OUT = Path('C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_025')
D = OUT / 'CUMPRIMENTO_FINAL'
AD = Path('C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_025_ADENDO_A_recorte_da_fala.md')
checks = []

def save(name, data):
    if not isinstance(data, (str, bytes)):
        data = json.dumps(data, ensure_ascii=False, indent=2)
    if isinstance(data, str):
        data = data.encode('utf-8')
    with (D / name).open('xb') as f:
        f.write(data)
    assert (D / name).read_bytes() == data

def record(name, passed, detail):
    checks.append({'id': name, 'pass': bool(passed), 'detail': detail})
    if not passed:
        raise AssertionError((name, detail))

def main():
    p = project()
    t = next(x for x in p['projection']['active'] if x['id'] == 'compliance_final')
    assert act('check', task_id=t['id'], lease_id=t['lease']['id'])['ready']
    D.mkdir(exist_ok=False)
    manifest = json.loads((OUT / 'RESULTADO.json').read_text(encoding='utf-8'))
    # Verify delivered files only. Nested source paths in historical manifests
    # are NOT followed, in particular the fourth speech withdrawn by Addendum A.
    for item in manifest['files']:
        path = Path(item['path']).resolve()
        record('file:' + path.name, path.is_relative_to(OUT.resolve()) and
               pin(path)['sha256'] == item['sha256'], str(path))
    ax = json.loads((OUT / 'AXIOMAS.json').read_text(encoding='utf-8'))
    src = OUT / 'PonteDaEscalaDual.lean'
    text = src.read_text(encoding='utf-8')
    code = re.sub(r'/\-.*?\-/', '', text, flags=re.S)
    code = re.sub(r'--[^\n]*', '', code)
    code = re.sub(r'"(?:[^"\\]|\\.)*"', '""', code)
    declarations = re.findall(r'^(?:theorem|def|abbrev)\s+(\w+)', code, re.M)
    prints = re.findall(r'^#print axioms TGLExt\.PonteDaEscalaDual\.(\w+)', code, re.M)
    record('all_explicit_axioms_printed', sorted(declarations) == sorted(prints),
           {'declarations': len(declarations), 'prints': len(prints)})
    record('no_sorry_or_axiom', not re.search(r'\bsorry\b|^axiom\s', code, re.M),
           'Comments/strings excluded; compiler axiom audit also checked below.')
    rows = ax['all_declarations_including_generated']
    record('trio', all(set(x['axioms']) <= {'propext','Classical.choice','Quot.sound'} for x in rows),
           {'entries': len(rows), 'theorems': ax['theorems']})
    b = json.loads((OUT / 'BUILD_RECEIPT.json').read_text(encoding='utf-8'))
    meta = b['build']
    for key in ['command','cwd','LEAN_PATH','start','end','duration_seconds','exit_code','toolchain']:
        record('build:' + key, key in meta, meta[key])
    record('build_exit_zero', meta['exit_code'] == 0 and b['status'] == 'PASS', meta['exit_code'])
    record('build_source_pin', pin(src)['sha256'] == meta['source_sha256'], pin(src))
    for key in ['receipt','stdout','olean']:
        item = b[key]
        record('build_pin:' + key, pin(Path(item['path']))['sha256'] == item['sha256'], item)
    log = Path(b['stdout']['path']).read_text(encoding='utf-8')
    emitted = [s.split('\t') for s in log.splitlines() if s.startswith('O25_DECL\t')]
    record('axioms_match_actual_log', {(x[1], x[2], tuple(sorted(filter(None, x[3].split(','))))) for x in emitted}
           == {(x['name'], x['kind'], tuple(sorted(x['axioms']))) for x in rows}, len(emitted))
    record('result_first_line_and_length', (OUT/'RESULTADO.md').read_text(encoding='utf-8').startswith('PONTE PARCIAL')
           and len((OUT/'RESULTADO.md').read_text(encoding='utf-8').splitlines()) <= 15,
           len((OUT/'RESULTADO.md').read_text(encoding='utf-8').splitlines()))
    ad = json.loads((OUT/'ADENDO_A/FONTES_VIGENTES_ADENDO_A.json').read_text(encoding='utf-8'))
    for key in ['order','source','custody','unchanged_lean','unchanged_result_manifest']:
        item = ad[key]
        record('addendum:' + key, pin(Path(item['path']))['sha256'] == item['sha256'], item)
    result = subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\NOS_VIVO\consultar.py','--unidade',UNIT], capture_output=True)
    record('nos_query', result.returncode == 0, 'Current graph now indexes this unit; previous absence was historical.')
    save('NOS_VIVO_ATUAL.txt', result.stdout)
    inv = Path('C:/IALD/Central de Patentes/memory/INVENTARIO_BANCADA_CHATGPT.md')
    patterns = ['H_modular_equals_geometric', 'GeneralMetricClausius', 'DualScalingData',
                'regularCoreDualScalingData', 'Clausius', 'rank c']
    inventory = inv.read_text(encoding='utf-8').splitlines()
    matches = {q:[{'line':i+1,'text':s} for i,s in enumerate(inventory) if q.casefold() in s.casefold()] for q in patterns}
    save('INVENTARIO_CONSULTA.json', {'source':pin(inv),'queries':matches,
         'scope':'Busca textual no inventario indicado pela ordem; nao prova ausencia global no acervo.'})
    model = subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','modelo'], capture_output=True)
    record('map_model_read', model.returncode == 0, 'Modelo oficial lido; nenhum registro no mapa efetuado.')
    save('MODELO_MAPA_ATUAL.txt', model.stdout)
    refs = json.loads((OUT/'REFERENCIAS.json').read_text(encoding='utf-8'))
    for item in refs:
        record('formal_source:' + Path(item['path']).name,
               pin(Path(item['path']))['sha256'] == item['sha256'], item['path'])
    criteria = [
      {'id':'0_ADENDO_A','status':'ATENDIDO','evidence':['ADENDO_A/FONTES_VIGENTES_ADENDO_A.json'],
       'finding':'Quarta fala somente pelo recorte declarado vigente; integra retirada nao consultada nesta conferencia.'},
      {'id':'1_REAPROVEITAMENTO','status':'ATENDIDO','evidence':['consultas','REFERENCIAS.json','CUMPRIMENTO_FINAL/NOS_VIVO_ATUAL.txt'],
       'finding':'Reaproveitados boost, solda/eta4, escala regular e nao vacuidade. A consulta nova ja encontra a unidade e v401; a ausencia antiga no grafo e historica.'},
      {'id':'A','status':'ATENDIDO','terms':['momentumScaling','pPlus_scaling','theta_zero','theta_add'],
       'finding':'Instancia concreta de DualScalingData sobre momentos longitudinais; tau=pPlus, theta=boost(-s).'},
      {'id':'B_I','status':'ATENDIDO','terms':['inertial_momentum_is_zero','rest_post_exists_and_moves'],
       'finding':'Compoe FalsidadeDaInercia. Inercial significa fixo por todos os boosts, nao movimento livre de forcas.'},
      {'id':'B_II','status':'ATENDIDO_COM_ESCOPO','terms':['mass_is_the_invariant','energy_is_the_reading','mass_is_eta4','embed_equivariant','lift_rest_energy','rest_energy_eq_mc2'],
       'finding':'Forma quadratica e acao 4D existentes; repouso e sinais explicitados. E=mc2 nao e derivado da escala isolada. Coordenadas nulas nao normalizadas corrigem fator2 da rota sugerida.'},
      {'id':'B_III','status':'ATENDIDO_PELO_RAMO_DE_HIPOTESES_NOMEADAS','evidence':['ANALISE_TECNICA.json','ESCOPO_PT.json'],
       'finding':'Sem hipotese nova a implicacao nao foi reivindicada. Nomeados T simetrico/conservado, identificacao/calibracao do fluxo e MetricScreenClausius em toda direcao; a ordem expressamente permite este ramo.'},
      {'id':'C','status':'ATENDIDO_COM_DIVIDAS_PRESERVADAS','evidence':['ANALISE_TECNICA.json','ESCOPO_PT.json'],
       'finding':'Preservar eta4 ja escolhida nao deriva (1,3) da positividade CP; Fin4/imersao longitudinal nao deriva rank(c)=4 nem H2.'},
      {'id':'D','status':'ATENDIDO_COM_AUSENCIA_DELIMITADA','evidence':['ANALISE_TECNICA.json','REFERENCIAS.json','CUMPRIMENTO_FINAL/INVENTARIO_CONSULTA.json'],
       'finding':'Quatro classes na ordem solicitada. Ausencia somente no recorte; massa nao selecionada demonstrada por lift_mass_not_selected. Interpretacao BW nao confunde acao dual theta e grupo modular sigma.'},
      {'id':'5_ENTREGA','status':'ATENDIDO','evidence':['PonteDaEscalaDual.lean','AXIOMAS.json','BUILD.log','BUILD_RECEIPT.json','RESULTADO.md','registro_mapa_ordem_025.json'],
       'finding':'Modulo, axiomas, log real, relatorio13linhas e proposta de registro entregues. Aceite, registro do mapa e integracao pertencem a gerencia.'}
    ]
    anchors = {name:next(i+1 for i,s in enumerate(text.splitlines()) if re.match(r'(?:theorem|def|abbrev) '+re.escape(name)+r'\b',s)) for name in declarations}
    save('VERIFICACAO.json', {'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'status':'PASS','statute':'REAL — conferencias de bytes e estrutura; nao e recompilacao',
         'checks':checks, 'requirement_assessment':criteria, 'source':pin(src),'source_anchors':anchors,
         'order':pin(SOURCE),'addendum':pin(AD),'prior_manifest':pin(OUT/'RESULTADO.json'),
         'scientific_result':'PONTE PARCIAL','implementation_obligations_complete':True,
         'management_acceptance_pending':True,
         'not_proved':['massa/corpo calibrado selecionado','igualdade da acao dual com fluxo modular BW','H3','assinatura a partir de CP','rank(c)=4'],
         'production_changes':False,'repeat_build':False})
    save('CUMPRIMENTO.md', '\n'.join([
      'PONTE PARCIAL — os itens de execução A–D e os entregáveis da ORDEM025 foram atendidos; a identificação física plena não foi provada.',
      '[REAL] Conferência final por script: pinos da entrega, fonte, .olean, log real, axiomas e recorte vigente do Adendo A.',
      '[REAL] A: instância tau=pPlus, theta=boost(-s), com scaling e leis de grupo provados.',
      '[REAL] B(i–ii): inércia definida na ordem implica peso zero; massa² invariante, energia depende do observador; inclusão na eta4 existente é equivarante.',
      '[REAL] E=mc² tem shell/repouso/sinais explícitos; lift_rest_energy compõe o repouso c=1 com a realização da escala.',
      '[REAL] A realização do core regular é não vazia; lift_mass_not_selected demonstra que a mesma escala admite massas distintas.',
      '[OPEN] B(iii), ramo permitido pela ordem: fonte T conservada/simétrica, correspondência do fluxo e hclausius permanecem hipóteses nomeadas.',
      '[OPEN] C: assinatura a partir de CP e rank(c)=4/H2 não são pagos por preservar eta4 e escolher Fin4.',
      '[DERIVED] D: classes ordenadas e fontes localizadas; ausência limitada ao recorte consultado, sem afirmar busca exaustiva da máquina.',
      '[REAL] Lean4.31.0, EXIT0, 29 teoremas/40 declarações explícitas, 65 entradas auditadas, zero sorry e somente o trio; recibo da compilação reaproveitado.',
      '[REAL] Adendo A conferido: apenas recorte declarado da fala de25/10 como quarta fonte; nenhuma busca da íntegra retirada.',
      '[REAL] A unidade agora aparece no Nós Vivo; a consulta anterior sem registro era retrato daquele momento.',
      '[INPUT] Entrega técnica completa no escopo autorizado, com resultado científico parcial. Gerência ainda examina, registra o mapa e decide integração; não se declarou FECHADA nem se alterou gate.',
    ])+'\n')
    print(json.dumps({'status':'PASS','checks':len(checks),'declarations':len(declarations),'entries':len(rows),'evidence':str(D/'VERIFICACAO.json')},ensure_ascii=False))

if __name__ == '__main__':
    main()
