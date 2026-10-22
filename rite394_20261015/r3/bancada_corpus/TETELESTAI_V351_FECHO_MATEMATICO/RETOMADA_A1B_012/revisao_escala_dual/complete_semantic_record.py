from build_delta import *

out = R / 'revisao_escala_dual'
rows = []
for p in sorted((R / 'dev_regular_dual_scaling').glob('*/run.json')):
    j = load(p)
    for field in ('stdout', 'stderr'):
        ck(j[field])
    text = Path(j['stdout']['path']).read_text(encoding='utf8')
    rows.append(dict(run=pin(p), returncode=j['returncode'],
        historical_source_metadata=j['source'], stdout=j['stdout'], stderr=j['stderr'],
        diagnostics=[line for line in text.splitlines() if 'error:' in line or 'warning:' in line],
        contains_sorryAx='sorryAx' in text,
        accepted_source=p.parent.name == '20260914_200033_241925'))
assert [r['returncode'] for r in rows] == [1, 0, 0]
assert rows[0]['contains_sorryAx'] and not rows[-1]['diagnostics']
save(out/'history_read.json', dict(timestamp=now(), rows=rows,
    scope='Streams measured; historical source hashes are metadata, not compared to the final source.',
    reviewer_preliminary_inspection_error='A preliminary read-only count assertion expected [1,1,0] and failed before writing. Actual statuses are [1,0,0]; no Lean invocation or acceptance depended on that assumption.'))

save(out/'semantic_notes.json', dict(
    review_complete=True, findings=[],
    status='A1_REGULAR_DUAL_SCALING_REVIEW_ACCEPTED__TRACE_OPEN',
    report_name='REVIEW_A1_REGULAR_DUAL_SCALING_FINAL',
    title='Revisão independente — escala dual do gerador regular',
    paragraphs=[
        '[REAL] Delta único: V351RegularGeneratorDualScaling, sete teoremas, nenhuma definição. Ficha e adendo foram lidos integralmente; seus fornecedores são verificados por bytes. As oito entregas anteriores são base reutilizada e permanecem preservadas, sem somar seus alvos a este aceite.',
        '[REAL] Convenções verificadas: Fourier inversa transporta shift(t) para characterMultiplier(−2πt); Fourier transporta characterMultiplier(s) para shift(−s/(2π)). A primeira prova usa SchwartzMap.fourierInv_coe explicitamente, a passagem ao L² usa densidade e continuidade de operadores limitados. Não há hipótese de separabilidade de H nem interseção a.e. não enumerável.',
        '[REAL] operatorFieldLift_commutes_character decorre de linearidade complexa ponto a ponto e eventos a.e. finitos. A aplicação usa o V=WF⁻¹ já construído, no mesmo espaço regular, e não supõe W∈N. regularSpectralCoordinates_dual produz V⁻¹C_s=shift(−s/(2π))V⁻¹.',
        '[REAL] O grafo é o mesmo regularPositiveGenerator. A translação das coordenadas exp(−2πξ) dá h C_s x=e^s C_s h x para todo x no domínio. A implicação inversa usa −s, characterMultiplier_inverse e e^(−s)e^s=1. Assim a igualdade de domínios é efetiva e a leitura de conjugação é Ad(C_s)h=e^(−s)h. Não se supõe domínio total, inversa limitada de h, gap, ou uma nova identificação espectral.',
        '[REAL] Histórico relido: DEV 19:55:13 rc1 contém erro de change/coerção de Fourier inversa, erro de simplificação e sorryAx; está excluído. DEV 19:59:17 é rc0 COM um aviso de tática inútil; não foi contado como rc1 nem usado como fonte final. O candidato 20:00:33 é rc0 sem avisos. history_read.json registra os streams e a correção de uma expectativa preliminar incorreta do revisor sobre essa contagem, sem repetir compilação.',
        '[DECLARADO / documentação conferida] A primeira preparação da ficha usou caminho de fornecedor inexistente; a ficha registra correção para V350StrongOperatorField antes do código. Isto é falha de preparação, não negativo matemático. O adendo explicita o fornecedor SchwartzMap.fourierInv_coe. A busca foi delimitada: não alego exaustividade do acervo.',
        '[REAL] O controle autoral BadRegularDualScalingSign foi relido com hashes de fonte/streams: substituir e^s por e^(−s) na segunda componente do grafo produz Type mismatch, com imports válidos. Esta revisão executou seu próprio Lake e auditor; não reexecutou o negativo autoral.'
    ],
    limits=[
        'A escala dual do mesmo grafo é aceita neste delta. Não há construção de τ, prova de tracialidade ou pagamento de A1(b) completo.',
        'A proposta posterior de cortes por escala dual é consulta separada, não alvo Lean destes sete teoremas.',
        'Nenhum monólito, recorder, memória, fonte autoral ou relatório anterior foi alterado; nenhuma promoção de gate.'
    ]))
print('SEMANTIC_AND_HISTORY_READY')
