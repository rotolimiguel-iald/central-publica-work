# -*- coding: utf-8 -*-
"""derivar_cadeia_v396.py -- DERIVA a cadeia pos-rito da v396 a partir do molde REAL e FINAL da v395 (cadeia_de_selo/v395/pos_rito, o que RODOU de verdade em 21/10; seus arquivos conferem com a DERIVACAO_v395.json por sha16) (molde do derivador:
derivar_cadeia_v395.py). A subida de versao e' UMA passada com fronteira de digitos (394 -> 395 e 395 -> 396: v/V/_sup/_f/_p/_m/k...), com a lista PROT dos nomes historicos que NAO sobem (registros e chaves do core nascidos em v393/v394, ext_bin394...);
os registros nascidos na v395 (psibit_v395...) NAO sao protegidos: o que sobrar deles vira psibit_v396, um nome que nao existe, e o derivador RECUSA (assert) -- toda mudanca de conteudo e' uma regra NOMEADA com contagem exata.
GERA (subida + regras com contagem exata; o script ABORTA se uma regra nao casar o numero esperado de vezes):
  chain_pos_rito_v396.sh, leitura_v396.py, superficies_v396.py, fechar_v396.py, b3_recibo_v396.py (a logica do B(n) simples nao muda: so' a subida),
  harness_textos_ensaio_v396.py, harness_fechar_sandbox_v396.py (os harness da v395 subidos + regras: a testemunha no lugar do psibit, os controles negativos novos, o refazer_out opcional so' com --nao-exigir-refazer, a validacao do registro pela rotas._valida SEM registrar).
CONFERE (autorais, escritos para a v396; a logica muda e uma derivacao mecanica nao a cobriria): textos_v396.py, registrar_mapa_v396.py (ast.parse, invariantes por texto, guarda P18, nenhuma marca pendente, e cada nome T.<x> chamado pelos derivados existe em textos_v396.py).
NAO executa nenhum script derivado: so' ast.parse, sh -n, invariantes, rotulos e a guarda de texto P18. Nao toca o Nos, a Bancada, a memoria, o Atlas, o mapa, o quadro, o tunel, o site nem o git.
GRAVA: DERIVACAO_v396.json (sha16 do molde, de cada derivado e de cada autoral; o molde confere com a DERIVACAO_v395; invariantes; sintaxe; marcas; rotulos; o que difere do molde). Reexecutavel: o que muda ganha .bak_<STAMP>_c1 (backup de BYTES).
Uso: python -I -B -X utf8 derivar_cadeia_v396.py"""
import ast, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)
MOLDE = os.path.join(os.path.dirname(PK), "v395", "pos_rito")
STAMP = time.strftime("%Y%m%d_%H%M%S")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
PALAVRA = "TEXTO_A_" + "REESCREVER"          # a palavra da marca, montada por concatenacao: este arquivo nunca a traz por extenso
MARCA = PALAVRA + "_V396"
# nomes que NAO sobem de versao: registros e chaves historicos do core (nascidos em v393 e v394), arquivos e rotas de versoes passadas
PROT = ["pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394",
        "criterio_binario_de_parada_v394", "declaration_sources_status_v394", "declaration_sources_v394", "umpy.v394.fock_tempo_e_cunhagens", "ext_bin394", "ponto_fixo_v394_d19", "C13_kh_n1_v394"]
MODELOS = ("leitura_v395.py", "superficies_v395.py", "fechar_v395.py", "chain_pos_rito_v395.sh", "b3_recibo_v395.py", "harness_textos_ensaio_v395.py", "harness_fechar_sandbox_v395.py")
AUTORAIS = ("textos_v396.py", "registrar_mapa_v396.py")
GUARDA_PENDENTE_RX = re.compile(r"(?m)^\s*#\s*" + MARCA)
RX_V = re.compile(r"(?<![0-9])39([45])(?![0-9])")        # fronteira de digitos: nao toca 3945, 13940, 0.394...
RX_HEXWORD = re.compile(r"[0-9A-Za-z_]*(?<![0-9])39[45](?![0-9])[0-9A-Za-z_]*")


def sobe(t):
    """subida de versao em UMA passada (394 -> 395, 395 -> 396), com os nomes historicos de PROT intactos."""
    for i, p in enumerate(PROT):
        t = t.replace(p, "@@P%d@@" % i)
    t = RX_V.sub(lambda m: "39" + str(int(m.group(1)) + 1), t)
    for i, p in enumerate(PROT):
        t = t.replace("@@P%d@@" % i, p)
    return t


def sem_hex(t, nome):
    """nenhuma ocorrencia de 394/395 dentro de uma palavra HEXADECIMAL (um hash seria subido por engano)."""
    for m in RX_HEXWORD.finditer(t):
        w = m.group(0)
        assert not (re.fullmatch(r"[0-9a-f]{8,}", w)), ("a subida tocaria um hash hexadecimal", nome, w)


def rd(d, n):
    return open(os.path.join(d, n), "rb").read().decode("utf-8")


def tr(t, old, new, n=1, nome=""):
    """troca sobe(old) por `new` (texto FINAL, nunca subido), exigindo exatamente n ocorrencias; `old` e' o texto do MOLDE (v395)."""
    o = sobe(old)
    assert t.count(o) == n, ("troca", nome or old[:70], t.count(o), n)
    return t.replace(o, new)


def tr_re(t, pattern, repl, n, nome=""):
    """troca por expressao regular (aplicada ao texto JA SUBIDO), exigindo exatamente n ocorrencias."""
    found = re.findall(pattern, t)
    assert len(found) == n, ("troca_re", nome or pattern, len(found), n)
    return re.sub(pattern, repl, t)


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
for n_, tx_ in MOL.items():
    sem_hex(tx_, n_)
# o molde e' o que a DERIVACAO_v395 registrou (os arquivos nao foram editados depois da derivacao; o rito real da v395 os usou como estao)
DER95 = json.load(open(os.path.join(MOLDE, "DERIVACAO_v395.json"), encoding="utf-8"))
reg95 = dict(DER95["derivados"]); reg95.update(DER95["autorais"])
MOLDE_CONFERE = {n: (sha16(MOL[n].encode("utf-8")) == reg95.get(n)) for n in MODELOS}
assert all(MOLDE_CONFERE.values()), ("o molde da v395 difere da DERIVACAO_v395.json (foi editado depois da derivacao?)", MOLDE_CONFERE)

# =============================================================================== leitura_v396.py
t = sobe(MOL["leitura_v395.py"])
i = t.index("import glob, hashlib, json, os, re, sys, datetime")
HEAD_L = ('# -*- coding: utf-8 -*-\n'
          '# A LEITURA da rodada v396 (molde: leitura_v395.py FINAL, o que rodou em 21/10): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v396, que aqui e\' o proprio pacote).\n'
          '# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e\' digitado: tudo sai dos JSON, do core, do selo e do stdout do rito.\n'
          '# v396: os registros NOVOS do core sao testemunha_estatica_v396 (runtime: a funcao chamada NA FRACTALIZACAO DO UM, logo depois do bloco do psibit_v395) e cunhagens_v396 e kh_n1_cobertura_v396 (por spec; ESPERADOS[registros_v396]); os da v395 (psibit_v395,\n'
          '# cunhagens_v395, kh_n1_cobertura_v395), os da v394 e os da v393 seguem no core e tem de seguir selados; o modulo novo de kernel (TGLExt/TestemunhaEstatica.lean) vem de ESPERADOS[pedras_sha256] e e\' conferido aqui contra o arquivo do kernel do Nos.\n'
          '# A escada vem de ESPERADOS[escada_v395_e_v396] e ESPERADOS[escada]; a troca dita (so numeros) e\' a de ESPERADOS[troca_dita]. O registro testemunha_estatica_v396 e\' conferido por inteiro (formal + suporte + mecanica + escada + fonte embutida + beta + inscricoes;\n'
          '# a composicao incondicional no kernel; a face de Fock do psion CONDICIONAL, declarada em Psibit.lean FORA da pedra e sem habitante exibido) e a linha `[v396] ... registros por spec` do stdout do rito tem de dizer selados == registros por spec;\n'
          '# o AVISO da v396 (e de qualquer bloco v393 a v395) no stdout reprova.\n'
          '# Diferencas para a v395: os registros novos sao DESCOBERTOS por comparacao com ESPERADOS[vereditos_v395]; o conferidor e\' lido da copia em pos_rito/conferidor (a cadeia o copia antes); V[\'testemunha\'], V[\'reg396\'] e V[\'patch_ids\'] sao os campos da v396;\n'
          '# a face condicional do psibit_v395 (bandeira True, sem habitante) e os registros da v395 sao conferidos de novo.\n')
