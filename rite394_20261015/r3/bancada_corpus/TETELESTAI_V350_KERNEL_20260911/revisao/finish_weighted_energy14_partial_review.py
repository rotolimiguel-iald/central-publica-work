import json, hashlib, pathlib, datetime, os
ROOT=pathlib.Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911')
REV=ROOT/'revisao'
RUNS=[REV/'weighted_energy_independent_20260913_075046_729438',REV/'weighted_energy14_independent_20260913_075357_051838']
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(pathlib.Path(p).read_bytes())
def write(p,b):
    assert p.is_relative_to(REV)
    if p.exists():
        old=p.read_bytes(); bak=p.with_name(p.name+'.bak_'+stamp); bak.write_bytes(old); assert bak.read_bytes()==old
        b=old+b'\n\n'+b
    temp=p.with_name(p.name+'.tmp_'+stamp); temp.write_bytes(b); assert temp.read_bytes()==b; os.replace(temp,p)
now=datetime.datetime.now().astimezone(); stamp=now.strftime('%Y%m%d_%H%M%S_%f')
ms=[read(p/'manifest.json') for p in RUNS]; cs=[read(p/'compilation.json') for p in RUNS]
for m,c in zip(ms,cs):
    for k in ['complete','all_exit_zero','all_axioms_allowed','all_axioms_match_author','source_snapshot_preserved','dependencies_preserved','external_direct_pins_preserved']: assert c[k],k
    for s in m['sources'].values():
        assert sha(s['path'])==sha(s['snapshot'])==s['sha256']
        assert sha(s['author_binary'])==s['author_binary_sha256']
        assert sha(s['author_log'])==s['author_log_sha256']
    for rec in c['records']:
        assert rec['returncode']==0 and rec['exact_targets'] and rec['axioms_allowed']
        assert sha(rec['command'][2])==rec['output_sha256']
        assert sha(rec['stdout'])==rec['stdout_sha256'] and sha(rec['stderr'])==rec['stderr_sha256']
assert cs[0]['exact_7_targets'] and cs[1]['exact_14_targets']
assert not cs[0]['binary_equal_author'] and cs[1]['binary_equal_author']
assert sha(ms[1]['inherited_first_binary'])==ms[1]['inherited_first_binary_sha256']
assert sha(ROOT/'paired_blocks_custody.json')==ms[1]['parent_custody_sha256']
rows=[]
for m,c in zip(ms,cs):
    s=next(iter(m['sources'].values())); rec=c['records'][0]
    rows.append(f"| {pathlib.Path(s['path']).name} | `{s['sha256']}` | `{s['author_binary_sha256']}` | `{rec['output_sha256']}` |")
