# -*- coding: utf-8 -*-
"""ENSAIOS PONTUAIS do corretor (04/10), um por achado que o ensaio de ponta a ponta nao cobre sozinho. SO ensaio: tudo em v384_selo\\ensaio_corretor
(copias); nada real e' tocado (a foto de conferir_reais_intocados_v384.py confere antes/depois). Nao roda um.py, arvore, atlas, porta nem o trabalhador.
 [2]  arquivar: a lista permitida (nenhum arquivo de revisao_*, de ensaio_* nem de arvore SINTETICO) e a RECUSA visivel (rc 3, nada copiado) quando a
      pasta do conferidor vem de arvore marcada SINTETICO;
 [5]  registrar_resultado: com a ROTA ja no mapa (um modulo `rotas` de ENSAIO injetado em sys.modules), «nada gravado», rc 0, nenhum JSON escrito;
 [6]  leitura: um modulo da v383 que muda de all_verified, o balde das recusas, remaining_after_citation_v374 e o the_iald_index -> PROBLEMAS;
 [7]  leitura: o texto da leitura nao tem exec/compile; sem o resumo no registro (ramo 9), a leitura segue com n/d, dito, sem executar nada;
 [9]  superficies: com a custodia da v383 lida DIFERENTE na reexecucao (o git mudou), nada e' acrescentado de novo (o marcador e' o prefixo estavel);
 [10] compactar: a passada interrompida (MEMORY_2 trocado, MEMORY.md nao) -> a reexecucao NAO duplica o bloco no MEMORY_2.
Saida: ensaio_saidas\\ensaio_corretor_v384.json; rc 0 = tudo como esperado."""
import hashlib, json, os, re, runpy, shutil, subprocess, sys, types
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v384 as A
import variantes_pilar_v384 as VP
B = os.path.join(HERE, 'ensaio_corretor'); SAI = os.path.join(HERE, 'ensaio_saidas')
NOS_S = os.path.join(HERE, 'ensaio_nos_sintetico'); CONF_E = os.path.join(HERE, 'conferidor_ensaio'); HOR = os.path.join(HERE, 'ensaio_horarios_v384_SINTETICO.txt')
ENS = os.path.join(HERE, 'ensaio_superficies')
assert os.path.exists(os.path.join(NOS_S, A.MARCA_SINT)) and os.path.exists(os.path.join(ENS, 'MEMORY.md')), 'rode antes o ensaio_v384.py'
if os.path.isdir(B):
    shutil.rmtree(B)