t = HEAD_L + t[i:]
t = subst_linha(t, "REG_V395 = (", '''REG_V394 = ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394")   # da v394: seguem no core e seguem selados (nao sao 'novos' da v396)
REG_V395 = ("psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395")   # da v395: seguem no core e seguem selados (nao sao 'novos' da v396)''')
t = subst_linha(t, "REG_FIXOS = (", '''REG_FIXOS = ("testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396")   # os tres registros NOVOS do core v396; + os de ESPERADOS[registros_v396] (REG_TODOS, dentro de ler)''')
assert "REG_V393 = (" in t and t.count("REG_V394 = (") == 1 and t.count("REG_V395 = (") == 1
NOVO_STDOUT = r'''    if [l for l in out.splitlines() if '[v396] AVISO' in l]:
        P.append('o stdout traz AVISO da v396 (a testemunha estatica ou os registros por spec nao rodaram): %s' % [l.strip()[:200] for l in out.splitlines() if '[v396] AVISO' in l][:2])
    elif [l for l in out.splitlines() if re.search(r'\[v39[3-5]\] AVISO', l)]:
        P.append('o stdout traz AVISO de um bloco anterior (v393 a v395): %s' % [l.strip()[:200] for l in out.splitlines() if re.search(r'\[v39[3-5]\] AVISO', l)][:2])
    m_sp = re.search(r'\[v396\] a testemunha estatica \(o psion habita a fronteira\): .*\| registros por spec: (\d+) \(selados (\d+)\)', out)
    if not m_sp or m_sp.group(1) != m_sp.group(2) or int(m_sp.group(1)) != len(ESP.get('registros_v396') or {}):
        P.append('a linha [v396] do stdout nao diz registros por spec selados == %d (%s)' % (len(ESP.get('registros_v396') or {}), m_sp.groups() if m_sp else 'ausente'))'''
t = subst_bloco(t, "    if [l for l in out.splitlines() if '[v396] AVISO' in l]:", "    hp = os.path.join(PK, 'rito_horarios_v396.txt')", NOVO_STDOUT)
NOVO_V396 = r'''    # --- v396: os tres registros novos conferidos contra o ensaio a seco registrado em ESPERADOS, e os da v395, da v394 e da v393, que seguem no core e tem de seguir selados; nenhum numero e' digitado
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
'''
t = subst_bloco(t, "    # --- v396: os tres registros novos conferidos", "    qp = core.get('quantum_pillar_v384')", NOVO_V396)
for proibido in ("AJUSTAR", "psibit_v396", "V['psibit']", "modo psionico", "reg395", "REG_V396"):
    assert proibido not in t, ("sobrou na leitura:", proibido)
ast.parse(t); LEITURA = t

# =============================================================================== superficies_v396.py
t = sobe(MOL["superficies_v395.py"])
i = t.index("# Registro da v396 SELADA"); j = t.index("import os, re, sys, time")
CAB = ("# Registro da v396 SELADA nas superficies de memoria (molde: superficies_v395.py FINAL, o que rodou em 21/10), pela regra da linhagem completa.\n"
       "# Diario (MEMORIA_DA_LINHAGEM, append datado), desenho (ADENDO), Atlas (append datado), TGL_CORE_MEMORY (append datado), o CLAUDE.md da Haja_Luz, as memorias-topico (missao, central, estatuto, e o topico NOVO da v396),\n"
       "# o MEMORY.md/MEMORY_2.md, e (so' sob reivindicacao nomeada em V396_AVISO_REIVINDICACAO) o AVISO_GERENCIA.md da ORDEM_019.\n"
       "# SEM erratas inline nesta versao (as erratas da v396 vao DENTRO dos blocos datados). A funcao inserir_ao_lado fica disponivel (nao e' chamada).\n"
       "# Duas fases (plano conferido ANTES da primeira escrita); backup de BYTES (.bak_<STAMP>_sup396); temporario -> conferir tamanho -> substituir; idempotente pelo marcador de cada bloco;\n"
       "# fim de linha de cada arquivo respeitado. GUARDA: so' grava se a leitura nao tiver problema E se a guarda de texto (P18, cinco regras) estiver limpa em todo texto novo.\n"
       "# Ensaio: --copias <pasta com copias dos alvos> (nada real e' tocado). MEMORY.md: ate 24.000 B e 195 linhas; se o indice passar de 192 linhas (o limite menos uma folga de tres), COMPACTA corridas de ganchos antigos (linhas que ja sao ponteiros ao\n"
       "# MEMORY_2.md) num ponteiro unico, com as linhas movidas VERBATIM ao MEMORY_2.md (regra dos dois arquivos); se nao houver como compactar o bastante, RECUSA sem escrever nada (rc 3). A linha do handoff novo entra ANTES da linha do handoff da v395\n"
       "# (que a custodia da v395 reescreveu: conferida presente no MEMORY.md real em 22/10, uma so').\n")
t = t[:i] + CAB + t[j:]
assert "sup395" not in t and "V395_AVISO" not in t and "V394" not in t and "(handoff-v395-custodia.md)" in t and "- [HANDOFF v395" in t and "V396_AVISO_REIVINDICACAO" in t
ast.parse(t); SUPERFICIES = t

# =============================================================================== fechar_v396.py
t = sobe(MOL["fechar_v395.py"])
assert "AO_CLAUDE" not in t and "_dd" not in t and "AJUSTAR" not in t and "_f395" not in t and "rede_fock" not in t.replace("registros_v396", "") and "psibit" not in t.lower()
ast.parse(t); FECHAR = t

# =============================================================================== b3_recibo_v396.py (a logica do B(n) simples nao muda: so' a subida; o harness a exercita com recibos SINTETICOS)
t = sobe(MOL["b3_recibo_v395.py"])
assert "v395" in t and "v394" not in t and "PINOS_BN_v396.json" in t and 'r.get("versao_alvo") != "v396"' in t and 'ma.get("version") != "v395"' in t and "B%d-v396-" in t
ast.parse(t); B3RECIBO = t

