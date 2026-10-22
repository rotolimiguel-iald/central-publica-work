# -*- coding: utf-8 -*-
"""derivar_cadeia_v395.py -- DERIVA a cadeia pos-rito da v395 a partir do molde REAL e FINAL da v394 (cadeia_de_selo/v394/pos_rito, o que RODOU de verdade em 19/10) (molde do derivador: derivar_cadeia_v394.py).
GERA (subida de versao v394 -> v395, v393 -> v394 (a versao anterior), V394 -> V395, V393 -> V394; edicoes pontuais com assert de contagem; os nomes historicos de registros do core NAO sobem, lista PROT):
  chain_pos_rito_v395.sh, leitura_v395.py, superficies_v395.py, fechar_v395.py.
CONFERE (autorais, escritos para a v395; a logica muda e uma derivacao mecanica nao a cobriria): b3_recibo_v395.py, textos_v395.py, registrar_mapa_v395.py, harness_textos_ensaio_v395.py (ast.parse, invariantes por texto, guarda P18,
nenhuma marca pendente, e cada nome T.<x> chamado pelos derivados existe em textos_v395.py).
NAO executa nenhum script derivado: so' ast.parse, sh -n, invariantes, rotulos e a guarda de texto P18.
Como a edicao funciona: tr(t, old, new) procura sobe(old) no texto JA SUBIDO (old e' copiado do molde v394; new e' o texto FINAL, que nunca e' subido), com assert da contagem; assim cada mudanca nao mecanica fica numa troca nomeada e conferida.
O QUE MUDA em relacao ao molde (e por que): (1) o PASSO 10 (B(n) da Bancada) e' um passo SIMPLES v394 -> v395: sem --cadeia-de-selos, sem pino cadeia_de_selos e sem 3o argumento do b3_recibo (a Bancada de producao pina a v394 e o Nos e' a v394
ate' a instalacao); o kernel_recibo e' o R3_2 da v395 (nao ha modulo de auditoria); (2) o passo 1 copia tambem o delta_v395.py, que o conferidor da v395 importa; (3) os marcadores dos passos 3 e 9 sao os da v395 (psibit_v395, kh_n1_cobertura_v395);
(4) a leitura le os tres registros novos (psibit_v395, cunhagens_v395, kh_n1_cobertura_v395), confere o registro psibit_v395 por inteiro e exige que os registros da v394 e da v393 sigam selados; (5) a leitura recusa o AVISO da v395 no stdout e confere a linha
`[v395] ... registros por spec`; (6) o handoff do fechar vem de textos_v395.handoff (testavel pelo harness) e o fechar recusa um recibo do B(n) com salto; (7) o fechar arquiva tambem DERIVACAO_v395.json, HARNESS_TEXTOS_ENSAIO_v395.json e registro_mapa_v395.json.
GRAVA: DERIVACAO_v395.json (sha16 de cada molde, de cada derivado e de cada autoral; invariantes; sintaxe; marcas; rotulos; o que difere do molde). Reexecutavel: o que muda ganha .bak_<STAMP>_c1 (backup de BYTES).
Uso: python -I -B -X utf8 derivar_cadeia_v395.py"""
import ast, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)
MOLDE = os.path.join(os.path.dirname(PK), "v394", "pos_rito")
STAMP = time.strftime("%Y%m%d_%H%M%S")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
MARCA = "TEXTO_A_REESCREVER" + "_V395"           # montada por concatenacao: so' as linhas marcadas a contem por extenso
# nomes que NAO sobem de versao: registros e chaves historicos do core, arquivos e rotas de versoes passadas (so' os com 393/394 importam: o resto nao sobe de qualquer forma)
PROT = ["pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394",
        "criterio_binario_de_parada_v394", "declaration_sources_status_v394", "declaration_sources_v394", "umpy.v394.fock_tempo_e_cunhagens"]
MODELOS = ("leitura_v394.py", "superficies_v394.py", "fechar_v394.py", "chain_pos_rito_v394.sh")
AUTORAIS = ("b3_recibo_v395.py", "textos_v395.py", "registrar_mapa_v395.py", "harness_textos_ensaio_v395.py", "harness_fechar_sandbox_v395.py")
GUARDA_PENDENTE_RX = re.compile(r"(?m)^\s*#\s*" + MARCA)


def sobe(t):
    for i, p in enumerate(PROT):
        t = t.replace(p, "@@P%d@@" % i)
    t = t.replace("v394", "@@A@@").replace("v393", "v394").replace("@@A@@", "v395")
    t = t.replace("V394", "@@B@@").replace("V393", "V394").replace("@@B@@", "V395")
    t = t.replace("_sup394", "_sup395").replace("_f394", "_f395").replace("_p394", "_p395")      # rotulos de backup/temporario que nao trazem o 'v' (o molde v394 os usa com 394)
    for i, p in enumerate(PROT):
        t = t.replace("@@P%d@@" % i, p)
    return t


def rd(d, n):
    return open(os.path.join(d, n), "rb").read().decode("utf-8")


def tr(t, old, new, n=1, nome=""):
    """troca sobe(old) por `new` (texto FINAL), exigindo exatamente n ocorrencias."""
    o = sobe(old)
    assert t.count(o) == n, ("troca", nome or old[:70], t.count(o), n)
    return t.replace(o, new)


def bloco(t, ini, fim):
    """(i, j, L): do inicio da unica linha que COMECA por `ini` ate o inicio da primeira linha posterior que comeca por `fim` (exclusive)."""
    L = t.split("\n"); a = [k for k, l in enumerate(L) if l.startswith(ini)]; assert len(a) == 1, ("ancora inicial", ini, len(a))
    b = [k for k, l in enumerate(L) if k > a[0] and l.startswith(fim)]; assert b, ("ancora final", fim)
    return a[0], b[0], L


def subst_bloco(t, ini, fim, novo):
    i, j, L = bloco(t, ini, fim)
    return "\n".join(L[:i] + novo.rstrip("\n").split("\n") + L[j:])


def subst_linha(t, prefixo, novo):
    L = t.split("\n"); a = [k for k, l in enumerate(L) if l.startswith(prefixo)]; assert len(a) == 1, ("linha", prefixo, len(a))
    L[a[0]:a[0] + 1] = novo.rstrip("\n").split("\n")
    return "\n".join(L)


def grava(nome, texto):
    p = os.path.join(HERE, nome); b = texto.encode("utf-8")
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + STAMP + "_c1"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_" + STAMP
    open(tmp, "wb").write(b); assert os.path.getsize(tmp) == len(b); os.replace(tmp, p)
    assert open(p, "rb").read() == b


MOL = {n: rd(MOLDE, n) for n in MODELOS}
GUARDA_PENDENTE = '''_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V395"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v395 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")'''

