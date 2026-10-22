# -*- coding: utf-8 -*-
"""REVERSÃO do conserto ACOM 12/10 a partir do RECIBO_IMPLANTACAO.json — ato da gerência. R2 de 13/10.

Funciona com recibo de implantação CONCLUÍDA ou PARCIAL (falhou no meio). Sem apagar nada (o que sai do lugar é
renomeado ou movido com sha256 conferido). Passo ausente no recibo = a implantação não chegou a ele = PULADO.
  1. parar o app          [gerir_processos] desabilita a tarefa agendada se estiver habilitada, para, silêncio
  2. restaurar arquivos   — TODO arquivo registrado no recibo, seja qual for o status do passo 4: volta aos bytes do
                            <alvo>.bak_ (sha256 conferido); arquivo novo da v2 vira <alvo>.removido_<stamp>; alvo já igual
                            ao original fica; tempário órfão de troca interrompida vira .removido_. Depois confere TODOS os
                            alvos do manifesto contra o original congelado (um alvo divergente sem registro = falha visível)
  3. restaurar o banco    — SÓ depois dos arquivos de volta (se o passo 2 falhou, o banco não é tocado). Só se o banco
                            atual for v2: memory.sqlite3 -> .v2_revertido_<stamp>; o pre_v2 (sha256 conferido) volta. Banco
                            ainda v1 fica como está (restaurar o pre_v2 perderia gravações v1 feitas depois do backup)
  4. restaurar os blocos  — pelo BLOCOS_RECIBO registrado (mesmo de aplicação parcial); ausente = PULADO
  5. backups legados      — ficam em D: salvo --mover-backups-de-volta (cópia + sha256 + remoção da cópia em D:)
  6. reiniciar o app      — SEMPRE tentado (salvo --sem-reiniciar/--dry-run), mesmo que um passo anterior tenha falhado:
                            a tarefa volta a habilitada se estava habilitada ANTES da implantação, e o app sobe por ela.
                            Num estado misto a memória recusa visivelmente (SchemaMigrationRequired), sem gravar
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
from implantacao_lib import (ImplantacaoError, backend_de, copy_file_verified, iniciar_app_gerido, mapear,  # noqa: E402
                             mover_de_lado, now_iso, parar_app_gerido, sha256_file, sqlite_schema_version,
                             sqlite_writer_probe, stamp, stat_info, write_json_atomic)

PASSOS = ['parar_app', 'restaurar_arquivos', 'restaurar_banco', 'restaurar_blocos', 'backups_legados', 'reiniciar_app']
DEPENDE = {'restaurar_banco': 'restaurar_arquivos'}   # o banco só volta depois dos arquivos
SEMPRE = ('reiniciar_app',)                           # tentado mesmo depois de falha


class PassoAusente(Exception):
    pass


class Reversao:
    def __init__(self, recibo_path, dry_run, mover_de_volta, sem_reiniciar):
        self.recibo_impl_path = Path(recibo_path).resolve()
        self.recibo_impl = json.loads(self.recibo_impl_path.read_text(encoding='utf-8'))
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
        self.backend = backend_de(self.cfg)
        self.recibo_path = self.recibos / ('RECIBO_REVERSAO.json' if not dry_run else 'RECIBO_REVERSAO_dry_run.json')
        self.recibo = {'titulo': 'RECIBO DE REVERSÃO — conserto ACOM 12/10 (R2)', 'versao_ferramenta': 'R2-20261013',
                       'iniciado_em': now_iso(), 'dry_run': dry_run, 'recibo_implantacao': str(self.recibo_impl_path),
                       'implantacao_status': self.recibo_impl.get('status'),
                       'implantacao_mudancas_iniciadas': self.recibo_impl.get('mudancas_iniciadas'),
                       'stamp': self.stamp, 'status': 'EM_CURSO', 'falhas': [], 'passos': {}}
        self.reg = None

    def salvar(self):
        self.recibo['atualizado_em'] = now_iso()
        write_json_atomic(self.recibo_path, self.recibo)

    def passo(self, nome, fn):
        t0 = time.time()
        self.reg = self.recibo['passos'][nome] = {'status': 'EM_CURSO', 'inicio': now_iso()}
        self.salvar()
        try:
            res = fn()
            self.reg.update(res or {})
            self.reg['status'] = self.reg.get('status_forcado', 'OK')
        except PassoAusente as exc:
            self.reg.update({'status': 'PULADO', 'nota': str(exc)})
        except Exception as exc:  # noqa: BLE001 - registrado; os passos independentes seguem
            self.reg.update({'status': 'FALHOU', 'erro': type(exc).__name__, 'mensagem': str(exc)})
            self.recibo['falhas'].append(nome)
        self.reg['segundos'] = round(time.time() - t0, 3)
        self.salvar()

    def _passo_impl(self, nome):
        p = self.recibo_impl['passos'].get(nome)
        if not p:
            raise PassoAusente('o recibo de implantação não tem o passo %s: a implantação não chegou a ele' % nome)
        return p

    # ---------------------------------------------------------------- 1
    def parar_app(self):
        if self.backend is None:
            return {'gerido': False, 'nota': 'gerir_processos=false: processos não consultados nem tocados (ensaio)'}
        if self.dry_run:
            return {'gerido': True, 'dry_run': True, 'tarefa': self.backend.tarefa_ler(), 'processos_encontrados': self.backend.listar()}
        self.reg['gerido'] = True
        parar_app_gerido(self.backend, self.reg, self.salvar, esperar_s=int(self.cfg.get('esperar_parada_s', 60)),
                         quieto_s=float(self.cfg.get('silencio_s', 5)))
        return {}

    # ---------------------------------------------------------------- 2
    def _alvos_do_manifesto(self):
        manifesto = json.loads(Path(self.cfg['manifesto_candidato']).read_text(encoding='utf-8'))
        originais = {o['source'].lower(): o['sha256'] for o in manifesto['originais']}
        out = []
        for item in manifesto['arquivos']:
            prod = item['target']
            out.append((prod, mapear(prod, self.cfg['raizes']), originais.get(prod.lower()), item['sha256']))
        return out

    def restaurar_arquivos(self):
        p = self._passo_impl('substituir_arquivos')
        registrados = p.get('arquivos') or []
        out = {'status_do_passo_na_implantacao': p.get('status'), 'registrados': len(registrados), 'arquivos': [],
               'tempararios_orfaos': []}
        self.reg.update(out)
        for a in reversed(registrados):
            alvo = Path(a['alvo'])
            atual = sha256_file(alvo) if alvo.exists() else None
            entry = {'alvo': str(alvo), 'existia': a['existia'], 'fase_na_implantacao': a.get('fase'), 'sha256_atual': atual}
            out['arquivos'].append(entry)
            # tempário órfão de uma troca interrompida (a R2 remove o seu; uma morte do processo pode deixá-lo)
            for tmp in sorted(alvo.parent.glob(alvo.name + '.tmp_*')):
                out['tempararios_orfaos'].append(str(tmp) if self.dry_run else str(mover_de_lado(tmp, 'removido')))
            if a['existia']:
                if atual == a['sha256_antes']:
                    entry['acao'] = 'ja_original'
                    continue
                bak = Path(a['backup']) if a.get('backup') else None
                if bak is None or not bak.exists():
                    raise ImplantacaoError('alvo alterado e sem backup registrado: %s' % alvo)
                if sha256_file(bak) != a['sha256_antes']:
                    raise ImplantacaoError('backup com sha256 diferente do recibo: %s' % bak)
                if atual != a.get('sha256_depois_esperado'):
                    entry['aviso'] = 'o alvo não estava igual ao candidato; o conteúdo atual é preservado de lado'
                if self.dry_run:
                    entry['acao'] = 'restauraria do backup'
                    continue
                if alvo.exists():
                    entry['atual_guardado_em'] = str(mover_de_lado(alvo, 'v2_revertido'))
                info = copy_file_verified(bak, alvo)
                if info['sha256'] != a['sha256_antes']:
                    raise ImplantacaoError('restauração divergente: %s' % alvo)
                entry['acao'] = 'restaurado'
                entry['sha256_restaurado'] = info['sha256']
            else:
                if atual is None:
                    entry['acao'] = 'ausente (nunca criado)'
                    continue
                if self.dry_run:
                    entry['acao'] = 'renomearia para .removido_'
                    continue
                entry['removido_para'] = str(mover_de_lado(alvo, 'removido'))
                entry['acao'] = 'arquivo novo da v2: renomeado, não apagado'
            self.salvar()
        moved = p.get('pycache_movido_para')
        if moved and not self.dry_run:
            cur = self.mem_root / 'lib' / 'iald_memory' / '__pycache__'
            if cur.exists():
                out['pycache_v2_guardado_em'] = str(mover_de_lado(cur, 'v2_revertido'))
            if Path(moved).exists():
                os.replace(moved, cur)
                out['pycache_v1_restaurado'] = True
        # conferência de TODOS os alvos do manifesto (inclusive os que o recibo não registrou)
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

    # ---------------------------------------------------------------- 3
    def restaurar_banco(self):
        bk = self.recibo_impl['passos'].get('backup_integral') or {}
        copia = bk.get('copia_local') or {}
        atual = dict(stat_info(self.db), **(sqlite_schema_version(self.db) if self.db.exists() else {}))
        out = {'banco_atual_antes': atual}
        if atual.get('schema_version') == '1':
            out['status_forcado'] = 'PULADO'
            out['nota'] = 'o banco está em v1 (a migração não chegou a gravar): fica como está'
            return out
        if not copia:
            if bk.get('status') == 'PULADO':
                out['status_forcado'] = 'PULADO'
                out['nota'] = 'o banco já estava em v2 antes da implantação: nada a restaurar'
                return out
            raise ImplantacaoError('banco em v%s e sem backup integral registrado' % atual.get('schema_version'))
        src = Path(copia['path'])
        if not src.exists():
            raise ImplantacaoError('backup integral pre_v2 ausente: %s' % src)
        real = sha256_file(src)
        if real != copia.get('sha256'):
            raise ImplantacaoError('backup integral com sha256 diferente do recibo')
        out.update({'backup': str(src), 'backup_sha256': real})
        if self.dry_run:
            out['dry_run'] = True
            return out
        if (self.state / 'memory.sqlite3-journal').exists():
            raise ImplantacaoError('memory.sqlite3-journal presente; não reverter com transação em curso')
        sqlite_writer_probe(self.db)
        out['banco_v2_guardado_em'] = str(mover_de_lado(self.db, 'v2_revertido'))
        self.reg.update(out)
        self.salvar()
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
        rec = Path(p['recibo']) if p.get('recibo') else None
        if rec is None or not rec.exists():
            return {'status_forcado': 'PULADO', 'nota': 'sem BLOCOS_RECIBO (o aplicar_blocos.py não chegou a gravá-lo)',
                    'recibo_esperado': str(rec) if rec else None}
        blocos = json.loads(rec.read_text(encoding='utf-8'))
        itens = list(blocos['arquivos']) + ([blocos['memory_md']] if blocos.get('memory_md') else [])
        out = {'recibo_blocos': str(rec), 'status_do_passo_na_implantacao': p.get('status'), 'arquivos': []}
        for a in itens:
            f = Path(a['file'])
            bak = Path(a['backup'])
            entry = {'file': str(f), 'backup': str(bak), 'sha256_atual': sha256_file(f) if f.exists() else None}
            out['arquivos'].append(entry)
            if entry['sha256_atual'] == a['old_sha256']:
                entry['acao'] = 'ja_original'
                continue
            if self.dry_run:
                entry['dry_run'] = True
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
            entry['acao'] = 'restaurado'
        return out

    # ---------------------------------------------------------------- 5
    def backups_legados(self):
        p = self._passo_impl('mover_backups_antigos')
        ap = p.get('apply') or {}
        manifest = Path(ap['manifest_jsonl']) if ap.get('manifest_jsonl') else (Path(p['dest']) / 'MANIFEST.jsonl' if p.get('dest') else None)
        if manifest is None or not manifest.exists() or 'apply' not in p:
            return {'status_forcado': 'PULADO', 'nota': 'nenhum backup legado foi movido na implantação'}
        out = {'manifest_jsonl': str(manifest), 'movidos_na_implantacao': ap.get('moved')}
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
            if back.exists() or not dst_d.exists():
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
        if self.backend is None:
            return {'gerido': False}
        if self.dry_run or self.sem_reiniciar:
            return {'status_forcado': 'PULADO', 'nota': 'dry-run' if self.dry_run else '--sem-reiniciar: tarefa fica desabilitada'}
        # o estado a devolver é o de ANTES da implantação (não o desta reversão, que já encontrou a tarefa desabilitada)
        tarefa_antes = (self.recibo_impl['passos'].get('parar_app') or {}).get('tarefa_antes') \
            or (self.recibo['passos'].get('parar_app') or {}).get('tarefa_antes')
        self.reg['tarefa_a_devolver'] = tarefa_antes
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


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--recibo', required=True)
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


if __name__ == '__main__':
    sys.exit(main())
