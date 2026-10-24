# -*- coding: utf-8 -*-
"""derivar_cadeia_v398.py -- DERIVA a cadeia pos-rito da v398 a partir do molde REAL e FINAL da v397 (cadeia_de_selo/v397/pos_rito, o que RODOU de verdade em 23/10; seus arquivos conferem com a DERIVACAO_v397.json por sha16).
A subida de versao REUTILIZA o bump() e as listas PROT/FANTASMAS/FANT_PRE de derivar_encanamento_v398.py (a ferramenta de subida de versao da cadeia: 396 -> 397 e 397 -> 398 numa passada so', fronteira de digitos, nomes nascidos no
um.py PROTEGIDOS), com PROTECAO ADICIONAL de tres nomes que o bump subiria e nao devia (o QUADRO do Teste da Unica Palavra fica com o nome da v397: quadro_v397 / runtime_quadro_v397; e os marcadores INICIO/FIM_PARAGRAFO_README_v397 do
paragrafo do quadro, que o handoff da v398 repete como a v397 os gerou). Os registros da v397 (teste_de_veracidade_fase9_v397, cunhagens_v397, kh_n1_cobertura_v397, registros_v397) sao nomes PROTEGIDOS: onde o texto da v397 os usava como "os desta
versao", uma REGRA NOMEADA COM CONTAGEM EXATA os troca pelos da v398 (sonico_v398, afinacao_das_cordas_v398, cunhagens_v398, kh_n1_cobertura_v398, registros_v398); o script ABORTA se uma regra nao casar o numero esperado de vezes.
GERA: chain_pos_rito_v398.sh, leitura_v398.py, superficies_v398.py, fechar_v398.py, b3_recibo_v398.py (so' a subida: a logica do B(n) simples nao muda), harness_textos_ensaio_v398.py e harness_fechar_sandbox_v398.py (os harness da v397 subidos + regras).
CONFERE (autorais, escritos para a v398; a logica muda e uma derivacao mecanica nao a cobriria): textos_v398.py, registrar_mapa_v398.py (ast.parse, invariantes, guarda P18, nenhuma marca pendente, e cada T.<nome> chamado pelos derivados existe em textos_v398.py).
NAO executa nenhum script derivado: so' ast.parse, sh -n, invariantes, rotulos e a guarda de texto P18. Nao toca o Nos, a Bancada, a memoria, o Atlas, o mapa, o quadro, o tunel, o site nem o git; nada fora de pos_rito e' escrito.
Os numeros do cabecalho do chain (bandeiras, escada, geracao do B(n)) sao LIDOS de ESPERADOS_v398.json e PINOS_BN_v398.json aqui, nunca digitados.
GRAVA: DERIVACAO_v398.json (sha256 de ENTRADA e de SAIDA de cada arquivo; sha16 do molde, de cada derivado e de cada autoral; invariantes; sintaxe; marcas; rotulos; contagem de cada regra). Reexecutavel: o que muda ganha .bak_<STAMP>_c1 (backup de BYTES).
Uso: python -I -B -X utf8 derivar_cadeia_v398.py"""
import ast, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)
sys.path.insert(0, PK)
import derivar_encanamento_v398 as ENC      # bump(), PROT, FANTASMAS, FANT_PRE (reuso; nada e' executado no import)
MOLDE = os.path.join(os.path.dirname(PK), "v397", "pos_rito")
STAMP = time.strftime("%Y%m%d_%H%M%S")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
sha256 = lambda b: hashlib.sha256(b).hexdigest()
PALAVRA = "TEXTO_A_" + "REESCREVER"          # a palavra da marca, montada por concatenacao: este arquivo nunca a traz por extenso
MARCA = PALAVRA + "_V398"
MODELOS = ("leitura_v397.py", "superficies_v397.py", "fechar_v397.py", "chain_pos_rito_v397.sh", "b3_recibo_v397.py", "harness_textos_ensaio_v397.py", "harness_fechar_sandbox_v397.py")
AUTORAIS = ("textos_v398.py", "registrar_mapa_v398.py")
GUARDA_PENDENTE_RX = re.compile(r"(?m)^\s*#\s*" + MARCA)
EXTRA_PROT = ("quadro_v397", "INICIO_PARAGRAFO_README_v397", "FIM_PARAGRAFO_README_v397")     # o bump subiria estes tres e nao devia (ver o docstring)
REGRAS = []                                                                                    # (arquivo, nome, casou, esperado)


def sobe(t):
    """subida de versao em UMA passada (396 -> 397, 397 -> 398): o bump() de derivar_encanamento_v398, com os nomes extras protegidos por marcadores."""
    for i, p in enumerate(EXTRA_PROT):
        t = t.replace(p, "@@Q%d@@" % i)
    t = ENC.bump(t)
    for i, p in enumerate(EXTRA_PROT):
        t = t.replace("@@Q%d@@" % i, p)
    return t


def sem_hex(t, nome):
    """nenhuma ocorrencia de 396/397 dentro de uma palavra HEXADECIMAL (um hash seria subido por engano)."""
    for m in re.finditer(r"[0-9A-Za-z_]*(?<![0-9])39[67](?![0-9])[0-9A-Za-z_]*", t):
        w = m.group(0)
        assert not re.fullmatch(r"[0-9a-f]{8,}", w), ("a subida tocaria um hash hexadecimal", nome, w)


def rd(d, n):
    return open(os.path.join(d, n), "rb").read().decode("utf-8")


class Arq:
    """um arquivo em derivacao: guarda o nome para registrar a contagem de cada regra."""

    def __init__(self, nome, texto):
        self.nome = nome
        self.t = texto

    def tr(self, old, new, n=1, nome=""):
        """troca sobe(old) por `new` (texto FINAL, nunca subido), exigindo exatamente n ocorrencias; `old` e' o texto do MOLDE (v397)."""
        o = sobe(old)
        c = self.t.count(o)
        assert c == n, ("troca", self.nome, nome or old[:70], c, n)
        self.t = self.t.replace(o, new)
        REGRAS.append((self.nome, nome or old[:60], c, n))
        return self

    def tr_s(self, old_sobe, new, n=1, nome=""):
        """como tr, mas `old_sobe` ja' esta no texto DEPOIS da subida (nao e' subido de novo)."""
        c = self.t.count(old_sobe)
        assert c == n, ("troca_s", self.nome, nome or old_sobe[:70], c, n)
        self.t = self.t.replace(old_sobe, new)
        REGRAS.append((self.nome, nome or old_sobe[:60], c, n))
        return self

    def bloco(self, ini, fim):
        L = self.t.split("\n")
        a = [k for k, l in enumerate(L) if l.startswith(ini)]
        assert len(a) == 1, ("ancora inicial", self.nome, ini[:70], len(a))
        b = [k for k, l in enumerate(L) if k > a[0] and l.startswith(fim)]
        assert b, ("ancora final", self.nome, fim[:70])
        return a[0], b[0], L

    def subst_bloco(self, ini, fim, novo, nome=""):
        i, j, L = self.bloco(ini, fim)
        self.t = "\n".join(L[:i] + novo.rstrip("\n").split("\n") + L[j:])
        REGRAS.append((self.nome, nome or ("bloco " + ini[:50]), 1, 1))
        return self

    def subst_linha(self, prefixo, novo, nome=""):
        L = self.t.split("\n")
        a = [k for k, l in enumerate(L) if l.startswith(prefixo)]
        assert len(a) == 1, ("linha", self.nome, prefixo[:70], len(a))
        L[a[0]:a[0] + 1] = novo.rstrip("\n").split("\n")
        self.t = "\n".join(L)
        REGRAS.append((self.nome, nome or ("linha " + prefixo[:50]), 1, 1))
        return self

    def insere_antes(self, prefixo, novo, nome=""):
        L = self.t.split("\n")
        a = [k for k, l in enumerate(L) if l.startswith(prefixo)]
        assert len(a) == 1, ("insercao: ancora", self.nome, prefixo[:70], len(a))
        L[a[0]:a[0]] = novo.rstrip("\n").split("\n")
        self.t = "\n".join(L)
        REGRAS.append((self.nome, nome or ("insere antes de " + prefixo[:50]), 1, 1))
        return self

    def insere_depois(self, prefixo, novo, nome=""):
        L = self.t.split("\n")
        a = [k for k, l in enumerate(L) if l.startswith(prefixo)]
        assert len(a) == 1, ("insercao: ancora", self.nome, prefixo[:70], len(a))
        L[a[0] + 1:a[0] + 1] = novo.rstrip("\n").split("\n")
        self.t = "\n".join(L)
        REGRAS.append((self.nome, nome or ("insere depois de " + prefixo[:50]), 1, 1))
        return self


def grava(nome, texto):
    p = os.path.join(HERE, nome)
    b = texto.encode("utf-8")
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == b:
            return
        bk = p + ".bak_" + STAMP + "_c1"
        open(bk, "wb").write(raw)
        assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_" + STAMP
    open(tmp, "wb").write(b)
    assert os.path.getsize(tmp) == len(b)
    os.replace(tmp, p)
    assert open(p, "rb").read() == b


# =============================================================================== o molde (v397 FINAL) e os dados que o cabecalho do chain e as notas leem (nada digitado)
MOL_RAW = {n: open(os.path.join(MOLDE, n), "rb").read() for n in MODELOS}
MOL = {n: b.decode("utf-8") for n, b in MOL_RAW.items()}
for n_, tx_ in MOL.items():
    sem_hex(tx_, n_)
    fp_ = sorted({m.group(0) for m in ENC.FANT_PRE.finditer(tx_)})
    assert not fp_, ("o molde da v397 traz nome da v398 (a protecao falhou antes de comecar)", n_, fp_[:4])
DER97 = json.load(open(os.path.join(MOLDE, "DERIVACAO_v397.json"), encoding="utf-8"))
reg97 = dict(DER97["derivados"]); reg97.update(DER97["autorais"])
MOLDE_CONFERE = {n: (sha16(MOL_RAW[n]) == reg97.get(n)) for n in MODELOS}
assert all(MOLDE_CONFERE.values()), ("o molde da v397 difere da DERIVACAO_v397.json (foi editado depois da derivacao ou do rito?)", MOLDE_CONFERE)
ESP = json.load(open(os.path.join(PK, "ESPERADOS_v398.json"), encoding="utf-8"))
PIN = json.load(open(os.path.join(PK, "PINOS_BN_v398.json"), encoding="utf-8"))
_bp = PIN["recibo_pre_selo"]["bancada_pina"]
GER_ATUAL = int(re.match(r"^B(\d+)-", _bp["deployment_id"]).group(1))
assert _bp["version"] == "v397" and PIN["recibo_pre_selo"].get("sem_salto") is True and "cadeia_de_selos" not in PIN
N_FLAGS, N_SON, N_AFI = ESP["n_bandeiras_novas"], ESP["n_bandeiras_por_grupo"]["sonico"], ESP["n_bandeiras_por_grupo"]["afinacao"]
assert N_SON + N_AFI == N_FLAGS and ESP["kernel"]["modulos_novos"] == 2
ESC0, ESC1 = ESP["escada_v397_e_v398"]

# =============================================================================== leitura_v398.py
HEAD_L = ('# -*- coding: utf-8 -*-\n'
          '# A LEITURA da rodada v398 (molde: leitura_v397.py FINAL, o que rodou em 23/10): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v398, que aqui e\' o proprio pacote).\n'
          '# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e\' digitado: tudo sai dos JSON, do core, do selo e do stdout do rito.\n'
          '# v398: os registros NOVOS do core sao sonico_v398 e afinacao_das_cordas_v398 (com FUNCAO, no runtime: lidos NA FRACTALIZACAO DO UM, logo depois da testemunha_estatica_v396; cada um LE do kernel do proprio rito a composicao incondicional da sua pedra,\n'
          '# os termos que ela cita e as inscricoes de 23/10, e CONFERE um calculo) e cunhagens_v398 e kh_n1_cobertura_v398 (por spec; ESPERADOS[registros_v398]); os da v397 (teste_de_veracidade_fase9_v397, cunhagens_v397, kh_n1_cobertura_v397), os da v396, os da v395,\n'
          '# os da v394 e os da v393 seguem no core e tem de seguir selados. Os modulos novos de kernel (TGLExt/Sonico.lean e TGLExt/AfinacaoDasCordas.lean) vem de ESPERADOS[pedras_sha256] e sao conferidos aqui contra os arquivos do kernel do Nos.\n'
          '# A escada vem de ESPERADOS[escada_v397_e_v398] e ESPERADOS[escada]; a troca dita (so numeros) e\' a de ESPERADOS[troca_dita]. sonico_v398 e afinacao_das_cordas_v398 sao conferidos por inteiro (veredito == o do ensaio a seco, checagens, NUMEROS == ESPERADOS:\n'
          '# ln 2, exp(ln 2), a entropia do colapso em theta_M em nats e em oitavas; zeta(-1) = -1/12, zeta(-1, 1/2) = 1/24, D = 26, D = 10, d = 9; a hipotese MasslessFirstLevel segue KNOWN, a geometria OPEN, nada deriva cordas do axioma, o kappa do boost nao vem do core),\n'
          '# e cada pedra e\' conferida no kernel do rito (bandeira True, composicao no trio, modulo da pedra, contrato e suporte). cunhagens_v398: as SEIS inscricoes por sha256 (embedded_ok) e a sexta, e so\' ela, ROTULADA como da gerencia (nunca fala do operador).\n'
          '# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual: o registro teste_de_veracidade_fase9_v397 == ESPERADOS e == o resultado pinado, o quadro sela nas duas linguas, e a conferencia do rito diz que ele segue no topo (artigo PT/EN e .md).\n'
          '# A face de Fock do psion segue CONDICIONAL (psibit_v395 e testemunha_estatica_v396); as linhas `[v398]` e `[v397]` do stdout do rito dizem os vereditos e registros por spec selados == registros por spec; o AVISO da v398 (e de qualquer bloco v393 a v397) no stdout reprova.\n'
          '# Diferencas para a v397: os registros novos sao DESCOBERTOS por comparacao com ESPERADOS[vereditos_v397]; V[\'sonico\'], V[\'afinacao\'], V[\'cunhagens\'], V[\'pedras_kernel\'], V[\'reg398\'] e V[\'patch_ids\'] sao os campos da v398.\n')
NOVAS_CONSTS = '''REG_V393 = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")   # da v393: seguem no core e seguem selados (nao sao 'novos' da v398)
REG_V394 = ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394")   # da v394: seguem no core e seguem selados (nao sao 'novos' da v398)
REG_V395 = ("psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395")   # da v395: seguem no core e seguem selados (nao sao 'novos' da v398)
REG_V396 = ("testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396")   # da v396: seguem no core e seguem selados (nao sao 'novos' da v398)
REG_V397 = ("teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397")   # da v397 (o Teste da Unica Palavra, a pedra Token e as falas de 23/10): seguem no core e seguem selados (nao sao 'novos' da v398); o quadro do topo le o primeiro
REG_FIXOS = ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398")   # os QUATRO registros NOVOS do core v398 (dois com FUNCAO, no runtime; dois por spec); + os de ESPERADOS[registros_v398] (REG_TODOS, dentro de ler)'''
NOVAS_FUNCS = '''def _feq(a, b):
    """igualdade dos NUMEROS dos registros: floats com tolerancia relativa 1e-12 (a mesma maquina deve dar igual), o resto exato; recursiva em dict/list."""
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_feq(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_feq(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float):
        return a == b or abs(a - b) <= 1e-12 * max(1.0, abs(a), abs(b))
    return a == b


_BASE_CORE = {}


def _base_core(pk):
    """O core da v397 SELADA (copia de bytes em PK/base_v397): de onde saem o teorema e o modulo da face de Fock da testemunha (nenhum nome digitado); lido uma vez por caminho."""
    p = os.path.join(pk, 'base_v397', 'um_absoluto.json')
    if p not in _BASE_CORE:
        _BASE_CORE[p] = json.load(open(p, encoding='utf-8'))['core']
    return _BASE_CORE[p]


def _res_path(ev):
    """O resultado pinado do Teste da Unica Palavra: a copia em PK/insumos/fase9 (so' existe no SANDBOX do harness) ou, no real, a copia duravel da v397 (ESPERADOS[veracidade][resultado][duravel]); o sha256 e' conferido contra ESPERADOS em ambos."""
    nome = os.path.basename((ev.get('resultado') or {}).get('duravel') or 'ausente')
    loc = os.path.join(PK, 'insumos', 'fase9', nome)
    return loc if os.path.exists(loc) else ((ev.get('resultado') or {}).get('duravel') or loc)

'''
NOVO_CONF = '''        if C.get('tudo_bate') is not True:
            P.append('o conferidor NAO bateu')
        for l_ in ('pt', 'en', 'md'):
            if ((C.get('quadro') or {}).get(l_) or {}).get('ok') is not True:
                P.append('a conferencia do rito diz que o quadro do topo (O Teste da Unica Palavra, %s) NAO segue no topo com os numeros do resultado pinado' % l_)'''