# =============================================================================== leitura_v395.py
t = sobe(MOL["leitura_v394.py"])
i = t.index("import glob, hashlib, json, os, re, sys, datetime")
HEAD_L = ('# -*- coding: utf-8 -*-\n'
          '# A LEITURA da rodada v395 (molde: leitura_v394.py FINAL): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v395, que aqui e\' o proprio pacote).\n'
          '# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e\' digitado: tudo sai dos JSON, do core, do selo e do stdout do rito.\n'
          '# v395: os registros NOVOS do core sao psibit_v395 (runtime: a funcao chamada NA FRACTALIZACAO DO UM) e cunhagens_v395 e kh_n1_cobertura_v395 (por spec; ESPERADOS[registros_v395]); os da v394 (tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394,\n'
          '# cunhagens_v394, kh_n1_cobertura_v394, criterio_binario_de_parada_v394) e os da v393 seguem no core e tem de seguir selados; o modulo novo de kernel (TGLExt/Psibit.lean) vem de ESPERADOS[pedras_sha256] e e\' conferido aqui contra o arquivo do kernel do Nos.\n'
          '# A escada vem de ESPERADOS[escada_v394_e_v395] e ESPERADOS[escada]; a troca dita (so numeros) e\' a de ESPERADOS[troca_dita]. O registro psibit_v395 e\' conferido por inteiro (formal + mecanica + escada + fonte embutida + beta + inscricoes; a conjuncao\n'
          '# incondicional no kernel; a face do psion CONDICIONAL e sem habitante exibido) e a linha `[v395] ... registros por spec` do stdout do rito tem de dizer selados == registros por spec; o AVISO da v395 no stdout reprova.\n'
          '# Diferencas para a v394: os registros novos sao DESCOBERTOS por comparacao com ESPERADOS[vereditos_v394]; o conferidor e\' lido da copia em pos_rito/conferidor (a cadeia o copia antes); V[\'psibit\'], V[\'reg395\'] e V[\'patch_ids\'] sao novos.\n')
t = HEAD_L + t[i:]
t = subst_linha(t, "REG_V394 = (", '''REG_V393 = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")   # da v393: seguem no core e seguem selados (nao sao 'novos' da v395)
REG_V394 = ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394")   # da v394: seguem no core e seguem selados (nao sao 'novos' da v395)''')
t = subst_linha(t, "REG_FIXOS = (", '''REG_FIXOS = ("psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395")   # os tres registros NOVOS do core v395; + os de ESPERADOS[registros_v395] (REG_TODOS, dentro de ler)''')
t = re.sub(r"   # AJUSTAR_V395_AO_ESPERADOS[^\n]*", "", t)            # os campos de ESPERADOS_v395.json existem (gerados pelo ensaio a seco): nao ha mais palpite a marcar
t = tr(t, "    V['n_patches'] = len(CM['patches']); V['patches'] = ', '.join(p['id'] for p in CM['patches'])\n",
       "    V['n_patches'] = len(CM['patches']); V['patches'] = ', '.join(p['id'] for p in CM['patches']); V['patch_ids'] = [p['id'] for p in CM['patches']]\n", nome="patch_ids")
EXTRA_STDOUT = r'''    if [l for l in out.splitlines() if '[v395] AVISO' in l]:
        P.append('o stdout traz AVISO da v395 (o modo psionico ou os registros por spec nao rodaram): %s' % [l.strip()[:200] for l in out.splitlines() if '[v395] AVISO' in l][:2])
    m_sp = re.search(r'\[v395\] o modo psionico \(psibit, lido na fractalizacao do Um\): .*\| registros por spec: (\d+) \(selados (\d+)\)', out)
    if not m_sp or m_sp.group(1) != m_sp.group(2) or int(m_sp.group(1)) != len(ESP.get('registros_v395') or {}):
        P.append('a linha [v395] do stdout nao diz registros por spec selados == %d (%s)' % (len(ESP.get('registros_v395') or {}), m_sp.groups() if m_sp else 'ausente'))'''
