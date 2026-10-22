# -*- coding: utf-8 -*-
"""SO LEITURA fora de v384_selo: confere os TEXTOS da v384 (molde: testar_formatos_v383.py).
(1) com a leitura da rodada (V384_NOS: no ensaio, o Nos SINTETICO), cada funcao de textos_v384 renderiza sem chave sobrando ({x}) e carrega os numeros de V;
(2) VARIANTES COERENTES do pilar (16o achado da revisao de 04/10 -- nunca mais V mutado a mao): para cada classe de variantes_pilar_v384.CLASSES, um Nos
    SINTETICO coerente (ensaio_variantes\\<classe>\\nos), o conferidor de ENSAIO rodado nele, a LEITURA REAL (subprocesso) com o aceite nomeado
    (V384_ACEITO_PILAR_NAO_CONCLUIDO = o sha16 da conferencia, quando ela reprova so itens do pilar) e TODOS os textos renderizados; e o handoff REAL
    em copias (primeiro com o MEMORY.md no tamanho real -- tem de RECUSAR sem gravar nada, rc 3 --, depois com o indice compactado -- grava).
    Confere: nenhum PROBLEMA; a classe esperada; a causa dita; o aceite dito; FORA do ramo 9 nenhuma frase de sucesso (textos_v384.FRASES_DE_SUCESSO) em
    texto algum, nem no handoff; nenhum literal do Python (None) nos textos; o arquivo do pilar no Nos dito como E (o MARCADOR, o parcial ou o resultado);
    a pasta da rodada so com os arquivos que existem; no RAMO9_NEGATIVOS, os negativos separados (da lista do V1 / da gerencia, ao lado);
(3) o FORMATO: os cabecalhos de cada bloco da v384 casam o MESMO padrao que o bloco da v383 nas superficies REAIS (lidas, nunca tocadas);
(4) os numeros DIGITADOS nos moldes de textos_v384.py (literais) listados para a auditoria (devem ser so os estruturais);
(5) a guarda das palavras proibidas em todo texto renderizado.
Saida: ensaio_saidas\\testar_formatos_v384.json (com o Nos sintetico) e o resumo na tela; rc 0 = tudo passa."""
import ast, glob, hashlib, json, os, re, shutil, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v384 as A
import leitura_v384 as L
import textos_v384 as T
import variantes_pilar_v384 as VP
AMB = A.ambiente()
V, P = L.ler()
R = {'problemas_da_leitura': P, 'render': {}, 'variantes': {}, 'formato': {}, 'digitados': [], 'proibidas': []}
FN = ('core_txt', 'rodada_txt', 'linhagem', 'desenho', 'atlas', 'topico_missao', 'topico_central', 'topico_regra', 'topico_regimes', 'topico_suspensao', 'topico_pilar',
      'arvore_linha', 'verbete', 'remissivo', 'marca_missao', 'linha_handoff')
RE_SOBRA = re.compile(r'\{[A-Za-z_][A-Za-z_0-9]*\}')
PROIB = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY|QG confirmada|QG CONFIRMADA|gravidade quântica confirmada')
LITERAIS = re.compile(r'\bNone\b|somente leitura: (?:True|False)|bit a bit o do core: (?:True|False|None)')
ok = True


def render(Vx, tag):
    global ok
    out = {}
    for fn in FN:
        try:
            s = getattr(T, fn)(Vx)
        except Exception as e:
            out[fn] = {'erro': repr(e)}; ok = False; continue
        sobra = [x for x in RE_SOBRA.findall(s) if x not in ('{ML',)]
        pr = PROIB.findall(s)
        if sobra or pr:
            ok = False
        if pr:
            R['proibidas'].append((tag, fn, pr))
        out[fn] = {'bytes': len(s.encode('utf-8')), 'sobra': sobra, 'proibidas': pr}
    return out


R['render']['leitura'] = render(V, 'leitura')
# os numeros de V aparecem nos textos (nao digitados): uma amostra das chaves numericas do pilar e do pre-registro
amostra = {k: str(V[k]) for k in ('t2_points', 't2_unique', 't2_name', 't2_folds', 't4_n', 't4_all', 'cpu_cmp', 't1_inj', 'pr_json16', 'pr_spec16', 'qp_res16', 's16', 'base16', 'pr_ev', 'n_afer',
                                  'pr_n_ordens', 'pr_n_trechos', 't3_n1')}
lin = T.linhagem(V) + T.topico_regimes(V)
R['numeros_de_V_no_diario'] = {k: (v in lin) for k, v in amostra.items()}
if not all(R['numeros_de_V_no_diario'].values()):
    ok = False
