from pathlib import Path
import datetime,hashlib,json,os,sys
R=Path(__file__).resolve().parent;OUT=R.parent.parent/'TUNEL/DO_CHATGPT'
SPECS={
 'core':dict(audit='AUDITORIA_ACAO_CORE_A1B',review='revisao_core/REVIEW_A1_CORE_FINAL',status='A1_CORE_ACTION_REVIEW_ACCEPTED__TRACE_OPEN',name='acao_modular_no_core_inteiro',title='A ação das potências do mesmo Tomita no core inteiro',theorems=5,definitions=0,docs=['REAPROVEITAMENTO_A1B_ESQUERDA','REAPROVEITAMENTO_A1B_ACAO_CORE'],description='O mesmo U_t, construído do resolvente de S†S no GNS do peso escalar, satisfaz U_t π(A)x=π(Λ_t A Λ_t*)U_t x para todo A no core concreto. A prova passa das unidades matriciais aos níveis, à base e ao core usando os fornecedores existentes. A fase do transporte esquerdo é conjugada por J. Não se afirma U_t=π(Λ_t): o operador relativo pode estar no comutante.',limit='Não constrói o gerador regular positivo afiliado nem o traço. Não acrescenta uma formalização separada da condição analítica KMS.'),
 'absorption':dict(audit='AUDITORIA_ABSORCAO_A1B',review='revisao_absorcao/REVIEW_A1_ABSORPTION_FINAL',status='A1_ABSORPTION_REVIEW_ACCEPTED__POSITIVE_GENERATOR_TRACE_OPEN',name='absorcao_do_fluxo_regular',title='A absorção do fluxo na representação regular existente',theorems=4,definitions=2,docs=['REAPROVEITAMENTO_A1B_ABSORCAO'],description='O campo unitário W já construído por operatorFieldLift satisfaz W S_t W*=Λ_t no mesmo L²(ℝ,H), com S_t f(x)=f(x−t). A família usa o fluxo da torre existente; não introduz um segundo espaço regular. O parâmetro auxiliar da família é matemático, não um acoplamento físico.',limit='Não afirma W∈N, não identifica potências do gerador, não produz o traço.'),
 'fourier':dict(audit='AUDITORIA_FOURIER_TRANSLACAO_A1B',review='revisao_fourier/REVIEW_A1_FOURIER_FINAL',status='A1_FOURIER_TRANSLATION_REVIEW_ACCEPTED__GENERATOR_TRACE_OPEN',name='fourier_da_translacao_regular',title='A Fourier existente lê a translação regular',theorems=3,definitions=0,docs=['REAPROVEITAMENTO_A1B_FOURIER_TRANSLACAO','ADENDO_FICHA_FOURIER_TRANSLACAO'],description='Na convenção de Fourier da mathlib, F S_t=M_(2πt) F no L² vetorial existente. A prova usa primeiro Schwartz e depois sua densidade e a isometria já fornecidas. Não redefine Fourier, translação ou multiplicador de caracteres.',limit='A identidade de Fourier isolada não é uma identificação das potências de um gerador construído, nem fornece afiliação ou traço.'),
 'graph':dict(audit='AUDITORIA_GRAFO_POSITIVO_A1B',review='revisao_grafo/REVIEW_A1_POSITIVE_GRAPH_FINAL',status='A1_POSITIVE_REGULAR_GRAPH_REVIEW_ACCEPTED__POWERS_AFFILIATION_TRACE_OPEN',name='grafo_positivo_regular',title='O grafo positivo no espaço regular concreto',theorems=12,definitions=3,docs=['REAPROVEITAMENTO_A1B_GERADOR_POSITIVO','ADENDO_GERADOR_ANTECEDENTE_ESCALAR'],description='V=W F⁻¹ transporta o multiplicador sigmoid(2πξ) ao resolvente R no espaço regular original. Foram provados 0≤R≤1, injetividade de R e 1−R, e as propriedades do grafo h=(1−R)/R com domínio RanR: fechado, densamente definido, autoadjunto, positivo e núcleo zero. A construção de grafo e suas propriedades gerais são fornecedores reutilizados. O antecedente escalar em L²(ℝ,ℂ) não podia ser instanciado diretamente no L² vetorial; a adaptação fica documentada.',limit='O delta constrói o grafo positivo; não identifica ainda h^it com Λ_t, não afirma afiliação nem escala dual, nem fornece RegularCoreTraceData.'),
 'spectral':dict(audit='AUDITORIA_GRAFO_ESPECTRAL_A1B',review='revisao_grafo_espectral/REVIEW_A1_SPECTRAL_GRAPH_FINAL',status='A1_SPECTRAL_GRAPH_REVIEW_ACCEPTED__POWERS_AFFILIATION_TRACE_OPEN',name='identificacao_espectral_do_mesmo_grafo',title='O mesmo grafo é a multiplicação exponencial em coordenadas espectrais',theorems=3,definitions=0,docs=['REAPROVEITAMENTO_A1B_GRAFO_ESPECTRAL'],description='Para x,y no espaço regular original, (x,y) pertence ao grafo positivo já construído se e somente se V⁻¹y(ξ)=e^(−2πξ)V⁻¹x(ξ) quase em toda parte. A condição especifica o domínio da multiplicação não limitada em classes L². Consome a equação resolvente existente e as identidades de sigmoid; não cria outro gerador, grafo ou domínio.',limit='A identificação do grafo não substitui a identificação de suas potências imaginárias, afiliação, escala dual ou construção do traço.')}
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def put(p,b):
 assert (p.is_relative_to(R) or p.is_relative_to(OUT)) and not p.exists(),p
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b and b;os.replace(t,p)
key=sys.argv[1];config=R/'delivery_configs'/(key+'.json');q=load(config) if config.exists() else SPECS[key]
ap=R/(q['audit']+'.json');rp=R/(q['review']+'.json');rmd=R/(q['review']+'.md')
a=load(ap);v=load(rp);cp=Path(v['compilation']['path']);c=load(cp)
assert v['status']==q['status'],v['status']
full_trace=q.get('full_trace_constructed',False)
assert full_trace == a.get('full_trace_constructed',False) == v.get('full_trace_constructed',False)
trace_label='contrato do traço concreto construído' if full_trace else 'traço concreto ainda OPEN'
trace_table='PAGO: mesmo peso, todas as leis do contrato.' if full_trace else 'NÃO PAGO por esta entrega.'
assert all(not v[k] for k in ['P0','P1','P2']) and not v['findings']
assert a['new_theorems']==q['theorems'] and a.get('new_definitions',0)==q['definitions']
assert c['exact_target_count']==q['theorems']+q['definitions']
assert c['new_theorems']==q['theorems'] and c['new_definitions']==q['definitions']
assert a['all_axioms_allowed'] and c['all_axioms_allowed'] and a['negative_controls_rejected']
assert not a['dev_objects_used'] and not c['dev_objects_used'] and not c['external_project_objects_inherited']
assert c['all_accepted_builds_exit_zero'] and c['all_target_typechecks_present'] and not c['targetwarnings']
assert c['all_prior_pins_preserved'] and v['all_prior_pins_preserved']
files=set([ap,rp,rmd,cp,Path(__file__)]);files.update([config] if config.exists() else [])
def check(obj):
 if isinstance(obj,dict):
  if {'path','bytes','sha256'}<=obj.keys():
   p=Path(obj['path']);assert pin(p)=={k:obj[k] for k in ['path','bytes','sha256']},p;files.add(p)
  for x in obj.values():check(x)
 elif isinstance(obj,list):
  for x in obj:check(x)
