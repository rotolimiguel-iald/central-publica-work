# -*- coding: utf-8 -*-
"""O ENSAIO DAS GUARDAS do chain_pos_rito_v384.sh, com STUBS (sem rodar arvore_da_prova.py, atlas_indice.py nem porta_memoria.py; sem tocar nada real).
Monta, por cenario, uma copia do chain com SO o bloco CONFIG trocado (conferido por diff: o resto e' identico byte a byte), um Nos de teste (o Nos SINTETICO,
por hardlink nos arquivos grandes que nao mudam), copias das superficies/ferramentas, e stubs que so acrescentam «STUB v384» nos arquivos de teste.
Cenarios: FELIZ (ate o FIM), UMPY_ERRADO, RC_1, SEM_LINHA_FINAL, TRACEBACK, TEOREMAS, SELO_AUSENTE, CONFERIDOR_REPROVA (artigo sem a nota),
SO_PILAR_REPROVA (o terceiro balde com o pilar: o diagnostico diz «SO itens do pilar»), SO_PILAR_ACEITO_MAS_LEITURA_PARA (o aceite nomeado nao passa a leitura),
LEITURA_PARA (o stdout com outro veredito do pilar: o conferidor nao le o stdout, a leitura le). Em cada falha: o rc, a linha PARADA e que NADA foi escrito
nas superficies de teste (sha256 antes/depois).
CORRETOR (04/10): + a 2a passada do FELIZ na mesma pasta (idempotente ate o FIM; o manifesto anterior em TOOLS vai a backup de bytes); + um cenario de PONTA
A PONTA POR CLASSE do pilar (variantes_pilar_v384.CLASSES): sem o aceite PARA no conferidor com «SO itens do pilar: True»; com o aceite nomeado (o sha16 que
o diagnostico imprimiu) vai ao FIM; o gravado diz a classe e o aceite e nenhuma frase de sucesso fora do ramo 9; + a ESPERA com um lancador de teste (vivo,
morto com o .pid velho, sem .pid): o horario de fim ausente com o lancador fora nao trava; sem RITO_RC com o lancador fora e' rc 5; vivo, espera.
Saida: ensaio_saidas\\ensaio_guardas_v384.json."""
import hashlib, json, os, re, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v384 as A
import variantes_pilar_v384 as VP
import textos_v384 as TX
BASE = os.path.join(HERE, 'ensaio_guardas'); NOS_S = os.path.join(HERE, 'ensaio_nos_sintetico'); CONF_E = os.path.join(HERE, 'conferidor_ensaio')
SAI = os.path.join(HERE, 'ensaio_saidas'); BASH = shutil.which('sh') or r'C:\Program Files\Git\usr\bin\sh.exe'
assert os.path.exists(os.path.join(NOS_S, A.MARCA_SINT)) and os.path.exists(os.path.join(CONF_E, 'conferir_rito_v384_ENSAIO.py')), 'rode antes o ensaio_v384.py (o Nos sintetico e o conferidor de ensaio)'
TOPICOS = ('missao-ultima-flag-um-py.md', 'central-de-patentes-estado.md', 'beta-e-a-regra-matriz-02out.md', 'regra-dos-dois-regimes.md', 'v382-custodia-suspensa.md', 'v384-pilar-quantico-gpu-02out.md')
CH = open(os.path.join(HERE, 'chain_pos_rito_v384.sh'), encoding='utf-8', newline='').read()
i0 = CH.index('# >>> CONFIG'); i1 = CH.index('# <<< CONFIG')
STUB = '''# -*- coding: utf-8 -*-
import os, sys
nos = os.environ["V384_NOS"]; assert os.path.exists(os.path.join(nos, "SINTETICO_ENSAIO_V384.txt")), "STUB so com o Nos SINTETICO"
alvo = %s
open(alvo, "a", encoding="utf-8").write("STUB v384 (ensaio das guardas: %s %%s)\\n" %% " ".join(sys.argv[1:]))
print("STUB %s", sys.argv[1:], "->", alvo)
'''
posix = lambda p: '/' + p[0].lower() + p[2:].replace('\\', '/')