NOVO_STDOUT = r'''    if [l for l in out.splitlines() if '[v398] AVISO' in l]:
        P.append('o stdout traz AVISO da v398 (o sonico, a afinacao das cordas ou os registros por spec nao rodaram): %s' % [l.strip()[:200] for l in out.splitlines() if '[v398] AVISO' in l][:2])
    elif [l for l in out.splitlines() if re.search(r'\[v39[3-7]\] AVISO', l)]:
        P.append('o stdout traz AVISO de um bloco anterior (v393 a v397): %s' % [l.strip()[:200] for l in out.splitlines() if re.search(r'\[v39[3-7]\] AVISO', l)][:2])
    for k_, r_ in (('sonico', 'sonico_v398'), ('afinacao', 'afinacao_das_cordas_v398')):
        ver_ = (ESP.get(k_) or {}).get('verdict')
        if not ver_ or ('>>> %s <<<' % ver_) not in out:
            P.append('o bloco %s do stdout nao traz a linha `>>> veredito <<<` do ensaio a seco' % r_)
    m_s8 = re.search(r'\[v398\] o sonico e a afinacao das cordas \(lidos na fractalizacao do Um\) e as inscricoes de 23/10 \(cunhagens_v398\): sonico=(\S+) \| afinacao=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s8 or (m_s8.group(1), m_s8.group(2), m_s8.group(3)) != ((ESP.get('sonico') or {}).get('verdict'), (ESP.get('afinacao') or {}).get('verdict'), (ESP.get('registros_v398') or {}).get('cunhagens_v398'))
            or m_s8.group(4) != m_s8.group(5) or int(m_s8.group(4)) != len(ESP.get('registros_v398') or {})):
        P.append('a linha [v398] do stdout (sonico, afinacao e cunhagens_v398; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v398') or {}), m_s8.groups()[3:] if m_s8 else 'ausente'))
    # as duas linhas [v397] que o main da v398 segue imprimindo (o Teste da Unica Palavra e as cunhagens da v397): iguais ao que a v397 selou
    m_tv = re.search(r'\[v397\] o Teste da Unica Palavra \(Fase 9 V2-c1, aberto uma vez em 23/10\), lido por hash ao lado do V1 \(nenhum sigma novo\): (\S+)', out)
    if not m_tv or m_tv.group(1) != (ESP.get('vereditos_v397') or {}).get('teste_de_veracidade_fase9_v397'):
        P.append('a linha [v397] do Teste da Unica Palavra esta ausente do stdout ou difere da que a v397 selou (%s)' % (m_tv.group(1)[:80] if m_tv else 'ausente'))
    n_spec7_ = len([k_ for k_ in REG_V397 if k_ != 'teste_de_veracidade_fase9_v397'])
    m_sp = re.search(r'\[v397\] a pedra Token e as falas de 23/10 \(cunhagens_v397\): (\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if not m_sp or m_sp.group(1) != (ESP.get('vereditos_v397') or {}).get('cunhagens_v397') or m_sp.group(2) != m_sp.group(3) or int(m_sp.group(2)) != n_spec7_:
        P.append('a linha [v397] das cunhagens da v397 esta ausente do stdout ou difere da que a v397 selou (registros por spec selados == %d)' % n_spec7_)'''
NOVO_V398 = r'''    # --- v398: os quatro registros novos conferidos contra o ensaio a seco registrado em ESPERADOS, e os da v397, da v396, da v395, da v394 e da v393, que seguem no core e tem de seguir selados; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    for k_ in REG_V393 + REG_V394 + REG_V395 + REG_V396 + REG_V397:
        if (core.get(k_) or {}).get('all_verified') is not True:
            P.append('%s (registro da v397, da v396, da v395, da v394 ou da v393) deixou de selar' % k_)
    RV_ = dict(ESP.get('vereditos_novos_v398') or {}); RV_.update(ESP.get('registros_v398') or {})   # registro -> veredito do ensaio a seco (sonico_v398 e afinacao_das_cordas_v398 sao runtime, com funcao; cunhagens_v398 e kh_n1_cobertura_v398 sao por spec)
    V['reg398'] = {}
    for k_ in REG_FIXOS:
        r_ = core.get(k_) or {}
        V['reg398'][k_] = {'verdict': r_.get('verdict'), 'ok': r_.get('all_verified')}
        esp_v_ = RV_.get(k_)
        if esp_v_ is None:
            P.append('ESPERADOS_v398 nao traz o veredito do ensaio a seco de %s (vereditos_novos_v398 / registros_v398): nao ha com que conferir' % k_)
        elif r_.get('verdict') != esp_v_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k_)
    kf_ = (core.get('kernel_formalization') or {})
    rf_ = core.get('rede_fock_v394') or {}   # limite dito: o contrato conjunto da rede segue NAO habitado (a face de Fock do psion depende dele)
    if rf_.get('whole_certificate_inhabited') is not False:
        P.append('rede_fock_v394: whole_certificate_inhabited deve seguir False (o contrato conjunto da rede segue aberto) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    if kf_.get('ext_bin394_0001') is not True:
        P.append('a bandeira da pedra da v394 (ext_bin394_0001) nao segue True no kernel do rito')
    # a face de Fock do psion segue como a v395 a selou: CONDICIONAL, sem habitante exibido, com a bandeira True e declarada em Psibit.lean (nem a v396, nem a v397, nem a v398 a habitam)
    pb_ = core.get('psibit_v395') or {}; pbc_ = pb_.get('conditional_psion_face') or {}
    if not (pbc_.get('status') == 'CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE' and pbc_.get('inhabitant_exhibited') is False and pbc_.get('flag_true') is True and kf_.get(pbc_.get('flag')) is True and pbc_.get('declared_in') == 'TGLExt/Psibit.lean'):
        P.append('psibit_v395: a face do psion deixou de estar como CONDICIONAL sem habitante exibido (bandeira True, declarada em TGLExt/Psibit.lean)')
    fkb_ = ((_base_core(PK).get('testemunha_estatica_v396') or {}).get('fock_face') or {})   # o que a v397 SELADA diz (copia de bytes): o teorema e o modulo da face de Fock, lidos, nao digitados
    te_ = core.get('testemunha_estatica_v396') or {}; fk_ = te_.get('fock_face') or {}
    if not (fk_.get('status') == 'CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE' and fk_.get('inhabitant_exhibited') is False and fk_.get('declared_outside_the_stone') is True and fk_.get('linked_to_the_corner_by_a_lemma') is False
            and fkb_.get('theorem') and fk_.get('theorem') == fkb_.get('theorem') and fkb_.get('declared_in') and fk_.get('declared_in') == fkb_.get('declared_in')):
        P.append('testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL, declarada em Psibit.lean fora da pedra e sem habitante exibido')
    # o registro teste_de_veracidade_fase9_v397 (o QUADRO do topo le os numeros dele): segue selado e igual, conferido por inteiro (os textos leem os numeros dele; NENHUM sigma e' calculado aqui)
    tv_ = core.get('teste_de_veracidade_fase9_v397') or {}; EV_ = ESP.get('veracidade') or {}
    ck_ = tv_.get('checks') or []; fo_ = {f_.get('chave'): f_ for f_ in (tv_.get('fontes') or []) if isinstance(f_, dict)}
    num_ = EV_.get('numeros_do_resultado') or {}; lido_ = tv_.get('lido') or {}
    nums_ok_ = bool(num_) and all(lido_.get(k_) == v_ for k_, v_ in num_.items())
    fontes_ok_ = bool(EV_.get('fontes')) and all((fo_.get(c_) or {}).get('sha256') == h_ and (fo_.get(c_) or {}).get('ok') is True for c_, h_ in EV_['fontes'].items())
    V['veracidade'] = {'verdict': tv_.get('verdict'), 'ok': tv_.get('all_verified'), 'n_checks': len(ck_), 'checks_ok': bool(ck_) and all(c_.get('ok') is True for c_ in ck_), 'lido': lido_, 'numeros_ok': nums_ok_,
                       'fontes': {c_: str(f_.get('sha256') or '') for c_, f_ in fo_.items()}, 'fontes_ok': fontes_ok_, 'does_not_gate_core': tv_.get('does_not_gate_core')}
    if not (tv_.get('all_verified') is True and tv_.get('does_not_gate_core') is True and len(ck_) == EV_.get('n_checks') and V['veracidade']['checks_ok'] and nums_ok_ and fontes_ok_ and tv_.get('verdict') == (ESP.get('vereditos_v397') or {}).get('teste_de_veracidade_fase9_v397')):
        P.append('teste_de_veracidade_fase9_v397 nao selou inteiro (selo, checagens, numeros lidos == ESPERADOS[veracidade], fontes por sha256): ver o registro no core')
    zd_, pw_ = lido_.get('z_disc_calibrado'), lido_.get('poder_previo')
    if not (isinstance(zd_, float) and zd_ < 5.0 and isinstance(pw_, float) and pw_ >= 5.0):
        P.append('o z_disc calibrado nao esta abaixo de 5 ou o poder previo nao e de 5 sigma ou mais (%r, %r): os textos e o quadro dizem que o degrau de 5 sigma da creditacao nao foi alcancado e que a TGL nao foi falsificada com poder' % (zd_, pw_))
    if PK not in sys.path:
        sys.path.insert(0, PK)
    try:
        import quadro_v397 as QV_
        rp_ = _res_path(EV_)
        rb_ = open(rp_, 'rb').read()
        if hashlib.sha256(rb_).hexdigest() != (EV_.get('fontes') or {}).get('f9v2_resultado'):
            P.append('o resultado pinado do Teste da Unica Palavra != o sha256 de ESPERADOS[veracidade][fontes][f9v2_resultado]')
        else:
            lr_ = QV_.lido_do_resultado(json.loads(rb_.decode('utf-8')))
            if not lr_ or any(lr_.get(k_) != lido_.get(k_) for k_ in lr_):
                P.append('os numeros que o registro leu != os do resultado pinado (lidos pelos mesmos caminhos de delta_v398.F9_CAMINHOS)')
        if QV_.Q._v397_atomos(tv_, 'pt').get('sealed') is not True or QV_.Q._v397_atomos(tv_, 'en').get('sealed') is not True:
            P.append('o quadro do Teste da Unica Palavra nao sela (algum numero ausente ou o registro nao selou): o artigo diria que o registro nao selou')
    except Exception as e_:   # noqa: BLE001
        P.append('nao consegui conferir o registro do Teste da Unica Palavra contra o resultado pinado: %r' % (e_,))
    # as DUAS pedras no kernel do rito e os dois registros com funcao, conferidos contra o ensaio a seco (ESPERADOS[sonico] e ESPERADOS[afinacao]); nenhum numero e' digitado
    TRIO_ = {'propext', 'Classical.choice', 'Quot.sound'}
    axr_ = kf_.get('axiom_report') or {}; src_ = kf_.get('declaration_sources_v394') or {}
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and set(axr_.get(n_)) <= TRIO_)
    NOME_PEDRA_ = {'sonico': 'Sonico', 'afinacao': 'AfinacaoDasCordas'}
    V['pedras_kernel'] = {}
    for key_, rn_ in (('sonico', 'sonico_v398'), ('afinacao', 'afinacao_das_cordas_v398')):
        ek_ = ESP.get(key_) or {}; rec_ = core.get(rn_) or {}
        th_ = (ESP.get('teoremas_das_pedras') or {}).get(key_); fl_ = (ESP.get('bandeiras_das_pedras') or {}).get(key_); rel_ = (ek_.get('unconditional') or {}).get('declared_in')
        contrato_ = (ESP.get('contrato_das_pedras') or {}).get(key_) or []; suporte_ = (ESP.get('suporte_das_pedras') or {}).get(key_) or {}
        un_ = rec_.get('unconditional') or {}; mec_ = rec_.get('mechanics') or {}; vals_ = rec_.get('values') or {}
        contrato_ok_ = bool(contrato_) and all(em_trio_(t_) and src_.get(t_) == rel_ for t_ in contrato_)
        suporte_ok_ = bool(suporte_) and all(em_trio_(t_) and src_.get(t_) == p_ for t_, p_ in suporte_.items())
        flag_true_ = bool(fl_) and kf_.get(fl_) is True
        kernel_ok_ = bool(th_ and fl_ and rel_ and flag_true_ and em_trio_(th_) and src_.get(th_) == rel_ and contrato_ok_ and suporte_ok_ and un_.get('in_kernel') is True and un_.get('flag_true') is True and un_.get('theorem') == th_
                          and un_.get('flag') == fl_ and rec_.get('exact_ladder') is True and rec_.get('embedded_source_ok') is True and all(v_ is True for v_ in (rec_.get('support_theorems') or {}).values()) and bool(rec_.get('support_theorems')))
        checks_ok_ = bool(mec_.get('checks')) and mec_.get('passed') is True and mec_.get('n_checks') == ek_.get('n_checks') and all(c_.get('ok') is True for c_ in mec_.get('checks'))
        values_ok_ = bool(ek_.get('values')) and _feq(vals_, ek_.get('values'))
        extra_ok_ = True
        if key_ == 'sonico':
            b0_ = core.get('beta')
            extra_ok_ = bool(rec_.get('beta_ok') is True and rec_.get('alpha_two_names_same') is True and isinstance(vals_.get('beta'), float) and isinstance(b0_, float) and abs(vals_['beta'] - b0_) <= 1e-9 * abs(b0_)
                             and all(v_ is True for v_ in (rec_.get('cited_outside') or {}).values()) and bool(rec_.get('cited_outside')))
        V['pedras_kernel'][key_] = {'rel': rel_, 'flag': fl_, 'flag_true': flag_true_, 'theorem': th_, 'axioms': axr_.get(th_), 'source': src_.get(th_), 'contrato_ok': contrato_ok_, 'suporte_ok': suporte_ok_, 'n_contrato': len(contrato_), 'n_suporte': len(suporte_)}
        V[key_] = {'verdict': rec_.get('verdict'), 'ok': rec_.get('all_verified'), 'n_checks': mec_.get('n_checks'), 'checks_ok': checks_ok_, 'values': vals_, 'values_ok': values_ok_, 'beta_ok': rec_.get('beta_ok'), 'flag': fl_, 'flag_true': flag_true_, 'theorem': th_,
                   'in_trio': em_trio_(th_) if th_ else False, 'declared_in': src_.get(th_) if th_ else None}
        if not kernel_ok_:
            P.append('a pedra %s nao esta no kernel do rito como o ensaio a seco a pinou (bandeira True, composicao incondicional no trio, proveniencia no modulo da pedra, contrato e suporte no trio e no modulo certo, escada exata, fonte embutida)' % NOME_PEDRA_[key_])
        if not (rec_.get('all_verified') is True and rec_.get('does_not_gate_core') is True and rec_.get('runtime_executed') is True and checks_ok_ and values_ok_ and rec_.get('verdict') == ek_.get('verdict') and extra_ok_ and not rec_.get('guarda_p18_violacoes')):
            P.append('%s nao selou inteiro (selo, checagens numericas, numeros == ESPERADOS[%s], veredito do ensaio a seco, beta/inscricoes): ver o registro no core' % (rn_, key_))
        if key_ == 'afinacao':
            hy_ = rec_.get('hypothesis') or {}
            if not (hy_ == (ek_.get('hypothesis') or {'x': 1}) and hy_.get('status') == 'KNOWN' and hy_.get('named_not_proved') is True and rec_.get('geometry') == 'OPEN' and rec_.get('derives_strings_from_the_axiom') is False and vals_.get('kappa_from_core') is None
                    and list((rec_.get('auxiliaries_outside_the_composition') or {})) == list(ek_.get('auxiliares_fora_da_composicao') or ['x']) and all(v_ is True for v_ in (rec_.get('auxiliaries_outside_the_composition') or {}).values())):
                P.append('afinacao_das_cordas_v398: a hipotese MasslessFirstLevel deixou de ser KNOWN (nomeada, nao provada), ou a geometria deixou de ser OPEN, ou o kappa veio do core, ou a TGL passou a derivar cordas do axioma, ou os auxiliares fora da composicao mudaram')
    # cunhagens_v398: as SEIS inscricoes por sha256 (embedded_ok) e a sexta, e so' ela, ROTULADA como da gerencia (nunca fala do operador)
    cu = core.get('cunhagens_v398') or {}; kh = core.get('kh_n1_cobertura_v398') or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = ESP.get('cunhagens') or {}
    ger_ = [k_ for k_, v_ in ec_.items() if str(v_.get('papel', '')).startswith('leitura da gerencia')]
    ger16_ = ger_[0][len('v398_cun_'):] if len(ger_) == 1 else None
    aut_ = cx_.get('autor_de_cada_inscricao') or {}
    rot_ok_ = bool(ger16_ and len(ec_) == 6 and aut_.get(ger16_) == 'gerencia' and sum(1 for a_ in aut_.values() if a_ == 'gerencia') == 1 and sum(1 for a_ in aut_.values() if a_ == 'operador') == len(ec_) - 1
                   and str((cx_.get('leitura_da_gerencia') or {}).get('sha16')) == ger16_ and str((cx_.get('leitura_da_gerencia') or {}).get('autor', '')).startswith('gerencia c1 (NAO e')
                   and aut_.get(str((cx_.get('leitura_da_gerencia') or {}).get('ratificada_pela_fala_de_sha16'))) == 'operador')
    verb_ok_ = bool(ec_) and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    V['cunhagens'] = {'n': len(vb_), 'verbatim_ok': verb_ok_, 'gerencia_sha16': ger16_, 'ratificada_pela': (cx_.get('leitura_da_gerencia') or {}).get('ratificada_pela_fala_de_sha16'), 'autores': aut_, 'rotulo_ok': rot_ok_, 'checks_ok': bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks')),
                      'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': pares_ok_}
    if not (verb_ok_ and V['cunhagens']['checks_ok'] and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and cx_.get('teoremas') == ESP.get('teoremas_das_pedras') and cx_.get('bandeiras') == ESP.get('bandeiras_das_pedras')
            and cx_.get('n_bandeiras_por_pedra') == ESP.get('n_bandeiras_por_grupo') and cx_.get('n_bandeiras') == ESP.get('n_bandeiras_novas') and cx_.get('cunhagens_embutidas') == len(ec_) and cx_.get('auxiliares_da_afinacao_fora_da_composicao') == (ESP.get('afinacao') or {}).get('auxiliares_fora_da_composicao')):
        P.append('cunhagens_v398: as inscricoes embutidas nao sao as de ESPERADOS (sha256, embedded_ok), ou as checagens do registro, ou os teoremas/bandeiras das pedras diferem do ensaio a seco')
    if not rot_ok_:
        P.append('cunhagens_v398: a leitura da gerencia nao esta rotulada como da gerencia (autor_de_cada_inscricao: a sexta, e so\' ela, e\' da gerencia; as outras cinco, do operador; a ratificacao e\' de uma fala do operador)')
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}   # o nome 'axiom_coverage_v392' e' do core (historico); segue na v398
    CB = ESP.get('cobertura_kh_n1') or {}
    V['kh'] = {'decl': cov.get('decl'), 'thm': cov.get('thm'), 'fora': cov.get('fora_do_trio'), 'nao_lidas': cov.get('nao_lidas_pelo_regex'), 'verdict': kh.get('verdict')}
    V['cunh_verdict'] = cu.get('verdict')
    if not (CB and cov.get('ok') is True and cov.get('decl') == CB.get('decl') and cov.get('thm') == CB.get('thm') and cov.get('fora_do_trio') == 0 and cov.get('nao_lidas_pelo_regex') == CB.get('nao_lidas_pelo_regex')):
        P.append('cobertura KH-N1 do rito != ESPERADOS (constantes, teoremas, fora do trio, nao lidas) ou ESPERADOS sem cobertura_kh_n1')'''


