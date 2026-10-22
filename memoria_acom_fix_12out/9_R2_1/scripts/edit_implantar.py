# -*- coding: utf-8 -*-
"""R2.1: implantar.py (9_R2_1) — K2 (trava de recibo anterior; recibo com carimbo), K3 (tarefa), passo 8, K6."""
from pathlib import Path

P = Path(__file__).resolve().parents[1] / 'implantar.py'
s = P.read_bytes().decode('utf-8')
assert '\r' not in s


def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:80], s.count(old))
    s = s.replace(old, new)


sub('''"""IMPLANTAÇÃO do conserto ACOM 12/10 (D1–D6) — ato da gerência, dirigido por um JSON de configuração. R2 de 13/10.

Ordem exata (o recibo é gravado a cada mudança; qualquer falha interrompe, visível):
''', '''"""IMPLANTAÇÃO do conserto ACOM 12/10 (D1–D6) — ato da gerência, dirigido por um JSON de configuração. R2/R2.1 de 13/10.

R2.1 (revisão independente R2 de 13/10):
  * K2 — o recibo tem CARIMBO (RECIBO_IMPLANTACAO_<carimbo>.json) e nunca é sobrescrito; antes de tudo (passo
    «trava_recibo_anterior»), uma implantação REAL anterior que mudou algo (ou foi morta no meio) e não tem
    RECIBO_REVERSAO REVERTIDA correspondente RECUSA esta execução, sem tocar em nada, e diz qual recibo reverter.
  * K3 — depois de falha sem mudança, a tarefa agendada é reabilitada SE E SÓ SE esta execução a desabilitou; o
    recibo descreve a tarefa e os processos LIDOS (nunca diz «nada mudou» se a tarefa foi desabilitada).
  * passo 8 — reinício lento (início aceito, processo vivo, saúde fora do prazo) = CONCLUIDA_AGUARDANDO_REINICIO,
    com «conferir, NÃO reverter»; falha real do reinício depois da verificação final diz que a implantação foi
    verificada e que reverter é decisão depois de diagnosticar.
  * K6 — recibos e trocas com nova tentativa curta em PermissionError (implantacao_lib).

Ordem exata (o recibo é gravado a cada mudança; qualquer falha interrompe, visível):
  T. trava            — [R2.1] recibos reais anteriores não revertidos -> RECUSADA (nada é tocado)
''')

sub('''Se falhar ANTES de qualquer mudança (passos 0–2), o app volta ao estado de antes (tarefa reabilitada e iniciada). Se falhar
DEPOIS de uma mudança (3–8), o app fica PARADO e a tarefa DESABILITADA, e o recibo diz: rode reverter.py --recibo <recibo>.

    python -X utf8 implantar.py --config implantar_config_producao.json --dry-run
    python -X utf8 implantar.py --config implantar_config_producao.json [--pular-mover-backups] [--sem-reiniciar]
"""''', '''Se falhar ANTES de qualquer mudança (passos 0–2), o app volta ao estado de antes (tarefa reabilitada só se esta execução
a desabilitou, e iniciada). Se falhar DEPOIS de uma mudança (3–7), o app fica PARADO e a tarefa DESABILITADA (por desenho:
o app não volta sozinho sobre estado misto), e o recibo diz: rode reverter.py --recibo <recibo>.

    python -X utf8 implantar.py --config implantar_config_producao_r2_1.json --dry-run
    python -X utf8 implantar.py --config implantar_config_producao_r2_1.json [--pular-mover-backups] [--sem-reiniciar]
"""''')

sub('''from implantacao_lib import (ImplantacaoError, assegurar_parado, backend_de, backup_bytes, copy_file_verified,  # noqa: E402
                             disk_free, iniciar_app_gerido, mapear, mover_de_lado, now_iso, parar_app_gerido,
                             restaurar_tarefa, run_python, sha256_file, sqlite_schema_version, sqlite_writer_probe, stamp,
                             stat_info, write_bytes_atomic, write_json_atomic)

PASSOS = ['pre_conferencias', 'parar_app',''', '''from implantacao_lib import (ImplantacaoError, ReinicioPendente, assegurar_parado, backend_de, backup_bytes,  # noqa: E402
                             copy_file_verified, disk_free, estado_real, iniciar_app_gerido, mapear, mover_de_lado, now_iso,
                             parar_app_gerido, recibos_pendentes, restaurar_tarefa, run_python, sha256_file,
                             sqlite_schema_version, sqlite_writer_probe, stamp, stat_info, write_bytes_atomic,
                             write_json_atomic)

VERSAO = 'R2.1-20261013'


class RecusaReciboAnterior(ImplantacaoError):
    """R2.1 (K2): implantação real anterior não revertida; nada foi tocado."""


PASSOS = ['trava_recibo_anterior', 'pre_conferencias', 'parar_app',''')

