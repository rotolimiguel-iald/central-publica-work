from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parents[1]
O=R/'revisao/functional_evaluation_independent_20260914_093032_161654'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def atomic(p,data):
    assert not p.exists(),str(p)
    if isinstance(data,str): data=data.encode('utf-8')
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(data)
    assert t.read_bytes()==data
    os.replace(t,p)
c=read(O/'compilation.json');p=read(O/'preflight.json');history=read(O/'author_history.json')
assert all(c[k] for k in ['all_exit_zero','exact_targets','trio_only','binary_byte_equal_to_author','pins_preserved'])
assert all(sha(path)==h for path,h in p['pins'].items())
source=R/'kernel/TGLExt/V351BaseFunctionalEvaluation.lean'
lines=source.read_text(encoding='utf-8').splitlines()
declarations=[]
for i,line in enumerate(lines,1):
    m=re.match(r'^(def|theorem)\s+(\w+)',line)
    if m:
        name='TGLV351.'+m[2]
        declarations.append({'name':name,'kind':m[1],'source_line':i,'axioms':c['auditor']['axioms'][name]})
assert len(declarations)==21
ficha=read(R/'REAPROVEITAMENTO_A1_AVALIACAO_FUNCIONAL.json')
for x in ficha['providers']:
    assert sha(x['file'])==x['sha256'],x['file']
    assert x['statement'] in Path(x['file']).read_text(encoding='utf-8'),x['declaration']
ficha_pins={str(R/f):sha(R/f) for f in ['REAPROVEITAMENTO_A1_AVALIACAO_FUNCIONAL.md','REAPROVEITAMENTO_A1_AVALIACAO_FUNCIONAL.json']}
for f in ficha_pins: atomic(O/Path(f).name,Path(f).read_bytes())
def link(path,label,line=None):return f'[{label}](<{Path(path).as_posix()}{":"+str(line) if line else ""}>)'
def src(name):
    d=next(d for d in declarations if d['name']=='TGLV351.'+name)
    return link(source,name,d['source_line'])
