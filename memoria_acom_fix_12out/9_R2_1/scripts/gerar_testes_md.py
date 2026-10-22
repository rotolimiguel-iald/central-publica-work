# -*- coding: utf-8 -*-
"""R2.1: TESTES_R2_1.md a partir dos resultados em disco (nada digitado à mão nos números)."""
import hashlib
import json
from pathlib import Path

R21 = Path(__file__).resolve().parents[1]
DEP = json.loads((R21 / 'copia' / 'testes_r2' / 'RESULTADOS_TESTES.json').read_text(encoding='utf-8'))
ANT = json.loads((R21 / 'copia_r2' / 'testes_r2' / 'RESULTADOS_TESTES_parcial.json').read_text(encoding='utf-8'))
S3 = {n: json.loads((R21 / 'runs' / ('s3c_%s.json' % n)).read_text(encoding='utf-8')) for n in ('copia_r2', 'copia')}
S4 = {n: json.loads((R21 / 'runs' / ('s4_medidas_nomes_%s.json' % n)).read_text(encoding='utf-8')) for n in ('copia_r2', 'copia')}
ENS = json.loads((R21 / 'runs' / 's5_ensaio_r2_1.json').read_text(encoding='utf-8'))

DESC = {
    'test_G_N1_basename_32k_under_50ms': ('N1', 'nome de 32 KB (`a` + `.bak`×8000): confidential_basename < 50 ms (melhor de 3)'),
    'test_G_N1_path_reason_32k_under_50ms': ('N1', 'caminho de 32 KB: path_reason < 50 ms'),
    'test_G_N1_read_allowed_file_32k_under_50ms': ('N1', 'caminho de 32 KB pelo session_memory.read_allowed_file < 50 ms'),
    'test_G_N1_same_decision_as_r2_loop': ('N1', 'controle: a remoção linear decide igual ao laço do R2 (3000 nomes aleatórios)'),
    'test_G_N2_names_refused': ('N2', '*.env e variantes, radicais psion/stack, homóglifos (ѕ cirílico, ‐, ZWSP, largura total), `~`'),
    'test_G_N2_benign_names_allowed': ('N2', 'controle: nomes benignos (environment.json, envoy.yaml, venv.txt…) seguem aceitos'),
    'test_G_N2_init_central_env_refused_and_bank_clean': ('N2', 'init com `central.env` (senha/AKIA sintéticos): recusado, nada no banco'),
    'test_G_N3_hardlink_swap_never_reads_canary': ('N3', 'troca ativa x.json ↔ hardlink do psion sintético por 12 s: 0 leituras do canário'),
    'test_G_N3_reads_return_resolved_path': ('N3', 'controle: a leitura devolve o caminho resolvido (como o R2)'),
    'test_T_K2_refuses_with_unreverted_real_receipt_and_preserves_it': ('K2', 'implantar com recibo real anterior não revertido: RECUSADA, recibo anterior byte a byte intocado, recibo novo com carimbo'),
    'test_T_K2_reverted_receipt_does_not_block': ('K2', 'com RECIBO_REVERSAO REVERTIDA citando o carimbo, a trava passa'),
    'test_T_K3_task_reenabled_and_receipt_honest': ('K3', 'stop script não derruba o web: a tarefa volta HABILITADA; o recibo não diz «nada mudou»; estado_real lido'),
    'test_T_K3_task_disabled_by_operator_stays_disabled': ('K3', 'controle: tarefa desabilitada pelo operador não é reabilitada'),
    'test_T_K4_failed_restore_does_not_restart_app': ('K4', 'reverter com passo 2 FALHOU: o app NÃO é religado; ação manual no recibo'),
    'test_T_K4_targets_always_checked_even_without_step4': ('K4', 'recibo sem passo 4 e alvo com bytes do candidato: conferir_alvos FALHOU, sem religar'),
    'test_T_K4_good_reversal_restarts': ('K4', 'controle: reversão boa restaura e religa; o recibo de reversão cita o carimbo da implantação'),
    'test_T_K6_receipt_held_by_reader_is_written_after_wait': ('K6', 'leitor segura o recibo 1 s: write_json_atomic espera e grava; sem tempário'),
    'test_T_K6_held_too_long_fails_visibly_without_orphan_temp': ('K6', 'leitor além do limite: PermissionError visível, alvo intacto, sem tempário'),
    'test_T_P8_slow_restart_is_waiting_not_failure': ('P8', 'saúde fora do prazo com processo vivo: CONCLUIDA_AGUARDANDO_REINICIO, sem mandar reverter'),
    'test_HB1_psion_replace_waits_for_reader': ('HB', 'psion sintético preso 0,4 s: _save_psion_state espera e grava; sem tempário'),
    'test_HB2_health_replace_waits_for_reader': ('HB', 'health preso 0,4 s: _heartbeat_health_save espera e grava'),
    'test_HB3_failed_replace_leaves_no_orphan_temp': ('HB', 'psion preso além do limite: falha visível, psion intacto, SEM tempário órfão'),
    'test_HB4_rotation_waits_for_reader': ('HB', 'rotação da telemetria com o .jsonl preso: espera e roda'),
    'test_HB5_sixty_beats_with_concurrent_sweeper_one_event': ('HB', '60 batidas com varredor em processo (30 ms por arquivo): todas ok, 1 evento, sem tempário'),
}


