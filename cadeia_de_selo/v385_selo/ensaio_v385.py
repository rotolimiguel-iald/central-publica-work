# -*- coding: utf-8 -*-
"""O ENSAIO da cadeia pos-rito v385, de ponta a ponta, contra o Nos SINTETICO e COPIAS das superficies reais -- NADA real e' tocado (conferido por sha256
antes/depois). Roda: montar o Nos sintetico -> o conferidor de ensaio (a unica linha do NOS trocada) -> leitura -> testar_formatos -> compactar (copia) ->
superficies (copia) -> superficies de novo (idempotencia) -> manifesto -> arquivar (pasta de ensaio) -> handoff (copias) -> registrar_resultado (JSON pre-validado,
NAO registrado) -> patch_arvore_indice (copias das ferramentas). NAO roda um.py, arvore_da_prova.py, atlas_indice.py nem porta_memoria.py.
Saida: ensaio_saidas\\ensaio_resultado_v385.json e o resumo na tela."""
import glob, hashlib, json, os, re, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v385 as A
NOS_S = os.path.join(HERE, 'ensaio_nos_sintetico'); CONF_E = os.path.join(HERE, 'conferidor_ensaio'); ENS = os.path.join(HERE, 'ensaio_superficies')
TOOLS_E = os.path.join(HERE, 'ensaio_tools'); ARQ_E = os.path.join(HERE, 'ensaio_arquivo'); SAI = os.path.join(HERE, 'ensaio_saidas')
HOR = os.path.join(HERE, 'ensaio_horarios_v385_SINTETICO.txt')
TOPICOS = ('missao-ultima-flag-um-py.md', 'central-de-patentes-estado.md', 'um-posto-jamais-pressuposto-e-h2-17set.md', 'v384-pilar-quantico-gpu-02out.md')
VAR = (sys.argv[1] if len(sys.argv) > 1 else 'BIT').upper(); assert VAR in ('BIT', 'DIFERENTE'), VAR   # a variante da reprodutibilidade no Nos sintetico
REAIS = [os.path.join(A.NOS_REAL, f) for f in ('MEMORIA_DA_LINHAGEM.md', 'DESENHO_DO_FECHAMENTO_QG.md', 'A_PROVA_DA_QG_TGL_arvore.md', 'HANDOFF_v385_CUSTODIA.md')]
REAIS += [os.path.join(A.ATLAS_DIR_REAL, f) for f in ('TGL_ATLAS.md', 'TGL_INDICE_VIVO.md')]
REAIS += [os.path.join(A.UMEM_REAL, f) for f in ('MEMORY.md', 'MEMORY_2.md', 'handoff-v385-custodia.md') + TOPICOS]
REAIS += [os.path.join(A.TOOLS_REAL, f) for f in ('arvore_da_prova.py', 'atlas_indice.py', 'v385_incorporacao_manifesto.json', os.path.join('v385', 'AFERIDOR_v385.txt'))]
REAIS += [r'C:\IALD\MAPA_DE_ROTAS\rotas.jsonl', os.path.join(A.SEL, 'conferidor', 'conferencia_rito_v385.json'), os.path.join(A.SEL, 'v385_incorporacao_manifesto.json')]


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


ENV_S = dict(os.environ, PYTHONIOENCODING='utf-8', V385_SINT_REPRO=VAR, V385_NOS=NOS_S, V385_CONF_DIR=CONF_E, V385_HORARIOS=HOR, V385_TOOLS=TOOLS_E, V385_ARQ_DEST=ARQ_E, V385_SAIDAS=SAI)
for k in ('V385_REMAP_DIR', 'V385_WRITE_ROOT', 'V385_UMEM', 'V385_ATLAS_DIR', 'V385_PIDF', 'V385_ESPERA_SEM_VIGIA', 'V385_RC', 'V385_ACEITO_PILAR_NAO_CONCLUIDO'):
    ENV_S.pop(k, None)
ENV_R = dict(ENV_S, V385_REMAP_DIR=ENS, V385_WRITE_ROOT=ENS)
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
roda('montar_nos', ['montar_nos_sintetico_v385.py'], ENV_S)
roda('preparar_conferidor', ['preparar_conferidor_ensaio_v385.py', CONF_E], ENV_S)
r = subprocess.run([sys.executable, 'conferir_rito_v385_ENSAIO.py'], cwd=CONF_E, env=ENV_S, capture_output=True, text=True, encoding='utf-8', errors='replace')
open(os.path.join(CONF_E, 'conferir_rito_v385_stdout.txt'), 'w', encoding='utf-8').write(r.stdout + r.stderr)
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
o = roda('leitura', ['leitura_v385.py'], ENV_S)
RES['leitura_problemas'] = o.splitlines()[-1]
roda('compactar_mede', ['compactar_memory_para_v385.py'], ENV_R)
roda('compactar_grava', ['compactar_memory_para_v385.py', '--gravar'], ENV_R)
roda('superficies', ['superficies_v385.py'], ENV_R)
roda('superficies_idemp', ['superficies_v385.py'], ENV_R)
roda('conferir_textos', ['conferir_textos_v385.py'], ENV_S)
roda('manifesto', ['manifesto_v385.py'], ENV_S)
if os.path.isdir(ARQ_E):
    shutil.rmtree(ARQ_E)