def deriva_leitura():
    a = Arq("leitura_v398.py", sobe(MOL["leitura_v397.py"]))
    i = a.t.index("import glob, hashlib, json, os, re, sys, datetime")
    a.t = HEAD_L + a.t[i:]
    a.subst_bloco("REG_V393 = (", "sha = lambda p:", NOVAS_CONSTS, nome="constantes dos registros")
    a.tr("REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v397') or ())))", "REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v398') or ())))", 1, "REG_TODOS: registros_v398")
    a.insere_antes("def ler():", NOVAS_FUNCS, nome="_feq, _base_core, _res_path")
    a.tr("        if C.get('tudo_bate') is not True:\n            P.append('o conferidor NAO bateu')", NOVO_CONF, 1, "conferencia: o quadro segue no topo")
    a.subst_bloco("    if [l for l in out.splitlines() if '[v398] AVISO' in l]:", "    hp = os.path.join(PK, 'rito_horarios_v398.txt')", NOVO_STDOUT, nome="stdout: AVISO e linhas [v398] e [v397]")
    a.subst_bloco("    # --- v398: os registros novos conferidos", "    qp = core.get('quantum_pillar_v384')", NOVO_V398, nome="registros novos da v398")
    for proibido in ("V['testemunha']", "V['token']", "V['reg397']", "REG_V398", "ESP.get('fock_face_teorema')", "ESP.get('pedra')", "ts_.get('values')", "registros_v397", "vereditos_novos_v397", "bandeiras_do_suporte", "teorema_da_pedra", "bandeira_da_pedra", "escada_v396"):
        assert proibido not in a.t, ("sobrou na leitura:", proibido)
    ast.parse(a.t)
    return a


# =============================================================================== superficies_v398.py
CAB_S = ("# Registro da v398 SELADA nas superficies de memoria (molde: superficies_v397.py FINAL, o que rodou em 23/10), pela regra da linhagem completa.\n"
         "# Diario (MEMORIA_DA_LINHAGEM, append datado), desenho (ADENDO), Atlas (append datado), TGL_CORE_MEMORY (append datado), o CLAUDE.md da Haja_Luz (SEM errata nova no CLAUDE.md da raiz), as memorias-topico (missao, central, estatuto, e o topico NOVO da v398),\n"
         "# o MEMORY.md/MEMORY_2.md, e (so' sob reivindicacao nomeada em V398_AVISO_REIVINDICACAO) o AVISO_GERENCIA.md da ORDEM_019.\n"
         "# SEM erratas inline nesta versao (as erratas da v398 vao DENTRO dos blocos datados). A funcao inserir_ao_lado fica disponivel (nao e' chamada).\n"
         "# Duas fases (plano conferido ANTES da primeira escrita); backup de BYTES (.bak_<STAMP>_sup398); temporario -> conferir tamanho -> substituir; idempotente pelo marcador de cada bloco;\n"
         "# fim de linha de cada arquivo respeitado. GUARDA: so' grava se a leitura nao tiver problema E se a guarda de texto (P18, cinco regras) estiver limpa em todo texto novo.\n"
         "# Ensaio: --copias <pasta com copias dos alvos> (nada real e' tocado). MEMORY.md: ate 24.000 B e 195 linhas. ESTA SUPERFICIE NAO COMPACTA NADA (nem reguas, nem ganchos antigos): se o indice DEPOIS da edicao (a linha do handoff novo mais a troca do gancho da missao,\n"
         "# que movem a velha VERBATIM ao MEMORY_2.md) passar de 195 linhas ou de 24.000 B, RECUSA com rc 3 SEM escrever nada e imprime as contagens (linhas antes, depois, limite) para a gerencia decidir o que sai do indice.\n"
         "# A linha do handoff novo entra ANTES da linha do handoff da v397 (que a custodia da v397 reescreveu e que segue VERBATIM: conferida presente no MEMORY.md real em 23/10, uma so').\n")


def deriva_superficies():
    a = Arq("superficies_v398.py", sobe(MOL["superficies_v397.py"]))
    i = a.t.index("# Registro da v398 SELADA"); j = a.t.index("import os, re, sys, time")
    a.t = a.t[:i] + CAB_S + a.t[j:]
    REGRAS.append((a.nome, "cabecalho", 1, 1))
    a.tr("def guarda(texto, onde):\n    v = violacoes(texto)\n    if v:\n        VIOLACOES.append((onde, v[:3]))\n",
         "def guarda(texto, onde):\n    v = violacoes(texto)\n    if v:\n        VIOLACOES.append((onde, v[:3]))\n    at = T.atribuicao_da_gerencia(texto)   # v398: a leitura da gerencia nunca entre aspas como fala do operador, e a sexta inscricao sempre rotulada\n    if at:\n        VIOLACOES.append((onde + ' (atribuicao da gerencia)', at[:3]))\n", 1, "guarda: atribuicao da gerencia")
    assert "sup397" not in a.t and "V397_AVISO" not in a.t and "(handoff-v397-custodia.md)" in a.t and "- [HANDOFF v397" in a.t and "V398_AVISO_REIVINDICACAO" in a.t and "compacta" in a.t and "_sup398" in a.t and "textos_v398" in a.t
    ast.parse(a.t)
    return a


# =============================================================================== fechar_v398.py
DOC_F = r'''"""fechar_v398.py -- DEPOIS da cadeia pos-rito e do elo B(n) (molde: fechar_v397.py FINAL): (1) o manifesto de incorporacao v398 -> pos_rito e a pasta das ferramentas;
(2) o ARQUIVO: o indice por sha256 de tudo o que esta na pasta da cadeia (work\\cadeia_de_selo\\v398 -- aqui o pacote JA mora na casa duravel, nao ha copia do pacote), a copia de
pos_rito -> work\\cadeia_de_selo\\v398_selo e do kernel (work\\cadeia_de_selo\\v398\\kernel e, se existir, work\\v398_kernel; mais as pedras do Nos) -> work\\cadeia_de_selo\\v398_kernel;
(3) os DOIS DIFFS para o auditor independente: DIFF_v397_v398.diff (um.py da base x o selado, GNU diff -U2) e DIFF_KERNEL_v398.txt (o kernel embutido, molde do v390);
(4) o HANDOFF (memory\\handoff-v398-custodia.md + Nos\\HANDOFF_v398_CUSTODIA.md) para a sessao do site, que TRAZ PRONTOS PARA COLAR OS DOIS PARAGRAFOS do README do espelho e do site: (a) o do QUADRO «O Teste da Unica Palavra» (v397, intocado),
gerado pelas MESMAS funcoes do quadro do artigo (quadro_v397.paragrafo_pronto_readme) sobre o core SELADO do Nos, mesmos numeros e estatutos; (b) o NOVO, «Sonico e a afinacao das cordas (v398)», gerado dos registros selados sonico_v398, afinacao_das_cordas_v398
e cunhagens_v398 (numeros LIDOS do core, estatutos, limites, sem o 4,44).
GUARDAS: a leitura sem problema; o PARAGRAFO DO QUADRO passa nas verificacoes do quadro contra o resultado pinado (quadro_v397.confere_md e a regra da ordem: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item; frase do operador verbatim; numeros
iguais aos do resultado); o PARAGRAFO NOVO passa na verificacao propria (T.verificar_paragrafo_sonico: numeros == ESPERADOS e == o gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim das falas do operador; a sexta inscricao rotulada como da gerencia) --
se QUALQUER um nao passar, o fechar RECUSA (rc 2) ANTES de escrever qualquer coisa e o handoff nao nasce; os tres RECIBOS do B(n) (o RECIBO_SINCRONIZACAO_v398_*.json do 10-bis, o recibo da PARADA do servico e o do RELIGAMENTO) -- sem eles o fechar RECUSA e o handoff nao nasce;
a guarda de texto P18 no handoff.
Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""'''
NOVO_F0 = r'''# ---------------------------------------------------------------- (0) os PARAGRAFOS PRONTOS do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO), as MESMAS funcoes do quadro do artigo sobre o core SELADO do Nos; (2) o paragrafo NOVO do sonico e da afinacao
# das cordas, gerado dos registros selados e verificado contra o core e contra ESPERADOS (sem o 4,44; citacoes verbatim das falas do operador; a sexta inscricao rotulada como da gerencia); sem passar nas verificacoes, RECUSA (rc 2) ANTES de escrever qualquer coisa
try:
    PAR, PAR_INFO = T.paragrafo_readme()
    PAR_S, PAR_S_INFO = T.paragrafo_sonico()
except BaseException as e_:   # noqa: BLE001
    print("FECHAR RECUSADO: um dos paragrafos prontos do README e do site (o quadro O Teste da Unica Palavra, v397, ou o do sonico e da afinacao das cordas) nao passou nas verificacoes (regra da ordem do 4,44; frase verbatim; numeros iguais aos do resultado pinado e aos de ESPERADOS; sexta inscricao rotulada como da gerencia):", repr(e_)[:700]); sys.exit(2)'''


def deriva_fechar():
    a = Arq("fechar_v398.py", sobe(MOL["fechar_v397.py"]))
    a.subst_bloco('"""fechar_v398.py', "import glob, hashlib, json, os, shutil, subprocess, sys, time", DOC_F, nome="docstring")
    a.subst_bloco("# ---------------------------------------------------------------- (0) o PARAGRAFO PRONTO", "NOS = L.NOS; WK =", NOVO_F0, nome="paragrafos prontos antes de escrever")
    a.tr('"registros_v397": V["registros"], "readme_paragrafo": {"sha16": hashlib.sha256(PAR.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_INFO}, ',
         '"registros_v398": V["registros"], "readme_paragrafo": {"sha16": hashlib.sha256(PAR.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_INFO}, "readme_paragrafo_sonico": {"sha16": hashlib.sha256(PAR_S.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_S_INFO}, ', 1, "manifesto: os dois paragrafos")
    a.tr('_k = {"readme_paragrafo": PAR, "ap_nome": ', '_k = {"readme_paragrafo": PAR, "readme_paragrafo_sonico": PAR_S, "ap_nome": ', 1, "k do handoff")
    for proibido in ("AO_CLAUDE", "_dd", "AJUSTAR", "_f397", "psibit", "registros_v397", "TestemunhaEstatica"):
        assert proibido not in a.t.replace("V398_AVISO", ""), ("sobrou no fechar:", proibido)
    assert "T.paragrafo_readme()" in a.t and "T.paragrafo_sonico()" in a.t and "FECHADO v398:" in a.t and "_f398" in a.t and "registros_v398" in a.t
    ast.parse(a.t)
    return a


# =============================================================================== b3_recibo_v398.py (a logica do B(n) simples nao muda: so' a subida; o harness a exercita com recibos SINTETICOS)
def deriva_b3():
    a = Arq("b3_recibo_v398.py", sobe(MOL["b3_recibo_v397.py"]))
    assert "v397" in a.t and "v396" not in a.t and "PINOS_BN_v398.json" in a.t and 'r.get("versao_alvo") != "v398"' in a.t and 'ma.get("version") != "v397"' in a.t and "B%d-v398-" in a.t
    ast.parse(a.t)
    return a


# =============================================================================== chain_pos_rito_v398.sh
HEADER = '''#!/bin/sh
# v398 (23/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v397.sh FINAL (o que rodou em 23/10; derivada por derivar_cadeia_v398.py; mesma ordem de passos 0..14 e mesmos portoes). O rito ja terminou (rito_v398.sh em segundo plano;
# RITO_RC=<rc> no fim do Nos\\rodada_v398_stdout.txt). A v398 e' um DELTA PEQUENO: {nmod} modulos novos de kernel (TGLExt/Sonico, o NOME «sonico» que o operador deu em 23/10; e TGLExt/AfinacaoDasCordas, pedra e nome ratificados por ele; {nf} bandeiras: {ns} e {na}),
# os registros COM FUNCAO sonico_v398 e afinacao_das_cordas_v398 (lidos NA FRACTALIZACAO DO UM, logo depois da testemunha_estatica_v396; cada um LE do kernel do proprio rito a composicao incondicional da sua pedra e CONFERE um calculo; nomes PROVISORIOS),
# os registros por spec cunhagens_v398 (as SEIS inscricoes de 23/10: cinco falas do operador e a leitura da GERENCIA que ele ratificou, esta ROTULADA como da gerencia) e kh_n1_cobertura_v398, e a secao «Sonico e a afinacao das cordas» do artigo PT/EN e do .md canonico.
# O QUADRO «O Teste da Unica Palavra» (v397, a regra do 4,44) PERMANECE no topo do artigo e do .md, INTOCADO: o conferidor e a leitura o conferem de novo; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item) segue valendo em TODO texto que o cite.
# ORDEM: 0 guardas -> 1 o CONFERIDOR (copia byte a byte, com o delta_v398.py, o quadro_v397.py e o runtime_quadro_v397.py que ele importa; so leitura do Nos) -> 2 a LEITURA (PROBLEMAS param) -> 3 ENSAIO das superficies em COPIAS
# (o plano e' conferido antes da primeira escrita; a arvore em dry; o sha16 da v398 na arvore (dry) e os marcadores do passo 9 nas COPIAS, conferidos ANTES de qualquer escrita real; se o MEMORY.md passaria de 195 linhas, a superficie RECUSA
# com rc 3 e a cadeia PARA aqui, sem tocar nada real: a superficie NAO compacta o indice) -> 4 patch arvore/indice (OPCIONAL: so' se existir patch_arvore_indice_v398.py) -> 5 a arvore -> 6 atlas+indice -> 7 superficies reais (appends datados;
# SEM errata nova no CLAUDE.md da raiz) -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e' falha visivel) e a guarda de MEMORY.md (<24.000 B, <=195 linhas) -> 10 B(n) da Bancada,
# ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(n) APLICAR (so com B3_AUTORIZADO=sim e o evento c1) -> 10c religamento (AGUARDA_OPERADOR) -> 11 fechar (o handoff TRAZ os DOIS paragrafos do README e do site: o do quadro do 4,44, intocado, e o do sonico e da afinacao) -> 12 registrar_mapa
# (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V398_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito).
# PASSO 10 SEM SALTO: a Bancada de producao pina a v397 (B{ger}, {depl}) e o Nos e' a v397 ate' a instalacao; portanto o B(n) da v398 e' um passo SIMPLES v397 -> v398 (esboco R3.5, sincronizar_bancada.py): NAO ha a opcao de cadeia de selos
# do esboco, nem o pino correspondente, e o b3_recibo_v398.py NAO tem o 3o argumento. Os pinos vem de PINOS_BN_v398.json (lidos na hora; hash nunca de memoria): criterios, esboco_R3_5, gerador_bateria, driver_t12_t14, bateria_base_R2,
# kernel_recibo (o KERNEL_RECIBO_v398.json, contrato R3_2: a v398 nao acrescenta modulo de auditoria), candidato, esperados, pins_do_candidato, recibo_pre_selo (gerado antes da instalacao; veredito JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA),
# selo_anterior_v397 e kernel_manifesto_anterior_v397 (as copias de bytes do selo e do manifesto do kernel da v397, em base_v397). A BATERIA da v398 e' GERADA por script no 10 (depois do selo; bateria por versao) e pinada ao lado
# (bateria_pos_selo/PINOS_BATERIA_v398.json).
# Vereditos esperados (lidos do codigo do esboco, nao rodados): ensaio REPINADA_B<n>__ENSAIO__NADA_GRAVADO_NA_BANCADA e aplicar REPINADA_B<n>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_, com n = a geracao do manifesto que a
# Bancada pina + 1 (B{ger} -> n = {prox}; o b3_recibo_v398.py o confere). A parada do servico (10a) e o religamento (10c) sao ato do operador (V398_AUTORIZACAO_OPERADOR nos scripts bancada_B3_servico\\recibo_parada_v398.py e recibo_religamento_v398.py); o chain so' confere os recibos.
# textos_v398.py, fechar_v398.py e registrar_mapa_v398.py RECUSAM rodar se tiverem trecho marcado para reescrever: os passos 0 a 2 nao os usam. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como na v397, com os rotulos da v398.
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).'''.format(nmod=ESP["kernel"]["modulos_novos"], nf=N_FLAGS, ns=N_SON, na=N_AFI, ger=GER_ATUAL, depl=_bp["deployment_id"], prox=GER_ATUAL + 1)
MARC_MOLDE = '"teste_de_veracidade_fase9_v397" "kh_n1_cobertura_v397"'
MARC_NOVO = '"sonico_v398" "kh_n1_cobertura_v398"'


