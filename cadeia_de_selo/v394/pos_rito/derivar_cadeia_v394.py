# -*- coding: utf-8 -*-
"""derivar_cadeia_v394.py -- DERIVA a cadeia pos-rito da v394 a partir do molde REAL da v393 (cadeia_de_selo/v393/pos_rito) (molde do derivar: derivar_cadeia_v393.py).
GERA (subida de versao v393 -> v394, v392 -> v393 (anterior), V393 -> V394, V392 -> V393, k393 -> k394, e edicoes com assert de contagem): leitura_v394.py, superficies_v394.py, fechar_v394.py, b3_recibo_v394.py,
chain_pos_rito_v394.sh, textos_v394.py, registrar_mapa_v394.py. NAO executa nenhum script derivado: so' ast.parse, sh -n, invariantes e a guarda de texto P18.
A SUBIDA E' MECANICA. Os nomes de registros historicos do core NAO sobem (lista PROT). As NARRATIVAS da v393 (textos_v394.py, o handoff de fechar_v394.py, as anotacoes e a rota de registrar_mapa_v394.py) saem
com a subida mecanica e com a linha de comentario marcada para reescrever (a marca esta' em MARCA, montada por concatenacao); enquanto houver marca no arquivo, ele RECUSA rodar (SystemExit): a cadeia nao grava
narrativa da v393 como se fosse da v394. Onde o derivado le um campo de ESPERADOS/CANDIDATO/PINOS cujo nome e' PALPITE (ESPERADOS_v394.json ainda nao existe), a linha leva a marca de ajuste (MARCA_AJ).
Melhorias sobre o molde (todas mantem os portoes: AGUARDA_OPERADOR/B3_AUTORIZADO exatamente como no molde): (1) rotulos de backup e variaveis de ambiente corretos para a v394 (_sup394, _f394, _p394,
V394_AVISO_REIVINDICACAO; no molde eram _sup392, _f392 e V392_ no codigo); (2) o passo 3 (ensaio) passa a conferir, ANTES de qualquer escrita real, que a arvore (dry) traz o sha16 da v394 e que as COPIAS das
superficies trazem os marcadores do passo 9 (risco 1 do ESTADO_V393 s.7: o passo 9 exigia o sha16 em A_PROVA_DA_QG_TGL_arvore.md e TGL_INDICE_VIVO.md depois de os passos 5-8 ja terem gravado); (3) o nome do
topico novo e' LIDO de textos_v394.TOPICO_NOVO (uma fonte so'); (4) a leitura da v394 le os cinco registros novos (tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394, cunhagens_v394, kh_n1_cobertura_v394)
e exige que os da v393 sigam selados.
GRAVA: DERIVACAO_v394.json (sha16 de cada molde e de cada derivado, invariantes, sintaxe, marcas, campos lidos, descartados). Reexecutavel: o que muda ganha .bak_<STAMP>_c1 (backup de BYTES).
Uso: python -I -B -X utf8 derivar_cadeia_v394.py"""
import ast, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)
MOLDE = os.path.join(os.path.dirname(PK), "v393", "pos_rito")
STAMP = time.strftime("%Y%m%d_%H%M%S")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
MARCA = "TEXTO_A_REESCREVER" + "_V394"          # montada por concatenacao: so' as linhas marcadas a contem por extenso
MARCA_AJ = "AJUSTAR_V394_AO_ESPERADOS"
# nomes que NAO sobem de versao: registros e chaves historicos do core, arquivos e rotas de versoes passadas
PROT = ["varredura_e_sorry_v392", "estatuto_da_prova_v391", "fundacao_v390", "three_stress_tests_v387", "pedras_v392", "pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393",
        "cunhagens_regra_v393", "kh_n1_cobertura_v393", "kh_n1_cobertura_v392", "axiom_coverage_v392", "KH_N1_v392", "AO_CLAUDE_INTEGRAR_REGRA_V393", "umpy.v392.pedras_e_barreiras", "formal.regra.integracao_v393"]
MODELOS = ("leitura_v393.py", "superficies_v393.py", "fechar_v393.py", "b3_recibo_v393.py", "chain_pos_rito_v393.sh", "textos_v393.py", "registrar_mapa_v393.py")


def bump(t):
    for i, p in enumerate(PROT):
        t = t.replace(p, "@@P%d@@" % i)
    t = t.replace("v393", "@@N@@").replace("v392", "v393").replace("@@N@@", "v394")
    t = t.replace("V393", "@@U@@").replace("V392", "V393").replace("@@U@@", "V394")
    t = t.replace("k393", "k394")
    for i, p in enumerate(PROT):
        t = t.replace("@@P%d@@" % i, p)
    return t


def rd(d, n):
    return open(os.path.join(d, n), "rb").read().decode("utf-8")


def troca(t, old, new, n=1, nome=""):
    assert t.count(old) == n, ("troca", nome or old[:70], t.count(old), n)
    return t.replace(old, new)


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