OLD_V = "    if len([l for l in out.splitlines() if '[v394]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v394]')\n"
t = tr(t, OLD_V, sobe(OLD_V) + EXTRA_STDOUT + "\n", nome="aviso e linha [v395] do stdout")
PEDRAS_V395 = '''    # v395: o modulo novo de kernel vem de ESPERADOS[pedras_sha256] (o ensaio a seco do candidato) e e' conferido AQUI contra o arquivo do kernel do Nos (sha256); o numero tem de ser o de kernel_modulos_novos_v395.json
    V['pedras'] = []
    for rel_, h_ in sorted((ESP.get('pedras_sha256') or {}).items()):
        pth_ = os.path.join(NOS, 'tgl_kernel', *rel_.split('/'))
        V['pedras'].append({'modulo': 'TGLExt.' + rel_[len('TGLExt/'):-len('.lean')].replace('/', '.'), 'bandeiras': None, 'decl': None, 'ok': bool(rel_.startswith('TGLExt/') and rel_.endswith('.lean') and os.path.isfile(pth_) and sha(pth_) == h_)})
    V['n_pedras'] = len(V['pedras'])
    njp_ = os.path.join(PK, 'kernel_modulos_novos_v395.json'); nj_ = json.load(open(njp_, encoding='utf-8')) if os.path.exists(njp_) else {}
    n_esperado_ = nj_.get('novos') if isinstance(nj_.get('novos'), int) else len(nj_.get('novos') or [])
    if not V['n_pedras'] or V['n_pedras'] != n_esperado_ or any(p['ok'] is not True for p in V['pedras']):
        P.append('modulos novos do kernel: numero (%s) != kernel_modulos_novos_v395.json (%s) ou algum arquivo do Nos difere do sha256 de ESPERADOS[pedras_sha256]' % (V['n_pedras'], n_esperado_))
'''
t = subst_bloco(t, "    # v395: os modulos novos de kernel vem de ESPERADOS", "    vs = core.get('varredura_e_sorry_v392')", PEDRAS_V395)
NOVO_V395 = r'''    # --- v395: os tres registros novos conferidos contra o ensaio a seco registrado em ESPERADOS, e os da v394 e da v393, que seguem no core e tem de seguir selados; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    for k_ in REG_V393 + REG_V394:
        if (core.get(k_) or {}).get('all_verified') is not True:
            P.append('%s (registro da v394 ou da v393) deixou de selar' % k_)
    RV_ = dict(ESP.get('vereditos_novos_v395') or {}); RV_.update(ESP.get('registros_v395') or {})   # registro -> veredito do ensaio a seco (psibit_v395 e' runtime; cunhagens_v395 e kh_n1_cobertura_v395 sao por spec)
    V['reg395'] = {}
    for k_ in REG_FIXOS:
        r_ = core.get(k_) or {}
        V['reg395'][k_] = {'verdict': r_.get('verdict'), 'ok': r_.get('all_verified')}
        esp_v_ = RV_.get(k_)
        if esp_v_ is None:
            P.append('ESPERADOS_v395 nao traz o veredito do ensaio a seco de %s (vereditos_novos_v395 / registros_v395): nao ha com que conferir' % k_)
        elif r_.get('verdict') != esp_v_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k_)
    kf_ = (core.get('kernel_formalization') or {})
    rf_ = core.get('rede_fock_v394') or {}   # limite dito: o contrato conjunto da rede segue NAO habitado (a face do psion depende dele)
    if rf_.get('whole_certificate_inhabited') is not False:
        P.append('rede_fock_v394: whole_certificate_inhabited deve seguir False (o contrato conjunto da rede segue aberto) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    if kf_.get('ext_bin394_0001') is not True:
        P.append('a bandeira da pedra da v394 (ext_bin394_0001) nao segue True no kernel do rito')
    # o registro psibit_v395, conferido por inteiro (os textos leem os numeros dele)
    pb_ = core.get('psibit_v395') or {}; EP_ = ESP.get('psibit') or {}; mech_ = pb_.get('mechanics') or {}; unc_ = pb_.get('unconditional') or {}; con_ = pb_.get('conditional_psion_face') or {}
    ft_ = pb_.get('formal_theorems') or {}
    V['psibit'] = {'verdict': pb_.get('verdict'), 'ok': pb_.get('all_verified'), 'values': pb_.get('values') or {}, 'n_checks': mech_.get('n_checks'), 'mech_passed': mech_.get('passed'), 'n_teoremas': len(ft_),
                   'teoremas_true': bool(ft_) and all(x_ is True for x_ in ft_.values()), 'unconditional': unc_, 'conditional': con_, 'beta_ok': pb_.get('beta_ok'), 'beta_core_rel_diff': pb_.get('beta_core_rel_diff'),
                   'alpha_two_names_same': pb_.get('alpha_two_names_same'), 'exact_ladder': pb_.get('exact_ladder'), 'embedded_source_ok': pb_.get('embedded_source_ok'), 'runtime_executed': pb_.get('runtime_executed'),
                   'does_not_gate_core': pb_.get('does_not_gate_core'), 'inscriptions_ok': bool(pb_.get('inscriptions')) and all(x_ is True for x_ in (pb_.get('inscriptions') or {}).values())}
    falta_ = [k_ for k_ in ('beta', 'theta_M_rad', 'theta_M_deg', 'code_weight', 'code_word', 'code_verb', 'parity', 'coherence', 'coherence_neg_theta', 'collapse_diagonal', 'collapse_diag_difference', 'decode_residual', 'roundtrip_residual_max',
                            'verb_derivative_residual', 'entropy_balanced_residual', 'entropy_at_theta_M', 'ln2', 'half_identity_residual', 'reconstruction_residual', 'rho') if (pb_.get('values') or {}).get(k_) is None]
    if falta_:
        P.append('psibit_v395.values sem os campos que os textos leem: %s' % falta_)
    if not (pb_.get('all_verified') is True and mech_.get('passed') is True and mech_.get('n_checks') == EP_.get('n_checks') and V['psibit']['teoremas_true'] and V['psibit']['n_teoremas'] == (ESP.get('contrato_psibit') or {}).get('n_teoremas')
            and pb_.get('exact_ladder') is True and pb_.get('embedded_source_ok') is True and pb_.get('runtime_executed') is True and pb_.get('does_not_gate_core') is True and pb_.get('beta_ok') is True
            and pb_.get('alpha_two_names_same') is True and V['psibit']['inscriptions_ok']):
        P.append('psibit_v395 nao selou inteiro (formal + mecanica + escada + fonte embutida + beta + inscricoes): ver o registro no core')
    if not (unc_.get('in_kernel') is True and unc_.get('flag_true') is True and unc_.get('theorem') == EP_.get('teorema_incondicional') and unc_.get('flag') == EP_.get('bandeira_incondicional') and set(unc_.get('axioms') or []) <= {'propext', 'Classical.choice', 'Quot.sound'}):
        P.append('psibit_v395: a conjuncao incondicional nao esta no kernel do rito (bandeira True, trio, modulo da pedra)')
    if not (con_.get('status') == 'CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE' and con_.get('inhabitant_exhibited') is False and con_.get('flag') == EP_.get('bandeira_condicional') and con_.get('flag_true') is True):
        P.append('psibit_v395: a face do psion nao esta como CONDICIONAL sem habitante exibido')
    cu = core.get('cunhagens_v395') or {}; kh = core.get('kh_n1_cobertura_v395') or {}
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}   # o nome 'axiom_coverage_v392' e' do core (historico); segue na v395
    CB = ESP.get('cobertura_kh_n1') or {}
    V['kh'] = {'decl': cov.get('decl'), 'thm': cov.get('thm'), 'fora': cov.get('fora_do_trio'), 'nao_lidas': cov.get('nao_lidas_pelo_regex'), 'verdict': kh.get('verdict')}
    V['cunh_verdict'] = cu.get('verdict')
    if not (CB and cov.get('ok') is True and cov.get('decl') == CB.get('decl') and cov.get('thm') == CB.get('thm') and cov.get('fora_do_trio') == 0 and cov.get('nao_lidas_pelo_regex') == CB.get('nao_lidas_pelo_regex')):
        P.append('cobertura KH-N1 do rito != ESPERADOS (constantes, teoremas, fora do trio, nao lidas) ou ESPERADOS sem cobertura_kh_n1')
'''
t = subst_bloco(t, "    # --- v395: os cinco registros novos conferidos", "    qp = core.get('quantum_pillar_v384')", NOVO_V395)
assert "AJUSTAR" not in t, "sobrou marca de ajuste na leitura"
ast.parse(t); LEITURA = t

# =============================================================================== superficies_v395.py
t = sobe(MOL["superficies_v394.py"])
i = t.index("# Registro da v395 SELADA"); j = t.index("import os, re, sys, time")
CAB = ("# Registro da v395 SELADA nas superficies de memoria (molde: superficies_v394.py FINAL), pela regra da linhagem completa.\n"
       "# Diario (MEMORIA_DA_LINHAGEM, append datado), desenho (ADENDO), Atlas (append datado), TGL_CORE_MEMORY (append datado), o CLAUDE.md da Haja_Luz, as memorias-topico (missao, central, estatuto, e o topico NOVO da v395),\n"
       "# o MEMORY.md/MEMORY_2.md, e (so' sob reivindicacao nomeada em V395_AVISO_REIVINDICACAO) o AVISO_GERENCIA.md da ORDEM_019.\n"
       "# SEM erratas inline nesta versao (as erratas da v395 vao DENTRO dos blocos datados). A funcao inserir_ao_lado fica disponivel (nao e' chamada).\n"
       "# Duas fases (plano conferido ANTES da primeira escrita); backup de BYTES (.bak_<STAMP>_sup395); temporario -> conferir tamanho -> substituir; idempotente pelo marcador de cada bloco;\n"
       "# fim de linha de cada arquivo respeitado. GUARDA: so' grava se a leitura nao tiver problema E se a guarda de texto (P18, cinco regras) estiver limpa em todo texto novo.\n"
       "# Ensaio: --copias <pasta com copias dos alvos> (nada real e' tocado). MEMORY.md: ate 24.000 B e 195 linhas; se passar de 195 linhas, COMPACTA corridas de ganchos antigos (linhas que ja sao ponteiros ao\n"
       "# MEMORY_2.md) num ponteiro unico, com as linhas movidas VERBATIM ao MEMORY_2.md (regra dos dois arquivos). A linha do handoff novo entra ANTES da linha do handoff da v394 (que a custodia da v394 reescreveu).\n")
t = t[:i] + CAB + t[j:]
assert "sup394" not in t and "V394_AVISO" not in t and "V393" not in t
ast.parse(t); SUPERFICIES = t

# =============================================================================== fechar_v395.py
t = sobe(MOL["fechar_v394.py"])
t = tr(t, '    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) de narrativa da v393 marcado(s) para reescrever na v394 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")',
       '    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) marcado(s) para reescrever na v395 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")', nome="mensagem da guarda")
t = tr(t, 'if not (str(r.get("veredito") or "").startswith("REPINADA_B") and r.get("modo") == "aplicar"',
       'if not (str(r.get("veredito") or "").startswith("REPINADA_B") and "__SALTO_" not in str(r.get("veredito") or "") and r.get("salto") in (None, {}) and r.get("modo") == "aplicar"', nome="recibo do aplicar sem salto")
