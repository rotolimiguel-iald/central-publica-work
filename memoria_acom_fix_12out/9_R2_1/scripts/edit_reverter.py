# -*- coding: utf-8 -*-
"""R2.1: reverter.py (9_R2_1) — K4 (sempre confere os 15 alvos; falha = NÃO religa), K2/K6 (recibos com carimbo)."""
from pathlib import Path

P = Path(__file__).resolve().parents[1] / 'reverter.py'
s = P.read_bytes().decode('utf-8')
assert '\r' not in s


def sub(old, new, count=1):
    global s
    assert s.count(old) == count, (old[:80], s.count(old))
    s = s.replace(old, new)


sub('''"""REVERSÃO do conserto ACOM 12/10 a partir do RECIBO_IMPLANTACAO.json — ato da gerência. R2 de 13/10.
''', '''"""REVERSÃO do conserto ACOM 12/10 a partir do RECIBO_IMPLANTACAO_<carimbo>.json — ato da gerência. R2/R2.1 de 13/10.

R2.1 (revisão independente R2 de 13/10):
  * K4 — os 15 alvos do manifesto são SEMPRE conferidos contra os originais (passo «conferir_alvos», mesmo quando o
    recibo não tem o passo 4) e de novo logo antes de religar; se QUALQUER passo falhou, o app NÃO é religado
    (fica parado, tarefa desabilitada) e o recibo traz a ação manual. `--forcar-reinicio` religa mesmo assim.
  * nenhum passo de restauração roda se o app não pôde ser parado (antes, a restauração seguia com o app vivo).
  * K2/K6 — recibo de reversão com carimbo (RECIBO_REVERSAO_<carimbo>.json), que cita o carimbo e o sha256 do recibo
    de implantação (é por ele que o implantar.py sabe que a implantação anterior foi revertida); recibos com nova
    tentativa curta em PermissionError. `--config <cfg>` acha sozinho a única implantação pendente.
''')

sub('''  6. reiniciar o app      — SEMPRE tentado (salvo --sem-reiniciar/--dry-run), mesmo que um passo anterior tenha falhado:
                            a tarefa volta a habilitada se estava habilitada ANTES da implantação, e o app sobe por ela.
                            Num estado misto a memória recusa visivelmente (SchemaMigrationRequired), sem gravar
  7. RECIBO_REVERSAO.json

    python -X utf8 reverter.py --recibo <RECIBO_IMPLANTACAO.json> [--dry-run] [--mover-backups-de-volta] [--sem-reiniciar]
"""''', '''  6. reiniciar o app      — R2.1: SÓ se nenhum passo falhou e os 15 alvos conferem com o original (salvo
                            --forcar-reinicio): a tarefa volta a habilitada se estava habilitada ANTES da implantação, e o
                            app sobe por ela. Com falha, o app fica PARADO e o recibo diz o que fazer (a revisão R2 mostrou
                            que a lib mista LÊ o banco v2: um estado misto não recusa sozinho)
  7. RECIBO_REVERSAO_<carimbo>.json

    python -X utf8 reverter.py --recibo <RECIBO_IMPLANTACAO_<carimbo>.json> [--dry-run] [--mover-backups-de-volta]
                               [--sem-reiniciar] [--forcar-reinicio]
    python -X utf8 reverter.py --config <implantar_config.json> [...]   (acha a única implantação pendente)
"""''')

sub('''from implantacao_lib import (ImplantacaoError, backend_de, copy_file_verified, iniciar_app_gerido, mapear,  # noqa: E402
                             mover_de_lado, now_iso, parar_app_gerido, sha256_file, sqlite_schema_version,
                             sqlite_writer_probe, stamp, stat_info, write_json_atomic)

PASSOS = ['parar_app', 'restaurar_arquivos', 'restaurar_banco', 'restaurar_blocos', 'backups_legados', 'reiniciar_app']
DEPENDE = {'restaurar_banco': 'restaurar_arquivos'}   # o banco só volta depois dos arquivos
SEMPRE = ('reiniciar_app',)                           # tentado mesmo depois de falha
''', '''from implantacao_lib import (ImplantacaoError, ReinicioPendente, backend_de, copy_file_verified,  # noqa: E402
                             estado_real, iniciar_app_gerido, ler_json_com_nova_tentativa, mapear, mover_de_lado, now_iso,
                             parar_app_gerido, recibos_pendentes, sha256_file, sqlite_schema_version, sqlite_writer_probe,
                             stamp, stat_info, write_json_atomic)

VERSAO = 'R2.1-20261013'
PASSOS = ['parar_app', 'restaurar_arquivos', 'conferir_alvos', 'restaurar_banco', 'restaurar_blocos', 'backups_legados',
          'reiniciar_app']
# R2.1: nenhuma restauração com o app vivo; o banco só volta depois dos arquivos E da conferência dos 15 alvos
DEPENDE = {'restaurar_arquivos': ('parar_app',),
           'conferir_alvos': (),
           'restaurar_banco': ('parar_app', 'restaurar_arquivos', 'conferir_alvos'),
           'restaurar_blocos': ('parar_app',),
           'backups_legados': ('parar_app',)}
''')