def antes_de(t, prefixo, texto, n=1):
    """insere `texto` (uma ou mais linhas) imediatamente ANTES da(s) linha(s) que comecam por `prefixo`"""
    L = t.split("\n"); a = [k for k, l in enumerate(L) if l.startswith(prefixo)]; assert len(a) == n, ("ancora", prefixo, len(a), n)
    for k in reversed(a):
        L[k:k] = texto.rstrip("\n").split("\n")
    return "\n".join(L)


def apos(t, prefixo, texto):
    L = t.split("\n"); a = [k for k, l in enumerate(L) if l.startswith(prefixo)]; assert len(a) == 1, ("ancora apos", prefixo, len(a))
    L[a[0] + 1:a[0] + 1] = texto.rstrip("\n").split("\n")
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
GUARDA_PENDENTE = '''_MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V394"
if ("# " + _MARCA_PENDENTE) in open(os.path.abspath(__file__), encoding="utf-8").read():
    raise SystemExit("RECUSO: " + os.path.basename(__file__) + " ainda tem trecho(s) de narrativa da v393 marcado(s) para reescrever na v394 (linha de comentario com a marca " + _MARCA_PENDENTE + "): a gerencia os reescreve e tira as marcas antes de a cadeia usar este arquivo")'''
M = "# " + MARCA


def marca_antes(t, prefixos, n=1):
    for p in prefixos:
        t = antes_de(t, p, M, n=n)
    return t


# =============================================================================== leitura_v394.py
t = bump(MOL["leitura_v393.py"])
i = t.index("import glob, hashlib, json, os, re, sys, datetime")
HEAD_L = ('# -*- coding: utf-8 -*-\n'
          '# A LEITURA da rodada v394 (molde: leitura_v393.py): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v394, que aqui e\' o proprio pacote).\n'
          '# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e\' digitado: tudo sai dos JSON, do core, do selo e do stdout do rito.\n'
          '# v394: os registros NOVOS do core sao tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394 (runtime) e cunhagens_v394, kh_n1_cobertura_v394 (por spec; ESPERADOS[registros_v394]); os da v393\n'
          '# (pedras_v393, regra_consumidor_v393, coracao_e_selo_gravitacional_v393, cunhagens_regra_v393, kh_n1_cobertura_v393) seguem no core e tem de seguir selados; os 189 modulos novos de kernel vem de\n'
          '# ESPERADOS[pedras_sha256] e sao conferidos aqui, um a um, contra o arquivo do kernel do Nos. A escada vem de ESPERADOS[escada_v393_e_v394] e ESPERADOS[escada]; a troca dita (so numeros) e\' a de ESPERADOS[troca_dita].\n'
          '# Os nomes de campo de ESPERADOS lidos aqui sao os do molde subidos de versao; onde o campo e\' PALPITE a linha leva a marca ' + MARCA_AJ + ' (ESPERADOS_v394.json e\' gerado por outro processo).\n'
          '# Diferencas para a v393: o pacote e\' a pasta V; os registros novos sao DESCOBERTOS por comparacao com ESPERADOS[vereditos_v393]; o conferidor e\' lido da copia em pos_rito/conferidor (a cadeia o copia antes).\n')
