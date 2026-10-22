# -*- coding: utf-8 -*-
"""Resume runs/s5_ensaio_rev22.json: campos-chave por cenario (so leitura)."""
import json
import sys
from pathlib import Path

ME = Path(__file__).resolve().parents[1]
d = json.loads((ME / 'runs' / 's5_ensaio_rev22.json').read_text(encoding='utf-8'))


def pega(o, *ks):
    for k in ks:
        if isinstance(o, dict):
            o = o.get(k)
        else:
            return None
    return o


def cur(s, n=330):
    return None if s is None else (s if len(str(s)) <= n else str(s)[:n] + '...')


out = {}
for nome, c in d['cenarios'].items():
    r = {'segundos': c.get('segundos')}
    if 'excecao' in c:
        r['EXCECAO'] = c['excecao'][-600:]
        out[nome] = r
        continue
    r['banco_igual'] = c.get('banco_igual_ao_original')
    r['lib_le'] = c.get('lib_le_o_banco')
    cf = c.get('comparacao_final')
    r['comparacao_final'] = cur(json.dumps(cf, ensure_ascii=False, default=str), 200) if cf else None
    r['tmp_orfaos'] = c.get('tmp_orfaos_final')
    r['sim_final'] = cur(json.dumps(c.get('estado_sim_final'), ensure_ascii=False, default=str), 260)
    for k in ('implantar', 'reverter', 'reverter_1', 'reverter_2', 'reverter_k3', 'reverter_normal', 'reverter_config',
              'reverter_config_de_novo', 'dry_run_antes', 'dry_run_depois', 'reverter_config_dry_run'):
        v = c.get(k)
        if isinstance(v, dict):
            r[k] = {kk: cur(json.dumps(vv, ensure_ascii=False, default=str) if not isinstance(vv, str) else vv)
                    for kk, vv in v.items() if kk in ('rc', 'status', 'falhas', 'app_religado', 'acao_requerida', 'diagnostico_reinicio',
                                                      'diz_app_parado', 'stdout_fim', 'passos', 'stdout', 'stderr_fim', 'ok')}
    for k in ('trava_implantar_ve_pendente', 'alvos_apos_reverter', 'alvos_apos_reverter_1', 'alvos_apos_reverter_2',
              'alvos_apos_reverter_k3', 'alvos_apos_reverter_normal', 'sim_apos_reverter_1', 'sim_apos_reverter_k3',
              'alvos_apos', 'sim_apos_dry_run_reverter'):
        if k in c:
            r[k] = cur(json.dumps(c[k], ensure_ascii=False, default=str), 220)
    out[nome] = r
Path(ME / 'runs' / 's7_resumo_ensaio.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
sel = sys.argv[1:] or list(out)
for n in sel:
    print('=====', n)
    print(json.dumps(out[n], ensure_ascii=False, indent=1))
