from pathlib import Path
import datetime, hashlib, json, os

REV = Path(__file__).resolve().parent
ROOT = REV.parent
RUN = Path((REV / 'adjoint_polar_first_latest_run.txt').read_text().strip())
load = lambda p: json.loads(Path(p).read_bytes())
hf = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
m = load(RUN / 'manifest.json')
c = load(RUN / 'compilation.json')
assert c['complete'] and all(x is True for x in c.values() if isinstance(x, bool))
src = m['sources']['TGLV350/ScalarTomitaAdjointPolar.lean']
assert hf(src['path']) == hf(src['snapshot']) == src['sha256']
assert hf(src['author_binary']) == c['records'][0]['output_sha256']
assert all(hf(p) == h for p, h in m['artifacts_readonly'].items())
assert set(c['records'][-1]['axioms']) == set(m['declarations'])
assert len(m['declarations']) == 10
assert all(set(a) == {'propext', 'Classical.choice', 'Quot.sound'} for a in c['records'][-1]['axioms'].values())
history = load(RUN / 'author_history.json')
failed = [x for x in history if x['returncode'] != 0]
date = datetime.datetime.now().astimezone().isoformat(timespec='seconds')

def link(label, p):
    return f'[{label}](<{Path(p).as_posix()}>)'

origins = '\n'.join(f'- `{p}` — manifesto `{d["manifest_sha256"]}`, compilação `{d["compilation_sha256"]}`.' for p, d in m['origins'].items())
targets = '\n'.join('- `' + n + '`.' for n in m['declarations'])
text = f'''# Revisão DEV — adjunto polar e transporte de gráficos

{date} — **ESTRATO PARCIAL: somente ScalarTomitaAdjointPolar, 1 módulo/10 alvos.**

[REAL — leitura integral, recompilação independente e auditor próprio] **Nenhum achado P0, P1 ou P2 neste primeiro módulo.** A consulta matemática anterior não foi usada como prova. O segundo módulo `ScalarRightConjugateGraph` e o manifesto conjunto aguardam aviso de fonte final; não foram congelados, lidos ou compilados nesta rodada. **Sem veredito ou marcador final do pacote.**

Escopo semântico conferido, em `kernel/TGLV350/ScalarTomitaAdjointPolar.lean`:

- **Linhas14–39:** `D(F) = J⁻¹ D(B)` em ambas as direções. A ida aplica `generic_adjoint_maximal` ao B auto-adjunto efetivo; a volta aplica a maximalidade do F já existente. O teste é em todo D(B)/D(S), usando as inclusões já provadas. Nenhuma hipótese de domínio total, inversa limitada ou novo adjunto é acrescentada.
- **Linhas41–69:** os subtipos transportam Jy ao domínio correto, e `F y = B(Jy)` decorre do pareamento na convenção local ⟨Sx,y⟩=⟨Fy,x⟩ e da densidade de D(S). B continua `scalarTomitaPositiveRoot P` e J continua `scalarTomitaPolarFactor P`.
- **Linhas71–106:** `F=JSJ` e `S=JFJ` conservam os domínios originais, com a involutividade efetivamente herdada de J. As igualdades entre entradas de subtipo identificam os mesmos vetores, sem trocar representações.
- **Linhas108–125:** J×J envia exatamente graph S sobre graph F, nos dois sentidos. A surjetividade é explícita pelo domínio conjugado. Este enunciado ainda não é o transporte do fecho do core direito, que pertence ao segundo módulo.

A dependência `TGLExt/GenericAntilinearAdjoint.lean` foi relida integralmente. `generic_adjoint_pairing` (linha114) usa o adjunto formal derivado de auto-adjunção; `generic_adjoint_maximal` (linha126) usa **o adjunto máximo Mathlib**, sua pertinência de domínio e `LinearPMap.isSelfAdjoint_def`. A prova genérica recebe involutividade de J, mas a aplicação concreta fornece `scalarTomitaPolarFactor_involutive P`, já provada. Não foi encontrada circularidade: a identidade nova F=BJ não é premissa dos resultados anteriores sobre S†S, B ou J. Os tipos impressos deixam somente P e os vetores/domínios indicados; não surge hipótese residual.

| Evidência | Resultado |
|---|---|
| Recompilação própria do módulo | rc0, {c['records'][0]['seconds']} s, sem warnings |
| Auditor próprio `#check` com universos e `#print axioms` | rc0, {c['records'][1]['seconds']} s, exatamente10 alvos, sem warnings |
| Binário | Próprio = autoral, byte a byte |
| Dependências de projeto | {len(m['dependencies'])} congeladas a partir de árvores próprias; não recompiladas |
| Pacotes externos | Oito caminhos readonly; {len(m['external_direct_pins'])} pins diretos herdados e reconferidos |
| LEAN_PATH | Build desta árvore + pacotes externos; nenhum build de projeto autoral |

Proveniência das árvores próprias reutilizadas:

{origins}

`GenericAntilinearAdjoint` veio da árvore própria da involução polar; seu registro de compilação anterior foi herdado, não é uma nova recompilação nesta rodada. Os pins de dependências e companions, fontes/binários autorais, log final/streams e artefatos readonly foram reconferidos ao terminar.

Pins lidos nesta reprodução:

- Fonte: `{src['sha256']}`.
- Binário autoral e próprio: `{src['author_binary_sha256']}`.
- Log final `{Path(src['author_log']).name}`: `{src['author_log_sha256']}`.
- Stdout autoral final: `{src['author_stdout_sha256']}`.
- Manifesto próprio: `{hf(RUN / 'manifest.json')}`.
- Compilação própria: `{hf(RUN / 'compilation.json')}`.

Histórico: **{len(failed)} tentativa autoral rc1 excluída**, log `{Path(failed[0]['log']).name}`. O timeout de isDefEq/whnf gerou prints vazios e referências a constantes/provas inválidas; nenhum foi aceito como evidência. O log final rc0 e o auditor próprio imprimem somente o trio. Houve também uma falha própria **de preparação, antes de executar Lean**, por catálogo sem `ScalarTomitaPolarInvolution`; preservada em `adjoint_polar_first_independent_20260913_025247_090820/preparation_failure.json`. A resolução foi adicionar a origem própria já revisada da involução, sem binários autorais nem rebuild de dependências.

Os dez alvos conferidos:

{targets}

{link('Manifesto e proveniência', RUN / 'manifest.json')}; {link('compilação própria completa', RUN / 'compilation.json')}; {link('tipos/universos/axiomas próprios', RUN / 'logs/AdjointPolarFirstAudit.stdout.txt')}; {link('histórico autoral preservado', RUN / 'author_history.json')}.

[OPEN] Inclusão inversa dos comutantes, estimativa/reconstrução dos quadrados, KMS e traço não decorrem destas identidades de domínio/polar. Nenhum novo J, raiz, gate ou memória foi criado. Integração não revista neste estrato. Só há escritas em `revisao/`; fontes do autor, monólito, custódias e pareceres anteriores permanecem intactos. **Pendente somente para completar este pacote: segundo módulo final e manifesto conjunto.**
'''

p = REV / 'REVIEW_ADJOINT_POLAR_GRAPH_DEV.md'
assert not p.exists()
raw = text.encode()
tmp = p.with_name(p.name + '.tmp')
with tmp.open('xb') as f:
    f.write(raw)
assert tmp.read_bytes() == raw
os.replace(tmp, p)
assert p.read_bytes() == raw
pin = {'timestamp': date, 'report': str(p), 'report_sha256': hf(p), 'status': 'PARTIAL_FIRST_MODULE_10_TARGETS',
       'compilation_sha256': hf(RUN / 'compilation.json'), 'P0': [], 'P1': [], 'P2': [], 'final_package_marker': False}
q = RUN / 'partial_review_pin.json'
assert not q.exists()
qr = (json.dumps(pin, ensure_ascii=False, indent=2) + '\n').encode()
qt = q.with_name(q.name + '.tmp')
with qt.open('xb') as f:
    f.write(qr)
assert qt.read_bytes() == qr
os.replace(qt, q)
print(json.dumps(pin, ensure_ascii=False))
