"""Write the integrated review atomically; no author program executes."""
from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=REV/'homogeneous_right_integrated_20260912_155452_339076'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
v=json.loads((RUN/'verification.json').read_bytes())
assert v['all_source_binary_log_stream_pins_match'] and v['parent_Audit_no_loss']
assert all(sha(ROOT/f)==h for f,h in v['artifact_pins'].items())
assert sha(ROOT/'um.py')==v['working_sha256']
assert sha(REV/'REVIEW_HOMOGENEOUS_RIGHT_GNS.md')==v['DEV_review_sha256']
assert not any((ROOT/f).exists() for f in v['new_custody_and_memory_recording_not_created'])
def link(label,p,line=None):return '['+label+'](<'+Path(p).as_posix()+((':'+str(line)) if line else '')+'>)'
rows=[]
for r in v['new_records']:
    rows.append('| '+link(r['file'],ROOT/'kernel'/r['file'])+' | `'+r['source_sha256']+'` | `'+r['binary_sha256']+'` | '+link(r['timestamp'],ROOT/'logs'/r['log_name'])+' |')
helpers=[]
for name,r in v['helpers'].items():helpers.append('| '+link(name,ROOT/name)+' | '+str(r['lines'])+' | `'+r['sha256']+'` |')
pins=[]
for f in ['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json']:
    pins.append('| '+link(f,ROOT/f)+' | `'+v['artifact_pins'][f]+'` |')
ar=v['final_Audit_record'];now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''# Revisão independente da integração — direita homogênea no GNS

INTEGRATED_HOMOGENEOUS_RIGHT_GNS_REVIEW

{now}. **[REAL — inspeção independente de bytes, registros e scripts] Nenhum achado P0, P1 ou P2. Integração dos mesmos cinco módulos/28 alvos conferida; gravação da nova memória/custódia ainda pendente.**

Escopo: transposição DEV→TGLExt, conteúdo embutido, raízes, 157 registros fonte/binário/log, Audit atual, 86 controles registrados e os três helpers. A matemática e a recompilação própria dos cinco DEV/28 alvos são herdadas do {link('parecer DEV preservado',REV/'REVIEW_HOMOGENEOUS_RIGHT_GNS.md')} (SHA256 `{v['DEV_review_sha256']}`). Nesta rodada houve **zero compilações Lean e zero execuções de monólito, integrador, testes autorais ou recorder**. O novo `ScalarRightStarGraph.lean` e quaisquer desenvolvimentos posteriores estão excluídos; suas provas não foram examinadas.

| Evidência | Resultado conferido | Origem |
|---|---|---|
| Transposição | 5/5, somente prefixo de import; demais bytes idênticos | Comparação própria com snapshots DEV já auditados |
| Embutido | 859 arquivos; exatamente cinco novas chaves; nenhuma antiga removida | Extração literal por AST, sem importar/executar um.py |
| Raízes | TGLExt: cinco imports; Audit: cinco imports e 28 impressões novas; conteúdo anterior preservado | Diff próprio contra cópia da mãe com hash conferido |
| Build incremental | 157 registros rc0: 150 idênticos aos da mãe + cinco módulos novos + duas raízes recompiladas | Registros autorais, relidos e confrontados aos arquivos atuais |
| Audit | 6.687 declarações distintas = 6.659 anteriores + 28 exatas; nenhum nome/axioma anterior perdido | Novo stdout reparseado e comparado integralmente a `axiom_report` |
| Controles | 86/86 registrados como aprovados; 84 anteriores preservados e dois novos | Leitura do relatório autoral; testes não repetidos |
| Fronteira | Seis flags maiores falsas; mesmo gate legado e mesma frontier; runtime integral false | Relatórios atuais e comparação com mãe |
| Memória | 34 superfícies iguais à custódia DEV imediata; nova gravação ainda ausente | Hashes/prefixos relidos, sem editar memória |

