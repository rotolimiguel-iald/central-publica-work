

# =====================================================================================================================
# REVISOR c1 R2.1: cenarios em FORMA NOVA (acrescentados ao ensaio adaptado; mesmas ferramentas R2.1 copiadas byte a byte)
# =====================================================================================================================
import ctypes  # noqa: E402

TOOLS_K3B = ENS / 'tools_k3b'


def preparar_rev(log):
    """Variante K3b: o stop script nao derruba o app E o Enable-ScheduledTask falha (so o simulador muda).
    P8b: o web simulado pode morrer ao nascer (tarefa.json: web_morre_ao_nascer)."""
    for n in ('implantar.py', 'reverter.py'):
        cpb(SRC21 / n, TOOLS_K3B / n)
    k3b = (SRC21 / 'implantacao_lib.py').read_bytes() + (
        b'\n\n# --- K3b (revisor c1 R2.1): stop sem efeito + Enable falha (so o simulador muda)\n'
        b'def _parar_script_sem_efeito(self):\n    return {"rc": 1, "nota": "K3b: stop script sem efeito (simulado)"}\n'
        b'def _habilitar_falha(self):\n    raise ImplantacaoError("K3b: Enable-ScheduledTask falhou (simulado)")\n'
        b'ProcessosSim.parar_script = _parar_script_sem_efeito\nProcessosSim.tarefa_habilitar = _habilitar_falha\n')
    (TOOLS_K3B / 'implantacao_lib.py').write_bytes(k3b)
    w = (SIMS / 'sim_web.py').read_text(encoding='utf-8')
    alvo = "time.sleep(float(t.get('saude_atraso_s', 0) or 0))\n"
    assert w.count(alvo) == 1
    w = w.replace(alvo, "if t.get('web_morre_ao_nascer'):\n    raise SystemExit(7)\n" + alvo)
    (SIMS / 'sim_web.py').write_text(w, encoding='utf-8')
    log['tools_k3b_lib_sha16'] = sha(TOOLS_K3B / 'implantacao_lib.py')[:16]
    log['sim_web_sha16'] = sha(SIMS / 'sim_web.py')[:16]
    return log


class PrendeExclusivo:
    """Abre o arquivo SEM compartilhamento (share=0): ninguem le, escreve, renomeia ou apaga ate soltar."""
    def __init__(self, path):
        self.flag = ENS / ('soltaX_%d_%d' % (os.getpid(), int(time.time() * 1000)))
        self.ready = Path(str(self.flag) + '_pronto')
        code = ('import sys,time,os,ctypes\nfrom ctypes import wintypes\n'
                'k=ctypes.WinDLL("kernel32",use_last_error=True)\n'
                'k.CreateFileW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE]\n'
                'k.CreateFileW.restype=wintypes.HANDLE\n'
                'h=k.CreateFileW(sys.argv[1],0x80000000,0,None,3,0,None)\n'
                'open(sys.argv[3],"w").write(str(ctypes.get_last_error()) if h in (None,0,(1<<64)-1) else "ok")\n'
                'while not os.path.exists(sys.argv[2]): time.sleep(0.05)\n'
                'k.CloseHandle(h)\n')
        self.p = subprocess.Popen([PY, '-c', code, str(path), str(self.flag), str(self.ready)], env=env())
        t0 = time.time()
        while not self.ready.exists() and time.time() - t0 < 10:
            time.sleep(0.02)
        self.estado = self.ready.read_text() if self.ready.exists() else None

    def soltar(self):
        self.flag.write_text('x')
        self.p.wait(10)


def alvo_de(cfg, target):
    for r, real in sorted(cfg['raizes'].items(), key=lambda kv: -len(kv[0])):
        if target.lower().startswith(r.lower() + '\\'):
            return Path(real) / target[len(r):].lstrip('\\')
    return None


