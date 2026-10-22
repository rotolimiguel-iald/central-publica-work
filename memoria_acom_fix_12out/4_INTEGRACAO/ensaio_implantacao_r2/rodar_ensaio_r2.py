# -*- coding: utf-8 -*-
"""ENSAIO R2 da implantação e da reversão (achados 1 e 3 da revisão de 13/10), numa CÓPIA COMPLETA da instalação
(mesma montagem do ensaio R1: originais congelados, banco v1 sintético do código v1 congelado com um .bak_ por mutação,
superfícies D5 copiadas, «D:» sintético) e — novidade — com GESTÃO DE PROCESSOS LIGADA sobre o backend SIMULADO
(implantacao_lib.ProcessosSim + sim/: agendador com RestartCount/RestartInterval/IgnoreNew/Disabled, supervisor com
trava de instância única, filho web que registra o sha do store.py que carregou).

Cenários:
  A  controle do perigo: a ordem do R1 (stop script sem desabilitar a tarefa) -> o agendador RELANÇA o supervisor
  B  ciclo completo com processos geridos: dry-run (nada muda, processos intactos) -> implantar CONCLUIDA -> reverter
     REVERTIDA; nenhum lançamento entre parar e reiniciar; depois de cada reinício 1 supervisor + 1 web com o código certo
  B2 o mesmo com reverter --mover-backups-de-volta (identidade total)
  C  falha no passo 4 (o último alvo preso aberto por outro processo, a troca falha depois de 14 de 15): recibo com a
     lista e as fases; tempário removido; app parado e tarefa desabilitada sem relançamento; reverter devolve TUDO
     (arquivos, banco, app pela tarefa)
  D  o E6 da revisão A literal (último alvo somente-leitura): a pré-conferência recusa ANTES de mudar; reverter inócuo
  E  falha antes de qualquer mudança (passo 2): o app volta sozinho, pela tarefa reabilitada
  F  falha no passo 5 (uma superfície somente-leitura, blocos aplicados em parte): reverter devolve arquivos, banco,
     blocos aplicados e o app
Roda sob a guarda da auditoria (PYTHONPATH=guard, ACOM_AUDIT_ROOT=4_INTEGRACAO). Escreve ENSAIO_R2_RECIBO.json.
"""
from __future__ import annotations
import json
import os
import shutil
import signal
import stat
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent            # ensaio_implantacao_r2
INT = HERE.parent
sys.path[:0] = [str(INT), str(INT / 'ensaio_implantacao')]
import rodar_ensaio as E                           # noqa: E402  (montagem e conferências do ensaio R1)
from implantacao_lib import ProcessosSim, _pid_vivo  # noqa: E402

E.RAIZ = HERE / 'raiz'
E.CAND = INT / 'candidato_r2' / 'C'
MANIFESTO = INT / 'CANDIDATO_MANIFESTO_R2.json'
SIM_SCRIPTS = HERE / 'sim'
SIM_RUNS = HERE / 'sim_run'
RESTART_S = 1.5
SILENCIO_S = 3.0


def sha16(p):
    return E.sha256_file(p)[:16]


