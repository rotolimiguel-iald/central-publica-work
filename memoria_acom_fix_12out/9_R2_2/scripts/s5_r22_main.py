

# =====================================================================================================================
# R2.2: main com TODOS os cenários e um resumo do que a R2.2 promete em cada um (acrescentado por scripts/s5_gerar.py)
# =====================================================================================================================
def _ult_json(txt):
    for ln in reversed((txt or '').splitlines()):
        ln = ln.strip()
        if ln.startswith('{') and ln.endswith('}'):
            try:
                return json.loads(ln)
            except ValueError:
                return None
    return None


def _base(res):
    return {'originais_identicos': (res.get('comparacao_final') or {}).get('identico_nos_originais'),
            'extras_estranhos': (res.get('comparacao_final') or {}).get('extras_estranhos'),
            'banco_igual_ao_original': res.get('banco_igual_ao_original'),
            'lib_le_o_banco_rc': (res.get('lib_le_o_banco') or {}).get('rc'),
            'schema_final': res.get('schema_final'), 'tmp_orfaos_final': res.get('tmp_orfaos_final'),
            'sim_final': res.get('estado_sim_final')}


def resumo_r22(n, res):
    if 'excecao' in res:
        return {'EXCECAO': res['excecao'][-600:]}
    r = _base(res)
    g = lambda *ks: _get(res, *ks)  # noqa: E731
    if n == 'K4c':
        r.update(reverter_1_status=g('reverter_1', 'status'), reverter_1_rc=g('reverter_1', 'rc'),
                 reverter_1_acao_feita=g('reverter_1', 'acao_feita'), reverter_1_app_religado=g('reverter_1', 'app_religado'),
                 reverter_1_falhas=g('reverter_1', 'falhas'), reverter_1_tem_acao=bool(g('reverter_1', 'acao_requerida')),
                 trava_ve_pendente=g('trava_implantar_ve_pendente'), reverter_2_status=g('reverter_2', 'status'),
                 promessa_nunca_REVERTIDA_e_trava_pendente=(g('reverter_1', 'status') != 'REVERTIDA'
                                                            and g('reverter_1', 'rc') != 0
                                                            and bool((g('trava_implantar_ve_pendente') or {}).get('pendentes'))))
    elif n == 'K4b':
        r.update(reverter_1_status=g('reverter_1', 'status'), reverter_1_rc=g('reverter_1', 'rc'),
                 reverter_1_acao_requerida=(g('reverter_1', 'acao_requerida') or '')[:300],
                 trava_ve_pendente=g('trava_implantar_ve_pendente'), reverter_2_status=g('reverter_2', 'status'),
                 promessa_acao_preenchida=bool(g('reverter_1', 'acao_requerida')))
    elif n == 'K3r':
        acao = g('reverter_k3', 'acao_requerida') or ''
        r.update(reverter_k3_status=g('reverter_k3', 'status'), reverter_k3_rc=g('reverter_k3', 'rc'),
                 acao=acao[:500], diz_fica_parado=g('reverter_k3', 'diz_app_parado'),
                 sim_apos_reverter_k3=g('sim_apos_reverter_k3'), alvos_apos_reverter_k3=g('alvos_apos_reverter_k3'),
                 reverter_normal_status=g('reverter_normal', 'status'),
                 promessa_tarefa_reabilitada_e_estado_lido=(bool((g('sim_apos_reverter_k3') or {}).get('tarefa_habilitada'))
                                                            and not g('reverter_k3', 'diz_app_parado')
                                                            and 'Estado LIDO' in acao))
    elif n in ('P8', 'P8b'):
        acao = g('implantar', 'acao_requerida') or ''
        r.update(implantar_rc=g('implantar', 'rc'), implantar_status=g('implantar', 'status'), acao=acao[:700],
                 leitura=('LACO' if 'LAÇO DE QUEDA PROVÁVEL' in acao else 'LENTO' if 'APP LENTO PROVÁVEL' in acao
                          else 'OUTRA'),
                 tem_como_distinguir='COMO DISTINGUIR' in acao, manda_reverter='reverter.py' in acao,
                 sim_10s_depois=g('sim_10s_depois'), reverter_final=g('reverter_para_limpar_o_ensaio', 'status') or g('reverter', 'status'))
    elif n == 'CFG':
        r.update({k: res.get(k) for k in ('dry_run_antes', 'implantar', 'reverter_config', 'reverter_config_de_novo', 'dry_run_depois')})
    else:
        for k, v in res.items():
            if isinstance(v, dict) and 'status' in v and k not in ('comparacao_final',):
                r[k + '_status'] = v.get('status')
                if 'rc' in v:
                    r[k + '_rc'] = v.get('rc')
                if v.get('app_religado') is not None:
                    r[k + '_app_religado'] = v.get('app_religado')
            elif k.startswith('alvos'):
                r[k] = v
    return r


def _get(d, *ks):
    for k in ks:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def main_r22(sel):
    out = {'at': datetime.now().isoformat(timespec='seconds'), 'preparo': preparar_rev(preparar()), 'cenarios': {},
           'resumo': {}}
    todos = {'K1a': cen_K1a, 'K1b2': cen_K1b2, 'K1c': cen_K1c, 'K1d': cen_K1d, 'K2': cen_K2, 'K3': cen_K3, 'K4': cen_K4,
             'K5': cen_K5, 'K6': cen_K6, 'P8': cen_P8,
             'K2b': cen_K2b, 'K2c': cen_K2c, 'K2d': cen_K2d, 'K3b': cen_K3b, 'K3r': cen_K3r, 'K4b': cen_K4b, 'K4c': cen_K4c,
             'K6b': cen_K6b, 'K6c': cen_K6c, 'P8b': cen_P8b, 'CFG': lambda: cen_CFG()}
    nome = 's5_ensaio_r2_2%s.json' % ('_' + '_'.join(sel) if sel else '')
    for n, fn in todos.items():
        if sel and n not in sel:
            continue
        t = time.time()
        try:
            res = fn()
        except Exception:  # noqa: BLE001
            res = {'excecao': traceback.format_exc()[-2500:]}
        res['segundos'] = round(time.time() - t, 1)
        out['cenarios'][n] = res
        out['resumo'][n] = resumo_r22(n, res)
        (R21 / 'runs' / nome).write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
        print(n, res['segundos'], flush=True)
    print('fim')
