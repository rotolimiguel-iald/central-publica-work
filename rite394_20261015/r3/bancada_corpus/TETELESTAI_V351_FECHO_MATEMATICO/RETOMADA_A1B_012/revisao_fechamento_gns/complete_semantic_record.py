from build_delta import *
out=R/'revisao_fechamento_gns';rows=[]
for p in sorted((R/'dev_gns_closedness').glob('*/run.json')):
 j=load(p)
 for f in ('stdout','stderr'):ck(j[f])
 text=Path(j['stdout']['path']).read_text(encoding='utf8')
 rows.append(dict(run=pin(p),returncode=j['returncode'],historical_source_metadata=j['source'],stdout=j['stdout'],stderr=j['stderr'],contains_sorryAx='sorryAx' in text,diagnostics=[l for l in text.splitlines() if 'error:' in l or 'warning:' in l],selected=p.parent.name=='20260914_203030_719820'))
final=[r for r in rows if r['selected']]
assert len(final)==1 and final[0]['returncode']==0 and not final[0]['diagnostics'] and not final[0]['contains_sorryAx']
ck(final[0]['historical_source_metadata'])
save(out/'history_read.json',dict(timestamp=now(),rows=rows,role='Author DEV history only; no objects inherited'))
hist=pin(out/'history_read.json')
notes=dict(review_complete=True,findings=[],status='A1_GNS_CLOSEDNESS_REVIEW_ACCEPTED__RIGHT_ACTION_TRACE_OPEN',report_name='REVIEW_A1_GNS_CLOSEDNESS_FINAL',title='Revisão independente — fechamento da inscrição GNS do peso',paragraphs=[
 '[REAL] Delta delimitado de três teoremas, zero definições. Fonte e ficha MD/JSON foram lidas integralmente. Os objetos são scalarWeightLeftIdeal, scalarWeightGNSEmbedding e ScalarGNSHilbert já existentes; o resultado não substitui o ideal completo por finiteDualLeftIdeal nem cria outro GNS.',
 '[REAL] scalarGNSCutMap_weight_embedding estende de fato a identidade dos cortes a TODO a∈nν. A prova mantém scalarCutVacuum com sqrt(dualHaarFactor), o mesmo regularVacuum e dualOrbitRepresentation. Usa eventos a.e. finitos para cada corte e linearidade complexa; não normaliza artificialmente um vetor de corte nem o declara separante.',
 '[REAL] scalarWeightGNSEmbedding_of_cut_actions usa somente os índices n naturais. A união de Ioc(−n,n) cobre ℝ; ae_all_iff é aplicado à família contável, sem uniformização sobre todos os vetores ou um filtro não enumerável. Da igualdade a.e. com v∈L² e sqrt(dualHaarFactor)>0, recupera MemLp da órbita pela escala inversa. hasFiniteScalarSquare_iff_memLp dá a pertinência real de A ao ideal completo, e scalarWeightOrbit_ae identifica a inscrição no mesmo H_I.',
 '[REAL] scalarWeightGNSEmbedding_closed_of_bounded_strong tem índice de universo arbitrário, filtro l e [NeBot l] explícito. A cota uniforme é de norma de operadores; hstrong e hgns são premissas separadas. A continuidade de cada scalarGNSCutMap e dualOrbit_tendsto_of_uniformly_bounded dão dois limites do MESMO vetor cortado; tendsto_nhds_unique usa a não trivialidade. Não se deduz convergência GNS de forte isolada, nem se requer convergência dos adjuntos para este teorema.',
 '[REAL] Cinco fornecedores antigos estavam ausentes em v: V350ScalarGNSCutMaps, V350DualCutLinearMap, V350ScalarBoundedCuts, V350ScalarGNSCutNorm e V350ScalarCutVacuum. Foram copiados em bytes de OLD/kernel após comparação com K e recompilados pelo Lake próprio. Os nomes/pins individuais estão em snapshot e compilation. O build de fornecedores do autor não foi importado nem contado como reprodução própria.',
 '[REAL] Histórico medido: '+ '; '.join(Path(r['run']['path']).parent.name+': rc'+str(r['returncode']) for r in rows)+'. O primeiro rc1 é ausência do objeto ScalarCutVacuum, não refutação matemática; o segundo contém erro de coerção real/complexa e uso inválido de MemLp.congr, com sorryAx transitivo, e está excluído. Só a fonte final rc0 sem avisos é aceita. [history_read.json](<'+hist['path']+'>), SHA256 `'+hist['sha256']+'`.',
 '[REAL] Auditoria autoral e negativo BadGNSCutNormalization relidos com hashes, sem execução pela revisão: acrescentar fator 2 à identidade do corte produz Type mismatch, não falha de importação ou ambiente. Um rótulo auxiliar do script validate_gns_closedness menciona INVERSE_CUTOFF; não foi usado para identificar/aceitar este delta. A evidência selecionada é AUDITORIA_FECHAMENTO_GNS_A1B com os três nomes exatos e streams correspondentes; essa observação de rótulo não altera o resultado formal.',
 '[REAL] A ficha antecede o código e aponta consumidor específico: extensão da ação direita para os cortes na perturbação do peso. O fechamento remove uma obrigação real dessa rota, mas não fornece por si uma família de aproximantes nem a segunda convergência exigida.'
 ],limits=[
 'Ação direita de elementos além dos fornecedores já pagos, geração forte limitada e passagem a sqrt(Bε) são obrigações posteriores.',
 'Nenhuma monotonicidade de sanduíches ou de avaliações perturbadas, tracialidade, novo predual ou pagamento completo de A1(b).',
 'Sem cobrança de minorantes positivos para ν, sem mudança de J, gate ou memória. Consulta posterior por grafos/projeções é separada, sem alvos Lean adicionais.'
 ])
save(out/'semantic_notes.json',notes)
print(json.dumps(dict(history=[dict(run=Path(r['run']['path']).parent.name,returncode=r['returncode']) for r in rows],semantic_complete=True),ensure_ascii=False))