t = HEAD_L + t[i:]
t = subst_linha(t, "REG_FIXOS = (", '''REG_V393 = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")   # da v393: seguem no core e seguem selados (nao sao 'novos' da v394)
REG_FIXOS = ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394")   # os cinco registros NOVOS do core v394; + os de ESPERADOS[registros_v394] (REG_TODOS, dentro de ler)''')
t = troca(t, "    REG_TODOS = tuple(REG_FIXOS) + tuple(ESP['registros_v394'])\n", "    REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v394') or ())))   # " + MARCA_AJ + ": campo registros_v394 (como registros_v393)\n", nome="REG_TODOS")
t = troca(t, "V['escada_antes'] = ESP['escada_v393_e_v394'][0]; V['escada_depois'] = ESP['escada'][1]", "V['escada_antes'] = ESP['escada_v393_e_v394'][0]; V['escada_depois'] = ESP['escada'][1]   # " + MARCA_AJ + ": campo escada_v393_e_v394", nome="escada")
t = troca(t, "for k, v in ESP['cunhagens'].items()}", "for k, v in (ESP.get('cunhagens') or {}).items()}   # " + MARCA_AJ + ": campo cunhagens (sha256 das cunhagens do operador embutidas)", nome="verbatins")
PEDRAS_V394 = '''    # v394: os modulos novos de kernel vem de ESPERADOS[pedras_sha256] (o ensaio a seco do candidato) e cada um e' conferido AQUI contra o arquivo do kernel do Nos (sha256); o numero tem de ser o de kernel_modulos_novos_v394.json
    pv = core.get('pedras_v394') or {}   # ''' + MARCA_AJ + ''': se a v394 tiver um registro de pedras proprio (nao esta entre os cinco), ele e' lido aqui; sem ele n_flags/n_decl ficam None
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
'''
t = subst_bloco(t, "    pv = core.get('pedras_v393')", "    vs = core.get('varredura_e_sorry_v392')", PEDRAS_V394)
NOVO_V394 = '''    # --- v394: os cinco registros novos conferidos contra o ensaio a seco registrado em ESPERADOS, e os da v393 (a regra e o coracao), que seguem no core e tem de seguir selados; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    for k_ in REG_V393:
        if (core.get(k_) or {}).get('all_verified') is not True:
            P.append('%s (registro da v393) deixou de selar' % k_)
    RV_ = dict(ESP.get('vereditos_novos_v394') or {}); RV_.update(ESP.get('registros_v394') or {})   # ''' + MARCA_AJ + ''': campos registros_v394 (por spec) e/ou vereditos_novos_v394 (runtime): registro -> veredito do ensaio a seco
    V['reg394'] = {}
    for k_ in REG_FIXOS:
        r_ = core.get(k_) or {}
        V['reg394'][k_] = {'verdict': r_.get('verdict'), 'ok': r_.get('all_verified')}
        esp_v_ = RV_.get(k_) or ESP.get('veredito_' + k_ + '_do_ensaio')
        if esp_v_ is None:
            P.append('ESPERADOS_v394 nao traz o veredito do ensaio a seco de %s (registros_v394 / vereditos_novos_v394 / veredito_%s_do_ensaio): nao ha com que conferir' % (k_, k_))
        elif r_.get('verdict') != esp_v_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k_)
    rf_ = core.get('rede_fock_v394') or {}   # limite dito: o contrato conjunto da rede NAO foi habitado (nenhum certificado inteiro); ''' + MARCA_AJ + ''': campo whole_certificate_inhabited do registro
    if rf_.get('whole_certificate_inhabited') is not False:
        P.append('rede_fock_v394: whole_certificate_inhabited deve ser False (a rede inteira nao foi habitada) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    rc = core.get('regra_consumidor_v393') or {}; co = core.get('coracao_e_selo_gravitacional_v393') or {}; cu = core.get('cunhagens_v394') or {}; kh = core.get('kh_n1_cobertura_v394') or {}
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}   # o nome 'axiom_coverage_v392' e' do core (historico); segue na v394
    CB = ESP.get('cobertura_kh_n1') or {}   # ''' + MARCA_AJ + ''': campo cobertura_kh_n1
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
'''
t = subst_bloco(t, "    # --- v394: a regra e o coracao", "    qp = core.get('quantum_pillar_v384')", NOVO_V394)
ast.parse(t); LEITURA = t

# =============================================================================== superficies_v394.py
t = bump(MOL["superficies_v393.py"])
i = t.index("# Registro da v394 SELADA"); j = t.index("import os, re, sys, time")
CAB = ("# Registro da v394 SELADA nas superficies de memoria (molde: superficies_v393.py), pela regra da linhagem completa.\n"
       "# Diario (MEMORIA_DA_LINHAGEM, append datado), desenho (ADENDO), Atlas (append datado), TGL_CORE_MEMORY (append datado), o CLAUDE.md da Haja_Luz, as memorias-topico (missao, central, estatuto, e o topico NOVO da v394),\n"
       "# o MEMORY.md/MEMORY_2.md, e (so' sob reivindicacao nomeada em V394_AVISO_REIVINDICACAO) o AVISO_GERENCIA.md da ORDEM_019.\n"
       "# SEM erratas inline nesta versao (erratas novas, se houver, vao DENTRO do bloco datado). A funcao inserir_ao_lado fica disponivel (nao e' chamada).\n"
       "# Duas fases (plano conferido ANTES da primeira escrita); backup de BYTES (.bak_<STAMP>_sup394); temporario -> conferir tamanho -> substituir; idempotente pelo marcador de cada bloco;\n"
       "# fim de linha de cada arquivo respeitado. GUARDA: so' grava se a leitura nao tiver problema E se a guarda de texto (P18, cinco regras) estiver limpa em todo texto novo.\n"
       "# Ensaio: --copias <pasta com copias dos alvos> (nada real e' tocado). MEMORY.md: ate 24.000 B e 195 linhas; se passar de 195 linhas, COMPACTA corridas de ganchos antigos (linhas que ja sao ponteiros ao\n"
       "# MEMORY_2.md) num ponteiro unico, com as linhas movidas VERBATIM ao MEMORY_2.md (regra dos dois arquivos).\n"
       "# Rotulos desta versao (no molde v393 ficaram uma versao atras no codigo): MARCA_BAK = _sup394 e a variavel de ambiente V394_AVISO_REIVINDICACAO (a mesma que a cadeia usa).\n")
t = t[:i] + CAB + t[j:]
t = troca(t, "MARCA_BAK = '_sup392'", "MARCA_BAK = '_sup394'", nome="MARCA_BAK")
t = troca(t, "os.environ.get('V393_AVISO_REIVINDICACAO', '')", "os.environ.get('V394_AVISO_REIVINDICACAO', '')", nome="env aviso (rotulo atrasado no molde)")
t = subst_linha(t, "# ---- 1. (sem erratas inline", "# ---- 1. (sem erratas inline nesta versao: erratas novas, se houver, vao dentro do bloco datado da linhagem, do Atlas, do core e do topico novo)")
assert "sup393" not in t and "sup392" not in t and "V392" not in t and "V393_AVISO" not in t
ast.parse(t); SUPERFICIES = t

