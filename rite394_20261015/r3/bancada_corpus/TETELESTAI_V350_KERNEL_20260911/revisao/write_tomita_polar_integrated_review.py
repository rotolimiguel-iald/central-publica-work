"""Write the new integration review; no previously issued report is edited."""
from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_polar_latest_run.txt').read_text().strip())
D=max(p for p in RUN.glob('integrated_*') if (p/'verification.json').exists())
load=lambda p:json.loads(Path(p).read_bytes());hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
V=load(D/'verification.json')
assert V['all_source_binary_stream_log_pins_match'] and not V['findings']
def link(label,p,line=None):return '['+label+'](<' +Path(p).as_posix()+((':'+str(line)) if line else '')+'>)'
for n,h in V['artifacts'].items():assert hf(ROOT/n)==h,n
for p in V['own_DEV_closures']:assert hf(p['review_path'])==p['review_sha256']
assert hf(ROOT/'um.py')==V['working_sha256']
source_rows=[]
for n,t in V['transposition'].items():
    row=next(r for r in V['new_records'] if r['file']=='TGLExt/V350'+n+'.lean')
    source_rows.append('| '+n+' | '+str(len(t['targets']))+' | `'+t['integrated_sha256']+'` | `'+row['binary_sha256']+'` |')
logs='\n'.join('| '+r['file']+' | '+link(r['log_name'],D/'logs'/r['log_name'])+' | 0 / sim |' for r in V['new_records'])
pinfiles=['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json','record_tomita_polar_progress.py','verify_tomita_polar_custody.py','test_polar_custody_binary_check.py','polar_custody_binary_check.json','tomita_resolvent_flip_draft_status.json','RELATORIO_TROCA_RESOLVENTE_TOMITA_DEV.md']
pins='\n'.join('| '+link(n,ROOT/n)+' | `'+V['artifacts'][n]+'` |' for n in pinfiles)
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''# Revisão integrada — domínio exato e fator antiunitário de Tomita

INTEGRATED_TOMITA_POLAR_REVIEW

{now}. **[REAL — inspeção independente de transposição, AST, pins e logs] Nenhum achado P0–P2 nos nove módulos/41 alvos e scripts finais examinados.** Escopo integrado concluído, com a ressalva histórica dos campos globais de hash do Audit explicitada abaixo. A inspeção dos scripts de custódia não é sua execução.

Cópia relida: `{V['working_sha256']}`, **841 embutidos**. Mãe `tomita_root_custody.json`, SHA `{V['parent_custody_sha256']}`, cópia antecedente `{V['parent_working_sha256']}`. Original relido por hash `{V['original_sha256']}`, igual à cópia-base; não executado/importado.

| Evidência | Resultado e responsabilidade |
|---|---|
| DEV independente anterior | Seis módulos/25 alvos de domínio + três/16 polares, nove recompilações e dois auditores próprios rc0. Pins e pareceres preservados; não repeti essas compilações. |
| Inspeção própria desta integração | Fontes DEV/congeladas/embutidas, imports, raízes e AST; hashes atuais dos 139 pares fonte/binário, JSON e streams de logs; reextração do mapa Audit e exame documental. Zero novas execuções Lean ou scripts autorais. |
| Build executado pelo autor | 139 registros rc0: **128 pares herdados idênticos** à mãe, nove módulos novos e duas raízes recompilados. Não são 139 recompilações novas. |
| Testes executados pelo autor | 80/80 controles no relatório, 78 anteriores preservados e dois novos. Li o relatório e comparei o AST do teste; não reexecutei os controles. |
| Audit efetivo | 6.580 declarações distintas, todas no trio. As 41 novas coincidem com os dois auditores próprios DEV; os 6.539 nomes anteriores e seus axiomas foram preservados. |

