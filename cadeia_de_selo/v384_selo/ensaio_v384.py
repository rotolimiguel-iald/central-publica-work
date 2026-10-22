# -*- coding: utf-8 -*-
"""O ENSAIO da cadeia pos-rito v384, de ponta a ponta, contra o Nos SINTETICO e COPIAS das superficies reais -- NADA real e' tocado (conferido por sha256
antes/depois). Roda: montar o Nos sintetico -> o conferidor de ensaio (a unica linha do NOS trocada) -> leitura -> testar_formatos -> compactar (copia) ->
superficies (copia) -> superficies de novo (idempotencia) -> manifesto -> arquivar (pasta de ensaio) -> handoff (copias) -> registrar_resultado (JSON pre-validado,
NAO registrado) -> patch_arvore_indice (copias das ferramentas). NAO roda um.py, arvore_da_prova.py, atlas_indice.py nem porta_memoria.py.
Saida: ensaio_saidas\\ensaio_resultado_v384.json e o resumo na tela."""
import glob, hashlib, json, os, re, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v384 as A
NOS_S = os.path.join(HERE, 'ensaio_nos_sintetico'); CONF_E = os.path.join(HERE, 'conferidor_ensaio'); ENS = os.path.join(HERE, 'ensaio_superficies')
TOOLS_E = os.path.join(HERE, 'ensaio_tools'); ARQ_E = os.path.join(HERE, 'ensaio_arquivo'); SAI = os.path.join(HERE, 'ensaio_saidas')
HOR = os.path.join(HERE, 'ensaio_horarios_v384_SINTETICO.txt')
TOPICOS = ('missao-ultima-flag-um-py.md', 'central-de-patentes-estado.md', 'beta-e-a-regra-matriz-02out.md', 'regra-dos-dois-regimes.md', 'v382-custodia-suspensa.md', 'v384-pilar-quantico-gpu-02out.md')
REAIS = [os.path.join(A.NOS_REAL, f) for f in ('MEMORIA_DA_LINHAGEM.md', 'DESENHO_DO_FECHAMENTO_QG.md', 'A_PROVA_DA_QG_TGL_arvore.md', 'HANDOFF_v384_CUSTODIA.md')]
REAIS += [os.path.join(A.ATLAS_DIR_REAL, f) for f in ('TGL_ATLAS.md', 'TGL_INDICE_VIVO.md')]
REAIS += [os.path.join(A.UMEM_REAL, f) for f in ('MEMORY.md', 'MEMORY_2.md', 'handoff-v384-custodia.md') + TOPICOS]
REAIS += [os.path.join(A.TOOLS_REAL, f) for f in ('arvore_da_prova.py', 'atlas_indice.py', 'v384_incorporacao_manifesto.json', os.path.join('v384', 'AFERIDOR_v384.txt'))]
REAIS += [r'C:\IALD\MAPA_DE_ROTAS\rotas.jsonl', os.path.join(A.SEL, 'conferidor', 'conferencia_rito_v384.json'), os.path.join(A.SEL, 'v384_incorporacao_manifesto.json')]


def foto():
    d = {}
    for p in REAIS:
        if os.path.exists(p):
            h = hashlib.sha256()
            with open(p, 'rb') as f:
                for b in iter(lambda: f.read(1 << 20), b''):
                    h.update(b)
            d[p] = (os.path.getsize(p), h.hexdigest())
        else:
            d[p] = None
    return d


ENV_S = dict(os.environ, PYTHONIOENCODING='utf-8', V384_NOS=NOS_S, V384_CONF_DIR=CONF_E, V384_HORARIOS=HOR, V384_TOOLS=TOOLS_E, V384_ARQ_DEST=ARQ_E, V384_SAIDAS=SAI)
for k in ('V384_REMAP_DIR', 'V384_WRITE_ROOT', 'V384_UMEM', 'V384_ATLAS_DIR', 'V384_PIDF', 'V384_ESPERA_SEM_VIGIA', 'V384_RC', 'V384_ACEITO_PILAR_NAO_CONCLUIDO'):
    ENV_S.pop(k, None)