# =============================================================================== textos_v394.py
t = bump(MOL["textos_v393.py"])
t = troca(t, "import hashlib, json, os, re\n", "import hashlib, json, os, re\n" + GUARDA_PENDENTE + "\n", nome="import textos")
t = subst_linha(t, "# NAO ha erratas novas sobre o CLAUDE.md da raiz", M + " (cabecalho): dizer aqui se a v394 traz erratas novas (a unica errata da v393 era a do registro kh_n1_cobertura_v392, dita dentro do proprio bloco)")
t = marca_antes(t, ["TOPICO_NOVO = ", "FRASE_FIGURA = ", "def _frase_do_operador", "def _num(", "def _kh_errata(", "def linhagem(", "def desenho(", "def atlas(", "def core_memory(", "def haja_luz(",
                    "def topico_missao(", "def topico_central(", "def topico_estatuto(", "def marca_missao(", "def linha_handoff(", "def topico_novo(", "def aviso(", "def arvore_linha(",
                    "def titulo_verbete(", "def verbete(", "def remissivo("])
ast.parse(t); TEXTOS = t

# =============================================================================== fechar_v394.py
t = bump(MOL["fechar_v393.py"])
t = troca(t, "_f392", "_f394", n=3, nome="rotulos _f392 (atrasados no molde)")
t = troca(t, "from guarda_p18_v394 import violacoes\n", "from guarda_p18_v394 import violacoes\n" + GUARDA_PENDENTE + "\n", nome="guarda pendente")
t = troca(t, '"insumo_codex_regra_sha16": s16(os.path.join(PK, "insumos", "AO_CLAUDE_INTEGRAR_REGRA_V393.md")), "b3": B3,',
          '"insumos_codex_sha16": {f_: s16(os.path.join(PK, "insumos", f_)) for f_ in sorted(os.listdir(os.path.join(PK, "insumos"))) if f_.startswith("AO_CLAUDE") and os.path.isfile(os.path.join(PK, "insumos", f_))}, "b3": B3,', nome="insumo codex")
t = antes_de(t, "m = {\"stamp\": ST,", "# " + MARCA_AJ + ": o manifesto lista os encaminhamentos do Codex da v394 (insumos/AO_CLAUDE*); o molde pinava AO_CLAUDE_INTEGRAR_REGRA_V393.md")
t = antes_de(t, "doc = (", M + " (o handoff inteiro e' narrativa da v393: a regra e o coracao, a errata do kh_n1_cobertura_v392, as tres pedras, a camada v393 dos 16 dispositivos)")
assert "_f392" not in t
ast.parse(t); FECHAR = t

# =============================================================================== registrar_mapa_v394.py
t = bump(MOL["registrar_mapa_v393.py"])
t = troca(t, "from guarda_p18_v394 import violacoes\n", "from guarda_p18_v394 import violacoes\n" + GUARDA_PENDENTE + "\n", nome="guarda pendente mapa")
t = marca_antes(t, ["NOVA = ", "T3 = []", "ROTA = {"])
t = troca(t, '# -*- coding: utf-8 -*-\n"""registrar_mapa_v394.py', '# -*- coding: utf-8 -*-\n' + M + ' (docstring: a descricao da rota nova e das anotacoes e\' a da v393)\n"""registrar_mapa_v394.py', nome="marca do docstring do mapa")
ast.parse(t); MAPA = t

# =============================================================================== b3_recibo_v394.py
t = bump(MOL["b3_recibo_v393.py"]); ast.parse(t); B3RECIBO = t

