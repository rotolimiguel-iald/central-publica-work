"""Pin compiled development proofs without promoting them to reviewed integration."""
from pathlib import Path
import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
MODULES = ['ScalarGNSOrbit', 'ScalarGNSLinear', 'ScalarGNSAction']
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, raw):
    assert p.resolve().is_relative_to(ROOT)
    if p.exists():
        before = p.read_bytes()
        b = p.with_name(p.name + '.bak_' + STAMP)
        with b.open('xb') as f:
            f.write(before)
        assert b.read_bytes() == before
    t = p.with_name(p.name + '.tmp_' + STAMP)
    with t.open('xb') as f:
        f.write(raw)
    assert t.read_bytes() == raw and len(raw) > 0
    t.replace(p)
    assert p.read_bytes() == raw


records = {}
targets = {}
for name in MODULES:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    matches = []
    for log in (ROOT / 'logs').glob(name + '_*.json'):
        row = json.loads(log.read_bytes())
        if row['sha256'] == sha(source) and row['returncode'] == 0:
            matches.append((log, row))
    assert matches, name
    log, row = sorted(matches, key=lambda pair: pair[1]['timestamp'])[-1]
    assert row['source_unchanged_during_compile']
    assert row['output_sha256'] == sha(ROOT / 'build/TGLV350' / (name + '.olean'))
    output = Path(row['stdout']).read_text(encoding='utf-8')
    names = re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)
    for target in names:
        full = 'TGLV350.Regular.' + target
        m = re.search(re.escape("'" + full + "' depends on axioms:") + r'\s*\[([^\]]*)\]', output)
        assert m, full
        axioms = {s.strip() for s in m.group(1).split(',')}
        assert axioms <= {'propext', 'Classical.choice', 'Quot.sound'}, (full, axioms)
        targets[full] = sorted(axioms)
    records[name] = {'log': str(log), **row}
assert len(targets) == 14
base = json.loads((ROOT / 'modular_domain_custody.json').read_bytes())
assert sha(ROOT / 'um.py') == base['working_sha256']
note = """# Inscrição GNS e ação ambiente — desenvolvimento

[REAL — Lean local, ainda sem revisão independente nem integração]
Três módulos e 14 alvos, com hashes e logs em gns_draft_status.json.
A custódia integrada continua modular_domain_custody.json. Esta nota não
amplia o escopo do pacote integrado ou de seus pareceres.

ScalarGNSOrbit mostra que a órbita s↦θ_s(A)η pertence a L² para A no ideal
esquerdo I de quadrados uniformemente limitados da forma dual. O fator
Haar c=(2π)⁻¹ é estritamente positivo; a prova remove esse fator da integral
sem converter infinito em zero. O vetor é
Λ_ν(A)=sqrt(c)·[s↦θ_s(A)η] no Hilbert ambiente L²(ℝ,L²(ℝ,H)).
Sua norma satisfaz exatamente ofReal(||Λ_ν(A)||²)=q_(A*A)(η).

ScalarGNSLinear prova a representação quase em toda parte, aditividade,
homogeneidade complexa e define uma aplicação linear I→L². A fidelidade
já provada de q no vácuo implica Λ_ν(A)=0↔A=0; a aplicação é injetiva.
As coerções são da mesma torre P; não se assume um funcional externo.

ScalarGNSAction define L_B como o campo s↦θ_s(B), um operador limitado no
Hilbert ambiente, com ||L_B||≤||B||. Para B∈N e A∈I, BA∈I e
L_B Λ_ν(A)=Λ_ν(BA). É a compatibilidade efetiva entre multiplicação e leitura
no domínio. Ainda não se empacotou uma representação por *-homomorfismo
sobre o completamento da imagem; a ação ambiente não é por si esse pacote.

[OPEN — próximos passos matemáticos]
Construir o fecho da imagem como Hilbert GNS e restringir a ação, com leis
de *-representação. A aproximação forte junto aos adjuntos A_h→A já provada
em N NÃO demonstra convergência na norma ν nem propriedade de core em norma
de grafo para Tomita. É necessário provar densidade de Λ_ν(I∩I*) no espaço
GNS e fechar o operador Λ_ν(A)↦Λ_ν(A*), antes da identificação modular/KMS.

Uma rota a testar, não um resultado: a cota uniforme de q_(A*A) pode controlar
a mudança de η para Λ_tη na multiplicação à direita por Λ_t, e a fase dual
pode ser controlada por convergência dominada na órbita L². Isso daria
continuidade na norma ν para a aproximação à direita; o lado esquerdo usa
a ação ambiente limitada. Essas estimativas ainda não foram provadas.

Permanecem o gerador afiliado, a perturbação e o traço canônico com escala,
a interface geral de peso operatorial/predual, Three Locks/H1, H2/H3 na
mesma geometria, setor quântico interagente/BRST/QME/anomalias/UV, certificado
completo consumido e runtime integral isolado. Nenhuma flag maior mudou.
Os logs de todas as tentativas permanecem, inclusive erros de elaboração e
limites de heartbeats. Somente logs finais rc0 com fontes/binários conferidos
são aceitos neste status. Original não importado ou executado.
"""
save(ROOT / 'ROTA_GNS_RASCUNHO.md', note.encode('utf-8'))
result = {
    'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'status': 'DEVELOPMENT_COMPILED__NOT_INTEGRATED__NOT_INDEPENDENTLY_REVIEWED',
    'records': records, 'targets': targets,
    'integrated_custody': 'modular_domain_custody.json',
    'integrated_custody_sha256': sha(ROOT / 'modular_domain_custody.json'),
    'working_sha256': base['working_sha256'],
    'draft_note_sha256': sha(ROOT / 'ROTA_GNS_RASCUNHO.md'),
    'full_runtime': False, 'canonical_trace_constructed': False,
    'GNS_completed_representation_constructed': False,
    'Tomita_operator_constructed_for_scalar_weight': False,
    'KMS_proved': False, 'full_goal_complete': False,
}
save(ROOT / 'gns_draft_status.json', json.dumps(result, ensure_ascii=False, indent=2).encode())
print(json.dumps({'development_modules': len(records), 'development_targets': len(targets),
                  'integrated': False, 'independently_reviewed': False}))