**Identidade das fontes e evidência de compilação.** As cinco fontes DEV continuam nos pins do manifesto revisado; a comparação por bytes substitui exclusivamente `import TGLV350.` por `import TGLExt.V350`. O corpo das declarações, namespaces, quantificações e hipóteses permanece idêntico. Os cinco streams de compilação integrada contêm exatamente os alvos de seus módulos e os mesmos axiomas do auditor DEV próprio. Para todos os 157 registros foram relidos a fonte, o `.olean`, stdout, stderr e JSON individual; `returncode=0`, existência do binário, hashes e correspondência entre registro agregado e JSON individual conferem. Os sete registros novos também têm `lean_returncode=0` e fonte inalterada durante compilação. Não se confundem os 157 registros válidos com 157 novas recompilações.

| Fonte integrada/raiz | SHA256 fonte | SHA256 .olean | Log autoral aceito |
|---|---|---|---|
{chr(10).join(rows)}

A cópia atual tem SHA256 `{v['working_sha256']}`. A comparação da AST Python, substituindo apenas o valor de `_EMBEDDED_KERNEL_FILES` por um marcador, foi igual à cópia da mãe `{v['parent_working_sha256']}`, localizada por hash em {link(Path(v['parent_working_backup']).name,v['parent_working_backup'])}. Entre as 854 chaves antigas, somente os dois agregadores mudaram. `gate_extension.py` permaneceu byte a byte igual à mãe: `{v['artifact_pins']['gate_extension.py']}`. O original canônico e `fontes/um_v350_original.py` foram relidos somente para hash e coincidem com o pin original `{v['original_sha256']}`.

**Audit atual, sem usar os campos históricos como âncora.** O log aceito é {link(ar['log_name'],ROOT/'logs'/ar['log_name'])}, SHA256 JSON `{ar['log_sha256']}`. Seu stdout tem SHA256 **`{ar['stdout_sha256']}`**; stderr vazio, rc0, sem warnings. A reanálise completa desse stream produz exatamente o mapa de 6.687 entradas do evidence atual, somente com axiomas do trio `propext`, `Classical.choice`, `Quot.sound`. Todos os 28 alvos do auditor próprio DEV reaparecem com o mesmo conjunto de axiomas, além dos 6.659 anteriores preservados.

Os campos globais `audit_stdout_sha256` e `audit_capture_sha256_full` continuam com `{v['inherited_Audit_hash_fields']['audit_stdout_sha256']['stored_sha256']}`, igual ao estrato histórico e diferente do stdout corrente. Essa ressalva conhecida é mantida: tais campos **não certificam o stream novo**. A evidência usada aqui é a cadeia registro Audit→JSON→stdout atual→mapa reparseado. Não há nova execução independente do Audit integrado nesta rodada.

**Scripts e controles.** Os três helpers foram lidos integralmente, incluindo os textos interpolados de relatório e memória, e suas ASTs foram analisadas sem execução:

| Helper | Linhas lidas | SHA256 |
|---|---:|---|
{chr(10).join(helpers)}

`prepare_homogeneous_right_stage.py` exige o parecer DEV pinado e as duas mães, verifica o estado anterior e prevê backup imediato de bytes/temporário antes de alterar os scripts. Os diffs contra backups cujos hashes coincidem com a mãe confirmam somente: cinco entradas no lote do integrador e contagem 302→330; cinco fontes antes das raízes no compilador; dois grupos adicionais no teste. Não houve enfraquecimento das condições anteriores.

Os dois controles acrescentados são:

- `homogeneous_right_full_scalar_weight_domain_does_not_discharge_KMS_trace_or_physical_frontier`;
- `homogeneous_right_same_GNS_adjoint_pairing_does_not_discharge_KMS_trace_or_physical_frontier`.

Eles verificam presença dos respectivos lemas, as seis flags falsas e a ausência de promoção do gate/plano. São controles de fronteira, não demonstrações de KMS. A tabela de gate continua consumindo somente as três pontes anteriores de tipos exatos em Lean; a existência dos 28 nomes novos não amplia esse consumo.