**Transposição e preservação dos objetos.** As nove fontes DEV continuam nos hashes dos snapshots próprios. Cada integrada é exatamente a troca literal, nas linhas de importação, de `TGLV350.` para `TGLExt.V350`; os embutidos reproduzem seus bytes. Nenhum termo, namespace, enunciado ou hipótese foi alterado. Em relação à mãe, há exatamente nove novas chaves Lean; entre as antigas, mudaram somente `TGLExt.lean` e `TGL/Audit.lean`. Ambas importam cada novo módulo uma vez, e o Audit acrescenta exatamente 41 alvos. Assim se preservam o mesmo `S`, `B` e `H_I` já revisados, incluindo domínio inteiro, energia e fatoração antiunitária.

| Módulo | Alvos | SHA256 fonte integrada | SHA256 `.olean` integrado |
|---|---|---|---|
{chr(10).join(source_rows)}

Os pins DEV correspondentes, de origem e próprios, estão em {link('verification.json',D/'verification.json')} e nos {link('parecer do domínio',REV/'REVIEW_SCALAR_TOMITA_DOMAIN.md')} e {link('parecer polar',REV/'REVIEW_SCALAR_TOMITA_POLAR.md')}, que permanecem intocados. A mudança de caminho de módulo não é tratada como igualdade de hash entre binário DEV e integrado; cada um foi confrontado com seu registro correto.

| Nova compilação autoral relida | Log final congelado em revisão | rc / fonte inalterada |
|---|---|---|
{logs}

Todos os JSON de compilação coincidem com as entradas de `integrated_compile.json`; fontes e `.olean` atuais coincidem com `sha256`/`output_sha256`. Os 11 registros novos têm `source_unchanged_during_compile=true`, sem erros ou warnings nos streams. O mesmo confronto de pins foi feito para os 128 registros herdados. Os caminhos, hashes de stdout/stderr/JSON e raízes constam da evidência própria.

**Ressalva herdada do Audit.** `audit_stdout_sha256` e `audit_capture_sha256_full` em `kernel_incremental_evidence.json` continuam valendo `{V['inherited_Audit_hash_fields']['audit_stdout_sha256']['stored']}`, como na mãe. **Não são o hash do Audit desta integração.** O registro efetivo é `Audit_20260912_130216_472645.json`; seu stdout tem SHA `{V['final_Audit_stdout_sha256']}`. Reextraí desse stream as 6.580 entradas e confrontei integralmente com `axiom_report`, além das 41 entradas DEV. A conclusão utiliza registro→stdout→mapa atual, preservando a limitação histórica; não transforma os campos antigos em evidência nova.

Os diffs dos helpers se restringem às nove inclusões no batch/compilador e a dois grupos de controles. O batch cumulativo passa de 182 para 223 alvos; a ordem de compilação deixa os nove módulos antes das duas raízes. Removidas apenas as entradas `exact_root_domain_and_full_energy` e `same_GNS_polar_antiunitary_without_modular_promotion`, o AST do teste é igual ao anterior. Seus controles verificam presença dos nomes e conservam as condições de fronteira; não acrescentam consumo matemático a um gate. O AST Python de `um.py`, excluído somente `_EMBEDDED_KERNEL_FILES`, coincide com a mãe; `gate_extension.py` é byte a byte igual, SHA `{V['artifacts']['gate_extension.py']}`.

As seis flags maiores permanecem falsas: `qgf_continuous_modular_realization_constructed`, `qgf_unconditional_continuous_corner_proved`, `qgf_full_TGL_witness_constructed`, `gpf_H1_internal_susy_relative_gap_discharged`, `gpf_H2_smooth_modular_four_frame_discharged`, `gpf_H3_local_horizon_equilibrium_discharged`. Gate legado inalterado; plano/objetivo integral e runtime permanecem incompletos.

**Recorder, verifier e regressão binária.** Li inteiros o recorder (203 linhas), verifier (60), teste binário (54) e seu JSON. O recorder confronta mães dos dois manifestos, fontes/binários, 41 axiomas e evidências; prepara 34 superfícies herdadas. Os 34 hashes atuais conferem com a mãe. A escrita proposta conserva backup imediato em bytes na mesma pasta, temporário conferido, prefixo/crescimento e nova conferência do estado antes da substituição. Não executado por mim; relatório/custódia/verificação novos ainda ausentes na captura.

