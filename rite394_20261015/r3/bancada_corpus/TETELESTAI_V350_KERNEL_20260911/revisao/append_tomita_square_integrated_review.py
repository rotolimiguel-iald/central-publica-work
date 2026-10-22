"""Append the delimited integrated review after read-only checks; no author execution."""
from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'tomita_square_latest_run.txt').read_text().strip())
CAP=max(p for p in RUN.glob('integrated_*') if (p/'verification.json').exists())
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
V=load(CAP/'verification.json');D=load(RUN/'closure_dev.json');E=load(CAP/'kernel_incremental_evidence.json')
OLD=max(p for p in (REV/'closed_tomita_batch_independent_20260912_101455_759612').glob('final_integrated_*') if (p/'verification.json').exists())
OE=load(OLD/'kernel_incremental_evidence.json')
for k in ['audit_stdout_sha256','audit_capture_sha256_full']:assert E[k]==OE[k]
for f,h in V['artifacts'].items():assert sha((ROOT/f).read_bytes())==h
assert sha((ROOT/'um.py').read_bytes())==V['working_sha256']
for n,r in V['transposition'].items():
    assert sha((ROOT/'kernel/TGLV350'/(n+'.lean')).read_bytes())==r['dev_sha256']
    assert sha((ROOT/'kernel/TGLExt'/('V350'+n+'.lean')).read_bytes())==r['integrated_sha256']
P=REV/'REVIEW_SCALAR_TOMITA_ADJOINT.md';old=P.read_bytes();assert sha(old)==D['review_sha256']
marker='INTEGRATED_TOMITA_SQUARE_REVIEW';assert marker.encode() not in old
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
backup=P.with_name(P.name+'.bak_'+stamp)
def link(label,p,line=None):return f'[{label}](<{Path(p).as_posix()}{":"+str(line) if line else ""}>)'
artifact_names=['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json',
 'gate_extension.py','record_tomita_square_progress.py','verify_tomita_square_custody.py']
