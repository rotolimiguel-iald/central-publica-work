from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parents[1]
O=R/'revisao/series_normality_independent_20260914_094019_216956'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def atomic(p,data):
    assert not p.exists(),str(p)
    if isinstance(data,str):data=data.encode('utf-8')
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(data)
    assert t.read_bytes()==data;os.replace(t,p)
c=read(O/'compilation.json');p=read(O/'preflight.json');hist=read(O/'author_history.json')
assert all(c[k] for k in ['all_exit_zero','exact_targets','trio_only','binary_byte_equal_to_author','pins_preserved'])
assert all(sha(x)==h for x,h in p['pins'].items())
source=R/'kernel/TGLExt/V351BaseSeriesNormality.lean'
decls=[]
for i,line in enumerate(source.read_text(encoding='utf-8').splitlines(),1):
    m=re.match(r'^theorem\s+(\w+)',line)
    if m:decls.append({'name':'TGLV351.'+m[1],'line':i,'axioms':c['auditor']['axioms']['TGLV351.'+m[1]]})
assert len(decls)==4
author_controls=[]
for name in ['AUDITORIA_A1_AVALIACAO_FUNCIONAL.json','AUDITORIA_A1_LEIS_FUNCIONAIS.json']:
    a=read(R/name)
    assert sha(a['source'])==a['source_sha256']
    obj=R/'build/TGLExt'/(Path(a['source']).stem+'.olean')
    assert sha(obj)==a['object_sha256']
    assert sha(a['negative']['path'])==a['negative']['sha256']
    atomic(O/name,(R/name).read_bytes())
    author_controls.append({'path':str(R/name),'sha256':sha(R/name),'scope':'author report read, source/object/probe pins checked; negative execution not repeated',
        'status_reported':a['status'],'negative_reported':a['negative']})
