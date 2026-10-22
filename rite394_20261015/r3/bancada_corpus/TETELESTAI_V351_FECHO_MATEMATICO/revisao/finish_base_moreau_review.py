from pathlib import Path
import datetime, hashlib, json, os
R=Path(__file__).resolve().parents[1]
O=R/'revisao/base_moreau_independent_20260914_090556_274602'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,b):
    assert not p.exists(),str(p)
    if not isinstance(b,bytes): b=(json.dumps(b,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f: f.write(b)
    assert t.read_bytes()==b
    os.replace(t,p)
def link(label,p): return f'[{label}](<{p.as_posix()}>)'
c=read(O/'compilation.json');p=read(O/'preflight.json')
assert all(c[k] is True for k in ['all_exit_zero','exact_targets','trio_only','pins_preserved','binary_byte_equal_to_author'])
assert all(sha(path)==h for path,h in p['pins'].items())
source=R/'kernel/TGLExt/V351BaseMoreauApproximants.lean'
binary=R/'build/TGLExt/V351BaseMoreauApproximants.olean'
assert sha(source)==c['module']['source_sha256']
assert sha(binary)==c['module']['object_sha256']==sha(O/'build/TGLExt/V351BaseMoreauApproximants.olean')
for label in ['module','auditor']:
    for stream in ['stdout','stderr']:
        assert sha(O/f'{label}.{stream}.txt')==c[label][f'{stream}_sha256']
neg=R/'attempts/20260914_090247_321102'
nr=read(neg/'run.json');ns=(neg/'stdout.txt').read_text(encoding='utf-8')
assert nr['returncode']==1 and 'sorryAx' in ns and ': error:' in ns
assert 'object file' not in ns and 'unknown module prefix' not in ns
neg_source=Path(nr['command'][-1]);assert sha(neg_source)==nr['source_sha256']
audit=read(R/'AUDITORIA_A1_APROXIMANTES_BASE.json')
assert audit['source_sha256']==sha(source) and audit['object_sha256']==sha(binary)
assert audit['negative']['sha256']==sha(neg_source)
save(O/'author_negative_readback.json',{'rerun':False,'run':nr,'run_sha256':sha(neg/'run.json'),
    'stdout_sha256':sha(neg/'stdout.txt'),'stderr_sha256':sha(neg/'stderr.txt'),
    'source_sha256':sha(neg_source),'real_elaboration_error':True,'sorryAx':True})
history=read(O/'author_history.json')
rejected=[d for d in history if not d['accepted']]
assert len([d for d in rejected if d['returncode']==1])==4
assert len([d for d in rejected if d['returncode']==0])==1
stamp=datetime.datetime.now().astimezone().isoformat()
report=R/'revisao/REVIEW_A1_APROXIMANTES_BASE_FINAL.md'
lines=source.read_text(encoding='utf-8').splitlines()
loc=lambda n: next(i for i,line in enumerate(lines,1) if line.startswith('theorem '+n))
body=f'''# Parecer independente — aproximantes positivos na base

{stamp}

**[REAL] DEV aceito no escopo de um módulo/três teoremas, sem achados P0–P2.** Fonte final lida integralmente, hipóteses e tipos conferidos, recompilação própria e auditor separado rc0, sem avisos. O binário produzido coincide byte a byte com o autoral. Não resta análise necessária deste delta.

| Declaração (`TGLV351`) | Tipos e alcance conferidos |
|---|---|
| `dualResolvent_minimum_energy_value` (linha {loc('dualResolvent_minimum_energy_value')}) | Hilbert complexa completa genérica; A≥0 e R dado como limite forte dos resolventes de cortes. Identifica a energia no minimizador com `ofReal(Re⟨v,(I−R)v⟩)`. |
| `exists_base_moreau_approximant` (linha {loc('exists_base_moreau_approximant')}) | Para todo P, input positivo A do mesmo core e c>0, existe D na base original, 0≤D≤cI, que representa o mínimo atingido para todo vetor regular e todos os competidores. |
| `exists_monotone_base_dual_approximation` (linha {loc('exists_monotone_base_dual_approximation')}) | Existe uma sequência D:ℕ→B(Hbase), escolhida antes dos vetores, positiva, pertencente à base e crescente na ordem dos operadores, recuperando q_A por supremo em ENNReal para **todo** vetor regular. |

No primeiro lema, `toReal` é usado após provar finitude de q_A(Rv). A orientação do produto interno é reconciliada pela simetria da parte real; não se supõe que os valores de q_A em vetores arbitrários sejam finitos.

No segundo, A/c mantém pertinência e positividade. O fornecedor existente produz R positivo, contrativo e fixo, com seu limite forte; essas premissas não ficam a cargo do consumidor final. B=c(I−R) pertence a F e satisfaz 0≤B≤cI. A identificação concreta F=amplificação de M e `fibre_nonneg_iff`/`fibre_le_iff` transportam a pertinência e a **mesma ordem** até D∈M. A escala é cancelada em ENNReal usando c>0; a normalização da integral dual permanece herdada, sem redefinir Haar.

No terceiro, c=n+1 evita a escala zero. A comparação de mínimos dá monotonicidade das avaliações. Positividade e auto-adjunção, mais teste em `testVector v`, devolvem monotonicidade real dos CLM: não é apenas ordem de valores truncados por `ofReal`. Para s=sup das avaliações, a prova separa s=∞ de s<∞. No caso finito, minimizadores w_n satisfazem q_A(w_n)≤s e (n+1)‖w_n−v‖²≤s.toReal; daí w_n→v e o subnível fechado da forma dá q_A(v)≤s. A desigualdade inversa usa o competidor v. Não há densidade do domínio finito presumida, troca ∞→0 por `toReal`, circularidade com o predual ou hipótese de cota uniforme da forma.

A cota D≤cI está explicitamente exportada pelo segundo teorema. O último exporta positividade, pertinência, monotonicidade e supremo; não exporta a cota D_n≤(n+1)I nem os minimizadores como campos adicionais. Isso basta para a ponte por supremos de avaliações de operadores limitados planejada.

## Reuso, errata documental e limites

[REAL] Ficha MD/JSON e `ADENDO_REAPROVEITAMENTO_A1_APROXIMANTES_BASE.json` lidos. A grafia correta `exists_dualFormRepresentation`, linha 137 de V350DualFormRepresentation, foi conferida com seu hash e enunciado. A busca antiga com sublinhados foi negativa por grafia; **não demonstra ausência da representação completa**. O fornecedor já constrói representação/raiz no suporte; o novo delta fornece especificamente aproximantes limitados crescentes na base. Os registros antigos e a correção ao lado foram preservados.

[REAL] Este resultado é um avanço concreto para a ponte predual de A1(b): oferece os D_n positivos da mesma base, com recuperação da mesma integral em toda a representação regular. Não define ainda m_A em todos os funcionais normais positivos nem prova suas compatibilidades preduais. Isso permanece a próxima ligação delimitada descrita na {link('consulta Moreau/predual',R/'revisao/CONSULTA_A1_MOREAU_PREDUAL.md')}. Não se exige isomorfismo geral de cones para aceitar estes três teoremas.

**[OPEN] A1(b), existência/perturbação do traço escalado, não está pago por este módulo.** Nenhum KMS, traço, gate, runtime ou custódia nova é afirmado. Os pareceres {link('base estendida',R/'revisao/REVIEW_A1_BASE_ESTENDIDA_FINAL.md')} e {link('semifinitude escalar',R/'revisao/REVIEW_A1_SEMIFINITUDE_FINAL.md')} permanecem íntegros e sustentam seus próprios escopos; esta revisão conclui somente o delta dos aproximantes.

## Evidência e proveniência

Lean 4.31.0. Execução própria final: módulo rc0 em {c['module']['seconds']:.3f}s; auditor rc0 em {c['auditor']['seconds']:.3f}s. `#check` com universos e `#print axioms` exatamente dos três alvos: somente **propext, Classical.choice, Quot.sound**, inclusive transitivamente.

| Artefato | SHA256 lido por script |
|---|---|
| Fonte final | `{c['module']['source_sha256']}` |
| Binário próprio = autoral | `{c['module']['object_sha256']}` |
| stdout próprio do módulo | `{c['module']['stdout_sha256']}` |
| stdout próprio do auditor | `{c['auditor']['stdout_sha256']}` |
| Adendo de reuso | `{p['pins'][str(R/'ADENDO_REAPROVEITAMENTO_A1_APROXIMANTES_BASE.json')]}` |
| Manifesto conjunto de dependências | `{p['pins'][str(R/'DEPENDENCIAS_A1_MARCO_BASE.json')]}` |

Foram relidos os 384 pares fonte/binário do manifesto conjunto: 380 herdados e quatro V351. Isso é verificação de pins, não 384 recompilações. Nesta árvore foram reutilizados por cópia 382 objetos da árvore própria de semifinitude: os 380 antigos são binários herdados, e dois pais V351 já tinham recompilação própria. Os pacotes externos são somente leitura e não foram reconstruídos. O LEAN_PATH final contém o build próprio e os pacotes, sem build autoral de projeto.

A primeira tentativa própria `base_moreau_independent_20260914_090448_645300` rc1 é preservada: o novo prefixo TGLExt ocultou a resolução do objeto pai existente na árvore anterior. A preparação foi corrigida copiando os objetos pinados ao novo build, sem alterar nenhuma fonte Lean nem recompilar dependências. A execução final ocorreu em `base_moreau_independent_20260914_090556_274602`.

Histórico autoral relido: quatro rc1 excluídos e um rc0 intermediário com aviso/snapshot anterior, não utilizado para aceitar a fonte final; somente `attempts/20260914_090140_683505` é o run final aceito. O negativo +1 em `090247_321102` foi **relido, não reexecutado**: rc1 por elaboração matemática e `sorryAx`, sem falha de ambiente. `AUDITORIA_A1_APROXIMANTES_BASE.json` é evidência autoral; os seis controles ali nomeados não são apresentados como seis testes executados pelo revisor.

Evidências próprias: {link('compilation.json',O/'compilation.json')}, {link('auditor.stdout.txt',O/'auditor.stdout.txt')}, {link('preflight.json',O/'preflight.json')}, {link('author_history.json',O/'author_history.json')}, {link('verification.json',O/'verification.json')}.

[REAL] Pins das fontes, binário final, fichas, `um.py` e pareceres anteriores reconferidos sem alteração. Todas as escritas ficaram em revisao/. Nenhum programa autoral, integrador, recorder ou monólito foi executado; memórias e originais intocados.
'''
save(report,body.encode('utf-8'))
verification={'time':stamp,'status':'DEV_ACCEPTED_NO_P0_P2','scope':'V351BaseMoreauApproximants: 3 targets',
    'compilation':c,'pins_preserved':True,'report':{'path':str(report),'sha256':sha(report)},
    'milestone_records_read':384,'dependencies_rebuilt':False,'author_negative_rerun':False,
    'A1_b_paid':False,'predual_value_constructed':False,'source':{'path':str(source),'sha256':sha(source)},
    'binary':{'path':str(binary),'sha256':sha(binary)},
    'evidence_pins':{str(O/f):sha(O/f) for f in ['compilation.json','preflight.json','author_history.json','author_negative_readback.json','dependencies.json','milestone_manifest_verified.json','module.stdout.txt','auditor.stdout.txt']}}
save(O/'verification.json',verification)
print(json.dumps(verification['report'],ensure_ascii=False))
print('FINAL_REVIEW_COMPLETE')