def sha_dir(d):
    r = {}
    for root, _ds, fs in os.walk(d):
        for f in fs:
            p = os.path.join(root, f); r[os.path.relpath(p, d)] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    return r


def cenario(nome, mexe=None, completo=False, env_extra=None):
    T = os.path.join(BASE, nome)
    if os.path.isdir(T):
        shutil.rmtree(T)
    for d in ('nos', 'umem', 'atlas', 'tools', 'stubs', 'saidas'):
        os.makedirs(os.path.join(T, d))
    N = os.path.join(T, 'nos')
    for root, _ds, fs in os.walk(NOS_S):
        for f in fs:
            s = os.path.join(root, f); q = os.path.join(N, os.path.relpath(s, NOS_S)); os.makedirs(os.path.dirname(q), exist_ok=True)
            os.link(s, q) if os.path.getsize(s) > 1 << 20 else shutil.copy2(s, q)
    # o run_dir do registro aponta para o Nos SINTETICO (absoluto): o Nos de teste e' outro caminho, entao o core e o selo de teste o reapontam
    for nm in ('um_absoluto.json', 'um_absoluto_selo.json'):
        p = os.path.join(N, nm); b = open(p, encoding='utf-8').read().replace(json.dumps(NOS_S)[1:-1], json.dumps(N)[1:-1])
        os.remove(p); open(p, 'w', encoding='utf-8').write(b)
    for f in ('MEMORIA_DA_LINHAGEM.md', 'DESENHO_DO_FECHAMENTO_QG.md'):
        shutil.copy2(os.path.join(A.NOS_REAL, f), os.path.join(N, f))
    if completo:
        shutil.copy2(os.path.join(A.ATLAS_DIR_REAL, 'TGL_ATLAS.md'), os.path.join(T, 'atlas', 'TGL_ATLAS.md'))
        for f in ('MEMORY.md', 'MEMORY_2.md') + TOPICOS:
            shutil.copy2(os.path.join(A.UMEM_REAL, f), os.path.join(T, 'umem', f))
    for f in ('arvore_da_prova.py', 'atlas_indice.py'):
        shutil.copy2(os.path.join(A.TOOLS_REAL, f), os.path.join(T, 'tools', f))
    open(os.path.join(T, 'stubs', 'arvore_stub.py'), 'w', encoding='utf-8').write(STUB % ('os.path.join(nos, "A_PROVA_DA_QG_TGL_arvore.md")', 'arvore', 'arvore'))
    open(os.path.join(T, 'stubs', 'atlas_stub.py'), 'w', encoding='utf-8').write(STUB % ('os.path.join(os.environ["V384_ATLAS_DIR"], "TGL_INDICE_VIVO.md")', 'atlas', 'atlas'))
    open(os.path.join(T, 'stubs', 'porta_stub.py'), 'w', encoding='utf-8').write(STUB % ('os.path.join(os.environ["V384_SAIDAS"], "porta_stub.txt")', 'porta', 'porta'))
    open(os.path.join(T, 'horarios.txt'), 'w', encoding='utf-8').write('SINT-15:32:44\nSINT-19:00:00\n')
    if mexe:
        mexe(N)
    w = lambda *a: os.path.join(T, *a)
    cfg = ('# >>> CONFIG (ENSAIO DAS GUARDAS: cenario %s; SO este bloco difere do chain real)\n' % nome
           + 'SP="%s"\nSEL="$SP/v384_selo"; PK="$SP/v384"\nTOOLS="%s"\nNOS="%s"\nUMEM="%s"\nATLD="%s"\n' % (posix(A.SP), posix(w('tools')), posix(N), posix(w('umem')), posix(w('atlas')))
           + 'ARVORE="%s"; ATLASPY="%s"; PORTA="%s"\n' % (posix(w('stubs', 'arvore_stub.py')), posix(w('stubs', 'atlas_stub.py')), posix(w('stubs', 'porta_stub.py')))
           + 'CONF_SRC="%s"; CONFOUT="%s"; ENS="%s"; OUTD="%s"; MANIF="%s"\n' % (posix(os.path.join(CONF_E, 'conferir_rito_v384_ENSAIO.py')), posix(w('conferidor')), posix(w('ens')), posix(w('saidas')), posix(w('saidas', 'v384_incorporacao_manifesto.json')))
           + 'unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR V384_REMAP_DIR\n'
           + 'export V384_NOS="%s" V384_CONF_DIR="%s" V384_HORARIOS="%s" V384_PIDF="%s" V384_ESPERA_SEM_VIGIA=1 V384_ESPERA_PASSO_S=1 V384_ESPERA_MAX_S=60\n' % (N, w('conferidor'), w('horarios.txt'), w('nao_existe.pid'))
           + 'export V384_UMEM="%s" V384_ATLAS_DIR="%s" V384_TOOLS="%s" V384_SAIDAS="%s" V384_WRITE_ROOT="%s" V384_ARQ_DEST="%s"\n' % (w('umem'), w('atlas'), w('tools'), w('saidas'), T, w('arquivo')))
    ch = CH[:i0] + cfg + CH[i1:]
    assert ch[:i0] == CH[:i0] and ch[-(len(CH) - i1):] == CH[i1:], 'o chain de teste difere fora do CONFIG'
    open(w('chain_teste.sh'), 'w', encoding='utf-8', newline='\n').write(ch)
    antes = {d: sha_dir(w(d)) for d in ('umem', 'atlas', 'tools')}; antes['nos_md'] = {f: hashlib.sha256(open(os.path.join(N, f), 'rb').read()).hexdigest() for f in ('MEMORIA_DA_LINHAGEM.md', 'DESENHO_DO_FECHAMENTO_QG.md')}
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    for k in [k for k in env if k.startswith('V384_')]:
        env.pop(k)
    env.update(env_extra or {})
    t0 = time.time()
    r = subprocess.run([BASH, w('chain_teste.sh')], cwd=T, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1800)
    out = r.stdout + r.stderr
    open(w('chain_teste.out.txt'), 'w', encoding='utf-8').write(out)
    depois = {d: sha_dir(w(d)) for d in ('umem', 'atlas', 'tools')}; depois['nos_md'] = {f: hashlib.sha256(open(os.path.join(N, f), 'rb').read()).hexdigest() for f in ('MEMORIA_DA_LINHAGEM.md', 'DESENHO_DO_FECHAMENTO_QG.md')}
    parada = [l for l in out.splitlines() if l.startswith('PARADA:')]
    diag = [l.strip() for l in out.splitlines() if 'diagnostico:' in l]
    passos = [l[3:].split(' $(')[0].strip()[:60] for l in out.splitlines() if l.startswith('== ')]
    res = {'rc': r.returncode, 's': round(time.time() - t0, 1), 'parada': parada[:1], 'diagnostico': diag[:1], 'ultimo_passo': passos[-1] if passos else None,
           'fim': '== FIM' in out, 'superficies_de_teste_intocadas': antes == depois, 'stubs': [l.strip()[:120] for l in out.splitlines() if l.startswith('STUB ')]}
    print('[%s] rc=%s; ultimo passo: %s; %s; superficies de teste intocadas: %s%s' % (nome, r.returncode, res['ultimo_passo'], (parada[0][:170] if parada else ('FIM' if res['fim'] else '?')),
                                                                                    res['superficies_de_teste_intocadas'], ('; ' + diag[0][:160]) if diag else ''), flush=True)
    return res, T


