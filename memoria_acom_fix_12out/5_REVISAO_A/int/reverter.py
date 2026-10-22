# -*- coding: utf-8 -*-
"""REVERSÃO do conserto ACOM 12/10 a partir do RECIBO_IMPLANTACAO.json — ato da gerência.

Desfaz, na ordem inversa e sem apagar nada (o que sai do lugar é renomeado ou movido com sha256 conferido):
  1. parar o app                       [gerir_processos]
  2. restaurar os arquivos             — cada alvo volta aos bytes do <alvo>.bak_<stamp> registrado (sha256 conferido contra
                                          o recibo); o conteúdo atual vai para <alvo>.v2_revertido_<stamp>; arquivos NOVOS
                                          (sem backup) são renomeados para <alvo>.removido_<stamp>
  3. restaurar o banco                 — memory.sqlite3 atual -> memory.sqlite3.v2_revertido_<stamp>; o backup integral
                                          pre_v2 (sha256 conferido contra o recibo) volta a ser memory.sqlite3. Os diários
                                          (journal/) e instantâneos (snapshots/) FICAM como evidência (a v1 os ignora): os
                                          eventos gravados depois da migração não voltam ao banco v1 — ficam nos diários
  4. restaurar os blocos (D5)          — cada arquivo volta ao <arquivo>.bak_<stamp> do BLOCOS_RECIBO (sha256 conferido)
  5. backups legados movidos para D:   — ficam em D: (íntegros, manifesto); --mover-backups-de-volta os devolve (cópia +
                                          sha256 + remoção da cópia em D:)
  6. reiniciar o app                   [gerir_processos e não --sem-reiniciar]
  7. RECIBO_REVERSAO.json

    python -X utf8 reverter.py --recibo <RECIBO_IMPLANTACAO.json> [--dry-run] [--mover-backups-de-volta] [--sem-reiniciar]
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
from implantacao_lib import (ImplantacaoError, copy_file_verified, listar_processos_web, mover_de_lado, now_iso,  # noqa: E402
                             parar_app, iniciar_app, sha256_file, sqlite_schema_version, sqlite_writer_probe, stamp,
                             stat_info, write_json_atomic)

PASSOS = ['parar_app', 'restaurar_arquivos', 'restaurar_banco', 'restaurar_blocos', 'backups_legados', 'reiniciar_app']


class Reversao:
    def __init__(self, recibo_path, dry_run, mover_de_volta, sem_reiniciar):
        self.recibo_impl = json.loads(Path(recibo_path).read_text(encoding='utf-8'))
        if self.recibo_impl.get('dry_run'):
            raise ImplantacaoError('o recibo é de um dry-run: nada a reverter')
        self.cfg = self.recibo_impl['config']
        self.dry_run = dry_run
        self.mover_de_volta = mover_de_volta
        self.sem_reiniciar = sem_reiniciar
        self.stamp = stamp()
        self.mem_root = Path(self.cfg['raizes'][r'C:\IALD\MEMORIA_IALD'])
        self.state = self.mem_root / 'state'
        self.db = self.state / 'memory.sqlite3'
        self.recibos = Path(self.cfg['recibos_dir'])
        self.recibo_path = self.recibos / ('RECIBO_REVERSAO.json' if not dry_run else 'RECIBO_REVERSAO_dry_run.json')
        self.recibo = {'titulo': 'RECIBO DE REVERSÃO — conserto ACOM 12/10', 'iniciado_em': now_iso(), 'dry_run': dry_run,
                       'recibo_implantacao': str(Path(recibo_path).resolve()), 'implantacao_status': self.recibo_impl.get('status'),
                       'stamp': self.stamp, 'status': 'EM_CURSO', 'passos': {}}

    def salvar(self):
        self.recibo['atualizado_em'] = now_iso()
        write_json_atomic(self.recibo_path, self.recibo)

    def passo(self, nome, fn):
        t0 = time.time()
        self.recibo['passos'][nome] = {'status': 'EM_CURSO', 'inicio': now_iso()}
        self.salvar()
        try:
            res = fn()
            self.recibo['passos'][nome].update(res or {})
            self.recibo['passos'][nome]['status'] = self.recibo['passos'][nome].get('status_forcado', 'OK')
        except Exception as exc:
            self.recibo['passos'][nome].update({'status': 'FALHOU', 'erro': type(exc).__name__, 'mensagem': str(exc)})
            self.recibo['status'] = 'FALHOU_EM_' + nome
            self.recibo['passos'][nome]['segundos'] = round(time.time() - t0, 3)
            self.salvar()
            raise
        self.recibo['passos'][nome]['segundos'] = round(time.time() - t0, 3)
        self.salvar()

    def _passo_impl(self, nome):
        p = self.recibo_impl['passos'].get(nome)
        if not p:
            raise ImplantacaoError('recibo de implantação sem o passo %s' % nome)
        return p

    # ---------------------------------------------------------------- 1
    def parar_app(self):
        app_root = self.cfg['app_root_processos']
        if not self.cfg.get('gerir_processos'):
            return {'gerido': False, 'nota': 'gerir_processos=false: processos não consultados nem tocados (ensaio)'}
        antes = listar_processos_web(app_root)
        if self.dry_run:
            return {'gerido': True, 'dry_run': True, 'processos_encontrados': antes}
        if not antes['web'] and not antes['supervisores'] and not antes['listen8082']:
            return {'gerido': True, 'parado': True, 'nota': 'já estava parado'}
        res = parar_app(app_root)
        if not res['parado']:
            raise ImplantacaoError('o web server não parou')
        return res

    # ---------------------------------------------------------------- 2
    def restaurar_arquivos(self):
        p = self._passo_impl('substituir_arquivos')
        if p['status'] not in ('OK',):
            return {'status_forcado': 'PULADO', 'nota': 'a substituição não chegou a OK (%s); conferir à mão' % p['status']}
        out = {'arquivos': []}
        for a in reversed(p['arquivos']):
            alvo = Path(a['alvo'])
            entry = {'alvo': str(alvo), 'existia': a['existia'], 'sha256_atual': sha256_file(alvo) if alvo.exists() else None}
            if entry['sha256_atual'] != a.get('sha256_depois_esperado') and alvo.exists():
                entry['aviso'] = 'o alvo mudou depois da implantação; o conteúdo atual é preservado de lado'
            if self.dry_run:
                entry['dry_run'] = True
                out['arquivos'].append(entry)
                continue
            if alvo.exists():
                entry['atual_guardado_em'] = str(mover_de_lado(alvo, 'v2_revertido'))
            if a['existia']:
                bak = Path(a['backup'])
                if not bak.exists():
                    raise ImplantacaoError('backup ausente: %s' % bak)
                if sha256_file(bak) != a['sha256_antes']:
                    raise ImplantacaoError('backup com sha256 diferente do recibo: %s' % bak)
                info = copy_file_verified(bak, alvo)
                if info['sha256'] != a['sha256_antes']:
                    raise ImplantacaoError('restauração divergente: %s' % alvo)
                entry['sha256_restaurado'] = info['sha256']
            else:
                entry['removido_para'] = entry.get('atual_guardado_em')
                entry['nota'] = 'arquivo novo da v2: renomeado, não apagado'
            out['arquivos'].append(entry)
        moved = p.get('pycache_movido_para')
        if moved and not self.dry_run:
            cur = self.mem_root / 'lib' / 'iald_memory' / '__pycache__'
            if cur.exists():
                out['pycache_v2_guardado_em'] = str(mover_de_lado(cur, 'v2_revertido'))
            if Path(moved).exists():
                os.replace(moved, cur)
                out['pycache_v1_restaurado'] = True
        return out

    # ---------------------------------------------------------------- 3
    def restaurar_banco(self):
        bk = self._passo_impl('backup_integral')
        mig = self._passo_impl('migracao')
        if bk['status'] == 'PULADO' and mig['status'] == 'PULADO':
            return {'status_forcado': 'PULADO', 'nota': 'o banco já estava em v2 antes da implantação: nada a restaurar aqui'}
        copia = bk.get('copia_local') or {}
        src = Path(copia.get('path', ''))
        if not src.exists():
            raise ImplantacaoError('backup integral pre_v2 ausente: %s' % src)
        real = sha256_file(src)
        if real != copia.get('sha256'):
            raise ImplantacaoError('backup integral com sha256 diferente do recibo')
        out = {'backup': str(src), 'backup_sha256': real, 'banco_atual_antes': dict(stat_info(self.db), **(sqlite_schema_version(self.db) if self.db.exists() else {}))}
        if self.dry_run:
            out['dry_run'] = True
            return out
        if (self.state / 'memory.sqlite3-journal').exists():
            raise ImplantacaoError('memory.sqlite3-journal presente; não reverter com transação em curso')
        sqlite_writer_probe(self.db)
        out['banco_v2_guardado_em'] = str(mover_de_lado(self.db, 'v2_revertido'))
        info = copy_file_verified(src, self.db)
        if info['sha256'] != real:
            raise ImplantacaoError('banco restaurado divergente')
        out['banco_restaurado'] = dict(stat_info(self.db), sha256=info['sha256'], **sqlite_schema_version(self.db))
        if out['banco_restaurado']['schema_version'] != '1':
            raise ImplantacaoError('o banco restaurado não é v1')
        out['nota'] = 'journal/ e snapshots/ ficam como evidência; eventos v2 posteriores à migração não entram no banco v1'
        return out

    # ---------------------------------------------------------------- 4
    def restaurar_blocos(self):
        p = self._passo_impl('aplicar_blocos')
        if p['status'] != 'OK':
            return {'status_forcado': 'PULADO', 'nota': 'blocos não chegaram a OK (%s)' % p['status']}
        blocos = json.loads(Path(p['recibo']).read_text(encoding='utf-8'))
        itens = list(blocos['arquivos']) + ([blocos['memory_md']] if blocos.get('memory_md') else [])
        out = {'arquivos': []}
        for a in itens:
            f = Path(a['file'])
            bak = Path(a['backup'])
            entry = {'file': str(f), 'backup': str(bak), 'sha256_atual': sha256_file(f) if f.exists() else None}
            if self.dry_run:
                entry['dry_run'] = True
                out['arquivos'].append(entry)
                continue
            if not bak.exists() or sha256_file(bak) != a['old_sha256']:
                raise ImplantacaoError('backup do bloco ausente ou divergente: %s' % bak)
            if entry['sha256_atual'] != a['new_sha256']:
                entry['aviso'] = 'o arquivo mudou depois da aplicação do bloco; conteúdo atual preservado de lado'
            entry['atual_guardado_em'] = str(mover_de_lado(f, 'v2_revertido'))
            info = copy_file_verified(bak, f)
            if info['sha256'] != a['old_sha256']:
                raise ImplantacaoError('restauração do bloco divergente: %s' % f)
            entry['sha256_restaurado'] = info['sha256']
            out['arquivos'].append(entry)
        return out

    # ---------------------------------------------------------------- 5
    def backups_legados(self):
        p = self._passo_impl('mover_backups_antigos')
        ap = p.get('apply')
        if not ap or not ap.get('moved'):
            return {'status_forcado': 'PULADO', 'nota': 'nenhum backup legado foi movido na implantação'}
        manifest = Path(ap['manifest_jsonl'])
        out = {'manifest_jsonl': str(manifest), 'movidos_na_implantacao': ap['moved']}
        if not self.mover_de_volta:
            out['nota'] = 'os backups legados ficam em D: (íntegros, com manifesto); use --mover-backups-de-volta para devolvê-los'
            return out
        devolvidos = 0
        for line in manifest.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            dst_d = Path(item.get('dst') or item.get('dest') or (manifest.parent / item['name']))
            back = self.state / item['name']
            if self.dry_run:
                devolvidos += 1
                continue
            if back.exists():
                continue
            info = copy_file_verified(dst_d, back)
            if info['sha256'] != item['sha256']:
                raise ImplantacaoError('backup legado divergente ao voltar: %s' % item['name'])
            dst_d.unlink()
            devolvidos += 1
        out['devolvidos'] = devolvidos
        return out

    # ---------------------------------------------------------------- 6
    def reiniciar_app(self):
        if not self.cfg.get('gerir_processos'):
            return {'gerido': False}
        if self.dry_run or self.sem_reiniciar:
            return {'status_forcado': 'PULADO'}
        res = iniciar_app(self.cfg['app_root_processos'])
        if not res['ok']:
            raise ImplantacaoError('o web server não respondeu após a reversão')
        return res

    def executar(self):
        try:
            for nome in PASSOS:
                self.passo(nome, getattr(self, nome))
            self.recibo['status'] = 'DRY_RUN_OK' if self.dry_run else 'REVERTIDA'
        finally:
            self.recibo['terminado_em'] = now_iso()
            self.salvar()
        return self.recibo


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--recibo', required=True)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--mover-backups-de-volta', action='store_true')
    ap.add_argument('--sem-reiniciar', action='store_true')
    args = ap.parse_args(argv)
    rev = Reversao(args.recibo, args.dry_run, args.mover_backups_de_volta, args.sem_reiniciar)
    try:
        rec = rev.executar()
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({'ok': False, 'status': rev.recibo['status'], 'erro': repr(exc), 'recibo': str(rev.recibo_path)}, ensure_ascii=False))
        return 1
    print(json.dumps({'ok': True, 'status': rec['status'], 'recibo': str(rev.recibo_path),
                      'passos': {k: v['status'] for k, v in rec['passos'].items()}}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
