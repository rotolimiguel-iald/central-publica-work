"""Publish this integration review only, keeping DEV and custody artifacts immutable."""
from pathlib import Path
import datetime, hashlib, json, sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
OUT=Path((REV/'regular_polar_integrated_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
v=load(OUT/'verification.json'); s=load(OUT/'static_verification.json'); w=load(OUT/'gate_wiring.json')
assert v['integrated_records']==168 and v['gate_passed_author_records']==93 and v['audit_distinct']==6769
assert not v['P0'] and not v['P1'] and not v['P2']
for f,h in v['artifact_pins'].items():assert hf(ROOT/f)==h
assert hf(ROOT/'um.py')==v['working_sha256']
assert hf(REV/'REVIEW_REGULAR_POLAR_DEV.md')==v['own_DEV_review_sha256']
assert not any((ROOT/f).exists() for f in v['new_custody_report_verification_absent'])
assert hf(load(ROOT/'environment.json')['original_source'])==hf(ROOT/'fontes/um_v350_original.py')==v['original_sha256']
for p,row in s['memory_surfaces'].items():
    assert hf(p)==row['sha256'] and hf(row['backup'])==row['backup_sha256']
for row in v['new_records']:
    assert hf(ROOT/'kernel'/row['file'])==row['source_sha256']
    assert hf(ROOT/'build'/Path(row['file']).with_suffix('.olean'))==row['binary_sha256']
def link(p,label=None):
    p=Path(p);return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
def pins(names):
    t='| Artefato | SHA-256 lido |\n|---|---|\n'
    for n in names:t+='| '+link(ROOT/n)+' | `'+v['artifact_pins'][n]+'` |\n'
    return t
table='| Fonte integrada | SHA-256 da fonte | SHA-256 do .olean relido |\n|---|---|---|\n'
for row in v['new_records'][:3]:
    table+='| '+link(ROOT/'kernel'/row['file'])+' | `'+row['source_sha256']+'` | `'+row['binary_sha256']+'` |\n'
logs='; '.join(link(OUT/'logs'/row['log_name'],row['log_name']) for row in v['new_records'])
ar=v['final_Audit_record']; stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')

PRE=REV/'regular_polar_helpers_20260912_174527_622631'
pre=load(PRE/'static_helpers_verification.json')
for name in ['prepare_regular_polar_stage.py','record_regular_polar_progress.py','verify_regular_polar_custody.py']:
    assert hf(ROOT/name)==pre['helper_pins'][name]
text=f'''Parecer integrado — conjugação polar regular e continuidade

REGULAR_POLAR_INTEGRATED_REVIEW

{stamp}. **Revisão integrada 3/16 concluída, sem achados P0–P2.** [REAL — inspeção independente de fontes, bytes, AST, logs e helpers.] A matemática, os tipos com universos e as quatro execuções próprias DEV (três módulos + auditor dos 16 alvos) são herdados de {link(REV/'REVIEW_REGULAR_POLAR_DEV.md')}, SHA-256 `{v['own_DEV_review_sha256']}`. Nesta rodada foram executadas somente verificações de leitura; não se repetiram compilações Lean, biblioteca ou testes autorais.

**Transposição e alcance.** As três fontes DEV e seus binários continuam nos pins do manifesto e da árvore própria. A transposição é literal em bytes, alterando apenas `import TGLV350.` para `import TGLExt.V350`; cada fonte integrada coincide com seu conteúdo embutido. Nomes, termos, hipóteses e domínios são os já revisados. **870 embutidos:** três chaves novas; entre as anteriores só mudaram as duas raízes. `TGLExt.lean` e `TGL/Audit.lean` importam os três módulos uma vez; o Audit adiciona apenas os 16 alvos próprios.

{table}
Permanece o resultado no mesmo `H_I`, com `A=S†S`, seu resolvente `T`, sua raiz `B` e **o efetivo `scalarTomitaPolarFactor P`**: `T R_t=R_t T`, invariância bijetiva de `D(B)` por `R_t`, comutação com `B` nesse domínio, `J R_t J⁻¹=π(λ_t*)` e `Jπ(λ_t)J⁻¹=R_(-t)`. `R_t` comuta com **todo** `π(a)`, e a família é fortemente contínua. A conjugação por J verificada neste lote abrange a família regular; não é ainda `Jπ(N)J=π(N)'`. Não há identificação com `TowerJ`, promoção a KMS ou hipótese nova de domínio/continuidade na transposição.

Cópia SHA-256 `{v['working_sha256']}`. O AST Python fora de `_EMBEDDED_KERNEL_FILES` coincide com a mãe `{s['parent_working_sha256']}`. Original canônico e cópia-base foram relidos somente para hash, ambos `{v['original_sha256']}`. `gate_extension.py` permanece idêntico em bytes ao pai, SHA-256 `{v['artifact_pins']['gate_extension.py']}`.

**Evidência final autoral relida.** Conferidos **168 pares fonte/.olean**, respectivos JSONs e streams: rc0, saída presente, hashes corretos, fonte embutida igual ao disco e cada JSON igual ao registro agregado. **163 registros são exatamente herdados; cinco são compilações novas do autor:** três módulos e depois as raízes `TGLExt.lean` e `TGL/Audit.lean`. Nos cinco, fonte inalterada durante a compilação, `lean_returncode=0` e dependências diretas presentes/frescas, com hashes capturados. Os cinco streams não têm warnings ou erros. Não são 168 recompilações novas, e não houve nova execução Lean própria neste escopo integrado.

Logs novos: {logs}.

Reparseado o stdout Audit final inteiro: **6769 declarações distintas = 6753 anteriores, inclusive seus axiomas preservados, + 16 novas**. O mapa coincide integralmente com `kernel_incremental_evidence.json`. Os 16 novos coincidem com os três streams integrados e com o auditor DEV próprio, todos exatamente no trio `propext`, `Classical.choice`, `Quot.sound`; as 6769 entradas usam somente subconjuntos desse trio. As tentativas DEV rc1 permanecem no histórico e não são evidência aceita. JSON Audit atual SHA-256 `{ar['log_sha256']}`; stdout bruto SHA-256 `{ar['stdout_sha256']}`.

`audit_stdout_sha256` e `audit_capture_sha256_full` são ambos iguais aos **bytes atuais** desse stdout. `audit_stdout_path` e o escopo `CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES` conferem. `historical_v350_audit_metadata` continua igual à base e à mãe, com os dois valores históricos `{v['historical_Audit_metadata_preserved']['audit_stdout_sha256']}`. A lógica de produção desses metadados não mudou neste incremento.

**Controles, gate e documentação.** [REAL — resultados autorais relidos, não reexecutados] **93/93 controles** verdes, preservados os 92 anteriores. A única adição é `same_polar_regular_generator_and_strong_continuity_does_not_discharge_KMS_trace_or_physical_frontier`, que confere seis declarações do novo estágio e mantém seis flags maiores falsas e fronteira sem promoção. Os dois controles de hash Audit atual/histórico seguem verdes. Veredito legado e objeto de fronteira são iguais aos maternos; `legacy_gate_changed=false`, `full_plan_complete=false`, `full_monolithic_runtime_run=false`.

O texto dos helpers preserva a distinção já conferida: `evaluate_quantum_gravity_closure` recebe `formal/physics/experiment`; o chamador prepara os mapas a partir de `qgc_`, `qgp_` e `experiment_feed`, anexando `kernel_frontier` depois. As seis flags maiores `qgf/gpf` não são entradas diretas desse avaliador. O AST corrente confirma a mesma fiação; linhas/trechos estão em {link(OUT/'gate_wiring.json')} e {link(OUT/'gate_AST','gate_AST/')}. Isso não atesta runtime integral nem transforma as provas presentes em novo certificado consumido.

**Helpers e pré-registro.** `prepare_regular_polar_stage.py`, `record_regular_polar_progress.py` e `verify_regular_polar_custody.py` foram lidos integralmente e parseados. Seus bytes finais são iguais aos da {link(PRE/'STATIC_HELPERS_NOTES.md','análise estática preliminar preservada')}. O preparador rodou pelo autor; os diffs efetivos contra backups de hash materna limitam-se ao batch **396→412**, três módulos antes das raízes e um grupo novo de controle. A lógica do gate e dos metadados Audit foi preservada.

{pins(['prepare_regular_polar_stage.py','record_regular_polar_progress.py','verify_regular_polar_custody.py'])}
O preparador exige `--review-read`, marcador DEV, mãe, artefatos, superfícies e pins das três fontes/binários. O recorder exige os dois pareceres/marcadores e confere original/cópia/AST, registros fonte/binário rc0, controles, stream Audit, histórico, 16 alvos exatos e 34 estados anteriores. O verificador relê fonte/binário de todos os registros, confronta a contagem e relê os artefatos/pareceres pinados, backups e prefixos. A correção de verificação binária permanece ativa. Não se executaram esses programas pelo revisor.

A mãe **integrada e documental é a mesma**, `regular_right_custody.json`, SHA-256 `{v['parent_custody_sha256']}`. Os **34 arquivos atuais e 34 backups** foram relidos e permanecem nos hashes/prefixos dessa mãe. O recorder prevê backup imediato de bytes na mesma pasta e append por temporário verificado → substituição, com nova checagem do estado anterior; recusa sobrescrever saídas novas. A atomicidade é por arquivo, sem alegar transação indivisível das 34 superfícies.

A minuta do relatório e da nota de memória descreve corretamente domínio completo, J efetivo, conjugação dos geradores regulares, comutação com toda a esquerda e continuidade forte. Deixa abertos geradores da base, igualdade global dos comutantes, `A^it`/fluxo/KMS e traço; propostas de reutilização física não recebem prova nova nesta revisão. Na conferência final ainda estavam ausentes `regular_polar_custody.json`, sua verificação e `RELATORIO_CONJUGACAO_POLAR_REGULAR_INTEGRADA.md`: o registro permanece posterior à leitura deste parecer. Nenhuma nova gravação das memórias é atestada.

{pins(['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json'])}
Evidências próprias: {link(OUT/'verification.json')}, SHA-256 `{hf(OUT/'verification.json')}`; {link(OUT/'static_verification.json')}, SHA-256 `{hf(OUT/'static_verification.json')}`. Incluem pins dos 168 registros/streams, transposição, diffs, dependências diretas, mapa Audit refeito e estado materno. A biblioteca e a análise matemática dos ancestrais são herdadas; o DEV próprio 3/16 não foi recompilado novamente.

**Escopo integrado 3/16 encerrado, sem pendência de revisão.** [OPEN] Igualdade global `Jπ(N)J=π(N)'`, identificação modular/KMS, traço, Three Locks, H1–H3 e runtime não são conclusões deste lote. Seis flags maiores seguem falsas. Pareceres anteriores e DEV, originais, fontes autorais e memórias foram preservados; todas as escritas próprias ficaram em `revisao/`.
'''
p=REV/'REVIEW_REGULAR_POLAR_INTEGRATED.md';assert not p.exists();b=text.encode('utf-8');tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:f.write(b)
assert tmp.read_bytes()==b;tmp.replace(p);assert p.read_bytes()==b
assert text.count('REGULAR_POLAR_INTEGRATED_REVIEW')==1
pin={'report':str(p),'sha256':hf(p),'bytes':len(b),'lines':len(text.splitlines()),'P0':[],'P1':[],'P2':[],
 'integration_review_complete':True,'recorder_execution_attested':False,'new_compilations_by_reviewer':0,
 'verification_sha256':hf(OUT/'verification.json'),'preliminary_helpers_verification_sha256':hf(PRE/'static_helpers_verification.json')}
p=OUT/'report_pin.json';assert not p.exists();b=json.dumps(pin,ensure_ascii=False,indent=2).encode();tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:f.write(b)
assert tmp.read_bytes()==b;tmp.replace(p)
print(json.dumps(pin,ensure_ascii=False))