def sub(arq, a, b, n=1):
    def f(N):
        p = os.path.join(N, arq); s = open(p, encoding='utf-8').read(); assert s.count(a) >= n, (arq, a[:60]); os.remove(p)
        open(p, 'w', encoding='utf-8', newline='\n').write(s.replace(a, b, n))
    return f


def selo(fun):
    def f(N):
        p = os.path.join(N, 'um_absoluto_selo.json'); S = json.load(open(p, encoding='utf-8')); fun(S); os.remove(p)
        open(p, 'w', encoding='utf-8').write(json.dumps(S, ensure_ascii=False, indent=2))
    return f


os.makedirs(BASE, exist_ok=True); os.makedirs(SAI, exist_ok=True)
R = {}
R['FELIZ'], TF = cenario('FELIZ', completo=True)
R['UMPY_ERRADO'], _ = cenario('UMPY_ERRADO', mexe=lambda N: (os.remove(os.path.join(N, 'um.py')), open(os.path.join(N, 'um.py'), 'w').write('# outro um.py\n')))
R['RC_1'], _ = cenario('RC_1', mexe=sub('rodada_v384_stdout.txt', 'RITO_RC=0', 'RITO_RC=1'))
R['SEM_LINHA_FINAL'], _ = cenario('SEM_LINHA_FINAL', mexe=sub('rodada_v384_stdout.txt', '[selo] colapso tipado: ', '[selo] colapso NAO tipado: '))
R['TRACEBACK'], _ = cenario('TRACEBACK', mexe=sub('rodada_v384_stdout.txt', '[selo] rite_checkpoints: ', 'Traceback (most recent call last):\n[selo] rite_checkpoints: '))
R['TEOREMAS'], _ = cenario('TEOREMAS', mexe=sub('rodada_v384_stdout.txt', 'teoremas limpos: 5998/5998', 'teoremas limpos: 5997/5998'))
R['SELO_AUSENTE'], _ = cenario('SELO_AUSENTE', mexe=lambda N: os.remove(os.path.join(N, 'um_absoluto_selo.json')))
R['CONFERIDOR_REPROVA'], _ = cenario('CONFERIDOR_REPROVA', mexe=sub('um_absoluto_pt.txt', 'Nota: o que se calcula na GPU e como', 'Nota: (removida no ensaio)'))
R['SO_PILAR_REPROVA'], TP = cenario('SO_PILAR_REPROVA', mexe=selo(lambda S: S['not_sealed_this_run'].update(computacao_nao_concluida=['quantum_pillar_v384'])))
c16 = hashlib.sha256(open(os.path.join(TP, 'conferidor', 'conferencia_rito_v384.json'), 'rb').read()).hexdigest()[:16]
R['SO_PILAR_ACEITO_MAS_LEITURA_PARA'], _ = cenario('SO_PILAR_ACEITO_MAS_LEITURA_PARA', mexe=selo(lambda S: S['not_sealed_this_run'].update(computacao_nao_concluida=['quantum_pillar_v384'])),
                                                   env_extra={'V384_ACEITO_PILAR_NAO_CONCLUIDO': c16})
