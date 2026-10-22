# -*- coding: utf-8 -*-
"""O ENSAIO da cadeia pos-rito v386, de ponta a ponta, contra o Nos SINTETICO e COPIAS das superficies reais -- NADA real e' tocado (conferido por sha256
antes/depois; o rito v386 REAL pode estar rodando ao lado: o ensaio nao le os arquivos que ele grava). Dois modos (argumento):
  AINDA_V385 -- o estado ATUAL do Nos (selo v385; o rito v386 nao acabou): montar -> espera (lancador FINGIDO vivo; tempo esgotado em poucos segundos ->
               rc 4, nada feito) -> leitura (PROBLEMAS, rc 2) -> superficies (RECUSA, rc 2; as copias intactas) -> conferidor de ensaio (NAO BATE, rc 1).
  V386 (padrao) -- o selo v386 SINTETICO: montar -> conferidor de ensaio (TUDO BATE) -> leitura -> compactar (copia) -> superficies (copia) -> superficies de
               novo (idempotencia) -> conferir_textos -> manifesto -> arquivar (pasta de ensaio) -> handoff (copias) x2 -> registrar_resultado (JSON, NAO
               registrado) -> patch_arvore_indice (copias das ferramentas) x2. NAO roda um.py, arvore_da_prova.py, atlas_indice.py nem porta_memoria.py.
Saida: ensaio_saidas\\ensaio_resultado_v386_<MODO>.json e o resumo na tela."""
import glob, hashlib, json, os, re, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v386 as A
NOS_S = os.path.join(HERE, 'ensaio_nos_sintetico'); CONF_E = os.path.join(HERE, 'conferidor_ensaio'); ENS = os.path.join(HERE, 'ensaio_superficies')
TOOLS_E = os.path.join(HERE, 'ensaio_tools'); ARQ_E = os.path.join(HERE, 'ensaio_arquivo'); SAI = os.path.join(HERE, 'ensaio_saidas')
HOR = os.path.join(HERE, 'ensaio_horarios_v386_SINTETICO.txt'); PIDF_E = os.path.join(HERE, 'ensaio_rito_v386_SINTETICO.pid')
TOPICOS = ('missao-ultima-flag-um-py.md', 'central-de-patentes-estado.md', 'verbo-selecao-da-acao-05out.md', 'ramo-b-reaberto-05out.md', 'v384-pilar-quantico-gpu-02out.md')
MODO = (sys.argv[1] if len(sys.argv) > 1 else 'V386').upper(); assert MODO in ('V386', 'AINDA_V385'), MODO
REAIS = [os.path.join(A.NOS_REAL, f) for f in ('MEMORIA_DA_LINHAGEM.md', 'DESENHO_DO_FECHAMENTO_QG.md', 'A_PROVA_DA_QG_TGL_arvore.md', 'HANDOFF_v386_CUSTODIA.md', 'HANDOFF_v385_CUSTODIA.md', 'rodada_v385_stdout.txt')]
REAIS += [os.path.join(A.ATLAS_DIR_REAL, f) for f in ('TGL_ATLAS.md', 'TGL_INDICE_VIVO.md')]
REAIS += [os.path.join(A.UMEM_REAL, f) for f in ('MEMORY.md', 'MEMORY_2.md', 'handoff-v386-custodia.md', 'handoff-v385-custodia.md') + TOPICOS]
REAIS += [A.HAJA_LUZ_REAL]
REAIS += [os.path.join(A.TOOLS_REAL, f) for f in ('arvore_da_prova.py', 'atlas_indice.py', 'v386_incorporacao_manifesto.json', 'v385_incorporacao_manifesto.json', os.path.join('v386', 'CONSTRUIR_v386_resultado.json'))]
REAIS += [r'C:\IALD\MAPA_DE_ROTAS\rotas.jsonl', os.path.join(A.SEL, 'conferidor', 'conferencia_rito_v386.json'), os.path.join(A.SEL, 'v386_incorporacao_manifesto.json')]
REAIS += [os.path.join(A.PRDIR_B, f) for f in ('PREREGISTRO_RAMO_B_RINGDOWN_V1.json', 'PREREGISTRO_RAMO_B_RINGDOWN_V1.md', 'V1_RAMO_B_HASHES.json', 'PODER_CEGO_RAMO_B_v2.json', 'poder_cego_ramo_b_v2.py', 'gerar_preregistro_ramo_b_05out.py')]
REAIS += [os.path.join(A.PK, f) for f in ('ESPERADOS_v386.json', 'CANDIDATO_v386.json', 'conferir_rito_v386.py', 'um_v386_candidato.py')]
REAIS += [os.path.join(A.DAT, f) for f in ('VERBO_operador_05out.txt', 'RESPOSTAS_operador_05out.txt', 'RESPOSTAS_operador_05out.json', os.path.join('ramo_b', 'DECISAO_OPERADOR_RAMO_B_05out.json'))]


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