# =============================================================================== chain_pos_rito_v396.sh
t = sobe(MOL["chain_pos_rito_v395.sh"])
HEADER = r'''#!/bin/sh
# v396 (22/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v395.sh FINAL (o que rodou em 21/10; derivada por derivar_cadeia_v396.py; mesma ordem de passos 0..14 e mesmos portoes). O rito ja terminou (rito_v396.sh em segundo plano;
# RITO_RC=<rc> no fim do Nos\rodada_v396_stdout.txt). A v396 e' um DELTA PEQUENO: 1 modulo novo de kernel (TGLExt/TestemunhaEstatica, o psion como habitante da testemunha estatica; nome provisorio), o registro testemunha_estatica_v396 (a funcao do runtime
# chamada NA FRACTALIZACAO DO UM, logo depois do bloco do psibit_v395) e os registros por spec cunhagens_v396 (as tres falas de 22/10) e kh_n1_cobertura_v396; os tres contratos da v394 e o contrato do psibit_v395 ganham expected_ladder novo e
# kh_n1_cobertura_v395 passa a piso (erratas ao lado).
# ORDEM: 0 guardas -> 1 o CONFERIDOR (copia byte a byte, com o delta_v396.py que ele importa; so leitura do Nos) -> 2 a LEITURA (PROBLEMAS param) -> 3 ENSAIO das superficies em COPIAS (o plano e' conferido antes da primeira escrita; a arvore em dry;
# o sha16 da v396 na arvore (dry) e os marcadores do passo 9 nas COPIAS, conferidos ANTES de qualquer escrita real) -> 4 patch arvore/indice (OPCIONAL: so' se existir patch_arvore_indice_v396.py) -> 5 a arvore
# -> 6 atlas+indice -> 7 superficies reais (appends datados; SEM errata nova no CLAUDE.md da raiz) -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e'
# falha visivel) e a guarda de MEMORY.md (<24.000 B, <=195 linhas) -> 10 B(n) da Bancada, ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(n) APLICAR (so com B3_AUTORIZADO=sim e o evento c1)
# -> 10c religamento (AGUARDA_OPERADOR) -> 11 fechar -> 12 registrar_mapa (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V396_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito).
# PASSO 10 SEM SALTO: a Bancada de producao pina a v395 (B5) e o Nos e' a v395 ate' a instalacao; portanto o B(n) da v396 e' um passo SIMPLES v395 -> v396 (esboco R3.5, sincronizar_bancada.py): NAO ha a opcao de cadeia de selos do esboco, nem o pino correspondente,
# e o b3_recibo_v396.py NAO tem o 3o argumento. Os pinos vem de PINOS_BN_v396.json (lidos na hora; hash nunca de memoria): criterios, esboco_R3_5, gerador_bateria, driver_t12_t14, bateria_base_R2, kernel_recibo (o KERNEL_RECIBO_v396.json,
# contrato R3_2: a v396 nao acrescenta modulo de auditoria), candidato, esperados, pins_do_candidato, recibo_pre_selo (gerado antes da instalacao; veredito JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA), selo_anterior_v395 e
# kernel_manifesto_anterior_v395 (as copias de bytes do selo e do manifesto do kernel da v395, em base_v395). A BATERIA da v396 e' GERADA por script no 10 (depois do selo; bateria por versao) e pinada ao lado (bateria_pos_selo/PINOS_BATERIA_v396.json).
# Vereditos esperados (lidos do codigo do esboco, nao rodados): ensaio REPINADA_B<n>__ENSAIO__NADA_GRAVADO_NA_BANCADA e aplicar REPINADA_B<n>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_, com n = a geracao do manifesto que a
# Bancada pina + 1 (B5 -> n = 6; o b3_recibo_v396.py o confere). A parada do servico (10a) e o religamento (10c) sao ato do operador (V396_AUTORIZACAO_OPERADOR nos scripts bancada_B3_servico\recibo_parada_v396.py e recibo_religamento_v396.py); o chain so' confere os recibos.
# textos_v396.py, fechar_v396.py e registrar_mapa_v396.py RECUSAM rodar se tiverem trecho marcado para reescrever: os passos 0 a 2 nao os usam. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como na v395, com os rotulos da v396.
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).'''
i, j, L = bloco(t, "#!/bin/sh", "PK=")
t = "\n".join([HEADER] + L[j:])
# os marcadores dos passos 3 e 9: os da testemunha estatica e do kh_n1 da v396 (6 ocorrencias: 3 no ensaio das copias, 3 nas superficies reais)
t = tr(t, '"psibit_v395" "kh_n1_cobertura_v395"', '"testemunha_estatica_v396" "kh_n1_cobertura_v396"', n=6, nome="marcadores dos passos 3 e 9")
# a unica data herdada do molde no corpo do chain (o comentario do b3_prepara): 21/10/2026 -> 22/10/2026
t = tr(t, "  # v395 (21/10/2026): o B(n) da v395 e' um PASSO SIMPLES", "  # v396 (22/10/2026): o B(n) da v396 e' um PASSO SIMPLES", nome="data do comentario do b3_prepara")
for proibido in ("--cadeia-de-selos", "W_CAD", "$CAD", "SALTO v392", "R3_4", "fundir_pinos", "psibit_v396", "selo_anterior_v394", "base_v394", "textos_v395", "leitura_v395", "fechar_v395", "PINOS_BN_v395"):
    assert proibido not in t, ("resto da v395 na cadeia", proibido)
CHAIN = t

# =============================================================================== harness_textos_ensaio_v396.py
t = sobe(MOL["harness_textos_ensaio_v395.py"])
DOC_HT = r'''"""harness_textos_ensaio_v396.py -- o HARNESS DO POS-RITO da v396 em modo ENSAIO (derivado do harness_textos_ensaio_v395.py, que rodou na v395); SO' LEITURA do Nos real, da producao e das superficies reais.
Importa os modulos REAIS textos_v396.py e leitura_v396.py (os que a cadeia usa) e os executa contra um NOS EMULADO montado de dry_v396 (core_ensaio.json -> um_absoluto.json, selo_ensaio.json -> um_absoluto_selo.json, o um.py candidato, o kernel,
o .md, o artigo PT/EN e o sumario; o stdout do rito e o APLICADO_AO_CANONICO sao EMULADOS e ditos). Tudo o que ele escreve fica em pos_rito\\harness_saida_v396\\ (e o resumo HARNESS_TEXTOS_ENSAIO_v396.json ao lado dele); nada do Nos real,
da memoria, do Atlas, do mapa de rotas, da Bancada ou do git e' tocado; nenhum rito e' rodado.
O que ele prova (cada etapa e' uma entrada do resumo):
  precondicoes   o candidato (ESPERADOS == CANDIDATO == arquivo == dry_v396/um.py) e a regeneracao terminada (refazer_out_v396.txt mostra '== FIM'); a evidencia carrega mtime e sha16 de cada entrada;
  conferidor     o conferir_rito_v396.py REAL (copia) roda contra o Nos emulado (V396_NOS) e da' TUDO BATE: a conferencia que a leitura le;
  leitura        a leitura_v396.ler() REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS (selo de outra versao, registro ausente, registro nao selado, face de Fock habitada ou dita dentro da pedra, mecanica que nao passou, composicao fora do trio,
                 registro da v395 ou da v394 nao selado, face de Fock do psibit habitada, AVISO da v396 ou de bloco anterior no stdout), cada um tem de reprovar;
  textos         todas as funcoes publicas de textos_v396 renderizam, a guarda P18 fica limpa em cada saida, os marcadores que a cadeia exige estao nos textos, a errata da palavra «teoremas» esta nos textos que carregam _num;
  cita_so_o_que_existe   cada `termo` entre crases de cada texto e' achado no kernel do Nos emulado, no um.py, nos insumos, nos arquivos ou como hash lido (o que nao e' achado e' dito e reprova);
  superficies    superficies_v396.py REAL roda em COPIAS das superficies reais (o plano e' conferido antes da primeira escrita; idempotente na 2a rodada; os marcadores do passo 9; MEMORY.md < 24 000 B e <= 195 linhas); os originais nao mudam;
  b3_recibo      b3_recibo_v396.py REAL contra recibos SINTETICOS derivados dos recibos reais da v395 (positivos e controles negativos);
  mapa           registrar_mapa_v396.montar() REAL contra o core emulado e o livro de rotas real (so' leitura), e cada registro validado pela MESMA funcao que o mapa usa (rotas._valida), SEM registrar; grava registro_mapa_v396_ENSAIO.json (nao e' o registro);
  marcas         nenhuma linha de comentario com a marca de texto pendente em pos_rito\\*.py; ast.parse de todo .py e sh -n do chain.
uso: python -I -B -X utf8 harness_textos_ensaio_v396.py [--sem-superficies] [--sem-b3] [--sem-negativos] [--rotulo <nome>] [--nao-exigir-refazer] [--manter-copias]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita, nada foi rodado;
--nao-exigir-refazer: NAO exige refazer_out_v396.txt (nem o '== FIM' nem as datas): modo de ENSAIO antes de a gerencia regerar o candidato; o resumo e o veredito DIZEM que a regeneracao nao foi comprovada;
sem --manter-copias o Nos emulado e as copias pesadas das superficies sao apagados no fim, so' dentro de harness_saida_v396)"""'''
t = subst_bloco(t, '"""harness_textos_ensaio_v396.py', "import contextlib", DOC_HT)
t = tr_re(t, r"\bV5\b", "PKG", 28, "V5 -> PKG (a pasta do pacote desta versao)")
t = tr_re(t, r"\bV4\b", "PKG_ANT", 3, "V4 -> PKG_ANT (a pasta do pacote da versao anterior)")
# precondicoes: o refazer_out so' e' exigido sem --nao-exigir-refazer
t = tr(t, 'for n in ("ESPERADOS_v395.json", "CANDIDATO_v395.json", "um_v395_candidato.py", "PINOS_BN_v395.json", "refazer_out_v395.txt"):\n    if not os.path.exists(os.path.join(PKG, n)):\n        recusa("falta %s no pacote" % n)',
       'for n in ("ESPERADOS_v396.json", "CANDIDATO_v396.json", "um_v396_candidato.py", "PINOS_BN_v396.json") + (() if NAO_REFAZER else ("refazer_out_v396.txt",)):\n    if not os.path.exists(os.path.join(PKG, n)):\n        recusa("falta %s no pacote" % n)', nome="precondicoes: arquivos do pacote")