R['literais_python_no_render'] = sorted(set(LITERAIS.findall(''.join(getattr(T, fn)(V) for fn in FN))))
if R['literais_python_no_render']:
    ok = False

# ---- (2) as VARIANTES COERENTES (subprocessos; tudo dentro de v384_selo\ensaio_variantes)
VB = os.path.join(HERE, 'ensaio_variantes'); os.makedirs(VB, exist_ok=True)
CONF_E = os.path.join(HERE, 'conferidor_ensaio')
ENS_COMP = os.path.join(HERE, 'ensaio_superficies')
CODE = r'''
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, %r)
import leitura_v384 as L, textos_v384 as T
V, P = L.ler()
FN = %r
txt = {fn: getattr(T, fn)(V) for fn in FN}
print(json.dumps({'P': P, 'V': {k: V.get(k) for k in ('qp_classe', 'qp_v', 'qp_classe_txt', 'qp_causa', 'qp_negativos', 'qp_neg_prereg_l', 'qp_neg_ger_l', 'qp_neg_extra',
                                                     'qp_arq_tipo', 'qp_arq_txt', 'qp_pasta_txt', 'qp_pasta_arquivos', 'qp_lanc_txt', 'conf_aceite', 'qp_custodia_txt')}, 'txt': txt}, ensure_ascii=False))
''' % (HERE, FN)


def roda(args, env, cwd):
    return subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')


def env_base(N, C, extra=None):
    e = {k: v for k, v in os.environ.items() if not k.startswith('V384_')}
    e.update(PYTHONIOENCODING='utf-8', V384_NOS=N, V384_CONF_DIR=C, V384_HORARIOS=os.path.join(HERE, 'ensaio_horarios_v384_SINTETICO.txt'),
             V384_SAIDAS=os.path.join(os.path.dirname(N), 'saidas'), V384_ARQ_DEST=os.path.join(os.path.dirname(N), 'arquivo'))
    e.update(extra or {})
    return e


