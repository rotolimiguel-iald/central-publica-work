# -*- coding: utf-8 -*-
"""derivar_cadeia_v399.py -- DERIVA a cadeia pos-rito da v399 a partir do molde REAL e FINAL da v398 (cadeia_de_selo/v398/pos_rito, o que RODOU de verdade em 23-24/10; seus arquivos conferem com a DERIVACAO_v398.json por sha16).
A subida de versao REUTILIZA o bump() e as listas PROT/FANTASMAS/FANT_PRE de derivar_encanamento_v399.py (a ferramenta de subida de versao da cadeia: 397 -> 398 e 398 -> 399 numa passada so', fronteira de digitos, nomes nascidos no
um.py PROTEGIDOS), com PROTECAO ADICIONAL de tres nomes que o bump subiria e nao devia (o QUADRO do Teste da Unica Palavra fica com o nome da v397: quadro_v397 / runtime_quadro_v397; e os marcadores INICIO/FIM_PARAGRAFO_README_v397 do
paragrafo do quadro, que o handoff da v399 repete como a v397 os gerou). Os registros da v398 (sonico_v398, afinacao_das_cordas_v398, cunhagens_v398, kh_n1_cobertura_v398, registros_v398) e os anteriores sao nomes PROTEGIDOS: onde o texto da v398
os usava como "os desta versao", uma REGRA NOMEADA COM CONTAGEM EXATA os troca pelos da v399 (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, cunhagens_v399, kh_n1_cobertura_v399, registros_v399); o script ABORTA se uma regra nao casar o numero esperado de vezes.
GERA: chain_pos_rito_v399.sh, leitura_v399.py, superficies_v399.py, fechar_v399.py, b3_recibo_v399.py (so' a subida: a logica do B(n) simples nao muda), harness_textos_ensaio_v399.py e harness_fechar_sandbox_v399.py (os harness da v398 subidos + regras).
CONFERE (autorais, escritos para a v399; a logica muda e uma derivacao mecanica nao a cobriria): textos_v399.py, registrar_mapa_v399.py (ast.parse, invariantes, guarda P18, nenhuma marca pendente, e cada T.<nome> chamado pelos derivados existe em textos_v399.py).
DESVIOS DO MOLDE (ditos): (1) o conferidor da v399 roda SEM -I (importa o um.py instalado e precisa do numpy do usuario) e NO LUGAR (cd $PK), porque acha o delta, o runtime e os insumos pelo caminho da propria pasta; os harness o rodam numa COPIA em arvore;
(2) a LEITURA le o sidecar um_absoluto_selo_acom.json e aceita, como linha final do rito, a linha do sidecar logo depois da linha do colapso tipado (o main da v399 imprime a do sidecar por ultimo); (3) o fechar copia o sidecar e o selo para v399_selo e os lista no manifesto e no handoff;
(4) a linha do handoff no MEMORY.md soma +1 (o gancho da missao SUBSTITUI a linha velha), a superficie NAO compacta e RECUSA com rc 3 se passar de 195 linhas ou 24.000 B;
(5) os dois harness rodam SEM -I (python -B -X utf8): geram o sidecar com a funcao do PROPRIO candidato (importam o um.py do Nos emulado) e o um.py da v399 importa o numpy do usuario no topo; o -I (que ignora o site do usuario) faria o import falhar (visto na rodada de depuracao 1).
NAO executa nenhum script derivado: so' ast.parse, sh -n, invariantes, rotulos e a guarda de texto P18. Nao toca o Nos, a Bancada, a memoria, o Atlas, o mapa, o quadro, o tunel, o site nem o git; nada fora de pos_rito e' escrito.
Os numeros do cabecalho do chain (bandeiras, escada, geracao do B(n)) sao LIDOS de ESPERADOS_v399.json e PINOS_BN_v399.json aqui, nunca digitados.
GRAVA: DERIVACAO_v399.json (sha256 de ENTRADA e de SAIDA de cada arquivo; sha16 do molde, de cada derivado e de cada autoral; invariantes; sintaxe; marcas; rotulos; contagem de cada regra). Reexecutavel: o que muda ganha .bak_<STAMP>_c1 (backup de BYTES).
Uso: python -I -B -X utf8 derivar_cadeia_v399.py"""
import ast, hashlib, json, os, re, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)
sys.path.insert(0, PK)
import derivar_encanamento_v399 as ENC      # bump(), PROT, FANTASMAS, FANT_PRE (reuso; nada e' executado no import)
MOLDE = os.path.join(os.path.dirname(PK), "v398", "pos_rito")
STAMP = time.strftime("%Y%m%d_%H%M%S")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
sha256 = lambda b: hashlib.sha256(b).hexdigest()
PALAVRA = "TEXTO_A_" + "REESCREVER"          # a palavra da marca, montada por concatenacao: este arquivo nunca a traz por extenso
MARCA = PALAVRA + "_V399"
MODELOS = ("leitura_v398.py", "superficies_v398.py", "fechar_v398.py", "chain_pos_rito_v398.sh", "b3_recibo_v398.py", "harness_textos_ensaio_v398.py", "harness_fechar_sandbox_v398.py")
AUTORAIS = ("textos_v399.py", "registrar_mapa_v399.py")
GUARDA_PENDENTE_RX = re.compile(r"(?m)^\s*#\s*" + MARCA)
EXTRA_PROT = ("quadro_v397", "INICIO_PARAGRAFO_README_v397", "FIM_PARAGRAFO_README_v397")     # o bump subiria estes tres e nao devia (ver o docstring)
REGRAS = []                                                                                    # (arquivo, nome, casou, esperado)


def sobe(t):
    """subida de versao em UMA passada (397 -> 398, 398 -> 399): o bump() de derivar_encanamento_v399, com os nomes extras protegidos por marcadores."""
    for i, p in enumerate(EXTRA_PROT):
        t = t.replace(p, "@@Q%d@@" % i)
    t = ENC.bump(t)
    for i, p in enumerate(EXTRA_PROT):
        t = t.replace("@@Q%d@@" % i, p)
    return t


def sem_hex(t, nome):
    """nenhuma ocorrencia de 397/398 dentro de uma palavra HEXADECIMAL (um hash seria subido por engano)."""
    for m in re.finditer(r"[0-9A-Za-z_]*(?<![0-9])39[78](?![0-9])[0-9A-Za-z_]*", t):
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
        """troca sobe(old) por `new` (texto FINAL, nunca subido), exigindo exatamente n ocorrencias; `old` e' o texto do MOLDE (v398)."""
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


# =============================================================================== o molde (v398 FINAL) e os dados que o cabecalho do chain e as notas leem (nada digitado)
MOL_RAW = {n: open(os.path.join(MOLDE, n), "rb").read() for n in MODELOS}
MOL = {n: b.decode("utf-8") for n, b in MOL_RAW.items()}
for n_, tx_ in MOL.items():
    sem_hex(tx_, n_)
    fp_ = sorted({m.group(0) for m in ENC.FANT_PRE.finditer(tx_)})
    assert not fp_, ("o molde da v398 traz nome da v399 (a protecao falhou antes de comecar)", n_, fp_[:4])
DER98 = json.load(open(os.path.join(MOLDE, "DERIVACAO_v398.json"), encoding="utf-8"))
reg98 = {n: v["sha16"] for n, v in DER98["derivados"].items()}; reg98.update({n: v["sha16"] for n, v in DER98["autorais"].items()})
MOLDE_CONFERE = {n: (sha16(MOL_RAW[n]) == reg98.get(n)) for n in MODELOS}
assert all(MOLDE_CONFERE.values()), ("o molde da v398 difere da DERIVACAO_v398.json (foi editado depois da derivacao ou do rito?)", MOLDE_CONFERE)
ESP = json.load(open(os.path.join(PK, "ESPERADOS_v399.json"), encoding="utf-8"))
PIN = json.load(open(os.path.join(PK, "PINOS_BN_v399.json"), encoding="utf-8"))
_bp = PIN["recibo_pre_selo"]["bancada_pina"]
GER_ATUAL = int(re.match(r"^B(\d+)-", _bp["deployment_id"]).group(1))
N_FLAGS = ESP["n_bandeiras_novas"]
assert _bp["version"] == "v398" and PIN["recibo_pre_selo"].get("sem_salto") is True and "cadeia_de_selos" not in PIN
assert N_FLAGS == ESP["n_bandeiras_por_grupo"]["testemunho"] and ESP["kernel"]["modulos_novos"] == 1
ESC0, ESC1 = ESP["escada_v398_e_v399"]

# =============================================================================== leitura_v399.py
HEAD_L = ('# -*- coding: utf-8 -*-\n'
          '# A LEITURA da rodada v399 (molde: leitura_v398.py FINAL, o que rodou em 24/10): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v399, que aqui e\' o proprio pacote).\n'
          '# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e\' digitado: tudo sai dos JSON, do core, do selo, do sidecar e do stdout do rito.\n'
          '# v399: os registros NOVOS do core sao selo_pela_propria_tecnologia_v399 e declaracao_do_operador_v399 (com FUNCAO, no runtime: lidos NA FRACTALIZACAO DO UM, logo depois da afinacao_das_cordas_v398; o primeiro sela os bytes do PROPRIO um.py ao lado do SHA-256\n'
          '# pelo metodo do operador, EMBUTIDO; o segundo REGISTRA a declaracao do operador de 24/10 [DECLARACAO DO OPERADOR / INPUT] e LE do kernel do proprio rito as dez ancoras e a pedra) e cunhagens_v399 e kh_n1_cobertura_v399 (por spec; ESPERADOS[registros_v399]);\n'
          '# os da v398 (sonico_v398, afinacao_das_cordas_v398, cunhagens_v398, kh_n1_cobertura_v398), os da v397 (teste_de_veracidade_fase9_v397, cunhagens_v397, kh_n1_cobertura_v397), os da v396, os da v395, os da v394 e os da v393 seguem no core e tem de seguir selados.\n'
          '# O modulo novo de kernel (TGLExt/Testemunho.lean) vem de ESPERADOS[pedras_sha256] e e\' conferido aqui contra o arquivo do kernel do Nos. A escada vem de ESPERADOS[escada_v398_e_v399] e ESPERADOS[escada]; a troca dita (so numeros) e\' a de ESPERADOS[troca_dita].\n'
          '# O SIDECAR um_absoluto_selo_acom.json (arquivo NOVO da custodia) e\' lido aqui: existe, e\' JSON valido, o veredito e\' ALL_OBJECTS_SEALED, tem os tres objetos (um.py, core e selo) com o SHA-256 igual ao dos arquivos do Nos, sem recusas, com a secao de honestidade (confidencialidade NAO alegada).\n'
          '# A DIRECAO DO TESTEMUNHO e\' conferida nos registros: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador (nenhuma frase inverte a direcao; as quatro inscricoes de 24/10 sao TODAS falas do operador, nenhuma e\' da gerencia).\n'
          '# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual: o registro teste_de_veracidade_fase9_v397 == ESPERADOS e == o resultado pinado, o quadro sela nas duas linguas, e a conferencia do rito diz que ele segue no topo (artigo PT/EN e .md).\n'
          '# A face de Fock do psion segue CONDICIONAL (psibit_v395 e testemunha_estatica_v396); as linhas `[v399]`, `[v398]` e `[v397]` do stdout do rito dizem os vereditos e registros por spec selados == registros por spec; o AVISO da v399 (e de qualquer bloco v393 a v398) no stdout reprova.\n'
          '# DESVIO DO MOLDE (dito): a linha final do rito deixou de ser a do colapso tipado: o main da v399 imprime, por ultimo, a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), logo depois da do colapso tipado; a leitura exige as DUAS, nessa ordem.\n'
          '# Diferencas para a v398: V[\'selo\'], V[\'declaracao\'], V[\'sidecar\'], V[\'testemunho\'], V[\'cunhagens\'], V[\'pedras_kernel\'], V[\'reg399\'] e V[\'patch_ids\'] sao os campos da v399.\n')
NOVAS_CONSTS = '''REG_V393 = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")   # da v393: seguem no core e seguem selados (nao sao 'novos' da v399)
REG_V394 = ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394")   # da v394: seguem no core e seguem selados (nao sao 'novos' da v399)
REG_V395 = ("psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395")   # da v395: seguem no core e seguem selados (nao sao 'novos' da v399)
REG_V396 = ("testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396")   # da v396: seguem no core e seguem selados (nao sao 'novos' da v399)
REG_V397 = ("teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397")   # da v397 (o Teste da Unica Palavra, a pedra Token e as falas de 23/10): seguem no core e seguem selados; o quadro do topo le o primeiro
REG_V398 = ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398")   # da v398 (o sonico, a afinacao das cordas e as falas de 23/10): seguem no core e seguem selados (nao sao 'novos' da v399)
REG_FIXOS = ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")   # os QUATRO registros NOVOS do core v399 (dois com FUNCAO, no runtime; dois por spec); + os de ESPERADOS[registros_v399] (REG_TODOS, dentro de ler)
SIDECAR_RE = re.compile(r'^\\[selo_acom\\] (TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED\\S*) ; objetos (\\d+) ; recusas (\\d+)$')   # a linha que o main da v399 imprime por ultimo (selo_acom_sidecar_v399)
_RX_INV = re.compile(r'IALD\\s+testifica\\s+(?:a\\s+mim|do\\s+operador|de\\s+mim)')   # a DIRECAO invertida (a IALD como quem testifica DO operador); so' a fala em que ele a recusa escapa'''
NOVAS_FUNCS = '''def _feq(a, b):
    """igualdade dos NUMEROS dos registros: floats com tolerancia relativa 1e-12 (a mesma maquina deve dar igual), o resto exato; recursiva em dict/list."""
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_feq(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_feq(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float):
        return a == b or abs(a - b) <= 1e-12 * max(1.0, abs(a), abs(b))
    return a == b


def _inv(t):
    """True se o texto poe a IALD como quem testifica DO operador (a DIRECAO invertida), fora da fala em que o operador a recusa ('... nao podia dizer que IALD testifica a mim ...')."""
    for m in _RX_INV.finditer(t):
        ant = t[max(0, m.start() - 40):m.start()].lower()
        if not (ant.endswith('nao ') or ant.endswith('não ') or 'podia dizer que ' in ant):
            return True
    return False


_BASE_CORE = {}


def _base_core(pk):
    """O core da v398 SELADA (copia de bytes em PK/base_v398): de onde saem o teorema e o modulo da face de Fock da testemunha (nenhum nome digitado); lido uma vez por caminho."""
    p = os.path.join(pk, 'base_v398', 'um_absoluto.json')
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
                P.append('a conferencia do rito diz que o quadro do topo (O Teste da Unica Palavra, %s) NAO segue no topo com os numeros do resultado pinado' % l_)
        ai_ = C.get('acom_itens') or {}
        V['acom_itens'] = {k_: (v_ or {}).get('ok') for k_, v_ in ai_.items()}
        faltam_ = [k_ for k_ in ('C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'round_trip_do_um_py_instalado_independente') if (ai_.get(k_) or {}).get('ok') is not True]
        if faltam_:
            P.append('a conferencia do rito diz que itens do selo pela propria tecnologia NAO conferiram (C1 a C14 e o round trip do um.py instalado): %s' % faltam_)
        sci_ = C.get('sidecar') or {}
        if not (sci_.get('existe') is True and str(sci_.get('veredito') or '').startswith('TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED')):
            P.append('a conferencia do rito diz que o sidecar um_absoluto_selo_acom.json nao existe ou nao esta selado')'''
NOVO_FINAL = '''    linhas = [l for l in out.splitlines() if l.strip() and not TRAILER_RE.match(l.strip())]
    if len(linhas) < 2 or not SIDECAR_RE.match(linhas[-1].strip()) or not FINAL_RE.match(linhas[-2]):
        P.append('as duas ultimas linhas do stdout nao sao a linha final do rito ([selo] colapso tipado) seguida da linha do sidecar ([selo_acom] ... ALL_OBJECTS_SEALED ; objetos N ; recusas 0)')
    else:
        m_sc_ = SIDECAR_RE.match(linhas[-1].strip())
        if int(m_sc_.group(3)) != 0 or int(m_sc_.group(2)) != len((ESP.get('sidecar') or {}).get('objetos') or []):
            P.append('a linha do sidecar no stdout nao diz %d objetos e 0 recusas (%s)' % (len((ESP.get('sidecar') or {}).get('objetos') or []), linhas[-1].strip()[-40:]))'''
NOVO_STDOUT = r'''    if [l for l in out.splitlines() if '[v399] AVISO' in l or '[selo_acom] AVISO' in l]:
        P.append('o stdout traz AVISO da v399 (o selo ACOM, a declaracao do operador, os registros por spec ou o sidecar nao rodaram): %s' % [l.strip()[:200] for l in out.splitlines() if '[v399] AVISO' in l or '[selo_acom] AVISO' in l][:2])
    elif [l for l in out.splitlines() if re.search(r'\[v39[3-8]\] AVISO', l)]:
        P.append('o stdout traz AVISO de um bloco anterior (v393 a v398): %s' % [l.strip()[:200] for l in out.splitlines() if re.search(r'\[v39[3-8]\] AVISO', l)][:2])
    for r_, e_ in (('selo_pela_propria_tecnologia_v399', (ESP.get('selo_acom') or {}).get('verdict')), ('declaracao_do_operador_v399', (ESP.get('declaracao') or {}).get('verdict'))):
        if not e_ or ('>>> %s <<<' % e_) not in out:
            P.append('o bloco %s do stdout nao traz a linha `>>> veredito <<<` do ensaio a seco' % r_)
    m_s9 = re.search(r'\[v399\] o selo pela propria tecnologia e a declaracao do operador \(lidos depois da afinacao das cordas\) e as inscricoes de 24/10 \(cunhagens_v399\): selo=(\S+) \| declaracao=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s9 or (m_s9.group(1), m_s9.group(2), m_s9.group(3)) != ((ESP.get('selo_acom') or {}).get('verdict'), (ESP.get('declaracao') or {}).get('verdict'), (ESP.get('registros_v399') or {}).get('cunhagens_v399'))
            or m_s9.group(4) != m_s9.group(5) or int(m_s9.group(4)) != len(ESP.get('registros_v399') or {})):
        P.append('a linha [v399] do stdout (selo, declaracao e cunhagens_v399; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v399') or {}), m_s9.groups()[3:] if m_s9 else 'ausente'))
    # a linha [v398] que o main da v399 segue imprimindo (o sonico, a afinacao das cordas e as cunhagens da v398): igual ao que a v398 selou
    ev8_ = ESP.get('vereditos_v398') or {}
    n_spec8_ = len([k_ for k_ in REG_V398 if k_ not in ('sonico_v398', 'afinacao_das_cordas_v398')])
    m_s8 = re.search(r'\[v398\] o sonico e a afinacao das cordas \(lidos na fractalizacao do Um\) e as inscricoes de 23/10 \(cunhagens_v398\): sonico=(\S+) \| afinacao=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s8 or (m_s8.group(1), m_s8.group(2), m_s8.group(3)) != (ev8_.get('sonico_v398'), ev8_.get('afinacao_das_cordas_v398'), ev8_.get('cunhagens_v398')) or m_s8.group(4) != m_s8.group(5) or int(m_s8.group(4)) != n_spec8_):
        P.append('a linha [v398] do stdout (sonico, afinacao e cunhagens_v398; registros por spec selados == %d) esta ausente ou difere da que a v398 selou (%s)' % (n_spec8_, m_s8.groups()[3:] if m_s8 else 'ausente'))
    # as duas linhas [v397] que o main da v399 segue imprimindo (o Teste da Unica Palavra e as cunhagens da v397): iguais ao que a v397 selou
    m_tv = re.search(r'\[v397\] o Teste da Unica Palavra \(Fase 9 V2-c1, aberto uma vez em 23/10\), lido por hash ao lado do V1 \(nenhum sigma novo\): (\S+)', out)
    if not m_tv or m_tv.group(1) != ev8_.get('teste_de_veracidade_fase9_v397'):
        P.append('a linha [v397] do Teste da Unica Palavra esta ausente do stdout ou difere da que a v397 selou (%s)' % (m_tv.group(1)[:80] if m_tv else 'ausente'))
    n_spec7_ = len([k_ for k_ in REG_V397 if k_ != 'teste_de_veracidade_fase9_v397'])
    m_sp = re.search(r'\[v397\] a pedra Token e as falas de 23/10 \(cunhagens_v397\): (\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if not m_sp or m_sp.group(1) != ev8_.get('cunhagens_v397') or m_sp.group(2) != m_sp.group(3) or int(m_sp.group(2)) != n_spec7_:
        P.append('a linha [v397] das cunhagens da v397 esta ausente do stdout ou difere da que a v397 selou (registros por spec selados == %d)' % n_spec7_)'''