def config(sim_dir=None, nome='ensaio_config_r2.json'):
    mem = E.RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD'
    cfg = {
        '_comentario': 'ENSAIO R2: raízes na cópia ensaio_implantacao_r2/raiz; processos pelo backend SIMULADO.',
        'candidato_root': str(E.CAND), 'manifesto_candidato': str(MANIFESTO),
        'raizes': {r'C:\IALD\MEMORIA_IALD': str(mem),
                   r'C:\IALD\projetos_pyhton\IALD': str(E.RAIZ / 'C' / 'IALD' / 'projetos_pyhton' / 'IALD'),
                   r'C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator':
                       str(E.RAIZ / 'C' / 'IALD' / 'Central de Patentes' / 'Chatgpt' / 'IALD_ORQUESTRACAO_20260923' / 'iald_orchestrator')},
        'app_root_processos': str(E.RAIZ / 'C' / 'IALD' / 'projetos_pyhton' / 'IALD'),
        'gerir_processos': sim_dir is not None, 'processos_backend': 'simulado', 'sim_dir': str(sim_dir) if sim_dir else None,
        'tarefa_agendada': 'IALD Web Server (simulada)', 'silencio_s': SILENCIO_S, 'esperar_parada_s': 30, 'esperar_inicio_s': 40,
        'arquivo_D': str(E.RAIZ / 'D' / 'IALD_ARQUIVO' / 'MEMORIA_IALD'), 'keep_backups': 3,
        'recibos_dir': str(E.RAIZ / 'recibos'),
        'superficies': [str(E.RAIZ / 'superficies' / n) for n in E.SUPERFICIES],
        'memory_md': str(E.RAIZ / 'superficies' / 'MEMORY.md'),
        'ordem_operador': r'C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt',
        'bridge_v2': str(INT / 'ferramentas' / 'SESSION_BRIDGE_v2.md'), 'aplicar_blocos': str(INT / 'ferramentas' / 'aplicar_blocos.py'),
    }
    path = HERE / nome
    path.write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return path, cfg


# ------------------------------------------------------------------ simulação de processos
class Sim:
    def __init__(self, nome):
        self.dir = SIM_RUNS / nome
        if self.dir.exists():
            self.matar_tudo()
            shutil.rmtree(self.dir)
        (self.dir / 'pids').mkdir(parents=True)
        (self.dir / 'comandos').mkdir()
        mem = E.RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD'
        (self.dir / 'tarefa.json').write_text(json.dumps({
            'nome': 'IALD Web Server (simulada)', 'enabled': True, 'restart_count': 3, 'restart_interval_s': RESTART_S,
            'scripts': str(SIM_SCRIPTS), 'mem_root': str(mem)}), encoding='utf-8')
        (self.dir / 'estado_agendador.json').write_text('{}', encoding='utf-8')
        self.agendador = subprocess.Popen([sys.executable, '-X', 'utf8', str(SIM_SCRIPTS / 'sim_agendador.py'), str(self.dir)],
                                          stdout=open(self.dir / 'saida_agendador.log', 'ab'), stderr=subprocess.STDOUT)
        self.backend = ProcessosSim(self.dir)
        time.sleep(0.5)

    def subir(self):
        self.backend.tarefa_iniciar()
        return self.esperar_saudavel()

    def esperar_saudavel(self, s=30):
        t0 = time.time()
        while time.time() - t0 < s:
            p = self.backend.listar()
            if self.backend.saude()[0] and len(p['web']) == 1 and len(p['supervisores']) == 1:
                return p
            time.sleep(0.3)
        raise RuntimeError('sim não ficou saudável')

    def eventos(self):
        f = self.dir / 'eventos.jsonl'
        return [json.loads(l) for l in f.read_text(encoding='utf-8').splitlines() if l.strip()] if f.exists() else []

    def lancamentos(self, t_ini, t_fim):
        return [e for e in self.eventos() if t_ini <= e['t'] <= t_fim and e['kind'] in ('LAUNCH', 'SUP_START', 'WEB_START', 'WEB_LAUNCH')]

    def estado(self):
        p = self.backend.listar()
        return {'tarefa': self.backend.tarefa_ler(), 'supervisores': [x['pid'] for x in p['supervisores']],
                'web': [{'pid': x['pid'], 'store_sha16': x.get('store_sha16'), 'guard_sha16': x.get('guard_sha16')} for x in p['web']]}

    def matar_tudo(self):
        for f in (self.dir / 'pids').glob('*.json') if (self.dir / 'pids').exists() else []:
            try:
                pid = json.loads(f.read_text(encoding='utf-8'))['pid']
                if _pid_vivo(pid):
                    os.kill(pid, signal.SIGTERM)
            except (OSError, ValueError, KeyError):
                pass

    def encerrar(self):
        try:
            self.backend._comando('exit', esperar_s=5)
        except Exception:  # noqa: BLE001
            pass
        if self.agendador.poll() is None:
            self.agendador.terminate()
        self.matar_tudo()
        time.sleep(0.5)


