# -*- coding: utf-8 -*-
"""R2.2: TESTES_R2_2.md gerado dos JSON em disco (suíte inteira na cópia R2.2, testes novos na cópia R2.1, ensaio)."""
import hashlib
import json
from pathlib import Path

R22 = Path(__file__).resolve().parents[1]
full = json.loads((R22 / 'copia' / 'testes_r2' / 'RESULTADOS_TESTES.json').read_text(encoding='utf-8'))
antes = json.loads((R22 / 'copia_r2_1' / 'testes_r2' / 'RESULTADOS_TESTES_parcial.json').read_text(encoding='utf-8'))
ens_p = R22 / 'runs' / 's5_ensaio_r2_2.json'
ens = json.loads(ens_p.read_text(encoding='utf-8'))


def sha16(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


DESC = {
    'test_T_K4c_target_modified_after_check_is_failure_and_lock_still_pending': ('K4c', 'alvo com bytes do candidato depois de conferir_alvos OK: status FALHOU_EM_*, ok=false, sem religar, ação preenchida, trava ainda vê a implantação pendente'),
    'test_T_K4c_misleading_reverted_receipt_does_not_release_lock': ('K4c', 'um RECIBO_REVERSAO REVERTIDA com app_religado=false não libera a trava'),
    'test_T_K4c_clean_reversal_still_releases_lock': ('K4c', 'controle: reversão boa dá REVERTIDA, ok, app_religado true, ação null, trava libera'),
    'test_T_K4b_target_locked_after_check_fills_action': ('K4b', 'lock EXCLUSIVO num alvo depois de conferir_alvos OK: ação preenchida (nunca null), sem religar, trava pendente'),
    'test_T_K4b2_sem_reiniciar_is_explicit_status_with_action': ('K4b', '--sem-reiniciar: REVERTIDA_SEM_RELIGAR com a ação manual'),
    'test_T_K3r_reverter_cannot_stop_app': ('K3r', 'o REVERTER não consegue parar o app: nada restaurado, tarefa reabilitada, recibo com estado lido (vivo sem supervisor), nunca «fica parado»'),
    'test_T_K3r_task_disabled_by_operator_stays_disabled': ('K3r', 'controle: tarefa desabilitada pelo operador segue desabilitada'),
    'test_T_P8b_crash_loop_is_distinguished_in_receipt_and_output': ('P8b', 'filho web com pid trocando: rc 3, LACO_DE_QUEDA_PROVAVEL no recibo e na saída, COMO DISTINGUIR'),
    'test_T_P8b_child_never_up_is_crash_loop': ('P8b', 'filho web nunca de pé com supervisor vivo: rc 3, LACO_DE_QUEDA_PROVAVEL (forma achada no ensaio)'),
    'test_T_P8b_slow_but_stable_is_read_as_slow': ('P8b', 'pid estável: rc 3, LENTO_PROVAVEL, «NÃO reverter»'),
    'test_G_N1c_path_reason_16000_components_refused_fast': ('N1', 'path_reason com 16.000 componentes: path_too_many_components em < 50 ms'),
    'test_G_N1c_read_allowed_file_16000_components_refused_fast': ('N1', 'read_allowed_file com 16.000 componentes: recusa visível em < 50 ms'),
    'test_G_N1c_dispatch_init_16000_components_refused_fast': ('N1', 'dispatch init com 16.000 componentes: recusa visível em < 50 ms'),
    'test_G_N1c_too_long_refused': ('N1', 'caminho de 40.000 caracteres: path_too_long (a R2.1 levantava ValueError do stat)'),
    'test_G_N1c_ordinary_deep_path_not_refused_by_shape': ('N1', 'controle: 40 componentes benignos não são recusados'),
    'test_M_DOC_tools_field_cites_real_sha': ('doc', 'campo ferramentas do manifesto cita o sha256 real do aplicar_blocos.py'),
    'test_A_N3_hardlink_swap_via_app_never_reads_canary': ('N3 app', 'troca ativa x.json <-> hardlink do psion sintético por 12 s pelo handler real /admin/api/agi/files/read: 0 leituras do canário'),
    'test_A_N1_validate_path_16000_components_refused_fast': ('N1 app', 'agi_validate_path com 16.000 componentes: recusa em < 50 ms'),
    'test_A_OK_benign_read_same_text_as_open': ('N3 app', 'controle: leitura benigna devolve o mesmo texto que open(...,"r") e recusa o psion sintético'),
}

L = ['# TESTES R2.2 — conserto ACOM 12/10 (13/10/2026)', '',
     'Gerado por `scripts/gerar_testes_md.py` a partir dos JSON em disco. Estatutos: [REAL] medido aqui.', '',
     '## 1. Suíte inteira do candidato R2.2 (cópia `copia\\`, guarda da auditoria, sem rede, sem provedor) [REAL]', '',
     '**%d testes, %d PASSA, %d FALHA** (%s): as 259 da R2.1 + %d novos. Bloqueios da guarda: %d (`%s`).'
     % (full['total'], full['passed'], full['failed'], full['at'], full['total'] - 259, full['guard']['n_blocks'],
        ', '.join(sorted({b['kind'] for b in full['guard']['blocks']}))), '',
     '| suíte | rodados | OK | segundos |', '|---|---|---|---|']
for s in full['suites']:
    L.append('| %s | %s | %s | %s |' % (s['suite'], s['ran'], 'sim' if s['ok'] else 'NÃO', s['seconds']))
nov = {t['test']: t['result'] for s in full['suites'] if s['suite'].startswith('R2.2') for t in s['tests']}
ant = {t['test']: t['result'] for s in antes['suites'] for t in s['tests']}
L += ['', '## 2. Os testes novos: antes (cópia `copia_r2_1`: candidato e ferramentas R2.1) × depois (R2.2) [REAL]', '',
      'Antes: %d de %d FALHAM na R2.1 (os que passam são controles). Depois: %d de %d PASSAM.'
      % (sum(v == 'FALHA' for v in ant.values()), len(ant), sum(v == 'PASSA' for v in nov.values()), len(nov)), '',
      '| achado | teste | o que reproduz | R2.1 | R2.2 |', '|---|---|---|---|---|']
for t in sorted(nov, key=lambda k: (DESC.get(k, ('z', ''))[0], k)):
    a, d = DESC.get(t, ('?', ''))
    L.append('| %s | `%s` | %s | %s | %s |' % (a, t, d, ant.get(t, '—'), nov[t]))
L += ['', 'Rodada da R2.1: `copia_r2_1/testes_r2/RESULTADOS_TESTES_parcial.json` (%s).' % antes['at'], '',
      '## 3. Ensaio de implantação e reversão (backend de processos SIMULADO, banco v1 sintético, guarda ligada) [REAL]', '',
      'Arquivo `runs/s5_ensaio_r2_2.json` (sha16 `%s`), ferramentas R2.2 copiadas byte a byte (preparo: %s).'
      % (sha16(ens_p), json.dumps({k: v for k, v in ens['preparo'].items() if k in ('implantar.py', 'reverter.py', 'implantacao_lib.py')})), '',
      '| cenário | resultado principal | originais idênticos no fim | banco = original | lib v1 lê | tmp órfão |', '|---|---|---|---|---|---|']
for n, r in ens['resumo'].items():
    princ = {k: v for k, v in r.items() if k not in ('originais_identicos', 'extras_estranhos', 'banco_igual_ao_original',
                                                     'lib_le_o_banco_rc', 'schema_final', 'tmp_orfaos_final', 'sim_final', 'acao')}
    txt = json.dumps(princ, ensure_ascii=False)
    txt = txt.replace('|', '/')[:420]
    L.append('| %s | %s | %s | %s | %s | %s |' % (n, txt, r.get('originais_identicos'), r.get('banco_igual_ao_original'),
                                                   r.get('lib_le_o_banco_rc') == 0, len(r.get('tmp_orfaos_final') or [])))
L += ['', 'Leitura [REAL, dos JSON]:', '',
      '- «tmp órfão» conta os tempários de uma troca interrompida pela morte do processo (K1a/K1b2), que o reverter '
      'RENOMEOU para `.removido_` (nunca apaga); nenhum `.tmp_` solto ficou.',
      '- K2b/K2c/K2d terminam com o estado misto porque o cenário do revisor só tenta `reverter --config` depois de o '
      'operador renomear, apagar ou truncar o recibo: a trava não vê o recibo renomeado/apagado e recusa o truncado; a '
      '2ª execução do implantar falha fechada sem tocar em nada. É a regra «nunca renomear, apagar ou editar recibo» '
      '(RUNBOOK §6); igual à R2.1 (revisão R2.1 §4).',
      '- P8: a reversão de limpeza do ensaio também encontra a saúde atrasada (o simulador mantém o atraso de 8 s e o '
      'prazo de 3 s) e termina REVERTIDA_AGUARDANDO_REINICIO, com a ação preenchida.',
      '- A 1ª rodada completa do ensaio (`runs/s5_ensaio_r2_2_rodada1_bug_P8b.json`) achou um defeito da própria R2.2: '
      'no P8b com o filho web que nunca fica de pé, o texto do diagnóstico levantava UnboundLocalError e a implantação '
      'verificada saía como falha (rc 1). Corrigido (ramo do texto e proteção: o texto nunca transforma implantação '
      'verificada em falha), com o teste `test_T_P8b_child_never_up_is_crash_loop`; a rodada acima é a 2ª, completa.']
(R22 / 'TESTES_R2_2.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print('TESTES_R2_2.md', sha16(R22 / 'TESTES_R2_2.md'))