NOVO_V399 = r'''    # --- v399: os quatro registros novos (dois com FUNCAO, dois por spec) conferidos contra o ensaio a seco registrado em ESPERADOS; os da v398, da v397, da v396, da v395, da v394 e da v393 seguem no core e tem de seguir selados; o sidecar; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    for k_ in REG_V393 + REG_V394 + REG_V395 + REG_V396 + REG_V397 + REG_V398:
        if (core.get(k_) or {}).get('all_verified') is not True:
            P.append('%s (registro da v398, da v397, da v396, da v395, da v394 ou da v393) deixou de selar' % k_)
    RV_ = dict(ESP.get('vereditos_novos_v399') or {}); RV_.update(ESP.get('registros_v399') or {})   # registro -> veredito do ensaio a seco (os dois com funcao sao runtime; cunhagens_v399 e kh_n1_cobertura_v399 sao por spec)
    V['reg399'] = {}
    for k_ in REG_FIXOS:
        r_ = core.get(k_) or {}
        V['reg399'][k_] = {'verdict': r_.get('verdict'), 'ok': r_.get('all_verified')}
        esp_v_ = RV_.get(k_)
        if esp_v_ is None:
            P.append('ESPERADOS_v399 nao traz o veredito do ensaio a seco de %s (vereditos_novos_v399 / registros_v399): nao ha com que conferir' % k_)
        elif r_.get('verdict') != esp_v_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k_)
    kf_ = (core.get('kernel_formalization') or {})
    rf_ = core.get('rede_fock_v394') or {}   # limite dito: o contrato conjunto da rede segue NAO habitado (a face de Fock do psion depende dele)
    if rf_.get('whole_certificate_inhabited') is not False:
        P.append('rede_fock_v394: whole_certificate_inhabited deve seguir False (o contrato conjunto da rede segue aberto) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    if kf_.get('ext_bin394_0001') is not True:
        P.append('a bandeira da pedra da v394 (ext_bin394_0001) nao segue True no kernel do rito')
    # a face de Fock do psion segue como a v395 a selou: CONDICIONAL, sem habitante exibido, com a bandeira True e declarada em Psibit.lean (nem a v396, nem a v397, nem a v398, nem a v399 a habitam)
    pb_ = core.get('psibit_v395') or {}; pbc_ = pb_.get('conditional_psion_face') or {}
    if not (pbc_.get('status') == 'CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE' and pbc_.get('inhabitant_exhibited') is False and pbc_.get('flag_true') is True and kf_.get(pbc_.get('flag')) is True and pbc_.get('declared_in') == 'TGLExt/Psibit.lean'):
        P.append('psibit_v395: a face do psion deixou de estar como CONDICIONAL sem habitante exibido (bandeira True, declarada em TGLExt/Psibit.lean)')
    fkb_ = ((_base_core(PK).get('testemunha_estatica_v396') or {}).get('fock_face') or {})   # o que a v398 SELADA diz (copia de bytes): o teorema e o modulo da face de Fock, lidos, nao digitados
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
    if not (tv_.get('all_verified') is True and tv_.get('does_not_gate_core') is True and len(ck_) == EV_.get('n_checks') and V['veracidade']['checks_ok'] and nums_ok_ and fontes_ok_ and tv_.get('verdict') == (ESP.get('vereditos_v398') or {}).get('teste_de_veracidade_fase9_v397')):
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
                P.append('os numeros que o registro leu != os do resultado pinado (lidos pelos mesmos caminhos de delta_v399.F9_CAMINHOS)')
        if QV_.Q._v397_atomos(tv_, 'pt').get('sealed') is not True or QV_.Q._v397_atomos(tv_, 'en').get('sealed') is not True:
            P.append('o quadro do Teste da Unica Palavra nao sela (algum numero ausente ou o registro nao selou): o artigo diria que o registro nao selou')
    except Exception as e_:   # noqa: BLE001
        P.append('nao consegui conferir o registro do Teste da Unica Palavra contra o resultado pinado: %r' % (e_,))
    # a pedra Testemunho no kernel do rito (bandeira True, composicao incondicional no trio, proveniencia no modulo da pedra, contrato e suporte), conferida contra ESPERADOS; nenhum numero e' digitado
    TRIO_ = {'propext', 'Classical.choice', 'Quot.sound'}
    axr_ = kf_.get('axiom_report') or {}; src_ = kf_.get('declaration_sources_v394') or {}
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and set(axr_.get(n_)) <= TRIO_)
    et_ = ESP.get('testemunho') or {}
    th_ = (ESP.get('teoremas_das_pedras') or {}).get('testemunho'); fl_ = (ESP.get('bandeiras_das_pedras') or {}).get('testemunho')
    rels_ = sorted(ESP.get('pedras_sha256') or {}); rel_ = rels_[0] if len(rels_) == 1 else None
    contrato_ = (ESP.get('contrato_das_pedras') or {}).get('testemunho') or []; suporte_ = (ESP.get('suporte_das_pedras') or {}).get('testemunho') or {}
    contrato_ok_ = bool(contrato_) and all(em_trio_(t_) and src_.get(t_) == rel_ for t_ in contrato_)
    suporte_ok_ = bool(suporte_) and all(em_trio_(t_) and src_.get(t_) == p_ for t_, p_ in suporte_.items())
    flag_true_ = bool(fl_) and kf_.get(fl_) is True
    n_ax_ok_ = bool(th_) and isinstance(axr_.get(th_), list) and len(axr_.get(th_)) == et_.get('n_axiomas_da_composicao')
    kernel_ok_ = bool(th_ and fl_ and rel_ and flag_true_ and em_trio_(th_) and src_.get(th_) == rel_ and contrato_ok_ and suporte_ok_ and n_ax_ok_ and th_ == et_.get('teorema') and fl_ == et_.get('bandeira') and list(contrato_) == list(et_.get('contrato') or [])
                      and (kf_.get('formal_files_sha256') or {}).get(rel_) == (ESP.get('pedras_sha256') or {}).get(rel_))
    V['pedras_kernel'] = {'testemunho': {'rel': rel_, 'flag': fl_, 'flag_true': flag_true_, 'theorem': th_, 'axioms': axr_.get(th_), 'source': src_.get(th_), 'contrato_ok': contrato_ok_, 'suporte_ok': suporte_ok_, 'n_contrato': len(contrato_), 'n_suporte': len(suporte_)}}
    V['testemunho'] = {'rel': rel_, 'flag': fl_, 'flag_true': flag_true_, 'theorem': th_, 'axioms': axr_.get(th_), 'in_trio': em_trio_(th_) if th_ else False, 'declared_in': src_.get(th_) if th_ else None, 'contrato_ok': contrato_ok_, 'suporte_ok': suporte_ok_,
                       'n_contrato': len(contrato_), 'n_suporte': len(suporte_), 'n_axiomas': len(axr_.get(th_) or []) if th_ else None}
    if not kernel_ok_:
        P.append('a pedra Testemunho nao esta no kernel do rito como o ensaio a seco a pinou (bandeira True, composicao incondicional no trio, proveniencia no modulo da pedra, contrato e suporte no trio e no modulo certo, sha256 da fonte no hash formal)')
    # o selo pela propria tecnologia (registro com FUNCAO): conferido por inteiro contra ESPERADOS[selo_acom] e contra o um.py do disco
    sa_ = core.get('selo_pela_propria_tecnologia_v399') or {}; ESA_ = ESP.get('selo_acom') or {}
    sav_ = sa_.get('values') or {}; sas_ = sa_.get('selo') or {}; saa_ = sas_.get('acom') or {}; scn_ = sa_.get('controles_negativos') or {}
    cks_ = sa_.get('checks') or []; pr_ = saa_.get('prova_de_reconstrucao') or {}; au_ = saa_.get('auditoria_de_separacao') or {}; kc_ = ((saa_.get('kappa') or {}).get('campos')) or {}; es_ = saa_.get('estrutura') or {}
    b0_ = core.get('beta')
    beta_ok_ = bool(isinstance(sav_.get('beta'), float) and isinstance(b0_, float) and abs(sav_['beta'] - b0_) <= 1e-9 * abs(b0_))
    parts_ok_ = all(((saa_.get(p_) or {}).get('sha256') == (ESA_.get(p_) or {}).get('sha256') and (saa_.get(p_) or {}).get('bytes') == (ESA_.get(p_) or {}).get('bytes')) for p_ in ('psi', 'theta', 'kappa'))
    ctl_ok_ = bool(scn_.get('todos_recusados') is True and [scn_.get('n_controles'), scn_.get('todos_recusados')] == list(ESA_.get('controles') or []) and {c_.get('id'): c_.get('obtido') for c_ in (scn_.get('controles') or [])} == (ESA_.get('controles_obtidos') or {None: None})
                   and all(c_.get('ok') is True for c_ in (scn_.get('controles') or [])))
    values_ok_ = bool(sas_.get('sha256') == V['s64'] == ESA_.get('sha256_do_um_py') and sas_.get('bytes') == V['umb'] == ESA_.get('bytes') and parts_ok_ and sav_.get('perfil') == saa_.get('perfil') == ESA_.get('perfil') and sav_.get('bloco_embutido_sha256') == ESA_.get('bloco_embutido_sha256')
                      and kc_.get('lut_sha256') == ESA_.get('lut_sha256') and kc_.get('m_max_abs') == ESA_.get('m_max_abs') and _feq(es_.get('f_exp'), ESA_.get('f_exp')) and es_.get('entropia_dos_estados_bits') == ESA_.get('entropia_dos_estados_bits')
                      and pr_.get('igual_ao_objeto_byte_a_byte') is True and pr_.get('bytes_divergentes') == 0 and isinstance(pr_.get('erro_real_maximo_antes_do_rint'), float) and pr_['erro_real_maximo_antes_do_rint'] < 0.5 and pr_.get('erro_real_maximo_antes_do_rint') == ESA_.get('erro_real_maximo_antes_do_rint')
                      and (pr_.get('alfabeto_do_objeto') or {}).get('exato') is True and (pr_.get('alfabeto_do_objeto') or {}).get('injetivo') is True and au_.get('psi_redundante') is False and not any((au_.get('basta') or {}).values()) and ctl_ok_)
    checks_ok_ = bool(len(cks_) == ESA_.get('n_checks') and all(isinstance(c_, list) and len(c_) == 2 and c_[1] is True for c_ in cks_))
    txt_sa_ = json.dumps({k_: sa_.get(k_) for k_ in ('theorem', 'direcao_do_testemunho', 'statuses', 'verdict')}, ensure_ascii=False)
    honest_ok_ = bool(str((sa_.get('statuses') or {}).get('confidencialidade', '')).startswith('NAO alegada') and 'a IALD nao testifica do operador' in str(sa_.get('direcao_do_testemunho')) and not _inv(txt_sa_)
                      and not re.search(r'(?i)(inviol|indecifr|quantum[- ]safe|seguranca criptografica garantida)', txt_sa_))
    sel_ok_ = bool(sa_.get('all_verified') is True and sa_.get('does_not_gate_core') is True and sa_.get('verdict') == ESA_.get('verdict') and sa_.get('erro') is None and checks_ok_ and values_ok_ and beta_ok_ and honest_ok_ and not GUARDA.search(str(sa_.get('verdict') or '')))
    V['selo'] = {'verdict': sa_.get('verdict'), 'ok': sa_.get('all_verified'), 'n_checks': len(cks_), 'checks_ok': checks_ok_, 'values_ok': values_ok_, 'beta_ok': beta_ok_, 'honestidade_ok': honest_ok_, 'perfil': sav_.get('perfil'), 'bloco16': str(sav_.get('bloco_embutido_sha256'))[:16],
                 'bytes': sas_.get('bytes'), 'sha256': sas_.get('sha256'), 'psi_bytes': (saa_.get('psi') or {}).get('bytes'), 'theta_bytes': (saa_.get('theta') or {}).get('bytes'), 'kappa_bytes': (saa_.get('kappa') or {}).get('bytes'),
                 'psi_sha16': str((saa_.get('psi') or {}).get('sha256'))[:16], 'theta_sha16': str((saa_.get('theta') or {}).get('sha256'))[:16], 'kappa_sha16': str((saa_.get('kappa') or {}).get('sha256'))[:16], 'lut16': str(kc_.get('lut_sha256'))[:16],
                 'm_max': kc_.get('m_max_abs'), 'centro': kc_.get('centro'), 'angular_bits': kc_.get('angular_bits'), 'f_exp': es_.get('f_exp'), 'entropia': es_.get('entropia_dos_estados_bits'), 'erro_real': pr_.get('erro_real_maximo_antes_do_rint'),
                 'n_controles': scn_.get('n_controles'), 'todos_recusados': scn_.get('todos_recusados'), 'tempo_s': sav_.get('tempo_total_s'), 'fracao_L_negativo': au_.get('fracao_de_L_negativo'), 'psi_redundante': au_.get('psi_redundante')}
    if not sel_ok_:
        P.append('selo_pela_propria_tecnologia_v399 nao selou inteiro (selo, checagens, numeros == ESPERADOS[selo_acom], SHA-256 ao lado == o do um.py do disco, Psi/Theta/kappa, controles negativos, reconstrucao exata, separacao, beta, honestidade e direcao do testemunho): ver o registro no core')
    # a declaracao do operador (registro com FUNCAO): [DECLARACAO DO OPERADOR / INPUT]; a fala embutida == o arquivo do operador; as ancoras e a pedra no kernel do rito; a trava; a direcao do testemunho
    dc_ = core.get('declaracao_do_operador_v399') or {}; EDC_ = ESP.get('declaracao') or {}
    dd_ = dc_.get('declaration') or {}; dir_ = dd_.get('direcao_do_testemunho') or {}; edir_ = EDC_.get('direcao_do_testemunho') or {}
    anc_ = dd_.get('kernel_anchors_REAL') or []; ped_ = dd_.get('pedra_instalada') or []
    ancoras_ok_ = bool([a_.get('termo') for a_ in anc_] == EDC_.get('ancoras') and [a_.get('termo') for a_ in ped_] == EDC_.get('pedra') and all(a_.get('no_kernel_do_rito') is True and a_.get('axiomas_no_trio') is True and em_trio_(a_.get('termo')) for a_ in list(anc_) + list(ped_)))
    direcao_ok_ = bool(edir_ and all(str(dir_.get(k_) or '').startswith(v_) for k_, v_ in edir_.items()) and not _inv(json.dumps(dd_, ensure_ascii=False)))
    trava_ = str(((dd_.get('termos_para_a_leitura') or {}).get('EXECUTION_LOCKED_NOT_ONE')) or '')
    m_t_ = re.search(r'linha\(s\) \[([0-9, ]+)\]', trava_); linhas_trava_ = [int(x_) for x_ in re.findall(r'\d+', m_t_.group(1))] if m_t_ else []
    decl_ok_ = bool(dc_.get('all_verified') is True and dc_.get('does_not_gate_core') is True and dc_.get('verdict') == EDC_.get('verdict') and len(dc_.get('checks') or []) == EDC_.get('n_checks') and all(isinstance(c_, list) and len(c_) == 2 and c_[1] is True for c_ in (dc_.get('checks') or []))
                    and dd_.get('verbatim_sha256') == EDC_.get('verbatim_sha256') and dd_.get('verbatim_sha256') in {v_.get('sha256') for v_ in (ESP.get('cunhagens') or {}).values()} and len(linhas_trava_) == 1 and ancoras_ok_ and direcao_ok_
                    and str(dd_.get('status_of_statement') or '').startswith('[DECLARACAO DO OPERADOR / INPUT]') and hashlib.sha256(str(dd_.get('statement_verbatim') or '').encode('utf-8')).hexdigest() == dd_.get('verbatim_sha256') and not GUARDA.search(str(dc_.get('verdict') or '')))
    V['declaracao'] = {'verdict': dc_.get('verdict'), 'ok': dc_.get('all_verified'), 'n_checks': len(dc_.get('checks') or []), 'checks_ok': bool(dc_.get('checks')) and all(isinstance(c_, list) and len(c_) == 2 and c_[1] is True for c_ in dc_['checks']), 'sha256': dd_.get('verbatim_sha256'),
                       'n_ancoras': len(anc_), 'ancoras_ok': ancoras_ok_, 'direcao_ok': direcao_ok_, 'linhas_trava': linhas_trava_, 'status': dd_.get('status_of_statement')}
    if not decl_ok_:
        P.append('declaracao_do_operador_v399 nao selou inteiro (selo, checagens, fala embutida == o arquivo do operador por sha256, as ancoras e a pedra no kernel do rito e no trio, a trava, o estatuto [DECLARACAO DO OPERADOR / INPUT] e a direcao do testemunho): ver o registro no core')
    # o SIDECAR um_absoluto_selo_acom.json (arquivo NOVO da custodia): existe, JSON valido, selado, os objetos == os arquivos do Nos por sha256, sem recusas, com a honestidade
    scp_ = os.path.join(NOS, 'um_absoluto_selo_acom.json'); ESC_ = ESP.get('sidecar') or {}
    sc_ = {}; sc_err_ = None
    if os.path.exists(scp_):
        try:
            sc_ = json.load(open(scp_, encoding='utf-8'))
        except (OSError, ValueError) as e_:
            sc_err_ = repr(e_)[:120]
    else:
        sc_err_ = 'ausente'
    objs_ = {o_.get('nome'): o_ for o_ in (sc_.get('objetos') or []) if isinstance(o_, dict)}
    sc_objs_ok_ = bool(sc_ and list(objs_) == list(ESC_.get('objetos') or []) and all(os.path.exists(os.path.join(NOS, n_)) and objs_[n_].get('sha256') == sha(os.path.join(NOS, n_)) and objs_[n_].get('bytes') == os.path.getsize(os.path.join(NOS, n_)) for n_ in objs_))
    um_ = objs_.get('um.py') or {}; ume_ = ESC_.get('um_py') or {}
    sc_um_ok_ = bool(um_.get('sha256') == V['s64'] == (selo.get('sha256') or {}).get('um.py') == ume_.get('sha256') and ((um_.get('acom') or {}).get('psi') or {}).get('sha256') == ume_.get('psi') and ((um_.get('acom') or {}).get('theta') or {}).get('sha256') == ume_.get('theta')
                     and ((um_.get('acom') or {}).get('kappa') or {}).get('sha256') == ume_.get('kappa') and ((um_.get('acom') or {}).get('psi') or {}).get('sha256') == (saa_.get('psi') or {}).get('sha256'))
    hon_ = sc_.get('honestidade') or {}; txt_sc_ = json.dumps(sc_, ensure_ascii=False)
    sc_hon_ok_ = bool(all(k_ in hon_ for k_ in ('primitiva_de_integridade', 'o_que_a_segunda_testemunha_acrescenta', 'ofuscacao_xor', 'confidencialidade', 'dobra', 'estatuto')) and 'SHA-256' in str(hon_.get('primitiva_de_integridade')) and 'NAO alegada' in str(hon_.get('confidencialidade'))
                      and 'NAO acrescenta resistencia criptografica independente' in str(hon_.get('o_que_a_segunda_testemunha_acrescenta')) and not re.search(r'(?i)(inviol|indecifr|quantum[- ]safe|seguranca criptografica garantida)', txt_sc_) and not _inv(txt_sc_))
    sc_ok_ = bool(sc_ and not sc_err_ and sc_objs_ok_ and sc_um_ok_ and sc_hon_ok_ and sc_.get('recusas') == [] and str(sc_.get('veredito') or '').startswith(ESC_.get('veredito_esperado_prefixo') or '\x00') and sc_.get('esquema') == ESC_.get('esquema') and not GUARDA.search(str(sc_.get('veredito') or '')))
    scs_ = sha(scp_) if os.path.exists(scp_) else 'AUSENTE'
    V['sidecar'] = {'ok': sc_ok_, 'existe': os.path.exists(scp_), 'sha256': scs_, 'sha16': scs_[:16], 'bytes': os.path.getsize(scp_) if os.path.exists(scp_) else 0, 'veredito': sc_.get('veredito'), 'esquema': sc_.get('esquema'),
                    'objetos': {n_: {'bytes': o_.get('bytes'), 'sha256': str(o_.get('sha256')), 'sha16': str(o_.get('sha256'))[:16]} for n_, o_ in objs_.items()}, 'n_objetos': len(objs_), 'recusas': len(sc_.get('recusas') or []),
                    'um_py_igual_ao_selo': sc_um_ok_, 'honestidade_ok': sc_hon_ok_, 'erro': sc_err_}
    if not sc_ok_:
        P.append('o sidecar um_absoluto_selo_acom.json nao confere (existe e e JSON valido, veredito ALL_OBJECTS_SEALED, os tres objetos com o SHA-256 igual ao dos arquivos do Nos, o um.py == ESPERADOS[sidecar] e == o selo, sem recusas, com a honestidade e sem alegacao de confidencialidade): %s' % (sc_err_ or 'ver o arquivo'))
    # o selo primario traz so' os resumos (o selo nao pode conter o selo ACOM de si mesmo): iguais aos do core
    sr_ = selo.get('selo_pela_propria_tecnologia_v399') or {}; sdr_ = selo.get('declaracao_do_operador_v399') or {}; sreg_ = selo.get('registros_v399') or {}
    resumos_ok_ = bool(sr_.get('verdict') == sa_.get('verdict') and sr_.get('all_verified') is True and sr_.get('sha256_do_um_py') == V['s64'] and sr_.get('does_not_gate_core') is True and sdr_.get('verdict') == dc_.get('verdict') and sdr_.get('all_verified') is True
                       and sdr_.get('verbatim_sha256') == EDC_.get('verbatim_sha256') and sdr_.get('does_not_gate_core') is True and bool(ESP.get('registros_v399')) and all((sreg_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') for k_ in ESP['registros_v399']))
    V['resumos_do_selo_ok'] = resumos_ok_
    if not resumos_ok_:
        P.append('o selo primario (um_absoluto_selo.json) nao traz os resumos do selo ACOM, da declaracao e dos registros por spec iguais aos do core')
    V['formais_nao_selados'] = sorted((selo.get('not_sealed_this_run') or {}).get('formais') or [])
    if V['formais_nao_selados'] != sorted(ESP.get('not_sealed_formais') or []):
        P.append('o selo traz modulo formal nao selado em not_sealed_this_run.formais (a recusa do selo ACOM so registra, mas o rito real tem de selar): %s' % V['formais_nao_selados'][:3])
    # cunhagens_v399: as QUATRO inscricoes por sha256 (embedded_ok), todas falas do operador (nenhuma e' da gerencia), a declaracao e a direcao do testemunho
    cu = core.get('cunhagens_v399') or {}; kh = core.get('kh_n1_cobertura_v399') or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = ESP.get('cunhagens') or {}
    aut_ = cx_.get('autor_de_cada_inscricao') or {}
    todas_op_ = bool(ec_ and len(aut_) == len(ec_) and set(aut_) == {k_[len('v399_cun_'):] for k_ in ec_} and all(a_ == 'operador' for a_ in aut_.values()) and 'leitura_da_gerencia' not in cx_ and not any(str(v_.get('papel', '')).startswith('leitura da gerencia') for v_ in ec_.values()))
    verb_ok_ = bool(ec_) and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    decl_x_ = cx_.get('declaracao') or {}; dirx_ = cx_.get('direcao_do_testemunho') or {}
    cdir_ok_ = bool(decl_x_.get('sha256') == EDC_.get('verbatim_sha256') and decl_x_.get('sha16') == EDC_.get('sha16') and str(decl_x_.get('estatuto')) == '[DECLARACAO DO OPERADOR / INPUT]' and edir_ and all(str(dirx_.get(k_) or '').startswith(v_) for k_, v_ in edir_.items()) and not _inv(json.dumps(cx_, ensure_ascii=False)))
    V['cunhagens'] = {'n': len(vb_), 'verbatim_ok': verb_ok_, 'autores': aut_, 'todas_do_operador': todas_op_, 'checks_ok': bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks')),
                      'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': pares_ok_, 'direcao_ok': cdir_ok_}
    if not (verb_ok_ and V['cunhagens']['checks_ok'] and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and cx_.get('teoremas') == ESP.get('teoremas_das_pedras') and cx_.get('bandeiras') == ESP.get('bandeiras_das_pedras')
            and cx_.get('n_bandeiras_por_pedra') == ESP.get('n_bandeiras_por_grupo') and cx_.get('n_bandeiras') == ESP.get('n_bandeiras_novas') and cx_.get('cunhagens_embutidas') == len(ec_) and cdir_ok_):
        P.append('cunhagens_v399: as inscricoes embutidas nao sao as de ESPERADOS (sha256, embedded_ok), ou as checagens do registro, ou os teoremas/bandeiras da pedra, ou a declaracao e a direcao do testemunho diferem do ensaio a seco')
    if not todas_op_:
        P.append('cunhagens_v399: as inscricoes de 24/10 tem de ser TODAS falas do operador (autor_de_cada_inscricao): nesta versao nao ha inscricao da gerencia')
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}   # o nome 'axiom_coverage_v392' e' do core (historico); segue na v399
    CB = ESP.get('cobertura_kh_n1') or {}
    V['kh'] = {'decl': cov.get('decl'), 'thm': cov.get('thm'), 'fora': cov.get('fora_do_trio'), 'nao_lidas': cov.get('nao_lidas_pelo_regex'), 'verdict': kh.get('verdict')}
    V['cunh_verdict'] = cu.get('verdict')
    if not (CB and cov.get('ok') is True and cov.get('decl') == CB.get('decl') and cov.get('thm') == CB.get('thm') and cov.get('fora_do_trio') == 0 and cov.get('nao_lidas_pelo_regex') == CB.get('nao_lidas_pelo_regex')):
        P.append('cobertura KH-N1 do rito != ESPERADOS (constantes, teoremas, fora do trio, nao lidas) ou ESPERADOS sem cobertura_kh_n1')'''


