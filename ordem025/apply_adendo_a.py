"""Register the authorized source substitution; do not access the withdrawn source."""
from task import *
AD=Path('C:/IALD/Central de Patentes/Chatgpt/TUNEL/PARA_CHATGPT/ORDEM_025_ADENDO_A_recorte_da_fala.md')
REC=Path('C:/IALD/Central de Patentes/work/cunhagens_13out/OPERADOR_25out_derivacao_inercia_gravitacao_impressao_do_um_RECORTE_verbatim.txt')
OUT=Path('C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_025')
D=OUT/'ADENDO_A'
expected='e26364c5c805734c27897a89bb80f257859da10eaa7f848fe083d9304846b6c0'
assert pin(REC)['sha256']==expected
pins=[pin(AD),pin(REC)]
new('ADENDO_A_EXTEND.json',act('extend',requirements=[{'id':'source_addendum_a',
    'criterion':'Registrar o recorte declarado da fala de 25/10 como fonte vigente da quarta fala, por hash, ao lado; não consultar a íntegra retirada nem modificar provas/evidências anteriores.',
    'depends_on':[]}],reason='Adendo A autorizado diretamente pelo operador.',sources=pins,event_id='o25-adendo-a-extend'))
new('ADENDO_A_CLAIM.json',act('claim',task_id='source_addendum_a',lease_seconds=3600,event_id='o25-adendo-a-claim'))
p=project();lease=next(t for t in p['projection']['active'] if t['id']=='source_addendum_a')['lease']['id']
new('ADENDO_A_PREFLIGHT.json',act('check',task_id='source_addendum_a',lease_id=lease))
D.mkdir(exist_ok=False)
def save(name,data):
    if isinstance(data,dict):data=json.dumps(data,ensure_ascii=False,indent=2).encode('utf-8')
    if isinstance(data,str):data=data.encode('utf-8')
    with (D/name).open('xb') as f:f.write(data)
    assert (D/name).read_bytes()==data
save('FALA_RECORTE_DECLARADO.txt',REC.read_bytes())
save('ADENDO_A_APLICADO.md',f'''[INPUT — ordem do operador; registro por codex-gerente-tgl, 25/10/2026]
A fonte vigente da quarta fala do §0 é o **recorte declarado da fala de 25/10**, indicado no ADENDO A.
SHA256 conferido dos bytes: `{expected}`. O recorte está copiado, sem alteração, em FALA_RECORTE_DECLARADO.txt.
O recorte é parcial e declarado; não deve ser apresentado como a fala integral.
As referências anteriores à quarta fala, nos inventários e recibos históricos da entrega, ficam superadas por este adendo quanto à fonte vigente.
A conferência anterior era um retrato daquele momento: não deve ser repetida para procurar ou consultar a íntegra retirada. Os scripts históricos de coleta não devem ser reexecutados para essa fonte.
Nenhuma busca, leitura ou citação da íntegra retirada foi feita nesta atualização. Não se inclui seu conteúdo neste adendo.
O módulo Lean, o build, os axiomas e o veredito PONTE PARCIAL permanecem os da entrega; não houve recompilação nem mudança de resultado, kernel, um.py ou gate.
''')
prior=json.loads((OUT/'RESULTADO.json').read_text())
src=OUT/'PonteDaEscalaDual.lean'
assert pin(src)['sha256']==prior['source']['sha256']
save('FONTES_VIGENTES_ADENDO_A.json',{'status':'SOURCE_SUBSTITUTION_APPLIED','label':'recorte declarado da fala de 25/10',
    'order':pin(AD),'source':pin(REC),'custody':pin(D/'FALA_RECORTE_DECLARADO.txt'),
    'applies_to':'Quarta fala do §0 da ORDEM025; referências de fonte da entrega histórica.',
    'withdrawn_source_policy':'Não procurar, consultar ou citar a íntegra retirada.',
    'unchanged_lean':pin(src),'unchanged_result_manifest':pin(OUT/'RESULTADO.json'),
    'prior_evidence_preserved':True,'no_build_or_scientific_change':True})
new('ADENDO_A_SUBMIT.json',act('submit',task_id='source_addendum_a',lease_id=lease,
    evidence=[pin(D/'FONTES_VIGENTES_ADENDO_A.json'),pin(D/'ADENDO_A_APLICADO.md')],event_id='o25-adendo-a-submit'))
p=call({'operation':'project','reference':str(REF),'max_chars':100000},False)
new('ADENDO_A_MEMORY.json',call({'operation':'transition','reference':str(REF),'actor':{'id':OWNER,'kind':'agent'},
    'expected_revision':p['receipt']['revision'],'event_id':'o25-adendo-a-memory',
    'changes':{'records':[{'id':'o25-fourth-speech-source-correction','kind':'erratum','statute':'INPUT',
        'text':'A quarta fala do §0 tem agora como única fonte vigente o recorte declarado da fala de 25/10, pinado no ADENDO_A/FONTES_VIGENTES_ADENDO_A.json. A íntegra retirada não deve ser procurada, consultada ou citada; não repetir sua coleta/verificação histórica. Demais termos da ORDEM025 e resultados matemáticos preservados.',
        'sources':[{'kind':'artifact','ref':str(AD),'sha256':pin(AD)['sha256']},
                   {'kind':'artifact','ref':str(D/'FONTES_VIGENTES_ADENDO_A.json'),'sha256':pin(D/'FONTES_VIGENTES_ADENDO_A.json')['sha256']}]}],
    'flow':{'phase':'awaiting_management_audit','next_action':'Gerencia examina a entrega ORDEM025 com ADENDO A e usa somente o recorte declarado como quarta fala. Nenhuma nova compilacao necessaria.'}}},False))
def board(args):
    p=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\PROGRAMA_IALD\iald.py',*args],capture_output=True)
    if p.returncode:raise RuntimeError(p.stdout.decode()+p.stderr.decode())
    return json.loads(p.stdout)
delivered=board(['avancar',UNIT,'--quem',OWNER,'--status','ENTREGUE','--evidencia',str(D/'FONTES_VIGENTES_ADENDO_A.json'),str(D/'ADENDO_A_APLICADO.md'),
    '--nota','Adendo A: recorte declarado pinado; fonte anterior nao consultada; prova e resultado preservados.'])
new('ADENDO_A_BOARD.json',delivered)
new('ADENDO_A_RELEASE.json',board(['liberar',UNIT,'--quem',OWNER,'--nota','Adendo documental entregue; aguarda gerencia.']))
new('ADENDO_A_VERIFY.json',call({'operation':'verify','reference':str(REF)},False))
print(json.dumps({'sha256':pin(REC)['sha256'],'board':delivered,'memory_revision':project()['receipt']['revision'],'path':str(D)},ensure_ascii=False))