t = tr(t, '"insumos_codex_sha16": {f_: s16(os.path.join(PK, "insumos", f_)) for f_ in sorted(os.listdir(os.path.join(PK, "insumos"))) if f_.startswith("AO_CLAUDE") and os.path.isfile(os.path.join(PK, "insumos", f_))}, "b3": B3,',
       '"insumos_sha16": {f_: s16(os.path.join(PK, "insumos", f_)) for f_ in sorted(os.listdir(os.path.join(PK, "insumos"))) if os.path.isfile(os.path.join(PK, "insumos", f_))}, "b3": B3,', nome="insumos")
t = tr(t, "# AJUSTAR_V394_AO_ESPERADOS: o manifesto lista os encaminhamentos do Codex da v394 (insumos/AO_CLAUDE*); o molde pinava AO_CLAUDE_INTEGRAR_REGRA_V393.md\n",
       "# v395: o manifesto lista as fontes pinadas dos registros (insumos/: a pedra, as patentes, o resultado e os dois exames, a medida KH-N1); as falas ficam em insumos/cunhagens (indexadas no arquivo)\n", nome="comentario do manifesto")
t = tr(t, 'if raiz == HERE and not (f.endswith((".py", ".sh", "_out.txt", ".out", ".txt")) or f == "v394_incorporacao_manifesto.json"):',
       'if raiz == HERE and not (f.endswith((".py", ".sh", "_out.txt", ".out", ".txt")) or f in ("v395_incorporacao_manifesto.json", "DERIVACAO_v395.json", "HARNESS_TEXTOS_ENSAIO_v395.json", "registro_mapa_v395.json", "NOTAS_DERIVACAO_v395.md")):', nome="arquivo de pos_rito")
HANDOFF_NOVO = '''# o handoff da v395: o texto vive em textos_v395.handoff(V, k) (testavel pelo harness); aqui so' entram os campos dos recibos do B(n), lidos dos arquivos (nenhum numero digitado)
_k = {"ap_nome": os.path.basename(ap_.get("path", "?")), "ap_sha": str(ap_.get("sha256"))[:16], "ap_ver": ap_.get("veredito"), "ap_evento": ap_.get("evento"), "ap_bat": ap_.get("bateria"),
      "par_sha": str((B3.get("parada") or {}).get("sha256"))[:16], "rel_sha": str((B3.get("religamento") or {}).get("sha256"))[:16], "rel_man": str((B3.get("religamento") or {}).get("manifesto_sha256"))[:16]}
doc = T.handoff(V, _k)'''
t = subst_bloco(t, "# o handoff da v395 (reescrito", "vv = violacoes(doc)", HANDOFF_NOVO)
assert "AO_CLAUDE" not in t and "_dd" not in t and "AJUSTAR" not in t and "_f394" not in t and "rede_fock" not in t.replace("registros_v395", "")
ast.parse(t); FECHAR = t

# =============================================================================== chain_pos_rito_v395.sh
t = sobe(MOL["chain_pos_rito_v394.sh"])
HEADER = r'''#!/bin/sh
# v395 (21/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v394.sh FINAL (o que rodou em 19/10; derivada por derivar_cadeia_v395.py; mesma ordem de passos 0..14 e mesmos portoes). O rito ja terminou (rito_v395.sh em segundo plano;
# RITO_RC=<rc> no fim do Nos\rodada_v395_stdout.txt). A v395 e' um DELTA PEQUENO: 1 modulo novo de kernel (TGLExt/Psibit, a leitura psibit da orbita do Um pela matriz-S), o registro psibit_v395 (a funcao do runtime chamada NA FRACTALIZACAO DO UM)
# e os registros por spec cunhagens_v395 (as quatro falas de 21/10) e kh_n1_cobertura_v395; os tres contratos da v394 ganham expected_ladder novo e kh_n1_cobertura_v394 passa a piso (erratas ao lado).
# ORDEM: 0 guardas -> 1 o CONFERIDOR (copia byte a byte, com o delta_v395.py que ele importa; so leitura do Nos) -> 2 a LEITURA (PROBLEMAS param) -> 3 ENSAIO das superficies em COPIAS (o plano e' conferido antes da primeira escrita; a arvore em dry;
# o sha16 da v395 na arvore (dry) e os marcadores do passo 9 nas COPIAS, conferidos ANTES de qualquer escrita real) -> 4 patch arvore/indice (OPCIONAL: so' se existir patch_arvore_indice_v395.py) -> 5 a arvore
# -> 6 atlas+indice -> 7 superficies reais (appends datados; SEM errata nova no CLAUDE.md da raiz) -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e'
# falha visivel) e a guarda de MEMORY.md (<24.000 B, <=195 linhas) -> 10 B(n) da Bancada, ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(n) APLICAR (so com B3_AUTORIZADO=sim e o evento c1)
# -> 10c religamento (AGUARDA_OPERADOR) -> 11 fechar -> 12 registrar_mapa (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V395_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito).
# PASSO 10 SEM SALTO: a Bancada de producao pina a v394 e o Nos e' a v394 ate' a instalacao; portanto o B(n) da v395 e' um passo SIMPLES v394 -> v395 (esboco R3.5, sincronizar_bancada.py): NAO ha a opcao de cadeia de selos do esboco, nem o pino correspondente,
# e o b3_recibo_v395.py NAO tem o 3o argumento. Os pinos vem de PINOS_BN_v395.json (lidos na hora; hash nunca de memoria): criterios, esboco_R3_5, gerador_bateria, driver_t12_t14, bateria_base_R2, kernel_recibo (o KERNEL_RECIBO_v395.json,
# contrato R3_2: a v395 nao acrescenta modulo de auditoria), candidato, esperados, pins_do_candidato, recibo_pre_selo (gerado antes da instalacao; veredito JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA), selo_anterior_v394 e
# kernel_manifesto_anterior_v394 (as copias de bytes do selo e do manifesto do kernel da v394, em base_v394). A BATERIA da v395 e' GERADA por script no 10 (depois do selo; bateria por versao) e pinada ao lado (bateria_pos_selo/PINOS_BATERIA_v395.json).
# Vereditos esperados (lidos do codigo do esboco, nao rodados): ensaio REPINADA_B<n>__ENSAIO__NADA_GRAVADO_NA_BANCADA e aplicar REPINADA_B<n>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_, com n = a geracao do manifesto que a
# Bancada pina + 1 (o b3_recibo_v395.py o confere). A parada do servico (10a) e o religamento (10c) sao ato do operador (V395_AUTORIZACAO_OPERADOR nos scripts bancada_B3_servico\recibo_parada_v395.py e recibo_religamento_v395.py); o chain so' confere os recibos.
# textos_v395.py, fechar_v395.py e registrar_mapa_v395.py RECUSAM rodar se tiverem trecho marcado para reescrever: os passos 0 a 2 nao os usam. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como na v394, com os rotulos da v395.
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).'''
i, j, L = bloco(t, "#!/bin/sh", "PK=")
t = "\n".join([HEADER] + L[j:])
# (a) os marcadores dos passos 3 e 9: os do psibit e do kh_n1 da v395 (6 ocorrencias: 3 no ensaio das copias, 3 nas superficies reais)
t = tr(t, '"tempo_frequencia_v394" "kh_n1_cobertura_v394"', '"psibit_v395" "kh_n1_cobertura_v395"', n=6, nome="marcadores dos passos 3 e 9")
# (b) passo 0: o delta_v395.py (que o conferidor importa) entra na lista de ferramentas; a guarda P18 cobre os tres arquivos de narrativa
t = tr(t, '"$PK/conferir_rito_v394.py" "$PK/ESPERADOS_v394.json"', '"$PK/conferir_rito_v395.py" "$PK/delta_v395.py" "$PK/ESPERADOS_v395.json"', nome="lista de ferramentas")
t = tr(t, '$PY "$PK/guarda_p18_v394.py" "$SEL/textos_v394.py" > /dev/null || parar "a guarda de texto P18 achou violacao em textos_v394.py"',
       '$PY "$PK/guarda_p18_v395.py" "$SEL/textos_v395.py" "$SEL/fechar_v395.py" "$SEL/registrar_mapa_v395.py" > /dev/null || parar "a guarda de texto P18 achou violacao em textos_v395.py, fechar_v395.py ou registrar_mapa_v395.py"', nome="guarda P18")