roda('arquivar', ['arquivar_v385.py'], ENV_S)
roda('handoff', ['handoff_v385.py'], ENV_R)
roda("handoff_idemp", ["handoff_v385.py"], ENV_R)
roda('registrar_json', ['registrar_resultado_v385.py'], ENV_S)
roda('patch_ferramentas', ['patch_arvore_indice_v385.py'], ENV_S)
roda('patch_idemp', ['patch_arvore_indice_v385.py'], ENV_S)
F1 = foto()
mud = [p for p in REAIS if F0[p] != F1[p]]
RES['reais_intocados'] = {'n_conferidos': len(REAIS), 'mudaram': mud, 'existiam': sum(1 for p in REAIS if F0[p]), 'ausentes_antes_e_depois': [os.path.basename(p) for p in REAIS if F0[p] is None and F1[p] is None]}
# o que o ensaio deixou nas copias
DEPOIS = {f: os.path.getsize(os.path.join(ENS, f)) for f in os.listdir(ENS) if not re.search(r'\.(bak|tmp)', f)}
RES['copias'] = {f: {'antes': ANTES.get(f), 'depois': DEPOIS[f], 'grep_v385': open(os.path.join(ENS, f), encoding='utf-8', errors='replace').read().count('v385')} for f in sorted(DEPOIS)}
mem = open(os.path.join(ENS, 'MEMORY.md'), encoding='utf-8').read(); mem2 = open(os.path.join(ENS, 'MEMORY_2.md'), encoding='utf-8').read()
RES['MEMORY_md_bytes'] = len(mem.encode('utf-8'))
orig_lines = open(os.path.join(A.UMEM_REAL, 'MEMORY.md'), encoding='utf-8').read().split('\n')
nao_mais = [l for l in orig_lines if l and l not in mem.split('\n')]
RES['linhas_do_indice_tocadas'] = len(nao_mais)
def _acrescimo_puro(old, novas):
    """(v385) a linha mudou SO por acrescimo -- o texto antigo inteiro fica na linha nova, com um trecho inserido num ponto (o marcador da missao na frente
    do texto; a marca do pilar no fim): nada se perdeu, e a regra dos dois arquivos nao exige a copia."""
    for nl in novas:
        if len(nl) > len(old) and any(nl.startswith(old[:k]) and nl.endswith(old[k:]) for k in range(len(old) + 1)):
            return True
    return False


_novas = mem.split('\n')
RES['tocadas_por_acrescimo_puro'] = [l[:80] for l in nao_mais if l not in mem2 and _acrescimo_puro(l, _novas)]
RES['tocadas_todas_verbatim_no_MEMORY_2'] = all((l in mem2) or _acrescimo_puro(l, _novas) for l in nao_mais)
tools = {f: open(os.path.join(TOOLS_E, f), encoding='utf-8').read() for f in ('arvore_da_prova.py', 'atlas_indice.py')}
RES['ferramentas'] = {'arvore_linha_v385': tools['arvore_da_prova.py'].count('- **O AXIOMA (v385)'), 'atlas_manifesto_v385': tools['atlas_indice.py'].count('v385_incorporacao_manifesto'),
                      'atlas_V385TXT': tools['atlas_indice.py'].count('_V385TXT')}
import ast
for f, s in tools.items():
    ast.parse(s)
RES['textos'] = json.load(open(os.path.join(SAI, 'conferir_textos_v385.json'), encoding='utf-8')); RES['variante'] = VAR
RES['ok'] = (not mud and RES['MEMORY_md_bytes'] <= 24000 and RES['tocadas_todas_verbatim_no_MEMORY_2'] and RES['textos']['ok'] is True
             and RES['ferramentas'] == {'arvore_linha_v385': 1, 'atlas_manifesto_v385': 2, 'atlas_V385TXT': 2})
open(os.path.join(SAI, 'ensaio_resultado_v385_%s.json' % VAR), 'w', encoding='utf-8').write(json.dumps(RES, ensure_ascii=False, indent=1))
print(json.dumps({k: RES[k] for k in ('reais_intocados', 'MEMORY_md_bytes', 'linhas_do_indice_tocadas', 'tocadas_todas_verbatim_no_MEMORY_2', 'ferramentas')}, ensure_ascii=False, indent=1))
for f, v in RES['copias'].items():
    print('   %-38s %10s -> %10s B   v385 x%d' % (f, format(v['antes'] or 0, ','), format(v['depois'], ','), v['grep_v385']))
print('ENSAIO:', 'TUDO CERTO' if RES['ok'] else 'FALHOU', '->', os.path.join(SAI, 'ensaio_resultado_v385.json'))
sys.exit(0 if RES['ok'] else 1)