for nome in VP.CLASSES:
    d = os.path.join(VB, nome); N = os.path.join(d, 'nos'); C = os.path.join(d, 'conferidor'); H = os.path.join(d, 'handoff_cheio'); H2 = os.path.join(d, 'handoff')
    for q in (C, H, H2, os.path.join(d, 'saidas'), os.path.join(d, 'arquivo')):
        if os.path.isdir(q):
            shutil.rmtree(q)
        os.makedirs(q)
    VP.copia_nos(N); verd = VP.transforma(N, nome)
    for f in ('conferir_rito_v384_ENSAIO.py', 'ESPERADOS_v384.json', 'rito_servidor_v384.log', 'rito_v384_sinal.txt'):
        if os.path.exists(os.path.join(CONF_E, f)):
            shutil.copyfile(os.path.join(CONF_E, f), os.path.join(C, f))
    rc_ = roda([sys.executable, 'conferir_rito_v384_ENSAIO.py'], env_base(N, C), C)
    open(os.path.join(C, 'conferir_rito_v384_stdout.txt'), 'w', encoding='utf-8').write(rc_.stdout + rc_.stderr)
    cj = json.load(open(os.path.join(C, 'conferencia_rito_v384.json'), encoding='utf-8'))
    c16 = hashlib.sha256(open(os.path.join(C, 'conferencia_rito_v384.json'), 'rb').read()).hexdigest()[:16]
    falhas = [k for k, v in list(cj['deve_mudar'].items()) + list(cj['nao_pode_mudar'].items()) if not v]
    so_pilar = bool(falhas) and all(any(k.startswith(p) for p in L.PILAR_ITENS) for k in falhas)
    ex = {'V384_ACEITO_PILAR_NAO_CONCLUIDO': c16} if rc_.returncode != 0 else {}
    rl = roda([sys.executable, '-c', CODE], env_base(N, C, ex), HERE)
    item = {'veredito': verd, 'classe_esperada': VP.CLASSE_ESPERADA[nome], 'conferidor_rc': rc_.returncode, 'conferidor_falhas': len(falhas), 'falhas_so_do_pilar': so_pilar,
            'aceite_nomeado': bool(ex)}
    if rl.returncode != 0:
        item['erro_da_leitura'] = rl.stderr[-2000:]; ok = False; R['variantes'][nome] = item; print('[%s] ERRO na leitura: %s' % (nome, rl.stderr[-500:])); continue
    o = json.loads(rl.stdout.strip().splitlines()[-1]); Vv = o['V']; tx = o['txt']; tudo = '\n'.join(tx.values())
    open(os.path.join(d, 'textos_%s.txt' % nome), 'w', encoding='utf-8').write('\n\n'.join('##### %s\n%s' % (k, v) for k, v in tx.items()) + '\n')
    nao9 = Vv['qp_classe'] != 'RAMO_9'
    item.update({'problemas': o['P'], 'classe_lida': Vv['qp_classe'], 'causa': Vv['qp_causa'], 'arquivo_no_nos': Vv['qp_arq_tipo'], 'pasta_arquivos': Vv['qp_pasta_arquivos'],
                 'negativos_do_V1': Vv['qp_neg_prereg_l'], 'negativos_da_gerencia': Vv['qp_neg_ger_l'],
                 'frases_de_sucesso_fora_do_ramo9': sorted({f for f in T.FRASES_DE_SUCESSO if f in tudo}) if nao9 else [],
                 'literais_python': sorted(set(LITERAIS.findall(tudo))), 'sobras': sorted(set(RE_SOBRA.findall(tudo)) - {'{ML'}), 'proibidas': PROIB.findall(tudo),
                 'aceite_dito': (not ex) or ('a gerência aceitou o resultado do pilar como resultado' in tx['linhagem'] and c16 in tx['linhagem'])})
    # o handoff REAL em copias: (a) com o MEMORY.md no tamanho REAL -> tem de recusar SEM gravar nada (rc 3); (b) com o indice compactado -> grava
    av = os.path.join(d, 'arquivo', 'v384'); os.makedirs(av, exist_ok=True)
    for f in ('AFERIDOR_v384.txt', 'disposicoes_afericoes_v384.json'):
        shutil.copyfile(os.path.join(A.PK, f), os.path.join(av, f))      # as afericoes REAIS, copiadas (a guarda do handoff as exige arquivadas)
    for f in ('MEMORY.md', 'MEMORY_2.md'):
        shutil.copyfile(os.path.join(A.UMEM_REAL, f), os.path.join(H, f))
    _mh = os.path.join(H, 'MEMORY.md')   # o indice CHEIO: se a copia do real tiver folga, enche-se a COPIA ate 23 990 B (nunca o real)
    if os.path.getsize(_mh) < 23990:
        open(_mh, 'ab').write((chr(10) + '<!-- ensaio: enchimento ' + 'x' * max(0, 23990 - os.path.getsize(_mh) - 40) + ' -->').encode('utf-8'))
    antes = {f: hashlib.sha256(open(os.path.join(H, f), 'rb').read()).hexdigest() for f in os.listdir(H)}
    rh = roda([sys.executable, 'handoff_v384.py'], env_base(N, C, dict(ex, V384_REMAP_DIR=H, V384_WRITE_ROOT=H)), HERE)
    depois = {f: hashlib.sha256(open(os.path.join(H, f), 'rb').read()).hexdigest() for f in os.listdir(H)}
    item['handoff_indice_cheio'] = {'rc': rh.returncode, 'recusou_sem_gravar': rh.returncode == 3 and antes == depois, 'ultima': (rh.stdout.strip().splitlines() or [''])[-1][:200]}
    for f in ('MEMORY.md', 'MEMORY_2.md'):
        shutil.copyfile(os.path.join(A.UMEM_REAL, f), os.path.join(H2, f))
    rcmp = roda([sys.executable, 'compactar_memory_para_v384.py', '--gravar'], env_base(N, C, dict(ex, V384_REMAP_DIR=H2, V384_WRITE_ROOT=H2)), HERE)
    rh2 = roda([sys.executable, 'handoff_v384.py'], env_base(N, C, dict(ex, V384_REMAP_DIR=H2, V384_WRITE_ROOT=H2)), HERE)
    hm = os.path.join(H2, 'handoff-v384-custodia.md')
    htx = open(hm, encoding='utf-8').read() if os.path.exists(hm) else ''
    item['handoff'] = {'compactar_rc': rcmp.returncode, 'rc': rh2.returncode, 'memoria_topico': bool(htx), 'MEMORY_md_bytes': os.path.getsize(os.path.join(H2, 'MEMORY.md')),
                       'frases_de_sucesso_fora_do_ramo9': sorted({f for f in T.FRASES_DE_SUCESSO if f in htx}) if nao9 else [],
                       'literais_python': sorted(set(LITERAIS.findall(htx))),
                       'diz_o_marcador': ('o MARCADOR desta rodada' in htx) if Vv['qp_arq_tipo'] == 'MARCADOR' else None,
                       'lista_so_o_que_existe': all(('`%s`' % f) not in htx.split('**PARA A SESSÃO DO SITE')[-1].split('**NÃO espelhar:**')[0] for f in ('result.json', 'result_partial.json', 'details.jsonl', 'cpuref.json') if f not in Vv['qp_pasta_arquivos'])
                       if htx else False,
                       'pendencias_v383_herdadas': 'herdadas da v383' in htx, 'v1x_dito': 'repetir a rodada sob o MESMO V1 congelado é decisão do operador' in htx,
                       'marcador_do_servidor': 'conferir o servidor do modelo nativo' in htx}
    ok_i = (not o['P'] and Vv['qp_classe'] == VP.CLASSE_ESPERADA[nome] and not item['frases_de_sucesso_fora_do_ramo9'] and not item['literais_python'] and not item['sobras']
            and not item['proibidas'] and item['aceite_dito'] and (bool(Vv['qp_causa']) or not nao9) and item['handoff_indice_cheio']['recusou_sem_gravar']
            and rcmp.returncode == 0 and rh2.returncode == 0 and item['handoff']['memoria_topico'] and not item['handoff']['frases_de_sucesso_fora_do_ramo9']
            and not item['handoff']['literais_python'] and item['handoff']['lista_so_o_que_existe'] and item['handoff']['diz_o_marcador'] in (None, True)
            and item['handoff']['pendencias_v383_herdadas'] and item['handoff']['v1x_dito'] and item['handoff']['marcador_do_servidor'] and item['handoff']['MEMORY_md_bytes'] <= 24000
            and (nao9 or (rc_.returncode == 0)) and (not nao9 or so_pilar))
    if nome == 'RAMO9_NEGATIVOS':
        ok_i = ok_i and len(Vv['qp_neg_prereg_l']) >= 4 and any('FOLDS_WINDOW em 0 de' in n for n in Vv['qp_neg_prereg_l']) and 'da lista do pré-registro' in tx['linhagem']
    item['ok'] = ok_i; ok = ok and ok_i
    R['variantes'][nome] = item
    print('[%-22s] classe %-12s conf rc %s (%d falhas, so pilar %s, aceite %s) | P %s | arq %s | sucesso fora do 9: %s | handoff cheio rc %s sem gravar %s | handoff rc %s | %s'
          % (nome, Vv['qp_classe'], rc_.returncode, len(falhas), so_pilar, bool(ex), o['P'] or '-', Vv['qp_arq_tipo'], item['frases_de_sucesso_fora_do_ramo9'] or '-',
             rh.returncode, item['handoff_indice_cheio']['recusou_sem_gravar'], rh2.returncode, 'OK' if ok_i else 'FALHOU'), flush=True)