report=R/'revisao/REVIEW_A1_AVALIACAO_FUNCIONAL_FINAL.md'
evidence=R/'revisao/REVIEW_A1_AVALIACAO_FUNCIONAL_FINAL.json'
stamp=datetime.datetime.now().astimezone().isoformat()
bad=[h for h in history if h['returncode']!=0]
oldgreen=[h for h in history if h['returncode']==0 and not h['accepted']]
text=f'''# Revisão independente — avaliação funcional na base

{stamp}

`A1_AVALIACAO_FUNCIONAL_DEV_REVIEW`

**[REAL] Aprovado o delta DEV delimitado: 21 declarações (3 definições e 18 teoremas). Nenhum achado P0, P1 ou P2.** Fonte inteira, tipos impressos com universos e dependências axiomáticas conferidos; recompilação própria do módulo e auditor separado rc0, sem warnings. A1(b) permanece **[OPEN]**.

## Evidência própria e pins

| Artefato | SHA256 lido |
|---|---|
| V351BaseFunctionalEvaluation.lean, autor/snapshot próprio | `{c['module']['source_sha256']}` |
| .olean autoral e .olean produzido independentemente, bytes iguais | `{c['module']['object_sha256']}` |
| Run autoral final 20260914_092635_416376 | `{sha(R/'attempts/20260914_092635_416376/run.json')}` |
| Manifesto DEPENDENCIAS_A1_MARCO_BASE.json | `{sha(R/'DEPENDENCIAS_A1_MARCO_BASE.json')}` |
| Ficha de reaproveitamento JSON | `{sha(R/'REAPROVEITAMENTO_A1_AVALIACAO_FUNCIONAL.json')}` |

Compilador Lean 4.31.0, mesmo executável pinado: `{p['compiler_sha256']}`. Módulo próprio: **{c['module']['seconds']:.3f}s**; auditor próprio: **{c['auditor']['seconds']:.3f}s**, ambos rc0. Os 21 conjuntos de axiomas coincidem com o stdout autoral e contêm somente `propext`, `Classical.choice`, `Quot.sound` (anotações de universo normalizadas apenas na comparação). Não há `sorry`, `axiom`, `native_decide`, `trustCompiler`, `unsafe` ou desvio de verificação na fonte examinada.

Árvore: {link(O,O.name)}. Evidência de execução: {link(O/'compilation.json','compilation.json')}; tipos completos e axiomas: {link(O/'auditor.stdout.txt','auditor.stdout.txt')}; cadeia de dependências: {link(O/'dependencies.json','dependencies.json')}. O {link(evidence,'JSON deste parecer')} lista nominalmente os 21 alvos, locadores, pins e limites.

**Herança declarada:** releitura dos 384 pares fonte/objeto do manifesto. Foram reutilizados 383 objetos da árvore própria Moreau anterior: 380 binários antigos herdados, sem recompilação nesta revisão, e três pais V351 antes recompilados independentemente. O quarto V351 do manifesto é o contrato: seus bytes foram conferidos, mas ele não precisou entrar na árvore de imports. O `LEAN_PATH` contém apenas a nova árvore de projeto e nove diretórios de pacotes externos readonly; não contém build de projeto autoral. Pacotes não foram reconstruídos; o import direto adicional `Lebesgue.Countable` e o compilador foram pinados. Não se reivindica reconstrução independente de toda a biblioteca. Fonte, objeto autoral, cópias de dependências, manifesto, programa apenas lido por hash e parecer Moreau permaneceram com os pins verificados.

## Significado e hipóteses efetivamente conferidos

1. **Mesma base e mesma forma.** `baseDualApproximant` escolhe a sequência existente, com pertinência no subtipo da mesma M, positividade e monotonicidade reais. A avaliação usa seu supremo em ENNReal. {src('baseDualEvaluation_vector')} identifica o valor com `baseDualWeight` no vetor da base, portanto com a integral dual em `testVector`. {src('baseDualEvaluation_vacuum')} já fornece o consumidor concreto `m_A(ω_Ω)=scalarDualWeight P A`, sem novo Haar ou nova representação.
2. **Funcional construído, não postulado.** {src('exists_base_series_functional')} recebe somente P, a sequência e `Summable (fun k => ‖v k‖^2)`. A cota {src('baseVectorFunctional_norm_le')} torna somável a série no espaço de funcionais contínuos complexos. A avaliação contínua transporta seu `HasSum` para cada D∈M. A representação não é uma hipótese residual do teorema existencial; o mesmo ψ serve a todos os inputs positivos A. A completude utilizada é a do espaço de funcionais, sem hipótese adicional de completude do subtipo M.
3. **Positividade complexa e orientação.** O produto interno tem v na primeira variável e Dv na segunda, logo é linear em D. `0 ≤ ψ D` usa `ComplexOrder`: parte real não negativa **e** parte imaginária zero, como explicita `Complex.nonneg_iff`. Não foi reduzida indevidamente à primeira dessas condições.
4. **HasSum e infinito.** {src('baseFunctional_hasSum_positive_evaluation')} passa ao valor ENNReal usando a soma real convergente e termos não negativos. {src('baseFunctional_hasSum_square_norm')} recupera a somabilidade quadrática pela unidade. Não há uso de `tsum` complexo divergente como evidência. A soma de valores duais finais pode ser infinita; não se introduz `toReal` dessa soma.
5. **Independência das decomposições.** {src('baseDualEvaluation_series_independent')} prova que duas representações positivas do mesmo ψ têm a mesma soma de valores da forma já integrada, via o supremo dos mesmos D_n. As hipóteses fracas desse lema dizem igualdade de avaliações ENNReal sobre D≥0; não dizem, sozinhas, igualdade complexa de funcionais. Os lemas `HasSum` e a construção existencial fornecem representações complexas genuínas que satisfazem essas hipóteses. A independência após a média é efetiva nesse sentido; não é afirmada independência de um levantamento ao core **antes** da média.
6. **Leis no argumento funcional.** Aditividade requer ψ e χ complexamente positivos. Escala NNReal inclui zero e valores infinitos. `baseDualEvaluation_zero` é zero no **funcional**, não um teorema novo sobre o input A=0. O lema de convergência monótona troca supremo e soma pela medida de contagem, sem impor finitude total.
7. **Topologia exata.** {src('baseDualEvaluation_lowerSemicontinuous')} usa a topologia padrão da norma de operadores em `M →L[ℂ] ℂ`: supremo de avaliações contínuas compostas com Re/ofReal. Não afirma semicontinuidade ultra-fraca nem identificação com uma topologia predual já construída.

## Limites e histórico

`baseDualEvaluation` é total em todos os funcionais contínuos; isso não os torna positivos ou normais. Este delta não prova a cobertura de todos os funcionais normais positivos por séries, não constrói um predual de Banach/quociente com dualidade, nem prova normalidade por ordem dos funcionais construídos. As leis consumidoras no input A, a interface padrão necessária à perturbação e a produção de τ não são certificadas por esta revisão. São limites explícitos, sem achado P2 por sua mera abertura.

A ficha MD/JSON foi lida e os {len(ficha['providers'])} fornecedores pinados foram confrontados às fontes/enunciados. Ela preserva a fronteira acima. Histórico preservado: {len(bad)} tentativas autorais rc1 com `sorryAx` visível foram excluídas; {len(oldgreen)} tentativa anterior rc0 com warning também não é a fonte final aceita. Ver {link(O/'author_history.json','author_history.json')}. Não houve falha na recompilação própria desta rodada. Uma busca auxiliar usou inicialmente o caminho inexistente `Data/Complex/Order.lean`; o arquivo correto `Analysis/Complex/Order.lean` foi localizado e lido, sem efeito na compilação ou na conclusão.

O controle negativo anunciado pelo autor não foi executado nem usado como condição de aceite desta revisão. Não houve integração, execução/importação de `um.py`, recorder, escrita em fontes ou memórias. **Não resta análise necessária dentro deste delta de 21 declarações. Aprovação DEV parcial; A1(b), traço e consumo final continuam abertos.**
'''
atomic(report,text)
ev={'time':stamp,'status':'APPROVED_DEV_21__A1B_OPEN','findings':[],'P0':0,'P1':0,'P2':0,
    'report':{'path':str(report),'sha256':sha(report)},'source':{'path':str(source),'sha256':sha(source)},
    'author_object_sha256':p['author_binary_sha256'],'independent_compilation':c,'declarations':declarations,
    'evidence_files':{str(O/n):sha(O/n) for n in ['preflight.json','compilation.json','dependencies.json','author_history.json','auditor.stdout.txt','module.stdout.txt','milestone_manifest_verified.json']},
    'ficha_pins':ficha_pins,'provider_pins_verified':len(ficha['providers']),
    'provenance':p['provenance'],'manifest_records_verified':384,
    'scope_limits':['Norm LSC only','No all-normal-functional vector-series coverage','No Banach predual identification',
        'No order-normality theorem for constructed functionals in this delta','No pre-average lift independence',
        'A-input consumer laws and trace construction outside scope','Author negative not executed/reviewed',
        'No full package/dependency rebuild','No integration/monolith/recorders/memory writes'],
    'final_recheck':{'pins_preserved':all(sha(path)==h for path,h in p['pins'].items()),'report_hash_verified':True}}
assert ev['final_recheck']['pins_preserved']
atomic(evidence,json.dumps(ev,ensure_ascii=False,indent=2)+'\n')
assert read(evidence)['report']['sha256']==sha(report)
print(json.dumps({'report':str(report),'sha256':sha(report),'evidence':str(evidence),'evidence_sha256':sha(evidence),'findings':0},ensure_ascii=False))