# (c) passo 1: o conferidor da v395 importa o delta_v395.py: a copia byte a byte leva os dois
t = tr(t, 'cp -p "$PK/conferir_rito_v394.py" "$CONFOUT/"; cmp "$PK/conferir_rito_v394.py" "$CONFOUT/conferir_rito_v394.py" || parar "copia do conferidor difere"\n',
       'cp -p "$PK/conferir_rito_v395.py" "$CONFOUT/"; cmp "$PK/conferir_rito_v395.py" "$CONFOUT/conferir_rito_v395.py" || parar "copia do conferidor difere"\n'
       'cp -p "$PK/delta_v395.py" "$CONFOUT/"; cmp "$PK/delta_v395.py" "$CONFOUT/delta_v395.py" || parar "copia do delta_v395.py (que o conferidor importa) difere"\n', nome="passo 1")
# (d) o b3_prepara: passo SIMPLES (sem cadeia de selos); o kernel_recibo e' o R3_2 da v395
B3_CHUNK = r'''  # v395 (21/10/2026): o B(n) da v395 e' um PASSO SIMPLES v394 -> v395 (a Bancada de producao pina a v394 e o Nos passou a v395): SEM salto e SEM cadeia de selos, com o esboco R3.5. Os pinos vem de PINOS_BN_v395.json (lidos na hora;
  # hash nunca de memoria): o esboco R3.5, o recibo pre_selo (gerado antes da instalacao, sobre a Bancada que pina a v394), o recibo do kernel (KERNEL_RECIBO_v395.json, contrato R3_2, sem modulos de auditoria: a v395 nao acrescenta
  # modulo de auditoria), o selo e o manifesto do kernel da v394 (custodia, em base_v394), o driver, o gerador e a base R2 da bateria. A bateria da v395 e' GERADA aqui, por script, depois do selo (bateria por versao).
  for k in criterios esboco_R3_5 gerador_bateria driver_t12_t14 bateria_base_R2 kernel_recibo candidato esperados pins_do_candidato recibo_pre_selo selo_anterior_v394 kernel_manifesto_anterior_v394; do
    tem_pino "$k" || aguarda "o PINO $k nao esta em PINOS_BN_v395.json: o PINOS_BN da v395 nao foi gerado (ato da gerencia: diff_e_pinos_v395.py) e retomar com CHAIN_DE=$1"
    p=$(pinop "$k"); a=$(pino "$k"); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino $k diverge do arquivo (pino $a != arquivo $b)"
  done
  if tem_pino cadeia_de_selos; then parar "PINOS_BN_v395.json traz o pino cadeia_de_selos: a v395 e' um passo simples (a Bancada pina a v394), sem salto e sem cadeia de selos"; fi
  [ "$(pino candidato)" = "$(sha256f "$(cygpath -w "$NOS/um.py")")" ] || parar "o um.py do Nos nao e o candidato pinado em PINOS_BN (candidato $(pino candidato))"
  CRI=$(pino criterios); RPS=$(pino recibo_pre_selo)
  W_NOS=$(cygpath -w "$NOS"); W_ESB=$(cygpath -w "$(pinop esboco_R3_5)"); W_CRI=$(cygpath -w "$(pinop criterios)"); W_RPS=$(cygpath -w "$(pinop recibo_pre_selo)")
  W_SELO=$(cygpath -w "$(pinop selo_anterior_v394)"); W_KMAN=$(cygpath -w "$(pinop kernel_manifesto_anterior_v394)")
  # o recibo do kernel do pos_selo e' o pino kernel_recibo (o KERNEL_RECIBO_v395.json, contrato R3_2: sem modulos de auditoria)
  W_KR=$(cygpath -w "$(pinop kernel_recibo)"); KRSHA=$(sha256f "$W_KR"); [ "$KRSHA" = "$(pino kernel_recibo)" ] || parar "o recibo do kernel diverge do pino"; echo "  recibo do kernel (R3_2, sha256 LIDO NA HORA, igual ao pino): $KRSHA"
  $PY -c "import json,os,sys;sys.exit(0 if os.path.isdir(json.load(open(sys.argv[1],encoding='utf-8'))['arvore']) else 1)" "$W_KR" || aguarda "a arvore so-fontes do recibo do kernel (campo arvore) nao existe mais: refazer a arvore (refazer_arvore_v395_pos_selo.py, sem build; ato da gerencia) e retomar com CHAIN_DE=$1"'''
t = subst_bloco(t, "  # R3.5 (19/10/2026): o B(n) da v", "  # a bateria da v395: GERADA UMA vez", B3_CHUNK)
# (e) os passos 10 e 10b: sem --cadeia-de-selos; sem o 3o argumento do helper; os ecos dizem passo simples
t = tr(t, '    --cadeia-de-selos "$W_CAD" --cadeia-de-selos-sha256 "$CAD" \\\n', '', n=2, nome="--cadeia-de-selos (10 e 10b)")
t = tr(t, ' ensaio "$CAD" || parar "o recibo do B(n) ENSAIO nao confere"', ' ensaio || parar "o recibo do B(n) ENSAIO nao confere"', nome="helper do ensaio")
t = tr(t, ' aplicar "$CAD" || parar "o recibo do B(n) APLICAR nao confere"', ' aplicar || parar "o recibo do B(n) APLICAR nao confere"', nome="helper do aplicar")
t = tr(t, 'echo "== 10. B(n) da Bancada, ENSAIO pos-selo, SALTO v392 -> v394, esboco R3.5 (nada e\' gravado na Bancada; o servico pode estar no ar) $(date +%T)"',
       'echo "== 10. B(n) da Bancada, ENSAIO pos-selo, passo simples v394 -> v395 (sem salto), esboco R3.5 (nada e\' gravado na Bancada; o servico pode estar no ar) $(date +%T)"', nome="eco do 10")
t = tr(t, 'echo "== 10-bis. B(n) APLICAR, SALTO v392 -> v394, esboco R3.5 (grava o manifesto B4 na Bancada de producao: backup de bytes, rollback se falhar) $(date +%T)"',
       'echo "== 10-bis. B(n) APLICAR, passo simples v394 -> v395 (sem salto), esboco R3.5 (grava o manifesto B<n> na Bancada de producao: backup de bytes, rollback se falhar) $(date +%T)"', nome="eco do 10b")
