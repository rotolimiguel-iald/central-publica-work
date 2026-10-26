"""Publish a new immutable source-reuse dossier; never edit prior evidence."""
from pathlib import Path
import sys,json,datetime
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import task

B=Path(__file__).resolve().parent
D=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_025\FONTES_FISICAS')
def write(path,obj):
    data=obj if isinstance(obj,bytes) else json.dumps(obj,ensure_ascii=False,indent=2).encode()
    with path.open('xb') as f:f.write(data)
    assert path.read_bytes()==data

def main():
    p=task.project();t=next(x for x in p['projection']['active'] if x['id']=='physical_sources')
    assert task.act('check',task_id=t['id'],lease_id=t['lease']['id'])['ready']
    review=B/'REVIEW_PHYSICAL_SOURCES.json'
    r=json.loads(review.read_text(encoding='utf-8'))
    assert r.get('verdict',r.get('status')) in ['PASS','PASS_WITH_SCOPE']
    for name in ['ROOT_SOURCES.json','MASS_SOURCES.json','H3_SOURCES.json']:
        for s in json.loads((B/name).read_text(encoding='utf-8'))['sources']:
            assert task.pin(Path(s['path']))['sha256']==s['sha256'],s['path']
    D.mkdir(exist_ok=False)
    names=['CONTRATO_DE_REUSO.md','ROOT_SOURCES.json','MASS_SOURCES.json','H3_SOURCES.json',
           'MASS_VERIFICATION.json','PRIMARY_ERRATA.json','SOURCES_VERIFIED.json','REVIEW_PHYSICAL_SOURCES.json']
    for name in names:write(D/name,(B/name).read_bytes())
    summary='''PONTE PARCIAL — fornecedores físicos recuperados, sem refazer a ponte provada.
Em nome de codex-gerente-tgl, F1.PONTE_NOMEADA, 25/10/2026; reivindicação1217.
[REAL documental] 66 fontes distintas,72 entradas e144 trechos conferidos; versão de programa lida:v401.
Calor do boost já é construído na tela óptica; falta ligar a carga/fonte do mesmo estado da ORDEM025.
H3 já tem família plane-wave em todos pontos/direções, com soma de coeficientes escolhida e shear livre.
Massa: energia confinada, potenciais, espectro e clock→Poisson→Gauss existem; seus dados físicos não são escolhidos por tau.
[DERIVED condicional] M=−c²/(4πG)∮∂n log(R_mod/θ_M)dA: fluxo dado independentemente permite calcular massa no regime fraco.
Controles: mesma normalização permite M=2Ac²R/G livre; potencial escalado mantém mínimo mas muda curvatura.
Gibbs finito da v394 preservado na v401 elimina Eref livre no estado/clock dados; não escolhe κ físico.
Fonte completa/variações R84–R90 reaproveitadas; representação e estacionariedade simultâneas permanecem abertas.
Errata M11: Chandrasekhar histórico foi retirado como validação no artigo; fórmula-beta de massa GA também retirada.
Próximo objeto: fornecedor único de estado/campo, massa/carga, T conservado e relação de área; interfaces prontas indicadas no contrato.
Revisão independente documental anexada; sem nova compilação, provedor, ajuste ao dado, resultado sigma ou alteração de originais/gate.
Gerência examina e registra o mapa; esta entrega não promove a ponte a realização física plena.
'''
    write(D/'RESULTADO.md',summary.encode())
    route={
      'tipo':'ANOTACAO','rota_id':'kernel.ordem025.ponte_escala_dual','dominio':'KERNEL_FORMAL',
      'titulo':'ORDEM025: fornecedores autorais de massa, fonte e Clausius/H3 recuperados',
      'pergunta':'Quais peças existentes podem fornecer a massa física e a fonte/área do mesmo estado?',
      'dados':['66 fontes científicas distintas por hash','um.py v401 lido sem execução',
               'BoostHeatConstruction','PlaneWaveEntropyMatching','Clock/Gauss','Gibbs finito','R84-R90','R13-R16'],
      'metodo':'Consulta dirigida Nós Vivo/mapa e artigos/kernel; confronto de hipóteses, controles algébricos e revisão documental distinta.',
      'resultado':'Calor óptico e H3 em família construída já existem; massa pelo clock/energia é condicional ao perfil e escala. Contrato mínimo de ligação ao mesmo objeto produzido.',
      'veredito':'PONTE_PARCIAL_COM_FORNECEDORES_IDENTIFICADOS','estatuto':'DERIVED','status':'EXAMINADA',
      'olhou_dados':False,'defeito':'Não há fornecedor simultâneo demonstrado de massa/carga física, fonte completa estacionária e área universal para a realização da ORDEM025.',
      'nao_refazer':'Não reconstruir escala dual, E=mc2, calor óptico, família plane-wave ou variações R84-R90. Não reintroduzir massa GA/Chandrasekhar retiradas.',
      'proximo_passo':'Gerência examina; construir fornecedor físico delimitado que consuma o contrato de reuso, conservando parâmetros independentes.',
      'onde':str(D),'artefatos':[str(D/n) for n in names]+[str(D/'RESULTADO.md')],
      'refs':['kernel.ordem025.ponte_escala_dual'],
      'nota':'Proposta de registro para gerência, não aplicada. Fontes antigas e entregas anteriores intactas; nenhum gate movido.'}
    write(D/'registro_mapa_fontes_fisicas.json',route)
    result={
      'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'unit':task.UNIT,'task_id':'physical_sources','status':'ENTREGA_DOCUMENTAL_REVISADA',
      'scientific_result':'PONTE_PARCIAL_COM_FORNECEDORES_IDENTIFICADOS',
      'statute':'DERIVED_WITH_EXPLICIT_INPUTS_AND_OPEN_LINKS','reference':str(task.REF),
      'files':[task.pin(x) for x in sorted(D.iterdir()) if x.is_file()],
      'source_verification':{'unique_files':66,'catalog_entries':72,'exact_excerpt_ranges':144},
      'validation':'Hashes/excertos + nove verificações algébricas delimitadas; revisão documental independente. Sem nova compilação ou teste empírico.',
      'review':task.pin(review),'original_order025_proof_reused':task.pin(D.parent/'PonteDaEscalaDual.lean'),
      'fourth_speech_current_source_index':task.pin(D.parent/'ADENDO_A/FONTES_VIGENTES_ADENDO_A.json'),
      'primary_source_state_correction':task.pin(D/'PRIMARY_ERRATA.json'),
      'scope':'Busca dirigida, não inventário exaustivo; encontrar receita condicional não seleciona automaticamente seus dados físicos.',
      'unchanged':['um.py','kernel do Nós','Bancada de produção','dados observados','gate','evidências anteriores'],
      'management_audit_pending':True,'map_registration_by_management':True}
    write(D/'RESULTADO_FONTES_FISICAS.json',result)
    print(json.dumps(task.pin(D/'RESULTADO_FONTES_FISICAS.json'),ensure_ascii=False))

if __name__=='__main__':main()