# (3) o formato: o cabecalho de cada bloco da v384 casa o MESMO padrao que o bloco da v383 nas superficies reais (so leitura)
D = r'\d\d/\d\d/\d{4}'; S16 = r'`[0-9a-f]{16}`'
PAD = {
    'linhagem': (os.path.join(A.NOS_REAL, 'MEMORIA_DA_LINHAGEM.md'), 'v383', r'^## ' + D + r' — \*\*v(\d{3}) SELADA \((?:COMPLETA|INTERMEDIÁRIA)\)\*\* ' + S16 + r' — \S'),
    'desenho': (os.path.join(A.NOS_REAL, 'DESENHO_DO_FECHAMENTO_QG.md'), 'v383', r'^## ADENDO — ' + D + r' · v(\d{3}) SELADA \((?:COMPLETA|INTERMEDIÁRIA)\) ' + S16 + r' — \S'),
    'atlas': (os.path.join(A.ATLAS_DIR_REAL, 'TGL_ATLAS.md'), 'v383', r'^## ' + D + r' — v(\d{3}) SELADA \((?:COMPLETA|INTERMEDIÁRIA)\): \S'),
    'topico_missao': (os.path.join(A.UMEM_REAL, 'missao-ultima-flag-um-py.md'), 'v383', r'^## ' + D + r' — v(\d{3}) SELADA ' + S16 + r' \(\d+/\d+; (?:COMPLETA|INTERMEDIÁRIA); gate INTOCADO\): \S'),
    'topico_central': (os.path.join(A.UMEM_REAL, 'central-de-patentes-estado.md'), 'v383', r'^\*\*' + D + r' — v(\d{3}) SELADA \((?:COMPLETA|INTERMEDIÁRIA)\):\*\* `um\.py` ' + S16 + r' \([\d,]+ B\) sobre a v\d{3} ' + S16),
    'topico_regra': (os.path.join(A.UMEM_REAL, 'beta-e-a-regra-matriz-02out.md'), 'v383', r'^## ' + D + r' — v(\d{3}) SELADA ' + S16 + r': \S'),
    'topico_regimes': (os.path.join(A.UMEM_REAL, 'regra-dos-dois-regimes.md'), 'v383', r'^## ' + D + r' — v(\d{3}) SELADA ' + S16 + r': \S'),
    'topico_suspensao': (os.path.join(A.UMEM_REAL, 'v382-custodia-suspensa.md'), 'v383', r'^## ' + D + r' — v(\d{3}) SELADA ' + S16 + r': \S'),
    'marca_missao': (os.path.join(A.UMEM_REAL, 'MEMORY.md'), 'v383', r'\*\*v(\d{3}) SELADA \d\d/\d\d ' + S16 + r' \d+/\d+ (?:COMPLETA|INTERMEDIÁRIA) \('),
    'linha_handoff': (os.path.join(A.UMEM_REAL, 'MEMORY.md'), 'v383', r'^- \[HANDOFF v(\d{3}) — [^\]]+\]\(handoff-v\d{3}-custodia\.md\) — \*\*\d\d/\d\d, para a sessão do site\*\*: \S'),
}
for fn, (arq, ver, pad) in PAD.items():
    rx = re.compile(pad, re.M)
    real = open(arq, encoding='utf-8', errors='replace').read()
    v383 = [m.group(0) for m in rx.finditer(real) if m.group(1) == ver[1:]]
    blk = getattr(T, fn)(V)
    v384 = [m.group(0) for m in rx.finditer(blk.replace('\r\n', '\n').split('\n', 3)[2] if fn in ('desenho', 'atlas') else blk) if m.group(1) == '384']
    R['formato'][fn] = {'v383_casa': bool(v383), 'v384_casa': bool(v384), 'v383_exemplo': (v383[0][:120] if v383 else None), 'v384_exemplo': (v384[0][:120] if v384 else None)}
    if not (v383 and v384):
        ok = False
