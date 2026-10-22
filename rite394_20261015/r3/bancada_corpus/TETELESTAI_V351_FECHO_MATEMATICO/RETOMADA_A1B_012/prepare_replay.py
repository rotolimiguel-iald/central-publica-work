from pathlib import Path
import datetime,hashlib,json,os,re,shutil
R=Path(__file__).resolve().parent;OLD=R.parent
B=OLD.parent/'TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA'
K=R/'k'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) and not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);q=p.with_name(p.name+'.tmp');q.write_bytes(b)
    assert q.read_bytes()==b and b;os.replace(q,p)
def load(p):return json.loads(p.read_text(encoding='utf8'))
receipt=load(B/'RECIBO_B6.json')
assert pin(Path(receipt['delivery']['path']))==receipt['delivery']
assert pin(Path(receipt['manifest']['path']))==receipt['manifest']
names=['V351ResolventImaginaryIntertwining','V351ScaledResolventFunctions','V351ScaledResolventCalculus','V351ImaginaryPowerScaling','V351ScalarImaginaryRightTransport','V351AntiunitaryResolventPhase','V351ScalarTomitaImaginaryConjugation']
modules=[];targets=[]
for n in names:
    p=OLD/'kernel/TGLExt'/f'{n}.lean';q=B/'kernel/TGLExt'/p.name
    assert p.read_bytes()==q.read_bytes()
    code=p.read_text(encoding='utf8');decl=[]
    for name in re.findall(r'^#print axioms (\w+)',code,re.M):
        m=re.search(r'^(theorem|def) '+name+r'\b([\s\S]*?)(?= :=| where)',code,re.M)
        assert m,name
        t=dict(name='TGLV350.Regular.'+name,kind=m[1],module=n,statement=m[0],source=pin(p),line=code[:m.start()].count('\n')+1)
        decl.append(t);targets.append(t)
    modules.append(dict(name=n,original=pin(p),v353=pin(q),declarations=decl))
assert len(targets)==40 and sum(t['kind']=='theorem' for t in targets)==36
prior_names=['REAPROVEITAMENTO_A1_ESCALA_IMAGINARIA.md','REAPROVEITAMENTO_A1_ESCALA_IMAGINARIA.json','ADENDO_REAPROVEITAMENTO_A1_ESCALA_IMAGINARIA.json','REAPROVEITAMENTO_A1_TRANSPORTE_ANTIUNITARIO.md','REAPROVEITAMENTO_A1_TRANSPORTE_ANTIUNITARIO.json','RELATORIO_A1_TRANSPORTE_ANTIUNITARIO.md','AUDITORIA_A1_TRANSPORTE_ANTIUNITARIO.json','LACUNAS_A1.md','BUSCAS_A1.json']
prior=[pin(OLD/n) for n in prior_names]
stamp=datetime.datetime.now().astimezone().isoformat()
f=dict(timestamp=stamp,status='REUSE_EXISTING_SEVEN_MODULES__NO_NEW_THEOREMS',decision='REUSAR',
    consumer=dict(path=str(OLD/'LACUNAS_A1.md'),named_bridge='regular_dual_weight_modular_implementation',final_contract='TGLV351.RegularCoreTraceData',
        exact_role='Bounded imaginary-power transport of matrix units and regular generators in the same scalar GNS; commutation with the original Tomita polar antiunitary; not the final trace'),
    exact_target='Audit 40 existing declarations (36 theorems,4 definitions), standalone Lake replay, own independent review, manifest and tunnel delivery. No added mathematical wrapper.',
    modules=modules,prior_fiches_and_searches=prior,entry_condition_b6_receipt=pin(B/'RECIBO_B6.json'),
    searches='Reuse the six modalities recorded before these unchanged sources. Nineteen V351 sources compared against the V353 snapshot; these seven are byte-identical. No claim of exhaustive fresh corpus search.',
    remaining=['extended dual-weight identification','full modular action AdLambda','positive affiliated regular generator','inverse-generator perturbation trace'],
    canonical_written=False)
