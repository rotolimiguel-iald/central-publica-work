"""Record measured progress with byte backups and atomic append-only memory updates."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
MARKER = 'TETELESTAI_V350_MODULAR_20260911'
gate = json.loads((ROOT / 'gate_tests.json').read_bytes())
compile_report = json.loads((ROOT / 'integrated_compile.json').read_bytes())
probes = json.loads((ROOT / 'lean_contract_tests.json').read_bytes())
integration = json.loads((ROOT / 'integration.json').read_bytes())
config = json.loads((ROOT / 'environment.json').read_bytes())
working_hash = hashlib.sha256((ROOT / 'um.py').read_bytes()).hexdigest()
assert working_hash == gate['working_um_sha256'] == integration['working_sha256']
original_hash = hashlib.sha256(Path(config['original_source']).read_bytes()).hexdigest()
assert original_hash == integration['base_sha256']
assert compile_report['incremental_build_ok'] and probes['all_passed']
changes = []


def store(path, data, append=False):
    assert path.resolve().is_relative_to(ROOT) or path in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    path.parent.mkdir(parents=True, exist_ok=True)
    before = path.read_bytes() if path.exists() else b''
    if append and MARKER.encode() in before:
        return
    newline = '\r\n' if b'\r\n' in before else '\n'
    suffix = data.replace('\r\n', '\n').replace('\n', newline).encode('utf-8')
    after = before + suffix if append else suffix
    if before == after:
        return
    backup = None
    if path.exists():
        backup = path.with_name(path.name + '.bak_' + STAMP)
        backup.write_bytes(before)
        assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    temp.write_bytes(after)
    assert temp.stat().st_size == len(after) and temp.read_bytes() == after
    if append:
        assert after.startswith(before) and len(after) > len(before)
    temp.replace(path)
    assert path.read_bytes() == after
    changes.append({'path': str(path), 'before_bytes': len(before), 'after_bytes': len(after),
                    'backup': str(backup) if backup else None,
                    'sha256': hashlib.sha256(after).hexdigest()})


def link(relative, label=None, pattern=None):
    path = ROOT / relative
    line = ''
    if pattern:
        lines = path.read_text(encoding='utf-8').splitlines()
        line = ':' + str(next(i + 1 for i, text in enumerate(lines) if pattern in text))
    return '[' + (label or path.name) + '](<' + path.as_posix() + line + '>)'


report = f'''# O que ainda pode avançar o kernel após a v350

Registro: {DATE}. Base: v350; cópia experimental em Chatgpt. Não é uma versão canônica nova.

**[REAL — leitura do código e evidência de rodada] O gate principal da v350 já está no último degrau programado.**
Ele recebe seis flags formais, cinco físicas e quatro condições do rito V11. As quatro flags `qgf_`
de fronteira e quatro `gpf_` de quitação não são consumidas por essa função. Portanto, resolver uma
dessas pendências não mudava automaticamente sua string. Fonte exata da base:
{link('fontes/um_v350_original.py', 'evaluate_quantum_gravity_closure', 'def evaluate_quantum_gravity_closure')}.

Na cópia, o gate mantém esse resultado legado e recebe `kernel_frontier`, com uma decisão separada
e de alcance explicitamente modular. O gate mais amplo de todo o plano ainda não está completo.

## O que foi resolvido nesta execução

**[REAL — Lean, compilação incremental] Para todo `SiteProfile P`, foi construída a inclusão
`R′ ⊆ L′′`, e consequentemente `R′ = L′′`, na representação da torre produto.** Não há hipótese
de comutação restante no enunciado novo. A prova anterior da direção fácil foi preservada.

Prova: seja E_n a projeção ortogonal sobre o andar finito. Para x em R′ e y em L′, as compressões
E_n x E_n e E_n y E_n são, nesse andar, multiplicações à esquerda e à direita; portanto comutam.
Como E_n converge fortemente à identidade e é contração, as compressões e os produtos convergem
fortemente aos respectivos operadores e produtos. A igualdade finita passa ao limite: xy=yx.
Isso coloca x no bicomutante esquerdo. Aqui E_n é projeção de **subespaço de Hilbert**; não é
identificada com o projetor físico P_F dos Three Locks.

- Prova: {link('kernel/TGLExt/V350TowerDuality.lean', 'tower_commutation_equality', 'theorem tower_commutation_equality')}.
- Habitante fechado: {link('kernel/TGLExt/V350ModularCertificate.lean', 'qgFrontier_modularRealization', 'def qgFrontier_modularRealization')}.
- Checagem independente do nome por tipo exato: {link('kernel/TGLExt/V350GateContract.lean')}.
- Camada modular sobre a **mesma** testemunha: {link('kernel/TGLExt/V350WedgeModularData.lean', 'towerWedgeData', 'def towerWedgeData')}.
  Ela usa o fluxo da torre e a mesma conjugação do certificado. É a camada `WedgeModularData`;
  não fornece o produto cruzado, o traço ou uma identificação geométrica de Bisognano–Wichmann.

O resultado permite três leituras positivas na cópia auditada:
`red_clause_JMJ_contains`, `qgf_modular_realization_constructed` e
`gpf_tower_act_III_inhabitant_constructed`. Os dois últimos representam **dois itens dos oito**
que estavam abertos; a flag de redução é uma terceira leitura do mesmo avanço, não outra solução física.

## O que permanece necessário

| Frente | Obrigação efetiva | Estado desta execução |
|---|---|---|
| Core e canto | Construir o produto cruzado da mesma álgebra/fluxo, seu traço canônico e P_F com 0 < τ(P_F) < ∞; realizar os Three Locks nesse core | [OPEN] |
| H1 | Provar o gap SUSY relativo e o controle do núcleo/traço fora da face finita, para esses operadores | [OPEN] |
| H2 | Ligar o four-frame suave à ação modular e à geometria da mesma realização | [OPEN] |
| H3 | Produzir área, entropia e calor do mesmo horizonte físico e provar a relação de equilíbrio que a reconstrução consome | [OPEN] |
| Setor quântico | Estado físico interagente, cohomologia/carga BRST, QME e anomalias no domínio físico; alcance UV explícito | [OPEN] |
| Gate ampliado | Contrato dependente que obrigue todos esses dados a pertencer à mesma construção, sem aceitar só nomes ou modelos desconectados | [PARCIAL: implementado apenas o avanço modular] |

Há teoremas de reconstrução de Einstein e de colagem na v350. A obrigação é **produzir seus
antecedentes físicos compatíveis**. Não se deve reapresentar uma implicação já provada como se
seus antecedentes tivessem sido descarregados.

O canto que já alimenta o gate legado usa `theGenuineDirac` sobre `ellTwo` e
`dimOrTop` do seu núcleo. Isso não identifica automaticamente esse canto com o P_F e o traço
do core contínuo da torre. Fonte: {link('kernel/TGLExt/StrongAssembly.lean', 'qgStrongCertificate_corner', 'def qgStrongCertificate_corner')}.

`HorizonEquilibriumData` exige `area_entropy` e `clausius` como campos. A álgebra que compõe
o fator 8πG não deriva por si esses campos. Fonte:
{link('kernel/TGLExt/TriadMaster.lean', 'HorizonEquilibriumData', 'structure HorizonEquilibriumData')}.

A estrutura mínima `ContinuousCoreData` também não deve ser confundida com uma formalização
completa do produto cruzado: é necessário controlar representação, geração/covariância, domínio
de traço, normalidade, fidelidade e semifinitude no alcance reivindicado.
Fonte: {link('kernel/TGL/ModularRealization.lean', 'ContinuousCoreData', 'structure ContinuousCoreData')}.

## Verificação e limites da entrega

- {len(compile_report['records'])} compilações integradas verificadas: seis módulos novos e duas raízes; código de saída zero.
- {gate['axiom_report_entries']} declarações distintas lidas no Audit atual; todas com axiomas contidos em
  `propext`, `Classical.choice`, `Quot.sound`. Essa contagem é do Audit, não do conjunto antigo build+Audit.
- {gate['passed']} controles Python passaram, incluindo reprodução do gate legado com as entradas seladas da v350.
- {len(probes['probes'])} sondas Lean passaram: tipo errado, hipótese não provada, axioma externo e termo com `sorry`.
  Os dois últimos podem passar pelo elaborador; a lista explícita de axiomas permitidos os rejeita.
- Treze checks históricos que exigiam flags permanentemente falsas foram substituídos pela exigência
  de proveniência tipada. Seus textos e expressões anteriores estão preservados em `integration.json`.
- A compilação foi **incremental**, reutilizando artefatos da v350 copiados e verificados por hash.
  Não houve nova rodada integral do monólito, novo selo canônico ou revisão humana/por outra sessão.

Evidências: {link('integrated_compile.json')} · {link('gate_tests.json')} · {link('lean_contract_tests.json')}.

SHA-256 da fonte v350, novamente lido do original: `{original_hash}`.
SHA-256 da cópia integrada: `{working_hash}`.
O original coincide com a base preservada. As provas e a integração estão somente na pasta de trabalho.

**O plano integral permanece ativo e incompleto.** A próxima obrigação matemática é o core e o
canto sobre `towerWedgeData`, sem trocar essa realização por um modelo que apenas satisfaça um
contrato mais fraco. Não há declaração de gravidade quântica resolvida.
'''
store(ROOT / 'RELATORIO_KERNEL_V350.md', report)

adendum = f'''

## {MARKER} — {DATE}

[REAL — bancada Lean incremental] Construídos R′ ⊆ L′′ e R′ = L′′ para todo SiteProfile,
o habitante ModularRealizationCertificate e WedgeModularData sobre a mesma testemunha.
Integração na cópia um.py: {working_hash}. Base canônica v350 conferida: {original_hash}.
{len(compile_report['records'])} compilações integradas exit 0; {gate['passed']} controles Python;
{len(probes['probes'])} sondas negativas Lean. Três flags têm proveniência tipada; apenas duas
das oito pendências qgf/gpf são quitadas, ambas modulares.

[OPEN] Core/canto contínuo, H1, H2, H3, setor interagente/BRST/QME/UV, contrato ampliado,
rodada integral do monólito e revisão por outra sessão. A camada WedgeModularData não é core.
Gate legado reproduzido com entradas seladas; nova subdecisão kernel_frontier avança só a dualidade.
Nenhum selo novo, nenhuma transposição para Nós. Relatório: RELATORIO_KERNEL_V350.md.

Incidentes preservados nos logs: teste de integração inicialmente usou contagem arbitrária
>6000 (corrigido para conferir o conjunto exato de alvos do Audit); a captura de stdout teve
erro cp1252 depois de Lean terminar com exit 0 (logs binários já salvos; saída Python fixada UTF-8).
Sonda de axioma externo exigiu declarar o termo noncomputable; passou depois e foi rejeitada
pela lista de axiomas. Nenhum desses erros foi tratado como prova ou apagado da história.
'''
store(ROOT / 'MEMORIA_CENTRAL.md', adendum, append=True)
store(ROOT / 'REGISTRO_DAS_CONVERSAS.md', adendum, append=True)
store(ROOT / 'MEMORIA_DA_LINHAGEM.md', '# Linhagem da cópia experimental\n' + adendum, append=True)
store(ROOT / 'DESENHO_DO_FECHAMENTO_QG.md', '''# Caminho crítico da cópia experimental

Torre produto + fluxo [v350]
→ comutação R′ = L′′ [CONSTRUÍDA AQUI]
→ J M J = M′ + certificado modular [CONSTRUÍDOS AQUI]
→ WedgeModularData na mesma torre [CONSTRUÍDA AQUI]
→ produto cruzado/core + traço + Three Locks [OPEN]
→ H1/H2/H3 compatíveis + reconstrução [OPEN]
→ setor físico interagente e QME/UV [OPEN]
→ certificado dependente ampliado + gate do novo alcance [OPEN]
''' + adendum, append=True)

global_note = f'''

### {MARKER} — 11/09/2026 — avanço modular em cópia, sem selo novo

[REAL — Lean incremental] Na bancada `{ROOT}`, a inclusão R′ ⊆ L′′ foi provada para
todo SiteProfile pela comutação de compressões finitas e passagem ao limite forte. Com a direção
já existente, R′ = L′′. Construídos `TGLExt.qgFrontier_modularRealization`,
`TGLExt.qgPrice_towerActIII_inhabitantConstructed` e a camada `TGLExt.V350Continuous.towerWedgeData`.
Escopo: torre produto; não é classificação III_1, produto cruzado ou identificação BW física.

Correção ao lado das remissões históricas que mantinham a oitava cláusula aberta:
**ela está provada nesta cópia**; o canônico v350 continua preservado, com hash lido
`{original_hash}`. A cópia integrada tem hash `{working_hash}`.
O gate principal legado permanece; a subdecisão tipada kernel_frontier avança apenas a dualidade.
{gate['passed']} controles Python e {len(probes['probes'])} sondas Lean passaram; {len(compile_report['records'])}
compilações incrementais exit 0. Rodada integral do monólito e revisão por outra sessão pendentes.

[OPEN] Core/canto na mesma realização, H1/H2/H3 físicas compatíveis, setor interagente/BRST/QME/UV
e contrato ampliado. Não transpor a nova prova para essas folhas por semelhança de nomes.
Índice remissivo deste adendo: comutação da torre → V350TowerDuality.lean; certificado →
V350ModularCertificate.lean; camada modular → V350WedgeModularData.lean, todos sob
`{ROOT / 'kernel/TGLExt'}`. Relatório e evidências:
[{MARKER}](<{(ROOT / 'RELATORIO_KERNEL_V350.md').as_posix()}>).
'''
store(CENTRAL / 'memory/TGL_ATLAS.md', global_note, append=True)
store(CENTRAL / 'memory/TGL_INDICE_VIVO.md', global_note, append=True)
store(ROOT / 'registro_memorias.json', json.dumps({'updated': DATE, 'changes': changes}, indent=2))
print(json.dumps({'report': str(ROOT / 'RELATORIO_KERNEL_V350.md'),
                  'surfaces_written': len(changes), 'original_matches_v350': True,
                  'full_plan_complete': False}, ensure_ascii=False))