# =============================================================================== chain_pos_rito_v394.sh
t = bump(MOL["chain_pos_rito_v393.sh"])
HEADER = r'''#!/bin/sh
# v394 (19/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v393.sh (derivada por derivar_cadeia_v394.py; mesma ordem de passos 0..14 e mesmos portoes). O rito ja terminou (rito_v394.sh em segundo plano;
# RITO_RC=<rc> no fim do Nos\rodada_v394_stdout.txt). A v394 acrescenta o tempo e a frequencia (TimeGraviton*), a regra quadratica (RuleQuadraticResidual), a rede de Fock/Takesaki/Maxwell (F1Fecho394/*, 189 modulos novos)
# e os registros tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394, cunhagens_v394 e kh_n1_cobertura_v394.
# ORDEM: 0 guardas -> 1 o CONFERIDOR (copia byte a byte; so leitura do Nos) -> 2 a LEITURA (PROBLEMAS param) -> 3 ENSAIO das superficies em COPIAS (o plano e' conferido antes da primeira escrita; a arvore em dry;
# o sha16 da v394 na arvore (dry) e os marcadores do passo 9 nas COPIAS, conferidos ANTES de qualquer escrita real) -> 4 patch arvore/indice (OPCIONAL: so' se existir patch_arvore_indice_v394.py) -> 5 a arvore
# -> 6 atlas+indice -> 7 superficies reais (appends datados; SEM errata nova no CLAUDE.md da raiz) -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e'
# falha visivel) e a guarda de MEMORY.md (<24.000 B, <=195 linhas) -> 10 B(3) da Bancada, ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(3) APLICAR (so com B3_AUTORIZADO=sim e o evento c1)
# -> 10c religamento (AGUARDA_OPERADOR) -> 11 fechar -> 12 registrar_mapa (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V394_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito).
# Os pinos do B(n) vem de PINOS_BN_v394.json (lidos na hora; hash nunca de memoria). Sem o PINO recibo_pre_selo (a fase pre_selo da B(n) nao foi preparada) o 10 PARA em AGUARDA_OPERADOR.
# textos_v394.py, o handoff de fechar_v394.py e registrar_mapa_v394.py RECUSAM rodar enquanto tiverem trecho marcado para reescrever (as narrativas da v393 saem com a subida mecanica): os passos 0 a 2 nao os usam.
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).'''
i, j, L = bloco(t, "#!/bin/sh", "PK=")
t = "\n".join([HEADER] + L[j:])
t = troca(t, 'TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md estatuto-da-prova-07out.md"\n',
          'TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md estatuto-da-prova-07out.md"\n'
          '# o NOME do topico novo e\' lido de textos_v394.TOPICO_NOVO (uma fonte so\'); so\' roda onde e\' usado (passos 3 e 9): o textos_v394.py recusa importar com trecho marcado para reescrever\n'
          'topico_novo() { $PY -c "import sys;sys.path.insert(0,sys.argv[1]);import textos_v394 as T;print(T.TOPICO_NOVO)" "$(cygpath -w "$SEL")"; }\n', nome="topico_novo()")
# passo 3: a arvore (dry) traz o sha16 e as COPIAS trazem os marcadores do passo 9 (fail-early: nada real foi escrito)
OLD3 = '(cd "$ENST" && $PY_B arvore_da_prova.py v394 dry) || parar "a arvore_da_prova.py (copia, dry) falhou"\n'
NEW3 = (OLD3 +
        '[ -f "$ENST/arvore_dry.md" ] || parar "a arvore (dry) nao gerou arvore_dry.md em $ENST"\n'
        'echo "  (fail-early do passo 9: a arvore (dry) e as COPIAS das superficies tem de trazer o sha16 e os marcadores da v394 ANTES de qualquer escrita real)"\n'
        'exige "$ENST/arvore_dry.md" "$S16"\n'
        'TOPICO_NOVO=$(topico_novo) || parar "nao li TOPICO_NOVO de textos_v394.py (o arquivo ainda tem trecho marcado para reescrever?)"\n'
        'exige "$ENS/MEMORIA_DA_LINHAGEM.md" "$S16" "<!-- linhagem_v394_selada -->" "tempo_frequencia_v394" "kh_n1_cobertura_v394"\n'
        'exige "$ENS/DESENHO_DO_FECHAMENTO_QG.md" "<!-- adendo_v394_selada -->" "$S16"\n'
        'exige "$ENS/TGL_ATLAS.md" "<!-- atlas_v394_selada -->" "$S16" "tempo_frequencia_v394" "kh_n1_cobertura_v394"\n'
        'exige "$ENS/TGL_CORE_MEMORY.md" "<!-- core_v394_selada -->" "$S16"\n'
        'exige "$ENS/CLAUDE.md" "<!-- haja_luz_v394_selada -->" "$S16"\n'
        'exige "$ENS/MEMORY.md" "$S16"\n'
        'exige "$ENS/MEMORY_2.md" "v394"\n'
        'exige "$ENS/estatuto-da-prova-07out.md" "<!-- v394_selada -->" "$S16"\n'
        'exige "$ENS/$TOPICO_NOVO" "$S16" "tempo_frequencia_v394" "kh_n1_cobertura_v394"\n')
t = troca(t, OLD3, NEW3, nome="passo 3 fail-early")
# passo 9: os marcadores da v394 (no molde: o da errata kh_n1_cobertura_v392, da v393)
t = troca(t, '"kh_n1_cobertura_v392"\n', '"tempo_frequencia_v394" "kh_n1_cobertura_v394"\n', n=3, nome="marcadores passo 9")
t = troca(t, 'exige "$UMEM/v394-selada-a-regra-e-o-coracao-14out.md" "$S16" "tempo_frequencia_v394" "kh_n1_cobertura_v394"\n',
          'TOPICO_NOVO=$(topico_novo) || parar "nao li TOPICO_NOVO de textos_v394.py"\nexige "$UMEM/$TOPICO_NOVO" "$S16" "tempo_frequencia_v394" "kh_n1_cobertura_v394"\n', nome="topico novo no passo 9")
