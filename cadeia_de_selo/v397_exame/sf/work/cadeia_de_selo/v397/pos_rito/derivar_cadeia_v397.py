# -*- coding: utf-8 -*-
"""derivar_cadeia_v397.py -- DERIVA a cadeia pos-rito da v397 a partir do molde REAL e FINAL da v396 (cadeia_de_selo/v396/pos_rito, o que RODOU de verdade em 22/10; seus arquivos conferem com a DERIVACAO_v396.json por sha16)
(molde do derivador: derivar_cadeia_v396.py). A subida de versao e' UMA passada com fronteira de digitos (395 -> 396 e 396 -> 397: v/V/_sup/_f/_p/_m/k...), com a lista PROT dos nomes historicos que NAO sobem (registros e chaves do core
nascidos em v393, v394, v395 e v396: psibit_v395, cunhagens_v395, kh_n1_cobertura_v395, testemunha_estatica_v396, cunhagens_v396, kh_n1_cobertura_v396, as rotas e as chaves historicas); os registros NOVOS da v397
(teste_de_veracidade_fase9_v397, cunhagens_v397, kh_n1_cobertura_v397) entram por regras NOMEADAS com contagem exata: o que sobrar dos nomes novos como se fossem velhos o derivador RECUSA (assert).
GERA (subida + regras com contagem exata; o script ABORTA se uma regra nao casar o numero esperado de vezes):
  chain_pos_rito_v397.sh, leitura_v397.py, superficies_v397.py, fechar_v397.py, b3_recibo_v397.py (a logica do B(n) simples nao muda: so' a subida),
  harness_textos_ensaio_v397.py, harness_fechar_sandbox_v397.py (os harness da v396 subidos + regras: o registro de veracidade no lugar da testemunha, os controles negativos novos, o paragrafo do README/site e a regra do 4,44,
  o ensaio do MEMORY.md em tres cenarios -- real, com folga, e no limite -- porque a superficie NAO compacta nada).
CONFERE (autorais, escritos para a v397; a logica muda e uma derivacao mecanica nao a cobriria): textos_v397.py, registrar_mapa_v397.py (ast.parse, invariantes por texto, guarda P18, nenhuma marca pendente, e cada nome T.<x>
chamado pelos derivados existe em textos_v397.py).
NAO executa nenhum script derivado: so' ast.parse, sh -n, invariantes, rotulos e a guarda de texto P18. Nao toca o Nos, a Bancada, a memoria, o Atlas, o mapa, o quadro, o tunel, o site nem o git.
GRAVA: DERIVACAO_v397.json (sha16 do molde, de cada derivado e de cada autoral; o molde confere com a DERIVACAO_v396; invariantes; sintaxe; marcas; rotulos; o que difere do molde). Reexecutavel: o que muda ganha .bak_<STAMP>_c1 (backup de BYTES).
Uso: python -I -B -X utf8 derivar_cadeia_v397.py"""
import ast, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)
MOLDE = os.path.join(os.path.dirname(PK), "v396", "pos_rito")
STAMP = time.strftime("%Y%m%d_%H%M%S")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
PALAVRA = "TEXTO_A_" + "REESCREVER"          # a palavra da marca, montada por concatenacao: este arquivo nunca a traz por extenso
MARCA = PALAVRA + "_V397"
# nomes que NAO sobem de versao: registros e chaves historicos do core (nascidos em v393 a v396), arquivos e rotas de versoes passadas
PROT = ["pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394",
        "criterio_binario_de_parada_v394", "declaration_sources_status_v394", "declaration_sources_v394", "umpy.v394.fock_tempo_e_cunhagens", "ext_bin394", "ponto_fixo_v394_d19", "C13_kh_n1_v394",
        "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "REG_V395", "umpy.v395", "kernel.psibit_v395", "psibit_na_fractalizacao", "_V395_PSIBIT_CONTRACT", "C13_kh_n1_v395", "ext_psb395",
        "testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396", "REG_V396", "umpy.v396", "kernel.testemunha_estatica_v396", "_V396_TESTEMUNHA_CONTRACT", "C13_kh_n1_v396", "ext_tes396"]
MODELOS = ("leitura_v396.py", "superficies_v396.py", "fechar_v396.py", "chain_pos_rito_v396.sh", "b3_recibo_v396.py", "harness_textos_ensaio_v396.py", "harness_fechar_sandbox_v396.py")
AUTORAIS = ("textos_v397.py", "registrar_mapa_v397.py")
GUARDA_PENDENTE_RX = re.compile(r"(?m)^\s*#\s*" + MARCA)
RX_V = re.compile(r"(?<![0-9])39([56])(?![0-9])")        # fronteira de digitos: nao toca 3945, 13960, 0.396...
RX_HEXWORD = re.compile(r"[0-9A-Za-z_]*(?<![0-9])39[56](?![0-9])[0-9A-Za-z_]*")


def sobe(t):
    """subida de versao em UMA passada (395 -> 396, 396 -> 397), com os nomes historicos de PROT intactos."""
    for i, p in enumerate(PROT):
        t = t.replace(p, "@@P%d@@" % i)
    t = RX_V.sub(lambda m: "39" + str(int(m.group(1)) + 1), t)
    for i, p in enumerate(PROT):
        t = t.replace("@@P%d@@" % i, p)
    return t


def sem_hex(t, nome):
    """nenhuma ocorrencia de 395/396 dentro de uma palavra HEXADECIMAL (um hash seria subido por engano)."""
    for m in RX_HEXWORD.finditer(t):
        w = m.group(0)
        assert not (re.fullmatch(r"[0-9a-f]{8,}", w)), ("a subida tocaria um hash hexadecimal", nome, w)


def rd(d, n):
    return open(os.path.join(d, n), "rb").read().decode("utf-8")


def tr(t, old, new, n=1, nome=""):
    """troca sobe(old) por `new` (texto FINAL, nunca subido), exigindo exatamente n ocorrencias; `old` e' o texto do MOLDE (v396)."""
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


def insere_antes(t, prefixo, novo):
    """insere `novo` (linhas) imediatamente ANTES da unica linha que comeca por `prefixo`."""
    L = t.split("\n"); a = [k for k, l in enumerate(L) if l.startswith(prefixo)]; assert len(a) == 1, ("insercao: ancora", prefixo, len(a))
    L[a[0]:a[0]] = novo.rstrip("\n").split("\n")
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
# o molde e' o que a DERIVACAO_v396 registrou (os arquivos nao foram editados depois da derivacao; o rito real da v396 os usou como estao)
DER96 = json.load(open(os.path.join(MOLDE, "DERIVACAO_v396.json"), encoding="utf-8"))
reg96 = dict(DER96["derivados"]); reg96.update(DER96["autorais"])
MOLDE_CONFERE = {n: (sha16(MOL[n].encode("utf-8")) == reg96.get(n)) for n in MODELOS}
assert all(MOLDE_CONFERE.values()), ("o molde da v396 difere da DERIVACAO_v396.json (foi editado depois da derivacao?)", MOLDE_CONFERE)

# =============================================================================== leitura_v397.py
t = sobe(MOL["leitura_v396.py"])
i = t.index("import glob, hashlib, json, os, re, sys, datetime")
HEAD_L = ('# -*- coding: utf-8 -*-\n'
          '# A LEITURA da rodada v397 (molde: leitura_v396.py FINAL, o que rodou em 22/10): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v397, que aqui e\' o proprio pacote).\n'
          '# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e\' digitado: tudo sai dos JSON, do core, do selo e do stdout do rito.\n'
          '# v397: os registros NOVOS do core sao teste_de_veracidade_fase9_v397 (runtime: lido NA FASE 9, logo depois do bloco hubble_ratio_opening_v388, AO LADO do V1; o resultado do Teste da Unica Palavra e os tres recibos, por sha256; NENHUM sigma novo)\n'
          '# e cunhagens_v397 e kh_n1_cobertura_v397 (por spec; ESPERADOS[registros_v397]); os da v396 (testemunha_estatica_v396, cunhagens_v396, kh_n1_cobertura_v396), os da v395, os da v394 e os da v393 seguem no core e tem de seguir selados; o modulo\n'
          '# novo de kernel (TGLExt/Token.lean) vem de ESPERADOS[pedras_sha256] e e\' conferido aqui contra o arquivo do kernel do Nos.\n'
          '# A escada vem de ESPERADOS[escada_v396_e_v397] e ESPERADOS[escada]; a troca dita (so numeros) e\' a de ESPERADOS[troca_dita]. O registro teste_de_veracidade_fase9_v397 e\' conferido por inteiro (checagens, numeros lidos == ESPERADOS[veracidade],\n'
          '# fontes por sha256, z_disc abaixo de 5 e poder previo >= 5, o resultado pinado em insumos\\fase9 == ESPERADOS e == o que o registro leu, o quadro selado nas duas linguas); a pedra Token e\' conferida no kernel do rito (bandeira True, trio, modulo da pedra,\n'
          '# suporte); a face de Fock do psion segue CONDICIONAL, declarada em Psibit.lean, fora da pedra e sem habitante; as linhas `[v397]` do stdout do rito dizem o veredito do Teste da Unica Palavra e registros por spec selados == registros por spec;\n'
          '# o AVISO da v397 (e de qualquer bloco v393 a v396) no stdout reprova.\n'
          '# Diferencas para a v396: os registros novos sao DESCOBERTOS por comparacao com ESPERADOS[vereditos_v396]; V[\'veracidade\'], V[\'token\'], V[\'reg397\'] e V[\'patch_ids\'] sao os campos da v397.\n')
t = HEAD_L + t[i:]
t = subst_linha(t, "REG_FIXOS = (", '''REG_V396 = ("testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396")   # da v396: seguem no core e seguem selados (nao sao 'novos' da v397)
REG_FIXOS = ("teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397")   # os tres registros NOVOS do core v397; + os de ESPERADOS[registros_v397] (REG_TODOS, dentro de ler)''')
assert "REG_V393 = (" in t and t.count("REG_V394 = (") == 1 and t.count("REG_V395 = (") == 1 and t.count("REG_V396 = (") == 1
NOVO_STDOUT = r'''    if [l for l in out.splitlines() if '[v397] AVISO' in l]:
        P.append('o stdout traz AVISO da v397 (o registro do Teste da Unica Palavra ou os registros por spec nao rodaram): %s' % [l.strip()[:200] for l in out.splitlines() if '[v397] AVISO' in l][:2])
    elif [l for l in out.splitlines() if re.search(r'\[v39[3-6]\] AVISO', l)]:
        P.append('o stdout traz AVISO de um bloco anterior (v393 a v396): %s' % [l.strip()[:200] for l in out.splitlines() if re.search(r'\[v39[3-6]\] AVISO', l)][:2])
    m_tv = re.search(r'\[v397\] o Teste da Unica Palavra \(Fase 9 V2-c1, aberto uma vez em 23/10\), lido por hash ao lado do V1 \(nenhum sigma novo\): (\S+)', out)
    if not m_tv or m_tv.group(1) != (ESP.get('vereditos_novos_v397') or {}).get('teste_de_veracidade_fase9_v397'):
        P.append('a linha [v397] do Teste da Unica Palavra esta ausente do stdout ou traz um veredito diferente do ensaio a seco (%s)' % (m_tv.group(1)[:80] if m_tv else 'ausente'))
    m_sp = re.search(r'\[v397\] a pedra Token e as quatro falas de 23/10 \(cunhagens_v397\): .*\| registros por spec: (\d+) \(selados (\d+)\)', out)
    if not m_sp or m_sp.group(1) != m_sp.group(2) or int(m_sp.group(1)) != len(ESP.get('registros_v397') or {}):
        P.append('a linha [v397] do stdout nao diz registros por spec selados == %d (%s)' % (len(ESP.get('registros_v397') or {}), m_sp.groups() if m_sp else 'ausente'))'''
