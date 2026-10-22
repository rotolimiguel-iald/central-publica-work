"""Append the completed read-only integration review, preserving exact prefix bytes."""
from pathlib import Path
import datetime, hashlib, json

REV=Path(__file__).resolve().parent
ROOT=REV.parent
RUN=Path((REV/'right_regularization_integrated_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
V=load(RUN/'verification.json');S=load(RUN/'static_verification.json')
P=load(RUN/'gaussian_polar_custody.json')
assert not any(V[k] for k in ('P0','P1','P2'))
assert V['integrated_records']==191 and V['unchanged_parent_records']==187 and V['new_author_compilations']==4
assert V['gate_passed_author_records']==98 and V['audit_distinct']==6901
assert V['new_axioms_equal_own_DEV']==19 and V['current_Audit_global_hashes_verified']
assert all(hf(ROOT/f)==h for f,h in V['artifact_pins'].items())
assert hf(ROOT/'um.py')==V['working_sha256']
assert all(hf(p)==h for p,h in P['surface_sha256'].items())
assert all(hf(p)==h for p,h in P['review_sha256'].items())
assert not (ROOT/'right_regularization_custody.json').exists()
assert not (ROOT/'right_regularization_custody_verification.json').exists()
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
def link(p,label):return '['+label+'](<'+Path(p).as_posix()+'>)'
ar=V['final_Audit_record']
text='''

## Adendo final — '''+date+'''

RIGHT_REGULARIZATION_INTEGRATED_REVIEW

**[REAL — inspeção integrada concluída] Nenhum achado P0, P1 ou P2 no delta de dois módulos/19 alvos, duas raízes e helpers.** As pendências do estrato preliminar acima foram conferidas nos artefatos finais. A evidência matemática própria permanece a revisão DEV; nesta etapa não houve recompilação, execução de teste autoral ou execução/importação de monólito.

| Conferência | Resultado medido |
|---|---|
| Fontes/binários/logs/streams integrados | 191 registros rc0 relidos; 187 idênticos à mãe e quatro novos: dois módulos + duas raízes |
| Transposição e embutidos | 893 arquivos; duas transposições literais somente de imports; bytes das fontes integradas iguais aos embutidos |
| Audit atual | 6.901 declarações distintas, todas no trio permitido; 6.882 anteriores preservadas com os mesmos axiomas + 19 iguais ao auditor DEV próprio |
| Controles autorais | 98/98 registrados; os 97 anteriores preservados + exatamente um grupo novo |
| Gate e corpo Python | AST externo ao dicionário Lean igual à mãe; `gate_extension.py` idêntico; seis flags maiores falsas; legado e runtime integral inalterados |
| Memórias | 34 superfícies e backups da mãe relidos; bytes atuais ainda iguais aos pins da mãe |

As quatro compilações novas, nesta ordem, foram `V350ScalarRightRegularization_20260912_220116_713208`, `V350ScalarCommutantRegularization_20260912_220217_412704`, `TGLExt_20260912_220336_329389` e `Audit_20260912_220400_374181`. Conferidos rc0, `source_unchanged_during_compile`, bytes de fonte/binário, comando, logs JSON e streams; dependências diretas dos alterados presentes e sem binário mais novo que o resultado. Os 187 registros herdados foram comparados integralmente à captura da mãe e seus pares fonte/binário/streams relidos. **191 registros não são 191 recompilações novas.**

Audit corrente: log SHA256 `'''+ar['log_sha256']+'''`; stdout bruto `'''+ar['stdout_sha256']+'''`. O mapa foi reextraído desse stream, não presumido pelos nomes ou por metadados antigos. `audit_stdout_sha256` e `audit_capture_sha256_full` coincidem com esses bytes; `audit_hash_scope` declara o stream incremental atual e `historical_v350_audit_metadata` conserva exatamente a base histórica. O novo controle é `'''+V['added_controls'][0]+'''`.

Cópia atual: `'''+V['working_sha256']+'''`. Original/cópia-base relidos somente para hash: `'''+V['original_sha256']+'''`. Mãe matemática e documental única: `gaussian_polar_custody.json`, SHA256 `'''+V['parent_custody_sha256']+'''`.

**Helpers e registro ainda pendente.** As versões efetivas de `prepare_right_regularization_stage.py`, `record_right_regularization_progress.py` e `verify_right_regularization_custody.py` foram relidas estaticamente. Os diffs do preparador/integrador/compiler/tester se limitam ao batch 525→544, inclusão dos dois módulos antes das raízes e um grupo de controle; a lógica de metadata Audit permanece a mesma. Recorder e verifier checam pins de fonte/binário, evidência, mãe, prefixos e backups imediatos de bytes de 34 superfícies, com temporário antes da substituição. O relatório e a custódia novos permaneciam ausentes na leitura final: não afirmo sua gravação nem execução desses helpers. A inspeção estática confirma as verificações previstas; não equivale à futura execução bem-sucedida.

**Alcance matemático preservado.** `R_h` atua no mesmo `H_I`, sobre as inscrições do `nν` completo, e `T R_h` aproxima fortemente todo `T∈π(N)'`, com cota uniforme. `ScalarRightBounded` não exige vetor adjunto/algebra-full. A hipótese `∀R, ScalarRightBounded P R → R∈Q`, com `Q` von Neumann, permanece explícita no critério; foi descarregada apenas para a álgebra gerada pelos multiplicadores. Não se identifica essa álgebra com `Jπ(N)J`, não se substitui J, não se supõe `I=nν` nem se conclui KMS/traço/identificação modular ou promoção do gate.

Evidência principal: '''+link(RUN/'verification.json','verification.json')+''' (`'''+hf(RUN/'verification.json')+'''`); '''+link(RUN/'axioms.json','mapa do Audit reextraído')+''' (`'''+hf(RUN/'axioms.json')+'''`); '''+link(RUN/'new_module_axioms.json','19 axiomas integrados comparados aos próprios')+'''. Capturas, diffs, hashes dos helpers e streams estão na mesma pasta. Recompilação própria herdada: '''+link(REV/'REVIEW_RIGHT_REGULARIZATION_DEV.md','parecer DEV')+''' (`'''+V['own_DEV_review_sha256']+'''`).

**Escopo integrado encerrado, sem pendência de conferência neste lote.** Registro e verificação de custódia pelo autor são atos posteriores; nenhum deles foi executado nesta revisão.
'''
p=REV/'REVIEW_RIGHT_REGULARIZATION_INTEGRATED.md'
before=p.read_bytes()
assert b'RIGHT_REGULARIZATION_INTEGRATED_REVIEW' not in before
backup=p.with_name(p.name+'.bak_'+stamp)
with backup.open('xb') as f:f.write(before)
assert backup.read_bytes()==before
raw=before+text.encode('utf-8')
temp=p.with_name(p.name+'.tmp_'+stamp)
with temp.open('xb') as f:f.write(raw)
assert temp.read_bytes()==raw and p.read_bytes()==before
temp.replace(p)
assert p.read_bytes().startswith(backup.read_bytes()) and len(p.read_bytes())>len(before)
summary={'timestamp':date,'report':str(p),'report_sha256':hf(p),'backup':str(backup),
 'backup_sha256':hf(backup),'prefix_preserved_byte_exact':True,
 'verification_sha256':hf(RUN/'verification.json'),'complete':True,'P0':[],'P1':[],'P2':[]}
q=RUN/'final_review_pin.json';assert not q.exists()
data=json.dumps(summary,ensure_ascii=False,indent=2).encode('utf-8')
tmp=q.with_name(q.name+'.tmp')
with tmp.open('xb') as f:f.write(data)
assert tmp.read_bytes()==data
tmp.replace(q)
print(json.dumps(summary,ensure_ascii=False))