sub('''class Reversao:
    def __init__(self, recibo_path, dry_run, mover_de_volta, sem_reiniciar):
        self.recibo_impl_path = Path(recibo_path).resolve()
        self.recibo_impl = json.loads(self.recibo_impl_path.read_text(encoding='utf-8'))
        if self.recibo_impl.get('dry_run'):
            raise ImplantacaoError('o recibo é de um dry-run: nada a reverter')
        self.cfg = self.recibo_impl['config']
        self.dry_run = dry_run
        self.mover_de_volta = mover_de_volta
        self.sem_reiniciar = sem_reiniciar
''', '''def achar_recibo_pendente(config_path):
    """R2.1: a ÚNICA implantação real pendente de reversão na pasta de recibos da config (0 ou >1 = recusa)."""
    cfg = json.loads(Path(config_path).read_text(encoding='utf-8'))
    dirs = [Path(cfg['recibos_dir'])] + [Path(d) for d in cfg.get('recibos_dirs_anteriores', [])]
    r = recibos_pendentes(dirs)
    if r['ilegiveis']:
        raise ImplantacaoError('recibo ilegível: %s' % [i['recibo'] for i in r['ilegiveis']])
    if len(r['pendentes']) != 1:
        raise ImplantacaoError('esperada exatamente 1 implantação pendente de reversão, achadas %d: %s; use --recibo'
                               % (len(r['pendentes']), [p['recibo'] for p in r['pendentes']]))
    return r['pendentes'][0]['recibo']


class Reversao:
    def __init__(self, recibo_path, dry_run, mover_de_volta, sem_reiniciar, forcar_reinicio=False):
        self.recibo_impl_path = Path(recibo_path).resolve()
        self.recibo_impl_sha256 = sha256_file(self.recibo_impl_path)
        self.recibo_impl = ler_json_com_nova_tentativa(self.recibo_impl_path)
        if self.recibo_impl.get('dry_run'):
            raise ImplantacaoError('o recibo é de um dry-run: nada a reverter')
        if str(self.recibo_impl.get('status') or '').startswith('RECUSADA'):
            raise ImplantacaoError('o recibo é de uma implantação RECUSADA (nada foi tocado): reverta o recibo que ela '
                                   'indica em acao_requerida: %s' % self.recibo_impl.get('acao_requerida'))
        self.cfg = self.recibo_impl['config']
        self.dry_run = dry_run
        self.mover_de_volta = mover_de_volta
        self.sem_reiniciar = sem_reiniciar
        self.forcar_reinicio = forcar_reinicio
''')

sub('''        self.recibo_path = self.recibos / ('RECIBO_REVERSAO.json' if not dry_run else 'RECIBO_REVERSAO_dry_run.json')
        self.recibo = {'titulo': 'RECIBO DE REVERSÃO — conserto ACOM 12/10 (R2)', 'versao_ferramenta': 'R2-20261013',
                       'iniciado_em': now_iso(), 'dry_run': dry_run, 'recibo_implantacao': str(self.recibo_impl_path),''',
    '''        # R2.1: recibo com carimbo; nunca sobrescreve
        self.recibo_path = self.recibos / (('RECIBO_REVERSAO_%s.json' if not dry_run else 'RECIBO_REVERSAO_dry_run_%s.json')
                                           % self.stamp)
        if self.recibo_path.exists():
            raise ImplantacaoError('recibo de reversão com o mesmo carimbo já existe: %s' % self.recibo_path)
        self.recibo = {'titulo': 'RECIBO DE REVERSÃO — conserto ACOM 12/10 (R2.1)', 'versao_ferramenta': VERSAO,
                       'iniciado_em': now_iso(), 'dry_run': dry_run, 'recibo_implantacao': str(self.recibo_impl_path),
                       'recibo_implantacao_stamp': self.recibo_impl.get('stamp'),
                       'recibo_implantacao_sha256': self.recibo_impl_sha256,''')