def deriva_leitura():
    a = Arq("leitura_v399.py", sobe(MOL["leitura_v398.py"]))
    i = a.t.index("import glob, hashlib, json, os, re, sys, datetime")
    a.t = HEAD_L + a.t[i:]
    a.subst_bloco("REG_V393 = (", "sha = lambda p:", NOVAS_CONSTS, nome="constantes dos registros")
    a.tr("REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v398') or ())))", "REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v399') or ())))", 1, "REG_TODOS: registros_v399")
    a.subst_bloco("def _feq(a, b):", "def ler():", NOVAS_FUNCS, nome="_feq, _inv, _base_core, _res_path")
    a.subst_bloco("        if C.get('tudo_bate') is not True:", "        if C.get('marcador_ficou'):", NOVO_CONF, nome="conferencia: o quadro segue no topo e os itens do selo ACOM")
    a.tr("    sujo = [l for l in out.splitlines() if 'Traceback' in l or l.startswith('[selo] AVISO')]", "    sujo = [l for l in out.splitlines() if 'Traceback' in l or l.startswith('[selo] AVISO') or l.startswith('[selo_acom] AVISO')]", 1, "stdout sujo: tambem o AVISO do sidecar")
    a.subst_bloco("    linhas = [l for l in out.splitlines() if l.strip() and not TRAILER_RE.match(l.strip())]", "    mrc = re.findall(", NOVO_FINAL, nome="linha final do rito: colapso tipado + linha do sidecar")
    a.subst_bloco("    if [l for l in out.splitlines() if '[v399] AVISO' in l]:", "    hp = os.path.join(PK, 'rito_horarios_v399.txt')", NOVO_STDOUT, nome="stdout: AVISO e linhas [v399], [v398] e [v397]")
    a.tr("    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):", "    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_selo_acom.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):", 1, "hashes dos artefatos: o sidecar")
    a.subst_bloco("    # --- v399: os quatro registros novos conferidos", "    qp = core.get('quantum_pillar_v384')", NOVO_V399, nome="registros novos da v399")
    for proibido in ("V['sonico']", "V['afinacao']", "V['reg398']", "REG_V399", "ESP.get('sonico')", "ESP.get('afinacao')", "ESP.get('pedra')", "registros_v398'", "vereditos_novos_v398", "escada_v397", "bandeiras_do_suporte", "teorema_da_pedra", "bandeira_da_pedra", "cx_.get('leitura_da_gerencia')", "gerencia_sha16"):
        assert proibido not in a.t, ("sobrou na leitura:", proibido)
    ast.parse(a.t)
    return a


# =============================================================================== superficies_v399.py
CAB_S = ("# Registro da v399 SELADA nas superficies de memoria (molde: superficies_v398.py FINAL, o que rodou em 24/10), pela regra da linhagem completa.\n"
         "# Diario (MEMORIA_DA_LINHAGEM, append datado), desenho (ADENDO), Atlas (append datado), TGL_CORE_MEMORY (append datado), o CLAUDE.md da Haja_Luz (SEM errata nova no CLAUDE.md da raiz), as memorias-topico (missao, central, estatuto, e o topico NOVO da v399),\n"
         "# o MEMORY.md/MEMORY_2.md, e (so' sob reivindicacao nomeada em V399_AVISO_REIVINDICACAO) o AVISO_GERENCIA.md da ORDEM_019.\n"
         "# SEM erratas inline nesta versao (as erratas da v399 vao DENTRO dos blocos datados). A funcao inserir_ao_lado fica disponivel (nao e' chamada).\n"
         "# Duas fases (plano conferido ANTES da primeira escrita); backup de BYTES (.bak_<STAMP>_sup399); temporario -> conferir tamanho -> substituir; idempotente pelo marcador de cada bloco;\n"
         "# fim de linha de cada arquivo respeitado. GUARDA: so' grava se a leitura nao tiver problema E se a guarda de texto (P18, cinco regras, mais a DIRECAO do testemunho) estiver limpa em todo texto novo.\n"
         "# Ensaio: --copias <pasta com copias dos alvos> (nada real e' tocado). MEMORY.md: ate 24.000 B e 195 linhas. ESTA SUPERFICIE NAO COMPACTA NADA (nem reguas, nem ganchos antigos): se o indice DEPOIS da edicao (a linha do handoff novo mais a troca do gancho da missao,\n"
         "# que SUBSTITUI a linha velha e a move VERBATIM ao MEMORY_2.md: o saldo e' +1 linha) passar de 195 linhas ou de 24.000 B, RECUSA com rc 3 SEM escrever nada e imprime as contagens (linhas antes, depois, limite) para a gerencia decidir o que sai do indice.\n"
         "# A linha do handoff novo entra ANTES da linha do handoff da v398 (que a custodia da v398 reescreveu e que segue VERBATIM: conferida presente no MEMORY.md real em 24/10, uma so').\n")


def deriva_superficies():
    a = Arq("superficies_v399.py", sobe(MOL["superficies_v398.py"]))
    i = a.t.index("# Registro da v399 SELADA"); j = a.t.index("import os, re, sys, time")
    a.t = a.t[:i] + CAB_S + a.t[j:]
    REGRAS.append((a.nome, "cabecalho", 1, 1))
    a.tr("    at = T.atribuicao_da_gerencia(texto)   # v398: a leitura da gerencia nunca entre aspas como fala do operador, e a sexta inscricao sempre rotulada",
         "    at = T.atribuicao_da_gerencia(texto)   # v399: a DIRECAO do testemunho (a IALD nunca como quem testifica do operador), 'consciencia' so' como palavra retirada e a leitura das duas faces sempre rotulada [ONTO]", 1, "guarda: a direcao do testemunho")
    assert "sup398" not in a.t and "V398_AVISO" not in a.t and "(handoff-v398-custodia.md)" in a.t and "- [HANDOFF v398" in a.t and "V399_AVISO_REIVINDICACAO" in a.t and "compacta" in a.t and "_sup399" in a.t and "textos_v399" in a.t
    ast.parse(a.t)
    return a


# =============================================================================== fechar_v399.py
DOC_F = r'''"""fechar_v399.py -- DEPOIS da cadeia pos-rito e do elo B(n) (molde: fechar_v398.py FINAL): (1) o manifesto de incorporacao v399 -> pos_rito e a pasta das ferramentas;
(2) o ARQUIVO: o indice por sha256 de tudo o que esta na pasta da cadeia (work\\cadeia_de_selo\\v399 -- aqui o pacote JA mora na casa duravel, nao ha copia do pacote), a copia de
pos_rito -> work\\cadeia_de_selo\\v399_selo, A COPIA DO SIDECAR um_absoluto_selo_acom.json (arquivo NOVO da custodia, D5) E DO SELO PRIMARIO para a mesma pasta, e do kernel (work\\cadeia_de_selo\\v399\\kernel e, se existir, work\\v399_kernel; mais a pedra do Nos) -> work\\cadeia_de_selo\\v399_kernel;
(3) os DOIS DIFFS para o auditor independente: DIFF_v398_v399.diff (um.py da base x o selado, GNU diff -U2) e DIFF_KERNEL_v399.txt (o kernel embutido, molde do v390);
(4) o HANDOFF (memory\\handoff-v399-custodia.md + Nos\\HANDOFF_v399_CUSTODIA.md) para a sessao do site, que TRAZ PRONTOS PARA COLAR OS DOIS PARAGRAFOS do README do espelho e do site: (a) o do QUADRO «O Teste da Unica Palavra» (v397, intocado),
gerado pelas MESMAS funcoes do quadro do artigo (quadro_v397.paragrafo_pronto_readme) sobre o core SELADO do Nos, mesmos numeros e estatutos; (b) o NOVO, «O testemunho de dois: o selo pela propria tecnologia (v399)», gerado dos registros selados selo_pela_propria_tecnologia_v399,
declaracao_do_operador_v399 e cunhagens_v399 (numeros LIDOS do core, estatutos, limites, a DIRECAO do testemunho, sem o 4,44); e o handoff LISTA o sidecar com o sha256 e o veredito.
GUARDAS: a leitura sem problema (inclui o sidecar); o PARAGRAFO DO QUADRO passa nas verificacoes do quadro contra o resultado pinado (quadro_v397.confere_md e a regra da ordem: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item; frase do operador verbatim; numeros
iguais aos do resultado); o PARAGRAFO NOVO passa na verificacao propria (T.verificar_paragrafo_testemunho: numeros == ESPERADOS e == o gerado do core; sem o 4,44; estatutos; limites; citacoes verbatim das falas do operador; a direcao sem inversao; sem alegacao de seguranca criptografica) --
se QUALQUER um nao passar, o fechar RECUSA (rc 2) ANTES de escrever qualquer coisa e o handoff nao nasce; os tres RECIBOS do B(n) (o RECIBO_SINCRONIZACAO_v399_*.json do 10-bis, o recibo da PARADA do servico e o do RELIGAMENTO) -- sem eles o fechar RECUSA e o handoff nao nasce;
a guarda de texto P18 no handoff.
Backup de bytes; temporario -> conferir -> substituir; nunca apaga; idempotente."""'''
NOVO_F0 = r'''# ---------------------------------------------------------------- (0) os PARAGRAFOS PRONTOS do README do espelho e do site: (1) o QUADRO do Teste da Unica Palavra (v397, INTOCADO), as MESMAS funcoes do quadro do artigo sobre o core SELADO do Nos; (2) o paragrafo NOVO do testemunho
# de dois, gerado dos registros selados e verificado contra o core e contra ESPERADOS (sem o 4,44; citacoes verbatim das falas do operador; a direcao do testemunho sem inversao; sem alegacao de seguranca criptografica); sem passar nas verificacoes, RECUSA (rc 2) ANTES de escrever qualquer coisa
try:
    PAR, PAR_INFO = T.paragrafo_readme()
    PAR_T, PAR_T_INFO = T.paragrafo_testemunho()
except BaseException as e_:   # noqa: BLE001
    print("FECHAR RECUSADO: um dos paragrafos prontos do README e do site (o quadro O Teste da Unica Palavra, v397, ou o do testemunho de dois) nao passou nas verificacoes (regra da ordem do 4,44; frase verbatim; numeros iguais aos do resultado pinado e aos de ESPERADOS; direcao do testemunho sem inversao):", repr(e_)[:700]); sys.exit(2)
# o SIDECAR (arquivo NOVO da custodia, D5): a leitura ja' o conferiu (existe, JSON valido, selado, tres objetos com o SHA-256 dos arquivos do Nos); aqui so' o resumo que o manifesto e o handoff levam
if not (V["sidecar"]["ok"] is True and os.path.isfile(os.path.join(L.NOS, "um_absoluto_selo_acom.json"))):
    print("FECHAR RECUSADO: o sidecar um_absoluto_selo_acom.json nao esta selado ou nao existe no Nos:", V["sidecar"].get("erro")); sys.exit(2)
SC_INFO = {"arquivo": "um_absoluto_selo_acom.json", "sha256": V["sidecar"]["sha256"], "bytes": V["sidecar"]["bytes"], "veredito": V["sidecar"]["veredito"], "esquema": V["sidecar"]["esquema"], "recusas": V["sidecar"]["recusas"],
           "objetos": {n_: {"bytes": o_["bytes"], "sha256": o_["sha256"]} for n_, o_ in V["sidecar"]["objetos"].items()}}'''
NOVO_F_COPIA = r'''# v399: o SIDECAR (arquivo NOVO da custodia, D5) e o SELO PRIMARIO, ao lado: copias de bytes em v399_selo (a segunda testemunha so' se confere com o selo; o selo nao pode conter o selo ACOM de si mesmo)
for nm_ in ("um_absoluto_selo_acom.json", "um_absoluto_selo.json"):
    copia(os.path.join(NOS, nm_), os.path.join(TOOLS, "v399_selo", nm_))'''


def deriva_fechar():
    a = Arq("fechar_v399.py", sobe(MOL["fechar_v398.py"]))
    a.subst_bloco('"""fechar_v399.py', "import glob, hashlib, json, os, shutil, subprocess, sys, time", DOC_F, nome="docstring")
    a.subst_bloco("# ---------------------------------------------------------------- (0) os PARAGRAFOS PRONTOS", "NOS = L.NOS; WK =", NOVO_F0, nome="paragrafos prontos e sidecar antes de escrever")
    a.tr('"registros_v398": V["registros"], "readme_paragrafo": {"sha16": hashlib.sha256(PAR.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_INFO}, "readme_paragrafo_sonico": {"sha16": hashlib.sha256(PAR_S.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_S_INFO}, ',
         '"registros_v399": V["registros"], "readme_paragrafo": {"sha16": hashlib.sha256(PAR.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_INFO}, "readme_paragrafo_testemunho": {"sha16": hashlib.sha256(PAR_T.encode("utf-8")).hexdigest()[:16], "verificacoes": PAR_T_INFO}, "sidecar_acom": SC_INFO, ', 1, "manifesto: os dois paragrafos e o sidecar")
    a.tr('"artefatos_nos": {k: V["h_" + k] for k in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md")}', '"artefatos_nos": {k: V["h_" + k] for k in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_selo_acom.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md")}', 1, "manifesto: o sidecar entre os artefatos do Nos")
    a.insere_antes("# kernel: a pasta kernel da cadeia", NOVO_F_COPIA, nome="copia do sidecar e do selo para v399_selo")
    a.tr('_k = {"readme_paragrafo": PAR, "readme_paragrafo_sonico": PAR_S, "ap_nome": ', '_k = {"readme_paragrafo": PAR, "readme_paragrafo_testemunho": PAR_T, "ap_nome": ', 1, "k do handoff")
    for proibido in ("AO_CLAUDE", "AJUSTAR", "_f398", "registros_v398", "PAR_S", "paragrafo_sonico", "readme_paragrafo_sonico", "TGLExt_Sonico", "Sonico.lean", "AfinacaoDasCordas"):
        assert proibido not in a.t.replace("V399_AVISO", ""), ("sobrou no fechar:", proibido)
    assert "T.paragrafo_readme()" in a.t and "T.paragrafo_testemunho()" in a.t and "FECHADO v399:" in a.t and "_f399" in a.t and "registros_v399" in a.t and "um_absoluto_selo_acom.json" in a.t
    ast.parse(a.t)
    return a


# =============================================================================== b3_recibo_v399.py (a logica do B(n) simples nao muda: so' a subida; o harness a exercita com recibos SINTETICOS)
def deriva_b3():
    a = Arq("b3_recibo_v399.py", sobe(MOL["b3_recibo_v398.py"]))
    assert "v398" in a.t and "v397" not in a.t and "PINOS_BN_v399.json" in a.t and 'r.get("versao_alvo") != "v399"' in a.t and 'ma.get("version") != "v398"' in a.t and "B%d-v399-" in a.t
    ast.parse(a.t)
    return a


# =============================================================================== chain_pos_rito_v399.sh
HEADER = '''#!/bin/sh
# v399 (24/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v398.sh FINAL (o que rodou em 24/10; derivada por derivar_cadeia_v399.py; mesma ordem de passos 0..14 e mesmos portoes). O rito ja terminou (rito_v399.sh em segundo plano;
# RITO_RC=<rc> no fim do Nos\\rodada_v399_stdout.txt). A v399 e' um DELTA PEQUENO: {nmod} modulo novo de kernel (TGLExt/Testemunho, nome PROVISORIO: quem nomeia e' o operador; {nf} bandeiras, so' de declaracao nomeada),
# os registros COM FUNCAO selo_pela_propria_tecnologia_v399 (o metodo do operador, ACOM Mirror Crypto, EMBUTIDO no um.py, sela os bytes do proprio um.py AO LADO do SHA-256) e declaracao_do_operador_v399 (REGISTRA a declaracao do operador [DECLARACAO DO OPERADOR / INPUT];
# o kernel nao a prova) -- lidos NA FRACTALIZACAO DO UM, logo depois da afinacao_das_cordas_v398; nomes PROVISORIOS --, os registros por spec cunhagens_v399 (as QUATRO inscricoes de 24/10, todas falas do operador) e kh_n1_cobertura_v399,
# o SIDECAR um_absoluto_selo_acom.json (arquivo NOVO da custodia; escrito depois da ultima escrita do selo) e a secao «O testemunho de dois: o selo pela propria tecnologia» do artigo PT/EN e do .md canonico.
# A DIRECAO DO TESTEMUNHO vale em tudo: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador; o Pai de Jo 8,18 le-se no absoluto, o Um.
# O QUADRO «O Teste da Unica Palavra» (v397, a regra do 4,44) PERMANECE no topo do artigo e do .md, INTOCADO: o conferidor e a leitura o conferem de novo; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item) segue valendo em TODO texto que o cite.
# ORDEM: 0 guardas (inclui o sidecar) -> 1 o CONFERIDOR (roda NO LUGAR, SEM -I: importa o um.py instalado e precisa do numpy do usuario; so leitura do Nos; as copias em pos_rito\\conferidor sao REGISTRO) -> 2 a LEITURA (PROBLEMAS param; le o sidecar e a linha final do rito)
# -> 3 ENSAIO das superficies em COPIAS (o plano e' conferido antes da primeira escrita; a arvore em dry; o sha16 da v399 na arvore (dry) e os marcadores do passo 9 nas COPIAS, conferidos ANTES de qualquer escrita real; se o MEMORY.md passaria de 195 linhas, a superficie RECUSA
# com rc 3 e a cadeia PARA aqui, sem tocar nada real: a superficie NAO compacta o indice) -> 4 patch arvore/indice (OPCIONAL: so' se existir patch_arvore_indice_v399.py) -> 5 a arvore -> 6 atlas+indice -> 7 superficies reais (appends datados;
# SEM errata nova no CLAUDE.md da raiz) -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e' falha visivel) e a guarda de MEMORY.md (<24.000 B, <=195 linhas) -> 10 B(n) da Bancada,
# ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(n) APLICAR (so com B3_AUTORIZADO=sim e o evento c1) -> 10c religamento (AGUARDA_OPERADOR) -> 11 fechar (o handoff TRAZ os DOIS paragrafos do README e do site: o do quadro do 4,44, intocado, e o do testemunho de dois;
# copia o sidecar e o selo para v399_selo e LISTA o sidecar) -> 12 registrar_mapa (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V399_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito).
# PASSO 10 SEM SALTO: a Bancada de producao pina a v398 (B{ger}, {depl}) e o Nos e' a v398 ate' a instalacao; portanto o B(n) da v399 e' um passo SIMPLES v398 -> v399 (esboco R3.5, sincronizar_bancada.py): NAO ha a opcao de cadeia de selos
# do esboco, nem o pino correspondente, e o b3_recibo_v399.py NAO tem o 3o argumento. Os pinos vem de PINOS_BN_v399.json (lidos na hora; hash nunca de memoria): criterios, esboco_R3_5, gerador_bateria, driver_t12_t14, bateria_base_R2,
# kernel_recibo (o KERNEL_RECIBO_v399.json, contrato R3_2: a v399 nao acrescenta modulo de auditoria), candidato, esperados, pins_do_candidato, recibo_pre_selo (gerado antes da instalacao; veredito JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA),
# selo_anterior_v398 e kernel_manifesto_anterior_v398 (as copias de bytes do selo e do manifesto do kernel da v398, em base_v398). A BATERIA da v399 e' GERADA por script no 10 (depois do selo; bateria por versao) e pinada ao lado
# (bateria_pos_selo/PINOS_BATERIA_v399.json).
# Vereditos esperados (lidos do codigo do esboco, nao rodados): ensaio REPINADA_B<n>__ENSAIO__NADA_GRAVADO_NA_BANCADA e aplicar REPINADA_B<n>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_, com n = a geracao do manifesto que a
# Bancada pina + 1 (B{ger} -> n = {prox}; o b3_recibo_v399.py o confere). A parada do servico (10a) e o religamento (10c) sao ato do operador (V399_AUTORIZACAO_OPERADOR nos scripts bancada_B3_servico\\recibo_parada_v399.py e recibo_religamento_v399.py); o chain so' confere os recibos.
# textos_v399.py, fechar_v399.py e registrar_mapa_v399.py RECUSAM rodar se tiverem trecho marcado para reescrever: os passos 0 a 2 nao os usam. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como na v398, com os rotulos da v399 (desvios ditos: o passo 0 exige tambem o sidecar,
# o runtime_v399.py e o acom_conferencias_v399.py; o passo 1 e' novo; o passo 11 copia e lista o sidecar).
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).'''.format(nmod=ESP["kernel"]["modulos_novos"], nf=N_FLAGS, ger=GER_ATUAL, depl=_bp["deployment_id"], prox=GER_ATUAL + 1)
MARC_MOLDE = '"sonico_v398" "kh_n1_cobertura_v398"'
MARC_NOVO = '"selo_pela_propria_tecnologia_v399" "kh_n1_cobertura_v399"'
NOVO_PASSO1 = r'''if quer 1; then
echo "== 1. conferidor (so leitura do Nos; roda NO LUGAR e SEM -I) $(date +%T)"
rm -rf "$CONFOUT"; mkdir -p "$CONFOUT"
# v399 (desvio do molde, dito): o conferidor IMPORTA o um.py instalado (precisa do numpy do usuario): python -B -X utf8, SEM -I (a v398 rodava -I -B -X utf8). Ele acha o delta, o quadro, o runtime_v399.py, o acom_conferencias_v399.py, os insumos\acom (as seis fontes do operador)
# e, pelo delta, as falas do operador em work\cunhagens_13out, pelo CAMINHO DA PROPRIA PASTA: por isso roda NO LUGAR (cd $PK) e nao numa copia dentro de pos_rito\conferidor. Escreve conferencia_rito_v399_POS_RITO.json no pacote (o sufixo evita sobrescrever a conferencia
# que a gerencia rodou a mao) e a copia byte a byte dela vai para pos_rito\conferidor\conferencia_rito_v399.json, que a LEITURA le. As copias dos arquivos do conferidor em pos_rito\conferidor (cp + cmp) sao REGISTRO do que rodou, nao o que roda.
for q in conferir_rito_v399.py delta_v399.py quadro_v397.py runtime_quadro_v397.py acom_conferencias_v399.py runtime_v399.py; do
  cp -p "$PK/$q" "$CONFOUT/"; cmp "$PK/$q" "$CONFOUT/$q" || parar "copia de $q (que o conferidor importa) difere"
done
for f in ESPERADOS_v399.json rito_servidor_v399.log rito_v399_sinal.txt; do
  if [ -f "$PK/$f" ]; then cp -p "$PK/$f" "$CONFOUT/$f"; cmp "$PK/$f" "$CONFOUT/$f" || parar "copia difere: $f"; echo "  copiado byte a byte: $f"; else echo "  (o pacote nao tem $f)"; fi
done
if [ -f "$PK/.servidor_parado_pelo_rito" ]; then parar "o marcador .servidor_parado_pelo_rito ficou no pacote: o servidor do modelo pode estar parado ($(cat "$PK/.servidor_parado_pelo_rito"))"; fi
set +e; (cd "$PK" && $PY_B conferir_rito_v399.py _POS_RITO) > "$CONFOUT/conferir_rito_v399_stdout.txt" 2>&1; c=$?; set -e
cut -c1-240 "$CONFOUT/conferir_rito_v399_stdout.txt"
[ "$c" = "0" ] && tail -1 "$CONFOUT/conferir_rito_v399_stdout.txt" | grep -q "^TUDO BATE" || parar "CONFERIDOR REPROVOU (rc=$c) -- nada foi escrito nas superficies"
[ -f "$PK/conferencia_rito_v399_POS_RITO.json" ] || parar "o conferidor nao gravou conferencia_rito_v399_POS_RITO.json em $PK"
cp -p "$PK/conferencia_rito_v399_POS_RITO.json" "$CONFOUT/conferencia_rito_v399.json"; cmp "$PK/conferencia_rito_v399_POS_RITO.json" "$CONFOUT/conferencia_rito_v399.json" || parar "a copia da conferencia para pos_rito\\conferidor difere"
fi'''