t = subst_bloco(t, "    if [l for l in out.splitlines() if '[v397] AVISO' in l]:", "    hp = os.path.join(PK, 'rito_horarios_v397.txt')", NOVO_STDOUT)
NOVO_V397 = r'''    # --- v397: os registros novos conferidos contra o ensaio a seco registrado em ESPERADOS, e os da v396, da v395, da v394 e da v393, que seguem no core e tem de seguir selados; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    for k_ in REG_V393 + REG_V394 + REG_V395 + REG_V396:
        if (core.get(k_) or {}).get('all_verified') is not True:
            P.append('%s (registro da v396, da v395, da v394 ou da v393) deixou de selar' % k_)
    RV_ = dict(ESP.get('vereditos_novos_v397') or {}); RV_.update(ESP.get('registros_v397') or {})   # registro -> veredito do ensaio a seco (teste_de_veracidade_fase9_v397 e' runtime; cunhagens_v397 e kh_n1_cobertura_v397 sao por spec)
    V['reg397'] = {}
    for k_ in REG_FIXOS:
        r_ = core.get(k_) or {}
        V['reg397'][k_] = {'verdict': r_.get('verdict'), 'ok': r_.get('all_verified')}
        esp_v_ = RV_.get(k_)
        if esp_v_ is None:
            P.append('ESPERADOS_v397 nao traz o veredito do ensaio a seco de %s (vereditos_novos_v397 / registros_v397): nao ha com que conferir' % k_)
        elif r_.get('verdict') != esp_v_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k_)
    kf_ = (core.get('kernel_formalization') or {})
    rf_ = core.get('rede_fock_v394') or {}   # limite dito: o contrato conjunto da rede segue NAO habitado (a face de Fock do psion depende dele)
    if rf_.get('whole_certificate_inhabited') is not False:
        P.append('rede_fock_v394: whole_certificate_inhabited deve seguir False (o contrato conjunto da rede segue aberto) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    if kf_.get('ext_bin394_0001') is not True:
        P.append('a bandeira da pedra da v394 (ext_bin394_0001) nao segue True no kernel do rito')
    # a face de Fock do psion segue como a v395 a selou: CONDICIONAL, sem habitante exibido, com a bandeira True e declarada em Psibit.lean (nem a v396 nem a v397 a habitam)
    pb_ = core.get('psibit_v395') or {}; pbc_ = pb_.get('conditional_psion_face') or {}
    if not (pbc_.get('status') == 'CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE' and pbc_.get('inhabitant_exhibited') is False and pbc_.get('flag_true') is True and kf_.get(pbc_.get('flag')) is True and pbc_.get('declared_in') == 'TGLExt/Psibit.lean'):
        P.append('psibit_v395: a face do psion deixou de estar como CONDICIONAL sem habitante exibido (bandeira True, declarada em TGLExt/Psibit.lean)')
    te_ = core.get('testemunha_estatica_v396') or {}; fk_ = te_.get('fock_face') or {}
    if not (fk_.get('status') == 'CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE' and fk_.get('inhabitant_exhibited') is False and fk_.get('declared_outside_the_stone') is True and fk_.get('linked_to_the_corner_by_a_lemma') is False
            and fk_.get('theorem') == ESP.get('fock_face_teorema') and fk_.get('declared_in') == ESP.get('fock_face_declarada_em')):
        P.append('testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL, declarada em Psibit.lean fora da pedra e sem habitante exibido')
    # o registro teste_de_veracidade_fase9_v397, conferido por inteiro (os textos leem os numeros dele; NENHUM sigma e' calculado aqui: so' se compara o que o registro leu com ESPERADOS e com o resultado pinado)
    tv_ = core.get('teste_de_veracidade_fase9_v397') or {}; EV_ = ESP.get('veracidade') or {}
    ck_ = tv_.get('checks') or []; fo_ = {f_.get('chave'): f_ for f_ in (tv_.get('fontes') or []) if isinstance(f_, dict)}
    num_ = EV_.get('numeros_do_resultado') or {}; lido_ = tv_.get('lido') or {}
    nums_ok_ = bool(num_) and all(lido_.get(k_) == v_ for k_, v_ in num_.items())
    fontes_ok_ = bool(EV_.get('fontes')) and all((fo_.get(c_) or {}).get('sha256') == h_ and (fo_.get(c_) or {}).get('ok') is True for c_, h_ in EV_['fontes'].items())
    V['veracidade'] = {'verdict': tv_.get('verdict'), 'ok': tv_.get('all_verified'), 'n_checks': len(ck_), 'checks_ok': bool(ck_) and all(c_.get('ok') is True for c_ in ck_), 'lido': lido_, 'numeros_ok': nums_ok_,
                       'fontes': {c_: str(f_.get('sha256') or '') for c_, f_ in fo_.items()}, 'fontes_ok': fontes_ok_, 'does_not_gate_core': tv_.get('does_not_gate_core')}
    if not (tv_.get('all_verified') is True and tv_.get('does_not_gate_core') is True and len(ck_) == EV_.get('n_checks') and V['veracidade']['checks_ok'] and nums_ok_ and fontes_ok_):
        P.append('teste_de_veracidade_fase9_v397 nao selou inteiro (selo, checagens, numeros lidos == ESPERADOS[veracidade], fontes por sha256): ver o registro no core')
    zd_, pw_ = lido_.get('z_disc_calibrado'), lido_.get('poder_previo')
    if not (isinstance(zd_, float) and zd_ < 5.0 and isinstance(pw_, float) and pw_ >= 5.0):
        P.append('o z_disc calibrado nao esta abaixo de 5 ou o poder previo nao e de 5 sigma ou mais (%r, %r): os textos e o quadro dizem que o degrau de 5 sigma da creditacao nao foi alcancado e que a TGL nao foi falsificada com poder' % (zd_, pw_))
    if PK not in sys.path:
        sys.path.insert(0, PK)
    try:
        import quadro_v397 as QV_
        rp_ = os.path.join(PK, 'insumos', 'fase9', os.path.basename((EV_.get('resultado') or {}).get('duravel') or 'ausente'))
        rb_ = open(rp_, 'rb').read()
        if hashlib.sha256(rb_).hexdigest() != (EV_.get('fontes') or {}).get('f9v2_resultado'):
            P.append('o resultado pinado em insumos\\fase9 != o sha256 de ESPERADOS[veracidade][fontes][f9v2_resultado]')
        else:
            lr_ = QV_.lido_do_resultado(json.loads(rb_.decode('utf-8')))
            if not lr_ or any(lr_.get(k_) != lido_.get(k_) for k_ in lr_):
                P.append('os numeros que o registro leu != os do resultado pinado (lidos pelos mesmos caminhos de delta_v397.F9_CAMINHOS)')
        if QV_.Q._v397_atomos(tv_, 'pt').get('sealed') is not True or QV_.Q._v397_atomos(tv_, 'en').get('sealed') is not True:
            P.append('o quadro do Teste da Unica Palavra nao sela (algum numero ausente ou o registro nao selou): o artigo diria que o registro nao selou')
    except Exception as e_:   # noqa: BLE001
        P.append('nao consegui conferir o registro do Teste da Unica Palavra contra o resultado pinado: %r' % (e_,))
    # a pedra Token no kernel do rito (a conjuncao incondicional de dois termos ja' no kernel) e as quatro falas embutidas
    tk_ = ESP.get('teorema_da_pedra'); fl_ = ESP.get('bandeira_da_pedra'); sup_ = ESP.get('bandeiras_do_suporte') or {}
    ax_ = (kf_.get('axiom_report') or {}).get(tk_)
    cu = core.get('cunhagens_v397') or {}; kh = core.get('kh_n1_cobertura_v397') or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = ESP.get('cunhagens') or {}
    V['token'] = {'theorem': tk_, 'flag': fl_, 'flag_true': kf_.get(fl_) is True, 'axioms': ax_, 'source': (kf_.get('declaration_sources_v394') or {}).get(tk_), 'suporte': sup_,
                  'suporte_true': bool(sup_) and all(kf_.get(b_) is True for b_ in sup_.values()), 'verbatim_ok': bool(ec_) and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_),
                  'checks_ok': bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks')), 'n_checks': len(cu.get('checks') or [])}
    if not (tk_ and fl_ and kf_.get(fl_) is True and isinstance(ax_, list) and set(ax_) <= {'propext', 'Classical.choice', 'Quot.sound'} and (kf_.get('declaration_sources_v394') or {}).get(tk_) == (ESP.get('pedra') or {}).get('path')
            and V['token']['suporte_true'] and cx_.get('teorema') == tk_ and cx_.get('bandeira') == fl_ and cx_.get('suporte') == sup_ and cx_.get('cunhagens_embutidas') == len(ec_) and V['token']['verbatim_ok'] and V['token']['checks_ok']
            and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True):
        P.append('a pedra Token nao esta no kernel do rito como o ensaio a seco a pinou (bandeira True, trio, proveniencia no modulo da pedra, suporte com bandeira True, quatro falas por sha256, checagens de cunhagens_v397)')
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}   # o nome 'axiom_coverage_v392' e' do core (historico); segue na v397
    CB = ESP.get('cobertura_kh_n1') or {}
    V['kh'] = {'decl': cov.get('decl'), 'thm': cov.get('thm'), 'fora': cov.get('fora_do_trio'), 'nao_lidas': cov.get('nao_lidas_pelo_regex'), 'verdict': kh.get('verdict')}
    V['cunh_verdict'] = cu.get('verdict')
    if not (CB and cov.get('ok') is True and cov.get('decl') == CB.get('decl') and cov.get('thm') == CB.get('thm') and cov.get('fora_do_trio') == 0 and cov.get('nao_lidas_pelo_regex') == CB.get('nao_lidas_pelo_regex')):
        P.append('cobertura KH-N1 do rito != ESPERADOS (constantes, teoremas, fora do trio, nao lidas) ou ESPERADOS sem cobertura_kh_n1')
'''
t = subst_bloco(t, "    # --- v397: os tres registros novos conferidos", "    qp = core.get('quantum_pillar_v384')", NOVO_V397)
for proibido in ("AJUSTAR", "V['testemunha']", "V['reg396']", "REG_V397", "reg395", "psibit_v397", "cunhagens_v396_", "ts_.get('values')"):
    assert proibido not in t, ("sobrou na leitura:", proibido)
ast.parse(t); LEITURA = t

# =============================================================================== superficies_v397.py
t = sobe(MOL["superficies_v396.py"])
i = t.index("# Registro da v397 SELADA"); j = t.index("import os, re, sys, time")
CAB = ("# Registro da v397 SELADA nas superficies de memoria (molde: superficies_v396.py FINAL, o que rodou em 22/10), pela regra da linhagem completa.\n"
       "# Diario (MEMORIA_DA_LINHAGEM, append datado), desenho (ADENDO), Atlas (append datado), TGL_CORE_MEMORY (append datado), o CLAUDE.md da Haja_Luz, as memorias-topico (missao, central, estatuto, e o topico NOVO da v397),\n"
       "# o MEMORY.md/MEMORY_2.md, e (so' sob reivindicacao nomeada em V397_AVISO_REIVINDICACAO) o AVISO_GERENCIA.md da ORDEM_019.\n"
       "# SEM erratas inline nesta versao (as erratas da v397 vao DENTRO dos blocos datados). A funcao inserir_ao_lado fica disponivel (nao e' chamada).\n"
       "# Duas fases (plano conferido ANTES da primeira escrita); backup de BYTES (.bak_<STAMP>_sup397); temporario -> conferir tamanho -> substituir; idempotente pelo marcador de cada bloco;\n"
       "# fim de linha de cada arquivo respeitado. GUARDA: so' grava se a leitura nao tiver problema E se a guarda de texto (P18, cinco regras) estiver limpa em todo texto novo.\n"
       "# Ensaio: --copias <pasta com copias dos alvos> (nada real e' tocado). MEMORY.md: ate 24.000 B e 195 linhas. ESTA SUPERFICIE NAO COMPACTA NADA (nem reguas, nem ganchos antigos; ordem da gerencia na v397): o MEMORY.md real tinha 196 linhas em 23/10;\n"
       "# se o indice DEPOIS da edicao (a linha do handoff novo mais a troca do gancho da missao, que movem a velha VERBATIM ao MEMORY_2.md) passar de 195 linhas ou de 24.000 B, RECUSA com rc 3 SEM escrever nada e imprime as contagens (linhas antes,\n"
       "# depois, limite) para a gerencia decidir o que sai do indice. A linha do handoff novo entra ANTES da linha do handoff da v396 (que a custodia da v396 reescreveu: conferida presente no MEMORY.md real em 23/10, uma so').\n")
t = t[:i] + CAB + t[j:]
NOVO_COMPACTA = r'''    # SEM compactacao (ordem da gerencia na v397): esta superficie NAO mexe nas demais linhas do indice (nem reguas, nem ganchos antigos). Se o indice passar do limite, RECUSA abaixo (rc 3), sem escrever nada.'''
t = subst_bloco(t, "    # compactacao: se o indice passar do limite de linhas", "    novo = '\\n'.join(lines).encode('utf-8')", NOVO_COMPACTA)
NOVO_RECUSA = r'''    novo = '\n'.join(lines).encode('utf-8')
    nlin = novo.count(b'\n')
    if len(novo) > LIMITE or nlin > LIMITE_LINHAS:
        print('SUPERFICIES RECUSADAS -- o MEMORY.md ficaria com %d B e %d linhas (limites %d B e %d linhas): nada foi escrito' % (len(novo), nlin, LIMITE, LIMITE_LINHAS))
        print('  CONTAGENS: linhas ANTES %d, linhas DEPOIS %d, limite de linhas %d; bytes ANTES %d, bytes DEPOIS %d, limite de bytes %d.' % (raw.count(b'\n'), nlin, LIMITE_LINHAS, len(raw), len(novo), LIMITE))
        print('  Esta superficie NAO compacta nada (nem reguas, nem ganchos antigos): a gerencia decide o que sai do indice (e a linha movida vai VERBATIM ao MEMORY_2.md) e roda de novo; o passo e idempotente.')
        sys.exit(3)'''
t = subst_bloco(t, "    novo = '\\n'.join(lines).encode('utf-8')", "    nl2 = nl_de(raw2)", NOVO_RECUSA)
assert "sup396" not in t and "V396_AVISO" not in t and "V395" not in t and "(handoff-v396-custodia.md)" in t and "- [HANDOFF v396" in t and "V397_AVISO_REIVINDICACAO" in t and "compacta" in t and "gancho = lambda" not in t and "corridas" not in t
ast.parse(t); SUPERFICIES = t

# =============================================================================== fechar_v397.py
t = sobe(MOL["fechar_v396.py"])
DOC_F = r'''"""fechar_v397.py -- DEPOIS da cadeia pos-rito e do elo B(n) (molde: fechar_v396.py): (1) o manifesto de incorporacao v397 -> pos_rito e a pasta das ferramentas;
(2) o ARQUIVO: o indice por sha256 de tudo o que esta na pasta da cadeia (work\\cadeia_de_selo\\v397 -- aqui o pacote JA mora na casa duravel, nao ha copia do pacote), a copia de
pos_rito -> work\\cadeia_de_selo\\v397_selo e do kernel (work\\cadeia_de_selo\\v397\\kernel e, se existir, work\\v397_kernel; mais as pedras do Nos) -> work\\cadeia_de_selo\\v397_kernel;
(3) os DOIS DIFFS para o auditor independente: DIFF_v396_v397.diff (um.py da base x o selado, GNU diff -U2) e DIFF_KERNEL_v397.txt (o kernel embutido, molde do v390);
(4) o HANDOFF (memory\\handoff-v397-custodia.md + Nos\\HANDOFF_v397_CUSTODIA.md) para a sessao do site, que TRAZ PRONTO PARA COLAR o PARAGRAFO do README do espelho e do site (O Teste da Unica Palavra): gerado pelas MESMAS funcoes
do quadro do artigo (quadro_v397.paragrafo_pronto_readme) sobre o core SELADO do Nos, mesmos numeros e estatutos.
GUARDAS: a leitura sem problema; o PARAGRAFO do README/site passa nas verificacoes do quadro contra o resultado pinado (quadro_v397.confere_md e a regra da ordem: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item; frase do
operador verbatim; numeros iguais aos do resultado) -- se nao passar, o fechar RECUSA (rc 2) ANTES de escrever qualquer coisa e o handoff nao nasce; os tres RECIBOS do B(n) (o RECIBO_SINCRONIZACAO_v397_*.json do 10-bis, o recibo da
PARADA do servico e o do RELIGAMENTO) -- sem eles o fechar RECUSA e o handoff nao nasce; a guarda de texto P18 no handoff.
Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""'''
t = subst_bloco(t, '"""fechar_v397.py', "import glob, hashlib, json, os, shutil, subprocess, sys, time", DOC_F)
t = tr(t, 'V, PROB = L.ler()\nif PROB:\n    print("FECHAR RECUSADO:", PROB); sys.exit(2)\n',
       'V, PROB = L.ler()\nif PROB:\n    print("FECHAR RECUSADO:", PROB); sys.exit(2)\n'
       '# ---------------------------------------------------------------- (0) o PARAGRAFO PRONTO do README do espelho e do site: as MESMAS funcoes do quadro do artigo, sobre o core SELADO do Nos; sem passar nas verificacoes, RECUSA (rc 2) ANTES de escrever qualquer coisa\n'
       'try:\n'
       '    PAR, PAR_INFO = T.paragrafo_readme()\n'
       'except BaseException as e_:   # noqa: BLE001\n'
       '    print("FECHAR RECUSADO: o paragrafo pronto do README e do site (O Teste da Unica Palavra) nao passou nas verificacoes do quadro contra o resultado pinado (regra da ordem do 4,44; frase verbatim; numeros iguais aos do resultado):", repr(e_)[:700]); sys.exit(2)\n',
       1, "paragrafo pronto antes de escrever")
