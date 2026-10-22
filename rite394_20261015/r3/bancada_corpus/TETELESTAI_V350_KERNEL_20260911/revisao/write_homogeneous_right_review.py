"""Create the scoped DEV verdict atomically from measured evidence."""
from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'homogeneous_right_latest_run.txt').read_text().strip())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
m=load(RUN/'manifest.json');c=load(RUN/'compilation.json');v=load(RUN/'verification.json');d=load(RUN/'homogeneous_right_draft_status.json')
assert v['all_six_rc0'] and v['all_28_exact_trio'] and v['five_binaries_equal_author']
assert sha(ROOT/'record_homogeneous_right_memory.py')==v['recorder_final_sha256']
assert sha(ROOT/'homogeneous_right_draft_status.json')==m['draft_status_sha256']
def link(label,p,line=None):return '['+label+'](<'+Path(p).as_posix()+((':'+str(line)) if line else '')+'>)'
def src(name,line):return link(name+'.lean:'+str(line),ROOT/'kernel/TGLV350'/(name+'.lean'),line)
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
rows=[]
for name,pin in d['modules'].items():
    row=next(x for x in c['records'] if x['module']=='TGLV350/'+name+'.lean')
    rows.append('| '+link(name,ROOT/'kernel/TGLV350'/(name+'.lean'))+' | '+str(pin['targets'])+' | `'+pin['source_sha256']+'` | `'+row['output_sha256']+'` | 0 / idêntico |')
logs=[]
for name,pin in d['modules'].items():
    logs.append('| '+name+' | '+link(Path(pin['final_log']).name,pin['final_log'])+' | `'+pin['final_log_sha256']+'` |')
