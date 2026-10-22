from pathlib import Path
import datetime, hashlib, json, os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
P=Path((REV/'scalar_vna_partial_latest_run.txt').read_text().strip())
R=Path((REV/'scalar_vna_final_latest_run.txt').read_text().strip())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
pm=load(P/'manifest.json');pc=load(P/'compilation.json');m=load(R/'manifest.json');c=load(R/'compilation.json')
st=load(R/'helper_static_inspection.json');d=load(R/'documents/scalar_vna_draft_status.json')
for obj in [pc,c]:
    assert obj['complete'] and obj['all_exit_zero'] and obj['all_axioms_allowed'] and obj['dependencies_preserved']
    assert obj['author_source_binary_preserved'] and obj['read_only_artifacts_preserved'] and obj['author_final_log_streams_preserved']
assert pc['three_binaries_equal_author'] and pc['exact_17_targets']
assert c['new_binary_equals_author'] and c['exact_27_targets'] and c['cumulative_four_pins_preserved'] and c['cumulative_27_axioms_match_draft']
assert not any(st['assessment'][x] for x in ['P0','P1','P2'])
assert all(hf(ROOT/n)==h for n,h in m['cumulative_draft_pins'].items())
assert all(hf(p)==v['expected'] for p,v in st['surface_pins'].items())
assert all(hf(p)==h for p,h in st['readonly_parent_artifacts'].items())
assert hf(ROOT/'um.py')==st['working_sha256'] and hf(ROOT/'gate_extension.py')==st['gate_sha256']
for name,x in d['modules'].items():
    assert hf(ROOT/'kernel/TGLV350'/(name+'.lean'))==x['source_sha256']
    assert hf(ROOT/'build/TGLV350'/(name+'.olean'))==x['binary_sha256']
def link(label,p,line=None):return f'[{label}](<{Path(p).as_posix()}{":"+str(line) if line else ""}>)'
def src(n,decl):return link(n+'.lean',ROOT/'kernel/TGLV350'/(n+'.lean'),st['declaration_lines'][n][decl])
table='\n'.join(f'| {n} | {x["targets"]} | `{x["source_sha256"]}` | `{x["binary_sha256"]}` |' for n,x in d['modules'].items())
logs='\n'.join('- '+link(Path(x['final_log']).name,x['final_log'])+f' — SHA256 `{x["final_log_sha256"]}`.' for x in d['modules'].values())
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''# Revisão DEV — imagem escalar de von Neumann

{date} — SCALAR_VNA_DEV_REVIEW

[REAL — revisão independente concluída neste escopo] **Nenhum achado P0, P1 ou P2.** Lidas integralmente as quatro fontes, o manifesto, o relatório DEV e os cinco helpers. Quatro módulos recompilados em árvores próprias; auditor cumulativo de **27 tipos/axiomas**, com universos impressos, rc0. Os quatro binários próprios são idênticos aos autorais aceitos. **DEV revisado; integração pendente.**

O resultado substantivo é a igualdade entre o bicomutante e a imagem efetiva de `scalarGNSRepresentation P` no **mesmo `ScalarGNSHilbert P`**. A definição por álgebra gerada é acompanhada de pré-imagem para cada elemento e de igualdade com `Set.range`; nenhuma hipótese residual de fechamento da imagem é recebida no teorema concreto.

Conferências matemáticas:

- {src('ReducingCommutantCompression','reducingBicommutant_orbit_bound')}: a coluna `C = D ∘ incl` entrelaça a representação restrita e a ambiente, também para `star a`. Logo `C* C` comuta com a imagem restrita. A hipótese `hB` é exatamente comutação com seu comutante; permite comutar com a raiz positiva e obter `‖D(Bv)‖ ≤ ‖B‖ ‖Dv‖`. Não exige que `D` preserve o subespaço, nem que `B` seja positivo, nem multiplicatividade da compressão.
- {src('ReducingBicommutantLift','reducingBicommutantLift_apply')}: densidade de `M′v`, obtida do vetor separante para **M**, e a cota anterior justificam a extensão `D v ↦ D(B v)`. A ordem dos produtos no comutante é preservada; não se supõe que seus elementos comutem entre si. Pertinência em `M = M′′`, cota e restrição exata são demonstradas. A definição total `extendOfNorm`, isolada, não é tomada como certificado. Na restrição usa-se a órbita projetada densa e a compressão que comuta com `B`; não uma extensão por zero supostamente comutante.
- {src('SeparatingRestrictionVonNeumann','mem_generated_restriction_iff')}: `hB` é descarregada a partir da pertinência na álgebra gerada. Permanecem no lema genérico as hipóteses explícitas de invariância, completude do subespaço e vetor separante em M. A invariância para a álgebra estrela fornece redução. O transporte de centralizadores e bicomutantes usa uma equivalência estrela entre os espaços, com direções verificadas.
- {src('ScalarGNSVonNeumann','scalarGaussianImage_generated_iff')}: a aplicação usa `dualOrbitVonNeumann (regularCoreAlgebra P)`, `scalarGaussianImage P` e `scalarGaussianVacuum P`. `mem_dualOrbitVonNeumann_iff`, invariância da imagem, completude, pertença e separação do vetor são provas herdadas efetivamente aplicadas. Não se pressupõe separação para o bicomutante restrito. A unitária **linear** `scalarGaussianUnitary` entrelaça as duas representações e transporta a igualdade; {src('ScalarGNSVonNeumann','mem_scalarGNSVonNeumann_iff')} e `scalarGNSVonNeumann_coe` não recebem nova hipótese sobre P, normalidade, KMS ou graph-core de F.

