from pathlib import Path
import hashlib, json, datetime, os

root = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO')
out = root / 'revisao'
tree = out / 'scalar_semifiniteness_independent_20260914_085400_122493'
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def atomic(p, b):
    assert not p.exists(), str(p)
    temp = p.with_name(p.name + '.tmp')
    with temp.open('xb') as f:
        f.write(b)
    assert temp.stat().st_size == len(b) and temp.read_bytes() == b
    os.replace(temp, p)

c = read(tree / 'compilation.json')
p = read(tree / 'preflight.json')
for k in ['all_exit_zero', 'exact_targets', 'trio_only', 'source_dependency_and_review_pins_preserved', 'binary_byte_equal_to_author']:
    assert c[k] is True, k
for path, pin in p['pins'].items():
    assert sha(path) == pin, path
author = root / 'build/TGLExt/V351ScalarWeightSemifiniteness.olean'
assert sha(author) == p['author_binary_sha256'] == c['module']['object_sha256']
assert sha(tree / 'build/TGLExt/V351ScalarWeightSemifiniteness.olean') == sha(author)
for label in ['module', 'auditor']:
    assert sha(tree / f'{label}.stdout.txt') == c[label]['stdout_sha256']
    assert sha(tree / f'{label}.stderr.txt') == c[label]['stderr_sha256']
    assert 'warning:' not in (tree / f'{label}.stdout.txt').read_text(encoding='utf-8')

