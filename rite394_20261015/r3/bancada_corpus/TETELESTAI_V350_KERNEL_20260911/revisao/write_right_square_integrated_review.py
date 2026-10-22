"""Publish only this final integration review, without touching the DEV review or memory."""
from pathlib import Path
import datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
OUT=Path((REV/'right_square_integrated_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
v=json.loads((OUT/'verification.json').read_bytes());s=json.loads((OUT/'static_verification.json').read_bytes())
assert v['integrated_records']==162 and v['gate_passed_author_records']==91 and v['audit_distinct']==6717
assert not v['P0'] and not v['P1'] and not v['P2']
for f,h in v['artifact_pins'].items():assert hf(ROOT/f)==h
assert hf(ROOT/'um.py')==v['working_sha256']
assert hf(REV/'REVIEW_RIGHT_SQUARE_DEV.md')==v['own_DEV_review_sha256']
assert not any((ROOT/f).exists() for f in v['new_custody_report_verification_absent'])
def link(p,label=None):
    p=Path(p);return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
def pins(names):
    r='| Artefato | SHA-256 lido |\n|---|---|\n'
    for n in names:r+='| '+link(ROOT/n)+' | `'+v['artifact_pins'][n]+'` |\n'
    return r
table='| Fonte integrada | SHA-256 da fonte | SHA-256 do .olean relido |\n|---|---|---|\n'
for r in v['new_records'][:2]:table+='| '+link(ROOT/'kernel'/r['file'])+' | `'+r['source_sha256']+'` | `'+r['binary_sha256']+'` |\n'
logs='; '.join(link(OUT/'logs'/r['log_name'],r['log_name']) for r in v['new_records'])
ar=v['final_Audit_record'];stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''Parecer integrado — escala direita no domínio de S†S

RIGHT_SQUARE_INTEGRATED_REVIEW

{stamp}. **Revisão integrada 2/13 concluída, sem achados P0–P2.** [REAL — inspeção independente de fontes, bytes, AST, logs e helpers.] A matemática e as três execuções próprias DEV (dois módulos e auditor de 13 alvos) são herdadas de {link(REV/'REVIEW_RIGHT_SQUARE_DEV.md')}, SHA-256 `{v['own_DEV_review_sha256']}`. Nesta rodada não se recompilaram Lean/biblioteca nem se executaram monólito, testes ou helpers autorais.

**Transposição.** Os dois DEV permanecem iguais ao manifesto e aos snapshots próprios. A transposição é literal em bytes, somente `import TGLV350.` → `import TGLExt.V350`; os valores embutidos coincidem com as fontes integradas. Não mudaram tipos, hipóteses ou objetos. São **864 embutidos**, dois novos; entre as entradas anteriores só mudaram `TGLExt.lean` e `TGL/Audit.lean`. Ambas importam os dois módulos exatamente uma vez; o Audit acrescenta apenas os 13 nomes auditados.

{table}
A cópia tem SHA-256 `{v['working_sha256']}`. Seu AST Python fora de `_EMBEDDED_KERNEL_FILES` coincide com a mãe `{s['parent_working_sha256']}`. O original canônico e a cópia-base foram somente relidos para hash, ambos `{v['original_sha256']}`. `gate_extension.py` permanece idêntico à mãe, SHA-256 `{v['artifact_pins']['gate_extension.py']}`.

**Evidência final.** Foram relidos **162 pares fonte/.olean**, JSONs e streams: rc0, saídas presentes, fontes/binários corretos e cada log igual ao respectivo registro agregado. **158 registros são exatamente herdados; quatro são compilações novas do autor** (dois módulos + duas raízes), com fonte inalterada, `lean_returncode=0` e dependências diretas presentes/frescas. Não são 162 recompilações novas.

Logs novos: {logs}.

O mapa de axiomas foi reconstruído do stdout atual: **6717 distintos = 6704 anteriores preservados, inclusive seus axiomas, + 13**. Confere integralmente com `kernel_incremental_evidence.json`; os 13 novos coincidem com o auditor DEV próprio e os dois streams integrados. Todo o Audit usa somente subconjuntos de `propext`, `Classical.choice`, `Quot.sound`. O JSON Audit final tem SHA-256 `{ar['log_sha256']}`; seu stdout bruto tem SHA-256 `{ar['stdout_sha256']}`.

[REAL — resultados autorais relidos, não reexecutados] **91/91 controles**: os 90 anteriores foram preservados; a única adição é `same_square_full_domain_matrix_unit_right_scaling_does_not_discharge_KMS_trace_or_physical_frontier`. Confere os cinco lemas de transporte/escala, as seis flags falsas e a fronteira sem promoção. Veredito legado e objeto de fronteira coincidem com a mãe; `legacy_gate_changed=false`, `full_plan_complete=false`, `full_monolithic_runtime_run=false`.

Os dois campos `audit_stdout_sha256` e `audit_capture_sha256_full` apontam aos **bytes atuais**, ambos `{ar['stdout_sha256']}`; `audit_stdout_path` e `CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES` conferem. O histórico explícito permanece igual à base e à mãe, ambos os valores `{v['historical_Audit_metadata_preserved']['audit_stdout_sha256']}`. A lógica desses hashes não mudou neste incremento.

**Helpers e mãe única.** `prepare_right_square_stage.py`, `record_right_square_progress.py` e `verify_right_square_custody.py` foram lidos integralmente e parseados, sem execução por este revisor. Os diffs efetivos, contra backups de hash materna, restringem-se aos dois módulos, batch **347 → 360**, ordem antes das raízes e único grupo de controle; não modificam a lógica do gate nem a dos hashes Audit.

{pins(['prepare_right_square_stage.py','record_right_square_progress.py','verify_right_square_custody.py'])}
O preparador exige leitura do parecer, vínculo materno e pins. O recorder exige `--review-read` e os marcadores DEV/integrado; confere original/cópia/AST, registros, controles, stream Audit, os 13 alvos exatos e 34 estados anteriores. O verificador relê fonte e binário de todos os registros, além dos artefatos/pareceres pinados e backups/prefixos. Ambos conferem o stream atual, sem confiar somente no booleano do agregado.

A mãe **integrada e de memória é a mesma**: `scalar_right_tomita_custody.json`, SHA-256 `{v['parent_custody_sha256']}`. Os **34 arquivos atuais e 34 backups** continuam nos hashes e prefixos dessa mãe. O recorder prevê backup imediato de bytes na mesma pasta e append por temporário verificado → substituição; atomicidade por arquivo, sem alegar transação única das 34 superfícies. Recusa novos arquivos de saída já existentes e confere o estado anterior antes da substituição.

A minuta preserva o alcance provado: para unidades matriciais locais, `R_y D(A)⊆D(A)` e `A R_y x=(w_i/w_j)R_y A x` no mesmo `A=S†S` e em todo `D(A)`. Não promove a relação local a identificação de `A^it`, KMS ou representação direita de toda a álgebra. O próximo gerador regular está rotulado como obrigação futura; não integra os 13 alvos. As frentes físicas são limites documentais, sem nova certificação por esta revisão.

[REAL — pré-registro] `right_square_custody.json`, sua verificação e `RELATORIO_ESCALA_DIREITA_SQUARED_INTEGRADA.md` ainda estavam ausentes na conferência final. A análise estática não atesta execução futura dos recorders nem nova gravação das 34 memórias. Os pareceres custodiados e o DEV permaneceram intactos.

{pins(['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json'])}
Evidência própria: {link(OUT/'verification.json')}, SHA-256 `{hf(OUT/'verification.json')}`; {link(OUT/'static_verification.json')}, SHA-256 `{hf(OUT/'static_verification.json')}`. Incluem pins dos 162 registros/streams, transposições, diffs, mapa Audit refeito e estado materno. Nenhuma execução Lean nova nesta rodada.

**Escopo encerrado sem pendências de revisão.** [OPEN] Identificação do fluxo/KMS global, traço, Three Locks, H1–H3 e runtime não são conclusões deste pacote. Nenhuma das seis flags foi promovida. Todas as escritas próprias ficaram em `revisao/`; fontes autorais, originais e memórias não foram modificados.
'''
p=REV/'REVIEW_RIGHT_SQUARE_INTEGRATED.md';assert not p.exists();b=text.encode('utf-8');tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:f.write(b)
assert tmp.read_bytes()==b;tmp.replace(p);assert p.read_bytes()==b
assert p.read_text(encoding='utf-8').count('RIGHT_SQUARE_INTEGRATED_REVIEW')==1
print(json.dumps({'report':str(p),'sha256':hf(p),'bytes':len(b),'lines':len(text.splitlines()),'P0':[],'P1':[],'P2':[]},ensure_ascii=False))