R['LEITURA_PARA'], _ = cenario('LEITURA_PARA', mexe=sub('rodada_v384_stdout.txt', '[v384] pilar quantico: TGL_QUANTUM_PILLAR_V1__', '[v384] pilar quantico: TGL_QUANTUM_PILLAR_V1__OUTRO__'))
ESPERADO = {'FELIZ': ('FIM', None), 'UMPY_ERRADO': ('PARADA', 'o um.py do disco nao e o instalado'), 'RC_1': ('PARADA', 'espera terminou com rc=3'),
            'SEM_LINHA_FINAL': ('PARADA', 'espera terminou com rc=3'), 'TRACEBACK': ('PARADA', 'Traceback/AVISO'), 'TEOREMAS': ('PARADA', 'RITO NAO LIMPO'),
            'SELO_AUSENTE': ('PARADA', 'o selo NAO existe'), 'CONFERIDOR_REPROVA': ('PARADA', 'CONFERIDOR REPROVOU'), 'SO_PILAR_REPROVA': ('PARADA', 'CONFERIDOR REPROVOU'),
            'SO_PILAR_ACEITO_MAS_LEITURA_PARA': ('PARADA', 'a LEITURA tem PROBLEMAS'), 'LEITURA_PARA': ('PARADA', 'a LEITURA tem PROBLEMAS')}
ok = True
for k, (tipo, frase) in ESPERADO.items():
    r = R[k]
    if tipo == 'FIM':
        r['ok'] = r['rc'] == 0 and r['fim'] and len(r['stubs']) == 3
    else:
        r['ok'] = r['rc'] != 0 and bool(r['parada']) and frase in r['parada'][0] and r['superficies_de_teste_intocadas']
    ok = ok and r['ok']