# conferência dos alvos sai do restaurar_arquivos e vira passo próprio (sempre roda)
sub('''        # conferência de TODOS os alvos do manifesto (inclusive os que o recibo não registrou)
        divergentes = []
        for prod, alvo, original, cand in self._alvos_do_manifesto():
            atual = sha256_file(alvo) if alvo.exists() else None
            if atual != original:
                divergentes.append({'alvo': str(alvo), 'atual': atual, 'original': original})
        out['conferencia_manifesto'] = {'alvos': len(self._alvos_do_manifesto()), 'divergentes': divergentes}
        if divergentes and not self.dry_run:
            self.reg.update(out)
            raise ImplantacaoError('%d alvo(s) não voltaram ao original: %s' % (len(divergentes), divergentes[:3]))
        return out
''', '''        # R2.1: a conferência de TODOS os alvos do manifesto é o passo seguinte (conferir_alvos), que roda sempre
        return out

    def _divergentes(self):
        alvos = self._alvos_do_manifesto()
        divergentes = []
        for prod, alvo, original, cand in alvos:
            atual = sha256_file(alvo) if alvo.exists() else None
            if atual != original:
                divergentes.append({'alvo': str(alvo), 'atual': atual, 'original': original,
                                    'e_o_candidato': atual == cand})
        return len(alvos), divergentes

    # ---------------------------------------------------------------- 2b (R2.1, K4)
    def conferir_alvos(self):
        """SEMPRE (mesmo sem o passo 4 no recibo, mesmo se restaurar_arquivos falhou ou foi pulado): os 15 alvos do
        manifesto contra o original congelado. Divergência = FALHOU (e o app não é religado)."""
        n, divergentes = self._divergentes()
        out = {'alvos': n, 'divergentes': divergentes, 'iguais_ao_original': n - len(divergentes)}
        if divergentes and not self.dry_run:
            self.reg.update(out)
            raise ImplantacaoError('%d de %d alvo(s) não estão no original: %s' % (len(divergentes), n,
                                                                              [d['alvo'] for d in divergentes][:5]))
        return out
''')

sub('''    def reiniciar_app(self):
        if self.backend is None:
            return {'gerido': False}
        if self.dry_run or self.sem_reiniciar:
            return {'status_forcado': 'PULADO', 'nota': 'dry-run' if self.dry_run else '--sem-reiniciar: tarefa fica desabilitada'}
''', '''    def reiniciar_app(self):
        if self.backend is None:
            return {'gerido': False}
        if self.dry_run or self.sem_reiniciar:
            return {'status_forcado': 'PULADO', 'nota': 'dry-run' if self.dry_run else '--sem-reiniciar: tarefa fica desabilitada'}
        # R2.1 (K4): com qualquer falha, ou com alvo fora do original, o app NÃO é religado sobre estado misto
        n, divergentes = self._divergentes()
        self.reg['conferencia_antes_de_religar'] = {'alvos': n, 'divergentes': len(divergentes)}
        motivo = list(self.recibo['falhas']) + (['alvos_divergentes:%d' % len(divergentes)] if divergentes else [])
        if motivo and not self.forcar_reinicio:
            cmd = 'python -X utf8 "%s" --recibo "%s"' % (HERE / 'reverter.py', self.recibo_impl_path)
            self.recibo['acao_requerida'] = (
                'O app NÃO foi religado (estado possivelmente misto: %s). Ele fica parado e a tarefa agendada desabilitada. '
                'Remova a causa (ver os passos FALHOU e a mensagem; ex.: arquivo preso por outro processo) e rode de novo: %s . '
                'Só religue sobre este estado por decisão explícita: o mesmo comando com --forcar-reinicio.' % (motivo, cmd))
            return {'status_forcado': 'NAO_EXECUTADO', 'motivo': motivo, 'estado_real': estado_real(self.backend)}
        if motivo:
            self.reg['forcado_apesar_de'] = motivo
''')