t = troca(t, "backups _p393 ao lado", "backups _p394 ao lado", nome="_p394")
t = troca(t, "backups .bak_<STAMP>_sup393 ao lado", "backups .bak_<STAMP>_sup394 ao lado", nome="_sup394")
t = troca(t, "o patch da v393 era das erratas CR-08/CR-02 e foi descartado; ver o relatorio", "a v394 nao tem patch da arvore/indice; as ferramentas escrevem o sha16 sozinhas (na v393 o fizeram); o passo 3 confere isso ANTES de gravar", nome="msg patch")
for proibido in ("errata_claude_md", "patch_arvore_indice_v393", "HANDOFF_v390", "handoff-v390", "refazer_sandbox_v393", "selo_anterior_v392", "kernel_manifesto_anterior_v392", "base_v392", "V393_AVISO", "v393-selada-a-regra", "kh_n1_cobertura_v392"):
    assert proibido not in t, ("resto da v393 na cadeia", proibido)
CHAIN = t

# =============================================================================== gravar e conferir
DERIV = {"leitura_v394.py": LEITURA, "superficies_v394.py": SUPERFICIES, "fechar_v394.py": FECHAR, "b3_recibo_v394.py": B3RECIBO, "chain_pos_rito_v394.sh": CHAIN, "textos_v394.py": TEXTOS, "registrar_mapa_v394.py": MAPA}
for n, tx in DERIV.items():
    grava(n, tx)
todos = {n: rd(HERE, n) for n in DERIV}
# invariantes do molde (DERIVACAO_v393.json), subidos de versao, que tem de sobreviver
INV93 = json.load(open(os.path.join(MOLDE, "DERIVACAO_v393.json"), encoding="utf-8"))["invariantes"]
INV = {}
for n93, lst in INV93.items():
    n94 = bump(n93)
    INV[n94] = [bump(x) for x in lst]
INV["leitura_v394.py"] = [x for x in INV["leitura_v394.py"] if x not in ("regra_consumidor_v393", "coracao_e_selo_gravitacional_v393")] + ["REG_V393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394",
                                                                                                                                              "kernel_modulos_novos_v394.json", "axiom_coverage_v392", "dict.fromkeys"]
INV["fechar_v394.py"] = [x for x in INV["fechar_v394.py"] if x != "insumo_codex_regra_sha16"] + ["insumos_codex_sha16", "_f394", "FECHAR RECUSADO:"]
INV["superficies_v394.py"] += ["_sup394", "V394_AVISO_REIVINDICACAO", "(handoff-v393-custodia.md)", "- [HANDOFF v393"]
INV["chain_pos_rito_v394.sh"] += ["V394_AVISO_REIVINDICACAO", "topico_novo()", "textos_v394", "arvore_dry.md", "_p394", "_sup394", "base_v393", "selo_anterior_v393", "kernel_manifesto_anterior_v393", "/c/IALD/Central de Patentes/work/cadeia_de_selo/v394",
                                  "B3_AUTORIZADO\" = \"sim\"", "exit 20", "C:/t/k394/arvore", "RECIBO_PARADA_v394.json", "RECIBO_RELIGAMENTO_v394.json", "--versao v394 --fase pos_selo"]
INV["textos_v394.py"] += ["_MARCA_PENDENTE", "TOPICO_NOVO"]
INV["registrar_mapa_v394.py"] += ["_MARCA_PENDENTE", "umpy.v392.pedras_e_barreiras", "assert selo.get(\"um_version\") == \"v394\""]
INV["b3_recibo_v394.py"] += ["versao_alvo\") != \"v394\""]
conf = {}; falhas = []
for n, lst in INV.items():
    conf[n] = {}
    for x in lst:
        ok = x in todos[n]; conf[n][x[:90]] = ok
        if not ok:
            falhas.append((n, x[:90]))
sint = {}
for n, tx in todos.items():
    if n.endswith(".py"):
        ast.parse(tx); sint[n] = "ast.parse ok"
    else:
        r = subprocess.run(["sh", "-n", os.path.join(HERE, n)], capture_output=True, text=True); sint[n] = "sh -n rc=%d %s" % (r.returncode, r.stderr[:200])
        if r.returncode:
            falhas.append((n, "sh -n"))
    assert "\r" not in tx, ("CR em", n)
# os portoes do B(n) (b3_prepara e os passos 10, 10a, 10b, 10c: AGUARDA_OPERADOR, B3_AUTORIZADO, EVENTO/EVENTO_HASH, recibos) TEM de ser identicos ao molde da v393 a menos da subida de versao
molde_b = bump(MOL["chain_pos_rito_v393.sh"])
for ini, fim in (("b3_prepara() {", 'echo "== 0.'), ("if quer 10; then", "if quer 11; then")):
    ia, ja, La = bloco(molde_b, ini, fim); ib, jb, Lb = bloco(CHAIN, ini, fim)
    if La[ia:ja] != Lb[ib:jb]:
        falhas.append(("portao do B(n) difere do molde subido de versao", ini))
    else:
        conf.setdefault("chain_pos_rito_v394.sh", {})["trecho identico ao molde (bump): " + ini] = True
