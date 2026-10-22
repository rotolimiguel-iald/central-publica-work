from pathlib import Path
from collections import Counter
from datetime import datetime
import hashlib
import json
import os

REV = Path(__file__).resolve().parent
RUN = REV / 'paired_right_first_independent_20260912_223704_199271'
REPORT = REV / 'REVIEW_PAIRED_RIGHT_DEV.md'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def link(label, p, line=None):
    target = p.resolve().as_posix() + (f':{line}' if line else '')
    return f'[{label}](<{target}>)'

def atomic(p, data):
    assert p.resolve().is_relative_to(REV)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name + '.bak_' + stamp)
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temp = p.with_name(p.name + '.tmp_' + stamp)
    temp.write_bytes(data)
    assert temp.read_bytes() == data
    os.replace(temp, p)
    assert p.read_bytes() == data

assert not REPORT.exists(), 'Existing partial review must be preserved and extended deliberately.'
c = json.loads((RUN / 'compilation.json').read_bytes())
m = json.loads((RUN / 'manifest.json').read_bytes())
pins = json.loads((RUN / 'reviewer_input_pins.json').read_bytes())
assert all(v for k, v in c.items() if isinstance(v, bool))
assert len(c['records']) == 2
assert len(m['declarations']) == 8
source = RUN / 'sources/TGLV350/ScalarRightAdjointPair.lean'
module, audit = c['records']
for rec in c['records']:
    assert rec['returncode'] == 0 and rec['exact_targets'] and rec['axioms_allowed']
    assert sha(Path(rec['command'][-1])) == rec['source_sha256']
    assert sha(Path(rec['command'][2])) == rec['output_sha256']
    assert sha(Path(rec['stdout'])) == rec['stdout_sha256']
    assert sha(Path(rec['stderr'])) == rec['stderr_sha256']
    assert len(rec['axioms']) == 8
    assert all(set(v) == {'propext', 'Classical.choice', 'Quot.sound'} for v in rec['axioms'].values())
origins = Counter(Path(v['reviewer_origin']).name for v in m['dependencies'].values())
assert len(m['dependencies']) == 414
lines = source.read_text(encoding='utf-8').splitlines()
def at(needle):
    return next(i for i, s in enumerate(lines, 1) if needle in s)