os.makedirs(B); os.makedirs(SAI, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
R = {}


def env(**kw):
    e = {k: v for k, v in os.environ.items() if not k.startswith('V384_')}
    e.update(PYTHONIOENCODING='utf-8', V384_NOS=NOS_S, V384_CONF_DIR=CONF_E, V384_HORARIOS=HOR, V384_SAIDAS=os.path.join(B, 'saidas'), V384_ARQ_DEST=os.path.join(B, 'arquivo'))
    e.update({k: v for k, v in kw.items() if v is not None})
    return e


def roda(args, e, cwd=HERE):
    r = subprocess.run(args, cwd=cwd, env=e, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1200)
    return r.returncode, r.stdout + r.stderr


# [2] arquivar: a lista permitida + a recusa
rc, o = roda([sys.executable, 'arquivar_v384.py'], env(V384_ARQ_DEST=os.path.join(B, 'arquivo')))
man = json.load(open(os.path.join(B, 'arquivo', 'v384_selo', 'MANIFESTO_ARQUIVO_v384.json'), encoding='utf-8'))
sel = sorted(k for k in man['arquivos'] if k.startswith('v384_selo/'))
# so os scripts e saidas do TOPO e a pasta do conferidor entram; qualquer outra pasta (revisao_*, ensaio_*, corretor_saidas, Nos sinteticos) e' falha
ruins = [k for k in sel if (k.count('/') > 1 and not k.startswith('v384_selo/conferidor/')) or 'SINTETICO' in k.upper()]
CF = os.path.join(B, 'conf_sintetico'); shutil.copytree(CONF_E, CF); open(os.path.join(CF, A.MARCA_SINT), 'w', encoding='utf-8').write('SINTETICO -- teste da recusa do arquivar\n')
rc2, o2 = roda([sys.executable, 'arquivar_v384.py'], env(V384_ARQ_DEST=os.path.join(B, 'arquivo_recusa'), V384_CONF_DIR=CF))
R['2_arquivar'] = {'rc': rc, 'da_cadeia_v384_selo': len(sel), 'arquivos_da_cadeia': sel, 'de_arvore_sintetica_ou_revisao': ruins,
                   'recusa_rc': rc2, 'recusa_ultima': o2.strip().splitlines()[-1][:220], 'recusa_nada_copiado': not os.path.exists(os.path.join(B, 'arquivo_recusa'))}
R['2_arquivar']['ok'] = rc == 0 and not ruins and rc2 == 3 and R['2_arquivar']['recusa_nada_copiado']
# [5] registrar: a rota ja existe -> nada gravado, rc 0
WR = os.path.join(B, 'registrar_wrapper.py')
open(WR, 'w', encoding='utf-8').write(
    "import sys, types, runpy\n"
    "m = types.ModuleType('rotas'); m._le = lambda: [{'rota_id': 'quantica.pilar_v384_rodada_completa', 'tipo': 'ROTA', 'seq': 1}]\n"
    "def _nao(*a, **k):\n    raise SystemExit('ENSAIO: rotas._valida/registrar NAO podiam ser chamadas')\n"
    "m._valida = _nao; m.registrar = _nao\n"
    "sys.modules['rotas'] = m\n"
    "sys.argv = [%r]\n"
    "runpy.run_path(%r, run_name='__main__')\n" % (os.path.join(HERE, 'registrar_resultado_v384.py'), os.path.join(HERE, 'registrar_resultado_v384.py')))
rc, o = roda([sys.executable, WR], env())
R['5_registrar'] = {'rc': rc, 'ultima': o.strip().splitlines()[-1][:200], 'json_escrito': os.path.exists(os.path.join(B, 'saidas', 'registro_mapa_v384.json'))}
R['5_registrar']['ok'] = rc == 0 and 'ja existe; nada gravado' in o and not R['5_registrar']['json_escrito']
# [6] leitura: as guardas herdadas da v383
CODE = ("import sys, json; sys.path.insert(0, %r); import leitura_v384 as L; V, P = L.ler(); print(json.dumps({'P': P, 'n_av': V.get('n_av'), 'resumo': V.get('resumo_fonte'), "
        "'t2_points': V.get('t2_points'), 'neg': V.get('qp_negativos')}, ensure_ascii=False))" % HERE)
casos6 = {}
for nome, f in (('all_verified', lambda C, S: C['core']['void_floor_v12'].update(all_verified=True)),
                ('recusas', lambda C, S: S['not_sealed_this_run'].update(recusas_de_dado=S['not_sealed_this_run']['recusas_de_dado'][1:])),
                ('remaining_after_citation', lambda C, S: C['core']['qg_closure']['gate']['kernel_frontier'].update(remaining_after_citation_v374=['X'])),
                ('iald_index', lambda C, S: C['core']['the_iald_index'].update(all_verified=False)),
                ('sem_resumo_ramo9', lambda C, S: (C['core']['quantum_pillar_v384'].pop('summary'), C['core']['quantum_pillar_v384'].update(summary_error="KeyError('x') [SINTETICO]")))):
    N = VP.copia_nos(os.path.join(B, 'nos_' + nome))
    cp, spp = os.path.join(N, 'um_absoluto.json'), os.path.join(N, 'um_absoluto_selo.json')
    C = json.load(open(cp, encoding='utf-8')); S = json.load(open(spp, encoding='utf-8')); f(C, S)
    VP._w(cp, json.dumps(C, ensure_ascii=False, indent=1).encode('utf-8')); VP._w(spp, json.dumps(S, ensure_ascii=False, indent=2).encode('utf-8'))
    rc, o = roda([sys.executable, '-c', CODE], env(V384_NOS=N))
    casos6[nome] = json.loads(o.strip().splitlines()[-1]) if rc == 0 else {'erro': o[-800:]}
R['6_leitura_guardas_v383'] = {k: v.get('P', v) for k, v in casos6.items() if k != 'sem_resumo_ramo9'}
R['6_leitura_guardas_v383']['ok'] = (any('mudaram de all_verified' in p for p in casos6['all_verified'].get('P', [])) and any('recusas de dado' in p for p in casos6['recusas'].get('P', []))
                                     and any('remaining_after_citation_v374' in p for p in casos6['remaining_after_citation'].get('P', []))
                                     and any('the_iald_index nao selado' in p for p in casos6['iald_index'].get('P', [])))
# [7] a leitura nao executa codigo
src = open(os.path.join(HERE, 'leitura_v384.py'), encoding='utf-8').read()
s7 = casos6['sem_resumo_ramo9']
R['7_leitura_sem_exec'] = {'exec_ou_compile_no_texto': bool(re.search(r'(?<![\w.])(?:exec|compile|eval)\(', src)), 'sem_resumo': s7}
R['7_leitura_sem_exec']['ok'] = (not R['7_leitura_sem_exec']['exec_ou_compile_no_texto'] and s7.get('P') == [] and s7.get('t2_points') == 'n/d'
                                 and 'AUSENTE no registro do core' in str(s7.get('resumo')) and 'nada recalculado' in str(s7.get('resumo')))
# [9] superficies: a reexecucao com a custodia da v383 lida diferente nao acrescenta de novo
D9 = os.path.join(B, 'sup_idem'); shutil.copytree(ENS, D9, ignore=shutil.ignore_patterns('*.bak_*', '*.tmp*'))
antes9 = {f: sha(os.path.join(D9, f)) for f in os.listdir(D9)}
W9 = os.path.join(B, 'superficies_wrapper.py')
open(W9, 'w', encoding='utf-8').write(
    "import sys, runpy\nsys.path.insert(0, %r)\nimport leitura_v384 as L\n_ler = L.ler\n"
    "def ler():\n    V, P = _ler(); V['v383_commit'] = 'abcd1234 custodia(v383): ENSAIO -- a custodia lida diferente na reexecucao'; return V, P\n"
    "L.ler = ler\nsys.argv = [%r]\nrunpy.run_path(%r, run_name='__main__')\n" % (HERE, os.path.join(HERE, 'superficies_v384.py'), os.path.join(HERE, 'superficies_v384.py')))
rc, o = roda([sys.executable, W9], env(V384_REMAP_DIR=D9, V384_WRITE_ROOT=D9))
depois9 = {f: sha(os.path.join(D9, f)) for f in os.listdir(D9) if not re.search(r'\.(bak|tmp)', f)}
R['9_superficies_marcador_estavel'] = {'rc': rc, 'ultima': o.strip().splitlines()[-1][:200], 'nada_mudou': all(antes9.get(f) == h for f, h in depois9.items()),
                                       'central_tem_1_bloco_v384': open(os.path.join(D9, 'central-de-patentes-estado.md'), encoding='utf-8').read().count('— v384 SELADA (')}
R['9_superficies_marcador_estavel']['ok'] = rc == 0 and 'NADA A GRAVAR' in o and R['9_superficies_marcador_estavel']['nada_mudou'] and R['9_superficies_marcador_estavel']['central_tem_1_bloco_v384'] == 1
# [10] compactar: a passada interrompida nao duplica o bloco no MEMORY_2
D10a = os.path.join(B, 'comp_inteira'); D10b = os.path.join(B, 'comp_interrompida'); os.makedirs(D10a); os.makedirs(D10b)
for f in ('MEMORY.md', 'MEMORY_2.md'):
    shutil.copyfile(os.path.join(A.UMEM_REAL, f), os.path.join(D10a, f))
rca, oa = roda([sys.executable, 'compactar_memory_para_v384.py', '--gravar'], env(V384_REMAP_DIR=D10a, V384_WRITE_ROOT=D10a))
shutil.copyfile(os.path.join(A.UMEM_REAL, 'MEMORY.md'), os.path.join(D10b, 'MEMORY.md'))          # o MEMORY.md NAO trocado
shutil.copyfile(os.path.join(D10a, 'MEMORY_2.md'), os.path.join(D10b, 'MEMORY_2.md'))             # o MEMORY_2 JA trocado (a passada caiu entre as duas trocas)
m2_antes = sha(os.path.join(D10b, 'MEMORY_2.md'))
rcb, ob = roda([sys.executable, 'compactar_memory_para_v384.py', '--gravar'], env(V384_REMAP_DIR=D10b, V384_WRITE_ROOT=D10b))
CAB = 'linhas do MEMORY.md tocadas pela compactação da v384'
R['10_compactar_interrompida'] = {'rc_inteira': rca, 'rc_reexecucao': rcb, 'disse_que_ja_tinha': 'JA tem o bloco verbatim' in ob,
                                  'MEMORY_2_inalterado': sha(os.path.join(D10b, 'MEMORY_2.md')) == m2_antes,
                                  'cabecalhos_no_MEMORY_2': open(os.path.join(D10b, 'MEMORY_2.md'), encoding='utf-8').read().count(CAB),
                                  'MEMORY_md_igual_ao_da_passada_inteira': sha(os.path.join(D10b, 'MEMORY.md')) == sha(os.path.join(D10a, 'MEMORY.md')),
                                  'MEMORY_md_bytes': os.path.getsize(os.path.join(D10b, 'MEMORY.md'))}
x = R['10_compactar_interrompida']
x['ok'] = rca == 0 and rcb == 0 and x['disse_que_ja_tinha'] and x['MEMORY_2_inalterado'] and x['cabecalhos_no_MEMORY_2'] == 1 and x['MEMORY_md_igual_ao_da_passada_inteira']
R['tudo_ok'] = all(v.get('ok') for v in R.values() if isinstance(v, dict))
open(os.path.join(SAI, 'ensaio_corretor_v384.json'), 'w', encoding='utf-8').write(json.dumps(R, ensure_ascii=False, indent=1))
for k, v in R.items():
    if isinstance(v, dict):
        print('[%s] %s | %s' % (k, 'OK' if v.get('ok') else 'FALHOU', json.dumps({kk: vv for kk, vv in v.items() if kk not in ('arquivos_da_cadeia', 'ok')}, ensure_ascii=False)[:600]))
print('ENSAIO DO CORRETOR:', 'TUDO CERTO' if R['tudo_ok'] else 'FALHOU')
sys.exit(0 if R['tudo_ok'] else 1)
