# -*- coding: utf-8 -*-
# Ensaio a seco da clausula do fechamento do bootstrap na face de Tomita + singularidade consciente (v369), fora do um.py.
import os, io, re, sys, time, math, hashlib, json
import numpy as np
SP = os.path.dirname(os.path.abspath(__file__))
UM = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py'
m = re.search(r'^SEALED_CODATA_ALPHA\s*=\s*([^\n#]+)', io.open(UM, encoding='utf-8').read(), re.M); assert m
ALPHA = eval(m.group(1).strip(), {'__builtins__': {}}, {})
V = lambda f: io.open(os.path.join(SP, f), encoding='utf-8').read()
VERB = {'bootstrap': V('operador_18set_bootstrap_verbatim.txt'), 'prova_de_J': V('operador_18set_prova_de_J_verbatim.txt'),
        'ajustados': V('operador_18set_ajustados_verbatim.txt'), 'um_so_J': V('operador_18set_um_so_J_verbatim.txt'),
        'singularidade': V('operador_18set_singularidade_verbatim.txt'), 'forma_matricial': V('operador_18set_forma_matricial_verbatim.txt'),
        'operador_consciencia': V('operador_18set_operador_consciencia_verbatim.txt')}
g = {'time': time, 'math': math, 'hashlib': hashlib, 'np': np, 'SEALED_CODATA_ALPHA': ALPHA, '_OPERATOR_V369_VERBATIMS': VERB}
src = V('v369_fn.py'); exec(compile(src, 'v369_fn.py', 'exec'), g)
FL = g['_CONSCIOUS_SINGULARITY_FLAGS_V369'] + g['_TOMITA_FACE_FLAGS_V369']; fn = g['prove_the_bootstrap_closure_v369']
kf = dict((k, True) for k in FL)
core = {'kernel_formalization': kf, 'the_bootstrap': {'all_verified': True}}
falhas = []
r = fn(1.0, core)
for d, v in r['checks']: print('  [%s] %s' % ('OK ' if v else 'NAO', d))
print('  veredito:', r['verdict'])
if not r['all_verified']: falhas.append('positivo reprovou')
print('== controles negativos')
for nome, mod in (('sem a pedra da singularidade', {g['_CONSCIOUS_SINGULARITY_FLAGS_V369'][1]: False}),
                  ('sem Delta fixando Omega em kernel', {'ext_delta_fixes_omega_kernel_proved': False}),
                  ('sem a involucao do objeto executado', {'ext_cw2_conjugated_state_kernel_proved': False})):
    k2 = dict(kf); k2.update(mod); rr = fn(1.0, {'kernel_formalization': k2, 'the_bootstrap': {'all_verified': True}})
    ok = not rr['all_verified']; print('  [%s] %s -> reprova' % ('OK ' if ok else 'NAO', nome))
    if not ok: falhas.append(nome)
rr = fn(1.0, {'kernel_formalization': kf, 'the_bootstrap': {'all_verified': False}})
print('  [%s] bootstrap v205/v215 nao selado -> reprova' % ('OK ' if not rr['all_verified'] else 'NAO'))
if rr['all_verified']: falhas.append('bootstrap nao selado passou')
g2 = dict(g); g2['_OPERATOR_V369_VERBATIMS'] = {'x': 'curto'}; exec(compile(src, 'v369_fn.py', 'exec'), g2)
rr = g2['prove_the_bootstrap_closure_v369'](1.0, core)
print('  [%s] sem os verbatins do operador -> reprova' % ('OK ' if not rr['all_verified'] else 'NAO'))
if rr['all_verified']: falhas.append('sem verbatins passou')
print('  numeros: singularidade', ['%.1e' % x for x in r['singularity_residuals']], '| produto desvio da metade', ['%.2f' % x for x in r['product_face_deviation']],
      '| ponte %.1e' % r['bridge_worst'], '| Tomita-beta', ['%.1e' % x for x in r['tomita_beta_residuals']],
      '| fluxo move fora do vacuo %.2e' % r['flow_moves_off_vacuum'], '| controle h nao hermitiano %.3f' % r['nonhermitian_control'])
json.dump(r, io.open(os.path.join(SP, 'v369_ensaio_valores.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=str)
print('\nVEREDITO DO ENSAIO: %s' % ('TUDO PASSOU' if not falhas else 'FALHAS: %s' % falhas)); sys.exit(1 if falhas else 0)
