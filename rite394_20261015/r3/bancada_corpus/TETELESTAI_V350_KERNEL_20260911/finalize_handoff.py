"""Finalize the requested handoff, with byte backups and append-only memory links."""
from pathlib import Path
from datetime import datetime
import argparse
import hashlib
import json
import math
import re

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'HANDOFF_SESSAO_UM_20260913'
now=datetime.now().astimezone()
stamp=now.strftime('%Y%m%d_%H%M%S_%f')
marker='TETELESTAI_V350_HANDOFF_FINAL_E_MULTISSONDA_20260913'
ap=argparse.ArgumentParser()
ap.add_argument('--canonical-hash',required=True)
args=ap.parse_args()

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()

backups=[]
def save(path,payload):
    if isinstance(payload,str): payload=payload.encode('utf-8')
    assert payload
    if path.exists():
        previous=path.read_bytes()
        backup=path.with_name(path.name+'.bak_'+stamp)
        with backup.open('xb') as stream: stream.write(previous)
        assert backup.read_bytes()==previous
        backups.append(dict(path=str(backup),target=str(path),sha256=sha(backup)))
    temporary=path.with_name(path.name+'.tmp_'+stamp)
    with temporary.open('xb') as stream: stream.write(payload)
    assert temporary.stat().st_size==len(payload)
    temporary.replace(path)
    assert path.read_bytes()==payload

assert not (OUT/'MANIFESTO_HANDOFF.json').exists(), 'Do not rewrite delivered custody'
inv=json.loads((OUT/'INVENTARIO_PORTABILIDADE.json').read_bytes())
assert args.canonical_hash.lower()==inv['baseline']['sha256']
assert sha(ROOT/'r/um.py')==inv['final']['sha256']==sha(ROOT/'um.py')
old_custody=ROOT/'runtime_final_custody.json'
old_custody_sha=sha(old_custody)
custody=json.loads(old_custody.read_bytes())
c=json.loads((ROOT/'r/um_absoluto.json').read_bytes())['core']

experimental={
 'timestamp':now.isoformat(),
 'source_path':str(ROOT/'r/um_absoluto.json'),
 'source_sha256':sha(ROOT/'r/um_absoluto.json'),
 'joint_sigma':None,
 'joint_status':'NAO_DETERMINADO__NAO_SOMAR_DIAGNOSTICOS_CORRELACIONADOS_E_RECUSADOS',
 'new_joint_likelihood_run':False,
 'results':{
   'gw_angular_surrogates':c['gw_angular_rite']['surrogates'],
   'old_may_echo':c['gw_angular_rite']['echo_preregistered_may_2026'],
   'coupled_may':c['gw_echo_rite']['stack'],
   'coupled_kms':c['gw_echo_kms_rite']['stack'],
   'anchored_v2':c['echo_anchored_result_v2']['laws'],
   'bayesian_pe_v2':c['echo_pe_result_v2']['outcomes'],
   'ringdown_v2':c['ringdown_dephasing_result_v2']['stacks'],
   'd1_camb_v2':{k:c['d1_camb_result_v2'][k] for k in ['chi2','delta_chi2','beta_posterior','bestfit_outcome','mcmc_outcome']}
 },
 'gaussian_planning_arithmetic':{
   'beta_runtime':c['ringdown_dephasing_result_v2']['beta_runtime'],
   'relative_percent_of_0002':100*.002/c['ringdown_dephasing_result_v2']['beta_runtime'],
   'sigma_for_median_5':c['ringdown_dephasing_result_v2']['beta_runtime']/5,
   'z_if_center_beta_sigma_0002':c['ringdown_dephasing_result_v2']['beta_runtime']/.002,
   'sigma_for_1p7_percent':.017*c['ringdown_dephasing_result_v2']['beta_runtime'],
   'toy_independent_three_z3':9/math.sqrt(3),
   'toy_correlated_three_z3_rho_half':9/math.sqrt(6)
 },
 'toy_is_not_tgl_measurement':True,
 'sources_consulted':[
   'https://cmb-s4.org/',
   'https://www.darkenergysurvey.org/des-year-3-cosmology-results-papers/',
   'https://pdg.lbl.gov/2025/reviews/rpp2025-rev-statistics.pdf',
   'https://arxiv.org/abs/1007.1727']
}
save(OUT/'EVIDENCIA_MULTISSONDA.json',json.dumps(experimental,ensure_ascii=False,indent=2)+'\n')