# marcas: contagem por arquivo (as narrativas a reescrever) e as de ajuste ao ESPERADOS
marcas = {n: tx.count(M) for n, tx in todos.items() if tx.count(M)}
marcas_aj = {n: tx.count(MARCA_AJ) for n, tx in todos.items() if tx.count(MARCA_AJ)}
for n in ("textos_v394.py", "fechar_v394.py", "registrar_mapa_v394.py"):
    assert marcas.get(n, 0) > 0 and "_MARCA_PENDENTE" in todos[n], ("sem marca ou sem guarda de pendencia", n)
assert not any(M in todos[n] for n in ("leitura_v394.py", "superficies_v394.py", "b3_recibo_v394.py", "chain_pos_rito_v394.sh")), "marca de narrativa em arquivo que nao e' narrativa"
# rotulos de versao: nenhum resto de '..._v393'/'_sup393'/... onde o sentido e' 'esta versao'. O que fica com 393/392 e' so' a versao ANTERIOR ou nome historico (lista abaixo, conferida)
OK_393 = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393", "base_v393", "selo_anterior_v393", "kernel_manifesto_anterior_v393", "handoff-v393-custodia",
          "REG_V393", "vereditos_v393", "escada_v393_e_v394", "formal.regra.integracao_v393", "AO_CLAUDE_INTEGRAR_REGRA_V393", "leitura_v393.py", "superficies_v393.py", "textos_v393.py", "fechar_v393.py", "registrar_mapa_v393.py",
          "chain_pos_rito_v393.sh", "derivar_cadeia_v393.py", "b3_recibo_v393.py", "KH_N1_v392", "kh_n1_cobertura_v392", "axiom_coverage_v392", "varredura_e_sorry_v392", "pedras_v392", "umpy.v392.pedras_e_barreiras",
          "estatuto_da_prova_v391", "fundacao_v390", "three_stress_tests_v387", "ESPERADOS_v393.json",
          "registros_v393", "fechar_v390.py", "DIFF_v393_v394.diff")   # (mencao ao campo/arquivo da versao anterior; 'DIFF_v393_v394' e' o diff da base v393 -> o selado v394)
resid = {}
for n, tx in todos.items():
    for m in re.finditer(r"[A-Za-z0-9_\-\.\[\]/]*(?<![0-9a-f])39[0-3][A-Za-z0-9_\-\.\[\]]*", tx):
        tok = m.group(0).rstrip(".")
        if re.fullmatch(r"[0-9a-f]*39[0-3][0-9a-f]*", tok) and len(tok) >= 8:
            continue   # hash hexadecimal
        resid.setdefault(tok, set()).add(n)
estranhos = {}
for tok, ns in resid.items():
    if any(p in tok for p in OK_393) or tok in ("v393", "v392", "v391", "v390") or (tok == "393" and ns == {"textos_v394.py"}):
        continue   # ('393' em textos_v394.py e' a citacao verbatim do operador «na v 393», dentro de narrativa MARCADA)
    estranhos[tok] = sorted(ns)
    falhas.append(("rotulo estranho com 390-393", tok, sorted(ns)))
# a guarda de texto (P18) sobre o arquivo de narrativa: nenhuma palavra proibida
sys.path.insert(0, os.path.dirname(PK)); sys.path.insert(0, PK)
try:
    from guarda_p18_v394 import violacoes
except ImportError:
    from importlib import util as _u
    _sp = _u.spec_from_file_location("guarda_p18_v393", os.path.join(os.path.dirname(PK), "v393", "guarda_p18_v393.py")); _m = _u.module_from_spec(_sp); _sp.loader.exec_module(_m); violacoes = _m.violacoes
gv = {n: violacoes(todos[n]) for n in ("textos_v394.py", "registrar_mapa_v394.py", "fechar_v394.py", "leitura_v394.py", "superficies_v394.py", "chain_pos_rito_v394.sh")}
if any(gv.values()):
    falhas.append(("guarda P18", {k: v[:3] for k, v in gv.items() if v}))