t = tr(t, 'refazer = rd(os.path.join(PKG, "refazer_out_v395.txt"))', 'refazer = rd(os.path.join(PKG, "refazer_out_v396.txt")) if os.path.exists(os.path.join(PKG, "refazer_out_v396.txt")) else ""', nome="refazer opcional")
t = tr(t, 'EVID = {n: {"mtime": mt(os.path.join(PKG, n)), "sha16": fsha(os.path.join(PKG, n))[:16]} for n in ("ESPERADOS_v395.json", "CANDIDATO_v395.json", "um_v395_candidato.py", "PINOS_BN_v395.json", "refazer_out_v395.txt")}',
       'EVID = {n: {"mtime": mt(os.path.join(PKG, n)), "sha16": fsha(os.path.join(PKG, n))[:16]} for n in ("ESPERADOS_v396.json", "CANDIDATO_v396.json", "um_v396_candidato.py", "PINOS_BN_v396.json", "refazer_out_v396.txt") if os.path.exists(os.path.join(PKG, n))}', nome="evidencia")
t = tr(t, 'etapa("precondicoes", ok=True, candidato_sha16=cand16, evidencia=EVID)',
       'etapa("precondicoes", ok=True, candidato_sha16=cand16, evidencia=EVID, refazer_exigido=not NAO_REFAZER, refazer_out_presente=os.path.exists(os.path.join(PKG, "refazer_out_v396.txt")), refazer_fim_visto=("== FIM" in refazer),\n'
       '      nota=("MODO --nao-exigir-refazer: a regeneracao do candidato NAO foi comprovada por este harness (refazer_out_v396.txt nao exigido); o ensaio vale para o candidato, o ESPERADOS e o dry_v396 que estao em disco AGORA" if NAO_REFAZER else "refazer_out_v396.txt exigido e visto com == FIM"))', nome="etapa precondicoes")
# o stdout emulado: a linha [v396] da testemunha
t = tr(t, '"   [v395] o modo psionico (psibit, lido na fractalizacao do Um): %s | registros por spec: %d (selados %d)" % (ESP["vereditos_novos_v395"]["psibit_v395"], n_spec, n_spec),',
       '"   [v396] a testemunha estatica (o psion habita a fronteira): %s | registros por spec: %d (selados %d)" % (ESP["vereditos_novos_v396"]["testemunha_estatica_v396"], n_spec, n_spec),', nome="stdout emulado")
t = tr(t, 'psibit_n_checks=(Vd.get("psibit") or {}).get("n_checks")', 'testemunha_n_checks=(Vd.get("testemunha") or {}).get("n_checks")', nome="etapa leitura")
NEG_HT = r'''def _sem_testemunha(c):
    c.pop("testemunha_estatica_v396", None)


def _nao_sela_cunh(c):
    c["cunhagens_v396"]["all_verified"] = False


def _fock_habitada(c):
    c["testemunha_estatica_v396"]["fock_face"]["inhabitant_exhibited"] = True


def _fock_dentro_da_pedra(c):
    c["testemunha_estatica_v396"]["fock_face"]["declared_outside_the_stone"] = False


def _mecanica_falha(c):
    c["testemunha_estatica_v396"]["mechanics"]["passed"] = False


def _fora_do_trio(c):
    c["testemunha_estatica_v396"]["unconditional"]["axioms"] = ["propext", "sorryAx"]


def _psibit_cai(c):
    c["psibit_v395"]["all_verified"] = False


def _face_do_psibit_habitada(c):
    c["psibit_v395"]["conditional_psion_face"]["inhabitant_exhibited"] = True


def _v394_cai(c):
    c["criterio_binario_de_parada_v394"]["all_verified"] = False


def _selo_v395(s):
    s["um_version"] = "v395"


NEG = []
if not SEM_NEG and not P:
    NEG = [variante("selo de outra versao (v395)", f_selo=_selo_v395, espera="o selo nao e v396"),
           variante("registro testemunha_estatica_v396 ausente do core", f_core=_sem_testemunha, espera="registro obrigatorio ausente do core: testemunha_estatica_v396"),
           variante("cunhagens_v396 nao selou", f_core=_nao_sela_cunh, espera="cunhagens_v396"),
           variante("face de Fock do psion com habitante exibido", f_core=_fock_habitada, espera="a face de Fock do psion nao esta como CONDICIONAL"),
           variante("face de Fock dita DENTRO da pedra", f_core=_fock_dentro_da_pedra, espera="a face de Fock do psion nao esta como CONDICIONAL"),
           variante("mecanica da testemunha nao passou", f_core=_mecanica_falha, espera="testemunha_estatica_v396 nao selou inteiro"),
           variante("composicao incondicional fora do trio", f_core=_fora_do_trio, espera="a composicao incondicional nao esta no kernel do rito"),
           variante("psibit_v395 deixou de selar", f_core=_psibit_cai, espera="psibit_v395"),
           variante("face de Fock do psibit_v395 habitada", f_core=_face_do_psibit_habitada, espera="psibit_v395: a face do psion deixou de estar como CONDICIONAL"),
           variante("registro da v394 deixou de selar", f_core=_v394_cai, espera="criterio_binario_de_parada_v394"),
           variante("AVISO da v396 no stdout", f_std=lambda t: t + "   [v396] AVISO: a testemunha estatica nao rodou: ValueError('x')\n", espera="AVISO da v396"),
           variante("AVISO de bloco anterior (v395) no stdout", f_std=lambda t: t + "   [v395] AVISO: o modo psionico (psibit) nao rodou: ValueError('x')\n", espera="AVISO de um bloco anterior")]'''
