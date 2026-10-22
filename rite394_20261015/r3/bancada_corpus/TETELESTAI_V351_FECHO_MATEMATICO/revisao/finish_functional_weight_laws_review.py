from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parents[1]
O=R/'revisao/functional_laws_independent_20260914_093642_937361'
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
source=R/'kernel/TGLExt/V351BaseFunctionalWeightLaws.lean'
decls=[]
for i,line in enumerate(source.read_text(encoding='utf-8').splitlines(),1):
    m=re.match(r'^theorem\s+(\w+)',line)
    if m:decls.append({'name':'TGLV351.'+m[1],'line':i,'axioms':c['auditor']['axioms']['TGLV351.'+m[1]]})
assert len(decls)==12
def link(path,label,line=None):return f'[{label}](<{Path(path).as_posix()}{":"+str(line) if line else ""}>)'
def src(name):return link(source,name,next(d['line'] for d in decls if d['name']=='TGLV351.'+name))
report=R/'revisao/REVIEW_A1_LEIS_FUNCIONAIS_FINAL.md'
evidence=R/'revisao/REVIEW_A1_LEIS_FUNCIONAIS_FINAL.json'
stamp=datetime.datetime.now().astimezone().isoformat()
text=f'''# Revisão independente — leis funcionais da avaliação dual

{stamp}

`A1_LEIS_FUNCIONAIS_DEV_REVIEW`

**[REAL] Delta DEV aprovado: 12 teoremas, nenhum achado P0, P1 ou P2.** Fonte inteira e tipos/axiomas examinados. Recompilação própria do módulo e auditor separado rc0, sem avisos; .olean próprio byte a byte igual ao autoral. **A1(b) permanece [OPEN].**

## Evidência e proveniência

| Artefato | SHA256 lido |
|---|---|
| V351BaseFunctionalWeightLaws.lean, autor e snapshot | `{c['module']['source_sha256']}` |
| .olean autoral / independente, bytes iguais | `{c['module']['object_sha256']}` |
| Run autoral final 20260914_093341_530178 | `{sha(R/'attempts/20260914_093341_530178/run.json')}` |
| Ficha REAPROVEITAMENTO_A1_LEIS_FUNCIONAIS.json | `{sha(R/'REAPROVEITAMENTO_A1_LEIS_FUNCIONAIS.json')}` |

Lean 4.31.0, executável SHA `{p['compiler_sha256']}`. Execução própria do módulo: **{c['module']['seconds']:.3f}s**; auditor: **{c['auditor']['seconds']:.3f}s**. Os 12 alvos foram impressos com `#check`, `pp.universes true` e `#print axioms`; conjuntos axiomáticos iguais aos autorais, somente `propext`, `Classical.choice`, `Quot.sound`. Fonte sem `sorry`, declaração `axiom`, `native_decide`, `trustCompiler`, `unsafe` ou mecanismo de substituição de prova.

Evidências: {link(O/'compilation.json','compilation.json')}, {link(O/'auditor.stdout.txt','tipos e axiomas completos')}, {link(O/'dependencies.json','dependencies.json')} e {link(evidence,'JSON deste parecer')}. Nomes e locadores dos 12 alvos constam no JSON.

Reutilizados **384 objetos da árvore própria**: 380 binários antigos herdados, não reconstruídos agora, e quatro pais V351 anteriormente recompilados de modo independente (forma-base, semifinitude, Moreau e avaliação). Todos os pares fonte/cópia foram repinados. Essa lista de 384 não é confundida com o manifesto antigo de mesmo número: naquele há contrato, aqui há o novo objeto da avaliação no lugar dele. `LEAN_PATH` exclusivo da nova árvore de projeto e nove diretórios de pacotes externos readonly; nenhum build de projeto autoral. Pacotes não reconstruídos. O parecer anterior, fonte, objeto autoral, manifesto de herança e `um.py` somente lido por hash permaneceram inalterados.

## Conteúdo matemático conferido

- **Hipótese de representação honesta.** As leis gerais recebem ψ contínuo complexo e uma sequência v com `HasSum` em **todo** D∈M. Não pressupõem representação para qualquer funcional normal. Essa hipótese tem fornecedor efetivo no módulo anterior para sequências quadrado-somáveis; a finitude da soma de normas pode ser recuperada pela unidade. Não se usa uma convenção de `tsum` divergente.
- **Leis no input A.** Zero/soma/escala/ordem agora são leis de A∈N⁺, herdadas da mesma `baseDualWeight` e transferidas por somas ENNReal. A escala NNReal cobre r=0, e valores infinitos não são convertidos para reais. Isto é consumo novo da avaliação, sem reconstruir peso ou GNS.
- **Redes arbitrárias.** {src('ennreal_tsum_iSup_directed')} aceita `ι : Type u` com preordem, direção e não-vazio; as somas finitas crescentes permitem trocar o supremo de ι com a série. Em {src('baseDualEvaluation_input_normal')}, A_i e S pertencem à **mesma** álgebra regular, `hpos`, `hmono` e `IsLUB (range A) S` são explícitos. A positividade de S é deduzida. Não há hipótese Countable ι, convergência forte dada ou supremo ambiente pressuposto: a passagem interna/ambiente vem do fornecedor já auditado. A normalidade é de A↦m_A(ψ), não um novo teorema de normalidade de ψ sobre a base.
- **Tonelli e descida após média.** {src('baseDualEvaluation_eq_dual_integral')} usa exatamente `dualQuadraticIntegrand A.val (testVector (v k)) s`, cuja definição contém `dualAmbient s A`, e `ofReal dualHaarFactor`, com `dualHaarFactor=(2*Real.pi)⁻¹`. A mensurabilidade é fornecida para cada termo; `lintegral_tsum` permite infinito, sem hipótese de integrabilidade finita. O resultado identifica a soma **já integrada** com m_A(ψ). Com a independência das séries aprovada no pai, a média independe da decomposição. Não identifica os levantamentos vetoriais ao core antes da média.
- **Bimódulo com χ explícito.** {src('baseDualEvaluation_bimodule')} usa a conjugação concreta de A por `fixedBaseEquiv P B` e supõe `HasSum` de χ com vetores `B.val (v k)`. O transporte por B está na hipótese e na prova; não foi substituído por um nome de funcional. O teorema não fornece sozinho uma definição canônica χ(D)=ψ(B*DB), nem empacota o cone/quociente; essas interfaces são adicionais. A hipótese é consistente e realizável pela estimativa ‖Bv_k‖²≤‖B‖²‖v_k‖² e pelo fornecedor existencial anterior, sem pedir um novo teorema como condição de aceite deste enunciado.
- **Output limitado.** {src('baseDualEvaluation_bounded_output')} exige D∈M, D≥0 e identidade quadrática limitada para **todos os vetores regulares**. Conclui avaliação desse mesmo D, sem supor que todo output seja limitado.
- **Fidelidade e controles.** {src('baseDualEvaluation_family_faithful')} testa a família inteira de funcionais vetoriais, equivalendo a A=0; a prova usa a fidelidade escalar existente via Ω. Não afirma fidelidade de cada ψ arbitrário. `baseDualEvaluation_averageSquare` recupera 1 no vetor Ω; `baseDualEvaluation_unit_infinite` recupera ∞ para w≠0. Nenhuma contradição com finitude de ψ em operadores limitados da base: ∞ é valor de m no input unidade do core.

## Alcance documental e limites

Ficha MD/JSON lida integralmente, {p['providers_verified']} fornecedores confrontados por hash e enunciado. O consumidor final `RegularCoreTraceData` é corretamente identificado como ainda não preenchido. Não há cobertura do predual inteiro, construção de predual por quociente, prova de normalidade por ordem de ψ, nova identificação KMS ou existência de traço. O arquivo posterior mencionado pelo autor permanece fora do escopo. Nenhum desses limites explícitos constitui P2 por si só.

Histórico: {sum(h['returncode']!=0 for h in hist)} tentativas autorais rc1 retidas e excluídas, ambas com `sorryAx` nos outputs; só os bytes finais rc0 de 093341 foram aceitos. Ver {link(O/'author_history.json','histórico pinado')}. A tentativa própria desta rodada não falhou. O controle negativo autoral é separado da reprodução independente e não foi reexecutado por esta revisão.

Não foram executados `um.py`, integradores, recorders ou novas provas de dependências; nenhuma fonte autoral, memória ou parecer anterior foi alterado. **Não resta verificação necessária no delta de 12 teoremas. Aceite DEV delimitado, sem promoção de A1(b).**
'''
atomic(report,text)
ev={'time':stamp,'status':'APPROVED_DEV_12__A1B_OPEN','findings':[],'P0':0,'P1':0,'P2':0,
    'report':{'path':str(report),'sha256':sha(report)},'source':{'path':str(source),'sha256':sha(source)},
    'author_object_sha256':p['author_object_sha256'],'independent_compilation':c,'declarations':decls,
    'evidence_files':{str(O/n):sha(O/n) for n in ['preflight.json','compilation.json','dependencies.json','author_history.json','auditor.stdout.txt','module.stdout.txt']},
    'provenance':p['provenance'],'providers_verified':p['providers_verified'],
    'scope_limits':['normality in A, not normality in psi','HasSum representation explicit','No complete predual coverage',
        'No pre-average lift independence','Chi existence/conjugation interface not packaged in candidate',
        'Bounded output has all-regular-vectors hypothesis','No trace/KMS/A1b closure',
        'No monolith/integration/recorders/dependency rebuild','Author negative not rerun'],
    'final_pins_preserved':all(sha(path)==h for path,h in p['pins'].items())}
assert ev['final_pins_preserved']
atomic(evidence,json.dumps(ev,ensure_ascii=False,indent=2)+'\n')
assert read(evidence)['report']['sha256']==sha(report)
print(json.dumps({'report':str(report),'report_sha256':sha(report),'json':str(evidence),'json_sha256':sha(evidence),'findings':0},ensure_ascii=False))