t = tr(t, '"registros_v396": V["registros"], ', '"registros_v397": V["registros"], "readme_paragrafo": {"sha16": hashlib.sha256(PAR.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_INFO}, ', 1, "manifesto: paragrafo")
t = tr(t, '_k = {"ap_nome": ', '_k = {"readme_paragrafo": PAR, "ap_nome": ', 1, "k do handoff")
assert "AO_CLAUDE" not in t and "_dd" not in t and "AJUSTAR" not in t and "_f396" not in t and "rede_fock" not in t.replace("registros_v397", "") and "psibit" not in t.lower() and "T.paragrafo_readme()" in t and "FECHADO v397:" in t
ast.parse(t); FECHAR = t

# =============================================================================== b3_recibo_v397.py (a logica do B(n) simples nao muda: so' a subida; o harness a exercita com recibos SINTETICOS)
t = sobe(MOL["b3_recibo_v396.py"])
assert "v396" in t and "v395" not in t and "PINOS_BN_v397.json" in t and 'r.get("versao_alvo") != "v397"' in t and 'ma.get("version") != "v396"' in t and "B%d-v397-" in t
ast.parse(t); B3RECIBO = t

# =============================================================================== chain_pos_rito_v397.sh
t = sobe(MOL["chain_pos_rito_v396.sh"])
HEADER = r'''#!/bin/sh
# v397 (23/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v396.sh FINAL (o que rodou em 22/10; derivada por derivar_cadeia_v397.py; mesma ordem de passos 0..14 e mesmos portoes). O rito ja terminou (rito_v397.sh em segundo plano;
# RITO_RC=<rc> no fim do Nos\rodada_v397_stdout.txt). A v397 e' um DELTA PEQUENO: 1 modulo novo de kernel (TGLExt/Token, o NOME «token» que o operador deu em 23/10 a pedra da testemunha estatica, que compoe por citacao
# psibit_is_the_mode_of_the_reader e the_psion_inhabits_the_static_witness; 1 bandeira), o registro teste_de_veracidade_fase9_v397 (o resultado do Teste da Unica Palavra, aberto UMA vez em 23/10, lido por sha256 junto dos tres recibos,
# AO LADO do V1; NENHUM sigma novo; nome PROVISORIO), os registros por spec cunhagens_v397 (as quatro falas de 23/10) e kh_n1_cobertura_v397, e o QUADRO «O Teste da Unica Palavra» no topo do artigo PT/EN e do .md canonico (ordem do operador).
# ORDEM: 0 guardas -> 1 o CONFERIDOR (copia byte a byte, com o delta_v397.py, o quadro_v397.py e o runtime_quadro_v397.py que ele importa; so leitura do Nos) -> 2 a LEITURA (PROBLEMAS param) -> 3 ENSAIO das superficies em COPIAS
# (o plano e' conferido antes da primeira escrita; a arvore em dry; o sha16 da v397 na arvore (dry) e os marcadores do passo 9 nas COPIAS, conferidos ANTES de qualquer escrita real; se o MEMORY.md passaria de 195 linhas, a superficie RECUSA
# com rc 3 e a cadeia PARA aqui, sem tocar nada real: a superficie NAO compacta o indice) -> 4 patch arvore/indice (OPCIONAL: so' se existir patch_arvore_indice_v397.py) -> 5 a arvore -> 6 atlas+indice -> 7 superficies reais (appends datados;
# SEM errata nova no CLAUDE.md da raiz) -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e' falha visivel) e a guarda de MEMORY.md (<24.000 B, <=195 linhas) -> 10 B(n) da Bancada,
# ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(n) APLICAR (so com B3_AUTORIZADO=sim e o evento c1) -> 10c religamento (AGUARDA_OPERADOR) -> 11 fechar (o handoff TRAZ o paragrafo do README e do site) -> 12 registrar_mapa
# (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V397_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito).
# PASSO 10 SEM SALTO: a Bancada de producao pina a v396 (B6, B6-v396-20261022-R1) e o Nos e' a v396 ate' a instalacao; portanto o B(n) da v397 e' um passo SIMPLES v396 -> v397 (esboco R3.5, sincronizar_bancada.py): NAO ha a opcao de cadeia de selos
# do esboco, nem o pino correspondente, e o b3_recibo_v397.py NAO tem o 3o argumento. Os pinos vem de PINOS_BN_v397.json (lidos na hora; hash nunca de memoria): criterios, esboco_R3_5, gerador_bateria, driver_t12_t14, bateria_base_R2,
# kernel_recibo (o KERNEL_RECIBO_v397.json, contrato R3_2: a v397 nao acrescenta modulo de auditoria), candidato, esperados, pins_do_candidato, recibo_pre_selo (gerado antes da instalacao; veredito JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA),
# selo_anterior_v396 e kernel_manifesto_anterior_v396 (as copias de bytes do selo e do manifesto do kernel da v396, em base_v396). A BATERIA da v397 e' GERADA por script no 10 (depois do selo; bateria por versao) e pinada ao lado
# (bateria_pos_selo/PINOS_BATERIA_v397.json).
# Vereditos esperados (lidos do codigo do esboco, nao rodados): ensaio REPINADA_B<n>__ENSAIO__NADA_GRAVADO_NA_BANCADA e aplicar REPINADA_B<n>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_, com n = a geracao do manifesto que a
# Bancada pina + 1 (B6 -> n = 7; o b3_recibo_v397.py o confere). A parada do servico (10a) e o religamento (10c) sao ato do operador (V397_AUTORIZACAO_OPERADOR nos scripts bancada_B3_servico\recibo_parada_v397.py e recibo_religamento_v397.py); o chain so' confere os recibos.
# textos_v397.py, fechar_v397.py e registrar_mapa_v397.py RECUSAM rodar se tiverem trecho marcado para reescrever: os passos 0 a 2 nao os usam. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como na v396, com os rotulos da v397.
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).'''
i, j, L = bloco(t, "#!/bin/sh", "PK=")
t = "\n".join([HEADER] + L[j:])
# os marcadores dos passos 3 e 9: os do registro de veracidade e do kh_n1 da v397 (6 ocorrencias: 3 no ensaio das copias, 3 nas superficies reais)
t = tr(t, '"testemunha_estatica_v396" "kh_n1_cobertura_v396"', '"teste_de_veracidade_fase9_v397" "kh_n1_cobertura_v397"', n=6, nome="marcadores dos passos 3 e 9")
# a unica data herdada do molde no corpo do chain (o comentario do b3_prepara): 22/10/2026 -> 23/10/2026
t = tr(t, "  # v396 (22/10/2026): o B(n) da v396 e' um PASSO SIMPLES", "  # v397 (23/10/2026): o B(n) da v397 e' um PASSO SIMPLES", nome="data do comentario do b3_prepara")
# passo 0: o quadro e o runtime do quadro tambem tem de existir (o conferidor os importa)
t = tr(t, '"$PK/delta_v396.py" "$PK/ESPERADOS_v396.json"', '"$PK/delta_v397.py" "$PK/quadro_v397.py" "$PK/runtime_quadro_v397.py" "$PK/ESPERADOS_v397.json"', n=1, nome="passo 0: lista de ferramentas")
# passo 1: o conferidor importa quadro_v397 e runtime_quadro_v397: copia byte a byte, como o delta
t = tr(t, 'cp -p "$PK/delta_v396.py" "$CONFOUT/"; cmp "$PK/delta_v396.py" "$CONFOUT/delta_v396.py" || parar "copia do delta_v396.py (que o conferidor importa) difere"',
       'cp -p "$PK/delta_v397.py" "$CONFOUT/"; cmp "$PK/delta_v397.py" "$CONFOUT/delta_v397.py" || parar "copia do delta_v397.py (que o conferidor importa) difere"\n'
       'for q in quadro_v397.py runtime_quadro_v397.py; do cp -p "$PK/$q" "$CONFOUT/"; cmp "$PK/$q" "$CONFOUT/$q" || parar "copia de $q (que o conferidor importa) difere"; done', n=1, nome="passo 1: copia do quadro")
# passo 3: o ensaio das superficies pode RECUSAR (rc 3) por causa do MEMORY.md; a mensagem diz o que e', e a cadeia para sem tocar nada real
t = tr(t, '[ "$es" = "0" ] || parar "o ENSAIO das superficies falhou (rc=$es) -- nada real foi tocado"',
       'if [ "$es" = "3" ]; then echo "  SUPERFICIES RECUSOU (rc=3): o MEMORY.md passaria do limite (195 linhas ou 24 000 B); a superficie NAO compacta nada; as CONTAGENS estao acima (linhas antes, depois, limite); a gerencia decide o que sai do indice e retoma com CHAIN_DE=3"; fi\n'
       '[ "$es" = "0" ] || parar "o ENSAIO das superficies falhou (rc=$es) -- nada real foi tocado"', n=1, nome="passo 3: rc 3 da superficie")
for proibido in ("--cadeia-de-selos", "W_CAD", "$CAD", "SALTO v392", "R3_4", "fundir_pinos", "psibit_v397", "selo_anterior_v395", "base_v395", "textos_v396", "leitura_v396", "fechar_v396", "PINOS_BN_v396", "testemunha_estatica_v397"):
    assert proibido not in t, ("resto da v396 na cadeia", proibido)
CHAIN = t

# =============================================================================== harness_textos_ensaio_v397.py
t = sobe(MOL["harness_textos_ensaio_v396.py"])
DOC_HT = r'''"""harness_textos_ensaio_v397.py -- o HARNESS DO POS-RITO da v397 em modo ENSAIO (derivado do harness_textos_ensaio_v396.py, que rodou na v396); SO' LEITURA do Nos real, da producao e das superficies reais.
Importa os modulos REAIS textos_v397.py e leitura_v397.py (os que a cadeia usa) e os executa contra um NOS EMULADO montado de dry_v397 (core_ensaio.json -> um_absoluto.json, selo_ensaio.json -> um_absoluto_selo.json, o um.py candidato, o kernel,
o .md, o artigo PT/EN e o sumario; o stdout do rito e o APLICADO_AO_CANONICO sao EMULADOS e ditos). Tudo o que ele escreve fica em pos_rito\\harness_saida_v397\\ (e o resumo HARNESS_TEXTOS_ENSAIO_v397.json ao lado dele); nada do Nos real,
da memoria, do Atlas, do mapa de rotas, da Bancada ou do git e' tocado; nenhum rito e' rodado.
O que ele prova (cada etapa e' uma entrada do resumo):
  precondicoes   o candidato (ESPERADOS == CANDIDATO == arquivo == dry_v397/um.py) e a regeneracao terminada (refazer_out_v397.txt mostra '== FIM'); a evidencia carrega mtime e sha16 de cada entrada;
  conferidor     o conferir_rito_v397.py REAL (copia, com delta_v397, quadro_v397 e runtime_quadro_v397) roda contra o Nos emulado (V397_NOS) e da' TUDO BATE: a conferencia que a leitura le;
  leitura        a leitura_v397.ler() REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS (selo de outra versao, registro ausente, registro nao selado, numero lido adulterado, z_disc acima de 5, checagem que falhou, fonte adulterada,
                 gate movido, bandeira da pedra Token ausente, composicao fora do trio, registros da v396/v395/v394 nao selados, face de Fock habitada ou dita dentro da pedra, AVISO da v397 ou de bloco anterior, linha do Teste da Unica Palavra ausente), cada um tem de reprovar;
  textos         todas as funcoes publicas de textos_v397 renderizam, a guarda P18 fica limpa em cada saida, os marcadores que a cadeia exige estao nos textos, a errata da palavra «teoremas» esta nos textos que carregam _num;
  paragrafo      o PARAGRAFO do README/site (textos_v397.paragrafo_readme) passa nas verificacoes do quadro contra o resultado pinado, e os CONTROLES NEGATIVOS reprovam: o 4,44 sem o p calibrado, o 4,44 sem a linha dos 5 sigma, numero adulterado,
                 p adulterado, a frase do operador parafraseada entre aspas, o 4,44 numa linha fora do item; e a regra da ordem vale para TODO texto renderizado (cada linha com o 4,44 traz o p calibrado, os 5 sigma e o 'nao foi alcancado');
  cita_so_o_que_existe   cada `termo` entre crases de cada texto e' achado no kernel do Nos emulado, no um.py, nos insumos, nos arquivos ou como hash lido (o que nao e' achado e' dito e reprova);
  superficies    superficies_v397.py REAL roda em COPIAS das superficies reais em TRES cenarios: (a) o MEMORY.md real como esta (a superficie NAO compacta: se ele passar de 195 linhas depois da edicao, tem de RECUSAR com rc 3 sem escrever nada; senao, o caminho normal),
                 (b) um MEMORY.md com FOLGA (copia reduzida): o plano e' conferido antes da primeira escrita, idempotente na 2a rodada, marcadores do passo 9, <= 195 linhas e < 24 000 B, (c) um MEMORY.md NO LIMITE (195 linhas): tem de RECUSAR com rc 3, imprimir as
                 contagens e nao escrever nada em nenhuma copia; os originais nao mudam;
  b3_recibo      b3_recibo_v397.py REAL contra recibos SINTETICOS derivados dos recibos reais da v396 (positivos e negativos);
  mapa           registrar_mapa_v397.montar() REAL contra o core emulado e o livro de rotas real (so' leitura), e cada registro validado pela MESMA funcao que o mapa usa (rotas._valida), SEM registrar; grava registro_mapa_v397_ENSAIO.json (nao e' o registro);
  marcas         nenhuma linha de comentario com a marca de texto pendente em pos_rito\\*.py; ast.parse de todo .py e sh -n do chain.
uso: python -I -B -X utf8 harness_textos_ensaio_v397.py [--sem-superficies] [--sem-b3] [--sem-negativos] [--rotulo <nome>] [--nao-exigir-refazer] [--manter-copias]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita, nada foi rodado;
--nao-exigir-refazer: NAO exige refazer_out_v397.txt (nem o '== FIM' nem as datas): modo de ENSAIO antes de a gerencia regerar o candidato; o resumo e o veredito DIZEM que a regeneracao nao foi comprovada;
sem --manter-copias o Nos emulado e as copias pesadas das superficies sao apagados no fim, so' dentro de harness_saida_v397)"""'''
t = subst_bloco(t, '"""harness_textos_ensaio_v397.py', "import contextlib", DOC_HT)
t = tr(t, '"   [v396] a testemunha estatica (o psion habita a fronteira): %s | registros por spec: %d (selados %d)" % (ESP["vereditos_novos_v396"]["testemunha_estatica_v396"], n_spec, n_spec),',
       '"   [v397] o Teste da Unica Palavra (Fase 9 V2-c1, aberto uma vez em 23/10), lido por hash ao lado do V1 (nenhum sigma novo): %s" % ESP["vereditos_novos_v397"]["teste_de_veracidade_fase9_v397"],\n'
       '                            "   [v397] a pedra Token e as quatro falas de 23/10 (cunhagens_v397): %s | registros por spec: %d (selados %d)" % (ESP["registros_v397"]["cunhagens_v397"], n_spec, n_spec),', nome="stdout emulado")