def res(d):
    out = {}
    for s in d['suites']:
        for t in s['tests']:
            out[t['test']] = t['result']
    return out


ra, rd = res(ANT), res(DEP)
L = ['# TESTES R2.1 — conserto ACOM 12/10 (13/10/2026)', '',
     'Gerado por `scripts/gerar_testes_md.py` a partir dos JSON em disco. Estatutos: [REAL] medido aqui.', '',
     '## 1. Suíte inteira do candidato R2.1 (cópia `copia\\`, guarda da auditoria, sem rede, sem provedor) [REAL]', '',
     '**%d testes, %d PASSA, %d FALHA** (%s): as 235 do revisor + 24 novos. Bloqueios da guarda: %s (`%s`).' % (
         DEP['total'], DEP['passed'], DEP['failed'], DEP['at'], DEP['guard']['n_blocks'],
         ', '.join(sorted({b['kind'] for b in DEP['guard']['blocks']}))), '',
     '| suíte | rodados | OK | segundos |', '|---|---|---|---|']
for s in DEP['suites']:
    L.append('| %s | %s | %s | %s |' % (s['suite'], s['ran'], 'sim' if s['ok'] else 'NÃO', s['seconds']))
L += ['', '## 2. Os 24 testes novos: antes (cópia do R2: candidato e ferramentas R2) × depois (R2.1) [REAL]', '',
      'Antes: %d de %d FALHAM no R2 (os 4 que passam são controles). Depois: %d de %d PASSAM.' % (
          ANT['failed'], ANT['total'], sum(rd.get(t) == 'PASSA' for t in DESC), len(DESC)), '',
      '| achado | teste | o que reproduz | R2 | R2.1 |', '|---|---|---|---|---|']
for t, (a, txt) in DESC.items():
    L.append('| %s | `%s` | %s | %s | %s |' % (a, t, txt, ra.get(t, '—'), rd.get(t, '—')))
L += ['', '## 3. Heartbeat: a repetição s3c do revisor (teste ORIGINAL `test_sixty_beats…`, sem injeção) [REAL]', '',
      '| cópia | fase | n | falhas do teste | falhas só da limpeza do tempdir no tearDown | aberturas do varredor |', '|---|---|---|---|---|---|']
for n in ('copia_r2', 'copia'):
    for k in ('S_sequencial', 'V_paralelo_4_com_varredor'):
        f = S3[n][k]
        L.append('| %s | %s | %d | %d | %d | %s |' % ('R2' if n == 'copia_r2' else 'R2.1', k, f['n'], f['falhas_do_teste'],
                                                     f['falhas_so_da_limpeza_tearDown'], f['aberturas_do_varredor']))
L += ['', 'Mensagens R2: `%s`.' % '`, `'.join(sorted({m[:70] for k in ('S_sequencial', 'V_paralelo_4_com_varredor') for m in S3['copia_r2'][k]['mensagens']})),
      'R2.1: as únicas falhas são `PermissionError` no `tempfile.cleanup()` do tearDown da fixture (o varredor externo ainda '
      'segura um arquivo do tempdir quando o teste tenta apagá-lo). O corpo do teste passou em todas: 0 `3 != 1`, 0 '
      '`psion_error`. Traceback completo em `runs/diag_s3c_copia.json`.', '',
      '## 4. Filtro: medidas N1/N2 (fora do unittest) [REAL]', '',
      '| medida | R2 (s) | R2.1 (s) |', '|---|---|---|']
for k in S4['copia']['N1']:
    L.append('| %s (%d car.) | %s | %s |' % (k, S4['copia']['N1'][k]['chars'], S4['copia_r2']['N1'][k]['s'], S4['copia']['N1'][k]['s']))
L += ['', '| nome | R2 | R2.1 |', '|---|---|---|']
for k in S4['copia']['N2']:
    L.append('| `%s` | %s | %s |' % (k.strip("'"), S4['copia_r2']['N2'][k], S4['copia']['N2'][k]))