# campos de ESPERADOS/CANDIDATO/PINOS que os derivados leem (PALPITES a conferir quando ESPERADOS_v394.json existir)
RX = {"ESPERADOS": re.compile(r"ESP(?:ERADOS)?\[['\"]([^'\"]+)['\"]\]|ESP\.get\(['\"]([^'\"]+)['\"]"), "CANDIDATO": re.compile(r"CM\[['\"]([^'\"]+)['\"]\]|CM\.get\(['\"]([^'\"]+)['\"]")}
campos = {"ESPERADOS": sorted({a or b for tx in todos.values() for a, b in RX["ESPERADOS"].findall(tx)}), "CANDIDATO": sorted({a or b for tx in todos.values() for a, b in RX["CANDIDATO"].findall(tx)})}
campos["ESPERADOS"] = [c for c in campos["ESPERADOS"] if not c.endswith("_")]   # (so' o prefixo de um nome montado por concatenacao: veredito_<registro>_do_ensaio)
campos["PINOS_BN"] = ["bateria", "criterios", "esboco_R3_3", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "recibo_pre_selo", "selo_anterior_v393 (opcional)", "kernel_manifesto_anterior_v393 (opcional)"]   # do b3_prepara da cadeia
presentes = {}
for rotulo, arq in (("ESPERADOS", "ESPERADOS_v394.json"), ("CANDIDATO", "CANDIDATO_v394.json"), ("PINOS_BN", "PINOS_BN_v394.json")):
    p = os.path.join(PK, arq)
    if os.path.exists(p):
        d = json.load(open(p, encoding="utf-8"))
        presentes[rotulo] = {"arquivo_sha16": sha16(open(p, "rb").read()), "faltam": [c for c in campos[rotulo] if c not in d and not c.endswith("(opcional)")]}
    else:
        presentes[rotulo] = {"arquivo": "ainda nao existe (gerado por outro processo): conferir os campos abaixo quando existir"}
DER = {"molde": {n: sha16(MOL[n].encode("utf-8")) for n in MOL}, "molde_derivar_cadeia_v393": sha16(open(os.path.join(MOLDE, "derivar_cadeia_v393.py"), "rb").read()),
       "derivados": {n: sha16(todos[n].encode("utf-8")) for n in todos},
       "sobe": "v393 -> v394, v392 -> v393 (anterior), V393 -> V394, V392 -> V393, k393 -> k394; PROT (nao sobem): " + ", ".join(PROT),
       "marcas_texto_a_reescrever": {"marca": "linha de comentario '# TEXTO_A_REESCREVER' + '_V394' (montada por concatenacao no derivador)", "por_arquivo": marcas, "total": sum(marcas.values()),
                                     "regra": "os tres arquivos com marca (textos, fechar, registrar_mapa) RECUSAM rodar (SystemExit) enquanto a marca existir; a gerencia reescreve a narrativa e tira a marca"},
       "marcas_ajuste_ao_esperados": {"marca": MARCA_AJ, "por_arquivo": marcas_aj},
       "campos_lidos_dos_arquivos_da_v394": campos, "arquivos_da_v394_no_pacote": presentes,
       "rotulos_corrigidos_em_relacao_ao_molde": {"superficies": "MARCA_BAK _sup392 -> _sup394; variavel de ambiente V392_AVISO_REIVINDICACAO (molde, lida no codigo) -> V394_AVISO_REIVINDICACAO (a que a cadeia exporta)",
                                                  "fechar": "_f392 (3 ocorrencias, atrasadas no molde) -> _f394", "chain": "_p393 -> _p394; _sup393 -> _sup394; V393_AVISO_REIVINDICACAO -> V394_AVISO_REIVINDICACAO"},
       "risco_1_passo_9": "a v393 passou o passo 9 (A_PROVA_DA_QG_TGL_arvore.md: 1 ocorrencia do sha16, na linha do sha256 completo; TGL_INDICE_VIVO.md: 3) porque arvore_da_prova.py e atlas_indice.py escrevem o sha da versao sozinhos; "
                          "a v394 NAO fica pior e fica melhor: o passo 3 exige o sha16 na arvore (dry) e os marcadores do passo 9 nas COPIAS antes de qualquer escrita real. Nao ha patch_arvore_indice_v394.py (passos 3/4 o tratam como opcional).",
       "risco_3_memory_md": "medido hoje: 192 linhas e 19.743 B (limites 195 e 24.000); a compactacao de ganchos antigos do molde segue (31 linhas em 9 corridas elegiveis); o passo 3 mede a copia e o passo 9 mede o real.",
       "invariantes": conf, "sintaxe": sint, "guarda_p18": {k: ("LIMPO" if not v else v[:3]) for k, v in gv.items()}, "rotulos_estranhos": estranhos, "falhas": falhas,
       "nao_validado": "nenhum derivado foi EXECUTADO nem revisto por cetico independente; so' ast.parse, sh -n, invariantes, rotulos e a guarda de texto; as narrativas da v393 estao MARCADAS para reescrever e os campos de ESPERADOS marcados para ajustar"}
grava("DERIVACAO_v394.json", json.dumps(DER, ensure_ascii=False, indent=1))
print("DERIVADOS:", ", ".join("%s %s" % (n, DER["derivados"][n]) for n in DER["derivados"]))
print("SINTAXE:", json.dumps(sint, ensure_ascii=False))
print("MARCAS texto:", json.dumps(marcas, ensure_ascii=False), "| ajuste:", json.dumps(marcas_aj, ensure_ascii=False))
print("ARQUIVOS DA v394 NO PACOTE:", json.dumps(presentes, ensure_ascii=False)[:600])
print("INVARIANTES:", sum(len(v) for v in conf.values()), "conferidos;", "FALHAS:", falhas if falhas else "nenhuma")
sys.exit(1 if falhas else 0)
