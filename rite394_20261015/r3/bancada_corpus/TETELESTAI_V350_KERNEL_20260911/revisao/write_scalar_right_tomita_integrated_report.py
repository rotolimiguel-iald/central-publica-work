"""Publish the final bounded integration review from measured evidence."""
from pathlib import Path
import datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
OUT=Path((REV/'scalar_right_tomita_integrated_latest_run.txt').read_text().strip())
sha=lambda b:hashlib.sha256(b).hexdigest();hf=lambda p:sha(Path(p).read_bytes())
v=json.loads((OUT/'verification.json').read_bytes());s=json.loads((OUT/'static_verification.json').read_bytes())
assert not v['P0'] and not v['P1'] and not v['P2']
assert v['integrated_records']==160 and v['new_axioms_equal_own_DEV']==17 and v['gate_passed_author_records']==90
for f,h in v['artifact_pins'].items():assert hf(ROOT/f)==h
assert hf(ROOT/'um.py')==v['working_sha256']
assert hf(REV/'REVIEW_SCALAR_RIGHT_CLOSED_TOMITA.md')==v['own_DEV_review_sha256']
assert not any((ROOT/n).exists() for n in v['new_custody_report_verification_absent'])
def link(p,label=None):
    p=Path(p);return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
def line(name,n):return '['+name+':'+str(n)+'](<'+(ROOT/name).as_posix()+':'+str(n)+'>)'
def pins(names):
    text='| Artefato | SHA-256 lido |\n|---|---|\n'
    for n in names:text+='| '+link(ROOT/n)+' | `'+v['artifact_pins'][n]+'` |\n'
    return text
rows='| Fonte integrada | SHA-256 da fonte | SHA-256 do .olean relido |\n|---|---|---|\n'
for r in v['new_records'][:3]:
    rows+='| '+link(ROOT/'kernel'/r['file'])+' | `'+r['source_sha256']+'` | `'+r['binary_sha256']+'` |\n'