now = datetime.now().astimezone().isoformat(timespec='seconds')
p = pins['modules']['ScalarRightAdjointPair']
origin_text = '; '.join(f'{n} de `{name}`' for name, n in sorted(origins.items()))
text = f'''# Revisão DEV parcial — pares de multiplicação direita

Estrato {now}. **PARCIAL: 1 módulo / 8 alvos; pacote de 3 / 29 ainda pendente.**

[REAL] **Nenhum achado P0–P2 no primeiro módulo congelado.** Leitura integral da fonte e dos oito tipos com universos, recompilação independente do módulo e auditor próprio concluídas. Este estrato não conclui a revisão dos dois módulos restantes nem dos cinco helpers.

O contrato {link('ScalarRightAdjointPair', source, at('structure ScalarRightAdjointPair'))} recebe as duas identidades de vetores para todo `a ∈ nν`, com operadores limitados `R` e `R*` no mesmo `ScalarGNSHilbert P`. A pertença de η ao domínio do adjunto e `Fη = ζ` são conclusões; não são campos nem premissas escondidas. Não se identifica o ideal uniforme I com nν.

O {link('pareamento regularizado', source, at('theorem scalarRightAdjointPair_regularized_pairing'))} respeita a ordem complexa: `⟨Λ(a*), π(e_h)η⟩ = ⟨ζ, R_h Λ(a)⟩`, para `a ∈ nν ∩ nν*` e `h > 0`. A média entra no ideal escalar pela inclusão já provada do ideal uniforme. A passagem ao limite usa π(e_h)→I e R_h→I fortemente e o filtro não vazio `𝓝[>] 0`; não pressupõe Λ(1) nem continuidade de S.

O {link('pareamento no fecho', source, at('theorem scalarRightAdjointPair_closed_pairing'))} usa a igualdade herdada entre o fecho do gráfico da estrela no domínio escalar completo e o gráfico do **S original**. O auxiliar privado aplica fechamento de uma igualdade contínua de pareamentos no produto Hilbert. Explicitar `p := (x, Sx)` resolve a inferência sem modificar a hipótese matemática. A {link('conclusão maximal', source, at('theorem scalarRightAdjointPair_maximal'))} aplica precisamente o **F = S† original**, para todo x ∈ D(S); não substitui um adjunto ou vetor gaussiano.

[REAL] Evidência própria: {link('compilation.json', RUN / 'compilation.json')} — módulo rc0 em {module['seconds']} s e auditor rc0 em {audit['seconds']} s. O {link('stream do auditor', Path(audit['stdout']))} contém exatamente oito `#check` com universos e oito `#print axioms`; todos usam somente `propext`, `Classical.choice`, `Quot.sound`. O auxiliar privado é coberto transitivamente. O binário próprio coincide byte a byte com o autoral.

| Artefato | SHA256 lido |
| --- | --- |
| Fonte congelada | `{module['source_sha256']}` |
| .olean próprio = autoral | `{module['output_sha256']}` |
| Log autoral final `{Path(p['final_log']).name}` | `{p['final_log_sha256']}` |
| Stream do auditor próprio | `{audit['stdout_sha256']}` |
| compilation.json próprio | `{sha(RUN / 'compilation.json')}` |
| Manifesto próprio de dependências | `{sha(RUN / 'manifest.json')}` |

Proveniência: {link('manifest.json', RUN / 'manifest.json')} fixa 414 dependências de projeto, copiadas das árvores **próprias** já revisadas: {origin_text}. Nenhuma dependência antiga foi recompilada. `LEAN_PATH` contém somente o build desta árvore e oito diretórios de pacotes externos em leitura; não contém build autoral do projeto. Lean 4.31.0 e pins das origens/pacotes constam no manifesto. A leitura externa para compilar foi autorizada com `require_escalated`; as saídas ficaram em revisao/.

O {link('registro parcial de pins', RUN / 'reviewer_input_pins.json')} é do revisor e declara explicitamente que o manifesto autoral de 29 alvos ainda está pendente. Mãe integrada lida: `right_regularization_custody.json`, SHA `{pins['parent_custody_sha256']}`. O {link('histórico capturado', RUN / 'author_history.json')} preserva seis tentativas rc1 e o rc0 final; prints das tentativas falhas não foram aceitos como auditoria. Fonte/binário autorais, dependências, 34 memórias/backups, pareceres anteriores, monólito e gate permaneceram inalterados segundo os checks desta execução.

[OPEN] Ainda faltam os dois módulos finais, manifesto cumulativo e exame definitivo dos helpers para encerrar 29 alvos. Este módulo não prova densidade no gráfico de F, reconstrução por J, inclusão inversa de comutantes, álgebra de Hilbert completa ou KMS/traço. Nenhuma integração, execução de monólito/recorder ou promoção de flag faz parte deste estrato. O marcador de conclusão conjunta fica reservado ao parecer cumulativo.
'''
atomic(REPORT, text.encode('utf-8'))
evidence = {'report': str(REPORT), 'report_sha256': sha(REPORT), 'timestamp': now,
            'status': 'PARTIAL_1_MODULE_8_TARGETS_COMPLETE__FULL_29_PENDING',
            'findings': [], 'dependency_origins': dict(origins),
            'compilation_sha256': sha(RUN / 'compilation.json'),
            'manifest_sha256': sha(RUN / 'manifest.json')}
atomic(RUN / 'partial_review_pin.json', (json.dumps(evidence, indent=2, ensure_ascii=False)+'\n').encode('utf-8'))
print(json.dumps(evidence, ensure_ascii=False))
