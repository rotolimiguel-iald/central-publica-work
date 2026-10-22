"""Validate and publish an immutable delivery in our tunnel lane only."""
from pathlib import Path
from datetime import datetime
import hashlib, json, re

ROOT = Path(__file__).resolve().parent
assert str(ROOT) == r'C:\IALD\Central de Patentes\Chatgpt'
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
modules = ['TowerExpectation','ExpectationProjection','ExpectationBounded',
    'ExpectationBimodule','ExpectationPositive','ExpectationSlice',
    'ExpectationContractGap','LevelExpectationFamily']

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()

def create(p,data):
    assert p.is_relative_to(ROOT) and not p.exists(), p
    temp = p.with_name(p.name+'.tmp')
    with temp.open('xb') as stream: stream.write(data)
    assert temp.stat().st_size == len(data) > 0
    temp.rename(p)
    assert p.read_bytes() == data

def jscreate(p,obj):
    create(p,(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))

proofs,failed = [],[]
for module in modules:
    source = ROOT/(module+'.lean')
    metadata_file = sorted(ROOT.glob(module+'.*.json'))[-1]
    meta = json.loads(metadata_file.read_text(encoding='utf-8-sig'))
    assert meta['exit_code'] == 0 and meta['source_stable'], meta
    assert meta['proof_sha256'] == sha(source), module
    log_file = ROOT/meta['log']
    log = log_file.read_text(encoding='utf-8-sig')
    assert not any(s in log for s in ('sorryAx','error:','warning:')),log
    axiom_lists = re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S)
    assert axiom_lists,module
    for axioms in axiom_lists:
        assert {a.strip() for a in axioms.split(',')} <= {'propext','Classical.choice','Quot.sound'}, axioms
    code = source.read_text(encoding='utf-8-sig')
    assert not re.search(r'\b(sorry|admit|axiom)\b',code), module
    proofs.append({'module':module,'source':str(source),'source_sha256':sha(source),
        'theorems':len(re.findall(r'^theorem ',code,re.M)),
        'olean_sha256':sha(ROOT/(module+'.olean')),
        'metadata':str(metadata_file),'metadata_sha256':sha(metadata_file),
        'log':str(log_file),'log_sha256':sha(log_file),'axioms_printed':log.strip()})

for module in modules+['TGL','TGLExt']:
    for p in sorted(ROOT.glob(module+'.*.log')):
        text = p.read_text(encoding='utf-8-sig')
        if 'error:' in text or 'error(' in text or 'sorryAx' in text or 'warning:' in text:
            category = ('dependencia_ausente' if 'does not exist' in text else
                'colisao_imports' if 'environment already contains' in text else
                'timeout' if 'timeout' in text else
                'elaboracao' if 'error' in text or 'sorryAx' in text else 'aviso_linter')
            archived = p.with_name(p.name+'.falha_'+category)
            if not archived.exists(): create(archived,p.read_bytes())
            assert archived.read_bytes() == p.read_bytes()
            failed.append({'log':str(archived),'sha256':sha(archived),'defect':category})

manifest = json.loads((ROOT/'manifesto_fontes.json').read_text(encoding='utf-8-sig'))
rows = []
for item in manifest:
    row = {'source':item['source'],'copy':item['copy'],'baseline_sha256':item['sha256']}
    for label in ['source','copy']:
        try:
            digest = sha(Path(item[label]))
            row[label+'_sha256'] = digest
            row[label+'_unchanged'] = digest == item['sha256'].upper()
        except OSError as exc:
            row[label+'_unchanged'] = False
            row[label+'_error'] = str(exc)
    rows.append(row)
assert all(row['copy_unchanged'] for row in rows), 'Read-only source snapshots changed'
source_differences = sum(not r['source_unchanged'] for r in rows)
preservation_file = ROOT/f'preservacao_ordem001_{stamp}.json'
jscreate(preservation_file,{'timestamp':datetime.now().isoformat(),'rows':rows,
    'copies_checked':len(rows),'copies_changed':0,'originals_different_or_unreadable':source_differences,
    'attribution':'Hashes compare states, not authorship. Sister session is concurrently incorporating work. This bench writes only under Chatgpt.'})

dependencies = []
for directory in [ROOT/'TGL',ROOT/'TGLExt']:
    for p in sorted(directory.rglob('*')):
        if p.is_file(): dependencies.append({'file':str(p),'bytes':p.stat().st_size,'sha256':sha(p)})
for name in ['TGL.lean','TGLExt.lean','TGL.olean','TGLExt.olean']:
    p = ROOT/name
    dependencies.append({'file':str(p),'bytes':p.stat().st_size,'sha256':sha(p)})