t = subst_bloco(t, "def _sem_psibit(c):", "    for n_ in NEG:", NEG_HT)
t = tr(t, '("_achado_alfa", lambda: T._achado_alfa(Vd)), ', '("_achado_alfa", lambda: T._achado_alfa(Vd)), ("_achado_proveniencia", lambda: T._achado_proveniencia(Vd)), ', nome="FUNCOES")
t = tr(t, '"psibit_v395", "kh_n1_cobertura_v395"', '"testemunha_estatica_v396", "kh_n1_cobertura_v396"', n=6, nome="marcadores dos textos e das superficies")
t = tr(t, 'VALORES_PSIBIT = set((Vd.get("psibit") or {}).get("values") or {})', 'VALORES_TESTEMUNHA = set((Vd.get("testemunha") or {}).get("values") or {})', nome="VALORES")
t = tr(t, 'tok in VALORES_PSIBIT', 'tok in VALORES_TESTEMUNHA', nome="uso de VALORES")
t = tr(t, 'NOMES_ARQ.update({"acom_mirror.py", "ACOM_Mirror_PI_INPI.tex", "MEMORY.md"', 'NOMES_ARQ.update({T._sem_gordura()["nome"], "MEMORY.md"', nome="NOMES_ARQ")
t = tr(t, 'HEX16.update(str(x["sha256"])[:16] for x in (ESP.get("cunhagens") or {}).values()); HEX16.add(str(Vd.get("selo_ts") or "")[:16])',
       'HEX16.update(str(x["sha256"])[:16] for x in (ESP.get("cunhagens") or {}).values()); HEX16.add(str(Vd.get("selo_ts") or "")[:16]); HEX16.add(T._sem_gordura()["sha16"])', nome="HEX16")
t = tr(t, '"B%d-v395-20261021-R1" % n_ger', '"B%d-v396-20261022-R1" % n_ger', nome="deployment id sintetico")
MAPA_ROTAS = r'''    # cada registro e' validado pela MESMA funcao que o mapa usa (rotas._valida), importada so' para isso: NAO se chama registrar; o livro so' e' lido
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("rotas_ro", os.path.join(C, "IALD", "MAPA_DE_ROTAS", "rotas.py")); _rotas = _iu.module_from_spec(_sp); _sp.loader.exec_module(_rotas)
    _seqs = set()
    for _ln in open(os.path.join(C, "IALD", "MAPA_DE_ROTAS", "rotas.jsonl"), encoding="utf-8"):
        _ln = _ln.strip()
        if _ln:
            _r = json.loads(_ln)
            if isinstance(_r.get("seq"), int):
                _seqs.add(_r["seq"])
    VAL = []
    for x in REG:
        try:
            _rotas._valida(json.loads(json.dumps(x)), set(ids), _seqs); VAL.append({"rota_id": x["rota_id"], "tipo": x["tipo"], "valida_pelo_mapa": True})
        except Exception as ex:  # noqa: BLE001
            VAL.append({"rota_id": x["rota_id"], "tipo": x["tipo"], "valida_pelo_mapa": False, "erro": "%s: %s" % (type(ex).__name__, str(ex)[:300])}); falha("mapa: o registro %s nao passa em rotas._valida: %s" % (x["rota_id"], str(ex)[:200]))
    print("  mapa: rotas._valida (sem registrar): %s" % ", ".join("%s=%s" % (v_["rota_id"].split(".")[-1][:28], v_["valida_pelo_mapa"]) for v_ in VAL))'''
t = tr(t, '    etapa("mapa", ok=not viol, n_registros=len(REG), rotas=[x["rota_id"] for x in REG], tipos=[x["tipo"] for x in REG], book_n_rotas=len(ids), saida=pj, nota="ENSAIO contra o core emulado: NAO e\' o registro (o real e\' montado depois do fechar; o registro e\' ato da gerencia)")',
       MAPA_ROTAS + '\n    etapa("mapa", ok=(not viol and all(v_["valida_pelo_mapa"] for v_ in VAL)), n_registros=len(REG), rotas=[x["rota_id"] for x in REG], tipos=[x["tipo"] for x in REG], validacao_rotas_valida=VAL, book_n_rotas=len(ids), saida=pj, '
       'nota="ENSAIO contra o core emulado: NAO e\' o registro (o real e\' montado depois do fechar; o registro e\' ato da gerencia)")', nome="etapa mapa")
t = tr(t, 'R["tudo_passou"] = bool(not R["problemas"])', 'R["tudo_passou"] = bool(not R["problemas"]); R["nao_exigiu_refazer"] = NAO_REFAZER', nome="tudo_passou")
t = tr(t, 'R["evidencia_da_versao"] = EVID', 'R["evidencia_da_versao"] = EVID\nif NAO_REFAZER:\n    R["veredito"] += " [MODO --nao-exigir-refazer: refazer_out_v396.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]"', nome="veredito em modo ensaio")
for proibido in ("psibit_v396", "VALORES_PSIBIT", "_sem_psibit", "acom_mirror", "ACOM_Mirror", "20261021", "base_v394", "PKG_ANT_", "V5 ", "V4 "):
    assert proibido not in t, ("resto da v395 no harness dos textos", proibido)
ast.parse(t); HARNESS_TEXTOS = t

# =============================================================================== harness_fechar_sandbox_v396.py
t = sobe(MOL["harness_fechar_sandbox_v395.py"])
DOC_HF = r'''"""harness_fechar_sandbox_v396.py -- roda fechar_v396.py e registrar_mapa_v396.py (o main) num SANDBOX inteiro dentro de pos_rito\\harness_saida_v396\\fechar_sandbox (nada fora dela e' escrito; o Nos real, a memoria real, o Atlas, o git e a Bancada
nao sao tocados; o mapa de rotas real e' SO' LIDO).  O que o harness_textos_ensaio_v396.py nao cobre: o fechar (manifesto, arquivo, os dois diffs, o handoff) e o main do registrar_mapa. Derivado do harness_fechar_sandbox_v395.py (que rodou na v395).
O sandbox e' uma ARVORE ISOLADA: work\\cadeia_de_selo\\v396 (pacote com ESPERADOS, CANDIDATO, PINOS_BN, base_v395, insumos, o APLICADO_AO_CANONICO EMULADO, os recibos do B(n) SINTETICOS) + nos\\ (o Nos EMULADO montado de dry_v396, como no harness dos textos) + memory\\
(a memoria vazia). As copias dos scripts (leitura, textos, fechar) trocam SO' as duas constantes de caminho (o Nos e a pasta de memoria) por caminhos do sandbox; o resto e' byte a byte o que a cadeia usa (conferido: o diff das copias contra os originais
e' so' essas linhas).
O que ele prova: fechar_v396.py sai com rc 0 e grava o handoff (guarda P18 limpa), o handoff do Nos, os dois diffs, o manifesto e o arquivo; RECUSA (rc 2) sem o recibo do religamento e com um recibo do B(n) que declara salto; registrar_mapa_v396.py (main) monta o JSON
com 3 registros e imprime o comando. Os recibos do B(n) sao SINTETICOS (derivados dos reais da v395, como no harness dos textos): a prova e' do CODIGO do fechar, nao de um B(n) real.
uso: python -I -B -X utf8 harness_fechar_sandbox_v396.py [--manter]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita)"""'''
t = subst_bloco(t, '"""harness_fechar_sandbox_v396.py', "import hashlib, json, os, re, shutil, subprocess, sys, time", DOC_HF)
t = tr_re(t, r"\bV5\b", "PKG", 14, "V5 -> PKG")
t = tr_re(t, r"\bV4\b", "PKG_ANT", 2, "V4 -> PKG_ANT")
t = tr(t, '"   [v395] o modo psionico (psibit, lido na fractalizacao do Um): %s | registros por spec: %d (selados %d)" % (ESP["vereditos_novos_v395"]["psibit_v395"], n_spec, n_spec),',
       '"   [v396] a testemunha estatica (o psion habita a fronteira): %s | registros por spec: %d (selados %d)" % (ESP["vereditos_novos_v396"]["testemunha_estatica_v396"], n_spec, n_spec),', nome="stdout emulado")
