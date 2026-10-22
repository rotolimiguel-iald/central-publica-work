"""Publish the integration-only review; no author code or Lean execution."""
from pathlib import Path
import datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_involution_latest_run.txt').read_text().strip())
DEST=max(p for p in RUN.glob('integrated_*') if (p/'verification.json').exists())
load=lambda p:json.loads(Path(p).read_bytes());hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
V=load(DEST/'verification.json');H=load(DEST/'helper_inspection.json');C=load(RUN/'closure_dev.json')
assert V['findings']==H['findings']==[] and V['integrated_records']==143 and V['new_axioms_equal_own_DEV']==19
assert hf(C['report'])==C['sha256']
assert all(hf(ROOT/n)==pin for n,pin in V['artifacts'].items())
assert all(hf(ROOT/n)==pin for n,pin in V['extra_recorder_artifact_pins_existence_only'].items())
assert all(hf(p)==r['sha256'] for p,r in V['parent_surfaces_current_pins'].items())
link=lambda p,label=None,line=None:f'[{label or Path(p).name}](<{Path(p).as_posix()}{":"+str(line) if line else ""}>)'
stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
ar=next(r for r in V['new_records'] if r['file']=='TGL/Audit.lean')
table=[]
for r in V['new_records']:
    table.append(f"| {link(ROOT/'logs'/r['log_name'],r['log_name'])} | `{r['source_sha256']}` | `{r['binary_sha256']}` |")
pinlist=['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json',
 'prepare_tomita_involution_stage.py','record_tomita_involution_progress.py','verify_tomita_involution_custody.py',
 'generate_tomita_involution_record_helpers.py']