sub('''        self.recibo_path = self.recibos / ('RECIBO_IMPLANTACAO.json' if not dry_run else 'RECIBO_IMPLANTACAO_dry_run.json')
        self.recibo = {'titulo': 'RECIBO DE IMPLANTAÇÃO — conserto ACOM 12/10 (R2)', 'versao_ferramenta': 'R2-20261013',''',
    '''        # R2.1 (K2): recibo com carimbo; nunca sobrescreve um recibo anterior (dry-run também)
        self.recibo_path = self.recibos / (('RECIBO_IMPLANTACAO_%s.json' if not dry_run else 'RECIBO_IMPLANTACAO_dry_run_%s.json')
                                           % self.stamp)
        if self.recibo_path.exists():
            raise ImplantacaoError('recibo com o mesmo carimbo já existe (nada feito): %s' % self.recibo_path)
        self.dirs_recibos = [self.recibos] + [Path(d) for d in cfg.get('recibos_dirs_anteriores', [])]
        self.aguardando_reinicio = False
        self.recibo = {'titulo': 'RECIBO DE IMPLANTAÇÃO — conserto ACOM 12/10 (R2.1)', 'versao_ferramenta': VERSAO,''')

# passo T
sub('''    # ---------------------------------------------------------------- 0
    def pre_conferencias(self):''', '''    # ---------------------------------------------------------------- T (R2.1, K2)
    def trava_recibo_anterior(self):
        """Antes de tudo: nenhuma implantação real anterior pode estar pendente de reversão (nada é tocado aqui)."""
        r = recibos_pendentes(self.dirs_recibos)
        out = {'pastas': [str(d) for d in self.dirs_recibos], 'pendentes': r['pendentes'], 'ilegiveis': r['ilegiveis']}
        if r['pendentes'] or r['ilegiveis']:
            self.reg.update(out)
            alvo = r['pendentes'][-1]['recibo'] if r['pendentes'] else None
            if alvo:
                self.recibo['acao_requerida'] = ('NÃO rode o implantar de novo. Reverta antes a implantação anterior: '
                                                 'python -X utf8 "%s" --recibo "%s"' % (HERE / 'reverter.py', alvo))
            else:
                self.recibo['acao_requerida'] = 'recibo ilegível na pasta de recibos: examine-o antes de qualquer coisa'
            raise RecusaReciboAnterior('implantação real anterior pendente de reversão (%d) ou recibo ilegível (%d): %s'
                                       % (len(r['pendentes']), len(r['ilegiveis']),
                                          [p['recibo'] for p in r['pendentes']] + [i['recibo'] for i in r['ilegiveis']]))
        return out

    # ---------------------------------------------------------------- 0
    def pre_conferencias(self):''')

# passo 8
sub('''        tarefa_antes = self.recibo['passos'].get('parar_app', {}).get('tarefa_antes')
        iniciar_app_gerido(self.backend, tarefa_antes, self.reg, self.salvar, esperar_s=int(self.cfg.get('esperar_inicio_s', 120)))
        return {}
''', '''        tarefa_antes = self.recibo['passos'].get('parar_app', {}).get('tarefa_antes')
        try:
            iniciar_app_gerido(self.backend, tarefa_antes, self.reg, self.salvar, esperar_s=int(self.cfg.get('esperar_inicio_s', 120)))
        except ReinicioPendente as exc:
            # R2.1: a implantação está VERIFICADA (passo 7); só a saúde do app demorou. Não é falha, não se reverte.
            self.aguardando_reinicio = True
            return {'status_forcado': 'AGUARDANDO_REINICIO', 'nota': str(exc), 'estado_real': estado_real(self.backend)}
        return {}
''')