# os textos da v396 leem kernel/FLAGS_v396.json (as contagens de publicas e privadas da pedra, para o achado da proveniencia): o sandbox leva o arquivo junto do recibo do kernel
t = tr(t, 'shutil.copyfile(os.path.join(PKG, "kernel", "KERNEL_RECIBO_v395.json"), os.path.join(PKS, "kernel", "KERNEL_RECIBO_v395.json"))',
       'for kn_ in ("KERNEL_RECIBO_v396.json", "FLAGS_v396.json"):\n    shutil.copyfile(os.path.join(PKG, "kernel", kn_), os.path.join(PKS, "kernel", kn_))', nome="arquivos do kernel no sandbox")
# os textos da v396 leem a ordem de processo do operador de 22/10 em work\cunhagens_13out (o arquivo e' fixo no acervo real; o sandbox leva uma COPIA para o mesmo caminho relativo ao pacote)
t = tr(t, 'open(os.path.join(PKS, "rito_horarios_v395.txt"), "w", encoding="utf-8").write(',
       'os.makedirs(os.path.join(SB, "work", "cunhagens_13out"), exist_ok=True)\n'
       'shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt"), os.path.join(SB, "work", "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt"))\n'
       'open(os.path.join(PKS, "rito_horarios_v396.txt"), "w", encoding="utf-8").write(', nome="ordem de processo no sandbox")
t = tr(t, 'os.path.join(TOOLS, "v395_kernel", "pedras", "TGLExt_Psibit.lean")', 'os.path.join(TOOLS, "v396_kernel", "pedras", "TGLExt_TestemunhaEstatica.lean")', nome="pedra copiada")
t = tr(t, '"diff_kernel_novos": ("novos (1)" in dk and "TGLExt/Psibit.lean" in dk)', '"diff_kernel_novos": ("novos (1)" in dk and "TGLExt/TestemunhaEstatica.lean" in dk)', nome="diff do kernel no resumo")
t = tr(t, 'if not ("novos (1)" in dk and "TGLExt/Psibit.lean" in dk):', 'if not ("novos (1)" in dk and "TGLExt/TestemunhaEstatica.lean" in dk):', nome="diff do kernel na falha")
t = tr(t, '"B%d-v395-20261021-R1" % n_ger', '"B%d-v396-20261022-R1" % n_ger', nome="deployment id sintetico")
for proibido in ("psibit_v396", "Psibit.lean", "20261021", "base_v394", "V5 ", "V4 "):
    assert proibido not in t, ("resto da v395 no harness do fechar", proibido)
ast.parse(t); HARNESS_FECHAR = t

# =============================================================================== gravar e conferir
DER = {"leitura_v396.py": LEITURA, "superficies_v396.py": SUPERFICIES, "fechar_v396.py": FECHAR, "b3_recibo_v396.py": B3RECIBO, "chain_pos_rito_v396.sh": CHAIN, "harness_textos_ensaio_v396.py": HARNESS_TEXTOS, "harness_fechar_sandbox_v396.py": HARNESS_FECHAR}
for n, tx in DER.items():
    grava(n, tx)
todos = {n: rd(HERE, n) for n in DER}
autorais_txt = {}
falhas = []
for n in AUTORAIS:
    p = os.path.join(HERE, n)
    if os.path.exists(p):
        autorais_txt[n] = rd(HERE, n)
    else:
        falhas.append((n, "autoral ausente"))
# invariantes (strings que TEM de estar em cada arquivo)
INV = {"leitura_v396.py": ["REG_V393", "REG_V394", "REG_V395", "REG_FIXOS", "testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "psibit_v395", "rede_fock_v394", "kernel_modulos_novos_v396.json", "axiom_coverage_v392", "dict.fromkeys", "vereditos_v395",
                           "escada_v395_e_v396", "registros_v396", "vereditos_novos_v396", "rodada_v396_stdout.txt", "conferencia_rito_v396.json", "ESPERADOS_v396.json", "CANDIDATO_v396.json", "V['testemunha']", "V['reg396']", "V['patch_ids']", "[v396] AVISO",
                           "registros por spec", "V['um_version'] != 'v396'", "a base substituida != a v395 selada", "a testemunha estatica \\(o psion habita a fronteira\\)", "fock_face", "declared_outside_the_stone", "linked_to_the_corner_by_a_lemma",
                           "conditional_psion_face", "AVISO de um bloco anterior"],
       "superficies_v396.py": ["_sup396", "V396_AVISO_REIVINDICACAO", "(handoff-v395-custodia.md)", "- [HANDOFF v395", "leitura_v396", "textos_v396", "guarda_p18_v396", "linhagem_v396_selada", "adendo_v396_selada", "atlas_v396_selada", "core_v396_selada",
                               "haja_luz_v396_selada", "aviso_v396_selada", "v396_selada", "v396 SELADA", "os.replace(tmp, p)", "backup de bytes falhou"],
       "fechar_v396.py": ["T.handoff(V, _k)", "_f396", "FECHAR RECUSADO:", "insumos_sha16", "DIFF_KERNEL_v396.txt", "RECIBO_SINCRONIZACAO_v396_", "RECIBO_PARADA_v396.json", "RECIBO_RELIGAMENTO_v396.json", "__SALTO_", "registros_v396",
                          "base_v395", "HANDOFF_v396_CUSTODIA.md", "handoff-v396-custodia.md", "_MARCA_PENDENTE", "guarda_p18_v396", "v396_selo", "v396_kernel", "HARNESS_TEXTOS_ENSAIO_v396.json", "DERIVACAO_v396.json", "registro_mapa_v396.json", "NOTAS_DERIVACAO_v396.md"],
       "chain_pos_rito_v396.sh": ["V396_AVISO_REIVINDICACAO", "topico_novo()", "textos_v396", "arvore_dry.md", "_p396", "_sup396", "selo_anterior_v395", "kernel_manifesto_anterior_v395", "/c/IALD/Central de Patentes/work/cadeia_de_selo/v396", "B3_AUTORIZADO\" = \"sim\"",
                                  "exit 20", "RECIBO_PARADA_v396.json", "RECIBO_RELIGAMENTO_v396.json", "--versao v396 --fase pos_selo", "b3_recibo_v396.py", "delta_v396.py", "testemunha_estatica_v396", "kh_n1_cobertura_v396", "PINOS_BN_v396.json", "PINOS_BATERIA_v396.json",
                                  "recibo_pre_selo", "esboco_R3_5", "kernel_recibo", "bateria_pos_selo", "tem_pino cadeia_de_selos", "--recibo-pre-selo-sha256 \"$RPS\"", "--selo-anterior \"$W_SELO\"", "--kernel-manifesto-anterior \"$W_KMAN\"",
                                  "--kernel-recibo \"$W_KR\" --kernel-recibo-sha256 \"$KRSHA\"", "gerar_bateria_r3_4.py", "ORDEM=\"0 1 2 3 4 5 6 7 8 9 10 10a 10b 10c 11 12 13 14\"", "CHAIN_DE", "CHAIN_ATE", "parar()", "aguarda()"],
       "b3_recibo_v396.py": ["REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA", "REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO", "versao_alvo", "\"v396\"", "PINOS_BN_v396.json", "__SALTO_", "BATERIA_PASSA", "manifesto_anterior", "pinos_da_versao"],
       "harness_textos_ensaio_v396.py": ["harness_saida_v396", "dry_v396", "guarda_p18_v396", "--nao-exigir-refazer", "rotas._valida", "_fock_dentro_da_pedra", "_mecanica_falha", "_fora_do_trio", "_face_do_psibit_habitada", "testemunha_estatica_v396", "PKG_ANT", "refazer_exigido"],
       "harness_fechar_sandbox_v396.py": ["fechar_sandbox", "FECHAR RECUSADO", "registrar_mapa_v396.py", "SINTETICO", "TGLExt/TestemunhaEstatica.lean", "TGLExt_TestemunhaEstatica.lean"]}