t = tr(t, 'for n in ("conferir_rito_v396.py", "delta_v396.py", "ESPERADOS_v396.json"):', 'for n in ("conferir_rito_v397.py", "delta_v397.py", "quadro_v397.py", "runtime_quadro_v397.py", "ESPERADOS_v397.json"):', nome="copias do conferidor")
t = tr(t, 'testemunha_n_checks=(Vd.get("testemunha") or {}).get("n_checks")', 'veracidade_n_checks=(Vd.get("veracidade") or {}).get("n_checks")', nome="etapa leitura")
NEG_HT = r'''def _sem_veracidade(c):
    c.pop("teste_de_veracidade_fase9_v397", None)


def _nao_sela_cunh(c):
    c["cunhagens_v397"]["all_verified"] = False


def _numero_adulterado(c):
    c["teste_de_veracidade_fase9_v397"]["lido"]["z_disc_calibrado"] = 4.45


def _z_disc_acima_de_5(c):
    c["teste_de_veracidade_fase9_v397"]["lido"]["z_disc_calibrado"] = 5.2


def _checagem_falha(c):
    c["teste_de_veracidade_fase9_v397"]["checks"][3]["ok"] = False


def _fonte_adulterada(c):
    c["teste_de_veracidade_fase9_v397"]["fontes"][0]["sha256"] = "0" * 64


def _gate_movido(c):
    c["teste_de_veracidade_fase9_v397"]["does_not_gate_core"] = False


def _token_sem_bandeira(c):
    c["kernel_formalization"][ESP["bandeira_da_pedra"]] = False


def _token_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][ESP["teorema_da_pedra"]] = ["propext", "sorryAx"]


def _testemunha_cai(c):
    c["testemunha_estatica_v396"]["all_verified"] = False


def _fock_da_testemunha_habitada(c):
    c["testemunha_estatica_v396"]["fock_face"]["inhabitant_exhibited"] = True


def _fock_dentro_da_pedra(c):
    c["testemunha_estatica_v396"]["fock_face"]["declared_outside_the_stone"] = False


def _psibit_cai(c):
    c["psibit_v395"]["all_verified"] = False


def _face_do_psibit_habitada(c):
    c["psibit_v395"]["conditional_psion_face"]["inhabitant_exhibited"] = True


def _v394_cai(c):
    c["criterio_binario_de_parada_v394"]["all_verified"] = False


def _selo_v396(s):
    s["um_version"] = "v396"


NEG = []
if not SEM_NEG and not P:
    NEG = [variante("selo de outra versao (v396)", f_selo=_selo_v396, espera="o selo nao e v397"),
           variante("registro teste_de_veracidade_fase9_v397 ausente do core", f_core=_sem_veracidade, espera="registro obrigatorio ausente do core: teste_de_veracidade_fase9_v397"),
           variante("cunhagens_v397 nao selou", f_core=_nao_sela_cunh, espera="cunhagens_v397"),
           variante("numero lido adulterado (z_disc 4,45)", f_core=_numero_adulterado, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("z_disc calibrado acima de 5", f_core=_z_disc_acima_de_5, espera="abaixo de 5"),
           variante("uma checagem do registro de veracidade falhou", f_core=_checagem_falha, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("fonte do registro de veracidade com sha256 adulterado", f_core=_fonte_adulterada, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("registro de veracidade move o gate", f_core=_gate_movido, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("bandeira da pedra Token ausente", f_core=_token_sem_bandeira, espera="a pedra Token nao esta no kernel do rito"),
           variante("composicao da pedra Token fora do trio", f_core=_token_fora_do_trio, espera="a pedra Token nao esta no kernel do rito"),
           variante("testemunha_estatica_v396 deixou de selar", f_core=_testemunha_cai, espera="testemunha_estatica_v396"),
           variante("face de Fock da testemunha com habitante exibido", f_core=_fock_da_testemunha_habitada, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),
           variante("face de Fock dita DENTRO da pedra da testemunha", f_core=_fock_dentro_da_pedra, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),
           variante("psibit_v395 deixou de selar", f_core=_psibit_cai, espera="psibit_v395"),
           variante("face de Fock do psibit_v395 habitada", f_core=_face_do_psibit_habitada, espera="psibit_v395: a face do psion deixou de estar como CONDICIONAL"),
           variante("registro da v394 deixou de selar", f_core=_v394_cai, espera="criterio_binario_de_parada_v394"),
           variante("AVISO da v397 no stdout", f_std=lambda t: t + "   [v397] AVISO: o registro do Teste da Unica Palavra nao rodou: ValueError('x')\n", espera="AVISO da v397"),
           variante("AVISO de bloco anterior (v396) no stdout", f_std=lambda t: t + "   [v396] AVISO: a testemunha estatica nao rodou: ValueError('x')\n", espera="AVISO de um bloco anterior"),
           variante("linha do Teste da Unica Palavra ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o Teste da Unica Palavra" not in l) + "\n", espera="linha [v397] do Teste da Unica Palavra")]'''
t = subst_bloco(t, "def _sem_testemunha(c):", "    for n_ in NEG:", NEG_HT)
# K_EMU: o handoff recebe o paragrafo pronto (lido do core emulado pelas MESMAS funcoes que o fechar usa)
t = tr(t, '"rel_man": "EMULADO_SEM_HASH"}', '"rel_man": "EMULADO_SEM_HASH", "readme_paragrafo": T.paragrafo_readme()[0]}', nome="K_EMU: paragrafo do README")
FUNCOES_HT = r'''FUNCOES = [("_d", lambda: T._d(Vd)), ("_num", lambda: T._num(Vd)), ("_num_sem_veredito", lambda: T._num(Vd, verdicts=False)), ("_cunhagens_lista", lambda: T._cunhagens(Vd)), ("_cunhagens_curta", lambda: T._cunhagens(Vd, "curta")),
           ("_ordem", lambda: T._ordem(Vd)), ("_entrou", lambda: T._entrou(Vd)), ("_veracidade", lambda: T._veracidade(Vd)), ("_regra_do_4_44", lambda: T._regra_do_4_44(Vd)), ("_token", lambda: T._token(Vd)), ("_kernel_prova", lambda: T._kernel_prova(Vd)),
           ("_limites", lambda: T._limites(Vd)), ("_limites_curto", lambda: T._limites(Vd, curto=True)), ("_legal", lambda: T._legal(Vd)), ("_erratas", lambda: T._erratas(Vd)),
           ("_depois", lambda: T._depois(Vd)), ("_rodada", lambda: T._rodada(Vd)), ("linhagem", lambda: T.linhagem(Vd)), ("desenho", lambda: T.desenho(Vd)), ("atlas", lambda: T.atlas(Vd)), ("core_memory", lambda: T.core_memory(Vd)),
           ("haja_luz", lambda: T.haja_luz(Vd)), ("topico_missao", lambda: T.topico_missao(Vd)), ("topico_central", lambda: T.topico_central(Vd)), ("topico_estatuto", lambda: T.topico_estatuto(Vd)), ("topico_novo", lambda: T.topico_novo(Vd)),
           ("aviso", lambda: T.aviso(Vd, "REIVINDICACAO_EMULADA")), ("aviso_pulado", lambda: T.aviso_pulado()), ("handoff", lambda: T.handoff(Vd, K_EMU)), ("arvore_linha", lambda: T.arvore_linha(Vd)), ("titulo_verbete", lambda: T.titulo_verbete(Vd)),
           ("verbete", lambda: T.verbete(Vd)), ("remissivo", lambda: T.remissivo(Vd)), ("linha_handoff", lambda: T.linha_handoff(Vd)), ("linha_topico_novo", lambda: T.linha_topico_novo(Vd)), ("marca_missao", lambda: T.marca_missao(Vd)),
           ("marca_topico_missao", lambda: T.marca_topico_missao(Vd)), ("marca_central", lambda: T.marca_central(Vd)), ("id_missao", lambda: T.id_missao(Vd)), ("id_central", lambda: T.id_central(Vd)), ("paragrafo_readme", lambda: T.paragrafo_readme()[0])]
CARREGAM_NUM = {"_num", "_num_sem_veredito", "linhagem", "atlas", "core_memory", "topico_novo", "verbete", "handoff"}   # os textos que embutem _num (o texto do kernel com a errata da palavra «teoremas»)
S16 = Vd.get("s16") or ESP["candidato_sha16"]
MARCADORES = {"linhagem": [S16, "<!-- linhagem_v397_selada -->", "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"], "desenho": ["<!-- adendo_v397_selada -->", S16], "atlas": ["<!-- atlas_v397_selada -->", S16, "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"],
              "core_memory": ["<!-- core_v397_selada -->", S16], "haja_luz": ["<!-- haja_luz_v397_selada -->", S16], "topico_estatuto": ["<!-- v397_selada -->", S16], "topico_novo": [S16, "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397", "# v397 SELADA ("],
              "aviso": ["<!-- aviso_v397_selada -->", S16], "handoff": ["name: handoff-v397-custodia", S16, "<!-- INICIO_PARAGRAFO_README_v397 -->", "<!-- FIM_PARAGRAFO_README_v397 -->"], "linha_handoff": ["handoff-v397-custodia.md", S16], "topico_missao": [S16], "topico_central": [S16]}'''