def deriva_chain():
    a = Arq("chain_pos_rito_v398.sh", sobe(MOL["chain_pos_rito_v397.sh"]))
    i, j, L = a.bloco("#!/bin/sh", "PK=")
    a.t = "\n".join([HEADER] + L[j:])
    REGRAS.append((a.nome, "cabecalho", 1, 1))
    # os marcadores dos passos 3 e 9: o registro com funcao do sonico e o kh_n1 da v398 (6 ocorrencias: 3 no ensaio das copias, 3 nas superficies reais)
    a.tr_s(MARC_MOLDE, MARC_NOVO, n=6, nome="marcadores dos passos 3 e 9")
    for proibido in ("--cadeia-de-selos", "W_CAD", "$CAD", "SALTO v392", "R3_4", "fundir_pinos", "psibit_v398", "selo_anterior_v396", "base_v396", "textos_v397", "leitura_v397", "fechar_v397", "PINOS_BN_v397", "testemunha_estatica_v398", "teste_de_veracidade_fase9_v397", "B6-v396"):
        assert proibido not in a.t, ("resto da v397 na cadeia", proibido)
    return a


# =============================================================================== harness_textos_ensaio_v398.py
DOC_HT = r'''"""harness_textos_ensaio_v398.py -- o HARNESS DO POS-RITO da v398 em modo ENSAIO (derivado do harness_textos_ensaio_v397.py, que rodou na v397); SO' LEITURA do Nos real, da producao e das superficies reais.
Importa os modulos REAIS textos_v398.py e leitura_v398.py (os que a cadeia usa) e os executa contra um NOS EMULADO montado de dry_v398 (core_ensaio.json -> um_absoluto.json, selo_ensaio.json -> um_absoluto_selo.json, o um.py candidato, o kernel,
o .md, o artigo PT/EN e o sumario; o stdout do rito e o APLICADO_AO_CANONICO sao EMULADOS e ditos). Tudo o que ele escreve fica em pos_rito\\harness_saida_v398\\ (e o resumo HARNESS_TEXTOS_ENSAIO_v398.json ao lado dele); nada do Nos real,
da memoria, do Atlas, do mapa de rotas, da Bancada ou do git e' tocado; nenhum rito e' rodado.
O que ele prova (cada etapa e' uma entrada do resumo):
  precondicoes   o candidato (ESPERADOS == CANDIDATO == arquivo == dry_v398/um.py) e a regeneracao terminada (refazer_out_v398.txt mostra '== FIM'); a evidencia carrega mtime e sha16 de cada entrada;
  conferidor     o conferir_rito_v398.py REAL (copia, com delta_v398, quadro_v397 e runtime_quadro_v397) roda contra o Nos emulado (V398_NOS) e da' TUDO BATE: a conferencia que a leitura le;
  leitura        a leitura_v398.ler() REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS (selo de outra versao, registro ausente, registro nao selado, numero adulterado no sonico e na afinacao, bandeira falsa, composicao fora do trio, hipotese dita derivada,
                 geometria dita fechada, a TGL derivando cordas do axioma, o kappa vindo do core, a leitura da gerencia rotulada como do operador, inscricao embutida adulterada, quadro do topo que deixa de selar ou de estar no topo, registros da v397 a v393 nao selados,
                 face de Fock habitada ou dita dentro da pedra, AVISO da v398 ou de bloco anterior, linhas [v398] e [v397] ausentes), cada um tem de reprovar;
  textos         todas as funcoes publicas de textos_v398 renderizam, a guarda P18 fica limpa em cada saida, os marcadores que a cadeia exige estao nos textos, a errata da palavra «teoremas» esta nos textos que carregam _num;
  paragrafos     o PARAGRAFO DO QUADRO (textos_v398.paragrafo_readme, o da v397, intocado) passa nas verificacoes do quadro contra o resultado pinado e os CONTROLES NEGATIVOS reprovam: o 4,44 sem o p calibrado, o 4,44 sem a linha dos 5 sigma, numero adulterado, p adulterado,
                 a frase do operador parafraseada entre aspas, o 4,44 numa linha fora do item; a regra da ordem vale para TODO texto renderizado; e o PARAGRAFO NOVO (textos_v398.paragrafo_sonico) passa na verificacao propria, com controles negativos (numero adulterado, a gerencia como
                 operador, citacao nao verbatim, o 4,44 intruso, estatuto removido, texto da gerencia entre aspas); mais a atribuicao da gerencia em todo texto renderizado;
  cita_so_o_que_existe   cada `termo` entre crases de cada texto e' achado no kernel do Nos emulado, no um.py, nos insumos, nos arquivos ou como hash lido (o que nao e' achado e' dito e reprova);
  superficies    superficies_v398.py REAL roda em COPIAS das superficies reais em TRES cenarios: (a) o MEMORY.md real como esta (a superficie NAO compacta: se ele passar de 195 linhas depois da edicao, tem de RECUSAR com rc 3 sem escrever nada; senao, o caminho normal),
                 (b) um MEMORY.md com FOLGA (copia reduzida): o plano e' conferido antes da primeira escrita, idempotente na 2a rodada, marcadores do passo 9, <= 195 linhas e < 24 000 B, (c) um MEMORY.md NO LIMITE (195 linhas): tem de RECUSAR com rc 3, imprimir as
                 contagens e nao escrever nada em nenhuma copia; os originais nao mudam;
  b3_recibo      b3_recibo_v398.py REAL contra recibos SINTETICOS derivados dos recibos reais da v397 (positivos e negativos);
  mapa           registrar_mapa_v398.montar() REAL contra o core emulado e o livro de rotas real (so' leitura), e cada registro validado pela MESMA funcao que o mapa usa (rotas._valida), SEM registrar; grava registro_mapa_v398_ENSAIO.json (nao e' o registro);
  marcas         nenhuma linha de comentario com a marca de texto pendente em pos_rito\\*.py; ast.parse de todo .py e sh -n do chain.
uso: python -I -B -X utf8 harness_textos_ensaio_v398.py [--sem-superficies] [--sem-b3] [--sem-negativos] [--rotulo <nome>] [--nao-exigir-refazer] [--manter-copias]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita, nada foi rodado;
--nao-exigir-refazer: NAO exige refazer_out_v398.txt (nem o '== FIM' nem as datas): modo de ENSAIO antes de a gerencia regerar o candidato; o resumo e o veredito DIZEM que a regeneracao nao foi comprovada;
sem --manter-copias o Nos emulado e as copias pesadas das superficies sao apagados no fim, so' dentro de harness_saida_v398)"""'''
NEW_STD = r'''N_ = ESP["escada"][1]; n_spec = len(ESP["registros_v398"]); n_spec7 = len([k for k in ("cunhagens_v397", "kh_n1_cobertura_v397") if k in ESP["vereditos_v397"]])
STDOUT_EMULADO = "\n".join(["[v398] EMULADO PELO HARNESS (nao e' o stdout de um rito; so' as linhas que a leitura confere)",
                            "SONICO [v398 -- EMULADO]:", "  >>> %s <<<" % ESP["sonico"]["verdict"], "AFINACAO DAS CORDAS [v398 -- EMULADO]:", "  >>> %s <<<" % ESP["afinacao"]["verdict"],
                            "   [v397] o Teste da Unica Palavra (Fase 9 V2-c1, aberto uma vez em 23/10), lido por hash ao lado do V1 (nenhum sigma novo): %s" % ESP["vereditos_v397"]["teste_de_veracidade_fase9_v397"],
                            "   [v397] a pedra Token e as falas de 23/10 (cunhagens_v397): %s | registros por spec: %d (selados %d)" % (ESP["vereditos_v397"]["cunhagens_v397"], n_spec7, n_spec7),
                            "   [v398] o sonico e a afinacao das cordas (lidos na fractalizacao do Um) e as inscricoes de 23/10 (cunhagens_v398): sonico=%s | afinacao=%s | cunhagens=%s | registros por spec: %d (selados %d)" % (ESP["sonico"]["verdict"], ESP["afinacao"]["verdict"], ESP["registros_v398"]["cunhagens_v398"], n_spec, n_spec),
                            "teoremas limpos: %s/%s" % (N_, N_), ">>> TGL_KERNEL_STAGE1_VERIFIED", "[selo] rite_checkpoints: chave desligada ; reaproveitados 0", "FAIL_CLOSED_SELFTEST_PASSED", "[selo] colapso tipado: EMULADO", "RITO_RC=0", ""])
open(os.path.join(NOSE, "rodada_v398_stdout.txt"), "w", encoding="utf-8", newline="\n").write(STDOUT_EMULADO)'''
NEW_VARIANTE = r'''def variante(nome, f_core=None, f_selo=None, f_std=None, f_conf=None, espera=""):
    """aplica a variante nos arquivos do Nos emulado (e da conferencia do rito), roda a leitura, RESTAURA os bytes e confere que reprovou (com o trecho esperado na mensagem)."""
    try:
        if f_core:
            c = json.loads(core_raw.decode("utf-8")); f_core(c["core"]); open(core_path, "wb").write(json.dumps(c, ensure_ascii=False).encode("utf-8"))
        if f_selo:
            s = json.loads(selo_raw.decode("utf-8")); f_selo(s); open(selo_path, "wb").write(json.dumps(s, ensure_ascii=False).encode("utf-8"))
        if f_std:
            open(std_path, "wb").write(f_std(std_raw.decode("utf-8")).encode("utf-8"))
        if f_conf:
            cj = json.loads(conf_raw.decode("utf-8")); f_conf(cj); open(conf_path, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
        _, PV = L.ler()
    finally:
        open(core_path, "wb").write(core_raw); open(selo_path, "wb").write(selo_raw); open(std_path, "wb").write(std_raw)
        if os.path.exists(conf_path):
            open(conf_path, "wb").write(conf_raw)
    ok = any(espera in x for x in PV)
    return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": ok, "problemas": [x[:140] for x in PV][:3]}

'''
NEG_HT = r'''def _sem_sonico(c):
    c.pop("sonico_v398", None)


def _sem_afinacao(c):
    c.pop("afinacao_das_cordas_v398", None)


def _nao_sela_cunh(c):
    c["cunhagens_v398"]["all_verified"] = False


def _nao_sela_kh(c):
    c["kh_n1_cobertura_v398"]["all_verified"] = False


def _sonico_ln2(c):
    c["sonico_v398"]["values"]["ln2"] = 0.69314719


def _sonico_entropia(c):
    c["sonico_v398"]["values"]["collapse_entropy_theta_M_nats"] = 0.0651


def _sonico_entropia_oitavas(c):
    c["sonico_v398"]["values"]["collapse_entropy_theta_M_octaves"] = 0.094


def _sonico_cheque_falha(c):
    c["sonico_v398"]["mechanics"]["checks"][2]["ok"] = False


def _sonico_move_gate(c):
    c["sonico_v398"]["does_not_gate_core"] = False


def _sonico_bandeira_falsa(c):
    c["kernel_formalization"][ESP["bandeiras_das_pedras"]["sonico"]] = False


def _sonico_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][ESP["teoremas_das_pedras"]["sonico"]] = ["propext", "sorryAx"]


def _sonico_suporte_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][sorted(ESP["suporte_das_pedras"]["sonico"])[0]] = ["propext", "sorryAx"]


def _afinacao_zeta(c):
    c["afinacao_das_cordas_v398"]["values"]["zeta_minus_one"] = "-1/11"


def _afinacao_dimensao(c):
    c["afinacao_das_cordas_v398"]["values"]["bosonic_critical_dimension"] = 25


def _afinacao_d_da_casa(c):
    c["afinacao_das_cordas_v398"]["values"]["house_spatial_dimension"] = 10


def _afinacao_hipotese(c):
    c["afinacao_das_cordas_v398"]["hypothesis"]["status"] = "DERIVED"


def _afinacao_hipotese_provada(c):
    c["afinacao_das_cordas_v398"]["hypothesis"]["named_not_proved"] = False


def _afinacao_geometria(c):
    c["afinacao_das_cordas_v398"]["geometry"] = "CLOSED"


def _afinacao_deriva(c):
    c["afinacao_das_cordas_v398"]["derives_strings_from_the_axiom"] = True


def _afinacao_kappa(c):
    c["afinacao_das_cordas_v398"]["values"]["kappa_from_core"] = 1.0


def _afinacao_bandeira_falsa(c):
    c["kernel_formalization"][ESP["bandeiras_das_pedras"]["afinacao"]] = False


def _afinacao_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][ESP["teoremas_das_pedras"]["afinacao"]] = ["propext", "sorryAx"]


def _gerencia_como_operador(c):
    ex = c["cunhagens_v398"]["extras"]; ex["autor_de_cada_inscricao"][ex["leitura_da_gerencia"]["sha16"]] = "operador"


def _gerencia_sem_rotulo(c):
    c["cunhagens_v398"]["extras"]["leitura_da_gerencia"]["autor"] = "operador"


def _inscricao_adulterada(c):
    list(c["cunhagens_v398"]["verbatim"].values())[0]["embedded_ok"] = False


def _inscricao_sha(c):
    list(c["cunhagens_v398"]["verbatim"].values())[1]["sha256"] = "0" * 64


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


def _veracidade_cai(c):
    c["teste_de_veracidade_fase9_v397"]["all_verified"] = False


def _cunh397_cai(c):
    c["cunhagens_v397"]["all_verified"] = False


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


def _selo_v397(s):
    s["um_version"] = "v397"


def _conf_quadro_pt(cj):
    cj["quadro"]["pt"]["ok"] = False


def _conf_quadro_md(cj):
    cj["quadro"]["md"]["ok"] = False


NEG = []
if not SEM_NEG and not P:
    NEG = [variante("selo de outra versao (v397)", f_selo=_selo_v397, espera="o selo nao e v398"),
           variante("registro sonico_v398 ausente do core", f_core=_sem_sonico, espera="registro obrigatorio ausente do core: sonico_v398"),
           variante("registro afinacao_das_cordas_v398 ausente do core", f_core=_sem_afinacao, espera="registro obrigatorio ausente do core: afinacao_das_cordas_v398"),
           variante("cunhagens_v398 nao selou", f_core=_nao_sela_cunh, espera="cunhagens_v398 nao selou"),
           variante("kh_n1_cobertura_v398 nao selou", f_core=_nao_sela_kh, espera="kh_n1_cobertura_v398 nao selou"),
           variante("sonico: ln 2 adulterado", f_core=_sonico_ln2, espera="sonico_v398 nao selou inteiro"),
           variante("sonico: entropia do colapso em theta_M (nats) adulterada", f_core=_sonico_entropia, espera="sonico_v398 nao selou inteiro"),
           variante("sonico: entropia do colapso em theta_M (oitavas) adulterada", f_core=_sonico_entropia_oitavas, espera="sonico_v398 nao selou inteiro"),
           variante("sonico: uma checagem numerica falhou", f_core=_sonico_cheque_falha, espera="sonico_v398 nao selou inteiro"),
           variante("sonico: o registro move o gate", f_core=_sonico_move_gate, espera="sonico_v398 nao selou inteiro"),
           variante("sonico: bandeira da composicao falsa", f_core=_sonico_bandeira_falsa, espera="a pedra Sonico nao esta no kernel do rito"),
           variante("sonico: composicao fora do trio", f_core=_sonico_fora_do_trio, espera="a pedra Sonico nao esta no kernel do rito"),
           variante("sonico: um termo antigo citado fora do trio", f_core=_sonico_suporte_fora_do_trio, espera="a pedra Sonico nao esta no kernel do rito"),
           variante("afinacao: zeta(-1) adulterado", f_core=_afinacao_zeta, espera="afinacao_das_cordas_v398 nao selou inteiro"),
           variante("afinacao: dimensao critica bosonica adulterada", f_core=_afinacao_dimensao, espera="afinacao_das_cordas_v398 nao selou inteiro"),
           variante("afinacao: d da casa adulterado", f_core=_afinacao_d_da_casa, espera="afinacao_das_cordas_v398 nao selou inteiro"),
           variante("afinacao: a hipotese MasslessFirstLevel dita derivada", f_core=_afinacao_hipotese, espera="a hipotese MasslessFirstLevel deixou de ser KNOWN"),
           variante("afinacao: a hipotese dita demonstrada", f_core=_afinacao_hipotese_provada, espera="a hipotese MasslessFirstLevel deixou de ser KNOWN"),
           variante("afinacao: a geometria dita fechada", f_core=_afinacao_geometria, espera="a hipotese MasslessFirstLevel deixou de ser KNOWN"),
           variante("afinacao: a TGL passa a derivar cordas do axioma", f_core=_afinacao_deriva, espera="a hipotese MasslessFirstLevel deixou de ser KNOWN"),
           variante("afinacao: o kappa do boost vem do core", f_core=_afinacao_kappa, espera="afinacao_das_cordas_v398"),
           variante("afinacao: bandeira da composicao falsa", f_core=_afinacao_bandeira_falsa, espera="a pedra AfinacaoDasCordas nao esta no kernel do rito"),
           variante("afinacao: composicao fora do trio", f_core=_afinacao_fora_do_trio, espera="a pedra AfinacaoDasCordas nao esta no kernel do rito"),
           variante("cunhagens: a leitura da gerencia rotulada como do operador", f_core=_gerencia_como_operador, espera="a leitura da gerencia nao esta rotulada como da gerencia"),
           variante("cunhagens: a leitura da gerencia sem o rotulo de autor", f_core=_gerencia_sem_rotulo, espera="a leitura da gerencia nao esta rotulada como da gerencia"),
           variante("cunhagens: uma inscricao deixou de estar embutida", f_core=_inscricao_adulterada, espera="as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens: sha256 de uma inscricao adulterado", f_core=_inscricao_sha, espera="as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("o quadro do topo: numero lido adulterado (z_disc 4,45)", f_core=_numero_adulterado, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: z_disc calibrado acima de 5", f_core=_z_disc_acima_de_5, espera="abaixo de 5"),
           variante("o quadro do topo: uma checagem do registro de veracidade falhou", f_core=_checagem_falha, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: fonte do registro de veracidade com sha256 adulterado", f_core=_fonte_adulterada, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: o registro de veracidade move o gate", f_core=_gate_movido, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: o registro de veracidade deixou de selar", f_core=_veracidade_cai, espera="teste_de_veracidade_fase9_v397"),
           variante("o quadro do topo: a conferencia diz que o quadro PT deixou de estar no topo", f_conf=_conf_quadro_pt, espera="o quadro do topo (O Teste da Unica Palavra, pt)"),
           variante("o quadro do topo: a conferencia diz que o quadro do .md deixou de estar no topo", f_conf=_conf_quadro_md, espera="o quadro do topo (O Teste da Unica Palavra, md)"),
           variante("cunhagens_v397 deixou de selar", f_core=_cunh397_cai, espera="cunhagens_v397"),
           variante("testemunha_estatica_v396 deixou de selar", f_core=_testemunha_cai, espera="testemunha_estatica_v396"),
           variante("face de Fock da testemunha com habitante exibido", f_core=_fock_da_testemunha_habitada, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),
           variante("face de Fock dita DENTRO da pedra da testemunha", f_core=_fock_dentro_da_pedra, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),
           variante("psibit_v395 deixou de selar", f_core=_psibit_cai, espera="psibit_v395"),
           variante("face de Fock do psibit_v395 habitada", f_core=_face_do_psibit_habitada, espera="psibit_v395: a face do psion deixou de estar como CONDICIONAL"),
           variante("registro da v394 deixou de selar", f_core=_v394_cai, espera="criterio_binario_de_parada_v394"),
           variante("AVISO da v398 no stdout", f_std=lambda t: t + "   [v398] AVISO: o sonico nao rodou: ValueError('x')\n", espera="AVISO da v398"),
           variante("AVISO de bloco anterior (v397) no stdout", f_std=lambda t: t + "   [v397] AVISO: o registro do Teste da Unica Palavra nao rodou: ValueError('x')\n", espera="AVISO de um bloco anterior"),
           variante("linha [v398] (sonico, afinacao e cunhagens) ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o sonico e a afinacao das cordas" not in l) + "\n", espera="linha [v398] do stdout"),
           variante("linha `>>> veredito <<<` do sonico ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if ESP["sonico"]["verdict"] not in l or "sonico=" in l) + "\n", espera="o bloco sonico_v398 do stdout"),
           variante("linha [v397] do Teste da Unica Palavra ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o Teste da Unica Palavra" not in l) + "\n", espera="linha [v397] do Teste da Unica Palavra")]'''
