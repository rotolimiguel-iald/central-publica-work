# -*- coding: utf-8 -*-
"""IMPLANTAÇÃO do conserto ACOM 12/10 (D1–D6) — ato da gerência, dirigido por um JSON de configuração.

Ordem exata (cada passo grava o recibo antes de seguir; qualquer falha interrompe, visível):
  0. pré-conferências  — Python, candidato == CANDIDATO_MANIFESTO.json, alvos == originais (CAS), banco v1 sem -journal,
                         ninguém segurando escrita, espaço em D:
  1. parar o app       — stop_iald_web.ps1 (supervisor + filho web) se estiver rodando [gerir_processos]
  2. backup integral   — cópia de bytes de memory.sqlite3 -> state\\memory.sqlite3.pre_v2_<stamp> + .sha256 e 2ª cópia em D:
  3. migração          — migrar_para_delta.py do CANDIDATO: dry-run, depois --apply (recibo próprio; v2 verificada deep)
  4. substituição      — cada arquivo do candidato sobre o alvo, com <alvo>.bak_<stamp> de bytes; novos sem backup (registrados)
  5. aplicar blocos    — aplicar_blocos.py (CAS pelo sha16 do bloco; backups) nos 5 arquivos + linha do MEMORY.md
  6. mover backups     — mover_backups_antigos.py INSTALADO: --keep 3 para D:\\...\\backups_ate_20261012 (sha conferido, manifesto)
  7. verificação final — sha256 de cada alvo == candidato; import da lib instalada; --verify-only --deep no banco
  8. reiniciar o app   — start_iald_web.ps1 desacoplado; /login 200 [gerir_processos e não --sem-reiniciar]
  9. RECIBO_IMPLANTACAO.json (sha256 antes/depois de cada arquivo, todos os passos) — insumo do reverter.py

    python -X utf8 implantar.py --config implantar_config_producao.json --dry-run
    python -X utf8 implantar.py --config implantar_config_producao.json [--pular-mover-backups] [--sem-reiniciar]

--dry-run: só pré-conferências, dry-run da migração, dry-run dos blocos e dos backups; nada em produção muda.
"""
from __future__ import annotations
import argparse
import importlib
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from implantacao_lib import (ImplantacaoError, backup_bytes, copy_file_verified, disk_free, listar_processos_web,  # noqa: E402
                             mapear, mover_de_lado, now_iso, parar_app, iniciar_app, run_python, sha256_file, sqlite_schema_version,
                             sqlite_writer_probe, stamp, stat_info, write_bytes_atomic, write_json_atomic)

PASSOS = ['pre_conferencias', 'parar_app', 'backup_integral', 'migracao', 'substituir_arquivos', 'aplicar_blocos',
          'mover_backups_antigos', 'verificacao_final', 'reiniciar_app']