R['SO_PILAR_REPROVA']['diagnostico_diz_so_pilar'] = bool(R['SO_PILAR_REPROVA']['diagnostico']) and 'SO itens do pilar: True' in R['SO_PILAR_REPROVA']['diagnostico'][0]
ok = ok and R['SO_PILAR_REPROVA']['diagnostico_diz_so_pilar']
# ---- (corretor, 04/10; 8o achado) a 2a PASSADA do FELIZ na MESMA pasta: a cadeia vai ao FIM de novo (idempotente), as superficies dizem NADA A GRAVAR, e o
# manifesto anterior em TOOLS vai a backup de BYTES antes da troca (temporario -> cmp -> mv; nenhum .tmp_m384 sobra)
_mf = os.path.join(TF, 'tools', 'v384_incorporacao_manifesto.json'); _mf0 = open(_mf, 'rb').read()
time.sleep(1.2)   # o stamp do manifesto muda de segundo: o novo DIFERE do anterior
_env2 = {k: v for k, v in os.environ.items() if not k.startswith('V384_')}; _env2['PYTHONIOENCODING'] = 'utf-8'
_r2 = subprocess.run([BASH, os.path.join(TF, 'chain_teste.sh')], cwd=TF, env=_env2, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1800)
_o2 = _r2.stdout + _r2.stderr; open(os.path.join(TF, 'chain_teste_2a_passada.out.txt'), 'w', encoding='utf-8').write(_o2)
_bk = sorted(f for f in os.listdir(os.path.join(TF, 'tools')) if f.startswith('v384_incorporacao_manifesto.json.bak_') and f.endswith('_m384'))
R['FELIZ_2a_passada'] = {'rc': _r2.returncode, 'fim': '== FIM' in _o2, 'superficies_idempotentes': 'NADA A GRAVAR' in _o2, 'backup_do_manifesto': _bk,
                         'o_backup_e_o_anterior': bool(_bk) and open(os.path.join(TF, 'tools', _bk[-1]), 'rb').read() == _mf0,
                         'o_novo_e_o_de_v384_selo': open(_mf, 'rb').read() == open(os.path.join(TF, 'saidas', 'v384_incorporacao_manifesto.json'), 'rb').read(),
                         'tmp_restante': [f for f in os.listdir(os.path.join(TF, 'tools')) if 'tmp_m384' in f]}
_f2 = R['FELIZ_2a_passada']
_f2['ok'] = bool(_f2['rc'] == 0 and _f2['fim'] and _f2['superficies_idempotentes'] and _f2['o_backup_e_o_anterior'] and _f2['o_novo_e_o_de_v384_selo'] and not _f2['tmp_restante'])
ok = ok and _f2['ok']
print('  [FELIZ, 2a passada] rc %s, FIM %s, superficies NADA A GRAVAR %s, backup do manifesto anterior %s (= o anterior: %s) -> %s'
      % (_f2['rc'], _f2['fim'], _f2['superficies_idempotentes'], _bk, _f2['o_backup_e_o_anterior'], 'OK' if _f2['ok'] else 'FALHOU'), flush=True)

# ---- (corretor, 04/10) PONTA A PONTA POR CLASSE DO PILAR: sem o aceite PARA no conferidor (so itens do pilar); com o aceite nomeado vai ao FIM; o gravado diz
# a classe e o aceite e nenhuma frase de sucesso fora do ramo 9 (o ramo 9 com negativos: o conferidor congelado o aprova e vai ao FIM direto)
REAL_ANTES = {'MEMORIA_DA_LINHAGEM.md': open(os.path.join(A.NOS_REAL, 'MEMORIA_DA_LINHAGEM.md'), 'rb').read(), 'DESENHO_DO_FECHAMENTO_QG.md': open(os.path.join(A.NOS_REAL, 'DESENHO_DO_FECHAMENTO_QG.md'), 'rb').read(),
              'TGL_ATLAS.md': open(os.path.join(A.ATLAS_DIR_REAL, 'TGL_ATLAS.md'), 'rb').read()}