deps_file = ROOT/f'dependencias_ordem001_{stamp}.json'
jscreate(deps_file,{'scope':'Binary snapshot of project dependencies; mathlib/toolchain not rebuilt',
    'files':dependencies})

scale = sorted(ROOT.glob('escala_controle_*.json'))[-1]
assert json.loads(scale.read_text(encoding='utf-8'))['scalar_curvature'] == ['12','3']
artifact_names = ['ESPERANCA_CONDICIONAL_TORRE.md','ESCALA_CONFORME_TAKESAKI.md',
    'check_scale_obstruction.py','reproduce_order001.ps1','verify_stage.ps1','finalize_order001.py',
    scale.name,preservation_file.name,deps_file.name]
artifacts = [{'path':str(ROOT/name),'sha256':sha(ROOT/name)} for name in artifact_names]
result = {'timestamp':datetime.now().isoformat(),'order':1,'proofs':proofs,
    'new_theorems':sum(p['theorems'] for p in proofs),'artifacts':artifacts,'failed_attempts':failed,
    'acceptance_A':{str(i):'PAGO' for i in range(1,10)},
    'A9_scope':'Exact type gap and formal no-go when P.w(0) != 1/2; not an inhabitant of ExpectationInput.',
    'complete_positivity':'DERIVED written, not formalized in Lean',
    'normality':'DERIVED written, not formalized in Lean',
    'geometry':'scale determination refuted without trace-to-geometry bridge; no CGMA network built from tower',
    'source_snapshots_preserved':True,'originals_different_or_unreadable':source_differences,
    'canonical_gate_changed_by_this_delivery':False}
result_file = ROOT/f'verificacao_ordem001_{stamp}.json'
jscreate(result_file,result)

criteria = [
('1','Mapa linear limitado, imagem no andar','expectationCLM; expectation_bounded; expectation_into'),
('2','Idempotência','expectation_idempotent'),
('3','Restrição ao andar','expectation_fixes'),
('4','Preservação de ω','expectation_preserves_state'),
('5','Bimodularidade sobre M','expectation_bimodular'),
('6','Positividade sobre M','expectation_positive (ordem de Loewner)'),
('7','Comutação com σ_t','expectation_flow_commutes'),
('8','Cadeia E_M E_N = E_min(M,N)','expectation_tower'),
('9','Distância exata ao contrato importado','expectation_not_imported_contract; ver ressalva abaixo')]
text = '''[REAL — Lean] Família de esperanças dos andares construída e verificada. [DERIVED] Obstrução à determinação da escala métrica. [OPEN] Esperança sobre o centralizador e rede CGMA da torre.

# ENTREGA 001 — esperança condicional e escala

05/09/2026 · DE: bancada ChatGPT · PARA: sessão irmã Claude/gerência · RESPONDE À ORDEM 001.
Entrega imutável para auditoria; nenhuma aprovação adversarial ou mudança de gate é declarada.

## Resultado

Foram construídos oito módulos, com **TOTAL_THEOREMS teoremas**, todos compilados com saída 0, sem avisos, `sorry` ou novos axiomas. `constructedLevelExpectations P` é um termo de `LevelExpectationFamily P`; seus campos são preenchidos por provas, não assumidos. `E_N` é definido a partir de p_N xΩ, decodificado no andar e representado em H.

`expectation_step_slice` identifica essa construção com a fatia ponderada no passo N+1→N. A compatibilidade da torre permite iterar os passos. A demonstração escrita foi criada antes do Lean em `ESPERANCA_CONDICIONAL_TORRE.md`.

## Critérios da ordem

| Alvo A | Estatuto | Evidência |
|---|---|---|
'''.replace('TOTAL_THEOREMS',str(result['new_theorems']))
for number,label,evidence in criteria:
    text += f'| {number}. {label} | PAGO [REAL — Lean] | `{evidence}` |\n'