# apos_falha
a = s.index('    def apos_falha(self):')
b = s.index('    def executar(self):')
s = s[:a] + '''    def apos_falha(self, exc=None):
        """R2/R2.1: falha antes de qualquer mudança -> o app volta ao estado de antes; depois de uma mudança -> o app fica
        parado com a tarefa desabilitada e o recibo diz o que fazer (reverter.py). R2.1 (K3): a tarefa é reabilitada
        SE E SÓ SE esta execução a desabilitou; o estado descrito é o LIDO. R2.1 (passo 8): falha só no reinício,
        depois da verificação final, não manda reverter às cegas."""
        reg = self.recibo['apos_falha'] = {'em': now_iso(), 'mudancas_iniciadas': list(self.recibo['mudancas_iniciadas'])}
        parar = self.recibo['passos'].get('parar_app', {})
        desabilitou = bool(parar.get('tarefa_desabilitada_por_esta_execucao'))
        reg['tarefa_desabilitada_por_esta_execucao'] = desabilitou
        if self.dry_run:
            reg['nota'] = 'dry-run: nada mudou'
            return
        if isinstance(exc, RecusaReciboAnterior):
            reg['nota'] = 'RECUSADA antes de qualquer ação: nada foi tocado (nem arquivos, nem banco, nem tarefa, nem processos)'
            return
        reverter_cmd = 'python -X utf8 "%s" --recibo "%s"' % (HERE / 'reverter.py', self.recibo_path)
        if self.recibo['mudancas_iniciadas']:
            passos = self.recibo['passos']
            verificada = passos.get('verificacao_final', {}).get('status') == 'OK'
            if verificada and passos.get('reiniciar_app', {}).get('status') == 'FALHOU':
                reg['implantacao_verificada'] = True
                reg['acao_requerida'] = ('A implantação foi VERIFICADA (passos 0-7 OK); só o reinício falhou. NÃO reverta '
                                         'às cegas: confira a tarefa (Get-ScheduledTask -TaskName \\'%s\\'), os processos e '
                                         'http://127.0.0.1:%s/login e o log do app. Se o app v2 não sobe por defeito do código '
                                         'novo, reverta com: %s' % (self.cfg.get('tarefa_agendada'), self.cfg.get('porta', 8082),
                                                                    reverter_cmd))
            else:
                reg['acao_requerida'] = reverter_cmd
                reg['nota'] = ('o app fica parado e a tarefa desabilitada POR DESENHO (o app não volta sozinho sobre um estado '
                               'misto); o reverter.py restaura e religa')
            reg['estado_real'] = estado_real(self.backend)
            self.recibo['acao_requerida'] = reg['acao_requerida']
            return
        if self.backend is None:
            reg['nota'] = 'nada mudou (processos não geridos)'
            return
        if parar.get('parado'):
            try:
                iniciar_app_gerido(self.backend, parar.get('tarefa_antes'), reg.setdefault('reinicio', {}), self.salvar)
                reg['nota'] = ('arquivos e banco intocados; o app foi parado e voltou ao estado de antes%s'
                               % (' (tarefa desabilitada e reabilitada por esta execução)' if desabilitou else ''))
            except Exception as exc2:  # noqa: BLE001 - registrado; a tarefa volta a habilitada se ESTA execução a desabilitou
                reg['reinicio_erro'] = repr(exc2)[:500]
                try:
                    restaurar_tarefa(self.backend, desabilitou, reg, self.salvar)
                except Exception as exc3:  # noqa: BLE001
                    reg['tarefa_erro'] = repr(exc3)[:500]
                reg['nota'] = 'arquivos e banco intocados; o app NÃO voltou sozinho: ver estado_real e reinicio_erro'
        else:
            # K3: o parar_app falhou no meio (ou não rodou). Nada de arquivo/banco mudou, mas a tarefa pode ter sido
            # desabilitada e parte do app pode ter morrido: reabilita a tarefa (se ESTA execução a desabilitou) e diz.
            try:
                restaurar_tarefa(self.backend, desabilitou, reg, self.salvar)
            except Exception as exc3:  # noqa: BLE001
                reg['tarefa_erro'] = repr(exc3)[:500]
            if desabilitou:
                reg['nota'] = ('arquivos e banco intocados; a tarefa agendada FOI desabilitada por esta execução e %s; o app '
                               'pode ter ficado PARCIALMENTE parado (ver estado_real)'
                               % ('foi reabilitada' if 'tarefa_erro' not in reg else 'a reabilitação FALHOU: reabilite à mão'))
                reg['acao_sugerida'] = ('conferir Get-ScheduledTask -TaskName \\'%s\\' e os processos; se o supervisor morreu e o '
                                        'filho web ficou, rode stop_iald_web.ps1 e depois Start-ScheduledTask'
                                        % self.cfg.get('tarefa_agendada'))
            else:
                reg['nota'] = 'arquivos e banco intocados; a tarefa agendada não foi desabilitada por esta execução'
        reg['estado_real'] = estado_real(self.backend)

''' + s[b:]