REAL_ANTES.update({t: open(os.path.join(A.UMEM_REAL, t), 'rb').read() for t in TOPICOS})
R['CLASSES'] = {}
for nome in VP.CLASSES:
    mexe = (lambda n: (lambda N: VP.transforma(N, n)))(nome)
    r1, TT = cenario('CLASSE_' + nome, mexe=mexe, completo=True)
    item = {'veredito_esperado': VP.CLASSE_ESPERADA[nome], 'passada_1': {k: r1[k] for k in ('rc', 'parada', 'diagnostico', 'fim', 'superficies_de_teste_intocadas')}}
    if VP.CLASSE_ESPERADA[nome] == 'RAMO_9':
        r2 = r1; c16 = None
        ok1 = r1['rc'] == 0 and r1['fim']
    else:
        dg = r1['diagnostico'][0] if r1['diagnostico'] else ''
        mm = re.search(r'conferencia sha16 ([0-9a-f]{16})', dg); c16 = mm.group(1) if mm else None
        ok1 = (r1['rc'] != 0 and bool(r1['parada']) and 'CONFERIDOR REPROVOU' in r1['parada'][0] and 'SO itens do pilar: True' in dg and r1['superficies_de_teste_intocadas'] and bool(c16))
        r2, TT = cenario('CLASSE_' + nome, mexe=mexe, completo=True, env_extra={'V384_ACEITO_PILAR_NAO_CONCLUIDO': c16 or 'x'})
    item['passada_2_com_aceite'] = {k: r2[k] for k in ('rc', 'parada', 'fim', 'ultimo_passo')}; item['aceite_sha16'] = c16
    # o que foi GRAVADO: so o que a cadeia acrescentou a cada superficie de teste (o arquivo novo menos os bytes do real copiado)
    gr = {}
    for f, sub in (('MEMORIA_DA_LINHAGEM.md', 'nos'), ('DESENHO_DO_FECHAMENTO_QG.md', 'nos'), ('TGL_ATLAS.md', 'atlas')):
        b = open(os.path.join(TT, sub, f), 'rb').read(); gr[f] = b[len(REAL_ANTES[f]):].decode('utf-8', 'replace') if b.startswith(REAL_ANTES[f]) else None
    for t in TOPICOS:
        b = open(os.path.join(TT, 'umem', t), 'rb').read(); gr[t] = b[len(REAL_ANTES[t]):].decode('utf-8', 'replace') if b.startswith(REAL_ANTES[t]) else None
    idxt = open(os.path.join(TT, 'umem', 'MEMORY.md'), encoding='utf-8').read()
    tudo = '\n'.join(v for v in gr.values() if v)
    nao9 = VP.CLASSE_ESPERADA[nome] != 'RAMO_9'
    item['gravado'] = {'append_puro_em_todas': all(v is not None and v.strip() for v in gr.values()),
                       'diz_a_classe': ('computação não concluída' in gr['MEMORIA_DA_LINHAGEM.md'] and ('NÃO CONCLUÍDO (%s)' % VP.CLASSE_ESPERADA[nome]) in idxt) if nao9 and gr['MEMORIA_DA_LINHAGEM.md'] else
                                     (bool(gr['MEMORIA_DA_LINHAGEM.md']) and 'o ramo 9 da árvore congelada' in gr['MEMORIA_DA_LINHAGEM.md']),
                       'diz_o_aceite': (('a gerência aceitou o resultado do pilar como resultado' in tudo) and (c16 in tudo)) if nao9 else True,
                       'frases_de_sucesso_fora_do_ramo9': sorted({f for f in TX.FRASES_DE_SUCESSO if f in tudo}) if nao9 else [],
                       'MEMORY_md_bytes': len(idxt.encode('utf-8'))}
    item['ok'] = bool(ok1 and r2['rc'] == 0 and r2['fim'] and item['gravado']['append_puro_em_todas'] and item['gravado']['diz_a_classe'] and item['gravado']['diz_o_aceite']
                      and not item['gravado']['frases_de_sucesso_fora_do_ramo9'] and item['gravado']['MEMORY_md_bytes'] <= 24000)
    ok = ok and item['ok']
    R['CLASSES'][nome] = item
    print('  [CLASSE %s] 1a: rc %s %s | 2a (aceite %s): rc %s, FIM %s | gravado: classe %s, aceite %s, sucesso fora do 9 %s, MEMORY.md %d B -> %s'
          % (nome, r1['rc'], (r1['parada'][0][:60] if r1['parada'] else 'FIM'), c16, r2['rc'], r2['fim'], item['gravado']['diz_a_classe'], item['gravado']['diz_o_aceite'],
             item['gravado']['frases_de_sucesso_fora_do_ramo9'] or '-', item['gravado']['MEMORY_md_bytes'], 'OK' if item['ok'] else 'FALHOU'), flush=True)
    if nome != 'RAMO9_NEGATIVOS' and os.path.isdir(TT):
        shutil.rmtree(TT)          # o espaco: as copias de cada classe (superficies de 6 MB) sao apagadas depois de medidas; o resultado fica no JSON

