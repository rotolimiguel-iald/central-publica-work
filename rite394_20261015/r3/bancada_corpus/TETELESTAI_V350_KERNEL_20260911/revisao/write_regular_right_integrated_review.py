"""Publish this integration review only, keeping DEV and custody artifacts immutable."""
from pathlib import Path
import datetime, hashlib, json, sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent; ROOT=REV.parent
OUT=Path((REV/'regular_right_integrated_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
v=load(OUT/'verification.json'); s=load(OUT/'static_verification.json'); w=load(OUT/'gate_wiring.json')
assert v['integrated_records']==165 and v['gate_passed_author_records']==92 and v['audit_distinct']==6753
assert not v['P0'] and not v['P1'] and not v['P2']
for f,h in v['artifact_pins'].items():assert hf(ROOT/f)==h
assert hf(ROOT/'um.py')==v['working_sha256']
assert hf(REV/'REVIEW_REGULAR_RIGHT_DEV.md')==v['own_DEV_review_sha256']
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
text=f'''Parecer integrado — direita unitária regular no mesmo GNS

REGULAR_RIGHT_INTEGRATED_REVIEW

{stamp}. **Integração 3/36 concluída, sem achados P0–P2.** [REAL — inspeção independente de fontes, bytes, AST, logs e helpers.] A matemática, os 36 tipos com universos e as quatro execuções próprias DEV (três módulos + auditor) são herdados de {link(REV/'REVIEW_REGULAR_RIGHT_DEV.md')}, SHA-256 `{v['own_DEV_review_sha256']}`. Esta rodada não repetiu compilações nem executou testes, monólito, integradores ou recorders autorais.

**Transposição e objetos.** Os três DEV permanecem iguais ao manifesto e aos snapshots próprios. A transformação DEV→TGLExt é literal em bytes, somente `import TGLV350.` → `import TGLExt.V350`; cada fonte integrada coincide com seu valor embutido. Nomes, termos, hipóteses e domínios foram preservados. São **867 embutidos**, três novos; entre as entradas anteriores só mudaram `TGLExt.lean` e `TGL/Audit.lean`. Ambas importam os três módulos uma vez; o Audit acrescenta exatamente os 36 nomes próprios, sem retirar os anteriores.

{table}
Permanece a conclusão revisada: `R_t` unitário no mesmo `H_I`, com caráter exterior e translação interior distintos; `S R_t=π(λ_t*)S`, `Fπ(λ_t)=R_t*F` e **`R_t x∈D(A) ↔ x∈D(A)`, `A R_t x=R_t Ax` para o mesmo `A=S†S`**, usando `R_(-t)` para o retorno. A integração não introduz KMS ou domínio presumido. A deprecação de `ContinuousLinearMap.one_apply` na linha 113 do terceiro módulo é o único warning novo observado; não é erro.

Cópia SHA-256 `{v['working_sha256']}`. Seu AST Python fora de `_EMBEDDED_KERNEL_FILES` coincide com o pai `{s['parent_working_sha256']}`. Original canônico e cópia-base foram relidos somente para hash, ambos `{v['original_sha256']}`. `gate_extension.py` permanece idêntico à mãe, SHA-256 `{v['artifact_pins']['gate_extension.py']}`.

**Compilação e Audit: execução autoral, conferência própria dos bytes.** Relidos **165 pares fonte/.olean**, respectivos JSONs, stdout e stderr: rc0, saídas existentes, hashes corretos, fonte embutida igual ao disco e cada JSON igual ao registro agregado. **160 registros são exatamente herdados; cinco são compilações novas do autor**: os três módulos, depois `TGLExt.lean` e `TGL/Audit.lean`. Nos cinco, `lean_returncode=0`, fonte inalterada durante compilação e dependências diretas presentes/frescas com hashes capturados. Não são 165 recompilações novas; a biblioteca e a proveniência anterior permanecem herdadas.

Logs novos: {logs}.

O mapa completo foi reparseado dos bytes do stdout atual: **6753 declarações distintas = 6717 anteriores, com axiomas preservados, + 36 novas**. Confere com `kernel_incremental_evidence.json`. Os 36 alvos coincidem exatamente com o auditor DEV próprio e com os streams dos três módulos integrados, todos no trio `propext`, `Classical.choice`, `Quot.sound`; as 6753 entradas usam somente subconjuntos desse trio. Não se inferiu aprovação de impressões de tentativas falhas. JSON Audit final SHA-256 `{ar['log_sha256']}`; stdout bruto SHA-256 `{ar['stdout_sha256']}`.

Os dois campos globais `audit_stdout_sha256` e `audit_capture_sha256_full` são atuais e iguais a esse stdout. `audit_stdout_path` e `audit_hash_scope=CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES` conferem. O objeto histórico é igual à base e à mãe; os dois hashes históricos permanecem `{v['historical_Audit_metadata_preserved']['audit_stdout_sha256']}`. Não foram confundidos com o stream corrente.

**Controles e consumo.** [REAL — resultados autorais relidos, não reexecutados] Lidos **92/92 controles**, preservados os 91 anteriores. A única adição é `same_square_regular_right_unitary_full_domain_does_not_discharge_KMS_trace_or_physical_frontier`: confere os seis nomes de unitariedade/entrelaçamento/domínio, as seis flags falsas e ausência de promoção da fronteira. Os controles dos hashes Audit atuais e históricos permanecem presentes e verdes. Veredito legado e objeto `frontier` coincidem com a mãe; `legacy_gate_changed=false`, `full_plan_complete=false`, `full_monolithic_runtime_run=false`.

A explicação acrescentada ao recorder está correta **como leitura da fiação por AST**. `evaluate_quantum_gravity_closure` (um.py:{w['evaluator_line']}) recebe `formal`, `physics`, `experiment`. Em `prove_qg_closure_gate`, os dois primeiros mapas vêm de `qgc_` (linha {w['formal_line']}) e `qgp_` (linha {w['physics_line']}); o terceiro vem de `experiment_feed` (linha {w['feed_line']}). Depois da chamada, na linha {w['call_line']}, `kernel_frontier` é anexado ao resultado na linha {w['annex_line']}. **As seis flags maiores `qgf/gpf` não são entradas diretas desse avaliador.** O controle de que o anexo é consumido não demonstra que ele decide o selo legado. Os trechos exatos estão em {link(OUT/'gate_AST','gate_AST')} e as linhas/pins em {link(OUT/'gate_wiring.json')}. Essa inspeção não é execução integral nem identificação matemática do fluxo.

**Helpers e pré-registro.** Os três helpers foram lidos integralmente e parseados. O preparador foi executado pelo autor; os diffs efetivos contra backups de hash materna limitam-se ao batch **360→396**, três módulos antes das raízes e um novo grupo de controle. A lógica dos hashes Audit e do gate não mudou.

{pins(['prepare_regular_right_stage.py','record_regular_right_progress.py','verify_regular_right_custody.py'])}
O preparador exige leitura do parecer, marcador DEV, vínculo materno e pins. O recorder exige `--review-read` e ambos os marcadores; confere original/cópia/AST, registros fonte/binário, controles, stream Audit, os 36 alvos exatos e 34 estados anteriores. O verificador relê fonte/binário de todos os registros rc0, confronta a contagem com a custódia e relê os artefatos/pareceres pinados, backups e prefixos. Nenhum dos dois foi executado nesta revisão; não se declara que seu registro futuro já existe.

A mãe **matemática integrada e documental é a mesma**, `right_square_custody.json`, SHA-256 `{v['parent_custody_sha256']}`. Os **34 arquivos atuais e 34 backups** foram relidos e continuam nos hashes/prefixos maternos. O recorder prevê backup imediato de bytes na mesma pasta, append que preserva o prefixo, temporário verificado e substituição, conferindo novamente o estado anterior. A atomicidade é por arquivo; não se afirma transação indivisível das 34 superfícies. As saídas novas recusam sobrescrita.

A minuta do relatório e da nota de memória preserva a conclusão em todo `D(A)` e deixa abertos `A^it`/fluxo, KMS global, extensão da direita a toda `N` e nova continuidade forte. Suas remissões a reaproveitamento físico futuro não recebem certificação desta revisão. Na conferência final, `regular_right_custody.json`, sua verificação e `RELATORIO_DIREITA_UNITARIA_REGULAR_INTEGRADA.md` ainda estavam ausentes, como esperado antes do recorder. O parecer DEV, a análise estática preliminar e os pareceres anteriores foram preservados.

{pins(['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json'])}
Evidências próprias: {link(OUT/'verification.json')}, SHA-256 `{hf(OUT/'verification.json')}`; {link(OUT/'static_verification.json')}, SHA-256 `{hf(OUT/'static_verification.json')}`. Contêm os pins dos 165 registros/streams, transposições, diffs, dependências diretas, mapa Audit e estado materno. A {link(OUT/'STATIC_NOTES.md','análise estática anterior ao aviso final')} permanece intacta.

**Escopo encerrado, sem pendência de revisão integrada 3/36.** [OPEN] Identificação modular/KMS, traço, Three Locks, H1–H3 e runtime não são conclusões deste pacote. Seis flags maiores continuam falsas. Registro de memória/custódia é ato posterior, ainda não atestado. Todas as escritas próprias ficaram em `revisao/`; originais, fontes autorais e memórias não foram alterados.
'''
p=REV/'REVIEW_REGULAR_RIGHT_INTEGRATED.md';assert not p.exists();b=text.encode('utf-8');tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:f.write(b)
assert tmp.read_bytes()==b;tmp.replace(p);assert p.read_bytes()==b
assert p.read_text(encoding='utf-8').count('REGULAR_RIGHT_INTEGRATED_REVIEW')==1
pin={'report':str(p),'sha256':hf(p),'bytes':len(b),'lines':len(text.splitlines()),'P0':[],'P1':[],'P2':[],
 'integration_review_complete':True,'recorder_execution_attested':False,'new_compilations_by_reviewer':0,
 'verification_sha256':hf(OUT/'verification.json')}
p=OUT/'report_pin.json';assert not p.exists();b=json.dumps(pin,ensure_ascii=False,indent=2).encode();tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:f.write(b)
assert tmp.read_bytes()==b;tmp.replace(p)
print(json.dumps(pin,ensure_ascii=False))