for obj in [a,v,c]:check(obj)
run=load(Path(a['positive_build']['path']));assert run['returncode']==0 and run['sources_unchanged_during_build'];check(run)
for stem in q['docs']:
 for ext in ['md','json']:
  p=R/(stem+'.'+ext);assert p.exists();files.add(p)
  if ext=='json':check(load(p))
types=load(Path(c['type_axiom_audit']['path']));check(types)
expected={t['name'] for t in a['targets']}
assert expected==set(types['types'])==set(a['axioms'])
stamp=datetime.datetime.now().astimezone().isoformat()
accept=dict(timestamp=stamp,status=q['status'],author_audit=pin(ap),independent_review=pin(rp),independent_compilation=pin(cp),theorems=q['theorems'],definitions=q['definitions'],new_trace_inhabitant=full_trace,gate_changed=False)
accept_path=R/('ACEITE_DELTA_'+key.upper()+'.json');put(accept_path,json.dumps(accept,ensure_ascii=False,indent=2).encode('utf8'));files.add(accept_path)
out=OUT/('ENTREGA_011_A1_'+q['name']+'.md')
body=f'''[REAL — {q['theorems']} teoremas e {q['definitions']} definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): {trace_label}.]

# ENTREGA 011 / A1 — {q['title']}

{stamp}

{q['description']}

{q['limit']}

## Critérios

| Critério | Resultado |
|---|---|
| Ficha anterior e consumidor nomeado | PAGO; fichas integrais anexas, fornecedores pinados. |
| Mesmos espaços e fornecedores | PAGO no alcance dos tipos abaixo; fontes antigas preservadas. |
| Lake isolado e tipos completos | PAGO; autor e revisor rc0, sem herança de objetos DEV. |
| Axiomas | PAGO; somente propext, Classical.choice e Quot.sound, ou subconjuntos. |
| Adulteração | PAGO; controles autorais recusados por TypeMismatch; alcance e eventual leitura do revisor discriminados em seu parecer. |
| Revisão distinta da autoria | PAGO; nenhuma pendência P0/P1/P2 no delta. |
| Habitante do contrato do traço | {trace_table} |
| Incorporação ao um.py / mudança de gate | NÃO EXECUTADA; escopo da gerência. |

## Reprodução

Autor: `{a['positive_build']['path']}`. Comando registrado: `{run['command']}`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `{v['run']['path']}`. `{c['own_previous_project_object_count']}` objetos próprios anteriores; `{c['newly_recompiled_old_supplier_count']}` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `{len(c['targetwarnings'])}` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
'''
for m in a['modules']:body+=f"| `{m['name']}` | `{m['source']['sha256']}` | `{m['object']['sha256']}` |\n"
body+='\n## Tipos completos e axiomas\n\n'
for t in a['targets']:
 name=t['name'];body+='```lean\n'+types['types'][name]+'\n```\n\nAxiomas: '+', '.join(a['axioms'][name])+'.\n\n'
body+='## Custódia e limites\n\n'
for p in [ap,rp,cp,accept_path]:body+=f"- `{p}` — SHA256 `{pin(p)['sha256']}`.\n"
body+='\nO manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.\n\n## Revisão independente integral\n\n'+rmd.read_text(encoding='utf8')
for stem in q['docs']:body+='\n\n## Ficha/adendo integral: '+stem+'\n\n'+(R/(stem+'.md')).read_text(encoding='utf8')
put(out,body.encode('utf8'));files.add(out)
manifest=R/('MANIFESTO_DELTA_'+key.upper()+'.json')
m=dict(timestamp=stamp,status=q['status'],files=[pin(p) for p in sorted(files,key=str)])
put(manifest,json.dumps(m,ensure_ascii=False,indent=2).encode('utf8'))
receipt=R/('RECIBO_DELTA_'+key.upper()+'.json')
put(receipt,json.dumps(dict(timestamp=stamp,delivery=pin(out),manifest=pin(manifest),acceptance=pin(accept_path)),ensure_ascii=False,indent=2).encode('utf8'))
for entry in m['files']:assert pin(Path(entry['path']))==entry
print(json.dumps(dict(delivery=pin(out),receipt=pin(receipt),files=len(files)),ensure_ascii=False))
