from pathlib import Path
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
K = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
F = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
O = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_025')
REF = BASE.parent / 'SESSION_REFERENCE.json'

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def source(key, path, ranges, status='REAL_LEITURA_DE_FONTE_LOCAL'):
    raw = path.read_bytes()
    lines = raw.decode('utf-8-sig').splitlines()
    excerpts = []
    for start, end in ranges:
        if not 1 <= start <= end <= len(lines):
            raise ValueError((str(path), start, end, len(lines)))
        excerpts.append({'start_line': start, 'end_line': end,
                         'text': '\n'.join(lines[start-1:end])})
    return {'id': key, 'path': str(path), 'sha256': digest(raw), 'bytes': len(raw),
            'line_count': len(lines), 'status': status, 'excerpts': excerpts}

SPECS = [
 ('o25', O/'PonteDaEscalaDual.lean', [(10,19),(25,57),(111,140),(142,179),(195,232)]),
 ('heat', K/'ConstructedHeatPrimitive.lean', [(24,30),(55,73),(101,114)]),
 ('metric', K/'GeneralMetricClausius.lean', [(41,63),(83,97),(108,131)]),
 ('unitary', K/'UnitaryClausiusBridge.lean', [(24,30),(38,46),(58,66),(75,105)]),
 ('coherent', K/'CoherentHeatMatching.lean', [(25,27),(35,45),(97,106),(113,134)]),
 ('coherent_einstein', K/'CoherentEinsteinBridge.lean', [(35,42),(54,62),(68,78),(98,114)]),
 ('calibration', K/'UnitarySourceCalibration.lean', [(39,50),(100,106),(135,137)]),
 ('realization', K/'GeneralSourceUnitaryRealization.lean', [(44,79),(108,120),(144,161),(202,205)]),
 ('general', K/'GeneralSourceEinsteinBridge.lean', [(43,52),(73,84),(95,109)]),
 ('reconstruction', K/'GeneralSourceResponseReconstruction.lean', [(48,53),(83,105)]),
 ('boost', K/'ApproximateBoostFlow.lean', [(36,54),(134,140),(285,302)]),
 ('boost_heat', K/'BoostHeatConstruction.lean', [(14,16),(34,56),(64,85),(91,104),(110,125),(172,186)]),
 ('boost_limits', K/'BoostMetricJets.lean', [(143,150)]),
 ('optical', K/'OpticalTidalScreen.lean', [(28,34)]),
 ('wave_solder', K/'PlaneWaveSolder.lean', [(27,34),(60,73),(108,116)]),
 ('wave_matter', K/'PlaneWaveMatter.lean', [(27,29),(50,58),(65,85)]),
 ('wave_matching', K/'PlaneWaveEntropyMatching.lean', [(3,11),(28,38),(42,64),(82,120),(122,138)]),
 ('wave_controls', K/'PlaneWaveReconstructionControls.lean', [(53,57),(75,79),(82,103),(147,151)]),
 ('optical_heat', K/'OpticalConstructedHeat.lean', [(47,67),(118,146)]),
 ('optical_clausius', K/'OpticalHeatClausius.lean', [(34,42),(67,71),(91,97)]),
 ('flat_control', K/'ConstructedClausiusControls.lean', [(65,88),(116,143)]),
 ('entropy_control', K/'RelativeEntropyGravityControls.lean', [(59,63),(203,205)]),
 ('state_clock', K/'StateClockDichotomy.lean', [(126,129),(142,169)]),
 ('state_clock_scope', K/'StateClockMatchingControls.lean', [(312,322),(330,341)]),
 ('gibbs', K/'GibbsMatterBridge.lean', [(28,38),(109,118),(125,156)]),
 ('same_p', K/'SelectedFisherGibbsBridge.lean', [(42,67),(91,124)]),
 ('sigma', K/'SelectedProbabilitySigma.lean', [(44,51),(133,156),(171,179),(192,212)]),
 ('maxwell', K/'TheImportedSecondQuantization.lean', [(494,516),(545,563)]),
 ('maxwell_adapter', F/'matter_h3_inventory/src/TGLExt/MaxwellBoostChargeAssemblyR1.lean', [(3,10),(22,71)]),
 ('maxwell_inventory', F/'matter_h3_inventory/INVENTARIO_R8_R9_R1.md', [(1,14)]),
 ('ligand', K/'LiganteLeiCampoCurvo.lean', [(9,15),(31,41),(46,72)]),
 ('r84', F/'integrated_h3_r84/p_variations/P_VARIATIONS_AND_COUNTEREXAMPLE_R84.md', []),
 ('r85', F/'selection_variation_r85/selection/SELECTION_AND_NORMAL_VARIATIONS_R85.md', []),
 ('r85_erratum', F/'selection_variation_r85/selection/ADENDO_SIGMA_EFFECTIVE_SOURCE_R85.md', []),
 ('r88', F/'full_source_r88/source/ONE_FORM_FULL_SOURCE_R88.md', []),
 ('r89', F/'stationary_selection_r89/source/ACTION_EOM_RESIDUAL_R89.md', []),
 ('r89_result', F/'stationary_selection_r89/RESULTADO_R89.json', []),
 ('r90', F/'completion_audit_r90/BALANCO_DA_META_R90.md', []),
 ('article', Path(r'C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py'), [(10319,10369),(10418,10460)]),
 ('anchor', BASE/'ANCHOR.json', []),
 ('preflight', BASE/'PREFLIGHT.json', []),
 ('nos_packet', BASE/'NOS_PACKET.txt', []),
 ('map', BASE/'MAP_QUERY.json', []),
]

