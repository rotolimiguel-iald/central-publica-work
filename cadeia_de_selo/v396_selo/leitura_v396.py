# -*- coding: utf-8 -*-
# A LEITURA da rodada v396 (molde: leitura_v395.py FINAL, o que rodou em 21/10): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v396, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo e do stdout do rito.
# v396: os registros NOVOS do core sao testemunha_estatica_v396 (runtime: a funcao chamada NA FRACTALIZACAO DO UM, logo depois do bloco do psibit_v395) e cunhagens_v396 e kh_n1_cobertura_v396 (por spec; ESPERADOS[registros_v396]); os da v395 (psibit_v395,
# cunhagens_v395, kh_n1_cobertura_v395), os da v394 e os da v393 seguem no core e tem de seguir selados; o modulo novo de kernel (TGLExt/TestemunhaEstatica.lean) vem de ESPERADOS[pedras_sha256] e e' conferido aqui contra o arquivo do kernel do Nos.
# A escada vem de ESPERADOS[escada_v395_e_v396] e ESPERADOS[escada]; a troca dita (so numeros) e' a de ESPERADOS[troca_dita]. O registro testemunha_estatica_v396 e' conferido por inteiro (formal + suporte + mecanica + escada + fonte embutida + beta + inscricoes;
# a composicao incondicional no kernel; a face de Fock do psion CONDICIONAL, declarada em Psibit.lean FORA da pedra e sem habitante exibido) e a linha `[v396] ... registros por spec` do stdout do rito tem de dizer selados == registros por spec;
# o AVISO da v396 (e de qualquer bloco v393 a v395) no stdout reprova.
# Diferencas para a v395: os registros novos sao DESCOBERTOS por comparacao com ESPERADOS[vereditos_v395]; o conferidor e' lido da copia em pos_rito/conferidor (a cadeia o copia antes); V['testemunha'], V['reg396'] e V['patch_ids'] sao os campos da v396;
# a face condicional do psibit_v395 (bandeira True, sem habitante) e os registros da v395 sao conferidos de novo.
import glob, hashlib, json, os, re, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)            # work\cadeia_de_selo\v396
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\S+|inicio |fim )')
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY|TGL_PRO' + 'VED')
REG_V393 = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")   # da v393: seguem no core e seguem selados (nao sao 'novos' da v396)
REG_V394 = ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394")   # da v394: seguem no core e seguem selados (nao sao 'novos' da v396)
REG_V395 = ("psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395")   # da v395: seguem no core e seguem selados (nao sao 'novos' da v396)
REG_FIXOS = ("testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396")   # os tres registros NOVOS do core v396; + os de ESPERADOS[registros_v396] (REG_TODOS, dentro de ler)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()


def _aplicado():
    ps = sorted(glob.glob(os.path.join(PK, 'APLICADO_AO_CANONICO_*.json'))); assert ps, 'APLICADO_AO_CANONICO_*.json ausente em ' + PK
    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]