**As duas mães e o estado pré-gravação.** Mãe matemática: {link('scalar_weight_gns_custody.json',ROOT/'scalar_weight_gns_custody.json')}, SHA256 `{v['mathematical_parent_sha256']}`. Mãe imediata de memória: {link('homogeneous_right_dev_custody.json',ROOT/'homogeneous_right_dev_custody.json')}, SHA256 `{v['immediate_memory_parent_sha256']}`. O vínculo desta última à mãe matemática confere, assim como o pin do parecer DEV. As 34 superfícies atuais coincidem com a custódia DEV e preservam os prefixos dos 34 backups já gravados naquela etapa; seus hashes diferem dos anteriores à gravação DEV. Não se exigiu incorretamente que permanecessem iguais à mãe matemática.

O recorder novo usa `memory['surface_sha256']` como estado imediato, verifica esse estado antes da escrita e prevê **novos** backups de bytes ao lado de cada arquivo, append de prefixo preservado e temporário→replace verificado por arquivo. A atomicidade é por arquivo, não uma transação indivisível das 34 superfícies. A custódia projetada guarda separadamente `previous_custody_*` (memória DEV) e `previous_integrated_custody_*` (mãe matemática). O verifier também confere esses dois vínculos, relê todos os pares fonte/binário dos registros compilados, confere artefatos/reviews e exige crescimento com prefixo idêntico ao backup. Não foi retirado o reexame dos `.olean`.

Os 17 caminhos da lista de artefatos que o recorder pretende pinarem existem. Na inspeção final **não existem ainda** `homogeneous_right_custody.json`, `homogeneous_right_custody_verification.json` ou `RELATORIO_DIREITA_MODULAR_GNS_INTEGRADA.md`; as 34 memórias continuam no estado DEV. A presente revisão avalia a lógica e os bytes desses helpers; **não declara o recorder/verifier executado nem a nova custódia, seus backups ou suas atualizações de memória concluídos**. O texto que eles gerarão está adequadamente rotulado e mantém a diferença entre adjunto local e KMS global.

**Alcance herdado.** Ficam transportados os operadores direitos para os dados homogêneos e suas instâncias matriciais, no mesmo H_I, com preservação de n_ν e pareamento para quaisquer A,B∈n_ν. Não se assume I=n_ν nem D(S) igual à imagem algébrica. Não se construiu nesta integração uma representação direita de toda N, a extensão por somas a toda matriz local, a identificação do fluxo com (S†S)^it, KMS global, traço, escala/canto Three Locks, hipóteses físicas ou consumo/runtime completo. Essas fronteiras permanecem abertas, sem constituir bugs deste pacote. As dependências e a matemática DEV previamente revisadas foram reutilizadas; não se refez a biblioteca nem a auditoria matemática anterior.

Pins principais e evidência própria:

| Artefato | SHA256 |
|---|---|
{chr(10).join(pins)}
| {link('Reconciliação própria dos 157 registros',RUN/'verification.json')} | `{sha(RUN/'verification.json')}` |
| {link('Mapa Audit reparseado',RUN/'axioms.json')} | `{sha(RUN/'axioms.json')}` |

Os snapshots das fontes, logs e helpers, os diffs e os pins completos estão em {link(RUN.name,RUN)}. Todas as escritas próprias ficaram em `revisao/`; o parecer DEV e as custódias anteriores permanecem intactos. **Revisão integrada delimitada encerrada sem P0–P2; registro posterior de memória/custódia permanece pendente.**
'''
text=text.replace('que o recorder pretende pinarem existem','que o recorder pretende pinar existem')
p=REV/'REVIEW_HOMOGENEOUS_RIGHT_GNS_INTEGRATED.md';raw=text.encode('utf-8')
if p.exists():
    old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with bk.open('xb') as f:f.write(old)
    assert bk.read_bytes()==old
tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(p);assert p.read_bytes()==raw
print(json.dumps({'report':str(p),'sha256':sha(p),'bytes':len(raw),'lines':len(text.splitlines())},ensure_ascii=False))
