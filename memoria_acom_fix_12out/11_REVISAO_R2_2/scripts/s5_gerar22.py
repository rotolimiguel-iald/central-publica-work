# -*- coding: utf-8 -*-
"""Gera scripts/s5_ensaio_rev22.py a partir do script do revisor anterior (10_REVISAO_R2_1/scripts/s5_ensaio_rev.py, que ja
inclui o s5_extra), trocando SO as entradas: ferramentas, candidato e manifesto de 9_R2_2; copia da suite = minha
suite_r22; saidas em 11_REVISAO_R2_2. Acrescenta o cenario P8c (o web v2 sobe, vive alguns segundos e morre; o pid muda).
Nada fora de 11_REVISAO_R2_2 e escrito."""
import hashlib
from pathlib import Path

ME = Path(__file__).resolve().parents[1]
SRC = ME.parent / '10_REVISAO_R2_1' / 'scripts' / 's5_ensaio_rev.py'
s = SRC.read_text(encoding='utf-8')
subs = [
    ("SRC21 = R21.parent / '9_R2_1'", "SRC21 = R21.parent / '9_R2_2'"),
    ("SRC21 / 'candidato_r2_1'", "SRC21 / 'candidato_r2_2'"),
    ("SRC21 / 'CANDIDATO_MANIFESTO_R2_1.json'", "SRC21 / 'CANDIDATO_MANIFESTO_R2_2.json'"),
    ("R21 / 'suite_r21'", "R21 / 'suite_r22'"),
    ("'CANDIDATO_MANIFESTO_R2_1_redigido.json'", "'CANDIDATO_MANIFESTO_R2_2_redigido.json'"),
    ("nome = 's5_ensaio_rev%s.json'", "nome = 's5_ensaio_rev22%s.json'"),
    ("nome = 's5_ensaio_r2_1%s.json'", "nome = 's5_ensaio_r2_2_antigo%s.json'"),
    ("Objetivo do ensaio R2.1", "Objetivo do ensaio R2.2 (revisor)"),
]
for a, b in subs:
    assert a in s, a
    s = s.replace(a, b)
# P8c + main
extra = r'''

# ----------------------------------------------------------------------------------------------------------------------
# REVISOR c1 R2.2: P8c = o web v2 SOBE, vive alguns segundos e MORRE (o supervisor o relanca: o pid do filho muda)
# ----------------------------------------------------------------------------------------------------------------------
def preparar_p8c(log):
    w = (SIMS / 'sim_web.py').read_text(encoding='utf-8')
    alvo = "if t.get('web_morre_ao_nascer'):\n    raise SystemExit(7)\n"
    assert w.count(alvo) == 1
    w = w.replace(alvo, alvo + "if t.get('web_morre_apos_s'):\n    time.sleep(float(t['web_morre_apos_s']))\n    raise SystemExit(7)\n")
    (SIMS / 'sim_web.py').write_text(w, encoding='utf-8')
    log['sim_web_p8c_sha16'] = sha(SIMS / 'sim_web.py')[:16]
    return log


def cen_P8c():
    def fn(sim, cfg_path, cfg, mont, antes):
        cfg8 = dict(cfg, esperar_inicio_s=12)
        p8 = ENS / 'config_P8c.json'
        p8.write_text(json.dumps(cfg8, ensure_ascii=False, indent=1), encoding='utf-8')
        t = json.loads((sim.dir / 'tarefa.json').read_text(encoding='utf-8'))
        t['web_morre_apos_s'] = 2.5
        sim.b._escrever_tarefa(t)
        r = run([TOOLS / 'implantar.py', '--config', p8, '--pular-mover-backups'])
        rp = recibo_impl_ultimo()
        rec = ler(rp)
        o = {'implantar': {'rc': r['rc'], 'status': rec['status'], 'diagnostico_reinicio': rec.get('diagnostico_reinicio'),
                           'stdout_fim': r['stdout'][-900:], 'acao_requerida': rec.get('acao_requerida')}}
        t['web_morre_apos_s'] = 0
        sim.b._escrever_tarefa(t)
        o['reverter'] = reverter(recibo=rp)
        o['alvos_apos_reverter'] = contar(alvos_estado())
        return o
    return com_sim('P8c', fn)


def main_rev22(sel):
    out = {'at': datetime.now().isoformat(timespec='seconds'), 'preparo': preparar_p8c(preparar_rev(preparar())), 'cenarios': {}}
    todos = {'K2': cen_K2, 'K3': cen_K3, 'K4': cen_K4, 'K6': cen_K6, 'P8': cen_P8,
             'K2b': cen_K2b, 'K2c': cen_K2c, 'K2d': cen_K2d, 'K3b': cen_K3b, 'K3r': cen_K3r, 'K4b': cen_K4b, 'K4c': cen_K4c,
             'K6b': cen_K6b, 'K6c': cen_K6c, 'P8b': cen_P8b, 'P8c': cen_P8c, 'CFG': lambda: cen_CFG()}
    nome = 's5_ensaio_rev22%s.json' % ('_' + '_'.join(sel) if sel else '')
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
'''
main_at = s.index("\nif __name__ == '__main__':")
s = s[:main_at] + extra + "\n\nif __name__ == '__main__':\n    main_rev22(sys.argv[1:])\n"
out = ME / 'scripts' / 's5_ensaio_rev22.py'
out.write_text(s, encoding='utf-8')
print(out.name, hashlib.sha256(out.read_bytes()).hexdigest()[:16])
for i, line in enumerate(s.splitlines(), 1):
    if ('R2_1' in line or 'r2_1' in line or 'R21' in line) and 'SRC21' not in line:
        print(i, line.strip()[:120])