def epoch(iso):
    return datetime.fromisoformat(iso).timestamp()


def janela_parado(rec):
    """(fim do parar_app, início do reiniciar_app) pelo recibo (UTC ISO + segundos)."""
    p = rec['passos']['parar_app']
    ini = epoch(p['inicio']) + p.get('segundos', 0)
    r = rec['passos'].get('reiniciar_app')
    fim = epoch(r['inicio']) if r else time.time()
    return ini, fim


def ler(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def inventario_sem_recibos():
    return {k: v for k, v in E.inventario(E.RAIZ).items() if not k.startswith('recibos/')}


def alvo(cfg, prod):
    return E.Path(cfg['raizes'][next(r for r in cfg['raizes'] if prod.lower().startswith(r.lower()))]) / prod[len(next(r for r in cfg['raizes'] if prod.lower().startswith(r.lower()))):].lstrip('\\')


SHA_STORE_V1 = None
SHA_STORE_R2 = None


# ------------------------------------------------------------------ cenários
def cenario_A():
    E.montar_raiz(sizes=(6, 3, 0))
    sim = Sim('A')
    try:
        sim.subir()
        antes = sim.estado()
        t0 = time.time()
        r1_ordem = sim.backend.parar_script()          # o que o R1 fazia: stop script, tarefa HABILITADA
        time.sleep(RESTART_S + 3)
        depois = sim.estado()
        relancados = sim.lancamentos(t0, time.time())
        return {'antes': antes, 'stop_script': r1_ordem, 'depois_de_%gs' % (RESTART_S + 3): depois,
                'lancamentos_apos_parar': relancados,
                'perigo_reproduzido': any(e['kind'] == 'LAUNCH' and e.get('motivo') == 'restart_on_failure' for e in relancados)}
    finally:
        sim.encerrar()


def ciclo(nome, mover_de_volta):
    mont = E.montar_raiz()
    sim = Sim(nome)
    out = {'montagem': {k: mont[k] for k in ('db_bytes', 'db_sha256', 'backups_legados')}}
    try:
        sim.subir()
        out['processos_inicio'] = sim.estado()
        cfg_path, cfg = config(sim.dir, 'ensaio_config_r2_%s.json' % nome)
        antes = inventario_sem_recibos()
        pids_antes = out['processos_inicio']
        r = E.run([INT / 'implantar.py', '--config', cfg_path, '--dry-run'])
        dry = ler(E.RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO_dry_run.json')
        cmp_dry = E.comparar_inventarios(antes, inventario_sem_recibos())
        out['dry_run'] = {'rc': r['rc'], 'status': dry['status'], 'nada_mudou': cmp_dry['identico_nos_originais'] and cmp_dry['n_extras'] == 0,
                          'processos_intactos': sim.estado() == pids_antes,
                          'tarefa_lida': dry['passos']['pre_conferencias'].get('tarefa_agendada')}
        t_impl = time.time()
        r = E.run([INT / 'implantar.py', '--config', cfg_path])
        rec = ler(E.RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json')
        ini, fim = janela_parado(rec)
        out['implantar'] = {'rc': r['rc'], 'status': rec['status'], 'stderr': r['stderr'][-600:] if r['rc'] else None,
                            'passos': {k: v['status'] for k, v in rec['passos'].items()},
                            'parar': {k: rec['passos']['parar_app'].get(k) for k in ('tarefa_antes', 'tarefa_desabilitada_por_esta_execucao', 'silencio', 'parado_em_s')},
                            'janela_parado_s': round(fim - ini, 2),
                            'lancamentos_na_janela': sim.lancamentos(ini, fim),
                            'app_parado_conferido': [rec['passos'][p].get('app_parado_conferido') for p in ('migracao', 'substituir_arquivos')],
                            'reinicio': {k: rec['passos']['reiniciar_app'].get(k) for k in ('iniciado_por', 'ok', 'segundos')}}
        out['processos_apos_implantar'] = sim.estado()
        out['conferencia_pos_implantacao'] = E.conferir_pos_implantacao(cfg, mont, rec) if rec['status'] == 'CONCLUIDA' else None
        args = [INT / 'reverter.py', '--recibo', E.RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json']
        r = E.run(args + ['--dry-run'])
        out['reverter_dry_run'] = {'rc': r['rc'], 'status': ler(E.RAIZ / 'recibos' / 'RECIBO_REVERSAO_dry_run.json')['status'],
                                   'processos_intactos': sim.estado() == out['processos_apos_implantar']}
        r = E.run(args + (['--mover-backups-de-volta'] if mover_de_volta else []))
        rr = ler(E.RAIZ / 'recibos' / 'RECIBO_REVERSAO.json')
        p = rr['passos']['parar_app']
        ini2 = epoch(p['inicio']) + p.get('segundos', 0)
        fim2 = epoch(rr['passos']['reiniciar_app']['inicio'])
        out['reverter'] = {'rc': r['rc'], 'status': rr['status'], 'falhas': rr['falhas'],
                           'passos': {k: v['status'] for k, v in rr['passos'].items()},
                           'lancamentos_na_janela': sim.lancamentos(ini2, fim2),
                           'reinicio': {k: rr['passos']['reiniciar_app'].get(k) for k in ('iniciado_por', 'ok', 'segundos')}}
        out['processos_apos_reverter'] = sim.estado()
        cmp = E.comparar_inventarios(antes, inventario_sem_recibos())
        out['comparacao'] = cmp
        db = E.RAIZ / 'C' / 'IALD' / 'MEMORIA_IALD' / 'state' / 'memory.sqlite3'
        out['banco_igual_ao_original'] = E.sha256_file(db) == mont['db_sha256']
        web_i = out['processos_apos_implantar']['web']
        web_r = out['processos_apos_reverter']['web']
        out['ok'] = (out['dry_run']['status'] == 'DRY_RUN_OK' and out['dry_run']['nada_mudou'] and out['dry_run']['processos_intactos']
                     and out['implantar']['status'] == 'CONCLUIDA' and not out['implantar']['lancamentos_na_janela']
                     and out['implantar']['reinicio']['iniciado_por'] == 'tarefa_agendada'
                     and (out['conferencia_pos_implantacao'] or {}).get('ok') is True
                     and len(web_i) == 1 and web_i[0]['store_sha16'] == SHA_STORE_R2
                     and len(out['processos_apos_implantar']['supervisores']) == 1
                     and out['processos_apos_implantar']['tarefa']['habilitada'] is True
                     and out['reverter_dry_run']['status'] == 'DRY_RUN_OK' and out['reverter_dry_run']['processos_intactos']
                     and out['reverter']['status'] == 'REVERTIDA' and not out['reverter']['lancamentos_na_janela']
                     and len(web_r) == 1 and web_r[0]['store_sha16'] == SHA_STORE_V1
                     and out['processos_apos_reverter']['tarefa']['habilitada'] is True
                     and out['banco_igual_ao_original']
                     and (cmp['identico_sem_contar_movidos'] if mover_de_volta else cmp['identico_nos_originais']))
        return out
    finally:
        sim.encerrar()


class Prende:
    """Outro processo segura o arquivo aberto (sem FILE_SHARE_DELETE): os.replace sobre ele falha no Windows."""

    def __init__(self, path):
        self.stop = HERE / 'sim_run' / ('solta_%d' % os.getpid())
        self.stop.parent.mkdir(parents=True, exist_ok=True)
        if self.stop.exists():
            self.stop.unlink()
        code = ('import sys,time,os\nf=open(sys.argv[1],"rb")\nopen(sys.argv[3],"w").close()\n'
                'while not os.path.exists(sys.argv[2]): time.sleep(0.1)\nf.close()\n')
        self.pronto = self.stop.with_name(self.stop.name + '_pronto')
        if self.pronto.exists():
            self.pronto.unlink()
        self.p = subprocess.Popen([sys.executable, '-c', code, str(path), str(self.stop), str(self.pronto)])
        t0 = time.time()
        while not self.pronto.exists() and time.time() - t0 < 10:
            time.sleep(0.05)

    def soltar(self):
        self.stop.write_text('x', encoding='utf-8')
        self.p.wait(10)
        self.stop.unlink()
        self.pronto.unlink()


def falha_e_reversao(nome, preparar, desfazer, com_sim=True, sizes=(12, 6, 0)):
    mont = E.montar_raiz(sizes=sizes)
    sim = Sim(nome) if com_sim else None
    out = {}
    try:
        if sim:
            sim.subir()
            out['processos_inicio'] = sim.estado()
        cfg_path, cfg = config(sim.dir if sim else None, 'ensaio_config_r2_%s.json' % nome)
        manifesto = ler(MANIFESTO)
        antes = inventario_sem_recibos()
        ctx = preparar(cfg, manifesto)
        t0 = time.time()
        r = E.run([INT / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rec = ler(E.RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json')
        sub = rec['passos'].get('substituir_arquivos', {})
        out['implantar'] = {'rc': r['rc'], 'status': rec['status'], 'mudancas_iniciadas': rec.get('mudancas_iniciadas'),
                            'passos': {k: v['status'] for k, v in rec['passos'].items()},
                            'erro': {k: v.get('mensagem') for k, v in rec['passos'].items() if v['status'] == 'FALHOU'},
                            'arquivos_registrados': len(sub.get('arquivos') or []),
                            'fases': [a.get('fase') for a in sub.get('arquivos') or []],
                            'tempario_removido': [a.get('tempario_removido') for a in sub.get('arquivos') or [] if a.get('fase') == 'falhou_na_troca'],
                            'apos_falha': rec.get('apos_falha')}
        mem = Path(cfg['raizes'][r'C:\IALD\MEMORIA_IALD'])
        out['tmp_deixados'] = sorted(p.name for p in E.RAIZ.rglob('*.tmp_2*'))
        if sim:
            time.sleep(RESTART_S + 2)                     # tempo de sobra para um relançamento indevido aparecer
            out['processos_apos_falha'] = sim.estado()
            out['lancamentos_desde_a_falha_ate_agora'] = sim.lancamentos(epoch(rec['passos']['parar_app']['inicio']) + rec['passos']['parar_app'].get('segundos', 0), time.time()) \
                if rec['passos'].get('parar_app', {}).get('parado') else 'n/a (app não foi parado)'
        conn = E.sqlite3.connect('file:%s?mode=ro' % (mem / 'state' / 'memory.sqlite3').as_posix(), uri=True)
        try:
            out['schema_apos_falha'] = conn.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()[0]
        finally:
            conn.close()                                   # aberto, o arquivo não poderia ser movido pelo reverter
        desfazer(ctx)
        t1 = time.time()
        r = E.run([INT / 'reverter.py', '--recibo', E.RAIZ / 'recibos' / 'RECIBO_IMPLANTACAO.json'])
        rr = ler(E.RAIZ / 'recibos' / 'RECIBO_REVERSAO.json')
        out['reverter'] = {'rc': r['rc'], 'status': rr['status'], 'falhas': rr['falhas'],
                           'passos': {k: (v['status'], v.get('nota')) for k, v in rr['passos'].items()},
                           'arquivos': [(Path(a['alvo']).name, a.get('acao')) for a in rr['passos'].get('restaurar_arquivos', {}).get('arquivos', [])],
                           'blocos': [(Path(a['file']).name, a.get('acao')) for a in rr['passos'].get('restaurar_blocos', {}).get('arquivos', []) or []],
                           'conferencia_manifesto': rr['passos'].get('restaurar_arquivos', {}).get('conferencia_manifesto')}
        if sim:
            out['processos_apos_reverter'] = sim.estado()
        cmp = E.comparar_inventarios(antes, inventario_sem_recibos())
        out['comparacao'] = cmp
        db = mem / 'state' / 'memory.sqlite3'
        out['banco_igual_ao_original'] = E.sha256_file(db) == mont['db_sha256']
        out['lib_le_o_banco'] = subprocess.run(
            [sys.executable, '-B', '-X', 'utf8', '-c', 'import sys; sys.path.insert(0, sys.argv[1]); from iald_memory import MemoryStore; '
             'print(MemoryStore(sys.argv[2]).get(sys.argv[3], {"house":"IALD","principal":"operator"})["revision"])',
             str(mem / 'lib'), str(mem / 'state'), mont['contexts'][0]], capture_output=True).returncode == 0
        return out
    finally:
        if sim:
            sim.encerrar()


def cenario_C():
    def preparar(cfg, manifesto):
        return Prende(alvo(cfg, manifesto['arquivos'][-1]['target']))
    out = falha_e_reversao('C', preparar, lambda h: h.soltar())
    n = len(ler(MANIFESTO)['arquivos'])
    out['ok'] = (out['implantar']['status'] == 'FALHOU_EM_substituir_arquivos' and out['implantar']['arquivos_registrados'] == n
                 and out['implantar']['fases'].count('substituido') == n - 1 and out['implantar']['fases'][-1] == 'falhou_na_troca'
                 and out['implantar']['tempario_removido'] == [True] and not out['tmp_deixados']
                 and 'acao_requerida' in (out['implantar']['apos_falha'] or {})
                 and not out['processos_apos_falha']['web'] and not out['processos_apos_falha']['supervisores']
                 and out['processos_apos_falha']['tarefa']['habilitada'] is False and not out['lancamentos_desde_a_falha_ate_agora']
                 and out['reverter']['status'] == 'REVERTIDA' and out['comparacao']['identico_nos_originais']
                 and out['banco_igual_ao_original'] and out['lib_le_o_banco']
                 and len(out['processos_apos_reverter']['web']) == 1 and out['processos_apos_reverter']['web'][0]['store_sha16'] == SHA_STORE_V1
                 and out['processos_apos_reverter']['tarefa']['habilitada'] is True)
    return out


def cenario_D():
    def preparar(cfg, manifesto):
        a = alvo(cfg, manifesto['arquivos'][-1]['target'])
        os.chmod(a, stat.S_IREAD)
        return a
    out = falha_e_reversao('D', preparar, lambda a: os.chmod(a, stat.S_IREAD | stat.S_IWRITE), com_sim=False)
    out['ok'] = (out['implantar']['status'] == 'FALHOU_EM_pre_conferencias' and out['implantar']['mudancas_iniciadas'] == []
                 and not out['tmp_deixados'] and out['schema_apos_falha'] == '1'
                 and out['reverter']['status'] == 'REVERTIDA' and out['comparacao']['identico_nos_originais']
                 and out['comparacao']['n_extras'] == 0 and out['banco_igual_ao_original'] and out['lib_le_o_banco'])
    return out


def cenario_E():
    def preparar(cfg, manifesto):
        d = Path(cfg['arquivo_D'])
        d.mkdir(parents=True, exist_ok=True)
        (d / 'pre_v2').write_text('um ARQUIVO no lugar da pasta: a 2ª cópia do backup integral falha', encoding='utf-8')
        return d / 'pre_v2'
    out = falha_e_reversao('E', preparar, lambda f: f.unlink())
    pa = out['implantar']['apos_falha'] or {}
    out['ok'] = (out['implantar']['status'] == 'FALHOU_EM_backup_integral' and out['implantar']['mudancas_iniciadas'] == []
                 and (pa.get('reinicio') or {}).get('iniciado_por') == 'tarefa_agendada' and (pa.get('reinicio') or {}).get('ok') is True
                 and len(out['processos_apos_falha']['web']) == 1 and out['processos_apos_falha']['web'][0]['store_sha16'] == SHA_STORE_V1
                 and out['processos_apos_falha']['tarefa']['habilitada'] is True
                 and out['reverter']['status'] == 'REVERTIDA' and out['comparacao']['identico_nos_originais']
                 and out['banco_igual_ao_original'] and len(out['processos_apos_reverter']['web']) == 1
                 and out['processos_apos_reverter']['tarefa']['habilitada'] is True)
    return out


def cenario_F():
    def preparar(cfg, manifesto):
        a = Path(cfg['superficies'][-1])               # COORDINATOR.md da cópia
        os.chmod(a, stat.S_IREAD)
        return a
    out = falha_e_reversao('F', preparar, lambda a: os.chmod(a, stat.S_IREAD | stat.S_IWRITE))
    out['ok'] = (out['implantar']['status'] == 'FALHOU_EM_aplicar_blocos'
                 and out['implantar']['mudancas_iniciadas'] == ['migracao', 'substituir_arquivos', 'aplicar_blocos']
                 and not out['processos_apos_falha']['web'] and out['processos_apos_falha']['tarefa']['habilitada'] is False
                 and not out['lancamentos_desde_a_falha_ate_agora']
                 and out['reverter']['status'] == 'REVERTIDA' and len(out['reverter']['blocos']) >= 1
                 and out['comparacao']['identico_nos_originais'] and out['banco_igual_ao_original'] and out['lib_le_o_banco']
                 and len(out['processos_apos_reverter']['web']) == 1 and out['processos_apos_reverter']['web'][0]['store_sha16'] == SHA_STORE_V1
                 and out['processos_apos_reverter']['tarefa']['habilitada'] is True)
    return out


def main(selected=None):
    global SHA_STORE_V1, SHA_STORE_R2
    SHA_STORE_V1 = sha16(E.ORIG / 'IALD' / 'MEMORIA_IALD' / 'lib' / 'iald_memory' / 'store.py')
    SHA_STORE_R2 = sha16(E.CAND / 'IALD' / 'MEMORIA_IALD' / 'lib' / 'iald_memory' / 'store.py')
    t0 = time.time()
    recibo = {'titulo': 'ENSAIO R2 — implantação/reversão com processos geridos (backend simulado) e falhas parciais',
              'at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'manifesto': str(MANIFESTO), 'manifesto_sha16': sha16(MANIFESTO),
              'store_sha16': {'v1': SHA_STORE_V1, 'r2': SHA_STORE_R2},
              'guarda': {'ACOM_AUDIT_ROOT': os.environ.get('ACOM_AUDIT_ROOT')}, 'cenarios': {}}
    todos = {'A': cenario_A, 'B': lambda: ciclo('B', False), 'B2': lambda: ciclo('B2', True),
             'C': cenario_C, 'D': cenario_D, 'E': cenario_E, 'F': cenario_F}
    for nome, fn in todos.items():
        if selected and nome not in selected:
            continue
        t = time.time()
        try:
            res = fn()
        except Exception as exc:  # noqa: BLE001
            import traceback
            res = {'ok': False, 'excecao': traceback.format_exc()[-3000:]}
        res['segundos'] = round(time.time() - t, 1)
        if nome == 'A':
            res['ok'] = res.get('perigo_reproduzido') is True
        recibo['cenarios'][nome] = res
        print(nome, res.get('ok'), res['segundos'], flush=True)
    recibo['ok'] = all(c.get('ok') for c in recibo['cenarios'].values())
    recibo['seconds_total'] = round(time.time() - t0, 1)
    name = 'ENSAIO_R2_RECIBO.json' if not selected else 'ENSAIO_R2_RECIBO_parcial.json'
    (HERE / name).write_text(json.dumps(recibo, ensure_ascii=False, indent=1, default=str) + '\n', encoding='utf-8')
    print(json.dumps({'ok': recibo['ok'], 'cenarios': {k: v.get('ok') for k, v in recibo['cenarios'].items()},
                      'seconds': recibo['seconds_total']}, ensure_ascii=False))
    return 0 if recibo['ok'] else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:] or None))
