# -*- coding: utf-8 -*-
# A LEITURA da rodada v394 (molde: leitura_v393.py): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v394, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo e do stdout do rito.
# v394: os registros NOVOS do core sao tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394 (runtime) e cunhagens_v394, kh_n1_cobertura_v394 (por spec; ESPERADOS[registros_v394]); os da v393
# (pedras_v393, regra_consumidor_v393, coracao_e_selo_gravitacional_v393, cunhagens_regra_v393, kh_n1_cobertura_v393) seguem no core e tem de seguir selados; os 189 modulos novos de kernel vem de
# ESPERADOS[pedras_sha256] e sao conferidos aqui, um a um, contra o arquivo do kernel do Nos. A escada vem de ESPERADOS[escada_v393_e_v394] e ESPERADOS[escada]; a troca dita (so numeros) e' a de ESPERADOS[troca_dita].
# Os nomes de campo de ESPERADOS lidos aqui sao os do molde subidos de versao; onde o campo e' PALPITE a linha leva a marca AJUSTAR_V394_AO_ESPERADOS (ESPERADOS_v394.json e' gerado por outro processo).
# Diferencas para a v393: o pacote e' a pasta V; os registros novos sao DESCOBERTOS por comparacao com ESPERADOS[vereditos_v393]; o conferidor e' lido da copia em pos_rito/conferidor (a cadeia o copia antes).
import glob, hashlib, json, os, re, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)            # work\cadeia_de_selo\v394
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\S+|inicio |fim )')
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY|TGL_PRO' + 'VED')
REG_V393 = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")   # da v393: seguem no core e seguem selados (nao sao 'novos' da v394)
REG_FIXOS = ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394")   # os cinco registros NOVOS do core v394; + os de ESPERADOS[registros_v394] (REG_TODOS, dentro de ler)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()


def _aplicado():
    ps = sorted(glob.glob(os.path.join(PK, 'APLICADO_AO_CANONICO_*.json'))); assert ps, 'APLICADO_AO_CANONICO_*.json ausente em ' + PK
    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]