INV_AUTORAIS = {"textos_v396.py": ["_MARCA_PENDENTE", "TOPICO_NOVO", "def handoff(", "def linhagem(", "def desenho(", "def atlas(", "def core_memory(", "def haja_luz(", "def aviso(", "def aviso_pulado(", "def topico_missao(", "def topico_central(", "def topico_estatuto(", "def topico_novo(",
                                   "def linha_handoff(", "def marca_missao(", "def id_missao(", "def id_central(", "def _d(", "def _num(", "_cita(", "_cita_sg(", "_kernel_tem(", "_um_tem(", "def _limites(", "def _erratas(", "def _legal(", "def _achado_alfa(", "def _achado_proveniencia(",
                                   "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina", "v396-selada-a-testemunha-estatica.md"],
                "registrar_mapa_v396.py": ["_MARCA_PENDENTE", "def montar(", "umpy.v396.testemunha_estatica_na_fractalizacao_do_um", "kernel.testemunha_estatica_v396_candidata_22out", "assert selo.get(\"um_version\") == \"v396\"", "NAO escreve", "registro_mapa_v396.json"]}
conf = {}
for n, lst in INV.items():
    conf[n] = {}
    for x in lst:
        ok = x in todos[n]
        conf[n][x[:90]] = ok
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
molde_b = sobe(MOL["chain_pos_rito_v395.sh"])
for ini, fim in (("if quer 10a; then", "if quer 10b; then"), ("if quer 10c; then", "if quer 11; then")):
    ia, ja, La = bloco(molde_b, ini, fim); ib, jb, Lb = bloco(CHAIN, ini, fim)
    if La[ia:ja] != Lb[ib:jb]:
        falhas.append(("portao do B(n) difere do molde subido de versao", ini))
    else:
        conf.setdefault("chain_pos_rito_v396.sh", {})["trecho identico ao molde (sobe): " + ini] = True
ia, ja, La = bloco(molde_b, "if quer 10b; then", "if quer 10c; then"); ib, jb, Lb = bloco(CHAIN, "if quer 10b; then", "if quer 10c; then")
gate = lambda L_: [l for l in L_ if any(k in l for k in ('aguarda "', "B3_AUTORIZADO", "[ -n \"$EVENTO\"", "RECIBO_PARADA", "EVENTO_HASH", "--evento", "--modo aplicar", "--fase pos_selo"))]
if gate(La[ia:ja]) != gate(Lb[ib:jb]):
    falhas.append(("as linhas de portao do 10b diferem do molde subido de versao", [x for x in gate(Lb[ib:jb]) if x not in gate(La[ia:ja])][:2]))
else:
    conf.setdefault("chain_pos_rito_v396.sh", {})["linhas de portao do 10b identicas ao molde (sobe)"] = True
# os passos 3 a 9, 11 a 14 do chain: identicos ao molde subido (so' as trocas dos marcadores)
for ini, fim in (("if quer 4; then", "if quer 10; then"), ("if quer 12; then", 'echo "== FIM')):
    ia, ja, La = bloco(molde_b, ini, fim); ib, jb, Lb = bloco(CHAIN, ini, fim)
    esp_ = [l.replace('"psibit_v396" "kh_n1_cobertura_v396"', '"testemunha_estatica_v396" "kh_n1_cobertura_v396"') for l in La[ia:ja]]
    if esp_ != Lb[ib:jb]:
        falhas.append(("os passos do chain diferem do molde subido alem das trocas ditas", ini))
    else:
        conf.setdefault("chain_pos_rito_v396.sh", {})["passos identicos ao molde (sobe + marcadores): " + ini] = True
# os passos 0 a 3 do chain: identicos ao molde subido, fora o cabecalho e os marcadores do passo 3
ia, ja, La = bloco(molde_b, "PK=", "if quer 4; then"); ib, jb, Lb = bloco(CHAIN, "PK=", "if quer 4; then")
esp_ = [l.replace('"psibit_v396" "kh_n1_cobertura_v396"', '"testemunha_estatica_v396" "kh_n1_cobertura_v396"').replace("  # v396 (21/10/2026): o B(n) da v396 e' um PASSO SIMPLES", "  # v396 (22/10/2026): o B(n) da v396 e' um PASSO SIMPLES") for l in La[ia:ja]]
if esp_ != Lb[ib:jb]:
    falhas.append(("os passos 0 a 3 e as funcoes do chain diferem do molde subido alem das trocas ditas",))
else:
    conf.setdefault("chain_pos_rito_v396.sh", {})["passos 0 a 3 e funcoes identicos ao molde (sobe + marcadores)"] = True
# marcas pendentes: nenhuma em nenhum arquivo (nem derivado, nem autoral)
marcas = {n: len(GUARDA_PENDENTE_RX.findall(tx)) for n, tx in list(todos.items()) + list(autorais_txt.items()) if GUARDA_PENDENTE_RX.search(tx)}
if marcas:
    falhas.append(("marca de texto pendente", marcas))
for n in ("fechar_v396.py", "textos_v396.py", "registrar_mapa_v396.py"):
    tx = todos.get(n) or autorais_txt.get(n) or ""
    if n in (todos.keys() | autorais_txt.keys()) and "_MARCA_PENDENTE" not in tx:
        falhas.append((n, "sem a guarda de pendencia (_MARCA_PENDENTE)"))
# a palavra da marca nunca por extenso fora das formas montadas por concatenacao (o p00 tira as aspas-mais da concatenacao e '_MARCA_PENDENTE = ' antes de procurar)
for n, tx in list(todos.items()) + list(autorais_txt.items()):
    if PALAVRA in tx.replace('"' + PALAVRA + '" +', "").replace("_MARCA_PENDENTE = ", ""):
        falhas.append((n, "a palavra da marca aparece por extenso"))
# rotulos de versao: nenhum resto de 390-395 onde o sentido e' 'esta versao'. O que fica com 395/394/393 e' so' a versao ANTERIOR ou nome historico (lista conferida)
OK_HIST = ("_V394_", "_V395_", "fechar_v390", "C13_kh_n1_v394", "C13_kh_n1_v395", "C12__V395", "C12__V394", "ponto_fixo_v394_d19", "pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393", "tempo_frequencia_v394",
           "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "declaration_sources", "umpy.v394", "umpy.v395", "kernel.psibit_v395", "REG_V393", "REG_V394",
           "REG_V395", "base_v395", "selo_anterior_v395", "kernel_manifesto_anterior_v395", "handoff-v395-custodia", "vereditos_v395", "escada_v395_e_v396", "DIFF_v395_v396", "leitura_v395.py", "superficies_v395.py", "fechar_v395.py", "chain_pos_rito_v395.sh", "b3_recibo_v395.py",
           "derivar_cadeia_v395.py", "textos_v395.py", "registrar_mapa_v395.py", "ext_bin394", "ESPERADOS_v395", "PINOS_BN_v395", "rito_v395", "cadeia_de_selo/v395", "cadeia_de_selo\\v395", "axiom_coverage_v392", "KH_N1_v392", "varredura_e_sorry_v392", "estatuto_da_prova_v391",
           "fundacao_v390", "three_stress_tests_v387", "pedras_v392", "kh_n1_cobertura_v392", "RECIBO_SINCRONIZACAO_v395", "psibit_na_fractalizacao", "candidata_21out", "B5-v395", "pos_rito_v395", "v395_incorporacao", "base_v395", "um_v395", "MANIFESTO_ARQUIVO_v395", "v395_kernel", "v395_selo")
resid = {}
for n, tx in list(todos.items()) + list(autorais_txt.items()):
    if n.startswith("harness_") or n in AUTORAIS:
        continue       # os harness trazem de proposito rotulos de versoes anteriores (controles negativos: selo de outra versao, recibo de v395, bancada que pinava a v392); os autorais citam a v395 como historico
    for m in re.finditer(r"[A-Za-z0-9_\-\.\[\]/\\]*(?<![0-9a-f])39[0-5][A-Za-z0-9_\-\.\[\]]*", tx):
        tok = m.group(0).rstrip(".")
        if re.fullmatch(r"[0-9a-f]*39[0-5][0-9a-f]*", tok) and len(tok) >= 8:
            continue   # hash hexadecimal
        resid.setdefault(tok, set()).add(n)