artifacts='\n'.join(f"| {n} | `{V['artifacts'][n]}` |" for n in artifact_names)
rows='\n'.join(f"| {r['file']} | `{r['source_sha256']}` | `{r['binary_sha256']}` |" for r in V['new_records'])
logrows='\n'.join(f"| {r['log_name']} | `{r['log_sha256']}` |" for r in V['new_records'])
aud=V['roots']['TGL/Audit.lean']
text=f'''

## ADENDO — conferência da integração dos sete módulos/53 alvos

<!-- {marker} -->

{date}. **[REAL — inspeção integrada encerrada; nenhum achado P0, P1 ou P2 novo.]** Foram conferidos exclusivamente os mesmos sete módulos/53 alvos do parecer DEV, as duas raízes, seus registros, a transposição, a AST, os controles e os dois scripts prospectivos de registro/custódia. **Nenhum processo Lean ou teste autoral foi executado neste adendo.** A matemática e as dez execuções próprias DEV já documentadas permanecem a evidência independente de recompilação; a integração abaixo é sustentada pela inspeção própria dos bytes e pela releitura dos resultados executados pelo autor.

O prefixo anterior foi preservado integralmente: {len(old)} bytes, SHA `{sha(old)}`, com {link('backup imediato de bytes',backup)}. Nenhum parecer custodiado anterior foi alterado.

**Snapshot conferido:** cópia **`{V['working_sha256']}`**, antecessor **`{V['parent_working_sha256']}`**, original **`{V['original_sha256']}`**. O original e a cópia-base local concordam com o pin antecedente. A cópia antecessora foi localizada pelo hash em backup real e comparada por AST, sem executar/importar nenhum dos monólitos.

### Transposição, mesmos objetos e integração

Nas sete fontes, a substituição literal de bytes `^import TGLV350.` por `import TGLExt.V350` reproduz **exatamente** o arquivo integrado. As fontes DEV coincidem com os pins aprovados. Cada valor embutido corresponde aos bytes da fonte integrada. Não houve mudança de enunciado, hipótese, namespace de declaração, corpo de prova, instância, definição de domínio ou representação: os nomes permanecem `TGLV350.Regular.*`, e S, S†, A e H_I continuam os objetos do parecer DEV. A leitura não reclassifica a auto-adjunticidade como identificação polar ou modular do peso.

O dicionário passa a **{V['embedded_files']} arquivos**, com exatamente sete entradas adicionadas e nenhuma removida. Entre as entradas preexistentes, somente `TGLExt.lean` e `TGL/Audit.lean` mudaram. Cada raiz importa os sete módulos uma vez; o Audit acrescenta exatamente **53** `#print axioms`, preservando todos os alvos antigos e suas multiplicidades. Os diffs estão em {link('TGLExt',CAP/'TGLExt.lean.diff.txt')} e {link('Audit',CAP/'TGL_Audit.lean.diff.txt')}. Não há inclusão de módulo posterior neste conjunto.

**AST Python fora de `_EMBEDDED_KERNEL_FILES` idêntica ao antecessor**, com hash da AST normalizada `{V['python_AST_sha256']}`. `gate_extension.py` coincide byte a byte com o artefato pinado na custódia antecedente. As alterações estáticas dos helpers são delimitadas: sete nomes na lista do integrador, sete módulos na lista de compilação, atualização da contagem cumulativa de seu lote anterior de 99 para 152 (=99+53) e duas entradas no dicionário de controles. Isso não significa 152 alvos novos nesta revisão.

### Resultados autorais relidos e pins medidos

**125 registros rc0 = 116 herdados + sete módulos novos + duas raízes novas.** Os 116 mantêm os mesmos hashes de fonte e binário da captura custodiada; não são 125 recompilações novas. Para todos os 125, conferi fonte, .olean, JSON individual coincidente com o registro e os streams preservados. Nos nove novos, os logs declaram também `lean_returncode=0` e `source_unchanged_during_compile=true`; não há warnings nesses outputs. O mecanismo de cache segue o estrato anterior: hashes de fonte/binário e frescor dos imports locais, sem rebuild dos pacotes.

| Fonte integrada recompilada pelo autor | SHA256 fonte | SHA256 .olean relido |
|---|---|---|
{rows}

| Log final autoral | SHA256 JSON |
|---|---|
{logrows}

O stdout final de `TGL/Audit.lean`, SHA **`{aud['stdout_sha256']}`**, foi analisado diretamente: **6509 declarações distintas**, sem axiomas fora de `propext`, `Classical.choice`, `Quot.sound`. O seu mapa coincide com `kernel_incremental_evidence.json`; o incremento em relação ao Audit anterior é exatamente o conjunto dos **53 alvos**, cujos axiomas coincidem também com o auditor DEV próprio. Os axiomas antigos permanecem iguais. Isto confere as declarações e axiomas integrados, apoiado na transposição literal dos tipos já impressos; **não houve novo `#check` ou nova compilação própria de raízes/integrados**.

**77/77 controles constam aprovados nos registros autorais**, com os 75 anteriores preservados. As duas entradas novas testam presença dos respectivos teoremas, as seis flags falsas e ausência de alteração do gate/plano: `maximal_antilinear_adjoint_does_not_discharge_KMS_trace_or_physical_frontier` e `positive_selfadjoint_Tomita_square_does_not_discharge_KMS_trace_or_physical_frontier`. Removidas somente essas duas entradas do dicionário da versão atual, a AST inteira de `test_gate_extension.py` coincide com a anterior. O corpo do laço e as condições antigas não mudaram. Uma primeira comparação própria exigiu indevidamente o mesmo nó inteiro do laço e interrompeu a inspeção; o diff mostrou apenas essas duas entradas, o comparador foi corrigido e a captura concluída. A interrupção está preservada, sem ser tratada como defeito autoral nem como teste Lean fracassado.

**As seis flags maiores são False** (`qgf_continuous_modular_realization_constructed`, `qgf_unconditional_continuous_corner_proved`, `qgf_full_TGL_witness_constructed`, `gpf_H1_internal_susy_relative_gap_discharged`, `gpf_H2_smooth_modular_four_frame_discharged`, `gpf_H3_local_horizon_equilibrium_discharged`). `frontier.legacy_gate_changed=false`, `frontier.full_plan_complete=false`, `full_monolithic_runtime_run=false`; o valor textual do gate legado também coincide com o antecedente. Nenhum certificado novo é consumido pelo gate.

**Limite de proveniência herdado:** `audit_stdout_sha256` e `audit_capture_sha256_full` no objeto global `kernel_incremental_evidence.json` continuam iguais ao estrato anterior (`{E['audit_stdout_sha256']}`); não são o hash do stdout incremental atual. Para esta rodada, a cadeia usada foi o **log específico final de Audit → stream relido → 6509 axiomas**, e não aqueles campos históricos. Os metadados globais herdados não foram promovidos a evidência de rebuild completo da base. Também não foi refeito o inventário I/O histórico, a auditoria de todos os pacotes ou qualquer runtime.

### Scripts e minuta de custódia — inspeção integral, sem execução

Li as **211** linhas de {link('record_tomita_square_progress.py',ROOT/'record_tomita_square_progress.py')} e as **78** linhas de {link('verify_tomita_square_custody.py',ROOT/'verify_tomita_square_custody.py')}, inclusive toda a minuta interpolada e o adendo de memória. A sintaxe AST é válida. As contagens são coerentes: grupos `adjoint=23`, `composition=18`, `resolvent=6`, `selfadjoint=6`, total **53**, sem alvo 55 ou módulo futuro contado. O texto mantém domínio exato, mesmo H_I, densidade/sobrejetividade/auto-adjunticidade deduzidas, núcleo trivial sem gap, ausência de I=n_ν e estatuto aberto de polar/KMS/traço.

O recorder exige `--review-read` e o marcador deste adendo (linhas 62–71), verifica original/cópia/custódia anterior, AST, registros, transposição, axiomas e flags antes de escrever o relatório. **32 superfícies distintas existentes** são calculadas nas linhas 178–180: as 30 da custódia anterior mais `RELATORIO_TOMITA_FECHADO_INTEGRADO.md` e `ROTA_APOS_TOMITA_FECHADO.md`. Não incluem pareceres em `revisao/`. A lista e seus hashes de leitura estão na verificação própria; esses hashes são um retrato da inspeção, não uma exigência de imutabilidade das memórias compartilhadas até a execução futura.

O mecanismo das linhas 26–53 lê o estado imediato, cria backup com `xb`, compara seus bytes, grava temporário, verifica bytes/tamanho, reconfere o estado esperado e só então substitui. O append conserva o prefixo e cresce; a custódia registra o hash do backup efetivamente tocado e eventuais mudanças intervenientes desde o antecessor. O verifier (linhas 29–39) confere os hashes das superfícies, o prefixo estrito, o backup imediato e a classificação das mudanças intervenientes; depois confere binários/registros, controles, alvos e flags. Sua própria saída também usa backup e substituição por temporário (linhas 63–77). **Trata-se de 32 backups/prefixos previstos e mecanismo inspecionado, não de custódia executada/verificada por mim.** Na leitura, os novos relatório integrado, custody e verification ainda não existiam.

A referência a `ROTA_POLAR_MESMO_GNS.md` aparece como **rota posterior, sem prova nova**. Não examinei sua matemática nem qualquer fonte posterior; nenhuma entra na conclusão. O pin do inventário I/O no recorder é apenas transporte documental de artefato histórico e não liberação de runtime. Não houve achado documental P2 neste escopo.

| Artefato lido e congelado na revisão | SHA256 |
|---|---|
{artifacts}

Captura e verificações: {link('verification.json',CAP/'verification.json')}; {link('axiomas extraídos do Audit final',CAP/'axioms.json')}. A captura guarda os scripts lidos, fontes integradas, JSONs e streams, com hashes. Os pins do compilador, dependências próprias e limitações binárias do DEV permanecem nos estratos anteriores; esta inspeção não os recompilou.

**Conclusão integrada delimitada:** transposição e evidências conferidas para os sete/53, sem P0–P2 e sem análise necessária pendente neste adendo. Permanecem os limites DEV: núcleo trivial não é gap; nenhuma identificação polar/modular do peso, KMS, traço, Three Locks/H1–H3, física ou runtime completo. Não houve execução/importação de monólito, scripts autorais, recorder ou verifier; fontes e memórias ficaram intactas e todas as saídas próprias estão em `revisao/`.
'''
# The complete report remains an exact prefix before the authorized append.
raw=old+text.encode('utf-8')
with backup.open('xb') as f:f.write(old)
assert backup.read_bytes()==old
tmp=P.with_name(P.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and len(raw)>len(old)
assert P.read_bytes()==old
tmp.replace(P);assert P.read_bytes().startswith(backup.read_bytes()) and P.read_bytes()==raw
close={'timestamp':date,'marker':marker,'status':'INTEGRATED_SCOPE_COMPLETE_NO_P0_P1_P2',
 'review_path':str(P),'review_sha256':sha(raw),'review_bytes':len(raw),'review_lines':len(raw.splitlines()),
 'backup':str(backup),'backup_sha256':sha(old),'exact_prefix_preserved':True,'integrated_modules':7,'targets':53,
 'author_integrated_records':125,'reused_records':116,'author_new_compilations':9,'author_controls':77,'audit_distinct':6509,
 'own_Lean_processes_this_addendum':0,'working_sha256':V['working_sha256'],'findings':[],
 'necessary_analysis_remaining':False,'custody_execution_reviewed':False,'author_programs_executed':False}
q=CAP/'closure_integrated.json';assert not q.exists();b=json.dumps(close,ensure_ascii=False,indent=2).encode();t=q.with_suffix('.tmp')
with t.open('xb') as f:f.write(b)
assert t.read_bytes()==b;t.replace(q)
print(json.dumps(close,ensure_ascii=False,indent=2))