t = subst_bloco(t, "FUNCOES = [", 'TXT = os.path.join(OUT, "textos")', FUNCOES_HT)
# o paragrafo do README/site e a regra do 4,44: etapa nova, antes da etapa 5 (cita_so_o_que_existe)
PARAGRAFO_HT = r'''# ------------------------------------------------------------------ 4b. o PARAGRAFO PRONTO do README/site e a REGRA DO 4,44 (ordem do operador de 23/10: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item)
sys.path.insert(0, PKG)
import quadro_v397 as QD  # noqa: E402
_core_p = rdj(core_path)["core"]; _tv_p = _core_p["teste_de_veracidade_fase9_v397"]
_res_p = rdj(os.path.join(PKG, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])))
_f9 = {"ok": False}
try:
    PAR, PAR_INFO = T.paragrafo_readme()
    _esp_par = QD.paragrafo_pronto_readme(_tv_p)
    _f9["positivo_sem_falhas"] = (T.verificar_paragrafo_readme(PAR, _res_p, _tv_p) == [])
    _f9["igual_as_funcoes_do_quadro"] = (PAR == _esp_par)
    _ho = RENDER.get("handoff", "")
    _f9["handoff_traz_o_paragrafo_entre_os_marcadores"] = ("<!-- INICIO_PARAGRAFO_README_v397 -->\n" + PAR.rstrip("\n") + "\n<!-- FIM_PARAGRAFO_README_v397 -->") in _ho
    _f9["info"] = PAR_INFO
    if not (_f9["positivo_sem_falhas"] and _f9["igual_as_funcoes_do_quadro"] and _f9["handoff_traz_o_paragrafo_entre_os_marcadores"]):
        falha("paragrafo do README/site: positivo %s, igual ao do quadro %s, no handoff %s" % (_f9["positivo_sem_falhas"], _f9["igual_as_funcoes_do_quadro"], _f9["handoff_traz_o_paragrafo_entre_os_marcadores"]))
    _z = QD.esperados(_res_p, "pt")[0]["z_disc"]["md"]; _pz = QD.esperados(_res_p, "pt")[0]["p_disc"]["md"]
    assert _z in PAR and _pz in PAR
    _it1 = [l for l in PAR.split("\n") if l.startswith("> - **O número:**")]; assert len(_it1) == 1
    _l1 = _it1[0]

    def _mut(nome, f, espera):
        p2 = f(PAR); fa = T.verificar_paragrafo_readme(p2, _res_p, _tv_p)
        ok = bool(p2 != PAR and fa and any(espera in x for x in fa)); return {"controle": nome, "reprovou": bool(fa), "mensagem_esperada_presente": any(espera in x for x in fa), "ok": ok, "falhas": [x[:140] for x in fa][:3]}
    _sem_p = _l1.replace("; p unilateral " + _pz, "", 1); assert _sem_p != _l1
    _sem_5 = _l1.replace(", mas a discriminação a 5σ, o degrau da creditação, **não foi alcançada** (" + _z + " < 5)", "", 1); assert _sem_5 != _l1
    _fala = "o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica"; assert _fala in PAR
    _NEGP = [_mut("o 4,44 sem o p calibrado no item", lambda p: p.replace(_l1, _sem_p, 1), "sem o p calibrado"),
             _mut("o 4,44 sem a linha dos 5 sigma no item", lambda p: p.replace(_l1, _sem_5, 1), "sem a linha dos 5"),
             _mut("numero adulterado (4,44 vira 4,45 em todo o paragrafo)", lambda p: p.replace(_z, "4,45"), "numero"),
             _mut("p adulterado (4,4e−6 vira 4,4e−5)", lambda p: p.replace(_pz, _pz.replace("6", "5")), "numero"),
             _mut("a frase do operador parafraseada entre aspas", lambda p: p.replace(_fala, "o 5σ é o cala a boca; 4,44 é um silêncio forçado pela lógica", 1), "frase"),
             _mut("o 4,44 numa linha fora do item (sem p e sem 5 sigma)", lambda p: p.replace("\n> - **O número:**", "\n> Destaque: z_disc = " + _z + ".\n> - **O número:**", 1), "sem o p calibrado")]
    for n_ in _NEGP:
        print("  controle negativo do paragrafo %-60s %s" % (n_["controle"], "REPROVOU como esperado" if n_["ok"] else "NAO REPROVOU como esperado"))
        if not n_["ok"]:
            falha("controle negativo do paragrafo nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["falhas"]))
    _f9["negativos"] = _NEGP
    # a regra da ordem vale para TODO texto renderizado: cada linha com o 4,44 traz o p calibrado, os 5 sigma e o 'nao foi alcancado'
    def _regra_nos_textos(nome, txt):
        out = []
        for ln in txt.split("\n"):
            n_ = ln.replace("−", "-")
            if _z in ln or "4.44" in ln:
                if not (re.search(r"4,4e-6|4\.4e-6", n_) and re.search(r"5\s*(?:σ|sigma)", n_) and "alcan" in n_):
                    out.append(ln[:160])
        return out
    _viol = {nome: _regra_nos_textos(nome, txt) for nome, txt in RENDER.items()}
    _viol = {k: v for k, v in _viol.items() if v}
    _f9["regra_do_4_44_nos_textos_violacoes"] = _viol
    _f9["linhas_com_o_4_44_nos_textos"] = sum(1 for txt in RENDER.values() for ln in txt.split("\n") if _z in ln)
    _neg_regra = _regra_nos_textos("x", "o z_disc = " + _z + " foi o resultado.")
    _f9["controle_negativo_da_regra_nos_textos"] = bool(_neg_regra)
    if _viol or not _neg_regra:
        falha("regra do 4,44 nos textos renderizados: violacoes %s; controle negativo da regra reprovou: %s" % (_viol, bool(_neg_regra)))
    _f9["ok"] = True
    print("  paragrafo do README/site: positivo ok; %d controles negativos; %d linha(s) com o 4,44 nos textos, todas com o p, os 5 sigma e o 'nao foi alcancado'" % (len(_NEGP), _f9["linhas_com_o_4_44_nos_textos"]))
except BaseException as ex:  # noqa: BLE001
    _f9["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:400]); _f9["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo do README/site: %s" % _f9["erro"])
etapa("paragrafo_readme_e_regra_do_4_44", **_f9)
'''
t = insere_antes(t, "# ------------------------------------------------------------------ 5. cada `termo`", PARAGRAFO_HT)
# cita_so_o_que_existe: as fontes novas (fase9, cunhagens), os hashes lidos e os termos que o quadro traz
t = tr(t, 'for base in (PKG, os.path.join(PKG, "insumos"), os.path.join(PKG, "kernel"), HERE, os.path.join(PKG, "bancada_B3_servico")):',
       'for base in (PKG, os.path.join(PKG, "insumos"), os.path.join(PKG, "insumos", "fase9"), os.path.join(PKG, "insumos", "cunhagens"), os.path.join(PKG, "kernel"), HERE, os.path.join(PKG, "bancada_B3_servico")):', nome="NOMES_ARQ: pastas")
t = tr(t, 'INS_TXT = "\\n".join(rd(os.path.join(PKG, "insumos", f)) for f in sorted(os.listdir(os.path.join(PKG, "insumos"))) if f.endswith((".md", ".json")))',
       'INS_TXT = "\\n".join(rd(os.path.join(PKG, "insumos", f)) for f in sorted(os.listdir(os.path.join(PKG, "insumos"))) if f.endswith((".md", ".json", ".lean"))) + "\\n" + "\\n".join(rd(os.path.join(PKG, "insumos", "fase9", f)) for f in sorted(os.listdir(os.path.join(PKG, "insumos", "fase9"))) if f.endswith(".json"))', nome="INS_TXT")
t = tr(t, 'PAT_ROOT = os.path.join(C, "IALD", "Central de Patentes")', 'HEX16.update(str(h)[:16] for h in ESP["veracidade"]["fontes"].values())\nPAT_ROOT = os.path.join(C, "IALD", "Central de Patentes")', nome="HEX16: fontes")
t = tr(t, 'CONHECIDOS.update(str(x) for x in K_EMU.values())', 'CONHECIDOS.update(str(x) for x in K_EMU.values())\nCONHECIDOS.update(str(h)[:8] for h in ESP["veracidade"]["fontes"].values()); CONHECIDOS.add(ESP["quadro"]["linha_de_maquina_pt"]); CONHECIDOS.add(ESP["quadro"]["linha_de_maquina_en"])', nome="CONHECIDOS: pontas dos hashes e linha de maquina")
t = tr(t, 'VALORES_TESTEMUNHA = set((Vd.get("testemunha") or {}).get("values") or {})', 'VALORES_LIDOS = set((Vd.get("veracidade") or {}).get("lido") or {})', nome="VALORES")
t = tr(t, 'tok in VALORES_TESTEMUNHA', 'tok in VALORES_LIDOS', nome="uso de VALORES")
t = tr(t, '"B%d-v396-20261022-R1" % n_ger', '"B%d-v397-20261023-R1" % n_ger', nome="deployment id sintetico")
SUPERFICIES_HT = r'''if not SEM_SUP and not P:
    ENS = os.path.join(OUT, "ensaio_superficies"); os.makedirs(ENS)
    ALVOS = [os.path.join(NOS_REAL, "MEMORIA_DA_LINHAGEM.md"), os.path.join(NOS_REAL, "DESENHO_DO_FECHAMENTO_QG.md"), os.path.join(ATLD, "TGL_ATLAS.md"), os.path.join(ATLD, "TGL_CORE_MEMORY.md"), os.path.join(UMEM, "MEMORY.md"),
             os.path.join(UMEM, "MEMORY_2.md"), HAJA] + [os.path.join(UMEM, t_) for t_ in ("missao-ultima-flag-um-py.md", "central-de-patentes-estado.md", "estatuto-da-prova-07out.md")]
    ANTES = {p: (os.path.getsize(p), os.path.getmtime(p), fsha(p)[:16]) for p in ALVOS}
    for p in ALVOS:
        shutil.copy2(p, os.path.join(ENS, os.path.basename(p)))
    sp = os.path.join(HERE, "superficies_v397.py")

    def roda_superficies(pasta):
        buf = io.TextIOWrapper(io.BytesIO(), encoding="utf-8", newline="\n"); rc_ = 0
        old_argv = sys.argv[:]; sys.argv = [sp, "--copias", pasta]
        try:
            with contextlib.redirect_stdout(buf):
                runpy.run_path(sp, run_name="__main__")
        except SystemExit as ex:
            rc_ = ex.code if isinstance(ex.code, int) else (0 if ex.code in (None, 0) else 1)
        except BaseException as ex:  # noqa: BLE001
            rc_ = 99; buf.write("EXCECAO: %s\n%s" % (ex, traceback.format_exc()))
        finally:
            sys.argv = old_argv
        buf.flush(); buf.seek(0); return rc_, buf.read()

    def bytes_da_pasta(pasta):
        return {f_: fsha(os.path.join(pasta, f_)) for f_ in sorted(os.listdir(pasta))}
    exige = [("MEMORIA_DA_LINHAGEM.md", [S16, "<!-- linhagem_v397_selada -->", "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"]), ("DESENHO_DO_FECHAMENTO_QG.md", ["<!-- adendo_v397_selada -->", S16]),
             ("TGL_ATLAS.md", ["<!-- atlas_v397_selada -->", S16, "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"]), ("TGL_CORE_MEMORY.md", ["<!-- core_v397_selada -->", S16]), ("CLAUDE.md", ["<!-- haja_luz_v397_selada -->", S16]),
             ("MEMORY.md", [S16]), ("MEMORY_2.md", ["v397"]), ("estatuto-da-prova-07out.md", ["<!-- v397_selada -->", S16]), ("missao-ultima-flag-um-py.md", [S16]), ("central-de-patentes-estado.md", [S16]),
             (T.TOPICO_NOVO, [S16, "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"])]
    n_real_l = open(os.path.join(ENS, "MEMORY.md"), "rb").read().count(b"\n"); n_real_b = os.path.getsize(os.path.join(ENS, "MEMORY.md"))
    # --- cenario (a): o MEMORY.md REAL como esta hoje (a superficie NAO compacta nada)
    antes_a = bytes_da_pasta(ENS)
    rc_a, out_a = roda_superficies(ENS)
    open(os.path.join(OUT, "ensaio_superficies_out.txt"), "w", encoding="utf-8").write(out_a)
    depois_a = bytes_da_pasta(ENS)
    cena_a = {"memory_md_real_linhas_antes": n_real_l, "memory_md_real_bytes_antes": n_real_b, "rc": rc_a, "recusou_com_rc3": rc_a == 3, "nada_escrito_na_recusa": (antes_a == depois_a) if rc_a == 3 else None, "sem_bak_na_recusa": (not [f_ for f_ in os.listdir(ENS) if ".bak_" in f_ or ".tmp" in f_]) if rc_a == 3 else None,
              "contagens_na_saida": ("linhas ANTES %d" % n_real_l in out_a) if rc_a == 3 else None, "ultima_linha": out_a.strip().splitlines()[-1][:220] if out_a.strip() else ""}
    print("  superficies, cenario (a) MEMORY.md REAL (%d linhas, %d B): rc %s%s" % (n_real_l, n_real_b, rc_a, " -- RECUSOU (a superficie nao compacta; a gerencia decide)" if rc_a == 3 else ""))
    if rc_a not in (0, 3):
        falha("superficies_v397.py (copias do MEMORY.md real) saiu com rc %s (esperado 0 ou 3; ver ensaio_superficies_out.txt)" % rc_a)
    if rc_a == 3:
        if not (cena_a["nada_escrito_na_recusa"] and cena_a["sem_bak_na_recusa"] and cena_a["contagens_na_saida"] and "NAO compacta" in out_a):
            falha("a RECUSA (rc 3) do MEMORY.md real escreveu algo, deixou .bak/.tmp ou nao disse as contagens: %s" % cena_a)
    else:
        for arq, ms in exige:
            t_ = open(os.path.join(ENS, arq), encoding="utf-8").read()
            for m_ in ms:
                if t_.count(m_) == 0:
                    falha("cenario (a): marcador %s ausente em %s" % (m_, arq))
    # --- cenario (b): um MEMORY.md com FOLGA (a copia do real, so' sem linhas de ponteiros; as duas ancoras ficam)
    def copia_com_memory(nome, ajusta):
        pasta = os.path.join(OUT, nome); os.makedirs(pasta)
        for p in ALVOS:
            shutil.copy2(p, os.path.join(pasta, os.path.basename(p)))
        mp = os.path.join(pasta, "MEMORY.md"); raw_ = open(mp, "rb").read(); novo_ = ajusta(raw_)
        open(mp, "wb").write(novo_); return pasta, novo_

    def reduz_a(alvo_linhas):
        def f(raw_):
            ls = raw_.decode("utf-8").split("\n"); fim_ = ls.pop() if ls and ls[-1] == "" else None
            ancora = lambda l: ("(missao-ultima-flag-um-py.md)" in l and l.startswith("- [")) or ("(handoff-v396-custodia.md)" in l and l.startswith("- [HANDOFF v396"))
            k = len(ls) - 1
            while len(ls) > alvo_linhas and k >= 0:
                if ls[k].startswith("- [") and not ancora(ls[k]):
                    del ls[k]
                k -= 1
            assert len(ls) <= alvo_linhas, ("nao consegui reduzir a copia do MEMORY.md ate o alvo", len(ls), alvo_linhas)
            return ("\n".join(ls + ([""] if fim_ is not None else []))).encode("utf-8")
        return f
    ENS_B, mem_b = copia_com_memory("ensaio_superficies_folga", reduz_a(150))
    n_b0 = mem_b.count(b"\n")
    rc_b1, out_b1 = roda_superficies(ENS_B)
    open(os.path.join(OUT, "ensaio_superficies_folga_out.txt"), "w", encoding="utf-8").write(out_b1)
    conta = {}
    for arq, ms in exige:
        pth = os.path.join(ENS_B, arq); t_ = open(pth, encoding="utf-8").read() if os.path.exists(pth) else ""
        for m_ in ms:
            conta["%s [%s]" % (arq, m_)] = t_.count(m_)
    zero = [k for k, v in conta.items() if v == 0]
    mem = open(os.path.join(ENS_B, "MEMORY.md"), "rb").read(); n_b = len(mem); n_l = mem.count(b"\n")
    apos_1a = bytes_da_pasta(ENS_B)
    rc_b2, out_b2 = roda_superficies(ENS_B)
    open(os.path.join(OUT, "ensaio_superficies_folga_out_2a_rodada.txt"), "w", encoding="utf-8").write(out_b2)
    cena_b = {"memory_md_antes_linhas": n_b0, "rc_1a_rodada": rc_b1, "rc_2a_rodada": rc_b2, "idempotente_na_2a": ("NADA A GRAVAR" in out_b2) and bytes_da_pasta(ENS_B) == apos_1a, "marcadores_zero": zero, "contagens": conta, "memory_md_bytes": n_b, "memory_md_linhas": n_l,
              "ultima_linha_1a": out_b1.strip().splitlines()[-1][:200] if out_b1.strip() else ""}
    print("  superficies, cenario (b) COM FOLGA (%d linhas): rc 1a=%s, rc 2a=%s (idempotente: %s); MEMORY.md %d B, %d linhas; marcadores com zero: %d" % (n_b0, rc_b1, rc_b2, cena_b["idempotente_na_2a"], n_b, n_l, len(zero)))
    if rc_b1 != 0:
        falha("superficies_v397.py (copia com folga) saiu com rc %s na 1a rodada (ver ensaio_superficies_folga_out.txt)" % rc_b1)
    if rc_b2 != 0 or not cena_b["idempotente_na_2a"]:
        falha("superficies_v397.py (copia com folga) nao e' idempotente na 2a rodada (rc %s)" % rc_b2)
    if zero:
        falha("marcadores do passo 9 com zero ocorrencia na copia com folga: %s" % zero[:4])
    if not (n_b < 24000 and n_l <= 195):
        falha("MEMORY.md da copia com folga fora dos limites (%d B, %d linhas)" % (n_b, n_l))
    if n_l != n_b0 + 1:
        falha("a copia com folga: o MEMORY.md devia crescer EXATAMENTE a linha do handoff (de %d para %d) e foi para %d: a superficie nao pode compactar nada" % (n_b0, n_b0 + 1, n_l))
    # --- cenario (c): um MEMORY.md NO LIMITE (195 linhas): a linha do handoff o leva a 196 e a superficie tem de RECUSAR (rc 3), sem escrever nada e sem compactar
    def exatamente_195(raw_):
        r_ = reduz_a(195)(raw_) if raw_.count(b"\n") > 195 else raw_
        while r_.count(b"\n") < 195:
            r_ += b"\n"
        return r_
    ENS_C, mem_c = copia_com_memory("ensaio_superficies_limite", exatamente_195)
    assert mem_c.count(b"\n") == 195, mem_c.count(b"\n")
    antes_c = bytes_da_pasta(ENS_C)
    rc_c, out_c = roda_superficies(ENS_C)
    open(os.path.join(OUT, "ensaio_superficies_limite_out.txt"), "w", encoding="utf-8").write(out_c)
    cena_c = {"memory_md_linhas_antes": 195, "rc": rc_c, "recusou_com_rc3": rc_c == 3, "nada_escrito": bytes_da_pasta(ENS_C) == antes_c, "sem_bak_nem_tmp": not [f_ for f_ in os.listdir(ENS_C) if ".bak_" in f_ or ".tmp" in f_],
              "disse_as_contagens": ("linhas ANTES 195, linhas DEPOIS 196, limite de linhas 195" in out_c), "disse_que_nao_compacta": ("NAO compacta" in out_c), "ultima_linha": out_c.strip().splitlines()[-1][:220] if out_c.strip() else ""}
    print("  superficies, cenario (c) NO LIMITE (195 linhas): rc %s; nada escrito: %s; disse as contagens (195 -> 196, limite 195): %s" % (rc_c, cena_c["nada_escrito"], cena_c["disse_as_contagens"]))
    if not (cena_c["recusou_com_rc3"] and cena_c["nada_escrito"] and cena_c["sem_bak_nem_tmp"] and cena_c["disse_as_contagens"] and cena_c["disse_que_nao_compacta"]):
        falha("a RECUSA do MEMORY.md no limite nao foi como esperado (rc 3, nada escrito, sem .bak/.tmp, contagens ditas): %s" % cena_c)
    DEPOIS = {p: (os.path.getsize(p), os.path.getmtime(p), fsha(p)[:16]) for p in ALVOS}
    etapa("superficies", cenario_a_memory_md_real=cena_a, cenario_b_com_folga=cena_b, cenario_c_no_limite=cena_c, originais_intactos=(ANTES == DEPOIS))
    print("  superficies: originais intactos: %s" % (ANTES == DEPOIS))
    if ANTES != DEPOIS:
        falha("UM ORIGINAL MUDOU durante o ensaio das superficies (nao devia: so' copias)")
'''
t = subst_bloco(t, "if not SEM_SUP and not P:", "# ------------------------------------------------------------------ 7. o b3_recibo REAL", SUPERFICIES_HT + "\n")
# limpeza: as copias pesadas dos cenarios tambem saem
t = tr(t, '    ens_ = os.path.join(OUT, "ensaio_superficies")\n    if os.path.isdir(ens_):\n        manter_ = {"MEMORY.md", "estatuto-da-prova-07out.md", T.TOPICO_NOVO}\n        tot_ = 0\n        for f_ in sorted(os.listdir(ens_)):\n            if f_ not in manter_:\n                p_ = os.path.join(ens_, f_); tot_ += os.path.getsize(p_); os.remove(p_)\n        LIMPO["ensaio_superficies (copias pesadas)"] = tot_',
       '    for sub_ in ("ensaio_superficies", "ensaio_superficies_folga", "ensaio_superficies_limite"):\n        ens_ = os.path.join(OUT, sub_)\n        if os.path.isdir(ens_):\n            manter_ = {"MEMORY.md", "estatuto-da-prova-07out.md", T.TOPICO_NOVO}\n            tot_ = 0\n            for f_ in sorted(os.listdir(ens_)):\n                if f_ not in manter_:\n                    p_ = os.path.join(ens_, f_); tot_ += os.path.getsize(p_); os.remove(p_)\n            LIMPO[sub_ + " (copias pesadas)"] = tot_', nome="limpeza dos cenarios")