newlogs='; '.join(link(OUT/'logs'/r['log_name'],r['log_name']) for r in v['new_records'])
ar=v['final_Audit_record'];stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
report=f'''Parecer integrado — direita homogênea, mesmo Tomita fechado e adjunto máximo

SCALAR_RIGHT_TOMITA_INTEGRATED_REVIEW

{stamp}. **Sem achados P0–P2; revisão integrada dos três módulos/17 alvos concluída.** [REAL — conferência independente de bytes, AST, logs e documentação.] Esta rodada não recompilou Lean nem executou testes, monólito, preparador, integrador ou recorders. A recompilação própria dos três DEV e auditores **12 + 5** é a evidência anterior preservada em {link(REV/'REVIEW_SCALAR_RIGHT_CLOSED_TOMITA.md')}, SHA-256 `{v['own_DEV_review_sha256']}`.

**Transposição e alcance.** Os três DEV pinados coincidem com os snapshots próprios. A passagem para `TGLExt/V350*.lean` é literalmente a substituição de `import TGLV350.` por `import TGLExt.V350`, conferida em bytes; cada fonte integrada coincide com seu valor embutido. Permanecem os mesmos enunciados, hipóteses, namespaces e objetos. A cópia tem **862 embutidos**: três entradas novas e somente as duas raízes alteradas entre as entradas anteriores. Cada raiz importa os três módulos uma vez; Audit acrescenta exatamente os 17 nomes, preservando as ocorrências anteriores.

{rows}
O SHA-256 da cópia é `{v['working_sha256']}`. O AST Python fora de `_EMBEDDED_KERNEL_FILES` coincide com o backup cuja hash é a da mãe `{s['parent_working_sha256']}`. O original canônico e `fontes/um_v350_original.py` foram apenas relidos para hash e coincidem em `{v['original_sha256']}`. `gate_extension.py` permanece byte a byte igual à mãe, hash `{v['artifact_pins']['gate_extension.py']}`.

**Build e Audit efetivos.** Foram relidos os **160 pares fonte/.olean**, seus JSONs de compilação e streams stdout/stderr: rc0, saídas presentes, hashes corretos e cada JSON igual ao registro agregado. **155 registros são exatamente os da mãe; cinco são novos**, correspondentes aos três módulos e às duas raízes. Nesses cinco, `lean_returncode=0`, fonte inalterada durante compilação e dependências diretas de projeto presentes/anteriores ao binário foram conferidos. Não são 160 recompilações novas.

Logs novos: {newlogs}.

O Audit atual é o último desses registros: JSON SHA-256 `{ar['log_sha256']}`, stdout bruto SHA-256 `{ar['stdout_sha256']}`. Seu mapa foi reconstruído independentemente: **6704 declarações distintas = 6687 anteriores preservadas, inclusive seus axiomas, + 17**. O mapa coincide integralmente com `kernel_incremental_evidence.json`; todo Audit usa somente subconjuntos do trio permitido. Os 17 novos axiomas coincidem exatamente com os auditores próprios DEV 12 + 5 e com os três streams integrados. Não se inferiu a validação apenas da presença dos nomes.

**Controles e correção dos hashes.** [REAL — leitura dos resultados autorais, sem reexecução] **90/90 controles**: os 86 anteriores foram preservados e há quatro adições — dois grupos de domínio e `current_audit_hashes_match_current_raw_stream`/`historical_v350_audit_hashes_preserved_as_history`. Os grupos novos exigem os lemas pertinentes e as seis flags falsas, além de `legacy_gate_changed=false` e `full_plan_complete=false`.

Em {line('test_gate_extension.py',48)}, o hash agora é calculado sobre `read_bytes()` do stdout corrente; `audit_stdout_sha256` e `audit_capture_sha256_full` valem ambos `{ar['stdout_sha256']}`. `audit_stdout_path` aponta ao mesmo stream e `audit_hash_scope` é `CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES`. Os dois valores históricos da base foram preservados em `historical_v350_audit_metadata`, ambos `{v['historical_Audit_metadata_preserved']['audit_stdout_sha256']}`. A igualdade atual e a preservação histórica foram também conferidas por esta revisão; a ressalva dos campos globais antigos **não se aplica a este snapshot**. O veredito legado e o objeto de fronteira coincidem com a mãe; seis flags maiores falsas, `full_plan_complete=false`, `full_monolithic_runtime_run=false`.

**Helpers e memória antes do registro.** Os três helpers foram lidos integralmente e parseados, sem execução. As diferenças de `integrate_v350.py`, `compile_integrated.py` e `test_gate_extension.py` foram comparadas aos backups com hashes pinadas na mãe: apenas três módulos, contagem do batch Tomita **330 → 347**, ordem antes das raízes, metadados Audit e quatro controles descritos acima.

{pins(['prepare_scalar_right_tomita_stage.py','record_scalar_right_tomita_progress.py','verify_scalar_right_tomita_custody.py'])}
O preparador exige `--review-read`, o marcador DEV, os vínculos de mãe e pins; escreve seus três scripts com backup imediato de bytes e temporário verificado. O recorder exige `--review-read` e os marcadores DEV/integrado, confere original/cópia, AST, registros, controles, stream Audit, 17 alvos e **34 estados anteriores de memória**. O verificador relê efetivamente fonte e binário de todos os registros, além dos artefatos pinados, stream atual, DEV, pareceres e pares de backup/prefixo; não se limita a aceitar o booleano do agregado.

As duas mães são distintas e foram conferidas: integrada `homogeneous_right_custody.json`, SHA-256 `{v['mathematical_parent_sha256']}`; memória imediata `scalar_right_tomita_draft_memory.json`, SHA-256 `{v['immediate_memory_parent_sha256']}`. Os **34 arquivos atuais e seus backups DEV** continuam nos hashes/prefixos dessa mãe imediata; não houve novo append para o adendo de cinco alvos. O recorder exige esse estado, grava backup no mesmo diretório, preserva os bytes como prefixo e substitui por temporário verificado. A atomicidade é por arquivo, não uma transação única das 34 superfícies.

O texto proposto pelo recorder distingue `S R_y = π(y*)S` de `S†π(y)=R_y*S†`, nos domínios completos do mesmo `H_I`. A torção aparece na identificação do adjunto direito da instância matricial. A futura composição no domínio de `S†S` está explicitamente [OPEN]; não é contada entre os 17 alvos nem tratada como KMS. A tabela de obrigações é orientação de fronteira, sem nova certificação das frentes físicas por este parecer.

[REAL — estado pré-registro] `scalar_right_tomita_custody.json`, sua verificação e `RELATORIO_DOMINIOS_TOMITA_ADJUNTO_INTEGRADOS.md` ainda estavam ausentes na conferência final. Este parecer avalia a lógica dos helpers e os bytes disponíveis; **não atesta execução futura, gravação de custódia ou atualização das memórias**. O `--review-read` e a leitura humana do parecer continuam sendo atos posteriores do operador.

{pins(['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json'])}
Evidência própria completa: {link(OUT/'verification.json')}, SHA-256 `{hf(OUT/'verification.json')}`; captura estática {link(OUT/'static_verification.json')}, SHA-256 `{hf(OUT/'static_verification.json')}`. A pasta contém hashes dos 160 registros/streams, diferenças de scripts/raízes, fontes transpostas, mapa Audit refeito e pins das duas revisões DEV. Dependências e matemática DEV já revistas são herança explícita, sem rebuild redundante.

**Limite final:** integração 3/17 encerrada, sem P0–P2 ou verificação necessária pendente neste escopo. Nenhuma promoção de KMS, identificação do fluxo por `S†S`, traço, Three Locks, H1–H3 ou runtime. Originais, fontes autorais, parecer DEV e memórias não foram modificados pela revisão; todas as saídas próprias ficaram em `revisao/`.
'''
p=REV/'REVIEW_SCALAR_RIGHT_TOMITA_INTEGRATED.md';assert not p.exists()
b=report.encode('utf-8');temp=p.with_name(p.name+'.tmp')
with temp.open('xb') as f:f.write(b)
assert temp.read_bytes()==b;temp.replace(p);assert p.read_bytes()==b
assert p.read_text(encoding='utf-8').count('SCALAR_RIGHT_TOMITA_INTEGRATED_REVIEW')==1
print(json.dumps({'report':str(p),'sha256':hf(p),'bytes':len(b),'lines':len(report.splitlines()),'P0':[],'P1':[],'P2':[]},ensure_ascii=False))