targets='\n'.join('- `'+n+'`' for n in ms[1]['declarations'])
doc=f'''# Revisão independente — energia ponderada e cota de bloco

WEIGHTED_ENERGY_DEV_REVIEW — PARCIAL DEV14, dois módulos congelados. {now.isoformat(timespec='seconds')}

[REAL] Concluídas leitura integral, exame dos tipos/hipóteses e recompilação própria dos dois módulos, com auditor cumulativo separado de 14 declarações. **Nenhum achado matemático P0–P2.** Há uma ressalva explícita de igualdade binária no primeiro módulo, descrita abaixo. Este parecer encerra apenas DEV14; não certifica outros módulos, integração ou consumo pelo gate.

## Evidência própria e proveniência

- `weighted_energy_independent_20260913_075046_729438`: WeightedVariationalEnergy rc0 em {cs[0]['records'][0]['seconds']} s; auditor7 rc0 em {cs[0]['records'][1]['seconds']} s.
- `weighted_energy14_independent_20260913_075357_051838`: ProjectionGapLowerBound rc0 em {cs[1]['records'][0]['seconds']} s; auditor14 rc0 em {cs[1]['records'][1]['seconds']} s. Os 14 tipos/universos foram impressos e lidos; cada fecho transitivo de axiomas contém somente propext, Classical.choice e Quot.sound, coincidindo com os alvos autorais aceitos.
- LEAN_PATH próprio com 337 e 340 dependências de projeto respectivamente, reaproveitadas e pinadas da árvore `paired_blocks27_independent_20260913_070702_176639`; a segunda execução inclui o binário produzido pela primeira. O manifesto guarda a origem imediata e hashes das fontes/binários herdados. Isso não significa recompilação de toda a ancestralidade nesta rodada. Oito diretórios de pacotes externos foram usados somente para leitura, com 14 pares externos diretos pinados. Nenhum build autoral de projeto no LEAN_PATH; nenhuma biblioteca reconstruída.
- Mãe documental lida: paired_blocks_custody.json SHA256 `{sha(ROOT/'paired_blocks_custody.json')}`. Preservação de dependências e artefatos readonly registrada nos compilation.json; nenhuma memória ou fonte autoral foi escrita.

| Fonte | SHA256 fonte | SHA256 .olean autor | SHA256 .olean próprio |
|---|---|---|---|
{chr(10).join(rows)}

Logs autorais aceitos: WeightedVariationalEnergy_20260913_074553_539505.json e ProjectionGapLowerBound_20260913_075000_423719.json. Seus hashes de log/stdout/stderr estão nos manifests próprios. Foram preservadas e excluídas as duas tentativas rc1 anteriores do primeiro módulo e a tentativa rc1 do segundo; prints parciais ou com sorryAx não contam como evidência.

**Ressalva binária:** o .olean próprio de WeightedVariationalEnergy não é literalmente igual ao autoral. Ambos contêm o caminho absoluto de sua fonte associado ao warning de hA não utilizado (linha 70); os stdout coincidem após somente substituir esse caminho. O arquivo binary_comparison.json registra comprimentos, hashes, posição do caminho e região igual. Não foi demonstrada equivalência completa de serialização normalizada. A recompilação integral e a importação no auditor passaram rc0. ProjectionGapLowerBound teve igualdade literal de binários. O campo binary_equal_author=true do segundo compilation.json refere-se apenas a esse módulo novo; não apaga a divergência do primeiro.

## Hipóteses e composição conferidas

**WeightedVariationalEnergy.lean, linhas 12–108.** Operadores limitados no mesmo Hilbert complexo completo. A orientação do produto interno e os conjugados são consistentes: Re z=1 e a identidade complexa fornecida dão a energia real. `variationalPair_energy_bound` recebe Y auto-adjunto, Z=L*L e a identidade variacional; não supõe simetria de uma forma B_z, nem precisa positividade de Y para essa desigualdade. A fatoração com sqrt(e) usa e≥0. O último teorema recebe explicitamente eT=Te, AT=TA e Bx=A(Tη); daí obtém a cota com ||T||². A prova não introduz AB=BA. O hA não utilizado na especialização intermediária é hipótese redundante benigna; hA é usado na etapa final. A identidade variacional e sua instanciação concreta não são construídas neste módulo genérico.

**ProjectionGapLowerBound.lean.** e=(I−cA)⁺ é definido pelo CFC; nas identidades e conclusões de ordem relevantes, A auto-adjunto é hipótese explícita. De eB=0, BB*=A(I−A), eA=Ae e injetividade de A, o cancelamento é ponto a ponto, sem dividir por B nem supor AB=BA. Para c≥1, e²=(1−c)e, positividade e a propriedade C* implicam e=0, inclusive c=1. De e=0 e c>0 resulta c⁻¹I≤A por multiplicação escalar não negativa e cancelamento; a implementação não depende da instância PosSMulReflectLE que falhou na tentativa autoral. A última declaração deriva IsStrictlyPositive A da cota já recebida, incluindo a condição IsUnit. Nenhum CompleteSpace de subtipo VNA, PVM, gap prévio ou domínio total de operador não limitado foi presumido.

**Limite determinante:** eB=0 permanece uma premissa honesta do segundo módulo, não resultado deste DEV14. A energia genérica não fornece sozinha esse anulamento nem a cota uniforme para os blocos concretos. São limites de composição, não defeitos dos enunciados revisados. Os resultados não identificam por si sós Δ^it/KMS, a inclusão inversa com J original ou traço. Tampouco esses objetivos adicionais são automaticamente requisitos do gate v350: essa relação deve ser decidida pelos contratos efetivamente consumidos, objeto da auditoria de reutilização separada solicitada depois.

## Alvos auditados

{targets}

## Artefatos verificáveis

Os diretórios acima, sob revisao/, contêm manifest.json, compilation.json, fontes congeladas, auditores, stdout/stderr e histórico autoral. Em particular: [compilation7](weighted_energy_independent_20260913_075046_729438/compilation.json), [comparação binária](weighted_energy_independent_20260913_075046_729438/binary_comparison.json), [compilation14](weighted_energy14_independent_20260913_075357_051838/compilation.json), [auditor14](weighted_energy14_independent_20260913_075357_051838/sources/WeightedEnergyAudit14.lean). Não houve execução de um.py, integrador, recorder ou testes autorais. Nenhuma integração aprovada por este parecer parcial.
'''
p=REV/'REVIEW_WEIGHTED_ENERGY_DEV.md';write(p,doc.encode('utf-8'))
e={'timestamp':now.isoformat(),'scope':'PARTIAL_DEV14','report':str(p),'report_sha256':sha(p),'mathematical_findings_P0_P2':[], 'first_binary_literal_equal':False,'second_binary_literal_equal':True,'integration_reviewed':False,'sources':[next(iter(m['sources'].values())) for m in ms], 'own_compilation_pins':{str(r/'compilation.json'):sha(r/'compilation.json') for r in RUNS}}
write(RUNS[1]/'partial_review_evidence.json',json.dumps(e,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({'report':str(p),'sha256':sha(p),'bytes':p.stat().st_size,'scope':'PARTIAL_DEV14'},ensure_ascii=False))