def link(path,label,line=None):return f'[{label}](<{Path(path).as_posix()}{":"+str(line) if line else ""}>)'
report=R/'revisao/REVIEW_A1_NORMALIDADE_SERIES_FINAL.md'
evidence=R/'revisao/REVIEW_A1_NORMALIDADE_SERIES_FINAL.json'
stamp=datetime.datetime.now().astimezone().isoformat()
text=f'''# Revisão independente — normalidade das séries na base

{stamp}

`A1_NORMALIDADE_SERIES_DEV_REVIEW`

**[REAL] Aprovado o delta DEV de quatro teoremas. Nenhum P0, P1 ou P2; nenhuma lacuna formal identificada exige controle adicional neste escopo.** Fonte inteira lida, tipos com universos conferidos, recompilação própria e auditor separado rc0 sem avisos. A1(b) permanece **[OPEN]**.

## Pins e execução própria

| Artefato | SHA256 lido |
|---|---|
| Fonte V351BaseSeriesNormality.lean, autor e snapshot próprio | `{c['module']['source_sha256']}` |
| .olean autoral e próprio, igualdade byte a byte | `{c['module']['object_sha256']}` |
| Run autoral 20260914_093715_947928 | `{sha(R/'attempts/20260914_093715_947928/run.json')}` |
| Ficha REAPROVEITAMENTO_A1_NORMALIDADE_SERIES.json | `{sha(R/'REAPROVEITAMENTO_A1_NORMALIDADE_SERIES.json')}` |

Mesmo Lean 4.31.0, executável SHA `{p['compiler_sha256']}`. Módulo próprio **{c['module']['seconds']:.3f}s**; auditor próprio **{c['auditor']['seconds']:.3f}s**. Os quatro `#check` e `#print axioms` confirmam somente `propext`, `Classical.choice`, `Quot.sound`; nenhum `sorry`, `axiom`, `native_decide`, `trustCompiler`, `unsafe` ou substituição de prova no candidato. Universos de ι permanecem arbitrários.

{link(O/'compilation.json','Compilação própria')}; {link(O/'auditor.stdout.txt','tipos/axiomas completos')}; {link(O/'dependencies.json','dependências pinadas')}; {link(evidence,'JSON do parecer')}.

Reutilizados **385 objetos próprios**: 380 antigos herdados, não reconstruídos aqui, e cinco módulos V351 já recompilados independentemente (forma-base, semifinitude, Moreau, avaliação e leis funcionais). Fontes/cópias conferidas por hash. Pacotes externos readonly e não reconstruídos; nenhum build de projeto autoral no `LEAN_PATH`. Essa lista ampliada é distinta do manifesto anterior de 384 entradas. Não houve rebuild de GNS/peso ou alteração de fonte, objeto autoral, programa/memória ou parecer anterior.

## Tipos e argumento conferidos

1. `positive_base_functional_real_mono`: positividade complexa de ψ sobre D≥0 torna monotônica a leitura ENNReal/ofReal/Re. O argumento usa ψ(B−A)=ψ(B)−ψ(A); não pressupõe normalidade.
2. `baseSeriesFunctional_positive`: `HasSum` em todo D∈M transporta a soma de valores vetoriais positivos para ψ(D). `ComplexOrder` assegura simultaneamente realidade e parte real não negativa, não somente uma desigualdade após Re. A representação é consistente com o fornecedor existencial do módulo de avaliação; não há apelo a `tsum` divergente.
3. `baseVectorFunctional_normal`: A_i e S são elementos da **mesma base M**, a rede é positiva, crescente e tem S como supremo interno. A cota ‖A_i‖≤‖S‖ vem da ordem. O fornecedor `vonNeumann_exists_positive_isLUB` constrói D e convergência forte; a unicidade do supremo interno identifica D=S. Só então a continuidade do pareamento/ofReal e a monotonicidade dão a igualdade de supremos. Não é fornecida convergência forte como premissa nem aplicada continuidade SOT geral de funcionais limitados.
4. `baseSeriesFunctional_normal`: a positividade de S é deduzida usando não-vazio da rede; a leitura em ψ(S) e ψ(A_i) passa às séries ENNReal. A troca supremo/série usa o lema dirigido dos 12 teoremas anteriores. `ι : Type u`, `Preorder`, `IsDirectedOrder`, `Nonempty` são as hipóteses exatas; não há Countable ι ou hipótese de separabilidade de H.

O resultado final é exatamente

    ofReal (Re ψ(S)) = sup_i ofReal (Re ψ(A_i)),   A_i ≥ 0,

para supremos internos dessas redes. A positividade complexa impede que a passagem a Re/ofReal esconda parte imaginária ou truncamento negativo no cone positivo. ψ(S) é finito por ser uma avaliação de um funcional limitado em um operador limitado. Esta normalidade é de **ψ no argumento da base**; a normalidade anterior de **A↦m_A(ψ) no core** tem tipos diferentes e não foi presumida como substituto.

## Alcance e controles

Ficha MD/JSON lida integralmente, quatro fornecedores confrontados por hash e enunciado. O módulo prova a direção **representação HasSum ⇒ funcional positivo normal por ordem**. Em conjunto com `exists_base_series_functional`, qualifica efetivamente o domínio representável das avaliações. Não prova o converso normal⇒série, cobertura de todo o predual, equivalência com WStar ou dualidade de Banach. Não produz traço ou fecha A1(b). Essas fronteiras são explícitas, não falhas do delta.

Uma tentativa autoral rc1 de 093630, com erro de tipo e `sorryAx` no output, foi retida/excluída. Apenas a versão final 093715 foi aceita; ver {link(O/'author_history.json','histórico')}. Nenhuma falha própria nesta rodada.

Foram relidos e pinados `AUDITORIA_A1_AVALIACAO_FUNCIONAL.json` e `AUDITORIA_A1_LEIS_FUNCIONAIS.json`, junto aos bytes atuais das fontes, objetos e probes a que apontam. Seus negativos são resultados **autorais**, não execuções próprias desta revisão. Não foi necessário repetir controles ou criar novo teste: a análise não encontrou preocupação concreta adicional. Não executados monólito, helpers de autoria, recorder ou integração.

**Revisão delimitada concluída.** As 12 leis anteriores permanecem no {link(R/'revisao/REVIEW_A1_LEIS_FUNCIONAIS_FINAL.md','parecer próprio já finalizado')}; este documento aceita somente os quatro teoremas adicionais. Memória/custódia/handoff do marco não foram escritos por esta revisão.
'''
atomic(report,text)
ev={'time':stamp,'status':'APPROVED_DEV_4__A1B_OPEN','findings':[],'P0':0,'P1':0,'P2':0,
    'report':{'path':str(report),'sha256':sha(report)},'source':{'path':str(source),'sha256':sha(source)},
    'author_object_sha256':p['author_object_sha256'],'independent_compilation':c,'declarations':decls,
    'evidence_files':{str(O/n):sha(O/n) for n in ['preflight.json','compilation.json','dependencies.json','author_history.json','auditor.stdout.txt','module.stdout.txt']},
    'author_controls_read_not_rerun':author_controls,'additional_control_required':False,
    'provenance':p['provenance'],'providers_verified':p['providers_verified'],
    'scope_limits':['HasSum implies positive order-normal, no converse','Normality of psi on M differs from A to m_A on N',
        'Internal positive nonempty directed nets with arbitrary index universe','No WStar/predual coverage/trace/A1b closure',
        'No monolith/integration/recorders/memory/dependency rebuild'],
    'final_pins_preserved':all(sha(x)==h for x,h in p['pins'].items())}
assert ev['final_pins_preserved']
atomic(evidence,json.dumps(ev,ensure_ascii=False,indent=2)+'\n')
assert read(evidence)['report']['sha256']==sha(report)
print(json.dumps({'report':str(report),'report_sha256':sha(report),'json':str(evidence),'json_sha256':sha(evidence),'findings':0},ensure_ascii=False))