# os blocos que comecam com '---' (desenho e atlas): a mesma moldura da v383
R['formato']['moldura_desenho_atlas'] = all(getattr(T, f)(V).startswith('---\n\n## ') for f in ('desenho', 'atlas'))
ok = ok and R['formato']['moldura_desenho_atlas']
# (4) os numeros digitados nos moldes (literais de string de textos_v384.py)
src = open(os.path.join(HERE, 'textos_v384.py'), encoding='utf-8').read()
for node in ast.walk(ast.parse(src)):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        for m in re.finditer(r'(?<![\w{])\d[\d.,/]*', node.value):
            R['digitados'].append(m.group(0))
R['digitados'] = sorted(set(R['digitados']), key=lambda x: (len(x), x))
for f in ('textos_v384.py', 'leitura_v384.py', 'superficies_v384.py', 'handoff_v384.py', 'registrar_resultado_v384.py', 'patch_arvore_indice_v384.py', 'manifesto_v384.py',
          'espera_rito_v384.py', 'arquivar_v384.py', 'compactar_memory_para_v384.py', 'ambiente_v384.py', 'montar_nos_sintetico_v384.py', 'preparar_conferidor_ensaio_v384.py',
          'variantes_pilar_v384.py', 'ensaio_guardas_v384.py', 'ensaio_v384.py', 'conferir_reais_intocados_v384.py'):
    ast.parse(open(os.path.join(HERE, f), encoding='utf-8').read())
R['compilam'] = True
R['tudo_passa'] = bool(ok and not P)
os.makedirs(AMB['saidas'], exist_ok=True)
out = A.pode_escrever(os.path.join(AMB['saidas'], 'testar_formatos_v384.json'), AMB)
open(out + '.tmp', 'w', encoding='utf-8').write(json.dumps(R, ensure_ascii=False, indent=1)); os.replace(out + '.tmp', out)
print('problemas da leitura:', P or 'nenhum')
print('render (leitura):', {k: (v.get('bytes'), v.get('sobra'), v.get('proibidas')) for k, v in R['render']['leitura'].items()})
print('numeros de V no diario:', R['numeros_de_V_no_diario'])
print('literais do Python no render:', R['literais_python_no_render'] or 'nenhum')
print('formato (v383 x v384):', json.dumps({k: (v if isinstance(v, bool) else (v['v383_casa'], v['v384_casa'])) for k, v in R['formato'].items()}, ensure_ascii=False))
print('numeros digitados nos moldes:', R['digitados'])
print('palavras proibidas:', R['proibidas'] or 'nenhuma')
print('variantes:', {k: v.get('ok') for k, v in R['variantes'].items()})
print('TUDO PASSA' if R['tudo_passa'] else 'NAO PASSA', '->', out)
sys.exit(0 if R['tudo_passa'] else 1)