put(R/'REAPROVEITAMENTO_RETORNO_A1B.json',json.dumps(f,ensure_ascii=False,indent=2).encode('utf8'))
md='[OPEN — ficha anterior à reprodução standalone; fontes matemáticas existentes, sem alteração]\n\n# Retomada A1(b) após B6\n\n'+stamp+'\n\nREUSAR sete módulos já presentes no snapshot v353, todos idênticos em bytes à bancada A1. Não criar outro teorema ou camada para repetir seus resultados. Produto: auditoria de40 declarações, reprodução Lake, revisão independente e entrega própria que faltavam.\n\nConsumidor: regular_dual_weight_modular_implementation, em LACUNAS_A1.md:25; contrato final TGLV351.RegularCoreTraceData, V351RegularCoreTraceContract.lean:43. Estas pontes tratam o grupo do MESMO resolvente/GNS e J polar, sem provar por si a implementação modular integral ou o traço.\n\n## Fornecedores e tipos exatos\n\n'
for m in modules:
    md+=f"### {m['name']}\n\n`{m['original']['path']}` · `{m['original']['sha256']}` · REUSAR, sem editar.\n\n"
    for t in m['declarations']:md+=f"Linha {t['line']}: `{t['name']}`\n```lean\n{t['statement']}\n```\n"
md+='\n## Aproveitamento, buscas e limites\n\nAs fichas anteriores e BUSCAS_A1 registram as seis modalidades: fontes embutidos por nomes/tipos; notasV350; entregas/bancadas; árvore; TOE; índice do acervo. Seus arquivos e hashes constam no JSON. A retomada acrescenta comparação em bytes contra o snapshot v353, que já contém os sete. Não se anuncia varredura nova exaustiva.\n\nOs 19V351 originais, relatórios e quatro entregas anteriores ficam intactos. O contrato forte e as provas anteriores não são refeitos. A cópia Lake nesta subpasta usa fontes da bancada antiga, caches Mathlib/pacotes pinados da bancada B e nenhum objeto de projeto autoral herdado. Falhas de compilação da manhã permanecem na casa antiga e não são confundidas com esta reprodução. A auditoria histórica antiunitária era autoral do sidecar: a nova revisão será separada.\n\nA1(b) continua OPEN: nenhuma instância de RegularCoreTraceData é prometida por esta entrega documental. O próximo consumidor matemático é o transporte à esquerda dos geradores, pela ponte polar já existente; qualquer novo código exige sua própria ficha.\n'
put(R/'REAPROVEITAMENTO_RETORNO_A1B.md',md.encode('utf8'))
put(R/'ALVOS_RETORNO_A1B.json',json.dumps(targets,ensure_ascii=False,indent=2).encode('utf8'))
records=[]
for p in sorted((OLD/'kernel').rglob('*')):
    if not p.is_file() or '.lake' in p.parts or '.bak' in p.name:continue
    if p.suffix!='.lean' and p.name not in ['lakefile.toml','lake-manifest.json','lean-toolchain']:continue
    rel=p.relative_to(OLD/'kernel');put(K/rel,p.read_bytes());records.append(dict(relative=str(rel),original=pin(p),copy=pin(K/rel)))
put(R/'FONTES_REPLAY.json',json.dumps(records,ensure_ascii=False,indent=2).encode('utf8'))
assert not (K/'.lake').exists()
assert (K/'lake-manifest.json').read_bytes()==(B/'kernel/lake-manifest.json').read_bytes()
shutil.copytree(B/'kernel/.lake/packages',K/'.lake/packages')
put(R/'CACHE_PROVENIENCIA.json',json.dumps(dict(timestamp=stamp,source=str(B/'kernel/.lake/packages'),target=str(K/'.lake/packages'),
    upstream_manifest=pin(B/'kernel/lake-manifest.json'),upstream_package_record=pin(B/'DEPENDENCIAS_LAKE_V353.json'),
    project_objects_inherited=False,external_package_cache_inherited=True,copy_method='shutil.copytree, byte copies, no hardlinks'),ensure_ascii=False,indent=2).encode('utf8'))
audit='\n'.join('import TGLExt.'+n for n in names)+'\n\nset_option pp.universes true\n\n'
audit+='\n'.join('#check '+t['name']+'\n#print axioms '+t['name'] for t in targets)+'\n'
put(K/'TGLExt/AuditA1Orphans.lean',audit.encode('utf8'))
print(json.dumps(dict(fiche_created=True,source_files=len(records),existing_targets=len(targets),new_theorems=0,cache_copied=True),ensure_ascii=False))