class Implantacao:
    def __init__(self, cfg, dry_run, pular_mover, sem_reiniciar):
        self.cfg = cfg
        self.dry_run = dry_run
        self.pular_mover = pular_mover
        self.sem_reiniciar = sem_reiniciar
        self.cand_root = Path(cfg['candidato_root'])
        self.manifesto = json.loads(Path(cfg['manifesto_candidato']).read_text(encoding='utf-8'))
        self.raizes = cfg['raizes']
        self.mem_root = Path(cfg['raizes'][r'C:\IALD\MEMORIA_IALD'])
        self.state = self.mem_root / 'state'
        self.db = self.state / 'memory.sqlite3'
        self.arquivo_d = Path(cfg['arquivo_D'])
        self.recibos = Path(cfg['recibos_dir'])
        self.recibos.mkdir(parents=True, exist_ok=True)
        self.stamp = stamp()
        self.recibo_path = self.recibos / ('RECIBO_IMPLANTACAO.json' if not dry_run else 'RECIBO_IMPLANTACAO_dry_run.json')
        self.recibo = {'titulo': 'RECIBO DE IMPLANTAÇÃO — conserto ACOM 12/10', 'iniciado_em': now_iso(), 'dry_run': dry_run,
                       'config': cfg, 'stamp': self.stamp, 'python': sys.version, 'status': 'EM_CURSO', 'passos': {}}
        self.alvos = []  # (caminho produção, alvo real, origem candidato, sha candidato)
        for item in self.manifesto['arquivos']:
            prod = Path(item['target'])
            src = self.cand_root / Path(*prod.parts[1:])
            self.alvos.append((str(prod), mapear(prod, self.raizes), src, item['sha256']))
        self.originais = {o['source'].lower(): o['sha256'] for o in self.manifesto['originais']}

    # ---------------------------------------------------------------- infra
    def salvar(self):
        self.recibo['atualizado_em'] = now_iso()
        write_json_atomic(self.recibo_path, self.recibo)

    def passo(self, nome, fn):
        t0 = time.time()
        self.recibo['passos'][nome] = {'status': 'EM_CURSO', 'inicio': now_iso()}
        self.salvar()
        try:
            resultado = fn()
            self.recibo['passos'][nome].update(resultado or {})
            self.recibo['passos'][nome]['status'] = self.recibo['passos'][nome].get('status_forcado', 'OK')
        except Exception as exc:  # falha visível, recibo gravado, interrupção
            self.recibo['passos'][nome].update({'status': 'FALHOU', 'erro': type(exc).__name__, 'mensagem': str(exc)})
            self.recibo['status'] = 'FALHOU_EM_' + nome
            self.recibo['passos'][nome]['segundos'] = round(time.time() - t0, 3)
            self.salvar()
            raise
        self.recibo['passos'][nome]['segundos'] = round(time.time() - t0, 3)
        self.salvar()

    # ---------------------------------------------------------------- 0
    def pre_conferencias(self):
        out = {'alvos': [], 'avisos': []}
        if sys.version_info < (3, 12):
            raise ImplantacaoError('Python >= 3.12 exigido')
        for prod, alvo, src, sha in self.alvos:
            if not src.exists():
                raise ImplantacaoError('candidato ausente: %s' % src)
            real = sha256_file(src)
            if real != sha:
                raise ImplantacaoError('candidato divergente do manifesto: %s' % src)
            entry = {'producao': prod, 'alvo': str(alvo), 'candidato': str(src), 'sha256_candidato': sha,
                     'alvo_existe': alvo.exists(), 'sha256_alvo_antes': sha256_file(alvo) if alvo.exists() else None,
                     'original_esperado': self.originais.get(prod.lower())}
            if alvo.exists():
                if entry['original_esperado'] is None:
                    raise ImplantacaoError('alvo existe mas o candidato não o conhece como original: %s' % alvo)
                if entry['sha256_alvo_antes'] != entry['original_esperado']:
                    if entry['sha256_alvo_antes'] == sha:
                        entry['ja_instalado'] = True
                        out['avisos'].append('já instalado: %s' % alvo)
                    else:
                        raise ImplantacaoError('CAS: alvo mudou desde o original do candidato: %s' % alvo)
            else:
                if entry['original_esperado'] is not None:
                    raise ImplantacaoError('alvo esperado não existe: %s' % alvo)
                if not alvo.parent.exists():
                    raise ImplantacaoError('pasta do alvo não existe: %s' % alvo.parent)
            out['alvos'].append(entry)
        if not self.db.exists():
            raise ImplantacaoError('banco não encontrado: %s' % self.db)
        if (self.state / 'memory.sqlite3-journal').exists():
            raise ImplantacaoError('memory.sqlite3-journal presente: transação em curso ou abortada; não prosseguir')
        out['banco_antes'] = dict(stat_info(self.db), sha256=sha256_file(self.db), **sqlite_schema_version(self.db))
        if out['banco_antes']['schema_version'] not in ('1', '2'):
            raise ImplantacaoError('schema_version inesperado: %r' % out['banco_antes']['schema_version'])
        if out['banco_antes']['journal_mode'].lower() != 'delete':
            raise ImplantacaoError('journal_mode %r: backup de bytes inseguro' % out['banco_antes']['journal_mode'])
        sqlite_writer_probe(self.db)
        out['escritor_livre'] = True
        baks = sorted(p for p in self.state.iterdir() if p.name.startswith('memory.sqlite3.bak_'))
        out['backups_legados'] = {'n': len(baks), 'bytes': sum(p.stat().st_size for p in baks)}
        free_d = disk_free(self.arquivo_d)
        out['espaco_livre_D'] = free_d
        need = 2 * self.db.stat().st_size + (0 if self.pular_mover else out['backups_legados']['bytes'])
        out['espaco_necessario_D_estimado'] = need
        if free_d is not None and free_d < need:
            raise ImplantacaoError('espaço insuficiente em %s: livre %d < necessário %d' % (self.arquivo_d, free_d, need))
        if free_d is None:
            raise ImplantacaoError('volume de arquivo inacessível: %s' % self.arquivo_d)
        for extra in ('superficies', 'memory_md', 'ordem_operador', 'bridge_v2', 'aplicar_blocos'):
            paths = self.cfg[extra] if isinstance(self.cfg[extra], list) else [self.cfg[extra]]
            for p in paths:
                if not Path(p).exists():
                    raise ImplantacaoError('%s ausente: %s' % (extra, p))
        out['superficies_antes'] = [dict(stat_info(p), sha256=sha256_file(p)) for p in self.cfg['superficies'] + [self.cfg['memory_md']]]
        return out

    # ---------------------------------------------------------------- 1
    def parar_app(self):
        app_root = self.cfg['app_root_processos']
        if not self.cfg.get('gerir_processos'):
            # ensaio: nenhum processo é consultado nem tocado (a guarda da auditoria recusa subprocessos não-Python)
            return {'gerido': False, 'nota': 'gerir_processos=false: processos NÃO consultados nem tocados (ensaio); '
                                               'em produção use gerir_processos=true'}
        antes = listar_processos_web(app_root)
        if self.dry_run:
            return {'gerido': True, 'dry_run': True, 'processos_encontrados': antes}
        if not antes['web'] and not antes['supervisores'] and not antes['listen8082']:
            return {'gerido': True, 'processos_encontrados': antes, 'parado': True, 'nota': 'já estava parado'}
        res = parar_app(app_root)
        res['processos_antes'] = antes
        if not res['parado']:
            raise ImplantacaoError('o web server não parou dentro do prazo')
        sqlite_writer_probe(self.db)
        return res

    # ---------------------------------------------------------------- 2
    def backup_integral(self):
        if self.dry_run:
            return {'dry_run': True, 'plano': 'cópia de bytes de %s para %s e %s' % (self.db, self.state, self.arquivo_d / 'pre_v2')}
        sv = sqlite_schema_version(self.db)['schema_version']
        if sv == '2':
            return {'status_forcado': 'PULADO', 'nota': 'banco já em v2; o backup integral da migração já existe (ver pre_v2_*)'}
        local = self.state / ('memory.sqlite3.pre_v2_%s' % self.stamp)
        info = copy_file_verified(self.db, local)
        write_bytes_atomic(local.with_name(local.name + '.sha256'), ('%s  %s\n' % (info['sha256'], local.name)).encode())
        segunda_dir = self.arquivo_d / 'pre_v2'
        segunda_dir.mkdir(parents=True, exist_ok=True)
        info2 = copy_file_verified(self.db, segunda_dir / local.name)
        if info2['sha256'] != info['sha256']:
            raise ImplantacaoError('segunda cópia divergente')
        write_bytes_atomic(segunda_dir / (local.name + '.sha256'), ('%s  %s\n' % (info2['sha256'], local.name)).encode())
        return {'banco': dict(stat_info(self.db), sha256=info['sha256']), 'copia_local': info, 'copia_D': info2}

    # ---------------------------------------------------------------- 3
    def migracao(self):
        script = self.cand_root / 'IALD' / 'MEMORIA_IALD' / 'migrar_para_delta.py'
        snap_dir = str(self.arquivo_d / 'snapshots')
        dry = run_python([script, '--state', self.state, '--snapshot-archive-dir', snap_dir])
        out = {'dry_run': {'rc': dry['returncode'], 'seconds': dry['seconds'], 'stderr': dry['stderr'][-1500:]}}
        try:
            out['dry_run']['resultado'] = json.loads(dry['stdout'])
        except ValueError:
            out['dry_run']['stdout'] = dry['stdout'][-3000:]
        if dry['returncode'] != 0:
            raise ImplantacaoError('dry-run da migração falhou')
        if self.dry_run:
            return out
        if out['dry_run']['resultado'].get('already_migrated'):
            out['status_forcado'] = 'PULADO'
            out['nota'] = 'banco já em v2'
            return out
        receipt = self.recibos / ('MIGRACAO_RECIBO_%s.json' % self.stamp)
        ap = run_python([script, '--state', self.state, '--apply', '--receipt', receipt, '--snapshot-archive-dir', snap_dir])
        out['apply'] = {'rc': ap['returncode'], 'seconds': ap['seconds'], 'stderr': ap['stderr'][-3000:], 'receipt': str(receipt)}
        if ap['returncode'] != 0:
            out['apply']['stdout'] = ap['stdout'][-3000:]
            raise ImplantacaoError('migração falhou (ver recibo e stderr)')
        res = json.loads(receipt.read_text(encoding='utf-8'))
        out['apply']['ok'] = res.get('ok')
        out['apply']['backup_da_migracao'] = res.get('backup')
        out['apply']['contexts'] = {k: {'events': v['events'], 'head_revision': v['head_revision']} for k, v in res.get('contexts', {}).items()}
        out['apply']['head_mismatches'] = res.get('head_mismatches')
        out['banco_depois'] = dict(stat_info(self.db), sha256=sha256_file(self.db), **sqlite_schema_version(self.db))
        if not res.get('ok') or out['banco_depois']['schema_version'] != '2':
            raise ImplantacaoError('migração sem ok ou schema não é 2')
        return out

    # ---------------------------------------------------------------- 4
    def substituir_arquivos(self):
        arquivos = []
        for prod, alvo, src, sha in self.alvos:
            data = src.read_bytes()
            entry = {'producao': prod, 'alvo': str(alvo), 'existia': alvo.exists(), 'sha256_antes': None, 'backup': None,
                     'sha256_depois_esperado': sha, 'bytes': len(data)}
            if alvo.exists():
                entry['sha256_antes'] = sha256_file(alvo)
            if self.dry_run:
                entry['dry_run'] = True
                arquivos.append(entry)
                continue
            if alvo.exists():
                if entry['sha256_antes'] == sha:
                    entry['nota'] = 'já era o candidato; backup feito mesmo assim'
                bak, bsha = backup_bytes(alvo)
                if bsha != entry['sha256_antes']:
                    raise ImplantacaoError('backup divergente: %s' % alvo)
                entry['backup'] = str(bak)
            write_bytes_atomic(alvo, data)
            entry['sha256_depois'] = sha256_file(alvo)
            if entry['sha256_depois'] != sha:
                raise ImplantacaoError('alvo não ficou igual ao candidato: %s' % alvo)
            arquivos.append(entry)
        out = {'arquivos': arquivos}
        pyc = self.mem_root / 'lib' / 'iald_memory' / '__pycache__'
        if pyc.exists() and not self.dry_run:
            out['pycache_movido_para'] = str(mover_de_lado(pyc, 'bak'))
        return out

    # ---------------------------------------------------------------- 5
    def aplicar_blocos(self):
        recibo = self.recibos / ('BLOCOS_RECIBO_%s%s.json' % (self.stamp, '_dry_run' if self.dry_run else ''))
        args = [self.cfg['aplicar_blocos'], '--bridge', self.cfg['bridge_v2'], '--ordem', self.cfg['ordem_operador'],
                '--memory-md', self.cfg['memory_md'], '--recibo', recibo]
        for alvo in self.cfg['superficies']:
            args += ['--alvo', alvo]
        if self.dry_run:
            args.append('--dry-run')
        r = run_python(args)
        out = {'rc': r['returncode'], 'seconds': r['seconds'], 'recibo': str(recibo), 'stdout': r['stdout'][-2000:], 'stderr': r['stderr'][-1500:]}
        if r['returncode'] != 0:
            raise ImplantacaoError('aplicar_blocos.py devolveu %d' % r['returncode'])
        blocos = json.loads(recibo.read_text(encoding='utf-8'))
        out['arquivos'] = [{k: a.get(k) for k in ('file', 'old_sha256', 'new_sha256', 'block_old_sha16', 'block_new_sha16', 'backup', 'rest_unchanged')} for a in blocos['arquivos']]
        out['memory_md'] = {k: blocos['memory_md'].get(k) for k in ('file', 'old_sha256', 'new_sha256', 'lines', 'bytes', 'backup')} if blocos.get('memory_md') else None
        out['falhas'] = blocos['falhas']
        if blocos['falhas']:
            raise ImplantacaoError('aplicar_blocos com falhas: %s' % blocos['falhas'])
        return out

    # ---------------------------------------------------------------- 6
    def mover_backups_antigos(self):
        script = self.mem_root / 'mover_backups_antigos.py'
        if not script.exists() or self.dry_run:
            script = self.cand_root / 'IALD' / 'MEMORIA_IALD' / 'mover_backups_antigos.py'
        dest = self.arquivo_d / 'backups_ate_20261012'
        dry = run_python([script, '--state', self.state, '--dest', dest, '--keep', str(self.cfg.get('keep_backups', 3)), '--dry-run'])
        out = {'dry_run': {'rc': dry['returncode'], 'seconds': dry['seconds']}}
        try:
            plan = json.loads(dry['stdout'])
            out['dry_run']['found'], out['dry_run']['to_move'] = plan.get('found'), plan.get('to_move')
            out['dry_run']['bytes_to_move'] = sum(p['bytes'] for p in plan.get('plan', []))
        except ValueError:
            out['dry_run']['stdout'] = dry['stdout'][-2000:]
        if dry['returncode'] != 0:
            raise ImplantacaoError('dry-run do arquivador falhou')
        if self.dry_run or self.pular_mover:
            out['status_forcado'] = 'PULADO' if self.pular_mover else 'OK'
            out['nota'] = 'não movido nesta execução' if self.pular_mover else 'dry-run'
            return out
        ap = run_python([script, '--state', self.state, '--dest', dest, '--keep', str(self.cfg.get('keep_backups', 3))], timeout=6 * 3600)
        out['apply'] = {'rc': ap['returncode'], 'seconds': ap['seconds'], 'stderr': ap['stderr'][-2000:]}
        try:
            rep = json.loads(ap['stdout'])
            out['apply'].update({k: rep.get(k) for k in ('ok', 'moved', 'moved_bytes', 'kept', 'failed', 'manifest_jsonl', 'manifest_jsonl_sha256', 'manifest_lines')})
        except ValueError:
            out['apply']['stdout'] = ap['stdout'][-2000:]
        if ap['returncode'] != 0:
            raise ImplantacaoError('arquivador dos backups legados falhou (origem preservada; ver manifesto)')
        return out

    # ---------------------------------------------------------------- 7
    def verificacao_final(self):
        out = {'arquivos': []}
        for prod, alvo, src, sha in self.alvos:
            real = sha256_file(alvo) if alvo.exists() else None
            out['arquivos'].append({'alvo': str(alvo), 'sha256': real, 'igual_ao_candidato': real == sha})
            if not self.dry_run and real != sha:
                raise ImplantacaoError('verificação final: %s difere do candidato' % alvo)
        lib = self.mem_root / 'lib'
        if not self.dry_run:
            imp = run_python(['-c', 'import iald_memory,sys; from iald_memory import store, guard; '
                              'print(iald_memory.__file__); print(store.SCHEMA_VERSION); print(sorted(iald_memory.__all__))'],
                             env={'PYTHONPATH': str(lib)})
            out['import_lib_instalada'] = {'rc': imp['returncode'], 'stdout': imp['stdout'][-1000:], 'stderr': imp['stderr'][-800:]}
            if imp['returncode'] != 0 or str(lib).lower() not in imp['stdout'].lower():
                raise ImplantacaoError('a lib instalada não importa do lugar esperado')
            ver = run_python([self.mem_root / 'migrar_para_delta.py', '--state', self.state, '--verify-only', '--deep',
                              '--snapshot-archive-dir', str(self.arquivo_d / 'snapshots')], timeout=3600)
            out['verify_deep'] = {'rc': ver['returncode'], 'seconds': ver['seconds']}
            try:
                res = json.loads(ver['stdout'])
                out['verify_deep']['ok'] = res.get('ok')
                out['verify_deep']['contexts'] = {k: {kk: v.get(kk) for kk in ('ok', 'event_count', 'legacy_events', 'delta_events', 'journal_ok')} for k, v in res.get('verify', {}).items()}
            except ValueError:
                out['verify_deep']['stdout'] = ver['stdout'][-2000:]
            if ver['returncode'] != 0 or not out['verify_deep'].get('ok'):
                raise ImplantacaoError('verify deep do banco migrado falhou')
            out['banco_final'] = dict(stat_info(self.db), sha256=sha256_file(self.db), **sqlite_schema_version(self.db))
            out['state_listagem'] = sorted(p.name for p in self.state.iterdir())[:50]
        return out

    # ---------------------------------------------------------------- 8
    def reiniciar_app(self):
        if not self.cfg.get('gerir_processos'):
            return {'gerido': False, 'nota': 'gerir_processos=false'}
        if self.dry_run or self.sem_reiniciar:
            return {'gerido': True, 'nota': 'não reiniciado (%s)' % ('dry-run' if self.dry_run else '--sem-reiniciar'), 'status_forcado': 'PULADO'}
        res = iniciar_app(self.cfg['app_root_processos'])
        if not res['ok']:
            raise ImplantacaoError('o web server não respondeu /login 200 após o reinício; inspecionar logs')
        return res

    # ---------------------------------------------------------------- execução
    def executar(self):
        try:
            for nome in PASSOS:
                self.passo(nome, getattr(self, nome))
            self.recibo['status'] = 'DRY_RUN_OK' if self.dry_run else 'CONCLUIDA'
        finally:
            self.recibo['terminado_em'] = now_iso()
            self.salvar()
        return self.recibo


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', required=True)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--pular-mover-backups', action='store_true')
    ap.add_argument('--sem-reiniciar', action='store_true')
    args = ap.parse_args(argv)
    cfg = json.loads(Path(args.config).read_text(encoding='utf-8'))
    imp = Implantacao(cfg, args.dry_run, args.pular_mover_backups, args.sem_reiniciar)
    try:
        rec = imp.executar()
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({'ok': False, 'status': imp.recibo['status'], 'erro': repr(exc), 'recibo': str(imp.recibo_path)}, ensure_ascii=False))
        return 1
    print(json.dumps({'ok': True, 'status': rec['status'], 'recibo': str(imp.recibo_path),
                      'passos': {k: v['status'] for k, v in rec['passos'].items()}}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