O verifier em {link('linhas 12–18',ROOT/'verify_tomita_polar_custody.py',12)} mantém exatamente, por AST, `verify_compile_record` corrigida na mãe. Em {link('linhas 31–35',ROOT/'verify_tomita_polar_custody.py',31)}, exige build válido, quantidade igual à custódia e relê **cada** fonte/`.olean`, rc0, `output_exists` e hashes. Também confere os binários DEV das nove fontes (linhas 41–44). O P2 binário anterior não reaparece.

O teste extrai as funções reais por AST; o JSON está pinado ao verifier atual, registra 139 pares e o ciclo cópia íntegra aceita → cópia corrompida rejeitada → restaurada aceita. Conferi a fixture restaurada contra os pins reais de `V350PartialSquareEnergy`, além de já ter relido os 139 binários nesta inspeção. **A rejeição intermediária é resultado autoral relido, não teste reexecutado por mim.** O JSON não contém exit code; é emitido pelo script somente após as asserções.

A minuta de relatório e memória (recorder, linhas 101–169) descreve corretamente `D(B)=D(S)`, energia nesse domínio e `U(Bx)=Sx` com antiunitário no mesmo espaço. Mantém abertas involução/identificação modular/KMS/traço e não afirma `B` limitado ou gap. Os dois DEV posteriores/quatro alvos aparecem explicitamente como **sem revisão/integração**, fora dos nove/41. Conferi seus metadados de segregação, pins documentais e ausência dos módulos/alvos no embutido/Audit; não examinei suas provas, binários ou logs e não os recompilei. Os helpers documentais adicionais apenas listados pelo recorder tiveram existência/hash conferidos, sem execução ou aprovação de conteúdo matemático posterior.

| Artefato final lido | SHA256 |
|---|---|
{pins}

Evidências próprias: {link('verification.json',D/'verification.json')}, {link('axioms.json',D/'axioms.json')}, {link('module_axioms.json',D/'module_axioms.json')} e os diffs/fontes/logs no mesmo diretório; script {link('capture_tomita_polar_integration.py',REV/'capture_tomita_polar_integration.py')}. Todas as escritas ficaram em `revisao/`. Fontes, pareceres anteriores, custódias, memórias e monólito foram preservados.

**Encerramento delimitado.** Transposição, evidências e scripts conferidos, sem P0–P2 pendentes neste escopo. Herdo a revisão matemática e os builds DEV próprios, além dos pacotes/base anteriores; a inspeção dos 139 registros não é rebuild global. Integração 9/41 reconhecida nos limites acima: não demonstra `U²=I`, conjugação modular/J, identificação com o peso/domínio máximo, KMS, traço, gap, Three Locks, condições físicas ou certificado completo consumido. Nenhuma promoção de gate/QG/runtime; execução futura da custódia permanece ato separado.
'''
out=REV/'REVIEW_SCALAR_TOMITA_POLAR_INTEGRATED.md';assert not out.exists();raw=text.encode('utf-8');q=out.with_name(out.name+'.tmp_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with q.open('xb') as f:f.write(raw)
assert q.read_bytes()==raw;q.replace(out);assert out.read_bytes()==raw
cl={'timestamp':now,'review_path':str(out),'review_sha256':hf(out),'bytes':len(raw),'lines':len(raw.splitlines()),
 'verification_sha256':hf(D/'verification.json'),'no_P0_P1_P2_findings':True,'integrated_scope_complete':True,
 'new_Lean_executions':0,'records':139,'controls':80,'Audit_distinct':6580}
p=D/'review_closure.json';assert not p.exists();b=json.dumps(cl,ensure_ascii=False,indent=2).encode();t=p.with_suffix('.tmp')
with t.open('xb') as f:f.write(b)
assert t.read_bytes()==b;t.replace(p)
print(json.dumps(cl,ensure_ascii=False,indent=2))