sub('''    def executar(self):
        try:
            for nome in PASSOS:
                self.passo(nome, getattr(self, nome))
            self.recibo['status'] = 'DRY_RUN_OK' if self.dry_run else 'CONCLUIDA'
        except Exception:
            try:
                self.apos_falha()
            finally:
                self.recibo['terminado_em'] = now_iso()
                self.salvar()
            raise
        self.recibo['terminado_em'] = now_iso()
        self.salvar()
        return self.recibo
''', '''    def executar(self):
        try:
            for nome in PASSOS:
                self.passo(nome, getattr(self, nome))
            if self.dry_run:
                self.recibo['status'] = 'DRY_RUN_OK'
            elif self.aguardando_reinicio:
                self.recibo['status'] = 'CONCLUIDA_AGUARDANDO_REINICIO'
                self.recibo['acao_requerida'] = (
                    'NÃO reverter: a implantação foi verificada (passos 0-7). O app recebeu o comando de início e há '
                    'processo vivo, mas /login não respondeu no prazo. Conferir em alguns minutos: '
                    'Get-ScheduledTask -TaskName \\'%s\\' e http://127.0.0.1:%s/login; só se o app v2 não subir, '
                    'diagnosticar antes de decidir reverter.' % (self.cfg.get('tarefa_agendada'), self.cfg.get('porta', 8082)))
            else:
                self.recibo['status'] = 'CONCLUIDA'
        except Exception as exc:
            if isinstance(exc, RecusaReciboAnterior):
                self.recibo['status'] = 'RECUSADA_RECIBO_ANTERIOR_NAO_REVERTIDO'
            try:
                self.apos_falha(exc)
            finally:
                self.recibo['terminado_em'] = now_iso()
                self.salvar()
            raise
        self.recibo['terminado_em'] = now_iso()
        self.salvar()
        return self.recibo
''')

sub('''    try:
        rec = imp.executar()
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({'ok': False, 'status': imp.recibo['status'], 'erro': repr(exc), 'recibo': str(imp.recibo_path),
                          'apos_falha': imp.recibo.get('apos_falha')}, ensure_ascii=False, default=str))
        return 1
    print(json.dumps({'ok': True, 'status': rec['status'], 'recibo': str(imp.recibo_path),
                      'passos': {k: v['status'] for k, v in rec['passos'].items()}}, ensure_ascii=False))
    return 0
''', '''    try:
        rec = imp.executar()
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({'ok': False, 'status': imp.recibo['status'], 'erro': repr(exc), 'recibo': str(imp.recibo_path),
                          'acao_requerida': imp.recibo.get('acao_requerida'),
                          'apos_falha': imp.recibo.get('apos_falha')}, ensure_ascii=False, default=str))
        return 1
    print(json.dumps({'ok': True, 'status': rec['status'], 'recibo': str(imp.recibo_path),
                      'acao_requerida': rec.get('acao_requerida'),
                      'passos': {k: v['status'] for k, v in rec['passos'].items()}}, ensure_ascii=False))
    return 3 if rec['status'] == 'CONCLUIDA_AGUARDANDO_REINICIO' else 0
''')

P.write_bytes(s.encode('utf-8'))
print('ok', P.stat().st_size)