ENV_R = dict(ENV_S, V384_REMAP_DIR=ENS, V384_WRITE_ROOT=ENS)
RES = {'quando': time.strftime('%Y-%m-%d %H:%M:%S'), 'passos': []}


def roda(nome, args, env, cwd=HERE, aceita=(0,)):
    t0 = time.time()
    r = subprocess.run([sys.executable] + args, cwd=cwd, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (r.stdout + r.stderr).strip()
    open(os.path.join(SAI, 'ensaio_%s.out.txt' % nome), 'w', encoding='utf-8').write(out + '\n')
    RES['passos'].append({'passo': nome, 'rc': r.returncode, 's': round(time.time() - t0, 1), 'ultima': out.splitlines()[-1][:300] if out else ''})
    print('== %-22s rc=%s  %s' % (nome, r.returncode, (out.splitlines()[-1][:200] if out else '')), flush=True)
    if r.returncode not in aceita:
        print(out[-3000:]); raise SystemExit('ENSAIO PAROU em %s (rc %s)' % (nome, r.returncode))
    return out


os.makedirs(SAI, exist_ok=True)
F0 = foto()
roda('montar_nos', ['montar_nos_sintetico_v384.py'], ENV_S)
roda('preparar_conferidor', ['preparar_conferidor_ensaio_v384.py', CONF_E], ENV_S)
r = subprocess.run([sys.executable, 'conferir_rito_v384_ENSAIO.py'], cwd=CONF_E, env=ENV_S, capture_output=True, text=True, encoding='utf-8', errors='replace')
open(os.path.join(CONF_E, 'conferir_rito_v384_stdout.txt'), 'w', encoding='utf-8').write(r.stdout + r.stderr)
RES['conferidor'] = {'rc': r.returncode, 'ultima': r.stdout.strip().splitlines()[-1], 'ok': sum(1 for l in r.stdout.splitlines() if l.startswith('  [OK ]')), 'nao': sum(1 for l in r.stdout.splitlines() if l.startswith('  [NAO]'))}
print('== conferidor (ensaio)   rc=%s  %s  (OK %d, NAO %d)' % (r.returncode, RES['conferidor']['ultima'], RES['conferidor']['ok'], RES['conferidor']['nao']))
assert r.returncode == 0 and RES['conferidor']['ultima'] == 'TUDO BATE'
# as COPIAS das superficies reais (so leitura dos originais)
if os.path.isdir(ENS):
    shutil.rmtree(ENS)
os.makedirs(ENS)
for p in [os.path.join(A.NOS_REAL, 'MEMORIA_DA_LINHAGEM.md'), os.path.join(A.NOS_REAL, 'DESENHO_DO_FECHAMENTO_QG.md'), os.path.join(A.ATLAS_DIR_REAL, 'TGL_ATLAS.md')] + \
         [os.path.join(A.UMEM_REAL, f) for f in ('MEMORY.md', 'MEMORY_2.md') + TOPICOS]:
    shutil.copy2(p, os.path.join(ENS, os.path.basename(p))); assert open(p, 'rb').read() == open(os.path.join(ENS, os.path.basename(p)), 'rb').read()
ANTES = {f: os.path.getsize(os.path.join(ENS, f)) for f in os.listdir(ENS)}
# as COPIAS das ferramentas (o patch so toca as copias)
if os.path.isdir(TOOLS_E):
    shutil.rmtree(TOOLS_E)
os.makedirs(TOOLS_E)
for f in ('arvore_da_prova.py', 'atlas_indice.py'):
    shutil.copy2(os.path.join(A.TOOLS_REAL, f), os.path.join(TOOLS_E, f))
o = roda('leitura', ['leitura_v384.py'], ENV_S)
RES['leitura_problemas'] = o.splitlines()[-1]
roda('testar_formatos', ['testar_formatos_v384.py'], ENV_S)
roda('compactar_mede', ['compactar_memory_para_v384.py'], ENV_R)
roda('compactar_grava', ['compactar_memory_para_v384.py', '--gravar'], ENV_R)
roda('superficies', ['superficies_v384.py'], ENV_R)
roda('superficies_idemp', ['superficies_v384.py'], ENV_R)
roda('manifesto', ['manifesto_v384.py'], ENV_S)
if os.path.isdir(ARQ_E):
    shutil.rmtree(ARQ_E)
roda('arquivar', ['arquivar_v384.py'], ENV_S)
roda('handoff', ['handoff_v384.py'], ENV_R)
roda("handoff_idemp", ["handoff_v384.py"], ENV_R)
roda('registrar_json', ['registrar_resultado_v384.py'], ENV_S)
roda('patch_ferramentas', ['patch_arvore_indice_v384.py'], ENV_S)
roda('patch_idemp', ['patch_arvore_indice_v384.py'], ENV_S)
F1 = foto()
mud = [p for p in REAIS if F0[p] != F1[p]]
RES['reais_intocados'] = {'n_conferidos': len(REAIS), 'mudaram': mud, 'existiam': sum(1 for p in REAIS if F0[p]), 'ausentes_antes_e_depois': [os.path.basename(p) for p in REAIS if F0[p] is None and F1[p] is None]}
# o que o ensaio deixou nas copias
DEPOIS = {f: os.path.getsize(os.path.join(ENS, f)) for f in os.listdir(ENS) if not re.search(r'\.(bak|tmp)', f)}
RES['copias'] = {f: {'antes': ANTES.get(f), 'depois': DEPOIS[f], 'grep_v384': open(os.path.join(ENS, f), encoding='utf-8', errors='replace').read().count('v384')} for f in sorted(DEPOIS)}
mem = open(os.path.join(ENS, 'MEMORY.md'), encoding='utf-8').read(); mem2 = open(os.path.join(ENS, 'MEMORY_2.md'), encoding='utf-8').read()
RES['MEMORY_md_bytes'] = len(mem.encode('utf-8'))
orig_lines = open(os.path.join(A.UMEM_REAL, 'MEMORY.md'), encoding='utf-8').read().split('\n')
nao_mais = [l for l in orig_lines if l and l not in mem.split('\n')]
RES['linhas_do_indice_tocadas'] = len(nao_mais)
RES['tocadas_todas_verbatim_no_MEMORY_2'] = all(l in mem2 for l in nao_mais)
tools = {f: open(os.path.join(TOOLS_E, f), encoding='utf-8').read() for f in ('arvore_da_prova.py', 'atlas_indice.py')}
RES['ferramentas'] = {'arvore_linha_v384': tools['arvore_da_prova.py'].count('- **O PILAR QUÂNTICO (v384)'), 'atlas_manifesto_v384': tools['atlas_indice.py'].count('v384_incorporacao_manifesto'),
                      'atlas_V384TXT': tools['atlas_indice.py'].count('_V384TXT')}
import ast
for f, s in tools.items():
    ast.parse(s)
RES['numeros_do_core_sintetico_nos_textos'] = json.load(open(os.path.join(SAI, 'testar_formatos_v384.json'), encoding='utf-8'))['numeros_de_V_no_diario']
RES['ok'] = (not mud and RES['MEMORY_md_bytes'] <= 24000 and RES['tocadas_todas_verbatim_no_MEMORY_2'] and all(v for v in RES['numeros_do_core_sintetico_nos_textos'].values())
             and RES['ferramentas'] == {'arvore_linha_v384': 1, 'atlas_manifesto_v384': 2, 'atlas_V384TXT': 2})
open(os.path.join(SAI, 'ensaio_resultado_v384.json'), 'w', encoding='utf-8').write(json.dumps(RES, ensure_ascii=False, indent=1))
print(json.dumps({k: RES[k] for k in ('reais_intocados', 'MEMORY_md_bytes', 'linhas_do_indice_tocadas', 'tocadas_todas_verbatim_no_MEMORY_2', 'ferramentas')}, ensure_ascii=False, indent=1))
for f, v in RES['copias'].items():
    print('   %-38s %10s -> %10s B   v384 x%d' % (f, format(v['antes'] or 0, ','), format(v['depois'], ','), v['grep_v384']))
print('ENSAIO:', 'TUDO CERTO' if RES['ok'] else 'FALHOU', '->', os.path.join(SAI, 'ensaio_resultado_v384.json'))
sys.exit(0 if RES['ok'] else 1)
