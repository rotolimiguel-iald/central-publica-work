from pathlib import Path
from datetime import datetime
import hashlib
import json
import os

REV = Path(__file__).resolve().parent
RUN = Path((REV / 'paired_right_second_latest_run.txt').read_text().strip())
FIRST = Path((REV / 'paired_right_first_latest_run.txt').read_text().strip())
REPORT = REV / 'REVIEW_PAIRED_RIGHT_DEV.md'
assert RUN.is_relative_to(REV) and FIRST.is_relative_to(REV)
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    return json.loads(p.read_bytes())
def link(label, p, line=None):
    return f'[{label}](<{p.resolve().as_posix()}' + (f':{line}' if line else '') + '>)'
def atomic(p, data):
    assert p.resolve().is_relative_to(REV)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name + '.bak_' + stamp)
        with backup.open('xb') as f:
            f.write(old)
        assert backup.read_bytes() == old
    temp = p.with_name(p.name + '.tmp_' + stamp)
    with temp.open('xb') as f:
        f.write(data)
    assert temp.read_bytes() == data
    os.replace(temp, p)
    assert p.read_bytes() == data

c = load(RUN / 'compilation.json')
m = load(RUN / 'manifest.json')
p = load(RUN / 'reviewer_input_pins.json')['modules']['ScalarCommutantSandwich']
first_pin = load(FIRST / 'partial_review_pin.json')
assert sha(REPORT) == first_pin['report_sha256']
assert all(v for v in c.values() if isinstance(v, bool))
assert len(c['records']) == 2
assert len(m['declarations']) == 12
assert len(m['dependencies']) == 415
for r in c['records']:
    assert r['returncode'] == 0 and r['exact_targets'] and r['axioms_allowed']
    assert sha(Path(r['command'][-1])) == r['source_sha256']
    assert sha(Path(r['command'][2])) == r['output_sha256']
    assert sha(Path(r['stdout'])) == r['stdout_sha256']
    assert sha(Path(r['stderr'])) == r['stderr_sha256']
    assert len(r['axioms']) == 12
    assert all(set(a) == {'propext', 'Classical.choice', 'Quot.sound'} for a in r['axioms'].values())
module, audit = c['records']
prior = load(FIRST / 'compilation.json')
assert prior['all_exit_zero'] and prior['exact_8_targets']
assert len(set(audit['axioms']) | set(prior['records'][-1]['axioms'])) == 20
dep = m['dependencies']['TGLV350.ScalarRightAdjointPair']
assert dep['sha256'] == prior['records'][0]['output_sha256']
assert sha(Path(dep['frozen_binary'])) == dep['sha256']
source = RUN / 'sources/TGLV350/ScalarCommutantSandwich.lean'
lines = source.read_text(encoding='utf-8').splitlines()
def at(needle):
    return next(i for i, s in enumerate(lines, 1) if needle in s)
