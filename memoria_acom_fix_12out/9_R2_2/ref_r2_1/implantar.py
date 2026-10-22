# -*- coding: utf-8 -*-
"""IMPLANTAÇÃO do conserto ACOM 12/10 (D1–D6) — ato da gerência, dirigido por um JSON de configuração. R2/R2.1 de 13/10.

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
  0. pré-conferências  — Python, candidato == manifesto, alvos == originais (CAS), banco sem -journal, ninguém segurando
                         escrita, espaço em D:, e (gerir_processos) a Tarefa Agendada e os processos LIDOS, sem tocar
  1. parar o app       — [gerir_processos] lê e REGISTRA a tarefa; Disable-ScheduledTask; Stop-ScheduledTask se corre;
                         stop_iald_web.ps1; espera; silêncio de N s (nada pode renascer)
  2. backup integral   — cópia de bytes de memory.sqlite3 -> state\\memory.sqlite3.pre_v2_<stamp> + .sha256 e 2ª cópia em D:
  3. migração          — [app parado conferido de novo] migrar_para_delta.py do CANDIDATO: dry-run, --apply, verify deep
  4. substituição      — [app parado conferido de novo] cada arquivo: REGISTRADO no recibo antes de tocar; <alvo>.bak_ de
                         bytes; tempário -> os.replace; o tempário de uma troca que falhou é removido
  5. aplicar blocos    — aplicar_blocos.py (o caminho do recibo dos blocos é registrado ANTES de rodar)
  6. mover backups     — mover_backups_antigos.py INSTALADO (--keep 3 para D:\\...\\backups_ate_20261012)
  7. verificação final — sha256 de cada alvo == candidato; import da lib instalada; --verify-only --deep
  8. reiniciar o app   — [gerir_processos e não --sem-reiniciar] reabilita a tarefa (se estava habilitada) e a inicia
                         (Start-ScheduledTask: nasce no Agendador, fora do job do shell); exige 1 supervisor + 1 web + /login 200
Se falhar ANTES de qualquer mudança (passos 0–2), o app volta ao estado de antes (tarefa reabilitada só se esta execução
a desabilitou, e iniciada). Se falhar DEPOIS de uma mudança (3–7), o app fica PARADO e a tarefa DESABILITADA (por desenho:
o app não volta sozinho sobre estado misto), e o recibo diz: rode reverter.py --recibo <recibo>.

    python -X utf8 implantar.py --config implantar_config_producao_r2_1.json --dry-run
    python -X utf8 implantar.py --config implantar_config_producao_r2_1.json [--pular-mover-backups] [--sem-reiniciar]
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from implantacao_lib import (ImplantacaoError, ReinicioPendente, assegurar_parado, backend_de, backup_bytes,  # noqa: E402
                             copy_file_verified, disk_free, estado_real, iniciar_app_gerido, mapear, mover_de_lado, now_iso,
                             parar_app_gerido, recibos_pendentes, restaurar_tarefa, run_python, sha256_file,
                             sqlite_schema_version, sqlite_writer_probe, stamp, stat_info, write_bytes_atomic,
                             write_json_atomic)

VERSAO = 'R2.1-20261013'


class RecusaReciboAnterior(ImplantacaoError):
    """R2.1 (K2): implantação real anterior não revertida; nada foi tocado."""


PASSOS = ['trava_recibo_anterior', 'pre_conferencias', 'parar_app', 'backup_integral', 'migracao', 'substituir_arquivos', 'aplicar_blocos',
          'mover_backups_antigos', 'verificacao_final', 'reiniciar_app']
PASSOS_QUE_MUDAM = ('migracao', 'substituir_arquivos', 'aplicar_blocos', 'mover_backups_antigos')


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
        self.backend = backend_de(cfg)
        # R2.1 (K2): recibo com carimbo; nunca sobrescreve um recibo anterior (dry-run também)
        self.recibo_path = self.recibos / (('RECIBO_IMPLANTACAO_%s.json' if not dry_run else 'RECIBO_IMPLANTACAO_dry_run_%s.json')
                                           % self.stamp)
        if self.recibo_path.exists():
            raise ImplantacaoError('recibo com o mesmo carimbo já existe (nada feito): %s' % self.recibo_path)
        self.dirs_recibos = [self.recibos] + [Path(d) for d in cfg.get('recibos_dirs_anteriores', [])]
        self.aguardando_reinicio = False
        self.recibo = {'titulo': 'RECIBO DE IMPLANTAÇÃO — conserto ACOM 12/10 (R2.1)', 'versao_ferramenta': VERSAO,
                       'iniciado_em': now_iso(), 'dry_run': dry_run, 'config': cfg, 'stamp': self.stamp, 'python': sys.version,
                       'status': 'EM_CURSO', 'mudancas_iniciadas': [], 'passos': {}}
        self.alvos = []  # (caminho produção, alvo real, origem candidato, sha candidato)
        for item in self.manifesto['arquivos']:
            prod = Path(item['target'])
            src = self.cand_root / Path(*prod.parts[1:])
            self.alvos.append((str(prod), mapear(prod, self.raizes), src, item['sha256']))
        self.originais = {o['source'].lower(): o['sha256'] for o in self.manifesto['originais']}
        self.reg = None

    # ---------------------------------------------------------------- infra
    def salvar(self):
        self.recibo['atualizado_em'] = now_iso()
        write_json_atomic(self.recibo_path, self.recibo)

    def marcar_mudanca(self, nome):
        if not self.dry_run and nome not in self.recibo['mudancas_iniciadas']:
            self.recibo['mudancas_iniciadas'].append(nome)
            self.salvar()

    def passo(self, nome, fn):
        t0 = time.time()
        self.reg = self.recibo['passos'][nome] = {'status': 'EM_CURSO', 'inicio': now_iso()}
        self.salvar()
        try:
            resultado = fn()
            self.reg.update(resultado or {})
            self.reg['status'] = self.reg.get('status_forcado', 'OK')
        except Exception as exc:  # falha visível, recibo gravado, interrupção
            self.reg.update({'status': 'FALHOU', 'erro': type(exc).__name__, 'mensagem': str(exc)})
            self.recibo['status'] = 'FALHOU_EM_' + nome
            self.reg['segundos'] = round(time.time() - t0, 3)
            self.salvar()
            raise
        self.reg['segundos'] = round(time.time() - t0, 3)
        self.salvar()

    def conferir_parado(self, onde):
        if self.backend is not None and not self.dry_run:
            self.reg.setdefault('app_parado_conferido', []).append(assegurar_parado(self.backend, onde))
            self.salvar()

    # ---------------------------------------------------------------- T (R2.1, K2)
    def trava_recibo_anterior(self):
        """Antes de tudo: nenhuma implantação real anterior pode estar pendente de reversão (nada é tocado aqui)."""
        r = recibos_pendentes(self.dirs_recibos, excluir=[self.recibo_path])
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
                if not os.access(alvo, os.W_OK):
                    raise ImplantacaoError('alvo somente-leitura (a troca falharia no passo 4): %s' % alvo)
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
        if free_d is None:
            raise ImplantacaoError('volume de arquivo inacessível: %s' % self.arquivo_d)
        if free_d < need:
            raise ImplantacaoError('espaço insuficiente em %s: livre %d < necessário %d' % (self.arquivo_d, free_d, need))
        for extra in ('superficies', 'memory_md', 'ordem_operador', 'bridge_v2', 'aplicar_blocos'):
            paths = self.cfg[extra] if isinstance(self.cfg[extra], list) else [self.cfg[extra]]
            for p in paths:
                if not Path(p).exists():
                    raise ImplantacaoError('%s ausente: %s' % (extra, p))
        out['superficies_antes'] = [dict(stat_info(p), sha256=sha256_file(p)) for p in self.cfg['superficies'] + [self.cfg['memory_md']]]
        if self.backend is not None:
            # só leitura: a tarefa e os processos são LIDOS aqui; nada é tocado antes do passo 1
            out['processos_backend'] = self.backend.nome
            out['tarefa_agendada'] = self.backend.tarefa_ler()
            out['processos'] = self.backend.listar()
            if self.cfg.get('tarefa_agendada') and not out['tarefa_agendada'].get('existe'):
                out['avisos'].append('tarefa agendada configurada mas ausente: o reinício será desacoplado (WMI)')
        else:
            out['processos_backend'] = None
        return out

    # ---------------------------------------------------------------- 1
    def parar_app(self):
        if self.backend is None:
            # ensaio: nenhum processo é consultado nem tocado
            return {'gerido': False, 'nota': 'gerir_processos=false: processos NÃO consultados nem tocados (ensaio); '
                                               'em produção use gerir_processos=true'}
        if self.dry_run:
            return {'gerido': True, 'dry_run': True, 'tarefa': self.backend.tarefa_ler(), 'processos_encontrados': self.backend.listar(),
                    'plano': 'Disable-ScheduledTask; Stop-ScheduledTask se Running; stop_iald_web.ps1; silêncio %gs'
                             % float(self.cfg.get('silencio_s', 5))}
        self.reg['gerido'] = True
        parar_app_gerido(self.backend, self.reg, self.salvar, esperar_s=int(self.cfg.get('esperar_parada_s', 60)),
                         quieto_s=float(self.cfg.get('silencio_s', 5)))
        sqlite_writer_probe(self.db)
        return {}

    # ---------------------------------------------------------------- 2
    def backup_integral(self):
        if self.dry_run:
            return {'dry_run': True, 'plano': 'cópia de bytes de %s para %s e %s' % (self.db, self.state, self.arquivo_d / 'pre_v2')}
        sv = sqlite_schema_version(self.db)['schema_version']
        if sv == '2':
            return {'status_forcado': 'PULADO', 'nota': 'banco já em v2; o backup integral da migração já existe (ver pre_v2_*)'}
        local = self.state / ('memory.sqlite3.pre_v2_%s' % self.stamp)
        self.reg['copia_local_planejada'] = str(local)
        self.salvar()
        info = copy_file_verified(self.db, local)
        self.reg['copia_local'] = info
        self.salvar()
        write_bytes_atomic(local.with_name(local.name + '.sha256'), ('%s  %s\n' % (info['sha256'], local.name)).encode())
        segunda_dir = self.arquivo_d / 'pre_v2'
        segunda_dir.mkdir(parents=True, exist_ok=True)
        info2 = copy_file_verified(self.db, segunda_dir / local.name)
        if info2['sha256'] != info['sha256']:
            raise ImplantacaoError('segunda cópia divergente')
        write_bytes_atomic(segunda_dir / (local.name + '.sha256'), ('%s  %s\n' % (info2['sha256'], local.name)).encode())
        return {'banco': dict(stat_info(self.db), sha256=info['sha256']), 'copia_D': info2}

    # ---------------------------------------------------------------- 3
    def migracao(self):
        self.conferir_parado('migracao')
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
        self.reg.update(out)
        self.reg['recibo_migracao'] = str(receipt)
        self.marcar_mudanca('migracao')
        ap = run_python([script, '--state', self.state, '--apply', '--receipt', receipt, '--snapshot-archive-dir', snap_dir])
        out['apply'] = {'rc': ap['returncode'], 'seconds': ap['seconds'], 'stderr': ap['stderr'][-3000:], 'receipt': str(receipt)}
        if ap['returncode'] != 0:
            out['apply']['stdout'] = ap['stdout'][-3000:]
            self.reg.update(out)
            raise ImplantacaoError('migração falhou (ver recibo e stderr)')
        res = json.loads(receipt.read_text(encoding='utf-8'))
        out['apply']['ok'] = res.get('ok')
        out['apply']['backup_da_migracao'] = res.get('backup')
        out['apply']['contexts'] = {k: {'events': v['events'], 'head_revision': v['head_revision']} for k, v in res.get('contexts', {}).items()}
        out['apply']['head_mismatches'] = res.get('head_mismatches')
        out['banco_depois'] = dict(stat_info(self.db), sha256=sha256_file(self.db), **sqlite_schema_version(self.db))
        if not res.get('ok') or out['banco_depois']['schema_version'] != '2':
            self.reg.update(out)
            raise ImplantacaoError('migração sem ok ou schema não é 2')
        return out

    # ---------------------------------------------------------------- 4
    def substituir_arquivos(self):
        """R2 (achado 1): cada arquivo entra no recibo ANTES de ser tocado, com a fase em que está:
        pendente -> backup_ok -> substituido (ou falhou_na_troca). O reverter lê esta lista mesmo com o passo FALHOU."""
        self.conferir_parado('substituir_arquivos')
        arquivos = self.reg['arquivos'] = []
        if not self.dry_run:
            self.marcar_mudanca('substituir_arquivos')
        for prod, alvo, src, sha in self.alvos:
            data = src.read_bytes()
            entry = {'producao': prod, 'alvo': str(alvo), 'existia': alvo.exists(), 'sha256_antes': None, 'backup': None,
                     'sha256_depois_esperado': sha, 'bytes': len(data), 'fase': 'pendente'}
            if alvo.exists():
                entry['sha256_antes'] = sha256_file(alvo)
            arquivos.append(entry)
            if self.dry_run:
                entry['dry_run'] = True
                continue
            self.salvar()
            if alvo.exists():
                if entry['sha256_antes'] == sha:
                    entry['nota'] = 'já era o candidato; backup feito mesmo assim'
                bak, bsha = backup_bytes(alvo)
                entry['backup'] = str(bak)
                if bsha != entry['sha256_antes']:
                    raise ImplantacaoError('backup divergente: %s' % alvo)
                entry['fase'] = 'backup_ok'
                self.salvar()
            try:
                write_bytes_atomic(alvo, data)
            except Exception as exc:
                entry['fase'] = 'falhou_na_troca'
                entry['erro'] = repr(exc)[:400]
                entry['tempario_removido'] = not any(alvo.parent.glob(alvo.name + '.tmp_*'))
                self.salvar()
                raise
            entry['sha256_depois'] = sha256_file(alvo)
            entry['fase'] = 'substituido'
            self.salvar()
            if entry['sha256_depois'] != sha:
                raise ImplantacaoError('alvo não ficou igual ao candidato: %s' % alvo)
        out = {}
        pyc = self.mem_root / 'lib' / 'iald_memory' / '__pycache__'
        if pyc.exists() and not self.dry_run:
            out['pycache_movido_para'] = str(mover_de_lado(pyc, 'bak'))
        return out

    # ---------------------------------------------------------------- 5
    def aplicar_blocos(self):
        recibo = self.recibos / ('BLOCOS_RECIBO_%s%s.json' % (self.stamp, '_dry_run' if self.dry_run else ''))
        self.reg['recibo'] = str(recibo)            # registrado ANTES de rodar: o reverter o acha mesmo se falhar
        if not self.dry_run:
            self.marcar_mudanca('aplicar_blocos')
        args = [self.cfg['aplicar_blocos'], '--bridge', self.cfg['bridge_v2'], '--ordem', self.cfg['ordem_operador'],
                '--memory-md', self.cfg['memory_md'], '--recibo', recibo]
        for alvo in self.cfg['superficies']:
            args += ['--alvo', alvo]
        if self.dry_run:
            args.append('--dry-run')
        r = run_python(args)
        out = {'rc': r['returncode'], 'seconds': r['seconds'], 'stdout': r['stdout'][-2000:], 'stderr': r['stderr'][-1500:]}
        self.reg.update(out)
        if recibo.exists():
            blocos = json.loads(recibo.read_text(encoding='utf-8'))
            out['arquivos'] = [{k: a.get(k) for k in ('file', 'old_sha256', 'new_sha256', 'block_old_sha16', 'block_new_sha16', 'backup', 'rest_unchanged')} for a in blocos['arquivos']]
            out['memory_md'] = {k: blocos['memory_md'].get(k) for k in ('file', 'old_sha256', 'new_sha256', 'lines', 'bytes', 'backup')} if blocos.get('memory_md') else None
            out['falhas'] = blocos['falhas']
            self.reg.update(out)
        if r['returncode'] != 0:
            raise ImplantacaoError('aplicar_blocos.py devolveu %d' % r['returncode'])
        if out.get('falhas'):
            raise ImplantacaoError('aplicar_blocos com falhas: %s' % out['falhas'])
        return out

    # ---------------------------------------------------------------- 6
    def mover_backups_antigos(self):
        script = self.mem_root / 'mover_backups_antigos.py'
        if not script.exists() or self.dry_run:
            script = self.cand_root / 'IALD' / 'MEMORIA_IALD' / 'mover_backups_antigos.py'
        dest = self.arquivo_d / 'backups_ate_20261012'
        self.reg['dest'] = str(dest)
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
        self.reg.update(out)
        self.marcar_mudanca('mover_backups_antigos')
        ap = run_python([script, '--state', self.state, '--dest', dest, '--keep', str(self.cfg.get('keep_backups', 3))], timeout=6 * 3600)
        out['apply'] = {'rc': ap['returncode'], 'seconds': ap['seconds'], 'stderr': ap['stderr'][-2000:]}
        try:
            rep = json.loads(ap['stdout'])
            out['apply'].update({k: rep.get(k) for k in ('ok', 'moved', 'moved_bytes', 'kept', 'failed', 'manifest_jsonl', 'manifest_jsonl_sha256', 'manifest_lines')})
        except ValueError:
            out['apply']['stdout'] = ap['stdout'][-2000:]
        if ap['returncode'] != 0:
            self.reg.update(out)
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
        if self.backend is None:
            return {'gerido': False, 'nota': 'gerir_processos=false'}
        if self.dry_run or self.sem_reiniciar:
            return {'gerido': True, 'status_forcado': 'PULADO',
                    'nota': 'não reiniciado (%s)' % ('dry-run' if self.dry_run else
                                                     '--sem-reiniciar: a tarefa agendada fica DESABILITADA; reabilite com '
                                                     'Enable-ScheduledTask e Start-ScheduledTask quando quiser subir o app')}
        tarefa_antes = self.recibo['passos'].get('parar_app', {}).get('tarefa_antes')
        try:
            iniciar_app_gerido(self.backend, tarefa_antes, self.reg, self.salvar, esperar_s=int(self.cfg.get('esperar_inicio_s', 120)))
        except ReinicioPendente as exc:
            # R2.1: a implantação está VERIFICADA (passo 7); só a saúde do app demorou. Não é falha, não se reverte.
            self.aguardando_reinicio = True
            return {'status_forcado': 'AGUARDANDO_REINICIO', 'nota': str(exc), 'estado_real': estado_real(self.backend)}
        return {}

    # ---------------------------------------------------------------- execução
    def apos_falha(self, exc=None):
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
                                         'às cegas: confira a tarefa (Get-ScheduledTask -TaskName \'%s\'), os processos e '
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
                reg['acao_sugerida'] = ('conferir Get-ScheduledTask -TaskName \'%s\' e os processos; se o supervisor morreu e o '
                                        'filho web ficou, rode stop_iald_web.ps1 e depois Start-ScheduledTask'
                                        % self.cfg.get('tarefa_agendada'))
            else:
                reg['nota'] = 'arquivos e banco intocados; a tarefa agendada não foi desabilitada por esta execução'
        reg['estado_real'] = estado_real(self.backend)

    def executar(self):
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
                    'Get-ScheduledTask -TaskName \'%s\' e http://127.0.0.1:%s/login; só se o app v2 não subir, '
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
        print(json.dumps({'ok': False, 'status': imp.recibo['status'], 'erro': repr(exc), 'recibo': str(imp.recibo_path),
                          'acao_requerida': imp.recibo.get('acao_requerida'),
                          'apos_falha': imp.recibo.get('apos_falha')}, ensure_ascii=False, default=str))
        return 1
    print(json.dumps({'ok': True, 'status': rec['status'], 'recibo': str(imp.recibo_path),
                      'acao_requerida': rec.get('acao_requerida'),
                      'passos': {k: v['status'] for k, v in rec['passos'].items()}}, ensure_ascii=False))
    return 3 if rec['status'] == 'CONCLUIDA_AGUARDANDO_REINICIO' else 0


if __name__ == '__main__':
    sys.exit(main())