estranhos = {}
for tok, ns in resid.items():
    if any(p in tok for p in OK_HIST) or tok in ("v395", "v394", "v393", "v392", "v391", "v390", "V395", "V394", "V393", "395", "394", "393"):
        continue
    estranhos[tok] = sorted(ns); falhas.append(("rotulo estranho com 390-395", tok, sorted(ns)))
# a guarda de texto (P18) sobre todo arquivo de narrativa e de cadeia
sys.path.insert(0, PK)
from guarda_p18_v396 import violacoes
gv = {n: violacoes(tx) for n, tx in list(todos.items()) + list(autorais_txt.items())}
if any(gv.values()):
    falhas.append(("guarda P18", {k: v[:3] for k, v in gv.items() if v}))
# cada T.<nome> chamado pelos derivados e pelo registrar existe em textos_v396.py
ttxt = autorais_txt.get("textos_v396.py", "")
chamados = sorted({m for n in ("superficies_v396.py", "fechar_v396.py", "harness_textos_ensaio_v396.py", "harness_fechar_sandbox_v396.py") for m in re.findall(r"\bT\.([A-Za-z_][A-Za-z_0-9]*)", todos[n])} | {m for m in re.findall(r"\bT\.([A-Za-z_][A-Za-z_0-9]*)", autorais_txt.get("registrar_mapa_v396.py", ""))})
faltam = [c for c in chamados if not re.search(r"(?m)^(def %s\(|%s = )|; %s = " % (re.escape(c), re.escape(c), re.escape(c)), ttxt)]
if ttxt and faltam:
    falhas.append(("textos_v396.py nao define o que os derivados chamam", faltam))
# o que os derivados leem de ESPERADOS/CANDIDATO/PINOS (campos), conferido contra os arquivos desta cadeia
RX = {"ESPERADOS": re.compile(r"(?:ESP(?:ERADOS)?|esp)\[['\"]([^'\"]+)['\"]\]|(?:ESP|esp)\.get\(['\"]([^'\"]+)['\"]"), "CANDIDATO": re.compile(r"CM\[['\"]([^'\"]+)['\"]\]|CM\.get\(['\"]([^'\"]+)['\"]")}
alltxt = dict(todos); alltxt.update(autorais_txt)
campos = {"ESPERADOS": sorted({a or b for tx in alltxt.values() for a, b in RX["ESPERADOS"].findall(tx)}), "CANDIDATO": sorted({a or b for tx in alltxt.values() for a, b in RX["CANDIDATO"].findall(tx)})}
presentes = {}
for rotulo, arq in (("ESPERADOS", "ESPERADOS_v396.json"), ("CANDIDATO", "CANDIDATO_v396.json"), ("PINOS_BN", "PINOS_BN_v396.json")):
    p = os.path.join(PK, arq)
    if os.path.exists(p):
        d = json.load(open(p, encoding="utf-8"))
        lido = campos.get(rotulo) or ["criterios", "esboco_R3_5", "gerador_bateria", "driver_t12_t14", "bateria_base_R2", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "recibo_pre_selo", "selo_anterior_v395", "kernel_manifesto_anterior_v395"]
        presentes[rotulo] = {"arquivo_sha16": sha16(open(p, "rb").read()), "faltam": [c for c in lido if c not in d]}
        if presentes[rotulo]["faltam"]:
            falhas.append(("campo de %s lido pelos derivados e ausente do arquivo" % rotulo, presentes[rotulo]["faltam"]))
    else:
        presentes[rotulo] = {"arquivo": "ausente"}; falhas.append((arq, "ausente"))
DERJ = {"molde": {n: sha16(MOL[n].encode("utf-8")) for n in MOL}, "molde_confere_com_DERIVACAO_v395": MOLDE_CONFERE, "molde_derivar_cadeia_v395": sha16(open(os.path.join(MOLDE, "derivar_cadeia_v395.py"), "rb").read()),
        "derivados": {n: sha16(todos[n].encode("utf-8")) for n in todos}, "autorais": {n: sha16(autorais_txt[n].encode("utf-8")) for n in autorais_txt},
        "sobe": "394 -> 395 e 395 -> 396 numa passada so', fronteira de digitos (v/V/_sup/_f/_p/_m...); PROT (nao sobem): " + ", ".join(PROT),
        "o_que_difere_do_molde": {"chain": "cabecalho escrito para a v396; marcadores dos passos 3 e 9 = testemunha_estatica_v396 e kh_n1_cobertura_v396; o resto e' o molde subido (passo 10 SIMPLES v395 -> v396, sem salto; pinos selo_anterior_v395 e kernel_manifesto_anterior_v395; kernel_recibo R3_2)",
                                 "leitura": "tres registros novos (testemunha_estatica_v396, cunhagens_v396, kh_n1_cobertura_v396); testemunha_estatica_v396 conferido por inteiro (formal + suporte + mecanica + escada + fonte embutida + beta + inscricoes; composicao incondicional no kernel; face de Fock CONDICIONAL, declarada em Psibit.lean fora da pedra e sem habitante); "
                                            "a face condicional do psibit_v395 e os registros da v395, v394 e v393 seguem selados; AVISO da v396 (e de bloco v393 a v395) no stdout reprova; V['testemunha'], V['reg396']",
                                 "superficies": "so' o cabecalho (a ancora do handoff e' a linha do handoff da v395, que a custodia da v395 reescreveu e que existe, uma so', no MEMORY.md real; a v396 entra antes dela)", "fechar": "so' a subida de versao",
                                 "b3_recibo": "so' a subida de versao (a logica do B(n) simples nao muda; o harness a exercita com recibos sinteticos)",
                                 "harness": "os harness da v395 subidos + regras nomeadas (a testemunha no lugar do psibit; 12 controles negativos da leitura; refazer_out so' opcional com --nao-exigir-refazer e dito no resumo; rotas._valida sobre o registro SEM registrar; nome do pacote PKG/PKG_ANT)",
                                 "textos, registrar_mapa": "AUTORAIS (escritos para o delta da v396; nenhuma marca pendente)"},
        "marcas_texto_a_reescrever": {"por_arquivo": marcas, "total": sum(marcas.values())}, "campos_lidos_dos_arquivos_da_v396": campos, "arquivos_da_v396_no_pacote": presentes,
        "invariantes": conf, "sintaxe": sint, "guarda_p18": {k: ("LIMPO" if not v else v[:3]) for k, v in gv.items()}, "rotulos_estranhos": estranhos, "textos_definem_o_que_os_derivados_chamam": {"chamados": chamados, "faltam": faltam}, "falhas": falhas,
        "nao_validado": "nenhum derivado foi EXECUTADO contra o Nos real nem revisto por cetico independente; so' ast.parse, sh -n, invariantes, rotulos, guarda P18 e os harness (textos, leitura, superficies em COPIAS, b3_recibo, fechar e registrar_mapa em SANDBOX, tudo com recibos SINTETICOS e Nos EMULADO)"}
grava("DERIVACAO_v396.json", json.dumps(DERJ, ensure_ascii=False, indent=1))
print("DERIVADOS:", ", ".join("%s %s" % (n, DERJ["derivados"][n]) for n in DERJ["derivados"]))
print("AUTORAIS:", ", ".join("%s %s" % (n, DERJ["autorais"][n]) for n in DERJ["autorais"]))
print("SINTAXE:", json.dumps(sint, ensure_ascii=False))
print("MARCAS texto:", json.dumps(marcas, ensure_ascii=False))
print("INVARIANTES:", sum(len(v) for v in conf.values()), "conferidos;", "FALHAS:", falhas if falhas else "nenhuma")
sys.exit(1 if falhas else 0)