# ---- (corretor, 04/10) A ESPERA com um lancador de TESTE (4o achado): o .pid velho e o horario de fim ausente nao travam a espera por 7 h
import subprocess as _sp


def lancador_teste(pidf, segundos):
    """um sh do Git Bash cuja linha de comando contem rito_v384 (como o lancador real), que grava o PROPRIO pid (MSYS) no .pid e vive `segundos`."""
    p = _sp.Popen([BASH, '-c', 'echo $$ > "$1"; sleep "$2"; true', 'rito_v384_ensaio_lancador', posix(pidf), str(segundos)])
    t_ = time.time()
    while not (os.path.exists(pidf) and open(pidf).read().strip()) and time.time() - t_ < 20:
        time.sleep(0.2)
    return p


def espera_caso(nome, stdout_txt, horarios_txt, pid_modo, max_s=60):
    d = os.path.join(BASE, 'ESPERA_' + nome)
    if os.path.isdir(d):
        shutil.rmtree(d)
    N = os.path.join(d, 'nos'); os.makedirs(N)
    open(os.path.join(N, A.MARCA_SINT), 'w', encoding='utf-8').write('SINTETICO -- ensaio da espera (corretor)\n')
    open(os.path.join(N, 'rodada_v384_stdout.txt'), 'w', encoding='utf-8', newline='\n').write(stdout_txt)
    hor = os.path.join(d, 'horarios.txt'); open(hor, 'w', encoding='utf-8').write(horarios_txt)
    pidf = os.path.join(d, 'lancador.pid'); proc = None
    if pid_modo == 'morto':
        q = _sp.Popen([BASH, '-c', 'echo $$ > "$1"', 'rito_v384_ensaio_morto', posix(pidf)]); q.wait()
    elif isinstance(pid_modo, int):
        proc = lancador_teste(pidf, pid_modo)
    env = {k: v for k, v in os.environ.items() if not k.startswith('V384_')}
    env.update(PYTHONIOENCODING='utf-8', V384_NOS=N, V384_HORARIOS=hor, V384_PIDF=pidf, V384_ESPERA_SEM_VIGIA='1', V384_ESPERA_PASSO_S='1', V384_ESPERA_MAX_S=str(max_s),
               V384_ESPERA_RESTAURO_MAX_S='30')
    t_ = time.time()
    r = _sp.run([sys.executable, os.path.join(HERE, 'espera_rito_v384.py')], env=env, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=600)
    s = round(time.time() - t_, 1)
    if proc is not None:
        proc.wait(timeout=120)
    out = r.stdout + r.stderr
    open(os.path.join(d, 'espera.out.txt'), 'w', encoding='utf-8').write(out)
    return {'rc': r.returncode, 's': s, 'ultima': (out.strip().splitlines() or [''])[-1][:200], 'viu_vivo': ' lancador VIVO ' in out, 'aviso_horario': 'horario de fim NAO gravado' in out}