FUNCOES_HT = r'''FUNCOES = [("_d", lambda: T._d(Vd)), ("_num", lambda: T._num(Vd)), ("_num_sem_veredito", lambda: T._num(Vd, verdicts=False)), ("_cunhagens_lista", lambda: T._cunhagens(Vd)), ("_cunhagens_curta", lambda: T._cunhagens(Vd, "curta")),
           ("_ordem", lambda: T._ordem(Vd)), ("_entrou", lambda: T._entrou(Vd)), ("_pedras", lambda: T._pedras(Vd)), ("_sonico", lambda: T._sonico(Vd)), ("_afinacao", lambda: T._afinacao(Vd)), ("_regra_do_4_44", lambda: T._regra_do_4_44(Vd)),
           ("_kernel_prova", lambda: T._kernel_prova(Vd)), ("_limites", lambda: T._limites(Vd)), ("_limites_curto", lambda: T._limites(Vd, curto=True)), ("_legal", lambda: T._legal(Vd)), ("_erratas", lambda: T._erratas(Vd)),
           ("_depois", lambda: T._depois(Vd)), ("_rodada", lambda: T._rodada(Vd)), ("linhagem", lambda: T.linhagem(Vd)), ("desenho", lambda: T.desenho(Vd)), ("atlas", lambda: T.atlas(Vd)), ("core_memory", lambda: T.core_memory(Vd)),
           ("haja_luz", lambda: T.haja_luz(Vd)), ("topico_missao", lambda: T.topico_missao(Vd)), ("topico_central", lambda: T.topico_central(Vd)), ("topico_estatuto", lambda: T.topico_estatuto(Vd)), ("topico_novo", lambda: T.topico_novo(Vd)),
           ("aviso", lambda: T.aviso(Vd, "REIVINDICACAO_EMULADA")), ("aviso_pulado", lambda: T.aviso_pulado()), ("handoff", lambda: T.handoff(Vd, K_EMU)), ("arvore_linha", lambda: T.arvore_linha(Vd)), ("titulo_verbete", lambda: T.titulo_verbete(Vd)),
           ("verbete", lambda: T.verbete(Vd)), ("remissivo", lambda: T.remissivo(Vd)), ("linha_handoff", lambda: T.linha_handoff(Vd)), ("linha_topico_novo", lambda: T.linha_topico_novo(Vd)), ("marca_missao", lambda: T.marca_missao(Vd)),
           ("marca_topico_missao", lambda: T.marca_topico_missao(Vd)), ("marca_central", lambda: T.marca_central(Vd)), ("id_missao", lambda: T.id_missao(Vd)), ("id_central", lambda: T.id_central(Vd)), ("paragrafo_readme", lambda: T.paragrafo_readme()[0]),
           ("paragrafo_sonico", lambda: T.paragrafo_sonico()[0])]
CARREGAM_NUM = {"_num", "_num_sem_veredito", "linhagem", "atlas", "core_memory", "topico_novo", "verbete", "handoff"}   # os textos que embutem _num (o texto do kernel com a errata da palavra «teoremas»)
S16 = Vd.get("s16") or ESP["candidato_sha16"]
MARCADORES = {"linhagem": [S16, "<!-- linhagem_v398_selada -->", "sonico_v398", "afinacao_das_cordas_v398", "kh_n1_cobertura_v398"], "desenho": ["<!-- adendo_v398_selada -->", S16], "atlas": ["<!-- atlas_v398_selada -->", S16, "sonico_v398", "afinacao_das_cordas_v398", "kh_n1_cobertura_v398"],
              "core_memory": ["<!-- core_v398_selada -->", S16], "haja_luz": ["<!-- haja_luz_v398_selada -->", S16], "topico_estatuto": ["<!-- v398_selada -->", S16], "topico_novo": [S16, "sonico_v398", "afinacao_das_cordas_v398", "kh_n1_cobertura_v398", "# v398 SELADA ("],
              "aviso": ["<!-- aviso_v398_selada -->", S16], "handoff": ["name: handoff-v398-custodia", S16, "<!-- INICIO_PARAGRAFO_README_v397 -->", "<!-- FIM_PARAGRAFO_README_v397 -->", "<!-- INICIO_PARAGRAFO_SONICO_v398 -->", "<!-- FIM_PARAGRAFO_SONICO_v398 -->"],
              "linha_handoff": ["handoff-v398-custodia.md", S16], "topico_missao": [S16], "topico_central": [S16]}'''
NEW_4B = r'''# ------------------------------------------------------------------ 4b. os PARAGRAFOS PRONTOS do README/site: o QUADRO (v397, INTOCADO; ordem do operador de 23/10: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item) e o paragrafo NOVO do sonico e da afinacao
sys.path.insert(0, PKG)
import quadro_v397 as QD  # noqa: E402
_core_p = rdj(core_path)["core"]; _tv_p = _core_p["teste_de_veracidade_fase9_v397"]
_res_p = rdj(T._res_path(ESP))
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
        falha("paragrafo do README/site (quadro): positivo %s, igual ao do quadro %s, no handoff %s" % (_f9["positivo_sem_falhas"], _f9["igual_as_funcoes_do_quadro"], _f9["handoff_traz_o_paragrafo_entre_os_marcadores"]))
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
        print("  controle negativo do paragrafo do quadro %-52s %s" % (n_["controle"], "REPROVOU como esperado" if n_["ok"] else "NAO REPROVOU como esperado"))
        if not n_["ok"]:
            falha("controle negativo do paragrafo do quadro nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["falhas"]))
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
    _viol = {nome: _regra_nos_textos(nome, txt) for nome, txt in RENDER.items() if nome != "paragrafo_sonico"}
    _viol = {k: v for k, v in _viol.items() if v}
    _f9["regra_do_4_44_nos_textos_violacoes"] = _viol
    _f9["linhas_com_o_4_44_nos_textos"] = sum(1 for nome, txt in RENDER.items() for ln in txt.split("\n") if _z in ln)
    _neg_regra = _regra_nos_textos("x", "o z_disc = " + _z + " foi o resultado.")
    _f9["controle_negativo_da_regra_nos_textos"] = bool(_neg_regra)
    _f9["paragrafo_sonico_sem_o_4_44"] = not _regra_nos_textos("paragrafo_sonico", RENDER.get("paragrafo_sonico", "")) and (_z not in RENDER.get("paragrafo_sonico", "")) and ("z_disc" not in RENDER.get("paragrafo_sonico", ""))
    if _viol or not _neg_regra or not _f9["paragrafo_sonico_sem_o_4_44"]:
        falha("regra do 4,44 nos textos renderizados: violacoes %s; controle negativo da regra reprovou: %s; paragrafo novo sem o 4,44: %s" % (_viol, bool(_neg_regra), _f9["paragrafo_sonico_sem_o_4_44"]))
    _f9["ok"] = True
    print("  paragrafo do quadro (README/site): positivo ok; %d controles negativos; %d linha(s) com o 4,44 nos textos, todas com o p, os 5 sigma e o 'nao foi alcancado'" % (len(_NEGP), _f9["linhas_com_o_4_44_nos_textos"]))
except BaseException as ex:  # noqa: BLE001
    _f9["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:400]); _f9["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo do README/site (quadro): %s" % _f9["erro"])
etapa("paragrafo_readme_e_regra_do_4_44", **_f9)
# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (sonico e afinacao das cordas): verificacao propria, controles negativos e a ATRIBUICAO da gerencia em todo texto renderizado
_sn = {"ok": False}
try:
    PAR_S, PAR_S_INFO = T.paragrafo_sonico()
    _sn["positivo_sem_falhas"] = (T.verificar_paragrafo_sonico(PAR_S, _core_p, ESP) == [])
    _sn["igual_ao_gerado_do_core"] = (PAR_S == T._paragrafo_sonico_de(_core_p))
    _ho = RENDER.get("handoff", "")
    _sn["handoff_traz_os_dois_paragrafos_entre_os_marcadores"] = bool((T.MARC_SON_INI + "\n" + PAR_S.rstrip("\n") + "\n" + T.MARC_SON_FIM) in _ho and ("<!-- INICIO_PARAGRAFO_README_v397 -->\n" + PAR.rstrip("\n") + "\n<!-- FIM_PARAGRAFO_README_v397 -->") in _ho)
    _sn["info"] = PAR_S_INFO
    if not (_sn["positivo_sem_falhas"] and _sn["igual_ao_gerado_do_core"] and _sn["handoff_traz_os_dois_paragrafos_entre_os_marcadores"]):
        falha("paragrafo novo do sonico e da afinacao: positivo %s, igual ao gerado do core %s, no handoff %s" % (_sn["positivo_sem_falhas"], _sn["igual_ao_gerado_do_core"], _sn["handoff_traz_os_dois_paragrafos_entre_os_marcadores"]))
    _sv = _core_p["sonico_v398"]["values"]; _av = _core_p["afinacao_das_cordas_v398"]["values"]
    _ln2 = T._pn(_sv["ln2"]); _hn = T._pn(_sv["collapse_entropy_theta_M_nats"]); _ho_ = T._pn(_sv["collapse_entropy_theta_M_octaves"])

    def _muts(nome, f, espera):
        p2 = f(PAR_S); fa = T.verificar_paragrafo_sonico(p2, _core_p, ESP)
        ok = bool(p2 != PAR_S and fa and any(espera in x for x in fa)); return {"controle": nome, "reprovou": bool(fa), "mensagem_esperada_presente": any(espera in x for x in fa), "ok": ok, "falhas": [x[:140] for x in fa][:3]}
    _trocado = lambda s: s[:-1] + str((int(s[-1]) + 1) % 10)
    _ger_frase = "o Verbo pina a oitava; a oitava pinada cobra um bit; o bit cobrado é o que fica, a memória"
    _NEGS = [_muts("ln 2 com um digito trocado (em todo o paragrafo)", lambda p: p.replace(_ln2, _trocado(_ln2)), "ausente do paragrafo"),
             _muts("entropia do colapso em theta_M (nats) adulterada", lambda p: p.replace(_hn, _trocado(_hn)), "ausente do paragrafo"),
             _muts("entropia do colapso em theta_M (oitavas) adulterada", lambda p: p.replace(_ho_, _trocado(_ho_)), "ausente do paragrafo"),
             _muts("zeta(-1) adulterado", lambda p: p.replace("−1/12", "−1/11"), "ausente do paragrafo"),
             _muts("a dimensao critica bosonica adulterada", lambda p: p.replace("D = 26", "D = 25"), "ausente do paragrafo"),
             _muts("a gerencia rotulada como operador (o rotulo da sexta inscricao some)", lambda p: p.replace("texto da gerência, não é fala do operador", "fala do operador"), "frase de limite ausente"),
             _muts("a gerencia como operador (GERENCIA vira operador)", lambda p: p.replace("GERÊNCIA", "operador"), "frase de limite ausente"),
             _muts("citacao do operador que nao e' verbatim", lambda p: p.replace("seletor de identidade", "seletor de identidades", 1), "NAO e' verbatim"),
             _muts("o texto da gerencia entre aspas como fala do operador", lambda p: p.replace("*sônico* é a estrutura", "«" + _ger_frase + "» — *sônico* é a estrutura", 1), "NAO e' verbatim"),
             _muts("o 4,44 entra no paragrafo", lambda p: p + "\n> z_disc = " + _z + "\n", "4,44"),
             _muts("a hipotese nomeada sem o estatuto KNOWN", lambda p: p.replace("[KNOWN]", "", 1), "estatuto ausente"),
             _muts("a geometria sem o estatuto OPEN", lambda p: p.replace("[OPEN]", "", 1), "estatuto ausente"),
             _muts("o d da casa sem o estatuto DECLARADO", lambda p: p.replace("[DECLARADO", "[medido", 1), "estatuto ausente"),
             _muts("a lei de custo dita derivada", lambda p: p.replace("A lei de custo é [INPUT]", "A lei de custo é derivada"), "frase de limite ausente"),
             _muts("a TGL dita teoria de cordas", lambda p: p.replace("não é dita teoria de cordas", "é dita teoria de cordas"), "frase de limite ausente")]
    for n_ in _NEGS:
        print("  controle negativo do paragrafo novo %-62s %s" % (n_["controle"], "REPROVOU como esperado" if n_["ok"] else "NAO REPROVOU como esperado"))
        if not n_["ok"]:
            falha("controle negativo do paragrafo novo nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["falhas"]))
    _sn["negativos"] = _NEGS

    def _levanta(f):
        try:
            f(); return False
        except AssertionError:
            return True
    _lista = RENDER["_cunhagens_lista"]; _sg = T._sha_ger(); _lin = [l for l in _lista.split("\n") if _sg in l]; assert len(_lin) == 1
    _tx = {"cita_fora_dos_bytes_levanta": _levanta(lambda: T._cita("o Verbo toca a oitava e o bit fica")),
           "cita_da_gerencia_como_fala_do_operador_levanta": _levanta(lambda: T._cita(_ger_frase)),
           "ger_sem_aspas_passa": (T._ger(_ger_frase) == _ger_frase),
           "ger_fora_dos_bytes_levanta": _levanta(lambda: T._ger("o Verbo toca a oitava e o bit fica")),
           "atribuicao_limpa_nos_textos": {nome: T.atribuicao_da_gerencia(txt) for nome, txt in RENDER.items() if T.atribuicao_da_gerencia(txt)} == {},
           "controle_gerencia_como_operador": bool(T.atribuicao_da_gerencia(_lista.replace(_lin[0], _lin[0].replace("GERÊNCIA", "operador").replace("gerência", "operador")))),
           "controle_gerencia_entre_aspas": bool(T.atribuicao_da_gerencia("a leitura: «" + _ger_frase + "»")),
           "controle_seis_falas_do_operador": bool(T.atribuicao_da_gerencia("as seis falas do operador"))}
    _sn["textos"] = _tx
    _ruim = [k for k, v in _tx.items() if not v]
    if _ruim:
        falha("atribuicao da gerencia / citacao verbatim: controles que nao deram o esperado: %s" % _ruim)
    _sn["ok"] = True
    print("  paragrafo novo (sonico e afinacao): positivo ok; %d controles negativos; atribuicao da gerencia: %d controles ok" % (len(_NEGS), len(_tx)))
except BaseException as ex:  # noqa: BLE001
    _sn["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:400]); _sn["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo novo do sonico e da afinacao: %s" % _sn["erro"])
etapa("paragrafo_sonico_e_atribuicao_da_gerencia", **_sn)'''