stamp = datetime.datetime.now().astimezone().isoformat()
report = out / 'REVIEW_A1_SEMIFINITUDE_FINAL.md'
link = lambda label, path: f'[{label}](<{path.as_posix()}>)'
body = f'''# Revisão independente — semifinitude escalar A1

Data: {stamp}

**[REAL] Aceito o delta DEV de um módulo/dois teoremas. Nenhum achado P0–P2 no escopo.** Leitura integral da fonte, dos tipos impressos e dos fornecedores pertinentes; recompilação própria e auditor separado concluídos rc0, sem avisos. Não resta análise necessária deste delta.

| Declaração em `TGLV351` | Alcance conferido |
|---|---|
| `scalarWeight_square_finite_wot_closure` | O fecho WOT de `nν` dentro do mesmo core regular é exatamente esse core, para todo `P : SiteProfile`. |
| `scalarWeight_unit_not_square_finite` | A unidade não pertence a `nν`, pois sua avaliação escalar é infinita. |

`HasFiniteScalarSquare P A` significa `q_(A* A)(regularVacuum P) < ∞`. Portanto o primeiro alvo trata o domínio escalar completo, não exige uma cota uniforme da forma em todos os vetores e não identifica esse domínio com o ideal uniforme anterior.

A inclusão do fecho no core usa seu fechamento WOT. A inclusão inversa reaproveita `A regularAverage_h`, pertencente ao core e de quadrado escalar finito quando `h>0`, convergindo fortemente para `A`. O filtro é o concreto `𝓝[>] 0` de reais, não vazio; a pertinência eventual vem de `h>0`. A passagem forte→WOT é explícita. Não há hipótese residual de densidade, continuidade SOT da estrela ou limite forte a fornecer.

O segundo alvo usa o mesmo vetor `hOmega P`: sua não nulidade decorre da norma unitária do `regularVacuum`, transportada pela isometria `testVector`. `baseDualWeight_unit_infinite` dá o valor `∞`, contradizendo estritamente `< ∞`; não ocorre uso indevido de `toReal` no infinito.

**[DERIVED — alcance matemático]** Junto às leis de peso fiel e normal já herdadas, a aproximação de quadrados finitos fornece o critério usual de semifinitude escalar. Os aproximantes herdados também são uniformemente limitados (`‖A regularAverage_h‖ ≤ ‖A‖`); não se infere uma identificação geral WOT/predual de redes arbitrárias. O novo enunciado Lean certifica precisamente o fecho WOT acima, sem construir uma interface geral de pesos no predual. A unidade ter peso infinito é compatível com semifinitude. Referência conceitual já examinada: definição 7.1 de [Hiai, Lectures on Selected Topics in von Neumann Algebras](https://arxiv.org/pdf/2004.02383).

**[OPEN] A1(b) permanece parcial.** Esta etapa paga a ponte de densidade do domínio escalar e reutiliza o transporte real para formas na base aprovado em {link('REVIEW_A1_BASE_ESTENDIDA_FINAL.md', out / 'REVIEW_A1_BASE_ESTENDIDA_FINAL.md')}. Não fornece a existência do traço fiel normal semifinito com escala dual exigido pelo contrato, nem sua perturbação a partir de ν. Também não acrescenta isomorfismo geral de cones/predual, KMS ou promoção de gate. A fórmula por supremos de minorantes positivos finitos do contrato **tracial** não é imposta aqui como requisito adicional para ν não tracial.

## Evidência própria e proveniência

Lean 4.31.0; módulo rc0 em {c['module']['seconds']:.3f}s e auditor rc0 em {c['auditor']['seconds']:.3f}s. Auditor com `#check` e universos explícitos mais `#print axioms` exatamente dos dois alvos. Ambos dependem apenas de `propext`, `Classical.choice`, `Quot.sound`, inclusive transitivamente.

| Artefato | SHA256 lido por script |
|---|---|
| Fonte final | `{c['module']['source_sha256']}` |
| `.olean` próprio = autoral, byte a byte | `{c['module']['object_sha256']}` |
| stdout próprio do módulo | `{c['module']['stdout_sha256']}` |
| stdout próprio do auditor | `{c['auditor']['stdout_sha256']}` |

O run autoral aceito é `attempts/20260914_084729_714501/run.json`; sua evidência foi relida e confrontada, sem substituir a reprodução própria. Foram conferidos os 378 registros do manifesto autoral de dependências e os seis fornecedores da ficha. A árvore própria congelada contém 382 objetos de projeto: 380 binários antigos herdados por hashes e dois pais V351 previamente recompilados de forma independente. Quatro dos antigos foram acrescentados agora por cópia pinada: `ContractionAdjointLimit`, `StrongBoundedApplication`, `FiniteDualStarCore` e `ScalarWeightDomain`. Não se afirma recompilação independente desses 380 objetos.

O `LEAN_PATH` usa somente o build próprio para objetos de projeto e pacotes externos somente leitura. Não foi usado build autoral de projeto como caminho de importação; pacotes não foram recompilados. Inventário, origens e hashes completos constam da árvore de evidências.

Evidências: {link('compilation.json', tree / 'compilation.json')}; {link('preflight.json', tree / 'preflight.json')}; {link('auditor.stdout.txt', tree / 'auditor.stdout.txt')}; {link('verification.json', tree / 'verification.json')}.

[REAL] Fonte/binário autorais, fichas pinadas, `um.py` e os pareceres anteriores conferidos permanecem byte a byte. Escritas restritas a `revisao/`; nenhum recorder, integrador ou monólito foi executado, nenhuma memória foi atualizada. Esta conclusão é DEV, sem aceite integrado ou nova custódia.
'''
atomic(report, body.encode('utf-8'))
v = {
    'time': stamp,
    'status': 'DEV_ACCEPTED_NO_P0_P2',
    'source_and_author_binary_rechecked': True,
    'prior_pins_preserved': True,
    'own_compilation': c,
    'pins': p['pins'],
    'report': {'path': str(report), 'sha256': sha(report)},
    'evidence_pins': {str(tree / n): sha(tree / n) for n in ['compilation.json', 'preflight.json', 'module.stdout.txt', 'module.stderr.txt', 'auditor.stdout.txt', 'auditor.stderr.txt']},
    'limits': ['WOT closure criterion explicitly proved; predual interface not constructed', 'A1(b) trace existence/perturbation open', '380 old project objects inherited, not recompiled', 'No integration, monolith execution, memory update or custody']
}
atomic(tree / 'verification.json', (json.dumps(v, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps(v['report'], ensure_ascii=False))
print('FINAL_REVIEW_WRITTEN')
