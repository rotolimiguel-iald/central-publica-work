"""Create the final integration review; no author program execution."""
from pathlib import Path
import datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
DEV=Path((REV/'scalar_weight_gns_latest_run.txt').read_text().strip())
OUT=DEV/'integrated_20260912_150136_734138'
load=lambda p:json.loads(Path(p).read_bytes());hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
V=load(OUT/'verification.json');PRE=Path(V['preflight_path']);P=load(PRE/'preflight.json')
assert not V['findings'] and V['all_source_binary_log_stream_pins_match']
assert all(hf(ROOT/f)==h for f,h in V['artifact_pins'].items())
assert hf(ROOT/'um.py')==V['working_sha256']
assert hf(V['own_DEV_closure']['report'])==V['own_DEV_closure']['sha256']
assert not (REV/'REVIEW_SCALAR_WEIGHT_GNS_INTEGRATION_PREFLIGHT.md').exists()
def link(label,p,line=None):
    return f'[{label}](<{Path(p).as_posix()}{":"+str(line) if line else ""}>)'
def code(f,line):return link(f+':'+str(line),ROOT/f,line)
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
ar=V['final_Audit_record'];legacy=V['inherited_Audit_hash_fields']['audit_stdout_sha256']['stored_sha256']
rows=[]
for r in V['new_records']:
    rows.append(f"| {link(r['file'],ROOT/'kernel'/r['file'])} | {link(r['log_name'],OUT/'logs'/r['log_name'])} | `{r['binary_sha256']}` |")
pinfiles=['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json',
 'prepare_scalar_weight_gns_stage.py','record_scalar_weight_gns_progress.py','verify_scalar_weight_gns_custody.py',
 'integrate_v350.py','compile_integrated.py','test_gate_extension.py']