# (f) as mensagens de AGUARDA_OPERADOR dos passos 10a e 10c dizem o que fazer na v395 (o servico esta no ar: a parada precede; os scripts ja existem; a autorizacao vem do ambiente); os portoes em si nao mudam
MSGS = [('aguarda "sem o recibo da PARADA do um_bancada.py ($RP): quiesce e parada (PID, porta 18777 fechada e hora no recibo), no molde do restart_and_deploy.ps1 / RESTART_RECEIPT_R1.json da B2 -- ato do operador autorizado na B3. Sem esse recibo a cadeia para aqui."',
         'aguarda "sem o recibo da PARADA do um_bancada.py ($RP): o servico esta no ar na porta 18777 e tem de ser PARADO pelo PID (ato do operador; nunca por nome); so\' depois se gera o recibo com bancada_B3_servico/recibo_parada_v395.py '
         '(exige V395_AUTORIZACAO_OPERADOR no ambiente; confere a porta fechada e zero processo um_bancada.py). Sem esse recibo a cadeia para aqui."'),
        ('aguarda "sem o recibo do RELIGAMENTO do um_bancada.py ($RR): religar o servico com recibo de identidade (a versao servida e v394 e o sha do manifesto e o do recibo do 10-bis) e reconectar os adaptadores MCP das sessoes (ato do operador)"',
         'aguarda "sem o recibo do RELIGAMENTO do um_bancada.py ($RR): religar o servico (ato do operador; o comando esta no campo religar do RECIBO_PARADA_v395.json) e gerar o recibo com bancada_B3_servico/recibo_religamento_v395.py '
         '(exige V395_AUTORIZACAO_OPERADOR; confere a versao servida v395, o sha do manifesto novo, o um.py e o PID); reconectar os adaptadores MCP das sessoes e ato do operador"')]
for old_, new_ in MSGS:
    t = tr(t, old_, new_, nome="mensagem de AGUARDA_OPERADOR")
for proibido in ("--cadeia-de-selos", "W_CAD", "$CAD", "SALTO v392", "R3_4", "fundir_pinos", "v392", "v393"):
    assert proibido not in t, ("resto da v394 (salto) na cadeia", proibido)
CHAIN = t

# =============================================================================== gravar e conferir
DER = {"leitura_v395.py": LEITURA, "superficies_v395.py": SUPERFICIES, "fechar_v395.py": FECHAR, "chain_pos_rito_v395.sh": CHAIN}
for n, tx in DER.items():
    grava(n, tx)
todos = {n: rd(HERE, n) for n in DER}
autorais_txt = {}
falhas = []
for n in AUTORAIS:
    p = os.path.join(HERE, n)
    if os.path.exists(p):
        autorais_txt[n] = rd(HERE, n)
    elif not n.startswith("harness_"):     # os harness sao os ultimos a nascer; os outros tres autorais tem de existir
        falhas.append((n, "autoral ausente"))
# invariantes (strings que TEM de estar em cada arquivo)
INV = {"leitura_v395.py": ["REG_V393", "REG_V394", "REG_FIXOS", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "rede_fock_v394", "kernel_modulos_novos_v395.json", "axiom_coverage_v392", "dict.fromkeys", "vereditos_v394", "escada_v394_e_v395",
                           "registros_v395", "vereditos_novos_v395", "rodada_v395_stdout.txt", "conferencia_rito_v395.json", "ESPERADOS_v395.json", "CANDIDATO_v395.json", "V['psibit']", "V['reg395']", "V['patch_ids']", "[v395] AVISO", "registros por spec",
                           "V['um_version'] != 'v395'", "a base substituida != a v394 selada"],
       "superficies_v395.py": ["_sup395", "V395_AVISO_REIVINDICACAO", "(handoff-v394-custodia.md)", "- [HANDOFF v394", "leitura_v395", "textos_v395", "guarda_p18_v395", "linhagem_v395_selada", "adendo_v395_selada", "atlas_v395_selada", "core_v395_selada",
                               "haja_luz_v395_selada", "aviso_v395_selada", "v395_selada", "v395 SELADA", "os.replace(tmp, p)", "backup de bytes falhou"],
       "fechar_v395.py": ["T.handoff(V, _k)", "_f395", "FECHAR RECUSADO:", "insumos_sha16", "DIFF_v394_v395.diff", "DIFF_KERNEL_v395.txt", "RECIBO_SINCRONIZACAO_v395_", "RECIBO_PARADA_v395.json", "RECIBO_RELIGAMENTO_v395.json", "__SALTO_", "registros_v395",
                          "base_v394", "HANDOFF_v395_CUSTODIA.md", "handoff-v395-custodia.md", "_MARCA_PENDENTE", "guarda_p18_v395", "v395_selo", "v395_kernel", "HARNESS_TEXTOS_ENSAIO_v395.json"],
       "chain_pos_rito_v395.sh": ["V395_AVISO_REIVINDICACAO", "topico_novo()", "textos_v395", "arvore_dry.md", "_p395", "_sup395", "selo_anterior_v394", "kernel_manifesto_anterior_v394", "/c/IALD/Central de Patentes/work/cadeia_de_selo/v395", "B3_AUTORIZADO\" = \"sim\"",
                                  "exit 20", "RECIBO_PARADA_v395.json", "RECIBO_RELIGAMENTO_v395.json", "--versao v395 --fase pos_selo", "b3_recibo_v395.py", "delta_v395.py", "psibit_v395", "kh_n1_cobertura_v395", "PINOS_BN_v395.json", "PINOS_BATERIA_v395.json",
                                  "recibo_pre_selo", "esboco_R3_5", "kernel_recibo", "bateria_pos_selo", "tem_pino cadeia_de_selos", "--recibo-pre-selo-sha256 \"$RPS\"", "--selo-anterior \"$W_SELO\"", "--kernel-manifesto-anterior \"$W_KMAN\"",
                                  "--kernel-recibo \"$W_KR\" --kernel-recibo-sha256 \"$KRSHA\"", "gerar_bateria_r3_4.py", "ORDEM=\"0 1 2 3 4 5 6 7 8 9 10 10a 10b 10c 11 12 13 14\"", "CHAIN_DE", "CHAIN_ATE", "parar()", "aguarda()"]}
INV_AUTORAIS = {"b3_recibo_v395.py": ["REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA", "REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO", "versao_alvo", "\"v395\"", "PINOS_BN_v395.json", "__SALTO_", "BATERIA_PASSA", "manifesto_anterior", "pinos_da_versao"],
                "textos_v395.py": ["_MARCA_PENDENTE", "TOPICO_NOVO", "def handoff(", "def linhagem(", "def desenho(", "def atlas(", "def core_memory(", "def haja_luz(", "def aviso(", "def aviso_pulado(", "def topico_missao(", "def topico_central(", "def topico_estatuto(", "def topico_novo(",
                                   "def linha_handoff(", "def marca_missao(", "def id_missao(", "def id_central(", "def _d(", "def _num(", "_cita(", "_kernel_tem(", "_um_tem(", "def _limites(", "def _erratas(", "def _legal(", "def _achado_alfa(",
                                   "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"],
                "registrar_mapa_v395.py": ["_MARCA_PENDENTE", "def montar(", "umpy.v395.psibit_na_fractalizacao_do_um", "kernel.psibit_v395_candidata_21out", "assert selo.get(\"um_version\") == \"v395\"", "NAO escreve", "registro_mapa_v395.json"],
                "harness_textos_ensaio_v395.py": ["harness_saida_v395", "dry_v395", "guarda_p18_v395"], "harness_fechar_sandbox_v395.py": ["fechar_sandbox", "FECHAR RECUSADO", "registrar_mapa_v395.py", "SINTETICO"]}