MAPA_CTL = r'''    REG = RM.montar(Vd, core_emu, selo_emu, ids, arts)
    # controles negativos de registrar_mapa_v398: a regra da ordem do 4,44 aplicada aos campos do registro (sem o p, sem a linha dos 5 sigma; a clausula completa passa) e as recusas de montar() (selo de outra versao; rota nova que ja' existe no livro)
    _zm = QD.esperados(_res_p, "pt")[0]["z_disc"]["md"]; _pm = QD.esperados(_res_p, "pt")[0]["p_disc"]["md"]

    def _recusa(f):
        try:
            f()
            return False
        except AssertionError:
            return True
    CTL_MAPA = {"regra_4_44_sem_o_p_reprova": bool(RM.regra_4_44([{"c": "o z_disc = " + _zm + ", abaixo do degrau de 5σ, que não foi alcançado"}], _zm, _pm)),
                "regra_4_44_sem_a_linha_dos_5_sigma_reprova": bool(RM.regra_4_44([{"c": "z_disc = " + _zm + " (p unilateral " + _pm + ")"}], _zm, _pm)),
                "regra_4_44_completa_passa": not RM.regra_4_44([{"c": "z_disc = " + _zm + " (calibrado; p unilateral " + _pm + "), abaixo do degrau de 5σ da creditação, que não foi alcançado (" + _zm + " < 5)"}], _zm, _pm),
                "montar_recusa_selo_de_outra_versao": _recusa(lambda: RM.montar(Vd, core_emu, dict(selo_emu, um_version="v397"), ids, arts)),
                "montar_recusa_rota_nova_que_ja_existe": _recusa(lambda: RM.montar(Vd, core_emu, selo_emu, set(ids) | {RM.NOVA}, arts))}
    etapa("mapa_controles_negativos", **CTL_MAPA)
    for k_, v_ in CTL_MAPA.items():
        print("  mapa, controle %-48s %s" % (k_, "ok" if v_ else "FALHOU"))
        if not v_:
            falha("mapa: controle negativo de registrar_mapa_v398 nao deu o esperado: %s" % k_)
'''


def deriva_harness_textos():
    a = Arq("harness_textos_ensaio_v398.py", sobe(MOL["harness_textos_ensaio_v397.py"]))
    a.subst_bloco('"""harness_textos_ensaio_v398.py', "import contextlib", DOC_HT, nome="docstring")
    a.subst_bloco('N_ = ESP["escada"][1]; n_spec = len(ESP["registros_v397"])', 'etapa("nos_emulado"', NEW_STD, nome="stdout emulado")
    a.tr('env = dict(os.environ); env["V397_NOS"] = NOSE; env["PYTHONIOENCODING"] = "utf-8"', 'env = dict(os.environ); env["V398_NOS"] = NOSE; env["PYTHONIOENCODING"] = "utf-8"', 1, "V398_NOS")
    a.subst_bloco("def variante(", "def _sem_veracidade(c):", NEW_VARIANTE, nome="variante (com f_conf)")
    a.tr_s('core_raw = open(core_path, "rb").read(); selo_raw = open(selo_path, "rb").read(); std_raw = open(std_path, "rb").read()',
           'core_raw = open(core_path, "rb").read(); selo_raw = open(selo_path, "rb").read(); std_raw = open(std_path, "rb").read()\nconf_path = os.path.join(POS_EMU, "conferidor", "conferencia_rito_v398.json"); conf_raw = open(conf_path, "rb").read() if os.path.exists(conf_path) else b""', 1, "bytes da conferencia")
    a.subst_bloco("def _sem_veracidade(c):", "    for n_ in NEG:", NEG_HT, nome="controles negativos da leitura")
    a.tr('"rel_man": "EMULADO_SEM_HASH", "readme_paragrafo": T.paragrafo_readme()[0]}', '"rel_man": "EMULADO_SEM_HASH", "readme_paragrafo": T.paragrafo_readme()[0], "readme_paragrafo_sonico": T.paragrafo_sonico()[0]}', 1, "K_EMU: os dois paragrafos")
    a.subst_bloco("FUNCOES = [", 'TXT = os.path.join(OUT, "textos")', FUNCOES_HT, nome="FUNCOES e MARCADORES")
    a.subst_bloco("# ------------------------------------------------------------------ 4b.", "# ------------------------------------------------------------------ 5. cada `termo`", NEW_4B + "\n", nome="4b e 4c: paragrafos e atribuicao")
    a.tr('for base in (PKG, os.path.join(PKG, "insumos"), os.path.join(PKG, "insumos", "fase9"), os.path.join(PKG, "insumos", "cunhagens"), os.path.join(PKG, "kernel"), HERE, os.path.join(PKG, "bancada_B3_servico")):',
         'for base in (PKG, os.path.join(PKG, "insumos"), os.path.dirname(T._res_path(ESP)), os.path.join(PKG, "insumos", "cunhagens"), os.path.join(PKG, "kernel"), HERE, os.path.join(PKG, "bancada_B3_servico")):', 1, "NOMES_ARQ: pastas")
    a.tr('INS_TXT = "\\n".join(rd(os.path.join(PKG, "insumos", f)) for f in sorted(os.listdir(os.path.join(PKG, "insumos"))) if f.endswith((".md", ".json", ".lean"))) + "\\n" + "\\n".join(rd(os.path.join(PKG, "insumos", "fase9", f)) for f in sorted(os.listdir(os.path.join(PKG, "insumos", "fase9"))) if f.endswith(".json"))',
         'INS_TXT = "\\n".join(rd(os.path.join(PKG, "insumos", f)) for f in sorted(os.listdir(os.path.join(PKG, "insumos"))) if f.endswith((".md", ".json", ".lean"))) + "\\n" + rd(T._res_path(ESP))', 1, "INS_TXT")
    a.tr('HEX16.update(d["sha16"] for d in T._falas().values()); HEX16.add(ESP["pedra"]["sha16"])', 'HEX16.update(d["sha16"] for d in T._falas().values()); HEX16.update(v["sha16"] for v in ESP["pedras"].values()); HEX16.add(ESP["quadro"]["frase_sha16"])', 1, "HEX16: as duas pedras e a fala do 4,44 (v397)")
    a.insere_depois('CONHECIDOS.update(str(h)[:8] for h in ESP["veracidade"]["fontes"].values())', 'CONHECIDOS.add(T._linha_maquina_sonico(core_emu["sonico_v398"]["values"], core_emu["afinacao_das_cordas_v398"]["values"]))   # a linha de maquina do paragrafo novo (lida dos dois registros do core emulado)', nome="CONHECIDOS: linha de maquina do paragrafo novo")
    a.tr('VALORES_LIDOS = set((Vd.get("veracidade") or {}).get("lido") or {})', 'VALORES_LIDOS = set((Vd.get("veracidade") or {}).get("lido") or {}) | set((Vd.get("sonico") or {}).get("values") or {}) | set((Vd.get("afinacao") or {}).get("values") or {})', 1, "VALORES lidos")
    a.tr_s('("TGL_ATLAS.md", ["<!-- atlas_v398_selada -->", S16, "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"])', '("TGL_ATLAS.md", ["<!-- atlas_v398_selada -->", S16, "sonico_v398", "kh_n1_cobertura_v398"])', 1, "exige do Atlas")
    a.tr_s('("MEMORIA_DA_LINHAGEM.md", [S16, "<!-- linhagem_v398_selada -->", "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"])', '("MEMORIA_DA_LINHAGEM.md", [S16, "<!-- linhagem_v398_selada -->", "sonico_v398", "kh_n1_cobertura_v398"])', 1, "exige da linhagem")
    a.tr_s('(T.TOPICO_NOVO, [S16, "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"])', '(T.TOPICO_NOVO, [S16, "sonico_v398", "kh_n1_cobertura_v398"])', 1, "exige do topico novo")
    a.tr('R["veredito"] = ("TUDO PASSOU: o conferidor da v397 bate no Nos emulado, a leitura le sem problema e reprova os controles negativos, os textos renderizam e a guarda P18 esta limpa, o paragrafo do README/site e a regra do 4,44 passam e os controles negativos reprovam, cada termo citado existe, as superficies fecham em copias (com folga) e RECUSAM no limite sem compactar, e o b3_recibo confere"',
         'R["veredito"] = ("TUDO PASSOU: o conferidor da v398 bate no Nos emulado, a leitura le sem problema e reprova os controles negativos (os dois registros novos, as pedras, as inscricoes e o quadro do topo), os textos renderizam e a guarda P18 esta limpa, os dois paragrafos do README/site e a regra do 4,44 passam e os controles negativos reprovam, a atribuicao da gerencia e a citacao verbatim valem, cada termo citado existe, as superficies fecham em copias (com folga) e RECUSAM no limite sem compactar, e o b3_recibo confere"',
         1, "veredito do harness")
    a.tr("    REG = RM.montar(Vd, core_emu, selo_emu, ids, arts)\n", MAPA_CTL, 1, "mapa: controles negativos de registrar_mapa")
    for proibido in ("V['token']", "_sem_testemunha", "20261022", "base_v396", "PKG_ANT_", "V5 ", "V4 ", "_selo_v396", "psibit_v398", "token_is_the", "ESP[\"pedra\"]", "bandeira_da_pedra", "teorema_da_pedra", "vereditos_novos_v397", "registros_v397\"]", "dry_v397", "textos_v397", "leitura_v397", "VALORES_TESTEMUNHA"):
        assert proibido not in a.t, ("resto da v397 no harness dos textos", proibido)
    ast.parse(a.t)
    return a


# =============================================================================== harness_fechar_sandbox_v398.py
DOC_HF = r'''"""harness_fechar_sandbox_v398.py -- roda fechar_v398.py e registrar_mapa_v398.py (o main) num SANDBOX inteiro dentro de pos_rito\\harness_saida_v398\\fechar_sandbox (nada fora dela e' escrito; o Nos real, a memoria real, o Atlas, o git e a Bancada
nao sao tocados; o mapa de rotas real e' SO' LIDO).  O que o harness_textos_ensaio_v398.py nao cobre: o fechar (manifesto, arquivo, os dois diffs, o handoff com os DOIS paragrafos do README/site) e o main do registrar_mapa. Derivado do harness_fechar_sandbox_v397.py (que rodou na v397).
O sandbox e' uma ARVORE ISOLADA: work\\cadeia_de_selo\\v398 (pacote com ESPERADOS, CANDIDATO, PINOS_BN, base_v397, insumos (o resultado pinado do Teste da Unica Palavra, que mora na v397, ganha uma COPIA em insumos\\fase9 so' no sandbox), quadro_v397 e runtime_quadro_v397, o APLICADO_AO_CANONICO
EMULADO, os recibos do B(n) SINTETICOS) + nos\\ (o Nos EMULADO montado de dry_v398, como no harness dos textos) + memory\\ (a memoria vazia). As copias dos scripts (leitura, textos, fechar) trocam SO' as duas constantes de caminho (o Nos e a pasta de memoria) por caminhos do sandbox;
o resto e' byte a byte o que a cadeia usa (conferido: o diff das copias contra os originais e' so' essas linhas).
O que ele prova: fechar_v398.py sai com rc 0 e grava o handoff (guarda P18 limpa) com os DOIS paragrafos do README/site entre os marcadores (o do quadro igual ao das funcoes do quadro sobre o core do sandbox e aprovado por T.verificar_paragrafo_readme; o do sonico e da afinacao
igual ao gerado do core e aprovado por T.verificar_paragrafo_sonico), o handoff do Nos, os dois diffs, o manifesto e o arquivo; RECUSA (rc 2, sem handoff) sem o recibo do religamento, com um recibo do B(n) que declara salto, com o resultado pinado adulterado (o paragrafo do quadro nao passa na verificacao contra o resultado),
com o numero lido do quadro adulterado, com o numero do sonico adulterado no core e com a sexta inscricao rotulada como do operador;
registrar_mapa_v398.py (main) monta o JSON com 4 registros e imprime o comando. Os recibos do B(n) sao SINTETICOS (derivados dos reais da v397, como no harness dos textos): a prova e' do CODIGO do fechar, nao de um B(n) real.
uso: python -I -B -X utf8 harness_fechar_sandbox_v398.py [--manter]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita)"""'''
NEW_STD_F = r'''N_ = ESP["escada"][1]; n_spec = len(ESP["registros_v398"]); n_spec7 = len([k for k in ("cunhagens_v397", "kh_n1_cobertura_v397") if k in ESP["vereditos_v397"]])
open(os.path.join(NOSS, "rodada_v398_stdout.txt"), "w", encoding="utf-8", newline="\n").write("\n".join([
    "[v398] EMULADO PELO SANDBOX", "SONICO [v398 -- EMULADO]:", "  >>> %s <<<" % ESP["sonico"]["verdict"], "AFINACAO DAS CORDAS [v398 -- EMULADO]:", "  >>> %s <<<" % ESP["afinacao"]["verdict"],
    "   [v397] o Teste da Unica Palavra (Fase 9 V2-c1, aberto uma vez em 23/10), lido por hash ao lado do V1 (nenhum sigma novo): %s" % ESP["vereditos_v397"]["teste_de_veracidade_fase9_v397"],
    "   [v397] a pedra Token e as falas de 23/10 (cunhagens_v397): %s | registros por spec: %d (selados %d)" % (ESP["vereditos_v397"]["cunhagens_v397"], n_spec7, n_spec7),
    "   [v398] o sonico e a afinacao das cordas (lidos na fractalizacao do Um) e as inscricoes de 23/10 (cunhagens_v398): sonico=%s | afinacao=%s | cunhagens=%s | registros por spec: %d (selados %d)" % (ESP["sonico"]["verdict"], ESP["afinacao"]["verdict"], ESP["registros_v398"]["cunhagens_v398"], n_spec, n_spec),
    "teoremas limpos: %s/%s" % (N_, N_), ">>> TGL_KERNEL_STAGE1_VERIFIED", "[selo] rite_checkpoints: chave desligada ; reaproveitados 0", "FAIL_CLOSED_SELFTEST_PASSED", "[selo] colapso tipado: EMULADO", "RITO_RC=0", ""]))'''
NEG_NOVOS_F = r'''# ---- 1c. controles negativos do PARAGRAFO NOVO e da atribuicao da gerencia: o numero do sonico adulterado no core do Nos emulado (a leitura e a porta do paragrafo recusam) e a sexta inscricao rotulada como do operador => RECUSA (rc 2, FECHAR RECUSADO), sem handoff
core_p = os.path.join(NOSS, "um_absoluto.json"); raw_core = open(core_p, "rb").read()
cj = json.loads(raw_core.decode("utf-8")); cj["core"]["sonico_v398"]["values"]["collapse_entropy_theta_M_nats"] = 0.0651
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v398.py", "fechar_sonico_adulterado"); NEG.append({"controle": "numero do sonico adulterado no core (entropia do colapso em theta_M)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v398-custodia.md"))})
# a PORTA do paragrafo novo isolada: T.paragrafo_sonico() da copia do sandbox tem de LEVANTAR com o numero do sonico adulterado no core (a verificacao compara com os numeros de ESPERADOS)
import importlib.util as _iu1
_sp1 = _iu1.spec_from_file_location("textos_sb1", os.path.join(POS, "textos_v398.py")); _t1 = _iu1.module_from_spec(_sp1); _sp1.loader.exec_module(_t1)
try:
    _t1.paragrafo_sonico(); _levantou1 = False
except AssertionError as _ex1:
    _levantou1 = "nao passou nas verificacoes" in str(_ex1)
NEG.append({"controle": "a porta do paragrafo novo (paragrafo_sonico, chamada pelo fechar) levanta com o numero do sonico adulterado", "rc": 2 if _levantou1 else 0, "recusou": _levantou1, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v398-custodia.md"))})
open(core_p, "wb").write(raw_core)
cj = json.loads(raw_core.decode("utf-8")); _ex = cj["core"]["cunhagens_v398"]["extras"]; _ex["autor_de_cada_inscricao"][_ex["leitura_da_gerencia"]["sha16"]] = "operador"
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v398.py", "fechar_gerencia_como_operador"); NEG.append({"controle": "a leitura da gerencia rotulada como do operador no core (autor_de_cada_inscricao)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v398-custodia.md"))})
open(core_p, "wb").write(raw_core)
'''
CHK_SON_F = r'''# ---- 2c. o PARAGRAFO NOVO (sonico e afinacao) nos dois handoffs gravados: igual ao gerado do core do sandbox, entre os marcadores, aprovado pela verificacao propria (e o do handoff do Nos tambem)
_core_s = rdj(os.path.join(NOSS, "um_absoluto.json"))["core"]
import importlib.util as _iu3
_sp3 = _iu3.spec_from_file_location("textos_sb3", os.path.join(POS, "textos_v398.py")); _t3 = _iu3.module_from_spec(_sp3); _sp3.loader.exec_module(_t3)
_par_s_esp = _t3._paragrafo_sonico_de(_core_s); _msi = _t3.MARC_SON_INI + "\n"; _msf = "\n" + _t3.MARC_SON_FIM
_ok_son = {}
for _nome, _ptxt in (("memory/handoff-v398-custodia.md", ho), ("nos/HANDOFF_v398_CUSTODIA.md", open(os.path.join(NOSS, "HANDOFF_v398_CUSTODIA.md"), encoding="utf-8").read() if os.path.exists(os.path.join(NOSS, "HANDOFF_v398_CUSTODIA.md")) else "")):
    _i = _ptxt.find(_msi); _j = _ptxt.find(_msf)
    _par = _ptxt[_i + len(_msi):_j] if (_i >= 0 and _j > _i) else ""
    _fa = _t3.verificar_paragrafo_sonico(_par + "\n" if _par and not _par.endswith("\n") else _par, _core_s, ESP) if _par else ["sem o bloco"]
    _ok_son[_nome] = {"traz_o_bloco": bool(_par), "igual_ao_gerado_do_core": _par.rstrip("\n") == _par_s_esp.rstrip("\n"), "falhas_da_verificacao": _fa[:3], "guarda_p18": [list(x) for x in violacoes(_par)][:3], "atribuicao_da_gerencia": _t3.atribuicao_da_gerencia(_ptxt)[:3]}
R["etapas"]["paragrafo_sonico_no_handoff"] = _ok_son
print("  paragrafo novo (sonico e afinacao) no handoff: %s" % {k: (v["traz_o_bloco"] and v["igual_ao_gerado_do_core"] and not v["falhas_da_verificacao"] and not v["guarda_p18"] and not v["atribuicao_da_gerencia"]) for k, v in _ok_son.items()})
for _nome, _v in _ok_son.items():
    if not (_v["traz_o_bloco"] and _v["igual_ao_gerado_do_core"] and not _v["falhas_da_verificacao"] and not _v["guarda_p18"] and not _v["atribuicao_da_gerencia"]):
        falha("o handoff (%s) nao traz o paragrafo novo do sonico e da afinacao pronto e aprovado: %s" % (_nome, _v))
'''