def ler():
    P = []
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v396.json'), encoding='utf-8')); CM = json.load(open(os.path.join(PK, 'CANDIDATO_v396.json'), encoding='utf-8'))
    ap, app = _aplicado()
    REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v396') or ())))
    core = json.load(open(os.path.join(NOS, 'um_absoluto.json'), encoding='utf-8'))['core']; selo = json.load(open(os.path.join(NOS, 'um_absoluto_selo.json'), encoding='utf-8'))
    stp = os.path.join(NOS, 'rodada_v396_stdout.txt'); out = open(stp, encoding='utf-8', errors='replace').read() if os.path.exists(stp) else ''
    V = {'nos': NOS, 'aplicado_json': app, 'pk': PK}
    if not out:
        P.append('rodada_v396_stdout.txt ausente ou vazio')
    V['s64'] = sha(os.path.join(NOS, 'um.py')); V['s16'] = V['s64'][:16]; V['umb'] = os.path.getsize(os.path.join(NOS, 'um.py'))
    if str((selo.get('sha256') or {}).get('um.py', '')) != V['s64']:
        P.append('selo.sha256(um.py) != disco')
    if not (ap['um_py_novo']['sha16'] == V['s16'] == ESP['candidato_sha16'] == CM['sha16']):
        P.append('um.py do disco != instalado/esperado/candidato')
    V['base16'] = ap['backups']['um.py']['sha16']; V['base_backup'] = ap['backups']['um.py']['backup']
    if V['base16'] != ESP['origem_sha16']:
        P.append('a base substituida != a v395 selada')
    V['n_patches'] = len(CM['patches']); V['patches'] = ', '.join(p['id'] for p in CM['patches']); V['patch_ids'] = [p['id'] for p in CM['patches']]
    V['instalado_em'] = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    m = re.search(r'teoremas limpos:\s*(\d+)/(\d+)', out); V['teor'] = '%s/%s' % m.groups() if m else 'AUSENTE'
    V['escada_antes'] = ESP['escada_v395_e_v396'][0]; V['escada_depois'] = ESP['escada'][1]
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
    if len([l for l in out.splitlines() if '[v396]' in l]) < 1:
        P.append('o stdout nao tem a linha [v396]')
    if [l for l in out.splitlines() if '[v396] AVISO' in l]:
        P.append('o stdout traz AVISO da v396 (a testemunha estatica ou os registros por spec nao rodaram): %s' % [l.strip()[:200] for l in out.splitlines() if '[v396] AVISO' in l][:2])
    elif [l for l in out.splitlines() if re.search(r'\[v39[3-5]\] AVISO', l)]:
        P.append('o stdout traz AVISO de um bloco anterior (v393 a v395): %s' % [l.strip()[:200] for l in out.splitlines() if re.search(r'\[v39[3-5]\] AVISO', l)][:2])
    m_sp = re.search(r'\[v396\] a testemunha estatica \(o psion habita a fronteira\): .*\| registros por spec: (\d+) \(selados (\d+)\)', out)
    if not m_sp or m_sp.group(1) != m_sp.group(2) or int(m_sp.group(1)) != len(ESP.get('registros_v396') or {}):
        P.append('a linha [v396] do stdout nao diz registros por spec selados == %d (%s)' % (len(ESP.get('registros_v396') or {}), m_sp.groups() if m_sp else 'ausente'))
    hp = os.path.join(PK, 'rito_horarios_v396.txt'); V['horarios'] = open(hp, encoding='utf-8').read().split() if os.path.exists(hp) else []
    V['selo_ts'] = selo.get('timestamp'); V['um_version'] = selo.get('um_version'); V['qg'] = selo.get('qg_closure_verdict')
    if V['um_version'] != 'v396':
        P.append('o selo nao e v396')
    if V['qg'] != ESP['qg_closure_verdict']:
        P.append('o gate MUDOU')
    qg = core.get('qg_closure') or {}
    V['n18'] = sum(1 for fam in ('formal_flags', 'physics_flags', 'experiment_flags') for v in (qg.get(fam) or {}).values() if v is True)
    if V['n18'] != 18:
        P.append('as bandeiras do gate nao sao 18 True (%s)' % V['n18'])
    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):
        V['h_' + k] = sha(os.path.join(NOS, k))[:16] if os.path.exists(os.path.join(NOS, k)) else 'AUSENTE'
    V['artigos'] = {os.path.basename(p): sha(p)[:16] for p in sorted(glob.glob(os.path.join(NOS, 'um_absoluto_??.pdf')) + glob.glob(os.path.join(NOS, 'um_absoluto_??.txt')))}
    cp = os.path.join(HERE, 'conferidor', 'conferencia_rito_v396.json')
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
    V['n_ver'] = len(ESP['vereditos_v395'])
    # --- os registros novos: descobertos por comparacao com o que a v395 ja tinha
    novos = []
    for k, r in core.items():
        if isinstance(r, dict) and 'verdict' in r and k not in ESP['vereditos_v395']:
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
    # v396: o modulo novo de kernel vem de ESPERADOS[pedras_sha256] (o ensaio a seco do candidato) e e' conferido AQUI contra o arquivo do kernel do Nos (sha256); o numero tem de ser o de kernel_modulos_novos_v396.json
    V['pedras'] = []
    for rel_, h_ in sorted((ESP.get('pedras_sha256') or {}).items()):
        pth_ = os.path.join(NOS, 'tgl_kernel', *rel_.split('/'))
        V['pedras'].append({'modulo': 'TGLExt.' + rel_[len('TGLExt/'):-len('.lean')].replace('/', '.'), 'bandeiras': None, 'decl': None, 'ok': bool(rel_.startswith('TGLExt/') and rel_.endswith('.lean') and os.path.isfile(pth_) and sha(pth_) == h_)})
    V['n_pedras'] = len(V['pedras'])
    njp_ = os.path.join(PK, 'kernel_modulos_novos_v396.json'); nj_ = json.load(open(njp_, encoding='utf-8')) if os.path.exists(njp_) else {}
    n_esperado_ = nj_.get('novos') if isinstance(nj_.get('novos'), int) else len(nj_.get('novos') or [])
    if not V['n_pedras'] or V['n_pedras'] != n_esperado_ or any(p['ok'] is not True for p in V['pedras']):
        P.append('modulos novos do kernel: numero (%s) != kernel_modulos_novos_v396.json (%s) ou algum arquivo do Nos difere do sha256 de ESPERADOS[pedras_sha256]' % (V['n_pedras'], n_esperado_))
    vs = core.get('varredura_e_sorry_v392') or {}
    V['varr'] = vs.get('varredura') or {}; V['varr_verdict'] = vs.get('verdict')
    V['axiom_report_n'] = len((core.get('kernel_formalization') or {}).get('axiom_report') or {})
    ep = core.get('estatuto_da_prova_v391') or {}
    V['ep_verdict'] = ep.get('verdict')
    V['fd390'] = (core.get('fundacao_v390') or {}).get('verdict')
    V['verbatins'] = {k: {'sha16': str(v.get('sha256'))[:16], 'bytes': v.get('bytes')} for k, v in (ESP.get('cunhagens') or {}).items()}
    # --- v396: os tres registros novos conferidos contra o ensaio a seco registrado em ESPERADOS, e os da v395, da v394 e da v393, que seguem no core e tem de seguir selados; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    for k_ in REG_V393 + REG_V394 + REG_V395:
        if (core.get(k_) or {}).get('all_verified') is not True:
            P.append('%s (registro da v395, da v394 ou da v393) deixou de selar' % k_)
    RV_ = dict(ESP.get('vereditos_novos_v396') or {}); RV_.update(ESP.get('registros_v396') or {})   # registro -> veredito do ensaio a seco (testemunha_estatica_v396 e' runtime; cunhagens_v396 e kh_n1_cobertura_v396 sao por spec)
    V['reg396'] = {}
    for k_ in REG_FIXOS:
        r_ = core.get(k_) or {}
        V['reg396'][k_] = {'verdict': r_.get('verdict'), 'ok': r_.get('all_verified')}
        esp_v_ = RV_.get(k_)
        if esp_v_ is None:
            P.append('ESPERADOS_v396 nao traz o veredito do ensaio a seco de %s (vereditos_novos_v396 / registros_v396): nao ha com que conferir' % k_)
        elif r_.get('verdict') != esp_v_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k_)
    kf_ = (core.get('kernel_formalization') or {})
    rf_ = core.get('rede_fock_v394') or {}   # limite dito: o contrato conjunto da rede segue NAO habitado (a face de Fock do psion depende dele)
    if rf_.get('whole_certificate_inhabited') is not False:
        P.append('rede_fock_v394: whole_certificate_inhabited deve seguir False (o contrato conjunto da rede segue aberto) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    if kf_.get('ext_bin394_0001') is not True:
        P.append('a bandeira da pedra da v394 (ext_bin394_0001) nao segue True no kernel do rito')
    # a face de Fock do psion segue como a v395 a selou: CONDICIONAL, sem habitante exibido, com a bandeira True e declarada em Psibit.lean (a v396 a deixa FORA da pedra nova)
    pb_ = core.get('psibit_v395') or {}; pbc_ = pb_.get('conditional_psion_face') or {}
    if not (pbc_.get('status') == 'CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE' and pbc_.get('inhabitant_exhibited') is False and pbc_.get('flag_true') is True and kf_.get(pbc_.get('flag')) is True and pbc_.get('declared_in') == 'TGLExt/Psibit.lean'):
        P.append('psibit_v395: a face do psion deixou de estar como CONDICIONAL sem habitante exibido (bandeira True, declarada em TGLExt/Psibit.lean)')
    # o registro testemunha_estatica_v396, conferido por inteiro (os textos leem os numeros dele)
    ts_ = core.get('testemunha_estatica_v396') or {}; EP_ = ESP.get('testemunha') or {}; CT_ = ESP.get('contrato_testemunha') or {}
    mech_ = ts_.get('mechanics') or {}; unc_ = ts_.get('unconditional') or {}; fk_ = ts_.get('fock_face') or {}
    ft_ = ts_.get('formal_theorems') or {}; sp_ = ts_.get('support_theorems') or {}
    V['testemunha'] = {'verdict': ts_.get('verdict'), 'ok': ts_.get('all_verified'), 'values': ts_.get('values') or {}, 'n_checks': mech_.get('n_checks'), 'mech_passed': mech_.get('passed'),
                       'n_teoremas': len(ft_), 'teoremas_true': bool(ft_) and all(x_ is True for x_ in ft_.values()), 'n_suporte': len(sp_), 'suporte_true': bool(sp_) and all(x_ is True for x_ in sp_.values()),
                       'unconditional': unc_, 'fock': fk_, 'beta_ok': ts_.get('beta_ok'), 'beta_core_rel_diff': ts_.get('beta_core_rel_diff'), 'alpha_two_names_same': ts_.get('alpha_two_names_same'),
                       'exact_ladder': ts_.get('exact_ladder'), 'embedded_source_ok': ts_.get('embedded_source_ok'), 'runtime_executed': ts_.get('runtime_executed'), 'does_not_gate_core': ts_.get('does_not_gate_core'),
                       'inscriptions_ok': bool(ts_.get('inscriptions')) and all(x_ is True for x_ in (ts_.get('inscriptions') or {}).values())}
    falta_ = [k_ for k_ in ('beta', 'pair_rank1_residual', 'pair_idempotence_residual', 'pair_trace', 'pair_purity', 'individual_reduction_residual', 'individual_idempotence_defect', 'individual_purity', 'individual_deficit', 'ln2', 'von_neumann_entropy',
                            'unbonded_purity_deficit', 'bell_gram_residual', 'bell_completeness_residual', 'closed_form_residual', 'eigen_residual', 'line_fixed_residual', 'off_line_min_move', 'global_witness_move', 'limit_residual', 'g_testes', 'tau_testes',
                            'collapse_idempotence_residual', 'collapse_identity_residual', 'collapse_scalarisation_residual', 'collapse_noninjectivity_input_gap', 'collapse_noninjectivity_output_gap') if (ts_.get('values') or {}).get(k_) is None]
    if falta_:
        P.append('testemunha_estatica_v396.values sem os campos que os textos leem: %s' % falta_)
    if not (ts_.get('all_verified') is True and mech_.get('passed') is True and mech_.get('n_checks') == EP_.get('n_checks') and V['testemunha']['teoremas_true'] and V['testemunha']['n_teoremas'] == CT_.get('n_teoremas')
            and V['testemunha']['suporte_true'] and V['testemunha']['n_suporte'] == CT_.get('n_suporte') and ts_.get('exact_ladder') is True and ts_.get('embedded_source_ok') is True and ts_.get('runtime_executed') is True
            and ts_.get('does_not_gate_core') is True and ts_.get('beta_ok') is True and ts_.get('alpha_two_names_same') is True and V['testemunha']['inscriptions_ok']):
        P.append('testemunha_estatica_v396 nao selou inteiro (formal + suporte + mecanica + escada + fonte embutida + beta + inscricoes): ver o registro no core')
    if not (unc_.get('in_kernel') is True and unc_.get('flag_true') is True and unc_.get('theorem') == EP_.get('teorema_incondicional') and unc_.get('flag') == EP_.get('bandeira_incondicional') and set(unc_.get('axioms') or []) <= {'propext', 'Classical.choice', 'Quot.sound'}):
        P.append('testemunha_estatica_v396: a composicao incondicional nao esta no kernel do rito (bandeira True, trio, modulo da pedra)')
    if not (fk_.get('status') == 'CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE' and fk_.get('inhabitant_exhibited') is False and fk_.get('declared_outside_the_stone') is True and fk_.get('linked_to_the_corner_by_a_lemma') is False
            and fk_.get('theorem') == EP_.get('fock_face_teorema') and fk_.get('declared_in') == EP_.get('fock_face_declarada_em')):
        P.append('testemunha_estatica_v396: a face de Fock do psion nao esta como CONDICIONAL, declarada em Psibit.lean fora da pedra e sem habitante exibido')
    cu = core.get('cunhagens_v396') or {}; kh = core.get('kh_n1_cobertura_v396') or {}
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}   # o nome 'axiom_coverage_v392' e' do core (historico); segue na v396
    CB = ESP.get('cobertura_kh_n1') or {}
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