conf = {}
for n, lst in INV.items():
    conf[n] = {}
    for x in lst:
        ok = x in todos[n]; conf[n][x[:90]] = ok
        if not ok:
            falhas.append((n, x[:90]))
for n, lst in INV_AUTORAIS.items():
    if n not in autorais_txt:
        continue
    conf[n] = {}
    for x in lst:
        ok = x in autorais_txt[n]; conf[n][x[:90]] = ok
        if not ok:
            falhas.append((n, x[:90]))
# sintaxe
sint = {}
for n, tx in list(todos.items()) + list(autorais_txt.items()):
    if n.endswith(".py"):
        try:
            ast.parse(tx); sint[n] = "ast.parse ok"
        except SyntaxError as e:
            sint[n] = "ast.parse FALHOU: %r" % (e,); falhas.append((n, "ast.parse"))
    else:
        r = subprocess.run(["sh", "-n", os.path.join(HERE, n)], capture_output=True, text=True); sint[n] = "sh -n rc=%d %s" % (r.returncode, r.stderr[:200])
        if r.returncode:
            falhas.append((n, "sh -n"))
    if "\r" in tx:
        falhas.append((n, "CR no arquivo"))
# os portoes do B(n): os blocos 10a e 10c sao IDENTICOS ao molde subido de versao; no 10b, as linhas de portao (aguarda/B3_AUTORIZADO/EVENTO/RECIBO_PARADA) sao as do molde
molde_b = sobe(MOL["chain_pos_rito_v394.sh"])
for old_, new_ in MSGS:
    molde_b = molde_b.replace(sobe(old_), new_)      # o molde subido, com as MESMAS mensagens dos passos 10a e 10c: o resto dos portoes tem de ser identico
for ini, fim in (("if quer 10a; then", "if quer 10b; then"), ("if quer 10c; then", "if quer 11; then")):
    ia, ja, La = bloco(molde_b, ini, fim); ib, jb, Lb = bloco(CHAIN, ini, fim)
    if La[ia:ja] != Lb[ib:jb]:
        falhas.append(("portao do B(n) difere do molde subido de versao", ini))
    else:
        conf.setdefault("chain_pos_rito_v395.sh", {})["trecho identico ao molde (sobe): " + ini] = True
ia, ja, La = bloco(molde_b, "if quer 10b; then", "if quer 10c; then"); ib, jb, Lb = bloco(CHAIN, "if quer 10b; then", "if quer 10c; then")
gate = lambda L_: [l for l in L_ if any(k in l for k in ('aguarda "', "B3_AUTORIZADO", "[ -n \"$EVENTO\"", "RECIBO_PARADA", "EVENTO_HASH", "--evento", "--modo aplicar", "--fase pos_selo"))]
if gate(La[ia:ja]) != gate(Lb[ib:jb]):
    falhas.append(("as linhas de portao do 10b diferem do molde subido de versao", [x for x in gate(Lb[ib:jb]) if x not in gate(La[ia:ja])][:2]))
else:
    conf.setdefault("chain_pos_rito_v395.sh", {})["linhas de portao do 10b identicas ao molde (sobe)"] = True
# o passo 3 a 9, 11 a 14 do chain: identicos ao molde subido (so' as trocas dos marcadores, do delta_v395 e da guarda P18)
for ini, fim in (("if quer 4; then", "if quer 10; then"), ("if quer 12; then", 'echo "== FIM')):
    ia, ja, La = bloco(molde_b, ini, fim); ib, jb, Lb = bloco(CHAIN, ini, fim)
    esp_ = [l.replace('"tempo_frequencia_v394" "kh_n1_cobertura_v394"', '"psibit_v395" "kh_n1_cobertura_v395"') for l in La[ia:ja]]
    if esp_ != Lb[ib:jb]:
        falhas.append(("os passos do chain diferem do molde subido alem das trocas ditas", ini))
    else:
        conf.setdefault("chain_pos_rito_v395.sh", {})["passos identicos ao molde (sobe + marcadores): " + ini] = True
# marcas pendentes: nenhuma em nenhum arquivo (nem derivado, nem autoral)
marcas = {n: len(GUARDA_PENDENTE_RX.findall(tx)) for n, tx in list(todos.items()) + list(autorais_txt.items()) if GUARDA_PENDENTE_RX.search(tx)}
if marcas:
    falhas.append(("marca de texto pendente", marcas))
for n in ("fechar_v395.py", "textos_v395.py", "registrar_mapa_v395.py"):
    tx = todos.get(n) or autorais_txt.get(n) or ""
    if n in (todos.keys() | autorais_txt.keys()) and "_MARCA_PENDENTE" not in tx:
        falhas.append((n, "sem a guarda de pendencia (_MARCA_PENDENTE)"))
# rotulos de versao: nenhum resto de 390-394 onde o sentido e' 'esta versao'. O que fica com 394/393 e' so' a versao ANTERIOR ou nome historico (lista conferida)
OK_HIST = ("_V394_", "fechar_v390", "C13_kh_n1_v394", "ponto_fixo_v394_d19", "pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394",
           "criterio_binario_de_parada_v394", "declaration_sources", "umpy.v394", "REG_V393", "REG_V394", "base_v394", "selo_anterior_v394", "kernel_manifesto_anterior_v394", "handoff-v394-custodia", "vereditos_v394", "escada_v394_e_v395",
           "DIFF_v394_v395", "leitura_v394.py", "superficies_v394.py", "fechar_v394.py", "chain_pos_rito_v394.sh", "textos_v394.py", "registrar_mapa_v394.py", "b3_recibo_v394.py", "derivar_cadeia_v394.py", "ext_bin394", "ESPERADOS_v394",
           "PINOS_BN_v394", "rito_v394", "cadeia_de_selo/v394", "cadeia_de_selo\\v394", "axiom_coverage_v392", "KH_N1_v392", "varredura_e_sorry_v392", "estatuto_da_prova_v391", "fundacao_v390", "three_stress_tests_v387", "pedras_v392", "kh_n1_cobertura_v392")
resid = {}
for n, tx in list(todos.items()) + list(autorais_txt.items()):
    if n.startswith("harness_"):
        continue       # o harness traz de proposito rotulos de versoes anteriores (controles negativos: selo de outra versao, recibo de v394, bancada que pinava a v392); os outros arquivos nao
    for m in re.finditer(r"[A-Za-z0-9_\-\.\[\]/\\]*(?<![0-9a-f])39[0-4][A-Za-z0-9_\-\.\[\]]*", tx):
        tok = m.group(0).rstrip(".")
        if re.fullmatch(r"[0-9a-f]*39[0-4][0-9a-f]*", tok) and len(tok) >= 8:
            continue   # hash hexadecimal
        resid.setdefault(tok, set()).add(n)