def deriva_harness_fechar():
    a = Arq("harness_fechar_sandbox_v398.py", sobe(MOL["harness_fechar_sandbox_v397.py"]))
    a.subst_bloco('"""harness_fechar_sandbox_v398.py', "import hashlib, json, os, re, shutil, subprocess, sys, time", DOC_HF, nome="docstring")
    a.tr_s('shutil.copytree(os.path.join(PKG, "insumos"), os.path.join(PKS, "insumos"))',
           'shutil.copytree(os.path.join(PKG, "insumos"), os.path.join(PKS, "insumos"))\n'
           'os.makedirs(os.path.join(PKS, "insumos", "fase9"), exist_ok=True)   # o resultado pinado do Teste da Unica Palavra mora na v397 (ESPERADOS[veracidade][resultado][duravel]); o sandbox ganha a sua COPIA, que os controles negativos adulteram\n'
           'shutil.copyfile(ESP["veracidade"]["resultado"]["duravel"], os.path.join(PKS, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])))\n'
           'os.makedirs(os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "cunhagens"), exist_ok=True)   # a fala do 4,44 (v397), de onde textos_v398 confere a frase verbatim do quadro\n'
           '_h444 = ESP["quadro"]["frase_sha16"]; _f444 = [f_ for f_ in os.listdir(os.path.join(os.path.dirname(PKG), "v397", "insumos", "cunhagens")) if f_.startswith(_h444 + "_")]; assert len(_f444) == 1\n'
           'shutil.copyfile(os.path.join(os.path.dirname(PKG), "v397", "insumos", "cunhagens", _f444[0]), os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "cunhagens", _f444[0]))', 1, "sandbox: resultado pinado e fala do 4,44")
    a.subst_bloco('N_ = ESP["escada"][1]; n_spec = len(ESP["registros_v397"])', "bu = os.path.join(PKS, ", NEW_STD_F, nome="stdout emulado")
    a.tr('env = dict(os.environ); env["V397_NOS"] = NOSS; env["PYTHONIOENCODING"] = "utf-8"', 'env = dict(os.environ); env["V398_NOS"] = NOSS; env["PYTHONIOENCODING"] = "utf-8"', 1, "V398_NOS")
    a.tr('os.path.join(TOOLS, "v397_kernel", "pedras", "TGLExt_Token.lean")', 'os.path.join(TOOLS, "v398_kernel", "pedras", "TGLExt_Sonico.lean"), os.path.join(TOOLS, "v398_kernel", "pedras", "TGLExt_AfinacaoDasCordas.lean")', 1, "pedras copiadas")
    a.tr('"diff_kernel_novos": ("novos (1)" in dk and "TGLExt/Token.lean" in dk)', '"diff_kernel_novos": ("novos (2)" in dk and "TGLExt/Sonico.lean" in dk and "TGLExt/AfinacaoDasCordas.lean" in dk)', 1, "diff do kernel no resumo")
    a.tr('if not ("novos (1)" in dk and "TGLExt/Token.lean" in dk):', 'if not ("novos (2)" in dk and "TGLExt/Sonico.lean" in dk and "TGLExt/AfinacaoDasCordas.lean" in dk):', 1, "diff do kernel na falha")
    a.tr('"limpa" if not vio else vio[:2], "novos (1)" in dk))', '"limpa" if not vio else vio[:2], "novos (2)" in dk))', 1, "print do diff do kernel")
    a.insere_antes("for n in NEG:", NEG_NOVOS_F, nome="controles negativos novos do fechar")
    a.insere_antes("# ---- 3. o registrar_mapa (main)", CHK_SON_F, nome="conferencia do paragrafo novo no handoff")
    a.tr_s('for k_ in ("registros_v397", "base_v397", "b3", "diffs", "insumos_sha16", "conferidor"):', 'for k_ in ("registros_v398", "base_v397", "b3", "diffs", "insumos_sha16", "conferidor", "readme_paragrafo", "readme_paragrafo_sonico"):', 1, "chaves do manifesto")
    a.tr_s('ok_m = (rc == 0 and len(reg) == 3 and', 'ok_m = (rc == 0 and len(reg) == 4 and', 1, "registrar_mapa: 4 registros")
    a.tr('R["veredito"] = "TUDO PASSOU: o fechar grava o handoff (com o paragrafo do README/site aprovado pelo quadro), os diffs, o manifesto e o arquivo e RECUSA sem o religamento, com salto, com o resultado pinado adulterado e com o numero lido adulterado; o registrar_mapa monta o registro"',
         'R["veredito"] = "TUDO PASSOU: o fechar grava o handoff (com os dois paragrafos do README/site aprovados: o do quadro pelo quadro, o do sonico e da afinacao pela verificacao propria), os diffs, o manifesto e o arquivo e RECUSA sem o religamento, com salto, com o resultado pinado adulterado, com o numero lido adulterado, com o numero do sonico adulterado e com a gerencia rotulada como operador; o registrar_mapa monta o registro"',
         1, "veredito do fechar")
    a.tr('"fechar_out.txt", "fechar_sem_religamento_out.txt", "fechar_com_salto_out.txt", "fechar_resultado_adulterado_out.txt", "fechar_numero_adulterado_out.txt", "registrar_mapa_out.txt"',
         '"fechar_out.txt", "fechar_sem_religamento_out.txt", "fechar_com_salto_out.txt", "fechar_resultado_adulterado_out.txt", "fechar_numero_adulterado_out.txt", "fechar_sonico_adulterado_out.txt", "fechar_gerencia_como_operador_out.txt", "registrar_mapa_out.txt"', 1, "saidas guardadas")
    for proibido in ("TestemunhaEstatica", "Psibit.lean", "20261022", "base_v396", "V5 ", "V4 ", "psibit_v398", "TGLExt_Token", "novos (1)", "registros_v397\"", "dry_v397", "textos_v397", "leitura_v397"):
        assert proibido not in a.t, ("resto da v397 no harness do fechar", proibido)
    ast.parse(a.t)
    return a


# =============================================================================== gravar e conferir
ARQS = [deriva_leitura(), deriva_superficies(), deriva_fechar(), deriva_b3(), deriva_chain(), deriva_harness_textos(), deriva_harness_fechar()]
DER = {a.nome: a.t for a in ARQS}
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
INV = {"leitura_v398.py": ["REG_V393", "REG_V394", "REG_V395", "REG_V396", "REG_V397", "REG_FIXOS", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "teste_de_veracidade_fase9_v397", "testemunha_estatica_v396", "psibit_v395", "rede_fock_v394",
                           "kernel_modulos_novos_v398.json", "axiom_coverage_v392", "dict.fromkeys", "vereditos_v397", "escada_v397_e_v398", "registros_v398", "vereditos_novos_v398", "rodada_v398_stdout.txt", "conferencia_rito_v398.json", "ESPERADOS_v398.json", "CANDIDATO_v398.json",
                           "V['sonico']", "V['afinacao']", "V['cunhagens']", "V['pedras_kernel']", "V['reg398']", "V['veracidade']", "V['patch_ids']", "[v398] AVISO", "registros por spec", "V['um_version'] != 'v398'", "a base substituida != a v397 selada", "_feq", "_base_core", "_res_path",
                           "MasslessFirstLevel", "derives_strings_from_the_axiom", "kappa_from_core", "autor_de_cada_inscricao", "leitura_da_gerencia", "a leitura da gerencia nao esta rotulada como da gerencia", "fock_face", "declared_outside_the_stone", "linked_to_the_corner_by_a_lemma",
                           "conditional_psion_face", "AVISO de um bloco anterior", "quadro_v397", "lido_do_resultado", "f9v2_resultado", "numeros_do_resultado", "z_disc_calibrado", "poder_previo", "abaixo de 5", "a pedra %s nao esta no kernel do rito"],
       "superficies_v398.py": ["_sup398", "V398_AVISO_REIVINDICACAO", "(handoff-v397-custodia.md)", "- [HANDOFF v397", "leitura_v398", "textos_v398", "guarda_p18_v398", "linhagem_v398_selada", "adendo_v398_selada", "atlas_v398_selada", "core_v398_selada",
                               "haja_luz_v398_selada", "aviso_v398_selada", "v398_selada", "v398 SELADA", "os.replace(tmp, p)", "backup de bytes falhou", "SUPERFICIES RECUSADAS", "sys.exit(3)", "linhas ANTES", "NAO compacta nada"],
       "fechar_v398.py": ["T.handoff(V, _k)", "T.paragrafo_readme()", "T.paragrafo_sonico()", "readme_paragrafo", "readme_paragrafo_sonico", "_f398", "FECHAR RECUSADO:", "insumos_sha16", "DIFF_KERNEL_v398.txt", "RECIBO_SINCRONIZACAO_v398_", "RECIBO_PARADA_v398.json", "RECIBO_RELIGAMENTO_v398.json", "__SALTO_",
                          "registros_v398", "base_v397", "HANDOFF_v398_CUSTODIA.md", "handoff-v398-custodia.md", "_MARCA_PENDENTE", "guarda_p18_v398", "v398_selo", "v398_kernel", "HARNESS_TEXTOS_ENSAIO_v398.json", "DERIVACAO_v398.json",
                          "registro_mapa_v398.json", "NOTAS_DERIVACAO_v398.md", "FECHADO v398:"],
       "chain_pos_rito_v398.sh": ["V398_AVISO_REIVINDICACAO", "V398_AUTORIZACAO_OPERADOR", "topico_novo()", "textos_v398", "arvore_dry.md", "_p398", "_sup398", "selo_anterior_v397", "kernel_manifesto_anterior_v397", "/c/IALD/Central de Patentes/work/cadeia_de_selo/v398", "B3_AUTORIZADO\" = \"sim\"",
                                  "exit 20", "RECIBO_PARADA_v398.json", "RECIBO_RELIGAMENTO_v398.json", "--versao v398 --fase pos_selo", "b3_recibo_v398.py", "delta_v398.py", "quadro_v397.py", "runtime_quadro_v397.py", "sonico_v398", "kh_n1_cobertura_v398",
                                  "PINOS_BN_v398.json", "PINOS_BATERIA_v398.json", "recibo_pre_selo", "esboco_R3_5", "kernel_recibo", "bateria_pos_selo", "tem_pino cadeia_de_selos", "--recibo-pre-selo-sha256 \"$RPS\"",
                                  "--selo-anterior \"$W_SELO\"", "--kernel-manifesto-anterior \"$W_KMAN\"", "--kernel-recibo \"$W_KR\" --kernel-recibo-sha256 \"$KRSHA\"", "gerar_bateria_r3_4.py", "ORDEM=\"0 1 2 3 4 5 6 7 8 9 10 10a 10b 10c 11 12 13 14\"",
                                  "CHAIN_DE", "CHAIN_ATE", "parar()", "aguarda()", "SUPERFICIES RECUSOU (rc=3)"],
       "b3_recibo_v398.py": ["REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA", "REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO", "versao_alvo", "\"v398\"", "PINOS_BN_v398.json", "__SALTO_", "BATERIA_PASSA", "manifesto_anterior", "pinos_da_versao"],
       "harness_textos_ensaio_v398.py": ["harness_saida_v398", "dry_v398", "guarda_p18_v398", "--nao-exigir-refazer", "rotas._valida", "_sonico_ln2", "_sonico_entropia", "_afinacao_zeta", "_afinacao_hipotese", "_afinacao_geometria", "_afinacao_deriva", "_afinacao_kappa", "_gerencia_como_operador", "_inscricao_adulterada",
                                         "_numero_adulterado", "_z_disc_acima_de_5", "_fonte_adulterada", "_fock_dentro_da_pedra", "_face_do_psibit_habitada", "sonico_v398", "PKG_ANT", "refazer_exigido", "paragrafo_readme_e_regra_do_4_44", "paragrafo_sonico_e_atribuicao_da_gerencia", "verificar_paragrafo_readme",
                                         "verificar_paragrafo_sonico", "atribuicao_da_gerencia", "cenario_a_memory_md_real", "cenario_b_com_folga", "cenario_c_no_limite", "quadro_v397", "regra_do_4_44_nos_textos_violacoes", "f_conf"],
       "harness_fechar_sandbox_v398.py": ["fechar_sandbox", "FECHAR RECUSADO", "registrar_mapa_v398.py", "SINTETICO", "TGLExt/Sonico.lean", "TGLExt/AfinacaoDasCordas.lean", "TGLExt_Sonico.lean", "TGLExt_AfinacaoDasCordas.lean", "paragrafo_no_handoff", "paragrafo_sonico_no_handoff", "fechar_resultado_adulterado", "fechar_numero_adulterado",
                                          "fechar_sonico_adulterado", "fechar_gerencia_como_operador", "INICIO_PARAGRAFO_README_v397", "quadro_v397"]}
INV_AUTORAIS = {"textos_v398.py": ["_MARCA_PENDENTE", "TOPICO_NOVO", "def handoff(", "def linhagem(", "def desenho(", "def atlas(", "def core_memory(", "def haja_luz(", "def aviso(", "def aviso_pulado(", "def topico_missao(", "def topico_central(", "def topico_estatuto(", "def topico_novo(",
                                   "def linha_handoff(", "def marca_missao(", "def id_missao(", "def id_central(", "def _d(", "def _num(", "_cita(", "_cita_sg(", "_ger(", "def _kernel_tem(", "def _um_tem(", "def _limites(", "def _erratas(", "def _legal(", "def _sonico(", "def _afinacao(", "def _pedras(",
                                   "def _regra_do_4_44(", "def paragrafo_readme(", "def verificar_paragrafo_readme(", "def paragrafo_sonico(", "def verificar_paragrafo_sonico(", "def atribuicao_da_gerencia(", "INICIO_PARAGRAFO_README_v397", "FIM_PARAGRAFO_README_v397",
                                   "INICIO_PARAGRAFO_SONICO_v398", "FIM_PARAGRAFO_SONICO_v398", "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina", "v398-selada-sonico-e-afinacao-das-cordas.md", "NÃO é fala do operador"],
                "registrar_mapa_v398.py": ["_MARCA_PENDENTE", "def montar(", "umpy.v398.sonico_e_afinacao_das_cordas_na_fractalizacao_do_um", "kernel.sonico_v398_candidata_23out", "kernel.afinacao_das_cordas_v398_candidata_23out", "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9",
                                           "assert selo.get(\"um_version\") == \"v398\"", "NAO escreve", "registro_mapa_v398.json", "regra_4_44"]}
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
        ok = x in autorais_txt[n]
        conf[n][x[:90]] = ok
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
        r = subprocess.run(["sh", "-n", os.path.join(HERE, n)], capture_output=True, text=True)
        sint[n] = "sh -n rc=%d %s" % (r.returncode, r.stderr[:200])
        if r.returncode:
            falhas.append((n, "sh -n"))
    if "\r" in tx:
        falhas.append((n, "CR no arquivo"))
# os portoes do B(n): os blocos 10a e 10c sao IDENTICOS ao molde subido de versao; no 10b, as linhas de portao (aguarda/B3_AUTORIZADO/EVENTO/RECIBO_PARADA) sao as do molde
molde_b = sobe(MOL["chain_pos_rito_v397.sh"])
CHAIN = DER["chain_pos_rito_v398.sh"]
molde_bloco = lambda t, ini, fim: Arq("x", t).bloco(ini, fim)
for ini, fim in (("if quer 10a; then", "if quer 10b; then"), ("if quer 10c; then", "if quer 11; then")):
    ia, ja, La = molde_bloco(molde_b, ini, fim); ib, jb, Lb = molde_bloco(CHAIN, ini, fim)
    if La[ia:ja] != Lb[ib:jb]:
        falhas.append(("portao do B(n) difere do molde subido de versao", ini))
    else:
        conf.setdefault("chain_pos_rito_v398.sh", {})["trecho identico ao molde (sobe): " + ini] = True
