from finish_delta import *
out=Path(__file__).resolve().parent
history=[]
for p in sorted((R/'dev_right_action_limits').glob('*/run.json')):
 j=load(p);row=dict(run=pin(p),returncode=j['returncode'],streams=[])
 for k in ['stdout','stderr']:
  ck(j[k]);row['streams'].append(j[k])
  if k=='stdout':row['stdout_text']=Path(j[k]['path']).read_text(encoding='utf8')
 history.append(row)
save(out/'history_read.json',dict(rows=history,only_final_rc0_accepted=True,old_source_pins_not_compared_to_new_source=True))
print(json.dumps([dict(path=x['run']['path'],rc=x['returncode'],text=x['stdout_text'][:1700]) for x in history],ensure_ascii=False))
notes=dict(review_complete=True,findings=[],status='A1_RIGHT_ACTION_LIMITS_REVIEW_ACCEPTED__CUTOFF_RIGHT_ACTION_TRACE_OPEN',report_name='REVIEW_A1_RIGHT_ACTION_LIMITS_FINAL',title='Revisão independente — limites da ação direita original',paragraphs=[
'[REAL] Dois teoremas, zero definições. Fonte e ficha MD/JSON relidas integralmente. A notação antiunitaryConjugate usa o mesmo scalarTomitaPolarFactor P, π é scalarGNSRepresentation P, e o domínio inicial é scalarWeightLeftIdeal P completo. Não há troca pelo J da torre nem por um GNS auxiliar.',
'[REAL] scalarRightAction_regular é uma ligação efetiva entre regularRightGNS_intertwines e scalarTomitaPolarFactor_regular_left: a estrela no elemento regular está presente e a inversa do antiunitário cancela pela isometria. O produto regular já contém sua prova de pertença ao ideal; nenhuma hipótese adicional de ação direita é introduzida para esse grupo.',
'[REAL] scalarRightAction_closed_of_bounded_strongStar recebe uma família b_i no mesmo core, uma cota C, convergência forte de b_i e de b_i*, um filtro arbitrário de universo arbitrário não trivial, e a identidade direita em cada aproximante. A existência dessa família continua INPUT. Para cada A∈nν, escolhe apenas as provas de pertença de A b_i ao ideal; a independência desses testemunhos é proposicional.',
'[REAL] A convergência GNS NÃO é premissa oculta nem consequência atribuída à forte isolada: norm_star mantém a mesma cota C nos adjuntos, scalarGNSRepresentation_tendsto_of_uniformly_bounded aplica-se a b_i* no vetor J⁻¹Λ(A), e a continuidade de J produz convergência em norma de Jπ(b_i*)J⁻¹Λ(A). A hipótese hadjoint é usada exatamente nesse ponto.',
'[REAL] A rede A b_i tem cota ||A|| C e converge fortemente a A B pela continuidade do operador A. O fechamento GNS já reproduzido recebe essas duas convergências e devolve A B∈nν e a identidade desejada. Não se presume continuidade da estrela para a topologia forte em geral, nem positividade de A ou dos b_i.',
'[REAL] A ficha anterior aos fontes descreve corretamente o consumidor dos cortes inversos, sem prometer aproximantes. Os pins dos sete fornecedores e da busca são verificados pelo finalizador. Os objetos próprios anteriores são reaproveitados, sem DEV autoral; os tipos universais e axiomas são capturados em auditor próprio separado.',
'[REAL] Histórico autoral preservado em history_read.json: a tentativa rc1 por binder i é excluída, inclusive quaisquer prints parciais; somente 20260914_203706_719663 rc0 é aceito. O negativo BadRightActionMissingStar é relido no stream autoral: trocar π(b*) por π(b) resulta em Type mismatch, com importações válidas. Nenhum negativo autoral foi reexecutado.'
],limits=[
'A rede aproximante e a ação de R ou sqrt(Bε) não são construídas neste delta.',
'A revisão não declara toda W*(Λ) coberta, nem tracialidade, nova perturbação do peso ou pagamento de A1(b).',
'Nenhuma memória, programa, gate, fonte autoral ou relatório anterior foi alterado. A consulta CFC/seno é separada e não acrescenta alvo Lean ao aceite.'
])
save(out/'semantic_notes.json',notes)