p=OUT/'HANDOFF_UM_FINAL.md'
s=p.read_text(encoding='utf-8').replace('IN\u200bVENTARIO','INVENTARIO')
s=s.replace('Todos os relatórios desta pasta estão inventariados por caminho/hash no campo `reports`.',
 'Os relatórios Markdown da raiz ROOT (a pasta de trabalho que contém este diretório de handoff) estão inventariados por caminho/hash no campo `reports`, no instante de sua leitura. Os arquivos do próprio handoff estão no `MANIFESTO_HANDOFF.json`. Adendos posteriores às memórias têm nova custódia; não invalidam o retrato histórico desses hashes.')
s=s.replace('## 10. Frase pronta para iniciar a outra sessão',
 'O operador também propôs a composição multissonda: ler [ADENDO_MULTISSONDA.md](<'+(OUT/'ADENDO_MULTISSONDA.md').as_posix()+'>). Ele registra as pontuações observadas de ecos/GW, o sigma conjunto ainda não determinado, e corrige fixação de β, covariâncias, sistemáticas e interpretação de Δχ². Essa análise não deve ser confundida com uma execução nova da combinação.\n\n## 10. Frase pronta para iniciar a outra sessão')
s=s.replace('Preenchidos abaixo por script a partir dos bytes, junto com o manifesto de arquivos do handoff.',
 'Lidos dos bytes durante a finalização. O original canônico foi somente conferido por hash, com acesso de leitura autorizado. Nenhum programa foi alterado por esta entrega.\n\n'+
 '| Artefato | SHA-256 |\n|---|---|\n'+
 ''.join(f'| `{name}` | `{sha(ROOT/name)}` |\n' for name in ['fontes/um_v350_original.py','r/um.py','r/um_absoluto.json','r/um_absoluto_selo.json','r/tgl_kernel_proof_manifest.json','runtime_final_custody.json'])+
 '\nO manifesto deste handoff lista todos os entregáveis, os 34 adendos de memória e seus backups. O selo formal permanece o da rodada03; esta entrega acrescenta documentação, inventário e planejamento experimental.\n')
save(p,s)

review_text='''# Revisão documental do handoff

Revisor independente reutilizado da revisão da integração. Revisão somente de leitura; não executou o monólito, compilador ou experimento.

Primeira leitura: sem P0/P1 e sem promessa indevida de 5σ. Confirmou as contagens 218+2 fontes, 5+12 funções, 13 sentinelas em oito funções, os 220 pins formais e as projeções 790,36× e 1.247,44×. Literatura externa não foi revalidada pelo revisor.

Dois P2 documentais encontrados: manifesto/pins ainda não finalizados no draft e caractere U+200B no nome do inventário. Correções: o alcance de reports passou a ser explicitamente a raiz ROOT; os próprios arquivos estão no manifesto final; pins foram preenchidos por script; U+200B foi removido. O manifesto é gerado depois dos adendos e a conferência de links é automática. Nenhum resultado de programa foi alterado para atender à revisão.

O adendo multissonda, solicitado pelo usuário após a primeira revisão, tem sua revisão registrada separadamente quando recebida. Nenhuma leitura futura é presumida neste parecer.
'''
save(OUT/'REVISAO_E_CORRECOES.md',review_text)