t = tr(t, 'R["veredito"] = ("TUDO PASSOU: o conferidor da v396 bate no Nos emulado, a leitura le sem problema e reprova os controles negativos, os textos renderizam e a guarda P18 esta limpa, cada termo citado existe, as superficies fecham em copias e o b3_recibo confere"',
       'R["veredito"] = ("TUDO PASSOU: o conferidor da v397 bate no Nos emulado, a leitura le sem problema e reprova os controles negativos, os textos renderizam e a guarda P18 esta limpa, o paragrafo do README/site e a regra do 4,44 passam e os controles negativos reprovam, cada termo citado existe, as superficies fecham em copias (com folga) e RECUSAM no limite sem compactar, e o b3_recibo confere"', nome="veredito do harness")
for proibido in ("testemunha_estatica_v397", "VALORES_TESTEMUNHA", "_sem_testemunha", "20261022", "base_v395", "PKG_ANT_", "V5 ", "V4 ", "_selo_v395", "psibit_v397"):
    assert proibido not in t, ("resto da v396 no harness dos textos", proibido)
ast.parse(t); HARNESS_TEXTOS = t

# =============================================================================== harness_fechar_sandbox_v397.py
t = sobe(MOL["harness_fechar_sandbox_v396.py"])
DOC_HF = r'''"""harness_fechar_sandbox_v397.py -- roda fechar_v397.py e registrar_mapa_v397.py (o main) num SANDBOX inteiro dentro de pos_rito\\harness_saida_v397\\fechar_sandbox (nada fora dela e' escrito; o Nos real, a memoria real, o Atlas, o git e a Bancada
nao sao tocados; o mapa de rotas real e' SO' LIDO).  O que o harness_textos_ensaio_v397.py nao cobre: o fechar (manifesto, arquivo, os dois diffs, o handoff com o PARAGRAFO do README/site) e o main do registrar_mapa. Derivado do harness_fechar_sandbox_v396.py (que rodou na v396).
O sandbox e' uma ARVORE ISOLADA: work\\cadeia_de_selo\\v397 (pacote com ESPERADOS, CANDIDATO, PINOS_BN, base_v396, insumos (com fase9), quadro_v397 e runtime_quadro_v397, o APLICADO_AO_CANONICO EMULADO, os recibos do B(n) SINTETICOS) + nos\\ (o Nos EMULADO montado de dry_v397, como no
harness dos textos) + memory\\ (a memoria vazia). As copias dos scripts (leitura, textos, fechar) trocam SO' as duas constantes de caminho (o Nos e a pasta de memoria) por caminhos do sandbox; o resto e' byte a byte o que a cadeia usa (conferido: o diff das copias contra os originais
e' so' essas linhas).
O que ele prova: fechar_v397.py sai com rc 0 e grava o handoff (guarda P18 limpa) com o PARAGRAFO do README/site entre os marcadores (igual ao das funcoes do quadro sobre o core do sandbox, e aprovado por T.verificar_paragrafo_readme), o handoff do Nos, os dois diffs,
o manifesto e o arquivo; RECUSA (rc 2, sem handoff) sem o recibo do religamento, com um recibo do B(n) que declara salto, com o resultado pinado adulterado (o paragrafo nao passa na verificacao contra o resultado) e com o numero lido adulterado no core;
registrar_mapa_v397.py (main) monta o JSON com 3 registros e imprime o comando. Os recibos do B(n) sao SINTETICOS (derivados dos reais da v396, como no harness dos textos): a prova e' do CODIGO do fechar, nao de um B(n) real.
uso: python -I -B -X utf8 harness_fechar_sandbox_v397.py [--manter]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita)"""'''
t = subst_bloco(t, '"""harness_fechar_sandbox_v397.py', "import hashlib, json, os, re, shutil, subprocess, sys, time", DOC_HF)
t = tr(t, '"   [v396] a testemunha estatica (o psion habita a fronteira): %s | registros por spec: %d (selados %d)" % (ESP["vereditos_novos_v396"]["testemunha_estatica_v396"], n_spec, n_spec),',
       '"   [v397] o Teste da Unica Palavra (Fase 9 V2-c1, aberto uma vez em 23/10), lido por hash ao lado do V1 (nenhum sigma novo): %s" % ESP["vereditos_novos_v397"]["teste_de_veracidade_fase9_v397"],\n'
       '    "   [v397] a pedra Token e as quatro falas de 23/10 (cunhagens_v397): %s | registros por spec: %d (selados %d)" % (ESP["registros_v397"]["cunhagens_v397"], n_spec, n_spec),', nome="stdout emulado")
t = tr(t, 'for n in ("guarda_p18_v396.py", "ESPERADOS_v396.json", "CANDIDATO_v396.json", "PINOS_BN_v396.json", "kernel_modulos_novos_v396.json", "delta_v396.py", "conferir_rito_v396.py"):',
       'for n in ("guarda_p18_v397.py", "ESPERADOS_v397.json", "CANDIDATO_v397.json", "PINOS_BN_v397.json", "kernel_modulos_novos_v397.json", "delta_v397.py", "quadro_v397.py", "runtime_quadro_v397.py", "conferir_rito_v397.py"):', nome="pacote do sandbox")