def ler():
    P = []
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v394.json'), encoding='utf-8')); CM = json.load(open(os.path.join(PK, 'CANDIDATO_v394.json'), encoding='utf-8'))
    ap, app = _aplicado()
    REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v394') or ())))   # AJUSTAR_V394_AO_ESPERADOS: campo registros_v394 (como registros_v393)
    core = json.load(open(os.path.join(NOS, 'um_absoluto.json'), encoding='utf-8'))['core']; selo = json.load(open(os.path.join(NOS, 'um_absoluto_selo.json'), encoding='utf-8'))
    stp = os.path.join(NOS, 'rodada_v394_stdout.txt'); out = open(stp, encoding='utf-8', errors='replace').read() if os.path.exists(stp) else ''
    V = {'nos': NOS, 'aplicado_json': app, 'pk': PK}
    if not out:
        P.append('rodada_v394_stdout.txt ausente ou vazio')
    V['s64'] = sha(os.path.join(NOS, 'um.py')); V['s16'] = V['s64'][:16]; V['umb'] = os.path.getsize(os.path.join(NOS, 'um.py'))
    if str((selo.get('sha256') or {}).get('um.py', '')) != V['s64']:
        P.append('selo.sha256(um.py) != disco')
    if not (ap['um_py_novo']['sha16'] == V['s16'] == ESP['candidato_sha16'] == CM['sha16']):
        P.append('um.py do disco != instalado/esperado/candidato')
    V['base16'] = ap['backups']['um.py']['sha16']; V['base_backup'] = ap['backups']['um.py']['backup']
    if V['base16'] != ESP['origem_sha16']:
        P.append('a base substituida != a v393 selada')
    V['n_patches'] = len(CM['patches']); V['patches'] = ', '.join(p['id'] for p in CM['patches'])
    V['instalado_em'] = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    m = re.search(r'teoremas limpos:\s*(\d+)/(\d+)', out); V['teor'] = '%s/%s' % m.groups() if m else 'AUSENTE'
    V['escada_antes'] = ESP['escada_v393_e_v394'][0]; V['escada_depois'] = ESP['escada'][1]   # AJUSTAR_V394_AO_ESPERADOS: campo escada_v393_e_v394
    if not m or m.group(1) != m.group(2) or int(m.group(1)) != ESP['escada'][1]:
        P.append('teoremas limpos ausente, N != M ou != %s (%s)' % (ESP['escada'][1], V['teor']))
    if 'FAIL_CLOSED_SELFTEST_PASSED' not in out or selo.get('fail_closed_selftest') != 'FAIL_CLOSED_SELFTEST_PASSED':
        P.append('selftest nao PASSED')
    if '>>> TGL_KERNEL_FORMALIZATION_FAILED <<<' in out or '>>> TGL_KERNEL_STAGE1_VERIFIED' not in out:
        P.append('a verificacao principal do kernel nao leu VERIFIED')
    if 'SEAL_WITHHELD' in out:
        P.append('SEAL_WITHHELD no stdout')
    m = re.search(r'\[selo\] rite_checkpoints: chave (\S+) ; reaproveitados (\d+)', out)
    V['compl'] = 'COMPLETA' if (m and m.group(1) == 'desligada' and m.group(2) == '0') else 'INTERMEDIÁRIA'
    if V['compl'] != 'COMPLETA':
        P.append('rodada nao COMPLETA')
    sujo = [l for l in out.splitlines() if 'Traceback' in l or l.startswith('[selo] AVISO')]
    if sujo:
        P.append('stdout com Traceback/AVISO: %s' % sujo[:3])
    linhas = [l for l in out.splitlines() if l.strip() and not TRAILER_RE.match(l.strip())]
    if not linhas or not FINAL_RE.match(linhas[-1]):
        P.append('a ultima linha do stdout nao e a linha final do rito')
    mrc = re.findall(r'^RITO_RC=(\S+)', out, flags=re.M); V['rc'] = mrc[-1] if mrc else 'NAO_LIDO'
    if V['rc'] != '0':
        P.append('rc do rito nao lido como 0 (%s)' % V['rc'])
    if len([l for l in out.splitlines() if '[v394]' in l]) < 1:
        P.append('o stdout nao tem a linha [v394]')
    hp = os.path.join(PK, 'rito_horarios_v394.txt'); V['horarios'] = open(hp, encoding='utf-8').read().split() if os.path.exists(hp) else []
    V['selo_ts'] = selo.get('timestamp'); V['um_version'] = selo.get('um_version'); V['qg'] = selo.get('qg_closure_verdict')
    if V['um_version'] != 'v394':
        P.append('o selo nao e v394')
    if V['qg'] != ESP['qg_closure_verdict']:
        P.append('o gate MUDOU')
    qg = core.get('qg_closure') or {}
    V['n18'] = sum(1 for fam in ('formal_flags', 'physics_flags', 'experiment_flags') for v in (qg.get(fam) or {}).values() if v is True)
    if V['n18'] != 18:
        P.append('as bandeiras do gate nao sao 18 True (%s)' % V['n18'])
    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):
        V['h_' + k] = sha(os.path.join(NOS, k))[:16] if os.path.exists(os.path.join(NOS, k)) else 'AUSENTE'
    V['artigos'] = {os.path.basename(p): sha(p)[:16] for p in sorted(glob.glob(os.path.join(NOS, 'um_absoluto_??.pdf')) + glob.glob(os.path.join(NOS, 'um_absoluto_??.txt')))}
    cp = os.path.join(HERE, 'conferidor', 'conferencia_rito_v394.json')
    if os.path.exists(cp):
        C = json.load(open(cp, encoding='utf-8'))
        V['conf16'] = sha(cp)[:16]; V['conf_dm'] = '%d/%d' % (sum(1 for v in C['deve_mudar'].values() if v), len(C['deve_mudar']))
        V['conf_np'] = '%d/%d' % (sum(1 for v in C['nao_pode_mudar'].values() if v), len(C['nao_pode_mudar'])); V['n_ver_mudaram'] = len(C.get('vereditos_que_mudaram_fora_da_troca') or {})
        V['servidor'] = 'marcador de servidor parado ficou: %s' % C.get('marcador_ficou')
        if C.get('tudo_bate') is not True:
            P.append('o conferidor NAO bateu')
        if C.get('marcador_ficou'):
            P.append('o marcador .servidor_parado_pelo_rito ficou: o servidor do modelo pode estar parado')
    else:
        V['conf16'] = 'AUSENTE'; P.append('a conferencia do rito nao foi achada em pos_rito/conferidor')
    V['troca_dita'] = list(ESP['troca_dita'])
    V['n_ver'] = len(ESP['vereditos_v393'])
    # --- os registros novos: descobertos por comparacao com o que a v393 ja tinha
    novos = []
    for k, r in core.items():
        if isinstance(r, dict) and 'verdict' in r and k not in ESP['vereditos_v393']:
            novos.append(k)
    V['registros_novos'] = sorted(novos)
    for k in REG_TODOS:
        if k not in novos:
            P.append('registro obrigatorio ausente do core: %s' % k)
    V['registros'] = {}
    for k in novos:
        r = core.get(k) or {}
        V['registros'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is False or (k in REG_TODOS and r.get('all_verified') is not True):
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
    for k in V['troca_dita']:
        r = core.get(k) or {}
        if r.get('all_verified') is False:
            P.append('%s (troca dita) nao selou' % k)
    # v394: os modulos novos de kernel vem de ESPERADOS[pedras_sha256] (o ensaio a seco do candidato) e cada um e' conferido AQUI contra o arquivo do kernel do Nos (sha256); o numero tem de ser o de kernel_modulos_novos_v394.json
    pv = core.get('pedras_v394') or {}   # AJUSTAR_V394_AO_ESPERADOS: se a v394 tiver um registro de pedras proprio (nao esta entre os cinco), ele e' lido aqui; sem ele n_flags/n_decl ficam None
    V['pedras'] = []
    for rel_, h_ in sorted((ESP.get('pedras_sha256') or {}).items()):
        pth_ = os.path.join(NOS, 'tgl_kernel', *rel_.split('/'))
        V['pedras'].append({'modulo': 'TGLExt.' + rel_[len('TGLExt/'):-len('.lean')].replace('/', '.'), 'bandeiras': None, 'decl': None, 'ok': bool(rel_.startswith('TGLExt/') and rel_.endswith('.lean') and os.path.isfile(pth_) and sha(pth_) == h_)})
    V['n_pedras'] = len(V['pedras']); V['n_flags'] = (pv.get('bandeiras') or [None, None])[0]; V['n_flags_de'] = (pv.get('bandeiras') or [None, None])[1]
    V['n_decl'] = (pv.get('declaracoes_no_trio') or [None, None])[0]; V['n_decl_de'] = (pv.get('declaracoes_no_trio') or [None, None])[1]
    V['pedras_verdict'] = pv.get('verdict'); V['verbatim_pedras'] = {k: {'sha256': (v or {}).get('sha256'), 'ok': (v or {}).get('embedded_ok')} for k, v in (pv.get('verbatim') or {}).items()}
    njp_ = os.path.join(PK, 'kernel_modulos_novos_v394.json'); nj_ = json.load(open(njp_, encoding='utf-8')) if os.path.exists(njp_) else {}
    n_esperado_ = nj_.get('novos') if isinstance(nj_.get('novos'), int) else len(nj_.get('novos') or [])
    if not V['n_pedras'] or V['n_pedras'] != n_esperado_ or any(p['ok'] is not True for p in V['pedras']):
        P.append('modulos novos do kernel: numero (%s) != kernel_modulos_novos_v394.json (%s) ou algum arquivo do Nos difere do sha256 de ESPERADOS[pedras_sha256]' % (V['n_pedras'], n_esperado_))
    vs = core.get('varredura_e_sorry_v392') or {}
    V['varr'] = vs.get('varredura') or {}; V['varr_verdict'] = vs.get('verdict')
    V['axiom_report_n'] = len((core.get('kernel_formalization') or {}).get('axiom_report') or {})
    ep = core.get('estatuto_da_prova_v391') or {}
    V['ep_verdict'] = ep.get('verdict')
    V['fd390'] = (core.get('fundacao_v390') or {}).get('verdict')
    V['verbatins'] = {k: {'sha16': str(v.get('sha256'))[:16], 'bytes': v.get('bytes')} for k, v in (ESP.get('cunhagens') or {}).items()}   # AJUSTAR_V394_AO_ESPERADOS: campo cunhagens (sha256 das cunhagens do operador embutidas)
    # --- v394: os cinco registros novos conferidos contra o ensaio a seco registrado em ESPERADOS, e os da v393 (a regra e o coracao), que seguem no core e tem de seguir selados; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    for k_ in REG_V393:
        if (core.get(k_) or {}).get('all_verified') is not True:
            P.append('%s (registro da v393) deixou de selar' % k_)
    RV_ = dict(ESP.get('vereditos_novos_v394') or {}); RV_.update(ESP.get('registros_v394') or {})   # AJUSTAR_V394_AO_ESPERADOS: campos registros_v394 (por spec) e/ou vereditos_novos_v394 (runtime): registro -> veredito do ensaio a seco
    V['reg394'] = {}
    for k_ in REG_FIXOS:
        r_ = core.get(k_) or {}
        V['reg394'][k_] = {'verdict': r_.get('verdict'), 'ok': r_.get('all_verified')}
        esp_v_ = RV_.get(k_) or ESP.get('veredito_' + k_ + '_do_ensaio')
        if esp_v_ is None:
            P.append('ESPERADOS_v394 nao traz o veredito do ensaio a seco de %s (registros_v394 / vereditos_novos_v394 / veredito_%s_do_ensaio): nao ha com que conferir' % (k_, k_))
        elif r_.get('verdict') != esp_v_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k_)
    rf_ = core.get('rede_fock_v394') or {}   # limite dito: o contrato conjunto da rede NAO foi habitado (nenhum certificado inteiro); AJUSTAR_V394_AO_ESPERADOS: campo whole_certificate_inhabited do registro
    if rf_.get('whole_certificate_inhabited') is not False:
        P.append('rede_fock_v394: whole_certificate_inhabited deve ser False (a rede inteira nao foi habitada) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    rc = core.get('regra_consumidor_v393') or {}; co = core.get('coracao_e_selo_gravitacional_v393') or {}; cu = core.get('cunhagens_v394') or {}; kh = core.get('kh_n1_cobertura_v394') or {}
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}   # o nome 'axiom_coverage_v392' e' do core (historico); segue na v394
    CB = ESP.get('cobertura_kh_n1') or {}   # AJUSTAR_V394_AO_ESPERADOS: campo cobertura_kh_n1
    cr = rc.get('criterio') or {}; nu = rc.get('numeros') or {}; rx = rc.get('replica_do_codex') or {}; sr = co.get('satisfacao_pela_regra') or {}
    ei = co.get('evidencia_espectral_independente') or {}
    V['cons'] = {'verdict': rc.get('verdict'), 'pontos': nu.get('pontos'), 'verificacoes': nu.get('verificacoes'), 'compl_ini': nu.get('complemento_inicial'), 'compl_fin': nu.get('complemento_final'),
                 'dimfix': nu.get('dimensao_fixa_complexa'), 'tol': cr.get('tolerancia_numerica'), 'hash_final': nu.get('ultimo_hash_da_trajetoria'), 'replica_hash_igual': rx.get('hash_final_igual')}   # da v393 (informativo)
    V['cora'] = {'verdict': co.get('verdict'), 'prev': co.get('previsao_independente'), 'G': co.get('G_derivado'), 'criterio': sr.get('criterio'), 'veredito_regra': sr.get('veredito_da_regra'),
                 'espectral_hoje': ei.get('hoje')}   # da v393 (informativo)
    V['kh'] = {'decl': cov.get('decl'), 'thm': cov.get('thm'), 'fora': cov.get('fora_do_trio'), 'nao_lidas': cov.get('nao_lidas_pelo_regex'), 'verdict': kh.get('verdict')}
    V['cunh_verdict'] = cu.get('verdict')
    if not (CB and cov.get('ok') is True and cov.get('decl') == CB.get('decl') and cov.get('thm') == CB.get('thm') and cov.get('fora_do_trio') == 0 and cov.get('nao_lidas_pelo_regex') == CB.get('nao_lidas_pelo_regex')):
        P.append('cobertura KH-N1 do rito != ESPERADOS (constantes, teoremas, fora do trio, nao lidas) ou ESPERADOS sem cobertura_kh_n1')
    qp = core.get('quantum_pillar_v384') or {}; V['pilar'] = {'mode': qp.get('mode'), 'result16': str(qp.get('result_sha256'))[:16]}
    V['data'] = datetime.datetime.now().strftime('%d/%m/%Y')
    return V, P


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    V, P = ler()
    print(json.dumps({k: v for k, v in V.items() if k not in ('registros', 'pedras')}, ensure_ascii=False, indent=1, default=str)[:4000])
    print('PROBLEMAS:', P if P else 'nenhum'); sys.exit(1 if P else 0)