def main():
    output = BASE/'H3_SOURCES.json'
    if output.exists():
        raise FileExistsError('Preserve existing report; use a separately named revision.')
    anchor = json.loads((BASE/'ANCHOR.json').read_text(encoding='utf-8-sig'))
    old_check = json.loads((BASE/'PREFLIGHT.json').read_text(encoding='utf-8-sig'))
    proc = subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],
        input=json.dumps({'operation':'project','reference':str(REF),'max_chars':120000}),
        capture_output=True,text=True,encoding='utf-8',check=True)
    response=json.loads(proc.stdout)
    if not response.get('ok'):
        raise RuntimeError('Project refused; no output written.')
    current=response['result']
    task=next(x for x in current['projection']['active'] if x['id']=='physical_sources')
    if not (current['receipt']['revision']==anchor['revision']==old_check['receipt']['revision']
            and current['projection_sha256']==anchor['projection_sha256']==old_check['projection_sha256']
            and task['lease']['id']==anchor['lease_id']==old_check['lease_id']
            and old_check['ready'] and task['lease']['expires_at']>datetime.now(timezone.utc).timestamp()):
        raise RuntimeError('Changed revision/lease/preflight: no output written.')
    sources=[]
    for key,path,ranges in SPECS:
        if key in {'r84','r85','r85_erratum','r88','r89','r90'}:
            # These prior analytical reports were read fully, without executing their scripts.
            ranges=[(1,len(path.read_text(encoding='utf-8-sig').splitlines()))]
        sources.append(source(key,path,ranges))
    by_id={s['id']:s for s in sources}
    if by_id['nos_packet']['sha256']!=anchor['packet']['sha256']:
        raise RuntimeError('NOS packet differs from delegated pin.')
    findings=[
      {'id':'F1','status':'EXISTE_E_ESTA_LIGADO','sources':['boost','boost_heat','heat','optical_heat'],
       'claim':'O fornecedor mais próximo de energia que entra em deltaQ já existe: boost_energy_flux_constructed identifica T(chi,k)dA com screenHeatFlux na tela óptica; boost_energy_heat_constructed identifica seu integral com constructedHeat como germe passado.',
       'premises':['Tela opticalEquilibriumScreen; a,c>=0 para o construtor óptico.', 'TensorField4 T é entrada; para a igualdade integral pronta usa-se waveMatter a c mass.', 'Convenção de orientação: integral 0..t versus t..0; calor e área mudam sinal juntos.'],
       'not_implied':['Não identifica tau do core nem pPlus da ORDEM025 com a carga/fluxo.', 'Não constrói Unruh/KMS; rate/(2pi) é normalização herdada.']},
      {'id':'F2','status':'EXISTE_E_ESTA_LIGADO_EM_FAMILIA_CONSTRUIDA','sources':['wave_solder','wave_matter','wave_matching','wave_controls'],
       'claim':'Existe habitante curvo de area matching em todo ponto e direção nula dentro da família plane-wave: matched_wave_area, matched_constructed_area, matched_wave_einstein e matched_wave_einstein_from_area.',
       'premises':['b:SummableAmplitude e eta nãozero para a via de área.', 'matchedLeft/right definidos por 2pi*amplitudeCoupling b/eta, com shear livre; a soma é escolhida para o matching.', 'Métrica/Levi-Civita/Ricci/fonte conservada são da mesma família explícita.'],
       'not_implied':['Não é derivação de geometria geral de omega(I)=1.', 'amplitudeMass/amplitudeCoupling/mass do fluxo não são automaticamente massa de repouso ou mu2 da ORDEM025.', 'Estado, Ricci e fonte não selecionam shear: state_alone_not_curvature_coordinate.']},
      {'id':'F3','status':'EXISTE_E_ESTA_LIGADO_CONDICIONAL','sources':['metric','unitary','coherent','coherent_einstein','gibbs','general'],
       'claim':'Calor e área são hipóteses distintas. coherent_heat_matching/gibbs_heat_matching/general_source_heat_matching fornecem a primeira. A área é equivalente a eta*Ric(v,v)=2pi*T(v,v). Einstein consome a área para todos pontos/nulos mais simetria, conservação e regularidade.',
       'premises':['U aberto e preconexo; g suave e lorentziana; T diferenciável/suave, simétrica e covariantemente conservada.', 'MetricScreenFamily U g, rate e eta nãozero na via Clausius.', 'harea/hclausius universal sobre p em U e v nãozero g-nulo.'],
       'not_implied':['Correspondência de calor sozinha não fornece a lei de área.', 'Um eixo longitudinal, uma tela ou uma cunha padrão não fornece o quantificador universal.']},
      {'id':'F4','status':'EXISTE_RECONSTRUCAO_NAO_SELECAO','sources':['calibration','realization','reconstruction'],
       'claim':'Qualquer fonte simétrica admitida pode ser realizada por oito rótulos calibrados, reconstruída e recuperada de dez respostas. realized_source_eq devolve o T de entrada; realized_source_conserved requer hc de entrada.',
       'premises':['g e T são fornecidos; inversa, simetria e suavidade conforme cada lema.', 'Calibração inclui contribuições de ambos sinais.'],
       'not_implied':['Não determina T a partir de tau ou do axioma.', 'Não transforma reconstrução em seleção dinâmica nem em identificação física.']},
      {'id':'F5','status':'EXISTE_NA_BANCADA_FIACAO_CONDICIONAL','sources':['maxwell','maxwell_adapter','maxwell_inventory'],
       'claim':'MaxwellBoostChargeAssemblyR1 compõe o fator modular 2pi e fornece standardWedgeH3 preservando o mesmo Q; TheImportedSecondQuantization constrói lightH3/lightH3v32 a partir de MaxwellCertificate.',
       'premises':['Mesmo FockCertificate, domínio regular e MaxwellQuadraticForm físico Q.', 'BoostChargeIdentity entre derivada do boost real e nullPlaneCharge, mais NonzeroChargeState.', 'T simétrico/conservado/covariante e integrabilidade dos momentos nulos.'],
       'not_implied':['Adaptador não constrói Q/Wick, sua identificação física nem habitante simultâneo das hipóteses.', 'nullDir fixa/cunha padrão não prova H3 curva em toda direção.']},
      {'id':'F6','status':'EXISTE_MESMA_ORIGEM_COM_RESIDUO_DINAMICO','sources':['same_p','sigma','r84','r85','r85_erratum'],
       'claim':'Há mapas concretos dos mesmos P para métrica Fisher refletida e fontes Gibbs/sigma. Conservação depende de onda/heigen, e H3 ainda exige área. R84 contém ramo positivo P5 sob coeficiente C*cG=4 e contraexemplo P6 conservado: duas direções requerem C*cG=2 e C*cG=7/2.',
       'premises':['Probabilidades positivas/normalizadas, rank4 e relógio nãozero.', 'C=2pi/eta e cG pertencem à fonte, não são ajustados para vencer o controle.'],
       'not_implied':['Origem comum+conservação não implica H3.', 'Rank10 de jets P5 não é livre variação de campos; P16 levanta campos mas modifica matéria.', 'Errata R85: on-shell sigma puro radial é incompatível com dez formas normais livres; T_eff não pode ser trocado por T_sigma.']},
      {'id':'F7','status':'EXISTE_FONTE_AUTORAL_E_VARIACAO_PARCIAL_NAO_LIGADA_A_H3_GERAL','sources':['article','r88','r89','r90'],
       'claim':'O artigo fornece ação matéria+campo+gravitação não minimal+termo modular; R88/R89 já calculam fonte/Euler sob leitura literal real de 1-forma. Não reconstruir essas variações. R90 preserva falta de representação única, estacionariedade da mesma ação completa e fechamento universal.',
       'premises':['Contrato 1-forma real A, u=gInv(A,A), f=F0+xi*u, F=dA e L_rest são explícitos, sem afirmar A=Psi(P).', 'Convenções de assinatura/curvatura/sinal de Hilbert e contorno precisam permanecer pareadas.', 'A passagem operador modular abstrato -> fonte geral é conjectura declarada nas linhas10449–10456 do artigo.'],
       'residual':'No contrato R88: 2*f*Ric(k,k)=T_M(k,k)+T_rest(k,k)+2*xi*Hess(u)(k,k)-2*xi*R*A(k)^2, se E_g=0. R89: E_A-W(A)=-grad(divA)-Ric.A+3xi*R*A+mPsi^2*A+beta*K*A+E_rest, condicional à mesma representação.',
       'not_implied':['Não chamar variação calculada de solução estacionária.', 'Psi escalar, Psi_mu 1-forma, psi fermiónico e phi Higgs não são intercambiáveis.', '|1+w| pode não ser diferenciável na fronteira; a classe variacional precisa ser especificada.']},
      {'id':'F8','status':'CONTROLES_EXISTENTES_REAPROVEITAR','sources':['flat_control','entropy_control','optical_clausius','state_clock','state_clock_scope','wave_controls','r85'],
       'claim':'Controles delimitam inferências: fonte plana simétrica e conservada falha Clausius; primeira ordem de entropia não fornece segunda; mesmo estado permite shear diferente; relógio comum não satisfaz quarta ordem em duas telas.',
       'not_implied':['O no-go de quarta ordem/igualdade finita NÃO exclui H3 infinitesimal de segunda ordem.', 'O reset GKLS da R85 é contramodelo lógico, não gerador físico instalado.', 'Esses controles não refutam a TGL inteira nem demonstram ausência universal no acervo.']},
      {'id':'F9','status':'LIGAR_COM_CONTRATO_EXPLICITO','sources':['o25','boost','optical','boost_limits','boost_heat'],
       'claim':'A ORDEM025 usa embed=(E,p,0,0), enquanto a rota óptica usa eixo3 e k=(1/2,0,0,1/2). Ambas possuem lei exponencial, mas faltam consumidor tipado e identificação física.',
       'premises':['Explicitar permutação/intertwiner do eixo1 ao eixo3, normalizações de coordenadas nulas e rapidity=rate*s.', 'Distinguir parâmetro de boost s do parâmetro afim t do integral.', 'O boost óptico é aproximado em geometria curva, não Killing em aberto quando rate!=0 e curvatura transversal!=0.'],
       'not_implied':['Mesmo caráter exponencial não identifica grandezas físicas.', 'Tau positivo não é massa invariante: positive_weight_cannot_be_invariant_mass já o delimita.']},
    ]
    report={
      'schema':'iald-ordem025-h3-sources/v1','generated_at_utc':datetime.now(timezone.utc).isoformat(),
      'author':'/root/o25_h3_sources','reference':str(REF),'task_id':'physical_sources',
      'status':'CANDIDATO_DOCUMENTAL_PARA_REVISAO_INDEPENDENTE',
      'scope':'Leitura local de fontes e recibos existentes. Zero build, zero import/execução um.py, zero provedor, zero alteração de originais/memória/quadro/gate. Não é nova prova.',
      'anchor':{'revision':current['receipt']['revision'],'projection_sha256':current['projection_sha256'],
                'lease_id':task['lease']['id'],'preflight_owner':task['lease']['owner'],
                'preflight_delegated_artifact':by_id['preflight']},
      'summary':'Fornecedor de calor óptico e família curva H3 já existem. A ponte longitudinal não os consome nem seleciona massa/fonte/geometria. O elo geral restante é de identificação do mesmo sistema e de dinâmica/área universal; não basta entropia, reconstrução, Gibbs, conservação ou correspondência exponencial.',
      'findings':findings,
      'minimal_contract':[
        {'id':'C0','status':'OPEN_PARA_O25','need':'Escolher a realização física e o mapa do objeto do core para estado/campo; dar origem independente do parâmetro mu2 e dos coeficientes dimensionais.', 'cannot_replace_with':'Não definir a massa livre para fazer a conclusão valer.'},
        {'id':'C1','status':'OPEN_PARA_O25','need':'No mesmo modelo, fornecer U,g,T, conexão e regularidade; provar T simétrico e conservado. Reutilizar waveMatter para subfamília declarada, ou a fonte completa da ação existente com todas suas parcelas e equações materiais.', 'cannot_replace_with':'Não usar T reconstruído de si mesmo como seleção; não substituir fonte completa por sigma/Maxwell isolado.'},
        {'id':'C2','status':'OPEN_IDENTIFICACAO','need':'Provar que a carga/fluxo do estado ligado a tau é o T(chi,k)dA usado no calor, com domínio, unidades, eixo, normalização e parâmetro explícitos. A via quântica mínima disponível é BoostChargeIdentity + NonzeroChargeState no mesmo Q regular.', 'reuse':'boost_energy_flux_constructed e boost_energy_heat_constructed cobrem a fiação óptica já pronta.'},
        {'id':'C3','status':'OPEN_GERAL_EXISTE_SUBFAMILIA','need':'Para cada ponto e direção g-nula nãozero, fornecer area matching da mesma preparação/fonte. Na família matched plane-wave isso já é construído com soma escolhida; para g geral é equivalente à igualdade nula de Ricci.', 'cannot_replace_with':'Adicionar harea dá teorema condicional honesto, mas não descarrega a hipótese física. Derivá-la por ação requer estacionariedade independente da ação completa e variações admissíveis suficientes.'},
        {'id':'C4','status':'PRONTO_APOS_C1_C3','need':'Consumir general_source_einstein_from_area ou metric_einstein_from_screen_clausius; para atlas global usar o ligante/colagem com transições e conservação.', 'cannot_replace_with':'Cunha padrão, linha nula ou apenas um componente pPlus não substitui o quantificador de todas as direções.'}
      ],
      'reuse_matrix':[
        {'object':'T(chi,k)dA -> calor integrado','reuse':'boost_heat + heat + optical_heat','link':'tau/estado/carga da O25 ao mesmo T','do_not_infer':'E=mc2 ou massa de repouso como amplitude do tensor'},
        {'object':'H3 em toda direção da onda plana','reuse':'wave_matching','link':'Selecionar justificadamente essa família, coeficiente e shear','do_not_infer':'Solução geral derivada do estado'},
        {'object':'Realização unitária de fonte arbitrária','reuse':'calibration + realization + general','link':'Fornecedor físico independente de T e harea','do_not_infer':'Seleção física a partir da capacidade de representar qualquer T'},
        {'object':'H3 Maxwell cunha padrão','reuse':'maxwell_adapter + maxwell','link':'Q físico, BoostChargeIdentity, estado regular nãozero, transporte geométrico','do_not_infer':'Fock físico completo ou H3 curva universal'},
        {'object':'Mesmo P -> g,T','reuse':'same_p + sigma + r84','link':'Dinâmica que seleciona a configuração e harea','do_not_infer':'Conservação/Gibbs/atração implica Einstein'},
        {'object':'Ação autoral e fonte completa','reuse':'article + r88 + r89 + r90','link':'Representação única, resíduo Euler, contorno, estacionariedade','do_not_infer':'Trocar tipos/sinais ou cancelar resíduo por definição'},
        {'object':'Paredes de relógio/entropia','reuse':'flat_control + state_clock + state_clock_scope','link':'Aplicar somente no regime e ordem indicados','do_not_infer':'No-go geral para H3 infinitesimal'}
      ],
      'search_scope':{'bases':[str(K),str(F),str(O)],
        'method':'Buscas locais dirigidas por nomes e declarações; leitura de módulos e relatórios apontados; artigos lidos apenas nas faixas pinadas.',
        'not_found_name':'CoherentMatterSource.lean não encontrado; dependência real lida via CoherentHeatMatching/ScalarStressConservation. Não é ausência de construção.',
        'exclusions':['Quarta fala original retirada: não buscada nem lida como fonte; Adendo A preservado.', 'Sem acervo Escritório, credenciais ou arquivos confidenciais.', 'Sem alegação de varredura de todo o PC ou corpus completo.']},
      'sources':sources,
      'counts':{'source_files':len(sources),'findings':len(findings),'new_builds':0,'provider_calls':0},
    }
    data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    tmp=BASE/'H3_SOURCES.json.tmp'
    with tmp.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if tmp.stat().st_size != len(data) or digest(tmp.read_bytes())!=digest(data):
        raise RuntimeError('Temporary write verification failed.')
    tmp.replace(output)
    check=json.loads(output.read_text(encoding='utf-8'))
    assert check['counts']['source_files']==len(SPECS)
    for s in check['sources']:
        assert digest(Path(s['path']).read_bytes())==s['sha256'], s['path']
    print(json.dumps({'status':'WRITTEN_AND_SOURCE_PINS_RECHECKED','path':str(output),
                      'bytes':len(data),'sha256':digest(data),'source_files':len(sources)},ensure_ascii=False))

if __name__=='__main__':
    main()
