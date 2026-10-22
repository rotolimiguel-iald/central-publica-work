"""Finish the static-only preflight report without reading live build/test outputs."""
from pathlib import Path
import ast,datetime,hashlib,json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
OUT=REV/'scalar_weight_gns_preflight_20260912_145351_129259'
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
P=load(OUT/'preflight.json');I=load(OUT/'integration.json')
def write(p,b):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f:f.write(b)
    assert q.read_bytes()==b;q.replace(p)
def link(label,p,line=None):
    return '['+label+'](<'+Path(p).as_posix()+((':'+str(line)) if line else '')+'>)'
def code(f,line):return link(f+':'+str(line),ROOT/f,line)
# Include Lean apostrophes and the two initial parallel compile entries.
t=ast.parse((OUT/'compile_integrated.py').read_bytes())
initial=next(ast.literal_eval(n.args[1]) for n in ast.walk(t) if isinstance(n,ast.Call)
    and isinstance(n.func,ast.Attribute) and n.func.attr=='map' and n.args
    and isinstance(n.args[0],ast.Name) and n.args[0].id=='compile_one')
sequential=P['compile_schedule'];schedule=initial+sequential
assert len(schedule)==len(set(schedule))==len(I['added_kernel_files'])+len(I['updated_kernel_files'])==152
assert set(schedule)==set(I['added_kernel_files']+I['updated_kernel_files'])
old=(OUT/'parent_sources/TGL/Audit.lean').read_text(encoding='utf-8')
new=(OUT/'sources/TGL/Audit.lean').read_text(encoding='utf-8')
oldnames=re.findall(r"^#print axioms ([\w.']+)",old,re.M)
newnames=re.findall(r"^#print axioms ([\w.']+)",new,re.M)
assert len(set(oldnames))==6599 and len(set(newnames))==6659
assert all(newnames.count(n)==oldnames.count(n) for n in oldnames)
targets={n for row in P['transposition'].values() for n in row['targets']}
assert set(newnames)-set(oldnames)==targets and len(targets)==60
R={**P,'timestamp_final':datetime.datetime.now().astimezone().isoformat(),
 'initial_capture_sha256':hf(OUT/'preflight.json'),'old_Audit_distinct_names':len(set(oldnames)),
 'new_Audit_distinct_names_in_source':len(set(newnames)),'projected_records_from_schedule':len(schedule),
 'compile_schedule':schedule,'sequential_entries':len(sequential),'initial_parallel_entries':initial,
 'counting_notes':['Complete Lean-name parser includes the inherited apostrophe in TGLExt.comm_of_fixed\'.',
                  'Total schedule includes two initial pool.map entries plus the 150 sequential entries.'],
 'helper_static_inspection_completed':True,'findings':[]}
assert all(hf(ROOT/f)==h for f,h in P['artifact_pins'].items())
assert hf(ROOT/'um.py')==P['working_sha256']
assert hf(P['prior_DEV_review']['report'])==P['prior_DEV_review']['sha256']
R['helper_semantics']={
 'prepare_immediate_byte_backup_atomic_replace':True,
 'recorder_requires_final_integrated_review_not_preflight':True,
 'recorder_exact_parent_surface_pins_then_byte_append':True,
 'verifier_rereads_source_and_binary_rc0_output_exists':True,
 'verifier_checks_custody_record_count_and_byte_prefixes':True,
 'future_full_runtime_or_gate_promotion_claimed':False,
 'atomicity_scope':'per file; not a transaction across 34 surfaces',
 'all_new_helpers_executed_by_reviewer':False}
raw=json.dumps(R,ensure_ascii=False,indent=2).encode('utf-8');write(OUT/'static_verification.json',raw)
rows=[]
for name,row in P['transposition'].items():
    rows.append(f"| {link(name,ROOT/'kernel/TGLExt'/('V350'+name+'.lean'))} | {len(row['targets'])} | `{row['integrated_sha256']}` |")
pinfiles=['integration.json','prepare_scalar_weight_gns_stage.py','record_scalar_weight_gns_progress.py',
 'verify_scalar_weight_gns_custody.py','integrate_v350.py','compile_integrated.py','test_gate_extension.py']