estranhos = {}
for tok, ns in resid.items():
    if any(p in tok for p in OK_HIST) or tok in ("v394", "v393", "v392", "v391", "v390", "V394", "V393", "394", "393"):
        continue
    estranhos[tok] = sorted(ns); falhas.append(("rotulo estranho com 390-394", tok, sorted(ns)))
# a guarda de texto (P18) sobre todo arquivo de narrativa e de cadeia
sys.path.insert(0, PK)
from guarda_p18_v395 import violacoes
gv = {n: violacoes(tx) for n, tx in list(todos.items()) + list(autorais_txt.items())}
if any(gv.values()):
    falhas.append(("guarda P18", {k: v[:3] for k, v in gv.items() if v}))
# cada T.<nome> chamado pelos derivados e pelo registrar existe em textos_v395.py
ttxt = autorais_txt.get("textos_v395.py", "")
chamados = sorted({m for n in ("superficies_v395.py", "fechar_v395.py") for m in re.findall(r"\bT\.([A-Za-z_][A-Za-z_0-9]*)", todos[n])} | {m for m in re.findall(r"\bT\.([A-Za-z_][A-Za-z_0-9]*)", autorais_txt.get("registrar_mapa_v395.py", ""))})
faltam = [c for c in chamados if not re.search(r"(?m)^(def %s\(|%s = )" % (re.escape(c), re.escape(c)), ttxt)]
if ttxt and faltam:
    falhas.append(("textos_v395.py nao define o que os derivados chamam", faltam))
# o que os derivados leem de ESPERADOS/CANDIDATO/PINOS (campos), conferido contra os arquivos desta cadeia
RX = {"ESPERADOS": re.compile(r"ESP(?:ERADOS)?\[['\"]([^'\"]+)['\"]\]|ESP\.get\(['\"]([^'\"]+)['\"]"), "CANDIDATO": re.compile(r"CM\[['\"]([^'\"]+)['\"]\]|CM\.get\(['\"]([^'\"]+)['\"]")}
alltxt = dict(todos); alltxt.update(autorais_txt)
campos = {"ESPERADOS": sorted({a or b for tx in alltxt.values() for a, b in RX["ESPERADOS"].findall(tx)}), "CANDIDATO": sorted({a or b for tx in alltxt.values() for a, b in RX["CANDIDATO"].findall(tx)})}
presentes = {}
for rotulo, arq in (("ESPERADOS", "ESPERADOS_v395.json"), ("CANDIDATO", "CANDIDATO_v395.json"), ("PINOS_BN", "PINOS_BN_v395.json")):
    p = os.path.join(PK, arq)
    if os.path.exists(p):
        d = json.load(open(p, encoding="utf-8"))
        lido = campos.get(rotulo) or ["criterios", "esboco_R3_5", "gerador_bateria", "driver_t12_t14", "bateria_base_R2", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "recibo_pre_selo", "selo_anterior_v394", "kernel_manifesto_anterior_v394"]
        presentes[rotulo] = {"arquivo_sha16": sha16(open(p, "rb").read()), "faltam": [c for c in lido if c not in d]}
        if presentes[rotulo]["faltam"]:
            falhas.append(("campo de %s lido pelos derivados e ausente do arquivo" % rotulo, presentes[rotulo]["faltam"]))
    else:
        presentes[rotulo] = {"arquivo": "ausente"}; falhas.append((arq, "ausente"))
DERJ = {"molde": {n: sha16(MOL[n].encode("utf-8")) for n in MOL}, "molde_derivar_cadeia_v394": sha16(open(os.path.join(MOLDE, "derivar_cadeia_v394.py"), "rb").read()),
        "derivados": {n: sha16(todos[n].encode("utf-8")) for n in todos}, "autorais": {n: sha16(autorais_txt[n].encode("utf-8")) for n in autorais_txt},
        "sobe": "v394 -> v395, v393 -> v394 (anterior), V394 -> V395, V393 -> V394; PROT (nao sobem): " + ", ".join(PROT),
        "o_que_difere_do_molde": {"chain": "passo 10 sem salto (sem --cadeia-de-selos, sem pino de cadeia de selos, sem o 3o argumento do b3_recibo); kernel_recibo R3_2; passo 1 copia o delta_v395.py; guarda P18 cobre textos, fechar e registrar_mapa; marcadores dos passos 3 e 9 = psibit_v395 e kh_n1_cobertura_v395; cabecalho escrito para a v395",
                                 "leitura": "tres registros novos (psibit_v395, cunhagens_v395, kh_n1_cobertura_v395); psibit_v395 conferido por inteiro; registros da v394 e da v393 seguem selados; AVISO da v395 no stdout reprova; V['psibit'], V['reg395'], V['patch_ids']; sem V['cons'] e V['cora'] (eram informativos da v393)",
                                 "superficies": "so' os rotulos (a ancora do handoff e' a linha do handoff da v394, que a custodia da v394 reescreveu; a v395 entra antes dela)",
                                 "fechar": "handoff vem de textos_v395.handoff; recibo do B(n) sem salto; insumos_sha16 (em vez dos encaminhamentos do Codex); arquiva DERIVACAO_v395.json, HARNESS_TEXTOS_ENSAIO_v395.json e registro_mapa_v395.json",
                                 "b3_recibo": "AUTORAL (a logica muda: sem salto; B<n> = geracao do manifesto anterior + 1; veredito exato; pino do recibo pre_selo conferido; manifesto anterior igual ao do pre_selo)",
                                 "textos, registrar_mapa": "AUTORAIS (escritos para o delta da v395; nenhuma marca pendente)", "harness": "AUTORAIS (harness_textos_ensaio_v395.py: porte de delta_19out/harness_textos_ensaio.py da v394, ampliado; harness_fechar_sandbox_v395.py: o fechar e o main do registrar_mapa num sandbox isolado, com recibos do B(n) SINTETICOS)"},
        "marcas_texto_a_reescrever": {"por_arquivo": marcas, "total": sum(marcas.values())}, "campos_lidos_dos_arquivos_da_v395": campos, "arquivos_da_v395_no_pacote": presentes,
        "invariantes": conf, "sintaxe": sint, "guarda_p18": {k: ("LIMPO" if not v else v[:3]) for k, v in gv.items()}, "rotulos_estranhos": estranhos, "textos_definem_o_que_os_derivados_chamam": {"chamados": chamados, "faltam": faltam}, "falhas": falhas,
        "nao_validado": "nenhum derivado foi EXECUTADO contra o Nos real nem revisto por cetico independente; so' ast.parse, sh -n, invariantes, rotulos, guarda P18 e os harness (textos, leitura, superficies em COPIAS, b3_recibo, fechar e registrar_mapa em SANDBOX, tudo com recibos SINTETICOS e Nos EMULADO)"}
grava("DERIVACAO_v395.json", json.dumps(DERJ, ensure_ascii=False, indent=1))
print("DERIVADOS:", ", ".join("%s %s" % (n, DERJ["derivados"][n]) for n in DERJ["derivados"]))
print("AUTORAIS:", ", ".join("%s %s" % (n, DERJ["autorais"][n]) for n in DERJ["autorais"]))
print("SINTAXE:", json.dumps(sint, ensure_ascii=False))
print("MARCAS texto:", json.dumps(marcas, ensure_ascii=False))
print("INVARIANTES:", sum(len(v) for v in conf.values()), "conferidos;", "FALHAS:", falhas if falhas else "nenhuma")
sys.exit(1 if falhas else 0)
