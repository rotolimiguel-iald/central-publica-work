from pathlib import Path
import datetime
import hashlib
import json
import os

REV = Path(__file__).resolve().parent
ROOT = REV.parent
RUN = Path((REV / 'gaussian_polar_integrated_latest_run.txt').read_text().strip())
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
v = json.loads((RUN / 'verification.json').read_bytes())
s = json.loads((RUN / 'static_verification.json').read_bytes())
assert v['integrated_records'] == 189 and v['unchanged_parent_records'] == 183
assert v['new_author_compilations'] == 6 and v['audit_distinct'] == 6882
assert v['gate_passed_author_records'] == 97 and v['new_axioms_equal_own_DEV'] == 34
assert v['all_source_binary_log_stream_pins_match'] and v['parent_Audit_no_loss']
assert not v['P0'] and not v['P1'] and not v['P2']
assert all(x is False for x in v['six_flags'].values())
assert all(sha(ROOT / f) == h for f, h in v['artifact_pins'].items())
assert sha(ROOT / 'um.py') == v['working_sha256']
assert sha(REV / 'REVIEW_GAUSSIAN_POLAR_DEV.md') == v['own_DEV_review_sha256']

def link(path, label):
    return f'[{label}](<{Path(path).as_posix()}>)'

ar = v['final_Audit_record']
rows = '\n'.join(
    f"| {r['file']} | `{r['log_name']}` | rc0; fonte/binário/streams conferidos |"
    for r in v['new_records']
)
pins = '\n'.join(
    f"- {link(RUN / f, f)}: `{sha(RUN / f)}`."
    for f in ['integration.json', 'integrated_compile.json', 'gate_tests.json', 'kernel_incremental_evidence.json', 'verification.json']
)
now = datetime.datetime.now().astimezone()
p = REV / 'REVIEW_GAUSSIAN_POLAR_INTEGRATED.md'
before = p.read_bytes()
assert b'GAUSSIAN_POLAR_INTEGRATED_REVIEW' not in before
stamp = now.strftime('%Y%m%d_%H%M%S_%f')
backup = p.with_name(p.name + '.bak_' + stamp)
before_sha = sha(p)
assert before_sha == '2d4fe549220d3fa10a387ef1e485b1930b1b1178bc6995eeb042e857a1e18e98'
adendo = f'''

---

Adendo final em {now.isoformat()} — GAUSSIAN_POLAR_INTEGRATED_REVIEW

**[REAL] Revisão integrada delimitada concluída, sem achados P0, P1 ou P2.** As pendências do estrato preliminar foram resolvidas pela inspeção dos artefatos finais. Não houve recompilação adicional, execução do monólito, dos testes ou dos helpers autorais pelo revisor.

Cópia atual SHA256 `{v['working_sha256']}`, **891 embutidos**. Os quatro módulos são transposições literais dos DEV independentemente recompilados, com troca apenas dos imports; os embutidos e as raízes coincidem com os arquivos em disco. O AST Python externo ao dicionário Lean e `gate_extension.py` conservam a identidade com a mãe `core_polar_custody.json`, SHA `{v['parent_custody_sha256']}`. O hash do original e da base relidos no estrato estático foi `{v['original_sha256']}`; esta revisão não os modificou.

**Evidência autoral relida:** 189 registros válidos, dos quais **183 são os mesmos registros da mãe e seis são novas compilações autorais**: quatro módulos e duas raízes. Para cada um dos 189 foram relidos fonte, `.olean`, log JSON e bytes de stdout/stderr; hashes, caminho de saída, rc0 e presença do binário coincidem com o registro. Nos seis novos, a fonte permaneceu inalterada durante a compilação e as dependências diretas de projeto têm binários presentes, pinados e anteriores às respectivas saídas.

| Fonte integrada | Log autoral final | Conferência |
|---|---|---|
{rows}

O Audit corrente foi reparseado a partir do stdout de `{ar['log_name']}` (log SHA `{ar['log_sha256']}`). Resultado: **6.882 declarações distintas = 6.848 anteriores preservadas com os mesmos axiomas + exatamente os 34 novos alvos**. Os quatro streams locais e o Audit integrado concordam com o auditor DEV próprio; não há axioma fora de `propext`, `Classical.choice`, `Quot.sound`. Os hashes fonte/binário individuais e todos os logs capturados estão no arquivo de verificação abaixo. Não se exige identidade binária entre módulos DEV e TGLExt com caminhos de importação distintos.

`audit_stdout_sha256` e `audit_capture_sha256_full` coincidem com os bytes do stream **atual**: `{ar['stdout_sha256']}`. O escopo é `CURRENT_INCREMENTAL_AUDIT_RAW_STDOUT_BYTES`. Os dois valores da base, `{v['historical_Audit_metadata_preserved']['audit_stdout_sha256']}`, permanecem separados em `historical_v350_audit_metadata` e iguais aos da mãe.

Os **97/97 controles do autor** foram lidos e comparados, sem reexecução: os 96 anteriores permanecem e há somente o grupo `gaussian_unitary_and_same_GNS_cyclic_separating_vector_does_not_discharge_KMS_trace_or_physical_frontier`. Gate legado e anexo de fronteira são iguais aos da mãe; os seis flags maiores continuam falsos, `full_plan_complete=false` e runtime integral não executado. Preserva-se a distinção do AST: esses seis flags não são entradas diretas de `evaluate_quantum_gravity_closure`.

**Helpers e pré-gravação:** as versões de prepare/record/verify conferidas estaticamente têm os mesmos hashes do estrato DEV; as alterações aplicadas ao integrador, compilador e testador são exatamente as previstas. Batch 491→525, quatro entradas novas, controle de fronteira e metadata Audit preservada. Recorder/verifier exigem evidência e leitura dos pareceres, releem fontes/binários e preveem backup imediato de bytes, prefixo e troca por temporário verificado para cada uma das 34 superfícies. O fluxo é atômico por arquivo, sem alegação de transação única. As 34 memórias e os backups da mãe foram novamente relidos e permanecem intactos; `gaussian_polar_custody.json`, sua verificação e o novo relatório integrado autoral ainda não existiam na conferência. **Não se afirma execução ou sucesso futuro desses helpers, nem nova memória/custódia gravada.**

Evidências capturadas e hashes lidos:

{pins}

A análise matemática e a reprodução própria 4+auditor34 permanecem no {link(REV / 'REVIEW_GAUSSIAN_POLAR_DEV.md', 'parecer DEV')}, SHA `{v['own_DEV_review_sha256']}`, com a origem exata das 387 dependências herdadas e os limites da biblioteca não reconstruída. Esta rodada acrescenta inspeção independente da integração autoral, não 189 recompilações próprias.

**Limites preservados:** V é a unitária **linear** `H_I→closure(C H_I)` que entrelaça a mesma π com a representação gaussiana restrita; ξ é seu transporte inverso de Ωg, cíclico e separante na mesma π. Não se identifica o Tomita/J de ξ com o S/J original do peso, nem ξ com representante normalizado do peso infinito. A inclusão inversa com o mesmo J, igualdade global de comutantes, identificação modular/KMS, traço e runtime integral continuam fora da conclusão. Nenhuma promoção de gate ou QG é autorizada por este parecer.

Preliminar preservado integralmente em {link(backup, backup.name)}, SHA `{before_sha}`. Adendo por append de bytes e substituição atômica, sem modificar o parecer DEV, outras revisões ou memórias. **Nenhuma análise necessária deste escopo integrado permanece pendente.**
'''
raw = before + adendo.encode('utf-8')
assert len(raw) > len(before) and raw.startswith(before)
with backup.open('xb') as stream:
    stream.write(before)
assert backup.read_bytes() == before
temp = p.with_name(p.name + '.tmp_' + stamp)
with temp.open('xb') as stream:
    stream.write(raw)
assert temp.read_bytes() == raw and p.read_bytes() == before
os.replace(temp, p)
assert p.read_bytes() == raw and backup.read_bytes() == before
result = {'report': str(p), 'report_sha256': sha(p), 'backup': str(backup),
          'backup_sha256': sha(backup), 'prefix_preserved': True,
          'marker': 'GAUSSIAN_POLAR_INTEGRATED_REVIEW', 'P0_P2': [],
          'verification_sha256': sha(RUN / 'verification.json')}
pin = RUN / 'final_review_pin.json'
assert not pin.exists()
b = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
t = pin.with_name(pin.name + '.tmp')
with t.open('xb') as stream:
    stream.write(b)
assert t.read_bytes() == b
os.replace(t, pin)
print(json.dumps(result, ensure_ascii=False))