hist=load(RUN/'author_history.json')
failed=[x for x in hist if x['returncode']!=0]
aud=c['records'][-1]
text=f'''# Revisão independente DEV — direita homogênea no mesmo GNS

HOMOGENEOUS_RIGHT_GNS_DEV_REVIEW

{now}. **[REAL — revisão de fontes e recompilação própria] Nenhum achado P0, P1 ou P2 no escopo examinado. DEV_REVIEWED__INTEGRATION_PENDING.** Os cinco módulos, os 28 enunciados/tipos e seus axiomas, o manifesto, o relatório autoral e o recorder final foram conferidos. Não resta análise DEV necessária neste pacote. Não constitui revisão integrada, KMS global ou promoção de gate.

O resultado delimitado é a multiplicação à direita por dados homogêneos explicitamente fornecidos, com instâncias concretas para cada unidade matricial local e sua torção, preservando o domínio escalar completo n_ν e o mesmo H_I. O adjunto é o adjunto de operador linear contínuo de Mathlib nesse H_I, com pareamento válido para quaisquer A,B∈n_ν.

**Evidência própria e proveniência.** A árvore {link(RUN.name,RUN)} contém cópias de bytes das cinco fontes, 393 dependências de projeto com fonte/binário pinados, histórico autoral, auditor e logs próprios. Foram recompilados os cinco módulos e, ao final, somente o auditor corrigido: **6 resultados aceitos rc0**, todos os 28 alvos exatamente no trio `propext`, `Classical.choice`, `Quot.sound`. Todos os cinco `.olean` próprios são byte a byte idênticos aos finais autorais. O auditor usa `#check` com `pp.universes true` de modo local e `#print axioms` para cada alvo; seu {link('stdout completo',aud['stdout'])} foi lido integralmente.

| Fonte | Alvos | SHA256 fonte | SHA256 .olean próprio = autor | rc próprio / comparação |
|---|---:|---|---|---|
{chr(10).join(rows)}

As dependências vieram da árvore própria anterior {link(Path(m['previous_run']).name,m['previous_run'])}; os hashes foram relidos antes da cópia e após a compilação, e o fecho de imports foi verificado sem ciclos. O `LEAN_PATH` efetivo contém somente o novo `build` de revisão e os oito diretórios de pacotes externos. Nenhum build autoral de projeto entrou nele. Não se recompilaram as 393 dependências nem Lean/Mathlib: a base compilada e sua proveniência histórica são herdadas, conforme o manifesto anterior. Compilador `{m['lean_version']}`, SHA256 `{m['compiler_sha256']}`; 16 pins de metadados de pacotes também foram preservados. Isso não equivale a reconstrução independente de toda a biblioteca.

Uma dependência herdada, `DualSemifiniteIdeal`, conserva o comentário anterior já revisado: fonte congelada `6af7365befd3125fa1b8a9a03f26bcd96d723659d035d2b52e73a8ced09b70b3`, fonte viva corrigida `f1c93aa724c9eb82df3d1ec74d040cdab6a78f0b57f51b224f60656669128da3`. Foi reconferida a substituição literal exclusiva do comentário, sem diferença de provas; essa herança está explícita no manifesto.

**Composição matemática conferida.**

1. {src('LocalRightModularTransport',13)}: igualdade sobre Ω determina operadores de M′ pela densidade da órbita da base. A covariância de `rTowerPi` usa o mesmo fluxo da torre, que fixa Ω, e a instância matricial recebe a frequência `log(localEigenvalue)`. Não se assume uma propriedade modular do novo peso/GNS.
2. {src('HomogeneousCommutantTransport',35)}: com M_s(x)=exp(−isx), o campo torcido de D homogêneo é M_−c·fibre(D)∈N′. A comutação fornece θ_c(A)fibre(D)=fibre(D)A; aplicar θ_(s−c) fornece exatamente o deslocamento **s−c**. Nenhuma inversa de D é usada.
3. {src('ScalarHomogeneousRightOrbit',14)}: finitude escalar é equivalente a `MemLp` da órbita para Lebesgue e expoente 2. A implicação herdada usa positividade estrita do mesmo fator Haar (2π)^−1, continuidade da órbita e integral quadrática; a volta usa a finitude do fator. `toReal_ofNat` simplifica o expoente 2, não converte uma avaliação infinita em finita. Translação de Lebesgue e CLM limitado preservam `MemLp`; nenhuma fechabilidade, KMS ou igualdade I=n_ν é premissa.
4. {src('HomogeneousRightData',14)} e {src('ScalarHomogeneousRightGNS',13)}: `left_mem` exige Y∈M e é consumido em `amplified_factor_mem`/`mul_mem`, antes de empacotar A·fibre(Y) no próprio `scalarWeightLeftIdeal`. A ressalva da consulta anterior sobre a finitude meramente ambiente está satisfeita na composição. Os outros campos — D∈M′, homogeneidade real e YΩ=DΩ — são explícitos e demonstrados nas duas instâncias concretas; não há campo KMS.
5. {src('ScalarHomogeneousRightGNS',20)}: o operador ambiente é `fibre(fibre D) * shift(c)` no L² externo. O fator √((2π)^−1) permanece o mesmo e passa pela linearidade. A prova a.e. transporta o conjunto conull pela translação e intersecta apenas as quatro condições necessárias para o vetor fixado; não exige representantes pontualmente contínuos nem uma interseção não enumerável para todos os vetores.
6. {src('ScalarHomogeneousRightGNS',39)}: o operador preserva primeiro a imagem de `scalarWeightLinear`, depois seu fecho por continuidade. `scalarWeight_completion_eq`, herdado da revisão anterior, identifica esse fecho com o **mesmo** `scalarGNSSubspace P`. A restrição é um CLM `ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P`, definido em todo H_I; não é um novo completamento nem um operador restrito só à imagem algébrica.
7. {src('HomogeneousRightData',42)}: o adjunto inverte o produto, troca c por −c e D por D*, e a comutação entre shift e fibra permite reordenar. A instância torcida usa `rTowerPi_star` para Y′=ρy*ρ⁻¹. O lema herdado `tState_kms` que participa dessa identidade é uma computação matricial de pesos já provada, não uma hipótese de KMS global do core.
8. {src('ScalarHomogeneousRightGNS',59)}: a igualdade dos adjuntos restritos é demonstrada pelo pareamento herdado do ambiente; ambos os dados d,e preservam H_I. O lema genérico exige explicitamente `e.right = star d.right` e `e.frequency = -d.frequency`; nas instâncias matriciais são `rfl`. {src('ScalarHomogeneousRightGNS',74)} quantifica sobre quaisquer A,B no domínio escalar completo, com a orientação complexa correta ⟨R_yΛ(A),Λ(B)⟩=⟨Λ(A),R_y*Λ(B)⟩. Não se exige A* ou B* em n_ν.

**Pins e histórico autorais relidos — distintos da recompilação própria.** Fonte, binário, JSON final, rc0 efetivo, `output_exists`, fonte inalterada e stdout de cada módulo foram confrontados ao manifesto; os 28 nomes/axiomas coincidem exatamente. Os hashes dos streams completos ficam no manifesto e em `verification.json`.

| Módulo | Log final aceito | SHA256 JSON |
|---|---|---|
{chr(10).join(logs)}

Foram preservadas {len(failed)} tentativas autorais rc1, excluídas da conclusão: elaboração/reescrita, identificador `conj` inexistente, metas de conjugação e dois timeouts do pareamento. Impressões transitórias com `sorryAx` nesses logs não contam como prova; nenhuma aparece nos resultados finais aceitos. Na revisão própria, a primeira árvore `homogeneous_right_independent_20260912_153231_099220` preserva a falha de acesso à Mathlib (sandbox/WinError 5), não uma ausência real da biblioteca. A repetição autorizada resolveu o acesso. A primeira versão do auditor próprio também foi excluída por `Unknown option pp.width`; apenas o auditor foi corrigido/recompilado, sem repetir os cinco módulos verdes. Seu log e a versão anterior de `compilation.json` permanecem preservados. O parser inicial também não normalizava nomes de axiomas com universos impressos; o auditor final usa impressão de universos apenas nos tipos, mantendo os nomes completos usuais dos axiomas.

**Recorder e fronteira — inspeção estática, sem execução.** O {link('recorder final',ROOT/'record_homogeneous_right_memory.py')} exige leitura humana por `--review-read`, marcador do parecer, mãe/working/original pinados e fontes/binários/logs finais; fixa 5/28 e integração/KMS falsos. Para as 34 superfícies, verifica os pins anteriores, lê bytes, cria backup imediato exclusivo na mesma pasta, verifica igualdade exata, acrescenta preservando o prefixo e usa temporário verificado→replace por arquivo. Foram relidos os 34 pins atuais e os artefatos da mãe; estão preservados. Não foi executado o recorder nem foram produzidos seus backups/custódia nesta revisão.

A alteração anunciada durante esta rodada inseriu exatamente seis linhas no relatório interpolado do helper. Snapshot inicial `{v['recorder_initial_sha256']}` e final `{v['recorder_final_sha256']}` estão preservados; a AST fora da atribuição do texto do relatório é idêntica. A tabela atual do gate possui três pontes e não contém as seis flags maiores. Precisão de alcance: os tipos exatos são conferidos por Lean em `V350GateContract`; o Python exige os termos/bridges e sua proveniência/axiomas. O adendo documental não habilita flags nem comprova consumo futuro. Por essa alteração anunciada, `compilation.json` conserva `recorder_unchanged=false`; `verification.json` explica e valida os bytes finais, sem ocultar o snapshot anterior.

O relatório DEV foi lido integralmente e corresponde ao alcance provado. A identidade é local para unidades matriciais e dados homogêneos com hipóteses explícitas; não foi acrescentada a extensão por somas a toda matriz local nem uma representação direita global de toda N. **[OPEN]** Não se identificou neste pacote o fluxo candidato com (S†S)^it, não se provou KMS global de faixa, traço, escala/Three Locks, hipóteses físicas, consumo pelo gate ou runtime completo. I⊆n_ν e igualdade dos completamentos são herança; I=n_ν não é afirmado. Não se identifica D(S) com imagem algébrica. Essas fronteiras são limites, não bugs destas provas.

Pins finais, lidos dos arquivos por scripts:

| Artefato | SHA256 |
|---|---|
| {link('Manifesto autoral',ROOT/'homogeneous_right_draft_status.json')} | `{m['draft_status_sha256']}` |
| {link('Relatório DEV autoral',ROOT/'RELATORIO_DIREITA_MODULAR_GNS_DEV.md')} | `{m['report_sha256']}` |
| {link('Mãe integrada',ROOT/'scalar_weight_gns_custody.json')} | `{m['custody_sha256']}` |
| Cópia um.py, somente hash/leitura | `{m['initial_um_sha256']}` |
| {link('Manifesto próprio',RUN/'manifest.json')} | `{sha(RUN/'manifest.json')}` |
| {link('Compilação própria',RUN/'compilation.json')} | `{sha(RUN/'compilation.json')}` |
| {link('Verificação própria final',RUN/'verification.json')} | `{sha(RUN/'verification.json')}` |
| {link('Auditor final — stdout',aud['stdout'])} | `{aud['stdout_sha256']}` |

As seis flags maiores foram relidas falsas, `gate_extension.py` e a cópia do monólito permaneceram com os hashes iniciais, e os pareceres/custódias anteriores foram preservados. Não se executou/importou monólito, recorder ou testes autorais. Todas as saídas próprias estão em `revisao/`. **Escopo DEV encerrado, sem P0–P2; integração pendente e não avaliada.**
'''
p=REV/'REVIEW_HOMOGENEOUS_RIGHT_GNS.md';raw=text.encode('utf-8')
assert 'HOMOGENEOUS_RIGHT_GNS_DEV_REVIEW' in text and len(raw)>5000
if p.exists():
    old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with bk.open('xb') as f:f.write(old)
    assert bk.read_bytes()==old
tmp=p.with_name(p.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw;tmp.replace(p);assert p.read_bytes()==raw
print(json.dumps({'report':str(p),'sha256':sha(p),'bytes':len(raw),'lines':len(text.splitlines())},ensure_ascii=False))