def k2_variante(nome, mexer):
    """1a implantacao falha no passo 4 (ultimo alvo preso); o operador MEXE no recibo (renomeia / apaga / corrompe)
    e roda o implantar de novo. Mede o que a trava faz e onde o estado fica."""
    def fn(sim, cfg_path, cfg, mont, antes):
        man = json.loads(MAN.read_text(encoding='utf-8'))
        alvo = alvo_de(cfg, man['arquivos'][-1]['target'])
        h = Prende(alvo)
        r1 = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rec1_p = recibo_impl_ultimo()
        o = {'implantar_1': {'rc': r1['rc'], 'recibo': rec1_p.name, 'status': ler(rec1_p)['status']},
             'alvos_apos_1': contar(alvos_estado()), 'schema_apos_1': schema(), 'sim_apos_1': sim.estado()}
        h.soltar()
        o['mexida'] = mexer(rec1_p)
        r2 = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        recs = recibos_impl()
        rec2_p = [p for p in recs if p != rec1_p][-1] if [p for p in recs if p != rec1_p] else None
        rec2 = ler(rec2_p) if rec2_p else None
        o['implantar_2'] = {'rc': r2['rc'], 'stdout': r2['stdout'][-700:], 'recibo': rec2_p and rec2_p.name,
                            'status': rec2 and rec2['status'],
                            'passos': rec2 and {k: v['status'] for k, v in rec2['passos'].items()},
                            'avisos_pre': rec2 and (rec2['passos'].get('pre_conferencias') or {}).get('avisos'),
                            'backup_integral': rec2 and (rec2['passos'].get('backup_integral') or {}).get('status')}
        o['alvos_apos_2'] = contar(alvos_estado())
        o['schema_apos_2'] = schema()
        o['sim_apos_2'] = sim.estado()
        # o operador segue a secao 4: reverter --config
        rc = run([TOOLS / 'reverter.py', '--config', cfg_path])
        rr = ler(recibo_rev_ultimo()) if recibo_rev_ultimo() else None
        o['reverter_config'] = {'rc': rc['rc'], 'stdout': rc['stdout'][-500:], 'stderr': rc['stderr'][-400:],
                                'status': rr and rr['status'], 'recibo_impl': rr and Path(rr['recibo_implantacao']).name,
                                'passos': rr and {k: v['status'] for k, v in rr['passos'].items()},
                                'app_religado': rr and rr.get('app_religado')}
        o['alvos_apos_reverter_config'] = contar(alvos_estado())
        o['schema_apos_reverter_config'] = schema()
        o['sim_apos_reverter_config'] = sim.estado()
        return o
    return com_sim(nome, fn)


def _renomear(p):
    novo = p.with_name(p.name + '.lido')
    os.replace(p, novo)
    return {'acao': 'renomeado', 'para': novo.name}


def _apagar(p):
    p.unlink()
    return {'acao': 'apagado'}