t = tr(t, 'for n in ("conferir_rito_v396.py", "delta_v396.py", "ESPERADOS_v396.json"):', 'for n in ("conferir_rito_v397.py", "delta_v397.py", "quadro_v397.py", "runtime_quadro_v397.py", "ESPERADOS_v397.json"):', nome="copias do conferidor")
t = tr(t, 'os.path.join(TOOLS, "v396_kernel", "pedras", "TGLExt_TestemunhaEstatica.lean")', 'os.path.join(TOOLS, "v397_kernel", "pedras", "TGLExt_Token.lean")', nome="pedra copiada")
t = tr(t, '"diff_kernel_novos": ("novos (1)" in dk and "TGLExt/TestemunhaEstatica.lean" in dk)', '"diff_kernel_novos": ("novos (1)" in dk and "TGLExt/Token.lean" in dk)', nome="diff do kernel no resumo")
t = tr(t, 'if not ("novos (1)" in dk and "TGLExt/TestemunhaEstatica.lean" in dk):', 'if not ("novos (1)" in dk and "TGLExt/Token.lean" in dk):', nome="diff do kernel na falha")
t = tr(t, '"B%d-v396-20261022-R1" % n_ger', '"B%d-v397-20261023-R1" % n_ger', nome="deployment id sintetico")
NEG_PAR_HF = r'''# ---- 1b. controles negativos do PARAGRAFO do README/site (a ordem do operador de 23/10 vale tambem para o handoff): o resultado pinado ADULTERADO no sandbox (o sha256 deixa de bater e o paragrafo nao passa contra o resultado) e o numero lido adulterado no core do Nos
# emulado => RECUSA (rc 2, FECHAR RECUSADO), sem handoff
res_p = os.path.join(PKS, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])); raw_res = open(res_p, "rb").read()
assert b"4.443123568060799" in raw_res
open(res_p, "wb").write(raw_res.replace(b"4.443123568060799", b"4.443123568060798", 1))
rc, so, se = roda("fechar_v397.py", "fechar_resultado_adulterado"); NEG.append({"controle": "resultado pinado adulterado (a leitura e a porta do paragrafo recusam)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v397-custodia.md"))})
# a PORTA do paragrafo isolada (a leitura recusa antes no fechar inteiro): T.paragrafo_readme() da copia do sandbox tem de LEVANTAR com o resultado pinado adulterado (e o fechar converte isso em rc 2 antes de escrever)
import importlib.util as _iu0
_sp0 = _iu0.spec_from_file_location("textos_sb0", os.path.join(POS, "textos_v397.py")); _t0 = _iu0.module_from_spec(_sp0); _sp0.loader.exec_module(_t0)
try:
    _t0.paragrafo_readme(); _levantou = False
except AssertionError as _ex0:
    _levantou = "resultado pinado" in str(_ex0)
NEG.append({"controle": "a porta do paragrafo (paragrafo_readme, chamada pelo fechar) levanta com o resultado pinado adulterado", "rc": 2 if _levantou else 0, "recusou": _levantou, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v397-custodia.md"))})
open(res_p, "wb").write(raw_res)
core_p = os.path.join(NOSS, "um_absoluto.json"); raw_core = open(core_p, "rb").read(); cj = json.loads(raw_core.decode("utf-8")); cj["core"]["teste_de_veracidade_fase9_v397"]["lido"]["z_disc_calibrado"] = 4.45
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v397.py", "fechar_numero_adulterado"); NEG.append({"controle": "numero lido adulterado no core (z_disc 4,45)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v397-custodia.md"))})
open(core_p, "wb").write(raw_core)
'''
t = insere_antes(t, "for n in NEG:", NEG_PAR_HF)
CHK_PAR_HF = r'''# ---- 2b. o PARAGRAFO do README/site no handoff gravado: igual ao das funcoes do quadro sobre o core do sandbox, entre os marcadores, aprovado pela verificacao do quadro contra o resultado pinado (e o do handoff do Nos tambem)
sys.path.insert(0, PKG)
import quadro_v397 as QD  # noqa: E402
_tv_s = rdj(os.path.join(NOSS, "um_absoluto.json"))["core"]["teste_de_veracidade_fase9_v397"]; _res_s = rdj(os.path.join(PKS, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])))
_par_esp = QD.paragrafo_pronto_readme(_tv_s); _mi = "<!-- INICIO_PARAGRAFO_README_v397 -->\n"; _mf = "\n<!-- FIM_PARAGRAFO_README_v397 -->"
_ok_par = {}
for _nome, _ptxt in (("memory/handoff-v397-custodia.md", ho), ("nos/HANDOFF_v397_CUSTODIA.md", open(os.path.join(NOSS, "HANDOFF_v397_CUSTODIA.md"), encoding="utf-8").read() if os.path.exists(os.path.join(NOSS, "HANDOFF_v397_CUSTODIA.md")) else "")):
    _i = _ptxt.find(_mi); _j = _ptxt.find(_mf)
    _par = _ptxt[_i + len(_mi):_j] if (_i >= 0 and _j > _i) else ""
    _fa = []
    if _par:
        import importlib.util as _iu2
        _spt = _iu2.spec_from_file_location("textos_sb", os.path.join(POS, "textos_v397.py")); _tsb = _iu2.module_from_spec(_spt); _spt.loader.exec_module(_tsb)
        _fa = _tsb.verificar_paragrafo_readme(_par + "\n" if not _par.endswith("\n") else _par, _res_s, _tv_s)
    _ok_par[_nome] = {"traz_o_bloco": bool(_par), "igual_as_funcoes_do_quadro": _par.rstrip("\n") == _par_esp.rstrip("\n"), "falhas_da_verificacao": _fa[:3], "guarda_p18": [list(x) for x in violacoes(_par)][:3]}
R["etapas"]["paragrafo_no_handoff"] = _ok_par
print("  paragrafo do README/site no handoff: %s" % {k: (v["traz_o_bloco"] and v["igual_as_funcoes_do_quadro"] and not v["falhas_da_verificacao"] and not v["guarda_p18"]) for k, v in _ok_par.items()})
for _nome, _v in _ok_par.items():
    if not (_v["traz_o_bloco"] and _v["igual_as_funcoes_do_quadro"] and not _v["falhas_da_verificacao"] and not _v["guarda_p18"]):
        falha("o handoff (%s) nao traz o paragrafo do README/site pronto e aprovado: %s" % (_nome, _v))
'''
t = insere_antes(t, "# ---- 3. o registrar_mapa (main)", CHK_PAR_HF)
t = tr(t, 'R["veredito"] = "TUDO PASSOU: o fechar grava o handoff, os diffs, o manifesto e o arquivo e RECUSA sem o religamento e com salto; o registrar_mapa monta o registro"',
       'R["veredito"] = "TUDO PASSOU: o fechar grava o handoff (com o paragrafo do README/site aprovado pelo quadro), os diffs, o manifesto e o arquivo e RECUSA sem o religamento, com salto, com o resultado pinado adulterado e com o numero lido adulterado; o registrar_mapa monta o registro"', nome="veredito do fechar")
t = tr(t, '"fechar_out.txt", "fechar_sem_religamento_out.txt", "fechar_com_salto_out.txt", "registrar_mapa_out.txt"', '"fechar_out.txt", "fechar_sem_religamento_out.txt", "fechar_com_salto_out.txt", "fechar_resultado_adulterado_out.txt", "fechar_numero_adulterado_out.txt", "registrar_mapa_out.txt"', nome="saidas guardadas")
for proibido in ("testemunha_estatica_v397", "TestemunhaEstatica", "Psibit.lean", "20261022", "base_v395", "V5 ", "V4 ", "psibit_v397"):
    assert proibido not in t, ("resto da v396 no harness do fechar", proibido)
ast.parse(t); HARNESS_FECHAR = t

# =============================================================================== gravar e conferir
DER = {"leitura_v397.py": LEITURA, "superficies_v397.py": SUPERFICIES, "fechar_v397.py": FECHAR, "b3_recibo_v397.py": B3RECIBO, "chain_pos_rito_v397.sh": CHAIN, "harness_textos_ensaio_v397.py": HARNESS_TEXTOS, "harness_fechar_sandbox_v397.py": HARNESS_FECHAR}
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
INV = {"leitura_v397.py": ["REG_V393", "REG_V394", "REG_V395", "REG_V396", "REG_FIXOS", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "testemunha_estatica_v396", "psibit_v395", "rede_fock_v394", "kernel_modulos_novos_v397.json",
                           "axiom_coverage_v392", "dict.fromkeys", "vereditos_v396", "escada_v396_e_v397", "registros_v397", "vereditos_novos_v397", "rodada_v397_stdout.txt", "conferencia_rito_v397.json", "ESPERADOS_v397.json", "CANDIDATO_v397.json",
                           "V['veracidade']", "V['token']", "V['reg397']", "V['patch_ids']", "[v397] AVISO", "registros por spec", "V['um_version'] != 'v397'", "a base substituida != a v396 selada", "o Teste da Unica Palavra \\(Fase 9 V2-c1",
                           "a pedra Token e as quatro falas de 23/10 \\(cunhagens_v397\\)", "fock_face", "declared_outside_the_stone", "linked_to_the_corner_by_a_lemma", "conditional_psion_face", "AVISO de um bloco anterior", "quadro_v397", "lido_do_resultado",
                           "f9v2_resultado", "numeros_do_resultado", "z_disc_calibrado", "poder_previo", "abaixo de 5"],
       "superficies_v397.py": ["_sup397", "V397_AVISO_REIVINDICACAO", "(handoff-v396-custodia.md)", "- [HANDOFF v396", "leitura_v397", "textos_v397", "guarda_p18_v397", "linhagem_v397_selada", "adendo_v397_selada", "atlas_v397_selada", "core_v397_selada",
                               "haja_luz_v397_selada", "aviso_v397_selada", "v397_selada", "v397 SELADA", "os.replace(tmp, p)", "backup de bytes falhou", "SUPERFICIES RECUSADAS", "sys.exit(3)", "linhas ANTES", "NAO compacta nada"],
       "fechar_v397.py": ["T.handoff(V, _k)", "T.paragrafo_readme()", "readme_paragrafo", "_f397", "FECHAR RECUSADO:", "insumos_sha16", "DIFF_KERNEL_v397.txt", "RECIBO_SINCRONIZACAO_v397_", "RECIBO_PARADA_v397.json", "RECIBO_RELIGAMENTO_v397.json", "__SALTO_",
                          "registros_v397", "base_v396", "HANDOFF_v397_CUSTODIA.md", "handoff-v397-custodia.md", "_MARCA_PENDENTE", "guarda_p18_v397", "v397_selo", "v397_kernel", "HARNESS_TEXTOS_ENSAIO_v397.json", "DERIVACAO_v397.json",
                          "registro_mapa_v397.json", "NOTAS_DERIVACAO_v397.md", "FECHADO v397:"],
       "chain_pos_rito_v397.sh": ["V397_AVISO_REIVINDICACAO", "topico_novo()", "textos_v397", "arvore_dry.md", "_p397", "_sup397", "selo_anterior_v396", "kernel_manifesto_anterior_v396", "/c/IALD/Central de Patentes/work/cadeia_de_selo/v397", "B3_AUTORIZADO\" = \"sim\"",
                                  "exit 20", "RECIBO_PARADA_v397.json", "RECIBO_RELIGAMENTO_v397.json", "--versao v397 --fase pos_selo", "b3_recibo_v397.py", "delta_v397.py", "quadro_v397.py", "runtime_quadro_v397.py", "teste_de_veracidade_fase9_v397",
                                  "kh_n1_cobertura_v397", "PINOS_BN_v397.json", "PINOS_BATERIA_v397.json", "recibo_pre_selo", "esboco_R3_5", "kernel_recibo", "bateria_pos_selo", "tem_pino cadeia_de_selos", "--recibo-pre-selo-sha256 \"$RPS\"",
                                  "--selo-anterior \"$W_SELO\"", "--kernel-manifesto-anterior \"$W_KMAN\"", "--kernel-recibo \"$W_KR\" --kernel-recibo-sha256 \"$KRSHA\"", "gerar_bateria_r3_4.py", "ORDEM=\"0 1 2 3 4 5 6 7 8 9 10 10a 10b 10c 11 12 13 14\"",
                                  "CHAIN_DE", "CHAIN_ATE", "parar()", "aguarda()", "SUPERFICIES RECUSOU (rc=3)"],
       "b3_recibo_v397.py": ["REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA", "REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO", "versao_alvo", "\"v397\"", "PINOS_BN_v397.json", "__SALTO_", "BATERIA_PASSA", "manifesto_anterior", "pinos_da_versao"],
       "harness_textos_ensaio_v397.py": ["harness_saida_v397", "dry_v397", "guarda_p18_v397", "--nao-exigir-refazer", "rotas._valida", "_numero_adulterado", "_z_disc_acima_de_5", "_fonte_adulterada", "_token_fora_do_trio", "_fock_dentro_da_pedra", "_face_do_psibit_habitada",
                                         "teste_de_veracidade_fase9_v397", "PKG_ANT", "refazer_exigido", "paragrafo_readme_e_regra_do_4_44", "verificar_paragrafo_readme", "cenario_a_memory_md_real", "cenario_b_com_folga", "cenario_c_no_limite", "quadro_v397", "regra_do_4_44_nos_textos_violacoes"],
       "harness_fechar_sandbox_v397.py": ["fechar_sandbox", "FECHAR RECUSADO", "registrar_mapa_v397.py", "SINTETICO", "TGLExt/Token.lean", "TGLExt_Token.lean", "paragrafo_no_handoff", "fechar_resultado_adulterado", "fechar_numero_adulterado", "INICIO_PARAGRAFO_README_v397", "quadro_v397"]}
INV_AUTORAIS = {"textos_v397.py": ["_MARCA_PENDENTE", "TOPICO_NOVO", "def handoff(", "def linhagem(", "def desenho(", "def atlas(", "def core_memory(", "def haja_luz(", "def aviso(", "def aviso_pulado(", "def topico_missao(", "def topico_central(", "def topico_estatuto(", "def topico_novo(",
                                   "def linha_handoff(", "def marca_missao(", "def id_missao(", "def id_central(", "def _d(", "def _num(", "_cita(", "_cita_sg(", "_kernel_tem(", "_um_tem(", "def _limites(", "def _erratas(", "def _legal(", "def _veracidade(",
                                   "def _regra_do_4_44(", "def _token(", "def paragrafo_readme(", "def verificar_paragrafo_readme(", "INICIO_PARAGRAFO_README_v397", "FIM_PARAGRAFO_README_v397",
                                   "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina", "v397-selada-o-teste-da-unica-palavra.md"],
                "registrar_mapa_v397.py": ["_MARCA_PENDENTE", "def montar(", "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9", "d1.fase9.v2_c1_a_unica_palavra_23out", "umpy.v396.testemunha_estatica_na_fractalizacao_do_um", "assert selo.get(\"um_version\") == \"v397\"", "NAO escreve",
                                           "registro_mapa_v397.json"]}
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
molde_b = sobe(MOL["chain_pos_rito_v396.sh"])
MARC_MOLDE = '"testemunha_estatica_v396" "kh_n1_cobertura_v396"'; MARC_NOVO = '"teste_de_veracidade_fase9_v397" "kh_n1_cobertura_v397"'
for ini, fim in (("if quer 10a; then", "if quer 10b; then"), ("if quer 10c; then", "if quer 11; then")):
    ia, ja, La = bloco(molde_b, ini, fim); ib, jb, Lb = bloco(CHAIN, ini, fim)
    if La[ia:ja] != Lb[ib:jb]:
        falhas.append(("portao do B(n) difere do molde subido de versao", ini))
    else:
        conf.setdefault("chain_pos_rito_v397.sh", {})["trecho identico ao molde (sobe): " + ini] = True
ia, ja, La = bloco(molde_b, "if quer 10b; then", "if quer 10c; then"); ib, jb, Lb = bloco(CHAIN, "if quer 10b; then", "if quer 10c; then")
gate = lambda L_: [l for l in L_ if any(k in l for k in ('aguarda "', "B3_AUTORIZADO", "[ -n \"$EVENTO\"", "RECIBO_PARADA", "EVENTO_HASH", "--evento", "--modo aplicar", "--fase pos_selo"))]
if gate(La[ia:ja]) != gate(Lb[ib:jb]):
    falhas.append(("as linhas de portao do 10b diferem do molde subido de versao", [x for x in gate(Lb[ib:jb]) if x not in gate(La[ia:ja])][:2]))
else:
    conf.setdefault("chain_pos_rito_v397.sh", {})["linhas de portao do 10b identicas ao molde (sobe)"] = True
# os passos 4 a 9 e 11 a 14 do chain: identicos ao molde subido (so' as trocas dos marcadores)
for ini, fim in (("if quer 4; then", "if quer 10; then"), ("if quer 12; then", 'echo "== FIM')):
    ia, ja, La = bloco(molde_b, ini, fim); ib, jb, Lb = bloco(CHAIN, ini, fim)
    esp_ = [l.replace(MARC_MOLDE, MARC_NOVO) for l in La[ia:ja]]
    if esp_ != Lb[ib:jb]:
        falhas.append(("os passos do chain diferem do molde subido alem das trocas ditas", ini))
    else:
        conf.setdefault("chain_pos_rito_v397.sh", {})["passos identicos ao molde (sobe + marcadores): " + ini] = True