FINAL = '[SINTETICO] ...\n[selo] colapso tipado: SINTETICO (ensaio da espera)\n'
R['ESPERA'] = {
    'RC0_SEM_HORARIO_LANCADOR_MORTO': espera_caso('RC0_SEM_HORARIO_LANCADOR_MORTO', FINAL + 'RITO_RC=0\n', 'SINT-15:32:44\n', 'morto'),
    'SEM_RC_LANCADOR_MORTO': espera_caso('SEM_RC_LANCADOR_MORTO', FINAL, 'SINT-15:32:44\n', 'morto'),
    'RC0_SEM_HORARIO_LANCADOR_VIVO_8s': espera_caso('RC0_SEM_HORARIO_LANCADOR_VIVO_8s', FINAL + 'RITO_RC=0\n', 'SINT-15:32:44\n', 8),
    'RC0_COM_HORARIO_SEM_PID': espera_caso('RC0_COM_HORARIO_SEM_PID', FINAL + 'RITO_RC=0\n', 'SINT-15:32:44\nSINT-19:00:00\n', None),
    'SEM_RC_LANCADOR_VIVO_TEMPO': espera_caso('SEM_RC_LANCADOR_VIVO_TEMPO', FINAL, 'SINT-15:32:44\n', 25, max_s=6),
}
E_ = R['ESPERA']
E_['ok'] = (E_['RC0_SEM_HORARIO_LANCADOR_MORTO']['rc'] == 0 and E_['RC0_SEM_HORARIO_LANCADOR_MORTO']['aviso_horario'] and E_['RC0_SEM_HORARIO_LANCADOR_MORTO']['s'] < 60
            and E_['SEM_RC_LANCADOR_MORTO']['rc'] == 5 and E_['SEM_RC_LANCADOR_MORTO']['s'] < 60
            and E_['RC0_SEM_HORARIO_LANCADOR_VIVO_8s']['rc'] == 0 and E_['RC0_SEM_HORARIO_LANCADOR_VIVO_8s']['viu_vivo'] and E_['RC0_SEM_HORARIO_LANCADOR_VIVO_8s']['s'] >= 5
            and E_['RC0_COM_HORARIO_SEM_PID']['rc'] == 0 and E_['SEM_RC_LANCADOR_VIVO_TEMPO']['rc'] == 4 and E_['SEM_RC_LANCADOR_VIVO_TEMPO']['viu_vivo'])
ok = ok and E_['ok']
print('  [ESPERA]', {k: (v['rc'], v['s']) for k, v in E_.items() if k != 'ok'}, '->', 'OK' if E_['ok'] else 'FALHOU', flush=True)
# no FELIZ: as superficies de teste receberam a v384 (grep) e o MEMORY.md <= 24 000
TU = os.path.join(TF, 'umem'); TN = os.path.join(TF, 'nos'); TA = os.path.join(TF, 'atlas')
R['FELIZ']['grep_v384'] = {os.path.basename(p): open(p, encoding='utf-8', errors='replace').read().count('v384') for p in
                           [os.path.join(TN, 'MEMORIA_DA_LINHAGEM.md'), os.path.join(TN, 'DESENHO_DO_FECHAMENTO_QG.md'), os.path.join(TA, 'TGL_ATLAS.md'), os.path.join(TA, 'TGL_INDICE_VIVO.md'),
                            os.path.join(TN, 'A_PROVA_DA_QG_TGL_arvore.md'), os.path.join(TU, 'MEMORY.md')] + [os.path.join(TU, t) for t in TOPICOS]}
R['FELIZ']['MEMORY_md_bytes'] = os.path.getsize(os.path.join(TU, 'MEMORY.md'))
R['chain_fora_do_CONFIG_identico'] = True
R['tudo_ok'] = ok
open(os.path.join(SAI, 'ensaio_guardas_v384.json'), 'w', encoding='utf-8').write(json.dumps(R, ensure_ascii=False, indent=1))
print('FELIZ: grep v384 =', R['FELIZ']['grep_v384'], '| MEMORY.md', R['FELIZ']['MEMORY_md_bytes'], 'B')
print('ENSAIO DAS GUARDAS:', 'TUDO CERTO' if ok else 'FALHOU', '->', os.path.join(SAI, 'ensaio_guardas_v384.json'))
sys.exit(0 if ok else 1)