pinrows=[f"| {link(ROOT/n)} | `{V['artifacts'][n]}` |" for n in pinlist]
text=f'''# Revisão integrada — involução polar de Tomita

INTEGRATED_TOMITA_INVOLUTION_REVIEW

{stamp}. **[REAL — inspeção integrada concluída] Sem achados P0, P1 ou P2 no lote quatro módulos/19 alvos.** Conferidos fontes/embutidos/imports, 143 pares fonte/binário e seus registros/streams, raízes, preservação do Audit anterior, 82 controles relatados pelo autor, AST Python e versões finais dos helpers. Não houve nova execução Lean, experimento de corrupção binária, execução de testes autorais, monólito, recorder, verifier ou gerador pelo revisor.

Cópia `um.py` SHA256 lido `{V['working_sha256']}`; pai integrado `{V['parent_working_sha256']}`. Original canônico e cópia-base relidos, SHA256 `{V['original_sha256']}`. A análise dos bytes e do AST não executou nem importou o monólito.

| Evidência | Conferência efetiva nesta rodada |
|---|---|
| Quatro DEV/19 alvos | Reutilizada a revisão matemática e recompilação próprias encerradas em {link(C['report'])}, SHA256 `{C['sha256']}`; não repetidas. Pins DEV atuais coincidem com os snapshots próprios. |
| Compilação integrada autoral | 143 registros rc0/output_exists; 137 fontes e binários idênticos ao pai, quatro módulos novos e duas raízes recompilados. Todos os 143 pares foram relidos por hash. Não são 143 recompilações novas. |
| Audit final | 6.599 declarações distintas reextraídas do stdout real: 6.580 anteriores preservadas integralmente e 19 novas; mapa exatamente igual a `kernel_incremental_evidence.json`, axiomas somente no trio. Os 19 novos mapas coincidem com o auditor DEV próprio. |
| Controles autorais | 82 nomes únicos, todos `passed=true`: 80 anteriores preservados e dois novos. Relatório e condições examinados; testes não reexecutados pelo revisor. |
| Embutido/Python/gate | 845 fontes; quatro chaves novas, nenhuma removida, apenas duas raízes alteradas entre as chaves antigas. AST Python fora de `_EMBEDDED_KERNEL_FILES` igual ao pai; `gate_extension.py` idêntico por bytes. |

**Transposição e identidade.** Para cada fonte congelada, comparei bytes depois da única substituição `^import TGLV350.` → `import TGLExt.V350`. O resultado coincide com `kernel/TGLExt/V350*.lean` e com o valor efetivo no dicionário embutido. `AntiunitaryPositiveConjugation` não tem import DEV a reescrever: sua fonte permanece idêntica por bytes. Os namespaces declarados continuam `TGLV350.Regular`; não houve renomeação de declarações, mudança de hipóteses ou novo objeto H_I/S/R/B/U. Os respectivos `.olean` integrados têm identidade de módulo própria e são conferidos contra seus logs, não confundidos com os binários DEV.

`TGLExt.lean` e `TGL/Audit.lean` importam cada módulo novo exatamente uma vez. O diff do Audit acrescenta precisamente as 19 impressões previstas, sem remover ou mudar a multiplicidade dos nomes anteriores. As raízes têm registros finais próprios rc0 e binários relidos. Os seis registros novos indicam `source_unchanged_during_compile=true`, sem erro no stdout/stderr; permanecem somente os três avisos de depreciação de API já documentados no DEV.

| Log autoral novo, rc0 | SHA256 da fonte integrada | SHA256 do .olean integrado |
|---|---|---|
{chr(10).join(table)}

Os hashes dos JSONs e de ambos os streams de todos os registros estão em {link(DEST/'verification.json')}; snapshots das fontes/JSONs/stdout/stderr foram preservados na árvore da revisão. Em particular, o JSON final {link(ROOT/'logs'/ar['log_name'])} tem SHA256 `{ar['log_sha256']}` e seu stdout real tem SHA256 `{ar['stdout_sha256']}`. Desse stream foi extraído o {link(DEST/'axioms.json','mapa próprio de 6.599 declarações')}, além dos {link(DEST/'module_axioms.json','mapas dos quatro módulos')}.

**Ressalva herdada do Audit.** Os campos globais `audit_stdout_sha256` e `audit_capture_sha256_full` continuam com `{V['inherited_Audit_hash_fields']['audit_stdout_sha256']['stored']}`, idêntico ao pai e diferente do stdout final. São metadados históricos; não os usei como pin do Audit atual. A evidência atual é registro final → JSON/stream real → mapa reextraído, com os hashes acima. A ressalva permanece explícita; não é nova falha da prova nem foi corrigida ficticiamente nesta inspeção.

**Helpers e controles.** Li integralmente `prepare_tomita_involution_stage.py`, `record_tomita_involution_progress.py` (versão final de 206 linhas), `verify_tomita_involution_custody.py` e `generate_tomita_involution_record_helpers.py`. As mudanças efetivas em `integrate_v350.py` são apenas os quatro nomes novos no batch e 223→242 alvos acumulados. Em `compile_integrated.py`, apenas os quatro módulos foram acrescentados imediatamente antes das duas raízes, preservando a lógica anterior. O código de `test_gate_extension.py`, retiradas apenas as duas entradas novas, tem AST idêntico ao pai. Os backups imediatos dos três helpers correspondem por bytes aos artefatos pinados da mãe matemática; diffs e pins estão em {link(DEST/'helper_inspection.json')}.

Os controles novos são:

- `same_GNS_resolvent_transport_without_weight_identification_does_not_discharge_KMS_trace_or_physical_frontier`;
- `same_GNS_polar_involution_without_KMS_promotion_does_not_discharge_KMS_trace_or_physical_frontier`.

As condições exigem presença dos alvos respectivos, seis flags maiores exatamente `False`, gate legado inalterado e `full_plan_complete=False`. As seis flags relidas são `qgf_continuous_modular_realization_constructed`, `qgf_unconditional_continuous_corner_proved`, `qgf_full_TGL_witness_constructed`, `gpf_H1_internal_susy_relative_gap_discharged`, `gpf_H2_smooth_modular_four_frame_discharged`, `gpf_H3_local_horizon_equilibrium_discharged`. `full_monolithic_runtime_run=False`. Esses controles verificam a fronteira de consumo; não constituem prova de KMS ou traço. `gate_extension.py` conserva o SHA256 `{V['artifacts']['gate_extension.py']}` do pai.

Em {link(ROOT/'verify_tomita_involution_custody.py',line=12)}, `verify_compile_record` é idêntica por AST à função corrigida e testada no pai: exige caminho sob `ROOT/kernel`, rc0/output_exists, hash da fonte, existência e hash do binário. O laço em {link(ROOT/'verify_tomita_involution_custody.py',line=35)} percorre todos os registros e confronta a quantidade à custódia; o próprio `integrated_compile.json` está no conjunto de pins de artefatos. Assim, a correção do antigo P2 de releitura binária foi preservada. Conforme o escopo, não repeti o experimento de corrupção, nem executei essa função autoral; fiz a releitura independente dos 143 pares.

**Duas mães e memória.** A mãe matemática é {link(ROOT/'tomita_polar_custody.json')}, SHA256 `{V['parent_custody_sha256']}`. A mãe documental é {link(ROOT/'tomita_involution_dev_memory_custody.json')}, SHA256 `{V['memory_parent_custody_sha256']}`. Sua ligação ao pai, pin do manifesto, pin do relatório DEV e working SHA anterior coincidem. As 34 superfícies atuais coincidem com os pins da mãe documental; seus backups imediatos têm bytes/prefixos e localização conferidos, e os estados anteriores coincidem com os pins da mãe matemática. Isso preserva o append DEV interveniente, em vez de exigir que as memórias ainda tenham o estado anterior à inscrição DEV.

O recorder usa explicitamente a mãe documental para os 34 estados `before`; exige os pins antes de escrever, cria backup de bytes na mesma pasta, confere o temporário, preserva o prefixo e só então substitui. O verifier confere as duas mães, hashes dos artefatos/revisões, estados atuais, backups e prefixos crescentes. O novo relatório, recorder e nova custódia ainda não foram executados/materializados nessa captura: a futura escrita dos 34 adendos foi examinada estaticamente, não declarada realizada. Parecer DEV e pareceres anteriores mantêm seus hashes.

**Alcance do texto final.** As minutas `report` e `note` do gerador coincidem por AST com as do recorder final. Elas afirmam U²=I para o fator original de S=UB e D(B)=D(S), distinguem execução incremental de rebuild global e mantêm peso/KMS/traço/gate/runtime fora da conclusão. A versão final separa corretamente o ideal I de `HasFiniteDualSquare` — cota uniforme da forma em todos os vetores — do domínio de finitude escalar n_ν. **Não se exige nem se presume I=n_ν.** Uma identificação adequada por completamento e núcleo de gráfico no domínio máximo permanece obrigação futura, sem estar provada por esta integração. Essa precisão de alcance é registrada aqui sem alterar o parecer DEV encerrado.

Pins finais efetivamente lidos:

| Artefato | SHA256 |
|---|---|
{chr(10).join(pinrows)}

**Proveniência própria e encerramento.** {link(DEST/'verification.json')} SHA256 `{hf(DEST/'verification.json')}`; {link(DEST/'helper_inspection.json')} SHA256 `{hf(DEST/'helper_inspection.json')}`. O script próprio {link(REV/'capture_tomita_involution_integration.py')} apenas lê/analisa dados e grava snapshots em `revisao/`. Não houve recompilação Lean nesta rodada; a evidência matemática própria é herdada do DEV quatro/19 já encerrado. Os 137 registros preservados e as bibliotecas mantêm sua proveniência anterior, sem alegação de reconstrução global independente.

**Sem P0–P2 e sem verificação necessária restante neste escopo integrado.** Está conferida a transposição e compilação autoral pinada da involução polar formal no mesmo H_I. Identificação do domínio máximo do peso, KMS, identificação com outros J, traço/Three Locks, física, objetivo integral e runtime não são promovidos. Escritas do revisor exclusivamente em `revisao/`; fontes, monólito, memórias, logs autorais e pareceres anteriores intocados.
'''
out=REV/'REVIEW_SCALAR_TOMITA_INVOLUTION_INTEGRATED.md';assert not out.exists()
raw=text.encode('utf8');tmp=out.with_name(out.name+'.tmp_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(out);assert out.read_bytes()==raw
result={'timestamp':stamp,'report':str(out),'sha256':hf(out),'bytes':len(raw),'lines':len(raw.splitlines()),'marker':'INTEGRATED_TOMITA_INVOLUTION_REVIEW','scope_complete':True,'findings_P0_P2':[],'verification_sha256':hf(DEST/'verification.json'),'helper_inspection_sha256':hf(DEST/'helper_inspection.json')}
p=DEST/'review_closure.json';assert not p.exists();t=p.with_suffix('.tmp');b=json.dumps(result,ensure_ascii=False,indent=2).encode();t.write_bytes(b);assert t.read_bytes()==b;t.replace(p)
print(json.dumps(result,ensure_ascii=False,indent=2))