common=f'''\n\n## {marker} — {now.isoformat()}

[INPUT] Handoff solicitado para incorporar a cadeia final à sessão do um.py; depois, avaliação de composição preditiva multissonda e sigma conjunto.
[REAL — documentação e comparação AST, sem execução nova] Handoff em `{OUT/'HANDOFF_UM_FINAL.md'}`. Diferença completa v350→cópia validada: 218 fontes Lean adicionais, duas raízes modificadas, cinco funções Python novas e doze modificadas; somente o último reparo se restringiu a dois leitores. Gate principal 11/11 já satisfeito; montagem modular 7/8→8/8 no alcance PRODUCT_TOWER. Programa validado SHA256 {sha(ROOT/'r/um.py')}; canônico apenas lido, igual à base preservada.
[REAL — leitura dos resultados existentes] O sigma conjunto de ecos/GW/cosmologia NÃO foi calculado nem definido nesta entrega. Há resultados correlacionados e recusados por sistemáticas; o 4,396σ do eco ancorado KMS é poder estimado, não detecção (Z observado 0,219). D1 CAMB V2 registra Δχ²=TGL−LCDM≈+9,70, desfavorável nesse procedimento. Preservar sinal e estatutos.
[DERIVED — planejamento] PLANO_EXPERIMENTAL_5SIGMA.md e ADENDO_MULTISSONDA.md registram meta de sensibilidade, hipótese de escala, β fixo vs diagnóstico livre, covariâncias e calibração do teste global. 0,002 equivale a 16,6% de β. Nenhuma descoberta de 5σ foi prometida, nenhum novo rito foi congelado/executado, nenhum requisito foi acrescentado ao gate. CMB-S4: consulta ao comunicado oficial informa encerramento do projeto após retirada de apoio em julho/2025; não usar como dado disponível ou instrumento futuro garantido.
[CUSTÓDIA] Backups de bytes imediatos antes deste adendo; raiz canônica física não editada. Manifesto desta documentação em `{OUT/'MANIFESTO_HANDOFF.json'}`; custódia histórica da execução permanece em runtime_final_custody.json. Próxima tarefa: incorporar o candidato na casa responsável, sem repetir provas nem importar DEV suspenso.
'''
memories={}
for name in custody['surface_sha256']:
    target=Path(name)
    assert target.is_relative_to(ROOT) or target in [Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'),Path(r'C:\IALD\Central de Patentes\memory\TGL_INDICE_VIVO.md')]
    prior=target.read_bytes()
    assert marker.encode() not in prior
    before=sha(target)
    addition=common
    if target.name=='REGISTRO_DAS_CONVERSAS.md':
        addition+='\n[REGISTRO — pedido do operador] “escreva um handoff para a sessão que cuida do um.py sobre tudo que fizemos aqui e tudo que precisa ser implementado no um.py na construção final de toda a cadeia. e ao final me responda, como eu posso incorporar os resultados experimentais em confirmação física, ou qual teste eu realmente posso fazer que demonstrará um resultado maior que 5sigma direto”. Mensagem posterior propôs combinação Planck/BAO/RSD/shear/SNe com β fixo e simultaneamente prior livre; respostas e números estão no adendo multissonda, sem presumir aprovação/execução de uma campanha nova.\n'
    newline='\r\n' if b'\r\n' in prior else '\n'
    appended=addition.replace('\r\n','\n').replace('\n',newline).encode('utf-8')
    save(target,prior+appended)
    assert target.read_bytes().startswith(prior) and target.stat().st_size>len(prior)
    memories[str(target)]=dict(before=before,after=sha(target),added_bytes=len(appended))
assert len(memories)==34

links=[]
for path in OUT.glob('*.md'):
    text=path.read_text(encoding='utf-8')
    assert '\u200b' not in text
    for link in re.findall(r'\]\(<(C:/[^>]+)>\)',text):
        resolved=Path(re.sub(r':\d+$','',link)); assert resolved.exists(),resolved
        links.append(dict(document=path.name,target=str(resolved)))
assert sha(old_custody)==old_custody_sha
assert sha(ROOT/'r/um.py')==inv['final']['sha256']
files={p.name:dict(bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(OUT.iterdir()) if p.is_file() and '.bak_' not in p.name}
manifest=dict(timestamp=now.isoformat(),status='HANDOFF_WRITTEN__NO_NEW_PROGRAM_OR_EXPERIMENT_RUN',
    directory=str(OUT),files=files,memory_updates=memories,backups=backups,
    previous_runtime_custody=dict(path=str(old_custody),sha256=old_custody_sha),
    canonical_hash_readonly=args.canonical_hash.lower(),validated_program_sha256=sha(ROOT/'r/um.py'),
    local_links_checked=len(links),source_original_not_modified=True,
    joint_sigma=None,new_joint_likelihood_run=False,
    inventory_report_hashes_are_snapshot_before_memory_append=True,
    scientific_limits='No universal physical confirmation or predicted positive 5-sigma result. Existing program contract and historical run seal unchanged.')
save(OUT/'MANIFESTO_HANDOFF.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(handoff=str(OUT/'HANDOFF_UM_FINAL.md'),manifest=str(OUT/'MANIFESTO_HANDOFF.json'),
  manifest_sha256=sha(OUT/'MANIFESTO_HANDOFF.json'),files=len(files),memories=len(memories),backups=len(backups),links=len(links)),ensure_ascii=False,indent=2))
