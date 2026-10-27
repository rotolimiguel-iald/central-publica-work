# -*- coding: utf-8 -*-
# STUB do harness (NAO e' a leitura da cadeia): monta a V minima que o fechar_v402.py usa, de ESPERADOS, do APLICADO_AO_CANONICO e do Nos do sandbox.
import glob, json, os
NOS = 'C:/IALD/Central de Patentes/work/cadeia_de_selo/v402_exame/final/sb8\\nos'
PK = 'C:/IALD/Central de Patentes/work/cadeia_de_selo/v402_exame/final/sb8\\work\\cadeia_de_selo\\v402'


def _aplicado():
    ps = sorted(glob.glob(os.path.join(PK, 'APLICADO_AO_CANONICO_*.json')))
    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]


def ler():
    import hashlib
    ap, app = _aplicado(); esp = json.load(open(os.path.join(PK, 'ESPERADOS_v402.json'), encoding='utf-8'))
    um = os.path.join(NOS, 'um.py'); sc = json.load(open(os.path.join(NOS, 'um_absoluto_selo_acom.json'), encoding='utf-8'))
    V = {'nos': NOS, 's16': esp['candidato_sha16'], 'umb': os.path.getsize(um), 'base16': ap['backups']['um.py']['sha16'], 'base_backup': ap['backups']['um.py']['backup'], 'escada_antes': esp['escada_v401_e_v402'][0], 'teor': '%d/%d' % (esp['escada'][1], esp['escada'][1]),
         'axiom_report_n': esp['axiom_report_esperado_min'], 'patches': 'stub', 'compl': 'COMPLETA', 'horarios': [], 'qg': esp['qg_closure_verdict'], 'conf_dm': '0/0', 'conf_np': '0/0', 'conf16': 'stub', 'servidor': 'stub', 'reg402': {'cunhagens_v402': {'ok': True}}, 'reg401': {'cunhagens_v401': {'ok': True}},
         'reg399': {'cunhagens_v399': {'ok': True}}, 'ponte': {'ok': True}, 'queda': {'ok': True}, 'esperanca': {'ok': True}, 'fal401': {'ok': True}, 'troca_dita': list(esp['troca_dita']), 'pedras': [], 'n_pedras': len(esp['pedras_sha256']), 'varr': {}, 'verbatins': {}, 'fd390': 'stub', 'pilar': {}, 'artigos': {}}
    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_selo_acom.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):
        V['h_' + k] = hashlib.sha256(open(os.path.join(NOS, k), 'rb').read()).hexdigest()[:16] if os.path.exists(os.path.join(NOS, k)) else 'AUSENTE'
    V['sidecar'] = {'ok': True, 'sha256': hashlib.sha256(open(os.path.join(NOS, 'um_absoluto_selo_acom.json'), 'rb').read()).hexdigest(), 'bytes': os.path.getsize(os.path.join(NOS, 'um_absoluto_selo_acom.json')), 'veredito': sc.get('veredito'), 'esquema': sc.get('esquema'), 'recusas': 0,
                    'objetos': {o['nome']: {'bytes': o.get('bytes'), 'sha256': o.get('sha256')} for o in sc.get('objetos', [])}}
    return V, []