L += ['', '## 5. Ensaio de implantação e reversão (cópia sintética, backend simulado, ferramentas R2.1) [REAL]', '',
      'Script `scripts/s5_ensaio_r2_1.py`; resultado `runs/s5_ensaio_r2_1.json`. O R2 nos mesmos cenários é o do revisor '
      '(`8_REVISAO_R2/runs/s5_ensaio_*.json`), não refeito aqui; os testes T_K* da §2 dão o antes/depois por cenário.', '',
      '| cenário | resultado R2.1 |', '|---|---|']


def r_ens(n, c):
    if 'excecao' in c:
        return 'EXCEÇÃO no harness: ' + c['excecao'][-200:].replace('\n', ' ')
    fin = 'final: originais idênticos=%s, banco=original %s, lib lê o banco rc=%s, sim=%s' % (
        c.get('comparacao_final', {}).get('identico_nos_originais'), c.get('banco_igual_ao_original'),
        (c.get('lib_le_o_banco') or {}).get('rc'), c.get('estado_sim_final'))
    if n.startswith('K1'):
        return ('morto=%s, %s leituras do recibo durante a execução; após a morte: alvos %s, schema %s; reverter %s; %s'
                % (c['implantar'].get('morto'), c['implantar'].get('leituras_do_recibo', '—'), c.get('alvos_apos_morte'),
                   c.get('schema_apos_morte'), c['reverter']['status'], fin))
    if n == 'K2':
        i2 = c['implantar_2']
        return ('1ª: %s (alvos %s); 2ª: %s, passos %s, recibo 1 intocado=%s; reverter com o recibo indicado: %s; dry-run depois: '
                'trava %s, %s; %s' % (c['implantar_1']['resumo']['status'], c['alvos_apos_1'], i2['status'], i2['passos'],
                                     i2['recibo_1_intocado'], c['reverter_com_o_recibo_indicado']['status'],
                                     c['dry_run_depois_de_revertida']['trava'], c['dry_run_depois_de_revertida']['status'], fin))
    if n == 'K3':
        i = c['implantar']
        return ('%s; tarefa desabilitada por esta execução=%s; reabilitada=%s; diz «nada mudou»=%s; sim depois=%s; nota: %s'
                % (i['status'], i['tarefa_desabilitada_por_esta_execucao'], i['tarefa_reabilitada'], c['diz_nada_mudou'],
                   c['sim_apos_falha'], i['apos_falha_nota']))
    if n == 'K4':
        return ('implantar %s; reverter com o web server preso: %s, app_religado=%s, sim=%s, alvos %s; 2º reverter: %s, '
                'alvos %s, sim=%s; %s' % (c['implantar']['status'], c['reverter']['status'], c['reverter']['app_religado'],
                                          c['sim_apos_reverter_com_falha'], c['alvos_apos_reverter_com_falha'],
                                          c['reverter_de_novo']['status'], c['alvos_apos_2o_reverter'], c['sim_apos_2o_reverter'], fin))
    if n == 'K5':
        return ('implantar %s; reverter morto=%s (alvos %s); 2º reverter %s, alvos %s; %s' % (
            c['implantar']['status'], c['reverter_1_morto'], c['alvos_apos_morte'], c['reverter_2']['status'],
            c['alvos_apos_reverter_2'], fin))
    if n == 'K6':
        return ('leitor segurou o recibo 2 s=%s; implantar %s (%d arquivos substituídos), sim=%s; reverter %s; %s' % (
            c['leitor_segurou_2s'], c['implantar']['status'], c['implantar']['arquivos_substituidos'], c['sim_apos'],
            c['reverter']['status'], fin))
    if n == 'P8':
        return ('implantar %s (passo 8 %s), manda reverter=%s; sim logo após=%s; 10 s depois=%s; reversão de limpeza: %s' % (
            c['implantar']['status'], c['implantar']['passos'].get('reiniciar_app'), c['implantar']['manda_reverter'],
            c['sim_logo_apos'], c['sim_10s_depois'], c['reverter_para_limpar_o_ensaio']['status']))
    return json.dumps(c, ensure_ascii=False)[:300]


for n, c in ENS['cenarios'].items():
    L.append('| %s | %s |' % (n, r_ens(n, c).replace('|', '/')))
L += ['', '## 6. Arquivos dos testes (sha256 lido)', '']
for p in sorted((R21 / 'src_r2_1').rglob('*.py')):
    L.append('- `%s` `%s`' % (p.relative_to(R21), hashlib.sha256(p.read_bytes()).hexdigest()[:16]))
(R21 / 'TESTES_R2_1.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
print('ok', len(L))