Os quatro auxiliares privados do último módulo foram lidos e estão abrangidos transitivamente pelo auditor. Todos os 27 alvos dependem somente de `propext`, `Classical.choice` e `Quot.sound`; nenhum `sorryAx`, axioma próprio ou `unsafe` nas fontes finais. Os genéricos deste lote usam `H : Type` (universo 0), conforme os tipos impressos; não atribuo generalização adicional de universos.

Evidência própria e proveniência:

- {link('Compilação própria dos três primeiros + auditor17',P/'compilation.json')}: quatro execuções rc0. {link('Manifesto parcial',P/'manifest.json')} fixa **{len(pm['dependencies'])} dependências de projeto** reutilizadas.
- {link('Compilação própria do quarto + auditor27',R/'compilation.json')}: duas execuções rc0. {link('Manifesto final',R/'manifest.json')} fixa **{len(m['dependencies'])} dependências de projeto**, incluindo os três novos binários próprios já verdes. Eles não foram recompilados novamente. {link('Tipos e axiomas cumulativos',R/'logs/ScalarVNAFinalAudit.stdout.txt')}.
- Origens próprias recuperadas: `core_polar_independent_20260912_203148_639288` (inclui `ReducingCommutantTransport`), `gaussian_polar_independent_20260912_210534_399150` (polar limitado e aplicação gaussiana), `right_vector_final_independent_20260913_000859_199687`, e o estrato parcial desta revisão. Manifestos, compilações e pares fonte/binário foram relidos e pinados; a origem imediata de cada dependência está nos manifestos.
- `LEAN_PATH`: apenas o build próprio e oito bibliotecas externas readonly. Nenhum build autoral de projeto. Lean {m['lean_version']}; SHA do executável `{m['compiler_sha256']}`. Bibliotecas herdadas não foram recompiladas; a verificação desta rodada fixa o compilador e os pins externos diretos registrados, não reaudita integralmente a biblioteca.
- Quatro tentativas autorais rc1 foram preservadas e excluídas, inclusive seus prints com `sorryAx`; somente logs finais que coincidem com fonte e binário correntes sustentam a comparação. A primeira preparação própria falhou **antes de executar Lean**, por ausência de uma dependência no catálogo mínimo; foi recuperada da árvore própria CorePolar. Registro em {link('falha de preparação preservada',REV/'scalar_vna_partial_independent_20260913_005752_578688/preparation_failure.json')}. Não houve erro Lean nas recompilações próprias executadas.

Pins SHA256 lidos por script; hashes completos de streams e resultados próprios nos artefatos acima:

| Módulo | Alvos | Fonte | Binário autoral = próprio |
|---|---:|---|---|
{table}

Logs autorais aceitos, distintos dos logs próprios:

{logs}

Manifesto DEV: `{st['manifest_sha256']}`. Relatório DEV: `{st['report_sha256']}`. Mãe `right_vector_custody.json`: `{st['parent_custody_sha256']}`. A custódia mãe foi usada como origem pinada; seus 197 registros antigos não foram recompilados nem integralmente reauditados nesta rodada.

Helpers e documentação: {link('inspeção estática e pins dos cinco helpers',R/'helper_static_inspection.json')}. Conferidos mãe única `right_vector`, quatro módulos/27 alvos, transição prevista 598→625, pré-condições de leitura dos pareceres DEV/integrado e preservação da fronteira. O preparador altera apenas as listas/controle previstos; o recorder exige fonte/binário, transposição, AST fora do embutido, Audit atual/histórico, flags e pins das 34 superfícies; faz backup imediato de bytes, append com prefixo preservado e substituição temporária por arquivo. O verifier relê pares fonte/binário e backups/prefixos. Essas funções de gravação permanecem iguais às correspondentes da etapa mãe. **Nenhum helper foi executado por esta revisão; não se certifica uma custódia futura por inspeção estática.**

[REAL — leitura de pins] As 34 superfícies ainda coincidem com a mãe; cópia `{st['working_sha256']}` e `gate_extension.py` preservados. Seis flags maiores falsas. As contagens futuras 201/101/6982/903 são expectativas do preparador, não resultados deste DEV. Monólito, integradores, recorders e testes autorais não foram executados/importados; não houve escrita fora de `revisao/`.

[OPEN] Graph-core do F original pela álgebra de pares, reconstrução `R = Jπ(b)J`, inclusão inversa com o mesmo J, identificação de `Δ^it`, KMS, traço/Three Locks e consumo tipado/runtime permanecem fora desta conclusão. A consulta por blocos é proposta, sem novo alvo Lean neste lote. A unitária gaussiana V não substitui J, e não se identifica Tomita do vetor com Tomita do peso. **Nenhuma análise DEV necessária dos quatro módulos/27 alvos resta pendente; nenhuma aprovação integrada ou de gate é emitida.**
'''
out=REV/'REVIEW_SCALAR_VNA_DEV.md';raw=text.encode('utf-8');old=None
if out.exists():
    old=out.read_bytes();bak=out.with_name(out.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with bak.open('xb') as f:f.write(old)
    assert bak.read_bytes()==old;raw=old+b'\n\n'+raw
tmp=out.with_name(out.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and (old is None or out.read_bytes()==old)
os.replace(tmp,out);assert out.read_bytes()==raw
print(json.dumps({'report':str(out),'sha256':hf(out),'bytes':len(raw),'P0':0,'P1':0,'P2':0,'DEV_complete':True,'integrated':False}))