def _corromper(p):
    b = p.read_bytes()
    p.write_bytes(b[:len(b) // 2])
    return {'acao': 'truncado pela metade', 'bytes': len(b) // 2}


def cen_K2b():
    return k2_variante('K2b_renomeado', _renomear)


def cen_K2c():
    return k2_variante('K2c_apagado', _apagar)


def cen_K2d():
    return k2_variante('K2d_corrompido', _corromper)


def cen_K3b():
    """O stop script nao derruba o app E o Enable-ScheduledTask falha: o recibo deve dizer que a tarefa ficou
    desabilitada e o que fazer."""
    def fn(sim, cfg_path, cfg, mont, antes):
        cfg3 = dict(cfg, esperar_parada_s=5)
        p3 = ENS / 'config_K3b.json'
        p3.write_text(json.dumps(cfg3, ensure_ascii=False, indent=1), encoding='utf-8')
        r = run([TOOLS_K3B / 'implantar.py', '--config', p3, '--pular-mover-backups'])
        rec = ler(recibo_impl_ultimo())
        af = rec.get('apos_falha') or {}
        time.sleep(2)
        return {'implantar': {'rc': r['rc'], 'stdout': r['stdout'][-600:], 'status': rec['status'], 'nota': af.get('nota'),
                              'tarefa_erro': af.get('tarefa_erro'), 'acao_sugerida': af.get('acao_sugerida'),
                              'acao_requerida': rec.get('acao_requerida')},
                'sim_apos_falha': sim.estado(), 'alvos': contar(alvos_estado())}
    return com_sim('K3b', fn, tools=TOOLS_K3B)


def cen_K3r():
    """Implantacao CONCLUIDA; depois o REVERTER encontra um stop script sem efeito (K3 do lado do reverter)."""
    def fn(sim, cfg_path, cfg, mont, antes):
        cfg3 = dict(cfg, esperar_parada_s=5)
        p3 = ENS / 'config_K3r.json'
        p3.write_text(json.dumps(cfg3, ensure_ascii=False, indent=1), encoding='utf-8')
        r = run([TOOLS / 'implantar.py', '--config', p3, '--pular-mover-backups'])
        rp = recibo_impl_ultimo()
        o = {'implantar': {'rc': r['rc'], 'status': ler(rp)['status']}, 'sim_apos_implantar': sim.estado()}
        rv = run([TOOLS_K3 / 'reverter.py', '--recibo', rp])
        rr = ler(recibo_rev_ultimo())
        o['reverter_k3'] = {'rc': rv['rc'], 'status': rr['status'], 'falhas': rr['falhas'], 'app_religado': rr.get('app_religado'),
                            'passos': {k: v['status'] for k, v in rr['passos'].items()}, 'acao_requerida': rr.get('acao_requerida'),
                            'diz_app_parado': 'fica parado' in (rr.get('acao_requerida') or '')}
        o['sim_apos_reverter_k3'] = sim.estado()
        o['alvos_apos_reverter_k3'] = contar(alvos_estado())
        o['reverter_normal'] = reverter(recibo=rp)
        o['alvos_apos_reverter_normal'] = contar(alvos_estado())
        return o
    return com_sim('K3r', fn)


def _reverter_com_gatilho(rp, gatilho, acao, limite=240):
    """Roda o reverter e, quando o recibo de reversao satisfaz `gatilho`, executa `acao()` UMA vez."""
    antes = set(p.name for p in (RAIZ / 'recibos').glob('RECIBO_REVERSAO_2*.json'))
    p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(TOOLS / 'reverter.py'), '--recibo', str(rp)], env=env(),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    t0, feito, res = time.time(), False, None
    while time.time() - t0 < limite and p.poll() is None:
        novos = [x for x in (RAIZ / 'recibos').glob('RECIBO_REVERSAO_2*.json') if x.name not in antes]
        if novos and not feito:
            try:
                rr = json.loads(novos[-1].read_text(encoding='utf-8'))
            except (OSError, ValueError):
                rr = None
            if rr and gatilho(rr):
                res = acao()
                feito = True
        time.sleep(0.01)
    out, err = p.communicate(timeout=300)
    rr = ler(recibo_rev_ultimo())
    return {'rc': p.returncode, 'acao_feita': feito, 'acao_res': res, 'stdout': out.decode('utf-8', 'replace')[-700:],
            'status': rr['status'], 'falhas': rr['falhas'], 'app_religado': rr.get('app_religado'),
            'passos': {k: (v['status'], (v.get('mensagem') or '')[:120]) for k, v in rr['passos'].items()},
            'acao_requerida': rr.get('acao_requerida')}


def _conferir_ok(rr):
    return (rr.get('passos', {}).get('conferir_alvos') or {}).get('status') == 'OK'


def cen_K4b():
    """K4 com o alvo travado SO na conferencia final (lock exclusivo depois de conferir_alvos OK)."""
    def fn(sim, cfg_path, cfg, mont, antes):
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rp = recibo_impl_ultimo()
        o = {'implantar': {'rc': r['rc'], 'status': ler(rp)['status']}}
        man = json.loads(MAN.read_text(encoding='utf-8'))
        alvo = alvo_de(cfg, man['arquivos'][3]['target'])
        trava = {}

        def acao():
            trava['h'] = PrendeExclusivo(alvo)
            return {'alvo': alvo.name, 'lock': trava['h'].estado}
        o['reverter_1'] = _reverter_com_gatilho(rp, _conferir_ok, acao)
        o['sim_apos_reverter_1'] = sim.estado()
        o['alvos_apos_reverter_1'] = contar(alvos_estado()) if 'h' not in trava else 'alvo travado (nao legivel)'
        if 'h' in trava:
            trava['h'].soltar()
        o['alvos_apos_soltar'] = contar(alvos_estado())
        o['schema_apos_reverter_1'] = schema()
        o['trava_implantar_ve_pendente'] = _trava_ve(cfg_path)
        o['reverter_2'] = reverter(recibo=rp)
        o['alvos_apos_reverter_2'] = contar(alvos_estado())
        return o
    return com_sim('K4b', fn)


def cen_K4c():
    """K4 com um alvo MODIFICADO (bytes do candidato de volta) depois de conferir_alvos OK, antes de religar."""
    def fn(sim, cfg_path, cfg, mont, antes):
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        rp = recibo_impl_ultimo()
        o = {'implantar': {'rc': r['rc'], 'status': ler(rp)['status']}}
        man = json.loads(MAN.read_text(encoding='utf-8'))
        item = man['arquivos'][3]
        alvo = alvo_de(cfg, item['target'])
        cand = CAND / Path(*Path(item['target']).parts[1:])

        def acao():
            alvo.write_bytes(cand.read_bytes())
            return {'alvo': alvo.name, 'escrito': 'bytes do candidato'}
        o['reverter_1'] = _reverter_com_gatilho(rp, _conferir_ok, acao)
        o['sim_apos_reverter_1'] = sim.estado()
        o['alvos_apos_reverter_1'] = contar(alvos_estado())
        o['trava_implantar_ve_pendente'] = _trava_ve(cfg_path)
        o['reverter_2'] = reverter(recibo=rp)
        o['alvos_apos_reverter_2'] = contar(alvos_estado())
        return o
    return com_sim('K4c', fn)


def _trava_ve(cfg_path):
    """A trava do implantar (recibos_pendentes, so leitura) ainda ve a implantacao como pendente?"""
    sys.path.insert(0, str(TOOLS))
    try:
        import implantacao_lib as L
        cfg = json.loads(Path(cfg_path).read_text(encoding='utf-8'))
        r = L.recibos_pendentes([cfg['recibos_dir']])
        return {'pendentes': [Path(p['recibo']).name for p in r['pendentes']], 'ilegiveis': len(r['ilegiveis'])}
    finally:
        sys.path.pop(0)


def cen_K6b():
    """Um leitor segura um ALVO (o 1o, CORE.md) por 2,5 s quando o passo 4 comeca (antivirus num .py recem-escrito)."""
    def fn(sim, cfg_path, cfg, mont, antes):
        man = json.loads(MAN.read_text(encoding='utf-8'))
        alvo = alvo_de(cfg, man['arquivos'][0]['target'])
        p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(TOOLS / 'implantar.py'), '--config', str(cfg_path), '--pular-mover-backups'],
                             env=env(slow_alvos(0.4)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        h = None
        t0 = time.time()
        while time.time() - t0 < 200 and p.poll() is None:
            rp = recibo_impl_ultimo()
            try:
                rec = json.loads(rp.read_text(encoding='utf-8')) if rp else None
            except (OSError, ValueError):
                rec = None
            if rec and 'substituir_arquivos' in rec['passos']:
                h = Prende(alvo)
                time.sleep(2.5)
                h.soltar()
                break
            time.sleep(0.01)
        out_s, err_s = p.communicate(timeout=300)
        rp = recibo_impl_ultimo()
        rec = ler(rp)
        sub = rec['passos'].get('substituir_arquivos', {})
        o = {'implantar': {'rc': p.returncode, 'status': rec['status'],
                           'substituidos': sum(a.get('fase') == 'substituido' for a in sub.get('arquivos') or [])},
             'leitor_segurou_alvo': h is not None, 'alvos': contar(alvos_estado()), 'sim': sim.estado()}
        o['reverter'] = reverter(recibo=rp)
        o['alvos_apos_reverter'] = contar(alvos_estado())
        return o
    return com_sim('K6b', fn)


def cen_K6c():
    """Um leitor segura o RECIBO por 40 s (acima do limite de 30 s) no meio do passo 4."""
    def fn(sim, cfg_path, cfg, mont, antes):
        p = subprocess.Popen([PY, '-B', '-X', 'utf8', str(TOOLS / 'implantar.py'), '--config', str(cfg_path), '--pular-mover-backups'],
                             env=env(slow_alvos(0.4)), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        h = None
        t0 = time.time()
        while time.time() - t0 < 200 and p.poll() is None:
            rp = recibo_impl_ultimo()
            try:
                rec = json.loads(rp.read_text(encoding='utf-8')) if rp else None
            except (OSError, ValueError):
                rec = None
            if rec and len(rec['passos'].get('substituir_arquivos', {}).get('arquivos') or []) >= 5:
                h = Prende(rp)
                time.sleep(40.0)
                h.soltar()
                break
            time.sleep(0.1)
        out_s, err_s = p.communicate(timeout=400)
        rp = recibo_impl_ultimo()
        rec = ler(rp)
        sub = rec['passos'].get('substituir_arquivos', {})
        o = {'implantar': {'rc': p.returncode, 'stdout': out_s.decode('utf-8', 'replace')[-700:], 'status': rec['status'],
                           'passos': {k: v['status'] for k, v in rec['passos'].items()},
                           'fases': [a.get('fase') for a in sub.get('arquivos') or []],
                           'acao_requerida': rec.get('acao_requerida')},
             'leitor_segurou_40s': h is not None, 'alvos': contar(alvos_estado()), 'sim': sim.estado(),
             'tmp_orfaos': sorted(x.name for x in RAIZ.rglob('*.tmp_2*'))}
        o['reverter'] = reverter(recibo=rp)
        o['alvos_apos_reverter'] = contar(alvos_estado())
        return o
    return com_sim('K6c', fn)


def cen_P8b():
    """O web v2 morre ao nascer (o supervisor fica vivo relancando): o que o operador ve no passo 8."""
    def fn(sim, cfg_path, cfg, mont, antes):
        cfg8 = dict(cfg, esperar_inicio_s=6)
        p8 = ENS / 'config_P8b.json'
        p8.write_text(json.dumps(cfg8, ensure_ascii=False, indent=1), encoding='utf-8')
        t = json.loads((sim.dir / 'tarefa.json').read_text(encoding='utf-8'))
        t['web_morre_ao_nascer'] = True
        sim.b._escrever_tarefa(t)
        r = run([TOOLS / 'implantar.py', '--config', p8, '--pular-mover-backups'])
        rp = recibo_impl_ultimo()
        rec = ler(rp)
        o = {'implantar': {'rc': r['rc'], 'status': rec['status'], 'passos': {k: v['status'] for k, v in rec['passos'].items()},
                           'acao_requerida': rec.get('acao_requerida')}, 'sim_logo_apos': sim.estado()}
        t['web_morre_ao_nascer'] = False
        sim.b._escrever_tarefa(t)
        o['reverter'] = reverter(recibo=rp)
        o['alvos_apos_reverter'] = contar(alvos_estado())
        return o
    return com_sim('P8b', fn)


def main_rev(sel):
    out = {'at': datetime.now().isoformat(timespec='seconds'), 'preparo': preparar_rev(preparar()), 'cenarios': {}}
    todos = {'K2': cen_K2, 'K3': cen_K3, 'K4': cen_K4, 'K6': cen_K6, 'P8': cen_P8,
             'K2b': cen_K2b, 'K2c': cen_K2c, 'K2d': cen_K2d, 'K3b': cen_K3b, 'K3r': cen_K3r, 'K4b': cen_K4b, 'K4c': cen_K4c,
             'K6b': cen_K6b, 'K6c': cen_K6c, 'P8b': cen_P8b, 'CFG': lambda: cen_CFG()}
    nome = 's5_ensaio_rev%s.json' % ('_' + '_'.join(sel) if sel else '')
    for n, fn in todos.items():
        if sel and n not in sel:
            continue
        t = time.time()
        try:
            res = fn()
        except Exception:  # noqa: BLE001
            res = {'excecao': traceback.format_exc()[-2500:]}
        res['segundos'] = round(time.time() - t, 1)
        out['cenarios'][n] = res
        (R21 / 'runs' / nome).write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
        print(n, res['segundos'], flush=True)
    print('fim')


def cen_CFG():
    """Os comandos da secao 4 na forma positiva: implantar (CONCLUIDA), reverter --config --dry-run, reverter --config
    (acha a unica pendente), reverter --config de novo (0 pendentes: recusa), implantar --dry-run (trava OK)."""
    def fn(sim, cfg_path, cfg, mont, antes):
        o = {}
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--dry-run'])
        o['dry_run_antes'] = {'rc': r['rc'], 'stdout': r['stdout'][-300:]}
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--pular-mover-backups'])
        o['implantar'] = {'rc': r['rc'], 'status': ler(recibo_impl_ultimo())['status']}
        r = run([TOOLS / 'reverter.py', '--config', cfg_path, '--dry-run'])
        o['reverter_config_dry_run'] = {'rc': r['rc'], 'stdout': r['stdout'][-400:]}
        o['sim_apos_dry_run_reverter'] = sim.estado()
        r = run([TOOLS / 'reverter.py', '--config', cfg_path])
        rr = ler(recibo_rev_ultimo())
        o['reverter_config'] = {'rc': r['rc'], 'status': rr['status'], 'recibo_impl': Path(rr['recibo_implantacao']).name,
                                'app_religado': rr.get('app_religado')}
        o['alvos_apos'] = contar(alvos_estado())
        r = run([TOOLS / 'reverter.py', '--config', cfg_path])
        o['reverter_config_de_novo'] = {'rc': r['rc'], 'stderr_fim': r['stderr'][-220:]}
        r = run([TOOLS / 'implantar.py', '--config', cfg_path, '--dry-run'])
        o['dry_run_depois'] = {'rc': r['rc'], 'stdout': r['stdout'][-200:]}
        return o
    return com_sim('CFG', fn)