pins='\n'.join(f"| {link(f,ROOT/f)} | `{V['artifact_pins'][f]}` |" for f in pinfiles)
report=f'''INTEGRATED_SCALAR_WEIGHT_GNS_REVIEW

{stamp} — [REAL — conferência independente da integração e inspeção estática dos helpers]. Mesmo pacote DEV, nove módulos/60 alvos; nenhuma nova compilação pelo revisor.

**Conclusão: nenhum achado P0, P1 ou P2 no escopo examinado.** Conferidos os 152 pares fonte/binário e seus registros/streams: 141 registros idênticos aos maternos e 11 compilações autorais novas, nove módulos e duas raízes, todas rc0 e com fonte inalterada durante a compilação. O stdout final do Audit contém 6659 declarações distintas: preserva as 6599 anteriores com os mesmos axiomas e acrescenta exatamente os 60 alvos do DEV. Os registros autorais mostram 84/84 controles. Fontes transpostas, embutido, AST Python, gate, minuta e lógica das 34 superfícies conferem nos limites abaixo. A revisão integrada está encerrada; recorder e verifier continuam sem execução nesta revisão.

O preflight já estava inspecionado e capturado, mas seu parecer Markdown ainda não havia sido criado quando o pedido foi redirecionado. Sua análise foi incorporada aqui; o snapshot {link('preflight preservado',PRE)} permanece intacto. O parecer {link('DEV anterior',V['own_DEV_closure']['report'])}, SHA256 `{V['own_DEV_closure']['sha256']}`, não foi alterado.

**Objeto e transposição.** Cópia um.py relida: `{V['working_sha256']}`; 854 embutidos. Mãe tomita_involution_custody.json: `{V['parent_custody_sha256']}`, com cópia `{V['parent_working_sha256']}`. Os nove DEV permanecem nos hashes do manifesto previamente revisto. Cada TGLExt/V350*.lean é exatamente o DEV com a substituição de prefixos `import TGLV350.` → `import TGLExt.V350`; a comparação foi de bytes, além dos hashes. Cada fonte integrada coincide com os bytes UTF-8 de sua entrada embutida. Os nomes continuam TGLV350.Regular, incluindo as declarações qualificadas HasFiniteScalarSquare.*. A substituição não alterou enunciados, hipóteses, provas, instâncias ou os objetos herdados.

Entraram somente nove novas chaves. Das 845 antigas, 843 são idênticas; somente TGLExt.lean e TGL/Audit.lean mudaram, com nove imports adicionais em cada raiz e os 60 #print axioms exatos acrescidos ao Audit. Todos os nomes e multiplicidades anteriores foram preservados. O AST do monólito, excluindo somente o valor da atribuição única _EMBEDDED_KERNEL_FILES, coincide com o backup materno `{Path(P['old_monolith_backup']).name}`, pinado pelo hash da mãe. Gate_extension.py é byte a byte o mesmo, SHA256 `{V['artifact_pins']['gate_extension.py']}`.

**Evidência própria e autoral, separadas.**

| Verificação | Evidência efetiva |
|---|---|
| Matemática DEV | Recompilação própria anterior dos nove módulos e auditor dos 60 tipos/universos/axiomas, 10 rc0; nove binários DEV idênticos aos autorais. Herança do parecer DEV; não repetida. |
| Transposição/integração | Comparação própria de bytes, hashes, imports, raízes, AST e nomes; nesta rodada nenhum processo Lean. |
| Build integrado | Leitura própria dos 152 pares reais fonte/.olean, JSONs de compilação e stdout/stderr; execução Lean atribuída ao autor. 141 registros preservados exatamente, 9+2 novos rc0. |
| Axiomas | Cada um dos nove stdout novos contém exatamente seus alvos e o mesmo mapa de axiomas do auditor DEV próprio. O Audit final foi parseado independentemente e comparado integralmente ao axiom_report e ao mapa materno. |
| Controles | Relido gate_tests.json: 84/84, preservados os 82 controles anteriores e acrescentados os dois controles deste pacote. Não executei test_gate_extension.py. |
| Memórias/custódia | Inspeção integral dos helpers e releitura dos 34 estados maternos atuais; novos backups, adendos e verificação pós-registro ainda não executados. |

Todos os 60 novos alvos dependem exatamente de propext, Classical.choice e Quot.sound. Todos os 6659 alvos do mapa integral estão dentro dessa lista permitida. Não há erro nos streams aceitos. Os 11 registros novos trazem lean_returncode=0 e source_unchanged_during_compile=true. Alguns registros antigos têm esquema anterior sem lean_returncode separado; foram aceitos pelo rc0 existente, identidade integral com o registro materno e hashes fonte/binário relidos, sem inventar esse campo. A primeira passagem do meu capturador interrompeu ao exigir o campo histórico ausente; foi corrigida apenas na árvore revisao, com backup de bytes, sem alterar evidência autoral ou disparar rebuild.

| Fonte recompilada pelo autor | Log final relido | SHA256 .olean relido |
|---|---|---|
{chr(10).join(rows)}

**Cadeia do Audit e ressalva herdada.** A âncora atual é {link(ar['log_name'],ROOT/'logs'/ar['log_name'])}, SHA256 `{ar['log_sha256']}`; fonte `{ar['source_sha256']}`, .olean `{ar['binary_sha256']}`. O stdout efetivo tem SHA256 `{ar['stdout_sha256']}`. Esse stream foi extraído do último registro real, parseado e confrontado a kernel_incremental_evidence.json; houve igualdade integral dos mapas, sem perda das 6599 entradas anteriores.

Os campos globais históricos `audit_stdout_sha256` e `audit_capture_sha256_full` continuam `{legacy}`, ambos iguais aos da mãe e **diferentes do stdout atual**. Não foram usados como âncora da prova atual. Esta é a ressalva de proveniência já conhecida, mantida explicitamente; a ligação válida nesta revisão é registro final → stream relido → mapa de axiomas. Hash da fonte, do binário ou de JSON agregado não foi apresentado como hash do stdout.

**Scripts e controles.** Os três backups `.bak_20260912_144900_431482` coincidem exatamente com os pins maternos. As diferenças foram lidas e confirmadas por AST: {code('integrate_v350.py',65)} acrescenta só os nove nomes e altera o total de tomita_batch de 242 para 302; {code('compile_integrated.py',173)} acrescenta só os nove módulos antes das duas raízes; {code('test_gate_extension.py',426)} acrescenta só duas entradas ao laço de controles. Removidas essas alterações em memória, cada AST coincide com o materno. Permanecem herdadas as rotinas de compilação, cache por hash/frescor e avaliação do gate. A programação total é 152, contando duas entradas paralelas iniciais além das 150 sequenciais; esse total agora foi confrontado aos registros concluídos.

Os controles novos são:

- `{V['added_controls'][0]}`;
- `{V['added_controls'][1]}`.

Ambos verificam seus nomes de prova e exigem seis flags maiores false, legacy_gate_changed=false e full_plan_complete=false. O relatório executado confirma esses estados e full_monolithic_runtime_run=false. O valor do gate legado é igual ao materno; o pacote não habilita novo consumo de KMS/traço/física. A presença de 84 controles não equivale a execução integral do monólito.

**Helpers e minuta: leitura integral, não execução.** Os bytes finais de prepare_scalar_weight_gns_stage.py, record_scalar_weight_gns_progress.py e verify_scalar_weight_gns_custody.py permanecem iguais aos capturados no preflight. O preparador exige leitura do parecer DEV, mãe e pins e faz backup dos bytes imediatos/temporário verificado antes de alterar os três scripts. As alterações concretas correspondem ao que ele prepara.

O recorder, {code('record_scalar_weight_gns_progress.py',49)}, exige `--review-read`, parecer DEV e este parecer integrado final com marcador próprio; confere mãe, original/base/cópia/testes, AST, rc0 e hashes fonte/.olean dos registros, transposição e mapas dos 60 alvos. As 34 superfícies vêm da custódia mãe e foram relidas agora com exatamente os hashes esperados. Antes de registrar, ele captura os bytes atuais e exige esses pins; em cada escrita verifica que o estado não mudou, cria backup imediato no mesmo diretório, preserva o prefixo byte a byte, acrescenta respeitando os fins de linha e substitui por temporário conferido. A atomicidade é por arquivo, não uma transação global sobre 34 destinos. Nenhum parecer em revisao faz parte dessas superfícies.

O verifier, {code('verify_scalar_weight_gns_custody.py',29)}, relê fonte e binário de todos os registros, exige rc0/output_exists e seus hashes, e compara a quantidade com a custódia. A verificação corrigida anteriormente para binários continua presente, agora no laço em vez de função separada; arquivo ausente faz a leitura falhar. Confere também pai, artefatos, pareceres, módulos e flags, e, nas linhas 37–41, hashes dos backups, prefixo integral e crescimento. Não executei o verifier nem repeti experimento de corrupção. Esses mecanismos foram inspecionados; não são alegação de backups novos já produzidos.

A minuta interpolada do relatório e das memórias, linhas 102–177 do recorder, está de acordo com o DEV: completamento de Λ_ν(n_ν)=H_I e fecho da estrela no núcleo n_ν∩n_ν* igual ao gráfico do mesmo S, mantendo S=UB e U²=I anteriores; não afirma I=n_ν nem D(S)=imagem algébrica sem fechamento. Marca fluxo modular/KMS, traço/canto, física e consumo integral como abertos. Os comentários sobre tower_kms/tState_kms foram confrontados somente aos tipos matriciais por andar em TowerModular:113 e RightMult:122; a minuta não os converte em KMS do peso no core. Não reabri sua investigação matemática.

**Pins dos artefatos finais.**

| Artefato | SHA256 relido |
|---|---|
{pins}

Evidência detalhada própria: {link('verification.json',OUT/'verification.json')} (SHA256 `{hf(OUT/'verification.json')}`), {link('mapa integral de axiomas',OUT/'axioms.json')} e {link('mapas dos nove módulos',OUT/'new_module_axioms.json')}. O JSON registra todos os 152 hashes fonte/binário/JSON/stdout/stderr, os 11 novos registros, as 34 superfícies, pins e a ressalva histórica do Audit. O snapshot estático anterior é preservado; a contagem final de nomes inclui o apóstrofo herdado em TGLExt.comm_of_fixed', sem colapsá-lo com outro nome. Fontes e scripts foram relidos contra os pins antes de fechar este parecer.

**Limites e encerramento.** Original e base foram apenas relidos e coincidem em `{V['original_sha256']}`. Nenhum monólito foi executado/importado, nenhum helper autoral foi executado, nenhum rebuild DEV ou integrado foi repetido e não houve escrita fora de revisao. O parecer DEV e os pareceres custodiados anteriores permanecem intactos. Nenhum achado necessário ficou pendente neste escopo integrado; a execução futura de recorder/verifier e a custódia resultante pertencem ao autor.

O pacote identifica o GNS do domínio escalar completo e o fecho de seu gráfico, preservando os objetos anteriores. Não conclui KMS, igualdade do fluxo candidato com o fluxo modular do peso, traço canônico, canto Three Locks, obrigações físicas, gate ampliado ou runtime integral. As seis flags maiores, full_plan_complete e full_monolithic_runtime_run permanecem false na evidência relida. Não há aprovação de QG ou de fechamento global.
'''
dest=REV/'REVIEW_SCALAR_WEIGHT_GNS_INTEGRATED.md';write(dest,report.encode('utf-8'))
closure={'timestamp':stamp,'report':str(dest),'sha256':hf(dest),'bytes':dest.stat().st_size,
 'marker':'INTEGRATED_SCALAR_WEIGHT_GNS_REVIEW','findings_P0_P1_P2':[],'scope_complete':True,
 'verification_sha256':hf(OUT/'verification.json'),'author_recorders_executed_by_reviewer':False}
write(OUT/'closure.json',json.dumps(closure,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(closure,ensure_ascii=False,indent=2))