sub('''        self.reg['tarefa_a_devolver'] = tarefa_antes
        iniciar_app_gerido(self.backend, tarefa_antes, self.reg, self.salvar, esperar_s=int(self.cfg.get('esperar_inicio_s', 120)))
        return {}

    def executar(self):
        for nome in PASSOS:
            dep = DEPENDE.get(nome)
            if dep and self.recibo['passos'].get(dep, {}).get('status') == 'FALHOU' and nome not in SEMPRE:
                self.recibo['passos'][nome] = {'status': 'NAO_EXECUTADO', 'nota': '%s falhou: o banco só volta depois dos arquivos' % dep}
                self.salvar()
                continue
            self.passo(nome, getattr(self, nome))
        if self.recibo['falhas']:
            self.recibo['status'] = 'FALHOU_EM_' + self.recibo['falhas'][0]
        else:
            self.recibo['status'] = 'DRY_RUN_OK' if self.dry_run else 'REVERTIDA'
        self.recibo['terminado_em'] = now_iso()
        self.salvar()
        return self.recibo
''', '''        self.reg['tarefa_a_devolver'] = tarefa_antes
        try:
            iniciar_app_gerido(self.backend, tarefa_antes, self.reg, self.salvar, esperar_s=int(self.cfg.get('esperar_inicio_s', 120)))
        except ReinicioPendente as exc:
            self.aguardando_reinicio = True
            return {'status_forcado': 'AGUARDANDO_REINICIO', 'nota': str(exc), 'estado_real': estado_real(self.backend)}
        return {}

    def executar(self):
        self.aguardando_reinicio = False
        for nome in PASSOS:
            deps = DEPENDE.get(nome, ())
            falhou = [d for d in deps if self.recibo['passos'].get(d, {}).get('status') in ('FALHOU', 'NAO_EXECUTADO')]
            if falhou:
                self.recibo['passos'][nome] = {'status': 'NAO_EXECUTADO',
                                               'nota': '%s não concluiu: este passo não roda (nada se restaura com o app vivo; '
                                                       'o banco só volta depois dos arquivos conferidos)' % falhou}
                if nome not in self.recibo['falhas']:
                    self.recibo['falhas'].append(nome)
                self.salvar()
                continue
            self.passo(nome, getattr(self, nome))
        religado = self.recibo['passos'].get('reiniciar_app', {}).get('status') == 'OK'
        if self.recibo['falhas']:
            self.recibo['status'] = 'FALHOU_EM_' + self.recibo['falhas'][0]
        elif self.dry_run:
            self.recibo['status'] = 'DRY_RUN_OK'
        elif self.aguardando_reinicio:
            self.recibo['status'] = 'REVERTIDA_AGUARDANDO_REINICIO'
        else:
            self.recibo['status'] = 'REVERTIDA'
        self.recibo['app_religado'] = religado
        self.recibo['estado_real_final'] = estado_real(self.backend)
        self.recibo['terminado_em'] = now_iso()
        self.salvar()
        return self.recibo
''')

sub('''    ap.add_argument('--recibo', required=True)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--mover-backups-de-volta', action='store_true')
    ap.add_argument('--sem-reiniciar', action='store_true')
    args = ap.parse_args(argv)
    rev = Reversao(args.recibo, args.dry_run, args.mover_backups_de_volta, args.sem_reiniciar)
    rec = rev.executar()
    ok = rec['status'] in ('REVERTIDA', 'DRY_RUN_OK')
    print(json.dumps({'ok': ok, 'status': rec['status'], 'recibo': str(rev.recibo_path), 'falhas': rec['falhas'],
                      'passos': {k: v['status'] for k, v in rec['passos'].items()}}, ensure_ascii=False))
    return 0 if ok else 1
''', '''    grupo = ap.add_mutually_exclusive_group(required=True)
    grupo.add_argument('--recibo')
    grupo.add_argument('--config', help='acha a única implantação real pendente de reversão na pasta de recibos da config')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--mover-backups-de-volta', action='store_true')
    ap.add_argument('--sem-reiniciar', action='store_true')
    ap.add_argument('--forcar-reinicio', action='store_true',
                    help='religa o app mesmo com passo FALHOU ou alvo fora do original (estado misto): só por decisão explícita')
    args = ap.parse_args(argv)
    recibo = args.recibo or achar_recibo_pendente(args.config)
    rev = Reversao(recibo, args.dry_run, args.mover_backups_de_volta, args.sem_reiniciar, args.forcar_reinicio)
    rec = rev.executar()
    ok = rec['status'] in ('REVERTIDA', 'REVERTIDA_AGUARDANDO_REINICIO', 'DRY_RUN_OK')
    print(json.dumps({'ok': ok, 'status': rec['status'], 'recibo': str(rev.recibo_path), 'falhas': rec['falhas'],
                      'app_religado': rec.get('app_religado'), 'acao_requerida': rec.get('acao_requerida'),
                      'passos': {k: v['status'] for k, v in rec['passos'].items()}}, ensure_ascii=False))
    return 0 if ok else 1
''')

P.write_bytes(s.encode('utf-8'))
print('ok', P.stat().st_size)