ENV_S = dict(os.environ, PYTHONIOENCODING='utf-8', V386_SINT_MODO=MODO, V386_NOS=NOS_S, V386_CONF_DIR=CONF_E, V386_HORARIOS=HOR, V386_TOOLS=TOOLS_E, V386_ARQ_DEST=ARQ_E, V386_SAIDAS=SAI, V386_PIDF=PIDF_E)
for k in ('V386_REMAP_DIR', 'V386_WRITE_ROOT', 'V386_UMEM', 'V386_ATLAS_DIR', 'V386_HAJA_LUZ', 'V386_ESPERA_SEM_VIGIA', 'V386_ESPERA_LANCADOR_FINGE', 'V386_RC', 'V386_ACEITO_PILAR_NAO_CONCLUIDO'):
    ENV_S.pop(k, None)
ENV_R = dict(ENV_S, V386_REMAP_DIR=ENS, V386_WRITE_ROOT=ENS)
RES = {'quando': time.strftime('%Y-%m-%d %H:%M:%S'), 'modo': MODO, 'passos': []}


def roda(nome, args, env, cwd=HERE, aceita=(0,)):
    t0 = time.time()
    r = subprocess.run([sys.executable] + args, cwd=cwd, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (r.stdout + r.stderr).strip()
    open(os.path.join(SAI, 'ensaio_%s_%s.out.txt' % (MODO, nome)), 'w', encoding='utf-8').write(out + '\n')
    RES['passos'].append({'passo': nome, 'rc': r.returncode, 's': round(time.time() - t0, 1), 'ultima': out.splitlines()[-1][:300] if out else ''})
    print('== %-22s rc=%s  %s' % (nome, r.returncode, (out.splitlines()[-1][:200] if out else '')), flush=True)
    if r.returncode not in aceita:
        print(out[-3000:]); raise SystemExit('ENSAIO PAROU em %s (rc %s; esperado %s)' % (nome, r.returncode, aceita))
    return out


def copias():
    if os.path.isdir(ENS):
        shutil.rmtree(ENS)
    os.makedirs(ENS)
    for p in [os.path.join(A.NOS_REAL, 'MEMORIA_DA_LINHAGEM.md'), os.path.join(A.NOS_REAL, 'DESENHO_DO_FECHAMENTO_QG.md'), os.path.join(A.ATLAS_DIR_REAL, 'TGL_ATLAS.md'), A.HAJA_LUZ_REAL] + \
             [os.path.join(A.UMEM_REAL, f) for f in ('MEMORY.md', 'MEMORY_2.md') + TOPICOS]:
        shutil.copy2(p, os.path.join(ENS, os.path.basename(p))); assert open(p, 'rb').read() == open(os.path.join(ENS, os.path.basename(p)), 'rb').read()
    return {f: os.path.getsize(os.path.join(ENS, f)) for f in os.listdir(ENS)}


os.makedirs(SAI, exist_ok=True)
F0 = foto()
roda('montar_nos', ['montar_nos_sintetico_v386.py'], ENV_S)
if MODO == 'AINDA_V385':
    # (1) a espera: o lancador FINGIDO vivo (o real nunca e' lido aqui), tempo esgotado em 3 s -> rc 4, nada feito
    ENV_W = dict(ENV_S, V386_ESPERA_SEM_VIGIA='1', V386_ESPERA_LANCADOR_FINGE='VIVO', V386_ESPERA_MAX_S='3', V386_ESPERA_PASSO_S='1')
    o = roda('espera_tempo_esgotado', ['espera_rito_v386.py'], ENV_W, aceita=(4,))
    RES['espera'] = o.splitlines()[-1]
    # (2) a leitura: PROBLEMAS (o selo e' v385; sem RITO_RC; sem os registros v386)
    o = roda('leitura_detecta', ['leitura_v386.py'], ENV_S, aceita=(2,))
    RES['leitura_problemas'] = o.splitlines()[-1][:1500]
    assert 'selo.um_version != v386' in RES['leitura_problemas'] and 'rc do rito nao lido como 0' in RES['leitura_problemas']
    # (3) as superficies: RECUSA, nada escrito nas copias
    ANTES = copias()
    o = roda('superficies_recusa', ['superficies_v386.py'], ENV_R, aceita=(2,))
    DEPOIS = {f: os.path.getsize(os.path.join(ENS, f)) for f in os.listdir(ENS)}
    RES['copias_intactas'] = (ANTES == DEPOIS)
    assert RES['copias_intactas'], (ANTES, DEPOIS)
    o = roda('handoff_recusa', ['handoff_v386.py'], ENV_R, aceita=(2,))
    o = roda('manifesto_recusa', ['manifesto_v386.py'], ENV_S, aceita=(2,))
    # (4) o conferidor de ensaio: NAO BATE (rc 1)
    roda('preparar_conferidor', ['preparar_conferidor_ensaio_v386.py', CONF_E], ENV_S)
    r = subprocess.run([sys.executable, 'conferir_rito_v386_ENSAIO.py'], cwd=CONF_E, env=ENV_S, capture_output=True, text=True, encoding='utf-8', errors='replace')
    open(os.path.join(CONF_E, 'conferir_rito_v386_stdout.txt'), 'w', encoding='utf-8').write(r.stdout + r.stderr)
    RES['conferidor'] = {'rc': r.returncode, 'ultima': (r.stdout.strip().splitlines() or [''])[-1], 'ok': sum(1 for l in r.stdout.splitlines() if l.startswith('  [OK ]')), 'nao': sum(1 for l in r.stdout.splitlines() if l.startswith('  [NAO]'))}
    print('== conferidor (ensaio)   rc=%s  %s  (OK %d, NAO %d)' % (r.returncode, RES['conferidor']['ultima'], RES['conferidor']['ok'], RES['conferidor']['nao']))
    assert r.returncode == 1 and RES['conferidor']['ultima'] == 'NAO BATE'
    F1 = foto()
    mud = [p for p in REAIS if F0[p] != F1[p]]
    RES['reais_intocados'] = {'n_conferidos': len(REAIS), 'mudaram': mud, 'existiam': sum(1 for p in REAIS if F0[p])}
    RES['ok'] = (not mud and RES['copias_intactas'])
    open(os.path.join(SAI, 'ensaio_resultado_v386_%s.json' % MODO), 'w', encoding='utf-8').write(json.dumps(RES, ensure_ascii=False, indent=1))
    print(json.dumps({k: RES[k] for k in ('reais_intocados', 'copias_intactas', 'espera', 'conferidor')}, ensure_ascii=False, indent=1))
    print('ENSAIO (%s): %s -> o rito ainda nao selou a v386: a cadeia PARA LIMPA, nada escrito' % (MODO, 'TUDO CERTO' if RES['ok'] else 'FALHOU'))
    sys.exit(0 if RES['ok'] else 1)
roda('preparar_conferidor', ['preparar_conferidor_ensaio_v386.py', CONF_E], ENV_S)
r = subprocess.run([sys.executable, 'conferir_rito_v386_ENSAIO.py'], cwd=CONF_E, env=ENV_S, capture_output=True, text=True, encoding='utf-8', errors='replace')
open(os.path.join(CONF_E, 'conferir_rito_v386_stdout.txt'), 'w', encoding='utf-8').write(r.stdout + r.stderr)
RES['conferidor'] = {'rc': r.returncode, 'ultima': (r.stdout.strip().splitlines() or [''])[-1], 'ok': sum(1 for l in r.stdout.splitlines() if l.startswith('  [OK ]')), 'nao': sum(1 for l in r.stdout.splitlines() if l.startswith('  [NAO]'))}
print('== conferidor (ensaio)   rc=%s  %s  (OK %d, NAO %d)' % (r.returncode, RES['conferidor']['ultima'], RES['conferidor']['ok'], RES['conferidor']['nao']))
if not (r.returncode == 0 and RES['conferidor']['ultima'] == 'TUDO BATE'):
    print(r.stdout[-4000:]); raise SystemExit('ENSAIO PAROU no conferidor')
ANTES = copias()
if os.path.isdir(TOOLS_E):
    shutil.rmtree(TOOLS_E)
os.makedirs(TOOLS_E)
for f in ('arvore_da_prova.py', 'atlas_indice.py'):
    shutil.copy2(os.path.join(A.TOOLS_REAL, f), os.path.join(TOOLS_E, f))
o = roda('leitura', ['leitura_v386.py'], ENV_S)
RES['leitura_problemas'] = o.splitlines()[-1]
roda('compactar_mede', ['compactar_memory_para_v386.py'], ENV_R)
roda('compactar_grava', ['compactar_memory_para_v386.py', '--gravar'], ENV_R)
roda('superficies', ['superficies_v386.py'], ENV_R)
roda('superficies_idemp', ['superficies_v386.py'], ENV_R)
roda('conferir_textos', ['conferir_textos_v386.py'], ENV_S)
roda('manifesto', ['manifesto_v386.py'], ENV_S)
if os.path.isdir(ARQ_E):
    shutil.rmtree(ARQ_E)
roda('arquivar', ['arquivar_v386.py'], ENV_S)
roda('handoff', ['handoff_v386.py'], ENV_R)
roda('handoff_idemp', ['handoff_v386.py'], ENV_R)
roda('registrar_json', ['registrar_resultado_v386.py'], ENV_S)
roda('patch_ferramentas', ['patch_arvore_indice_v386.py'], ENV_S)
roda('patch_idemp', ['patch_arvore_indice_v386.py'], ENV_S)
F1 = foto()
mud = [p for p in REAIS if F0[p] != F1[p]]
RES['reais_intocados'] = {'n_conferidos': len(REAIS), 'mudaram': mud, 'existiam': sum(1 for p in REAIS if F0[p]), 'ausentes_antes_e_depois': [os.path.basename(p) for p in REAIS if F0[p] is None and F1[p] is None]}
DEPOIS = {f: os.path.getsize(os.path.join(ENS, f)) for f in os.listdir(ENS) if not re.search(r'\.(bak|tmp)', f)}
RES['copias'] = {f: {'antes': ANTES.get(f), 'depois': DEPOIS[f], 'grep_v386': open(os.path.join(ENS, f), encoding='utf-8', errors='replace').read().count('v386')} for f in sorted(DEPOIS)}
mem = open(os.path.join(ENS, 'MEMORY.md'), encoding='utf-8').read(); mem2 = open(os.path.join(ENS, 'MEMORY_2.md'), encoding='utf-8').read()
RES['MEMORY_md_bytes'] = len(mem.encode('utf-8'))
orig_lines = open(os.path.join(A.UMEM_REAL, 'MEMORY.md'), encoding='utf-8').read().split('\n')
nao_mais = [l for l in orig_lines if l and l not in mem.split('\n')]
RES['linhas_do_indice_tocadas'] = len(nao_mais)


def _acrescimo_puro(old, novas):
    for nl in novas:
        if len(nl) > len(old) and any(nl.startswith(old[:k]) and nl.endswith(old[k:]) for k in range(len(old) + 1)):
            return True
    return False


_novas = mem.split('\n')
RES['tocadas_por_acrescimo_puro'] = [l[:80] for l in nao_mais if l not in mem2 and _acrescimo_puro(l, _novas)]
RES['tocadas_todas_verbatim_no_MEMORY_2'] = all((l in mem2) or _acrescimo_puro(l, _novas) for l in nao_mais)
tools = {f: open(os.path.join(TOOLS_E, f), encoding='utf-8').read() for f in ('arvore_da_prova.py', 'atlas_indice.py')}
RES['ferramentas'] = {'arvore_linha_v386': tools['arvore_da_prova.py'].count('- **O VERBO SELECIONA (v386)'), 'atlas_manifesto_v386': tools['atlas_indice.py'].count('v386_incorporacao_manifesto'),
                      'atlas_V386TXT': tools['atlas_indice.py'].count('_V386TXT')}
import ast
for f, s in tools.items():
    ast.parse(s)
RES['textos'] = json.load(open(os.path.join(SAI, 'conferir_textos_v386.json'), encoding='utf-8'))
RES['arquivo'] = json.load(open(os.path.join(ARQ_E, 'v386_selo', 'MANIFESTO_ARQUIVO_v386.json'), encoding='utf-8'))
RES['arquivo'] = {'n_arquivos': len(RES['arquivo']['arquivos']), 'bytes': sum(v['bytes'] for v in RES['arquivo']['arquivos'].values()), 'n_nao_arquivados': len(RES['arquivo']['nao_arquivado'])}
RES['registro_mapa'] = [(r['tipo'], r['rota_id']) for r in json.load(open(os.path.join(SAI, 'registro_mapa_v386.json'), encoding='utf-8'))]
RES['ok'] = (not mud and RES['MEMORY_md_bytes'] <= 24000 and RES['tocadas_todas_verbatim_no_MEMORY_2'] and RES['textos']['ok'] is True
             and RES['ferramentas'] == {'arvore_linha_v386': 1, 'atlas_manifesto_v386': 2, 'atlas_V386TXT': 2})
open(os.path.join(SAI, 'ensaio_resultado_v386_%s.json' % MODO), 'w', encoding='utf-8').write(json.dumps(RES, ensure_ascii=False, indent=1))
print(json.dumps({k: RES[k] for k in ('reais_intocados', 'MEMORY_md_bytes', 'linhas_do_indice_tocadas', 'tocadas_todas_verbatim_no_MEMORY_2', 'ferramentas', 'arquivo', 'registro_mapa')}, ensure_ascii=False, indent=1))
for f, v in RES['copias'].items():
    print('   %-38s %10s -> %10s B   v386 x%d' % (f, format(v['antes'] or 0, ','), format(v['depois'], ','), v['grep_v386']))
print('ENSAIO (%s):' % MODO, 'TUDO CERTO' if RES['ok'] else 'FALHOU', '->', os.path.join(SAI, 'ensaio_resultado_v386_%s.json' % MODO))
sys.exit(0 if RES['ok'] else 1)