pins='\n'.join(f"| {link(f,ROOT/f)} | `{P['artifact_pins'][f]}` |" for f in pinfiles)
report=f'''SCALAR_WEIGHT_GNS_INTEGRATION_PREFLIGHT

{R['timestamp_final']} — [REAL — inspeção estática independente]. Parecer **PRELIMINAR**, limitado à transposição e aos helpers; nenhuma nova execução Lean, de testes autorais, recorder ou monólito.

**Nenhum achado P0, P1 ou P2 identificado neste escopo estático.** A fonte integrada preserva o pacote DEV revisto de nove módulos/60 alvos. A aceitação dos binários integrados, raízes e controles finais fica pendente da evidência autoral concluída. Este documento encerra a consulta preliminar e não satisfaz a pré-condição do recorder de revisão integrada final.

**Snapshot conferido.** A cópia um.py tem SHA256 `{P['working_sha256']}`, igual a integration.json, e 854 arquivos embutidos. Mãe: tomita_involution_custody.json, SHA256 `{P['parent_custody_sha256']}`, cópia `{P['parent_working_sha256']}`. Original e cópia-base readonly foram relidos: `{P['original_sha256']}`. Os nove DEV seguem os pins e o parecer {link('REVIEW_SCALAR_WEIGHT_GNS.md',P['prior_DEV_review']['report'])}, SHA256 `{P['prior_DEV_review']['sha256']}`, preservado intacto. Os rc0 e axiomas próprios daquele DEV são evidência anterior, não novas recompilações nesta rodada.

**Transposição e raízes.** A comparação de bytes confirmou, para cada módulo, exatamente `import TGLV350.` → `import TGLExt.V350`; todo o restante da fonte é idêntico. Os nomes completos continuam em TGLV350.Regular, inclusive HasFiniteScalarSquare.zero/left_mul/add/smul. As nove fontes TGLExt são idênticas às respectivas strings UTF-8 do dicionário embutido. Entraram somente nove chaves novas; das 845 antigas, 843 ficaram idênticas e somente TGLExt.lean/TGL/Audit.lean mudaram. Ambas as raízes importam cada novo módulo exatamente uma vez; o Audit acrescenta os 60 nomes exatos do manifesto e do auditor DEV, preservando todas as entradas anteriores e suas multiplicidades. Há 6659 nomes distintos escritos no Audit atual contra 6599 no anterior; isto é contagem **da fonte**, não leitura de um novo stdout compilado. Nenhuma hipótese ou corpo de prova mudou na transposição.

| Módulo integrado | Alvos | SHA256 da fonte integrada = embutida |
|---|---:|---|
{chr(10).join(rows)}

**Corpo Python e diferenças dos scripts.** O AST completo de um.py, substituindo somente o valor da única atribuição _EMBEDDED_KERNEL_FILES, é igual ao backup materno `{Path(P['old_monolith_backup']).name}`, cujo hash coincide com a custódia. Gate_extension.py conserva o pin materno `{P['artifact_pins']['gate_extension.py']}`. Não há promoção por mudança de Python neste incremento.

- {code('integrate_v350.py',65)} e linha 762: só foram acrescentados nove nomes ao tomita_batch e a contagem desse lote passou de 242 para 302 alvos. Revertidas essas duas alterações no AST em memória, o script coincide com o materno. As rotinas de reescrita e amarração legadas permanecem herdadas; o resultado concreto foi comparado por bytes e AST.
- {code('compile_integrated.py',173)}: só nove entradas novas, na ordem DEV, antes de TGLExt.lean e TGL/Audit.lean. Removidas essas entradas do AST em memória, o script é igual ao materno. A programação completa tem 152 registros previstos: duas entradas iniciais paralelas e 150 sequenciais; cobre exatamente added_kernel_files+updated_kernel_files. A política herdada de reúso exige hash da fonte/binário e frescor das dependências presentes. Isso não prova que o build em curso já terminou ou reutilizou/recompilou qualquer quantidade específica.
- {code('test_gate_extension.py',426)}: só duas entradas novas no laço de controles; cada uma exige nomes deste DEV, seis flags maiores false, legacy_gate_changed=false e full_plan_complete=false. Removidas as duas entradas, o AST é idêntico ao materno. Os nomes resultantes são `full_scalar_weight_GNS_completion_identification_does_not_discharge_KMS_trace_or_physical_frontier` e `full_scalar_weight_closed_Tomita_graph_identification_does_not_discharge_KMS_trace_or_physical_frontier`. O parser de axiomas e os controles anteriores permanecem iguais. São controles preparados, **não controles executados pelo revisor**.

Os backups imediatos dos três scripts, todos com sufixo `.bak_20260912_144900_431482`, foram confrontados aos três hashes da custódia mãe, não escolhidos apenas por data/nome. Diffs completos estão no {link('snapshot estático',OUT)}.

**Helpers lidos integralmente, sem execução.** {code('prepare_scalar_weight_gns_stage.py',12)} exige `--review-read`, marcador DEV, mãe e pins das nove fontes/binários; usa backup dos bytes atuais, temporário verificado e substituição, preservando a fonte anterior antes de cada alteração dos três scripts. As alterações efetivamente encontradas são exatamente as previstas pelo preparador.

{code('record_scalar_weight_gns_progress.py',49)} exige `--review-read` e os dois pareceres, inclusive `REVIEW_SCALAR_WEIGHT_GNS_INTEGRATED.md` com seu marcador final. Esse parecer ainda não existe no snapshot; este preflight tem outro nome e marcador. Antes de registrar, o helper confronta original/cópia/testes, mãe, AST, rc0 e hashes de todos os pares fonte/.olean, transposição, 60 nomes/axiomas e seis flags falsas. As 34 superfícies vêm exatamente da mãe, estão todas presentes com seus hashes maternos atuais e passam pelo limite de destinos permitido no helper. Nenhuma é parecer em revisao. O laço captura bytes imediatos, exige igualdade do estado antes de cada escrita, cria backup no mesmo diretório, verifica bytes, acrescenta o adendo preservando o prefixo, usa temporário e replace; os fins de linha anteriores não são reencodados. A atomicidade é **por arquivo**, não uma transação indivisível entre as 34 superfícies.

{code('verify_scalar_weight_gns_custody.py',29)} relê todos os pares fonte/binário a partir dos registros, exige rc0/output_exists, confere hashes e confronta a contagem com a nova custódia. A checagem antes encapsulada em verify_compile_record está aqui no próprio laço: não foi eliminada. Ausência de binário faz a leitura falhar. As linhas 37–41 verificam hash do backup, prefixo byte a byte e crescimento; também são confrontados parent, artefatos, pareceres, fontes DEV/integradas e flags. Não foi repetido teste de corrupção de binário nem executado este verificador. Estes são comportamentos inspecionados no código; execução e novos backups permanecem futuros.

**Minuta incorporada ao recorder.** Li o relatório interpolado e o adendo de memória completos, nas linhas 102–177. Dizem corretamente igualdade do completamento e dos fechos de gráficos no mesmo H_I/S, sem I=n_ν e sem D(S) igual à imagem algébrica não fechada. Contagens são interpoladas dos registros finais, e os textos deixam fluxo modular/KMS, traço/canto Three Locks, obrigações físicas e consumo integral abertos. A referência adicional a tower_kms/tState_kms foi conferida somente quanto aos tipos em {code('kernel/TGLExt/TowerModular.lean',113)} e {code('kernel/TGLExt/RightMult.lean',122)}: são identidades matriciais por andar; a minuta não as promove a KMS do peso no core. Não foi reaberta a revisão matemática nem a pesquisa do acervo.

**Pins estáticos relidos.**

| Artefato | SHA256 |
|---|---|
{pins}

Evidência própria: {link('static_verification.json',OUT/'static_verification.json')} (SHA256 `{hf(OUT/'static_verification.json')}`), com fontes transpostas, pins maternos, diferenças e superfícies. A captura inicial foi preservada; a conciliação final inclui o apóstrofo herdado em TGLExt.comm_of_fixed' na contagem de nomes e as duas entradas paralelas iniciais na programação total. Isso não altera os 60 novos alvos nem indica defeito autoral.

**Ainda depende do pedido final.** [PENDENTE — não tratado como falha transitória] Conferir o término das nove compilações integradas e das duas raízes, os 152 registros efetivos com fonte/.olean/log/stdout/rc0, os 60 axiomas novos no stdout final e preservação do Audit anterior, os novos resultados dos controles e a mesma cópia/hash. A expectativa estrutural é 84 controles e 6659 nomes Audit após a execução, mas este parecer não declara esses resultados. A ligação do Audit deve usar o registro real da raiz e seu stdout final, sem presumir atualidade de campos históricos globais. Execução do recorder/verifier e seus 34 backups/prefixos também não ocorreu nesta revisão.

Não foram consumidos integrated_compile.json, gate_tests.json ou kernel_incremental_evidence.json em trânsito como evidência final. As seis flags falsas foram conferidas como exigência estática dos helpers/controles e herança materna; seu estado no novo resultado executado será relido depois. Nenhuma escrita fora de revisao, nenhum monólito/helper autoral executado, nenhum novo rebuild, nenhuma alteração nos DEV, pareceres anteriores ou memórias. **Escopo preliminar encerrado; aprovação integrada final ainda pendente.**
'''
dest=REV/'REVIEW_SCALAR_WEIGHT_GNS_INTEGRATION_PREFLIGHT.md'
write(dest,report.encode('utf-8'))
closure={'timestamp':R['timestamp_final'],'report':str(dest),'sha256':hf(dest),'bytes':dest.stat().st_size,
 'static_findings_P0_P1_P2':[],'static_scope_complete':True,'final_integration_approval':False,
 'static_verification_sha256':hf(OUT/'static_verification.json')}
write(OUT/'closure.json',json.dumps(closure,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(closure,ensure_ascii=False,indent=2))