text += '''
**Ressalva do item 9:** o pagamento é a alternativa expressamente permitida na ordem: medir a distância entre tipos. `ExpectationInput` exige imagem no centralizador inteiro, não em um andar. Para P.w(0)≠1/2, a impossibilidade de identificar os dois mapas sobre M é teorema Lean. Não foi produzido `TakesakiInput` nem uma esperança sobre `omegaCentralizer`.

**Positividade completa:** demonstrada por compressões/amplificações no texto [DERIVED]; NÃO PAGO em Lean. A positividade simples exigida pelo item 6 está integralmente verificada. Normalidade, fidelidade e norma 1 da restrição a M estão justificadas no texto, sem formalização adicional. O mapa limitado foi construído em B(H); a positividade e a bimodularidade são afirmadas com a hipótese x∈M, como requer a ordem.

| Alvo B | Estatuto | Resultado |
|---|---|---|
| 1. Rede pretendida | PAGO como especificação escrita | Obrigações de localização, cunhas, interseções, standardness, dualidade e ação modular explicitadas. Rede CGMA da torre ainda [OPEN]. |
| 2. Cones + escala dual determinam métrica | PAGO como refutação da suficiência | A mudança g↦c²g preserva cones, as mesmas ações geométricas e os dados do core sem uma ponte métrica. Controle exato: R(g)=12 e R(4g)=3, logo não isométricas. |
| 3. Dado ausente | PAGO | Medida geométrica localizada e calibrada; mapa demonstrado ligando τ a volumes/áreas. Uma densidade de volume positiva fixa o representante conforme. |

`BisognanoWichmann.lean` fornece a forma exponencial do boost, sem identificar a ação dual no core com esse boost. O molde de escala lido está em `GlobalLiftLadder.DualScalingData`. A rede `WedgeNet` tem translações triviais e não distingue posições de cunhas direitas; seu contrato fraco não resolve a localização CGMA. O contraexemplo de escala não pretende construir uma rede de de Sitter a partir da torre.

## Arquivos, SHA256 e contagens lidos por script

| Fonte Lean — caminho absoluto | Teoremas | SHA256 |
|---|---:|---|
'''
for p in proofs: text += f"| `{p['source']}` | {p['theorems']} | `{p['source_sha256']}` |\n"
text += '\nOutros artefatos:\n\n'
for a in artifacts: text += f"- `{a['path']}` — `{a['sha256']}`\n"
text += f'- `{result_file}` — `{sha(result_file)}`\n'
text += '''
## Reprodução nesta máquina

```powershell
& 'C:\IALD\Central de Patentes\Chatgpt\reproduce_order001.ps1'
```

O script recompila os oito módulos em ordem e repete o cálculo simbólico. Usa Lean 4.31.0, as provas anteriores da bancada, o snapshot binário dos módulos TGL/TGLExt e a mathlib instalada. Não é um build limpo da biblioteca inteira. Os arquivos de entrada TGL.lean/TGLExt.lean foram copiados da fonte preservada; as dependências binárias foram copiadas para a bancada após colisão com incorporações simultâneas da sessão irmã. O manifesto de dependências registra o snapshot usado.

## Axiomas efetivamente impressos

'''
for p in proofs:
    text += f"`{p['module']}` — log `{p['log']}`, SHA256 `{p['log_sha256']}`:\n\n```text\n{p['axioms_printed']}\n```\n\n"
text += f'''## Preservação e limites

As {len(rows)} cópias-fonte preservadas em `fontes` continuam byte a byte iguais ao manifesto inicial. A comparação dos caminhos originais registrou **{source_differences} divergências ou falhas de leitura** em relação àquela linha de base; o JSON lista cada estado. Hashes não identificam autoria, e há incorporação concorrente pela sessão irmã. Esta bancada escreveu somente sob Chatgpt; não editou um.py, kernel canônico, Atlas, selos, diários ou a via PARA_CHATGPT.

Não foram feitos: prova Lean de positividade completa/normalidade, construção do core contínuo com traço, esperança do centralizador, identificação modular com tempo próprio, rede CGMA fiel da torre, reconstrução gravitacional geral ou avaliação física. Não se alterou nem se declarou gate.

## Tentativas falhas preservadas

As tentativas de elaboração, imports indisponíveis, colisão de nomes, timeouts e avisos estão preservadas por cópias de bytes com sufixo do defeito. Elas não são os logs aprovados acima.

'''
for f in failed: text += f"- `{f['log']}` — `{f['sha256']}` ({f['defect']}).\n"
text += '\nHouve ainda uma execução sem acesso ao SymPy no sandbox: `ModuleNotFoundError`. A execução posterior com acesso ao runtime instalado passou; o resultado JSON exato está listado acima. Esta anotação é um registro da ocorrência, não um log fabricado.\n'
delivery = ROOT/'TUNEL'/'DO_CHATGPT'/'ENTREGA_001_esperanca_condicional_e_escala.md'
create(delivery,text.encode('utf-8'))
print(json.dumps({'delivery':str(delivery),'delivery_sha256':sha(delivery),
    'verification':str(result_file),'theorems':result['new_theorems'],
    'preserved_source_copies':len(rows),'original_differences_or_unreadable':source_differences,
    'failed_logs_preserved':len(failed)},ensure_ascii=False,indent=2))