ia, ja, La = molde_bloco(molde_b, "if quer 10b; then", "if quer 10c; then"); ib, jb, Lb = molde_bloco(CHAIN, "if quer 10b; then", "if quer 10c; then")
gate = lambda L_: [l for l in L_ if any(k in l for k in ('aguarda "', "B3_AUTORIZADO", "[ -n \"$EVENTO\"", "RECIBO_PARADA", "EVENTO_HASH", "--evento", "--modo aplicar", "--fase pos_selo"))]
if gate(La[ia:ja]) != gate(Lb[ib:jb]):
    falhas.append(("as linhas de portao do 10b diferem do molde subido de versao", [x for x in gate(Lb[ib:jb]) if x not in gate(La[ia:ja])][:2]))
else:
    conf.setdefault("chain_pos_rito_v398.sh", {})["linhas de portao do 10b identicas ao molde (sobe)"] = True
# os passos 4 a 9 e 11 a 14 do chain: identicos ao molde subido (so' as trocas dos marcadores)
for ini, fim in (("if quer 4; then", "if quer 10; then"), ("if quer 12; then", 'echo "== FIM')):
    ia, ja, La = molde_bloco(molde_b, ini, fim); ib, jb, Lb = molde_bloco(CHAIN, ini, fim)
    esp_ = [l.replace(MARC_MOLDE, MARC_NOVO) for l in La[ia:ja]]
    if esp_ != Lb[ib:jb]:
        falhas.append(("os passos do chain diferem do molde subido alem das trocas ditas", ini))
    else:
        conf.setdefault("chain_pos_rito_v398.sh", {})["passos identicos ao molde (sobe + marcadores): " + ini] = True
# os passos 0 a 3 do chain: so' as linhas NOVAS declaradas (marcadores) diferem do molde subido, fora o cabecalho (a lista de ferramentas e a copia do quadro ja' saem do molde subido)
ia, ja, La = molde_bloco(molde_b, "PK=", "if quer 4; then"); ib, jb, Lb = molde_bloco(CHAIN, "PK=", "if quer 4; then")
set_a = set(La[ia:ja]); novas_l = [l for l in Lb[ib:jb] if l not in set_a]
DECL = (MARC_NOVO,)
estranhas = [l for l in novas_l if not any(d in l for d in DECL)]
if estranhas:
    falhas.append(("os passos 0 a 3 e as funcoes do chain diferem do molde subido alem das trocas ditas", estranhas[:3]))
else:
    conf.setdefault("chain_pos_rito_v398.sh", {})["passos 0 a 3 e funcoes: so' as %d linha(s) novas declaradas diferem do molde (sobe)" % len(novas_l)] = True
# marcas pendentes: nenhuma em nenhum arquivo (nem derivado, nem autoral)
marcas = {n: len(GUARDA_PENDENTE_RX.findall(tx)) for n, tx in list(todos.items()) + list(autorais_txt.items()) if GUARDA_PENDENTE_RX.search(tx)}
if marcas:
    falhas.append(("marca de texto pendente", marcas))
for n in ("fechar_v398.py", "textos_v398.py", "registrar_mapa_v398.py"):
    tx = todos.get(n) or autorais_txt.get(n) or ""
    if n in (todos.keys() | autorais_txt.keys()) and "_MARCA_PENDENTE" not in tx:
        falhas.append((n, "sem a guarda de pendencia (_MARCA_PENDENTE)"))
# a palavra da marca nunca por extenso fora das formas montadas por concatenacao
for n, tx in list(todos.items()) + list(autorais_txt.items()):
    if PALAVRA in tx.replace('"' + PALAVRA + '" +', "").replace("_MARCA_PENDENTE = ", ""):
        falhas.append((n, "a palavra da marca aparece por extenso"))
# nomes fantasma (objetos do um.py da v397 que nao existem na v398)
for n, tx in list(todos.items()) + list(autorais_txt.items()):
    fant = sorted({m.group(0) for m in ENC.FANTASMAS.finditer(tx)})
    if fant:
        falhas.append(("nome fantasma", n, fant[:4]))
# rotulos de versao: nenhum resto de 390-397 onde o sentido e' 'esta versao'. O que fica com 397/396/395/394/393 e' so' a versao ANTERIOR ou nome historico (lista conferida)
OK_HIST = ("_V394_", "_V395_", "_V396_", "_V397_", "fechar_v390", "C13_kh_n1_v394", "C13_kh_n1_v395", "C13_kh_n1_v396", "C13_kh_n1_v397", "C12__V396", "C12__V395", "C12__V394", "ponto_fixo_v394_d19", "pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393",
           "kh_n1_cobertura_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "testemunha_estatica_v396",
           "cunhagens_v396", "kh_n1_cobertura_v396", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "registros_v397", "declaration_sources", "umpy.v394", "umpy.v395", "umpy.v396", "umpy.v397", "kernel.psibit_v395", "kernel.testemunha_estatica_v396",
           "REG_V393", "REG_V394", "REG_V395", "REG_V396", "REG_V397", "base_v397", "selo_anterior_v397", "kernel_manifesto_anterior_v397", "handoff-v397-custodia", "vereditos_v397", "escada_v397_e_v398", "DIFF_v397_v398", "leitura_v397.py", "superficies_v397.py", "fechar_v397.py",
           "chain_pos_rito_v397.sh", "b3_recibo_v397.py", "derivar_cadeia_v397.py", "textos_v397.py", "registrar_mapa_v397.py", "ext_bin394", "ext_psb395", "ext_tes396", "ext_tok397", "ESPERADOS_v397", "PINOS_BN_v397", "rito_v397", "cadeia_de_selo/v397", "cadeia_de_selo\\v397",
           "axiom_coverage_v392", "KH_N1_v392", "varredura_e_sorry_v392", "estatuto_da_prova_v391", "fundacao_v390", "three_stress_tests_v387", "pedras_v392", "kh_n1_cobertura_v392", "RECIBO_SINCRONIZACAO_v397", "psibit_na_fractalizacao", "candidata_21out", "candidata_22out",
           "B7-v397", "pos_rito_v397", "v397_incorporacao", "um_v397", "MANIFESTO_ARQUIVO_v397", "v397_kernel", "v397_selo", "tgl_kernel_v397", "pilar_anterior_v397", "quadro_v397", "runtime_quadro_v397", "_v397_atomos", "INICIO_PARAGRAFO_README_v397", "FIM_PARAGRAFO_README_v397",
           "v397_cun_", "token_e_veracidade_preparo", "[v397")        # "[v397": as duas linhas [v397] do stdout que o main da v398 segue imprimindo (o Teste da Unica Palavra e as cunhagens da v397), lidas pela leitura
resid = {}
for n, tx in list(todos.items()):
    if n.startswith("harness_") or n in AUTORAIS:
        continue       # os harness trazem de proposito rotulos de versoes anteriores (controles negativos); os autorais citam a v397 como historico
    for m in re.finditer(r"[A-Za-z0-9_\-\.\[\]/\\]*(?<![0-9a-f])39[0-7][A-Za-z0-9_\-\.\[\]]*", tx):
        tok = m.group(0).rstrip(".")
        if re.fullmatch(r"[0-9a-f]*39[0-7][0-9a-f]*", tok) and len(tok) >= 8:
            continue   # hash hexadecimal
        resid.setdefault(tok, set()).add(n)
estranhos = {}
for tok, ns in resid.items():
    if "398" in tok:
        continue
    if any(p in tok for p in OK_HIST) or tok in ("v397", "v396", "v395", "v394", "v393", "v392", "v391", "v390", "V397", "V396", "V395", "V394", "V393", "397", "396", "395", "394", "393"):
        continue
    estranhos[tok] = sorted(ns); falhas.append(("rotulo estranho com 390-397", tok, sorted(ns)))
# a guarda de texto (P18) sobre todo arquivo de narrativa e de cadeia
from guarda_p18_v398 import violacoes
gv = {n: violacoes(tx) for n, tx in list(todos.items()) + list(autorais_txt.items())}
if any(gv.values()):
    falhas.append(("guarda P18", {k: v[:3] for k, v in gv.items() if v}))
# cada T.<nome> chamado pelos derivados e pelo registrar existe em textos_v398.py
ttxt = autorais_txt.get("textos_v398.py", "")
chamados = sorted({m for n in ("superficies_v398.py", "fechar_v398.py", "harness_textos_ensaio_v398.py", "harness_fechar_sandbox_v398.py") for m in re.findall(r"\bT\.([A-Za-z_][A-Za-z_0-9]*)", todos[n])} | {m for m in re.findall(r"\bT\.([A-Za-z_][A-Za-z_0-9]*)", autorais_txt.get("registrar_mapa_v398.py", ""))})
faltam = [c for c in chamados if not re.search(r"(?m)^(def %s\(|%s = )|; %s = " % (re.escape(c), re.escape(c), re.escape(c)), ttxt)]
if ttxt and faltam:
    falhas.append(("textos_v398.py nao define o que os derivados chamam", faltam))
# o que os derivados leem de ESPERADOS/CANDIDATO/PINOS (campos), conferido contra os arquivos desta cadeia
RX = {"ESPERADOS": re.compile(r"(?:ESP(?:ERADOS)?|esp)\[['\"]([^'\"]+)['\"]\]|(?:ESP|esp)\.get\(['\"]([^'\"]+)['\"]"), "CANDIDATO": re.compile(r"CM\[['\"]([^'\"]+)['\"]\]|CM\.get\(['\"]([^'\"]+)['\"]")}
alltxt = dict(todos); alltxt.update(autorais_txt)
campos = {"ESPERADOS": sorted({a or b for tx in alltxt.values() for a, b in RX["ESPERADOS"].findall(tx)}), "CANDIDATO": sorted({a or b for tx in alltxt.values() for a, b in RX["CANDIDATO"].findall(tx)})}
presentes = {}
for rotulo, arq in (("ESPERADOS", "ESPERADOS_v398.json"), ("CANDIDATO", "CANDIDATO_v398.json"), ("PINOS_BN", "PINOS_BN_v398.json")):
    p = os.path.join(PK, arq)
    if os.path.exists(p):
        d = json.load(open(p, encoding="utf-8"))
        lido = campos.get(rotulo) or ["criterios", "esboco_R3_5", "gerador_bateria", "driver_t12_t14", "bateria_base_R2", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "recibo_pre_selo", "selo_anterior_v397", "kernel_manifesto_anterior_v397"]
        presentes[rotulo] = {"arquivo_sha16": sha16(open(p, "rb").read()), "faltam": [c for c in lido if c not in d]}
        if presentes[rotulo]["faltam"]:
            falhas.append(("campo de %s lido pelos derivados e ausente do arquivo" % rotulo, presentes[rotulo]["faltam"]))
    else:
        presentes[rotulo] = {"arquivo": "ausente"}; falhas.append((arq, "ausente"))
por_regra = {}
for arq_, nome_, c_, n_ in REGRAS:
    por_regra.setdefault(arq_, []).append({"regra": nome_, "casou": c_, "esperado": n_})
DERJ = {"molde": {n: {"sha16": sha16(MOL_RAW[n]), "sha256": sha256(MOL_RAW[n])} for n in MOL_RAW}, "molde_confere_com_DERIVACAO_v397": MOLDE_CONFERE, "molde_derivar_cadeia_v397": sha16(open(os.path.join(MOLDE, "derivar_cadeia_v397.py"), "rb").read()),
        "ferramenta_de_subida": {"derivar_encanamento_v398.py": sha16(open(os.path.join(PK, "derivar_encanamento_v398.py"), "rb").read()), "reuso": "bump(), PROT, FANTASMAS e FANT_PRE importados (nada executado no import)", "protecao_adicional": list(EXTRA_PROT)},
        "derivados": {n: {"sha16": sha16(todos[n].encode("utf-8")), "sha256": sha256(todos[n].encode("utf-8"))} for n in todos},
        "autorais": {n: {"sha16": sha16(autorais_txt[n].encode("utf-8")), "sha256": sha256(autorais_txt[n].encode("utf-8"))} for n in autorais_txt},
        "sobe": "396 -> 397 e 397 -> 398 numa passada so', fronteira de digitos (bump() de derivar_encanamento_v398); PROT (nomes nascidos no um.py, nao sobem) = ENC.PROT + " + ", ".join(EXTRA_PROT),
        "regras_com_contagem_exata": por_regra,
        "o_que_difere_do_molde": {"chain": "cabecalho escrito para a v398 (numeros LIDOS de ESPERADOS e PINOS_BN); marcadores dos passos 3 e 9 = sonico_v398 e kh_n1_cobertura_v398; passo 0 exige quadro_v397.py e runtime_quadro_v397.py e o passo 1 os copia byte a byte (saem do molde subido, com o quadro protegido); "
                                 "o resto e' o molde subido (passo 10 SIMPLES v397 -> v398, sem salto, B8; pinos selo_anterior_v397 e kernel_manifesto_anterior_v397; kernel_recibo R3_2; V398_AUTORIZACAO_OPERADOR)",
                                 "leitura": "quatro registros novos (sonico_v398, afinacao_das_cordas_v398 com funcao; cunhagens_v398 e kh_n1_cobertura_v398 por spec); cada pedra no kernel do rito (bandeira True, composicao no trio, modulo da pedra, contrato e suporte); numeros do sonico e da afinacao == ESPERADOS; hipotese KNOWN, geometria OPEN, "
                                            "nada deriva cordas do axioma, kappa fora do core; as seis inscricoes por sha256 com a sexta rotulada da gerencia; o quadro do topo segue selado e igual (registro == ESPERADOS e == resultado pinado; conferencia do rito diz que segue no topo); registros da v397 a v393 seguem selados; "
                                            "linhas [v398] e [v397] do stdout; AVISO da v398 (e de bloco v393 a v397) reprova; a face de Fock vem da base v397 (copia de bytes), nao de ESPERADOS",
                                 "superficies": "so' o cabecalho e a ancora (a linha do handoff da v397); SEM COMPACTACAO, rc 3 se passar de 195 linhas ou 24.000 B",
                                 "fechar": "o handoff traz os DOIS paragrafos do README/site: o do QUADRO (T.paragrafo_readme, o da v397, com os marcadores da v397) e o NOVO (T.paragrafo_sonico, verificado por T.verificar_paragrafo_sonico); RECUSA (rc 2) antes de escrever se qualquer um falhar; o manifesto traz os dois",
                                 "b3_recibo": "so' a subida de versao (a logica do B(n) simples nao muda; o harness a exercita com recibos sinteticos)",
                                 "harness": "os harness da v397 subidos + regras nomeadas; %d controles negativos da leitura (os dois registros novos, as pedras, as inscricoes, o quadro do topo, os registros anteriores, o stdout); paragrafo do quadro com %d controles e a regra do 4,44 em todo texto; paragrafo novo com %d controles; "
                                            "atribuicao da gerencia e citacao verbatim; %d controles de registrar_mapa; ensaio do MEMORY.md em tres cenarios; no fechar: controles do resultado pinado, do numero do quadro, do numero do sonico e da gerencia como operador, e a conferencia dos dois paragrafos nos dois handoffs"
                                            % (NEG_HT.count("variante("), NEW_4B.count('_mut("'), NEW_4B.count('_muts("'), MAPA_CTL.count('"regra_4_44_') + MAPA_CTL.count('"montar_recusa_')),
                                 "textos, registrar_mapa": "AUTORAIS (escritos para o delta da v398; nenhuma marca pendente)"},
        "marcas_texto_a_reescrever": {"por_arquivo": marcas, "total": sum(marcas.values())}, "campos_lidos_dos_arquivos_da_v398": campos, "arquivos_da_v398_no_pacote": presentes,
        "invariantes": conf, "sintaxe": sint, "guarda_p18": {k: ("LIMPO" if not v else v[:3]) for k, v in gv.items()}, "rotulos_estranhos": estranhos, "textos_definem_o_que_os_derivados_chamam": {"chamados": chamados, "faltam": faltam}, "falhas": falhas,
        "nao_validado": "nenhum derivado foi EXECUTADO contra o Nos real nem revisto por cetico independente; so' ast.parse, sh -n, invariantes, rotulos, guarda P18 e os harness (textos, leitura, superficies em COPIAS, b3_recibo, fechar e registrar_mapa em SANDBOX, tudo com recibos SINTETICOS e Nos EMULADO)"}
grava("DERIVACAO_v398.json", json.dumps(DERJ, ensure_ascii=False, indent=1))
print("DERIVADOS:", ", ".join("%s %s" % (n, DERJ["derivados"][n]["sha16"]) for n in DERJ["derivados"]))
print("AUTORAIS:", ", ".join("%s %s" % (n, DERJ["autorais"][n]["sha16"]) for n in DERJ["autorais"]))
print("SINTAXE:", json.dumps(sint, ensure_ascii=False))
print("MARCAS texto:", json.dumps(marcas, ensure_ascii=False))
print("REGRAS:", sum(len(v) for v in por_regra.values()), "regras com contagem exata")
print("INVARIANTES:", sum(len(v) for v in conf.values()), "conferidos;", "FALHAS:", falhas if falhas else "nenhuma")
sys.exit(1 if falhas else 0)