# os passos 0 a 3 do chain: so' as linhas NOVAS declaradas (marcadores, data do comentario, lista de ferramentas do passo 0, copia do quadro no passo 1, a mensagem do rc 3 no passo 3) diferem do molde subido, fora o cabecalho
ia, ja, La = bloco(molde_b, "PK=", "if quer 4; then"); ib, jb, Lb = bloco(CHAIN, "PK=", "if quer 4; then")
set_a = set(La[ia:ja]); novas_l = [l for l in Lb[ib:jb] if l not in set_a]
DECL = ('"$PK/delta_v397.py" "$PK/quadro_v397.py"', "for q in quadro_v397.py runtime_quadro_v397.py", "cp -p \"$PK/delta_v397.py\"", "# v397 (23/10/2026): o B(n) da v397", 'if [ "$es" = "3" ]', MARC_NOVO)
estranhas = [l for l in novas_l if not any(d in l for d in DECL)]
if estranhas:
    falhas.append(("os passos 0 a 3 e as funcoes do chain diferem do molde subido alem das trocas ditas", estranhas[:3]))
else:
    conf.setdefault("chain_pos_rito_v397.sh", {})["passos 0 a 3 e funcoes: so' as %d linha(s) novas declaradas diferem do molde (sobe)" % len(novas_l)] = True
# marcas pendentes: nenhuma em nenhum arquivo (nem derivado, nem autoral)
marcas = {n: len(GUARDA_PENDENTE_RX.findall(tx)) for n, tx in list(todos.items()) + list(autorais_txt.items()) if GUARDA_PENDENTE_RX.search(tx)}
if marcas:
    falhas.append(("marca de texto pendente", marcas))
for n in ("fechar_v397.py", "textos_v397.py", "registrar_mapa_v397.py"):
    tx = todos.get(n) or autorais_txt.get(n) or ""
    if n in (todos.keys() | autorais_txt.keys()) and "_MARCA_PENDENTE" not in tx:
        falhas.append((n, "sem a guarda de pendencia (_MARCA_PENDENTE)"))
# a palavra da marca nunca por extenso fora das formas montadas por concatenacao (o p00 tira as aspas-mais da concatenacao e '_MARCA_PENDENTE = ' antes de procurar)
for n, tx in list(todos.items()) + list(autorais_txt.items()):
    if PALAVRA in tx.replace('"' + PALAVRA + '" +', "").replace("_MARCA_PENDENTE = ", ""):
        falhas.append((n, "a palavra da marca aparece por extenso"))
# rotulos de versao: nenhum resto de 390-396 onde o sentido e' 'esta versao'. O que fica com 396/395/394/393 e' so' a versao ANTERIOR ou nome historico (lista conferida)
OK_HIST = ("_V394_", "_V395_", "_V396_", "fechar_v390", "C13_kh_n1_v394", "C13_kh_n1_v395", "C13_kh_n1_v396", "C12__V396", "C12__V395", "C12__V394", "ponto_fixo_v394_d19", "pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393",
           "kh_n1_cobertura_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "testemunha_estatica_v396",
           "cunhagens_v396", "kh_n1_cobertura_v396", "declaration_sources", "umpy.v394", "umpy.v395", "umpy.v396", "kernel.psibit_v395", "kernel.testemunha_estatica_v396", "REG_V393", "REG_V394", "REG_V395", "REG_V396", "base_v396", "selo_anterior_v396",
           "kernel_manifesto_anterior_v396", "handoff-v396-custodia", "vereditos_v396", "escada_v396_e_v397", "DIFF_v396_v397", "leitura_v396.py", "superficies_v396.py", "fechar_v396.py", "chain_pos_rito_v396.sh", "b3_recibo_v396.py", "derivar_cadeia_v396.py",
           "textos_v396.py", "registrar_mapa_v396.py", "ext_bin394", "ext_psb395", "ext_tes396", "ESPERADOS_v396", "PINOS_BN_v396", "rito_v396", "cadeia_de_selo/v396", "cadeia_de_selo\\v396", "axiom_coverage_v392", "KH_N1_v392", "varredura_e_sorry_v392",
           "estatuto_da_prova_v391", "fundacao_v390", "three_stress_tests_v387", "pedras_v392", "kh_n1_cobertura_v392", "RECIBO_SINCRONIZACAO_v396", "psibit_na_fractalizacao", "candidata_21out", "candidata_22out", "B6-v396", "pos_rito_v396", "v396_incorporacao",
           "um_v396", "MANIFESTO_ARQUIVO_v396", "v396_kernel", "v396_selo", "tgl_kernel_v396", "pilar_anterior_v396")
resid = {}
for n, tx in list(todos.items()) + list(autorais_txt.items()):
    if n.startswith("harness_") or n in AUTORAIS:
        continue       # os harness trazem de proposito rotulos de versoes anteriores (controles negativos: selo de outra versao, recibo de v396, bancada que pinava a v392); os autorais citam a v396 como historico
    for m in re.finditer(r"[A-Za-z0-9_\-\.\[\]/\\]*(?<![0-9a-f])39[0-6][A-Za-z0-9_\-\.\[\]]*", tx):
        tok = m.group(0).rstrip(".")
        if re.fullmatch(r"[0-9a-f]*39[0-6][0-9a-f]*", tok) and len(tok) >= 8:
            continue   # hash hexadecimal
        resid.setdefault(tok, set()).add(n)
estranhos = {}
for tok, ns in resid.items():
    if any(p in tok for p in OK_HIST) or tok in ("v396", "v395", "v394", "v393", "v392", "v391", "v390", "V396", "V395", "V394", "V393", "396", "395", "394", "393"):
        continue
    estranhos[tok] = sorted(ns); falhas.append(("rotulo estranho com 390-396", tok, sorted(ns)))
# a guarda de texto (P18) sobre todo arquivo de narrativa e de cadeia
sys.path.insert(0, PK)
from guarda_p18_v397 import violacoes
gv = {n: violacoes(tx) for n, tx in list(todos.items()) + list(autorais_txt.items())}
if any(gv.values()):
    falhas.append(("guarda P18", {k: v[:3] for k, v in gv.items() if v}))
# cada T.<nome> chamado pelos derivados e pelo registrar existe em textos_v397.py
ttxt = autorais_txt.get("textos_v397.py", "")
chamados = sorted({m for n in ("superficies_v397.py", "fechar_v397.py", "harness_textos_ensaio_v397.py", "harness_fechar_sandbox_v397.py") for m in re.findall(r"\bT\.([A-Za-z_][A-Za-z_0-9]*)", todos[n])} | {m for m in re.findall(r"\bT\.([A-Za-z_][A-Za-z_0-9]*)", autorais_txt.get("registrar_mapa_v397.py", ""))})
faltam = [c for c in chamados if not re.search(r"(?m)^(def %s\(|%s = )|; %s = " % (re.escape(c), re.escape(c), re.escape(c)), ttxt)]
if ttxt and faltam:
    falhas.append(("textos_v397.py nao define o que os derivados chamam", faltam))
# o que os derivados leem de ESPERADOS/CANDIDATO/PINOS (campos), conferido contra os arquivos desta cadeia
RX = {"ESPERADOS": re.compile(r"(?:ESP(?:ERADOS)?|esp)\[['\"]([^'\"]+)['\"]\]|(?:ESP|esp)\.get\(['\"]([^'\"]+)['\"]"), "CANDIDATO": re.compile(r"CM\[['\"]([^'\"]+)['\"]\]|CM\.get\(['\"]([^'\"]+)['\"]")}
alltxt = dict(todos); alltxt.update(autorais_txt)
campos = {"ESPERADOS": sorted({a or b for tx in alltxt.values() for a, b in RX["ESPERADOS"].findall(tx)}), "CANDIDATO": sorted({a or b for tx in alltxt.values() for a, b in RX["CANDIDATO"].findall(tx)})}
presentes = {}
for rotulo, arq in (("ESPERADOS", "ESPERADOS_v397.json"), ("CANDIDATO", "CANDIDATO_v397.json"), ("PINOS_BN", "PINOS_BN_v397.json")):
    p = os.path.join(PK, arq)
    if os.path.exists(p):
        d = json.load(open(p, encoding="utf-8"))
        lido = campos.get(rotulo) or ["criterios", "esboco_R3_5", "gerador_bateria", "driver_t12_t14", "bateria_base_R2", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "recibo_pre_selo", "selo_anterior_v396", "kernel_manifesto_anterior_v396"]
        presentes[rotulo] = {"arquivo_sha16": sha16(open(p, "rb").read()), "faltam": [c for c in lido if c not in d]}
        if presentes[rotulo]["faltam"]:
            falhas.append(("campo de %s lido pelos derivados e ausente do arquivo" % rotulo, presentes[rotulo]["faltam"]))
    else:
        presentes[rotulo] = {"arquivo": "ausente"}; falhas.append((arq, "ausente"))
DERJ = {"molde": {n: sha16(MOL[n].encode("utf-8")) for n in MOL}, "molde_confere_com_DERIVACAO_v396": MOLDE_CONFERE, "molde_derivar_cadeia_v396": sha16(open(os.path.join(MOLDE, "derivar_cadeia_v396.py"), "rb").read()),
        "derivados": {n: sha16(todos[n].encode("utf-8")) for n in todos}, "autorais": {n: sha16(autorais_txt[n].encode("utf-8")) for n in autorais_txt},
        "sobe": "395 -> 396 e 396 -> 397 numa passada so', fronteira de digitos (v/V/_sup/_f/_p/_m...); PROT (nao sobem): " + ", ".join(PROT),
        "o_que_difere_do_molde": {"chain": "cabecalho escrito para a v397; marcadores dos passos 3 e 9 = teste_de_veracidade_fase9_v397 e kh_n1_cobertura_v397; passo 0 exige quadro_v397.py e runtime_quadro_v397.py; passo 1 os copia byte a byte (o conferidor os importa); passo 3 diz o rc 3 da superficie; "
                                 "o resto e' o molde subido (passo 10 SIMPLES v396 -> v397, sem salto; pinos selo_anterior_v396 e kernel_manifesto_anterior_v396; kernel_recibo R3_2)",
                                 "leitura": "tres registros novos (teste_de_veracidade_fase9_v397, cunhagens_v397, kh_n1_cobertura_v397); o registro de veracidade conferido por inteiro (checagens, numeros == ESPERADOS, fontes por sha256, z_disc < 5, poder >= 5, resultado pinado, quadro selado nas duas linguas); "
                                            "a pedra Token no kernel do rito (bandeira True, trio, modulo da pedra, suporte, quatro falas por sha256); a face de Fock do psion CONDICIONAL (psibit_v395 e testemunha_estatica_v396); os registros da v396, v395, v394 e v393 seguem selados; "
                                            "AVISO da v397 (e de bloco v393 a v396) no stdout reprova; V['veracidade'], V['token'], V['reg397']",
                                 "superficies": "cabecalho e SEM COMPACTACAO: se o MEMORY.md (196 linhas em 23/10) passar de 195 linhas ou de 24.000 B depois da edicao, RECUSA com rc 3, sem escrever, e imprime as contagens; a ancora do handoff e' a linha do handoff da v396",
                                 "fechar": "o PARAGRAFO do README/site (T.paragrafo_readme: quadro_v397.paragrafo_pronto_readme sobre o core SELADO do Nos + verificacoes de quadro_v397.confere_md e da regra da ordem do 4,44 contra o resultado pinado) e' gerado e verificado ANTES de qualquer escrita (rc 2 se nao passar) e entra no handoff entre marcadores; o resto e' a subida de versao",
                                 "b3_recibo": "so' a subida de versao (a logica do B(n) simples nao muda; o harness a exercita com recibos sinteticos)",
                                 "harness": "os harness da v396 subidos + regras nomeadas (o registro de veracidade no lugar da testemunha; 19 controles negativos da leitura; etapa do paragrafo do README/site com 6 controles negativos e a regra do 4,44 em todo texto; ensaio do MEMORY.md em tres cenarios (real, com folga, no limite); "
                                            "no fechar: 2 controles negativos novos e a conferencia do paragrafo no handoff; refazer_out so' opcional com --nao-exigir-refazer e dito no resumo; rotas._valida sobre o registro SEM registrar)",
                                 "textos, registrar_mapa": "AUTORAIS (escritos para o delta da v397; nenhuma marca pendente)"},
        "marcas_texto_a_reescrever": {"por_arquivo": marcas, "total": sum(marcas.values())}, "campos_lidos_dos_arquivos_da_v397": campos, "arquivos_da_v397_no_pacote": presentes,
        "invariantes": conf, "sintaxe": sint, "guarda_p18": {k: ("LIMPO" if not v else v[:3]) for k, v in gv.items()}, "rotulos_estranhos": estranhos, "textos_definem_o_que_os_derivados_chamam": {"chamados": chamados, "faltam": faltam}, "falhas": falhas,
        "nao_validado": "nenhum derivado foi EXECUTADO contra o Nos real nem revisto por cetico independente; so' ast.parse, sh -n, invariantes, rotulos, guarda P18 e os harness (textos, leitura, superficies em COPIAS, b3_recibo, fechar e registrar_mapa em SANDBOX, tudo com recibos SINTETICOS e Nos EMULADO)"}
grava("DERIVACAO_v397.json", json.dumps(DERJ, ensure_ascii=False, indent=1))
print("DERIVADOS:", ", ".join("%s %s" % (n, DERJ["derivados"][n]) for n in DERJ["derivados"]))
print("AUTORAIS:", ", ".join("%s %s" % (n, DERJ["autorais"][n]) for n in DERJ["autorais"]))
print("SINTAXE:", json.dumps(sint, ensure_ascii=False))
print("MARCAS texto:", json.dumps(marcas, ensure_ascii=False))
print("INVARIANTES:", sum(len(v) for v in conf.values()), "conferidos;", "FALHAS:", falhas if falhas else "nenhuma")
sys.exit(1 if falhas else 0)