history = load(RUN / 'author_history.json')
failures = sum(r['returncode'] != 0 for r in history)
now = datetime.now().astimezone().isoformat(timespec='seconds')
old = REPORT.read_bytes()
old_sha = sha(REPORT)
addition = f'''

---

Adendo {now} — **segundo módulo / 12 alvos; acumulado próprio: 2 módulos / 20 alvos.** Estrato inicial preservado por backup imediato de bytes e append. A conclusão conjunta dos 29 continua pendente.

[REAL] **Nenhum achado P0–P2 em ScalarCommutantSandwich na versão final pinada.** Fonte e doze tipos com universos lidos integralmente; recompilação independente rc0 em {module['seconds']} s, auditor próprio rc0 em {audit['seconds']} s. Os doze alvos usam apenas o trio lógico; os dois auxiliares privados são cobertos transitivamente. Binário próprio igual ao autoral. {link('Compilação e preservação', RUN / 'compilation.json')}; {link('tipos e axiomas próprios', Path(audit['stdout']))}.

A definição {link('K_h(T) = R_h* T R_h', source, at('def scalarCommutantSandwich ('))} conserva a ordem. A prova da identidade direita usa somente T e R_h* comutando com π(a), nunca T comutando com R_h. Para h>0, os vetores são precisamente η=R_h*Tη_h e ζ=R_h*T*η_h; o {link('par construído', source, at('def scalarCommutantSandwichPair'))} vale para todo a∈nν. A pertença de η ao domínio do **F=S† original** e Fη=ζ são deduzidas do primeiro módulo, sem hipótese adicional sobre o gráfico de F.

Os {link('auxiliares genéricos', source, at('private theorem boundedRightStarMul'))} provam a reversão do produto por `ContinuousLinearMap.adjoint_comp` e preservação da norma por `ContinuousLinearMap.adjoint.norm_map`. Não impõem uma nova hipótese `NormedStarGroup` ao GNS concreto nem mudam sua norma/estrela. As falhas anteriores de elaboração não permanecem como axiomas nos resultados aceitos.

A cota ‖K_h(T)‖≤‖T‖ vale para todo h. Os {link('limites fortes de K_h(T) e K_h(T)*', source, at('theorem scalarCommutantSandwich_tendsto'))} usam a cota uniforme e a convergência dos adjuntos de **contrações para I**, não continuidade geral de star em SOT. A aproximação final é em `𝓝[>] 0`, filtro não vazio; a pertinência ao contrato do par é eventual nesse filtro. As duas convergências não exigem comutação de T; a hipótese T∈π(N)' é usada para construir os pares.

| Artefato | SHA256 lido |
| --- | --- |
| Segunda fonte congelada | `{module['source_sha256']}` |
| Segundo .olean próprio = autoral | `{module['output_sha256']}` |
| Log autoral final `{Path(p['final_log']).name}` | `{p['final_log_sha256']}` |
| Auditor próprio: stdout | `{audit['stdout_sha256']}` |
| compilation.json do segundo estrato | `{sha(RUN / 'compilation.json')}` |
| Manifesto próprio do segundo estrato | `{sha(RUN / 'manifest.json')}` |

{link('Proveniência', RUN / 'manifest.json')}: 415 dependências de projeto copiadas da primeira árvore própria deste pacote, incluindo o .olean verde de ScalarRightAdjointPair. O primeiro módulo e as 414 dependências herdadas não foram recompilados. Foram executados somente a segunda fonte e seu auditor; o LEAN_PATH mantém build próprio e pacotes externos readonly. {link('Histórico autoral', RUN / 'author_history.json')}: {failures} rc1 preservados e excluídos da aceitação. Preservação de fontes/binários autorais, dependências, 34 memórias/backups, mãe, pareceres anteriores, monólito e gate verificada pelo runner.

[OPEN] Terceiro módulo, manifesto autoral de 29 alvos e exame final dos helpers ainda pendentes. Estes 20 alvos não estabelecem núcleo denso no gráfico de F, reconstrução por J, inclusão inversa dos comutantes, álgebra de Hilbert completa ou KMS/traço. Nenhuma integração, recorder ou memória foi executada/atualizada pelo revisor.
'''
atomic(REPORT, old + addition.encode('utf-8'))
assert REPORT.read_bytes().startswith(old)
evidence = {'timestamp': now, 'report': str(REPORT), 'report_sha256': sha(REPORT),
            'preserved_prefix_sha256': old_sha, 'preserved_prefix_bytes': len(old),
            'status': 'PARTIAL_2_MODULES_20_TARGETS_COMPLETE__FULL_29_PENDING',
            'first_compilation_sha256': sha(FIRST / 'compilation.json'),
            'second_compilation_sha256': sha(RUN / 'compilation.json'), 'findings': []}
atomic(RUN / 'partial_review_pin.json', (json.dumps(evidence, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
print(json.dumps(evidence, ensure_ascii=False))