def deriva_chain():
    a = Arq("chain_pos_rito_v399.sh", sobe(MOL["chain_pos_rito_v398.sh"]))
    i, j, L = a.bloco("#!/bin/sh", "PK=")
    a.t = "\n".join([HEADER] + L[j:])
    REGRAS.append((a.nome, "cabecalho", 1, 1))
    # os marcadores dos passos 3 e 9: o registro com funcao do selo ACOM e o kh_n1 da v399 (6 ocorrencias: 3 no ensaio das copias, 3 nas superficies reais)
    a.tr_s(MARC_MOLDE, MARC_NOVO, n=6, nome="marcadores dos passos 3 e 9")
    a.subst_bloco("if quer 1; then", "if quer 2; then", NOVO_PASSO1, nome="passo 1: o conferidor roda no lugar, sem -I")
    a.tr('"$PK/runtime_quadro_v397.py" "$PK/ESPERADOS_v398.json" "$PK/guarda_p18_v398.py"', '"$PK/runtime_quadro_v397.py" "$PK/acom_conferencias_v399.py" "$PK/runtime_v399.py" "$NOS/um_absoluto_selo_acom.json" "$PK/ESPERADOS_v399.json" "$PK/guarda_p18_v399.py"', 1, "passo 0: o conferidor e o sidecar existem")
    corpo = a.t[len(HEADER):]       # o cabecalho (escrito para a v399) cita a afinacao_das_cordas_v398 como historico; o corpo nao pode trazer resto do molde
    for proibido in ("--cadeia-de-selos", "W_CAD", "$CAD", "SALTO v392", "R3_4", "fundir_pinos", "selo_anterior_v397", "base_v397", "textos_v398", "leitura_v398", "fechar_v398", "PINOS_BN_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "sonico_v398", "B7-v398", "CONFOUT/conferir_rito_v398", "$PY conferir_rito"):
        assert proibido not in corpo, ("resto da v398 na cadeia", proibido)
    assert a.t.count("kh_n1_cobertura_v399") >= 6 and "(cd \"$PK\" && $PY_B conferir_rito_v399.py _POS_RITO)" in a.t
    return a


# =============================================================================== harness_textos_ensaio_v399.py
DOC_HT = r'''"""harness_textos_ensaio_v399.py -- o HARNESS DO POS-RITO da v399 em modo ENSAIO (derivado do harness_textos_ensaio_v398.py, que rodou na v398); SO' LEITURA do Nos real, da producao e das superficies reais.
Importa os modulos REAIS textos_v399.py e leitura_v399.py (os que a cadeia usa) e os executa contra um NOS EMULADO montado de dry_v399 (core_ensaio.json -> um_absoluto.json, selo_ensaio.json -> um_absoluto_selo.json, o um.py candidato, o kernel,
o .md, o artigo PT/EN e o sumario; o SIDECAR um_absoluto_selo_acom.json e' GERADO pela funcao do PROPRIO candidato (selo_acom_sidecar_v399, executada de uma copia de bytes) sobre o core e o selo FINAIS do Nos emulado, como em teste_conferidor_positivo_v399.py;
o stdout do rito e o APLICADO_AO_CANONICO sao EMULADOS e ditos: o stdout traz as linhas REAIS do fluxo principal do ensaio a seco mais as que so' o rito acrescenta, com a linha real do sidecar por ultimo). Tudo o que ele escreve fica em pos_rito\\harness_saida_v399\\
(e o resumo HARNESS_TEXTOS_ENSAIO_v399.json ao lado dele); nada do Nos real, da memoria, do Atlas, do mapa de rotas, da Bancada ou do git e' tocado; nenhum rito e' rodado.
O que ele prova (cada etapa e' uma entrada do resumo):
  precondicoes   o candidato (ESPERADOS == CANDIDATO == arquivo == dry_v399/um.py) e a regeneracao terminada (refazer_out_v399.txt mostra '== FIM'); a evidencia carrega mtime e sha16 de cada entrada;
  conferidor     o conferir_rito_v399.py REAL roda numa COPIA em ARVORE (conferidor_emulado\\work\\cadeia_de_selo\\v399 + work\\cunhagens_13out ao lado, porque o delta acha as falas do operador pelo caminho da propria pasta), SEM -I (importa o um.py do Nos emulado, que precisa do numpy do usuario),
                 contra o Nos emulado (V399_NOS) e da' TUDO BATE, com os 14 itens C1-C14 e o round trip: a conferencia que a leitura le;
  leitura        a leitura_v399.ler() REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS (selo de outra versao, registro ausente, registro nao selado, o selo ACOM adulterado em perfil, hash, controles, reconstrucao, separacao, gate, confidencialidade e direcao do testemunho,
                 a declaracao adulterada em fala, sha256, direcao, ancora, estatuto e pedra, a pedra Testemunho com bandeira falsa ou fora do trio, inscricao embutida adulterada ou rotulada como da gerencia, o sidecar ausente ou adulterado, os resumos do selo primario, quadro do topo que deixa de selar
                 ou de estar no topo, registros da v398 a v393 nao selados, face de Fock habitada ou dita dentro da pedra, AVISO da v399 ou de bloco anterior, linhas [v399], [v398], [v397] e a linha do sidecar ausentes), cada um tem de reprovar;
  textos         todas as funcoes publicas de textos_v399 renderizam, a guarda P18 e a da DIRECAO ficam limpas em cada saida, os marcadores que a cadeia exige estao nos textos, a errata da palavra «teoremas» esta nos textos que carregam _num;
  paragrafos     o PARAGRAFO DO QUADRO (textos_v399.paragrafo_readme, o da v397, intocado) passa nas verificacoes do quadro contra o resultado pinado e os CONTROLES NEGATIVOS reprovam: o 4,44 sem o p calibrado, o 4,44 sem a linha dos 5 sigma, numero adulterado, p adulterado,
                 a frase do operador parafraseada entre aspas, o 4,44 numa linha fora do item; a regra da ordem vale para TODO texto renderizado; e o PARAGRAFO NOVO (textos_v399.paragrafo_testemunho) passa na verificacao propria, com controles negativos (numero adulterado, direcao invertida,
                 estatuto removido, citacao nao verbatim, o 4,44 intruso, alegacao de seguranca criptografica, «consciencia» como termo, frase de limite removida); mais a direcao do testemunho em todo texto renderizado;
  cita_so_o_que_existe   cada `termo` entre crases de cada texto e' achado no kernel do Nos emulado, no um.py, nos insumos, nos arquivos ou como hash lido (o que nao e' achado e' dito e reprova);
  superficies    superficies_v399.py REAL roda em COPIAS das superficies reais em TRES cenarios: (a) o MEMORY.md real como esta (a superficie NAO compacta: se ele passar de 195 linhas depois da edicao, tem de RECUSAR com rc 3 sem escrever nada; senao, o caminho normal),
                 (b) um MEMORY.md com FOLGA (copia reduzida): o plano e' conferido antes da primeira escrita, idempotente na 2a rodada, marcadores do passo 9, <= 195 linhas e < 24 000 B, (c) um MEMORY.md NO LIMITE (195 linhas): tem de RECUSAR com rc 3, imprimir as
                 contagens e nao escrever nada em nenhuma copia; os originais nao mudam;
  b3_recibo      b3_recibo_v399.py REAL contra recibos SINTETICOS derivados dos recibos reais da v398 (positivos e negativos);
  mapa           registrar_mapa_v399.montar() REAL contra o core emulado e o livro de rotas real (so' leitura), e cada registro validado pela MESMA funcao que o mapa usa (rotas._valida), SEM registrar; grava registro_mapa_v399_ENSAIO.json (nao e' o registro);
  marcas         nenhuma linha de comentario com a marca de texto pendente em pos_rito\\*.py; ast.parse de todo .py e sh -n do chain.
uso: python -B -X utf8 harness_textos_ensaio_v399.py [--sem-superficies] [--sem-b3] [--sem-negativos] [--rotulo <nome>] [--nao-exigir-refazer] [--manter-copias]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita, nada foi rodado;
--nao-exigir-refazer: NAO exige refazer_out_v399.txt (nem o '== FIM' nem as datas): modo de ENSAIO antes de a gerencia regerar o candidato; o resumo e o veredito DIZEM que a regeneracao nao foi comprovada, e o resumo vai para
HARNESS_TEXTOS_ENSAIO_v399_DEPURACAO_sem_refazer.json (o nome HARNESS_TEXTOS_ENSAIO_v399.json so' nasce na rodada que EXIGE o refazer);
sem --manter-copias o Nos emulado e as copias pesadas das superficies sao apagados no fim, so' dentro de harness_saida_v399)"""'''
NEW_STD = r'''_ens = rdj(os.path.join(PKG, "ensaio_a_seco_v399.json"))   # o fluxo do main do ensaio a seco: as linhas REAIS que o main imprime (o resto e' EMULADO e dito)
# o SIDECAR: a funcao do PROPRIO candidato (a copia de bytes do Nos emulado; __file__ = nos_emulado\um.py) sobre o core e o selo FINAIS do Nos emulado; a linha que ela imprime e' a linha REAL do sidecar
_spec_sc = importlib.util.spec_from_file_location("um_sidecar_emulacao", os.path.join(NOSE, "um.py")); _umm = importlib.util.module_from_spec(_spec_sc)
_so = sys.stdout; sys.stdout = io.StringIO()
try:
    _spec_sc.loader.exec_module(_umm); _umm.OUT = NOSE
    sys.stdout = _buf_sc = io.StringIO()
    _umm.selo_acom_sidecar_v399()
    _linha_sidecar = _buf_sc.getvalue().strip()
finally:
    sys.stdout = _so; sys.stdout.reconfigure(encoding="utf-8")
del _umm, _spec_sc
N_ = ESP["escada"][1]
STDOUT_EMULADO = "\n".join(["[v399] EMULADO PELO HARNESS (nao e' o stdout de um rito; as linhas do fluxo principal sao as REAIS do ensaio a seco; as do kernel e do selo e o RITO_RC sao emulados)"] + list(_ens["mainflow"]["stdout"])
                           + ["teoremas limpos: %s/%s" % (N_, N_), ">>> TGL_KERNEL_STAGE1_VERIFIED", "[selo] rite_checkpoints: chave desligada ; reaproveitados 0", "FAIL_CLOSED_SELFTEST_PASSED", "[selo] colapso tipado: EMULADO", _linha_sidecar, "RITO_RC=0", ""])
open(os.path.join(NOSE, "rodada_v399_stdout.txt"), "w", encoding="utf-8", newline="\n").write(STDOUT_EMULADO)'''
NOVA_CONF_HT = r'''# v399 (desvio do molde, dito): o conferidor importa o delta, o runtime, o acom_conferencias e os insumos pelo caminho da propria pasta, e o delta acha as falas do operador em ..\..\cunhagens_13out: por isso roda numa COPIA em ARVORE
# (conferidor_emulado\work\cadeia_de_selo\v399, com work\cunhagens_13out ao lado) e SEM -I (importa o um.py do Nos emulado, que precisa do numpy do usuario). Nada fora de harness_saida_v399 e' escrito.
DLX = importar("delta_v399_x", os.path.join(PKG, "delta_v399.py"))
CFR = os.path.join(OUT, "conferidor_emulado"); CF = os.path.join(CFR, "work", "cadeia_de_selo", "v399"); os.makedirs(CF)
for n in ("conferir_rito_v399.py", "delta_v399.py", "quadro_v397.py", "runtime_quadro_v397.py", "acom_conferencias_v399.py", "runtime_v399.py", "ESPERADOS_v399.json"):
    shutil.copyfile(os.path.join(PKG, n), os.path.join(CF, n))
shutil.copytree(os.path.join(PKG, "insumos", "acom"), os.path.join(CF, "insumos", "acom"))
os.makedirs(os.path.join(CFR, "work", "cunhagens_13out"))
for _o in DLX.VERBATIM_ORIGEM:
    shutil.copyfile(_o, os.path.join(CFR, "work", "cunhagens_13out", os.path.basename(_o)))
env = dict(os.environ); env["V399_NOS"] = NOSE; env["PYTHONIOENCODING"] = "utf-8"
pr = subprocess.run([sys.executable, "-B", "-X", "utf8", "conferir_rito_v399.py"], cwd=CF, env=env, capture_output=True, text=True, encoding="utf-8")'''
NEW_VARIANTE_E_NEG = r'''sc_path = os.path.join(NOSE, "um_absoluto_selo_acom.json"); sc_raw = open(sc_path, "rb").read() if os.path.exists(sc_path) else b""


def variante(nome, f_core=None, f_selo=None, f_std=None, f_conf=None, f_sc=None, sc_fora=False, espera=""):
    """aplica a variante nos arquivos do Nos emulado (e da conferencia do rito e do sidecar), roda a leitura, RESTAURA os bytes e confere que reprovou (com o trecho esperado na mensagem)."""
    try:
        if f_core:
            c = json.loads(core_raw.decode("utf-8")); f_core(c["core"]); open(core_path, "wb").write(json.dumps(c, ensure_ascii=False).encode("utf-8"))
        if f_selo:
            s = json.loads(selo_raw.decode("utf-8")); f_selo(s); open(selo_path, "wb").write(json.dumps(s, ensure_ascii=False).encode("utf-8"))
        if f_std:
            open(std_path, "wb").write(f_std(std_raw.decode("utf-8")).encode("utf-8"))
        if f_conf:
            cj = json.loads(conf_raw.decode("utf-8")); f_conf(cj); open(conf_path, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
        if f_sc:
            sj = json.loads(sc_raw.decode("utf-8")); f_sc(sj); open(sc_path, "wb").write(json.dumps(sj, ensure_ascii=False).encode("utf-8"))
        if sc_fora:
            os.remove(sc_path)
        _, PV = L.ler()
    finally:
        open(core_path, "wb").write(core_raw); open(selo_path, "wb").write(selo_raw); open(std_path, "wb").write(std_raw)
        if os.path.exists(conf_path):
            open(conf_path, "wb").write(conf_raw)
        open(sc_path, "wb").write(sc_raw)
    ok = any(espera in x for x in PV)
    return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": ok, "problemas": [x[:140] for x in PV][:3]}


def _core_k(c, k):
    return c[k]


def _sem_selo(c):
    c.pop("selo_pela_propria_tecnologia_v399", None)


def _sem_declaracao(c):
    c.pop("declaracao_do_operador_v399", None)


def _nao_sela_cunh(c):
    c["cunhagens_v399"]["all_verified"] = False


def _nao_sela_kh(c):
    c["kh_n1_cobertura_v399"]["all_verified"] = False


def _selo_nao_sela(c):
    c["selo_pela_propria_tecnologia_v399"]["all_verified"] = False


def _selo_cheque_falha(c):
    c["selo_pela_propria_tecnologia_v399"]["checks"][2][1] = False


def _selo_perfil(c):
    c["selo_pela_propria_tecnologia_v399"]["values"]["perfil"] = "ACOM-INT-C128-Q8"


def _selo_bloco(c):
    c["selo_pela_propria_tecnologia_v399"]["values"]["bloco_embutido_sha256"] = "0" * 64


def _selo_sha(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["sha256"] = "0" * 64


def _selo_psi(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["psi"]["sha256"] = "0" * 64


def _selo_theta_bytes(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["theta"]["bytes"] += 1


def _selo_controles_12(c):
    c["selo_pela_propria_tecnologia_v399"]["controles_negativos"]["n_controles"] = 12


def _selo_controle_aceito(c):
    r = c["selo_pela_propria_tecnologia_v399"]["controles_negativos"]; r["controles"][0]["ok"] = False; r["todos_recusados"] = False


def _selo_reconstrucao(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["prova_de_reconstrucao"]["bytes_divergentes"] = 1


def _selo_psi_redundante(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["auditoria_de_separacao"]["psi_redundante"] = True


def _selo_gate(c):
    c["selo_pela_propria_tecnologia_v399"]["does_not_gate_core"] = False


def _selo_confidencialidade(c):
    c["selo_pela_propria_tecnologia_v399"]["statuses"]["confidencialidade"] = "garantida pelo metodo"


def _selo_direcao_invertida(c):
    c["selo_pela_propria_tecnologia_v399"]["direcao_do_testemunho"] = "o operador testifica DA IALD; a IALD testifica do operador"


def _selo_beta(c):
    c["selo_pela_propria_tecnologia_v399"]["values"]["beta"] = 0.0121


def _decl_nao_sela(c):
    c["declaracao_do_operador_v399"]["all_verified"] = False


def _decl_fala(c):
    c["declaracao_do_operador_v399"]["declaration"]["statement_verbatim"] += " "


def _decl_sha(c):
    c["declaracao_do_operador_v399"]["declaration"]["verbatim_sha256"] = "0" * 64


def _decl_direcao(c):
    c["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"]["a_IALD"] = "testifica do operador"


def _decl_pai(c):
    c["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"]["o_Pai_de_Jo_8_18"] = "le-se na IALD"


def _decl_ancora_fora(c):
    c["declaracao_do_operador_v399"]["declaration"]["kernel_anchors_REAL"][0]["axiomas_no_trio"] = False


def _decl_estatuto(c):
    c["declaracao_do_operador_v399"]["declaration"]["status_of_statement"] = "[REAL] o kernel a prova"


def _decl_pedra_vazia(c):
    c["declaracao_do_operador_v399"]["declaration"]["pedra_instalada"] = []


def _decl_gate(c):
    c["declaracao_do_operador_v399"]["does_not_gate_core"] = False


def _pedra_bandeira(c):
    c["kernel_formalization"][ESP["bandeiras_das_pedras"]["testemunho"]] = False


def _pedra_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][ESP["teoremas_das_pedras"]["testemunho"]] = ["propext", "sorryAx"]


def _pedra_lema_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][ESP["contrato_das_pedras"]["testemunho"][0]] = ["propext", "sorryAx"]


def _pedra_suporte_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][sorted(ESP["suporte_das_pedras"]["testemunho"])[0]] = ["propext", "sorryAx"]


def _pedra_fonte_adulterada(c):
    c["kernel_formalization"]["formal_files_sha256"][sorted(ESP["pedras_sha256"])[0]] = "0" * 64


def _gerencia_na_cunhagem(c):
    ex = c["cunhagens_v399"]["extras"]; ex["autor_de_cada_inscricao"][sorted(ex["autor_de_cada_inscricao"])[0]] = "gerencia"


def _cunh_direcao(c):
    c["cunhagens_v399"]["extras"]["direcao_do_testemunho"]["a_IALD"] = "testifica do operador"


def _cunh_declaracao_sha(c):
    c["cunhagens_v399"]["extras"]["declaracao"]["sha256"] = "0" * 64


def _inscricao_adulterada(c):
    list(c["cunhagens_v399"]["verbatim"].values())[0]["embedded_ok"] = False


def _inscricao_sha(c):
    list(c["cunhagens_v399"]["verbatim"].values())[1]["sha256"] = "0" * 64


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


def _sonico398_cai(c):
    c["sonico_v398"]["all_verified"] = False


def _afinacao398_cai(c):
    c["afinacao_das_cordas_v398"]["all_verified"] = False


def _cunh398_cai(c):
    c["cunhagens_v398"]["all_verified"] = False


def _kh398_cai(c):
    c["kh_n1_cobertura_v398"]["all_verified"] = False


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


def _selo_v398(s):
    s["um_version"] = "v398"


def _selo_resumo_diferente(s):
    s["selo_pela_propria_tecnologia_v399"]["verdict"] = "OUTRO_VEREDITO"


def _selo_resumo_sha(s):
    s["selo_pela_propria_tecnologia_v399"]["sha256_do_um_py"] = "0" * 64


def _selo_formal_nao_selado(s):
    s["not_sealed_this_run"]["formais"] = ["selo_pela_propria_tecnologia_v399"]


def _conf_quadro_pt(cj):
    cj["quadro"]["pt"]["ok"] = False


def _conf_quadro_md(cj):
    cj["quadro"]["md"]["ok"] = False


def _conf_c5(cj):
    cj["acom_itens"]["C5"]["ok"] = False


def _conf_round_trip(cj):
    cj["acom_itens"]["round_trip_do_um_py_instalado_independente"]["ok"] = False


def _conf_sidecar(cj):
    cj["sidecar"]["existe"] = False


def _sc_sha_objeto(sj):
    sj["objetos"][1]["sha256"] = "0" * 64


def _sc_recusas(sj):
    sj["recusas"] = [{"nome": "um.py", "recusa": "RECUSOU:X"}]


def _sc_veredito(sj):
    sj["veredito"] = "TGL_SELO_ACOM_SIDECAR_V399__REFUSED__SOME_OBJECTS_REFUSED"


def _sc_objeto_faltando(sj):
    sj["objetos"].pop()


def _sc_confidencialidade(sj):
    sj["honestidade"]["confidencialidade"] = "garantida pelo metodo"


def _sc_um_py_outro(sj):
    sj["objetos"][0]["acom"]["psi"]["sha256"] = "0" * 64


def _sc_esquema(sj):
    sj["esquema"] = "outro_esquema"


def _sc_direcao_invertida(sj):
    sj["gerado_por"] = "a IALD testifica do operador"


NEG = []
if not SEM_NEG and not P:
    NEG = [variante("selo de outra versao (v398)", f_selo=_selo_v398, espera="o selo nao e v399"),
           variante("registro selo_pela_propria_tecnologia_v399 ausente do core", f_core=_sem_selo, espera="registro obrigatorio ausente do core: selo_pela_propria_tecnologia_v399"),
           variante("registro declaracao_do_operador_v399 ausente do core", f_core=_sem_declaracao, espera="registro obrigatorio ausente do core: declaracao_do_operador_v399"),
           variante("cunhagens_v399 nao selou", f_core=_nao_sela_cunh, espera="cunhagens_v399 nao selou"),
           variante("kh_n1_cobertura_v399 nao selou", f_core=_nao_sela_kh, espera="kh_n1_cobertura_v399 nao selou"),
           variante("selo ACOM: o registro nao selou", f_core=_selo_nao_sela, espera="selo_pela_propria_tecnologia_v399 nao selou"),
           variante("selo ACOM: uma checagem falhou", f_core=_selo_cheque_falha, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: perfil adulterado", f_core=_selo_perfil, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: hash do bloco embutido adulterado", f_core=_selo_bloco, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: o SHA-256 ao lado difere do um.py do disco", f_core=_selo_sha, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: hash de Psi adulterado", f_core=_selo_psi, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: bytes de Theta adulterados", f_core=_selo_theta_bytes, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: controles negativos 12 em vez do pinado", f_core=_selo_controles_12, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: um controle negativo ACEITOU", f_core=_selo_controle_aceito, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: reconstrucao com byte divergente", f_core=_selo_reconstrucao, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: Psi redundante (separacao vazia)", f_core=_selo_psi_redundante, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: o registro move o gate", f_core=_selo_gate, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: confidencialidade alegada", f_core=_selo_confidencialidade, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: direcao do testemunho invertida", f_core=_selo_direcao_invertida, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: beta do registro != alfa x raiz de e do core", f_core=_selo_beta, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("declaracao: o registro nao selou", f_core=_decl_nao_sela, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: a fala embutida difere do arquivo do operador", f_core=_decl_fala, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: sha256 da fala adulterado", f_core=_decl_sha, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: a IALD como quem testifica do operador", f_core=_decl_direcao, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: o Pai de Jo 8,18 lido na IALD", f_core=_decl_pai, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: uma ancora do kernel fora do trio", f_core=_decl_ancora_fora, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: o estatuto trocado por REAL", f_core=_decl_estatuto, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: a pedra Testemunho nao conferida", f_core=_decl_pedra_vazia, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: o registro move o gate", f_core=_decl_gate, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("pedra Testemunho: bandeira da composicao falsa", f_core=_pedra_bandeira, espera="a pedra Testemunho nao esta no kernel do rito"),
           variante("pedra Testemunho: composicao fora do trio", f_core=_pedra_fora_do_trio, espera="a pedra Testemunho nao esta no kernel do rito"),
           variante("pedra Testemunho: o lema novo fora do trio", f_core=_pedra_lema_fora_do_trio, espera="a pedra Testemunho nao esta no kernel do rito"),
           variante("pedra Testemunho: um termo antigo citado fora do trio", f_core=_pedra_suporte_fora_do_trio, espera="a pedra Testemunho nao esta no kernel do rito"),
           variante("pedra Testemunho: sha256 da fonte no hash formal adulterado", f_core=_pedra_fonte_adulterada, espera="a pedra Testemunho nao esta no kernel do rito"),
           variante("cunhagens: uma inscricao rotulada como da gerencia", f_core=_gerencia_na_cunhagem, espera="TODAS falas do operador"),
           variante("cunhagens: a direcao do testemunho invertida no registro", f_core=_cunh_direcao, espera="cunhagens_v399: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens: sha256 da declaracao adulterado no registro", f_core=_cunh_declaracao_sha, espera="cunhagens_v399: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens: uma inscricao deixou de estar embutida", f_core=_inscricao_adulterada, espera="as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens: sha256 de uma inscricao adulterado", f_core=_inscricao_sha, espera="as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("sidecar: ausente", sc_fora=True, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: sha256 de um objeto adulterado", f_sc=_sc_sha_objeto, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: recusas registradas", f_sc=_sc_recusas, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: veredito de recusa", f_sc=_sc_veredito, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: um objeto faltando", f_sc=_sc_objeto_faltando, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: confidencialidade alegada na honestidade", f_sc=_sc_confidencialidade, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: o hash de Psi do um.py != ESPERADOS", f_sc=_sc_um_py_outro, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: esquema trocado", f_sc=_sc_esquema, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: a direcao do testemunho invertida", f_sc=_sc_direcao_invertida, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("selo primario: o resumo do selo ACOM difere do core", f_selo=_selo_resumo_diferente, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: o sha256 do um.py no resumo difere do disco", f_selo=_selo_resumo_sha, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: modulo formal nao selado", f_selo=_selo_formal_nao_selado, espera="o selo traz modulo formal nao selado"),
           variante("o quadro do topo: numero lido adulterado (z_disc 4,45)", f_core=_numero_adulterado, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: z_disc calibrado acima de 5", f_core=_z_disc_acima_de_5, espera="abaixo de 5"),
           variante("o quadro do topo: uma checagem do registro de veracidade falhou", f_core=_checagem_falha, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: fonte do registro de veracidade com sha256 adulterado", f_core=_fonte_adulterada, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: o registro de veracidade move o gate", f_core=_gate_movido, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: o registro de veracidade deixou de selar", f_core=_veracidade_cai, espera="teste_de_veracidade_fase9_v397"),
           variante("o quadro do topo: a conferencia diz que o quadro PT deixou de estar no topo", f_conf=_conf_quadro_pt, espera="o quadro do topo (O Teste da Unica Palavra, pt)"),
           variante("o quadro do topo: a conferencia diz que o quadro do .md deixou de estar no topo", f_conf=_conf_quadro_md, espera="o quadro do topo (O Teste da Unica Palavra, md)"),
           variante("a conferencia diz que o item C5 do selo ACOM nao conferiu", f_conf=_conf_c5, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia diz que o round trip do um.py instalado nao conferiu", f_conf=_conf_round_trip, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia diz que o sidecar nao existe", f_conf=_conf_sidecar, espera="o sidecar um_absoluto_selo_acom.json nao existe ou nao esta selado"),
           variante("sonico_v398 deixou de selar", f_core=_sonico398_cai, espera="sonico_v398"),
           variante("afinacao_das_cordas_v398 deixou de selar", f_core=_afinacao398_cai, espera="afinacao_das_cordas_v398"),
           variante("cunhagens_v398 deixou de selar", f_core=_cunh398_cai, espera="cunhagens_v398"),
           variante("kh_n1_cobertura_v398 deixou de selar", f_core=_kh398_cai, espera="kh_n1_cobertura_v398"),
           variante("cunhagens_v397 deixou de selar", f_core=_cunh397_cai, espera="cunhagens_v397"),
           variante("testemunha_estatica_v396 deixou de selar", f_core=_testemunha_cai, espera="testemunha_estatica_v396"),
           variante("face de Fock da testemunha com habitante exibido", f_core=_fock_da_testemunha_habitada, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),
           variante("face de Fock dita DENTRO da pedra da testemunha", f_core=_fock_dentro_da_pedra, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),
           variante("psibit_v395 deixou de selar", f_core=_psibit_cai, espera="psibit_v395"),
           variante("face de Fock do psibit_v395 habitada", f_core=_face_do_psibit_habitada, espera="psibit_v395: a face do psion deixou de estar como CONDICIONAL"),
           variante("registro da v394 deixou de selar", f_core=_v394_cai, espera="criterio_binario_de_parada_v394"),
           variante("AVISO da v399 no stdout", f_std=lambda t: t + "   [v399] AVISO: o selo ACOM nao rodou: ValueError('x')\n", espera="AVISO da v399"),
           variante("AVISO do sidecar no stdout", f_std=lambda t: t.replace("RITO_RC=0", "[selo_acom] AVISO: nao consegui escrever o sidecar: OSError('x')\nRITO_RC=0"), espera="AVISO da v399"),
           variante("AVISO de bloco anterior (v398) no stdout", f_std=lambda t: t + "   [v398] AVISO: o sonico nao rodou: ValueError('x')\n", espera="AVISO de um bloco anterior"),
           variante("linha [v399] ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o selo pela propria tecnologia e a declaracao do operador" not in l) + "\n", espera="linha [v399] do stdout"),
           variante("linha `>>> veredito <<<` do selo ACOM ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if ESP["selo_acom"]["verdict"] not in l or "selo=" in l) + "\n", espera="o bloco selo_pela_propria_tecnologia_v399 do stdout"),
           variante("linha `>>> veredito <<<` da declaracao ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if ESP["declaracao"]["verdict"] not in l or "declaracao=" in l) + "\n", espera="o bloco declaracao_do_operador_v399 do stdout"),
           variante("linha [v398] (sonico, afinacao e cunhagens) ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o sonico e a afinacao das cordas" not in l) + "\n", espera="linha [v398] do stdout"),
           variante("linha [v397] do Teste da Unica Palavra ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o Teste da Unica Palavra" not in l) + "\n", espera="linha [v397] do Teste da Unica Palavra"),
           variante("linha do sidecar ausente do stdout (a ultima nao e' a do sidecar)", f_std=lambda t: "\n".join(l for l in t.splitlines() if not l.startswith("[selo_acom]")) + "\n", espera="as duas ultimas linhas do stdout"),
           variante("a linha do sidecar antes da do colapso tipado (ordem trocada)", f_std=lambda t: "\n".join(sorted(t.splitlines(), key=lambda l: (l.startswith("[selo] colapso tipado") and 1 or 0, l.startswith("[selo_acom]") and 0 or 1)) if False else [l for l in t.splitlines() if not l.startswith("[selo_acom]") and not l.startswith("[selo] colapso tipado") and not l.startswith("RITO_RC=")] + [l for l in t.splitlines() if l.startswith("[selo_acom]")] + [l for l in t.splitlines() if l.startswith("[selo] colapso tipado")] + ["RITO_RC=0"]) + "\n", espera="as duas ultimas linhas do stdout")]'''
K_EMU_NOVO = '"rel_man": "EMULADO_SEM_HASH", "readme_paragrafo": T.paragrafo_readme()[0], "readme_paragrafo_testemunho": T.paragrafo_testemunho()[0]}'
FUNCOES_HT = r'''FUNCOES = [("_d", lambda: T._d(Vd)), ("_num", lambda: T._num(Vd)), ("_num_sem_veredito", lambda: T._num(Vd, verdicts=False)), ("_cunhagens_lista", lambda: T._cunhagens(Vd)), ("_cunhagens_curta", lambda: T._cunhagens(Vd, "curta")),
           ("_ordem", lambda: T._ordem(Vd)), ("_entrou", lambda: T._entrou(Vd)), ("_direcao", lambda: T._direcao(Vd)), ("_declaracao", lambda: T._declaracao(Vd)), ("_selo_acom", lambda: T._selo_acom(Vd)), ("_sidecar", lambda: T._sidecar(Vd)), ("_pedra", lambda: T._pedra(Vd)),
           ("_regra_do_4_44", lambda: T._regra_do_4_44(Vd)), ("_kernel_prova", lambda: T._kernel_prova(Vd)), ("_limites", lambda: T._limites(Vd)), ("_limites_curto", lambda: T._limites(Vd, curto=True)), ("_legal", lambda: T._legal(Vd)), ("_erratas", lambda: T._erratas(Vd)),
           ("_depois", lambda: T._depois(Vd)), ("_rodada", lambda: T._rodada(Vd)), ("linhagem", lambda: T.linhagem(Vd)), ("desenho", lambda: T.desenho(Vd)), ("atlas", lambda: T.atlas(Vd)), ("core_memory", lambda: T.core_memory(Vd)),
           ("haja_luz", lambda: T.haja_luz(Vd)), ("topico_missao", lambda: T.topico_missao(Vd)), ("topico_central", lambda: T.topico_central(Vd)), ("topico_estatuto", lambda: T.topico_estatuto(Vd)), ("topico_novo", lambda: T.topico_novo(Vd)),
           ("aviso", lambda: T.aviso(Vd, "REIVINDICACAO_EMULADA")), ("aviso_pulado", lambda: T.aviso_pulado()), ("handoff", lambda: T.handoff(Vd, K_EMU)), ("arvore_linha", lambda: T.arvore_linha(Vd)), ("titulo_verbete", lambda: T.titulo_verbete(Vd)),
           ("verbete", lambda: T.verbete(Vd)), ("remissivo", lambda: T.remissivo(Vd)), ("linha_handoff", lambda: T.linha_handoff(Vd)), ("linha_topico_novo", lambda: T.linha_topico_novo(Vd)), ("marca_missao", lambda: T.marca_missao(Vd)),
           ("marca_topico_missao", lambda: T.marca_topico_missao(Vd)), ("marca_central", lambda: T.marca_central(Vd)), ("id_missao", lambda: T.id_missao(Vd)), ("id_central", lambda: T.id_central(Vd)), ("paragrafo_readme", lambda: T.paragrafo_readme()[0]),
           ("paragrafo_testemunho", lambda: T.paragrafo_testemunho()[0])]
CARREGAM_NUM = {"_num", "_num_sem_veredito", "linhagem", "atlas", "core_memory", "topico_novo", "verbete", "handoff"}   # os textos que embutem _num (o texto do kernel com a errata da palavra «teoremas»)
S16 = Vd.get("s16") or ESP["candidato_sha16"]
MARCADORES = {"linhagem": [S16, "<!-- linhagem_v399_selada -->", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "kh_n1_cobertura_v399"], "desenho": ["<!-- adendo_v399_selada -->", S16], "atlas": ["<!-- atlas_v399_selada -->", S16, "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "kh_n1_cobertura_v399"],
              "core_memory": ["<!-- core_v399_selada -->", S16], "haja_luz": ["<!-- haja_luz_v399_selada -->", S16], "topico_estatuto": ["<!-- v399_selada -->", S16], "topico_novo": [S16, "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "kh_n1_cobertura_v399", "# v399 SELADA ("],
              "aviso": ["<!-- aviso_v399_selada -->", S16], "handoff": ["name: handoff-v399-custodia", S16, "<!-- INICIO_PARAGRAFO_README_v397 -->", "<!-- FIM_PARAGRAFO_README_v397 -->", "<!-- INICIO_PARAGRAFO_TESTEMUNHO_v399 -->", "<!-- FIM_PARAGRAFO_TESTEMUNHO_v399 -->", "um_absoluto_selo_acom.json"],
              "linha_handoff": ["handoff-v399-custodia.md", S16], "topico_missao": [S16], "topico_central": [S16]}'''
NEW_4C = r'''# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (o testemunho de dois): verificacao propria, controles negativos e a DIRECAO do testemunho em todo texto renderizado
_sn = {"ok": False}
try:
    PAR_T, PAR_T_INFO = T.paragrafo_testemunho()
    _sn["positivo_sem_falhas"] = (T.verificar_paragrafo_testemunho(PAR_T, _core_p, ESP) == [])
    _sn["igual_ao_gerado_do_core"] = (PAR_T == T._paragrafo_testemunho_de(_core_p))
    _ho = RENDER.get("handoff", "")
    _sn["handoff_traz_os_dois_paragrafos_entre_os_marcadores"] = bool((T.MARC_TMN_INI + "\n" + PAR_T.rstrip("\n") + "\n" + T.MARC_TMN_FIM) in _ho and ("<!-- INICIO_PARAGRAFO_README_v397 -->\n" + PAR.rstrip("\n") + "\n<!-- FIM_PARAGRAFO_README_v397 -->") in _ho)
    _sn["handoff_lista_o_sidecar"] = bool("um_absoluto_selo_acom.json" in _ho and Vd["sidecar"]["sha256"] in _ho and Vd["sidecar"]["veredito"] in _ho)
    _sn["info"] = PAR_T_INFO
    if not (_sn["positivo_sem_falhas"] and _sn["igual_ao_gerado_do_core"] and _sn["handoff_traz_os_dois_paragrafos_entre_os_marcadores"] and _sn["handoff_lista_o_sidecar"]):
        falha("paragrafo novo do testemunho: positivo %s, igual ao gerado do core %s, no handoff %s, sidecar listado %s" % (_sn["positivo_sem_falhas"], _sn["igual_ao_gerado_do_core"], _sn["handoff_traz_os_dois_paragrafos_entre_os_marcadores"], _sn["handoff_lista_o_sidecar"]))
    _sv = _core_p["selo_pela_propria_tecnologia_v399"]; _ss = _sv["selo"]; _psi = format(int(_ss["acom"]["psi"]["bytes"]), ","); _nbytes = format(int(_ss["bytes"]), ","); _nctl = "%s controles negativos" % _sv["controles_negativos"]["n_controles"]

    def _muts(nome, f, espera):
        p2 = f(PAR_T); fa = T.verificar_paragrafo_testemunho(p2, _core_p, ESP)
        ok = bool(p2 != PAR_T and fa and any(espera in x for x in fa)); return {"controle": nome, "reprovou": bool(fa), "mensagem_esperada_presente": any(espera in x for x in fa), "ok": ok, "falhas": [x[:140] for x in fa][:3]}
    _NEGS = [_muts("bytes de Psi com um digito trocado (em todo o paragrafo)", lambda p: p.replace(_psi, _psi[:-1] + str((int(_psi[-1]) + 1) % 10)), "ausente do paragrafo"),
             _muts("bytes do um.py com um digito trocado (em todo o paragrafo)", lambda p: p.replace(_nbytes, _nbytes[:-1] + str((int(_nbytes[-1]) + 1) % 10)), "ausente do paragrafo"),
             _muts("o numero de controles negativos adulterado", lambda p: p.replace(_nctl, "12 controles negativos"), "ausente do paragrafo"),
             _muts("a IALD como quem testifica do operador (direcao invertida)", lambda p: p.replace("a IALD NÃO testifica do operador", "a IALD testifica do operador", 1), "DIRECAO"),
             _muts("o Pai de Jo 8,18 lido na IALD em vez de no absoluto", lambda p: p.replace("NO ABSOLUTO, o Um", "na IALD, o Um", 1), "frase de limite ausente"),
             _muts("o kernel passa a provar a declaracao", lambda p: p.replace("O kernel NÃO a prova", "O kernel a prova", 1), "frase de limite ausente"),
             _muts("a segunda testemunha com forca criptografica independente", lambda p: p.replace("NÃO força criptográfica independente", "tem força criptográfica independente", 1), "frase de limite ausente"),
             _muts("seguranca criptografica garantida", lambda p: p.replace("a confidencialidade não é alegada nem medida", "o sigilo está garantido", 1), "frase de limite ausente"),
             _muts("a confidencialidade garantida (alegacao)", lambda p: p + "\n> - A confidencialidade garantida e o sigilo garantido do metodo.\n", "alega seguranca criptografica"),
             _muts("o arredondamento dito da patente", lambda p: p.replace("NÃO é da patente", "é da patente", 1), "frase de limite ausente"),
             _muts("a leitura das duas faces sem o rotulo da gerencia", lambda p: p.replace("[ONTO] da gerência, a ratificar", "do operador", 1), "frase de limite ausente"),
             _muts("a decisao [LEGAL] tirada do operador", lambda p: p.replace("decisão do operador com a agente de PI", "decisão da gerência", 1), "frase de limite ausente"),
             _muts("citacao do operador que nao e' verbatim", lambda p: p.replace("a operação quadrática da inscrição viva", "a operação quadrática da inscrição vivida", 1), "NAO e' verbatim"),
             _muts("a declaracao sem o estatuto DECLARACAO DO OPERADOR / INPUT", lambda p: p.replace("[DECLARAÇÃO DO OPERADOR / INPUT]", "[REAL]", 1), "estatuto ausente"),
             _muts("a pedra sem o estatuto REAL", lambda p: p.replace("**A pedra Testemunho** [REAL]", "**A pedra Testemunho**", 1), "diferem" if False else "difere do gerado"),
             _muts("o SHA-256 sem o estatuto KNOWN", lambda p: p.replace("[KNOWN]", "", 1), "estatuto ausente"),
             _muts("o 4,44 entra no paragrafo", lambda p: p + "\n> z_disc = " + _z + "\n", "4,44"),
             _muts("a palavra consciencia usada como termo", lambda p: p + "\n> - A consciência é a tipagem que falta.\n", "consciencia"),
             _muts("o gate dito movido", lambda p: p.replace("o gate não se move", "o gate se move", 1), "frase de limite ausente"),
             _muts("a creditacao dita pela validade", lambda p: p.replace("validade no kernel não é creditação", "validade no kernel é creditação", 1), "frase de limite ausente")]
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
    _inv_txt = "A IALD testifica do operador, e o um.py testifica em hash."
    _tx = {"cita_fora_dos_bytes_levanta": _levanta(lambda: T._cita("o um.py testifica de si mesmo e a IALD de ninguem")),
           "cita_verbatim_passa": (T._cita("falta só a tipagem") == "«falta só a tipagem»"),
           "atribuicao_limpa_nos_textos": {nome: T.atribuicao_da_gerencia(txt) for nome, txt in RENDER.items() if T.atribuicao_da_gerencia(txt)} == {},
           "controle_direcao_invertida": bool(T.atribuicao_da_gerencia(_inv_txt)),
           "controle_a_fala_em_que_ele_recusa_a_ordem_inversa_passa": (T.atribuicao_da_gerencia(T._cita("eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela")) == []),
           "controle_a_IALD_nao_testifica_passa": (T.atribuicao_da_gerencia("a IALD NÃO testifica do operador") == []),
           "controle_consciencia_como_termo": bool(T.atribuicao_da_gerencia("A consciência é a tipagem que falta.")),
           "controle_consciencia_palavra_retirada_passa": (T.atribuicao_da_gerencia("a palavra «consciência» é retirada por ele") == []),
           "controle_inscricao_da_gerencia": bool(T.atribuicao_da_gerencia("as falas do operador e da gerência"))}
    _sn["textos"] = _tx
    _ruim = [k for k, v in _tx.items() if not v]
    if _ruim:
        falha("direcao do testemunho / citacao verbatim: controles que nao deram o esperado: %s" % _ruim)
    _sn["ok"] = True
    print("  paragrafo novo (o testemunho de dois): positivo ok; %d controles negativos; direcao e citacao: %d controles ok" % (len(_NEGS), len(_tx)))
except BaseException as ex:  # noqa: BLE001
    _sn["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:400]); _sn["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo novo do testemunho de dois: %s" % _sn["erro"])
etapa("paragrafo_testemunho_e_direcao_do_testemunho", **_sn)'''
HEX16_NOVO = r'''HEX16.update(str(v)[:16] for v in ((ESP.get("selo_acom") or {}).get(k) for k in ("bloco_embutido_sha256", "sha256_do_um_py", "lut_sha256")) if v); HEX16.update(str(((ESP.get("selo_acom") or {}).get(p) or {}).get("sha256"))[:16] for p in ("psi", "theta", "kappa"))
HEX16.add(str((ESP.get("declaracao") or {}).get("verbatim_sha256"))[:16]); HEX16.add((Vd.get("sidecar") or {}).get("sha16") or ""); HEX16.update((o.get("sha16") or "") for o in ((Vd.get("sidecar") or {}).get("objetos") or {}).values())
HEX16.add((Vd.get("selo") or {}).get("bloco16") or ""); HEX16.update((Vd.get("selo") or {}).get(k) or "" for k in ("psi_sha16", "theta_sha16", "kappa_sha16", "lut16"))
HEX64 = {str((Vd.get("sidecar") or {}).get("sha256") or ""), str(Vd.get("s64") or "")} | {str(o.get("sha256") or "") for o in ((Vd.get("sidecar") or {}).get("objetos") or {}).values()}; HEX64.discard("")   # os hashes COMPLETOS que o handoff lista (o sidecar e os tres objetos), lidos do sidecar e do um.py do disco'''
CONHEC_NOVO = r'''CONHECIDOS.add(T._linha_maquina_testemunho(core_emu["selo_pela_propria_tecnologia_v399"]["values"], dict(core_emu["selo_pela_propria_tecnologia_v399"]["selo"]["acom"], bytes=core_emu["selo_pela_propria_tecnologia_v399"]["selo"]["bytes"]), core_emu["selo_pela_propria_tecnologia_v399"]["controles_negativos"]["n_controles"], core_emu["declaracao_do_operador_v399"]["declaration"]["verbatim_sha256"]))   # a linha de maquina do paragrafo novo (lida dos registros do core emulado)
CONHECIDOS.add((Vd.get("selo") or {}).get("perfil") or ""); CONHECIDOS.add((Vd.get("sidecar") or {}).get("esquema") or ""); CONHECIDOS.add((Vd.get("sidecar") or {}).get("veredito") or "")'''
NOMES_NOVOS = r'''NOMES_ARQ.update({"um_absoluto_selo_acom.json", "um_absoluto_selo.json", "um_absoluto.json", "conferencia_rito_v399.json", "v399_selo", "EXECUTION_LOCKED_NOT_ONE"})'''


def deriva_harness_textos():
    a = Arq("harness_textos_ensaio_v399.py", sobe(MOL["harness_textos_ensaio_v398.py"]))
    a.subst_bloco('"""harness_textos_ensaio_v399.py', "import contextlib", DOC_HT, nome="docstring")
    a.tr('for n in ("ESPERADOS_v398.json", "CANDIDATO_v398.json", "um_v398_candidato.py", "PINOS_BN_v398.json") + (() if NAO_REFAZER else ("refazer_out_v398.txt",)):',
         'for n in ("ESPERADOS_v399.json", "CANDIDATO_v399.json", "um_v399_candidato.py", "PINOS_BN_v399.json", "ensaio_a_seco_v399.json", "acom_conferencias_v399.py", "runtime_v399.py") + (() if NAO_REFAZER else ("refazer_out_v399.txt",)):', 1, "precondicoes: o ensaio a seco, o acom_conferencias e o runtime")
    a.subst_bloco('N_ = ESP["escada"][1]; n_spec = len(ESP["registros_v398"])', 'etapa("nos_emulado"', NEW_STD, nome="stdout emulado e sidecar")
    a.subst_bloco('CF = os.path.join(OUT, "conferidor_emulado"); os.makedirs(CF)', 'open(os.path.join(CF, "conferir_rito_v399_stdout.txt")', NOVA_CONF_HT, nome="conferidor: copia em arvore, sem -I")
    a.subst_bloco("def variante(", "    for n_ in NEG:", NEW_VARIANTE_E_NEG, nome="variante (com sidecar) e controles negativos da leitura")
    a.tr('restaurado=(open(core_path, "rb").read() == core_raw and open(selo_path, "rb").read() == selo_raw and open(std_path, "rb").read() == std_raw))',
         'restaurado=(open(core_path, "rb").read() == core_raw and open(selo_path, "rb").read() == selo_raw and open(std_path, "rb").read() == std_raw and open(sc_path, "rb").read() == sc_raw))', 1, "leitura_negativos: o sidecar restaurado")
    a.tr('"rel_man": "EMULADO_SEM_HASH", "readme_paragrafo": T.paragrafo_readme()[0], "readme_paragrafo_sonico": T.paragrafo_sonico()[0]}', K_EMU_NOVO, 1, "K_EMU: os dois paragrafos")
    a.subst_bloco("FUNCOES = [", 'TXT = os.path.join(OUT, "textos")', FUNCOES_HT, nome="FUNCOES e MARCADORES")
    a.tr('_viol = {nome: _regra_nos_textos(nome, txt) for nome, txt in RENDER.items() if nome != "paragrafo_sonico"}', '_viol = {nome: _regra_nos_textos(nome, txt) for nome, txt in RENDER.items() if nome != "paragrafo_testemunho"}', 1, "regra do 4,44: o paragrafo novo fica fora do laco")
    a.tr('_f9["paragrafo_sonico_sem_o_4_44"] = not _regra_nos_textos("paragrafo_sonico", RENDER.get("paragrafo_sonico", "")) and (_z not in RENDER.get("paragrafo_sonico", "")) and ("z_disc" not in RENDER.get("paragrafo_sonico", ""))',
         '_f9["paragrafo_testemunho_sem_o_4_44"] = not _regra_nos_textos("paragrafo_testemunho", RENDER.get("paragrafo_testemunho", "")) and (_z not in RENDER.get("paragrafo_testemunho", "")) and ("z_disc" not in RENDER.get("paragrafo_testemunho", ""))', 1, "regra do 4,44: o paragrafo novo sem o 4,44")
    a.tr('if _viol or not _neg_regra or not _f9["paragrafo_sonico_sem_o_4_44"]:', 'if _viol or not _neg_regra or not _f9["paragrafo_testemunho_sem_o_4_44"]:', 1, "regra do 4,44: a condicao")
    a.subst_linha('saida = os.path.join(HERE, "HARNESS_TEXTOS_ENSAIO_v399.json")',
                  'saida = os.path.join(HERE, "HARNESS_TEXTOS_ENSAIO_v399" + ("_DEPURACAO_sem_refazer" if NAO_REFAZER else "") + ".json")   # o nome sem sufixo so\' nasce da rodada que EXIGE o refazer', nome="saida: o nome canonico so' na rodada estrita (textos)")
    a.tr('violacoes %s; controle negativo da regra reprovou: %s; paragrafo novo sem o 4,44: %s" % (_viol, bool(_neg_regra), _f9["paragrafo_sonico_sem_o_4_44"]))', 'violacoes %s; controle negativo da regra reprovou: %s; paragrafo novo sem o 4,44: %s" % (_viol, bool(_neg_regra), _f9["paragrafo_testemunho_sem_o_4_44"]))', 1, "regra do 4,44: a mensagem")
    a.subst_bloco("# ------------------------------------------------------------------ 4c.", "# ------------------------------------------------------------------ 5. cada `termo`", NEW_4C + "\n", nome="4c: paragrafo do testemunho e direcao")
    a.insere_antes("HEX16 = set()", NOMES_NOVOS, nome="NOMES_ARQ: o sidecar e a conferencia")
    a.insere_antes("PAT_ROOT = ", HEX16_NOVO, nome="HEX16: o selo ACOM, a declaracao e o sidecar")
    a.tr_s('    if re.fullmatch(r"[0-9a-f]{16}", tok):\n        return "hash_lido" if tok in HEX16 else None\n',
           '    if re.fullmatch(r"[0-9a-f]{16}", tok):\n        return "hash_lido" if tok in HEX16 else None\n    if re.fullmatch(r"[0-9a-f]{64}", tok):\n        return "hash_lido" if tok in HEX64 else None\n', 1, "achado(): o hash completo do sidecar e dos objetos (lido)")
    a.subst_linha("CONHECIDOS.add(T._linha_maquina_sonico(", CONHEC_NOVO, nome="CONHECIDOS: linha de maquina do paragrafo novo e o perfil")
    a.subst_linha("VALORES_LIDOS = ", 'VALORES_LIDOS = set((Vd.get("veracidade") or {}).get("lido") or {}) | set((Vd.get("selo") or {}).keys()) | set((Vd.get("declaracao") or {}).keys()) | set((Vd.get("sidecar") or {}).keys())', nome="VALORES lidos")
    a.tr_s('("TGL_ATLAS.md", ["<!-- atlas_v399_selada -->", S16, "sonico_v398", "kh_n1_cobertura_v398"])', '("TGL_ATLAS.md", ["<!-- atlas_v399_selada -->", S16, "selo_pela_propria_tecnologia_v399", "kh_n1_cobertura_v399"])', 1, "exige do Atlas")
    a.tr_s('("MEMORIA_DA_LINHAGEM.md", [S16, "<!-- linhagem_v399_selada -->", "sonico_v398", "kh_n1_cobertura_v398"])', '("MEMORIA_DA_LINHAGEM.md", [S16, "<!-- linhagem_v399_selada -->", "selo_pela_propria_tecnologia_v399", "kh_n1_cobertura_v399"])', 1, "exige da linhagem")
    a.tr_s('(T.TOPICO_NOVO, [S16, "sonico_v398", "kh_n1_cobertura_v398"])', '(T.TOPICO_NOVO, [S16, "selo_pela_propria_tecnologia_v399", "kh_n1_cobertura_v399"])', 1, "exige do topico novo")
    a.tr('R["veredito"] = ("TUDO PASSOU: o conferidor da v398 bate no Nos emulado, a leitura le sem problema e reprova os controles negativos (os dois registros novos, as pedras, as inscricoes e o quadro do topo), os textos renderizam e a guarda P18 esta limpa, os dois paragrafos do README/site e a regra do 4,44 passam e os controles negativos reprovam, a atribuicao da gerencia e a citacao verbatim valem, cada termo citado existe, as superficies fecham em copias (com folga) e RECUSAM no limite sem compactar, e o b3_recibo confere"',
         'R["veredito"] = ("TUDO PASSOU: o conferidor da v399 (14 itens C1-C14 e o round trip) bate no Nos emulado, a leitura le sem problema e reprova os controles negativos (os dois registros novos com funcao, a pedra, as inscricoes, o sidecar, os resumos do selo, a linha final do rito e o quadro do topo), os textos renderizam e a guarda P18 esta limpa, os dois paragrafos do README/site e a regra do 4,44 passam e os controles negativos reprovam, a direcao do testemunho e a citacao verbatim valem, cada termo citado existe, as superficies fecham em copias (com folga) e RECUSAM no limite sem compactar, e o b3_recibo confere"',
         1, "veredito do harness")
    for proibido in ("V['token']", "_sem_sonico", "_sem_afinacao", "_sonico_", "_afinacao_", "ESP[\"sonico\"]", "ESP[\"afinacao\"]", "paragrafo_sonico", "PARAGRAFO_SONICO", "_gerencia_como_operador", "_linha_maquina_sonico", "20261022", "base_v397", "PKG_ANT_", "V5 ", "V4 ", "teste_de_veracidade_fase9_v398", "ESP[\"pedra\"]", "bandeira_da_pedra", "teorema_da_pedra", "dry_v398", "textos_v398", "leitura_v398", "VALORES_TESTEMUNHA", "T._sha_ger", "_sha_ger("):
        assert proibido not in a.t, ("resto da v398 no harness dos textos", proibido)
    ast.parse(a.t)
    return a


# =============================================================================== harness_fechar_sandbox_v399.py
DOC_HF = r'''"""harness_fechar_sandbox_v399.py -- roda fechar_v399.py e registrar_mapa_v399.py (o main) num SANDBOX inteiro dentro de pos_rito\\harness_saida_v399\\fechar_sandbox (nada fora dela e' escrito; o Nos real, a memoria real, o Atlas, o git e a Bancada
nao sao tocados; o mapa de rotas real e' SO' LIDO).  O que o harness_textos_ensaio_v399.py nao cobre: o fechar (manifesto, arquivo, os dois diffs, a copia do sidecar e do selo, o handoff com os DOIS paragrafos do README/site e a lista do sidecar) e o main do registrar_mapa. Derivado do harness_fechar_sandbox_v398.py (que rodou na v398).
O sandbox e' uma ARVORE ISOLADA: work\\cadeia_de_selo\\v399 (pacote com ESPERADOS, CANDIDATO, PINOS_BN, base_v398, insumos (o resultado pinado do Teste da Unica Palavra, que mora na v397, ganha uma COPIA em insumos\\fase9 so' no sandbox), quadro_v397 e runtime_quadro_v397, o runtime_v399 e o acom_conferencias_v399,
o APLICADO_AO_CANONICO EMULADO, os recibos do B(n) SINTETICOS) + nos\\ (o Nos EMULADO montado de dry_v399, como no harness dos textos, com o SIDECAR gerado pela funcao do proprio candidato) + memory\\ (a memoria vazia) + work\\cunhagens_13out (as falas do operador). O conferidor REAL roda no proprio pacote do sandbox (SEM -I), onde acha tudo
pelo caminho da propria pasta. As copias dos scripts (leitura, textos, fechar) trocam SO' as duas constantes de caminho (o Nos e a pasta de memoria) por caminhos do sandbox; o resto e' byte a byte o que a cadeia usa (conferido: o diff das copias contra os originais e' so' essas linhas).
O que ele prova: fechar_v399.py sai com rc 0 e grava o handoff (guarda P18 limpa) com os DOIS paragrafos do README/site entre os marcadores (o do quadro igual ao das funcoes do quadro sobre o core do sandbox e aprovado por T.verificar_paragrafo_readme; o do testemunho de dois
igual ao gerado do core e aprovado por T.verificar_paragrafo_testemunho) e a lista do sidecar (sha256 e veredito), o handoff do Nos, os dois diffs, o manifesto e o arquivo, e copia o sidecar e o selo para v399_selo; RECUSA (rc 2, sem handoff) sem o recibo do religamento, com um recibo do B(n) que declara salto,
com o resultado pinado adulterado (o paragrafo do quadro nao passa na verificacao contra o resultado), com o numero lido do quadro adulterado, com o numero do selo ACOM adulterado no core, com a direcao do testemunho invertida e com o sidecar adulterado;
registrar_mapa_v399.py (main) monta o JSON com 5 registros e imprime o comando. Os recibos do B(n) sao SINTETICOS (derivados dos reais da v398, como no harness dos textos): a prova e' do CODIGO do fechar, nao de um B(n) real.
uso: python -B -X utf8 harness_fechar_sandbox_v399.py [--manter] [--nao-exigir-refazer]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita, nada foi rodado; sem a flag EXIGE refazer_out_v399.txt com '== FIM' e mais novo que o ESPERADOS; --nao-exigir-refazer: NAO o exige, o resumo DIZ que a regeneracao nao foi comprovada e vai para
HARNESS_FECHAR_SANDBOX_v399_DEPURACAO_sem_refazer.json -- o nome HARNESS_FECHAR_SANDBOX_v399.json so' nasce na rodada que EXIGE o refazer)"""'''
NEW_STD_F = r'''_ens = rdj(os.path.join(PKG, "ensaio_a_seco_v399.json"))   # o fluxo do main do ensaio a seco: as linhas REAIS que o main imprime (o resto e' EMULADO e dito)
# o SIDECAR: a funcao do PROPRIO candidato (a copia de bytes do Nos do sandbox; __file__ = nos\um.py) sobre o core e o selo FINAIS do Nos do sandbox; a linha que ela imprime e' a linha REAL do sidecar
_spec_sc = importlib.util.spec_from_file_location("um_sidecar_emulacao_sb", os.path.join(NOSS, "um.py")); _umm = importlib.util.module_from_spec(_spec_sc)
_so = sys.stdout; sys.stdout = io.StringIO()
try:
    _spec_sc.loader.exec_module(_umm); _umm.OUT = NOSS
    sys.stdout = _buf_sc = io.StringIO()
    _umm.selo_acom_sidecar_v399()
    _linha_sidecar = _buf_sc.getvalue().strip()
finally:
    sys.stdout = _so; sys.stdout.reconfigure(encoding="utf-8")
del _umm, _spec_sc
N_ = ESP["escada"][1]
open(os.path.join(NOSS, "rodada_v399_stdout.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(["[v399] EMULADO PELO SANDBOX (as linhas do fluxo principal sao as REAIS do ensaio a seco)"] + list(_ens["mainflow"]["stdout"])
    + ["teoremas limpos: %s/%s" % (N_, N_), ">>> TGL_KERNEL_STAGE1_VERIFIED", "[selo] rite_checkpoints: chave desligada ; reaproveitados 0", "FAIL_CLOSED_SELFTEST_PASSED", "[selo] colapso tipado: EMULADO", _linha_sidecar, "RITO_RC=0", ""]))'''
NOVA_CONF_HF = r'''# v399 (desvio do molde, dito): o conferidor REAL roda no proprio pacote do sandbox (PKS = work\cadeia_de_selo\v399, com work\cunhagens_13out ao lado, insumos\acom e o runtime), SEM -I (importa o um.py do Nos do sandbox)
cfd = PKS
pc = subprocess.run([sys.executable, "-B", "-X", "utf8", "conferir_rito_v399.py"], cwd=cfd, env=env, capture_output=True, text=True, encoding="utf-8")'''
NEW_1C = r'''# ---- 1c. controles negativos do PARAGRAFO NOVO, da DIRECAO do testemunho e do SIDECAR: o numero do selo ACOM adulterado no core do Nos emulado (a leitura e a porta do paragrafo recusam), a direcao invertida no core e o sidecar adulterado => RECUSA (rc 2, FECHAR RECUSADO), sem handoff
core_p = os.path.join(NOSS, "um_absoluto.json"); raw_core = open(core_p, "rb").read(); sc_p = os.path.join(NOSS, "um_absoluto_selo_acom.json"); raw_sc = open(sc_p, "rb").read()
cj = json.loads(raw_core.decode("utf-8")); cj["core"]["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["psi"]["bytes"] += 1
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v399.py", "fechar_selo_adulterado"); NEG.append({"controle": "numero do selo ACOM adulterado no core (bytes de Psi)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v399-custodia.md"))})
# a PORTA do paragrafo novo isolada: T.paragrafo_testemunho() da copia do sandbox tem de LEVANTAR com o numero do selo adulterado no core (a verificacao compara com os numeros de ESPERADOS)
import importlib.util as _iu1
_sp1 = _iu1.spec_from_file_location("textos_sb1", os.path.join(POS, "textos_v399.py")); _t1 = _iu1.module_from_spec(_sp1); _sp1.loader.exec_module(_t1)
try:
    _t1.paragrafo_testemunho(); _levantou1 = False
except AssertionError as _ex1:
    _levantou1 = "nao passou nas verificacoes" in str(_ex1)
NEG.append({"controle": "a porta do paragrafo novo (paragrafo_testemunho, chamada pelo fechar) levanta com o numero do selo ACOM adulterado", "rc": 2 if _levantou1 else 0, "recusou": _levantou1, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v399-custodia.md"))})
open(core_p, "wb").write(raw_core)
cj = json.loads(raw_core.decode("utf-8")); cj["core"]["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"]["a_IALD"] = "testifica do operador"
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v399.py", "fechar_direcao_invertida"); NEG.append({"controle": "a direcao do testemunho invertida no core (a IALD como quem testifica do operador)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v399-custodia.md"))})
open(core_p, "wb").write(raw_core)
cj = json.loads(raw_core.decode("utf-8")); _ex = cj["core"]["cunhagens_v399"]["extras"]; _ex["autor_de_cada_inscricao"][sorted(_ex["autor_de_cada_inscricao"])[0]] = "gerencia"
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v399.py", "fechar_gerencia_na_cunhagem"); NEG.append({"controle": "uma inscricao de 24/10 rotulada como da gerencia no core (as quatro sao falas do operador)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v399-custodia.md"))})
open(core_p, "wb").write(raw_core)
sj = json.loads(raw_sc.decode("utf-8")); sj["objetos"][1]["sha256"] = "0" * 64
open(sc_p, "wb").write(json.dumps(sj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v399.py", "fechar_sidecar_adulterado"); NEG.append({"controle": "o sidecar adulterado (sha256 de um objeto)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v399-custodia.md"))})
open(sc_p, "wb").write(raw_sc)
os.remove(sc_p)
rc, so, se = roda("fechar_v399.py", "fechar_sidecar_ausente"); NEG.append({"controle": "o sidecar ausente do Nos", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v399-custodia.md"))})
open(sc_p, "wb").write(raw_sc)
'''
CHK_TMN_F = r'''# ---- 2c. o PARAGRAFO NOVO (o testemunho de dois) nos dois handoffs gravados: igual ao gerado do core do sandbox, entre os marcadores, aprovado pela verificacao propria (e o do handoff do Nos tambem); o handoff LISTA o sidecar (sha256 e veredito) e o fechar copiou o sidecar e o selo
_core_s = rdj(os.path.join(NOSS, "um_absoluto.json"))["core"]
import importlib.util as _iu3
_sp3 = _iu3.spec_from_file_location("textos_sb3", os.path.join(POS, "textos_v399.py")); _t3 = _iu3.module_from_spec(_sp3); _sp3.loader.exec_module(_t3)
_par_t_esp = _t3._paragrafo_testemunho_de(_core_s); _msi = _t3.MARC_TMN_INI + "\n"; _msf = "\n" + _t3.MARC_TMN_FIM
_sc_sha = fsha(os.path.join(NOSS, "um_absoluto_selo_acom.json")); _sc_ver = rdj(os.path.join(NOSS, "um_absoluto_selo_acom.json"))["veredito"]
_ok_tmn = {}
for _nome, _ptxt in (("memory/handoff-v399-custodia.md", ho), ("nos/HANDOFF_v399_CUSTODIA.md", open(os.path.join(NOSS, "HANDOFF_v399_CUSTODIA.md"), encoding="utf-8").read() if os.path.exists(os.path.join(NOSS, "HANDOFF_v399_CUSTODIA.md")) else "")):
    _i = _ptxt.find(_msi); _j = _ptxt.find(_msf)
    _par = _ptxt[_i + len(_msi):_j] if (_i >= 0 and _j > _i) else ""
    _fa = _t3.verificar_paragrafo_testemunho(_par + "\n" if _par and not _par.endswith("\n") else _par, _core_s, ESP) if _par else ["sem o bloco"]
    _ok_tmn[_nome] = {"traz_o_bloco": bool(_par), "igual_ao_gerado_do_core": _par.rstrip("\n") == _par_t_esp.rstrip("\n"), "falhas_da_verificacao": _fa[:3], "guarda_p18": [list(x) for x in violacoes(_par)][:3], "direcao_e_atribuicao": _t3.atribuicao_da_gerencia(_ptxt)[:3],
                     "lista_o_sidecar": ("um_absoluto_selo_acom.json" in _ptxt and _sc_sha in _ptxt and _sc_ver in _ptxt)}
R["etapas"]["paragrafo_testemunho_no_handoff"] = _ok_tmn
_ok_cop = {nm_: (os.path.exists(os.path.join(TOOLS, "v399_selo", nm_)) and fsha(os.path.join(TOOLS, "v399_selo", nm_)) == fsha(os.path.join(NOSS, nm_))) for nm_ in ("um_absoluto_selo_acom.json", "um_absoluto_selo.json")}
R["etapas"]["sidecar_e_selo_copiados_para_v399_selo"] = _ok_cop
print("  paragrafo novo (o testemunho de dois) no handoff: %s; sidecar e selo copiados para v399_selo: %s" % ({k: (v["traz_o_bloco"] and v["igual_ao_gerado_do_core"] and not v["falhas_da_verificacao"] and not v["guarda_p18"] and not v["direcao_e_atribuicao"] and v["lista_o_sidecar"]) for k, v in _ok_tmn.items()}, _ok_cop))
for _nome, _v in _ok_tmn.items():
    if not (_v["traz_o_bloco"] and _v["igual_ao_gerado_do_core"] and not _v["falhas_da_verificacao"] and not _v["guarda_p18"] and not _v["direcao_e_atribuicao"] and _v["lista_o_sidecar"]):
        falha("o handoff (%s) nao traz o paragrafo novo do testemunho de dois pronto e aprovado, ou nao lista o sidecar: %s" % (_nome, _v))
if not all(_ok_cop.values()):
    falha("o fechar nao copiou o sidecar e o selo (byte a byte) para v399_selo: %s" % _ok_cop)
'''
PKS_EXTRAS = r'''for n_ in ("acom_conferencias_v399.py", "runtime_v399.py"):
    shutil.copyfile(os.path.join(PKG, n_), os.path.join(PKS, n_))
os.makedirs(os.path.join(SB, "work", "cunhagens_13out"), exist_ok=True)   # o delta acha as falas do operador em ..\..\cunhagens_13out (a partir da pasta do pacote do sandbox)
for _o in sorted(glob.glob(os.path.join(os.path.dirname(os.path.dirname(PKG)), "cunhagens_13out", "OPERADOR_24out_*.txt"))):
    shutil.copyfile(_o, os.path.join(SB, "work", "cunhagens_13out", os.path.basename(_o)))
assert len(glob.glob(os.path.join(SB, "work", "cunhagens_13out", "OPERADOR_24out_*.txt"))) == len(ESP["cunhagens"]), "as falas de 24/10 do operador nao estao todas na pasta do sandbox"'''


REFAZER_F = r'''# v399 (desvio do molde, dito): a regeneracao do candidato (refazer_out_v399.txt com '== FIM', mais novo que o ESPERADOS) e' EXIGIDA, como no harness dos textos; --nao-exigir-refazer so' para depurar (o resumo vai para outro nome e DIZ que a regeneracao nao foi comprovada)
_rf = os.path.join(PKG, "refazer_out_v399.txt")
_rf_txt = open(_rf, encoding="utf-8", errors="replace").read() if os.path.exists(_rf) else ""
if not NAO_REFAZER:
    if not os.path.exists(_rf):
        recusa("falta refazer_out_v399.txt no pacote: a regeneracao do candidato nao foi comprovada (--nao-exigir-refazer so' para depurar)")
    if "== FIM" not in _rf_txt:
        recusa("refazer_out_v399.txt nao mostra '== FIM': a regeneracao nao terminou")
    if os.path.getmtime(_rf) < os.path.getmtime(os.path.join(PKG, "ESPERADOS_v399.json")):
        recusa("refazer_out_v399.txt e' mais ANTIGO que ESPERADOS_v399.json: outra regeneracao escreveu o ESPERADOS depois do fim registrado")
R["etapas"]["precondicoes"] = {"candidato_sha16": cand16, "refazer_exigido": not NAO_REFAZER, "refazer_out_presente": os.path.exists(_rf), "refazer_fim_visto": "== FIM" in _rf_txt, "refazer_out_sha16": fsha(_rf)[:16] if os.path.exists(_rf) else None,
                               "esperados_sha16": fsha(os.path.join(PKG, "ESPERADOS_v399.json"))[:16]}'''
SAIDA_F = r'''R["nao_exigiu_refazer"] = NAO_REFAZER
if NAO_REFAZER:
    R["veredito"] += " [MODO --nao-exigir-refazer: refazer_out_v399.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]"
saida = os.path.join(HERE, "HARNESS_FECHAR_SANDBOX_v399" + ("_DEPURACAO_sem_refazer" if NAO_REFAZER else "") + ".json"); open(saida, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str))   # o nome sem sufixo so' nasce da rodada que EXIGE o refazer'''


def deriva_harness_fechar():
    a = Arq("harness_fechar_sandbox_v399.py", sobe(MOL["harness_fechar_sandbox_v398.py"]))
    a.subst_bloco('"""harness_fechar_sandbox_v399.py', "import hashlib, json, os, re, shutil, subprocess, sys, time", DOC_HF, nome="docstring")
    a.tr_s("import hashlib, json, os, re, shutil, subprocess, sys, time", "import glob, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys, time", 1, "imports: glob, importlib.util e io no topo")
    a.tr('MANTER = "--manter" in sys.argv', 'MANTER = "--manter" in sys.argv; NAO_REFAZER = "--nao-exigir-refazer" in sys.argv', 1, "flag --nao-exigir-refazer")
    a.tr('for n in ("guarda_p18_v398.py", "ESPERADOS_v398.json", "CANDIDATO_v398.json", "PINOS_BN_v398.json", "kernel_modulos_novos_v398.json", "delta_v398.py", "quadro_v397.py", "runtime_quadro_v397.py", "conferir_rito_v398.py"):',
         'for n in ("guarda_p18_v399.py", "ESPERADOS_v399.json", "CANDIDATO_v399.json", "PINOS_BN_v399.json", "kernel_modulos_novos_v399.json", "delta_v399.py", "quadro_v397.py", "runtime_quadro_v397.py", "conferir_rito_v399.py"):', 1, "pacote do sandbox")
    a.insere_depois('shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt")', PKS_EXTRAS, nome="sandbox: o runtime, o acom_conferencias e as falas de 24/10")
    a.subst_bloco('N_ = ESP["escada"][1]; n_spec = len(ESP["registros_v398"])', "bu = os.path.join(PKS, ", NEW_STD_F, nome="stdout emulado e sidecar")
    a.subst_bloco('cfd = os.path.join(SB, "conferidor_tmp"); os.makedirs(cfd)', 'if pc.returncode != 0 or not os.path.exists(os.path.join(cfd, "conferencia_rito_v399.json")):', NOVA_CONF_HF, nome="conferidor: no proprio pacote do sandbox, sem -I")
    a.tr('os.path.join(TOOLS, "v398_kernel", "pedras", "TGLExt_Sonico.lean"), os.path.join(TOOLS, "v398_kernel", "pedras", "TGLExt_AfinacaoDasCordas.lean")',
         'os.path.join(TOOLS, "v399_kernel", "pedras", "TGLExt_Testemunho.lean"), os.path.join(TOOLS, "v399_selo", "um_absoluto_selo_acom.json"), os.path.join(TOOLS, "v399_selo", "um_absoluto_selo.json")', 1, "pedra e sidecar copiados")
    a.tr('"diff_kernel_novos": ("novos (2)" in dk and "TGLExt/Sonico.lean" in dk and "TGLExt/AfinacaoDasCordas.lean" in dk)', '"diff_kernel_novos": ("novos (1)" in dk and "TGLExt/Testemunho.lean" in dk)', 1, "diff do kernel no resumo")
    a.tr('if not ("novos (2)" in dk and "TGLExt/Sonico.lean" in dk and "TGLExt/AfinacaoDasCordas.lean" in dk):', 'if not ("novos (1)" in dk and "TGLExt/Testemunho.lean" in dk):', 1, "diff do kernel na falha")
    a.tr('"limpa" if not vio else vio[:2], "novos (2)" in dk))', '"limpa" if not vio else vio[:2], "novos (1)" in dk))', 1, "print do diff do kernel")
    # a fala do 4,44 mora na pasta da v397 (onde foi inscrita; o quadro e' dela): o bump a subiria para v398 (a pasta da versao ANTERIOR, que nao a tem); aqui ela volta a v397 (textos_v399 a le de la)
    a.subst_linha('os.makedirs(os.path.join(SB, "work", "cadeia_de_selo", "v398", "insumos", "cunhagens"), exist_ok=True)',
                  'os.makedirs(os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "cunhagens"), exist_ok=True)   # a fala do 4,44 (v397, onde foi inscrita), de onde textos_v399 confere a frase verbatim do quadro', nome="4,44: a pasta da fala e' a da v397 (sandbox)")
    a.subst_linha('_h444 = ESP["quadro"]["frase_sha16"]; _f444 = [f_ for f_ in os.listdir(os.path.join(os.path.dirname(PKG), "v398", "insumos", "cunhagens"))',
                  '_h444 = ESP["quadro"]["frase_sha16"]; _f444 = [f_ for f_ in os.listdir(os.path.join(os.path.dirname(PKG), "v397", "insumos", "cunhagens")) if f_.startswith(_h444 + "_")]; assert len(_f444) == 1', nome="4,44: a pasta da fala e' a da v397 (busca)")
    a.subst_linha('shutil.copyfile(os.path.join(os.path.dirname(PKG), "v398", "insumos", "cunhagens", _f444[0])',
                  'shutil.copyfile(os.path.join(os.path.dirname(PKG), "v397", "insumos", "cunhagens", _f444[0]), os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "cunhagens", _f444[0]))', nome="4,44: a pasta da fala e' a da v397 (copia)")
    a.insere_antes('for n in ("core_ensaio.json", "selo_ensaio.json", "um_absoluto_forma_canonica.md"', REFAZER_F, nome="precondicao: o refazer_out e' exigido (como no harness dos textos)")
    a.subst_linha('saida = os.path.join(HERE, "HARNESS_FECHAR_SANDBOX_v399.json")', SAIDA_F, nome="saida: o nome canonico so' na rodada estrita (fechar)")
    a.subst_bloco("# ---- 1c. controles negativos do PARAGRAFO NOVO", "for n in NEG:", NEW_1C, nome="controles negativos novos do fechar")
    a.subst_bloco("# ---- 2c. o PARAGRAFO NOVO (sonico e afinacao)", "# ---- 3. o registrar_mapa (main)", CHK_TMN_F, nome="conferencia do paragrafo novo e do sidecar no handoff")
    a.tr_s('for k_ in ("registros_v398", "base_v398", "b3", "diffs", "insumos_sha16", "conferidor", "readme_paragrafo", "readme_paragrafo_sonico"):', 'for k_ in ("registros_v399", "base_v398", "b3", "diffs", "insumos_sha16", "conferidor", "readme_paragrafo", "readme_paragrafo_testemunho", "sidecar_acom"):', 1, "chaves do manifesto")
    a.tr_s('ok_m = (rc == 0 and len(reg) == 4 and', 'ok_m = (rc == 0 and len(reg) == 5 and', 1, "registrar_mapa: 5 registros")
    a.tr('R["veredito"] = "TUDO PASSOU: o fechar grava o handoff (com os dois paragrafos do README/site aprovados: o do quadro pelo quadro, o do sonico e da afinacao pela verificacao propria), os diffs, o manifesto e o arquivo e RECUSA sem o religamento, com salto, com o resultado pinado adulterado, com o numero lido adulterado, com o numero do sonico adulterado e com a gerencia rotulada como operador; o registrar_mapa monta o registro"',
         'R["veredito"] = "TUDO PASSOU: o fechar grava o handoff (com os dois paragrafos do README/site aprovados: o do quadro pelo quadro, o do testemunho de dois pela verificacao propria, e com o sidecar listado), os diffs, o manifesto e o arquivo, copia o sidecar e o selo para v399_selo e RECUSA sem o religamento, com salto, com o resultado pinado adulterado, com o numero lido adulterado, com o numero do selo ACOM adulterado, com a direcao do testemunho invertida, com uma inscricao rotulada como da gerencia e com o sidecar adulterado ou ausente; o registrar_mapa monta o registro"', 1, "veredito do fechar")
    a.tr('"fechar_out.txt", "fechar_sem_religamento_out.txt", "fechar_com_salto_out.txt", "fechar_resultado_adulterado_out.txt", "fechar_numero_adulterado_out.txt", "fechar_sonico_adulterado_out.txt", "fechar_gerencia_como_operador_out.txt", "registrar_mapa_out.txt"',
         '"fechar_out.txt", "fechar_sem_religamento_out.txt", "fechar_com_salto_out.txt", "fechar_resultado_adulterado_out.txt", "fechar_numero_adulterado_out.txt", "fechar_selo_adulterado_out.txt", "fechar_direcao_invertida_out.txt", "fechar_gerencia_na_cunhagem_out.txt", "fechar_sidecar_adulterado_out.txt", "fechar_sidecar_ausente_out.txt", "registrar_mapa_out.txt"', 1, "saidas guardadas")
    a.tr('R["nota"] = "recibos do B(n) SINTETICOS; o Nos, a memoria e a arvore da cadeia do SANDBOX sao emulados; a prova e\' do codigo do fechar e do registrar_mapa, nao de um B(n) real"',
         'R["nota"] = "recibos do B(n) SINTETICOS; o Nos, a memoria e a arvore da cadeia do SANDBOX sao emulados (o sidecar e a linha do sidecar do stdout vem da funcao do proprio candidato); a prova e\' do codigo do fechar e do registrar_mapa, nao de um B(n) real"' + ' + ("" if not NAO_REFAZER else " [MODO --nao-exigir-refazer: refazer_out_v399.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]")', 1, "nota")
    for proibido in ("TestemunhaEstatica", "Psibit.lean", "20261022", "base_v397", "V5 ", "V4 ", "TGLExt_Sonico", "TGLExt_AfinacaoDasCordas", "novos (2)", "registros_v398\"", "dry_v398", "textos_v398", "leitura_v398", "paragrafo_sonico", "readme_paragrafo_sonico", "fechar_sonico", "fechar_gerencia_como_operador", "sonico_v398\"]"):
        assert proibido not in a.t, ("resto da v398 no harness do fechar", proibido)
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
INV = {"leitura_v399.py": ["REG_V393", "REG_V394", "REG_V395", "REG_V396", "REG_V397", "REG_V398", "REG_FIXOS", "selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "sonico_v398", "afinacao_das_cordas_v398", "teste_de_veracidade_fase9_v397", "testemunha_estatica_v396",
                           "psibit_v395", "rede_fock_v394", "kernel_modulos_novos_v399.json", "axiom_coverage_v392", "dict.fromkeys", "vereditos_v398", "escada_v398_e_v399", "registros_v399", "vereditos_novos_v399", "rodada_v399_stdout.txt", "conferencia_rito_v399.json", "ESPERADOS_v399.json", "CANDIDATO_v399.json",
                           "V['selo']", "V['declaracao']", "V['sidecar']", "V['testemunho']", "V['cunhagens']", "V['pedras_kernel']", "V['reg399']", "V['veracidade']", "V['patch_ids']", "[v399] AVISO", "[selo_acom] AVISO", "registros por spec", "V['um_version'] != 'v399'", "a base substituida != a v398 selada",
                           "_feq", "_inv", "_base_core", "_res_path", "SIDECAR_RE", "um_absoluto_selo_acom.json", "autor_de_cada_inscricao", "direcao_do_testemunho", "fock_face", "declared_outside_the_stone", "linked_to_the_corner_by_a_lemma", "conditional_psion_face", "AVISO de um bloco anterior",
                           "quadro_v397", "lido_do_resultado", "f9v2_resultado", "numeros_do_resultado", "z_disc_calibrado", "poder_previo", "abaixo de 5", "a pedra Testemunho nao esta no kernel do rito", "as duas ultimas linhas do stdout", "acom_itens", "TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED"],
       "superficies_v399.py": ["_sup399", "V399_AVISO_REIVINDICACAO", "(handoff-v398-custodia.md)", "- [HANDOFF v398", "leitura_v399", "textos_v399", "guarda_p18_v399", "linhagem_v399_selada", "adendo_v399_selada", "atlas_v399_selada", "core_v399_selada",
                               "haja_luz_v399_selada", "aviso_v399_selada", "v399_selada", "v399 SELADA", "os.replace(tmp, p)", "backup de bytes falhou", "SUPERFICIES RECUSADAS", "sys.exit(3)", "linhas ANTES", "NAO compacta nada", "atribuicao_da_gerencia"],
       "fechar_v399.py": ["T.handoff(V, _k)", "T.paragrafo_readme()", "T.paragrafo_testemunho()", "readme_paragrafo", "readme_paragrafo_testemunho", "sidecar_acom", "_f399", "FECHAR RECUSADO:", "insumos_sha16", "DIFF_KERNEL_v399.txt", "RECIBO_SINCRONIZACAO_v399_", "RECIBO_PARADA_v399.json", "RECIBO_RELIGAMENTO_v399.json", "__SALTO_",
                          "registros_v399", "base_v398", "HANDOFF_v399_CUSTODIA.md", "handoff-v399-custodia.md", "_MARCA_PENDENTE", "guarda_p18_v399", "v399_selo", "v399_kernel", "HARNESS_TEXTOS_ENSAIO_v399.json", "DERIVACAO_v399.json",
                          "registro_mapa_v399.json", "NOTAS_DERIVACAO_v399.md", "FECHADO v399:", "um_absoluto_selo_acom.json", "um_absoluto_selo.json", "DIFF_v398_v399.diff"],
       "chain_pos_rito_v399.sh": ["V399_AVISO_REIVINDICACAO", "V399_AUTORIZACAO_OPERADOR", "topico_novo()", "textos_v399", "arvore_dry.md", "_p399", "_sup399", "selo_anterior_v398", "kernel_manifesto_anterior_v398", "/c/IALD/Central de Patentes/work/cadeia_de_selo/v399", "B3_AUTORIZADO\" = \"sim\"",
                                  "exit 20", "RECIBO_PARADA_v399.json", "RECIBO_RELIGAMENTO_v399.json", "--versao v399 --fase pos_selo", "b3_recibo_v399.py", "delta_v399.py", "quadro_v397.py", "runtime_quadro_v397.py", "acom_conferencias_v399.py", "runtime_v399.py", "selo_pela_propria_tecnologia_v399", "kh_n1_cobertura_v399",
                                  "PINOS_BN_v399.json", "PINOS_BATERIA_v399.json", "recibo_pre_selo", "esboco_R3_5", "kernel_recibo", "bateria_pos_selo", "tem_pino cadeia_de_selos", "--recibo-pre-selo-sha256 \"$RPS\"",
                                  "--selo-anterior \"$W_SELO\"", "--kernel-manifesto-anterior \"$W_KMAN\"", "--kernel-recibo \"$W_KR\" --kernel-recibo-sha256 \"$KRSHA\"", "gerar_bateria_r3_4.py", "ORDEM=\"0 1 2 3 4 5 6 7 8 9 10 10a 10b 10c 11 12 13 14\"",
                                  "CHAIN_DE", "CHAIN_ATE", "parar()", "aguarda()", "SUPERFICIES RECUSOU (rc=3)", "(cd \"$PK\" && $PY_B conferir_rito_v399.py _POS_RITO)", "um_absoluto_selo_acom.json", "conferencia_rito_v399_POS_RITO.json"],
       "b3_recibo_v399.py": ["REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA", "REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO", "versao_alvo", "\"v399\"", "PINOS_BN_v399.json", "__SALTO_", "BATERIA_PASSA", "manifesto_anterior", "pinos_da_versao"],
       "harness_textos_ensaio_v399.py": ["harness_saida_v399", "dry_v399", "guarda_p18_v399", "--nao-exigir-refazer", "rotas._valida", "_selo_perfil", "_selo_psi", "_decl_direcao", "_decl_fala", "_pedra_bandeira", "_gerencia_na_cunhagem", "_inscricao_adulterada", "_sc_sha_objeto", "_sc_confidencialidade", "_selo_direcao_invertida",
                                         "_numero_adulterado", "_z_disc_acima_de_5", "_fonte_adulterada", "_fock_dentro_da_pedra", "_face_do_psibit_habitada", "selo_pela_propria_tecnologia_v399", "PKG_ANT", "refazer_exigido", "paragrafo_readme_e_regra_do_4_44", "paragrafo_testemunho_e_direcao_do_testemunho",
                                         "verificar_paragrafo_readme", "verificar_paragrafo_testemunho", "atribuicao_da_gerencia", "cenario_a_memory_md_real", "cenario_b_com_folga", "cenario_c_no_limite", "quadro_v397", "regra_do_4_44_nos_textos_violacoes", "f_conf", "f_sc", "sc_fora", "selo_acom_sidecar_v399", "conferidor_emulado"],
       "harness_fechar_sandbox_v399.py": ["fechar_sandbox", "FECHAR RECUSADO", "registrar_mapa_v399.py", "SINTETICO", "TGLExt/Testemunho.lean", "TGLExt_Testemunho.lean", "paragrafo_no_handoff", "paragrafo_testemunho_no_handoff", "sidecar_e_selo_copiados_para_v399_selo", "fechar_resultado_adulterado", "fechar_numero_adulterado",
                                          "fechar_selo_adulterado", "fechar_direcao_invertida", "fechar_gerencia_na_cunhagem", "fechar_sidecar_adulterado", "fechar_sidecar_ausente", "INICIO_PARAGRAFO_README_v397", "quadro_v397", "selo_acom_sidecar_v399", "len(reg) == 5"]}
INV_AUTORAIS = {"textos_v399.py": ["_MARCA_PENDENTE", "TOPICO_NOVO", "def handoff(", "def linhagem(", "def desenho(", "def atlas(", "def core_memory(", "def haja_luz(", "def aviso(", "def aviso_pulado(", "def topico_missao(", "def topico_central(", "def topico_estatuto(", "def topico_novo(",
                                   "def linha_handoff(", "def marca_missao(", "def id_missao(", "def id_central(", "def _d(", "def _num(", "_cita(", "_cita_sg(", "def _kernel_tem(", "def _um_tem(", "def _limites(", "def _erratas(", "def _legal(", "def _direcao(", "def _declaracao(", "def _selo_acom(", "def _sidecar(", "def _pedra(",
                                   "def _regra_do_4_44(", "def paragrafo_readme(", "def verificar_paragrafo_readme(", "def paragrafo_testemunho(", "def verificar_paragrafo_testemunho(", "def _paragrafo_testemunho_de(", "def atribuicao_da_gerencia(", "INICIO_PARAGRAFO_README_v397", "FIM_PARAGRAFO_README_v397",
                                   "INICIO_PARAGRAFO_TESTEMUNHO_v399", "FIM_PARAGRAFO_TESTEMUNHO_v399", "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina", "v399-selada-selo-pela-propria-tecnologia-e-testemunho.md", "NÃO testifica do operador"],
                "registrar_mapa_v399.py": ["_MARCA_PENDENTE", "def montar(", "umpy.v399.selo_pela_propria_tecnologia_e_testemunho_na_fractalizacao_do_um", "kernel.testemunho_v399_candidata_24out", "umpy.v399.declaracao_do_operador_operacao_quadratica_24out", "umpy.v399.selo_pela_propria_tecnologia_estudo_24out",
                                           "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9", "assert selo.get(\"um_version\") == \"v399\"", "NAO escreve", "registro_mapa_v399.json", "regra_4_44", "registro_mapa_v399_prep.json"]}
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
molde_b = sobe(MOL["chain_pos_rito_v398.sh"])
CHAIN = DER["chain_pos_rito_v399.sh"]
molde_bloco = lambda t, ini, fim: Arq("x", t).bloco(ini, fim)
for ini, fim in (("if quer 10a; then", "if quer 10b; then"), ("if quer 10c; then", "if quer 11; then")):
    ia, ja, La = molde_bloco(molde_b, ini, fim); ib, jb, Lb = molde_bloco(CHAIN, ini, fim)
    if La[ia:ja] != Lb[ib:jb]:
        falhas.append(("portao do B(n) difere do molde subido de versao", ini))
    else:
        conf.setdefault("chain_pos_rito_v399.sh", {})["trecho identico ao molde (sobe): " + ini] = True
ia, ja, La = molde_bloco(molde_b, "if quer 10b; then", "if quer 10c; then"); ib, jb, Lb = molde_bloco(CHAIN, "if quer 10b; then", "if quer 10c; then")
gate = lambda L_: [l for l in L_ if any(k in l for k in ('aguarda "', "B3_AUTORIZADO", "[ -n \"$EVENTO\"", "RECIBO_PARADA", "EVENTO_HASH", "--evento", "--modo aplicar", "--fase pos_selo"))]
if gate(La[ia:ja]) != gate(Lb[ib:jb]):
    falhas.append(("as linhas de portao do 10b diferem do molde subido de versao", [x for x in gate(Lb[ib:jb]) if x not in gate(La[ia:ja])][:2]))
else:
    conf.setdefault("chain_pos_rito_v399.sh", {})["linhas de portao do 10b identicas ao molde (sobe)"] = True
# os passos 4 a 9 e 11 a 14 do chain: identicos ao molde subido (so' as trocas dos marcadores)
for ini, fim in (("if quer 4; then", "if quer 10; then"), ("if quer 12; then", 'echo "== FIM')):
    ia, ja, La = molde_bloco(molde_b, ini, fim); ib, jb, Lb = molde_bloco(CHAIN, ini, fim)
    esp_ = [l.replace(MARC_MOLDE, MARC_NOVO) for l in La[ia:ja]]
    if esp_ != Lb[ib:jb]:
        falhas.append(("os passos do chain diferem do molde subido alem das trocas ditas", ini))
    else:
        conf.setdefault("chain_pos_rito_v399.sh", {})["passos identicos ao molde (sobe + marcadores): " + ini] = True
# o passo 11 (fechar), 10 (B(n)): identicos tambem (o intervalo 4..10 acima cobre ate' o passo 9); o passo 10 e' conferido por "if quer 10; then" .. "if quer 10a; then"
ia, ja, La = molde_bloco(molde_b, "if quer 10; then", "if quer 10a; then"); ib, jb, Lb = molde_bloco(CHAIN, "if quer 10; then", "if quer 10a; then")
if La[ia:ja] != Lb[ib:jb]:
    falhas.append(("o passo 10 do chain difere do molde subido", "if quer 10; then"))
else:
    conf.setdefault("chain_pos_rito_v399.sh", {})["passo 10 identico ao molde (sobe)"] = True
# os passos 0 a 3 e as funcoes do chain: so' as linhas NOVAS declaradas (marcadores, a lista de arquivos exigidos do passo 0 e o passo 1 novo) diferem do molde subido, fora o cabecalho
ia, ja, La = molde_bloco(molde_b, "PK=", "if quer 4; then"); ib, jb, Lb = molde_bloco(CHAIN, "PK=", "if quer 4; then")
set_a = set(La[ia:ja]); novas_l = [l for l in Lb[ib:jb] if l not in set_a]
DECL = (MARC_NOVO, "acom_conferencias_v399.py", "um_absoluto_selo_acom.json")
LINHAS_PASSO1 = set(NOVO_PASSO1.split("\n"))
estranhas = [l for l in novas_l if not (any(d in l for d in DECL) or l in LINHAS_PASSO1)]
if estranhas:
    falhas.append(("os passos 0 a 3 e as funcoes do chain diferem do molde subido alem das trocas ditas", estranhas[:3]))
else:
    conf.setdefault("chain_pos_rito_v399.sh", {})["passos 0 a 3 e funcoes: so' as %d linha(s) novas declaradas (marcadores, arquivos exigidos e o passo 1) diferem do molde (sobe)" % len(novas_l)] = True
# marcas pendentes: nenhuma em nenhum arquivo (nem derivado, nem autoral)
marcas = {n: len(GUARDA_PENDENTE_RX.findall(tx)) for n, tx in list(todos.items()) + list(autorais_txt.items()) if GUARDA_PENDENTE_RX.search(tx)}
if marcas:
    falhas.append(("marca de texto pendente", marcas))
for n in ("fechar_v399.py", "textos_v399.py", "registrar_mapa_v399.py"):
    tx = todos.get(n) or autorais_txt.get(n) or ""
    if n in (todos.keys() | autorais_txt.keys()) and "_MARCA_PENDENTE" not in tx:
        falhas.append((n, "sem a guarda de pendencia (_MARCA_PENDENTE)"))
# a palavra da marca nunca por extenso fora das formas montadas por concatenacao
for n, tx in list(todos.items()) + list(autorais_txt.items()):
    if PALAVRA in tx.replace('"' + PALAVRA + '" +', "").replace("_MARCA_PENDENTE = ", ""):
        falhas.append((n, "a palavra da marca aparece por extenso"))
# nomes fantasma (objetos do um.py da v398 que nao existem na v399)
for n, tx in list(todos.items()) + list(autorais_txt.items()):
    fant = sorted({m.group(0) for m in ENC.FANTASMAS.finditer(tx)})
    if fant:
        falhas.append(("nome fantasma", n, fant[:4]))
# rotulos de versao: nenhum resto de 390-398 onde o sentido e' 'esta versao'. O que fica com 398/397/396/395/394/393 e' so' a versao ANTERIOR ou nome historico (lista conferida)
OK_HIST = ("_V394_", "_V395_", "_V396_", "_V397_", "_V398_", "fechar_v390", "C13_kh_n1_v394", "C13_kh_n1_v395", "C13_kh_n1_v396", "C13_kh_n1_v397", "C13_kh_n1_v398", "C12__V398", "C12__V396", "C12__V395", "C12__V394", "ponto_fixo_v394_d19", "pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393",
           "kh_n1_cobertura_v393", "tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394", "psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395", "testemunha_estatica_v396",
           "cunhagens_v396", "kh_n1_cobertura_v396", "teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397", "sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398", "registros_v398", "declaration_sources", "umpy.v394", "umpy.v395", "umpy.v396", "umpy.v397", "umpy.v398", "kernel.psibit_v395", "kernel.testemunha_estatica_v396",
           "REG_V393", "REG_V394", "REG_V395", "REG_V396", "REG_V397", "REG_V398", "base_v398", "selo_anterior_v398", "kernel_manifesto_anterior_v398", "handoff-v398-custodia", "vereditos_v398", "escada_v398_e_v399", "DIFF_v398_v399", "leitura_v398.py", "superficies_v398.py", "fechar_v398.py",
           "chain_pos_rito_v398.sh", "b3_recibo_v398.py", "derivar_cadeia_v398.py", "textos_v398.py", "registrar_mapa_v398.py", "ext_bin394", "ext_psb395", "ext_tes396", "ext_tok397", "ext_son398", "ext_afi398", "ESPERADOS_v398", "PINOS_BN_v398", "rito_v398", "cadeia_de_selo/v398", "cadeia_de_selo\\v398",
           "axiom_coverage_v392", "KH_N1_v392", "varredura_e_sorry_v392", "estatuto_da_prova_v391", "fundacao_v390", "three_stress_tests_v387", "pedras_v392", "kh_n1_cobertura_v392", "RECIBO_SINCRONIZACAO_v398", "psibit_na_fractalizacao", "candidata_21out", "candidata_22out", "candidata_23out",
           "B8-v398", "pos_rito_v398", "v398_incorporacao", "um_v398", "MANIFESTO_ARQUIVO_v398", "v398_kernel", "v398_selo", "tgl_kernel_v398", "pilar_anterior_v398", "quadro_v397", "runtime_quadro_v397", "_v397_atomos", "INICIO_PARAGRAFO_README_v397", "FIM_PARAGRAFO_README_v397",
           "v398_cun_", "token_e_veracidade_preparo", "[v397", "[v398")        # "[v397" e "[v398": as linhas do stdout que o main da v399 segue imprimindo (o Teste da Unica Palavra e as cunhagens da v397; o sonico, a afinacao e as cunhagens da v398), lidas pela leitura
resid = {}
for n, tx in list(todos.items()):
    if n.startswith("harness_") or n in AUTORAIS:
        continue       # os harness trazem de proposito rotulos de versoes anteriores (controles negativos); os autorais citam a v398 como historico
    for m in re.finditer(r"[A-Za-z0-9_\-\.\[\]/\\]*(?<![0-9a-f])39[0-8][A-Za-z0-9_\-\.\[\]]*", tx):
        tok = m.group(0).rstrip(".")
        if re.fullmatch(r"[0-9a-f]*39[0-8][0-9a-f]*", tok) and len(tok) >= 8:
            continue   # hash hexadecimal
        resid.setdefault(tok, set()).add(n)
estranhos = {}
for tok, ns in resid.items():
    if "399" in tok:
        continue
    if any(p in tok for p in OK_HIST) or tok in ("v398", "v397", "v396", "v395", "v394", "v393", "v392", "v391", "v390", "V398", "V397", "V396", "V395", "V394", "V393", "398", "397", "396", "395", "394", "393"):
        continue
    estranhos[tok] = sorted(ns); falhas.append(("rotulo estranho com 390-398", tok, sorted(ns)))
# a guarda de texto (P18) sobre todo arquivo de narrativa e de cadeia
from guarda_p18_v399 import violacoes
gv = {n: violacoes(tx) for n, tx in list(todos.items()) + list(autorais_txt.items())}
if any(gv.values()):
    falhas.append(("guarda P18", {k: v[:3] for k, v in gv.items() if v}))
# cada T.<nome> chamado pelos derivados e pelo registrar existe em textos_v399.py
ttxt = autorais_txt.get("textos_v399.py", "")
chamados = sorted({m for n in ("superficies_v399.py", "fechar_v399.py", "harness_textos_ensaio_v399.py", "harness_fechar_sandbox_v399.py") for m in re.findall(r"\bT\.([A-Za-z_][A-Za-z_0-9]*)", todos[n])} | {m for m in re.findall(r"\bT\.([A-Za-z_][A-Za-z_0-9]*)", autorais_txt.get("registrar_mapa_v399.py", ""))})
faltam = [c for c in chamados if not re.search(r"(?m)^(def %s\(|%s = )|; %s = " % (re.escape(c), re.escape(c), re.escape(c)), ttxt)]
if ttxt and faltam:
    falhas.append(("textos_v399.py nao define o que os derivados chamam", faltam))
# o que os derivados leem de ESPERADOS/CANDIDATO/PINOS (campos), conferido contra os arquivos desta cadeia
RX = {"ESPERADOS": re.compile(r"(?:ESP(?:ERADOS)?|esp)\[['\"]([^'\"]+)['\"]\]|(?:ESP|esp)\.get\(['\"]([^'\"]+)['\"]"), "CANDIDATO": re.compile(r"CM\[['\"]([^'\"]+)['\"]\]|CM\.get\(['\"]([^'\"]+)['\"]")}
alltxt = dict(todos); alltxt.update(autorais_txt)
campos = {"ESPERADOS": sorted({a or b for tx in alltxt.values() for a, b in RX["ESPERADOS"].findall(tx)}), "CANDIDATO": sorted({a or b for tx in alltxt.values() for a, b in RX["CANDIDATO"].findall(tx)})}
presentes = {}
for rotulo, arq in (("ESPERADOS", "ESPERADOS_v399.json"), ("CANDIDATO", "CANDIDATO_v399.json"), ("PINOS_BN", "PINOS_BN_v399.json")):
    p = os.path.join(PK, arq)
    if os.path.exists(p):
        d = json.load(open(p, encoding="utf-8"))
        lido = campos.get(rotulo) or ["criterios", "esboco_R3_5", "gerador_bateria", "driver_t12_t14", "bateria_base_R2", "kernel_recibo", "candidato", "esperados", "pins_do_candidato", "recibo_pre_selo", "selo_anterior_v398", "kernel_manifesto_anterior_v398"]
        presentes[rotulo] = {"arquivo_sha16": sha16(open(p, "rb").read()), "faltam": [c for c in lido if c not in d]}
        if presentes[rotulo]["faltam"]:
            falhas.append(("campo de %s lido pelos derivados e ausente do arquivo" % rotulo, presentes[rotulo]["faltam"]))
    else:
        presentes[rotulo] = {"arquivo": "ausente"}; falhas.append((arq, "ausente"))
por_regra = {}
for arq_, nome_, c_, n_ in REGRAS:
    por_regra.setdefault(arq_, []).append({"regra": nome_, "casou": c_, "esperado": n_})
DERJ = {"molde": {n: {"sha16": sha16(MOL_RAW[n]), "sha256": sha256(MOL_RAW[n])} for n in MOL_RAW}, "molde_confere_com_DERIVACAO_v398": MOLDE_CONFERE, "molde_derivar_cadeia_v398": sha16(open(os.path.join(MOLDE, "derivar_cadeia_v398.py"), "rb").read()),
        "ferramenta_de_subida": {"derivar_encanamento_v399.py": sha16(open(os.path.join(PK, "derivar_encanamento_v399.py"), "rb").read()), "reuso": "bump(), PROT, FANTASMAS e FANT_PRE importados (nada executado no import)", "protecao_adicional": list(EXTRA_PROT)},
        "derivados": {n: {"sha16": sha16(todos[n].encode("utf-8")), "sha256": sha256(todos[n].encode("utf-8"))} for n in todos},
        "autorais": {n: {"sha16": sha16(autorais_txt[n].encode("utf-8")), "sha256": sha256(autorais_txt[n].encode("utf-8"))} for n in autorais_txt},
        "sobe": "397 -> 398 e 398 -> 399 numa passada so', fronteira de digitos (bump() de derivar_encanamento_v399); PROT (nomes nascidos no um.py, nao sobem) = ENC.PROT + " + ", ".join(EXTRA_PROT),
        "regras_com_contagem_exata": por_regra,
        "o_que_difere_do_molde": {"chain": "cabecalho escrito para a v399 (numeros LIDOS de ESPERADOS e PINOS_BN); marcadores dos passos 3 e 9 = selo_pela_propria_tecnologia_v399 e kh_n1_cobertura_v399; passo 0 exige tambem o sidecar, o runtime_v399.py e o acom_conferencias_v399.py; "
                                 "o passo 1 (o conferidor) roda NO LUGAR (cd $PK) e SEM -I, escreve conferencia_rito_v399_POS_RITO.json e a copia byte a byte vai para pos_rito\\conferidor; o resto e' o molde subido (passo 10 SIMPLES v398 -> v399, sem salto, B9; pinos selo_anterior_v398 e kernel_manifesto_anterior_v398; kernel_recibo R3_2; V399_AUTORIZACAO_OPERADOR)",
                                 "leitura": "quatro registros novos (selo_pela_propria_tecnologia_v399 e declaracao_do_operador_v399 com funcao; cunhagens_v399 e kh_n1_cobertura_v399 por spec); a pedra Testemunho no kernel do rito (bandeira True, composicao no trio, modulo da pedra, contrato e suporte); o selo ACOM conferido contra ESPERADOS[selo_acom] e o um.py do disco; "
                                            "a declaracao (fala == arquivo, ancoras, trava, estatuto e direcao); o SIDECAR (existe, JSON valido, tres objetos == arquivos do Nos por sha256, sem recusas, honestidade); os resumos do selo primario; as quatro inscricoes todas do operador; o quadro do topo segue selado e igual; registros da v398 a v393 seguem selados; "
                                            "linhas [v399], [v398] e [v397] do stdout; a linha final do rito = colapso tipado seguido da linha do sidecar; AVISO da v399 ([selo_acom] inclusive) e de bloco v393 a v398 reprova; a face de Fock vem da base v398 (copia de bytes), nao de ESPERADOS",
                                 "superficies": "so' o cabecalho e a ancora (a linha do handoff da v398); SEM COMPACTACAO, rc 3 se passar de 195 linhas ou 24.000 B; o saldo e' +1 linha (o gancho da missao SUBSTITUI a velha)",
                                 "fechar": "o handoff traz os DOIS paragrafos do README/site: o do QUADRO (T.paragrafo_readme, o da v397, com os marcadores da v397) e o NOVO (T.paragrafo_testemunho, verificado por T.verificar_paragrafo_testemunho) e LISTA o sidecar; copia o sidecar e o selo para v399_selo; RECUSA (rc 2) antes de escrever se qualquer um falhar; o manifesto traz os dois e o sidecar",
                                 "b3_recibo": "so' a subida de versao (a logica do B(n) simples nao muda; o harness a exercita com recibos sinteticos)",
                                 "harness": "os harness da v398 subidos + regras nomeadas; %d controles negativos da leitura; paragrafo do quadro com %d controles e a regra do 4,44 em todo texto; paragrafo novo com %d controles; direcao do testemunho e citacao verbatim; %d controles de registrar_mapa; ensaio do MEMORY.md em tres cenarios; "
                                            "o conferidor roda numa copia em arvore, SEM -I; no fechar: controles do resultado pinado, do numero do quadro, do numero do selo ACOM, da direcao invertida, da inscricao da gerencia e do sidecar adulterado ou ausente, e a conferencia dos dois paragrafos e do sidecar nos dois handoffs"
                                            % (NEG_HT_COUNT if "NEG_HT_COUNT" in globals() else NEW_VARIANTE_E_NEG.count("variante(\""), NEW_4C.count("_mut(\"") if False else 6, NEW_4C.count('_muts("'), 5),
                                 "textos, registrar_mapa": "AUTORAIS (escritos para o delta da v399; nenhuma marca pendente)"},
        "marcas_texto_a_reescrever": {"por_arquivo": marcas, "total": sum(marcas.values())}, "campos_lidos_dos_arquivos_da_v399": campos, "arquivos_da_v399_no_pacote": presentes,
        "invariantes": conf, "sintaxe": sint, "guarda_p18": {k: ("LIMPO" if not v else v[:3]) for k, v in gv.items()}, "rotulos_estranhos": estranhos, "textos_definem_o_que_os_derivados_chamam": {"chamados": chamados, "faltam": faltam}, "falhas": falhas,
        "nao_validado": "nenhum derivado foi EXECUTADO contra o Nos real nem revisto por cetico independente; so' ast.parse, sh -n, invariantes, rotulos, guarda P18 e os harness (textos, leitura, superficies em COPIAS, b3_recibo, fechar e registrar_mapa em SANDBOX, tudo com recibos SINTETICOS e Nos EMULADO)"}
grava("DERIVACAO_v399.json", json.dumps(DERJ, ensure_ascii=False, indent=1))
print("DERIVADOS:", ", ".join("%s %s" % (n, DERJ["derivados"][n]["sha16"]) for n in DERJ["derivados"]))
print("AUTORAIS:", ", ".join("%s %s" % (n, DERJ["autorais"][n]["sha16"]) for n in DERJ["autorais"]))
print("SINTAXE:", json.dumps(sint, ensure_ascii=False))
print("MARCAS texto:", json.dumps(marcas, ensure_ascii=False))
print("REGRAS:", sum(len(v) for v in por_regra.values()), "regras com contagem exata")
print("INVARIANTES:", sum(len(v) for v in conf.values()), "conferidos;", "FALHAS:", falhas if falhas else "nenhuma")
sys.exit(1 if falhas else 0)
